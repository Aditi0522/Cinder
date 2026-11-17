"""Measure fresh-process verification on development reference proofs only."""

import argparse
import json
import math
import os
import statistics
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from pathlib import Path

from harness.cli import read_jsonl
from harness.environment import ROOT, VerifierConfig
from harness.manifest import RunManifest, code_state, file_hash, machine_state
from harness.resources import process_tree_rss
from harness.schema import Problem, Sample
from harness.verifier import LeanVerifier


class MemoryMonitor:
    """Sample summed descendant RSS; shared pages are counted in each process."""

    def __init__(self):
        self.peak_kb = 0
        self.stop = threading.Event()
        self.thread = threading.Thread(target=self.sample, daemon=True)

    def sample(self):
        while not self.stop.is_set():
            rss = process_tree_rss(os.getpid(), include_root=False)[1]
            self.peak_kb = max(self.peak_kb, rss)
            self.stop.wait(0.1)


def measure(config, problems, samples, repeats, output, inputs):
    verifier = LeanVerifier(config)
    warmup = verifier.verify(problems[samples[0].problem_id], samples[0])
    if warmup.verdict != "pass":
        raise RuntimeError(f"Warmup failed: {warmup.errors}")
    expanded = [
        replace(sample, sample_id=f"repeat-{r}-{sample.sample_id}")
        for r in range(repeats)
        for sample in samples
    ]
    manifest = RunManifest(output.with_suffix(".manifest.json"), verifier, inputs, output)
    monitor = MemoryMonitor()
    results = []
    started = time.monotonic()
    monitor.thread.start()
    status = "interrupted"
    try:
        with (
            output.open("x") as stream,
            ThreadPoolExecutor(max_workers=config.worker_count) as pool,
        ):

            def verify(sample):
                return verifier.verify(problems[sample.problem_id], sample)

            for result in pool.map(verify, expanded):
                result.run_id = manifest.record["run_id"]
                stream.write(result.to_json() + "\n")
                stream.flush()
                results.append(result)
                manifest.counts[result.verdict] += 1
        status = "complete" if all(r.verdict == "pass" for r in results) else "reference_failure"
    finally:
        elapsed = time.monotonic() - started
        monitor.stop.set()
        monitor.thread.join()
        manifest.finish(status)
    latencies = sorted(r.wall_time_seconds for r in results)
    return {
        "status": status,
        "verdict_counts": dict(manifest.counts),
        "workers": config.worker_count,
        "samples": len(results),
        "elapsed_seconds": elapsed,
        "proofs_per_minute": 60 * manifest.counts["pass"] / elapsed,
        "median_latency_seconds": statistics.median(latencies),
        "p95_latency_seconds": latencies[math.ceil(0.95 * len(latencies)) - 1],
        "max_sampled_worker_rss_mb": max(r.peak_rss_kb or 0 for r in results) / 1024,
        "sampled_peak_sum_rss_mb": monitor.peak_kb / 1024,
        "manifest": str(manifest.path),
        "results_sha256": file_hash(output),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=ROOT / "configs/minif2f.toml")
    parser.add_argument("--problems", type=Path, default=ROOT / "examples/minif2f/problems.jsonl")
    parser.add_argument("--samples", type=Path, default=ROOT / "examples/minif2f/samples.jsonl")
    parser.add_argument("--worker-counts", nargs="+", type=int, default=[1, 2, 4])
    parser.add_argument("--repeats", type=int, default=2)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.repeats < 1 or any(w < 1 for w in args.worker_counts):
        parser.error("Worker counts and repeats must be positive")
    if args.output.exists():
        parser.error("Benchmark output already exists")
    config = VerifierConfig.load(args.config)
    problems = {row["problem_id"]: Problem(**row) for row in read_jsonl(args.problems)}
    samples = [Sample.from_record(row) for row in read_jsonl(args.samples)]
    if not samples or any(p.metadata.get("split") != "valid" for p in problems.values()):
        parser.error("This benchmark requires nonempty development/valid fixtures")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    report = {
        "schema_version": 1,
        "code": code_state(),
        "machine": machine_state(),
        "warmup_proofs_per_configuration": 1,
        "repeats": args.repeats,
        "measurements": [],
    }
    for workers in args.worker_counts:
        output = args.output.with_name(f"{args.output.stem}.workers-{workers}.jsonl")
        measurement = measure(
            replace(config, workers=workers),
            problems,
            samples,
            args.repeats,
            output,
            {"problems": args.problems, "samples": args.samples},
        )
        report["measurements"].append(measurement)
        args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
        print(json.dumps(measurement), flush=True)


if __name__ == "__main__":
    main()
