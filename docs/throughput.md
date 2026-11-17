# Verifier throughput

Measurements and the persistent-REPL decision are recorded here after validating
the pinned miniF2F environment. The reproducible measurement command is:

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
process and is not a measurement of unique physical memory.

The official test set is not used. These easy reference proofs characterize
verification/import overhead, not the cost or success rate of generated proofs.
