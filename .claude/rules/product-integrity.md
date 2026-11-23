# Product integrity rules

Decision [0011](../../docs/decisions/0011-product-integrity-rules.md), accepted by the owner on 19 Nov 2026. These apply to code, copy, prompts, evaluations and docs.

| Rule | How it is checked |
|---|---|
| 1. **No invented facts.** Prices, entry rules, safety advice, opening times and figures come from a cited source or are not shown. | Review rule. Evaluation cases (for example "a fare with no data shows no price") are planned for step 2, when the planner exists |
| 2. **Every outside value is labelled** Live, Cached (with its age), Fallback or Unavailable. | Tests on each adapter's output (`backend/tests/sources/test_holidays.py`) and on the website's label (`SourceLabel.test.tsx`); review rule. Each new adapter adds its own tests |
| 3. **The model never does the arithmetic.** Budget totals, currency conversions and comparisons come from tested code (the `test-first` skill). | `tools/check_numeric_tests.py` (in `make check`) requires "Working:" and "Source:" in the backend money tests (the website's money tests are tracked in #111); tests with hand-worked expected values. Planned: an evaluation case that checks a total came from a tool call |
| 4. **Missing data is never shown as zero**, a favourable value or a clean result. | Tests for empty and error states (the widget tests and `test_holidays.py`); review rule. Evaluation cases planned for step 2 |
| 5. **No scraping.** Data comes from APIs and feeds used under their terms ([data sources](../../docs/references/data-sources.md)). | Review rule: every new source gets a row with its terms before it is used |
| 6. **Entry and safety advice always links to the FCDO page and shows its update date.** Layover never says a destination is "safe". | `tools/check_copy.py` (in `make check`) and tests that fixed copy never calls a destination safe (for example `AdviceCard.test.tsx`, "never calls the destination safe"). Planned: an evaluation case on advice answers |

Rules without an automatic check yet (1, 5 and the evaluation cases marked planned) are enforced by the Code Review Rules in `AGENTS.md`; each check is added with the code it covers.
