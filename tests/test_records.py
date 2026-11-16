from dataclasses import replace

import pytest

from harness.classifier import classify, repetition_ratio
from harness.extraction import extract_proof
from harness.schema import Problem, sha256


def test_problem_hash_covers_statement_and_context():
    problem = Problem("p", "True", "lean-core-4.24.0")
    assert problem.problem_hash == replace(problem).problem_hash
    for field in (
        {"statement": "False"},
        {"preamble": "open Nat"},
        {"imports": ("Lean",)},
        {"environment_id": "another"},
    ):
        assert problem.problem_hash != replace(problem, **field).problem_hash


def test_markdown_extraction():
    assert extract_proof("Proof:\n```lean4\nby trivial\n```", "markdown") == "by trivial"


@pytest.mark.parametrize(
    "raw,mode",
    [
        ("", "proof"),
        ("plain text", "markdown"),
        ("```lean\nby trivial\n```\n```lean\nby trivial\n```", "markdown"),
        ("by trivial", "guess"),
    ],
)
def test_extraction_fails_closed(raw, mode):
    with pytest.raises(ValueError):
        extract_proof(raw, mode)


@pytest.mark.parametrize(
    "verdict,message,expected",
    [
        ("fail", "unknown identifier 'x'", "unknown_identifier"),
        ("fail", "type mismatch", "type_mismatch"),
        ("fail", "tactic failed", "tactic_failed"),
        ("fail", "unsolved goals", "tactic_failed"),
        ("fail", "CINDER_PARSE: expected token", "syntax_error"),
        ("fail", "CINDER_POLICY: forbidden syntax sorry", "contains_sorry"),
        ("fail", "CINDER_AXIOMS: disallowed axioms [sorryAx]", "contains_sorry"),
        ("fail", "CINDER_POLICY: forbidden syntax run_tac", "policy_violation"),
        ("timeout", "Lean wall-clock timeout", "timeout"),
        ("extraction_error", "Expected exactly one fenced Lean proof block", "no_code_block"),
        ("infrastructure_error", "worker died", "infrastructure_error"),
    ],
)
def test_classifier(verdict, message, expected):
    assert expected in classify(verdict, [{"message": message}], "", False)


def test_repetition_and_truncation_can_coexist_with_failure():
    text = "repeat these same four tokens " * 50
    assert repetition_ratio(text) > 0.9
    assert classify("fail", [{"message": "unknown identifier"}], text, True) == [
        "truncated",
        "repetition",
        "unknown_identifier",
    ]
    assert repetition_ratio("") == 0
    assert repetition_ratio("one two") == 0
    assert sha256("") == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"


def test_invalid_ngram_size():
    with pytest.raises(ValueError):
        repetition_ratio("text", 0)
