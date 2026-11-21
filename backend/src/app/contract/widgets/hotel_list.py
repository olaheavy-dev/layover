"""`hotel_list`: hotels near the place, from OpenStreetMap. No prices."""

from typing import Literal, Self

from pydantic import Field, HttpUrl, model_validator

from app.contract.common import WidgetBase
from app.contract.widgets._parts import Part


class Hotel(Part):
    name: str
    area: str | None = None
    stars: int | None = Field(default=None, ge=1, le=5)
    website: HttpUrl | None = None


class HotelList(WidgetBase):
    kind: Literal["hotel_list"]
    place: str
    hotels: list[Hotel] = Field(default_factory=list)
    selection: Literal["undecided", "chosen", "skipped", "changed"] = "undecided"
    chosen_hotel: str | None = None

    @model_validator(mode="after")
    def _chosen_needs_a_hotel(self) -> Self:
        if self.selection in ("chosen", "changed") and not (
            self.chosen_hotel and self.chosen_hotel.strip()
        ):
            raise ValueError("a chosen or changed selection needs chosen_hotel")
        return self
