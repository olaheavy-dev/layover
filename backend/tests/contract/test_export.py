"""The exported JSON Schemas in `schemas/` must match the models; `--check` is the guard."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

from app.contract.export import default_out_dir


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(  # noqa: S603 - fixed command, our own module
        [sys.executable, "-m", "app.contract.export", *args],
        capture_output=True,
        text=True,
        check=False,
    )


def test_exports_are_current() -> None:
    result = _run("--check")
    assert result.returncode == 0, result.stdout + result.stderr


def test_export_check_catches_drift(tmp_path: Path) -> None:
    copy = tmp_path / "schemas"
    shutil.copytree(default_out_dir(), copy, ignore=shutil.ignore_patterns("samples"))
    assert _run("--check", "--out", str(copy)).returncode == 0
    target = copy / "widgets" / "money.schema.json"
    target.write_text(target.read_text() + " ")
    (copy / "trip.schema.json").unlink()
    result = _run("--check", "--out", str(copy))
    assert result.returncode == 1
    assert "widgets/money.schema.json" in result.stdout
    assert "trip.schema.json" in result.stdout
