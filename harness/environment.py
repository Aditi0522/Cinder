"""Pinned Lake projects and runtime policy, independent of the host machine size."""

import hashlib
import json
import os
import re
import shutil
import subprocess
import tomllib
from dataclasses import asdict, dataclass
from pathlib import Path

from harness.schema import sha256

ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class VerifierConfig:
    environment_id: str
    lean_toolchain: str
    mathlib_commit: str
    timeout_seconds: float
    max_heartbeats: int
    workers: int
    project_dir: str = "."
    benchmark_repository: str = ""
    benchmark_commit: str = ""
    memory_mb: int = 4096
    max_processes: int = 64
    disk_mb: int = 64

    def __post_init__(self):
        if self.timeout_seconds <= 0 or self.max_heartbeats < 1 or self.workers < 0:
            raise ValueError("Timeout and heartbeats must be positive; workers must be nonnegative")
        if self.memory_mb < 32 or self.max_processes < 8 or self.disk_mb < 1:
            raise ValueError("Sandbox limits require memory >=32 MB, tasks >=8 and disk >=1 MB")
        for name in ("mathlib_commit", "benchmark_commit"):
            value = getattr(self, name)
            if value and not re.fullmatch(r"[0-9a-f]{40}", value):
                raise ValueError(f"{name} must be an exact 40-character Git revision")

    @classmethod
    def load(cls, path: Path) -> "VerifierConfig":
        return cls(**tomllib.loads(path.read_text(encoding="utf-8")))

    @property
    def project_root(self) -> Path:
        return (ROOT / self.project_dir).resolve()

    @property
    def worker_count(self) -> int:
        if self.workers:
            return self.workers
        cores = len(os.sched_getaffinity(0)) if hasattr(os, "sched_getaffinity") else os.cpu_count()
        return max(1, (cores or 1) - 1)

    @property
    def config_hash(self) -> str:
        return sha256(json.dumps(asdict(self), sort_keys=True))


class LeanEnvironment:
    def __init__(self, config: VerifierConfig):
        self.config = config
        self.project = config.project_root
        if (self.project / "lean-toolchain").read_text().strip() != config.lean_toolchain:
            raise RuntimeError("Config does not match the environment's pinned toolchain")
        elan = shutil.which("elan") or str(Path.home() / ".elan/bin/elan")
        self.lean = Path(
            subprocess.check_output(
                [elan, "which", "lean"],
                cwd=self.project,
                text=True,
            ).strip()
        ).resolve()
        self.toolchain = self.lean.parent.parent
        self.version = subprocess.check_output([str(self.lean), "--version"], text=True).strip()
        expected = config.lean_toolchain.rsplit(":v", 1)[-1]
        if not re.search(rf"version {re.escape(expected)}(?:,|\))", self.version):
            raise RuntimeError(f"Lean version mismatch: {self.version}")
        manifest_path = self.project / "lake-manifest.json"
        self.manifest = json.loads(manifest_path.read_text())
        mathlib = next((p for p in self.manifest["packages"] if p["name"] == "mathlib"), None)
        if (mathlib or {}).get("rev", "") != config.mathlib_commit:
            raise RuntimeError("Mathlib config and Lake manifest pins differ")
        self.dependencies = {}
        for package in self.manifest["packages"]:
            package_root = self.project / self.manifest["packagesDir"] / package["name"]
            revision = subprocess.check_output(
                ["git", "rev-parse", "HEAD"],
                cwd=package_root,
                text=True,
            ).strip()
            if revision != package["rev"]:
                raise RuntimeError(f"Dependency revision mismatch: {package['name']}")
            dirty = subprocess.check_output(
                ["git", "status", "--porcelain", "--untracked-files=no"],
                cwd=package_root,
                text=True,
            ).strip()
            if dirty:
                raise RuntimeError(f"Modified trusted dependency: {package['name']}")
            self.dependencies[package["name"]] = revision
        lake = self.lean.parent / "lake"
        search_path = subprocess.check_output(
            [str(lake), "env", "printenv", "LEAN_PATH"],
            cwd=self.project,
            text=True,
        ).strip()
        self.lean_paths = tuple((self.project / p).resolve() for p in search_path.split(":") if p)
        checker = self.project / ".lake/build/lib/lean/Cinder/Verifier.olean"
        if not checker.exists():
            raise RuntimeError(
                "Verifier module is not built; run scripts/setup.sh for this environment"
            )
        self.fingerprint = {
            "environment_id": config.environment_id,
            "lean_version": self.version,
            "mathlib_commit": config.mathlib_commit or None,
            "benchmark_commit": config.benchmark_commit or None,
            "dependencies": self.dependencies,
            "lake_manifest_sha256": sha256(manifest_path.read_text()),
            "lakefile_sha256": sha256(next(self.project.glob("lakefile.*")).read_text()),
            "checker_sha256": hashlib.sha256(checker.read_bytes()).hexdigest(),
        }
