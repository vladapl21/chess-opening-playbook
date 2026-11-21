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

## Phase 1.22: lines that don't stop when the pieces are out (done, November 20)

Notes from play: in the Four Knights and the Vienna the lines ended once the knights and bishops were out, and what comes after is exactly what isn't obvious. The same was true across both books: half the Vienna lines were five moves long.

- **Every line played on** (`pipeline/deepen.py`, a step of both builds). The other side makes the reply club players pick most; your side plays the move the book already has for that position, else a natural move Stockfish accepts. A line runs to at least move nine and on through anything forced, to move thirteen at most, and never comes back to a position it has had. 1,550 of the 1,721 lines in the library grew. The median line went from 12 plies to 20, and the lines that ended by move six went from 871 to 51 (stems and lines that show a mistake). A stem (the lesson on the first three moves) stays as written.
- **Replies without a line** (`pipeline/fill.py`). 166 new side lines: every reply picked one time in ten that comes up in three games in a thousand, with a finer net for the Italian and for the Four Knights and Vienna, and 28 named gambits and attacks that are rare by the odds (the Fritz, the Ulvestad, the Kloss and the Colman in the Two Knights, the Portuguese, the Philidor Gambit, the Dubov Italian, the Blackmar-Diemer's side lines, the Halasz, the Fyfe, the Williams and others). The Two Knights was then worked through by hand, turn by turn: 35 more lines, one for every reply with real odds in the Fried Liver, the knight to the rim, the Traxler, the Fritz and the Ulvestad.
- **Plans follow the lines.** A main line that was played on gets a plan from its new last position, and the hand-written plan shows in the lesson at the move it was written for. A divider in the list of moves, *How it usually goes on*, marks where the added moves begin. A quiet position gets the engine's next moves for both sides, so no line ends without a plan.
- **The cost.** Every changed line shows as Changed and is due again, and the page is 8 MB (1.2 MB over the wire) where it was 4.5. It opens in 0.4 s on a laptop.
- **Hand fixes and circles.** A check that takes nothing gives way to a capture that is as good, and a line never comes back to a position it has had: two lines had been checking back and forth to the last move. A move fixed by hand (`content/deepen_fixes.py`) holds for the position, and the build works the line out again by itself. `make check` now reads the lines as built and measures a flagged move against the engine's own move at the same depth; one finding is left, and it is a choice.
- **Next: a choice of variation inside an opening.** Which Sicilian, which line against the Caro-Kann, the center attack or the slow Italian. Each variation is a pack of its own, drafted like the Scandinavian (`pipeline/draft.py`: a setup's order, the moves fixed by hand, lessons, notes, a course unit), and the choice needs a second step: the family first (Sicilian), then the variation, on the would-you-rather card and in Settings. First batch proposed: the Dragon beside the Kan for Black, the Open Sicilian beside the small c-pawn for White, the slow Italian beside the center attack, the Advance beside the bishop chase against the Caro-Kann.

## Phase 1.21: a lesson board you can move on, and no more waiting on games (done, November 20)

- **Move any piece in a lesson.** The line's own move steps on. A move the book answers opens that line. Anything else opens the explore board with the move made and the engine on.
- **The order of your moves, on the board.** Each piece carries the number of the move that put it there, on from the start and kept with the settings; a purple number is played at another turn than in the main line. The strip of small diagrams from Phase 1.19 is gone: it was more to decode than the board.
- **The lag.** Reading a month of games replayed every game through the chess library's own move reader on the page's main thread: on a slow phone, 23 seconds for the last three games and two minutes for the first monthly recap, with the page frozen. A reader written for the job is nine times quicker, only the newest three games are replayed for the reviews, and the recap yields every four games. The same month now takes a quarter of a second and about nine seconds in the background.
- **Said once.** The engine's verdict and depth are under the board, so the card beside it lists the moves only. The explore board's way back is a centred button. The coach's bubble closes with a bigger cross on a phone.
- **The welcome page** shows a lesson's board with its opening's name in place of the tilted board, the speech bubble and the four locked cards.

## Phase 1.20: one book, a daily shop, marks on the board (done, November 20)

Notes from play, the same day: the shop said everything twice, the marks were only in lessons, and switching between White and Black by hand was a chore in the Sandbox.

- **No White/Black switch.** The header is the brand, the tabs and the player's corner. The Sandbox plays both books: with Everything picked, games come with White and with Black in turn, a tap on a colour keeps that one, and openings from both books can be picked together. Drill lists both books an opening at a time, Your games shows White's and then Black's in every part, and whatever is opened loads its own book with the board turned to it. A drill or a practice game under way keeps its colour across tabs.
- **An opening's lines are its lessons' lines.** The Sandbox used to take an opening's lines from what its first moves reach, which left out the odd move orders filed under it: 45 of the 71 lines under Philidor & Petrov could come up, and 16 of the 39 under rare first moves. Found while counting the lines of both books together.
- **The daily shop.** The whole shop is one shelf of six pieces that changes at midnight (two hats, two colours, glasses, something for the neck, picked by the date from everything not owned), with the locker beside it. The header is the switch and a timer. Gone: the heading, the day names, the card for tomorrow, the sub-lines and the items that were always for sale.
- **Marks with the usual signs, on the board.** !, ?!, ? and ?? in blue, amber, orange and red (the family other sites use, not their values). In a line drill and a Sandbox game they come up as the moves are played, with the word beside the badge for a moment, and the key move keeps its ! on the piece through the reply. Phase 1.19 held them back until the game was over; in play that only hid the part that helps.
- **Variation names.** The name of the position is the panel's heading in a drill and sits above the move card in a lesson: the variation large, the names that lead to it as a trail above, a flash when a move starts a named line, and that move tagged with the name in every list of moves.
- **Plainer words.** Headlines made of two fragments joined by a comma are gone from the app and the content (unit ideas, opening pages, lesson and game titles, badges), and so are lines that repeat a heading, a timer or a number beside them. It is a house rule now.

## Phase 1.19: key moves, move order, the coach on a game that left the book (done, November 20)

Notes from play: the openings weren't sticking as fast as hoped, least of all a setup whose moves come in another order from line to line.

- **Marks on the moves.** In every lesson the other side's inaccuracies, mistakes and blunders carry a mark, and so does your key move: the answer that makes one cost. Judged from the stored engine numbers as a share of the point, a move into a forced mate, and what the notes already call a mistake. Their own shapes and colours. Nothing is marked while a line is being played; the Sandbox marks its list when the game is over. The old "Key move" chip, which sat on half the moves, is gone.
- **Your moves, in order.** A strip under a lesson's board: each of your moves as a small picture, the main line above a line that plays them in another order with the move that changed places ringed in both, and a switch that puts each move's number on its piece. A drill names a move of the line played before its turn as that (right move, wrong moment), and the coach's note says the order slipped, not the move.
- **A game that left the book.** When your own move left it, the coach says which move and what your book plays, with the drill on the bubble; the Drill page leads with that line and the coach brings it up once a day until it has been drilled clean, which is now kept with the game.
- **The Sandbox.** The fold-out of the other side's moves has an arrow and keeps its state; the start position moved under the board; the count of lines met is every line a game can end on with the openings picked, counted from the book on the page (274 for the house White book until the odd lines made it 343; 524 for Black), and from a set position it counts the lines through it.
- **Moves land at once.** Your own move in every drill, game and checkpoint and on the explore board, and every move on the set-up board. Only the reply slides.
- **Counts that keep up.** `pipeline/lint_counts.py` works out every number the README quotes from the built books and the build fails on a stale one. It found the At a glance table two releases behind (278 lines for 343, 79 lessons for 82, a count of positions from the first release).
- **The wardrobe, refitted.** Hats sit on their rim with a shadow and the picture makes room for them; scarves, leis, chains and ties are drawn along each coach's neck, and on the knight they are cut to its outline so they read as worn. Shop cards show the piece by itself.

## Phase 1.18: three more systems and the odd lines (done, November 19)

- **The Scandinavian** for Black (slot `blackE4`, pack `scandi`; `content/black/bscandi.py`): 10 lessons, 120 lines, unit `b-scandi` with a deep dive.
- **The King's Indian** for Black (slot `blackD4`, pack `kid`; `content/black/bkid.py`): two chapters (`kid` against the c-pawn, `kidx` against the London, the Torre, the Colle, the Jobava and the Trompowsky), 12 lessons, 136 lines, units `b-kid` and `b-kidx`. The d-pawn slot now has a real choice, so its would-you-rather card shows.
- **The English** for White (slot `white`, pack `flank`; `content/white/english.py`): three chapters (`english` against the e-pawn, `engsym` against the c-pawn, the knight and the fianchetto, `engrare` against the d-pawn and rare moves), 15 lessons, 191 lines, units `w-english`, `w-engsym` and `w-engrare`.
- **Odd lines** in the house books (`content/black/bodd.py`, `content/white/odd.py`): 111 lines for the named oddities, from the Bongcloud and the Halloween Gambit to the Borg and the Lemming, each in the chapter where it belongs.
- **`pipeline/draft.py`** drafts a pack: the other side's moves by the Maia odds, yours from the setup's order wherever Stockfish accepts it. It writes the lessons, the titles (real names first) and the named lines; the notes for the moves that matter are still written by hand. The script for each pack is in `pipeline/drafts/` and reproduces its module exactly. All three packs and the odd lines pass the depth-14 checks with nothing to look at.
- A choice card offers up to four systems. Every new line has a plan at its end (five were written by hand).
- **Open:** the chapter for White's other first moves is shared by every Black pack, so a King's Indian player answers the English and the flank openings with the e-pawn and the d-pawn like everyone else. A fianchetto answer there needs that chapter split into packs.

## Phase 1.17: a set-up board with arrows, no stale counts (done, November 19)

- **The Sandbox's set-up board.** Arrows under the board and on the keyboard step back and forward through the moves made, a tap on a move in the list jumps to it, the heading says how many lines go on from the position, the other side's moves show how often they are played, and the opening's name follows along. The rest of the Sandbox's settings are out of the way while a position is set up.
- **Your games** opens straight on its parts: the header with a count of games is gone, and no text quotes a total any more.
- **Wording.** The last "your study" and "this guide" notes in the Italian now say "your book" or say nothing; the Italian page's two panels about changes to the study are gone; a Sandbox report no longer repeats its slip count, and a plan read off the board says "soon" where "then" had nothing before it.

## Phase 1.16: a plan at the end of every line, real names, a tour that keeps up (done, November 19)

- **A plan at the end of every line.** The main lines kept their written plans; the other 811 lines got one (767 read off the board, 42 shared with a main line, two written). A side line that ends where a main line ends shares its plan; the rest are read off the last position and Stockfish's line from there: pieces still at home, castling now or once a piece is out, the pawn or piece move the engine plays next and what it hits, the material and what it means for trades, a king that can't castle, a pawn with no neighbour, the other side's next two moves in words. Six Black lessons got written plans. The card shows at the end of a line in study, after a clean drill and in every Sandbox report.
- **Real names.** Opening names come from lichess's list (CC0): every board in study, drills, the Sandbox and the explore board shows the position's name, and the reviews name a move that starts a named line. Move descriptions with a real name behind them gave way to it: *Nimzowitsch Defense* for "Knight first", *Englund Gambit* for "The e-pawn gambit", *Evans Gambit* for "The b-pawn gambit", *Saragossa Opening* for "Small c-pawn move", 136 move labels, 62 lesson titles, 55 line titles, 38 parts and all 22 opening tiles in all. The "Not in your study" chips and sentences are gone from lessons.
- **The tour keeps up.** Its steps now cover the plan and the opening names, and its test fails when a tab, a part of Your games, a setting or a listed feature isn't named in it.

## Phase 1.15: the last three games, practice from a position, plainer words (done, November 19)

- **Last 3 games** (Your games). The three newest games, reviewed: where each left the book and whose move it was, the book's move or the engine's answer, and the first move that cost a pawn and a half or more. Drill it plays that spot on the drill board; Drill your line and Practise from here when the player left the book. Read from the account on the website every quarter of an hour, or pasted in any copy; the coach says when a new review is waiting, and the Drill page points to what is left to drill. Kept in the progress record and merged per game.
- **The Sandbox from a position.** A set-up board takes the book's moves for both sides; practice games then start there and only its lines come up. Practise from here in a lesson and in a review does the same.
- **Wording.** The footer line about the coach's study is gone; the repertoire is "your book" everywhere (no "study", "guide" or "prep"); lesson chips that only meant something to the house player are gone or kept to it; the Drill page no longer says the same thing three times; a few kickers and coach lines say something concrete instead.

## Phase 1.14: a tour, and every move explained (done, November 19)

A friend played it for the first time and missed half of it: playing on with the engine, the other side's answers in a lesson, even the switch between White and Black.

- **The tour.** The first time the app opens, the coach the player picks shows them around in about two minutes: the White | Black switch (tapped, and back), the tabs, a unit, Play along (one move on the arrow), today's five, a slip punished and the arrow after two misses (played by the coach), Play on with the engine (tapped) and the explore board, a lesson's list of the other side's answers, the move card, the engine switch, Your games, the Sandbox, the level, the streak, the shop, Settings, the account and the coach. It can't be skipped; Fast forward plays it through by itself, Show me does one tap, Back goes back. Nothing in it is recorded. It is stamped in the progress record, so it runs once per player, and Settings has Take the tour again.
- **Every move explained** (`app/ideas.js`). Each move, the player's and the other side's, is read from the board with a few rules: what it wins, threatens or stops, a fork, a check that wins something, a pin, a guard taken away, an uncovered attack. A wrong move is answered with the reply that punishes it and what that costs; a second miss adds why the book's move is the move, and the coach's note at the end of the line says both. It shows in drills, Play along, the Sandbox, the lesson's move card ("On the board", leaving out what the note already says), a practice set's refutations and the explore board's last move. About 85% of the books' moves get at least one line.
- **The README** has a guide to where everything is, the tour, the explainer, and the tests as a table.

## Phase 1.13: learning by playing (done, November 17)

The app is for a player who would rather play than read; the learning should happen in the playing.

- **Play along** replaces "Learn the lines" in every course unit. A lesson is played on the drill board with the move to make as a green arrow and the coach's word beside the board in two bullets at most; a wrong move just doesn't go and isn't counted. Played to its end, the lesson counts as studied and the next step is the same line once from memory. The unit page has one button that always leads on: that line from memory, then the next lesson to play along, then the practice games and the checkpoint. Skipping to the end of a lesson's page no longer counts as studying it; stepping through it (or letting it play) still does.
- **A slip in a unit drill keeps the line in front.** Again leads, ahead of the way back to the unit; a clean run leads to the unit's next thing. A unit drill or play-along stays under the Course tab, with a way back to the unit above the board.
- **The header** is a grid: brand and the player's things on one row, the tabs on their own row, so nothing sits on a tab at any width; on a phone the White/Black switch gets the middle row. The level is a ring that fills toward the next level around a number in ink. The streak in the coach's bubble is a pill: flame, number, "days in a row".
- **Fewer words at a time.** The coach, the unit steps, the course and opening pages, the lesson notes, the welcome screen and the shop's lock speak in short bullets instead of paragraphs.

## Phase 1.12: the monthly recap, daily drops, a coach that says something (done, November 17)

- **Monthly recap**, a fourth part of Your games (`Recap` in `app/product.js`). The month's games are read straight from the playbook's own account (the house playbook's chess.com account, `HOUSE_ACCT`; a personal playbook's account from `me.src`), bullet and daily left out, run through the same analysis, and kept as a small summary per month in `d.recap.m` (the newest copy of each month wins a merge; `d.recap.seen`, the last finished month opened, is the latest; `d.recap.chk`, the last good check, the latest). The part shows the month beside the one before: games, score, rating and how far it moved, moves in the book, the rating day by day, what changed in plain sentences, each opening's games and time in the book beside the lines drilled from it that month, highlights, the place the player left the book most, and the months side by side. A check runs when the app opens and when Your games opens, at most every six hours, and **Check now** runs one at once; the month before is read again after it ends so its recap is final, and the coach says when a finished month is new. The claude.ai copy can't reach chess.com, so it points to the website. The analysis rows gained `tc`, `ot` (lost or won on time) and `by: 'end'` (the book ran out, nobody left it).
- **No accounts or dates in the house playbook's text.** Lesson notes say "Against X:" instead of a date and an account, the game data no longer carries dates or account names, and the skill units' boards say only who the game was against.
- **Shop.** The first-full-week token and the spent row are gone. Twenty drops come out on set weekdays, two a day picked by the date (`Shop.on`), with the time left and a card for tomorrow; bought ones go in the locker and leave the rotation. A switch between the shop and the locker (`S.shopTab`); five new colours, eight hats, two faces and four neck items, all of them drops. On phones the drops sit two to a row and the mannequin is smaller.
- **The coach.** A note in the drill panel when a line ends (`Coach.lineNote`): the move that caught the player, what they played, what the book says about that move when it knows it (the warned moves), why the line's move is the move, how often that move has caught them (`sl` on the line's record counts slips per move), a link to study it; on a clean run only something worth saying (the move that caught them held, a lesson's lines all clean, full strength). A checkpoint with misses names the lesson most of them came from (`Coach.quizNote`). Once a day per tab, what is worth knowing there (`Coach.news`); a tap on the coach brings that back. Badges keep their medal bubble, now with a sentence on what they were for. Fixed: the level wrapper dropped the slips; "Black's" and opening names were lower-cased mid-sentence; developing moves now say which knight or bishop; a first move played within half a second of a line starting could make the line count twice (the drill now ends a line once and plays each opponent move once).

## Phase 1.11: levels, and a calmer Your games (done, November 15)

- **Levels.** Everything practised earns points: 10 for a line without a slip (4 with one), 5 for a lesson studied, 5 for a practice game, 15 for a day with today's five, 40 for a checkpoint. Each level asks for a little more (45 points to level 2, then 60, 75…). The level sits in the corner with a small bar; points float up from it and a new level drops a card, held back while a line is being played (`XP` and `Level` in the template, `Lv` in `app/product.js`). Points are worked out from the record, never stored; `d.lvl` keeps the highest level celebrated (the higher wins across devices), and a line whose moves change keeps the points it earned (`ps`, `pc` on the line's record).
- **The shop opens at level 5** instead of after a week in a row, and every level from 5 on is a token.
- **Your games opens on one grid.** A switch above it (your openings, missed shots, game reviews) shows one part at a time. Each opening is a tile in the old cheat-sheet look: their move highlighted, the answer as a green arrow, the games and the record, and how many of its lines are known. Game reviews are a list that opens at the key moment. A player's own Your games has the same switch: every opening in their playbook for both colours (including the ones not met yet), where they leave the book, and the recent games with where they score. Its table no longer pushes the page sideways on a phone.
- **No cheat sheet tab.** Each opening's page has a switch between its lessons and the opening at a glance, the same cards as before (`glanceHTML`). Old `#cheat` links open an opening's page at a glance.
- **Not done: more theory.** The book builders need python-chess, Stockfish and the Maia net, and this round's environment couldn't install them. The next lines to write are the ones under Phase 5, "Next", starting with the Caro-Kann gaps that `check_black.py` lists.

## Phase 1.9: sync, the shop, course games (done, November 14)

- **Everything follows the account.** Settings keep a time per setting; worn items per slot; every save reads and merges first; unknown fields are carried along. The claude.ai copy used to replace one device's progress with the other's newer copy and never heard the other device while open: it now merges and listens (`Prog.take`). `tests/e2e_artifact_sync.py` and the accounts test check two devices for both.
- **Shop** (`SHOP`, `Shop`, `renderShop`, `gearSVG` in `app/product.js`): tokens from badges and every third day in a row, a wardrobe that opens after a week in a row, colours and gear for all three coaches.
- **Course practice games**: the unit, its clean games and the way back sit at the top of the game's panel; free play is a wide button under the board; no opening picker during a course game.

## Phase 1.10: after the course (done, November 14)

- **The big moment.** The last unit's checkpoint opens a congratulations screen: the coach in a graduation cap, a gold medal, five numbers from the course, the badge and its token, and the coach's suggestion for what next (`renderGrad` in `app/product.js`). It shows once; `d.course.grad` keeps the moment (earliest wins across devices), and a course finished before this existed gets its screen the next time the Course tab opens.
- **The library.** After that the Course tab shows the coach's pick and two more deep dives, each with one sentence on why. The others are folded away, and the first course's path and its units stay one click away (`renderLibrary`, `deepRank`). The ranking is how often the player meets the opening (a chapter's games shared between the units that teach it), weighed by slips in drills and practice games, the checkpoint, and the results in those games.
- **Deep dives.** `DEEP` in `content/course.py` groups each unit's optional lessons into parts with hand-written titles and words. The build adds the boards: where the part's lessons split (blue arrows) and one per lesson at its own first new move (green for the answer, red for a move to leave alone). It also adds six checkpoint positions per part. Parts work like units, numbered Part 1, 2…, and open in order once the course is finished. Two badges: one deep dive, three deep dives.
- Still to do: hand-written idea boards for the biggest deep dives (the Italian, against the Italian), a deep dive for the Slav (it has no optional lessons yet), and a short "since you finished" recap on the library.

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
- Done (Phase 1.9 and 1.10): the shop and the coach's wardrobe; the course-complete celebration and the library.
- Done (Phase 1.11): points and levels, the shop at level 5.
- Done (Phase 1.12): the monthly recap, daily drops in the shop.
- Done (Phase 1.13): Play along, a lesson played with the arrows and the coach before it is played from memory.
- Done (Phase 1.14): the first-time tour, led by the coach the player picks.
- Still to do: a streak freeze (one a week), a smaller celebration when you pass a checkpoint, and optional sound.
- Leagues and friends later, once other players exist.

## Phase 5: the systems library (ongoing)

**Done so far (November 12 to 19):**

- **Packs.** `PACKS` in `content/black/bmeta.py` names the slots and their packs; the build writes `slot` and `pack` on every chapter and `packs` on the book. The page cuts the books to the packs in play (`applyPacks` in the template; the choice lives in `Prog.d.packs` for the house playbook and in the picks of a personal one, with a copy on the device). Settings has a row per slot with more than one pack. The would-you-rather cards offer every ready system. `lint_repeats` runs per combination of packs.
- **The Caro-Kann** for Black (`content/black/bcaro.py`, lessons and notes in one file): 7 lessons, 59 lines, a course unit (`b-caro`), plans for the three core lessons, 12 cheat-sheet rows. Engine-checked at depth 14 with no line losing ground.
- **The London** for White (item 2 below): the first pack in the White book, which now has a slot of its own (`white`).

**Next, in this order:**

1. ~~The Sicilian for Black~~ Done on November 13 (`content/black/bsicilian.py`: the Kan setup, 5 lessons, 31 lines, unit `b-sicilian`). Original note: (slot `blackE4`, pack `sicilian`). Same recipe as the Caro-Kann: explore with Maia odds, write `content/black/bsicilian.py`, add the chapter to `CHAPTERS`, `CH_META`, `PACKS`, `CHEAT`, a course unit and plans. The catalogue entry in `product.js` becomes ready by itself once the pack exists.
2. ~~A d-pawn system for White~~ Done on November 19: the London (`content/white/london.py`, lessons and notes in one file): 3 chapters (`london` against the d-pawn, `lindian` against the king's knight, `lrare` for the rest), 18 lessons, 102 lines, units `w-london`, `w-lindian` and `w-lrare`, deep dives for the first two, a plan for every lesson, 19 cheat-sheet rows. One setup, one order (README); Black's moves from the Maia odds, every White move checked at depth 14 with no line losing ground (`pipeline/check_white.py`, now part of `make check`). `PACKS` for White sits in `content/white/content2_meta.py`; the e-pawn book is untouched (same lines, same node numbers; only the root gained a second child). The page sets the book's first move to the system in play (`applyPacks`), so the Sandbox opens with the d-pawn; `oddsRoot` stays on the e-pawn node, where the odds are the house player's own games. Original note: (slot `white`). The White build has no packs yet: give its chapters `slot`/`pack` the way `build_black.py` does and write `packs` into the book. The White book's root has one first move today; the chapter stats, `e4` and `oddsRoot` fields assume it.
3. ~~The English for White~~ Done on November 19 (Phase 1.18).
4. Coverage gaps in the Caro-Kann that `check_black.py` lists as `W-MISS` (the most common: the Two Knights after the bishop comes out, the pawn trade with the bishop check taken), and in the London that `check_white.py` lists as `B-MISS`. The London's are almost all move orders into positions the book already has, by a path it doesn't (the tree is kept by moves, not positions): the most common is the king's knight before the queen's knight and then the e-pawn or the bishop, about one game in 150 each.
5. ~~A second answer to the d-pawn for Black~~ Done on November 19: the King's Indian, and the Scandinavian as a fourth answer to the e-pawn (Phase 1.18). **Next: the French** (slot `blackE4`, pack `french`) **and the Queen's Gambit Declined** (slot `blackD4`, pack `qgd`), both already on the cards as "being written"; then the shared chapter for White's other first moves, split into packs so a King's Indian player can fianchetto there too.

**The tools these need** (none are in the repository, and each new chat starts on a clean machine): `pip install chess`; Stockfish built from source (`git clone https://github.com/official-stockfish/Stockfish`, `make -j build ARCH=x86-64-avx2` in `src`, with the two network files fetched from the Stockfish repository's releases or raw files); the Maia weights (`git clone https://github.com/CSSLab/maia-chess`, the `maia_weights` folder); and `git clone https://github.com/LeelaChessZero/lczero-training`. Point `STOCKFISH`, `MAIA_WEIGHTS` and `LCZERO_TRAINING` at them. With network access on, a chat can set all of this up in about ten minutes. The exact commands that worked on November 17 are in the README ("Changing the books"): the tag `sf_17.1`, so new evaluations match the cached ones; `make net` is blocked by the proxy, but `raw.githubusercontent.com/official-stockfish/networks` serves both network files; a sparse clone of maia-chess fetches only the weights.

- **Split today's two books into packs.** For White: Italian, Two Knights, the Sicilian with c3, the Caro-Kann main line, the French advance, Scandinavian, Pirc, Philidor and Petrov, and the rare first moves. For Black: the e-pawn setup with the bishop on c5, the Slav setup, and the answers to the English and Réti.
- **Add alternatives so toss-ups have real choices.** Against 1.e4, a Caro-Kann setup (done). Against 1.d4, a King's Indian setup. For White, a London system for d-pawn players (done).
- **Each pack** gets lines, opponent odds at 1200 to 1800, engine checks, and notes with no notation, built by the existing pipeline.
- **The repeat check has to run across packs.** Two packs chosen together can transpose into each other (a Vienna that becomes an Italian), so the one-move-per-position check runs on the combined repertoire a player ends up with, not on each pack alone.

## Phase 6: open it to friends

- Invite codes, a privacy note, limits on imports, and a custom email sender.
- Installable on phones as an offline-capable web app (PWA), and a custom domain.

## Still to decide

- The app's name and the mascot's look. Mock-ups come in Phase 2.
- Whether to add Google sign-in.
- Friends and leaderboards.
