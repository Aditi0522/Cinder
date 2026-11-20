import hashlib
import json
import subprocess

from harness.verifier import ROOT


def invoke(
    output, samples=ROOT / "examples/samples.jsonl", problems=ROOT / "examples/problems.jsonl"
):
    return subprocess.run(
        [
            "cinder",
            "--problems",
            str(problems),
            "--samples",
            str(samples),
            "--output",
            str(output),
        ],
        capture_output=True,
        text=True,
        check=False,
    )


def test_jsonl_evaluation_and_overwrite_protection(tmp_path):
    output = tmp_path / "results.jsonl"
    result = invoke(output)
    assert result.returncode == 0, result.stderr
    original = output.read_text()
    records = [json.loads(line) for line in original.splitlines()]
    assert [record["verdict"] for record in records] == ["pass", "fail"]
    assert all(record["problem_hash"] and record["config_hash"] for record in records)
    assert records[1]["labels"] == ["contains_sorry"]
    assert invoke(output).returncode == 2
    assert output.read_text() == original
    manifest = json.loads(output.with_suffix(".manifest.json").read_text())
    assert manifest["status"] == "complete"
    assert manifest["verdict_counts"] == {"pass": 1, "fail": 1}
    assert manifest["output_sha256"] == hashlib.sha256(output.read_bytes()).hexdigest()
    assert manifest["code"]["git_commit"]
    assert manifest["code"]["source_hash"]
    assert manifest["environment"]["lean_version"]
    assert manifest["machine"]["cpu_count"] > 0
    assert all(row["run_id"] == manifest["run_id"] for row in records)


def test_unknown_problem_is_rejected_before_creating_output(tmp_path):
    sample = json.loads((ROOT / "examples/samples.jsonl").read_text().splitlines()[0])
    sample["problem_id"] = "unknown"
    samples = tmp_path / "samples.jsonl"
    samples.write_text(json.dumps(sample) + "\n")
    output = tmp_path / "results.jsonl"
    result = invoke(output, samples)
    assert result.returncode == 2
    assert "Unknown problem id" in result.stderr
    assert not output.exists()


def test_candidate_crash_is_recorded_without_aborting_batch(tmp_path):
    problem = json.loads((ROOT / "examples/problems.jsonl").read_text().splitlines()[0])
    problem["preamble"] = 'elab "cinder_abort" : tactic => do IO.Process.exit 37'
    problems = tmp_path / "problems.jsonl"
    problems.write_text(json.dumps(problem) + "\n")
    sample = json.loads((ROOT / "examples/samples.jsonl").read_text().splitlines()[0])
    crash = {**sample, "sample_id": "crash", "raw_output": "by cinder_abort"}
    samples = tmp_path / "samples.jsonl"
    samples.write_text(json.dumps(crash) + "\n" + json.dumps(sample) + "\n")
    output = tmp_path / "results.jsonl"
    result = invoke(output, samples, problems)
    assert result.returncode == 0, result.stderr
    records = [json.loads(line) for line in output.read_text().splitlines()]
    assert [record["verdict"] for record in records] == ["candidate_crash", "pass"]
    assert records[0]["labels"] == ["candidate_crash"]


def test_generation_metadata_is_preserved(tmp_path):
    sample = json.loads((ROOT / "examples/samples.jsonl").read_text().splitlines()[0])
    sample.update(
        model_revision="checkpoint-sha",
        finish_reason="stop",
        metadata={"temperature": 0.7, "finish_reason": "nested-value"},
    )
    samples = tmp_path / "samples.jsonl"
    samples.write_text(json.dumps(sample) + "\n")
    output = tmp_path / "results.jsonl"
    result = invoke(output, samples)
    assert result.returncode == 0, result.stderr
    record = json.loads(output.read_text())
    assert record["metadata"] == sample["metadata"]
    assert record["additional_fields"] == {
        "model_revision": "checkpoint-sha",
        "finish_reason": "stop",
    }
    assert record["peak_rss_kb"] > 0
