# Roadmap: from my playbook to a personal opening trainer

**Where this is going.** Anyone opens the app, is greeted Duolingo-style, signs up, brings in their recent games, and gets an opening repertoire matched to how they actually play. When the games don't settle a choice, they pick between options shown as boards. Then they work through a gamified course built from their own games: drills, practice games, checkpoints, and threat-spotting from their own blunders.

**Today's app** is that course for one player (me), built by hand from 200 of my games. The plan below turns each hand-made step into something the app does for any player, in small releases that are each usable on their own.

## Decisions (November 8, 2026)

| Question | Decision | Why |
|---|---|---|
| Hosting | Static site on GitHub Pages, served from `main` → `/docs` | Free, already set up, and the app is one page |
| Accounts | Supabase: Auth plus Postgres with row-level security | Free tier, works from a static site, and has room for each player's games and repertoire later |
| Sign-in | Email and password | No extra setup. Google can be added later |
| Who uses it this week | Just me, with everything built so others can join later | Real use first, then open it up |
| Repertoires for other players | Ready-made systems from a library, matched to their games; the player chooses on toss-ups | Keeps the hand-checked lines and notes, and makes personalisation a matching problem |
| Bringing in games | chess.com or Lichess username (public APIs), PGN upload as a fallback | No files to export for most people |
| Where analysis runs | In the browser (a Web Worker, Stockfish compiled to WebAssembly), results saved to the account | No server costs, and games never leave the device unprocessed |
| The claude.ai artifact | Stays as a personal build with its own storage | Its sandbox blocks network calls, so it can't reach Supabase. The site is the main app |
| What comes first (November 12) | The systems library. Personal playbooks stay unannounced until players who prefer other openings have real lessons to choose | A playbook that tells half its players "your opening is not written yet" is not a product |
| Visitors without an account | The welcome screen and the Sandbox. Same tabs, the rest locked until games are in | The site is the product now, not a showcase of one player's book |
| Games in | Username first (chess.com and Lichess public APIs, called from the page), PGN file as the fallback. 150 is the target, 50 the minimum | No export step for most players |
| The analysis | A script in the page: rules and counting, no language model, no engine (`app/analyze.js`) | Instant, free, the same answer every time, and it runs under Node for tests |
| The coach | Three faces to choose from in Settings and on the bring-your-games screen (Pip the knight, Rocco the rook, Dot the pawn; `COACHES` and `FACES` in `product.js`), bottom right, speech bubbles. Says something the first time a tab is opened and after a drill; never during a test; can be switched off | Short things read better in a bubble than in a block of text |
| One position, one move (November 12) | The build fails when two move orders reach one position and the book answers differently, or when a label claims a pin, a guard or an attack that is not on the board. Each setup has one order, with a stated reason wherever it changes | A drill that asks for two different moves in one position can't be memorised, and a label that is wrong once makes every label suspect |
| Changed lines (November 12) | Every line carries a version that goes up when its moves change; an older progress record counts as due and is marked Changed | Lines get rewritten, and nobody should be told they have mastered moves the line no longer has |
| Engine in the app (November 10) | Stockfish.js 19, lite single-threaded build, in a web worker; hidden while you are being tested | Runs on a plain static host with no special headers, and the same worker will do the game analysis in Phase 3 |

Facts that shape the design:

- Lichess's [opening explorer API now requires authentication](https://lichess.org/@/thibault/blog/the-opening-explorer-now-requires-authentication/FSWh9Zg3), so the app can't ask it for opponent statistics at run time. Opponent move odds get baked into each system pack at build time, as the books already do with Maia.
- chess.com's public API sometimes answers browsers without CORS headers. If that bites, imports go through a small Supabase Edge Function.
- Supabase's built-in email sender allows only a few emails an hour. That's fine for one player, but a custom SMTP sender is needed before friends join.

## Phase 0: the live site (done)

