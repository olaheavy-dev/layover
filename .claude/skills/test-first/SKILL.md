---
name: test-first
description: Test-first workflow for Layover's numeric code (budget totals, currency conversion, fare comparisons, anything Layover calculates). Use before writing implementation code for such a change, on top of Superpowers test-driven-development.
---

# Test-first workflow for numbers

Every figure Layover calculates comes from code, and this skill applies to all of it. If [proposed decision 0011](../../../docs/decisions/0011-product-integrity-rules.md) is accepted, its point 3 also rules out the model doing the arithmetic. This skill makes those tests trustworthy. It adds to Superpowers `test-driven-development`; where they differ, this skill wins for numeric code.

Write the test before the code it proves, in small vertical slices. For each slice:

1. **Write the test from a worked example**, not from the implementation: the inputs, the working step by step, and the source of each input (a recorded fare response, an exchange-rate snapshot with its date, a rounding rule). Put the working in the test's docstring or a comment. Test names follow `test_<function>_<condition>_<result>`.
2. **State the expected failure** in words before every run: which test, and why it should fail (for example "`test_convert_gbp_to_eur_half_cent_follows_rule` fails: `convert` does not exist yet").
3. **Run the test.** Only a failure that matches your statement counts. A different failure means the test or your understanding is wrong: fix that first.
4. **Stop if a test passes unexpectedly.** A test that passes before the code exists proves nothing: find out why before going on.
5. Write the smallest code that makes the test pass, then run again.
6. **Never weaken an assertion** (looser tolerance, removed case, changed expected value) to make a test pass. If an expected value looks wrong, recheck the worked example and its source, and ask the owner.
7. **Stop after 3 failed attempts** at the same problem and report what was tried.

Money is held as an integer number of minor units (pence, cents) or as `decimal.Decimal`, never as a binary float ([Python `decimal`](https://docs.python.org/3/library/decimal.html)).

Record a **slice table** in the PR description:

| Slice | Test written | Expected failure | Observed failure | Passes after |
|---|---|---|---|---|

## Rounding boundary cases

Every rounded figure names its rounding rule and cites where the rule comes from (a decision record, a register line, or the provider's documentation). If no rule is set yet, stop and ask; don't pick one. Then cover all six cases (just below, exactly and just above half a minor unit, each positive and negative), worked out before the code.

For **round-to-nearest rules** (half-up, half-even, half-down) the outcomes are:

| Case | Positive | Negative |
|---|---|---|
| Just below half | smaller in size (towards zero) | smaller in size (towards zero) |
| Exactly half | per the cited rule | per the cited rule |
| Just above half | larger in size (away from zero) | larger in size (away from zero) |

For a **directed rule** (`ROUND_FLOOR`, `ROUND_CEILING`, `ROUND_DOWN`, `ROUND_UP`), this table does not apply: work out all six cases from the rule itself. Exact halves differ between languages: Python's `decimal` `ROUND_HALF_UP` rounds -2.5 to -3 (away from zero), while JavaScript's `Math.round(-2.5)` gives -2 ([Python `decimal` rounding modes](https://docs.python.org/3/library/decimal.html#rounding-modes), [MDN `Math.round`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/round)).

Pass the rounding mode explicitly in code (for example `Decimal.quantize(..., rounding=ROUND_HALF_UP)`); never rely on a default.
