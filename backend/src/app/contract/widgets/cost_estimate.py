"""`cost_estimate`: known costs for a place, always an estimate and often partial."""

from typing import Literal

from pydantic import Field

from app.contract.common import MoneyValue, WidgetBase
from app.contract.widgets._parts import CostLine


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
    # total minus budget: negative is under, positive is over. None while a line is missing.
    over_budget_by: MoneyValue | None = None
    nights: int | None = Field(default=None, ge=1)
    people: int | None = Field(default=None, ge=1)
