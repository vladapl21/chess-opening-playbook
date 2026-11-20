// Runs the move explainer (app/ideas.js) under Node: known positions first, then every move of both books.
//   node tests/ideas_check.js            checks, a summary and a sample of lines; exits 1 on a failed check
//   node tests/ideas_check.js --all      every line it writes, for reading through
const fs = require('fs'), path = require('path'), vm = require('vm');
const root = path.join(__dirname, '..');
const ctx = {console, exports: {}, module: {exports: {}}};
vm.createContext(ctx);
vm.runInContext(fs.readFileSync(path.join(root, 'app/vendor/chess.js'), 'utf8') + '\n;globalThis.Chess = typeof Chess !== "undefined" ? Chess : exports.Chess;', ctx);
vm.runInContext(fs.readFileSync(path.join(root, 'app/ideas.js'), 'utf8') + '\n;globalThis.Ideas = Ideas;', ctx);
const I = ctx.Ideas, Chess = ctx.Chess;
let failed = 0;
const check = (c, m) => { if (!c){ console.error('FAILED:', m); failed++; } };
// a position from moves in plain coordinates
function at(moves){ const ch = new Chess(); for (const u of moves.split(' ').filter(Boolean)) if (!ch.move({from: u.slice(0, 2), to: u.slice(2, 4), promotion: u[4] || 'q'})) throw new Error('bad move ' + u); return ch.fen(); }
const lines = (moves, u, me = 'w', prev) => I.of(at(moves), u, {me, prev}).lines;
const has = (xs, s) => xs.some(x => x.includes(s));
const show = (name, xs) => console.log(`  ${name.padEnd(34)} ${xs.join(' | ') || '(nothing)'}`);

console.log('== known positions');
let L;
L = lines('', 'e2e4'); show('1 e-pawn two squares', L); check(has(L, 'center') && has(L, 'Opens a line for your'), 'e4: center and a line opened');
L = lines('e2e4 e7e5', 'g1f3'); show('2 knight out', L); check(has(L, "Threatens to take Black's e-pawn"), 'Nf3 hits the e-pawn');
L = lines('e2e4 e7e5 g1f3', 'b8c6'); show("2... knight defends (White's book)", L); check(has(L, "Guards Black's e-pawn from your knight"), 'Nc6 guards e5, from White');
L = lines('e2e4 e7e5 g1f3', 'b8c6', 'b'); show("2... knight defends (Black's book)", L); check(has(L, "Guards your e-pawn from White's knight"), 'Nc6 guards e5, from Black');
L = lines('e2e4 e7e5 g1f3 b8c6', 'f1c4'); show('3 the Italian bishop', L); check(has(L, "Aims at f7, which only Black's king guards"), 'Bc4 aims at f7');
L = lines('e2e4 e7e5 f1c4 b8c6', 'd1h5'); show('3 queen out (scholar)', L); check(has(L, 'Threatens mate on f7'), 'Qh5 threatens mate on f7');
L = lines('e2e4 e7e5 f1c4 b8c6 d1h5', 'g7g6'); show('3... g-pawn one square', L); check(has(L, 'Stops the mate on f7') && has(L, 'Threatens to take your queen'), 'g6 stops the mate and hits the queen');
L = lines('e2e4 e7e5 g1f3 d7d6 f1c4', 'c8g4'); show('3... bishop to the knight', L); check(has(L, 'Pins your knight: moving it would drop the queen'), 'Bg4 pins the knight to the queen');
L = lines('e2e4 e7e5 g1f3 b8c6 f1b5 a7a6', 'b5c6'); show('4 bishop takes the knight', L); check(has(L, 'A trade: bishop for knight'), 'Bxc6 is a trade');
L = lines('e2e4 e7e5 g1f3 b8c6 f1c4 g8f6 f3g5 d7d5 e4d5', 'f6d5', 'w', 'e4d5'); show('5... knight takes back', L); check(!has(L, 'Wins'), 'a recapture is not a win');
L = lines('e2e4 e7e5 g1f3 b8c6 f1c4 g8f6 f3g5 d7d5 e4d5 f6d5', 'g5f7'); show('6 knight takes on f7 (fried liver)', L); check(has(L, 'A fork') || has(L, 'Threatens') || has(L, 'Wins'), 'Nxf7 forks queen and rook');
L = lines('e2e4 e7e5 g1f3 b8c6 f1c4 g8f6 e1g1', '');
L = lines('e2e4 e7e5 g1f3 b8c6 f1c4 g8f6', 'e1g1'); show('5 castles', L); check(has(L, 'Tucks the king in'), 'castling');
L = lines('e2e4 d7d5 e4d5', 'd8d5'); show('2... queen takes back', L);
L = lines('e2e4 d7d5 e4d5 d8d5', 'b1c3'); show('3 knight hits the queen', L); check(has(L, "Threatens to take Black's queen") || has(L, 'queen'), 'Nc3 hits the queen');
L = lines('e2e4 d7d5 e4d5 d8d5 b1c3', 'd5a5'); show('3... queen steps away', L); check(has(L, "Moves Black's queen out of danger"), 'Qa5 gets out of danger');
// a knight fork with check: the knight on b5 jumps to c7, hitting the king and the rook
L = I.of('r3k3/8/8/1N6/8/8/8/4K3 w - - 0 1', 'b5c7', {me: 'w'}).lines; show('knight jumps in with check', L); check(has(L, "A fork: your knight hits Black's king and rook at once"), 'Nc7+ forks king and rook');

