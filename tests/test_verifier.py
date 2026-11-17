from dataclasses import replace

import pytest

from harness.schema import Problem, Sample, sha256
from harness.verifier import ROOT, LeanVerifier, VerifierConfig

pytestmark = pytest.mark.integration


@pytest.fixture(scope="module")
def verifier():
    # Missing Lean/sandbox infrastructure must fail the gate, not skip its tests.
    return LeanVerifier(VerifierConfig.load(ROOT / "configs/verifier.toml"))


def run(verifier, statement, proof, preamble=""):
    problem = Problem("sanity", statement, verifier.config.environment_id, preamble=preamble)
    sample = Sample("sanity", "0", "human-sanity", 0, sha256(""), proof)
    return verifier.verify(problem, sample)


@pytest.mark.parametrize(
    "statement,proof",
    [
        ("True", "by trivial"),
        ("True", "True.intro"),
        ("∀ n : Nat, n = n", "by intro n; rfl"),
        ("2 + 2 = (4 : Nat)", "by decide"),
        ("∀ p : Prop, p → p", "by intro p h; exact h"),
        ("True ∧ True", "by constructor <;> trivial"),
        ("∀ p q : Prop, p ∧ q → q ∧ p", "by intro p q h; exact ⟨h.2, h.1⟩"),
        ("True", "by /- sorry in a comment is not a hole -/ trivial"),
        ("True", 'by let sorryText := "sorry"; exact True.intro'),
        ("∀ p : Prop, p ∨ ¬p", "by intro p; exact Classical.em p"),
    ],
)
def test_human_proofs_pass(verifier, statement, proof):
    result = run(verifier, statement, proof)
    assert result.verdict == "pass", result.errors
    assert set(result.axioms) <= {"propext", "Classical.choice", "Quot.sound"}


@pytest.mark.parametrize(
    "proof",
    [
        "by sorry",
        "by admit",
        "sorryAx False false",
        "by exact (by sorry)",
        "by exact ?_",
        "by skip",
        "by exact True.intro",
        "by exact fabricated_lemma",
        "by trivial\naxiom injected : False",
        "by trivial\ntheorem other : True := by trivial",
        "by trivial\nimport Lean",
        "by trivial\n#print axioms cinder_verified_candidate",
        "by set_option maxHeartbeats 0 in trivial",
        "by run_tac do pure ()",
        "by exact (by run_tac do pure ())",
        "by exact «sorryAx» False false",
        "by exact Lean.ofReduceBool (α := False)",
        "by native_decide",
        "by exact (by decide : True)",
        'by trivial\n#eval IO.println "CINDER_RESULT:{\\"verdict\\":\\"pass\\"}"',
    ],
)
def test_injected_cheats_and_wrong_proofs_fail(verifier, proof):
    result = run(verifier, "False", proof)
    assert result.verdict == "fail", (result.verdict, result.errors)


def test_indirect_sorry_is_caught_by_kernel_axiom_audit(verifier):
    result = run(verifier, "False", "hiddenHole", "theorem hiddenHole : False := by sorry")
    assert result.verdict == "fail"
    assert "CINDER_AXIOMS" in str(result.errors)


def test_custom_axiom_is_caught_by_kernel_axiom_audit(verifier):
    result = run(verifier, "False", "customFalse", "axiom customFalse : False")
    assert result.verdict == "fail"
    assert "CINDER_AXIOMS" in str(result.errors)


def test_axiom_audit_respects_trusted_namespace(verifier):
    result = run(verifier, "False", "customFalse", "namespace Bench\naxiom customFalse : False")
    assert result.verdict == "fail", result.errors
    assert "CINDER_AXIOMS" in str(result.errors)


@pytest.mark.parametrize("statement", ["not_a_type", "∀", "Nat"])
def test_bad_trusted_statement_is_an_infrastructure_error(verifier, statement):
    result = run(verifier, statement, "by trivial")
    assert result.verdict == "infrastructure_error", result.errors
    assert result.labels == ["infrastructure_error"]


def test_bad_trusted_context_is_an_infrastructure_error(verifier):
    result = run(verifier, "True", "by trivial", "open MissingNamespace")
    assert result.verdict == "infrastructure_error", result.errors


def test_repeat_is_deterministic(verifier):
    results = [run(verifier, "∀ n : Nat, n = n", "by intro n; rfl") for _ in range(3)]
    assert [result.verdict for result in results] == ["pass"] * 3
    assert len({result.problem_hash for result in results}) == 1
    assert len({result.config_hash for result in results}) == 1


def test_wall_clock_timeout_kills_worker(verifier):
    short = LeanVerifier(replace(verifier.config, timeout_seconds=1.0))
    result = run(short, "True", "by sleep 5000; trivial")
    assert result.verdict == "timeout", result.errors
    assert result.wall_time_seconds < 5
    # A killed candidate cannot contaminate the next verification.
    assert run(verifier, "True", "by trivial").verdict == "pass"


def test_environment_mismatch_is_not_a_model_failure(verifier):
    problem = Problem("p", "True", "wrong-environment")
    sample = Sample("p", "0", "human", 0, sha256(""), "by trivial")
    assert verifier.verify(problem, sample).verdict == "infrastructure_error"


@pytest.mark.parametrize(
    "output",
    [
        "",
        'Cinder.workerStdout.putStrLn "fatal runtime error"; Cinder.workerStdout.flush; ',
    ],
)
def test_abrupt_candidate_exit_is_a_candidate_crash(verifier, output):
    preamble = f'elab "cinder_abort" : tactic => do {output}IO.Process.exit 37'
    result = run(verifier, "True", "by cinder_abort", preamble)
    assert result.verdict == "candidate_crash", result.errors
    assert result.labels == ["candidate_crash"]
    assert any("37" in error["message"] for error in result.errors)


def test_crash_in_trusted_statement_remains_an_infrastructure_error(verifier):
    preamble = 'elab "cinder_abort_type" : term => do IO.Process.exit 37'
    result = run(verifier, "cinder_abort_type", "by trivial", preamble)
    assert result.verdict == "infrastructure_error", result.errors
    assert result.labels == ["infrastructure_error"]
