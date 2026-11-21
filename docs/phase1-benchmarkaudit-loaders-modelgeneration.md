# miniF2F benchmark for Cinder

Pinned source, audit and loader notes for `benchmarks/minif2f/`. Machine-readable pins: `pins.json`, `audit/checker_pins.json`, `audit/RESULTS.sha256`.

## 1. Source and why this fork

| Item | Value |
|---|---|
| Repo | `yangky11/miniF2F-lean4` (submodule `upstream/`, never edited) |
| Commit | `5746b7d6c47855ce1294bed87329618ff7f1bc31` (tree hash and licence in `pins.json`) |
| Toolchain | Lean 4.24.0 (same as Cinder's verifier); Mathlib rev in `upstream/lake-manifest.json` |
| Size | 488 problems: 244 valid, 244 test |

**Why this fork.** Lean 4, matches the verifier toolchain, familiar problem set and splits, exact commit/Mathlib/hash pinning, and we audit it ourselves. It is not a gold standard (no fork is), and we do not rely on upstream maintenance: the pinned commit is the benchmark.

**Layout facts (verified).** One `theorem` per file, each ending `:= by sorry`; no `admit`, `axiom`, `lemma`, namespaces, sections, attributes or `variable`. Every file has the same header: `import Mathlib`, `set_option maxHeartbeats 0`, `open BigOperators Real Nat Topology Rat`. No informal statements, no JSONL in this commit, no trailing newline (hash raw bytes).

## 2. Policy: what the audit judges

We audit **statements**, not the placeholder proof.

| Finding | Treatment |
|---|---|
| `sorry` in upstream proof body | Expected, never a reason to exclude |
| `admit` in proof body | Investigate; not automatically a bad statement |
| Statement fails to elaborate | Potential exclusion; record exact error |
| Vacuous or malformed statement | Investigate and document |
| Extra axioms affecting the theorem | Flag for review, never silently discard |

**Target for models:** the elaborated theorem declaration with all binders and named hypotheses (`h₀`, ...) preserved exactly. Models never see the upstream `sorry` body.

**Exclusion tiers.** 1: mechanically proven defect (proven vacuous or counterexample). 2: defect confirmed by two independent human reviews against the informal problem. 3: annotate and keep. Decisions use statements only, never model results. Ledger: `exclusions.jsonl` (reason, checker, commit, reviewers, date); Tier 3 in `annotations.jsonl`.

## 3. Extraction

`utils/minif2f_extract.py` (run from repo root) reads tracked `.lean` files and fails loudly on any deviation. Output `extracted.jsonl`, sha256 `0a6ed8a95d77bc37a74db722fc297d05f59d117e11e0267e386986c2fe549456`, deterministic (two runs identical). Fields: name, split, source_path, theorem_line, header, declaration (no proof), source/header/statement sha256.

## 4. Audit setup

| Item | Value |
|---|---|
| Checker | `Shashi456/atp-checkers`, commit `3e7e99d027fece04d9cd96288cdd040c366458e5` |
| Checker toolchain | `leanprover/lean4:v4.30.0-rc2` (sha256 of `lean-toolchain` / `lake-manifest.json` in `audit/environment.txt`) |
| Input | `utils/minif2f_audit_input.py` builds `lean_code` = header minus `import` + declaration + `:= by sorry`; extra fields kept as metadata |
| Full input sha256 | `56e837cb3877eeff78159cc08c29e03f42c0132ff34f9315c6ffa669fa29d625` (`audit/full488.jsonl`) |
| Machine | Kaggle CPU notebook, no accelerator: 4 cores, 31 GiB RAM, Xeon 2.2 GHz |
| Run | `-j 2 --timeout 120`, 40 min wall; preamble keeps `maxHeartbeats 0` |

The checker runs on a **newer Lean/Mathlib than miniF2F's 4.24.0**, so statements are elaborated under a different Mathlib. Result: no statement failed to elaborate; one aborted with a Lean panic (see 6).

## 5. Results

Main run: 392 ok, 82 findings, 14 without a usable result (12 infra errors, 1 timeout, 1 panic). After retries: **484 audited (401 ok, 83 with findings), 4 unaudited.** Merged per-problem table: `audit/audit_results.jsonl` (source run and transform per row).

Findings in the main run (117): 6 proven, 111 maybe. Categories: 0-indexed Range 36 (INFO), Division by Zero 33, Truncated Nat Subtraction 22, Analytic Domain 13, Integer Division Truncation 12 (all 6 proven ones), Modulo Edge Case 1. `maybe` findings have a real false-positive rate (e.g. `aime_1983_p1` logs: guard exists but was not proved) and need manual review. No Vacuous, Counterexample or Axiom findings.

**Unaudited (not excluded, reviewed by hand):**

| Problem | Cause |
|---|---|
| `mathd_numbertheory_328` | Linter recursion error even at `maxRecDepth 100000` |
| `mathd_numbertheory_543` | Timeout at 120 s |
| `numbertheory_2pownm1prime_nprime` | Timeout at 300 s |
| `numbertheory_3pow2pownm1mod2pownp3eq2pownp2` | `INTERNAL PANIC: Nat.pow exponent is too big` (Lean abort) |

## 6. Difficulties and workarounds

1. **Laptop disk.** The project sat on a 5400 rpm HDD. `import Mathlib` took 8 to 14 min at ~2% CPU (I/O pressure, ~12 MB/s reads); the first pilot timed out 7/7. That output is invalid and kept as `raw/pilot20_hdd_invalid`. Fix: moved the audit to a Kaggle CPU notebook (import in seconds, ~8 s/problem). A GPU does not help; Lean is CPU-only and GPU quota is needed for Phase 2.
2. **Checker README inconsistencies.** It gives two toolchain versions and a `--backend` flag that this checkout lacks. We trust `lean-toolchain`, `run.json` and the CLI usage, never the README.
3. **Linter recursion errors.** 12 number-theory problems with large concrete arithmetic made the linter report `Linter Internal Error` (maximum recursion depth, `declarations: 0`, mapped to `infra_error`). Documented transform: add `set_option maxRecDepth 100000` after the `open` line (statement unchanged). Fixed 10; rows are labelled `transform` in the merged table.
4. **Panic is not catchable.** No option fixes `Nat.pow exponent is too big`; worth an upstream issue with the minimal statement.
5. **Vacuity checker gap (found by controls).** It proves contradictions with `omega`: fires for ℕ/ℤ, closed and empty cases, but **not for ℝ** (`vac_real`, `vac_conj_real` stayed `ok`). Counterexample enumerates only small Nat/Int/Fin, so it is validated for ℕ only. Consequently, zero vacuity/counterexample findings do **not** show real-valued problems are clean. Mitigation: supplementary screen (`utils/vacuity_screen.py`): per statement `exfalso` then `omega | linarith | nlinarith | norm_num | simp_all`, kernel-checked, so it can only add proven findings and never clears a problem. Heartbeats 200000. Results: `audit/vacuity_screen.jsonl` Screen ran on 484 statements plus 3 controls (chunks of 25, 20 files): 1 proven vacuous (mathd_algebra_275), 483 inconclusive, 0 chunk failures. Controls behaved as expected.
6. **Controls.** Positive controls fired for: natural subtraction, division, integer-division truncation/cast, ℕ counterexample, vacuity (ℕ/ℤ/closed/empty); clean control stayed `ok`. Not individually tested: modulo, exponent, analytic-domain checkers.
7. **Input hygiene.** The converter must drop the `import` line (runner adds its own); regenerate inputs from scripts, never hand-edit JSONL. Runner refuses an existing output dir without `--append`; `--skip-existing` skips failed ids too, so retries use fresh inputs/outputs. Kaggle `/tmp` is wiped per session: rerun setup and build.

## 7. Open decisions for the loader

- **Binders:** verifier takes one proposition; miniF2F has named hypotheses. Settle with the verifier author (e.g. `∀`-closure vs intro) while preserving names. Problem records may need extra fields; `problem_hash` covers all fields.
- **Preamble:** `maxHeartbeats 0` in the trusted header vs Cinder's heartbeat budget and its `set_option` ban (which targets candidates only); decide which budget wins.
- **Notation:** header opens `Real Nat Topology Rat`; confirm hand-parsed terms see scoped notation in the Mathlib backend.
- Human-proof and elaboration checks wait for the Mathlib environment backend.

## 8. Loader spec (`harness/benchmarks/minif2f.py`)

`verify_pins()` (refuse on any mismatch) → `read_extracted()` → `apply_ledger()` → `to_problem()` → `write_outputs()` → `build_manifest()`. Outputs: `problems.valid.jsonl`, `problems.test.jsonl` (explicit flag), `problems_excluded.jsonl` (never read by the CLI), `manifest.json`. Evaluation refuses any id not in the manifest's included list. Tests: golden problems, no excluded name in main files, byte-identical reruns, split counts, tamper refusal.

## 9. Reproduce

Submodule at the pinned commit → `python3 utils/minif2f_extract.py` → `python3 utils/minif2f_audit_input.py --out benchmarks/minif2f/audit/full488.jsonl` → Kaggle notebook: install elan, clone checker at the pinned commit, `lake exe cache get && lake build`, run `python -m runner full488.jsonl -w . -o <dir> --timeout 120 -j 2`, then retries and controls. Verify with `audit/INPUTS.sha256` and `audit/RESULTS.sha256`.
