"""Tests for Layover's money arithmetic (app.money), written before the code.

Rounding rule: full precision through a calculation, then once to the minor unit, half up
(owner's rounding rule, register, 21 Nov 2026). Estimates: exact value rounded once to the nearest
10 major units, half up (owner, 21 Nov 2026, "Parts to £1, totals to £10").
Expected failure before app.money exists: every test fails at import (ModuleNotFoundError).
"""

import json
from decimal import Decimal
from pathlib import Path

import pytest

from app.contract.common import MoneyEstimate, MoneyValue
from app.money import (
    UnknownCurrency,
    convert_exact,
    estimate,
    exact,
    round_estimate,
    to_minor,
    total,
)

SAMPLES = Path(__file__).resolve().parents[2] / "schemas" / "samples"


def gbp(minor: int) -> MoneyValue:
    return MoneyValue(amount_minor=minor, currency="GBP")


def test_exact_gives_major_units() -> None:
    """A MoneyValue of 78,200 pence is exactly 782 pounds.

    Working: 78200 pence / 100 pence per pound = 782.
    Source: ISO 4217 exponent 2 for GBP (app/data/currencies.json).
    """
    assert exact(gbp(78200)) == Decimal("782")


def test_convert_rounds_once_half_up() -> None:
    """EUR 47.35 at 0.8412 is GBP 39.83.

    Working: 4735 x 8412 = 39,830,820, so 47.35 x 0.8412 = 39.830820 pounds, which rounds to 39.83.
    Source: the owner's rounding rule (register, 21 Nov 2026); the rate is an illustrative input.
    """
    eur = MoneyValue(amount_minor=4735, currency="EUR")
    assert to_minor(convert_exact(eur, Decimal("0.8412")), "GBP") == gbp(3983)


def test_half_penny_goes_up() -> None:
    """39.835 pounds is exactly half a penny above 39.83, so half up gives 39.84.

    Working: 39.835 = 3983.5 pence; half up gives 3984 pence.
    Source: the owner's rounding rule (register, 21 Nov 2026).
    """
    assert to_minor(Decimal("39.835"), "GBP").amount_minor == 3984


@pytest.mark.parametrize(
    ("value", "minor"),
    [
        ("39.834", 3983),
        ("39.836", 3984),
        ("-39.834", -3983),
        ("-39.835", -3984),
        ("-39.836", -3984),
    ],
)
def test_to_minor_half_penny_boundaries(value: str, minor: int) -> None:
    """Half-up rounding to the penny, just below, exactly at and just above half, both signs.

    Working: pence values are 3983.4, 3983.6, -3983.4, -3983.5, -3983.6. Below half rounds towards
    zero (3983, -3983); above half rounds away from zero (3984, -3984); exactly half rounds away
    from zero (-3983.5 gives -3984), as the positive 3983.5 gives 3984.
    Source: the owner's half-up rule (register, 21 Nov 2026); Python decimal ROUND_HALF_UP rounds
    exact halves away from zero (https://docs.python.org/3/library/decimal.html#rounding-modes).
    """
    assert to_minor(Decimal(value), "GBP").amount_minor == minor


@pytest.mark.parametrize(
    ("value", "minor"),
    [
        ("415.01", 42000),
        ("-414.99", -41000),
        ("-415.00", -42000),
        ("-415.01", -42000),
    ],
)
def test_round_estimate_ten_pound_boundaries(value: str, minor: int) -> None:
    """Estimate rounding to the nearest 10 pounds, just below, exactly at and just above half.

    Working: value / 10 is 41.501, -41.499, -41.5, -41.501. Half up gives 42, -41, -42, -42
    (exact half goes away from zero), times 10 is 420, -410, -420, -420 pounds, so 42000, -41000,
    -42000, -42000 pence. The positive 414.99 and 415.00 cases are in test_estimate_nearest_ten.
    Source: owner's estimate rule and half-up rule (21 Nov 2026); Python decimal ROUND_HALF_UP
    (https://docs.python.org/3/library/decimal.html#rounding-modes).
    """
    assert round_estimate(Decimal(value), "GBP") == gbp(minor)


