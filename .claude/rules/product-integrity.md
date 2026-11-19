# Product integrity rules

Decision [0011](../../docs/decisions/0011-product-integrity-rules.md), accepted by the owner on 19 Nov 2026. These apply to code, copy, prompts, evaluations and docs.

| Rule | How it is checked |
|---|---|
| 1. **No invented facts.** Prices, entry rules, safety advice, opening times and figures come from a cited source or are not shown. | Review rule now; evaluation cases (for example "a fare with no data shows no price") once the planner exists |
| 2. **Every outside value is labelled** Live, Cached (with its age), Fallback or Unavailable. | Tests on each adapter's output once code exists; review rule now |
| 3. **The model never does the arithmetic.** Budget totals, currency conversions and comparisons come from tested code (the `test-first` skill). | Tests with hand-worked expected values; an evaluation case that checks a total came from a tool call |
| 4. **Missing data is never shown as zero**, a favourable value or a clean result. | Tests for empty and error states; review rule |
| 5. **No scraping.** Data comes from APIs and feeds used under their terms ([data sources](../../docs/references/data-sources.md)). | Review rule: every new source gets a row with its terms before it is used |
| 6. **Entry and safety advice always links to the FCDO page and shows its update date.** Layover never says a destination is "safe". | Evaluation case on advice answers; a test that the word "safe" isn't used to describe a destination in fixed copy |

Until code exists, each rule is enforced by the Code Review Rules in `AGENTS.md`; the checks above are added with the code they cover.
