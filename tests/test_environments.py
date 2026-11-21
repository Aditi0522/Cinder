from dataclasses import replace

import pytest

from harness.environment import ROOT, LeanEnvironment, VerifierConfig
from harness.schema import Sample


def test_environment_projects_are_independent():
    core = VerifierConfig.load(ROOT / "configs/verifier.toml")
    mathlib = VerifierConfig.load(ROOT / "configs/minif2f.toml")
    assert core.project_root == ROOT
    assert mathlib.project_root == ROOT / "environments/minif2f"
    assert core.config_hash != mathlib.config_hash
    assert mathlib.mathlib_commit == "f897ebcf72cd16f89ab4577d0c826cd14afaafc7"


def test_toolchain_config_must_match_selected_project(tmp_path):
    (tmp_path / "lean-toolchain").write_text("leanprover/lean4:v4.23.0\n")
    config = replace(VerifierConfig.load(ROOT / "configs/verifier.toml"), project_dir=str(tmp_path))
    with pytest.raises(RuntimeError, match="pinned toolchain"):
        LeanEnvironment(config)


def test_mathlib_config_must_match_lockfile():
    config = replace(VerifierConfig.load(ROOT / "configs/verifier.toml"), mathlib_commit="0" * 40)
    with pytest.raises(RuntimeError, match="manifest pins differ"):
        LeanEnvironment(config)


@pytest.mark.parametrize(
    "field,value",
    [
        ("mathlib_commit", "latest"),
        ("benchmark_commit", "main"),
        ("memory_mb", 0),
        ("max_processes", 0),
        ("disk_mb", 0),
    ],
)
def test_unpinned_revisions_and_disabled_limits_are_rejected(field, value):
    config = VerifierConfig.load(ROOT / "configs/verifier.toml")
    with pytest.raises(ValueError):
        replace(config, **{field: value})


def test_ambiguous_additional_metadata_is_rejected():
    with pytest.raises(ValueError, match="Ambiguous"):
        Sample.from_record({"additional_fields": {"checkpoint": "first"}, "checkpoint": "second"})
