"""Tests for the evaluation runner (docs/evaluations/cases.md).

Expected failure before the code exists: `app.evals` cannot be imported.
These tests make no model calls, so they run in `make check`.
"""

import importlib.util
import json
import re
import sys
from pathlib import Path

import pytest

from app.evals.cases import Case, parse_cases
from app.evals.runner import Outcome, build_step_map, run_case, run_cases
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
        assert result.outcome is Outcome.PASS, (n, result.detail)


def test_widget_check_fails_when_a_state_is_missing(tmp_path: Path) -> None:
    from app.evals.checks.widget_schemas import check_widget_samples

    (tmp_path / "widgets" / "money").mkdir(parents=True)
    ok, detail = check_widget_samples("money", tmp_path)
    assert not ok
    assert "money" in detail


def test_unbuilt_cases_not_run() -> None:
    steps = build_step_map(DIRECTION_MD)
    result = run_case(_by_id()["TRIP-01"], steps)
    assert result.outcome is Outcome.NOT_RUN
    assert result.line() == "NOT RUN (needs step 4)"


def test_every_case_has_a_result_and_a_step() -> None:
    results = run_cases(parse_cases(CASES_MD), build_step_map(DIRECTION_MD))
    assert len(results) == 53
    assert not [r for r in results if r.outcome is Outcome.FAIL]
    passed = [r.case.case_id for r in results if r.outcome is Outcome.PASS]
    assert passed == [f"WIDGET-{n:02d}" for n in range(1, 21)]


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
