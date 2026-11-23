"""Tests for the evaluation runner (docs/evaluations/cases.md).

Expected failure before the code exists: `app.evals` cannot be imported.
These tests make no model calls, so they run in `make check`.
"""

import importlib.util
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

from app.evals import runner
from app.evals.cases import Case, parse_cases
from app.evals.runner import (
    Outcome,
    ReportInfo,
    Result,
    build_step_map,
    main,
    render_report,
    run_case,
    run_cases,
    totals_line,
)
from app.evals.travellers import ScriptedTraveller, load_traveller

REPO_ROOT = Path(__file__).resolve().parents[3]
CASES_MD = REPO_ROOT / "docs" / "evaluations" / "cases.md"
DIRECTION_MD = REPO_ROOT / "docs" / "product" / "01-research-and-direction.md"
TRAVELLERS = REPO_ROOT / "evals" / "travellers"


def test_parses_all_cases() -> None:
    cases = parse_cases(CASES_MD)
    assert len(cases) == 53
    assert all(re.fullmatch(r"[A-Z]+-\d{2,}", c.case_id) for c in cases)
    judged = sorted(c.case_id for c in cases if c.scored_by == "judge")
    assert judged == ["COMPARE-06", "ITIN-02", "ITIN-05"]
    assert sum(c.scored_by == "code" for c in cases) == 50


def test_reads_the_same_ids_as_the_id_checker(monkeypatch: pytest.MonkeyPatch) -> None:
    """The runner mirrors tools/check_eval_ids.py (tools/ is not importable from the package)."""
    spec = importlib.util.spec_from_file_location(
        "check_eval_ids", REPO_ROOT / "tools" / "check_eval_ids.py"
    )
    assert spec is not None
    assert spec.loader is not None
    monkeypatch.setattr(sys, "dont_write_bytecode", True)  # no tools/__pycache__
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    expected = module.defined_ids(CASES_MD.read_text(encoding="utf-8"))
    assert [c.case_id for c in parse_cases(CASES_MD)] == expected


