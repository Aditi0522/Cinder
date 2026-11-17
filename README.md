# Cinder

Research tooling for weight-space programming of Lean 4 provers. The research
plan is in [docs](docs/Weight-Space%20Programming%20for%20Lean%204%20-%20Research%20Plan.pdf).

The verifier supports pinned core and miniF2F/Mathlib environments, proof terms
and complete theorem declarations, resource-limited workers, and run manifests.
The broader Phase 1 gate remains open: miniCTX, dataset-wide audits and model
generation are separate work. See [issue #3](https://github.com/Aditi0522/Cinder/issues/3).

## Setup

Use Linux with `git`, `curl`, [uv](https://docs.astral.sh/uv/getting-started/installation/),
[bubblewrap](https://github.com/containers/bubblewrap), `prlimit` and a
working systemd user session with delegated cgroup v2 memory/pid controllers.
On Ubuntu, the additional packages are `bubblewrap util-linux`. User
namespaces must be enabled. The verifier fails closed if isolation or aggregate
resource limits cannot be applied; there is no unbounded fallback.

From a fresh checkout, choose an environment:

```bash
bash scripts/setup.sh                       # core environment and core tests
bash scripts/setup.sh --environment minif2f # Mathlib cache, checker and full tests
```

Setup installs the selected Lean toolchain through elan, syncs Python dependencies
from `uv.lock`, fetches cached Mathlib builds when selected, builds the trusted
checker, and runs the relevant tests. Downloads require internet during setup;
proof workers have no network access. Setup uses the checked-in Lake lockfile
and does not run `lake update`.

| Environment | Config | Lake project | Pins |
|---|---|---|---|
| Lean core | `configs/verifier.toml` | repository root | Lean 4.24.0 |
| miniF2F | `configs/minif2f.toml` | `environments/minif2f` | Lean 4.24.0, Mathlib `f897ebcf…`, miniF2F `5746b7d6…` |

Each project has its own toolchain and transitive dependency lock. Verification
checks the installed Lean version, manifest revisions, dependency Git HEADs and
modified tracked dependency files. New benchmark versions use separate projects
and configs. miniCTX and older Lean-version backports are deferred.

## Verify samples

```bash
uv run cinder \
  --problems examples/problems.jsonl \
  --samples examples/samples.jsonl \
  --output artifacts/results.jsonl
```

The core examples produce one accepted proof and one rejected `sorry`.
An output file must not already exist. The command exits 0 when evaluation
completed, including ordinary failed proofs, and 2 for infrastructure errors.
Candidate crashes are recorded per sample and do not abort the batch. A manifest
is written alongside results (`results.manifest.json` above); use `--manifest`
to choose another destination. Both files are protected against overwriting.

To check the five adapted upstream miniF2F-valid reference proofs:

```bash
uv run cinder --config configs/minif2f.toml \
  --problems examples/minif2f/problems.jsonl \
  --samples examples/minif2f/samples.jsonl \
  --output artifacts/minif2f-sanity.jsonl
```

Fixture provenance and proof adaptations are documented in
[examples/minif2f](examples/minif2f/README.md). Official test proofs are not used.

Problem records own the statement, binders, imports, preamble and environment ID. They
must come from a trusted registry. Sample records supply the proof, never the
theorem signature. For example, a problem may have `binders: "(n : Nat) (h : n = 1)"`
and `statement: "n + 1 = 2"`; its proof body can use `n` and `h` directly.
Existing proposition-only statements such as `∀ n : Nat, n = n` remain supported.

Use `output_format: "proof"` for a Lean term or one complete theorem declaration,
`"declaration"` for an explicit declaration contract, or `"markdown"` for exactly
one fenced Lean block containing either form. Complete `theorem` declarations
and Mathlib `lemma` declarations are parsed structurally. Their fully elaborated
types must be definitionally equal to the trusted signature, allowing renamed
binders but rejecting changed assumptions or conclusions. The checked theorem's
type is compared again after kernel checking. Model theorem names are discarded.

Auxiliary top-level lemmas/definitions, multiple declarations, imports, namespaces,
attributes, declaration modifiers, explicit declaration universes and `where`
declarations are rejected. Local `have` and `let` proofs are supported. Nothing is
silently dropped from a model's Lean block to make it pass.

Additional generation fields (checkpoint/tokenizer revisions, decoding settings,
finish reason, and similar metadata) are accepted and preserved in
`additional_fields`. An explicit `metadata` object is retained independently;
ambiguous duplicate additional fields are rejected.

The checker parses a single term, constructs the theorem from the stored
statement, asks Lean to kernel-check it, and inspects transitive axioms. Only
`propext`, `Classical.choice`, and `Quot.sound` are allowed. Source policy also
rejects holes, native evaluation, option changes, syntax quotations and explicit
elaborator execution. Comments and strings containing `sorry` are allowed;
indirect dependencies on `sorryAx` are rejected by the axiom audit.

Each candidate runs in a fresh process with read-only access to its toolchain,
compiled libraries and input directory. A private tmpfs is the only writable
regular filesystem. Bubblewrap isolates process/network namespaces and disables
nested user namespaces. A systemd scope enforces aggregate memory and task
limits across the worker and its descendants; swap is disabled for that scope.
Task limits include threads. Default worker limits are 4 GiB memory, 64 tasks,
64 MiB tmpfs, 256 file descriptors, no core dumps and 2 MB per-file/output writes.
Memory, task and tmpfs limits are configurable. Wall-clock and heartbeat limits
are also enforced; trusted preambles cannot override the configured heartbeat
budget. No candidate environment is reused.

[configs/verifier.toml](configs/verifier.toml) controls core limits and concurrency.
`workers = 0` uses available CPU cores minus one. No GPU or fixed machine-size
assumption is built into the verifier. The miniF2F config starts at one worker;
choose a count from measured memory and throughput, rather than CPU count alone.
Kaggle generation can later export the
same JSONL sample contract and leave all Lean evaluation on this machine.

Results preserve generation metadata, raw output, extracted proof, verdict,
diagnostics, elapsed time, axiom dependencies, Lean version, environment ID,
and statement/context and config hashes. Result schema version 2 adds preserved
metadata, per-worker peak RSS and a run ID. `mathlib_commit` is null only in the
core environment; unknown token counts remain null. Failure labels include truncation,
repetition, extraction failures, parser errors, unknown identifiers, tactic
failures, type mismatches and timeouts. They do not infer obstacle versus
capability. Candidate diagnostics use positions relative to the extracted Lean
block (line numbers start at 1, columns at 0), including complete declarations.
Errors distinguish candidate source from driver/setup source; runtime failures
without source locations retain null positions. A parser error without a reliable
end offset has no fabricated end position.

Each run manifest records the Git commit and dirty state, source-file hashes,
compiled checker hash, dependency/environment pins, effective config and worker
count, input hashes, selected machine/runtime details, status, verdict counts
and final result checksum. It does not record environment variables or credentials.
Worker RSS is sampled every 50 ms by the host supervisor across the worker's
process tree, including children inside nested PID namespaces. `peak_rss_kb` is
the largest observed process RSS, not a kernel high-water counter. Shared mapped
library pages are included in each process's RSS.

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
uv run pytest -m 'not mathlib' # after core setup
uv run pytest                # after miniF2F setup
uv run ruff check harness scripts tests
```

See [Phase 1 status](docs/phase1.md) for the remaining gate requirements.
Measured worker scaling and the REPL decision are in [docs/throughput.md](docs/throughput.md).
