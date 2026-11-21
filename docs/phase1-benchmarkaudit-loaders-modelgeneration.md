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

**Exclusion tiers.**

- **Tier 1:** Mechanically proven defect (proven vacuous or counterexample).
- **Tier 2:** Defect confirmed by two independent human reviews against the informal problem.
- **Tier 3:** Annotate and keep.

Decisions use statements only, never model results.

Ledger: `exclusions.jsonl` (reason, checker, commit, reviewers, date); Tier 3 in `annotations.jsonl`.

A pending review is not an exclusion. Reviewer names must identify people who independently reviewed the original informal problem and agreed on the decision. Placeholder reviewer names are rejected by the loader.

## 3. Extraction

`utils/minif2f_extract.py` (run from repo root) reads tracked `.lean` files and fails loudly on any deviation.

Output: `extracted.jsonl`

SHA256:

`0a6ed8a95d77bc37a74db722fc297d05f59d117e11e0267e386986c2fe549456`

Deterministic (two runs identical).

Fields: name, split, source_path, theorem_line, header, declaration (no proof), source/header/statement sha256.

The extraction process preserves the original source statement and does not modify the upstream submodule.

## 4. Audit setup

| Item | Value |
|---|---|
| Checker | `Shashi456/atp-checkers`, commit `3e7e99d027fece04d9cd96288cdd040c366458e5` |
| Checker toolchain | `leanprover/lean4:v4.30.0-rc2` (sha256 of `lean-toolchain` / `lake-manifest.json` in `audit/environment.txt`) |
| Input | `utils/minif2f_audit_input.py` builds `lean_code` = header minus `import` + declaration + `:= by sorry`; extra fields kept as metadata |
| Full input sha256 | `56e837cb3877eeff78159cc08c29e03f42c0132ff34f9315c6ffa669fa29d625` (`audit/full488.jsonl`) |
| Machine | Kaggle CPU notebook, no accelerator: 4 cores, 31 GiB RAM, Xeon 2.2 GHz |
| Run | `-j 2 --timeout 120`, 40 min wall; preamble keeps `maxHeartbeats 0` |

The checker runs on a **newer Lean/Mathlib than miniF2F's 4.24.0**, so statements are elaborated under a different Mathlib.

Result: no statement failed to elaborate; one aborted with a Lean panic (see Section 5).

## 5. Results

Main run: 392 ok, 82 findings, 14 without a usable result (12 infra errors, 1 timeout, 1 panic).

After retries: **484 audited (401 ok, 83 with findings), 4 unaudited.**

Merged per-problem table: `audit/audit_results.jsonl` (source run and transform per row).

Findings in the main run (117): 6 proven, 111 maybe.

| Category | Count | Notes |
|---|---:|---|
| 0-indexed Range | 36 | INFO |
| Division by Zero | 33 | |
| Truncated Nat Subtraction | 22 | |
| Analytic Domain | 13 | |
| Integer Division Truncation | 12 | All 6 proven findings are in this category |
| Modulo Edge Case | 1 | |

`maybe` findings have a real false-positive rate (e.g. `aime_1983_p1` logs: guard exists but was not proved) and need manual review.

No Vacuous, Counterexample or Axiom findings.

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

5. **Vacuity checker gap (found by controls).** It proves contradictions with `omega`: fires for ℕ/ℤ, closed and empty cases, but **not for ℝ** (`vac_real`, `vac_conj_real` stayed `ok`). Counterexample enumerates only small Nat/Int/Fin, so it is validated for ℕ only. Consequently, zero vacuity/counterexample findings do **not** show real-valued problems are clean.

   Mitigation: supplementary screen (`utils/vacuity_screen.py`): per statement `exfalso` then `omega | linarith | nlinarith | norm_num | simp_all`, kernel-checked, so it can only add proven findings and never clears a problem. Heartbeats 200000.

   Results: `audit/vacuity_screen.jsonl`. Screen ran on 484 statements plus 3 controls (chunks of 25, 20 files): 1 proven vacuous (`mathd_algebra_275`), 483 inconclusive, 0 chunk failures. Controls behaved as expected.

6. **Controls.** Positive controls fired for: natural subtraction, division, integer-division truncation/cast, ℕ counterexample, vacuity (ℕ/ℤ/closed/empty); clean control stayed `ok`. Not individually tested: modulo, exponent, analytic-domain checkers.

7. **Input hygiene.** The converter must drop the `import` line (runner adds its own); regenerate inputs from scripts, never hand-edit JSONL. Runner refuses an existing output dir without `--append`; `--skip-existing` skips failed ids too, so retries use fresh inputs/outputs. Kaggle `/tmp` is wiped per session: rerun setup and build.

