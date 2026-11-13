// Runs the game analysis under Node on the PGN files in data/games and checks the result against known facts.
//   node tests/analyze_check.js            (prints a summary and exits 1 on a failed check)
const fs = require('fs'), path = require('path'), vm = require('vm');
const root = path.join(__dirname, '..');
const ctx = {console, setTimeout, Date, exports: {}, module: {exports: {}}};
vm.createContext(ctx);
vm.runInContext(fs.readFileSync(path.join(root, 'app/vendor/chess.js'), 'utf8') + '\n;globalThis.Chess = typeof Chess !== "undefined" ? Chess : exports.Chess;', ctx);
vm.runInContext(fs.readFileSync(path.join(root, 'app/analyze.js'), 'utf8') + '\n;globalThis.Analyze = Analyze;', ctx);
const books = {w: JSON.parse(fs.readFileSync(path.join(root, 'data/build/data_white.json'))), b: JSON.parse(fs.readFileSync(path.join(root, 'data/build/data_black.json')))};
const A = ctx.Analyze, assert = (c, m) => { if (!c){ console.error('FAILED:', m); process.exitCode = 1; } };
(async () => {
  for (const [file, user] of [['vladapl_1.pgn vladapl_2.pgn', 'vladapl'], ['aqua_alpaca.pgn', 'aqua_alpaca']]){
    const text = file.split(' ').map(f => fs.readFileSync(path.join(root, 'data/games', f), 'utf8')).join('\n\n');
    const raw = A.parsePGN(text); assert(A.guessUser(raw) === user, 'guessUser ' + A.guessUser(raw));
    const t0 = Date.now(), P = await A.run(text, '', books), ms = Date.now() - t0;
    const sys = s => Object.entries(s.systems).sort((a, b) => b[1].n - a[1].n).map(([k, t]) => `${k} ${t.n} (${t.w}-${t.l}${t.d ? '-' + t.d : ''}, ${t.depth} plies)`).join(', ');
    console.log(`\n== ${user}: ${P.n} of ${raw.length} games in ${ms} ms | ${P.tc} ${P.rating} (peak ${P.peak}), opponents ${P.oppAvg} | ${P.all.w}-${P.all.l}-${P.all.d}`);
    console.log('White', JSON.stringify(P.white.first), '| in the book:', sys(P.white), '| outside', P.white.off);
    console.log('Black vs', JSON.stringify(Object.fromEntries(Object.entries(P.black.vs).map(([k, t]) => [k, t.n]))), '| in the book:', sys(P.black), '| outside', P.black.off);
    for (const [k, s] of Object.entries(P.slots)) console.log('  slot', k, Object.entries(s.opts).map(([o, t]) => `${o} ${t.n}`).join(', '));
    console.log('  buckets', Object.entries(P.buckets).map(([b, o]) => b + ': ' + Object.entries(o).map(([k, t]) => `${k} ${t.n}/${A.pct(t.w + t.d / 2, t.n)}%`).join(', ')).join(' | '));
    for (const f of P.facts) console.log('  fact:', f.text);
    console.log('  leaks:', P.leaks.slice(0, 5).map(l => `${l.side}:${l.ch} node ${l.node} ${l.uci} x${l.n}`).join(' | '), '| warned moves played:', P.warned.length);
    assert(P.n === raw.length, 'every game should be usable');
    assert(P.white.all.n + P.black.all.n === P.n, 'colours add up');
    assert(Object.keys(P.white.first).every(k => k === 'e4') || user !== 'vladapl', 'vladapl opens with the e-pawn');
    assert(P.white.off === 0, 'every White game starts with the playbook move: ' + P.white.off);
    const faced = Object.values(P.black.systems).reduce((a, t) => a + t.n, 0);
    assert(faced >= P.black.all.n * 0.9, 'nearly every Black game is sorted into a chapter by what White set up: ' + faced);
    if (user === 'vladapl') assert(P.leaks[0].ch === 'slav' && P.leaks[0].n >= 15, 'the old habit against the d-pawn is the biggest leak');
    assert(JSON.stringify(P).length < 60000, 'profile stays small: ' + JSON.stringify(P).length);
    assert(P.games.every(g => g.ch === null || books[g.me].chapters.some(c => c.id === g.ch)), 'chapters exist');
  }
  // a player the library does not cover: Sicilian as Black, d-pawn as White
  const fake = ['1. d4 d5 2. Bf4 Nf6 3. e3 e6 4. Nf3 c5 5. c3 Nc6 1-0', '1. e4 c5 2. Nf3 d6 3. d4 cxd4 4. Nxd4 Nf6 5. Nc3 a6 0-1'].flatMap((m, i) => Array.from({length: 30}, (_, k) =>
    `[White "${i ? 'opp' + k : 'newbie'}"]\n[Black "${i ? 'newbie' : 'opp' + k}"]\n[Result "${m.split(' ').pop()}"]\n[WhiteElo "1100"]\n[BlackElo "1090"]\n[TimeControl "600"]\n[Date "2026.10.${String(k % 28 + 1).padStart(2, '0')}"]\n\n${m}\n`)).join('\n');
  const Q = await A.run(fake, '', books);
  console.log('\n== newbie:', Q.n, 'games | slots', JSON.stringify(Object.fromEntries(Object.entries(Q.slots).map(([k, s]) => [k, Object.keys(s.opts)]))), '| outside the book', Q.white.off, Q.black.off);
  assert(Q.user === 'newbie' && Q.n === 60 && Q.tc === 'rapid', 'newbie basics');
  assert(Q.slots.white.opts.d4.n === 30 && Q.slots.whiteD4.opts.london.n === 30 && Q.slots.blackE4.opts.sicilian.n === 30, 'named what they play');
  // the d-pawn games with White are outside the library; the Sicilian games with Black are in it since the Sicilian pack
  assert(Q.white.off === 30 && Q.black.off === 0, 'White outside the library, Black inside: ' + Q.white.off + ' ' + Q.black.off);
  console.log(process.exitCode ? '\nanalysis checks FAILED' : '\nanalysis checks passed');
})();
