"""`advice_card`: a link to the FCDO page and its update date. It never rates safety."""

from datetime import date
from typing import Literal, Self

from pydantic import HttpUrl, field_validator, model_validator

from app.contract.common import WidgetBase


class AdviceCard(WidgetBase):
    kind: Literal["advice_card"]
    place: str
    title: str | None = None
    fcdo_url: HttpUrl  # always shown, even when the page could not be read
    updated_on: date | None = None  # the FCDO's own update date
    layover_copy: str | None = None

    @field_validator("fcdo_url")
    @classmethod
    def _is_the_fcdo_page(cls, url: HttpUrl) -> HttpUrl:
        if (
            url.scheme != "https"
            or url.host != "www.gov.uk"
            or url.port not in (None, 443)
            or (
                (url.path or "") != "/foreign-travel-advice"
                and not (url.path or "").startswith("/foreign-travel-advice/")
            )
        ):
            raise ValueError("fcdo_url must be an https://www.gov.uk/foreign-travel-advice page")
        return url

    @model_validator(mode="after")
    def _filled_shows_its_date(self) -> Self:
        if self.state == "filled" and self.updated_on is None:
            raise ValueError("a filled advice card must show the FCDO update date")
        return self
