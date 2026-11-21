"""Small models that more than one widget uses."""

from typing import Annotated, Literal, Self

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, StringConstraints, model_validator

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

    @model_validator(mode="after")
    def _times_agree(self) -> Self:
        if self.source.captured_at is not None and self.source.captured_at != self.captured_at:
            raise ValueError("fare captured_at and its source label captured_at must match")
        return self


BudgetPosition = Literal["under", "over", "on"]


def check_budget_gap(
    *,
    has_budget: bool,
    core_lines: list["CostLine | None"],
    gap: MoneyEstimate | None,
    position: BudgetPosition | None,
) -> None:
    """Rules for the budget comparison, shared by cost_estimate and comparison cards.

    The gap is never negative: the position says under, over or on. Both are set or both are
    empty. They are set only when there is a budget and the core lines (flights, stay and meals)
    all have amounts; a missing core line could change the answer. Local transport and
    activities are always unknown, so a partial total is still compared, on the known costs.
    """
    if (gap is None) != (position is None):
        raise ValueError("budget_gap and budget_position are both set or both empty")
    if gap is None or position is None:
        return
    if not has_budget:
        raise ValueError("a budget comparison needs a budget")
    if any(line is None or line.amount is None for line in core_lines):
        raise ValueError("no budget comparison while flights, stay or meals has no amount")
    if gap.exact.amount_minor < 0 or gap.shown.amount_minor < 0:
        raise ValueError("budget_gap is never negative; use budget_position")
    if (position == "on") != (gap.exact.amount_minor == 0):
        raise ValueError('budget_position "on" means a gap of exactly zero')


YearMonth = Annotated[str, StringConstraints(pattern=r"^\d{4}-(0[1-9]|1[0-2])$")]  # "2026-03"


class CostLine(Part):
    """One line of a cost estimate. A line with no amount says why (decision 0011, rule 4)."""

    unit: MoneyValue | None = None  # a part, to the pound: per night, per meal, per person
    amount: MoneyEstimate | None = None
    source: SourceLabel | None = None
    missing: str | None = None
    listing_count: int | None = Field(default=None, ge=0)  # Wikivoyage lines
    page_edited: YearMonth | None = None  # Wikivoyage lines: the boards give a month, no day

    @model_validator(mode="after")
    def _amount_or_reason(self) -> Self:
        if self.amount is not None and self.source is None:
            raise ValueError("a cost line with an amount needs its own source label")
        if self.amount is None and not (self.missing and self.missing.strip()):
            raise ValueError("a cost line with no amount needs a missing reason")
        return self


def check_partial_flag(is_partial: bool, lines: list[CostLine | None]) -> None:
    """A total with a line that has no amount must say it is partial (decision 0011, rule 4)."""
    if not is_partial and any(line is not None and line.amount is None for line in lines):
        raise ValueError("a line has no amount, so is_partial must be True")


Latitude = Annotated[float, Field(ge=-90, le=90)]
Longitude = Annotated[float, Field(ge=-180, le=180)]
