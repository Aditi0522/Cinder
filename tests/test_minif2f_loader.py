import json
from dataclasses import asdict

import pytest

from harness.benchmarks import minif2f as m
from harness.schema import Problem

HEADER = "import Mathlib\n\nset_option maxHeartbeats 0\n\nopen BigOperators Real Nat Topology Rat\n\n"
D1 = (
    "theorem imo_1961_p1 (x y z a b : ℝ) (h₀ : 0 < x ∧ 0 < y ∧ 0 < z) (h₁ : x ≠ y) (h₂ : y ≠ z)\n"
    "  (h₃ : z ≠ x) (h₄ : x + y + z = a) (h₅ : x ^ 2 + y ^ 2 + z ^ 2 = b ^ 2) (h₆ : x * y = z ^ 2) :\n"
    "  0 < a ∧ b ^ 2 < a ^ 2 ∧ a ^ 2 < 3 * b ^ 2"
)
BASE = dict(header=HEADER, source_path="x", theorem_line=7, source_sha256="a", header_sha256="b", statement_sha256="c")
ROWS = [
    dict(BASE, name="imo_1961_p1", split="valid", declaration=D1),
    dict(BASE, name="t_nobinders", split="valid", declaration="theorem t_nobinders :\n  (2 : ℕ) + 2 = 4"),
    dict(BASE, name="t_test", split="test", declaration="theorem t_test (n : ℕ) (h : 0 < n) :\n  n ≥ 1"),
]
EXP = {"valid": 2, "test": 1}
EXC = {"problem_id": "imo_1961_p1", "tier": 1, "decision": "exclude", "reviewers": ["a", "b"], "notes": "vacuous"}


def make_mf(tmp_path, exclusions=None):
    mf = tmp_path / "mf"
    mf.mkdir()
    (mf / "extracted.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in ROWS), encoding="utf-8")
    if exclusions is not None:
        (mf / "exclusions.jsonl").write_text("".join(json.dumps(r) + "\n" for r in exclusions), encoding="utf-8")
    return mf


def build(mf, **kw):
    return m.build("env-test", mf=mf, verify=False, expected=EXP, **kw)


def loaded(mf, split):
    return [Problem(**json.loads(x)) for x in (mf / f"problems.{split}.jsonl").read_text(encoding="utf-8").splitlines()]


def test_split_with_binders():
    b, g = m.split_declaration(D1, "imo_1961_p1")
    assert b.startswith("(x y z a b : ℝ)") and b.endswith("(h₆ : x * y = z ^ 2)")
    assert g == "0 < a ∧ b ^ 2 < a ^ 2 ∧ a ^ 2 < 3 * b ^ 2"


def test_split_without_binders():
    assert m.split_declaration("theorem t :\n  (2 : ℕ) + 2 = 4", "t") == ("", "(2 : ℕ) + 2 = 4")


def test_colon_inside_goal_is_not_the_separator():
    b, g = m.split_declaration("theorem t (s : Set ℕ) : ∀ n : ℕ, n ∈ s", "t")
    assert b == "(s : Set ℕ)" and g == "∀ n : ℕ, n ∈ s"


def test_split_rejects_malformed():
    with pytest.raises(ValueError):
        m.split_declaration("theorem t x : ℕ", "t")
    with pytest.raises(ValueError):
        m.split_declaration("theorem other : ℕ", "t")


def test_preamble_drops_import_and_heartbeats():
    assert m.preamble_from_header(HEADER) == "open BigOperators Real Nat Topology Rat\n"
    with pytest.raises(ValueError):
        m.preamble_from_header("import Mathlib\nvariable (x : ℕ)\n")


def test_to_problem_fields():
    p = m.to_problem(ROWS[0], "env-test", "c" * 40, "open Real\n")
    assert p.problem_id == "minif2f.imo_1961_p1" and p.imports == ("Mathlib",)
    assert p.binders.startswith("(x y z a b : ℝ)") and "theorem" not in p.statement
    assert p.metadata["split"] == "valid" and p.metadata["benchmark_commit"] == "c" * 40


def test_deterministic_output(tmp_path):
    mf = make_mf(tmp_path)
    build(mf)
    first = {p.name: p.read_bytes() for p in mf.glob("*.json*")}
    build(mf)
    assert first == {p.name: p.read_bytes() for p in mf.glob("*.json*")}


def test_excluded_never_in_problem_files(tmp_path):
    mf = make_mf(tmp_path, [EXC])
    man = build(mf)
    for s in EXP:
        assert "imo_1961_p1" not in (mf / f"problems.{s}.jsonl").read_text(encoding="utf-8")
    assert man["excluded"] == {"minif2f.imo_1961_p1": "vacuous"}
    assert man["counts"]["valid"] == {"included": 1, "excluded": 1}
    record = json.loads((mf / "problems_excluded.jsonl").read_text(encoding="utf-8").splitlines()[0])
    with pytest.raises(TypeError):  # extra field: cannot be loaded as a Problem
        Problem(**record)


def test_exclusion_needs_two_reviewers(tmp_path):
    with pytest.raises(ValueError, match="two reviewers"):
        build(make_mf(tmp_path, [dict(EXC, reviewers=["a"])]))


def test_pending_review_blocks_build(tmp_path):
    mf = make_mf(tmp_path, [dict(EXC, decision="pending_review", reviewers=[])])
    with pytest.raises(ValueError, match="pending"):
        build(mf)
    assert build(mf, allow_pending=True)["excluded"] == {}


def test_split_counts_enforced(tmp_path):
    with pytest.raises(ValueError, match="split counts"):
        m.build("env-test", mf=make_mf(tmp_path), verify=False, expected={"valid": 244, "test": 244})


def test_evaluation_guard(tmp_path):
    mf = make_mf(tmp_path, [EXC])
    build(mf)
    man = mf / "manifest.json"
    valid = loaded(mf, "valid")
    m.check_problems(man, valid)
    with pytest.raises(ValueError, match="test split"):
        m.check_problems(man, loaded(mf, "test"))
    m.check_problems(man, loaded(mf, "test"), allow_test=True)
    record = json.loads((mf / "problems_excluded.jsonl").read_text(encoding="utf-8").splitlines()[0])
    record.pop("exclusion_reason")
    with pytest.raises(ValueError, match="excluded"):
        m.check_problems(man, [Problem(**record)])
    with pytest.raises(ValueError, match="not in the benchmark"):
        m.check_problems(man, [Problem(problem_id="minif2f.zzz", statement="x", environment_id="e")])
    with pytest.raises(ValueError, match="differs"):
        m.check_problems(man, [Problem(**{**asdict(valid[0]), "statement": "False"})])


REAL = m.MF / "extracted.jsonl"


@pytest.mark.skipif(not REAL.exists(), reason="extracted.jsonl not present")
def test_all_real_statements_split_and_roundtrip():
    rows = m.read_jsonl(REAL)
    assert len(rows) == 488
    for r in rows:
        _, goal = m.split_declaration(r["declaration"], r["name"])
        assert goal
