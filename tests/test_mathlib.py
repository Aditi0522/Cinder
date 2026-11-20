import json
from dataclasses import replace

import pytest

from harness.schema import Problem, Sample, sha256
from harness.verifier import ROOT, LeanVerifier, VerifierConfig

pytestmark = [pytest.mark.integration, pytest.mark.mathlib]


@pytest.fixture(scope="module")
def verifier():
    return LeanVerifier(VerifierConfig.load(ROOT / "configs/minif2f.toml"))


def fixtures():
    problems = [
        Problem(**json.loads(line))
        for line in (ROOT / "examples/minif2f/problems.jsonl").read_text().splitlines()
    ]
    samples = [
        Sample.from_record(json.loads(line))
        for line in (ROOT / "examples/minif2f/samples.jsonl").read_text().splitlines()
    ]
    return list(zip(problems, samples, strict=True))


@pytest.mark.parametrize("problem,sample", fixtures(), ids=lambda item: item.problem_id)
def test_upstream_reference_proofs_pass(verifier, problem, sample):
    result = verifier.verify(problem, sample)
    assert result.verdict == "pass", result.errors
    assert result.mathlib_commit == verifier.config.mathlib_commit
    assert result.peak_rss_kb and result.peak_rss_kb > 0


@pytest.mark.parametrize(
    "proof",
    [
        "by sorry",
        "by admit",
        "by exact ?_",
        "by native_decide",
        "theorem replaced : True := by trivial",
        "axiom cheat : False\ntheorem replaced : 17 * 18 % 4 = 2 := by omega",
        "by exact False.elim (sorryAx False false)",
    ],
)
def test_mathlib_cheats_are_rejected(verifier, proof):
    problem, sample = fixtures()[0]
    result = verifier.verify(problem, replace(sample, raw_output=proof))
    assert result.verdict == "fail", result.errors


def test_mathlib_lemma_output_with_renamed_binders(verifier):
    problem = Problem(
        "lemma",
        "a + b = b + a",
        verifier.config.environment_id,
        imports=("Mathlib",),
        binders="(a b : ℝ)",
    )
    sample = Sample(
        "lemma", "0", "human", 0, sha256(""), "lemma renamed (x y : ℝ) : x + y = y + x := by ring"
    )
    result = verifier.verify(problem, sample)
    assert result.verdict == "pass", result.errors