console.log('\n== punishments');
const pun = (moves, u, me = 'w') => { const p = I.punish(at(moves), u, {me, words: (f, x) => x}); return p ? `[${p.kind} ${p.u} +${p.gain}${p.took ? ' for ' + p.took : ''}] ${p.lines.join(' | ')}` : '(nothing)'; };
let P;
P = pun('e2e4 e7e5 f1c4 g8f6', 'c4f7'); console.log('  bishop takes on f7 for nothing:', P); check(/take e8f7/.test(P) && /Nothing guarded your bishop/.test(P), 'Bxf7+? Kxf7: nothing guarded the bishop');
P = pun('e2e4 e7e5 g1f3 b8c6', 'f3g5'); console.log('  knight to the edge-ish:', P);
P = pun('e2e4 e7e5 f1c4 b8c6', 'g1f3'); console.log('  a sound move:', P); check(P === '(nothing)', 'Nf3 loses nothing');
P = pun('e2e4 e7e5 g1f3 d7d6', 'f3e5'); console.log('  knight takes a guarded pawn:', P); check(/take d6e5/.test(P), 'Nxe5? dxe5');
P = pun('e2e4 e7e5 g1f3 b8c6 f1c4 g8f6', 'f3e5'); console.log('  the knight grabs the e-pawn:', P); check(/take c6e5 \+3 for 1\]/.test(P), 'Nxe5? Nxe5: a piece for a pawn');
P = pun('e2e4 e7e5 g1f3 b8c6 f1b5 a7a6', 'b5c6'); console.log('  bishop takes the knight:', P); check(P === '(nothing)', 'Bxc6 dxc6 is a fair trade, nothing to punish');
P = pun('e2e4 e7e5 d1h5 b8c6 f1c4', 'g8f6', 'b'); console.log('  Black ignores the mate threat:', P); check(/mate/.test(P), 'Nf6?? Qxf7#');
P = I.punish('r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 0 1', 'b1a3', {me: 'w'}); console.log('  a quiet move:', P ? P.lines.join(' | ') : '(nothing)');

console.log('\n== every book move');
const books = {w: JSON.parse(fs.readFileSync(path.join(root, 'data/build/data_white.json'))), b: JSON.parse(fs.readFileSync(path.join(root, 'data/build/data_black.json')))};
// the full position of a book node: its moves played from the start (odds games start from their own root)
function fenOf(N, i){ const us = []; let j = i; for (; N[j] && N[j].p !== null && N[j].p !== undefined; j = N[j].p) us.push(N[j].u);
  const ch = new Chess(); let ok = true; for (let k = us.length - 1; k >= 0 && ok; k--) ok = !!ch.move({from: us[k].slice(0, 2), to: us[k].slice(2, 4), promotion: us[k][4] || 'q'});
  return ok ? ch.fen() : null; }
const NOTATION = /\b(?![fF][27]\b)[a-h][1-8]\b|\b[KQRBN][a-h]?x?[a-h][1-8]|O-O/;
const kinds = {}, sample = [], all = process.argv.includes('--all'); let n = 0, withLine = {mine: 0, theirs: 0}, tot = {mine: 0, theirs: 0}, noNote = {mine: [0, 0], theirs: [0, 0]};
const t0 = Date.now();
for (const [side, D] of Object.entries(books)){
  const N = D.nodes, me = side, meW = side === 'w' ? 1 : 0;
  for (let i = 0; i < N.length; i++){
    const nd = N[i]; if (nd.p === undefined || nd.p === null || !nd.u) continue;
    const par = N[nd.p], pf = fenOf(N, nd.p); if (!pf) continue;
    const r = I.of(pf, nd.u, {me, prev: par.u}); n++;
    const who = nd.w === meW ? 'mine' : 'theirs'; tot[who]++; if (r.lines.length) withLine[who]++;
    if (!nd.t){ noNote[who][0]++; if (r.lines.length) noNote[who][1]++; }
    for (const f of r.facts) kinds[f.k] = (kinds[f.k] || 0) + 1;
    for (const s of r.lines) check(!NOTATION.test(s), `notation in "${s}" (${side} node ${i})`);
    if (all) console.log(`${side} ${String(i).padStart(4)} ${who === 'mine' ? 'you ' : 'them'} ${nd.l.padEnd(34)} ${r.lines.join(' | ')}`);
    else if ((i * 7919 + (side === 'b' ? 13 : 0)) % 97 === 0 && sample.length < 44) sample.push(`${side} ${who === 'mine' ? 'you ' : 'them'} ${nd.l.padEnd(34)} ${r.lines.join(' | ') || '-'}${nd.t ? '' : '   (no note)'}`);
  }
}
const pc = (a, b) => `${a} of ${b} (${Math.round(100 * a / Math.max(1, b))}%)`;
console.log(`${n} moves in ${Date.now() - t0} ms`);
console.log('player moves with a line:', pc(withLine.mine, tot.mine), '| without a note:', pc(noNote.mine[1], noNote.mine[0]));
console.log('other side with a line:  ', pc(withLine.theirs, tot.theirs), '| without a note:', pc(noNote.theirs[1], noNote.theirs[0]));
console.log('kinds:', Object.entries(kinds).sort((a, b) => b[1] - a[1]).map(([k, v]) => `${k} ${v}`).join(', '));
if (!all) for (const s of sample) console.log('  ' + s);
check(withLine.theirs / tot.theirs > 0.6, 'most of the other side\'s moves get a line');
if (failed){ console.error(failed + ' check(s) failed'); process.exitCode = 1; } else console.log('ideas checks passed');
