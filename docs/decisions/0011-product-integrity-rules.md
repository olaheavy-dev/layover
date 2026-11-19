# 0011. Product integrity rules

Status: Proposed (19 Nov 2026), awaiting the owner

## Context

Vestagraph's rules on facts and data served it well and fit a travel product directly. A public tutorial project in the same domain shows what goes wrong without them: its flight agent asks the model for an "estimated airfare range" with no price data, so the prices are invented ([TripMate review](../reviews/2026-11-19-tripmate-reference-review.md)).

## Proposed decision

1. **No invented facts.** Prices, entry rules, safety advice, opening times and figures come from a cited source or are not shown.
2. **Every outside value is labelled** Live, Cached (with its age), Fallback or Unavailable.
3. **The model never does the arithmetic.** Budget totals, currency conversions and comparisons come from tested code.
4. **Missing data is never shown as zero**, a favourable value or a clean result.
5. **No scraping.** Data comes from APIs and feeds used under their terms.
6. **Entry and safety advice always links to the FCDO page and shows its update date.** Layover never says a destination is "safe".

## Consequences

- Each rule needs a check (an evaluation case, a test or a review rule) once code exists, as `AGENTS.md` rule 7 requires.
- When accepted, these rules move into a project rules file under `.claude/rules/` so agents load them.

## Sources

- FCDO foreign travel advice: https://www.gov.uk/foreign-travel-advice
