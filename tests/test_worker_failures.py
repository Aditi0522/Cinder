"""Replay worker failures through the real subprocess/output-handling boundary."""

import json
import sys
from dataclasses import replace

import pytest

from harness.schema import Problem
from harness.verifier import ROOT, LeanVerifier, VerifierConfig


@pytest.fixture
def worker(monkeypatch):
    # Replace only the worker executable: keep _check's process and parser path.
    verifier = object.__new__(LeanVerifier)
    verifier.config = VerifierConfig.load(ROOT / "configs/verifier.toml")
    verifier.lean = ROOT / "unused-lean"

    def replay(events, exit_code=0, sleep_seconds=0):
        script = (
            "import os, sys, time\n"
            f"sys.stdout.write({events!r})\n"
            "sys.stdout.flush()\n"
            f"time.sleep({sleep_seconds!r})\n"
            f"code = {exit_code}\n"
            "if code < 0: os.kill(os.getpid(), -code)\n"
            "os._exit(code)\n"
        )
        monkeypatch.setattr(verifier, "_sandbox_command", lambda *_: [sys.executable, "-c", script])
        if sleep_seconds:
            verifier.config = replace(verifier.config, timeout_seconds=0.3)
        problem = Problem("p", "True", verifier.config.environment_id)
        return verifier._check(problem, "by trivial")[:3]

    return replay


def diagnostic(message, severity="information"):
    return json.dumps({"severity": severity, "data": message}) + "\n"


CONTEXT_READY = diagnostic("CINDER_CONTEXT_READY")
CANDIDATE_READY = json.dumps({"cinder_event": "candidate_ready"}) + "\n"


@pytest.mark.parametrize("ready", [False, True])
@pytest.mark.parametrize(
    "tail,exit_code",
    [
        ("fatal runtime error\n", 1),
        ("null\n", 1),
        ('{"severity": [], "data": "bad diagnostic"}\n', 1),
        ("", 37),
        ("", -9),
    ],
)
def test_runtime_failures_are_attributed_to_execution_phase(worker, ready, tail, exit_code):
    events = CONTEXT_READY + (CANDIDATE_READY if ready else "") + tail
    verdict, errors, _ = worker(events, exit_code)
    assert verdict == ("candidate_crash" if ready else "infrastructure_error")
    assert errors


def test_trusted_context_error_cannot_be_overridden_by_candidate_marker(worker):
    events = diagnostic("unknown namespace `Missing`", "error") + CONTEXT_READY + CANDIDATE_READY
    verdict, _, _ = worker(events, -9)
    assert verdict == "infrastructure_error"


def test_fatal_exit_is_not_hidden_by_an_earlier_candidate_diagnostic(worker):
    events = CONTEXT_READY + CANDIDATE_READY + diagnostic("tactic failed", "error")
    verdict, errors, _ = worker(events, -9)
    assert verdict == "candidate_crash"
    assert any("-9" in error["message"] for error in errors)


@pytest.mark.parametrize("ready", [False, True])
def test_timeout_is_attributed_to_execution_phase(worker, ready):
    events = CONTEXT_READY + (CANDIDATE_READY if ready else "")
    verdict, errors, _ = worker(events, sleep_seconds=2)
    assert verdict == ("timeout" if ready else "infrastructure_error")
    assert any("timeout" in error["message"] for error in errors)


def test_normal_candidate_error_remains_a_proof_failure(worker):
    verdict, errors, _ = worker(
        CONTEXT_READY + CANDIDATE_READY + diagnostic("unknown identifier 'x'", "error"),
        1,
    )
    assert verdict == "fail"
    assert errors[0]["message"] == "unknown identifier 'x'"


def test_missing_success_report_is_still_an_infrastructure_error(worker):
    verdict, _, _ = worker(CONTEXT_READY + CANDIDATE_READY)
    assert verdict == "infrastructure_error"
