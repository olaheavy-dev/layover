"""`climate_chart`: typical monthly highs, lows and rainy days."""

from typing import Literal

from pydantic import Field

from app.contract.common import WidgetBase
from app.contract.widgets._parts import Part


class ClimateMonth(Part):
    month: int = Field(ge=1, le=12)
    high_c: float | None = None
    low_c: float | None = None
    rainy_days: int | None = Field(default=None, ge=0)


class ClimateChart(WidgetBase):
    kind: Literal["climate_chart"]
    place: str
    highlight_month: int | None = Field(default=None, ge=1, le=12)
    averages_period: str | None = None  # "1991-2020"
    months: list[ClimateMonth] = Field(default_factory=list)
