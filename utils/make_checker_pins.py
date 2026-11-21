#!/usr/bin/env python3
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path.cwd()
CHECKER = ROOT / "tools/atp-checkers"

def git(*args):
    return subprocess.check_output(
        ["git", "-C", str(CHECKER), *args],
        text=True,
    ).strip()

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

commit = git("rev-parse", "HEAD")
tree = git("rev-parse", "HEAD^{tree}")

pins = {
    "repository": "https://github.com/Shashi456/atp-checkers",
    "commit": commit,
    "tree": tree,
    "toolchain": {
        "version": (CHECKER / "lean-toolchain").read_text().strip(),
        "sha256": sha(CHECKER / "lean-toolchain"),
    },
    "lake_manifest": {
        "sha256": sha(CHECKER / "lake-manifest.json"),
    },
}

output = ROOT / "benchmarks/minif2f/audit/checker_pins.json"
output.write_text(json.dumps(pins, indent=2) + "\n")

print(json.dumps(pins, indent=2))
print(f"\nWrote {output}")
