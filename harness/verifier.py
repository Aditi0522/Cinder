"""Fresh, isolated Lean processes; no candidate state survives between samples."""

import json
import os
import re
import shutil
import signal
import subprocess
import tempfile
import time
import tomllib
from dataclasses import dataclass
from pathlib import Path

from harness.classifier import classify
from harness.extraction import extract_proof
from harness.schema import Problem, Sample, VerificationResult, sha256

ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class VerifierConfig:
    environment_id: str
    lean_toolchain: str
    mathlib_commit: str
    timeout_seconds: float
    max_heartbeats: int
    workers: int

    @classmethod
    def load(cls, path: Path) -> "VerifierConfig":
        config = cls(**tomllib.loads(path.read_text()))
        if config.timeout_seconds <= 0 or config.max_heartbeats < 1 or config.workers < 0:
            raise ValueError("Timeout and heartbeats must be positive; workers must be nonnegative")
        if config.mathlib_commit:
            raise ValueError("This bring-up backend supports the core-only environment")
        return config

    @property
    def worker_count(self) -> int:
        if self.workers:
            return self.workers
        cores = len(os.sched_getaffinity(0)) if hasattr(os, "sched_getaffinity") else os.cpu_count()
        return max(1, (cores or 1) - 1)

    @property
    def config_hash(self) -> str:
        from dataclasses import asdict

        return sha256(json.dumps(asdict(self), sort_keys=True))


