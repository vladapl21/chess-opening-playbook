# Notes for working on this repo

The plan for the next phases is in [ROADMAP.md](ROADMAP.md). Read it first.

## Build and test

- `make build` (or the four scripts in `pipeline/`) rebuilds both books, the course and the page. It needs the engine paths from the README: `STOCKFISH`, `MAIA_WEIGHTS`, `LCZERO_TRAINING`. The engine caches in `data/cache/` make rebuilds fast and reproducible. Check that a rebuild reproduces the committed files.
- `pipeline/assemble.py` writes two pages from `app/template.html`:
  - `data/build/playbook.html` for the claude.ai artifact (no accounts, uses the artifact's own database);
  - `docs/index.html` for GitHub Pages (accounts through Supabase when `app/site.json` has a URL and key).
- Tests drive the real page in Chromium (Playwright, pre-installed): `tests/e2e_white.py`, `e2e_black.py`, `e2e_sandbox_switch.py`, `e2e_course.py`, `e2e_accounts.py`, `e2e_engine.py`, `e2e_versions.py`. `tests/e2e_shell.py` and `tests/e2e_onboarding.py` cover the shell and a new visitor, `tests/e2e_skills.py` the skill units and the engine's numbers, `tests/e2e_packs.py` the systems (over local HTTP: headless Chromium sometimes drops a `file://` page's storage across a scripted reload). Run the suites one at a time and with no engine job beside them: they are timing-sensitive on two CPUs. Screenshots go to `tests/out/` (ignored). Console errors that mention `ERR_TUNNEL_CONNECTION_FAILED` are the proxy blocking Google Fonts and the supabase-js CDN, not the app.
- The engine is a web worker, so it can't start from a `file://` page. `tests/serve.py` serves the build over local HTTP with `engine/` beside it; `e2e_engine.py` and the engine screenshot use it.
- `make check` runs the engine and wording checks on the Black book. `W-RARE` and `W-MISS` lines are information, not failures; `B-LOSS`, `ILLEGAL` and `ENDS-ON-WHITE` need a look. `B-LOSS bv-ponziani-d5` is a known depth-14 artifact (the book's move is also the engine's best; the two searches disagree on the number). `B-LOSS bsi-open-c3` is a choice: the book declines a pawn offer the engine would take, and stays level.
- `pipeline/lint_claims.py` checks both books for the same position answered with two different moves, for pin wording with no pin on the board, and for labels that say a move guards or hits a piece when it doesn't. `assemble.py` runs it and stops on any finding, so fix the content, never the check.
- `data/line_versions.json` holds `{line id: [version, hash of its moves]}` and is committed. `assemble.py` bumps a version when a line's moves change; the page then treats older progress on that line as due ("Changed"). A rebuild that changes no moves must leave the file untouched. Ids of removed lines stay in it, so a reused id starts on a new version.
- The site build opens on the welcome screen for a visitor without games. The older suites test the hand-built playbook, so `launch()` in `tests/e2e_white.py` marks every context as the house player; `launch(p, house=False)` starts as a new visitor (`e2e_onboarding.py`, the last part of `e2e_accounts.py`). A test that seeds its own progress must not be skipped by that mark (see the seed in `e2e_versions.py`).
- `docs/img/welcome.png`, `findings.png` and `choices.png` are copies of `tests/out/o_start.png`, `o_findings.png` and `o_choice_system.png` from `e2e_onboarding.py`.
- README images: `FONTS_DIR=<google/fonts ofl folder> python3 tests/readme_shots.py` (needs `barlow`, `barlowcondensed` and `jetbrainsmono` from a sparse checkout of google/fonts).

## Deploy

- Work on a branch, push it, open a PR with `gh api` (GraphQL is blocked here), and merge it with `gh api -X PUT repos/vladapl21/chess-opening-playbook/pulls/<n>/merge`. GitHub Pages serves `main` → `/docs`.
- The claude.ai artifact is https://claude.ai/artifact/5RHAUYcSDGBWjJa2QWPaxi. `data/build/playbook.html` has no document skeleton: wrap it (doctype, charset and viewport metas, the small reset the live page starts with) and publish the result as `index.html` of that artifact. Its two engine files (`engine/…`) and its capabilities (db, user) are kept when only `index.html` is sent.
- The proxy blocks Supabase hosts from this environment. Account features are tested against `tests/fake_supabase.js`; the real project is checked in the browser.

