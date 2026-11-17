# Verifier throughput

Measured on 2026-11-17 using implementation commit `1682301`, Lean 4.24.0,
Mathlib `f897ebcf72cd16f89ab4577d0c826cd14afaafc7` and miniF2F revision
`5746b7d6c47855ce1294bed87329618ff7f1bc31`. The machine exposes 24 logical
CPUs and about 7.5 GiB RAM; exact CPU/kernel/Python details are retained in the
run manifests. The reproducible measurement command is:

```bash
uv run python scripts/benchmark_verifier.py \
  --worker-counts 1 2 4 --repeats 2 \
  --output artifacts/throughput/measurements.json
```

The workload consists of the five checked-in miniF2F-valid reference proofs,
repeated twice at each worker count. One warmup proof precedes each configuration.
Each measured proof still runs in a fresh isolated Lean process; warmup warms
filesystem caches, not a persistent Lean environment. Results include per-sample
JSONL, per-run manifests, latency, verified proofs/minute, maximum worker RSS and
sampled aggregate descendant RSS. Aggregate RSS counts shared mappings in each
process and is not a measurement of unique physical memory. Individual worker
RSS is sampled from the host process tree every 50 ms; aggregate RSS is sampled
every 100 ms. These are observed peaks, not kernel high-water counters. Runtime
failures are retained in the report, and a configuration with reference failures
is not considered a usable throughput result.

The official test set is not used. These easy reference proofs characterize
verification/import overhead, not the cost or success rate of generated proofs.

## Results

| Workers | Verified | Elapsed (s) | Verified proofs/min | Median latency (s) | p95 latency (s) | Max sampled worker RSS (GiB) | Sampled summed RSS (GiB) |
|---|---|---|---|---|---|---|---|
| 1 | 10/10 | 49.39 | 12.15 | 4.81 | 5.87 | 5.13 | 5.13 |
| 2 | 10/10 | 26.55 | 22.60 | 5.33 | 6.58 | 5.01 | 10.01 |
| 4 | 10/10 | 73.83 | 8.13 | 25.55 | 35.82 | 4.87 | 17.61 |

This is a small, warm-cache import/verification measurement: five distinct easy
problems, not 30 independent benchmark problems. The nearest-rank p95 is the
maximum latency with ten observations. Do not interpret these numbers as model
success rates or as throughput for long generated proof searches.

RSS includes shared mapped Mathlib pages and can exceed both physical RAM when
summed across processes and a worker's 4 GiB `MemoryMax`. The latter limits
memory **charged to its cgroup**, not every shared page visible in RSS. Memory
may remain charged to the cgroup which first instantiated it, as described in
the [kernel's memory ownership documentation](https://docs.kernel.org/admin-guide/cgroup-v2.html#memory-ownership).
The memory-limit tests separately verify that private allocations are stopped.

A preliminary four-worker attempt also recorded four 60-second import/startup
timeouts. Its incorrect launcher-only RSS readings were rejected and are not
included in this table. The [failure-only summary](../results/throughput/2026-11-17/preliminary-workers-4-failures.json)
preserves that evidence. The corrected four-worker rerun completed but was
substantially slower; it is not the recommended configuration.

## Decision

Use **two workers on this host** for the initial miniF2F pilot. The checked-in
miniF2F config retains a portable one-worker default; set `workers = 2` in a
run-specific config when reproducing this machine's setting. Do not select
workers from CPU count alone.

Keep the fresh-process backend for now; a persistent REPL is not required for
the initial screening workload. At the measured two-worker rate, 60 reference
proofs take about 2.7 minutes, and 600 about 27 minutes, excluding startup and
warmup. Those are extrapolations for this workload, not promises for generated
proofs. The fresh process provides an explicit environment reset per sample.
Revisit a REPL only after representative model-output runs show verification
blocking the next experiment, and require the same signature, axiom, resource
and state-reset tests before adopting it.

## Evidence

[Measurement summary](../results/throughput/2026-11-17/measurements.json),
per-worker JSONL results and run manifests are tracked under
[`results/throughput/2026-11-17`](../results/throughput/2026-11-17/).
Copies retain their original runtime paths inside the manifests. Each manifest
records the clean implementation commit/source fingerprint, exact dependency
pins, effective worker count and limits, machine details, input hashes and the
raw result checksum.
