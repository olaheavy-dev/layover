# Project checks for the design files (not a template layer). The base Makefile includes mk/*.mk.
# PYTHONDONTWRITEBYTECODE keeps Python cache files out of the working tree (.gitignore is template-owned).

CHECKS += check-design
FAST_CHECKS += check-design

.PHONY: check-design

check-design: ## Design tokens meet WCAG 2.2 AA in both themes; boards use only tokens, never say "safe", load nothing from outside; media is registered
	PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools -p 'test_*.py'
	PYTHONDONTWRITEBYTECODE=1 python3 tools/check_contrast.py docs/design/tokens.css
	PYTHONDONTWRITEBYTECODE=1 python3 tools/check_boards.py
