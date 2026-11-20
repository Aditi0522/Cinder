from dataclasses import replace

import pytest

from harness.schema import Problem, Sample, sha256
from harness.verifier import ROOT, LeanVerifier, VerifierConfig

pytestmark = pytest.mark.integration


@pytest.fixture(scope="module")
def verifier():
    return LeanVerifier(VerifierConfig.load(ROOT / "configs/verifier.toml"))


def check(verifier, proof, **kwargs):
    problem = Problem(
        "sig",
        "n + 1 = 2",
        verifier.config.environment_id,
        binders="(n : Nat) (h : n = 1)",
        **kwargs,
    )
    return verifier.verify(problem, Sample("sig", "0", "human", 0, sha256(""), proof))


@pytest.mark.parametrize(
    "proof",
    [
        "by omega",
        "theorem renamed (x : Nat) (hx : x = 1) : x + 1 = 2 := by omega",
        "theorem another (n : Nat) (h : n = 1) : n + 1 = 2 := by rw [h]",
    ],
)
def test_binders_hypotheses_and_complete_declarations_pass(verifier, proof):
    result = check(verifier, proof)
    assert result.verdict == "pass", result.errors


@pytest.mark.parametrize(
    "proof",
    [
        "theorem bad (x : Nat) (h : False) : x + 1 = 2 := by contradiction",
        "theorem bad (x : Nat) (h : x = 2) : x + 1 = 3 := by omega",
        "theorem bad (x : Nat) (h : x = 1) (extra : False) : x + 1 = 2 := by omega",
        "theorem bad (x : Nat) (h : x = 1) : True := by trivial",
        "@[simp] theorem bad (n : Nat) (h : n = 1) : n + 1 = 2 := by omega",
        "axiom bad : False",
        "def helper := 1\ntheorem bad : True := by trivial",
        "theorem bad (n : Nat) (h : n = 1) : n + 1 = 2 := by omega\naxiom cheat : False",
    ],
)
def test_changed_signatures_and_auxiliary_commands_are_rejected(verifier, proof):
    result = check(verifier, proof)
    assert result.verdict == "fail", result.errors


def test_local_have_and_let_are_allowed(verifier):
    result = check(verifier, "by\n  have localFact : n = 1 := h\n  let one := 1\n  omega")
    assert result.verdict == "pass", result.errors


def test_implicit_binders_and_typeclass_hypotheses(verifier):
    problem = Problem(
        "implicit",
        "x = x",
        verifier.config.environment_id,
        binders="{α : Type} [Inhabited α] (x : α)",
    )
    sample = Sample("implicit", "0", "human", 0, sha256(""), "by rfl")
    result = verifier.verify(problem, sample)
    assert result.verdict == "pass", result.errors


def test_trusted_preamble_cannot_override_heartbeat_budget(verifier):
    preamble = """set_option maxHeartbeats 0
elab "assert_budget" : tactic => do
  unless (← Lean.getOptions).getNat `maxHeartbeats 0 == 200000 do
    throwError "wrong heartbeat budget"
  Lean.Elab.Tactic.evalTactic (← `(tactic| trivial))
"""
    problem = Problem("budget", "True", verifier.config.environment_id, preamble=preamble)
    sample = Sample("budget", "0", "human", 0, sha256(""), "by assert_budget")
    result = verifier.verify(problem, sample)
    assert result.verdict == "pass", result.errors


@pytest.mark.parametrize(
    "raw,mode,line,column",
    [
        ("by\n  have α : Nat := 0\n  exact nonexistent", "proof", 3, 8),
        ("Explanation\n\n```lean\nby\n  exact nonexistent\n```", "markdown", 2, 8),
        (
            "theorem other (n : Nat) (h : n = 1) : n + 1 = 2 := by\n  exact nonexistent",
            "declaration",
            2,
            8,
        ),
        ("by\n  exact )", "proof", 2, 8),
        ("by\n  sorry", "proof", 2, 2),
    ],
)
def test_positions_are_relative_to_extracted_candidate(verifier, raw, mode, line, column):
    problem = Problem("position", "True", verifier.config.environment_id)
    if mode == "declaration":
        problem = replace(problem, binders="(n : Nat) (h : n = 1)", statement="n + 1 = 2")
    sample = Sample("position", "0", "human", 0, sha256(""), raw, output_format=mode)
    result = verifier.verify(problem, sample)
    assert result.verdict == "fail", result.errors
    assert any(
        error.get("source") == "candidate" and error["position"] == {"line": line, "column": column}
        for error in result.errors
    ), result.errors
