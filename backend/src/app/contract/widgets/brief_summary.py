"""`brief_summary`: the traveller's brief as chips."""

from typing import Literal

from pydantic import Field

from app.contract.common import MoneyValue, WidgetBase


class BriefSummary(WidgetBase):
    kind: Literal["brief_summary"]
    trip_name: str | None = None
    origin: str | None = None  # for example "Manchester (MAN)"
    when: str | None = None  # the traveller's words, for example "May 2027"
    nights: int | None = Field(default=None, ge=1)
    adults: int | None = Field(default=None, ge=1)
    budget: MoneyValue | None = None
    feel: str | None = None
    brief_state: Literal["waiting", "editing", "confirmed"] | None = None
