"""Small models that more than one widget uses."""

from datetime import date
from typing import Annotated, Self

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, model_validator

from app.contract.common import MoneyEstimate, MoneyValue, SourceLabel


class Part(BaseModel):
    """Base for the small models inside a widget: strict and immutable."""

    model_config = ConfigDict(extra="forbid", frozen=True)


class Fare(Part):
    """A cached return fare per person. It always carries when it was captured.

    No "too old" limit lives here; build step 4 sets it.
    """

    price: MoneyValue
    captured_at: AwareDatetime
    source: SourceLabel


class CostLine(Part):
    """One line of a cost estimate. A line with no amount says why (decision 0011, rule 4)."""

    unit: MoneyValue | None = None  # a part, to the pound: per night, per meal, per person
    amount: MoneyEstimate | None = None
    source: SourceLabel | None = None
    missing: str | None = None
    listing_count: int | None = Field(default=None, ge=0)  # Wikivoyage lines
    page_edited: date | None = None  # Wikivoyage lines

    @model_validator(mode="after")
    def _amount_or_reason(self) -> Self:
        if self.amount is not None and self.source is None:
            raise ValueError("a cost line with an amount needs its own source label")
        if self.amount is None and not (self.missing and self.missing.strip()):
            raise ValueError("a cost line with no amount needs a missing reason")
        return self


Latitude = Annotated[float, Field(ge=-90, le=90)]
Longitude = Annotated[float, Field(ge=-180, le=180)]
