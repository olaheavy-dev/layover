"""`fare_card`: one cached return fare for a route and month."""

from typing import Literal

from pydantic import HttpUrl

from app.contract.common import WidgetBase
from app.contract.widgets._parts import Fare, YearMonth


class FareCard(WidgetBase):
    kind: Literal["fare_card"]
    origin: str
    destination: str
    month: YearMonth  # "2027-05"
    fare: Fare | None = None
    search_url: HttpUrl | None = None  # the plain Aviasales search link
