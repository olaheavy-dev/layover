# Sample data for the boards

**Sample data, not real.** Every figure, date, age, hotel name and opening time in this file is made up for the design boards. None is a real fare, rate, forecast or advice date. Owner: "Marked samples, one file (Recommended)", 20 Nov 2026 ([brief](../brief.md#sample-content-on-the-boards)).

Rules:

- A board takes every figure from this file and never types a new one. If a board needs a figure that is not here, add it here first.
- Every board page shows the label "Sample data, not real" (`make check` fails without it).
- Place names are real, so the boards look like Layover. Links go to real pages (the FCDO page for the country, Aviasales search). Hotel names are made up and start with "Sample", so nobody can take them for real hotels.
- Totals below are worked by hand, so the boards agree with each other. Layover's real totals come from tested code (decision 0011, rule 3).

## The brief

| Field | Sample value |
|---|---|
| From | Manchester (MAN) |
| When | May 2027, 5 nights |
| Travellers | 2 adults |
| Budget | £800 in total |
| Feel | Warm, relaxed, good food |
| Trip name | "Lisbon, May" after the pick; "Warm break, May" before it; "New trip" before the brief has fields |

## The three places

The cost lines use one rule for every place, so the boards stay consistent: flights are the fare per person × 2; stay is the nightly estimate × 5 nights; meals are the meal estimate × 2 people × 5 days × 2 meals a day. The real meal rule is set in the build plan; this is a sample.

| | Lisbon | Valencia | Valletta |
|---|---|---|---|
| Fare from MAN, return, per person | £96, Cached, 3 days old | £84, Cached, 1 day old | £121, Cached, 6 days old |
| Flights for 2 | £96 × 2 = £192 | £84 × 2 = £168 | £121 × 2 = £242 |
| Stay estimate per night | about £70 (estimate from 6 Wikivoyage listings, page edited March 2026, Cached, 4 days old) | Not known (too few priced listings) | about £80 (estimate from 5 Wikivoyage listings, page edited January 2026, Cached, 9 days old) |
| Stay for 5 nights | £70 × 5 = £350 | Not known | £80 × 5 = £400 |
| Meal estimate, one person | about £12 (estimate from the same Wikivoyage page, Cached, 4 days old) | about £11 (estimate from 5 Wikivoyage listings, page edited February 2026, Cached, 2 days old) | about £13 (estimate from the same Wikivoyage page, Cached, 9 days old) |
| Meals | £12 × 2 × 5 × 2 = £240 | £11 × 2 × 5 × 2 = £220 | £13 × 2 × 5 × 2 = £260 |
| Known costs | £192 + £350 + £240 = £782, partial (local transport and activities not known) | £168 + £220 = £388, partial (stay, local transport and activities not known) | £242 + £400 + £260 = £902, partial (local transport and activities not known) |
| Against £800 | £800 − £782 = £18 under on the known costs; the costs that are not known could take it over | Not known: stay is missing | £902 − £800 = £102 over on the known costs alone |
| Local transport, activities | Not known | Not known | Not known |
| May temperature, typical high and low | 22°C and 14°C | 24°C and 15°C | 23°C and 16°C |
| Rainy days in May, typical | 5 | 4 | 2 |
| Sea temperature (sample label: "Source: Open-Meteo Marine, Live") | 17°C | 18°C | 19°C |
| Currency | Euro | Euro | Euro |
| FCDO page | [Portugal](https://www.gov.uk/foreign-travel-advice/portugal) | [Spain](https://www.gov.uk/foreign-travel-advice/spain) | [Malta](https://www.gov.uk/foreign-travel-advice/malta) |
| FCDO "updated" date | 12 Nov 2026 | 3 Nov 2026 | 28 Oct 2026 |

States to draw with these places:

- Valencia's stay row is the "Not known" row in the comparison.
- Valletta is the "over budget" state of `cost_estimate`.
- For the error state of one comparison card, Valletta's card fails and offers "Try again".

## The chosen place: Lisbon

| Widget | Sample content |
|---|---|
| `money` | £1 = €1.15, European Central Bank rate for 18 Nov 2026, Live. Conversion: £500 is about €575 (£500 × 1.15 = €575) |
| `daylight` | 15 May 2027: sunrise 06:20, sunset 20:40, day length 14 h 20 min (20:40 − 06:20 = 14 h 20 min) |
| `climate_chart` | The May row above. The months either side for the chart: April 20°C and 12°C, 7 rainy days; June 25°C and 16°C, 2 rainy days. Averages period: 1991 to 2020, Live |
| `place_intro` | Two sentences in Layover's own words, with "Source: Wikivoyage, Lisbon, page edited March 2026, Cached, 4 days old". For the Fallback state: "Fallback: Wikipedia, Lisbon" |
| `advice_card` | "FCDO travel advice: Portugal, updated 12 Nov 2026", Layover's copy Cached, 1 day old, with the link above. Error state: the same link and "Layover could not read it just now" |

## The long chat and the phone cue

Used on `trip-lisbon-chat.html`. The labels follow the rule in the [brief](../brief.md#source-labels).

| Item | Sample content |
|---|---|
| Trip strip | "Lisbon, May", "5 facts ready" (fare, cost estimate, advice, weather, money), "View trip" |
| Trip tab badge | "3 new" |
| Compact cards | Flights: £96 return per person, Cached, 3 days old. Cost estimate: about £782, estimate, partial, Cached, 3 to 4 days old (the flights are 3 days old and the Wikivoyage lines 4). Travel advice: FCDO advice for Portugal, updated 12 Nov 2026, Cached, 1 day old. Weather in May: highs of 22°C, lows of 14°C, 5 rainy days, Live. Money: £1 = €1.15, rate for 18 Nov 2026, Live |
| Side question: the beach | "The sea is 17°C in May. Typical highs are 22°C, with 5 rainy days." Source line: Live; Sea: Open-Meteo Marine; Weather: Open-Meteo |
| Side question: what the estimate leaves out | Local transport and activities: Not known, not counted as £0 |
| Side question: the FCDO date | "The FCDO page for Portugal was updated on 12 Nov 2026." Layover's copy: Cached, 1 day old |
| Checks rows | 2 checks (fares and weather for 3 places), 4 checks (FCDO advice, exchange rate, sunrise and sunset, Wikivoyage page), 2 checks (sea temperature, typical May weather), 1 check (FCDO advice) |

## Vague and unclear messages

Used on `vague.html` (four states). Sample messages written for the boards; none is a real traveller's message. Facts allowed: place names and the money figures already above. "Not too pricey" is the traveller's own wording, not a budget: no amount is set until Layover asks.

| State | Traveller says | Layover says and offers |
|---|---|---|
| Missing detail | "Somewhere warm in May, not too pricey" | "Good start. I have May, somewhere warm, and not too pricey. Nothing is confirmed yet." Question: "Which airport would you fly from?" Quick answers: Manchester (MAN), London Heathrow (LHR), Birmingham (BHX), Somewhere else. Trip name: "Warm break, May". Brief so far: May; Warm; Budget: not too pricey (no amount yet). Not set yet: Departure airport, Length, Travellers |
| One clarifying question | "Lisbon or Porto?" | "I can do a few things with that." Question: "Do you want to compare the two for a trip, or plan days in one of them?" Choices: Compare them for a trip, Plan days in Lisbon, Plan days in Porto, Something else. Trip name: "New trip" |
| Which place | "Three days in Valencia" | "More than one place has that name, so I will not guess." Question: "Which Valencia do you mean?" Choices: Valencia, Spain; Valencia, Venezuela; Somewhere else. Both are real places; the board says nothing else about them. Trip name: "New trip" |
| Side answer, no place yet | "How much is £500 in euros?" | The `money` widget in the chat: £1 = €1.15, £500 is about €575 (from the `money` row above: £500 × 1.15 = €575), Live, European Central Bank rate for 18 Nov 2026, Source: Frankfurter. No "Add to trip" (no place yet). "Here is the conversion. Say where you want to go, or what kind of break, and I will start a trip." Trip name: "New trip" |

Empty canvas lines: "It appears here once Layover knows what you want." (clarifying question), "It appears here once you have chosen the place." (which place), "It appears here once you have a place." (side answer).

## Where you're staying

| Hotel (made up) | Area | Stars | Website |
|---|---|---|---|
| Sample Hotel Alfama | Alfama | 4 | Not known |
| Sample Guesthouse Baixa | Baixa | Not known | Not known |
| Sample Hotel Belém | Belém | 3 | sample.example (made up) |

The chosen state uses Sample Hotel Alfama. The skipped state says "Days start from the centre of Lisbon".

## Days

| Day | Stops | Notes |
|---|---|---|
| Day 1 | Castelo de São Jorge (10:00 to 18:00), Miradouro de Santa Luzia (opening times Not known), a walk through Alfama (no opening times: it is a walk) | Opening hours are sample values |
| Day 2 | Torre de Belém (opening times Not known), Mosteiro dos Jerónimos (10:00 to 17:30) | Draws the row-level "Not known" |
| Day 3 | Too few sourced places for the afternoon | Draws the Empty state of `itinerary_day` |

## Booking (sandbox)

| Field | Sample value |
|---|---|
| Flights | MAN to LIS, 14 May 2027, back 19 May 2027, 2 adults |
| Sandbox price | £192 for 2 (the same as the fare above) |
| Price-changed state | £204 for 2, and Layover asks again |
| Approved state | Sandbox order SANDBOX-0001, "Sandbox: no real booking or payment" |
| Hotel | Flights only on the boards, until Nuitee agrees to sandbox use (status file) |

## Web results

Question: "Can I take a pushchair on Lisbon trams?" Two results, each a made-up quote from `example.org` with the retrieval date 18 Nov 2026, labelled "From a web search, not checked by Layover". The boards never quote a real site with made-up words.

## Sharing

Shared trip "as of" 18 Nov 2026. Every age on the shared board is shown "as of" that date.

## Widget gallery: place widgets

Used on `widgets-place.html`. One extra state needs a figure that the tables above do not hold: Lisbon's cost estimate when the fares source fails.

| Item | Sample content |
|---|---|
| Lisbon cost estimate, fares source failed | Flights: Unavailable (no figure). Stay £70 × 5 = £350 and meals £12 × 2 × 5 × 2 = £240, as above. Known costs so far: £350 + £240 = £590, partial (flights, local transport and activities missing). No comparison with the £800 budget, because a missing line could change the answer |

## Widget gallery: journey widgets

Used on `widgets-journey.html`. Only what the gallery needs beyond the sections above. None of it is a real fact.

| Item | Sample content |
|---|---|
| Swapped place | The traveller types "Porto" to replace Valletta. The card is named by what they typed, says "Researching your place" and shows no figure and no photo |
| No place fits | Only the brief above is used: the budget chip "£800 in total" is marked as the part that rules places out. No other figure is shown |
| Day 1 stops | Only the castle has opening hours (10:00 to 18:00). The viewpoint and the walk show no hours row. The walk comes from Wikivoyage, Lisbon, Cached, 4 days old; the other stops come from OpenStreetMap, Live |
| Day 2 after a hotel change | The rebuilt-day note uses the Day 2 stops, because Torre de Belém and Mosteiro dos Jerónimos are in Belém, the base of Sample Hotel Belém |
| Booking, price you saw and price now | £192 for 2 and £204 for 2 (no difference is shown). Declined: "Nothing was ordered" |
| Web result quotes | Two made-up quotes from `example.org`, retrieved 18 Nov 2026: "Fold the pushchair before you board if the tram is busy." and "Ask the driver where to stand with a pushchair." Each is marked "sample quote" |
| `not_known` answer | "Layover doesn't know local bus fares in Lisbon: none of its sources has them. It can show the cost estimate without them." |
| Compact card ages | Compare places: "Cached, 1 to 6 days old" (the fares are 3, 1 and 6 days old). Known costs: Lisbon "3 to 4 days old", Valencia "1 to 2 days old", Valletta "6 to 9 days old" (the flights and the Wikivoyage lines) |

## Widget gallery: proposed widgets

Used on `widgets-proposed.html` (proposals for [#26](https://github.com/olaheavy-dev/layover/issues/26)). Made up for the boards, except the two time zone rows, which were derived and checked.

| Item | Sample content |
|---|---|
| Release dates in labels | "Cached, release of 1 Nov 2026" is a made-up date for the library or database release. The real widget shows the real release |
| `public_holidays` | Lisbon, 14 to 19 May 2027. Layover could not run the holidays library for these boards, so no real holiday date is used. Two made-up rows, both named "Sample holiday": Mon 17 May 2027 (day 4 of the trip) and Wed 19 May 2027 (the day you fly home). The weekdays are worked from 14 May 2027 being a Friday. The Empty state ("No public holidays on 14 to 19 May 2027") is a sample outcome and is not checked against the library |
| `time_difference`, Lisbon | Derived with Python `zoneinfo` on 20 Nov 2026, for 14 May 2027 at 12:00: `Europe/London` is BST, UTC+1; `Europe/Lisbon` is WEST, UTC+1. Difference 1 − 1 = 0 hours: "Same time as the UK" |
| `time_difference`, Valletta | Same check: `Europe/Malta` is CEST, UTC+2. Difference 2 − 1 = 1 hour ahead: 12:00 in the UK is 13:00 in Valletta. The tz data release on the machine was not recorded |
| `fare_list` | From Bristol (BRS), leaving in March 2027, return, per person, all made up and sorted lowest first: Faro £59 (Cached, 3 days old), Valencia £64 (1 day), Lisbon £71 (2 days), Valletta £98 (5 days). Naples is the "Not known" row: no cached fare. Compact card: "From £59", "Cached, 1 to 5 days old" for the four fares shown. Whether these routes run from Bristol is not claimed |
| `transport_route` | A made-up journey from Paddington station to Heathrow Terminals 2 and 3: walk to the platform 5 min, Elizabeth line 32 min, walk to departures 6 min. Total 5 + 32 + 6 = 43 min. Planned for Fri 14 May 2027, leaving 09:00 (made up). Station and line names are real places and services, but the times are not TfL's |
