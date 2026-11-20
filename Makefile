PY ?= python3

.PHONY: build test check shots

# Rebuild both books and the page (needs only python-chess while data/cache covers every position and every line end)
build:
	$(PY) pipeline/build_white.py
	$(PY) pipeline/build_black.py
	$(PY) pipeline/build_course.py
	$(PY) pipeline/plan_lines.py
	$(PY) pipeline/assemble.py

# Browser tests against docs/index.html (needs Playwright + Chromium; the engine test serves the page over local HTTP)
test: build
	$(PY) tests/e2e_white.py
	$(PY) tests/e2e_black.py
	$(PY) tests/e2e_sandbox_switch.py
	$(PY) tests/e2e_course.py
	$(PY) tests/e2e_accounts.py
	$(PY) tests/e2e_engine.py
	$(PY) tests/e2e_versions.py
	$(PY) tests/e2e_shell.py
	$(PY) tests/e2e_onboarding.py
	$(PY) tests/e2e_skills.py
	$(PY) tests/e2e_packs.py
	$(PY) tests/e2e_daily.py
	$(PY) tests/e2e_shop.py
	$(PY) tests/e2e_recap.py
	$(PY) tests/e2e_artifact_sync.py
	$(PY) tests/e2e_library.py
	$(PY) tests/e2e_tour.py
	$(PY) tests/e2e_review.py
	$(PY) tests/e2e_marks.py
	node tests/analyze_check.js
	node tests/nudge_check.mjs
	node tests/ideas_check.js

# Engine and wording checks: the Black book, and the White book's packs after the first (the London and the English),
# and the counts the README quotes against the built books (lint_counts.py --write puts them right)
check:
	$(PY) pipeline/check_black.py 14
	$(PY) pipeline/check_white.py 14
	$(PY) pipeline/lint_notes.py
	$(PY) pipeline/lint_claims.py
	$(PY) pipeline/lint_counts.py

# Regenerate the README images in docs/img
shots: build
	$(PY) tests/readme_shots.py
