# Build tasks: Layover boards

Issue: [#28](https://github.com/olaheavy-dev/layover/issues/28). Made from the [design brief](../brief.md), the [information architecture](../information-architecture.md), the [tokens](../tokens.css) and the [sample data](sample-data.md) on 20 Nov 2026, with the `brief-to-tasks` skill.

Style: warm editorial (brief, "Aesthetic direction"). Photos and type carry the warmth; figures sit in calm cards with their source and age. The first build task sets this look, so the owner can check it before the other boards are built.

## How the boards work

- **Screens and board pages.** Each screen state is one HTML file in `screens/` that fills the browser window, like the real app would. A board page in this folder shows that screen twice, in frames 390 px and 1440 px wide, with a light and dark switch. A board page can show several states of the same screen, one above the other.
- **Shared files.** `boards.css` holds the components (top bar, buttons, chips, source label, chat, cards, section index), built only from `var(--…)` tokens. `board.css` and `board.js` hold the board page itself (frames, theme switch). Every page links `../tokens.css`, so a token change reaches every board.
- **Rules from `make check`** (`tools/check_boards.py`): no literal colours, never the word "safe", no local paths, nothing loaded from outside the repository, the label "Sample data, not real" on every page, and every image, font and illustration registered in `docs/assets/README.md` first.
- **Figures** come only from [sample-data.md](sample-data.md). A figure that is not there is added there first, with its working.

Already in place, reused as they are: `tokens.css` (both themes), `sample-data.md`, `tools/check_boards.py` and `tools/check_contrast.py`. Everything else is new: no components exist yet (brief, "Existing patterns").

## Foundation

- [x] **Asset register and files**: create `docs/assets/README.md` first; then commit the Source Serif 4 and Source Sans 3 WOFF2 files with their OFL text, the Lucide icons used (copied in as SVG) with the ISC and MIT notices, and three Unsplash photos (Lisbon, Valencia, Valletta), each under 1 MB, after reading the Unsplash licence again. Done when `make check` passes with every file registered with its source, terms and date checked. _New._
- [x] **Board shell and the chosen place, Lisbon (first look)**: the board page (two frames, theme switch, sample label), `boards.css` with the top bar, section index, chat column, message input, source label, buttons and widget card, and one complete screen: the working trip on the chosen place, with the comparison folded and the key facts (`fare_card`, `cost_estimate`, `advice_card`, `climate_chart`, `money`) on the first screen. Done when the owner has seen it in both themes at both widths. _New. Sets the look for everything after it._ **Owner checkpoint.**
- [x] **Logo marks**: two or three marks drawn as SVG, each shown in the real top bar at both widths and in both themes on one board. The owner picks one in a prompt window; the chosen mark is registered and used everywhere after. _Depends on: board shell._ **Owner choice.**
- [x] **Illustration test**: the welcome screen drawn three times: an isometric illustration drawn for Layover, an editorial travel-poster line drawing drawn for Layover, and a recoloured free-library illustration. With it, one or two proposed libraries whose licence allows changes and commercial use without credit, each with its licence text and the date checked. The owner picks the style and the library in a prompt window. Then a one-page style guide (shapes, line, light, colours from the tokens). _Depends on: board shell._ **Owner choice.** _Done 20 Nov 2026: owner chose isometric; the guide is `illustration-guide.html`._

## Widget gallery

Every `kind` with every state in the [state table](../brief.md#widget-states) that is not "not applicable", plus the extra states, at canvas width and phone width, in both themes.

- [x] **Place widgets**: `fare_card`, `cost_estimate`, `advice_card`, `climate_chart` (with its table alternative), `money`, `sea_conditions`, `daylight`, `place_intro` (with Fallback) and `map` (the drawn sample map). Covers: filled, loading, error (Unavailable), not known, and each kind's extra states. _Reuses: the widget card and source label._
- [x] **Journey widgets**: `brief_summary`, `comparison_table` (including the phone cards in a horizontal scroll), `hotel_list`, `itinerary_day`, `booking_approval`, `web_results` and `not_known`, plus the phone compact card in the chat. Covers: every state in the table, including empty, the folded rows and every booking state.
- [x] **Proposals for the kinds without a `kind`** ([#26](https://github.com/olaheavy-dev/layover/issues/26)): local holidays, the time difference, fares "to anywhere" and TfL journeys, each drawn as a widget with its source label. The figures they need are added to `sample-data.md` first. Plan 1 fixes the schemas.

## Screens

Each screen follows the checklist in [#28](https://github.com/olaheavy-dev/layover/issues/28) and is drawn at 390 px and 1440 px, in both themes.

- [x] **Welcome screen** (`/`), with the isometric illustration, the four example prompts and the honesty line: `screens/welcome.html` and the board page `welcome.html`.
- [ ] **Welcome mood scenes**: the prompts are in `mood-scene-prompts.md`. The owner makes the images in ChatGPT; each is registered in `docs/assets/README.md` before it is committed, and the footer line goes on the page with the first one. _Waits for the owner's images._ Tracked in #35.
- [x] **Vague and unclear messages** (owner, 20 Nov 2026): the brief agent asking for missing details with quick-answer chips; the one clarifying question; "Which Valencia?" with the matches as choices; a side answer before any place is chosen (no "Add to trip"). Shown first as clickable samples.
- [x] **Starting a trip**: the empty canvas after the first message; the brief waiting for confirmation, editing a chip and confirmed.
- [x] **Comparing**: three loading cards; one failed card with "Try again"; a "Not known" row (Valencia's stay); a swapped place; no place fits.
- [x] **The chosen place, finished**: the remaining place widgets below the first screen; a side answer inline in the chat with "Add to trip", and the same answer pinned under "Added from the chat". _Reuses: the first-look screen._
- [x] **Stay and Days**: hotel chosen; hotel skipped (days from the centre); Days with a "Not known" opening time and an empty afternoon; the itinerary-only trip (the place, then Stay and Days, with no Compare section).
- [x] **Booking**: waiting for approval, approved, declined and price changed, always with "Sandbox: no real booking or payment".
- [x] **Chat-only replies and interruptions**: `web_results` in the chat; "I can't help with that yet"; the `not_travel` decline; lost connection with "Try again"; the "New trip" confirmation; the "Share trip" step.
- [x] **Phone and navigation**: Chat and Trip tabs, the Trip tab badge, compact widget cards, the sideways section index; folded sections and the section index on desktop. Part drawn: the long chat (grouped checks, "Jump to latest"), the trip strip, the compact cards and the "3 new" badge are on `trip-lisbon-chat.html`. Drawn on `phone-nav.html` (the badge, the sideways index, two folded states on desktop).
- [x] **Pages outside the trip**: the shared trip (`/s/{share_id}`) with "as of" dates; How Layover works with "no evaluation results yet"; link not found; limit reached, with wording that needs no figure. Drawn on `pages.html`.

## Review and handover

- [x] **Board index**: `index.html` in this folder links every board, with the state each one shows, so the reviewers can check coverage against #28 and the state table. `tools/check_boards.py` fails when a board page is not linked from it.
- [x] **Accessibility pass**: contrast from the tokens (text on the `--tint-surface-*` tokens is now enforced by `tools/check_contrast.py`: lowest 4.58:1, quiet text on the traveller bubble in light; the glows, lines and the transparent index bar are skipped and listed, and the decorative `--illus-*` tokens are left out), visible focus on every control, targets of at least 24 by 24 px, reduced motion, text alternatives for charts and illustrations (brief, "Accessibility requirements").
- [x] **Design review**: the `design-reviewer` against the 12 "bar for Layover" rules and the state table; the `visual-reviewer` at 390, 768, 1024 and 1440 px.
- [ ] **Handover**: tick #28's checklist, update `docs/planning/status.md` and `docs/planning/backlog.md`, run `make check`, then the pre-push review and the pull request.
