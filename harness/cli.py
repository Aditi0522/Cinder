"""JSONL in and JSONL out; generation machines do not need Lean installed."""

import argparse
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from harness.manifest import RunManifest
from harness.schema import Problem, Sample
from harness.verifier import ROOT, LeanVerifier, VerifierConfig


def read_jsonl(path: Path) -> list[dict]:
    records = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.strip():
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as error:
                raise ValueError(f"{path}:{number}: {error}") from error
    return records


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=ROOT / "configs/verifier.toml")
    parser.add_argument("--problems", type=Path, required=True)
    parser.add_argument("--samples", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, help="Defaults to OUTPUT.manifest.json")
    parser.add_argument(
        "--benchmark-manifest",
        type=Path,
        help="Benchmark manifest; required for miniF2F problems",
    )
    parser.add_argument(
        "--allow-test",
        action="store_true",
        help="Permit problems from a benchmark's locked test split",
    )
    args = parser.parse_args()
    try:
        config = VerifierConfig.load(args.config)
        problems = {}
        for record in read_jsonl(args.problems):
            problem = Problem(**record)
            if problem.problem_id in problems:
                raise ValueError(f"Duplicate problem id: {problem.problem_id}")
            problems[problem.problem_id] = problem
        if any(pid.startswith("minif2f.") for pid in problems) and not args.benchmark_manifest:
            raise ValueError("minif2f problems require --benchmark-manifest")
        if args.benchmark_manifest:
            from harness.benchmarks.minif2f import check_problems

            check_problems(args.benchmark_manifest, list(problems.values()), args.allow_test)
        samples = [Sample.from_record(record) for record in read_jsonl(args.samples)]
        seen = set()
        for sample in samples:
            if sample.problem_id not in problems:
                raise ValueError(f"Unknown problem id: {sample.problem_id}")
            key = (sample.model, sample.problem_id, sample.sample_id)
            if key in seen:
                raise ValueError(f"Duplicate sample: {key}")
            seen.add(key)
        verifier = LeanVerifier(config)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        infrastructure_failure = False
        manifest_path = args.manifest or args.output.with_suffix(".manifest.json")
        if manifest_path.exists() or args.output.exists():
            raise FileExistsError("Result or manifest file already exists")
        if manifest_path.resolve() == args.output.resolve():
            raise ValueError("Manifest and results must use different files")
        # Exclusive creation prevents accidentally overwriting an experiment.
        with (
            args.output.open("x", encoding="utf-8") as output,
            ThreadPoolExecutor(max_workers=config.worker_count) as pool,
        ):
            manifest = RunManifest(
                manifest_path,
                verifier,
                {"problems": args.problems, "samples": args.samples},
                args.output,
            )
            status = "interrupted"
            try:

                def verify(sample: Sample):
                    return verifier.verify(problems[sample.problem_id], sample)

                for result in pool.map(verify, samples):
                    result.run_id = manifest.record["run_id"]
                    output.write(result.to_json() + "\n")
                    output.flush()
                    manifest.counts[result.verdict] += 1
                    infrastructure_failure |= result.verdict == "infrastructure_error"
                status = "infrastructure_error" if infrastructure_failure else "complete"
            finally:
                output.flush()
                manifest.finish(status)
        return 2 if infrastructure_failure else 0
    except (
        ValueError,
        TypeError,
        KeyError,
        OSError,
        RuntimeError,
        subprocess.SubprocessError,
    ) as error:
        print(f"cinder: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
