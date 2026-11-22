# Layover

[![CI](https://github.com/olaheavy-dev/layover/actions/workflows/ci.yml/badge.svg)](https://github.com/olaheavy-dev/layover/actions/workflows/ci.yml)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/olaheavy-dev/layover/badge)](https://scorecard.dev/viewer/?uri=github.com/olaheavy-dev/layover)

An AI travel planner for UK-based holidaymakers, built as a portfolio project with real travel APIs.

Status: design stage. See [`docs/planning/status.md`](docs/planning/status.md).

- **What it is and where it's going:** [`docs/README.md`](docs/README.md)
- **How it's built and decided:** [`docs/decisions/`](docs/decisions/)
- **How agents and people work here:** [`AGENTS.md`](AGENTS.md)

## Run it locally

```bash
make install   # toolchains, dependencies and git hooks
make check     # everything CI runs
make help      # every target
```

To run the whole app on your computer with traces, install Docker and the [Aspire CLI](https://aspire.dev/get-started/install-cli/), then run:

```bash
make dev-all   # PostgreSQL, the backend and the website, under Aspire
```

Aspire prints the address of its dashboard, and the website has its own address in the dashboard's resource list. Open the website's `/trip/sample-lisbon` page, then open **Traces** in the dashboard. You see one trace that starts in the website and goes on into the backend. The database queries are traced too, but no page asks the database for anything yet, so you will see them from the next build step. The dashboard's environment view shows the generated database password. It is for the local database only and changes on each run. Press Ctrl+C to stop everything. `make check` and CI never need Aspire.

## Security

See [`SECURITY.md`](SECURITY.md) to report a vulnerability.
