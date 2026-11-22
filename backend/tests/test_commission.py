"""The commission switch (decision register: "Commission is built but switched off")."""

from __future__ import annotations

import pytest

from app.settings import Settings


def test_commission_off_by_default(monkeypatch: pytest.MonkeyPatch) -> None:
    """Working: no COMMISSION_ENABLED in the environment means the field keeps its default, False.
    Source: docs/decisions/README.md#register, 2026-11-19 row
    "Commission is built but switched off"."""
    monkeypatch.delenv("COMMISSION_ENABLED", raising=False)
    assert Settings(_env_file=None).commission_enabled is False
