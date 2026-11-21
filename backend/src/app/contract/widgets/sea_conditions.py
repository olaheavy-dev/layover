"""`sea_conditions`: typical sea temperature."""

from typing import Literal

from pydantic import Field

from app.contract.common import WidgetBase


class SeaConditions(WidgetBase):
    kind: Literal["sea_conditions"]
    place: str
    month: int | None = Field(default=None, ge=1, le=12)
    sea_temp_c: float | None = None
