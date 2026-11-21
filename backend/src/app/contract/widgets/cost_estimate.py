"""`cost_estimate`: known costs for a place, always an estimate and often partial."""

from typing import Literal, Self

from pydantic import Field, model_validator

from app.contract.common import MoneyEstimate, MoneyValue, WidgetBase
from app.contract.widgets._parts import (
    BudgetPosition,
    CostLine,
    check_budget_gap,
    check_partial_flag,
)


class CostEstimate(WidgetBase):
    kind: Literal["cost_estimate"]
    place: str
    flights: CostLine | None = None
    stay: CostLine | None = None
    meals: CostLine | None = None
    local_transport: CostLine | None = None
    activities: CostLine | None = None
    total: CostLine | None = None
    is_partial: bool = True
    budget: MoneyValue | None = None
    budget_gap: MoneyEstimate | None = None  # how far from the budget; never negative
    budget_position: BudgetPosition | None = None
    nights: int | None = Field(default=None, ge=1)
    people: int | None = Field(default=None, ge=1)

    @model_validator(mode="after")
    def _partial_and_budget(self) -> Self:
        check_partial_flag(
            self.is_partial,
            [
                self.flights,
                self.stay,
                self.meals,
                self.local_transport,
                self.activities,
                self.total,
            ],
        )
        check_budget_gap(
            has_budget=self.budget is not None,
            core_lines=[self.flights, self.stay, self.meals],
            gap=self.budget_gap,
            position=self.budget_position,
        )
        return self
