"""Stored workflow checkpoints (not used here)

This project has no model code, so this revision does nothing. It keeps its place in the
chain, so a project that adds model code later (or ran it before) follows the same history.

Revision ID: 0008
Revises: 0007
Create Date: 2026-11-12
"""

from __future__ import annotations

from collections.abc import Sequence

revision: str = "0008"
down_revision: str | Sequence[str] | None = "0007"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
