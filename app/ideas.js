// app/ideas.js: what a move does, in plain words, read off the board.
//   Ideas.of(fen, uci, o)      {facts, lines}: what the move takes, threatens, stops, pins or forks (two lines at most)
//   Ideas.punish(fen, uci, o)  the other side's best answer to a move when that answer wins something, or null:
//                              {u, kind: 'mate' | 'take' | 'fork', gain, lines}
//   Ideas.reply(fen, uci, o)   why an answer that is already known works (the practice sets): lines
// o.me is the player's colour, 'w' or 'b': pieces are "your knight" and "Black's knight" from the player's side.
// o.prev is the move before (uci), o.words(fen, uci) puts a move in words (the page passes moveWords).
//
// No engine. Attack maps, a static exchange count (what each side wins on one square when both keep taking back with
// their cheapest piece, pinned pieces left out) and a short look ahead (every answer, then the best capture). Each line
// is a claim about the board it describes, the way the labels are: a threat is a capture or a mate the side could play
// next if it moved again, "guards" means the moved piece now defends that square, a pin has the king or a bigger piece
// behind it, a fork wins something whatever the other side answers. No squares in the words, except f7 and f2.
const Ideas = (() => {
  const V = {p: 1, n: 3, b: 3, r: 5, q: 9, k: 100}, NAME = {p: 'pawn', n: 'knight', b: 'bishop', r: 'rook', q: 'queen', k: 'king'};
  const KN = [[1, 2], [2, 1], [2, -1], [1, -2], [-1, -2], [-2, -1], [-2, 1], [-1, 2]];
  const KG = [[1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, -1]];
  const DG = [[1, 1], [1, -1], [-1, 1], [-1, -1]], OR = [[1, 0], [-1, 0], [0, 1], [0, -1]];
  const isW = p => p === p.toUpperCase(), low = p => p.toLowerCase(), val = p => V[low(p)];
  const idx = s => (s.charCodeAt(1) - 49) * 8 + (s.charCodeAt(0) - 97), sqn = i => 'abcdefgh'[i % 8] + (1 + (i >> 3));
  const F7 = idx('f7'), F2 = idx('f2'), CENTER = ['d4', 'e4', 'd5', 'e5'].map(idx);
  const HOME = {w: {n: ['b1', 'g1'], b: ['c1', 'f1']}, b: {n: ['b8', 'g8'], b: ['c8', 'f8']}};
  const cap = s => s.charAt(0).toUpperCase() + s.slice(1);
  const times = n => n === 1 ? 'once' : n === 2 ? 'twice' : n + ' times';

  function board(fen){
    const a = new Array(64).fill(null); let r = 7, c = 0;
    for (const ch of fen.split(' ')[0]){ if (ch === '/'){ r--; c = 0; } else if (ch >= '1' && ch <= '8') c += +ch; else { a[r * 8 + c] = ch; c++; } }
    return a;
  }
  // the squares the piece on i attacks (sliders stop at the first piece)
  function hits(a, i){
    const p = a[i]; if (!p) return [];
    const t = low(p), f0 = i % 8, r0 = i >> 3, out = [];
    const one = (x, y) => { const f = f0 + x, r = r0 + y; if (f >= 0 && f < 8 && r >= 0 && r < 8) out.push(r * 8 + f); };
    if (t === 'p'){ const d = isW(p) ? 1 : -1; one(-1, d); one(1, d); return out; }
    if (t === 'n'){ KN.forEach(([x, y]) => one(x, y)); return out; }
    if (t === 'k'){ KG.forEach(([x, y]) => one(x, y)); return out; }
    for (const [x, y] of t === 'b' ? DG : t === 'r' ? OR : DG.concat(OR)){
      let f = f0 + x, r = r0 + y;
      while (f >= 0 && f < 8 && r >= 0 && r < 8){ out.push(r * 8 + f); if (a[r * 8 + f]) break; f += x; r += y; }
    }
    return out;
  }
  const dirOf = (i, j) => { const df = (j % 8) - (i % 8), dr = (j >> 3) - (i >> 3); if (!df && !dr) return null;
    if (df && dr && Math.abs(df) !== Math.abs(dr)) return null; return [Math.sign(df), Math.sign(dr)]; };
  // the squares strictly between i and j on a line (none when they are not on one)
  function between(i, j){ const d = dirOf(i, j); if (!d) return []; const out = []; let f = (i % 8) + d[0], r = (i >> 3) + d[1];
    while (r * 8 + f !== j){ out.push(r * 8 + f); f += d[0]; r += d[1]; } return out; }
  // a piece pinned to its own king may only move along the pin
  function pinLine(a, i){
    const p = a[i]; if (!p || low(p) === 'k') return null;
    const white = isW(p), k = a.findIndex(q => q && low(q) === 'k' && isW(q) === white); if (k < 0) return null;
    const d = dirOf(k, i); if (!d || between(k, i).some(s => a[s])) return null;
    let f = (i % 8) + d[0], r = (i >> 3) + d[1];
    while (f >= 0 && f < 8 && r >= 0 && r < 8){
      const q = a[r * 8 + f];
      if (q){ const t = low(q), diag = d[0] && d[1]; return isW(q) !== white && (t === 'q' || t === (diag ? 'b' : 'r')) ? [k, r * 8 + f] : null; }
      f += d[0]; r += d[1];
    }
    return null;
  }
  const canGo = (a, i, t) => { const pl = pinLine(a, i); return !pl || t === pl[1] || between(pl[0], pl[1]).includes(t); };
  const by = (a, t, white) => { const out = []; for (let i = 0; i < 64; i++) if (a[i] && isW(a[i]) === white && hits(a, i).includes(t) && canGo(a, i, t)) out.push(i); return out; };
  // what the piece on f wins by taking on t, when both sides go on taking back with their cheapest piece while it pays
  function see(a, f, t){
    const b = a.slice(), g = [b[t] ? val(b[t]) : 0]; let on = b[f], side = !isW(on), d = 0;
    b[t] = on; b[f] = null;
    for (;;){
      const at = by(b, t, side); if (!at.length) break;
      const i = at.reduce((x, y) => val(b[x]) <= val(b[y]) ? x : y);
      d++; g[d] = val(on) - g[d - 1];
      if (Math.max(-g[d - 1], g[d]) < 0) break;
      on = b[i]; b[t] = on; b[i] = null; side = !side;
    }
    while (d){ g[d - 1] = -Math.max(-g[d - 1], g[d]); d--; }
    return g[0];
  }
  const load = fen => { const ch = new Chess(); return ch.load(fen) ? ch : null; };
  const uciOf = m => m.from + m.to + (m.promotion || '');
  const asMove = u => ({from: u.slice(0, 2), to: u.slice(2, 4), promotion: u[4] || 'q'});
  // the same position with the other side to move: what a side threatens is what it could do if it moved again
  const pass = fen => { const p = fen.split(' '); p[1] = p[1] === 'w' ? 'b' : 'w'; p[3] = '-'; return p.join(' '); };
  // the captures and the mates the side to move has, each with what it wins: [{u, f, t, v, cap, pc, mate}]
  const CAPS = new Map();
  function captures(fen){
    if (CAPS.has(fen)) return CAPS.get(fen);
    const ch = load(fen), out = []; if (!ch){ CAPS.set(fen, out); return out; }
    const a = board(fen);
    for (const m of ch.moves({verbose: true})){
      const mate = m.san.endsWith('#'); if ((!m.captured && !mate) || m.captured === 'k') continue;
      const f = idx(m.from), t = idx(m.to);
      let v = m.captured ? (m.flags.includes('e') ? 1 : see(a, f, t)) : 0; if (m.promotion) v += V[m.promotion] - 1;
      out.push({u: uciOf(m), f, t, v, cap: m.captured || null, pc: m.piece, mate});
    }
    if (CAPS.size > 4000) CAPS.clear();
    CAPS.set(fen, out); return out;
  }
  const winning = xs => xs.filter(x => x.mate || x.v >= 1);
  const inCheck = fen => { const ch = load(fen); return !!ch && ch.in_check(); };
  // what the side not to move is sure to win: every answer of the side to move, then the best capture (a mate counts
  // as a lot), less what that answer took. Two moves deep, static at the end.
  function forced(fen, info){
    const ch = load(fen); if (!ch) return 0;
    const a = board(fen); let worst = Infinity; const ts = new Set();
    for (const m of ch.moves({verbose: true})){
      const took = m.captured ? (m.flags.includes('e') ? 1 : Math.max(0, see(a, idx(m.from), idx(m.to)))) : 0;
      ch.move(m); const f2 = ch.fen(), mated = ch.in_checkmate(); ch.undo();
      const cs = captures(f2), top = cs.reduce((b, x) => (x.mate ? 1000 : x.v) > (b ? (b.mate ? 1000 : b.v) : 0) ? x : b, null);
      const best = mated ? -1000 : top ? (top.mate ? 1000 : top.v) : 0;
      worst = Math.min(worst, best - took); if (top && !top.mate) ts.add(top.t); else ts.add(-1);
      if (worst <= 0) return 0;
    }
    if (info) info.t = ts.size === 1 && !ts.has(-1) ? [...ts][0] : null;
    return worst === Infinity ? 0 : worst;
  }

  // names from the player's side: "your bishop", "Black's e-pawn", "the pawn on f7"
  function namer(me){
    const opp = me === 'w' ? 'Black' : 'White', owner = white => (white ? 'w' : 'b') === me ? 'your' : `${opp}'s`;
    const bare = (a, i) => { const t = low(a[i]); return t === 'p' ? (i === F7 || i === F2 ? 'pawn on ' + sqn(i) : sqn(i)[0] + '-pawn') : NAME[t]; };
    const pn = (a, i) => `${owner(isW(a[i]))} ${bare(a, i)}`;
    const both = (a, is) => { const ns = is.slice(0, 2).map(i => bare(a, i));
      return `${owner(isW(a[is[0]]))} ${ns[0] === ns[1] && !/pawn/.test(ns[0]) ? 'two ' + ns[0] + 's' : ns.join(' and ')}`; };
    return {opp, owner, bare, pn, both};
  }
  const PRI = {mate: 100, win: 90, fork: 85, checkwin: 84, mthreat: 75, smate: 72, threat: 70, uncover: 68, unguard: 67, takeatt: 65, escape: 64, guard: 62, block: 61,
    guard2: 35, pin: 66, trade: 50, f7: 45, hang: 44, castle: 40, offer: 30, opens: 25, center: 24, dev: 22};
  const MEMO = new Map();

  function of(fen, u, o = {}){
    const key = fen + '|' + u + '|' + (o.me || 'w') + '|' + (o.prev || '');
    if (MEMO.has(key)) return MEMO.get(key);
    const res = facts(fen, u, o); if (MEMO.size > 3000) MEMO.clear(); MEMO.set(key, res); return res;
  }
  function facts(fen, u, o){
    const ch = load(fen); if (!ch) return {facts: [], lines: []};
    const wasCheck = ch.in_check(), mv = ch.move(asMove(u)); if (!mv) return {facts: [], lines: []};
    const after = ch.fen(), S = mv.color === 'w', a0 = board(fen), a1 = board(after), from = idx(mv.from), to = idx(mv.to);
    const N = namer(o.me || 'w'), F = [], mine = (o.me || 'w') === mv.color;
    if (ch.in_checkmate()) return finish([{k: 'mate'}], N, a0, a1, to, mv);
    const check = ch.in_check();
    // what it takes
    if (mv.captured){
      const back = o.prev && o.prev.slice(2, 4) === mv.to, v = mv.flags.includes('e') ? 1 : see(a0, from, to);
      if (!back && v >= 1) F.push({k: 'win', free: by(a0, to, !S).length === 0, all: v >= V[mv.captured], t: to, v});
      else if (!back && v === 0 && mv.captured !== 'p') F.push({k: 'trade', pc: mv.piece, cap: mv.captured});
    }
    // what the moved piece now hits that the other side cannot hold; nothing, if the piece itself can simply be taken
    const exposed = !mv.captured && winning(captures(after)).some(x => !x.mate && x.t === to);
    const targets = exposed ? [] : hits(a1, to).filter(s => a1[s] && isW(a1[s]) !== S && (low(a1[s]) === 'k' || see(a1, to, s) >= 1));
    if (check){
      const g = forced(after);
      if (g >= 1 && targets.length >= 2) F.push({k: 'fork', is: targets.sort((x, y) => val(a1[y]) - val(a1[x])), v: g});
      else if (g >= 2){ const info = {}; forced(after, info); F.push({k: 'checkwin', t: info.t !== undefined && info.t !== null && a1[info.t] ? info.t : null, v: g}); }
    } else {
      // threats: what it could take (or mate) next if it moved again, that it could not before
      const before = new Set(winning(captures(fen)).map(x => x.t)), hadMate = captures(fen).some(x => x.mate);
      const next = captures(pass(after)), mates = next.filter(x => x.mate);
      if (mates.length && !hadMate) F.push({k: 'mthreat', sq: mates.map(x => x.t).find(t => t === F7 || t === F2)});
      const mateSq = new Set(mates.map(x => x.t));
      const fresh = winning(next).filter(x => !x.mate && !before.has(x.t) && a1[x.t] && !mateSq.has(x.t) && !(exposed && x.f === to));
      const fromMoved = [...new Set(fresh.filter(x => x.f === to).map(x => x.t))];
      if (fromMoved.length >= 2 && forced(after) >= 1) F.push({k: 'fork', is: fromMoved.sort((x, y) => val(a1[y]) - val(a1[x]))});
      else for (const x of fresh.sort((p, q) => q.v - p.v).filter((x, k, xs) => xs.findIndex(y => y.t === x.t) === k).slice(0, 2)){
        if (x.f === to) F.push({k: 'threat', t: x.t});
        else if (between(x.f, x.t).includes(from)) F.push({k: 'uncover', f: x.f, t: x.t});          // the move opened that line
        else if (mv.captured && hits(a0, to).includes(x.t)) F.push({k: 'unguard', t: x.t});          // it took the piece that guarded it
        else if (!mv.captured) F.push({k: 'threat', t: x.t});                                         // the move added an attacker
      }
    }
    // what it stops: the other side's threats before the move that are gone after it
    if (!wasCheck){
      const was = captures(pass(fen)), now = captures(after), nowWin = winning(now);
      if (was.some(x => x.mate) && !now.some(x => x.mate)){ const m = was.find(x => x.mate); F.push({k: 'smate', sq: m.t === F7 || m.t === F2 ? m.t : null}); }
      const seen = new Set();
      for (const T of winning(was).filter(x => !x.mate).sort((p, q) => q.v - p.v)){
        if (seen.has(T.t)) continue; seen.add(T.t);
        if (T.t === from){ if (!nowWin.some(x => x.t === to) && !F.some(x => x.k === 'win')) F.push({k: 'escape'}); continue; }
        if (nowWin.some(x => x.t === T.t) || !a1[T.t] || !a1[T.f]) continue;   // still there, or the piece went with the move (castling)
        if (mv.captured && to === T.f) F.push({k: 'takeatt', t: T.t, att: T.f});
        else if (hits(a1, to).includes(T.t)) F.push({k: 'guard', t: T.t, att: T.f});
        else if (between(T.f, T.t).includes(to)) F.push({k: 'block', t: T.t});
        else if (by(a1, T.t, S).length > by(a0, T.t, S).length) F.push({k: 'guard2', t: T.t});
      }
    }
    // a pin by the moved piece: an enemy piece with its king, or something bigger, behind it on the same line
    if ('brq'.includes(mv.piece)){
      for (const [x, y] of mv.piece === 'b' ? DG : mv.piece === 'r' ? OR : DG.concat(OR)){
        let f = (to % 8) + x, r = (to >> 3) + y, first = -1;
        while (f >= 0 && f < 8 && r >= 0 && r < 8){
          const i = r * 8 + f, q = a1[i];
          if (q){
            if (first < 0){ if (isW(q) === S || 'kp'.includes(low(q))) break; first = i; }
            else {
              const t = low(q);
              if (isW(q) !== S && (t === 'k' || (val(q) > val(a1[first]) && (val(q) > V[mv.piece] || !by(a1, i, !S).length))))
                F.push({k: 'pin', x: first, y: i, abs: t === 'k'});
              break;
            }
          }
          f += x; r += y;
        }
      }
    }
    if (mv.flags.includes('k') || mv.flags.includes('q')) F.push({k: 'castle'});
    // the pawn next to the king that only the king guards
    const T7 = S ? F7 : F2;
    if (a1[T7] && low(a1[T7]) === 'p' && isW(a1[T7]) !== S && by(a1, T7, S).length > by(a0, T7, S).length && by(a1, T7, !S).every(i => low(a1[i]) === 'k')) F.push({k: 'f7', sq: T7});
    // the other side's move left something of its own to be taken (the player's moves that do this are offers)
    if (!check){
      const opp = winning(captures(after)).filter(x => !x.mate && a1[x.t] && isW(a1[x.t]) === S), was = new Set(winning(captures(pass(fen))).map(x => x.t));
      const h = opp.filter(x => x.t === to ? !mv.captured : !was.has(x.t)).sort((p, q) => q.v - p.v)[0];
      if (h && !F.some(x => x.k === 'win' && x.v >= h.v)) F.push(mine ? {k: 'offer', t: h.t} : {k: 'hang', t: h.t, att: h.f, free: !by(a1, h.t, S).length});
    }
    if (mv.piece === 'p' && CENTER.includes(to)) F.push({k: 'center'});
    if (mv.piece === 'p'){
      let best = null, gain = 1;
      for (let i = 0; i < 64; i++){ const q = a1[i]; if (!q || isW(q) !== S || !'bq'.includes(low(q))) continue;
        const d = hits(a1, i).length - hits(a0, i).length; if (d > gain || (d === gain && best !== null && low(q) === 'b' && low(a1[best]) === 'q')){ best = i; gain = d; } }
      if (best !== null) F.push({k: 'opens', at: best});
    }
    if ('nb'.includes(mv.piece) && HOME[mv.color][mv.piece].includes(mv.from)) F.push({k: 'dev'});
    return finish(F, N, a0, a1, to, mv);
  }
  function finish(F, N, a0, a1, to, mv){
    F.sort((x, y) => PRI[y.k] - PRI[x.k]);
    if (F.some(x => x.k === 'fork')) F = F.filter(x => x.k !== 'threat');
    if (F.some(x => x.k === 'castle')) F = F.filter(x => x.k !== 'dev');
    const f7 = F.find(x => x.k === 'f7'); if (f7 && F.some(x => (x.k === 'threat' || x.k === 'win' || x.k === 'unguard') && x.t === f7.sq || (x.k === 'mthreat' && x.sq === f7.sq))) F = F.filter(x => x !== f7);
    const out = [];
    for (const x of F){
      let s = ''; try { s = line(x, N, a0, a1, to, mv); } catch(e){ s = ''; }
      if (s && !out.includes(s)) out.push(s);
      if (out.length >= 2) break;
    }
    return {facts: F, lines: out};
  }
  function line(x, N, a0, a1, to, mv){
    switch (x.k){
      case 'mate': return 'Checkmate';
      case 'win': return x.free ? `Wins ${N.pn(a0, x.t)} for free: nothing guarded it` : x.all ? `Wins ${N.pn(a0, x.t)}: taking back would cost ${N.owner(mv.color === 'w') === 'your' ? N.opp : 'you'} more` : `Wins material: ${N.pn(a0, x.t)} for a ${NAME[mv.piece]}`;
      case 'trade': return `A trade: ${NAME[x.pc]} for ${NAME[x.cap]}`;
      case 'fork': return `A fork: ${N.pn(a1, to)} hits ${N.both(a1, x.is)} at once`;
      case 'checkwin': return x.t !== null ? `Check, and every answer loses ${N.pn(a1, x.t)}` : 'Check, and every answer loses material';
      case 'mthreat': return x.sq ? `Threatens mate on ${sqn(x.sq)}` : 'Threatens mate';
      case 'smate': return x.sq ? `Stops the mate on ${sqn(x.sq)}` : 'Stops a mate';
      case 'threat': return `Threatens to take ${N.pn(a1, x.t)}`;
      case 'uncover': return `Uncovers an attack: ${N.pn(a1, x.f)} now hits ${N.pn(a1, x.t)}`;
      case 'unguard': return `Takes away the guard of ${N.pn(a1, x.t)}`;
      case 'takeatt': return `Takes ${N.pn(a0, to)}, which was hitting ${N.pn(a1, x.t)}`;
      case 'escape': return `Moves ${N.pn(a1, to)} out of danger`;
      case 'guard': return `Guards ${N.pn(a1, x.t)} from ${N.pn(a1, x.att)}`;
      case 'block': return `Blocks the attack on ${N.pn(a1, x.t)}`;
      case 'guard2': return `${cap(N.pn(a1, x.t))} is guarded now`;
      case 'pin': return x.abs ? `Pins ${N.pn(a1, x.x)} to the king: it can't move` : `Pins ${N.pn(a1, x.x)}: moving it would drop the ${NAME[low(a1[x.y])]}`;
      case 'castle': return 'Tucks the king in behind its pawns and brings a rook toward the middle';
      case 'f7': return `Aims at ${sqn(x.sq)}, which only ${N.owner(isW(a1[x.sq]))} king guards`;
      case 'hang': return x.free ? `Leaves ${N.pn(a1, x.t)} unguarded` : `Puts ${N.pn(a1, x.t)} where ${N.pn(a1, x.att)} can take it`;
      case 'offer': return `Offers ${N.pn(a1, x.t)}: ${N.opp} can take it`;
      case 'opens': return `Opens a line for ${N.pn(a1, x.at)}`;
      case 'center': return 'Takes space in the center';
      case 'dev': return 'Brings a piece into play';
    }
    return '';
  }

  // why a capture works, from the side that loses the piece
  function whyTaken(a, f, t, N){
    const d = by(a, t, isW(a[t])).length, n = by(a, t, isW(a[f])).length;
    if (!d) return `Nothing guarded ${N.pn(a, t)}`;
    if (val(a[f]) < val(a[t])) return `${cap(N.pn(a, t))} is worth more than the ${NAME[low(a[f])]} that takes it`;
    if (n > d) return `${cap(N.pn(a, t))} is attacked ${times(n)} and guarded only ${times(d)}`;
    return '';
  }
  // the reason an answer works, on the board after the move it answers (fen): a mate, a capture, a fork, a threat
  function reply(fen, u, o = {}){
    const ch = load(fen); if (!ch) return [];
    const N = namer(o.me || 'w'), a = board(fen), mv = ch.move(asMove(u)); if (!mv) return [];
    if (ch.in_checkmate()) return [];
    const out = [];
    if (mv.captured && !mv.flags.includes('e')){ const w = whyTaken(a, idx(mv.from), idx(mv.to), N); if (w) out.push(w); }
    for (const s of of(fen, u, o).lines) if (!/^(Wins|A trade)/.test(s) && !out.includes(s)) out.push(s);
    return out.slice(0, 2);
  }
  // the other side's best answer to a move, when it wins something: a mate, a capture that pays, or a fork (or a check)
  // that wins whatever the reply. Null when the move loses nothing that this can see.
  function punish(fen, u, o = {}){
    const ch = load(fen); if (!ch) return null;
    const mv = ch.move(asMove(u)); if (!mv || ch.in_checkmate() || ch.in_draw()) return null;
    const after = ch.fen(), S = mv.color === 'w', N = namer(o.me || mv.color), a1 = board(after);
    const words = (x, f = after) => { try { return o.words ? o.words(f, x) : ''; } catch(e){ return ''; } };
    const took = mv.captured ? V[mv.captured] : 0;   // what the move itself took: a fair trade is no mistake to punish
    let best = null;
    for (const x of captures(after)){
      if (x.mate) return {u: x.u, kind: 'mate', gain: 1000, took, lines: [`${N.opp} has mate: ${low1(words(x.u)) || 'checkmate'}`]};
      if (x.v - took >= 1 && (!best || x.v > best.gain)) best = {u: x.u, kind: 'take', gain: x.v, took, t: x.t, f: x.f};
    }
    for (const m of ch.moves({verbose: true})){
      if (m.captured && best && best.u === uciOf(m)) continue;
      ch.move(m); const f2 = ch.fen(), chk = /[+#]$/.test(m.san); ch.undo();
      const a2 = board(f2), t = idx(m.to);
      if (see(a1, idx(m.from), t) < 0 && a1[t]) continue;
      const tg = hits(a2, t).filter(s => a2[s] && isW(a2[s]) === S && (low(a2[s]) === 'k' || see(a2, t, s) >= 1));
      if (!(tg.length >= 2 || (chk && tg.length >= 1))) continue;
      if (by(a2, t, S).length && see(a2, by(a2, t, S).reduce((x, y) => val(a2[x]) <= val(a2[y]) ? x : y), t) >= 1) continue;   // the forking piece itself can be taken
      const g = forced(f2);
      if (g - took >= 1 && (!best || g > best.gain)) best = {u: uciOf(m), kind: 'fork', gain: g, took, is: tg.sort((x, y) => val(a2[y]) - val(a2[x])), at: t, a2};
    }
    if (!best) return null;
    const w = low1(words(best.u));
    if (best.kind === 'take'){ const why = whyTaken(a1, best.f, best.t, N); return Object.assign(best, {lines: [`${N.opp} answers: ${w || 'takes ' + N.pn(a1, best.t)}`].concat(why ? [why] : [])}); }
    return Object.assign(best, {lines: [`${N.opp} answers: ${w || NAME[low(best.a2[best.at])] + ' move'}`, `A fork: it hits ${N.both(best.a2, best.is)} at once`]});
  }
  const low1 = s => s ? s.charAt(0).toLowerCase() + s.slice(1) : s;

  return {of, punish, reply, see, board, captures, forced, _hits: hits};
})();
if (typeof module !== 'undefined') module.exports = Ideas;
