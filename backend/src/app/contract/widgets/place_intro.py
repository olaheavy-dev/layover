"""`place_intro`: a short introduction to the place."""

from typing import Literal

from pydantic import Field

from app.contract.common import WidgetBase


class PlaceIntro(WidgetBase):
    kind: Literal["place_intro"]
    place: str
    hero_line: str | None = None
    paragraphs: list[str] = Field(default_factory=list)
    intro_source: Literal["wikivoyage", "wikipedia"] | None = None
