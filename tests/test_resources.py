from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace

import pytest

from harness.environment import ROOT, LeanEnvironment, VerifierConfig
from harness.sandbox import Sandbox
from harness.schema import Problem
from harness.verifier import LeanVerifier

pytestmark = pytest.mark.integration


def test_rss_sampler_measures_nested_worker_not_only_launcher(tmp_path, monkeypatch):
    config = replace(VerifierConfig.load(ROOT / "configs/verifier.toml"), memory_mb=128)
    environment = LeanEnvironment(config)
    sandbox = Sandbox(environment, config)
    verifier = object.__new__(LeanVerifier)
    verifier.config = config
    verifier.lean = environment.lean
    script = """import json, time
data=bytearray(64*1024*1024)
for i in range(0,len(data),4096): data[i]=1
print(json.dumps({'cinder_event':'candidate_ready'}),flush=True)
time.sleep(0.4)
print(json.dumps({'severity':'information','data':'CINDER_RESULT:{"verdict":"pass","axioms":[]}'}),flush=True)
"""
    monkeypatch.setattr(
        verifier,
        "_sandbox_command",
        lambda work, _: sandbox.command(work, ["/usr/bin/python3", "-c", script]),
    )
    with ThreadPoolExecutor(max_workers=1) as pool:
        result = pool.submit(
            verifier._check, Problem("p", "True", config.environment_id), "by trivial"
        ).result()
    assert result[0] == "pass", result[1]
    assert result[3] > 60 * 1024