8. **Kaggle storage.** Kaggle input datasets are mounted read-only. Copy the project to `/kaggle/working/` before running Lean commands that create `.lake` or build artifacts. For example:

   ```python
   from pathlib import Path
   import shutil

   SOURCE = Path("/kaggle/input/datasets/aditis0ni05/minif2f-audit-1")
   UPSTREAM = Path("/kaggle/working/minif2f-audit-1")

   if not UPSTREAM.exists():
       shutil.copytree(
           SOURCE,
           UPSTREAM,
           ignore=shutil.ignore_patterns(".git")
       )
   ```

   Run the checker and build commands from the writable copy, not the read-only dataset mount.

## 7. Loader integration and remaining decisions

The miniF2F loader is integrated with Cinder's main-branch harness schema and CLI.

**Schema and binders.** Cinder's `harness/schema.py` includes the `binders: str = ""` field. The loader uses the current `RunManifest` and `Sample.from_record` interfaces. The CLI has a dedicated `--benchmark-manifest` argument alongside the existing `--manifest` argument, with a guard that restricts evaluation to IDs included in the benchmark manifest.

The exact verifier-side treatment of named hypotheses still needs confirmation with the verifier author (e.g. `∀`-closure vs intro) while preserving names.

**Preamble.** `maxHeartbeats 0` in the trusted header vs Cinder's heartbeat budget and its `set_option` ban (which targets candidates only); decide which budget wins.

**Notation.** Header opens `Real Nat Topology Rat`; confirm hand-parsed terms see scoped notation in the Mathlib backend.

**Human-proof and elaboration checks.** These wait for the Mathlib environment backend.

## 8. Loader specification (`harness/benchmarks/minif2f.py`)

The loader pipeline is:

`verify_pins()` → `read_extracted()` → `apply_ledger()` → `to_problem()` → `write_outputs()` → `build_manifest()`.

**Pin verification.** `verify_pins()` refuses to proceed on any mismatch. It reads the `derived` entry in `pins.json`, including the `extracted_jsonl` path and SHA256. Paths are resolved relative to the repository root. All derived files and tools must exist before their hashes are pinned.

**Ledger validation.** `read_ledger()` validates exclusion decisions and rejects placeholder reviewer names beginning with `REVIEWER_`. Pending review decisions and exclusions without the required reviewer sign-off and notes are not accepted.

**Outputs:**

- `problems.valid.jsonl`
- `problems.test.jsonl` (explicit flag)
- `problems_excluded.jsonl` (never read by the CLI)
- `manifest.json`

Evaluation refuses any ID not in the manifest's included list.

**CLI integration.** The loader is connected to Cinder's main-branch CLI. Benchmark manifest handling uses `--benchmark-manifest`, separately from the general `--manifest` option. The manifest guard ensures that benchmark evaluation only accepts included problem IDs.

**Tests.** Loader tests live in `tests/test_minif2f_loader.py`, not under `harness/benchmarks/`.

Coverage includes golden problems, no excluded name in main files, byte-identical reruns, split counts, and tamper refusal.

## 9. Reproduce

### Audit reproduction (Kaggle)

1. Use the submodule at the pinned commit.
2. Run the extractor:

   ```bash
   python3 utils/minif2f_extract.py
   ```

3. Build the full audit input:

   ```bash
   python3 utils/minif2f_audit_input.py \
     --out benchmarks/minif2f/audit/full488.jsonl
   ```

4. Verify the generated input and its `lean_code` preamble. The converter must drop the `import Mathlib` line because the checker runner supplies its own import.

5. Upload a private Kaggle dataset named `minif2f-audit` containing:
   - `smoke5.jsonl`
   - `pilot20.jsonl`
   - `full488.jsonl`

   The repository itself does not need to be uploaded, and the checker is public.

6. In Kaggle, install elan, clone the checker at the pinned commit, and run:

   ```bash
   lake exe cache get
   lake build
   ```

7. Run the checker:

   ```bash
   python -m runner full488.jsonl -w . -o <dir> --timeout 120 -j 2
   ```

8. Run retries and controls. Verify with `audit/INPUTS.sha256` and `audit/RESULTS.sha256`.

### Local preparation (Cinder repository)

Run from the repository root:

```bash
cd ~/projects/cinder
```

**Collect the pins.**

From `benchmarks/minif2f/audit/checker_pins.json`, take the full checker commit SHA. Also take the toolchain string from the pilot's `run.json` (`leanprover/lean4:v4.30.0-rc2`) and the Mathlib revision from the checker's `lake-manifest.json`.

**Quarantine the invalid pilot.**

If the invalid pilot has not already been renamed, move it so it cannot be mixed into valid audit data:

