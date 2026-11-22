# Project checks for the design files (not a template layer). The base Makefile includes mk/*.mk.
# PYTHONDONTWRITEBYTECODE keeps Python cache files out of the working tree (.gitignore is template-owned).

CHECKS += check-design
FAST_CHECKS += check-design

.PHONY: check-design

check-design: ## Design tokens (and the frontend's copy) meet WCAG 2.2 AA in both themes; boards use only tokens, never say "safe", load nothing from outside; media is registered; the frontend never says "safe" and its font and token copies match the originals; no Python cache files tracked; evaluation case IDs are unique, well formed and defined where cited; Floorplan snapshots hold no local paths or git remotes
	PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools -p 'test_*.py'
	PYTHONDONTWRITEBYTECODE=1 python3 tools/check_contrast.py
	PYTHONDONTWRITEBYTECODE=1 python3 tools/check_boards.py
	PYTHONDONTWRITEBYTECODE=1 python3 tools/check_copy.py
	PYTHONDONTWRITEBYTECODE=1 python3 tools/check_eval_ids.py
	PYTHONDONTWRITEBYTECODE=1 python3 tools/check_floorplan.py
	@! git ls-files | grep -E '(^|/)__pycache__/|\.py[co]$$' || { echo 'Python cache files are tracked (they hold local paths): git rm -r --cached them'; exit 1; }
