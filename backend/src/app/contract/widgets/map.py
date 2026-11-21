"""`map`: the place centre, the chosen hotel and the stops."""

from typing import Literal

from pydantic import Field, HttpUrl

from app.contract.common import WidgetBase
from app.contract.widgets._parts import Latitude, Longitude, Part


class MapPlace(Part):
    name: str
    lat: Latitude
    lon: Longitude
    url: HttpUrl | None = None  # the link the list fallback shows


class Map(WidgetBase):
    kind: Literal["map"]
    centre: MapPlace | None = None
    hotel: MapPlace | None = None
    stops: list[MapPlace] = Field(default_factory=list)
