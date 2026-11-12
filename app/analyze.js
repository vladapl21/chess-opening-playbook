/* Game analysis for a personal playbook. Plain rules and counting, no model and no engine.
   In:  PGN text (or parsed games), the player's name, both books.
   Out: a profile (ratings, what they play, where they score, where they leave the book) and a compact game list.
   Needs chess.js (`Chess`) for replaying moves. Runs in the page and under Node (tests/analyze_check.js). */
const Analyze = (() => {
  const pct = (a, b) => b ? Math.round(100 * a / b) : 0;
  const tally = () => ({n: 0, w: 0, l: 0, d: 0});
  const add = (t, r) => { t.n++; if (r === 1) t.w++; else if (r === 0) t.l++; else t.d++; return t; };
  const score = t => t.n ? (t.w + t.d / 2) / t.n : 0;

  /* ---- PGN: headers and the main line's moves; comments, clocks, side lines and annotations are dropped */
  function parsePGN(text){
    const games = []; let h = null, body = [];
    const flush = () => { if (h && (body.length || h.Result)){ games.push({h, moves: movesOf(body.join(' '))}); } h = null; body = []; };
    for (const raw of String(text || '').replace(/\r/g, '').split('\n')){
      const line = raw.trim(), m = line.match(/^\[(\w+)\s+"(.*)"\]$/);
      if (m){ if (body.length) flush(); (h = h || {})[m[1]] = m[2].replace(/\\"/g, '"'); }
      else if (line){ if (!h) h = {}; body.push(line); }
    }
    flush(); return games;
  }
  function movesOf(s){
    s = s.replace(/\{[^}]*\}/g, ' ').replace(/;[^\n]*/g, ' ');
    for (let k = 0; k < 6 && /\([^()]*\)/.test(s); k++) s = s.replace(/\([^()]*\)/g, ' ');
    return s.replace(/\$\d+/g, ' ').replace(/\d+\.(\.\.)?/g, ' ').split(/\s+/)
      .filter(t => t && !/^(1-0|0-1|1\/2-1\/2|\*)$/.test(t)).map(t => t.replace(/[!?]+$/, ''));
  }
  // the name that appears in the most games is the player
  function guessUser(games){
    const c = {}; for (const g of games) for (const k of ['White', 'Black']){ const n = (g.h[k] || '').toLowerCase(); if (n) c[n] = (c[n] || 0) + 1; }
    const top = Object.entries(c).sort((a, b) => b[1] - a[1]);
    return top.length && top[0][1] >= Math.max(2, games.length * 0.6) ? top[0][0] : '';
  }
  function timeClass(tc){
    if (!tc || tc === '-') return 'other';
    if (tc.includes('/')) return 'daily';
    const [b, inc] = tc.split('+').map(Number), t = (b || 0) + 40 * (inc || 0);
    return t < 180 ? 'bullet' : t < 480 ? 'blitz' : t < 1500 ? 'rapid' : 'classical';
  }
  const stamp = h => { const d = (h.UTCDate || h.Date || '').replace(/\./g, '-'), t = h.UTCTime || h.StartTime || '00:00:00'; const v = Date.parse(`${d}T${t}Z`); return isNaN(v) ? 0 : v; };

  /* ---- what the player chose, named in plain words. Each entry: [slot, key, name, test on the move list] */
  const S = (g, ...mv) => mv.every((m, i) => m === null || g[i] === m);
  const has = (g, color, san, upto = 12) => { for (let i = color === 'w' ? 0 : 1; i < Math.min(g.length, upto); i += 2) if (g[i] === san) return true; return false; };
  const NAMES = {
    white: [
      ['e4', 'The e-pawn', g => g[0] === 'e4'], ['d4', 'The d-pawn', g => g[0] === 'd4'],
      ['c4', 'The c-pawn (English)', g => g[0] === 'c4'], ['nf3', 'The king\'s knight first', g => g[0] === 'Nf3'], ['other', 'Something else', () => true]],
    whiteE4: [ // against 1…e5
      ['italian', 'Italian bishop', g => S(g, 'e4', 'e5', 'Nf3') && g[4] === 'Bc4'], ['ruy', 'Spanish bishop (Ruy Lopez)', g => S(g, 'e4', 'e5', 'Nf3') && g[4] === 'Bb5'],
      ['scotch', 'Scotch (early d-pawn)', g => S(g, 'e4', 'e5', 'Nf3') && g[4] === 'd4'], ['vienna', 'Vienna (queen\'s knight first)', g => S(g, 'e4', 'e5', 'Nc3')],
      ['kg', 'King\'s Gambit', g => S(g, 'e4', 'e5', 'f4')], ['bishop', 'Bishop first', g => S(g, 'e4', 'e5', 'Bc4')], ['other', 'Something else', g => S(g, 'e4', 'e5')]],
    whiteD4: [
      ['london', 'London bishop', g => g[0] === 'd4' && has(g, 'w', 'Bf4', 8) && !has(g, 'w', 'c4', 6)], ['qg', 'Queen\'s Gambit', g => g[0] === 'd4' && has(g, 'w', 'c4', 6)],
      ['other', 'Something else', g => g[0] === 'd4']],
    blackE4: [
      ['e5', 'E-pawn against e-pawn', g => S(g, 'e4', 'e5')], ['sicilian', 'Sicilian', g => S(g, 'e4', 'c5')], ['caro', 'Caro-Kann', g => S(g, 'e4', 'c6')],
      ['french', 'French', g => S(g, 'e4', 'e6')], ['scandi', 'Scandinavian', g => S(g, 'e4', 'd5')], ['pirc', 'Pirc or Modern', g => S(g, 'e4') && (g[1] === 'd6' || g[1] === 'g6')],
      ['other', 'Something else', g => S(g, 'e4')]],
    blackD4: [
      ['slav', 'Slav setup (d-pawn and c-pawn)', g => S(g, 'd4', 'd5') && has(g, 'b', 'c6', 8) && !has(g, 'b', 'e6', 4)],
      ['qgd', 'Queen\'s Gambit Declined (d-pawn and e-pawn)', g => S(g, 'd4', 'd5') && has(g, 'b', 'e6', 6)],
      ['kid', 'King\'s Indian or Grünfeld (fianchetto)', g => S(g, 'd4', 'Nf6') && has(g, 'b', 'g6', 6)], ['nimzo', 'Knight and e-pawn (Nimzo or Queen\'s Indian)', g => S(g, 'd4', 'Nf6') && has(g, 'b', 'e6', 6)],
      ['dutch', 'Dutch (f-pawn)', g => S(g, 'd4', 'f5')], ['d5', 'D-pawn against d-pawn', g => S(g, 'd4', 'd5')], ['other', 'Something else', g => S(g, 'd4')]]
  };
  const nameIn = (slot, sans) => { for (const [key, name, test] of NAMES[slot]) if (test(sans)) return {key, name}; return null; };

  /* ---- the books: which chapter a position belongs to */
  function indexBook(D){
    if (D._chOf) return D._chOf;
    const partCh = {}; for (const p of D.parts) partCh[p.id] = p.ch;
    const lesCh = {}; for (const l of D.lessons) lesCh[l.id] = partCh[l.part];
    const chOf = {}, lesOf = {};
    for (const ln of D.lines){ const ch = lesCh[ln.lesson]; if (!ch) continue; for (const i of ln.n){ if (!(i in chOf)){ chOf[i] = ch; lesOf[i] = ln.id; } } }
    // a position shared by several chapters (the first moves) belongs to none of them yet
    const cnt = {}; for (const ln of D.lines){ const ch = lesCh[ln.lesson]; if (!ch) continue; for (const i of ln.n){ (cnt[i] = cnt[i] || new Set()).add(ch); } }
    for (const i in cnt) if (cnt[i].size > 1) delete chOf[i];
    Object.defineProperty(D, '_chOf', {value: chOf, enumerable: false}); Object.defineProperty(D, '_lineOf', {value: lesOf, enumerable: false});
    return chOf;
  }
  // Follow a game through a book: how far it stays in, who left first and with what.
  // After the player leaves, the walk goes on as a shadow (the book's move for them, the opponent's real moves) for as long
  // as the opponent stays in the book, because the chapter is decided by what the opponent set up, not by the player's slip.
  function walk(D, ucis, me){
    const N = D.nodes, chOf = indexBook(D), isMine = ply => (ply % 2 === 0) === (me === 'w');
    const bookKid = n => (N[n].k || []).find(c => !!N[c].w === (me === 'w') && !(N[c].g || []).includes('warn'));
    let node = 0, ply = 0, ch = null, out = null;
    for (; ply < ucis.length; ply++){
      const k = (N[node].k || []).find(c => N[c].u === ucis[ply]);
      if (k !== undefined && !(isMine(ply) && (N[k].g || []).includes('warn'))){ node = k; if (chOf[node]) ch = chOf[node]; continue; }
      out = {ply, node, by: isMine(ply) ? 'me' : 'opp', uci: ucis[ply], warned: k !== undefined};
      break;
    }
    if (!out) return {ply, node, ch, by: null};
    if (out.by === 'me'){
      let n = bookKid(node);
      for (let q = ply + 1; n !== undefined && q < ucis.length; q++){
        if (chOf[n]) ch = chOf[n];
        n = isMine(q) ? bookKid(n) : (N[n].k || []).find(c => N[c].u === ucis[q]);
      }
      if (n !== undefined && chOf[n]) ch = chOf[n];
      out.hasBook = bookKid(node) !== undefined;
    }
    out.ch = ch; return out;
  }

  /* ---- one game: replay it and note the plain facts */
  function replay(g, user){
    const h = g.h, me = (h.White || '').toLowerCase() === user ? 'w' : (h.Black || '').toLowerCase() === user ? 'b' : null;
    if (!me) return null;
    if (h.Variant && !/standard|from position/i.test(h.Variant)) return null;
    if (h.SetUp === '1' || h.FEN) return null;
    const res = h.Result === '1-0' ? (me === 'w' ? 1 : 0) : h.Result === '0-1' ? (me === 'b' ? 1 : 0) : h.Result === '1/2-1/2' ? 0.5 : null;
    if (res === null || g.moves.length < 6) return null;
    const c = new Chess(), ucis = [], sans = []; let castle = {w: null, b: null}, qGone = 0, qOffPly = null, open = null;
    for (const san of g.moves){
      const m = c.move(san, {sloppy: true}); if (!m) break;
      ucis.push(m.from + m.to + (m.promotion || '')); sans.push(m.san.replace(/[+#]/g, ''));
      if (m.flags.includes('k')) castle[m.color] = 'K'; else if (m.flags.includes('q')) castle[m.color] = 'Q';
      if (m.captured === 'q' && ++qGone === 2 && qOffPly === null) qOffPly = ucis.length;
      if (ucis.length === 24){ let p = 0; for (const row of c.board()) for (const f of [3, 4]) if (row[f] && row[f].type === 'p') p++; open = p <= 2; }
    }
    if (ucis.length < 6) return null;
    const term = (h.Termination || '').toLowerCase();
    return {me, res, ucis, sans, plies: ucis.length, t: stamp(h), tc: timeClass(h.TimeControl),
      opp: me === 'w' ? h.Black : h.White, elo: +(me === 'w' ? h.WhiteElo : h.BlackElo) || 0, oppElo: +(me === 'w' ? h.BlackElo : h.WhiteElo) || 0,
      url: h.Link || (/^https?:/.test(h.Site || '') ? h.Site : ''), castle: castle[me], oppCastle: castle[me === 'w' ? 'b' : 'w'],
      qOff: qOffPly !== null && qOffPly <= 40, open, onTime: /time/.test(term) && res !== 0.5};
  }

  /* ---- the whole set */
  async function run(input, user, books, onProgress){
    const raw = typeof input === 'string' ? parsePGN(input) : input;
    user = (user || guessUser(raw) || '').toLowerCase();
    const tick = () => new Promise(r => setTimeout(r, 0)), games = [];
    for (let i = 0; i < raw.length; i++){
      const g = replay(raw[i], user); if (g) games.push(g);
      if (i % 8 === 7){ if (onProgress) onProgress({stage: 'read', done: i + 1, of: raw.length, last: g}); await tick(); }
    }
    games.sort((a, b) => b.t - a.t);
    if (onProgress) onProgress({stage: 'read', done: raw.length, of: raw.length});
    return profile(games, user, books);
  }

  function profile(games, user, books){
    const P = {v: 1, user, n: games.length, made: Date.now(), all: tally(), white: {all: tally(), first: {}, systems: {}, off: 0}, black: {all: tally(), vs: {}, systems: {}, off: 0},
      slots: {}, buckets: {}, leaks: [], warned: [], games: []};
    // rating: the time control played most, its latest and best rating
    const byTc = {}; for (const g of games) (byTc[g.tc] = byTc[g.tc] || []).push(g);
    const main = Object.keys(byTc).sort((a, b) => byTc[b].length - byTc[a].length)[0] || 'other', mg = (byTc[main] || []).filter(g => g.elo);
    P.tc = main; P.rating = mg.length ? mg[0].elo : 0; P.peak = mg.reduce((m, g) => Math.max(m, g.elo), 0);
    P.oppAvg = Math.round(games.filter(g => g.oppElo).reduce((s, g) => s + g.oppElo, 0) / Math.max(1, games.filter(g => g.oppElo).length));
    P.from = games.length ? games[games.length - 1].t : 0; P.to = games.length ? games[0].t : 0;
    const slot = (name, key, label, r) => { const s = P.slots[name] = P.slots[name] || {n: 0, opts: {}}; s.n++; add(s.opts[key] = s.opts[key] || Object.assign(tally(), {name: label}), r); };
    const bucket = (name, key, r) => add((P.buckets[name] = P.buckets[name] || {})[key] = (P.buckets[name] || {})[key] || tally(), r);
    const leak = {}, warn = {};
    games.forEach((g, gi) => {
      const side = g.me === 'w' ? P.white : P.black, D = books[g.me], r = g.res;
      add(P.all, r); add(side.all, r);
      // what they chose
      if (g.me === 'w'){
        const f = nameIn('white', g.sans); slot('white', f.key, f.name, r); add(side.first[g.sans[0]] = side.first[g.sans[0]] || tally(), r);
        if (g.sans[0] === 'e4' && g.sans[1] === 'e5'){ const o = nameIn('whiteE4', g.sans); slot('whiteE4', o.key, o.name, r); }
        if (g.sans[0] === 'd4'){ const o = nameIn('whiteD4', g.sans); slot('whiteD4', o.key, o.name, r); }
      } else {
        const first = g.sans[0]; add(side.vs[first] = side.vs[first] || tally(), r);
        if (first === 'e4'){ const o = nameIn('blackE4', g.sans); slot('blackE4', o.key, o.name, r); }
        else if (first === 'd4'){ const o = nameIn('blackD4', g.sans); slot('blackD4', o.key, o.name, r); }
      }
      // where it sits in the books
      const w = walk(D, g.ucis, g.me), inBook = !!w.ch;
      // systems: how often each chapter's setup was faced. off: games where the player's own first move was not the playbook's
      if (inBook) add(side.systems[w.ch] = side.systems[w.ch] || Object.assign(tally(), {depth: 0}), r), side.systems[w.ch].depth += w.ply;
      if (!inBook || (w.by === 'me' && w.ply <= 1)) side.off++;
      if (inBook && w.by === 'me' && w.hasBook){
        const k = `${g.me}:${w.node}:${w.uci}`, store = w.warned ? warn : leak;
        const e = store[k] = store[k] || {side: g.me, node: w.node, uci: w.uci, ch: w.ch, n: 0, w: 0, l: 0, d: 0, games: []}; add(e, r); if (e.games.length < 6) e.games.push(gi);
      }
      // the kind of game it became
      bucket('colour', g.me === 'w' ? 'white' : 'black', r);
      bucket('castle', !g.castle ? 'none' : !g.oppCastle ? 'only me' : g.castle === g.oppCastle ? 'same side' : 'opposite sides', r);
      bucket('queens', g.qOff ? 'off early' : 'on', r);
      if (g.open !== null) bucket('centre', g.open ? 'open' : 'closed', r);
      bucket('length', g.plies < 50 ? 'short' : g.plies <= 90 ? 'middle' : 'long', r);
      if (g.oppElo && g.elo) bucket('opponent', g.oppElo - g.elo > 25 ? 'higher rated' : g.elo - g.oppElo > 25 ? 'lower rated' : 'about level', r);
      if (r === 0) bucket('losses', g.onTime ? 'on time' : g.plies < 50 ? 'before move 25' : 'later', 0);
      P.games.push({t: g.t, me: g.me, r, opp: g.opp || '', oe: g.oppElo, e: g.elo, pl: g.plies, ch: inBook ? w.ch : null, bp: w.ply, by: w.by, nd: w.node, u: w.by ? w.uci : '', url: g.url,
        o: g.sans.slice(0, 8).join(' ')});
    });
    for (const s of [P.white, P.black]) for (const k in s.systems){ const t = s.systems[k]; t.depth = Math.round(t.depth / t.n * 10) / 10; }
    const rank = o => Object.values(o).sort((a, b) => b.n - a.n || b.l - a.l);
    P.leaks = rank(leak).slice(0, 24); P.warned = rank(warn).slice(0, 12);
    P.facts = facts(P);
    return P;
  }

  /* ---- sentences the app can say about the player. Each: {k: kind, big, text, d: how strong the contrast is} */
  function facts(P){
    const out = [], LAB = {castle: {'same side': 'both kings castle on the same side', 'opposite sides': 'the kings castle on opposite sides', none: 'you never castle', 'only me': 'only you castle'},
      queens: {'off early': 'the queens come off early', on: 'the queens stay on'}, centre: {open: 'the centre opens up', closed: 'the centre stays closed'},
      length: {short: 'the game is over inside 25 moves', middle: 'the game runs 25 to 45 moves', long: 'the game goes past move 45'},
      opponent: {'higher rated': 'the opponent is rated above you', 'lower rated': 'the opponent is rated below you', 'about level': 'the opponent is rated about level with you'}, colour: {white: 'you have White', black: 'you have Black'}};
    for (const b of ['castle', 'queens', 'centre', 'length', 'colour']){
      const e = Object.entries(P.buckets[b] || {}).filter(([, t]) => t.n >= Math.max(6, P.n * 0.08)); if (e.length < 2) continue;
      e.sort((x, y) => score(y[1]) - score(x[1])); const [hi, lo] = [e[0], e[e.length - 1]], d = score(hi[1]) - score(lo[1]);
      if (d >= 0.08) out.push({k: b, d, big: pct(hi[1].w + hi[1].d / 2, hi[1].n) + '%', hi: hi[0], lo: lo[0],
        text: `You score ${pct(hi[1].w + hi[1].d / 2, hi[1].n)}% when ${LAB[b][hi[0]]} and ${pct(lo[1].w + lo[1].d / 2, lo[1].n)}% when ${LAB[b][lo[0]]}.`});
    }
    const L = P.buckets.losses || {}, ln = Object.values(L).reduce((s, t) => s + t.n, 0);
    if (ln >= 8 && L['on time'] && L['on time'].n / ln >= 0.25) out.push({k: 'clock', d: L['on time'].n / ln / 2, big: pct(L['on time'].n, ln) + '%', text: `${pct(L['on time'].n, ln)}% of your losses are on the clock, not on the board.`});
    if (ln >= 8 && L['before move 25'] && L['before move 25'].n / ln >= 0.3) out.push({k: 'early', d: L['before move 25'].n / ln / 2, big: pct(L['before move 25'].n, ln) + '%', text: `${pct(L['before move 25'].n, ln)}% of your losses are over before move 25. The opening is where your points go.`});
    return out.sort((a, b) => b.d - a.d);
  }

  return {parsePGN, guessUser, run, profile, replay, walk, nameIn, score, pct, timeClass, NAMES};
})();
if (typeof module !== 'undefined') module.exports = Analyze;
