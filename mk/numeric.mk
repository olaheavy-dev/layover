# Project check for numeric code (not a template layer). The base Makefile includes mk/*.mk.
# Enforces the test-first skill: worked examples in numeric tests, and no floats in money code.
# PYTHONDONTWRITEBYTECODE keeps Python cache files out of the working tree.

CHECKS += check-numeric
FAST_CHECKS += check-numeric

.PHONY: check-numeric

check-numeric: ## Numeric tests state their Working and Source; money code and money contract fields use no float
	PYTHONDONTWRITEBYTECODE=1 python3 tools/check_numeric_tests.py
