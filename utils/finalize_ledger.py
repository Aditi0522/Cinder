#!/usr/bin/env python3
"""Apply the reviewed exclusion decisions to benchmarks/minif2f/exclusions.jsonl.

Run from the repo root, with the real reviewer names:
    python3 utils/finalize_ledger.py --reviewers "Name One" "Name Two"
Keeps existing evidence/checker fields, refuses placeholder names, refuses to finish while any
other row is still pending_review, and rewrites the file deterministically (sorted).
"""
import argparse
import json
import sys
from pathlib import Path

MF = Path(__file__).resolve().parents[1] / "benchmarks" / "minif2f"

DECISIONS = {
    "mathd_algebra_208": (2, "Lean elaboration confirms the exponent 1/3 is Nat, so it evaluates to 0. "
                             "The expression (1000000 : ℝ) ^ (1/3) evaluates to 1 instead of the intended "
                             "cube root 100, changing the original mathematical statement."),
    "mathd_algebra_275": (1, "Proven vacuous: the exfalso screen closes the statement with kernel-checked "
                             "arithmetic tactics, so the hypotheses are contradictory and any conclusion is "
                             "provable. The formalization does not preserve the original problem."),
    "mathd_algebra_282": (2, "Lean elaboration confirms the exponent 1/3 is Nat, so 8 ^ (1/3) evaluates to 1 "
                             "instead of the intended cube root 2. This changes an argument to the function f "
                             "and therefore changes the original problem."),
    "mathd_algebra_314": (2, "The expression is inferred in Nat, so both occurrences of 1/4 evaluate to 0. "
                             "With n = 11, the statement reduces to 0 = 0 rather than the intended "
                             "fractional identity."),
}

ap = argparse.ArgumentParser()
ap.add_argument("--reviewers", nargs=2, required=True, metavar="NAME")
a = ap.parse_args()
if len(set(a.reviewers)) != 2 or any(n.upper().startswith("REVIEWER_") for n in a.reviewers):
    sys.exit("need two distinct real reviewer names (no REVIEWER_* placeholders)")

path = MF / "exclusions.jsonl"
rows = {}
for line in path.read_text(encoding="utf-8").splitlines():
    if line.strip():
        r = json.loads(line)
        rows[r["problem_id"]] = r

names = {json.loads(x)["name"] for x in (MF / "extracted.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()}
unknown = sorted(set(DECISIONS) - names)
if unknown:
    sys.exit(f"not benchmark problems: {unknown}")

for pid, (tier, note) in DECISIONS.items():
    r = rows.setdefault(pid, {"problem_id": pid})
    r.update(tier=tier, decision="exclude", reviewers=list(a.reviewers), notes=note)

pending = sorted(p for p, r in rows.items() if r["decision"] == "pending_review")
if pending:
    sys.exit(f"still pending (decide keep or exclude first): {pending}")

path.write_text("".join(json.dumps(rows[p], sort_keys=True, ensure_ascii=False) + "\n" for p in sorted(rows)),
                encoding="utf-8", newline="\n")
print(f"{len(rows)} ledger rows; excluded: {sorted(DECISIONS)}")
