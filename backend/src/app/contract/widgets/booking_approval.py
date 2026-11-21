"""`booking_approval`: the sandbox booking step. Never a real booking."""

from datetime import date
from typing import Literal, Self

from pydantic import model_validator

from app.contract.common import MoneyValue, WidgetBase


class BookingApproval(WidgetBase):
    kind: Literal["booking_approval"]
    sandbox: Literal[True]
    booking_state: (
        Literal["waiting", "approved", "declined", "price_changed", "flights_only"] | None
    ) = None
    origin: str | None = None
    destination: str | None = None
    depart: date | None = None
    return_date: date | None = None
    adults: int | None = None
    sandbox_price: MoneyValue | None = None  # the price you saw
    new_price: MoneyValue | None = None  # price_changed: the price now
    order_ref: str | None = None  # approved: the sandbox order

    @model_validator(mode="after")
    def _booking_fields(self) -> Self:
        if self.booking_state == "approved" and not self.order_ref:
            raise ValueError("an approved booking needs its sandbox order reference")
        if self.booking_state == "price_changed" and self.new_price is None:
            raise ValueError("a price_changed booking needs the new price")
        return self
