"""Scripted travellers: one JSON file per evaluation trip (format in evals/travellers/README.md)."""

from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, ValidationError


class ScriptedTraveller(BaseModel):
    """Answers the brief questions, picks a place, and approves or rejects the booking."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    description: str = ""
    answers: dict[str, str] = Field(min_length=1)  # brief field -> the traveller's answer
    place_to_pick: str = Field(min_length=1)
    approve: bool


def load_traveller(path: Path) -> ScriptedTraveller:
    try:
        return ScriptedTraveller.model_validate_json(path.read_bytes())
    except ValidationError as error:
        raise ValueError(f"{path.name}: {error}") from error
