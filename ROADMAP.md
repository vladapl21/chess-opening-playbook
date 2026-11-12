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

## Phase 2: onboarding

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

- XP for every step, a daily goal ring, a streak (with one freeze a week), and levels.
- A celebration when you pass a checkpoint, a short weekly recap card, and optional sound.
- Leagues and friends later, once other players exist.

## Phase 5: the systems library (ongoing)

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
