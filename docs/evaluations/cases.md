# Evaluation cases

The master list of Layover's evaluation cases, and the coverage table for the Design gate (`AGENTS.md`, "Review rounds and debt"; issue [#39](https://github.com/olaheavy-dev/layover/issues/39)).

Each case has a permanent ID: an area code and a number (`AGENTS.md`). An ID is never reused or renumbered. A case that is no longer needed stays in the table, marked `withdrawn`. `make check` runs `tools/check_eval_ids.py`. It fails when an ID is defined twice, is not in `AREA-NN` form, or is cited under `docs/` without a row here.

**Status.** `planned` means the case is written but not yet run. The build step that adds a case's code also adds the case to the evaluation set ([01 §4](../product/01-research-and-direction.md)). The Design gate has no evaluation set yet, so it reports no scores.

**Scored by** (spec §7): *code* for factual checks (sources, budget, approval, labels); *judge* for a model that scores against a written rubric, with the owner spot-checking a sample. Each evaluation trip has a scripted traveller that answers the brief questions, picks a place, and approves or rejects booking.

**Areas.** `INTENT` classifying messages, `BRIEF` the brief, `COMPARE` comparing places, `TRIP` the whole trip and the trip summary, `ITIN` the itinerary and where to stay, `BOOK` the sandbox booking, `SHARE` trip links, `WIDGET` one widget `kind`. The first 16 cases come from the [journey design, §7](../superpowers/specs/2026-11-19-layover-journey-design.md#7-evaluations), with the same IDs and meaning.

## Cases

| ID | Area | What it checks | Passes when | Fails when | Scored by | Status |
|---|---|---|---|---|---|---|
| `INTENT-01` | Intent | Each example message in spec §5a is classified to its intent | Every example gets the intent it is listed under | Any example gets another intent | code | planned |
| `INTENT-02` | Intent | A non-travel request is declined | The reply declines politely and offers what Layover can do | The reply answers the request | code | planned |
| `INTENT-03` | Intent | An unsupported travel question gets web-search quotes, or "not yet" | Quotes with links, the retrieval date and the "not checked by Layover" label; or "I can't help with that yet" | An answer with no source, or a quote without its link or label | code | planned |
| `INTENT-04` | Intent | A non-travel question (for example about investments) is declined without a web search | No web-search call, and a decline | A web-search call is made | code | planned |
| `INTENT-05` | Intent | A web-search query never contains the traveller's details | The query holds the travel question only | The query holds a name, budget, dates, party size or home airport from the trip | code | planned |
| `INTENT-06` | Intent | A message the classifier isn't confident about gets one clarifying question | One question, and no tool call until it is answered | Layover guesses an intent and runs a tool | code | planned |
| `INTENT-07` | Intent | A side question (`destination_facts`) during `plan_trip` keeps the trip | After the side answer, the brief, comparison and choice are unchanged, and the journey carries on | Any part of the trip state is lost or changed | code | planned |
| `INTENT-08` | Intent | An entry or safety answer links the FCDO page and shows its update date | The FCDO link and its "updated" date are in the answer, and the destination is never called "safe" | No FCDO link, no update date, or "safe" used of a destination | code | planned |
| `BRIEF-01` | Brief | A vague request ends in a confirmed summary with every field set | Departure airport, month or dates, length, people, budget and feel are all set, and the traveller confirmed | A search starts with a field missing or unconfirmed | code | planned |
| `BRIEF-02` | Brief | A budget or date misread is corrected before searching | The traveller's correction is in the confirmed brief before any search | A search runs on the misread value | code | planned |
| `BRIEF-03` | Brief | A place name with more than one match gets a "which one" question | The matches are offered as choices, and nothing is searched until one is picked | Layover picks one of the matches itself | code | planned |
| `COMPARE-01` | Compare | All three places stay within the budget in code, or say why not | Each place's budget line comes from the tested budget check, and a place over budget says by how much | A place is shown as within budget without the check, or over budget without saying so | code | planned |
| `COMPARE-02` | Compare | Every figure carries its source and age | Every figure in the comparison has a label (Live, Cached with its age, Fallback or Unavailable) | A figure with no label or no age | code | planned |
| `COMPARE-03` | Compare | No destination is called "safe" | The word is never used of a destination | The word is used of a destination | code | planned |
| `COMPARE-04` | Compare | The traveller swaps a place for one of their own | The new place is researched like the others, and the comparison is checked again in code | The swapped place has fewer checks, or the old ranking stays | code | planned |
| `COMPARE-05` | Compare | A total shown to the traveller came from a tool call | Each total or conversion in the reply matches a tool result in the trace | A figure in the reply has no matching tool result (the model did the sum) | code | planned |
| `COMPARE-06` | Compare | The three places fit the brief | The places match the brief's month, feel and departure airport (rubric) | The rubric score is below its threshold, set in the plan that adds the case | judge | planned |
| `TRIP-01` | Trip | The agent team and the single-agent baseline run the same trips | Both run the same trip set, and speed, tokens and quality are reported side by side with the set's size | The sets differ, or a figure is reported without the other or the set size | code | planned |
| `TRIP-02` | Trip | After the pick, the chosen place and the confirmed brief carry into the summary unchanged | The summary is for the chosen place, with the confirmed brief | The summary uses another place, or a changed brief | code | planned |
| `TRIP-03` | Trip | The trip summary shows each section with its source, or "not known" | Fares, weather, sea, daylight, holidays, money, FCDO advice, introduction, photos and map are each shown with a label, or as "Not known" | A section is left out without saying so, or shown with no label | code | planned |
| `TRIP-04` | Trip | Every source cited in a trip is listed in [data sources](../references/data-sources.md) | Every source name in the trip's labels and links has a row there | A source with no row (decision 0011, rule 5) | code | planned |
| `ITIN-01` | Itinerary | Every stop exists in the source data | Each stop links to an OpenStreetMap, Wikivoyage or Wikipedia record that exists | A stop with no source record | code | planned |
| `ITIN-02` | Itinerary | A gap in the data is stated, not filled | Missing opening times or too few places are stated in words | A missing value is filled in or guessed | judge | planned |
| `ITIN-03` | Itinerary | The days start from the chosen hotel | With a hotel chosen, each day starts from it; with none, from the centre, and the day says so | The days ignore the chosen hotel | code | planned |
| `ITIN-04` | Itinerary | The hotel list shows no prices | Names, locations and tagged details only | Any price or price range | code | planned |
| `ITIN-05` | Itinerary | The days are arranged sensibly | Stops are grouped by distance and fit known opening times and the weather (rubric) | The rubric score is below its threshold, set in the plan that adds the case | judge | planned |
| `BOOK-01` | Booking | No order is placed without the approval step | Every order call follows a recorded approval | An order call with no approval | code | planned |
| `BOOK-02` | Booking | The booking is labelled as a sandbox and never uses a Travelpayouts fare | "Sandbox: no real booking or payment" shows, and prices come from Duffel or Nuitee | The label is missing, or a Travelpayouts fare is used | code | planned |
| `BOOK-03` | Booking | Layover asks for exact dates before booking and never picks them | With only a month known, booking asks for dates first | Layover searches with dates it chose | code | planned |
| `BOOK-04` | Booking | A price change at the price check asks for approval again | The new price is shown and approved before any order | An order is placed at the changed price without a new approval | code | planned |
| `BOOK-05` | Booking | Flights only, if Nuitee is unavailable | Booking offers flights only and says why | A hotel booking is attempted or shown without the sandbox | code | planned |
| `SHARE-01` | Share | A shared link opens a frozen copy | The copy shows the trip as at the share date, with "as of" on every label, and no chat | It shows live values, labels without "as of", or the chat | code | planned |
| `SHARE-02` | Share | "Include my budget and who's travelling" off by default | With the tick box off, the shared copy has no budget, no traveller chips and no budget lines | Any of them shows | code | planned |
| `WIDGET-01` | Widget | `brief_summary` | Output is valid against its schema; its states match the [brief's state table](../design/brief.md#widget-states) | A state missing or different from the table | code | planned |
| `WIDGET-02` | Widget | `comparison_table` | As `WIDGET-01`; one failed card keeps the other two; "Not known" rows are never zero | As `WIDGET-01`, or a failed card hides the others | code | planned |
| `WIDGET-03` | Widget | `fare_card` | As `WIDGET-01`; Cached with its age; a fare with no data shows no price | As `WIDGET-01`, or a figure with no cached fare behind it (decision 0011, rule 1) | code | planned |
| `WIDGET-04` | Widget | `climate_chart` | As `WIDGET-01`; one missing series is "Not known", the other still shows | As `WIDGET-01` | code | planned |
| `WIDGET-05` | Widget | `sea_conditions` | As `WIDGET-01`; not shown at all for an inland place | As `WIDGET-01`, or an empty card for an inland place | code | planned |
| `WIDGET-06` | Widget | `daylight` | As `WIDGET-01`; uses the middle of the month and says so when no dates are given | As `WIDGET-01` | code | planned |
| `WIDGET-07` | Widget | `money` | As `WIDGET-01`; the rate shows its date and source; a currency outside the reference rates is "Not known" | As `WIDGET-01`, or a rate shown as 0 or 1 | code | planned |
| `WIDGET-08` | Widget | `advice_card` | As `WIDGET-01`; the FCDO link and update date always show, even when the page could not be read | As `WIDGET-01`, or "safe" used of a destination | code | planned |
| `WIDGET-09` | Widget | `place_intro` | As `WIDGET-01`; the Wikipedia fallback is labelled "Fallback: Wikipedia" | As `WIDGET-01`, or a fallback without its label | code | planned |
| `WIDGET-10` | Widget | `map` | As `WIDGET-01`; when the map can't load, the places show as a list with links | As `WIDGET-01` | code | planned |
| `WIDGET-11` | Widget | `itinerary_day` | As `WIDGET-01`; each stop links to its source | As `WIDGET-01` | code | planned |
| `WIDGET-12` | Widget | `hotel_list` | As `WIDGET-01`; no hotels tagged says so, and the days start from the centre | As `WIDGET-01` | code | planned |
| `WIDGET-13` | Widget | `cost_estimate` | As `WIDGET-01`; uncovered lines say "Not known"; a total with a failed line says it is partial | As `WIDGET-01`, or a missing cost counted as zero (decision 0011, rule 4) | code | planned |
| `WIDGET-14` | Widget | `booking_approval` | As `WIDGET-01`; the sandbox label always shows | As `WIDGET-01` | code | planned |
| `WIDGET-15` | Widget | `web_results` | As `WIDGET-01`; always labelled "From a web search, not checked by Layover" with the retrieval date; never "Add to trip" | As `WIDGET-01`, or labelled Live or Cached | code | planned |
| `WIDGET-16` | Widget | `not_known` | As `WIDGET-01`; says what is missing, why, and what Layover can do instead | As `WIDGET-01` | code | planned |
| `WIDGET-17` | Widget | `public_holidays` (proposed for #26) | As `WIDGET-01`; Cached with the data's release date; says local or regional holidays may be missing | As `WIDGET-01` | code | planned |
| `WIDGET-18` | Widget | `time_difference` (proposed for #26) | As `WIDGET-01`; Cached with the time-zone data's release date | As `WIDGET-01` | code | planned |
| `WIDGET-19` | Widget | `fare_list` (proposed for #26) | As `WIDGET-01`; every fare Cached with its age | As `WIDGET-01` | code | planned |
| `WIDGET-20` | Widget | `transport_route` (proposed for #26) | As `WIDGET-01`; labelled with its source | As `WIDGET-01` | code | planned |

The four proposed kinds get their schemas in build plan 1 ([#26](https://github.com/olaheavy-dev/layover/issues/26)); their state rows join the brief's table then.

## Coverage

Every intent, journey step, widget `kind` and decision 0011 rule has at least one case (`AGENTS.md`, "Evaluations at each gate"). A gap blocks the gate. Reviewers check these tables against the spec, the brief and decision 0011.

### Intents ([spec §5a](../superpowers/specs/2026-11-19-layover-journey-design.md))

| Intent | Cases |
|---|---|
| `plan_trip` | `INTENT-01`, `INTENT-07`, `BRIEF-01` |
| `destination_facts` | `INTENT-01`, `INTENT-07`, `INTENT-08` |
| `itinerary` | `INTENT-01`, `ITIN-01` |
| `fares_and_transport` | `INTENT-01`, `WIDGET-19`, `WIDGET-20` |
| `unsupported_travel` | `INTENT-03`, `INTENT-05` |
| `not_travel` | `INTENT-02`, `INTENT-04` |
| Not confident (no intent yet) | `INTENT-06` |

### Journey steps ([spec §5](../superpowers/specs/2026-11-19-layover-journey-design.md#5-the-journey-plan_trip))

| Step | Cases |
|---|---|
| 1. Brief | `BRIEF-01`, `BRIEF-02`, `BRIEF-03`, `WIDGET-01` |
| 2. Compare three places | `COMPARE-01` to `COMPARE-06`, `WIDGET-02` |
| 3. Pick | `TRIP-02` |
| 4. Trip summary | `TRIP-03`, `WIDGET-03` to `WIDGET-10`, `WIDGET-17`, `WIDGET-18` |
| 5. Itinerary | `ITIN-01`, `ITIN-02`, `ITIN-03`, `ITIN-05`, `WIDGET-11` |
| 6. Where to stay | `ITIN-04`, `WIDGET-12` |
| 7. Try booking | `BOOK-01` to `BOOK-05`, `WIDGET-14` |
| 8. Keep it (trip links) | `SHARE-01`, `SHARE-02` |
| The whole journey, team against baseline | `TRIP-01` |

### Widget kinds ([spec §5d](../superpowers/specs/2026-11-19-layover-journey-design.md#5d-widgets-for-tool-results-and-the-design-bar) and #26)

| `kind` | Cases |
|---|---|
| `brief_summary` | `WIDGET-01`, `BRIEF-01` |
| `comparison_table` | `WIDGET-02`, `COMPARE-02` |
| `fare_card` | `WIDGET-03` |
| `climate_chart` | `WIDGET-04` |
| `sea_conditions` | `WIDGET-05` |
| `daylight` | `WIDGET-06` |
| `money` | `WIDGET-07` |
| `advice_card` | `WIDGET-08`, `INTENT-08` |
| `place_intro` | `WIDGET-09` |
| `map` | `WIDGET-10` |
| `itinerary_day` | `WIDGET-11`, `ITIN-01` |
| `hotel_list` | `WIDGET-12`, `ITIN-04` |
| `cost_estimate` | `WIDGET-13`, `COMPARE-01` |
| `booking_approval` | `WIDGET-14`, `BOOK-01` |
| `web_results` | `WIDGET-15`, `INTENT-03` |
| `not_known` | `WIDGET-16` |
| `public_holidays` (proposed) | `WIDGET-17` |
| `time_difference` (proposed) | `WIDGET-18` |
| `fare_list` (proposed) | `WIDGET-19` |
| `transport_route` (proposed) | `WIDGET-20` |

### Decision 0011 rules ([product integrity rules](../decisions/0011-product-integrity-rules.md))

| Rule | Cases |
|---|---|
| 1. No invented facts | `WIDGET-03`, `ITIN-01`, `INTENT-03` |
| 2. Every outside value is labelled | `COMPARE-02`, `TRIP-03`, `WIDGET-01` to `WIDGET-20` |
| 3. The model never does the arithmetic | `COMPARE-01`, `COMPARE-05` |
| 4. Missing data is never shown as zero | `ITIN-02`, `WIDGET-07`, `WIDGET-13` |
| 5. No scraping | `TRIP-04` |
| 6. FCDO links and never "safe" | `INTENT-08`, `COMPARE-03`, `WIDGET-08` |
