# Notes for working on this repo

The plan for the next phases is in [ROADMAP.md](ROADMAP.md). Read it first.

## Build and test

- `make build` (or the four scripts in `pipeline/`) rebuilds both books, the course and the page. It needs the engine paths from the README: `STOCKFISH`, `MAIA_WEIGHTS`, `LCZERO_TRAINING`. The engine caches in `data/cache/` make rebuilds fast and reproducible. Check that a rebuild reproduces the committed files.
- `pipeline/assemble.py` writes two pages from `app/template.html`:
  - `data/build/playbook.html` for the claude.ai artifact (no accounts, uses the artifact's own database);
  - `docs/index.html` for GitHub Pages (accounts through Supabase when `app/site.json` has a URL and key).
- Tests drive the real page in Chromium (Playwright, pre-installed): `tests/e2e_white.py`, `e2e_black.py`, `e2e_sandbox_switch.py`, `e2e_course.py`, `e2e_accounts.py`. Screenshots go to `tests/out/` (ignored).
- README images: `FONTS_DIR=<google/fonts ofl folder> python3 tests/readme_shots.py`.

## Deploy

- Work on a branch, push it, open a PR with `gh api` (GraphQL is blocked here), and merge it with `gh api -X PUT repos/vladapl21/chess-opening-playbook/pulls/<n>/merge`. GitHub Pages serves `main` → `/docs`.
- The claude.ai artifact is https://claude.ai/artifact/5RHAUYcSDGBWjJa2QWPaxi. Publish `data/build/playbook.html` to that URL, keeping its capabilities (db, user).
- The proxy blocks Supabase hosts from this environment. Account features are tested against `tests/fake_supabase.js`; the real project is checked in the browser.

## House rules for the app

- No chess notation in anything the user reads. The squares f7 and f2 are the only exception. Arrow and move data inside the code is fine.
- Every colour is a CSS token defined for both light and dark themes. Check phone width (390px) for sideways scrolling.
- Progress records are shared between the books, so line, puzzle and lesson ids must never collide (`assemble.py` asserts this).
- Record counts quoted in the course text come from all 200 games; the books' own stats come from the original 149.
