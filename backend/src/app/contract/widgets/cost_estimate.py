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
        lines = [self.flights, self.stay, self.meals, self.local_transport, self.activities]
        # An omitted line counts as missing, so only a trip with all five lines can be complete.
        check_partial_flag(self.is_partial, lines, omitted_counts_as_missing=True)
        check_partial_flag(self.is_partial, [self.total])
        total = self.total.amount if self.total is not None else None
        line_is_estimate = any(line and line.amount and line.amount.is_estimate for line in lines)
        if total is not None and not total.is_estimate and line_is_estimate:
            raise ValueError("a total built from an estimate must be an estimate")
        check_budget_gap(
            has_budget=self.budget is not None,
            core_lines=[self.flights, self.stay, self.meals],
            gap=self.budget_gap,
            position=self.budget_position,
        )
        if self.budget is not None and total is not None and self.budget_gap is not None:
            self._check_gap_figures(self.budget, total)
        return self

    def _check_gap_figures(self, budget: MoneyValue, total: MoneyEstimate) -> None:
        gap = self.budget_gap
        assert gap is not None  # noqa: S101 - narrowed by the caller
        if gap.exact.currency != budget.currency or total.exact.currency != budget.currency:
            raise ValueError("budget, total and budget_gap must use one currency")
        difference = budget.amount_minor - total.exact.amount_minor
        if gap.exact.amount_minor != abs(difference):
            raise ValueError("budget_gap must equal the difference between budget and total")
        expected = "under" if difference > 0 else "over" if difference < 0 else "on"
        if self.budget_position != expected:
            raise ValueError(f'budget_position must be "{expected}" for this budget and total')
