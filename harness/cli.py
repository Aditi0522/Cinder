"""JSONL in and JSONL out; generation machines do not need Lean installed."""

import argparse
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

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
    args = parser.parse_args()
    try:
        config = VerifierConfig.load(args.config)
        problems = {}
        for record in read_jsonl(args.problems):
            problem = Problem(**record)
            if problem.problem_id in problems:
                raise ValueError(f"Duplicate problem id: {problem.problem_id}")
            problems[problem.problem_id] = problem
        samples = [Sample(**record) for record in read_jsonl(args.samples)]
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
        # Exclusive creation prevents accidentally overwriting an experiment.
        with (
            args.output.open("x", encoding="utf-8") as output,
            ThreadPoolExecutor(max_workers=config.worker_count) as pool,
        ):

            def verify(sample: Sample):
                return verifier.verify(problems[sample.problem_id], sample)

            for result in pool.map(verify, samples):
                output.write(result.to_json() + "\n")
                output.flush()
                infrastructure_failure |= result.verdict == "infrastructure_error"
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
