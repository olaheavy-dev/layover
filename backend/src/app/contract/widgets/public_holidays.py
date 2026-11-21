"""`public_holidays`: national holidays in the trip month."""

from datetime import date
from typing import Literal

from pydantic import Field

from app.contract.common import WidgetBase
from app.contract.widgets._parts import Part


class Holiday(Part):
    day: date
    name: str


class PublicHolidays(WidgetBase):
    kind: Literal["public_holidays"]
    place: str
    country: str | None = None
    year: int | None = Field(default=None, ge=1900, le=2200)
    month: int | None = Field(default=None, ge=1, le=12)
    holidays: list[Holiday] = Field(default_factory=list)
    # National holidays only: local or regional ones may be missing, and the card says so.
    national_only: Literal[True] = True
