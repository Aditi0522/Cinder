#!/usr/bin/env python3
"""Supplementary vacuity screen for the miniF2F audit.

atp-checkers proves vacuity with omega only, so it misses real-valued
contradictions. For each statement this checks, with Lean, whether
`exfalso; first | omega | linarith | nlinarith | norm_num | simp_all` closes
the goal. Success is a kernel-checked proof of vacuity; failure is only
"inconclusive" (never evidence the statement is fine).

Run from the repo root (needs a built Lean workspace with Mathlib, e.g. the
atp-checkers checkout):

    python3 utils/vacuity_screen.py --checker tools/atp-checkers
    # Kaggle: --checker /tmp/atp-checkers --input /kaggle/input/.../full488.jsonl \
    #         --out-dir /kaggle/working/audit

Parameters used for the published results: chunk 25, heartbeats 200000, 2 jobs.
Controls vac_real / vac_conj_real must be proven_vacuous and ctrl_clean
inconclusive, otherwise the script exits non-zero.
"""
import argparse, json, os, re, subprocess, sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "benchmarks" / "minif2f" / "audit"

# Statements the linter could not process (see audit_results.jsonl); they can
# crash Lean on large concrete powers, so they stay out of the shared chunks.
SKIP = {"mathd_numbertheory_328", "mathd_numbertheory_543",
        "numbertheory_2pownm1prime_nprime", "numbertheory_3pow2pownm1mod2pownp3eq2pownp2"}
CONTROLS = [
    ("vac_real", "theorem vac_real (x : ℝ) (h₀ : x < 3) (h₁ : 5 < x) : x = 7"),
    ("vac_conj_real", "theorem vac_conj_real (x : ℝ) (h : x < 0 ∧ 0 < x) : x = 5"),
    ("ctrl_clean", "theorem ctrl_clean (x : ℝ) (h : 0 < x) : 0 < x * x"),
]
EXPECTED = {"vac_real": "proven_vacuous", "vac_conj_real": "proven_vacuous", "ctrl_clean": "inconclusive"}
TACT = " := by\n  exfalso\n  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)\n\n"
PAT = re.compile(r":=\s*by\s+sorry\s*\Z")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", type=Path, default=AUDIT / "full488.jsonl")
    ap.add_argument("--out-dir", type=Path, default=AUDIT)
    ap.add_argument("--checker", type=Path, default=ROOT / "tools" / "atp-checkers")
    ap.add_argument("--chunk", type=int, default=25)
    ap.add_argument("--heartbeats", type=int, default=200000)
    ap.add_argument("--jobs", type=int, default=2)
    ap.add_argument("--timeout", type=int, default=900)
    a = ap.parse_args()

    if "ELAN_HOME" not in os.environ and Path("/tmp/elan").exists():
        os.environ["ELAN_HOME"] = "/tmp/elan"
        os.environ["PATH"] = "/tmp/elan/bin:" + os.environ["PATH"]

    items = []
    for line in a.input.read_text(encoding="utf-8").splitlines():
        d = json.loads(line)
        if d["id"] in SKIP:
            continue
        m = PAT.search(d["lean_code"])
        assert m, d["id"]
        code = d["lean_code"]
        items.append((d["id"], code[code.index("theorem "):m.start()].rstrip()))
    items += CONTROLS
    print(len(items), "items")

    hdr = ("import Mathlib\n" f"set_option maxHeartbeats {a.heartbeats}\n"
           "open BigOperators Real Nat Topology Rat\n\n")
    work = (a.out_dir / "vac_screen").resolve()
    work.mkdir(parents=True, exist_ok=True)

    def run_chunk(ci, chunk):
        text, starts, ln = hdr, {}, hdr.count("\n") + 1
        for pid, decl in chunk:
            starts[pid] = ln
            body = decl + TACT
            text += body
            ln += body.count("\n")
        f = work / f"chunk{ci:02d}.lean"
        f.write_text(text, encoding="utf-8")
        try:
            r = subprocess.run(["lake", "env", "lean", str(f)], cwd=a.checker,
                               capture_output=True, text=True, timeout=a.timeout)
        except subprocess.TimeoutExpired:
            return [(p, "chunk_failed") for p, _ in chunk]
        out = r.stdout + r.stderr
        if "PANIC" in out or r.returncode not in (0, 1):
            return [(p, "chunk_failed") for p, _ in chunk]
        errs = [int(x.group(1)) for x in re.finditer(r":(\d+):\d+: error", out)]
        ids = [p for p, _ in chunk]
        res = []
        for i, pid in enumerate(ids):
            lo = starts[pid]
            hi = starts[ids[i + 1]] if i + 1 < len(ids) else ln
            res.append((pid, "inconclusive" if any(lo <= e < hi for e in errs) else "proven_vacuous"))
        return res

    chunks = [items[i:i + a.chunk] for i in range(0, len(items), a.chunk)]
    with ThreadPoolExecutor(a.jobs) as ex:
        allres = [x for part in ex.map(lambda t: run_chunk(*t), enumerate(chunks)) for x in part]

    out_file = a.out_dir / "vacuity_screen.jsonl"
    out_file.write_text("".join(json.dumps({"problem_id": p, "vacuity_screen": s}, ensure_ascii=False) + "\n"
                                for p, s in allres), encoding="utf-8", newline="\n")
    print(Counter(s for _, s in allres))
    got = dict(allres)
    print("controls:", {k: got[k] for k in EXPECTED})
    print("PROVEN VACUOUS:", [p for p, s in allres if s == "proven_vacuous" and p not in EXPECTED])
    print("CHUNK FAILED:", [p for p, s in allres if s == "chunk_failed"])
    if any(got.get(k) != v for k, v in EXPECTED.items()):
        sys.exit("control check failed: results are not valid")


if __name__ == "__main__":
    main()
