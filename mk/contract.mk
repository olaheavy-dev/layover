# Project checks for the data contract (not a template layer). The base Makefile includes mk/*.mk.
# The JSON Schemas in schemas/ come from the Pydantic models in backend/src/app/contract/.

CHECKS += check-contract

.PHONY: export-schemas check-contract

export-schemas: ## Write the JSON Schemas in schemas/ from the contract models
	uv --directory backend run --locked --extra db python -m app.contract.export

check-contract: ## The JSON Schemas in schemas/ match the contract models
	uv --directory backend run --locked --extra db python -m app.contract.export --check
