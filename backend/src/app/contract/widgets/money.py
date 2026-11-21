"""`money`: an exchange rate, and optionally a conversion of an amount."""

from datetime import date
from decimal import Decimal
from typing import Annotated, Literal

from pydantic import Field

from app.contract.common import MoneyValue, WidgetBase
from app.contract.widgets._parts import Part

Currency = Annotated[str, Field(pattern=r"^[A-Z]{3}$")]


class Conversion(Part):
    amount: MoneyValue
    converted: MoneyValue


class Money(WidgetBase):
    kind: Literal["money"]
    from_currency: Currency = "GBP"
    to_currency: Currency | None = None
    rate: Decimal | None = Field(default=None, gt=0)
    rate_date: date | None = None
    conversion: Conversion | None = None
