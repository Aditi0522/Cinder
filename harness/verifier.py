"""Fresh, isolated Lean processes; no candidate state survives between samples."""

import json
import os
import re
import signal
import subprocess
import tempfile
import time
from pathlib import Path

from harness.classifier import classify
from harness.environment import ROOT, LeanEnvironment, VerifierConfig
from harness.extraction import extract_proof
from harness.resources import process_tree_rss
from harness.sandbox import Sandbox
from harness.schema import Problem, Sample, VerificationResult

__all__ = ["ROOT", "LeanVerifier", "VerifierConfig"]


def _diagnostic(item: dict) -> dict:
    source = "candidate" if item.get("fileName") == "candidate.lean" else "driver"
    position = item.get("pos")
    parsed = re.search(r"CINDER_PARSE: candidate\.lean:(\d+):(\d+):", item["data"])
    if parsed:
        source = "candidate"
        position = {"line": int(parsed[1]), "column": int(parsed[2])}
    return {
        "message": item["data"],
        "position": position,
        "source": source,
        "end_position": None if parsed else item.get("endPos"),
    }


def _worker_result(
    raw: bytes, returncode: int, timed_out: bool
) -> tuple[str, list[dict], list[str]]:
    """Attribute runtime failures to the last observed, flushed execution phase."""
    messages = []
    errors = []
    runtime_errors = []
    candidate_started = False
    trusted_failure = False
    for line in raw.decode("utf-8", errors="replace").splitlines():
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            item = None
        if item == {"cinder_event": "candidate_ready"}:
            # A marker cannot erase failures already observed in trusted setup.
            if not errors and not runtime_errors:
                candidate_started = True
            continue
        if (
            not isinstance(item, dict)
            or not isinstance(item.get("severity"), str)
            or item.get("severity") not in {"information", "warning", "error"}
            or not isinstance(item.get("data"), str)
        ):
            runtime_errors.append({"message": line, "position": None})
            continue
        messages.append(item)
        if item["severity"] == "error":
            errors.append(_diagnostic(item))
            if not candidate_started or item["data"].startswith("CINDER_INTERNAL:"):
                trusted_failure = True

    if len(raw) > 2_000_000:
        runtime_errors.append({"message": "Lean diagnostic output exceeded 2 MB", "position": None})
    if timed_out:
        errors += runtime_errors + [{"message": "Lean wall-clock timeout", "position": None}]
        return (
            "timeout" if candidate_started and not trusted_failure else "infrastructure_error",
            errors,
            [],
        )
    # Lean exits 1 for ordinary diagnostics. Other statuses (including negative
    # signal codes), or status 1 without diagnostics, describe abnormal execution.
    if returncode not in (0, 1) or (returncode and not errors):
        runtime_errors.append(
            {
                "message": f"Lean exited with code {returncode}",
                "position": None,
            }
        )
    if trusted_failure:
        return "infrastructure_error", errors + runtime_errors, []
    if runtime_errors:
        verdict = "candidate_crash" if candidate_started else "infrastructure_error"
        return verdict, errors + runtime_errors, []
    if errors:
        return "fail", errors, []

    reports = [
        item["data"].removeprefix("CINDER_RESULT:")
        for item in messages
        if item["data"].startswith("CINDER_RESULT:")
    ]
    if not candidate_started or len(reports) != 1:
        return (
            "infrastructure_error",
            [
                {
                    "message": "Missing or ambiguous trusted verifier result or candidate phase marker",
                    "position": None,
                }
            ],
            [],
        )
    try:
        report = json.loads(reports[0])
        if (
            not isinstance(report, dict)
            or report.get("verdict") != "pass"
            or not isinstance(report.get("axioms"), list)
            or not all(isinstance(axiom, str) for axiom in report["axioms"])
        ):
            raise ValueError("Invalid trusted verifier result")
    except ValueError as error:
        return "infrastructure_error", [{"message": str(error), "position": None}], []
    return "pass", [], report["axioms"]


class LeanVerifier:
    def __init__(self, config: VerifierConfig):
        self.config = config
        self.environment = LeanEnvironment(config)
        self.lean = self.environment.lean
        self.sandbox = Sandbox(self.environment, config)

    def _sandbox_command(self, work: Path, command: list[str]) -> list[str]:
        return self.sandbox.command(work, command)

    def verify(self, problem: Problem, sample: Sample) -> VerificationResult:
        started = time.monotonic()
        proof = None
        errors = []
        axioms = []
        verdict = "infrastructure_error"
        peak_rss_kb = None
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
                verdict, errors, axioms, peak_rss_kb = self._check(problem, proof)
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
            metadata=sample.metadata,
            additional_fields=sample.additional_fields,
            peak_rss_kb=peak_rss_kb,
        )
        result.labels = classify(verdict, errors, sample.raw_output, sample.truncated)
        return result

    def _check(self, problem: Problem, proof: str) -> tuple[str, list[dict], list[str], int | None]:
        if any(not re.fullmatch(r"[A-Za-z_][A-Za-z_0-9.]*", name) for name in problem.imports):
            raise ValueError("Invalid trusted import name")
        with tempfile.TemporaryDirectory(prefix="cinder-") as directory:
            work = Path(directory)
            (work / "statement.txt").write_text(problem.statement, encoding="utf-8")
            (work / "proof.txt").write_text(proof, encoding="utf-8")
            (work / "binders.txt").write_text(problem.binders, encoding="utf-8")
            source = "import Cinder.Verifier\n"
            source += "".join(f"import {name}\n" for name in problem.imports)
            source += problem.preamble + "\n"
            source += "set_option Elab.async false\n"
            source += f"set_option maxHeartbeats {self.config.max_heartbeats}\n"
            source += "set_option autoImplicit false\n"
            source += "#cinder_context_ready\n"
            source += '#cinder_verify "/work/statement.txt" "/work/proof.txt" "/work/binders.txt"\n'
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
                    stdin=subprocess.DEVNULL,
                    stdout=output,
                    stderr=subprocess.STDOUT,
                    start_new_session=True,
                )
                timed_out = False
                peak = 0
                deadline = time.monotonic() + self.config.timeout_seconds
                while True:
                    peak = max(peak, process_tree_rss(process.pid)[0])
                    remaining = deadline - time.monotonic()
                    try:
                        process.wait(timeout=max(0, min(0.05, remaining)))
                        break
                    except subprocess.TimeoutExpired:
                        if remaining > 0:
                            continue
                        timed_out = True
                        try:
                            os.killpg(process.pid, signal.SIGKILL)
                        except ProcessLookupError:
                            pass
                        process.wait()
                        break
                output.seek(0)
                raw = output.read(2_000_001)
            return (*_worker_result(raw, process.returncode, timed_out), peak)
