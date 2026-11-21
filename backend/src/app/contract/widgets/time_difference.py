"""`time_difference`: the clock difference between the UK and the place on one day."""

from datetime import date
from typing import Literal, Self

from pydantic import model_validator

from app.contract.common import WidgetBase


class TimeDifference(WidgetBase):
    kind: Literal["time_difference"]
    place: str
    place_zone: str | None = None  # IANA name, for example "Europe/Lisbon"
    on_date: date | None = None
    dates_set: bool = True  # False: the day is the middle of the month
    uk_offset_minutes: int | None = None  # UTC offset on that day, BST included
    place_offset_minutes: int | None = None
    difference_minutes: int | None = None  # place minus UK; positive is ahead

    @model_validator(mode="after")
    def _difference_matches(self) -> Self:
        if self.uk_offset_minutes is not None and self.place_offset_minutes is not None:
            expected = self.place_offset_minutes - self.uk_offset_minutes
            if self.difference_minutes != expected:
                raise ValueError("difference_minutes must be place offset minus UK offset")
        return self
