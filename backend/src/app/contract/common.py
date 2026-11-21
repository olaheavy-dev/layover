"""Source labels, the widget base and money values.

Every value that comes from outside Layover carries a source label
(decision 0011, rule 2). Money is held as integer minor units, never a float.
"""

from datetime import date
from typing import Annotated, Literal, Self

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, HttpUrl, model_validator

SourceStatus = Literal["live", "cached", "fallback", "unavailable"]
WidgetState = Literal["loading", "filled", "empty", "error", "not_known"]

# Kinds whose content is the traveller's own or Layover's, so they need no source label.
NO_OUTSIDE_SOURCE: frozenset[str] = frozenset({"brief_summary", "not_known"})


class SourceLabel(BaseModel):
    """Where a value came from, and how fresh it is."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    status: SourceStatus
    source: Annotated[str, Field(min_length=1)]
    source_url: HttpUrl | None = None
    captured_at: AwareDatetime | None = None
    data_date: date | None = None

    @model_validator(mode="after")
    def _cached_needs_a_date(self) -> Self:
        if self.status == "cached" and self.captured_at is None and self.data_date is None:
            raise ValueError("a cached label needs captured_at or data_date")
        return self


class WidgetBase(BaseModel):
    """Fields every widget shares. Subclasses add their own `kind` and content."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    state: WidgetState
    sources: list[SourceLabel]
    missing: str | None = None

    @model_validator(mode="after")
    def _check_state(self) -> Self:
        if self.missing is not None and not self.missing.strip():
            raise ValueError("missing must say what is missing, never an empty string")
        if self.state == "not_known" and not self.missing:
            raise ValueError("a not_known widget needs a missing reason")
        kind = getattr(self, "kind", None)
        if self.state == "filled" and not self.sources and kind not in NO_OUTSIDE_SOURCE:
            raise ValueError("a filled widget needs at least one source")
        return self


class MoneyValue(BaseModel):
    """An amount in integer minor units (pence, cents) and a currency code."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    amount_minor: Annotated[int, Field(strict=True)]
    currency: Annotated[str, Field(pattern=r"^[A-Z]{3}$")]


class MoneyEstimate(BaseModel):
    """A rounded money figure that is always shown as an estimate."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    exact: MoneyValue
    shown: MoneyValue
    is_estimate: Literal[True]

    @model_validator(mode="after")
    def _same_currency(self) -> Self:
        if self.exact.currency != self.shown.currency:
            raise ValueError("exact and shown must use the same currency")
        return self
