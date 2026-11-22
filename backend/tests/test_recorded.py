"""Recorded provider responses: each has a capture date and source, and none holds a secret."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
from pydantic import ValidationError

from tests.recorded_check import (
    RECORDED_DIR,
    Recording,
    find_secrets,
    load_recording,
    recording_files,
)

VALID: dict[str, Any] = {
    "provider": "sample",
    "captured_at": "2026-11-22",
    "source": "https://example.org/",
    "request": {"method": "GET", "path": "/things"},
    "response": {"things": []},
}


def test_every_recording_has_date_and_source() -> None:
    files = recording_files()
    assert files, "tests/recorded/ holds at least the sample recording"
    for path in files:
        recording = Recording.model_validate_json(path.read_text(encoding="utf-8"))
        assert recording.provider == path.parent.name, f"{path}: provider is not its folder name"


def test_no_secrets_in_recordings() -> None:
    for path in recording_files():
        data = json.loads(path.read_text(encoding="utf-8"))
        assert find_secrets(data) == [], f"{path.relative_to(RECORDED_DIR)} holds a secret"


def test_load_recording_reads_the_sample() -> None:
    recording = load_recording("sample", "example")
    assert recording.provider == "sample"
    assert str(recording.source) == "https://example.org/"
    assert recording.captured_at.isoformat() == "2026-11-22"


def test_load_recording_rejects_a_recording_without_a_source(tmp_path: Path) -> None:
    (tmp_path / "p").mkdir()
    bad = {k: v for k, v in VALID.items() if k != "source"}
    (tmp_path / "p" / "n.json").write_text(json.dumps(bad), encoding="utf-8")
    with pytest.raises(ValidationError):
        load_recording("p", "n", root=tmp_path)


def test_load_recording_rejects_a_recording_without_a_date(tmp_path: Path) -> None:
    (tmp_path / "p").mkdir()
    bad = {k: v for k, v in VALID.items() if k != "captured_at"}
    (tmp_path / "p" / "n.json").write_text(json.dumps(bad), encoding="utf-8")
    with pytest.raises(ValidationError):
        load_recording("p", "n", root=tmp_path)


def test_load_recording_rejects_an_unknown_field(tmp_path: Path) -> None:
    (tmp_path / "p").mkdir()
    (tmp_path / "p" / "n.json").write_text(json.dumps({**VALID, "extra": 1}), encoding="utf-8")
    with pytest.raises(ValidationError):
        load_recording("p", "n", root=tmp_path)


def test_load_recording_rejects_a_bad_date_and_a_non_url_source(tmp_path: Path) -> None:
    (tmp_path / "p").mkdir()
    for change in ({"captured_at": "yesterday"}, {"source": "not a url"}):
        (tmp_path / "p" / "n.json").write_text(json.dumps({**VALID, **change}), encoding="utf-8")
        with pytest.raises(ValidationError):
            load_recording("p", "n", root=tmp_path)


@pytest.mark.parametrize("key", ["token", "api_key", "authorization", "x-access-token", "password"])
def test_secret_key_names_are_caught_in_any_case_at_any_depth(key: str) -> None:
    for name in (key, key.upper(), key.title()):
        data = {"a": [{"b": {name: "x"}}]}
        assert find_secrets(data) != []


def test_secret_values_are_caught_in_nested_lists_and_dicts() -> None:
    assert find_secrets({"a": [{"b": ["duffel_test_abc123"]}]}) != []
    assert find_secrets({"a": {"b": "key is duffel_live_abc123 here"}}) != []
    assert find_secrets({"a": [["ask jo.bloggs@example.com"]]}) != []


def test_clean_data_has_no_findings() -> None:
    assert find_secrets(VALID) == []
    assert find_secrets({"tokens_used": 3, "note": "duffel is a provider"}) == []


def test_secret_check_covers_every_file_it_is_given(tmp_path: Path) -> None:
    (tmp_path / "p").mkdir()
    planted = {**VALID, "response": {"Authorization": "Bearer x"}}
    (tmp_path / "p" / "n.json").write_text(json.dumps(planted), encoding="utf-8")
    files = recording_files(tmp_path)
    assert len(files) == 1
    assert find_secrets(json.loads(files[0].read_text(encoding="utf-8"))) != []


@pytest.mark.parametrize(
    "data",
    [
        {"note": "Bearer sk_abc123"},
        {"headers": [["Authorization", "Bearer abc"]]},
        {"headers": [["x-api-key", "k"]]},
        {"access_token": "x"},
        {"x-api-key": "x"},
        {"apikey": "x"},
        {"Api-Key": "x"},
        {"client_secret": "x"},
        {"session_id": "x"},
        {"duffel_test_abc": 1},
        {"jo@example.com": 1},
        {"url": "https://x/?api_key=abc&token=def"},
        {"url": "https://x/?a=1&token=def"},
        {"url": "https://x/?access_token=def"},
        {"note": "Basic dXNlcjpwYXNzd29yZA=="},
        {"jwt": "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxIn0.sig"},
    ],
    ids=lambda d: next(iter(d)) + "-" + str(len(str(d))),
)
def test_secret_variants_are_caught(data: object) -> None:
    assert find_secrets(data) != []


def test_names_that_only_contain_a_secret_word_are_clean() -> None:
    clean = {"tokens_used": 3, "keyboard": "x", "passwordless": True, "monkey": 1}
    assert find_secrets(clean) == []
