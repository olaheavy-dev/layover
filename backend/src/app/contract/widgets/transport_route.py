"""`transport_route`: a journey to the airport, from TfL."""

from datetime import date, time
from typing import Literal, Self

from pydantic import Field, model_validator

from app.contract.common import WidgetBase
from app.contract.widgets._parts import Part


class Leg(Part):
    mode: str  # "walk", "Elizabeth line"
    minutes: int = Field(ge=0)
    description: str | None = None


class TransportRoute(WidgetBase):
    kind: Literal["transport_route"]
    origin: str
    destination: str
    planned_for: date | None = None
    dates_set: bool = True
    leaves_at: time | None = None
    legs: list[Leg] = Field(default_factory=list)
    total_minutes: int | None = Field(default=None, ge=0)

    @model_validator(mode="after")
    def _total_matches(self) -> Self:
        if self.legs and self.total_minutes != sum(leg.minutes for leg in self.legs):
            raise ValueError("total_minutes must equal the sum of the legs")
        return self
