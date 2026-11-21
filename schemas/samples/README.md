# Sample files

These files are **samples**. They are not real data. Layover never uses them for a real figure: no fare, rate, forecast, advice date or total a traveller sees comes from here.

They exist so that every widget has one example in every state. They feed the backend tests, the sample API endpoints (they come in a later task) and the website's widget gallery.

- `widgets/<kind>/<state>.json`: one file for each widget kind and state in `WIDGET_STATES` (`backend/src/app/contract/widgets/__init__.py`). The file name is the state, for example `swapped.json`. The widget's own `state` field can differ: `swapped` is a `filled` comparison with one swapped card.
- `trip/sample-lisbon.json`: the sample Lisbon trip, with `is_sample` set to `true`.

Load them with `app.contract.samples` (`load_sample_trip`, `load_sample_widgets`). The folder is the `SAMPLES_DIR` setting; it defaults to this folder.

## Where each value comes from

Every value is copied from [`docs/design/boards/sample-data.md`](../../docs/design/boards/sample-data.md) and the design boards that use it. Nothing here was typed fresh. Dates are the boards' sample dates: "today" is 18 Nov 2026, and an age of "3 days old" is a `captured_at` of 15 Nov 2026 at 09:00 UTC.

| Samples | Section of `sample-data.md` |
|---|---|
| `brief_summary`, the trip's brief | "The brief" |
| `comparison_table`, `fare_card`, `cost_estimate`, the cards' weather | "The three places", "Comparison card labels", "Widget gallery: journey widgets" |
| `cost_estimate` `partial` (fares failed) | "Widget gallery: place widgets" |
| `money`, `daylight`, `climate_chart`, `place_intro`, `advice_card` | "The chosen place: Lisbon" |
| `sea_conditions` | "The three places" (sea temperature) |
| `hotel_list` | "Where you're staying" |
| `itinerary_day` | "Days", "Widget gallery: journey widgets" |
| `booking_approval` | "Booking (sandbox)" |
| `web_results`, `not_known` | "Web results", "Widget gallery: journey widgets" |
| `public_holidays`, `time_difference`, `fare_list`, `transport_route` | "Widget gallery: proposed widgets" |

Notes on values the boards give only in part:

- **Cached ages** use the age on the board. A label that covers several lines (known costs, "3 to 4 days old") uses the oldest of them.
- The `fare_list` `empty` sample's "3 days old" is a sample value the boards don't give. It matches the Faro row's age.
- **Wikivoyage "page edited March 2026"** gives a month and no day on the boards, so `page_edited` holds the month only (`2026-03`) and no sample invents a day.
- **Sample coordinates.** The boards have no map coordinates (their map is drawn, and the position is "not real"). The `map` samples use made-up coordinates with the source name **"Sample"**, and the map is **not** part of the sample trip.
- **Fares, holidays, times and journeys** in `fare_list`, `public_holidays`, `time_difference` and `transport_route` are made up for the boards, as `sample-data.md` says. The two holiday rows are named "Sample holiday". The release date `2026-11-01` is the boards' "sample date".
- **Same data twice.** Where a state has no separate board (for example `time_difference` `filled` and `same_time`, or `comparison_table` `not_known`, which is the board's "Filled, with a Not known row"), the files differ only where the state needs it.

## Rounding working for `MoneyEstimate.shown`

Every estimate has an `exact` value and a `shown` value. `shown` is the exact value rounded to the nearest £10, half up. The working is below. The rounding function comes later and is tested against these figures. Money is in pence, so £782 is 78200.

| Estimate | Exact working | Exact | Rounded to the nearest £10, half up | Shown |
|---|---|---|---|---|
| Lisbon known costs | £192 + £350 + £240 = £782 | 78200 | £782 is between £780 and £790, and nearer £780 | 78000 |
| Lisbon gap to the £800 budget | £800 − £782 = £18 (under) | 1800 | £18 is between £10 and £20, and nearer £20 | 2000 |
| Valencia known costs | £168 + £220 = £388 | 38800 | £388 is between £380 and £390, and nearer £390 | 39000 |
| Valletta known costs | £242 + £400 + £260 = £902 | 90200 | £902 is between £900 and £910, and nearer £900 | 90000 |
| Valletta gap to the £800 budget | £902 − £800 = £102 (over) | 10200 | £102 is between £100 and £110, and nearer £100 | 10000 |
| Lisbon known costs, fares failed | £350 + £240 = £590 | 59000 | already a whole ten | 59000 |

The lines are already whole tens, so their `shown` equals their `exact`: stay £70 × 5 = £350 (35000), £80 × 5 = £400 (40000), meals £12 × 2 × 5 × 2 = £240 (24000), £11 × 2 × 5 × 2 = £220 (22000), £13 × 2 × 5 × 2 = £260 (26000). Flights are exact cached fares, so they carry `is_estimate: false` with equal `exact` and `shown`: £96 × 2 = £192 (19200), £84 × 2 = £168 (16800), £121 × 2 = £242 (24200). Every other estimate above, including each known-costs total, is `is_estimate: true`.

The money conversion is not an estimate: £500 × 1.15 = €575 (50000 pence, 57500 cents).
