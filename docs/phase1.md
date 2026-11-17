# Phase 1: evaluation harness

Status: started; the Phase 1 completion gate has **not** been met.

The PDF defines Phase 1 on pages 3–5. The current machine's capacity supersedes
its old eight-core/no-GPU limits. Runtime concurrency and budgets are config
values; generation and verification communicate through JSONL files so
generation can move to Kaggle independently.

## First milestone implemented

- Lean 4.24.0 core-only bring-up environment, pinned in `lean-toolchain`.
- Trusted Lean command that parses the candidate as one proof term and
  constructs a theorem with the registry's statement.
- Synchronous kernel checking and a transitive axiom allowlist.
- Syntax policy rejecting explicit holes, elaborator execution, option changes,
  syntax quotations and native evaluation.
- Fresh bubblewrap worker processes with no network and a per-sample timeout.
- Configurable concurrency, JSONL records and SHA-256 provenance hashes.
- Explicit proof/Markdown extraction and failure classifier v0.
- Human proofs and injected-cheat integration tests, including indirect holes,
  custom axioms and a worker that exceeds its time budget.
- One-command setup, smoke inputs and a documented evaluation command.

Validation on 2026-11-16: all 61 tests passed when running
`bash scripts/setup.sh` from a fresh source directory without a virtual
environment or Lake build artifacts. Elan's installed toolchain and download
caches were reused. Ruff and shell syntax checks also passed. This is setup
validation for the first milestone, not completion of the benchmark/generation gate.

The core toolchain is a bring-up choice, not a benchmark/model compatibility
decision. The current upstream
[miniF2F Lean 4 toolchain](https://github.com/yangky11/miniF2F-lean4/blob/5746b7d6c47855ce1294bed87329618ff7f1bc31/lean-toolchain)
also uses 4.24.0. Before importing any benchmark, pin its exact source revision,
Mathlib commit and other dependencies together. Models requiring older versions
need separate environments, not an automatic toolchain upgrade.

## Next milestones, in order

1. Add a fully pinned miniF2F environment with cached Mathlib and a loader that
   preserves trusted statements and records source hashes. Verify known human
   proofs on the development split. Keep official test proofs out of pilot runs.
2. Add miniCTX loaders with separate per-project environments and explicit
   context handling. Do not pretend one global Lean version supports all projects.
3. Run the benchmark audit tools, pin their revisions and keep an exclusions
   ledger with reasons. No problem list is currently claimed to be audited.
4. Normalize diagnostic source mapping and validate registered problems before
   batch evaluation. Invalid trusted statements and context already receive
   infrastructure-error verdicts rather than model-failure labels.
5. Measure realistic Mathlib worker memory and throughput. Evaluate a persistent
   REPL backend against the same sanity cases and verify state resets. Current
   process isolation favors a clear trust boundary over import amortization.
6. Add Kaggle-compatible vLLM generation with per-batch checkpoints, pinned model
   and tokenizer revisions, per-sample metadata and safe resume behavior. Test a
   small model end to end on development problems.
7. Reproduce from a clean clone, record throughput at explicit worker counts,
   and review all Phase 1 gate criteria before tagging `phase1-done`.

The current syntax policy is an initial explicit denylist, backed by the kernel
axiom audit and OS isolation. It is not a proof of resistance to every Lean
metaprogramming exploit. Expand the adversarial suite as trusted imports and
accepted model output formats grow. Trusted benchmark statements/preambles
still require the separate mathematical audit in the research plan.
