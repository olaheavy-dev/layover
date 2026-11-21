"""`web_results`: web search results, not checked by Layover. No figures field."""

from typing import Literal, Self

from pydantic import AwareDatetime, Field, HttpUrl, model_validator

from app.contract.common import WidgetBase
from app.contract.widgets._parts import Part


class WebResult(Part):
    title: str
    url: HttpUrl
    quote: str


class WebResults(WidgetBase):
    kind: Literal["web_results"]
    question: str | None = None
    results: list[WebResult] = Field(default_factory=list)
    retrieved_at: AwareDatetime | None = None

    @model_validator(mode="after")
    def _filled_has_retrieval_date(self) -> Self:
        if self.state == "filled" and self.retrieved_at is None:
            raise ValueError("filled web results need retrieved_at")
        return self
