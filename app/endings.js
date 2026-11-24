/* ------------------------------------------------------------------ ENDINGS
   The Endings tab and the endings course (app/endings.js, inlined by assemble.py after product.js), for the house
   player and for a player with a playbook of their own (egOn). The house player's course starts with units from a scan
   of their games (pipeline/scan_endings.py) and their own endings (kind `mine`); everyone gets the basics. Every
   position, line and checkpoint answer is built by pipeline/build_endings.py (EGD). Each position has a rating on the
   lichess puzzle scale (r), and the player gets the ones near their level (EG.level: their rating moved to that scale,
   with the Easier and Harder setting egl). King and queen, king and rook, and king and pawn against a lone king are
   judged by exact tables (EGT, pipeline/endtables.mjs); a lone king against two pieces by the rule that only a
   stalemate or a piece left to be taken throws the win away; everything else by the engine, which also plays the
   other side. Show me how plays a position's line (sol: the method's moves, the table's, Stockfish's or the solution
   of a position from a real game; else the engine's move by move) with the reason for each move (ex, EGD.why, or what
   the board shows). Progress is Prog.d.end (merged in mergeProg by egMerge): p, each position played as [runs, clean,
   last time, best stars]; u, each unit: l when its pictures were seen, a the lines played along (time each), q the
   checkpoint's best [score, of, time]. */
const EGD = /*__DATA_E__*/null, EGT = /*__TABLES_E__*/null;
const EG_MATE = 99000;
const EG_HOUSE = 1160;      // the house player's chess.com blitz rating (their main account): the level their endings start from
function egOn(){ return !!EGD && typeof PERSONA !== 'undefined' && (PERSONA === 'house' || PERSONA === 'ready'); }
const egKey = fen => fen.split(' ').slice(0, 4).join(' ');
const egUci = m => m.from + m.to + (m.promotion || '');

// The exact tables: one byte per position, ((strong king * 64 + its piece) * 64 + lone king) * 2 + side to move (0: the
// stronger side), squares a1 = 0; 0 is a draw, anything else the distance in plies plus one.
const EGTB = {
  t: null, wait: null,
  load(){
    if (this.wait) return this.wait;
    const un = async b64 => { const bin = Uint8Array.from(atob(b64), c => c.charCodeAt(0));
      return new Uint8Array(await new Response(new Blob([bin]).stream().pipeThrough(new DecompressionStream('deflate'))).arrayBuffer()); };
    const go = EGT && typeof DecompressionStream === 'function' ? Promise.all(['kqk', 'krk', 'kpk'].map(k => un(EGT[k]))) : Promise.reject(new Error('no tables'));
    this.wait = go.then(([q, r, p]) => { this.t = {kqk: q, krk: r, kpk: p}; }, () => { this.t = null; });
    return this.wait;
  },
  // the value for the side to move: {w: 1 a win, 0 a draw, -1 a loss; d: plies to mate, or for king and pawn to the
  // promotion that wins}, or null when the position isn't one of the three
  probe(fen){
    if (!this.t) return null;
    const [pl, turn] = fen.split(' '), a = fenArr(pl);
    let wk = -1, bk = -1, x = -1, xp = '', n = 0;
    for (let i = 0; i < 64; i++){ const p = a[i]; if (!p) continue; n++; if (p === 'K') wk = i; else if (p === 'k') bk = i; else { x = i; xp = p; } }
    const name = n === 3 && {q: 'kqk', r: 'krk', p: 'kpk'}[xp.toLowerCase()]; if (!name) return null;
    const white = xp === xp.toUpperCase(), f = white ? 0 : 56;
    const stm = (turn === 'w') === white ? 0 : 1, v = this.t[name][((((white ? wk : bk) ^ f) * 64 + (x ^ f)) * 64 + ((white ? bk : wk) ^ f)) * 2 + stm];
    return v ? {w: stm ? -1 : 1, d: v - 1} : {w: 0, d: null};
  },
  // the value for the side that plays u, after it
  after(fen, u){
    const ch = new Chess(fen); if (!ch.move(uciObj(u))) return null;
    if (ch.in_checkmate()) return {w: 1, d: 0};
    if (ch.in_stalemate() || ch.insufficient_material()) return {w: 0, d: null};
    const r = this.probe(ch.fen()); return r && {w: -r.w, d: r.d};
  },
  each(fen, f){ let best = null; for (const m of new Chess(fen).moves({verbose: true})){ const u = egUci(m), r = this.after(fen, u); if (!r) continue; const k = f(m, r); if (k && (!best || cmpArr(k, best.k) > 0)) best = {k, u}; } return best && best.u; },
  // the quickest win, else a move that holds the draw (a capture first)
  best(fen){ return this.each(fen, (m, r) => r.w === 1 ? [2, -r.d] : r.w === 0 ? [1, m.captured ? 1 : 0] : [0, r.d]); },
  // the other side's defence: a draw if there is one, else the longest loss, toward the middle
  defend(fen){ return this.each(fen, (m, r) => { const t = sqi(m.to), mid = -Math.max(Math.abs(3.5 - t % 8), Math.abs(3.5 - (t >> 3)));
    return r.w === 1 ? [3, -r.d, 0] : r.w === 0 ? [2, m.captured ? 1 : 0, mid] : [1, r.d, mid]; }); },
  // the attacking side in a drawn position: the move that leaves the defender the fewest moves that hold
  tricky(fen){ return this.each(fen, (m, r) => {
    if (r.w === 1) return [9, -r.d]; if (r.w < 0) return null;
    const ch = new Chess(fen); ch.move(uciObj(egUci(m))); const f2 = ch.fen();
    const holds = ch.moves({verbose: true}).filter(x => { const q = this.after(f2, egUci(x)); return q && q.w >= 0; }).length;
    return [1, -holds, m.piece === 'p' ? 1 : 0]; }) || this.defend(fen); }
};

// one search for the endings: the score for the side to move (a mate as +-(100000 - 100 n)) and the engine's line
function egSearch(fen, cb, depth = 18, ms = 1200){
  const stm = fen.split(' ')[1] === 'w' ? 1 : -1;
  Engine.run({fen, multipv: 1, depth, ms, onDone: j => { const l = j.lines[0]; cb(l && l.pv && l.pv[0] ? {s: scoreNum(l.s) * stm, pv: l.pv} : null); }, onFail: () => cb(null)});
}
// a lone king with nothing to say: the move toward the middle
function egMid(fen){
  let best = null;
  for (const m of new Chess(fen).moves({verbose: true})){ const t = sqi(m.to), k = -Math.max(Math.abs(3.5 - t % 8), Math.abs(3.5 - (t >> 3))); if (!best || k > best.k) best = {k, u: egUci(m)}; }
  return best && best.u;
}