class LeanVerifier:
    def __init__(self, config: VerifierConfig):
        self.config = config
        elan = shutil.which("elan") or str(Path.home() / ".elan/bin/elan")
        self.lean = Path(
            subprocess.check_output([elan, "which", "lean"], cwd=ROOT, text=True).strip()
        ).resolve()
        self.toolchain = self.lean.parent.parent
        actual_version = subprocess.check_output([str(self.lean), "--version"], text=True)
        expected = config.lean_toolchain.rsplit(":v", 1)[-1]
        if not re.search(rf"version {re.escape(expected)}(?:,|\))", actual_version):
            raise RuntimeError(f"Lean version mismatch: {actual_version.strip()}")
        if (ROOT / "lean-toolchain").read_text().strip() != config.lean_toolchain:
            raise RuntimeError("Config does not match this project's pinned toolchain")
        self.bwrap = shutil.which("bwrap")
        if not self.bwrap:
            raise RuntimeError("bubblewrap is required; install it before verification")
        if not (ROOT / ".lake/build/lib/lean/Cinder/Verifier.olean").exists():
            raise RuntimeError("Verifier module is not built; run scripts/setup.sh")
        # Fail closed if namespaces are disabled. Never silently run candidates on the host.
        subprocess.run(
            self._sandbox_command(ROOT, ["/usr/bin/true"]),
            check=True,
            capture_output=True,
            text=True,
            timeout=10,
        )

    def _sandbox_command(self, work: Path, command: list[str]) -> list[str]:
        args = [
            self.bwrap,
            "--unshare-all",
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
        args += [
            "--ro-bind",
            str(self.toolchain),
            str(self.toolchain),
            "--ro-bind",
            str(ROOT / ".lake/build/lib/lean"),
            "/cinder-lib",
            "--bind",
            str(work),
            "/work",
            "--proc",
            "/proc",
            "--dev",
            "/dev",
            "--tmpfs",
            "/tmp",
            "--setenv",
            "LEAN_PATH",
            "/cinder-lib",
            "--setenv",
            "HOME",
            "/tmp",
            "--setenv",
            "PATH",
            f"{self.lean.parent}:/usr/bin",
            "--chdir",
            "/work",
        ]
        return args + command

    def verify(self, problem: Problem, sample: Sample) -> VerificationResult:
        started = time.monotonic()
        proof = None
        errors = []
        axioms = []
        verdict = "infrastructure_error"
        try:
            if sample.problem_id != problem.problem_id:
                raise ValueError("Sample and problem ids differ")
            if problem.environment_id != self.config.environment_id:
                raise ValueError("Problem requires a different environment")
            try:
                proof = extract_proof(sample.raw_output, sample.output_format)
            except ValueError as error:
                verdict = "extraction_error"
                errors = [{"message": str(error), "position": None}]
            else:
                verdict, errors, axioms = self._check(problem, proof)
        except (OSError, ValueError, subprocess.SubprocessError) as error:
            errors = [{"message": str(error), "position": None}]
        result = VerificationResult(
            **{
                key: getattr(sample, key)
                for key in (
                    "problem_id",
                    "sample_id",
                    "model",
                    "seed",
                    "prompt_hash",
                    "raw_output",
                    "token_count",
                    "truncated",
                )
            },
            extracted_proof=proof,
            verdict=verdict,
            errors=errors,
            wall_time_seconds=time.monotonic() - started,
            lean_toolchain=self.config.lean_toolchain,
            mathlib_commit=self.config.mathlib_commit or None,
            environment_id=problem.environment_id,
            problem_hash=problem.problem_hash,
            config_hash=self.config.config_hash,
            axioms=axioms,
        )
        result.labels = classify(verdict, errors, sample.raw_output, sample.truncated)
        return result

    def _check(self, problem: Problem, proof: str) -> tuple[str, list[dict], list[str]]:
        if any(not re.fullmatch(r"[A-Za-z_][A-Za-z_0-9.]*", name) for name in problem.imports):
            raise ValueError("Invalid trusted import name")
        with tempfile.TemporaryDirectory(prefix="cinder-") as directory:
            work = Path(directory)
            (work / "statement.txt").write_text(problem.statement, encoding="utf-8")
            (work / "proof.txt").write_text(proof, encoding="utf-8")
            source = "import Cinder.Verifier\n"
            source += "".join(f"import {name}\n" for name in problem.imports)
            source += problem.preamble + "\n"
            source += "set_option Elab.async false\n"
            source += "#cinder_context_ready\n"
            source += '#cinder_verify "/work/statement.txt" "/work/proof.txt"\n'
            (work / "Candidate.lean").write_text(source, encoding="utf-8")
            command = self._sandbox_command(
                work,
                [
                    str(self.lean),
                    "--json",
                    "-j1",
                    f"-DmaxHeartbeats={self.config.max_heartbeats}",
                    "/work/Candidate.lean",
                ],
            )
            with tempfile.TemporaryFile() as output:
                process = subprocess.Popen(
                    command,
                    stdout=output,
                    stderr=subprocess.STDOUT,
                    start_new_session=True,
                )
                try:
                    process.wait(timeout=self.config.timeout_seconds)
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGKILL)
                    process.wait()
                    return "timeout", [{"message": "Lean wall-clock timeout", "position": None}], []
                output.seek(0)
                raw = output.read(2_000_001)
            if len(raw) > 2_000_000:
                return (
                    "infrastructure_error",
                    [
                        {
                            "message": "Lean diagnostic output exceeded 2 MB",
                            "position": None,
                        }
                    ],
                    [],
                )
            messages = []
            for line in raw.decode("utf-8", errors="replace").splitlines():
                try:
                    messages.append(json.loads(line))
                except json.JSONDecodeError:
                    return "infrastructure_error", [{"message": line, "position": None}], []
            errors = [
                {"message": item.get("data", ""), "position": item.get("pos")}
                for item in messages
                if item.get("severity") == "error"
            ]
            if errors:
                context_marker = next(
                    (
                        index
                        for index, item in enumerate(messages)
                        if item.get("data") == "CINDER_CONTEXT_READY"
                    ),
                    len(messages),
                )
                context_errors = any(
                    item.get("severity") == "error" for item in messages[:context_marker]
                )
                if context_errors:
                    return "infrastructure_error", errors, []
                if any(
                    "CINDER_STATEMENT:" in error["message"]
                    or "CINDER_CONTEXT:" in error["message"]
                    or "unknown module prefix" in error["message"]
                    or "CINDER_INTERNAL:" in error["message"]
                    for error in errors
                ):
                    return "infrastructure_error", errors, []
                return "fail", errors, []
            if process.returncode:
                return (
                    "infrastructure_error",
                    [
                        {
                            "message": f"Lean exited with code {process.returncode}",
                            "position": None,
                        }
                    ],
                    [],
                )
            reports = [
                item["data"].removeprefix("CINDER_RESULT:")
                for item in messages
                if item.get("data", "").startswith("CINDER_RESULT:")
            ]
            if len(reports) != 1:
                return (
                    "infrastructure_error",
                    [
                        {
                            "message": "Missing or ambiguous trusted verifier result",
                            "position": None,
                        }
                    ],
                    [],
                )
            report = json.loads(reports[0])
            if report.get("verdict") != "pass":
                raise ValueError("Invalid trusted verifier result")
            return "pass", [], report["axioms"]
