"""Run provenance without recording credentials or the process environment."""

import hashlib
import json
import os
import platform
import subprocess
import uuid
from collections import Counter
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path

from harness.environment import ROOT


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def code_state() -> dict:
    files = (
        subprocess.check_output(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
            cwd=ROOT,
        )
        .decode()
        .split("\0")
    )
    hashes = {}
    for filename in filter(None, files):
        path = ROOT / filename
        if Path(filename).parts[0] in {"results", "artifacts"}:
            continue
        if path.is_file() and (
            path.suffix in {".py", ".lean", ".toml", ".json", ".lock", ".sh"}
            or path.name == "lean-toolchain"
        ):
            hashes[filename] = file_hash(path)
    return {
        "git_commit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip(),
        "git_status": subprocess.check_output(
            ["git", "status", "--porcelain"], cwd=ROOT, text=True
        ).splitlines(),
        "files": hashes,
        "source_hash": hashlib.sha256(json.dumps(hashes, sort_keys=True).encode()).hexdigest(),
    }


def machine_state() -> dict:
    memory = {}
    for line in Path("/proc/meminfo").read_text().splitlines():
        key, value = line.split(":", 1)
        if key in {"MemTotal", "SwapTotal"}:
            memory[key] = int(value.split()[0]) * 1024
    model = next(
        (
            line.split(":", 1)[1].strip()
            for line in Path("/proc/cpuinfo").read_text().splitlines()
            if line.startswith("model name")
        ),
        platform.processor(),
    )
    return {
        "hostname": platform.node(),
        "platform": platform.platform(),
        "cpu_model": model,
        "cpu_count": os.cpu_count(),
        "cpu_affinity": sorted(os.sched_getaffinity(0)),
        "python": platform.python_version(),
        "memory_bytes": memory,
    }


class RunManifest:
    def __init__(self, path: Path, verifier, inputs: dict[str, Path], output: Path):
        self.path = path
        self.output = output
        self.counts = Counter()
        self.record = {
            "schema_version": 1,
            "run_id": str(uuid.uuid4()),
            "status": "running",
            "started_at": datetime.now(UTC).isoformat(),
            "code": code_state(),
            "machine": machine_state(),
            "config": asdict(verifier.config),
            "config_hash": verifier.config.config_hash,
            "worker_count": verifier.config.worker_count,
            "environment": verifier.environment.fingerprint,
            "inputs": {
                name: {"path": str(source.resolve()), "sha256": file_hash(source)}
                for name, source in inputs.items()
            },
            "output": str(output.resolve()),
        }
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("x", encoding="utf-8") as stream:
            json.dump(self.record, stream, indent=2, sort_keys=True)

    def finish(self, status: str):
        self.record.update(
            status=status,
            finished_at=datetime.now(UTC).isoformat(),
            verdict_counts=dict(self.counts),
            output_sha256=file_hash(self.output),
        )
        temporary = self.path.with_name(self.path.name + ".tmp")
        temporary.write_text(json.dumps(self.record, indent=2, sort_keys=True) + "\n")
        temporary.replace(self.path)
