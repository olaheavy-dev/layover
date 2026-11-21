"""`not_known`: Layover says what it does not know. What is missing goes in `missing`."""

from typing import Literal, Self

from pydantic import model_validator

from app.contract.common import WidgetBase


class NotKnown(WidgetBase):
    kind: Literal["not_known"]
    reason: str | None = None  # why no source has it
    instead: str | None = None  # what Layover can do instead

    @model_validator(mode="after")
    def _always_not_known(self) -> Self:
        if self.state != "not_known":
            raise ValueError("a not_known widget is always in the not_known state")
        return self
