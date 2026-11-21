"""`fare_list`: cached fares from one airport to many places, lowest first."""

from typing import Literal, Self

from pydantic import Field, model_validator

from app.contract.common import WidgetBase
from app.contract.widgets._parts import Fare, Part


class FareRow(Part):
    destination: str
    fare: Fare | None = None
    missing: str | None = None  # a row with no fare says why

    @model_validator(mode="after")
    def _fare_or_reason(self) -> Self:
        if self.fare is None and not (self.missing and self.missing.strip()):
            raise ValueError("a fare row with no fare needs a missing reason")
        return self


class FareList(WidgetBase):
    kind: Literal["fare_list"]
    origin: str
    month: str  # "2027-03"
    rows: list[FareRow] = Field(default_factory=list)

    @model_validator(mode="after")
    def _lowest_first(self) -> Self:
        prices = [r.fare.price.amount_minor for r in self.rows if r.fare is not None]
        if prices != sorted(prices):
            raise ValueError("fare rows must be sorted lowest first")
        return self