```bash
mv benchmarks/minif2f/audit/raw/pilot20 \
   benchmarks/minif2f/audit/raw/pilot20_hdd_invalid
```

Do not overwrite an existing destination. If the destination already exists, inspect both directories before proceeding.

**Check the audit input.**

```bash
jq -r '.lean_code' benchmarks/minif2f/audit/pilot20.jsonl | head -3
```

Earlier, `head -3` of the baseline file showed `import Mathlib` twice, and one import had been prepended manually. The runner deduplicates imports, but the README specifies that `lean_code` should omit the import. Fix the converter if it is still present.

**Build the full input.**

```bash
python3 utils/minif2f_audit_input.py \
  --out benchmarks/minif2f/audit/full488.jsonl
```

Record its SHA256 in the pins. Do not hand-edit the generated JSONL.

**Finalize the ledger.**

Only after the two reviewers have independently reviewed the original informal problems and agreed on the decisions, run:

```bash
python3 utils/finalize_ledger.py --reviewers "Aditi" "Vaibhav"
```

The names must correspond to the actual reviewers. Do not use the command to bypass independent review.

Regenerate the pins after finalizing the ledger:

```bash
python3 utils/make_pins.py
```

**Cinder integration.**

When reproducing the loader integration on a fresh branch:

1. Merge `origin/main` before replacing `harness/cli.py`.
2. Keep the main-branch CLI implementation and apply the benchmark-specific CLI changes on top.
3. Move the loader test into `tests/test_minif2f_loader.py`.
4. Confirm that `harness/schema.py` contains the `binders` field.
5. Confirm that `harness/benchmarks/minif2f.py` uses the current `derived` pin format and rejects `REVIEWER_` placeholders.
6. Run `uv sync` after the merge.

The test file should be located at:

`tests/test_minif2f_loader.py`

The loader should be located at:

`harness/benchmarks/minif2f.py`

**Local validation.**

Run:

```bash
uv run pytest tests/test_minif2f_loader.py -q
uv run ruff check harness tests utils
python -m harness.benchmarks.minif2f \
  --environment-id lean-core-4.24.0
```

Inspect the final changes before committing:

```bash
git status --short
git diff --check
git diff
```

The benchmark command should use an environment ID that exists in the repository's environment configuration. The `lean-core-4.24.0` ID was used successfully for the loader invocation documented below; it does not by itself establish that full Mathlib proof evaluation is available.

## 10. Current local validation status

Latest recorded local validation:

| Check | Result |
|---|---|
| miniF2F loader tests | 15 passed |
| Ruff | 21 findings; not yet clean |
| Benchmark loader invocation | Successful |
| Valid split | 243 included, 1 excluded |
| Test split | 241 included, 3 excluded |
| Total | 484 included, 4 excluded |

**Loader tests.**

Command:

```bash
uv run pytest tests/test_minif2f_loader.py -q
```

Result:

```text
15 passed in 0.08s
```

**Lint.**

Command:

```bash
uv run ruff check harness tests utils
```

Result:

```text
Found 21 errors.
[*] 5 fixable with `--fix` (6 unsafe fixes available with `--fix --unsafe-fixes`).
```

Findings include:

- `EXE001`: Shebang is present but file is not executable.
- `I001`: Import block is unsorted or unformatted.
- `ISC004`: Unparenthesized implicit string concatenation in a collection.
- `PERF102`: Dictionary `.items()` used when only values are needed.
- `TRY004`: `ValueError` used for invalid input types.
- `PLW1510`: `subprocess.run` lacks an explicit `check` argument.
- `FURB167`: Regular expression alias `re.M` instead of `re.MULTILINE`.

Some fixes are unsafe and require manual review. A clean Ruff run has not yet been recorded.

**Benchmark loader invocation.**

Command:

```bash
python -m harness.benchmarks.minif2f \
  --environment-id lean-core-4.24.0
```

Output:

```json
{
  "test": {
    "excluded": 3,
    "included": 241
  },
  "valid": {
    "excluded": 1,
    "included": 243
  }
}
```

This confirms that the loader successfully applied the exclusion ledger and constructed the expected valid and test splits.

It does **not** demonstrate that model evaluation, proof generation, or the Mathlib environment backend has run successfully.

**Next validation steps.**

1. Resolve the Ruff findings, reviewing unsafe fixes manually.
2. Rerun the loader tests.
3. Rerun the benchmark loader command.
4. Inspect `git status`, `git diff --check`, and the final diff.
5. Confirm the generated files and hashes match `pins.json` and the audit checksum files.
6. Commit the reviewed integration changes.

The audit results, loader construction, and actual model evaluation are separate stages and should be reported separately.
