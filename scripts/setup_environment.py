"""Install and build one pinned environment without advancing its dependency lock."""

import subprocess
import sys
from pathlib import Path

from harness.environment import LeanEnvironment, VerifierConfig


def main():
    config = VerifierConfig.load(Path(sys.argv[1]))
    elan = str(Path.home() / ".elan/bin/elan")
    subprocess.run([elan, "toolchain", "install", config.lean_toolchain], check=True)
    lake = str(Path.home() / ".elan/bin/lake")
    if config.mathlib_commit:
        subprocess.run([lake, "exe", "cache", "get"], cwd=config.project_root, check=True)
    subprocess.run([lake, "build", "Cinder"], cwd=config.project_root, check=True)
    environment = LeanEnvironment(config)
    print(f"Built {config.environment_id}: {environment.version}")


if __name__ == "__main__":
    main()