const EG = {
  pick: (() => { try { return JSON.parse(localStorage.getItem('playbook-endings') || 'null'); } catch(e){ return null; } })(),
  last: null,
  kind: id => EGD.kinds.find(k => k.id === id),
  item: id => EGD.items.find(i => i.id === id),
  unit: id => EGD && EGD.units.find(u => u.id === id),
  rd(){ return Prog.d.end || {p: {}, u: {}}; },
  st(){ const d = Prog.d; d.end = d.end || {}; d.end.p = d.end.p || {}; d.end.u = d.end.u || {}; return d.end; },
  up(uid){ const u = this.st().u; return u[uid] || (u[uid] = {}); },
  pr(id){ return this.rd().p[id] || [0, 0, 0, 0]; },
  savePick(){ try { localStorage.setItem('playbook-endings', JSON.stringify(this.pick)); } catch(e){} },
  engineKind: K => K.how === 'engine' || K.how === 'mate',
  canPlay(K){ return !this.engineKind(K) || Engine.state !== 'failed'; },
  chosen(){ const ks = this.kindsOn().map(k => k.id), p = (this.pick || []).filter(k => ks.includes(k)); return p.length ? p : null; },
  // the kinds this player has: the house player's own endings are theirs alone
  kindsOn(){ return EGD.kinds.filter(k => k.id !== 'mine' || PERSONA === 'house'); },
  // a position's kind, with what the position itself says about its goal (a position from a real game may be a mate
  // to find, or a draw to hold, in a kind that is about winning)
  kindFor(it){ const K = this.kind(it.k); return it.goal || it.how ? Object.assign({}, K, it.goal ? {goal: it.goal} : {}, it.how ? {how: it.how} : {}) : K; },
  // the player's level on the lichess puzzle scale: the house player's rating, or what the player's own games show,
  // moved to that scale (chess.com ratings sit about 350 under it, lichess's about 50), and 150 a step for Easier and
  // Harder (the setting egl, from -3 to 3)
  level(){
    const me = typeof meOf === 'function' ? meOf(Prog.d) : null, P = me && me.P;
    const lich = ((me && me.src) || {}).site === 'lichess' || (P && P.site === 'lichess');
    const base = PERSONA !== 'house' && P && P.rating ? P.rating + (lich ? 50 : 350) : PERSONA === 'house' ? EG_HOUSE + 350 : 1300;
    return Math.round((base + 150 * (+SET.egl || 0)) / 10) * 10;
  },
  // the positions near the level: 250 under it to 300 over; where fewer than n are, the nearest ones (all of a kind
  // whose positions share one rating)
  dist(it){ const lo = this.level() - 250, hi = lo + 550; return it.r < lo ? lo - it.r : it.r > hi ? it.r - hi : 0; },
  near(list, n = 3){
    if (list.length <= n) return list;
    const cut = list.map(it => this.dist(it)).sort((a, b) => a - b)[n - 1];
    return list.filter(it => this.dist(it) <= cut);
  },
  // the positions the units' checkpoints ask, kept out of practice games
  asked(){ return this._asked || (this._asked = new Set(EGD.units.flatMap(U => U.check.flatMap(c => (c.alts || [c]).map(a => a.fen))))); },
  // the positions a game can start from, each once, near the player's level: a unit's kinds; the kinds picked, each
  // with its positions nearest the level; or for Everything, the kinds that have positions at that level
  pool(uid){
    const U = uid && this.unit(uid), pick = !U && this.chosen(), ks = U ? U.kinds : pick || this.kindsOn().map(k => k.id), seen = new Set(), skip = U && this.asked();
    const all = EGD.items.filter(it => ks.includes(it.k) && this.canPlay(this.kindFor(it)) && !(skip && skip.has(it.fen)) && !seen.has(it.fen) && seen.add(it.fen));
    if (U) return this.near(all);
    const by = {}; for (const it of all) (by[it.k] = by[it.k] || []).push(it);
    const fit = Object.keys(by).filter(k => by[k].some(it => !this.dist(it))), keep = pick || !fit.length ? Object.keys(by) : fit;
    return keep.flatMap(k => this.near(by[k]));
  },
  // the next position: a kind at random among those picked (each as likely as any other), and in it a position never
  // played, else the one played longest ago; never the one just played
  next(uid){
    const pool = this.pool(uid).filter(it => it.id !== this.last); if (!pool.length) return this.pool(uid)[0] || null;
    const ks = [...new Set(pool.map(it => it.k))], k = ks[Math.floor(Math.random() * ks.length)];
    return pool.filter(it => it.k === k).map(it => ({it, r: this.pr(it.id)})).sort((a, b) => (a.r[0] ? 1 : 0) - (b.r[0] ? 1 : 0) || a.r[2] - b.r[2])[0].it;
  },
  fen(D){ return D.kind === 'egq' ? (D.view || D.items[D.k].fen) : D.hist[D.hist.length - 1]; },
  legal(D){ const fen = this.fen(D); return new Chess(fen).moves({verbose: true}).map(egUci); },
  lastU(D){ return D.kind === 'egq' ? D.lastU : D.moves.length ? D.moves[D.moves.length - 1] : null; },
  cap(D){ return D.k.cap || (D.it.par ? D.it.par + 12 : 40); },
  goalText(D){ return this.goalOf(D.k, D.it); },
  goalOf(K, it){ K = it ? Object.assign({}, K, it.goal ? {goal: it.goal} : {}, it.how ? {how: it.how} : {}) : K;
    return K.goal === 'mate' && K.how === 'mate' && it.par ? `Mate in ${it.par}` : {mate: 'Mate them', queen: 'Queen the pawn', hold: 'Hold the draw', win: 'Win it'}[K.goal]; },
  // the line Show me how plays from the start, when the build worked one out; and while a game follows a real game's
  // solution, that game's reply
  solOf(it){ return it.sol && it.sol.length ? it.sol : null; },
  onSol(D){ const s = D.it.pz && this.solOf(D.it); return !!s && D.moves.every((u, k) => s[k] === u); },

  // ---- a game against the engine (and Play along, the same board with the green arrow)
  async start(id, o = {}){
    await EGTB.load();
    const it = this.item(id); if (!it) return;
    const K = this.kindFor(it);
    if (['kqk', 'krk', 'kpk'].includes(K.how) && !EGTB.t){ toast('This ending needs a newer browser.'); return; }
    this.last = id;
    S.egState = {kind: 'eg', id, it, k: K, me: it.me, hist: [it.fen], moves: [], keys: [egKey(it.fen)], state: 'play', busy: false, sel: null, flash: null,
      hint: null, msg: '', feed: '', tries: 0, slips: 0, mine: 0, unit: o.unit || null, tick: 0};
    S.view = 'endings'; render(); setHash(); window.scrollTo({top: 0, behavior: reduced ? 'auto' : 'smooth'});
  },
  // a line of a unit to play along: the green arrow shows each of your moves, the other side's come by themselves
  async along(uid, k){
    await EGTB.load();
    const U = this.unit(uid), L = U && U.along[k]; if (!L) return;
    const it = {id: L.id, fen: L.fen, me: L.me, k: U.kinds[0]};
    S.egState = {kind: 'eg', guided: true, id: L.id, it, k: Object.assign({}, this.kind(U.kinds[0]), {goal: 'along'}), me: L.me, line: L.moves, ex: L.ex || '', hist: [L.fen], moves: [],
      keys: [egKey(L.fen)], state: 'play', busy: false, sel: null, flash: null, hint: L.moves[0], msg: '', feed: '', tries: 0, slips: 0, mine: 0, unit: uid, tick: 0};
    S.view = 'endings'; render(); setHash(); window.scrollTo({top: 0, behavior: reduced ? 'auto' : 'smooth'});
  },
  // Show me how: a position's line on the same board, the arrow showing each of your moves with why it is played (Play
  // it makes the move for you) and the other side's coming by themselves; where the build worked out no line, the
  // engine's move each turn. Nothing is recorded: Try it yourself starts the game.
  async show(id, o = {}){
    await EGTB.load();
    const it = this.item(id); if (!it) return;
    const K = this.kindFor(it), line = this.solOf(it);
    if (!line && Engine.state === 'failed'){ toast('Show me how needs the engine, and it couldn\'t start here.'); return; }
    this.last = id;
    S.egState = {kind: 'eg', guided: true, show: true, live: !line, id, it, k: K, me: it.me, line, ex: line ? it.ex || '' : '', hist: [it.fen], moves: [], keys: [egKey(it.fen)],
      state: 'play', busy: false, sel: null, flash: null, hint: line ? line[0] : null, msg: '', feed: '', tries: 0, slips: 0, mine: 0, unit: o.unit || null, tick: 0};
    S.view = 'endings'; render(); setHash(); window.scrollTo({top: 0, behavior: reduced ? 'auto' : 'smooth'});
    if (!line) this.liveHint(S.egState);
  },
  // the engine's move for you, where there is no line (the tables' where they know)
  liveHint(D){
    const t = ++D.tick, fen = this.fen(D), tb = EGTB.probe(fen); D.busy = true; D.hint = null; renderDrillPanel();
    const got = u => { if (S.drill !== D || D.tick !== t) return; D.busy = false; D.hint = u || null; if (!u) return this.finish(D, 'along'); renderDrillBoard(); renderDrillPanel(); };
    if (tb) return got(EGTB.best(fen));
    egSearch(fen, r => got(r && r.pv[0]), 18, 1500);
  },
  // why a move of yours is played: the build's reason for the line's move, else what the board shows it does
  whyOf(D, fen, u, k){
    const c = D.ex && D.ex[k], w = c && EGD.why && EGD.why[c]; if (w) return w;
    try { const x = typeof Ideas !== 'undefined' && Ideas.of(fen, u, {me: D.me}); return (x && x.lines && x.lines[0]) || ''; } catch(e){ return ''; }
  },
  tryMove(u, to){
    const D = S.drill; if (!D || D.busy || D.state !== 'play') return;
    if (D.kind === 'egq') return this.answer(D, u, to);
    if (D.guided) return this.guidedTry(D, u, to);
    const fen0 = this.fen(D), ch = new Chess(fen0), mv = ch.move(uciObj(u)); if (!mv) return;
    const fen1 = ch.fen(), t = ++D.tick;
    D.sel = null; D.hint = null; D.flash = null; D.msg = ''; D.feed = ''; D.busy = true;
    D.hist.push(fen1); D.moves.push(u); D.keys.push(egKey(fen1));
    renderDrillBoard(); renderDrillPanel();                          // your move lands at once
    this.judge(D, fen1, mv, v => { if (S.drill !== D || D.tick !== t) return; v.ok ? this.accept(D, fen1, v, t) : this.slip(D, fen0, fen1, to, v, t); });
  },
  // is the move good? {ok, done: 'won' | 'held', reply: their move, why: what went wrong}
  judge(D, fen1, mv, cb){
    const goal = D.k.goal, hold = goal === 'hold', ch = new Chess(fen1), K = egKey(fen1);
    if (ch.in_checkmate()) return cb({ok: true, done: 'won'});
    if (ch.in_stalemate()) return cb(hold ? {ok: true, done: 'held'} : {ok: false, why: 'stale'});
    if (ch.insufficient_material()) return cb(hold ? {ok: true, done: 'held'} : {ok: false, why: 'nomat'});
    if (D.keys.filter(k => k === K).length >= 3) return cb(hold ? {ok: true, done: 'held'} : {ok: false, why: 'rep'});
    const queened = mv.flags.includes('p');
    // a position from a real game, its solution followed: the known answer, and the game's own reply
    if (D.it.pz && this.onSol(D)) return cb({ok: true, reply: D.it.sol[D.moves.length] || null});
    if (D.k.how === 'mate'){
      // a mate to find: the move has to keep a mate within the moves it should take (two more for a long one)
      return egSearch(fen1, r => {
        if (!r) return cb(Engine.state === 'failed' ? {ok: false, why: 'noeng'} : {ok: true, reply: egMid(fen1)});
        const s = -r.s, left = s >= EG_MATE ? Math.round((100000 - s) / 100) : null, par = D.it.par || 3;
        if (left === null) return cb({ok: false, why: 'nomate', reply: r.pv[0]});
        if (D.mine + 1 + left > par + (par > 3 ? 2 : 0)) return cb({ok: false, why: 'slower'});
        cb({ok: true, reply: r.pv[0]});
      }, 20, 1500);
    }
    if (D.k.how === 'bare'){
      const take = ch.moves({verbose: true}).find(m => m.captured);
      if (take) return cb({ok: false, why: 'drop', reply: egUci(take)});
      return egSearch(fen1, r => cb({ok: true, reply: r ? r.pv[0] : egMid(fen1)}), 12, 500);
    }
    const tb = EGTB.probe(fen1);
    if (tb){
      const mine = -tb.w;
      if (hold ? mine < 0 : mine <= 0) return cb({ok: false, why: mine < 0 ? 'lose' : 'draw', reply: tb.w > 0 ? EGTB.best(fen1) : EGTB.defend(fen1)});
      if ((goal === 'queen' && queened) || goal === 'win') return cb({ok: true, done: 'won'});
      return cb({ok: true, reply: tb.w < 0 ? EGTB.defend(fen1) : EGTB.tricky(fen1)});
    }
    egSearch(fen1, r => {
      if (!r) return cb(Engine.state === 'failed' ? {ok: false, why: 'noeng'} : {ok: true, reply: egMid(fen1)});
      const s = -r.s, keep = Math.min(200, (D.it.v || 400) / 2);    // from your side
      if (hold ? s <= -200 : s < keep) return cb({ok: false, why: s <= -EG_MATE ? 'mated' : s <= -200 ? 'lose' : 'draw', reply: r.pv[0]});
      // won: a pawn queened, their king left alone, or for an ending that started short of +8, the engine at +9
      const bare = !fen1.split(' ')[0].split('').some(c => D.me === 'w' ? 'pnbrq'.includes(c) : 'PNBRQ'.includes(c));
      if ((goal === 'queen' && queened) || (goal === 'win' && (queened || bare || ((D.it.v || 0) < 800 && s >= 900)))) return cb({ok: true, done: 'won'});
      cb({ok: true, reply: r.pv[0]});
    });
  },
  accept(D, fen1, v, t){
    D.tries = 0; D.mine++;
    if (v.done) return this.finish(D, v.done);
    if (D.k.goal === 'hold' && D.mine >= (D.it.hold || 10)) return this.finish(D, 'held');
    // a position from a real game is solved once its solution's moves are played, each one good
    if (D.it.pz && D.k.how !== 'mate' && D.mine >= Math.ceil(D.it.sol.length / 2)) return this.finish(D, 'won');
    if (D.mine >= this.cap(D)) return this.finish(D, 'slow');
    this.reply(D, fen1, this.onSol(D) ? D.it.sol[D.moves.length] || v.reply : v.reply, t);
  },
  // their move, after a moment, sliding in
  reply(D, fen1, r, t){
    setTimeout(() => {
      if (S.drill !== D || D.tick !== t) return;
      const ch = new Chess(fen1), m = r && ch.move(uciObj(r));
      if (!m){ D.busy = false; renderDrillPanel(); return; }
      const fen2 = ch.fen(); D.hist.push(fen2); D.moves.push(r); D.keys.push(egKey(fen2)); D.busy = false;
      D.feed = `${OPP}: ${lc(wordsAt(fen1, r))}`;
      const hold = D.k.goal === 'hold';
      if (ch.in_checkmate()) return this.finish(D, 'lost', {u: r});
      if (ch.in_stalemate() || ch.insufficient_material() || D.keys.filter(k => k === egKey(fen2)).length >= 3) return this.finish(D, hold ? 'held' : 'drawn', {u: r});
      if (D.live){ renderDrillBoard({u: r, meta: {}}); return this.liveHint(D); }
      if (D.guided){ D.hint = D.line[D.moves.length] || null; if (!D.hint) return this.finish(D, 'along', {u: r}); }
      renderDrillBoard({u: r, meta: {}}); renderDrillPanel();
    }, D.guided ? 420 : 280);
  },
  slip(D, fen0, fen1, to, v, t){
    D.hist.pop(); D.moves.pop(); D.keys.pop(); D.busy = false;
    if (v.why === 'noeng'){ D.msg = this.whyText(v, fen1); renderDrillBoard(); renderDrillPanel(); return; }
    if (D.tries === 0) D.slips++;
    D.tries++; D.flash = {sq: to, ok: false};
    D.msg = this.whyText(v, fen1);
    renderDrillBoard(); renderDrillPanel();
    setTimeout(() => { if (S.drill === D && D.flash && !D.flash.ok){ D.flash = null; renderDrillBoard(); } }, 650);
    if (D.tries < 2) return;
    // the second miss: the arrow
    const hint = u => { if (S.drill !== D || D.tick !== t || !u) return; D.hint = u; D.msg = 'Play the arrow\'s move.'; renderDrillBoard(); renderDrillPanel(); };
    const tb = EGTB.probe(fen0);
    if (tb) hint(EGTB.best(fen0)); else egSearch(fen0, r => hint(r && r.pv[0]), 16, 900);
  },
  // what a move that throws it away runs into, in a line
  whyText(v, fen1){
    const said = v.reply ? `${OPP}: ${lc(wordsAt(fen1, v.reply))}` : '';
    const map = {noeng: 'This ending needs the engine, and it couldn\'t start here.', stale: 'Stalemate: a draw.', nomat: 'Nothing left to mate with: a draw.', rep: 'Third time in this position: a draw.',
      drop: `${said}. That throws the win away.`, draw: `${said}. That lets the win go.`, lose: `${said}. That loses.`, mated: `${said}, with mate to follow.`,
      nomate: `${said}. The mate is gone.`, slower: 'Still a mate, but a slower one.'};
    return map[v.why] || '';
  },
  guidedTry(D, u, to){
    const want = D.live ? D.hint : D.line[D.moves.length];
    if (!want || u !== want){ D.flash = {sq: to, ok: false}; D.msg = 'Follow the green arrow.'; renderDrillBoard(); renderDrillPanel();
      setTimeout(() => { if (S.drill === D && D.flash && !D.flash.ok){ D.flash = null; D.msg = ''; renderDrillBoard(); renderDrillPanel(); } }, 700); return; }
    const fen0 = this.fen(D), ch = new Chess(fen0), mv = ch.move(uciObj(u)); const fen1 = ch.fen(), t = ++D.tick;
    D.hist.push(fen1); D.moves.push(u); D.keys.push(egKey(fen1)); D.flash = null; D.msg = ''; D.mine++;
    D.said = lc(wordsAt(fen0, u));
    if (D.live){
      // the engine's way: over when the ending is won (or held), else their reply and your next move
      D.busy = true; D.hint = null; renderDrillBoard(); renderDrillPanel();
      return this.judge(D, fen1, mv, v => { if (S.drill !== D || D.tick !== t) return;
        if (v.done || !v.reply || D.mine >= 30 || (D.k.goal === 'hold' && D.mine >= (D.it.hold || 10))) return this.finish(D, 'along');
        this.reply(D, fen1, v.reply, t); });
    }
    const r = D.line[D.moves.length];
    if (!r){ renderDrillBoard(); return this.finish(D, 'along'); }
    D.busy = true; D.hint = null; renderDrillBoard(); renderDrillPanel();
    this.reply(D, fen1, r, t);
  },
  // Play it: the arrow's move made for you
  playIt(D){ if (!D || !D.guided || D.busy || D.state !== 'play' || !D.hint) return; const u = D.hint; this.guidedTry(D, u, u.slice(2, 4)); },
  finish(D, res, last){
    if (D.show) res = 'along';                                       // Show me how records nothing
    D.state = 'done'; D.busy = false; D.res = res; D.hint = null;
    const won = res === 'won' || res === 'held', par = D.it.par;
    D.stars = !won ? 0 : D.slips ? (D.slips === 1 ? 2 : 1) : par ? (D.mine <= par + 2 ? 3 : D.mine <= par + 6 ? 2 : 1) : 3;
    if (res === 'along' && D.show){}
    else if (res === 'along'){ const u = this.up(D.unit), a = u.a || (u.a = {}); a[D.id] = Date.now(); Prog.save(); }
    else if (!D.tour){
      const p = this.st().p, r = p[D.id] || [0, 0, 0, 0];
      p[D.id] = [r[0] + 1, r[1] + (won && !D.slips ? 1 : 0), Date.now(), Math.max(r[3] || 0, D.stars)];
      const n = this.st().n || (this.st().n = [0, 0]); n[0]++; if (won && !D.slips) n[1]++;
      Prog.save();
    }
    if (won && !D.slips) Sound.play('done');
    render();
    if (last && last.u){ const el = document.getElementById('db'); if (el) animateMove(el.querySelector('svg'), last.u, {}, false); }
  },

  // ---- the board's panel
  panelHTML(D){
    if (D.kind === 'egq') return this.quizPanelHTML(D);
    const K = D.k, U = D.unit && this.unit(D.unit);
    if (D.guided){
      const mine = D.line ? Math.ceil(D.line.length / 2) : 0, par = D.it.par;
      const bar = mine ? `<div class="progressbar" aria-hidden="true"><i style="width:${D.state === 'done' ? 100 : Math.round(D.mine / mine * 100)}%"></i></div>` : '';
      const head = `<p class="kicker">${D.show ? 'Show me how' : 'Play along'}</p><h3>${esc(D.show ? this.goalOf(K, D.it) : U ? U.title : K.name)}</h3>${bar}`
        + (D.show ? `<p class="egcount tnum">${plural(D.mine, 'move')}${par ? ` · par ${par}` : ''}</p>` : '');
      if (D.state === 'done'){
        if (D.show) return `<div class="dpanel">${head}<div class="donebox"><h4>${par && D.mine <= par ? 'That\'s par' : 'That\'s how'}</h4>
          <div class="lesson-actions"><button class="btn primary" id="egTry">Try it yourself</button><button class="btn" id="egAgain">Again</button></div><div id="deng"></div></div></div>`;
        return `<div class="dpanel">${head}<div class="donebox"><h4>Played along</h4><div class="lesson-actions">${this.nextBtn(D)}<button class="btn" id="egAgain">Again</button></div><div id="deng"></div></div></div>`;
      }
      const my = !D.busy && D.hint, fen = this.fen(D), said = D.feed ? `<p class="gsaid">${esc(D.feed)}</p>` : '';
      const why = my ? this.whyOf(D, fen, D.hint, D.mine) : '', point = D.show && !D.moves.length && D.it.pt ? `<p class="gsaid">${esc(D.it.pt)}</p>` : '';
      return `<div class="dpanel">${head}<div class="coachnote gcoach" role="status"><div class="cntx">${point}${said}${my ? `<p class="gmove">${esc(wordsAt(fen, D.hint))}</p>${why ? `<p class="gwhy">${esc(why)}</p>` : ''}` : `<p class="gmove wait">${OPP} is thinking…</p>`}${D.msg ? `<p class="gwarn">${esc(D.msg)}</p>` : ''}</div></div>
        ${D.show && my ? '<div class="lesson-actions"><button class="btn" id="egPlayIt">Play it</button></div>' : ''}</div>`;
    }
    const par = D.it.par, cnt = K.goal === 'hold' ? `<div class="progressbar" aria-hidden="true"><i style="width:${Math.round(Math.min(1, D.mine / (D.it.hold || 10)) * 100)}%"></i></div><p class="egcount tnum">${D.mine} of ${D.it.hold || 10} moves held</p>`
      : K.how === 'mate' ? '' : `<p class="egcount tnum">${D.mine} ${D.mine === 1 ? 'move' : 'moves'}${par ? ` · par ${par}` : ''}</p>`;
    const head = `<p class="kicker">${esc(K.name)}${D.it.src ? ' · vs ' + esc(D.it.src.split(' ').slice(1).join(' ')) : U ? ' · ' + esc(U.title) : ''}</p><h3>${this.goalText(D)}</h3>${cnt}`;
    if (D.state === 'done') return `<div class="dpanel">${head}${this.doneBox(D)}</div>`;
    const status = D.busy ? `${OPP} is thinking…` : 'Your move';
    return `<div class="dpanel">${head}<div class="status ${D.busy ? 'wait' : ''} ${D.tries ? 'bad' : ''}"><span class="bub"></span>${status}</div>
      <p class="feedback">${D.msg ? esc(D.msg) : D.feed ? esc(D.feed) : '&nbsp;'}</p></div>`;
  },
  starsHTML(n){ return `<span class="egstars" aria-label="${n} of 3 stars">${[1, 2, 3].map(k => `<svg viewBox="0 0 24 24" class="${k <= n ? 'on' : ''}" aria-hidden="true"><path d="M12 2.8l2.8 5.9 6.4.8-4.7 4.4 1.2 6.4L12 17.2l-5.7 3.1 1.2-6.4L2.8 9.5l6.4-.8z"/></svg>`).join('')}</span>`; },
  doneBox(D){
    const won = D.res === 'won' || D.res === 'held';
    const h = {won: D.k.how === 'mate' ? 'Mate' : D.k.goal === 'mate' ? `Mate in ${D.mine}` : D.k.goal === 'queen' ? 'Queened' : 'Won', held: 'Held', slow: 'Too slow', lost: 'Mated', drawn: 'A draw'}[D.res];
    const sub = won ? (D.slips ? plural(D.slips, 'slip') : 'Clean') : D.res === 'slow' ? `${D.k.goal === 'mate' ? 'No mate' : 'Not won'} in ${this.cap(D)} moves` : '';
    const showme = this.canShow(D.it) && !(won && !D.slips && D.stars === 3) ? '<button class="btn" id="egShow">Show me how</button>' : '';
    return `<div class="donebox ${won && !D.slips ? '' : 'bad'}"><h4>${h}</h4>${won ? this.starsHTML(D.stars) : ''}${sub ? `<p class="egsub">${esc(sub)}</p>` : ''}${D.it.why ? `<p class="egsub">In the game: ${esc(lc(D.it.why))}</p>` : D.it.pt ? `<p class="egsub">${esc(D.it.pt)}</p>` : ''}
      <div class="lesson-actions">${this.nextBtn(D)}<button class="btn" id="egAgain">Again</button>${showme}</div><div id="deng"></div></div>`;
  },
  // Show me how can play a position when it has a line, or when the engine is there to play one
  canShow(it){ return !!(it && (this.solOf(it) || Engine.state !== 'failed'));
  },
  nextBtn(D){
    if (D.unit){ const U = this.unit(D.unit), nx = this.unitNext(U);
      return nx ? `<button class="btn primary" id="egUnitNext">${esc(nx.cta)}</button><button class="btn" data-egunit="${U.id}">Back to the unit</button>` : `<button class="btn primary" data-egunit="${U.id}">Back to the unit</button>`; }
    return '<button class="btn primary" id="egNext">Next ending</button>';
  },
  wirePanel(){
    const D = S.drill, p = document.getElementById('dpanel'); if (!p || !D) return;
    const b = id => document.getElementById(id);
    if (b('egNext')) b('egNext').onclick = () => { const it = this.next(); this.peek = null; if (it) this.start(it.id); };
    if (b('egAgain')) b('egAgain').onclick = () => D.kind === 'egq' ? this.quiz(D.unit) : D.show ? this.show(D.id, {unit: D.unit}) : D.guided ? this.along(D.unit, this.unit(D.unit).along.findIndex(l => l.id === D.id)) : this.start(D.id, {unit: D.unit});
    if (b('egShow')) b('egShow').onclick = () => this.show(D.id, {unit: D.unit});
    if (b('egTry')) b('egTry').onclick = () => this.start(D.id, {unit: D.unit});
    if (b('egPlayIt')) b('egPlayIt').onclick = () => this.playIt(D);
    if (b('egUnitNext')) b('egUnitNext').onclick = () => { const nx = this.unitNext(this.unit(D.unit)); if (nx) nx.go(); };
    if (b('egQNext')) b('egQNext').onclick = () => this.quizNext(D);
    p.querySelectorAll('[data-egunit]').forEach(x => x.onclick = () => this.openUnit(x.dataset.egunit));
  },

  // ---- the checkpoint: one position at a time, one try each
  quiz(uid){
    const U = this.unit(uid); if (!U) return;
    const items = U.check.map(c => c.alts ? this.pickAlt(c.alts) : c);
    S.egState = {kind: 'egq', unit: uid, items, k: 0, res: [], state: 'play', sel: null, flash: null, msg: '', view: null, lastU: null, arrows: null, me: items[0].me, busy: false, answered: null};
    S.view = 'endings'; render(); setHash(); window.scrollTo({top: 0, behavior: reduced ? 'auto' : 'smooth'});
  },
  need: n => n <= 3 ? n - 1 : Math.ceil(n * .8),
  // a question with a position for each band of ratings: the one nearest the player's level
  pickAlt(alts){ const t = this.level(); return alts.slice().sort((a, b) => this.dist(a) - this.dist(b) || Math.abs(a.r - t) - Math.abs(b.r - t))[0]; },
  answer(D, u, to){
    if (D.answered) return;
    const it = D.items[D.k], ok = it.ok.includes(u);
    D.res[D.k] = ok; D.answered = ok ? 'ok' : 'bad'; D.sel = null; D.flash = {sq: to, ok};
    if (ok){ D.arrows = [u + 'g']; D.msg = /mate/i.test(it.ask) ? 'Mate.' : 'That\'s it.'; }
    else {
      const [r, what] = it.bad[u] || [null, 'draw'], ch = new Chess(it.fen); ch.move(uciObj(u));
      const said = r ? `${OPP}: ${lc(wordsAt(ch.fen(), r))}` : '';
      D.arrows = [u + 'r', it.ok[0] + 'g'];
      D.msg = {stale: 'Stalemate: a draw.', draw: `${said}. A draw.`, lose: `${said}. That loses.`, mated: `${said}: mate.`, less: 'That still wins, but it isn\'t the move.'}[what] || '';
    }
    renderDrillBoard(); renderDrillPanel();
  },
  quizNext(D){
    if (D.k + 1 < D.items.length){ D.k++; D.answered = null; D.arrows = null; D.flash = null; D.msg = ''; D.me = D.items[D.k].me; render(); return; }
    D.state = 'done';
    const score = D.res.filter(Boolean).length, n = D.items.length, u = this.up(D.unit), q = u.q || [0, n, 0];
    if (score >= q[0]) u.q = [score, n, Date.now()];
    Prog.save(); render();
  },
  quizPanelHTML(D){
    const U = this.unit(D.unit), n = D.items.length;
    if (D.state === 'done'){
      const score = D.res.filter(Boolean).length, pass = score >= this.need(n);
      return `<div class="dpanel"><p class="kicker">Checkpoint · ${esc(U.title)}</p><div class="bigstat"><b class="tnum">${score}/${n}</b><span>${pass ? 'Passed' : `${this.need(n)} to pass`}</span></div>
        <div class="lesson-actions">${pass ? this.nextBtn(D) : `<button class="btn primary" id="egAgain">Try again</button><button class="btn" data-egunit="${U.id}">Back to the unit</button>`}</div></div>`;
    }
    const it = D.items[D.k];
    return `<div class="dpanel"><p class="kicker">Checkpoint · ${D.k + 1} of ${n}</p><h3>${esc(it.ask)}</h3>
      <div class="progressbar" aria-hidden="true"><i style="width:${Math.round(D.k / n * 100)}%"></i></div>
      ${D.answered ? `<p class="feedback ${D.answered === 'ok' ? 'good' : 'bad'}">${esc(D.msg)}${it.why ? `<span class="pwhy">${esc(it.why)}</span>` : ''}</p><div class="lesson-actions"><button class="btn primary" id="egQNext">${D.k + 1 < n ? 'Next' : 'See how you did'}</button></div>`
        : `<div class="status"><span class="bub"></span>${MYC} to move</div>`}</div>`;
  },

  // ---- the course: units, each with pictures, lines to play along, endings to win and a checkpoint
  steps(U){
    const u = this.rd().u[U.id] || {}, a = u.a || {}, won = this.won(U), q = u.q;
    const st = [{key: 'idea', title: 'The idea', done: !!u.l}];
    if (U.along.length) st.push({key: 'along', title: 'Play along', n: U.along.filter(l => a[l.id]).length, of: U.along.length, done: U.along.every(l => a[l.id])});
    st.push({key: 'prac', title: 'Win them', n: Math.min(won, U.need), of: U.need, done: won >= U.need});
    st.push({key: 'cp', title: 'Checkpoint', best: q ? q[0] : undefined, of: U.check.length, done: !!q && q[0] >= this.need(U.check.length)});
    return st;
  },
  // the endings of a unit's kinds won without a slip, each position once
  won(U){ const p = this.rd().p; return EGD.items.filter(it => U.kinds.includes(it.k) && p[it.id] && p[it.id][1] > 0).length; },
  passed(U){ return this.steps(U).every(s => s.done); },
  mineU(){ return PERSONA === 'house' ? EGD.units.filter(U => !U.lib) : []; },
  libU(){ return EGD.units.filter(U => U.lib); },
  listOf(U){ return U.lib ? this.libU() : this.mineU(); },
  // the unit up next: the first of the player's own not passed, then the first of the basics
  cur(){ return this.mineU().find(U => !this.passed(U)) || this.libU().find(U => !this.passed(U)) || null; },
  // the one thing that leads on in a unit
  unitNext(U){
    const s = this.steps(U).find(x => !x.done); if (!s) return null;
    const a = (this.rd().u[U.id] || {}).a || {};
    if (s.key === 'idea') return {cta: 'See the idea', go: () => this.openUnit(U.id)};
    if (s.key === 'along'){ const k = U.along.findIndex(l => !a[l.id]); return {cta: 'Play along', go: () => this.along(U.id, k)}; }
    if (s.key === 'prac') return {cta: 'Win an ending', go: () => { const it = this.next(U.id); if (it) this.start(it.id, {unit: U.id}); }};
    return {cta: 'Take the checkpoint', go: () => this.quiz(U.id)};
  },
  openUnit(id){ const U = this.unit(id); if (!U || (!U.lib && PERSONA !== 'house')){ S.cseg = 'end'; return go('course'); }
    S.egUnit = id; S.egSlide = 0; S.drill = S.egState = null; S.view = 'egunit'; render(); setHash(); window.scrollTo({top: 0, behavior: reduced ? 'auto' : 'smooth'}); },
  slideBoard(s, mini){ return boardSVG(s.fen.split(' ')[0], {coords: !mini, mini, flip: s.me === 'b', arrows: (s.arrows || []).slice(), circles: (s.circles || []).slice(), aria: s.h}); },
  seg(){ return segHTML([['open', 'Openings'], ['end', 'Endings']], S.cseg === 'end' ? 'end' : 'open', 'cseg'); },
  wireSeg(){ view.querySelectorAll('[data-cseg]').forEach(b => b.onclick = () => { S.cseg = b.dataset.cseg; S.deep = null; render(); setHash(); }); },
  renderCourse(){
    const own = this.mineU(), lib = this.libU(), cur = this.cur(), units = own.length ? own : lib, passedN = units.filter(U => this.passed(U)).length;
    const bar = units.map(U => `<i class="${this.passed(U) ? 'on' : ''}" title="${esc(U.title)}"></i>`).join('');
    let hero;
    if (cur){
      const st = this.steps(cur), nx = st.find(s => !s.done), act = this.unitNext(cur), list = this.listOf(cur);
      hero = `<section class="chero"><div class="board">${this.slideBoard(cur.slides[0], true)}</div><div><div class="chips"><span class="chip">Up next · ${cur.lib && own.length ? 'The basics · ' : ''}Unit ${list.indexOf(cur) + 1} of ${list.length}</span></div>
        <h3>${esc(cur.title)}</h3><p class="egwhy">${esc(cur.why)}</p>
        <ol class="ministeps" aria-label="Steps in this unit">${st.map(s => `<li class="${s.done ? 'done' : s === nx ? 'next' : ''}">${s.done ? ICON.check : ''}${esc(s.title)}</li>`).join('')}</ol>
        <div class="cta"><button class="btn primary" id="egGo">${esc(act ? act.cta : 'Open the unit')}</button></div></div></section>`;
    } else hero = `<section class="chero done"><div><h3>Every endings unit passed</h3><div class="cta"><button class="btn primary" data-go="endings">Play more endings</button></div></div></section>`;
    const row = (U, k) => { const pass = this.passed(U), st = this.steps(U), done = st.filter(s => s.done).length, isCur = U === cur;
      return `<li class="urow"><div class="rail">${pass ? `<span class="ubub pass" title="Passed">${ICON.check}</span>` : `<span class="ubub ${isCur ? 'cur' : ''}">${k + 1}</span>`}</div>
        <button class="ucard ${isCur ? 'cur' : ''}" data-egunit="${U.id}" aria-label="${esc(`Unit ${k + 1}: ${U.title}${pass ? ', passed' : ''}`)}"><div class="thumb">${this.slideBoard(U.slides[0], true)}</div>
          <span class="ut"><b>${esc(U.title)}</b><span class="egwhy">${esc(U.why)}</span></span><span class="ust"><span class="pips" aria-label="${done} of ${st.length} steps">${st.map(s => `<i class="${s.done ? 'on' : ''}"></i>`).join('')}</span></span></button></li>`; };
    const libN = lib.filter(U => this.passed(U)).length;
    view.innerHTML = `${this.seg()}<div class="chead solo"><div class="cmeter"><div class="bar" aria-hidden="true">${bar}</div><span>${passedN} of ${units.length} units passed</span></div></div>
      ${hero}<ol class="path" aria-label="${own.length ? 'Endings units' : 'The basics'}">${units.map(row).join('')}</ol>
      ${own.length && lib.length ? `<div class="eglib"><h3>The basics</h3><span class="tnum">${libN} of ${lib.length} passed</span></div><ol class="path" aria-label="The basics">${lib.map(row).join('')}</ol>` : ''}`;
    this.wireSeg();
    const g = document.getElementById('egGo'); if (g) g.onclick = () => { const m = this.unitNext(cur); if (m) m.go(); else this.openUnit(cur.id); };
    view.querySelectorAll('[data-egunit]').forEach(b => b.onclick = () => this.openUnit(b.dataset.egunit));
    view.querySelectorAll('[data-go]').forEach(b => b.onclick = () => go(b.dataset.go));
  },
  renderUnit(){
    const U = this.unit(S.egUnit); if (!U || (!U.lib && PERSONA !== 'house')){ S.view = 'course'; S.cseg = 'end'; return render(); }
    const list = this.listOf(U), k = list.indexOf(U), n = U.slides.length; S.egSlide = Math.max(0, Math.min(S.egSlide || 0, n - 1));
    if (S.egSlide === n - 1 && !(this.rd().u[U.id] || {}).l){ this.up(U.id).l = Date.now(); Prog.save(); }
    // (the unit's next action is `act`: a local `go` would hide the global one, and ← Course calls that)
    const s = U.slides[S.egSlide], u = this.rd().u[U.id] || {}, a = u.a || {}, st = this.steps(U), nx = st.find(x => !x.done), act = this.unitNext(U);
    const idea = `<div class="idea"><div class="board" id="ideaBoard">${this.slideBoard(s)}</div>
      <div class="ideacap"><p class="kicker">The idea · ${S.egSlide + 1} of ${n}</p><h3>${esc(s.h)}</h3>${bullets(s.t)}
        <div class="ideanav"><button class="ctl" id="iPrev" aria-label="Previous picture" ${S.egSlide === 0 ? 'disabled' : ''}>${ICON.prev}</button>
          <span class="dots" aria-hidden="true">${U.slides.map((_, j) => `<i class="${j === S.egSlide ? 'cur' : (u.l || j < S.egSlide) ? 'on' : ''}"></i>`).join('')}</span>
          <button class="ctl" id="iNext" aria-label="Next picture" ${S.egSlide >= n - 1 ? 'disabled' : ''}>${ICON.next}</button></div></div></div>`;
    const head = (t, cnt) => `<h3>${esc(t)}${cnt ? ` <span class="cnt">${cnt}</span>` : ''}</h3>`;
    const step = (x, j) => {
      const prim = x === nx ? 'primary' : '';
      let body;
      if (x.key === 'idea') body = head('The idea');
      else if (x.key === 'along') body = head('Play along', `${x.n}/${x.of}`) + `<div class="sx"><div class="lrows">${U.along.map((l, i) => `<button class="lrow" data-egalong="${i}"><div class="thumb">${boardSVG(l.fen.split(' ')[0], {mini: true, flip: l.me === 'b'})}</div><span><b>${esc(U.title)}${U.along.length > 1 ? ' · ' + (i + 1) : ''}</b></span><span class="tick ${a[l.id] ? '' : 'no'}">${a[l.id] ? ICON.check + 'Played' : ''}</span></button>`).join('')}</div></div>`;
      else if (x.key === 'prac') body = head('Win them', `${x.n}/${x.of}`) + `<p class="sp">Without a slip</p><div class="sx"><div class="lesson-actions"><button class="btn ${prim}" data-egstep="prac">Win an ending</button></div></div>`;
      else body = head('Checkpoint', x.best !== undefined ? `${x.best}/${x.of}` : '') + `<p class="sp">${this.need(x.of)} of ${x.of} to pass</p><div class="sx"><div class="lesson-actions"><button class="btn ${prim}" data-egstep="cp">${x.done ? 'Take it again' : 'Take the checkpoint'}</button></div></div>`;
      return `<li class="step ${x.done ? 'done' : ''} ${x === nx ? 'next' : ''}"><span class="sn">${x.done ? ICON.check : j + 1}</span><div>${body}</div></li>`;
    };
    const prev = list[k - 1], next = list[k + 1];
    view.innerHTML = `<div class="crumbs"><button class="btn small" id="egBack">← Course</button><span class="where">${U.lib && this.mineU().length ? 'The basics · ' : ''}Unit ${k + 1} of ${list.length}</span><span class="spacer"></span>
        ${prev ? `<button class="btn small" data-egunit="${prev.id}" aria-label="Previous unit">‹<span class="navtxt"> Unit ${k}</span></button>` : ''}${next ? `<button class="btn small" data-egunit="${next.id}" aria-label="Next unit"><span class="navtxt">Unit ${k + 2} </span>›</button>` : ''}</div>
      <div class="ugrid"><div class="bcol">${idea}</div><div class="ucol"><header class="uhead">${this.passed(U) ? '<div class="chips"><span class="chip good">Passed</span></div>' : ''}<h2>${esc(U.title)}</h2><p class="egwhy">${esc(U.why)}</p>
        ${nx ? `<div class="cta" style="margin-top:14px"><button class="btn primary" id="uGo">${nx.key === 'idea' ? 'Next picture' : esc(act.cta)}</button></div>` : ''}</header>
        <ol class="steps">${st.map(step).join('')}</ol></div></div>`;
    const slide = d => { S.egSlide = Math.max(0, Math.min(n - 1, S.egSlide + d)); this.renderUnit(); };
    document.getElementById('iPrev').onclick = () => slide(-1);
    document.getElementById('iNext').onclick = () => slide(1);
    document.getElementById('egBack').onclick = () => { S.cseg = 'end'; go('course'); };
    const g = document.getElementById('uGo'); if (g) g.onclick = () => { const x = this.steps(U).find(y => !y.done); if (x && x.key === 'idea') return slide(1); const m = this.unitNext(U); if (m) m.go(); };
    view.querySelectorAll('[data-egunit]').forEach(b => b.onclick = () => this.openUnit(b.dataset.egunit));
    view.querySelectorAll('[data-egalong]').forEach(b => b.onclick = () => this.along(U.id, +b.dataset.egalong));
    view.querySelectorAll('[data-egstep]').forEach(b => b.onclick = () => { if (b.dataset.egstep === 'cp') return this.quiz(U.id); const it = this.next(U.id); if (it) this.start(it.id, {unit: U.id}); });
  },

  // ---- the Endings tab: pick the kinds, start, play; the course's games and checkpoints play on the same page
  // the card above the kinds: what the next ending is, with its idea to look at first; or the idea, picture by picture
  topHTML(it){
    const K = this.kind(it.k), I = S.egIdea && S.egIdea.k === K.id && K.idea ? K.idea : null;
    if (I){
      const i = S.egIdea.i = Math.max(0, Math.min(S.egIdea.i || 0, I.length - 1)), sl = I[i];
      return `<div class="dpanel egtop"><p class="kicker">${esc(K.name)} · The idea</p><h3>${esc(sl.h)}</h3>${bullets(sl.t)}
        ${I.length > 1 ? `<div class="ideanav"><button class="ctl" id="eiPrev" aria-label="Previous picture" ${i === 0 ? 'disabled' : ''}>${ICON.prev}</button><span class="dots" aria-hidden="true">${I.map((_, j) => `<i class="${j === i ? 'cur' : j < i ? 'on' : ''}"></i>`).join('')}</span><button class="ctl" id="eiNext" aria-label="Next picture" ${i >= I.length - 1 ? 'disabled' : ''}>${ICON.next}</button></div>` : ''}
        <div class="lesson-actions"><button class="btn primary" id="egStart">Start</button><button class="btn" id="eiBack">Back</button></div></div>`;
    }
    const who = it.src ? 'vs ' + it.src.split(' ').slice(1).join(' ') : K.name;
    return `<div class="dpanel egtop"><p class="kicker">${esc(K.group)} · ${esc(who)}</p><h3>${esc(this.goalOf(K, it))}</h3>
      <div class="lesson-actions"><button class="btn primary" id="egStart">Start</button>${this.canShow(it) ? '<button class="btn" id="egShowTop">Show me how</button>' : ''}${K.idea ? '<button class="btn" id="egIdea">The idea</button>' : ''}</div></div>`;
  },
  sideHTML(){
    const D = S.drill; if (D && D.state === 'play') return '';
    const pick = this.chosen(), kinds = this.kindsOn(), groups = [...new Set(kinds.map(k => k.group))], p = this.rd().p, open = S.egOpen || (S.egOpen = new Set());
    const chip = (K, label) => `<button data-egk="${K.id}" aria-pressed="${!!pick && pick.includes(K.id)}" ${this.canPlay(K) ? '' : 'disabled'}>${esc(label || K.name)}</button>`;
    const played = Object.values(p).reduce((a, r) => a + r[0], 0), clean = Object.values(p).reduce((a, r) => a + r[1], 0), stars = Object.values(p).reduce((a, r) => a + (r[3] || 0), 0);
    // a group of one is a single chip; the others fold, with the number picked beside the name
    const grp = g => { const ks = kinds.filter(k => k.group === g), n = pick ? ks.filter(k => pick.includes(k.id)).length : 0;
      if (ks.length === 1) return `<div class="seg egone">${chip(ks[0], g)}</div>`;
      return `<details class="egg" data-eggrp="${esc(g)}" ${open.has(g) ? 'open' : ''}><summary><b>${esc(g)}</b><span class="egn tnum">${n ? `${n} of ${ks.length}` : ks.length}</span></summary>
        <div class="seg"><button class="sbcol" data-egg="${esc(g)}" aria-pressed="${n === ks.length}">All ${esc(lc(g))}</button>${ks.map(K => chip(K)).join('')}</div></details>`; };
    return `<div class="dpanel">
      <div class="eggroups"><div class="seg"><button data-egk="all" aria-pressed="${!pick}">Everything</button></div>
        ${groups.map(grp).join('')}</div>
      <div class="eglv"><span>Rated about <b class="tnum">${this.level()}</b></span><div class="seg"><button data-eglv="-1" ${(+SET.egl || 0) <= -3 ? 'disabled' : ''}>Easier</button><button data-eglv="1" ${(+SET.egl || 0) >= 3 ? 'disabled' : ''}>Harder</button></div></div>
      ${Engine.state === 'failed' ? `<p class="lockednote">${Engine.why === 'file' ? 'Most endings need the engine, and the engine needs the page opened from the web.' : 'The engine couldn\'t start here, so only the endings it isn\'t needed for are on.'}</p>` : ''}
      <div class="queue"><div><b class="tnum">${played}</b><span>played</span></div><div><b class="tnum">${clean}</b><span>clean</span></div><div><b class="tnum">${stars}</b><span>stars</span></div></div>
    </div>`;
  },
  wireSide(){
    view.querySelectorAll('[data-egk]').forEach(b => b.onclick = () => { const id = b.dataset.egk;
      this.peek = null;
      if (id === 'all') this.pick = null;
      else { const p = new Set(this.pick || []); p.has(id) ? p.delete(id) : p.add(id); this.pick = p.size ? [...p] : null; }
      S.egIdea = null; this.savePick(); this.render(); });
    view.querySelectorAll('[data-eglv]').forEach(b => b.onclick = () => { setSetting('egl', Math.max(-3, Math.min(3, (+SET.egl || 0) + +b.dataset.eglv))); this.peek = null; S.egIdea = null; this.render(); });
    view.querySelectorAll('[data-egg]').forEach(b => b.onclick = () => { const ks = this.kindsOn().filter(k => k.group === b.dataset.egg).map(k => k.id), p = new Set(this.pick || []);
      const all = ks.every(k => p.has(k)); ks.forEach(k => all ? p.delete(k) : p.add(k)); this.pick = p.size ? [...p] : null; this.peek = null; S.egIdea = null; this.savePick(); this.render(); });
    view.querySelectorAll('details.egg').forEach(d => d.ontoggle = () => { const g = d.dataset.eggrp; d.open ? S.egOpen.add(g) : S.egOpen.delete(g); });
  },
  render(){
    if (!egOn()){ S.view = 'course'; return render(); }
    EGTB.load();
    const D = S.drill, U = D && D.unit && this.unit(D.unit);
    const crumbs = U ? `<div class="crumbs"><button class="btn small" data-egunit="${U.id}">← ${esc(U.title)}</button></div>` : D ? '<div class="crumbs"><button class="btn small" id="egHome">← Endings</button></div>' : '';
    const pool = this.pool();
    if (!D && (!this.peek || !pool.includes(this.peek))){ this.peek = this.next() || EGD.items[0]; S.egIdea = null; }
    const prev = !D && this.peek, K0 = prev && this.kind(prev.k), I = prev && S.egIdea && K0.idea ? K0.idea[S.egIdea.i || 0] : null;
    // before a game the board shows the next ending, or a picture of its idea
    const shown = I ? this.slideBoard(I) : prev ? boardSVG(prev.fen.split(' ')[0], {coords: true, flip: prev.me === 'b'}) : '';
    view.innerHTML = `${crumbs}<div class="sgrid">
      <div class="bcol"><div class="mat top"></div><div class="board ${D && (D.state === 'play' || drillOver(D)) ? 'input' : ''} ${D && D.guided ? 'guided' : ''}" id="db">${D ? '' : shown}</div><div class="mat bot"></div>
        <p class="evaltext" id="deval" ${drillOver(D) ? '' : 'hidden'}>Engine: thinking…</p></div>
      <div class="ccol"><div id="dpanel">${D ? this.panelHTML(D) : this.topHTML(prev)}</div>
        <div id="egside">${U ? '' : this.sideHTML()}</div></div></div>`;
    if (D) renderDrillBoard(); else { const el = document.getElementById('db'); matUpdate(el, I ? I.fen : prev.fen, I ? I.me === 'b' : prev.me === 'b', true); }
    wireBoardInput(); this.wirePanel(); this.wireSide();
    const st = document.getElementById('egStart'); if (st) st.onclick = () => { const it = this.peek || this.next(); this.peek = null; S.egIdea = null; if (it) this.start(it.id); };
    const ib = id => document.getElementById(id);
    if (ib('egIdea')) ib('egIdea').onclick = () => { S.egIdea = {k: prev.k, i: 0}; this.render(); };
    if (ib('egShowTop')) ib('egShowTop').onclick = () => { const it = this.peek; this.peek = null; S.egIdea = null; if (it) this.show(it.id); };
    if (ib('eiBack')) ib('eiBack').onclick = () => { S.egIdea = null; this.render(); };
    if (ib('eiPrev')) ib('eiPrev').onclick = () => { S.egIdea.i--; this.render(); };
    if (ib('eiNext')) ib('eiNext').onclick = () => { S.egIdea.i++; this.render(); };
    const h = document.getElementById('egHome'); if (h) h.onclick = () => { S.drill = S.egState = null; this.render(); };
    view.querySelectorAll('.crumbs [data-egunit]').forEach(b => b.onclick = () => this.openUnit(b.dataset.egunit));
  },
  xp(d){
    const e = d.end; if (!e) return 0; let x = 0;
    for (const r of Object.values(e.p || {})) x += (r[1] || 0) * XP.clean + Math.max(0, (r[0] || 0) - (r[1] || 0)) * XP.slip;
    for (const id in (e.u || {})){ const u = e.u[id]; if (u.l) x += XP.lesson; for (const k in (u.a || {})) x += XP.lesson;
      const U = this.unit(id); if (U && u.q && u.q[0] >= this.need(U.check.length)) x += XP.pass; }
    return x;
  }
};
// points from the endings, for Level.xp (a function, so the template can call it before this file's objects exist)
function egXP(d){ return EGD ? EG.xp(d) : 0; }
// the endings' part of the progress record, merged from two copies: o is the copy being written, r the other one
function egMerge(o, r){
  if (!r.end) return;
  const a = o.end || (o.end = {}), b = r.end;
  a.p = a.p || {}; for (const id in (b.p || {})){ const x = a.p[id] || [0, 0, 0, 0], y = b.p[id]; a.p[id] = x.map((v, k) => Math.max(v || 0, y[k] || 0)); }
  a.u = a.u || {};
  for (const id in (b.u || {})){
    const x = a.u[id] || (a.u[id] = {}), y = b.u[id];
    if (y.l) x.l = x.l ? Math.min(x.l, y.l) : y.l;
    if (y.a){ x.a = x.a || {}; for (const k in y.a) x.a[k] = x.a[k] ? Math.min(x.a[k], y.a[k]) : y.a[k]; }
    if (y.q && (!x.q || y.q[0] > x.q[0] || (y.q[0] === x.q[0] && y.q[2] < x.q[2]))) x.q = y.q.slice();
  }
  if (b.n){ a.n = a.n || [0, 0]; a.n = a.n.map((v, k) => Math.max(v || 0, b.n[k] || 0)); }
}
