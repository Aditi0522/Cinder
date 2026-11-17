# Issue #3: completion checklist

Scope: [Complete Lean Infrastructure and Verifier](https://github.com/Aditi0522/Cinder/issues/3).
Implementation, measurements and clean-checkout validation are complete.

## 1. Benchmark-specific environments

- [x] Introduce independent Lake-project, Lean-toolchain and Mathlib-revision
  configuration (`harness/environment.py`). Dependency revisions and tracked
  source modifications are checked before verification.
- [x] Pin miniF2F Lean 4.24.0, Mathlib
  `f897ebcf72cd16f89ab4577d0c826cd14afaafc7`, benchmark revision
  `5746b7d6c47855ce1294bed87329618ff7f1bc31`, and transitive Lake dependencies.
  Fetch compiled caches through `scripts/setup.sh --environment minif2f`.
- [x] Keep miniCTX's project-specific environments and old-version backports
  deferred, as requested. The config/project boundary supports separate pins;
  only the core and miniF2F Lean 4.24.0 projects are validated here.

## 2. Verifier behavior

- [x] Support explicit/implicit binders, hypotheses and typeclass parameters.
- [x] Accept one complete `theorem` or Mathlib `lemma`, including renamed
  binders. Compare elaborated signatures against the trusted problem before
  checking the body, then compare the checked theorem's type again.
- [x] Define the auxiliary-declaration policy: reject top-level helpers, extra
  commands, attributes, modifiers and `where` declarations. Local `have` and
  `let` are supported. Do not silently discard model code.
- [x] Preserve explicit sample metadata and unknown generation fields in result
  schema version 2, while rejecting ambiguous duplicate additional fields.

## 3. Sandbox security

- [x] Enforce cgroup-charged memory and task limits across the worker family,
  disable its swap, and bound its total writable tmpfs. Root/input/library
  mounts are read-only; output/file sizes, descriptors and core dumps are bounded.
- [x] Exercise actual memory exhaustion, process creation, disk exhaustion and
  attempts to write outside the writable mount in tests.
- [x] Retain kernel checking and the three-axiom allowlist. Reject direct and
  indirect holes, custom axioms, native-evaluation axioms, changed signatures,
  injected commands and invalid proof terms. Fresh processes prevent state reuse.

The supported sandbox requires Linux user namespaces and a delegated systemd
user/cgroup-v2 environment. Unsupported hosts fail closed. These protections do
not establish resistance to every possible Lean/kernel exploit.

## 4. Diagnostics and reproducibility

- [x] Map candidate elaboration, signature, parser and policy diagnostics to the
  extracted Lean block. Test multiline terms, complete declarations, Markdown
  extraction and Unicode. Identify driver diagnostics separately and leave
  unavailable runtime/end positions unset.
- [x] Write a run manifest containing code commit/dirty state and source hashes,
  compiled-checker/environment/dependency fingerprints, machine details,
  effective settings, input hashes, status/counts and output checksum.
- [x] Measure worker RSS from the host process tree, rather than only the
  launcher. Test a known allocation in a worker reached through a pool thread
  and nested PID namespace. Document sampling and shared-page limitations.

## 5. Performance

- [x] Measure the same five valid-split reference proofs twice at 1, 2 and 4
  workers. Record latency, verified proofs/minute, sampled process and aggregate RSS.
- [x] Publish [the report](throughput.md), manifests and raw measurement records.
  At two workers this host achieved 22.60 verified proofs/minute; four workers
  were slower, and a preliminary run also had startup timeouts.
- [x] Decide to retain fresh processes for the initial pilot. A 60-sample screen
  takes about 2.7 minutes at the measured rate. Revisit persistent REPLs only
  after representative generated proofs demonstrate a bottleneck, with the
  same trust/resource/state-reset checks required before adoption.

## 6. Mathlib sanity tests

- [x] Add five known-good miniF2F-valid reference proof ports, with immutable
  statement/reference provenance, source hashes, adaptation notes and licenses.
  Original authorship includes people and GPT-f; individual human authorship
  is not asserted. See [fixture provenance](../examples/minif2f/README.md).
- [x] Verify the reference proofs and reject manipulated statements, proof holes,
  unsupported axioms, injected declarations and malformed constructions under Mathlib.

## Completion validation

Command: `bash scripts/setup.sh --environment minif2f` from a clean clone on a
disk-backed filesystem, with no project virtualenv or Lake build directory.
The installed Lean toolchain and global download caches may be reused.

Validation on 2026-11-17: **136 tests passed** from a new local clone at
`e6322bfad29deb6acb4827e219e0dde70b6ccccc`. Setup took about 219 seconds in
total; pytest took 131 seconds. Both core and Mathlib projects were built from
source in that checkout. Only the user's installed toolchain and global download
caches were reused. The [validation record](../results/validation/issue3-clean-checkout.json)
preserves the command, commit and result. Ruff, formatting, Python type checks
and shell syntax checks also passed.

miniCTX, dataset-wide benchmark loaders/audits and Kaggle model generation remain
outside this issue. Their remaining Phase 1 work is tracked in [phase1.md](phase1.md).