def test_unknown_scorer_rejected(tmp_path: Path) -> None:
    bad = tmp_path / "cases.md"
    bad.write_text(
        "## Cases\n\n"
        "| ID | Area | What it checks | Passes when | Fails when | Scored by | Status |\n"
        "|---|---|---|---|---|---|---|\n"
        "| `INTENT-01` | Intent | x | y | z | owner | planned |\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="INTENT-01"):
        parse_cases(bad)


def _by_id() -> dict[str, Case]:
    return {c.case_id: c for c in parse_cases(CASES_MD)}


def test_judge_cases_not_run() -> None:
    steps = build_step_map(DIRECTION_MD)
    for case_id, step in (("COMPARE-06", 4), ("ITIN-02", 5), ("ITIN-05", 5)):
        result = run_case(_by_id()[case_id], steps)
        assert result.outcome is Outcome.NOT_RUN
        assert result.line() == f"NOT RUN (needs step {step})"


def test_widget_schema_check_runs() -> None:
    steps = build_step_map(DIRECTION_MD)
    for n in range(1, 21):
        result = run_case(_by_id()[f"WIDGET-{n:02d}"], steps)
        assert result.outcome is Outcome.SCHEMA_PASS, (n, result.detail)
        assert result.line() == f"SCHEMA PASS (full case needs step {steps[f'WIDGET-{n:02d}']})"


def test_widget_check_fails_when_a_state_is_missing(tmp_path: Path) -> None:
    from app.evals.checks.widget_schemas import check_widget_samples

    real = REPO_ROOT / "schemas" / "samples" / "widgets" / "money"
    (tmp_path / "widgets" / "money").mkdir(parents=True)
    for sample in real.glob("*.json"):
        if sample.stem != "error":
            shutil.copy(sample, tmp_path / "widgets" / "money" / sample.name)
    ok, detail = check_widget_samples("money", tmp_path)
    assert not ok
    assert "no sample for state error" in detail


def test_widget_case_with_no_step_fails_and_never_prints_step_none() -> None:
    result = run_case(_by_id()["WIDGET-01"], {})
    assert result.outcome is Outcome.FAIL
    assert "no build step" in result.detail
    assert "None" not in result.line()


def test_main_exits_1_for_an_unknown_case(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["--case", "NOPE-99"]) == 1
    assert "unknown case: NOPE-99" in capsys.readouterr().out


def test_main_exits_1_when_a_case_fails(monkeypatch: pytest.MonkeyPatch) -> None:
    case = _by_id()["TRIP-01"]
    monkeypatch.setattr(runner, "run_cases", lambda cases, steps: [Result(case, Outcome.FAIL, "x")])
    assert main([]) == 1


def test_main_exits_0_when_nothing_fails() -> None:
    assert main(["--case", "WIDGET-01"]) == 0


def test_unbuilt_cases_not_run() -> None:
    steps = build_step_map(DIRECTION_MD)
    result = run_case(_by_id()["TRIP-01"], steps)
    assert result.outcome is Outcome.NOT_RUN
    assert result.line() == "NOT RUN (needs step 4)"


def test_every_case_has_a_result_and_a_step() -> None:
    results = run_cases(parse_cases(CASES_MD), build_step_map(DIRECTION_MD))
    assert len(results) == 53
    assert not [r for r in results if r.outcome is Outcome.FAIL]
    assert not [r for r in results if r.outcome is Outcome.PASS]  # no case is fully checked yet
    schema_passed = [r.case.case_id for r in results if r.outcome is Outcome.SCHEMA_PASS]
    assert schema_passed == [f"WIDGET-{n:02d}" for n in range(1, 21)]


def test_traveller_files_parse() -> None:
    files = sorted(TRAVELLERS.glob("*.json"))
    assert files
    for path in files:
        traveller = load_traveller(path)
        assert isinstance(traveller, ScriptedTraveller)
        assert traveller.answers
        assert traveller.place_to_pick
        assert isinstance(traveller.approve, bool)


def test_traveller_missing_field_rejected(tmp_path: Path) -> None:
    path = tmp_path / "t.json"
    path.write_text(json.dumps({"answers": {"budget": "x"}}), encoding="utf-8")
    with pytest.raises(ValueError, match=r"t\.json"):
        load_traveller(path)


def _info(**over: Any) -> ReportInfo:
    base = {
        "date": "2026-11-23",
        "commit": "abc1234",
        "command": "python -m app.evals.runner --report x",
        "seconds": 1.25,
        "model_calls": 0,
        "trips_run": 0,
        "scripts_on_disk": 1,
    }
    return ReportInfo(**{**base, **over})


def totals_line_from(stdout: str) -> str:
    return next(line for line in stdout.splitlines() if line.startswith("total "))


def test_report_totals_match_printout() -> None:
    results = run_cases(parse_cases(CASES_MD), build_step_map())
    assert totals_line(results) in render_report(results, _info())


def test_report_tokens_none_when_no_calls() -> None:
    text = render_report([], _info(model_calls=0))
    assert "Tokens: none: this run made no model calls" in text
    assert not re.search(r"Tokens:\s*0\b", text)


def test_report_trip_set_counts_trips_run_not_files() -> None:
    text = render_report([], _info(trips_run=0, scripts_on_disk=1))
    assert "Trip set: none yet" in text
    assert "1 traveller script on disk, not run yet" in text


def test_report_shows_fail_detail() -> None:
    case = parse_cases(CASES_MD)[0]
    text = render_report([Result(case, Outcome.FAIL, "boom")], _info())
    assert f"| `{case.case_id}` | FAIL | boom |" in text


def test_main_writes_report_and_creates_folder(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    out = tmp_path / "new" / "build-1.md"
    assert main(["--report", str(out)]) == 0
    assert totals_line_from(capsys.readouterr().out) in out.read_text(encoding="utf-8")


def test_report_with_case_rejected() -> None:
    with pytest.raises(SystemExit) as exc:
        main(["--report", "x.md", "--case", "WIDGET-01"])
    assert exc.value.code == 2


def test_main_exit_1_still_writes_report_on_fail(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        runner, "run_case", lambda case, steps: Result(case, Outcome.FAIL, "forced failure")
    )
    out = tmp_path / "report.md"
    assert main(["--report", str(out)]) == 1
    text = out.read_text(encoding="utf-8")
    assert "| FAIL | forced failure |" in text


def test_current_commit_not_known_without_git(monkeypatch: pytest.MonkeyPatch) -> None:
    def no_git(*args: Any, **kwargs: Any) -> None:
        raise FileNotFoundError("git")

    monkeypatch.setattr(subprocess, "run", no_git)
    assert runner.current_commit() == "not known"
