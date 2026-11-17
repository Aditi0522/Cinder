"""Exercise real kernel-enforced limits without unbounded host allocations."""

import subprocess
from dataclasses import replace

import pytest

from harness.environment import ROOT, LeanEnvironment, VerifierConfig
from harness.sandbox import Sandbox

pytestmark = pytest.mark.integration


@pytest.fixture(scope="module")
def environment():
    return LeanEnvironment(VerifierConfig.load(ROOT / "configs/verifier.toml"))


def execute(environment, tmp_path, script, **limits):
    config = replace(environment.config, **limits)
    sandbox = Sandbox(environment, config)
    return subprocess.run(
        sandbox.command(tmp_path, ["/usr/bin/python3", "-c", script]),
        text=True,
        capture_output=True,
        timeout=15,
        check=False,
    )


def test_cgroup_memory_limit_is_enforced(environment, tmp_path):
    result = execute(
        environment,
        tmp_path,
        "data=[]\nfor _ in range(512): data.append(bytearray(1024*1024))\nprint('unbounded')",
        memory_mb=128,
    )
    assert result.returncode != 0
    assert "unbounded" not in result.stdout


def test_cgroup_process_limit_is_enforced(environment, tmp_path):
    result = execute(
        environment,
        tmp_path,
        """import errno, os, time
children=[]
try:
    for _ in range(64):
        pid=os.fork()
        if pid == 0:
            time.sleep(2)
            os._exit(0)
        children.append(pid)
except OSError as error:
    assert error.errno == errno.EAGAIN
    print('limited', len(children))
finally:
    for pid in children: os.waitpid(pid, 0)
""",
        max_processes=16,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.startswith("limited ")
    assert int(result.stdout.split()[1]) < 64


def test_total_writable_disk_is_bounded(environment, tmp_path):
    result = execute(
        environment,
        tmp_path,
        """import errno, os
from pathlib import Path
assert os.statvfs('/tmp').f_blocks * os.statvfs('/tmp').f_frsize == 1024*1024
try:
    for i in range(64): Path(f'/tmp/file-{i}').write_bytes(b'x' * 65536)
except OSError as error:
    assert error.errno == errno.ENOSPC
    print('disk limited')
""",
        disk_mb=1,
    )
    assert result.returncode == 0, result.stderr
    assert "disk limited" in result.stdout


@pytest.mark.parametrize("path", ["/work/escape", "/escape", "/dev/escape"])
def test_other_filesystems_are_readonly(environment, tmp_path, path):
    result = execute(
        environment,
        tmp_path,
        f"""import errno
from pathlib import Path
try:
    Path({path!r}).write_text('escape')
except OSError as error:
    assert error.errno in (errno.EROFS, errno.EACCES)
    print('readonly')
""",
    )
    assert result.returncode == 0, result.stderr
    assert "readonly" in result.stdout
    assert not (tmp_path / "escape").exists()
