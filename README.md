# Cinder

Research tooling for weight-space programming of Lean 4 provers. The research
plan is in [docs](docs/Weight-Space%20Programming%20for%20Lean%204%20-%20Research%20Plan.pdf).

Phase 1 has started with an isolated verifier for **proof terms**. This first
environment pins Lean 4.24.0 and uses its core library. Mathlib benchmark
environments and model generation are the next steps; the Phase 1 gate is open.

## Setup

Use Linux with `curl`, [uv](https://docs.astral.sh/uv/getting-started/installation/)
and [bubblewrap](https://github.com/containers/bubblewrap) installed. On Ubuntu,
install bubblewrap with `sudo apt install bubblewrap`. User namespaces must be
enabled. The verifier refuses to run without isolation.

From a fresh checkout:

```bash
bash scripts/setup.sh
```

This installs the pinned Lean toolchain through elan, syncs Python dependencies
from `uv.lock`, builds the trusted Lean checker, and runs the full sanity suite.
Toolchain and package downloads require internet during setup. Proof workers
have no network access.

## Verify samples

```bash
uv run cinder \
  --problems examples/problems.jsonl \
  --samples examples/samples.jsonl \
  --output artifacts/results.jsonl
```

The examples produce one accepted human proof and one rejected `sorry`.
An output file must not already exist. The command exits 0 when evaluation
completed, including ordinary failed proofs, and 2 for infrastructure errors.
Candidate crashes are recorded per sample and do not abort the batch.

Problem records own the statement, imports, preamble and environment ID. They
must come from a trusted registry. Sample records supply the proof, never the
theorem declaration. Use `output_format: "proof"` for a Lean term such as
`by intro n; rfl`, or `"markdown"` for exactly one fenced Lean proof block.
Full theorem declarations are rejected rather than silently rewritten.

The checker parses a single term, constructs the theorem from the stored
statement, asks Lean to kernel-check it, and inspects transitive axioms. Only
`propext`, `Classical.choice`, and `Quot.sound` are allowed. Source policy also
rejects holes, native evaluation, option changes, syntax quotations and explicit
elaborator execution. Comments and strings containing `sorry` are allowed;
indirect dependencies on `sorryAx` are rejected by the axiom audit.

Each candidate runs in a fresh process with read-only access to its toolchain
and the compiled checker, a private writable directory, isolated process and
network namespaces, a heartbeat budget and a wall-clock timeout. No candidate
environment is reused. This is the initial correctness backend; a persistent
REPL pool can be added after equivalent checks pass.

[configs/verifier.toml](configs/verifier.toml) controls timeouts and concurrency.
`workers = 0` uses available CPU cores minus one. No GPU or fixed machine-size
assumption is built into the verifier. Kaggle generation can later export the
same JSONL sample contract and leave all Lean evaluation on this machine.

Results preserve generation metadata, raw output, extracted proof, verdict,
diagnostics, elapsed time, axiom dependencies, Lean version, environment ID,
and statement/context and config hashes. `mathlib_commit` and unknown token
counts are null in this environment. Failure labels include truncation,
repetition, extraction failures, parser errors, unknown identifiers, tactic
failures, type mismatches and timeouts. They do not infer obstacle versus
capability. Lean diagnostic positions can refer to the proof term or the
generated driver; normalized source mapping is still pending.

Infrastructure verdicts receive only the `infrastructure_error` label, regardless
of diagnostic text or generation flags. A flushed marker records entry into
candidate processing after the trusted statement has been validated. Abnormal
exits, malformed worker output, and diagnostic-output overflow after that marker
receive `candidate_crash`; the same failures during trusted setup receive
`infrastructure_error`. Timeouts follow the same boundary and use `timeout` once
candidate processing has started. Exit/signal codes and available diagnostics
are retained. This records the observed execution phase; it does not establish
whether a kill was caused by the candidate, host memory pressure, or another
external event. Missing or invalid success reports remain infrastructure errors.

```bash
uv run pytest
uv run ruff check harness tests
```

See [Phase 1 status](docs/phase1.md) for the remaining gate requirements.
