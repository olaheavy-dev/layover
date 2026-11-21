"""`comparison_table`: the places side by side."""

from typing import Literal, Self

from pydantic import Field, model_validator

from app.contract.common import MoneyEstimate, SourceLabel, WidgetBase
from app.contract.widgets._parts import (
    BudgetPosition,
    CostLine,
    Fare,
    Part,
    check_budget_gap,
    check_partial_flag,
)


class Weather(Part):
    """Typical weather for the trip month, with its own label (sample-data.md)."""

    high_c: float | None = None
    low_c: float | None = None
    rainy_days: int | None = Field(default=None, ge=0)
    averages_period: str  # "1991-2020"
    source: SourceLabel


class PlaceCard(Part):
    place: str
    card_state: Literal["loading", "ready", "failed", "swapped"]
    fare: Fare | None = None
    flights: CostLine | None = None
    stay: CostLine | None = None
    meals: CostLine | None = None
    known_costs: CostLine | None = None
    is_partial: bool = False
    budget_gap: MoneyEstimate | None = None  # how far from the budget; never negative
    budget_position: BudgetPosition | None = None
    weather: Weather | None = None

    @model_validator(mode="after")
    def _partial_and_budget(self) -> Self:
        check_partial_flag(self.is_partial, [self.flights, self.stay, self.meals, self.known_costs])
        check_budget_gap(
            has_budget=True,  # the brief holds the budget; the card only holds the gap
            core_lines=[self.flights, self.stay, self.meals],
            gap=self.budget_gap,
            position=self.budget_position,
        )
        return self


class ComparisonTable(WidgetBase):
    kind: Literal["comparison_table"]
    cards: list[PlaceCard] = Field(default_factory=list)
    chosen_place: str | None = None
    rules_out: str | None = None  # empty state: the part of the brief that rules places out
