# miniF2F development sanity fixtures

These five problems come only from the official **valid** split. No official
test proofs are evaluated. Each problem records its immutable source URL and
SHA-256, and retains the original binder/hypothesis signature and conclusion.
The benchmark's `set_option maxHeartbeats 0` is deliberately omitted: the
verifier owns its execution budget.

Statements: [miniF2F Lean 4 revision 5746b7d](https://github.com/yangky11/miniF2F-lean4/tree/5746b7d6c47855ce1294bed87329618ff7f1bc31/MiniF2F/Valid).
Reference proofs: [original miniF2F revision 4e433ff](https://github.com/openai/miniF2F/blob/4e433ff5cadff23f9911a2bb5bbab2d351ce5554/lean/src/valid.lean).
Original authors: Kunhao Zheng, Stanislas Polu, David Renshaw, OpenAI GPT-f.
The Lean 4 repository uses the MIT license (copyright Meta Platforms, Inc. and
affiliates); the original miniF2F reference uses Apache-2.0 (copyright OpenAI).
The MIT license file and the Apache-2.0 text referenced by the original source
header are included here. These are upstream reference proofs adapted to Lean 4,
not a claim that every original proof was authored by a human.

- `mathd_numbertheory_101`, `mathd_algebra_10`: `norm_num`, unchanged strategy.
- `mathd_algebra_51`: `linarith`, unchanged strategy.
- `mathd_algebra_110`: substitution and polynomial normalization; the Lean 3
  imaginary-unit simplification is replaced with `norm_num [Complex.I_sq]`.
- `algebra_sqineq_4bap1lt4bsqpap1sq`: the original nonnegative-square argument,
  discharged with `nlinarith [sq_nonneg ...]`.

These fixtures establish harness correctness on known proofs. They do not
constitute a mathematical audit or a benchmark performance score. Dataset-wide
loaders and audits are separate work.

```bash
bash scripts/setup.sh --environment minif2f
uv run cinder --config configs/minif2f.toml \
  --problems examples/minif2f/problems.jsonl \
  --samples examples/minif2f/samples.jsonl \
  --output artifacts/minif2f-sanity.jsonl
```
