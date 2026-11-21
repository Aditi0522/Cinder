"""Generate reproducible miniF2F pins from the pinned upstream checkout.

Run from the repo root AFTER the ledger review and the elaboration check:
    python3 utils/make_pins.py
`derived` holds data the loader re-verifies on every build (paths relative to the repo root);
`tools` records the scripts that produced them, for provenance only.
"""
import datetime
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path.cwd()
MF = ROOT / "benchmarks/minif2f"
UP = MF / "upstream"
AUDIT = MF / "audit"

COMMIT = "5746b7d6c47855ce1294bed87329618ff7f1bc31"

DERIVED = {
    "extracted_jsonl": "benchmarks/minif2f/extracted.jsonl",
    "exclusions": "benchmarks/minif2f/exclusions.jsonl",
    "annotations": "benchmarks/minif2f/annotations.jsonl",
    "audit_input_full488": "benchmarks/minif2f/audit/full488.jsonl",
    "audit_results": "benchmarks/minif2f/audit/audit_results.jsonl",
    "vacuity_screen": "benchmarks/minif2f/audit/vacuity_screen.jsonl",
    "elab_check": "benchmarks/minif2f/audit/elab_check.jsonl",
    "checker_pins": "benchmarks/minif2f/audit/checker_pins.json",
}
TOOLS = {
    "extractor": "utils/minif2f_extract.py",
    "audit_input_builder": "utils/minif2f_audit_input.py",
    "vacuity_screen": "utils/vacuity_screen.py",
    "elab_check": "utils/minif2f_elab_check.py",
    "ledger_builder": "utils/build_ledger.py",
}


def git(*args):
    return subprocess.check_output(["git", "-C", str(UP), *args], text=True).strip()


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def jsonl(path):
    return [json.loads(x) for x in Path(path).read_text(encoding="utf-8").splitlines() if x.strip()]


# Confirm that the source checkout is exactly the revision we audited.
assert git("rev-parse", "HEAD") == COMMIT, "Unexpected upstream commit"
assert git("status", "--porcelain", "--untracked-files=all") == "", "Upstream working tree is not clean"

# Derive the consumed source list from Git, not a manually maintained list.
tracked = subprocess.check_output(
    ["git", "-C", str(UP), "ls-files", "-z", "--", "MiniF2F/Valid", "MiniF2F/Test"]
).decode().split("\0")
CONSUMED = sorted(p for p in tracked if p.endswith(".lean"))
assert len(CONSUMED) == 488, f"Expected 488 individual problem files, found {len(CONSUMED)}"

# Read and identify the actual upstream license.
license_heading = (UP / "LICENSE").read_text().splitlines()[0].strip()
assert license_heading == "MIT License", f"Unexpected license heading: {license_heading!r}"

# Every derived file and tool must exist before its hash is pinned.
for group in (DERIVED, TOOLS):
    for key, rel in group.items():
        path = ROOT / rel
        assert path.is_file() and path.stat().st_size > 0, f"Missing or empty: {rel}"

# Ordering guards: pin only a finished review and a clean elaboration check.
ledger = jsonl(ROOT / DERIVED["exclusions"])
pending = [r["problem_id"] for r in ledger if r["decision"] == "pending_review"]
assert not pending, f"Ledger review unfinished, pending: {pending}"
excluded = {r["problem_id"] for r in ledger if r["decision"] == "exclude"}
failing = {r["problem_id"] for r in jsonl(ROOT / DERIVED["elab_check"]) if not r["elaborates"]}
assert failing <= excluded, f"Statements that fail to elaborate but are not excluded: {sorted(failing - excluded)}"

manifest = json.loads((UP / "lake-manifest.json").read_text())
mathlib = next(p for p in manifest["packages"] if p["name"] == "mathlib")

archive = subprocess.run(
    ["git", "-C", str(UP), "archive", "--format=tar", "HEAD"], capture_output=True, check=True
).stdout

tree = git("rev-parse", "HEAD^{tree}")
assert len(tree) == 40, f"Unexpected Git tree hash: {tree}"

pins = {
    "benchmark": "minif2f-lean4",
    "source": {
        "url": git("remote", "get-url", "origin"),
        "commit": COMMIT,
        "tree": tree,
        "archive_sha256": hashlib.sha256(archive).hexdigest(),
        "git_version": subprocess.check_output(["git", "--version"], text=True).strip(),
        "license": "MIT",
    },
    "pinned_on": datetime.date.today().isoformat(),
    "toolchain": {
        "lean": (UP / "lean-toolchain").read_text().strip(),
        "file_sha256": sha(UP / "lean-toolchain"),
    },
    "lake_manifest": {
        "sha256": sha(UP / "lake-manifest.json"),
        "mathlib": {k: mathlib.get(k) for k in ("url", "rev", "inputRev")},
    },
    "files": {p: sha(UP / p) for p in CONSUMED},
    "derived": {k: {"path": rel, "sha256": sha(ROOT / rel)} for k, rel in DERIVED.items()},
    "tools": {k: {"path": rel, "sha256": sha(ROOT / rel)} for k, rel in TOOLS.items()},
}

output = MF / "pins.json"
output.write_text(json.dumps(pins, indent=2) + "\n")

print(f"Consumed source files: {len(CONSUMED)}")
print(f"Tree: {tree}")
print(f"Ledger: {len(excluded)} excluded, {len(failing)} fail to elaborate")
print(f"Derived files pinned: {', '.join(DERIVED)}")
print(f"Wrote: {output.relative_to(ROOT)}")