- The course is merged into `main` (PR #1).
- GitHub Pages: Settings → Pages → Deploy from a branch → `main` / `/docs`. Vlad switches this on; the GitHub proxy can't change repository settings.

## Phase 1: accounts and synced progress

- `supabase/schema.sql`: `profiles` and `progress` tables, row-level security (each person sees only their own rows), grants, and a trigger that creates a profile on sign-up.
- The site build loads `@supabase/supabase-js@2.105.4` from jsDelivr. The project URL and publishable key live in `app/site.json` (both public by design). The artifact build leaves accounts out.
- An account sheet in the header: create an account, sign in, reset a password, sign out, and a status that says when progress was last saved.
- Sync is local-first. Every save goes to the browser at once and to the account a second later. Progress is pulled and merged on sign-in, on load, and whenever the tab comes back into view. Merge rules: the newest record wins for each drill line and puzzle; course steps keep the best score and any completion; sandbox counters keep the higher number. Progress made without an account is adopted by the first account that signs in on that device. A different account signing in on the same device starts from its own saved progress instead.
- Tested in Playwright against a fake Supabase that keeps one in-memory server across two browsers ("two devices").

## Phase 1.5: the engine, plans and the rest of the course (done)

- **Sign-in after signing out.** The account sheet opens on "Sign in" with the last email filled in, with tabs for both forms.
- **A built-in engine.** Stockfish.js runs in the browser: the three best moves in words, the other side's idea (a search with the move handed to them), and the line it expects. It is off during drills, practice games and checkpoints and comes on when they end.
- **The explore board.** "Play on from here" at the end of any line, drill, puzzle, practice game or missed checkpoint position: moves for both sides, or the engine answers.
- **Plans.** One card per lesson for the position its main line ends in: king, pawns, pieces, target, their plan, watch for (`content/plans.py`).
- **The four units that were "coming soon".** The Black Scotch, Vienna and King's Gambit lines rebuilt around the bishop-to-c5 setup, and two skill units from my own games: Finish the job and Endings.

## Phase 1.6: one move per position (done)

- **The complaint.** Two Slav lines reached the same position by different move orders and then asked for different moves, and one of them called a bishop sortie a pin when nothing was pinned.
- **One order for the Slav setup,** used in the Queen's Gambit, London, Colle, Torre, Veresov and Réti lessons, with the reason written at each place where the order has to change (README, "One setup, one order").
- **The same sweep over both books.** 43 lines changed, 18 added, 10 removed. Along the way the engine found a real hole: in the Colle, closing the chain with the e-pawn before the c-pawn let White's queen check and win the b-pawn.
- **`pipeline/lint_claims.py`** checks repeats, pin claims and labels that say a move guards or hits a piece; `assemble.py` runs it and stops on a finding.
- **Line versions** (`data/line_versions.json`), so the changed lines came back into review marked Changed.

## Phase 1.7: fixes from play (done, November 12)

- Engine numbers follow the usual convention for both colours (plus: White is better); a key under the engine card says so.
- Skill units: every wrong move has a reason (`pipeline/explain_skills.py`), longer tricks are listed and can be played out, safe moves that are not the engine's first choice count, "Show me the danger", and the engine per position in practice sets.
- Sandbox: several openings at once.
- Three coaches to choose from: Pip, Rocco and Dot. Bigger face, narrower bubble.
- Settings and the account button moved out of the header into the corner of the screen; the header fits one row on an ordinary monitor and centres its rows when it has to wrap.
- A lesson opened from a course unit has "Next lesson" at the top. The Sandbox has "Free play: pick openings" to leave a course practice game.

## Phase 1.8: the daily habit (done, November 13)

- **Today's five** opens the Drill tab: five lines from move one, from both books, slips first (oldest first), then changed lines, what is due, new lines from studied lessons, then new lines in course order. Any line played to its end counts toward the day; five different lines keep the streak (`Daily` and `dailyNext` in the template; `d.days` in the progress record, merged across devices as a union per day).
- A **!** on the Drill tab until today's five are done. The red counts beside White and Black and on Drill are gone.
- **Badges** in the profile (the flame in the corner, or the account button): sixteen of them in four groups, locked ones grey with a progress bar. A new one arrives as a medal in the coach's bubble, held back while a line, practice game or checkpoint is being played (`BADGES`, `Badges`, `profileHTML` in `app/product.js`; `d.badges` keeps the first date).
- **Reminder emails**, written but not switched on: `supabase/functions/nudge` (Deno) with its rules in `pick.js`, `supabase/nudge.sql` for the log table and the hourly schedule. At most one a week, only in the player's evening, only with reminders on. Needs a Resend key and a sending domain (README, "Reminder emails").
- **Connect your account**: the chess username is part of sign-up and the games are read straight after; bullet is left out; under 200 games that aren't bullet, the page says to play more first and remembers it. No game counts anywhere in the app's words.
- **Learn folded into Your games**: the openings list there opens each opening's page; the tab is gone (`#learn` links still work).
- **Settings follow the account** (`d.set`, the newer copy wins). The system switch is folded away in Settings and asks for the username.
- **The explore board keeps the game from move one**, with a mark and a button for where you came in.
- **The footer** says whose playbook it is, then a copyright line.
- A bug found on the way: a second function called `fenAfter` (for the skill units) had replaced the puzzle one, so a solved missed shot threw an error and showed no final position. Renamed, and three suites now fail on page errors instead of printing them.

## Phase 2: onboarding (first version built, November 12)

Built (see README, "Where it is going"):

- The shell: Sandbox first, the colour switch keeps its tab, Settings (theme, text size, board colour, board letters, coach).
- Three states of the page: house playbook, new player (locked tabs, Sandbox open), personal playbook. Kept as `me` in the progress record and merged across devices.
- Welcome, account first, games by username or PGN file, the reading screen, findings, would-you-rather cards, the "ready" screen.
- The personal playbook: course order and unit text from the profile, chapter numbers, Your games (results by opening, where you leave the book, recent games).
- The coach.

Still to do in this phase:

- **More systems, first** (Phase 5 below). Order suggested by what club players at this level play: for Black against the e-pawn the Sicilian and the Caro-Kann; against the d-pawn the classical defence and a fianchetto setup; for White a d-pawn system. The would-you-rather cards already list them as "being written" (`CATALOG` in `app/product.js`); a system becomes selectable by adding its lessons and setting `ready`.
- The questions from the old plan that are not asked yet: rating and time control are read from the games. The daily goal is fixed at five lines; a choice of three, five or ten could come later.
- **Sign in with chess.com.** chess.com has OAuth 2.0 / OpenID Connect by application (their form); once approved, it plugs into Supabase as a custom OIDC provider and the username comes with the sign-in.
- Sentences about the house player's games are cut at start-up by a pattern (`PERS` in `app/product.js`). Better: mark them in the content so they can be replaced by the player's own.
- "Update from new games" re-reads everything. It should add to what is there.
- The real chess.com and Lichess calls have only been run against a stand-in. Check both in a browser with a real username, and add the Edge Function fallback if chess.com refuses the page.

The original plan for this phase, for reference:

- **Welcome.** An original mascot (a knight), with "Get started" and "I already have an account".
- **A few quick questions.** Which colours you want to work on, your rating and time control, and a daily goal (5, 10, 15 or 20 minutes).
- **Account**, then **bring your games**: a chess.com or Lichess username with a month range, or a PGN file.
- **Analysis screen** with live progress, then **"Here's what we found"**: the first moves you face most, your score against each, and where you leave your preparation.
- **Choices.** For every toss-up, two or three cards, each with a board, a one-line pitch, how it fits your games, and your record in it. Then the course opens.
- **Storage.** The profile holds usernames, rating and daily goal; games are kept compact (moves and metadata); plus the analysis summary and the chosen systems.

## Phase 3: the analysis engine

- **In a worker.** Parse the PGNs, walk each game through the system packs' move trees, and count frequency and score for each opponent first move and each system. Note where you leave the book.
- **Toss-ups.** Two systems that are close in frequency and score, a first move none of your systems answers, or a system you score badly in that has a natural alternative.
- **Blunder mining** with Stockfish WebAssembly on your own moves (the engine worker from Phase 1.5). This produces personal "Spot the threat", "Finish the job" and "Endings" sets in the same format as `data/course_threats.json`.
- **Plans for any position.** The plan cards are hand-written today. For generated repertoires they need a template filled from the position: pawn structure, king placement, open files and the engine's top lines.
- **Course generator.** Units come from the chosen systems, ordered by how often you face them and how badly you score, with skill units mixed in.

## Phase 4: gamification

- Done (Phase 1.8): the daily goal ring, the streak, badges with the coach's medal, scarce reminder emails.
- Still to do: a streak freeze (one a week), XP and levels, a celebration when you pass a checkpoint, a short weekly recap card, and optional sound.
- Leagues and friends later, once other players exist.

## Phase 5: the systems library (ongoing)

**Done so far (November 12):**

- **Packs.** `PACKS` in `content/black/bmeta.py` names the slots and their packs; the build writes `slot` and `pack` on every chapter and `packs` on the book. The page cuts the books to the packs in play (`applyPacks` in the template; the choice lives in `Prog.d.packs` for the house playbook and in the picks of a personal one, with a copy on the device). Settings has a row per slot with more than one pack. The would-you-rather cards offer every ready system. `lint_repeats` runs per combination of packs.
- **The Caro-Kann** for Black (`content/black/bcaro.py`, lessons and notes in one file): 7 lessons, 59 lines, a course unit (`b-caro`), plans for the three core lessons, 12 cheat-sheet rows. Engine-checked at depth 14 with no line losing ground.

**Next, in this order:**

1. ~~The Sicilian for Black~~ Done on November 13 (`content/black/bsicilian.py`: the Kan setup, 5 lessons, 31 lines, unit `b-sicilian`). Original note: (slot `blackE4`, pack `sicilian`). Same recipe as the Caro-Kann: explore with Maia odds, write `content/black/bsicilian.py`, add the chapter to `CHAPTERS`, `CH_META`, `PACKS`, `CHEAT`, a course unit and plans. The catalogue entry in `product.js` becomes ready by itself once the pack exists.
2. **A d-pawn system for White** (slot `white`). The White build (`pipeline/build_white.py`, `content/white/`) has no packs yet: give its chapters `slot`/`pack` the way `build_black.py` does and write `packs` into the book. The White book's root has one first move today; the chapter stats, `e4` and `oddsRoot` fields assume it.
3. **The English for White** (slot `white`, pack `flank`).
4. Coverage gaps in the Caro-Kann that `check_black.py` lists as `W-MISS` (the most common: the Two Knights after the bishop comes out, the pawn trade with the bishop check taken).

- **Split today's two books into packs.** For White: Italian, Two Knights, the Sicilian with c3, the Caro-Kann main line, the French advance, Scandinavian, Pirc, Philidor and Petrov, and the rare first moves. For Black: the e-pawn setup with the bishop on c5, the Slav setup, and the answers to the English and Réti.
- **Add alternatives so toss-ups have real choices.** Against 1.e4, a Caro-Kann setup. Against 1.d4, a King's Indian setup. For White, a London system for d-pawn players.
- **Each pack** gets lines, opponent odds at 1200 to 1800, engine checks, and notes with no notation, built by the existing pipeline.
- **The repeat check has to run across packs.** Two packs chosen together can transpose into each other (a Vienna that becomes an Italian), so the one-move-per-position check runs on the combined repertoire a player ends up with, not on each pack alone.

## Phase 6: open it to friends

- Invite codes, a privacy note, limits on imports, and a custom email sender.
- Installable on phones as an offline-capable web app (PWA), and a custom domain.

## Still to decide

- The app's name and the mascot's look. Mock-ups come in Phase 2.
- Whether to add Google sign-in.
- Friends and leaderboards.
