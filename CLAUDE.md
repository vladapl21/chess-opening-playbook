# Notes for working on this repo

The plan for the next phases is in [ROADMAP.md](ROADMAP.md). Read it first.

## Build and test

- `make build` (or the four scripts in `pipeline/`) rebuilds both books, the course and the page. It needs the engine paths from the README: `STOCKFISH`, `MAIA_WEIGHTS`, `LCZERO_TRAINING`. The engine caches in `data/cache/` make rebuilds fast and reproducible. Check that a rebuild reproduces the committed files.
- `pipeline/assemble.py` writes two pages from `app/template.html`:
  - `data/build/playbook.html` for the claude.ai artifact (no accounts, uses the artifact's own database);
  - `docs/index.html` for GitHub Pages (accounts through Supabase when `app/site.json` has a URL and key).
- Tests drive the real page in Chromium (Playwright, pre-installed): `tests/e2e_white.py`, `e2e_black.py`, `e2e_sandbox_switch.py`, `e2e_course.py`, `e2e_accounts.py`, `e2e_engine.py`. Screenshots go to `tests/out/` (ignored). Console errors that mention `ERR_TUNNEL_CONNECTION_FAILED` are the proxy blocking Google Fonts and the supabase-js CDN, not the app.
- The engine is a web worker, so it can't start from a `file://` page. `tests/serve.py` serves the build over local HTTP with `engine/` beside it; `e2e_engine.py` and the engine screenshot use it.
- `make check` runs the engine and wording checks on the Black book. `W-RARE` and `W-MISS` lines are information, not failures; `B-LOSS`, `ILLEGAL` and `ENDS-ON-WHITE` need a look.
- README images: `FONTS_DIR=<google/fonts ofl folder> python3 tests/readme_shots.py`.

## Deploy

- Work on a branch, push it, open a PR with `gh api` (GraphQL is blocked here), and merge it with `gh api -X PUT repos/vladapl21/chess-opening-playbook/pulls/<n>/merge`. GitHub Pages serves `main` → `/docs`.
- The claude.ai artifact is https://claude.ai/artifact/5RHAUYcSDGBWjJa2QWPaxi. Publish `data/build/playbook.html` to that URL, keeping its capabilities (db, user), with the two engine files from `docs/engine` as supporting files at `engine/…`.
- The proxy blocks Supabase hosts from this environment. Account features are tested against `tests/fake_supabase.js`; the real project is checked in the browser.

## Where things live

- `app/template.html` is the whole app. The engine code sits in one block before the boot code: `Engine` (the worker and UCI), `Ana` (one analysis per position, kept for the session), `moveWords` (engine moves in plain words), `EngineUI` (card, arrows, eval bar) and the explore view (`exploreFrom`, `renderExplore`).
- `content/plans.py` holds the plan shown where each lesson's main line ends. `assemble.py` attaches the plans and checks them for notation.
- `docs/engine/` is Stockfish.js 19 (GPL-3.0), unchanged release files. Keep its README and license next to it. `app/vendor/chess.js` (BSD-2) is inlined by `assemble.py`.
- Skill units (`threats`, `finish`, `endings`) share one item format in `data/course_*.json`; their wording is the `SKILL` table in the template.

## House rules for the app

- No chess notation in anything the user reads. The squares f7 and f2 are the only exception. Arrow and move data inside the code is fine. This covers what the engine says too: its moves go through `moveWords`.
- The engine never shows during a drill, a practice game or a checkpoint. It comes on when they end, and it is always available in lessons and game reviews.
- Every colour is a CSS token defined for both light and dark themes. Check phone width (390px) for sideways scrolling.
- Progress records are shared between the books, so line, puzzle and lesson ids must never collide (`assemble.py` asserts this).
- Record counts quoted in the course text come from all 200 games; the books' own stats come from the original 149.
