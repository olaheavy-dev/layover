"""The 20 widget models, the `Widget` union and the states each kind must show."""

from typing import Annotated

from pydantic import Field

from app.contract.widgets.advice_card import AdviceCard
from app.contract.widgets.booking_approval import BookingApproval
from app.contract.widgets.brief_summary import BriefSummary
from app.contract.widgets.climate_chart import ClimateChart
from app.contract.widgets.comparison_table import ComparisonTable
from app.contract.widgets.cost_estimate import CostEstimate
from app.contract.widgets.daylight import Daylight
from app.contract.widgets.fare_card import FareCard
from app.contract.widgets.fare_list import FareList
from app.contract.widgets.hotel_list import HotelList
from app.contract.widgets.itinerary_day import ItineraryDay
from app.contract.widgets.map import Map
from app.contract.widgets.money import Money
from app.contract.widgets.not_known import NotKnown
from app.contract.widgets.place_intro import PlaceIntro
from app.contract.widgets.public_holidays import PublicHolidays
from app.contract.widgets.sea_conditions import SeaConditions
from app.contract.widgets.time_difference import TimeDifference
from app.contract.widgets.transport_route import TransportRoute
from app.contract.widgets.web_results import WebResults

Widget = Annotated[
    BriefSummary
    | ComparisonTable
    | FareCard
    | ClimateChart
    | SeaConditions
    | Daylight
    | Money
    | AdviceCard
    | PlaceIntro
    | Map
    | ItineraryDay
    | HotelList
    | CostEstimate
    | BookingApproval
    | WebResults
    | NotKnown
    | PublicHolidays
    | TimeDifference
    | FareList
    | TransportRoute,
    Field(discriminator="kind"),
]

WIDGET_KINDS: tuple[str, ...] = (
    "brief_summary",
    "comparison_table",
    "fare_card",
    "climate_chart",
    "sea_conditions",
    "daylight",
    "money",
    "advice_card",
    "place_intro",
    "map",
    "itinerary_day",
    "hotel_list",
    "cost_estimate",
    "booking_approval",
    "web_results",
    "not_known",
    "public_holidays",
    "time_difference",
    "fare_list",
    "transport_route",
)

# For each kind, every state its samples must cover: `filled`, then the states the brief's
# "Widget states" table does not mark "Not applicable", then the extra states the boards draw.
# `not_known` is the Not known state itself, so it has no `filled` or `loading`.
WIDGET_STATES: dict[str, tuple[str, ...]] = {
    "brief_summary": ("filled", "loading", "waiting", "editing", "confirmed"),
    "comparison_table": ("filled", "loading", "empty", "error", "not_known", "swapped", "chosen"),
    "fare_card": ("filled", "loading", "error", "not_known", "older_fare"),
    "climate_chart": ("filled", "loading", "error", "not_known"),
    "sea_conditions": ("filled", "loading", "error", "not_known"),
    "daylight": ("filled", "loading", "error", "not_known"),
    "money": ("filled", "loading", "error", "not_known", "conversion"),
    "advice_card": ("filled", "loading", "error", "not_known"),
    "place_intro": ("filled", "loading", "error", "not_known", "fallback"),
    "map": ("filled", "loading", "error", "centre_only"),
    "itinerary_day": ("filled", "loading", "empty", "error", "not_known", "from_centre", "rebuilt"),
    "hotel_list": (
        "filled",
        "loading",
        "empty",
        "error",
        "not_known",
        "chosen",
        "skipped",
        "changed",
    ),
    "cost_estimate": ("filled", "loading", "error", "not_known", "partial", "over_budget"),
    "booking_approval": (
        "filled",
        "loading",
        "empty",
        "error",
        "waiting",
        "approved",
        "declined",
        "price_changed",
        "flights_only",
    ),
    "web_results": ("filled", "loading", "error"),
    "not_known": ("not_known",),
    "public_holidays": ("filled", "loading", "empty", "error", "not_known"),
    "time_difference": ("filled", "loading", "error", "not_known", "same_time", "hours_ahead"),
    "fare_list": ("filled", "loading", "empty", "error", "not_known", "one_place_not_known"),
    "transport_route": ("filled", "loading", "error", "not_known"),
}

__all__ = [
    "WIDGET_KINDS",
    "WIDGET_STATES",
    "AdviceCard",
    "BookingApproval",
    "BriefSummary",
    "ClimateChart",
    "ComparisonTable",
    "CostEstimate",
    "Daylight",
    "FareCard",
    "FareList",
    "HotelList",
    "ItineraryDay",
    "Map",
    "Money",
    "NotKnown",
    "PlaceIntro",
    "PublicHolidays",
    "SeaConditions",
    "TimeDifference",
    "TransportRoute",
    "WebResults",
    "Widget",
]
