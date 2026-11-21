#!/usr/bin/env python3
"""Generate the audit ledger drafts from data (run from repo root).

Reads  benchmarks/minif2f/{extracted.jsonl, audit/audit_results.jsonl, audit/vacuity_screen.jsonl}
Writes benchmarks/minif2f/exclusions.jsonl   Tier 1 candidates, decision "pending_review"
       benchmarks/minif2f/annotations.jsonl  Tier 3: flags kept with the problem (never excluded)
       benchmarks/minif2f/audit/REVIEW.md    statements + findings for manual review
       benchmarks/minif2f/audit/AUDIT.md     counts (only if absent)
Nothing is excluded automatically: the loader must only honour decision == "exclude",
which a human sets after two independent reviews. Existing ledger files are never
overwritten unless --force.
"""
import json, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MF = ROOT / "benchmarks" / "minif2f"
AU = MF / "audit"
CHECKER_COMMIT = "3e7e99d027fece04d9cd96288cdd040c366458e5"
TIER1 = {"Vacuous Theorem", "Counterexample Found"}
REVIEW_CATS = {"Integer Division Truncation", "Modulo Edge Case", "Cast After Truncation"} | TIER1
force = "--force" in sys.argv


def jl(p):
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]


def dump(p, rows):
    if p.exists() and not force:
        sys.exit(f"{p} exists; refusing to overwrite (use --force)")
    p.write_text("".join(json.dumps(r, sort_keys=True, ensure_ascii=False) + "\n" for r in rows),
                 encoding="utf-8", newline="\n")


res = sorted(jl(AU / "audit_results.jsonl"), key=lambda r: r["problem_id"])
vac = {r["problem_id"]: r["vacuity_screen"] for r in jl(AU / "vacuity_screen.jsonl")}
ext = {r["name"]: r for r in jl(MF / "extracted.jsonl")}
assert len(res) == 488 and all(r["problem_id"] in ext for r in res)

excl, ann, review = [], [], []
for r in res:
    pid, fs = r["problem_id"], r["findings"]
    ev = [{"checker": f["category"], "confidence": f["confidence"], "provedBy": f.get("provedBy"),
           "message": f["message"][:300]} for f in fs if f["category"] in TIER1 and f["confidence"] == "proven"]
    if vac.get(pid) == "proven_vacuous":
        ev.append({"checker": "vacuity_screen", "confidence": "proven", "provedBy": "exfalso + arithmetic tactics",
                   "message": "hypotheses contradictory; kernel-checked"})
    if ev:
        excl.append({"problem_id": pid, "tier": 1, "decision": "pending_review", "evidence": ev,
                     "checker_commit": CHECKER_COMMIT, "reviewers": [], "notes": ""})
    flags = sorted({(f["category"], f["confidence"], f["severity"]) for f in fs})
    if flags or r["coverage"] == "unaudited":
        ann.append({"problem_id": pid, "coverage": r["coverage"], "final_status": r["final_status"],
                    "transform": r["transform"],
                    "flags": [{"category": c, "confidence": k, "severity": s} for c, k, s in flags]})
    if ev or r["coverage"] == "unaudited" or any(f["category"] in REVIEW_CATS for f in fs):
        review.append((r, ev))

dump(MF / "exclusions.jsonl", excl)
dump(MF / "annotations.jsonl", ann)

lines = ["# Manual review queue", "",
         "Both reviewers judge each statement against the informal problem, independently. "
         "Set `decision` in `exclusions.jsonl` to `exclude` or `keep` and fill `reviewers`.", ""]
for r, ev in review:
    pid = r["problem_id"]
    lines += [f"## {pid} ({r['split']}) — {r['final_status']}", "", "```lean", ext[pid]["declaration"], "```", ""]
    for f in r["findings"]:
        lines.append(f"- [{f['confidence']}/{f.get('provedBy')}] {f['category']}: {f['message'][:200]}")
    if ev:
        lines.append("- **Tier 1 candidate**")
    lines += ["", "Decision: ____  Reviewer A: ____  Reviewer B: ____  Notes: ____", ""]
(AU / "REVIEW.md").write_text("\n".join(lines), encoding="utf-8")

if not (AU / "AUDIT.md").exists() or force:
    fc = Counter((f["category"], f["confidence"]) for r in res for f in r["findings"])
    out = ["# miniF2F audit summary", "",
           f"Checker `{CHECKER_COMMIT}`; narrative and difficulties: `../README.md`.", "",
           f"- Problems: {len(res)} ({Counter(r['split'] for r in res)})",
           f"- Coverage: {dict(Counter(r['coverage'] for r in res))}",
           f"- Final status: {dict(Counter(r['final_status'] for r in res))}",
           f"- Transformed (maxRecDepth): {sum(bool(r['transform']) for r in res)}",
           f"- Vacuity screen: {dict(Counter(v for p, v in vac.items() if p in ext))}", "",
           "| Finding | Confidence | Count |", "|---|---|---|"]
    out += [f"| {c} | {k} | {n} |" for (c, k), n in sorted(fc.items())]
    out += ["", f"Tier 1 candidates: {len(excl)}; review queue: {len(review)} (see REVIEW.md).", "",
            "## Review decisions (fill in by hand)", "", "| Problem | Decision | Reviewers | Reason |", "|---|---|---|---|", ""]
    (AU / "AUDIT.md").write_text("\n".join(out), encoding="utf-8")

print(f"exclusion candidates {len(excl)}, annotations {len(ann)}, review queue {len(review)}")
