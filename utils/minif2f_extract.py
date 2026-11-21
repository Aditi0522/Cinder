#!/usr/bin/env python3
"""Extract miniF2F statements from the pinned upstream checkout. Run from the repo root."""
import hashlib, json, re, subprocess
from pathlib import Path

UP = Path("benchmarks/minif2f/upstream")
OUT = Path("benchmarks/minif2f/extracted.jsonl")
SPLITS = {"Valid": "valid", "Test": "test"}
EXPECTED = {"valid": 244, "test": 244}
THEOREM = re.compile(r"^theorem[ \t]+(\S+)", re.M)
PROOF = re.compile(r":=[ \t\r\n]*by[ \t\r\n]+sorry[ \t\r\n]*\Z")

def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def fail(path, msg):
    raise SystemExit(f"{path}: {msg}")

tracked = subprocess.check_output(
    ["git", "-C", str(UP), "ls-files", "-z", "MiniF2F/Valid", "MiniF2F/Test"], text=True
).split("\0")
files = sorted(p for p in tracked if p.endswith(".lean"))

rows, headers = [], set()
for rel in files:
    raw = (UP / rel).read_bytes()
    text = raw.decode("utf-8")
    split = SPLITS[rel.split("/")[1]]
    ms = list(THEOREM.finditer(text))
    if len(ms) != 1:
        fail(rel, f"expected 1 theorem, found {len(ms)}")
    m = ms[0]
    name = m.group(1)
    if name != Path(rel).stem:
        fail(rel, f"theorem name {name!r} != file stem")
    header = text[: m.start()]
    body = text[m.start():]
    p = PROOF.search(body)
    if not p:
        fail(rel, "does not end with ':= by sorry'")
    declaration = body[: p.start()].rstrip()
    if "sorry" in declaration or ":= by" in declaration:
        fail(rel, "unexpected proof material inside statement")
    headers.add(header)
    rows.append({
        "name": name,
        "split": split,
        "source_path": rel,
        "theorem_line": text.count("\n", 0, m.start()) + 1,
        "header": header,
        "declaration": declaration,
        "source_sha256": sha(raw),
        "header_sha256": sha(header.encode()),
        "statement_sha256": sha(declaration.encode()),
    })

if len(headers) != 1:
    raise SystemExit(f"{len(headers)} distinct headers; expected 1")
counts = {s: sum(r["split"] == s for r in rows) for s in EXPECTED}
if counts != EXPECTED:
    raise SystemExit(f"split counts {counts} != {EXPECTED}")
if len({r["name"] for r in rows}) != len(rows):
    raise SystemExit("duplicate theorem names")

rows.sort(key=lambda r: (r["split"], r["name"]))
with OUT.open("w", encoding="utf-8", newline="\n") as f:
    for r in rows:
        f.write(json.dumps(r, sort_keys=True, ensure_ascii=False) + "\n")
print(f"wrote {len(rows)} rows {counts} -> {OUT}")
