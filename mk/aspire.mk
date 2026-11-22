# Project targets for the Aspire app host (not a template layer). The base Makefile includes mk/*.mk.
# Never part of `make check`: CI does not need Aspire, Docker for PostgreSQL, or a dashboard.

.PHONY: dev-all

dev-all: ## Run PostgreSQL, the backend and the website together under Aspire, with traces (needs the Aspire CLI and Docker)
	cd apphost && npm ci && aspire run
