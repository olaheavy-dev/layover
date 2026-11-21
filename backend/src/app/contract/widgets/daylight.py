"""`daylight`: sunrise, sunset and day length for one day."""

from datetime import date, time
from typing import Literal

from pydantic import Field, HttpUrl

from app.contract.common import WidgetBase


class Daylight(WidgetBase):
    kind: Literal["daylight"]
    place: str
    day: date | None = None
    dates_set: bool  # False: the day is the middle of the month
    sunrise: time | None = None
    sunset: time | None = None
    day_length_minutes: int | None = Field(default=None, ge=0, le=1440)
    credit_url: HttpUrl | None = None  # visible link to sunrise-sunset.org
