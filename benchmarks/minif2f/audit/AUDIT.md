# miniF2F audit summary

Checker `3e7e99d027fece04d9cd96288cdd040c366458e5`; narrative and difficulties: `../README.md`.

- Problems: 488 (Counter({'valid': 244, 'test': 244}))
- Coverage: {'audited': 484, 'unaudited': 4}
- Final status: {'ok': 401, 'findings': 83, 'unaudited_linter_error': 1, 'unaudited_timeout': 2, 'unaudited_linter_abort': 1}
- Transformed (maxRecDepth): 10
- Vacuity screen: {'inconclusive': 483, 'proven_vacuous': 1}

| Finding | Confidence | Count |
|---|---|---|
| 0-Indexed Range | maybe | 37 |
| Analytic Domain Totalization | maybe | 13 |
| Integer Division Truncation | maybe | 7 |
| Integer Division Truncation | proven | 6 |
| Modulo Edge Case | maybe | 1 |
| Potential Division by Zero | maybe | 33 |
| Truncated Nat Subtraction | maybe | 22 |

Tier 1 candidates: 1; review queue: 15 (see REVIEW.md).

## Review decisions (fill in by hand)

| Problem | Decision | Reviewers | Reason |
|---|---|---|---|
