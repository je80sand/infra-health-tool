import json
import subprocess
import sys
from pathlib import Path


def run_cli(args: list[str]) -> subprocess.CompletedProcess:
    """
    Run the CLI as a module: python -m src.cli <args>
    Returns CompletedProcess with returncode, stdout, stderr.
    """
    return subprocess.run(
        [sys.executable, "-m", "src.cli", *args],
        capture_output=True,
        text=True,
        cwd=Path(__file__).resolve().parents[1], # repo root
    )


def test_exit_code_ok_when_all_below_thresholds():
    # Set thresholds high so it should be OK on most machines
    result = run_cli(["--cpu-warn", "95", "--mem-warn", "95", "--disk-warn", "95"])
    assert result.returncode == 0, f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"


def test_exit_code_warn_when_thresholds_too_low():
    # Set thresholds extremely low so it should WARN on most machines
    result = run_cli(["--cpu-warn", "0", "--mem-warn", "0", "--disk-warn", "0"])
    assert result.returncode == 1, f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"