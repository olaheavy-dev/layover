"""National public holidays from the `holidays` Python library (cached data, no network).

The library holds its rules in code, so a value is "cached" and dated by the library release
(`data/holidays_release.json`). It covers national holidays only; local or regional ones may be
missing, and the widget says so (`national_only`). An unsupported country is "not known", never
an empty list (decision 0011 rule 4).
"""

import json
from datetime import date
from pathlib import Path

import holidays as holidays_lib

from app.contract.common import SourceLabel
from app.contract.widgets.public_holidays import Holiday, PublicHolidays

SOURCE = "holidays (Python library)"
_RELEASE = Path(__file__).resolve().parent.parent / "data" / "holidays_release.json"


def _release() -> dict[str, str]:
    data: dict[str, str] = json.loads(_RELEASE.read_text(encoding="utf-8"))
    return data


def national_holidays(
    country: str, year: int, month: int, *, place: str | None = None
) -> PublicHolidays:
    """National public holidays for an ISO 3166-1 alpha-2 `country` in one month."""
    code = country.strip().upper()
    where = place or code
    release = _release()
    try:
        calendar = holidays_lib.country_holidays(
            code, years=year, categories=("public",), language="en_US"
        )
    except NotImplementedError:
        return PublicHolidays(
            kind="public_holidays",
            state="not_known",
            place=where,
            country=code,
            year=year,
            month=month,
            missing=f"a holiday list for {code}, so Layover cannot say if any fall in the month",
            sources=[SourceLabel(status="unavailable", source=SOURCE)],
        )
    found = [
        Holiday(day=day, name=name) for day, name in sorted(calendar.items()) if day.month == month
    ]
    label = SourceLabel(
        status="cached",
        source=SOURCE,
        source_url=release["source"],
        data_date=date.fromisoformat(release["released"]),
    )
    return PublicHolidays(
        kind="public_holidays",
        state="filled" if found else "empty",
        place=where,
        country=code,
        year=year,
        month=month,
        holidays=found,
        sources=[label],
    )
