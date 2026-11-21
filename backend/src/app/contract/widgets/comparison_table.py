"""`comparison_table`: the places side by side."""

from typing import Literal

from pydantic import Field

from app.contract.common import MoneyValue, WidgetBase
from app.contract.widgets._parts import CostLine, Fare, Part


class PlaceCard(Part):
    place: str
    card_state: Literal["loading", "ready", "failed", "swapped"]
    fare: Fare | None = None
    flights: CostLine | None = None
    stay: CostLine | None = None
    meals: CostLine | None = None
    known_costs: CostLine | None = None
    is_partial: bool = False
    # known costs minus budget, in minor units: negative is under, positive is over.
    # None when it cannot be worked out (a missing line could change the answer).
    over_budget_by: MoneyValue | None = None
    high_c: float | None = None
    low_c: float | None = None
    rainy_days: int | None = Field(default=None, ge=0)


class ComparisonTable(WidgetBase):
    kind: Literal["comparison_table"]
    cards: list[PlaceCard] = Field(default_factory=list)
    chosen_place: str | None = None
    rules_out: str | None = None  # empty state: the part of the brief that rules places out