## Where things live

- `app/template.html` is the whole app. The engine code sits in one block before the boot code: `Engine` (the worker and UCI), `Ana` (one analysis per position, kept for the session), `moveWords` (engine moves in plain words), `EngineUI` (card, arrows, eval bar) and the explore view (`exploreFrom`, `renderExplore`).
- `app/analyze.js` is the game analysis (PGN in, profile out). No DOM, so `node tests/analyze_check.js` runs it on `data/games`.
- `app/product.js` and `app/product.css` are the product shell: who is looking (`PERSONA`: house, new, ready), the welcome and locked screens, games in, the reading screen, findings, the would-you-rather cards (`CATALOG`, `STYLE`), the personal playbook (`applyProfile`) and the coach. `assemble.py` inlines all three files. `product.js` wraps `render`, `renderGames` and `Prog.record`, so it has to stay after them and before the boot code.
- New class names in `product.css` must not exist in the template's styles: `.opt`, `.locked`, `.ring`, `.field`, `.dots`, `.big` and `.who` were all taken. Check with grep before adding one.
- Systems: `PACKS` in `content/black/bmeta.py` (slot → packs → chapters). A new system is a content module like `content/black/bcaro.py`, a chapter in `CHAPTERS`/`CH_META`, an entry in `PACKS`, cheat rows, a course unit and plans. The page keeps only the packs in play (`applyPacks`, `PICKS`, `syncPacks`); `D.full` is the whole library and is what the game analysis reads. `tests/e2e_packs.py` covers the switch.
- `content/plans.py` holds the plan shown where each lesson's main line ends. `assemble.py` attaches the plans and checks them for notation.
- `docs/engine/` is Stockfish.js 19 (GPL-3.0), unchanged release files. Keep its README and license next to it. `app/vendor/chess.js` (BSD-2) is inlined by `assemble.py`.
- Skill units (`threats`, `finish`, `endings`) share one item format in `data/course_*.json`; their wording is the `SKILL` table in the template. `pipeline/explain_skills.py` (needs Stockfish, not part of `make build`) fills `refute[move] = [reply, label, material won at once, the moves after it, material lost, engine number]` for every wrong move and `fine` (accepted moves that lose nothing) for the threat positions. `recut` and `regrade` redo the cutting and the grading without a full engine pass.

## House rules for the app

- The house playbook (the artifact build, and accounts with progress from before personal playbooks) must look and behave as before. Anything written for other players goes through `PERSONA`.
- The coach never speaks while a drill, practice game or checkpoint is being played, and never hints at a move.
- One position, one move, inside every combination of packs a player can hold. If two move orders reach the same position, the book plays the same move in both. Before changing a line, look for the position in the other lessons (`lint_claims.py` reports the conflicting paths).
- One order per setup. The d-pawn setup comes out in the order given in the README ("One setup, one order"). Where a line has to leave that order, the note at that move says why.
- A label says only what is on the board. "Pin" needs a piece that can't or shouldn't move because of what is behind it; a bishop coming at a knight with a pawn behind it is "Bishop comes at your knight". "Guards" and "hits" are checked the same way.
- No chess notation in anything the user reads. The squares f7 and f2 are the only exception. Arrow and move data inside the code is fine. This covers what the engine says too: its moves go through `moveWords`.
- The engine never shows during a drill, a practice game or a checkpoint. It comes on when they end, and it is always available in lessons and game reviews. In a skill unit's practice sets it opens per position once that position is answered.
- Engine numbers are from White's side for both colours (plus: White is better). Only the words are turned to the player's side.
- Every colour is a CSS token defined for both light and dark themes. Check phone width (390px) for sideways scrolling.
- Progress records are shared between the books, so line, puzzle and lesson ids must never collide (`assemble.py` asserts this).
- Record counts quoted in the course text come from all 200 games; the books' own stats come from the original 149.
