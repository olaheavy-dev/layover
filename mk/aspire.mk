# Project targets for the Aspire app host (not a template layer). The base Makefile includes mk/*.mk.
# Never part of `make check`: CI does not need Aspire, Docker for PostgreSQL, or a dashboard. That is
# also why the app host's type check (`npm run typecheck` in apphost/) is not in `make check`: it
# needs .aspire/modules, which `aspire run` or `aspire restore` generates.

CHECKS += check-apphost-image

.PHONY: dev-all check-apphost-image

dev-all: ## Run PostgreSQL, the backend and the website together under Aspire, with traces (needs the Aspire CLI and Docker)
	cd apphost && npm ci --ignore-scripts && aspire run

check-apphost-image: ## The app host's PostgreSQL image is the one in backend/compose/db/compose.yaml
	PYTHONDONTWRITEBYTECODE=1 python3 tools/check_apphost_image.py
