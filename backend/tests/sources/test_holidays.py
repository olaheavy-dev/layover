"""Tests for the national holidays adapter (app.sources.holidays), written before the code.

Expected failure before app.sources.holidays exists: every test fails at import
(ModuleNotFoundError). The release record test fails until the record and the package exist.
"""

import json
from datetime import date
from importlib.metadata import version
from pathlib import Path

from app.sources.holidays import national_holidays

RELEASE = Path(__file__).resolve().parents[2] / "src" / "app" / "data" / "holidays_release.json"


def test_portugal_may_2027() -> None:
    """The national holidays for Portugal in May 2027 are 1 May and 27 May.

    Working: Portugal's Labour Code, article 234(1), lists the mandatory holidays: 1 January,
    Good Friday, Easter Sunday, 25 April, 1 May, Corpus Christi, 10 June, 15 August, 5 October,
    1 November, 1, 8 and 25 December. Of these, the fixed-date ones in May are only 1 May (Labour
    Day). Corpus Christi is Easter + 60 days (the Thursday after Trinity Sunday). Easter Sunday
    2027 is 28 March. 28 March + 3 days = 31 March; + 30 days = 30 April (33 days); + 27 days =
    27 May (60 days). Easter was cross-checked with the anonymous Gregorian (Meeus/Jones/Butcher)
    algorithm, by hand, for Y = 2027: a = 2027 mod 19 = 13; b = 20, c = 27 (2027 div, mod 100);
    d = 20 div 4 = 5, e = 0; f = (20 + 8) div 25 = 1; g = (20 - 1 + 1) div 3 = 6;
    h = (19 * 13 + 20 - 5 - 6 + 15) mod 30 = 271 mod 30 = 1; i = 27 div 4 = 6, k = 27 mod 4 = 3;
    l = (32 + 2 * 0 + 2 * 6 - 1 - 3) mod 7 = 40 mod 7 = 5; m = (13 + 11 * 1 + 22 * 5) div 451
    = 134 div 451 = 0; month = (1 + 5 - 0 + 114) div 31 = 120 div 31 = 3 (March); day =
    (120 mod 31) + 1 = 27 + 1 = 28. Easter is 28 March 2027.
    Good Friday (26 March) and Easter (28 March) fall in March, not May.
    So May 2027 holds exactly 2027-05-01 and 2027-05-27.

    Source: Lei n.º 8/2016, 1 April 2016, Diário da República, 1.ª série, n.º 64, p. 1112,
    article 2, which sets the wording of article 234(1) of the Código do Trabalho (Lei n.º 7/2009):
    https://www.garrigues.com/sites/default/files/noticias/files/l_8_2016.pdf (a copy of the
    official page; read on 22 Nov 2026). Easter 2027 = 28 March:
    https://www.timeanddate.com/holidays/us/easter-sunday (read on 22 Nov 2026).
    """
    result = national_holidays("PT", 2027, 5)

    assert result.state == "filled"
    assert [h.day for h in result.holidays] == [date(2027, 5, 1), date(2027, 5, 27)]
    assert result.national_only is True
    assert (result.year, result.month, result.country) == (2027, 5, "PT")
    label = result.sources[0]
    assert label.status == "cached"
    assert label.source == "holidays (Python library)"
    assert label.data_date == date(2026, 11, 2)  # the release date in holidays_release.json
    assert str(label.source_url) == "https://pypi.org/pypi/holidays/0.108/json"


def test_country_without_data() -> None:
    """An unsupported country code is not known, never an empty list.

    Working: "ZZ" is not an ISO 3166-1 alpha-2 country the library supports, so Layover has no
    list and must not say "no holidays".
    Source: decision 0011 rule 4 (missing data is never shown as zero or a clean result).
    """
    result = national_holidays("ZZ", 2027, 5)

    assert result.state == "not_known"
    assert result.missing
    assert result.holidays == []
    assert result.sources[0].status == "unavailable"


def test_supported_month_without_holidays_is_empty() -> None:
    """A supported country with no national holiday in the month is a known "empty".

    Working: Portugal's article 234 list (see test_portugal_may_2027) has no date in July, so
    July 2027 has none.
    Source: Lei n.º 8/2016, article 2 (same page as above).
    """
    result = national_holidays("PT", 2027, 7)

    assert result.state == "empty"
    assert result.holidays == []
    assert result.sources[0].status == "cached"


def test_release_record_matches_installed() -> None:
    record = json.loads(RELEASE.read_text(encoding="utf-8"))

    assert record["version"] == version("holidays")
    assert record["source"] == f"https://pypi.org/pypi/holidays/{record['version']}/json"
    assert date.fromisoformat(record["released"]) <= date.fromisoformat(record["checked"])
