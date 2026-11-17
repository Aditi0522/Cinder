"""Aggregate cgroup limits and a read-only bubblewrap filesystem."""

import shutil
import subprocess
import uuid
from pathlib import Path

from harness.environment import LeanEnvironment, VerifierConfig


class Sandbox:
    def __init__(self, environment: LeanEnvironment, config: VerifierConfig):
        self.environment = environment
        self.config = config
        for command in ("bwrap", "systemd-run", "prlimit"):
            if not shutil.which(command):
                raise RuntimeError(f"Sandbox requires {command}")
        # This also checks cgroup delegation. No silent unbounded fallback.
        subprocess.run(
            self.command(Path.cwd(), ["/usr/bin/true"]),
            check=True,
            capture_output=True,
            text=True,
            timeout=15,
        )

    def command(self, work: Path, command: list[str]) -> list[str]:
        args = [
            "systemd-run",
            "--user",
            "--scope",
            "--quiet",
            "--collect",
            f"--unit=cinder-{uuid.uuid4().hex}",
            f"--property=MemoryMax={self.config.memory_mb * 1024**2}",
            "--property=MemorySwapMax=0",
            f"--property=TasksMax={self.config.max_processes}",
            "--property=OOMPolicy=kill",
            "prlimit",
            "--core=0",
            "--fsize=2000000",
            "--nofile=256",
            "--",
            "bwrap",
            "--unshare-all",
            "--unshare-user",
            "--disable-userns",
            "--die-with-parent",
            "--new-session",
            "--clearenv",
            "--ro-bind",
            "/usr",
            "/usr",
        ]
        for path in ("/lib", "/lib64"):
            if Path(path).exists():
                args += ["--ro-bind", path, path]
        toolchain = self.environment.toolchain
        args += ["--ro-bind", str(toolchain), str(toolchain)]
        sandbox_paths = []
        for index, path in enumerate(self.environment.lean_paths):
            if path.exists():
                target = f"/lean-lib/{index}"
                args += ["--ro-bind", str(path), target]
                sandbox_paths.append(target)
        args += [
            "--ro-bind",
            str(work),
            "/work",
            "--proc",
            "/proc",
            "--dev",
            "/dev",
            "--size",
            str(self.config.disk_mb * 1024**2),
            "--tmpfs",
            "/tmp",
            "--remount-ro",
            "/dev",
            "--remount-ro",
            "/",
            "--setenv",
            "LEAN_PATH",
            ":".join(sandbox_paths),
            "--setenv",
            "HOME",
            "/tmp",
            "--setenv",
            "PATH",
            f"{toolchain}/bin:/usr/bin",
            "--chdir",
            "/work",
        ]
        return args + command
