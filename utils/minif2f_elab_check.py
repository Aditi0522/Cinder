#!/usr/bin/env python3
"""Check that every miniF2F statement elaborates under the pinned Mathlib (Lean 4.24).

Run from the repo root, after warming the disk cache:
    find benchmarks/minif2f/upstream/.lake -name '*.olean' -print0 | xargs -0 cat > /dev/null
    python3 utils/minif2f_elab_check.py
Builds ONE Lean file (single Mathlib import) with every declaration closed by `sorry`,
under `autoImplicit false` like the Cinder verifier. Writes audit/elab_check.{lean,jsonl}.
"""
import bisect
import json
import re
import subprocess
import sys
from pathlib import Path

MF = Path(__file__).resolve().parents[1] / "benchmarks" / "minif2f"
rows = [json.loads(x) for x in (MF / "extracted.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
headers = {r["header"] for r in rows}
assert len(headers) == 1, "expected one shared header"
text = headers.pop() + "set_option autoImplicit false\n\n"
line = text.count("\n") + 1
starts = []
for r in rows:
    starts.append(line)
    body = r["declaration"] + " := by sorry\n\n"
    text += body
    line += body.count("\n")
lean = MF / "audit" / "elab_check.lean"
lean.write_text(text, encoding="utf-8", newline="\n")

proc = subprocess.run(["lake", "env", "lean", str(lean.resolve())], cwd=MF / "upstream",
                      capture_output=True, text=True, timeout=7200)
out = proc.stdout + proc.stderr
if "PANIC" in out or proc.returncode not in (0, 1):
    sys.exit(f"Lean aborted (exit {proc.returncode}):\n{out[-1500:]}")
errors = {}
for mt in re.finditer(r":(\d+):\d+: error: (.*)", out):
    i = bisect.bisect_right(starts, int(mt.group(1))) - 1
    if i >= 0:
        errors.setdefault(rows[i]["name"], mt.group(2)[:300])
result = [{"problem_id": r["name"], "elaborates": r["name"] not in errors, "error": errors.get(r["name"])}
          for r in sorted(rows, key=lambda r: r["name"])]
(MF / "audit" / "elab_check.jsonl").write_text(
    "".join(json.dumps(x, sort_keys=True, ensure_ascii=False) + "\n" for x in result), encoding="utf-8", newline="\n")
print(f"{len(rows) - len(errors)} elaborate, {len(errors)} fail")
for n, e in sorted(errors.items()):
    print(" ", n, "|", e)
