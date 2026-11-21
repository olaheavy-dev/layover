"""`itinerary_day`: one day of stops."""

from datetime import date, time
from typing import Literal, Self

from pydantic import Field, model_validator

from app.contract.common import SourceLabel, WidgetBase
from app.contract.widgets._parts import Part


class Stop(Part):
    name: str
    kind: Literal["place", "walk"] = "place"
    hours_status: Literal["known", "not_known", "depends_on_day", "not_applicable"] = (
        "not_applicable"
    )
    opens: time | None = None
    closes: time | None = None
    source: SourceLabel | None = None

    @model_validator(mode="after")
    def _hours(self) -> Self:
        if self.hours_status == "known" and (self.opens is None or self.closes is None):
            raise ValueError("known hours need opens and closes")
        if self.hours_status != "known" and (self.opens or self.closes):
            raise ValueError("opening times given but hours_status is not known")
        return self


class ItineraryDay(WidgetBase):
    kind: Literal["itinerary_day"]
    day_number: int = Field(ge=1)
    day: date | None = None
    base: str | None = None  # the chosen hotel; None means the day starts from the centre
    starts_from_centre: bool = False
    rebuilt: bool = False  # rebuilt after a hotel change
    stops: list[Stop] = Field(default_factory=list)

    @model_validator(mode="after")
    def _base_and_centre_agree(self) -> Self:
        if self.starts_from_centre and self.base is not None:
            raise ValueError("a day that starts from the centre has no base hotel")
        if self.state != "loading" and self.starts_from_centre != (self.base is None):
            raise ValueError("a day needs a base hotel, or starts_from_centre set to true")
        return self
