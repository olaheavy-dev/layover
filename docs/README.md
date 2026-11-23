# Documentation index

## Folder structure

```
docs/
├── README.md            this index
├── product/             the main product documents (numbered, read in order)
├── decisions/           one record per decision, plus the register
├── assets/              the asset register (every image, font and media file, with its source and terms)
├── design/              the design brief, information architecture, design tokens and boards
├── evaluations/         the evaluation cases, their coverage table and the build-gate reports (`reports/`)
├── floorplan/           the Floorplan map snapshot from each stage gate
├── planning/            the status file, the ordered backlog and working plans
├── references/          data sources and official third-party documentation
├── reviews/             dated reviews and research
└── superpowers/         specs and plans written with the Superpowers skills
```

Planned folder, added when its stage starts: `docs/architecture/` for system diagrams. Specs and plans live in `docs/superpowers/`.

## What each document is for

| Document | Owns | Status |
|---|---|---|
| [01 Research and direction](product/01-research-and-direction.md) | What Layover is, what it shows, build order, open design questions | Draft; build order (§4) approved 20 Nov 2026 (#39) |
| [Design brief](design/brief.md) | Tone, style, benchmark, component inventory, widget states and source labels, images, sample content, accessibility | Approved; amended 20 Nov 2026 (#31) |
| [Sample data for the boards](design/boards/sample-data.md) | The only source of figures on the design boards, all marked "Sample data, not real" | For the boards |
| [Information architecture](design/information-architecture.md) | Screens, links, navigation, flows for each intent, interface wording | Approved |
| [Design tokens](design/tokens.css) | Colours (light and dark), fonts, spacing, shapes, motion; checked for contrast by `make check` | Approved |
| [Journey design](superpowers/specs/2026-11-19-layover-journey-design.md) | The traveller's journey, intents, agent team, widgets and first evaluation cases | Approved |
| [Design boards](design/boards/index.html) | Every screen and widget state, drawn | Approved (#37) |
| [Evaluation cases](evaluations/cases.md) | Every evaluation case ID and the coverage table | Current (#39) |
| [Floorplan snapshot, Design gate](floorplan/design.html) | A blueprint map of the planned code, drawn from the approved design | Snapshot, 20 Nov 2026 |
| [Evaluation report, build step 1](evaluations/reports/build-1.md) | The first baseline: quality (schema checks only), speed and tokens | Baseline, 23 Nov 2026 |
| [Floorplan snapshot, build step 1](floorplan/build-1.html) | A map of the real code at the end of build step 1 | Snapshot, 23 Nov 2026 |
| [Decision register](decisions/README.md) | Every decision's status and record | Current |
| [Ordered backlog](planning/backlog.md) | Every open issue in order, by stage milestone, and the stage gate | Current |
| [Status](planning/status.md) | Open pull requests, next steps, blockers and the owner's to-dos; overwritten every session | Current |
| [Data sources](references/data-sources.md) | Each outside source's access, terms, limits and when it was checked | Current |
| [Third-party documentation](references/third-party.md) | Official documentation links, and pinned versions once dependencies exist | Current |
| [TripMate review, 19 Nov 2026](reviews/2026-11-19-tripmate-reference-review.md) | Lessons from a public tutorial travel planner | Record |

Accepted decision records override anything in the documents that contradicts them. For process, `AGENTS.md` is the rulebook.

**Reading order for someone new:** 01, then the journey design, then the decision register.

## Naming conventions

- Lowercase words separated by hyphens; no spaces.
- Numbered prefixes where order matters: `01-` for product documents, `0001-` upwards for decisions.
- Dates as `YYYY-MM-DD` at the start of dated files, for example reviews.