def test_total_rounds_once() -> None:
    """Two lines of 0.004 pounds total 0.01 pounds, not 0.00.

    Working: 0.004 + 0.004 = 0.008 pounds = 0.8 pence, which rounds to 1 penny. Rounding each
    line first gives 0 + 0 = 0.
    Source: the owner's rounding rule (round once, at the end).
    """
    assert total([Decimal("0.004"), Decimal("0.004")], "GBP").amount_minor == 1


@pytest.mark.parametrize(
    ("value", "minor"),
    [
        ("417.00", 42000),
        ("415.00", 42000),
        ("414.99", 41000),
    ],
)
def test_estimate_nearest_ten(value: str, minor: int) -> None:
    """Estimates round to the nearest 10 pounds, half up.

    Working: 417 is between 410 and 420 and nearer 420; 415 is exactly half way, half up gives
    420; 414.99 is below half way, so 410. In pence: 42000, 42000, 41000.
    Source: owner's estimate rule (21 Nov 2026) and the rounding rule (half up).
    """
    assert round_estimate(Decimal(value), "GBP") == gbp(minor)


def test_estimate_rounds_once_from_exact() -> None:
    """414.999 pounds shows as 410, though its penny value is 415.00.

    Working: 414.999 is below 415, so the nearest 10 is 410. Rounding to the penny first gives
    415.00, then to 10 gives 420, which is wrong (two roundings).
    Source: owner's estimate rule (21 Nov 2026): round once from the exact value.
    """
    assert round_estimate(Decimal("414.999"), "GBP") == gbp(41000)
    result = estimate(Decimal("414.999"), "GBP")
    assert result.exact == gbp(41500)
    assert result.shown == gbp(41000)
    assert result.is_estimate is True


def test_sample_estimates_round_once() -> None:
    """In every sample file (widgets and trip), each estimate's shown is round_estimate(exact).

    Working: each exact is read from the file, rounded to the nearest 10 pounds, half up, as in
    the table in schemas/samples/README.md (for example 78200 pence -> 78000).
    Source: schemas/samples/README.md, "Rounding working for MoneyEstimate.shown".
    """
    checked = 0
    in_trip = 0

    def walk(node: object) -> None:
        nonlocal checked
        if isinstance(node, dict):
            if {"exact", "shown", "is_estimate"} <= node.keys():
                money = MoneyEstimate.model_validate(node)
                if money.is_estimate:
                    want = round_estimate(exact(money.exact), money.exact.currency)
                    assert money.shown == want, node
                    checked += 1
            for child in node.values():
                walk(child)
        elif isinstance(node, list):
            for child in node:
                walk(child)

    for path in sorted(SAMPLES.rglob("*.json")):
        before = checked
        walk(json.loads(path.read_text(encoding="utf-8")))
        if path.parent.name == "trip":
            in_trip += checked - before
    assert checked > 0
    assert in_trip > 0, "the walk must reach the estimates in the trip sample"


def test_unknown_currency_raises() -> None:
    """A currency with no entry in currencies.json is refused, never guessed.

    Working: XYZ is not in the data file, which lists GBP and EUR only.
    Source: backend/src/app/data/currencies.json.
    """
    with pytest.raises(UnknownCurrency):
        to_minor(Decimal("1"), "XYZ")


def test_lisbon_known_costs() -> None:
    """Lisbon known costs 782 pounds show as 780; the 18 pound gap to 800 shows as 20.

    Working: 782 is between 780 and 790 and nearer 780 -> 78000 pence. 800 - 782 = 18, which is
    between 10 and 20 and nearer 20 -> 2000 pence.
    Source: schemas/samples/README.md rounding table, from docs/design/boards/sample-data.md.
    """
    known = estimate(Decimal("782"), "GBP")
    assert known.shown == gbp(78000)
    gap = estimate(Decimal("800") - Decimal("782"), "GBP")
    assert gap.exact == gbp(1800)
    assert gap.shown == gbp(2000)
