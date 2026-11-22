# Build step 1: foundation and data contract (design)

Status: approved by the owner, 21 Nov 2026 ("Approve, write the plan (Recommended)"). Milestone "Build 1: Foundation and data contract". Build order: [01 §4](../../product/01-research-and-direction.md#4-build-order), step 1.

## Intent

Step 1 lays the foundation that every later step builds on. At its end, Layover has a running backend and website, but no model calls and no outside data. The website shows the sample Lisbon trip from the boards, so later steps only connect real data to widgets that are already finished (owner, 20 Nov 2026: "Widgets in Build 1 (Recommended)").

Why it matters: Layover is a portfolio project for AI and agent engineering jobs ([0003](../../decisions/0003-purpose-and-traveller.md)). A recruiter judges the code as well as the product, so the foundation follows the house templates and their checks, and the widgets match the approved boards.

## Goals

1. The FastAPI and Next.js template layers are applied, and `make check` runs both.
2. The data contract is fixed: the trip state and all 20 widget kinds, each with its states.
3. All 20 widget components are built, in every state the boards show, from the boards' sample data.
4. The website's pages are built and show the sample Lisbon trip, marked as a sample.
5. A development-only gallery shows every widget in every state.
6. Money types, the commission switch (off), recorded-response tests and the evaluation runner exist and are tested.
7. Aspire starts the backend, the frontend and PostgreSQL together, and shows traces from the website through the backend (the database leg is proved by a test now and checked end to end in step 2).

## Non-goals

- No model calls, no agent framework code (Microsoft Agent Framework, [0013](../../decisions/0013-microsoft-agent-framework.md)), no agents (step 2).
- No outside API calls: no fares, weather, FCDO or any other source (steps 3 to 6).
- The chat doesn't talk to the server (step 2). The message box shows, and says it isn't connected yet.
- No hosting, no public site, no real trip links (step 7).
- No MCP servers yet (step 2). The vector database is still chosen in step 3: the FastAPI layer's database part brings `pgvector` and enables its PostgreSQL extension, but nothing uses it until then.

## Anti-goals (a failure even if it works)

- A sample figure that could pass for a real one. Every page that shows the sample trip says so.
- A widget that shows a missing value as zero, a dash or "N/A" (decision 0011 rule 4; the interface word is "Not known").
- A widget without its source and age label, or a destination described as "safe" (0011 rules 2 and 6).
- The frontend and backend each keeping their own copy of a widget's shape.
- Money held as a binary float.

## Decisions made in this brainstorm (21 Nov 2026)

Each goes into the register in the plan's PR.

| Decision | Owner's answer |
|---|---|
| FastAPI layer options | "Database only (Recommended)": PostgreSQL on; the model gateway (`llm`) off until step 2, after the Anthropic terms and prices are checked; file storage off |
| Where the data contract lives | "Python models, exported (Recommended)": Pydantic models in the backend are the one true copy; `make check` exports them to JSON Schema files in `schemas/` and to TypeScript types, and fails when an export is out of date |
| What step 1 ends with on screen | "Pages + widget gallery (Recommended)" |
| Packages from the template layers | "Approve the template sets (Recommended)": the packages each layer brings at its tagged version are approved as a set; any other package still goes to the owner, apart from those already approved (`holidays`, Lucide, Aspire) |
| GitHub project board | "Add a project board" (the agent recommended keeping the backlog file only) |
| How widgets are built | "go with A": React components styled with Tailwind v4 over Layover's tokens, with the boards as the visual reference |
| Money rounding | "Half up, once at the end (Recommended)": full precision through a calculation, then one rounding to the penny, a half penny going up (£39.835 to £39.84) |
| How estimates are shown | "Nearest £10 (Recommended)", then, after the pre-push review found the samples broke it, "Parts to £1, totals to £10 (Recommended)": a part from listings (per night, per meal) shows to the pound; lines, totals and differences that include an estimate are worked out exactly, rounded once to the nearest £10 and shown with "about" ("about £780"); flights show exact. The samples and boards are corrected in PR 2 |
| Tracing packages | "Approve OpenTelemetry (Recommended)": OpenTelemetry for Python, Apache 2.0, added in the Aspire PR. **Correction, 21 Nov 2026:** the question said the FastAPI layer has no tracing; it does (FastAPI 0.162's built-in OpenTelemetry traces each request). The approval now covers only the PostgreSQL query instrumentation the layer lacks |

## Approaches considered for the widgets

| Approach | Trade-off | Chosen |
|---|---|---|
| A. Rebuild in Tailwind, boards as the reference | Most rebuild work, and small visual drift has to be caught; follows the Next.js layer's rule, so template updates fit, and it is the style frontend reviewers expect | Yes (owner: "go with A") |
| B. Reuse the boards' CSS as it is | Fastest and closest to the approved boards; breaks the template's Tailwind rule, the static-page CSS needs reworking for components and dark mode, and the code ends up with two styling systems | No |
| C. Tailwind for layout, board CSS for the chart, map and table | Less work on the hard widgets; two systems, and a reader must learn which applies where | No |

## The design

### 1. Templates

- `copier update` on the base layer adds the `fastapi` and `nextjs` stacks. Then `house-template-fastapi` v0.11.1 is applied with `database: true`, `llm: none`, `storage: false`, and `house-template-nextjs` v0.3.0 with the FastAPI backend.
- Template-owned files stay template-owned. Layover's own code sits next to them.
- `docs/references/third-party.md` lists every package each layer brings, with its version, licence and official documentation, under the approved sets.
- Issue #27 (CodeQL doesn't scan Python) is closed by the FastAPI layer's CodeQL setup, if the layer covers it; otherwise the plan fixes it in the same PR.

### 2. The data contract

- **Where:** Pydantic models under `backend/src/app/contract/`: one module for the trip state and one per widget `kind`.
- **The 20 kinds:** the 16 in the [design brief](../../design/brief.md) plus `public_holidays`, `time_difference`, `fare_list` and `transport_route` (proposed in #26, drawn and chosen in #37). Step 1 closes #26.
- **Every widget** carries a `kind`, a `state` and, for each outside value, a source label: Live, Cached with its age (or, for offline data, its release date), Fallback or Unavailable (0011 rule 2). The states are loading, filled, empty, error and not known, plus each kind's other states from the brief's widget state table. The two kinds with no outside value, `brief_summary` and `not_known`, need no source label.
- **(Agent's call)** The four new kinds get their rows in the brief's state table in PR 2, written from the approved "Widgets: proposed" board, for the owner to see in that PR.
- **Trip state (agent's call):** the fields the traveller sees on the boards and in the [information architecture](../../design/information-architecture.md): the brief, the three places and their comparison, the chosen place, where you're staying, the days, the booking state, pinned answers from the chat, and the shared copy's settings (its "as of" date and the "Include my budget and who's travelling" choice). The agents' working state (intent, journey step, checkpoints) belongs to step 2's graph, not to this contract.
- **Fare age (agent's call):** `fare_card` and `fare_list` carry each fare's capture date and age; when a fare is too old to show is set in step 4, with its source.
- **Money:** integer minor units with an ISO 4217 currency code; exchange rates as `Decimal` strings. Never a float (enforced by a lint rule on the money and contract modules).
- **Exports:** `make check` writes each model to `schemas/widgets/<kind>.schema.json` and the trip state to `schemas/trip.schema.json`, and fails if a committed file differs. The models are also in the OpenAPI schema, so the template's `make api-types` gives the frontend its TypeScript types.
- **Sample data:** the boards' sample data ([sample-data.md](../../design/boards/sample-data.md)) becomes fixture files under `schemas/samples/` (next to the exported schemas, so both the backend and the frontend read the same files), one per widget state, each checked against its model. The same files feed the frontend. They are labelled as samples, and they never feed a figure that could reach a traveller as real.

### 3. Backend foundation

- **Money types** (`app/money.py`): amounts in minor units, conversion and rounding in tested code, built test-first with the `test-first` skill and hand-worked expected values. Rounding: full precision through a calculation, then once to the penny, half up (owner, 21 Nov 2026). Estimates follow the owner's rule: parts to the pound, lines and totals to the nearest £10, half up, rounded in the backend so the frontend never rounds money. Worked example (an illustrative rate): €47.35 at 0.8412 is £39.830820, shown as £39.83.
- **Commission switch:** a setting, off by default, with a test that it is off (01 §4 step 1 case).
- **Recorded responses:** `tests/recorded/<provider>/` with a loader and a check, run in `make check`, that each recording has a capture date and source and holds no key, token or personal data. There are no providers yet; the check runs on a sample recording.
- **`holidays` library:** added as an approved dependency, with its `third-party.md` entry, and an adapter that gives a country's national holidays for a month, labelled Cached with the library's release date, with a test against the official holiday dates (register, 20 Nov 2026, "In build plan 1 (Recommended)", says "a recorded test"; for an offline library the hand-worked official dates play that part). The boards' sample fixtures keep their "Sample holiday" rows; the agent that uses the adapter comes in step 3.
- **Sample endpoints:** read-only routes `GET /v1/sample/trip` and `GET /v1/sample/widgets` serve the samples, checked against the contract, so every widget model is in the OpenAPI schema and the frontend reads the samples through the real API and the typed client. They are built with the contract (PR 2), and the frontend switches to them in the join (PR 5).
- **Evaluation runner** (`backend/evals/` or as the plan decides): reads the case IDs from [cases.md](../../evaluations/cases.md), runs the cases marked `code` that step 1 can run (the schema part of `WIDGET-01` to `WIDGET-20`), and prints a report. The scripted traveller is a data file of answers per evaluation trip; step 1 sets its format, and step 2 first uses it. The runner is not part of `make check` once it calls models; in step 1 it makes no calls and runs in `make check`.

### 4. Website

- **Pages** ([information architecture](../../design/information-architecture.md)):
  - Welcome and new trip, `/`.
  - Working trip, `/trip/sample-lisbon`, showing the sample trip. **(Agent's call)** The sample's readable link is an exception to the information architecture's rule that links are long random values with no place name; real links follow the rule from step 7.
  - Shared trip, `/s/sample-lisbon`, read only.
  - How Layover works, `/how-it-works`.
  - Link not found.
  - The limit-reached state.
- **Layout:** chat on the left and canvas on the right from 1024 px; Chat and Trip tabs below it, with the trip strip. The canvas has its section index.
- **Sample banner:** every page that shows the sample trip carries a visible "Sample trip" label, so no figure passes for real.
- **Chat:** the message box shows, with the welcome's example prompts. Sending says the chat isn't connected yet.
- **Limit reached:** built as a component and shown in the gallery; it joins `/` and `/trip/{trip_id}` with the limits in step 7.
- **Gallery:** `/dev/widgets` shows every widget in every state. It answers "not found" unless the `ENABLE_WIDGET_GALLERY` setting is on, which it is only in development and in the end-to-end tests (the tests run against the production build, so the page is switched off by a setting, not left out of the build).
- **Styling:** Tailwind v4 over Layover's [tokens.css](../../design/tokens.css), which replaces the template's neutral tokens. The fonts already committed with the boards are reused (Source Serif 4, Source Sans 3), and Lucide for icons.
- **Tests:** Vitest and Testing Library for each widget's states. The template's Playwright tests run on every page and on the gallery, in light, dark and phone width: axe (WCAG 2.2 AA), no CSP violations, one `h1`, and screenshots. A side-by-side check of each widget against its board, at 390, 768, 1024 and 1440 px, is run by the `visual-reviewer` before merge.
- **"Safe" check:** the boards' `SAFE` pattern (`tools/check_boards.py`) is reused by a new check over the frontend's copy.

### 5. Aspire

A TypeScript Aspire app host starts the FastAPI backend, the Next.js frontend and PostgreSQL, and shows traces from the website through the backend in its dashboard ([register](../../decisions/README.md#register), 19 Nov 2026). The backend sends traces with FastAPI's built-in OpenTelemetry (`fastapi.telemetry`, used by the FastAPI layer's `backend/src/app/main.py`), plus PostgreSQL query instrumentation (approved 21 Nov 2026; OpenTelemetry's psycopg one, because the SQLAlchemy one does not support SQLAlchemy 2.1); the frontend uses the Next.js layer's `@vercel/otel`. No route queries the database in step 1, so a backend test proves queries create spans, and the full website-to-database trace is checked in step 2, the first step with a database route (register, 22 Nov 2026). Traces stay on the local machine. `make check` and CI never need Aspire. The plan checks the official documentation for the version in use and adds its pinned version to `third-party.md`.

### 6. Project board

A GitHub Projects board for the Build milestones, with columns To do, In progress, In review and Done. It exists: [Layover build](https://github.com/orgs/olaheavy-dev/projects/5), created by the agent on 21 Nov 2026 at the owner's word ("you can cerate the board"), with every open Build issue on it. Every issue in a Build milestone is on it. `docs/planning/backlog.md` stays the ordered list, and the board shows progress. The agent that opens, closes or moves an issue updates both.

### 7. How the work ships

One plan, about five PRs, each with its own issue in the Build 1 milestone:

1. Templates applied, with the third-party entries.
2. The data contract, the exports, and the sample fixtures.
3. Backend foundation: money, the commission switch, recorded responses, `holidays`, sample endpoints, the evaluation runner.
4. Website: tokens, fonts, the 20 widgets, the pages, the gallery.
5. Join: the frontend reads the sample endpoints, then Aspire is added.

PRs 3 and 4 are built in parallel, after PR 2 merges, by separate agents in separate worktrees (01 §4). Issues #36 (board checks with a real HTML parser) and #40 (Floorplan snapshot exemption upstream) are small PRs of their own within step 1. #9 (the `task` label) is the owner's.

The step ends with its gate: a whole-repository review, a Floorplan map of the real code, and the evaluation report from the step 1 runner.

## Left to the builder

- Module and file names inside `backend/` and `frontend/`, apart from those named above.
- How the export check is wired into `make check`.
- The exact route names of the sample endpoints, and the gallery's layout.
- Splitting the widgets across agents within PR 4.
