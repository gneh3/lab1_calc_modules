import os
import subprocess
import sys


def test_cli_calc_success():
    env = os.environ.copy()
    env["PYTHONPATH"] = "src"

    res = subprocess.run(
        [sys.executable, "-m", "toolkit", "calc", "2+2"],
        capture_output=True,
        text=True,
        env=env,
        check=False
    )
    assert res.returncode == 0
    assert "4" in res.stdout


def test_cli_error_code():
    env = os.environ.copy()
    env["PYTHONPATH"] = "src"

    res = subprocess.run(
        [sys.executable, "-m", "toolkit", "calc", "1/0"],
        capture_output=True,
        text=True,
        env=env,
        check=False
    )
    assert res.returncode == 2
    assert "Error" in res.stderr