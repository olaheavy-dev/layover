"""The trip: every section of one planned holiday, each optional until it is planned."""

from pydantic import AwareDatetime, BaseModel, ConfigDict

from app.contract.widgets import (
    BookingApproval,
    BriefSummary,
    ComparisonTable,
    HotelList,
    ItineraryDay,
    Widget,
)


class ShareSettings(BaseModel):
    """What a shared link shows. Budget and travellers are hidden unless the owner opts in."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    as_of: AwareDatetime | None = None
    include_budget_and_travellers: bool = False


class Trip(BaseModel):
    """One trip. An empty trip has only its identity and share settings."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    trip_id: str
    is_sample: bool
    name: str
    brief: BriefSummary | None = None
    comparison: ComparisonTable | None = None
    chosen_place: str | None = None
    place_widgets: list[Widget] = []  # the facts about the chosen place
    stay: HotelList | None = None
    days: list[ItineraryDay] = []
    booking: BookingApproval | None = None
    pinned: list[Widget] = []  # "Added from the chat"
    share: ShareSettings
