"""Money arithmetic: exact values, one rounding at the end, and estimates.

Rules (owner, 21 Nov 2026): carry full precision through a calculation, then round once to the
minor unit, half up. An estimate is rounded once, straight from the unrounded amount, to the
nearest 10 major units, half up. Money is integer minor units or `Decimal`, never a float.
The model never does this arithmetic (decision 0011, rule 3).
"""

import json
from collections.abc import Iterable
from decimal import ROUND_HALF_UP, Decimal
from functools import lru_cache
from pathlib import Path

from app.contract.common import MoneyEstimate, MoneyValue

_CURRENCIES = Path(__file__).parent / "data" / "currencies.json"
_ESTIMATE_STEP = Decimal(10)  # major units


class UnknownCurrency(Exception):
    """The currency has no minor-unit exponent in `data/currencies.json`."""


@lru_cache
def _exponents() -> dict[str, int]:
    data = json.loads(_CURRENCIES.read_text(encoding="utf-8"))
    return {code: int(exp) for code, exp in data["minor_unit_exponents"].items()}


def _scale(currency: str) -> Decimal:
    """Minor units per major unit: 100 for GBP and EUR."""
    try:
        return Decimal(10) ** _exponents()[currency]
    except KeyError:
        raise UnknownCurrency(currency) from None


def exact(amount: MoneyValue) -> Decimal:
    """The amount in major units, exactly (78200 GBP pence is 782)."""
    return Decimal(amount.amount_minor) / _scale(amount.currency)


def convert_exact(amount: MoneyValue, rate: Decimal) -> Decimal:
    """The amount times a rate, in major units, unrounded. Round once with `to_minor`."""
    return exact(amount) * rate


def to_minor(value: Decimal, currency: str) -> MoneyValue:
    """Round a major-unit `Decimal` to whole minor units, half up."""
    minor = (value * _scale(currency)).quantize(Decimal(1), rounding=ROUND_HALF_UP)
    return MoneyValue(amount_minor=int(minor), currency=currency)


def total(values: Iterable[Decimal], currency: str) -> MoneyValue:
    """Sum unrounded values exactly, then round once."""
    return to_minor(sum(values, Decimal(0)), currency)


def round_estimate(exact: Decimal, currency: str) -> MoneyValue:
    """Round the unrounded amount to the nearest 10 major units, half up, in one step."""
    tens = (exact / _ESTIMATE_STEP).quantize(Decimal(1), rounding=ROUND_HALF_UP)
    return to_minor(tens * _ESTIMATE_STEP, currency)


def estimate(exact: Decimal, currency: str) -> MoneyEstimate:
    """An estimate: `exact` to the penny and `shown` to the nearest 10, both from `exact`."""
    return MoneyEstimate(
        exact=to_minor(exact, currency),
        shown=round_estimate(exact, currency),
        is_estimate=True,
    )
