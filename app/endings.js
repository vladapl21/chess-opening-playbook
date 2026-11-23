/* ------------------------------------------------------------------ ENDINGS
   The Endings tab and the endings course (app/endings.js, inlined by assemble.py after product.js). Both are the house
   player's for now (egOn): the course comes from a scan of their games (pipeline/scan_endings.py), and every position,
   line and checkpoint answer is built by pipeline/build_endings.py (EGD). King and queen, king and rook, and king and
   pawn against a lone king are judged by exact tables (EGT, pipeline/endtables.mjs); a lone king against two pieces by
   the rule that only a stalemate or a piece left to be taken throws the win away; everything else by the engine, which
   also plays the other side. Progress is Prog.d.end (merged in mergeProg by egMerge): p, each position played as
   [runs, clean, last time, best stars]; u, each unit: l when its pictures were seen, a the lines played along (time
   each), q the checkpoint's best [score, of, time]. */
const EGD = /*__DATA_E__*/null, EGT = /*__TABLES_E__*/null;
const EG_MATE = 99000;
function egOn(){ return !!EGD && typeof PERSONA !== 'undefined' && PERSONA === 'house'; }
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
  engineKind: K => K.how === 'engine',
  canPlay(K){ return !this.engineKind(K) || Engine.state !== 'failed'; },
  chosen(){ return this.pick && this.pick.length ? this.pick : null; },
  // the positions a game can start from: the kinds picked (or a unit's), each position once
  pool(uid){
    const U = uid && this.unit(uid), ks = U ? U.kinds : this.chosen() || EGD.kinds.map(k => k.id), seen = new Set();
    return EGD.items.filter(it => ks.includes(it.k) && this.canPlay(this.kind(it.k)) && !seen.has(it.fen) && seen.add(it.fen));
  },
  // the next position: one never played first, then the one played longest ago; never the one just played
  next(uid){
    const pool = this.pool(uid).filter(it => it.id !== this.last); if (!pool.length) return this.pool(uid)[0] || null;
    const by = pool.map(it => ({it, r: this.pr(it.id)})).sort((a, b) => (a.r[0] ? 1 : 0) - (b.r[0] ? 1 : 0) || a.r[2] - b.r[2]);
    const top = by.slice(0, Math.min(3, by.length)); return top[Math.floor(Math.random() * top.length)].it;
  },
  fen(D){ return D.kind === 'egq' ? (D.view || D.items[D.k].fen) : D.hist[D.hist.length - 1]; },
  legal(D){ const fen = this.fen(D); return new Chess(fen).moves({verbose: true}).map(egUci); },
  lastU(D){ return D.kind === 'egq' ? D.lastU : D.moves.length ? D.moves[D.moves.length - 1] : null; },
  cap(D){ return D.k.cap || (D.it.par ? D.it.par + 12 : 40); },
  goalText(D){ return {mate: 'Mate them', queen: 'Queen the pawn', hold: 'Hold the draw', win: 'Win it'}[D.k.goal]; },

  // ---- a game against the engine (and Play along, the same board with the green arrow)
  async start(id, o = {}){
    await EGTB.load();
    const it = this.item(id); if (!it) return;
    const K = this.kind(it.k);
    if (K.how !== 'engine' && K.how !== 'bare' && !EGTB.t){ toast('This ending needs a newer browser.'); return; }
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
    S.egState = {kind: 'eg', guided: true, id: L.id, it, k: Object.assign({}, this.kind(U.kinds[0]), {goal: 'along'}), me: L.me, line: L.moves, hist: [L.fen], moves: [],
      keys: [egKey(L.fen)], state: 'play', busy: false, sel: null, flash: null, hint: L.moves[0], msg: '', feed: '', tries: 0, slips: 0, mine: 0, unit: uid, tick: 0};
    S.view = 'endings'; render(); setHash(); window.scrollTo({top: 0, behavior: reduced ? 'auto' : 'smooth'});
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
      if ((goal === 'queen' && queened) || (goal === 'win' && s >= 900)) return cb({ok: true, done: 'won'});
      cb({ok: true, reply: r.pv[0]});
    });
  },
  accept(D, fen1, v, t){
    D.tries = 0; D.mine++;
    if (v.done) return this.finish(D, v.done);
    if (D.k.goal === 'hold' && D.mine >= (D.it.hold || 10)) return this.finish(D, 'held');
    if (D.mine >= this.cap(D)) return this.finish(D, 'slow');
    this.reply(D, fen1, v.reply, t);
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
      drop: `${said}. That throws the win away.`, draw: `${said}. That lets the win go.`, lose: `${said}. That loses.`, mated: `${said}, with mate to follow.`};
    return map[v.why] || '';
  },
  guidedTry(D, u, to){
    const want = D.line[D.moves.length];
    if (u !== want){ D.flash = {sq: to, ok: false}; D.msg = 'Follow the green arrow.'; renderDrillBoard(); renderDrillPanel();
      setTimeout(() => { if (S.drill === D && D.flash && !D.flash.ok){ D.flash = null; D.msg = ''; renderDrillBoard(); renderDrillPanel(); } }, 700); return; }
    const fen0 = this.fen(D), ch = new Chess(fen0); ch.move(uciObj(u)); const fen1 = ch.fen(), t = ++D.tick;
    D.hist.push(fen1); D.moves.push(u); D.keys.push(egKey(fen1)); D.flash = null; D.msg = ''; D.mine++;
    D.said = lc(wordsAt(fen0, u));
    const r = D.line[D.moves.length];
    if (!r){ renderDrillBoard(); return this.finish(D, 'along'); }
    D.busy = true; D.hint = null; renderDrillBoard(); renderDrillPanel();
    this.reply(D, fen1, r, t);
  },
  finish(D, res, last){
    D.state = 'done'; D.busy = false; D.res = res; D.hint = null;
    const won = res === 'won' || res === 'held', par = D.it.par;
    D.stars = !won ? 0 : D.slips ? (D.slips === 1 ? 2 : 1) : par ? (D.mine <= par + 2 ? 3 : D.mine <= par + 6 ? 2 : 1) : 3;
    if (res === 'along'){ const u = this.up(D.unit), a = u.a || (u.a = {}); a[D.id] = Date.now(); Prog.save(); }
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
      const n = D.line.length, mine = Math.ceil(n / 2), done = Math.ceil(D.moves.length / 2);
      const head = `<p class="kicker">Play along</p><h3>${esc(U ? U.title : K.name)}</h3><div class="progressbar" aria-hidden="true"><i style="width:${D.state === 'done' ? 100 : Math.round(done / mine * 100)}%"></i></div>`;
      if (D.state === 'done') return `<div class="dpanel">${head}<div class="donebox"><h4>Played along</h4><div class="lesson-actions">${this.nextBtn(D)}<button class="btn" id="egAgain">Again</button></div><div id="deng"></div></div></div>`;
      const my = !D.busy, said = D.feed ? `<p class="gsaid">${esc(D.feed)}</p>` : '';
      return `<div class="dpanel">${head}<div class="coachnote gcoach" role="status"><div class="cntx">${said}${my && D.hint ? `<p class="gmove">${esc(wordsAt(this.fen(D), D.hint))}</p>` : `<p class="gmove wait">${OPP} is thinking…</p>`}${D.msg ? `<p class="gwarn">${esc(D.msg)}</p>` : ''}</div></div></div>`;
    }
    const par = D.it.par, cnt = K.goal === 'hold' ? `<div class="progressbar" aria-hidden="true"><i style="width:${Math.round(Math.min(1, D.mine / (D.it.hold || 10)) * 100)}%"></i></div><p class="egcount tnum">${D.mine} of ${D.it.hold || 10} moves held</p>`
      : `<p class="egcount tnum">${D.mine} ${D.mine === 1 ? 'move' : 'moves'}${par ? ` · par ${par}` : ''}</p>`;
    const head = `<p class="kicker">${esc(K.name)}${D.it.src ? ' · vs ' + esc(D.it.src.split(' ').slice(1).join(' ')) : U ? ' · ' + esc(U.title) : ''}</p><h3>${this.goalText(D)}</h3>${cnt}`;
    if (D.state === 'done') return `<div class="dpanel">${head}${this.doneBox(D)}</div>`;
    const status = D.busy ? `${OPP} is thinking…` : 'Your move';
    return `<div class="dpanel">${head}<div class="status ${D.busy ? 'wait' : ''} ${D.tries ? 'bad' : ''}"><span class="bub"></span>${status}</div>
      <p class="feedback">${D.msg ? esc(D.msg) : D.feed ? esc(D.feed) : '&nbsp;'}</p></div>`;
  },
  starsHTML(n){ return `<span class="egstars" aria-label="${n} of 3 stars">${[1, 2, 3].map(k => `<svg viewBox="0 0 24 24" class="${k <= n ? 'on' : ''}" aria-hidden="true"><path d="M12 2.8l2.8 5.9 6.4.8-4.7 4.4 1.2 6.4L12 17.2l-5.7 3.1 1.2-6.4L2.8 9.5l6.4-.8z"/></svg>`).join('')}</span>`; },
  doneBox(D){
    const won = D.res === 'won' || D.res === 'held';
    const h = {won: D.k.goal === 'mate' ? `Mate in ${D.mine}` : D.k.goal === 'queen' ? 'Queened' : 'Won', held: 'Held', slow: 'Too slow', lost: 'Mated', drawn: 'A draw'}[D.res];
    const sub = won ? (D.slips ? plural(D.slips, 'slip') : 'Clean') : D.res === 'slow' ? `${D.k.goal === 'mate' ? 'No mate' : 'Not won'} in ${this.cap(D)} moves` : '';
    return `<div class="donebox ${won && !D.slips ? '' : 'bad'}"><h4>${h}</h4>${won ? this.starsHTML(D.stars) : ''}${sub ? `<p class="egsub">${esc(sub)}</p>` : ''}${D.it.why ? `<p class="egsub">In the game: ${esc(lc(D.it.why))}</p>` : ''}
      <div class="lesson-actions">${this.nextBtn(D)}<button class="btn" id="egAgain">Again</button></div><div id="deng"></div></div>`;
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
    if (b('egAgain')) b('egAgain').onclick = () => D.kind === 'egq' ? this.quiz(D.unit) : D.guided ? this.along(D.unit, this.unit(D.unit).along.findIndex(l => l.id === D.id)) : this.start(D.id, {unit: D.unit});
    if (b('egUnitNext')) b('egUnitNext').onclick = () => { const nx = this.unitNext(this.unit(D.unit)); if (nx) nx.go(); };
    if (b('egQNext')) b('egQNext').onclick = () => this.quizNext(D);
    p.querySelectorAll('[data-egunit]').forEach(x => x.onclick = () => this.openUnit(x.dataset.egunit));
  },

  // ---- the checkpoint: one position at a time, one try each
  quiz(uid){
    const U = this.unit(uid); if (!U) return;
    S.egState = {kind: 'egq', unit: uid, items: U.check, k: 0, res: [], state: 'play', sel: null, flash: null, msg: '', view: null, lastU: null, arrows: null, me: U.check[0].me, busy: false, answered: null};
    S.view = 'endings'; render(); setHash(); window.scrollTo({top: 0, behavior: reduced ? 'auto' : 'smooth'});
  },
  need: n => n <= 3 ? n - 1 : Math.ceil(n * .8),
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
      ${D.answered ? `<p class="feedback ${D.answered === 'ok' ? 'good' : 'bad'}">${esc(D.msg)}</p><div class="lesson-actions"><button class="btn primary" id="egQNext">${D.k + 1 < n ? 'Next' : 'See how you did'}</button></div>`
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
  cur(){ return EGD.units.find(U => !this.passed(U)) || null; },
  // the one thing that leads on in a unit
  unitNext(U){
    const s = this.steps(U).find(x => !x.done); if (!s) return null;
    const a = (this.rd().u[U.id] || {}).a || {};
    if (s.key === 'idea') return {cta: 'See the idea', go: () => this.openUnit(U.id)};
    if (s.key === 'along'){ const k = U.along.findIndex(l => !a[l.id]); return {cta: 'Play along', go: () => this.along(U.id, k)}; }
    if (s.key === 'prac') return {cta: 'Win an ending', go: () => { const it = this.next(U.id); if (it) this.start(it.id, {unit: U.id}); }};
    return {cta: 'Take the checkpoint', go: () => this.quiz(U.id)};
  },
  openUnit(id){ S.egUnit = id; S.egSlide = 0; S.drill = S.egState = null; S.view = 'egunit'; render(); setHash(); window.scrollTo({top: 0, behavior: reduced ? 'auto' : 'smooth'}); },
  slideBoard(s, mini){ return boardSVG(s.fen.split(' ')[0], {coords: !mini, mini, flip: s.me === 'b', arrows: (s.arrows || []).slice(), circles: (s.circles || []).slice(), aria: s.h}); },
  seg(){ return segHTML([['open', 'Openings'], ['end', 'Endings']], S.cseg === 'end' ? 'end' : 'open', 'cseg'); },
  wireSeg(){ view.querySelectorAll('[data-cseg]').forEach(b => b.onclick = () => { S.cseg = b.dataset.cseg; S.deep = null; render(); setHash(); }); },
  renderCourse(){
    const units = EGD.units, cur = this.cur(), passedN = units.filter(U => this.passed(U)).length;
    const bar = units.map(U => `<i class="${this.passed(U) ? 'on' : ''}" title="${esc(U.title)}"></i>`).join('');
    let hero;
    if (cur){
      const st = this.steps(cur), nx = st.find(s => !s.done), go = this.unitNext(cur);
      hero = `<section class="chero"><div class="board">${this.slideBoard(cur.slides[0], true)}</div><div><div class="chips"><span class="chip">Up next · Unit ${units.indexOf(cur) + 1} of ${units.length}</span></div>
        <h3>${esc(cur.title)}</h3><p class="egwhy">${esc(cur.why)}</p>
        <ol class="ministeps" aria-label="Steps in this unit">${st.map(s => `<li class="${s.done ? 'done' : s === nx ? 'next' : ''}">${s.done ? ICON.check : ''}${esc(s.title)}</li>`).join('')}</ol>
        <div class="cta"><button class="btn primary" id="egGo">${esc(go ? go.cta : 'Open the unit')}</button></div></div></section>`;
    } else hero = `<section class="chero done"><div><h3>Every endings unit passed</h3><div class="cta"><button class="btn primary" data-go="endings">Play more endings</button></div></div></section>`;
    const row = (U, k) => { const pass = this.passed(U), st = this.steps(U), done = st.filter(s => s.done).length, isCur = U === cur;
      return `<li class="urow"><div class="rail">${pass ? `<span class="ubub pass" title="Passed">${ICON.check}</span>` : `<span class="ubub ${isCur ? 'cur' : ''}">${k + 1}</span>`}</div>
        <button class="ucard ${isCur ? 'cur' : ''}" data-egunit="${U.id}" aria-label="${esc(`Unit ${k + 1}: ${U.title}${pass ? ', passed' : ''}`)}"><div class="thumb">${this.slideBoard(U.slides[0], true)}</div>
          <span class="ut"><b>${esc(U.title)}</b><span class="egwhy">${esc(U.why)}</span></span><span class="ust"><span class="pips" aria-label="${done} of ${st.length} steps">${st.map(s => `<i class="${s.done ? 'on' : ''}"></i>`).join('')}</span></span></button></li>`; };
    view.innerHTML = `${this.seg()}<div class="chead solo"><div class="cmeter"><div class="bar" aria-hidden="true">${bar}</div><span>${passedN} of ${units.length} units passed</span></div></div>
      ${hero}<ol class="path" aria-label="Endings units">${units.map(row).join('')}</ol>`;
    this.wireSeg();
    const g = document.getElementById('egGo'); if (g) g.onclick = () => { const m = this.unitNext(cur); if (m) m.go(); else this.openUnit(cur.id); };
    view.querySelectorAll('[data-egunit]').forEach(b => b.onclick = () => this.openUnit(b.dataset.egunit));
    view.querySelectorAll('[data-go]').forEach(b => b.onclick = () => go(b.dataset.go));
  },
  renderUnit(){
    const U = this.unit(S.egUnit); if (!U){ S.view = 'course'; S.cseg = 'end'; return render(); }
    const k = EGD.units.indexOf(U), n = U.slides.length; S.egSlide = Math.max(0, Math.min(S.egSlide || 0, n - 1));
    if (S.egSlide === n - 1 && !(this.rd().u[U.id] || {}).l){ this.up(U.id).l = Date.now(); Prog.save(); }
    const s = U.slides[S.egSlide], u = this.rd().u[U.id] || {}, a = u.a || {}, st = this.steps(U), nx = st.find(x => !x.done), go = this.unitNext(U);
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
    const prev = EGD.units[k - 1], next = EGD.units[k + 1];
    view.innerHTML = `<div class="crumbs"><button class="btn small" id="egBack">← Course</button><span class="where">Unit ${k + 1} of ${EGD.units.length}</span><span class="spacer"></span>
        ${prev ? `<button class="btn small" data-egunit="${prev.id}" aria-label="Previous unit">‹<span class="navtxt"> Unit ${k}</span></button>` : ''}${next ? `<button class="btn small" data-egunit="${next.id}" aria-label="Next unit"><span class="navtxt">Unit ${k + 2} </span>›</button>` : ''}</div>
      <div class="ugrid"><div class="bcol">${idea}</div><div class="ucol"><header class="uhead">${this.passed(U) ? '<div class="chips"><span class="chip good">Passed</span></div>' : ''}<h2>${esc(U.title)}</h2><p class="egwhy">${esc(U.why)}</p>
        ${nx ? `<div class="cta" style="margin-top:14px"><button class="btn primary" id="uGo">${nx.key === 'idea' ? 'Next picture' : esc(go.cta)}</button></div>` : ''}</header>
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
  sideHTML(){
    const D = S.drill; if (D && D.state === 'play') return '';
    const pick = this.chosen(), groups = [...new Set(EGD.kinds.map(k => k.group))], p = this.rd().p;
    const on = id => !pick || pick.includes(id);
    const chip = K => `<button data-egk="${K.id}" aria-pressed="${!!pick && pick.includes(K.id)}" ${this.canPlay(K) ? '' : 'disabled'}>${esc(K.name)}</button>`;
    const played = Object.values(p).reduce((a, r) => a + r[0], 0), clean = Object.values(p).reduce((a, r) => a + r[1], 0), stars = Object.values(p).reduce((a, r) => a + (r[3] || 0), 0);
    return `<div class="dpanel">
      <div><div class="seg"><button data-egk="all" aria-pressed="${!pick}">Everything</button></div>
        ${groups.map(g => { const ks = EGD.kinds.filter(k => k.group === g); return `<div class="seg sbrow"><button class="sbcol" data-egg="${esc(g)}" aria-pressed="${!!pick && ks.every(k => pick.includes(k.id))}">${esc(g)}</button>${g === 'From your games' ? '' : ks.map(chip).join('')}</div>`; }).join('')}</div>
      ${Engine.state === 'failed' ? `<p class="lockednote">${Engine.why === 'file' ? 'Most endings need the engine, and the engine needs the page opened from the web.' : 'The engine couldn\'t start here, so only the endings it isn\'t needed for are on.'}</p>` : ''}
      <div class="queue"><div><b class="tnum">${played}</b><span>played</span></div><div><b class="tnum">${clean}</b><span>clean</span></div><div><b class="tnum">${stars}</b><span>stars</span></div></div>
    </div>`;
  },
  wireSide(){
    view.querySelectorAll('[data-egk]').forEach(b => b.onclick = () => { const id = b.dataset.egk;
      this.peek = null;
      if (id === 'all') this.pick = null;
      else { const p = new Set(this.pick || []); p.has(id) ? p.delete(id) : p.add(id); this.pick = p.size ? [...p] : null; }
      this.savePick(); this.render(); });
    view.querySelectorAll('[data-egg]').forEach(b => b.onclick = () => { const ks = EGD.kinds.filter(k => k.group === b.dataset.egg).map(k => k.id), p = new Set(this.pick || []);
      const all = ks.every(k => p.has(k)); ks.forEach(k => all ? p.delete(k) : p.add(k)); this.pick = p.size ? [...p] : null; this.peek = null; this.savePick(); this.render(); });
  },
  render(){
    if (!egOn()){ S.view = 'course'; return render(); }
    EGTB.load();
    const D = S.drill, U = D && D.unit && this.unit(D.unit);
    const crumbs = U ? `<div class="crumbs"><button class="btn small" data-egunit="${U.id}">← ${esc(U.title)}</button></div>` : D ? '<div class="crumbs"><button class="btn small" id="egHome">← Endings</button></div>' : '';
    const pool = this.pool();
    if (!D && (!this.peek || !pool.includes(this.peek))) this.peek = this.next() || EGD.items[0];
    const prev = !D && this.peek;
    view.innerHTML = `${crumbs}<div class="sgrid">
      <div class="bcol"><div class="mat top"></div><div class="board ${D && (D.state === 'play' || drillOver(D)) ? 'input' : ''} ${D && D.guided ? 'guided' : ''}" id="db">${D ? '' : boardSVG(prev.fen.split(' ')[0], {coords: true, flip: prev.me === 'b'})}</div><div class="mat bot"></div>
        <p class="evaltext" id="deval" ${drillOver(D) ? '' : 'hidden'}>Engine: thinking…</p></div>
      <div class="ccol"><div id="dpanel">${D ? this.panelHTML(D) : `<div class="dpanel"><div class="lesson-actions"><button class="btn primary" id="egStart">Start an ending</button></div></div>`}</div>
        <div id="egside">${U ? '' : this.sideHTML()}</div></div></div>`;
    if (D) renderDrillBoard(); else { const el = document.getElementById('db'); matUpdate(el, prev.fen, prev.me === 'b', true); }
    wireBoardInput(); this.wirePanel(); this.wireSide();
    const st = document.getElementById('egStart'); if (st) st.onclick = () => { const it = this.peek || this.next(); this.peek = null; if (it) this.start(it.id); };
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
