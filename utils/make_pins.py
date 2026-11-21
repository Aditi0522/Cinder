
"""Generate reproducible miniF2F pins from the pinned upstream checkout."""
import datetime
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path.cwd()
UP = ROOT / "benchmarks/minif2f/upstream"
EXTRACTED = ROOT / "benchmarks/minif2f/extracted.jsonl"
EXTRACTOR = ROOT / "utils/minif2f_extract.py"
assert EXTRACTOR.is_file(), f"Missing extractor: {EXTRACTOR}"

COMMIT = "5746b7d6c47855ce1294bed87329618ff7f1bc31"


def git(*args):
    return subprocess.check_output(
        ["git", "-C", str(UP), *args], text=True
    ).strip()


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


# Confirm that the source checkout is exactly the revision we audited.
assert git("rev-parse", "HEAD") == COMMIT, "Unexpected upstream commit"
assert git("status", "--porcelain", "--untracked-files=all") == "", (
    "Upstream working tree is not clean"
)

# Derive the consumed source list from Git, not a manually maintained list.
tracked = subprocess.check_output(
    [
        "git", "-C", str(UP),
        "ls-files", "-z", "--", "MiniF2F/Valid", "MiniF2F/Test"
    ]
).decode().split("\0")

CONSUMED = sorted(
    p for p in tracked
    if p.endswith(".lean")
)

assert len(CONSUMED) == 488, (
    f"Expected 488 individual problem files, found {len(CONSUMED)}"
)

# Read and identify the actual upstream license.
license_file = UP / "LICENSE"
license_heading = license_file.read_text().splitlines()[0].strip()
assert license_heading == "MIT License", (
    f"Unexpected license heading: {license_heading!r}"
)
license_name = "MIT"

# Confirm that the extraction artifact exists before pinning its hash.
assert EXTRACTED.is_file(), f"Missing extraction artifact: {EXTRACTED}"
assert EXTRACTED.stat().st_size > 0, "extracted.jsonl is empty"

manifest = json.loads((UP / "lake-manifest.json").read_text())
mathlib = next(p for p in manifest["packages"] if p["name"] == "mathlib")

archive = subprocess.run(
    ["git", "-C", str(UP), "archive", "--format=tar", "HEAD"],
    capture_output=True,
    check=True,
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
        "git_version": subprocess.check_output(
            ["git", "--version"], text=True
        ).strip(),
        "license": license_name,
    },
    "pinned_on": datetime.date.today().isoformat(),
    "toolchain": {
        "lean": (UP / "lean-toolchain").read_text().strip(),
        "file_sha256": sha(UP / "lean-toolchain"),
    },
    "lake_manifest": {
        "sha256": sha(UP / "lake-manifest.json"),
        "mathlib": {
            k: mathlib.get(k) for k in ("url", "rev", "inputRev")
        },
    },
    "files": {
        p: sha(UP / p) for p in CONSUMED
    },
    "derived": {
    "extracted_jsonl": {
        "path": "extracted.jsonl",
        "sha256": sha(EXTRACTED),
    },
    "extractor": {
        "path": "utils/minif2f_extract.py",
        "sha256": sha(EXTRACTOR),
         },
    },
}

output = ROOT / "benchmarks/minif2f/pins.json"
output.write_text(json.dumps(pins, indent=2) + "\n")

print(f"Consumed source files: {len(CONSUMED)}")
print(f"License: {license_name}")
print(f"Tree: {tree}")
print(f"Extracted SHA-256: {pins['derived']['extracted_jsonl']['sha256']}")
print(f"Wrote: {output.relative_to(ROOT)}")

