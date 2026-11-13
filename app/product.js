/* ------------------------------------------------------------------ the product shell
   Who is looking decides what the app shows:
     house  the hand-built playbook (the personal build, and accounts that had progress before personal playbooks existed)
     new    no games yet: the sandbox works, everything else is locked behind bringing games in
     ready  games read, choices made: the course, Learn and Your games are built from the player's own profile
   The profile comes from app/analyze.js (rules and counting, no model). It is kept with the progress record as d.me. */
const legacyProg = d => !!(d && ((d.lines && Object.keys(d.lines).length) || (d.course && d.course.u && Object.keys(d.course.u).length)));
const meOf = d => d && d.me ? d.me : (legacyProg(d) ? {state: 'house'} : null);
const personaOf = d => { if (!SITE) return 'house'; const m = meOf(d); return m && m.state ? m.state : 'new'; };
const ME_RANK = {house: 3, ready: 2, 'new': 1};
function mergeMe(a, b){ const x = meOf(a), y = meOf(b); if (!x || !y) return x || y; const rx = ME_RANK[x.state] || 0, ry = ME_RANK[y.state] || 0; return rx !== ry ? (rx > ry ? x : y) : (y.updated || 0) > (x.updated || 0) ? y : x; }
let PERSONA = 'house';
const PVIEWS = ['start', 'setup', 'reading', 'findings', 'choices', 'built'], OPEN_NEW = PVIEWS.concat(['sandbox', 'explore']);
const TARGET = 150, MINIMUM = 50;
const pc = (a, b) => b ? Math.round(100 * a / b) : 0, rec = t => `${t.w}–${t.l}${t.d ? '–' + t.d : ''}`, scoreOf = t => t.n ? (t.w + t.d / 2) / t.n : 0;
const plural = (n, w) => `${n} ${w}${n === 1 ? '' : 's'}`;

/* the coaches: three original characters drawn here. They say the same things; the player picks the face and the name comes with it. */
const COACHES = [{id: 'knight', name: 'Pip', what: 'the knight'}, {id: 'rook', name: 'Rocco', what: 'the rook'}, {id: 'pawn', name: 'Dot', what: 'the pawn with plans'}];
const coachWho = () => COACHES.find(c => c.id === SET.who) || COACHES[0], coachName = () => coachWho().name;
// two eyes for the characters that face you: round and looking at you, looking up when thinking, shut and smiling when pleased
const eyes2 = (x1, x2, y, r, mood) => mood === 'cheer' ? `<path class="kn-line" d="M${x1 - r + 1} ${y + 1}q${r - 1}-${r} ${2 * r - 2} 0M${x2 - r + 1} ${y + 1}q${r - 1}-${r} ${2 * r - 2} 0"/>`
  : [x1, x2].map(x => `<circle class="kn-eye" cx="${x}" cy="${y}" r="${r}"/><circle class="kn-pupil" cx="${x + (mood === 'think' ? 1.1 : 0)}" cy="${y + (mood === 'think' ? -1.5 : .5)}" r="${r / 2}"/><circle class="kn-eye" cx="${x + (mood === 'think' ? 1.9 : .9)}" cy="${y - (mood === 'think' ? 2.3 : .5)}" r=".9"/>`).join('');
const FACES = {
  knight(mood){
    const eye = mood === 'cheer' ? '<path class="kn-line" d="M25 22q3.5-4.5 7 0"/>' : `<circle class="kn-eye" cx="28.5" cy="21" r="5"/><circle class="kn-pupil" cx="${mood === 'think' ? 29.6 : 27.6}" cy="${mood === 'think' ? 19.4 : 21.4}" r="2.5"/><circle class="kn-eye" cx="${mood === 'think' ? 30.4 : 28.4}" cy="${mood === 'think' ? 18.6 : 20.4}" r=".9"/>`;
    return `<path class="kn-mane" d="M33 6c12 1 22 11 23 26l1 26H44c4-16 2-34-11-52z"/>
    <path class="kn-body" d="M22 58c-2-12 1-19 8-25l-5-3c-4 5-11 9-15 5-4-5 1-15 12-21l1-10 8 6c13 0 22 11 22 26v22z"/>
    <path class="kn-muzzle" d="M10 35c-3-4 0-11 7-16 2 4 6 7 10 8-5 6-12 11-17 8z"/>${eye}
    <ellipse class="kn-pupil" cx="13.2" cy="29.6" rx="1.3" ry="1.7"/><path class="kn-line" d="M13.5 34.5q3.6 2.6 7.4-.6"/><circle class="kn-blush" cx="24" cy="29.5" r="2.6"/>
    <rect class="kn-base" x="16" y="56" width="42" height="7" rx="3.5"/>`;
  },
  rook(mood){
    return `<path class="kn-mane" d="M13 7h9v6h5V7h10v6h5V7h9v15H13z"/><path class="kn-body" d="M17 21h30l4 37H13z"/><rect class="kn-muzzle" x="15" y="20" width="34" height="5.5" rx="2.2"/>
    ${eyes2(25, 39, 35.5, 5.2, mood)}<path class="kn-line" d="M${mood === 'think' ? '28 46q4 1.6 8 0' : '26.5 45q5.5 5 11 0'}"/><circle class="kn-blush" cx="19.5" cy="43" r="2.6"/><circle class="kn-blush" cx="44.5" cy="43" r="2.6"/>
    <rect class="kn-base" x="9" y="56" width="46" height="7" rx="3.5"/>`;
  },
  pawn(mood){
    return `<path class="kn-crown" d="M22.5 13.5 21 4l6.2 4.6L32 2.5l4.8 6.1L43 4l-1.5 9.5z"/><path class="kn-body" d="M17 58c0-10 5-16 15-16s15 6 15 16z"/><circle class="kn-body" cx="32" cy="26" r="15.5"/>
    <rect class="kn-mane" x="19" y="39.5" width="26" height="5.6" rx="2.8"/>${eyes2(26, 38, 25, 4.8, mood)}<path class="kn-line" d="M${mood === 'think' ? '29 33.5q3 1.4 6 0' : '27.5 32.5q4.5 4.4 9 0'}"/>
    <circle class="kn-blush" cx="20.5" cy="31" r="2.4"/><circle class="kn-blush" cx="43.5" cy="31" r="2.4"/><rect class="kn-base" x="12" y="56" width="40" height="7" rx="3.5"/>`;
  }
};
function knightSVG(mood, who){ return `<svg viewBox="0 0 64 64" aria-hidden="true">${(FACES[who || coachWho().id] || FACES.knight)(mood)}</svg>`; }
// the three faces to choose from (Settings, and the first screen after an account is made)
function coachPickHTML(){ return `<div class="coachpick" role="group" aria-label="Your coach">${COACHES.map(c => `<button type="button" data-coachwho="${c.id}" aria-pressed="${coachWho().id === c.id}"><span class="cface">${knightSVG('', c.id)}</span><b>${c.name}</b><span>${c.what}</span></button>`).join('')}</div>`; }
document.addEventListener('click', e => {
  const b = e.target.closest('[data-coachwho]'); if (!b) return;
  setSetting('who', b.dataset.coachwho); if (!document.getElementById('setSheet').hidden) Settings.render();
  render(); Coach.say(`${coachName()} here. Same advice, new face.`, {mood: 'cheer', ms: 5000});
});

/* ---- the systems the library has, and the ones being written. `keys` are the analysis names for what a player already plays. */
const CATALOG = [
  {slot: 'white', ask: 'With White, would you rather…', flip: false, opts: [
    {id: 'e4', keys: ['e4'], ready: true, name: 'Open with the e-pawn', line: 'e4 e5 Nf3 Nc6 Bc4', pitch: 'Fast development and open lines. Your bishop aims at f7 from move three, and every reply has a ready answer.'},
    {id: 'd4', keys: ['d4'], ready: false, name: 'Open with the d-pawn', line: 'd4 d5 Bf4 Nf6 e3 e6 Nf3', pitch: 'A slower build-up around one setup that works against almost anything.'},
    {id: 'flank', keys: ['c4', 'nf3'], ready: false, name: 'Start from the side', line: 'c4 e5 Nc3 Nf6 g3', pitch: 'Hold the centre pawns back and steer the game to your kind of position.'}]},
  {slot: 'blackE4', ask: 'Against the e-pawn, would you rather…', flip: true, chapters: ['italian', 'ruy', 'scotch', 'vienna', 'attacks'], opts: [
    {id: 'e5', keys: ['e5'], ready: true, name: 'Meet it head-on', line: 'e4 e5 Nf3 Nc6 Bc4 Bc5', pitch: 'Your own e-pawn, your bishop on the same diagonal as theirs, and an early castle. Classical and direct.'},
    {id: 'sicilian', keys: ['sicilian'], ready: false, name: 'Fight from the side (Sicilian)', line: 'e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6', pitch: 'Unbalanced from move one. More to learn and more winning chances.'},
    {id: 'caro', keys: ['caro'], ready: false, name: 'Build a wall (Caro-Kann)', line: 'e4 c6 d4 d5 Nc3 dxe4 Nxe4', pitch: 'A sound pawn structure, few early tactics and a good bishop.'},
    {id: 'french', keys: ['french'], ready: false, name: 'Lock the centre (French)', line: 'e4 e6 d4 d5 e5 c5', pitch: 'A closed centre and a clear plan against White\'s pawn chain.'}]},
  {slot: 'blackD4', ask: 'Against the d-pawn, would you rather…', flip: true, chapters: ['slav', 'london', 'd4x'], opts: [
    {id: 'slav', keys: ['slav'], ready: true, name: 'One solid setup (Slav)', line: 'd4 d5 c4 c6 Nf3 Nf6 e3 Bf5', pitch: 'D-pawn, c-pawn, bishop out, e-pawn: the same order against every d-pawn system.'},
    {id: 'kid', keys: ['kid'], ready: false, name: 'Let them build, then strike', line: 'd4 Nf6 c4 g6 Nc3 Bg7 e4 d6', pitch: 'A fianchetto bishop behind your pawns and an attack on the kingside (King\'s Indian).'},
    {id: 'qgd', keys: ['qgd', 'nimzo'], ready: false, name: 'The classical defence', line: 'd4 d5 c4 e6 Nc3 Nf6', pitch: 'D-pawn and e-pawn side by side: hard to break down, with a quieter bishop.'}]}
];
const STYLE = [
  {id: 'order', ask: 'Where should your course start? Would you rather…', opts: [
    {id: 'leaks', big: 'p-wr', name: 'Fix what costs me the most games', pitch: 'Units are ordered by how often you meet each opening and how badly it goes.'},
    {id: 'often', big: 'p-wn', name: 'Start with what I play most', pitch: 'Units are ordered by how often each opening comes up, whatever your score in it.'}]},
  {id: 'depth', ask: 'And when you drill, would you rather…', opts: [
    {id: 'core', big: 'p-wk', name: 'Know a few lines cold', pitch: 'Drills start with the core lines only. The side lines wait until you ask for them.'},
    {id: 'wide', big: 'p-wq', name: 'See a little of everything', pitch: 'Drills mix in the side lines from the start.'}]}
];
function fenOf(line){ const c = new Chess(); let last = null; for (const s of line.split(' ')){ const m = c.move(s, {sloppy: true}); if (m) last = [m.from, m.to]; } return {fen: c.fen().split(' ')[0], last}; }
// which cards to show: a system card only where the player's own habit and the library differ; the two style cards always
function makeChoices(P){
  const out = [];
  for (const C of CATALOG){
    const s = P.slots[C.slot]; if (!s || s.n < 5) continue;
    const share = o => o.keys.reduce((a, k) => a + ((s.opts[k] || {}).n || 0), 0), tal = o => o.keys.reduce((a, k) => { const t = s.opts[k]; if (t){ a.n += t.n; a.w += t.w; a.l += t.l; a.d += t.d; } return a; }, {n: 0, w: 0, l: 0, d: 0});
    const own = C.opts.slice().sort((a, b) => share(b) - share(a))[0], ready = C.opts.find(o => o.ready);
    if (own === ready || share(own) / s.n < 0.3) continue;
    out.push({id: C.slot, ask: C.ask, kind: 'system', flip: C.flip, opts: [own, ready].map(o => Object.assign({}, o, {t: tal(o), of: s.n}))});
  }
  for (const Q of STYLE) out.push(Object.assign({kind: 'style'}, Q));
  return out;
}
const defaultPicks = () => ({white: 'e4', blackE4: 'e5', blackD4: 'slav', order: 'leaks', depth: 'core'});

/* ---- text that speaks about the house player's own games is taken out for everyone else */
const PERS = /\b(your games?|in your game|you (lost|won|played|pushed|took|missed|resigned|blundered|had)\b|against \S+ (in|on) (jul|aug|sep|oct|nov)|both of your|you have (won|lost)|your last|this exact shot against)/i;
function scrub(t){ if (!t || !PERS.test(t)) return t; return (t.match(/[^.!?]+[.!?]+["')]*\s*|[^.!?]+$/g) || []).filter(x => !PERS.test(x)).join('').trim(); }
const ORIG = {};
function depersonalise(){
  for (const s of ['w', 'b']){
    const D = BOOKS[s];
    for (const n of D.nodes) if (n.t) n.t = scrub(n.t);
    for (const l of D.lessons){ l.why = scrub(l.why); l.sub = scrub(l.sub) || l.sub; }
    for (const C of D.chapters){ C.notes = []; C.facts = []; }
    D.insights = []; D.puzzles = D.puzzles || [];
  }
  const I = BOOKS.w.chapters.find(c => c.id === 'italian'), setup = BOOKS.w.lines.find(l => l.id === 'setup');
  if (I && setup) Object.assign(I, {hero: setup.n[setup.n.length - 1], arrows: ['c4f7r', 'f3g5g'], circles: ['f7r'], cap: 'Bishop and knight both aim at f7.', kicker: 'Black\'s e-pawn mirrors yours · then the knight',
    headline: 'Aim everything at <em>f7</em>.', lede: 'The pawn beside Black\'s king has only one defender. Your bishop, your knight and often your queen all point at it.'});
  for (const U of COURSE) for (const sl of (U.idea || [])) for (const k in sl) if (typeof sl[k] === 'string') sl[k] = scrub(sl[k]) || sl[k];
  const gen = t => t.replace('from your games', 'from real club games').replace('you were winning and the next move', 'the player was winning and the next move')
    .replace('In this game your next move lost material.', 'In the game the next move lost material.').replace('In the game your next move let most of it slip.', 'In the game the next move let most of it slip.')
    .replace('An ending from your game. Your next move in the game', 'An ending from a real game. The next move in the game');
  for (const k in SKILL){ const K = SKILL[k]; K.what = gen(K.what); const ask = K.ask; K.ask = it => gen(ask(it)); }
  const skillWhy = {threats: 'Positions from real club games where the next move lost material. Spot what is attacked before you move.', finish: 'Winning positions from real club games that were let slip. Find the move that keeps the win.',
    endings: 'Endings from real club games where one move decided the result.'};
  for (const U of COURSE) if (U.kind === 'skill'){ U.why = skillWhy[U.id] || U.why; U.kicker = 'Skill · from real club games'; for (const sl of (U.idea || [])) for (const k in sl) if (typeof sl[k] === 'string') sl[k] = gen(sl[k]).replace(/\byour (own )?games\b/g, 'real club games'); }
  for (const s of ['w', 'b']){ const T = TXT[s], side = s === 'w' ? 'White' : 'Black';
    T.learnKick = st => st.total ? `Your ${st.total} games with ${side}` : `The ${side} playbook`;
    T.gamesP = st => `${st.total} games with ${side}: ${st.wins} wins, ${st.losses} losses${st.draws ? `, ${plural(st.draws, 'draw')}` : ''}.`;
    T.foot = ['Every line checked with Stockfish 17.1.', 'Opponent odds come from Maia, a model trained on real club games.']; }
}
const chaptersOfUnit = U => [...new Set((U.lessons || []).map(l => { const L = LIDX[U.side] && LIDX[U.side][l], p = L && BOOKS[U.side].parts.find(x => x.id === L.part); return p && p.ch; }).filter(Boolean))];
// the profile decides the numbers on every chapter, the order of the course and what each unit says about the player
function applyProfile(me){
  const P = me.P, picks = Object.assign(defaultPicks(), me.picks || {});
  for (const s of ['w', 'b']){
    const D = BOOKS[s], side = s === 'w' ? P.white : P.black;
    Object.assign(D.stats, {total: side.all.n, wins: side.all.w, losses: side.all.l, draws: side.all.d});
    for (const C of D.chapters){
      const t = side.systems[C.id] || {n: 0, w: 0, l: 0, d: 0, depth: 0}; C.stats = {n: t.n, w: t.w, l: t.l, d: t.d};
      C.facts = t.n ? [{big: String(t.n), text: `of your ${side.all.n} ${s === 'w' ? 'White' : 'Black'} games went here`}, {big: rec(t), text: 'your record in them', alert: t.l > t.w},
        {big: String(Math.max(1, Math.round(t.depth / 2))), text: 'moves, on average, before the game left the playbook'}] : [{big: '0', text: 'of your games went here so far'}];
    }
    TXT[s].foot = TXT[s].foot.slice(0, 2).concat([`Built from ${P.n} of your games${P.user ? ' as ' + P.user : ''}.`]);
  }
  const skills = COURSE.map((U, k) => U.kind === 'skill' ? [k, U] : null).filter(Boolean), open = COURSE.filter(U => U.kind !== 'skill');
  for (const U of open){
    const side = U.side === 'w' ? P.white : P.black, word = U.side === 'w' ? 'White' : 'Black', t = {n: 0, w: 0, l: 0, d: 0, depth: 0};
    for (const c of chaptersOfUnit(U)){ const x = side.systems[c]; if (x){ t.n += x.n; t.w += x.w; t.l += x.l; t.d += x.d; t.depth += x.depth * x.n; } }
    const share = side.all.n ? t.n / side.all.n : 0;
    U.need = picks.order === 'often' ? share : share * (1.3 - scoreOf(t));
    const slot = U.side === 'w' ? 'white' : CATALOG.find(C => C.chapters && chaptersOfUnit(U).some(c => C.chapters.includes(c)));
    const C = typeof slot === 'string' ? CATALOG[0] : slot, pick = C && C.opts.find(o => o.id === picks[C.slot]);
    U.soon = !!(pick && !pick.ready);
    U.kicker = `${word} · ${t.n ? `${pc(t.n, side.all.n)}% of your ${word} games` : 'not in your games yet'}`;
    U.why = U.soon ? `You chose "${pick.name}" here, and that system is still being written. This unit opens when it is ready.`
      : t.n ? `You met this in ${t.n} of your ${side.all.n} ${word} games and scored ${rec(t)}. On average the game stayed in the playbook for ${plural(Math.max(1, Math.round(t.depth / t.n / 2)), 'move')}.`
      : `None of your ${side.all.n} ${word} games went here, so it comes late in your course. It is here for the day someone plays it.`;
  }
  open.sort((a, b) => (a.soon - b.soon) || (b.need - a.need) || (a.k - b.k));
  const order = open.slice(); for (const [k, U] of skills) order.splice(Math.min(k, order.length), 0, U);
  COURSE.length = 0; order.forEach((U, k) => { U.k = k; COURSE.push(U); });
}

/* ---- bringing games in */
const Importer = {
  async json(url){ const r = await fetch(url); if (r.status === 404) throw Object.assign(new Error('missing'), {missing: true}); if (!r.ok) throw new Error('http ' + r.status); return r.json(); },
  async chesscom(user, want, tick){
    const base = 'https://api.chess.com/pub/player/' + encodeURIComponent(user.trim().toLowerCase());
    const months = ((await this.json(base + '/games/archives')).archives || []).reverse().slice(0, 36), out = [];
    for (const m of months){
      const gs = ((await this.json(m)).games || []).filter(g => g.rules === 'chess' && g.pgn && g.time_class !== 'daily').reverse();
      for (const g of gs) out.push(g.pgn); tick(out.length); if (out.length >= want) break;
    }
    return out.slice(0, want).join('\n\n');
  },
  async lichess(user, want, tick){
    const r = await fetch(`https://lichess.org/api/games/user/${encodeURIComponent(user.trim())}?max=${want}&perfType=bullet,blitz,rapid,classical&clocks=false&evals=false&opening=false`, {headers: {Accept: 'application/x-chess-pgn'}});
    if (r.status === 404) throw Object.assign(new Error('missing'), {missing: true}); if (!r.ok) throw new Error('http ' + r.status);
    const t = await r.text(); tick((t.match(/^\[Event /gm) || []).length); return t;
  }
};

const Product = {
  pool: '', msg: null, busy: false, site: 'chess.com', names: null, user: '', draft: null, cards: null, ci: 0, picks: null,
  me(){ return Prog.d.me || {}; },
  boot(){
    PERSONA = personaOf(Prog.d);
    if (SITE && !meOf(Prog.d)) Prog.d.me = {state: 'new', since: Date.now()};
    if (PERSONA !== 'house') depersonalise();
    if (PERSONA === 'ready' && this.me().P) applyProfile(this.me());
    document.querySelectorAll('.tabs button').forEach(b => b.classList.toggle('lock', PERSONA === 'new' && b.dataset.view !== 'sandbox'));
  },
  landing(h){ if (PERSONA === 'ready' && (this.me().picks || {}).depth === 'core' && S.dfilter){ DF_PRI = 'core'; S.dfilter.pri = 'core'; }   // drills start with the core lines
    if (PERSONA === 'new' && !OPEN_NEW.includes(S.view)) S.view = 'start'; if (PERSONA === 'new' && PVIEWS.includes(h) && h !== 'reading' && h !== 'built') S.view = (h === 'findings' || h === 'choices') && !this.me().P ? 'start' : h; },
  // after a sign-in merge: if the account turns out to be someone else's kind of playbook, start over with it
  afterMerge(){ if (SITE && !meOf(Prog.d)) Prog.d.me = {state: 'new', since: Date.now()}; if (personaOf(Prog.d) !== PERSONA){ Prog.saveLocal(); location.reload(); return true; } return false; },
  signedOut(){ return Cloud.on() && !Cloud.user; },
  render(){
    const v = S.view;
    view.innerHTML = `<div class="pv">${v === 'start' ? this.startHTML() : v === 'setup' ? this.setupHTML() : v === 'reading' ? this.readingHTML() : v === 'findings' ? this.findingsHTML() : v === 'choices' ? this.choiceHTML() : this.builtHTML()}</div>`;
    this.wire();
  },
  /* -- welcome */
  startHTML(){
    const out = this.signedOut(), has = !!this.me().P, step = out ? 1 : has ? 3 : 2, w = fenOf('e4 e5 Nf3 Nc6 Bc4 Bc5 c3 Nf6 d4');
    const cta = out ? `<button class="btn primary" data-acct="signup">Create your account</button><button class="btn" data-acct="signin">I already have an account</button>`
      : has ? `<button class="btn primary" data-pgo="findings">Continue: see what I found</button>` : `<button class="btn primary" data-pgo="setup">Bring your games</button>`;
    const li = (k, h, p) => `<li class="${k < step ? 'done' : k === step ? 'now' : ''}"><b>${h}</b><span>${p}</span></li>`;
    const lock = (v, h, p) => `<button class="lockcard" data-view="${v}"><b>${ICON.lock}${h}</b>${p}</button>`;
    return `<section class="whero"><div><p class="kicker">An opening course built from your own games</p>
        <h2>Bring ${TARGET} games.<br>Get <em>your</em> playbook.</h2>
        <p class="lede" style="margin-top:14px">It reads what you already play, where you score and where you leave the book, asks you a few would-you-rather questions, and builds a course in that order. No notation anywhere.</p>
        <div class="cta">${cta}<button class="btn ghost" data-view="sandbox">Try the sandbox first</button></div></div>
      <div class="wart"><div class="board">${boardSVG(w.fen, {coords: false, last: w.last, arrows: ['c4f7r'], flip: false})}</div><p class="wbub">Hi, I'm ${coachName()}. Show me your games and I'll show you your openings.</p><div class="wcoach cface">${knightSVG()}</div></div></section>
      <ol class="steps3">${li(1, 'Make an account', 'So your playbook follows you to every device.')}${li(2, `Bring ${TARGET} games`, 'A chess.com or Lichess username is enough. A file works too.')}${li(3, 'Pick your lines', 'A few would-you-rather questions, then your course opens.')}</ol>
      <div><p class="kicker" style="margin-bottom:10px">Opens with your games</p><div class="lockgrid">${lock('course', 'Course', 'One path, ordered by what your games say matters most.')}${lock('learn', 'Learn', 'Every line as a board you step through, in plain words.')}${lock('drill', 'Drill', 'Your moves from memory, on a schedule that brings slips back.')}${lock('games', 'Your games', 'Results by opening and where you leave the book.')}${lock('cheat', 'Cheat sheet', 'One card per decision.')}</div></div>`;
  },
  locked(tab){
    const T = {course: ['Your course', 'One path through your openings, in the order your games say matters most: the idea, the lines, a drill, practice games and a checkpoint for each.'],
      learn: ['Learn', 'Every line of your playbook as a board you step through, with each move described in plain words.'], drill: ['Drill', 'Your moves from memory. Clean runs come back later; slips come back today.'],
      games: ['Your games', 'Your results by opening, and the exact positions where you leave your playbook most often.'], cheat: ['Cheat sheet', 'One card per decision: their move, your answer.']}[tab] || ['This section', ''];
    const out = this.signedOut(), idx = [LINES[DATA.lessons[0].lines[0]].n.slice(-1)[0], LINES[DATA.lessons[1].lines[0]].n.slice(-1)[0], LINES[DATA.lessons[2].lines[0]].n.slice(-1)[0]];
    view.innerHTML = `<div class="pv"><section class="plocked"><div class="lk">${ICON.lock}</div><p class="kicker">Locked until your games are in</p><h3>${T[0]}</h3><p>${T[1]}</p>
      <div class="cta">${out ? `<button class="btn primary" data-acct="signup">Create your account</button>` : `<button class="btn primary" data-pgo="setup">Bring your games</button>`}<button class="btn" data-view="sandbox">Open the sandbox</button></div>
      <div class="ghost3" aria-hidden="true">${idx.map(i => thumb(i, {coords: false})).join('')}</div></section></div>`;
    this.wire();
  },
  /* -- games in */
  count(){ return this.pool ? (this.pool.match(/^\[Event /gm) || this.pool.match(/^\[White /gm) || []).length : 0; },
  setupHTML(){
    if (this.signedOut()) return `<section class="plocked"><div class="lk">${ICON.lock}</div><h3>First, an account</h3><p>Your games and your playbook are kept with your account, so they are there on every device.</p><div class="cta"><button class="btn primary" data-acct="signup">Create your account</button><button class="btn" data-acct="signin">Sign in</button></div></section>`;
    const n = this.count(), seg = (v, l) => `<button type="button" data-site="${v}" aria-pressed="${this.site === v}">${l}</button>`;
    const month = new Date().toISOString().slice(0, 7).replace('-', '/');
    return `<div class="chead"><div><p class="kicker">Step 2 of 3</p><h2 style="font-size:clamp(30px,4vw,46px)">Bring your games</h2><p>${TARGET} recent games is the target: enough to see what you really play. ${MINIMUM} is the least that works, and the picture sharpens as you add more.</p></div>
        <div class="meter"><div class="pring" style="--p:${Math.min(100, pc(n, TARGET))}"><i>${n}<small>of ${TARGET}</small></i></div></div></div>
      ${this.msg ? `<p class="pmsg ${this.msg.bad ? 'bad' : 'ok'}" role="status">${esc(this.msg.t)}</p>` : ''}
      <div class="pcard pickc"><div><h3>Pick your coach</h3><p>They say the same things. Change your mind any time in Settings.</p></div>${coachPickHTML()}</div>
      ${this.names ? `<div class="pcard"><b>Which one is you?</b><div class="pwho" style="margin-top:10px">${this.names.map(x => `<button class="btn" data-who="${esc(x)}">${esc(x)}</button>`).join('')}</div></div>` : ''}
      <div class="setup"><form class="pcard" id="uform"><h3>Fetch them by username</h3>
          <div class="setseg" role="group" aria-label="Where you play">${seg('chess.com', 'chess.com')}${seg('lichess', 'Lichess')}</div>
          <div class="pfield"><label for="uname">Your username on ${this.site === 'lichess' ? 'Lichess' : 'chess.com'}</label><input type="text" id="uname" autocomplete="off" autocapitalize="off" spellcheck="false" value="${esc(this.user)}" placeholder="for example: ${this.site === 'lichess' ? 'your_lichess_name' : 'your_chesscom_name'}"></div>
          <button class="btn primary" type="submit" ${this.busy ? 'disabled' : ''} style="justify-content:center;min-height:46px">${this.busy ? 'Fetching…' : `Fetch my last ${TARGET} games`}</button>
          <p style="color:var(--muted);font-size:13.5px">Only your public games are read, straight from ${this.site === 'lichess' ? 'Lichess' : 'chess.com'} to this page. Nothing is posted and no password is needed.</p></form>
        <div class="pcard"><h3>Or drop a PGN file</h3>
          <label class="drop" id="drop"><input type="file" id="pgnFile" accept=".pgn,.txt,text/plain" multiple><b>Drop PGN files here, or tap to choose</b><span>Several files are fine. They add up.</span></label>
          <details class="how"><summary>How do I get a PGN file?</summary>
            <ol><li><b>chess.com:</b> open this address in your browser with your own name in it, once for each month you need. Each one downloads a file.<br><code>api.chess.com/pub/player/YOUR_NAME/games/${month}/pgn</code></li>
              <li><b>Lichess:</b> open your profile, press the download button above your games, and choose "Export games".</li><li>Drop every file you got into the box above.</li></ol></details></div></div>`;
  },
  async fetchUser(){
    const u = (document.getElementById('uname').value || '').trim(); this.user = u; if (!u){ this.msg = {bad: 1, t: 'Type your username first.'}; return render(); }
    this.busy = true; this.msg = {t: `Looking for ${u} on ${this.site}…`}; render();
    try {
      const text = await Importer[this.site === 'lichess' ? 'lichess' : 'chesscom'](u, TARGET + 50, n => { const r = document.querySelector('.pring'); if (r){ r.style.setProperty('--p', Math.min(100, pc(n, TARGET))); r.firstElementChild.firstChild.textContent = n; } });
      this.busy = false; this.pool = text; this.src = {site: this.site, user: u.toLowerCase()}; this.ingest(u.toLowerCase());
    } catch(e){
      this.busy = false;
      this.msg = {bad: 1, t: e.missing ? `There is no player called "${u}" on ${this.site}. Check the spelling.` : `Couldn't reach ${this.site} from this page. Use a PGN file instead: the steps are under "How do I get a PGN file?"`}; render();
    }
  },
  async addFiles(files){
    const texts = await Promise.all([...files].map(f => f.text().catch(() => '')));
    this.pool = [this.pool].concat(texts).filter(Boolean).join('\n\n'); this.src = this.src && this.src.site !== 'pgn' ? this.src : {site: 'pgn', user: ''}; this.ingest(this.src.user);
  },
  // enough games and a known player: read them. Otherwise say what is missing.
  ingest(user){
    const raw = Analyze.parsePGN(this.pool); this.names = null;
    if (!raw.length){ this.msg = {bad: 1, t: 'No games found in that. A PGN file starts with lines like [Event "…"].'}; return render(); }
    user = (user || Analyze.guessUser(raw) || '').toLowerCase();
    if (!user){ const c = {}; for (const g of raw) for (const k of ['White', 'Black']) if (g.h[k]) c[g.h[k]] = (c[g.h[k]] || 0) + 1; this.names = Object.keys(c).sort((a, b) => c[b] - c[a]).slice(0, 4); this.msg = {t: `${raw.length} games read. They are not all by one player, so tell me who you are.`}; return render(); }
    const mine = raw.filter(g => (g.h.White || '').toLowerCase() === user || (g.h.Black || '').toLowerCase() === user);
    const key = g => (g.h.UTCDate || g.h.Date || '') + (g.h.UTCTime || g.h.StartTime || ''); mine.sort((a, b) => key(b) < key(a) ? -1 : 1);
    if (mine.length < MINIMUM){ this.msg = {bad: mine.length === 0, t: mine.length ? `${mine.length} of your games so far. ${MINIMUM} is the least I can work with, ${TARGET} is the target. Add more.` : `None of those ${raw.length} games were played by "${user}".`}; return render(); }
    this.read(mine.slice(0, 250), user);
  },
  /* -- the reading screen: the analysis runs while the board plays through the games */
  STAGES: ['Reading your games', 'Sorting them by opening', 'Measuring where you score', 'Finding where you leave the book', 'Building your playbook'],
  readingHTML(){
    return `<section class="proc"><div class="board" id="pboard">${boardSVG(N[0].f, {coords: false})}</div>
      <div><p class="kicker">Step 2 of 3 · this takes a few seconds</p><h2 style="font-size:clamp(30px,4vw,48px)">Reading your games</h2>
        <ul class="plist" id="plist">${this.STAGES.map((s, k) => `<li class="${k === 0 ? 'on' : ''}" data-k="${k}"><i>${ICON.check}</i><span>${s}</span><span class="c"></span></li>`).join('')}</ul>
        <div class="pbar"><i id="pbar"></i></div>
        <div class="say"><div class="cface">${knightSVG('think')}</div><p id="psay">Let me look.</p></div></div></section>`;
  },
  async read(raw, user){
    S.view = 'reading'; this.msg = null; render(); setHash(); window.scrollTo({top: 0});
    const wait = ms => new Promise(r => setTimeout(r, reduced ? 60 : ms)), say = t => { const e = document.getElementById('psay'); if (e) e.textContent = t; };
    const stage = (k, c) => { document.querySelectorAll('#plist li').forEach(li => { const i = +li.dataset.k; li.className = i < k ? 'ok' : i === k ? 'on' : ''; if (i === k && c !== undefined) li.querySelector('.c').textContent = c; }); const b = document.getElementById('pbar'); if (b) b.style.width = Math.min(100, (k + (c && c.frac || 0)) / this.STAGES.length * 100) + '%'; };
    // the board plays the first moves of the games as they are read
    const queue = []; let ch = new Chess(), cur = null, ci = 0;
    const anim = setInterval(() => {
      const el = document.getElementById('pboard'); if (!el){ clearInterval(anim); return; }
      if (!cur || ci >= Math.min(cur.length, 14)){ if (!queue.length) return; cur = queue.shift(); ci = 0; ch = new Chess(); }
      const m = ch.move(uciObj(cur[ci++])); if (m) el.innerHTML = boardSVG(ch.fen().split(' ')[0], {coords: false, last: [m.from, m.to]});
    }, reduced ? 400 : 95);
    const t0 = Date.now();
    const P = await Analyze.run(raw, user, BOOKS, p => { if (p.last && queue.length < 40) queue.push(p.last.ucis); stage(0, `${p.done} of ${p.of}`); const b = document.getElementById('pbar'); if (b) b.style.width = (p.done / p.of * 20) + '%'; });
    if (S.view !== 'reading'){ clearInterval(anim); return; }
    await wait(Math.max(0, 1500 - (Date.now() - t0)));
    const top = side => Object.entries(side.systems).sort((a, b) => b[1].n - a[1].n)[0], cn = (s, id) => (BOOKS[s].chapters.find(c => c.id === id) || {}).name || id;
    stage(1, `${Object.keys(P.white.systems).length + Object.keys(P.black.systems).length} openings`);
    const tw = top(P.white), tb = top(P.black); say(tw ? `With White you land in the ${cn('w', tw[0])} most: ${plural(tw[1].n, 'game')}.` : `${P.white.all.n} games with White, ${P.black.all.n} with Black.`); await wait(1500);
    stage(2, `${pc(P.all.w + P.all.d / 2, P.all.n)}% overall`); say(P.facts[0] ? P.facts[0].text : `You score ${pc(P.all.w + P.all.d / 2, P.all.n)}% over these ${P.n} games.`); await wait(1700);
    stage(3, plural(P.leaks.length, 'spot')); say(P.leaks[0] ? `One position came up ${plural(P.leaks[0].n, 'time')} and you left the playbook the same way each time. We'll fix that one first.` : 'You stay in the book longer than most.'); await wait(1700);
    stage(4); say(tb ? `Against you, White goes for the ${cn('b', tb[0])} most. Nearly done.` : 'Nearly done.'); await wait(1300);
    stage(5); clearInterval(anim);
    this.pool = ''; Prog.d.me = {state: 'new', since: this.me().since || Date.now(), updated: Date.now(), src: this.src || {site: 'pgn', user}, P}; Prog.save();
    S.view = 'findings'; render(); setHash(); window.scrollTo({top: 0});
  },
  /* -- what the games say */
  barsHTML(slot, P){
    const s = P.slots[slot]; if (!s) return '';
    return Object.values(s.opts).sort((a, b) => b.n - a.n).slice(0, 4).map(t => `<div class="brow"><span class="bn">${esc(t.name)}</span><span class="br">${plural(t.n, 'game')} · ${rec(t)}</span><span class="bb"><i style="width:${Math.max(3, pc(t.n, s.n))}%"></i></span></div>`).join('');
  },
  leakHTML(L, btn){
    const D = BOOKS[L.side], n = D.nodes[L.node], kid = (n.k || []).find(c => !!D.nodes[c].w === (L.side === 'w') && !(D.nodes[c].g || []).includes('warn')), bk = kid !== undefined ? D.nodes[kid] : null;
    const us = []; for (let i = L.node; D.nodes[i] && D.nodes[i].p !== null && D.nodes[i].p !== undefined; i = D.nodes[i].p) us.push(D.nodes[i].u);
    const ch = new Chess(); let prev = null; for (let k = us.length - 1; k >= 0; k--) prev = ch.move(uciObj(us[k]));
    const mv = ch.move(uciObj(L.uci)); if (mv) ch.undo(); const words = mv ? moveWords(ch, mv, prev) : 'another move';
    const les = new Set(D.lessons.map(l => l.id)), ln = bk ? D.lines.find(l => les.has(l.lesson) && l.n.includes(kid)) : null, line = ln ? ln.id : null;
    return `<div class="leak"><div class="thumb">${boardSVG(n.f, {mini: true, coords: false, flip: L.side === 'b', arrows: [L.uci.slice(0, 4) + 'r'].concat(bk ? [bk.u.slice(0, 4) + 'g'] : [])})}</div>
      <div><p><b>${plural(L.n, 'time')}</b> · you scored ${rec(L)}</p><p>You played: <b>${esc(lc(words))}</b>.${bk ? ` The playbook plays: <b>${esc(lc(bk.l || 'the green arrow'))}</b>.` : ''}</p>
      ${btn && line ? `<button class="btn small" data-leak="${L.side}:${line}:${kid}" style="margin-top:8px">Open the lesson</button>` : ''}</div></div>`;
  },
  findingsHTML(){
    const P = this.me().P; if (!P) return this.startHTML();
    const tile = (b, s) => `<div class="tile"><b>${b}</b><span>${s}</span></div>`;
    return `<div class="chead"><div><p class="kicker">Step 2 of 3 · done</p><h2 style="font-size:clamp(30px,4vw,48px)">Here's what your games say${P.user ? ', ' + esc(P.user) : ''}</h2></div></div>
      <div class="tiles">${tile(P.n, 'games read')}${tile(P.rating || '–', `your ${P.tc} rating${P.peak > P.rating ? `, best ${P.peak}` : ''}`)}${tile(rec(P.all), 'wins and losses')}${tile(pc(P.all.w + P.all.d / 2, P.all.n) + '%', `score against ${P.oppAvg || '?'}-rated opponents`)}</div>
      <div class="fgrid"><div class="pcard"><p class="kicker">What you already play</p>
          <h3 style="margin-top:6px">With White</h3><div class="bars">${this.barsHTML('white', P)}</div>
          <h3 style="margin-top:20px">Against the e-pawn</h3><div class="bars">${this.barsHTML('blackE4', P) || '<p style="color:var(--muted)">Not enough games yet.</p>'}</div>
          <h3 style="margin-top:20px">Against the d-pawn</h3><div class="bars">${this.barsHTML('blackD4', P) || '<p style="color:var(--muted)">Not enough games yet.</p>'}</div></div>
        <div style="display:grid;gap:16px"><div class="pcard"><p class="kicker">Where you score</p>
          <ul class="factl">${(P.facts.length ? P.facts.slice(0, 4) : [{big: pc(P.all.w + P.all.d / 2, P.all.n) + '%', text: 'Your results are even across the kinds of game I measured.'}]).map(f => `<li><b>${f.big}</b><span>${esc(f.text)}</span></li>`).join('')}</ul></div>
          ${P.leaks.length ? `<div class="pcard"><p class="kicker">Where you leave the book most</p><div style="display:grid;gap:10px;margin-top:12px">${P.leaks.slice(0, 2).map(L => this.leakHTML(L)).join('')}</div></div>` : ''}</div></div>
      <div class="cta" style="justify-content:flex-end;display:flex"><button class="btn primary" data-pgo="choices" style="min-height:46px;padding:11px 22px">Next: a few choices</button></div>`;
  },
  /* -- would you rather */
  choiceHTML(){
    const P = this.me().P; if (!P) return this.startHTML();
    if (!this.cards){ this.cards = makeChoices(P); this.ci = 0; this.picks = defaultPicks(); }
    const Q = this.cards[this.ci], dots = this.cards.map((_, k) => `<i class="${k <= this.ci ? 'on' : ''}"></i>`).join('');
    const opt = (o, k) => {
      if (Q.kind === 'style') return `<button class="wopt plain pop" data-pick="${o.id}" style="animation-delay:${k * 90}ms"><svg class="pbig" viewBox="0 0 45 45" aria-hidden="true"><use href="#${o.big}"/></svg><b>${esc(o.name)}</b><p>${esc(o.pitch)}</p></button>`;
      const f = fenOf(o.line), mine = o.t.n / o.of >= 0.3;
      return `<button class="wopt pop" data-pick="${o.id}" style="animation-delay:${k * 90}ms"><div class="board">${boardSVG(f.fen, {coords: false, flip: Q.flip, last: f.last})}</div>
        <span><span class="chip ${o.ready ? 'good' : 'new'}">${o.ready ? 'Ready now' : 'Being written'}</span></span><b>${esc(o.name)}</b><p>${esc(o.pitch)}</p>
        <span class="you">${mine ? `What you play now: ${pc(o.t.n, o.of)}% of these games, ${rec(o.t)}.` : o.t.n ? `You have tried it ${plural(o.t.n, 'time')}: ${rec(o.t)}.` : 'New to you.'}${o.ready ? '' : ' Its lessons are not written yet, so this part of your course would wait.'}</span></button>`;
    };
    return `<section class="wyr"><p class="kicker">Step 3 of 3 · would you rather · ${this.ci + 1} of ${this.cards.length}</p><div class="pdots" aria-hidden="true">${dots}</div>
      <div class="say"><div class="cface">${knightSVG()}</div><p>${esc(Q.ask)}</p></div>
      <div class="duo">${opt(Q.opts[0], 0)}<span class="or">or</span>${opt(Q.opts[1], 1)}</div>
      ${this.ci ? `<button class="btn ghost" data-cback>Back</button>` : ''}</section>`;
  },
  pick(id){
    this.picks[this.cards[this.ci].id] = id;
    if (++this.ci < this.cards.length) return render();
    Prog.d.me = Object.assign({}, this.me(), {state: 'ready', picks: this.picks, updated: Date.now()}); Prog.save(); this.cards = null;
    S.view = 'built'; render(); setHash();
  },
  builtHTML(){
    const P = this.me().P || {n: 0};
    return `<section class="done-art"><div class="cface pop">${knightSVG('cheer')}</div><p class="kicker">Built from ${P.n} games</p><h2>Your playbook is <em>ready</em>.</h2>
      <p class="lede">Your course is ordered by your own games, every chapter shows your own record, and Your games shows where you leave the book.</p>
      <div class="cta"><button class="btn primary" data-open style="min-height:48px;padding:12px 24px;font-size:16px">Open my course</button></div></section>`;
  },
  /* -- Your games, for a player with a profile */
  games(){
    const P = this.me().P, cn = (s, id) => (BOOKS[s].chapters.find(c => c.id === id) || {}).name || '';
    const col = (s, side) => { const max = Math.max(1, ...Object.values(side.systems).map(t => t.n));
      return Object.entries(side.systems).sort((a, b) => b[1].n - a[1].n).map(([id, t]) => `<button class="brow" data-pch="${s}:${id}" style="border:0;background:none;padding:0;text-align:left;cursor:pointer;font:inherit;color:inherit"><span class="bn">${esc(cn(s, id))}</span><span class="br">${plural(t.n, 'game')} · ${rec(t)}</span><span class="bb"><i style="width:${Math.max(3, pc(t.n, max))}%"></i></span></button>`).join(''); };
    const day = t => t ? new Date(t).toLocaleDateString(undefined, {month: 'short', day: 'numeric'}) : '';
    const rows = P.games.slice(0, 40).map(g => `<tr><td>${day(g.t)}</td><td>${g.me === 'w' ? 'White' : 'Black'}</td><td>${esc(g.opp)}${g.oe ? ` <span style="color:var(--muted)">${g.oe}</span>` : ''}</td><td><span class="chip ${g.r === 1 ? 'win' : g.r === 0 ? 'loss' : 'draw'}">${g.r === 1 ? 'Won' : g.r === 0 ? 'Lost' : 'Draw'}</span></td><td>${esc(g.ch ? cn(g.me, g.ch) : 'Outside the playbook')}</td><td>${g.ch ? plural(Math.floor(g.bp / 2), 'move') + ' in the book' : ''}</td></tr>`).join('');
    const tile = (b, s) => `<div class="tile"><b>${b}</b><span>${s}</span></div>`;
    view.innerHTML = `<div class="pv"><div class="chead"><div><p class="kicker">Your games${P.user ? ' · ' + esc(P.user) : ''}</p><h2 style="font-size:clamp(30px,4vw,44px)">What actually happened</h2><p>${P.n} games, read without an engine: what you met, how it went, and where your moves and your playbook part ways.</p></div>
        <button class="btn" data-pgo="setup">Update from new games</button></div>
      <div class="tiles">${tile(P.n, 'games')}${tile(rec(P.all), 'wins and losses')}${tile(P.rating || '–', `${P.tc} rating`)}${tile(P.leaks.length, 'spots where you leave the book')}</div>
      <div class="fgrid"><div class="pcard"><p class="kicker">With White · ${rec(P.white.all)}</p><div class="bars">${col('w', P.white)}</div></div><div class="pcard"><p class="kicker">With Black · ${rec(P.black.all)}</p><div class="bars">${col('b', P.black)}</div></div></div>
      ${P.leaks.length ? `<div><div class="sechead"><h2>Where you leave your playbook</h2><p>The same position, the same different move. Red is what you played, green is the playbook.</p></div><div class="leaks">${P.leaks.slice(0, 8).map(L => this.leakHTML(L, true)).join('')}</div></div>` : ''}
      ${P.facts.length ? `<div class="pcard"><p class="kicker">Where you score</p><ul class="factl">${P.facts.map(f => `<li><b>${f.big}</b><span>${esc(f.text)}</span></li>`).join('')}</ul></div>` : ''}
      <div><div class="sechead"><h2>Recent games</h2></div><div class="gwrap pcard" style="padding:6px 10px"><table class="gtable"><thead><tr><th>Date</th><th>Colour</th><th>Opponent</th><th>Result</th><th>Opening</th><th></th></tr></thead><tbody>${rows}</tbody></table></div></div></div>`;
    this.wire();
  },
  wire(){
    view.querySelectorAll('[data-acct]').forEach(b => b.onclick = () => Acct.open(b.dataset.acct));
    view.querySelectorAll('[data-pgo]').forEach(b => b.onclick = () => { this.msg = null; if (b.dataset.pgo === 'choices') this.cards = null; go(b.dataset.pgo); });
    view.querySelectorAll('[data-site]').forEach(b => b.onclick = () => { this.site = b.dataset.site; this.user = (document.getElementById('uname') || {}).value || ''; render(); });
    view.querySelectorAll('[data-who]').forEach(b => b.onclick = () => { if (this.src) this.src.user = b.dataset.who.toLowerCase(); this.ingest(b.dataset.who); });
    view.querySelectorAll('[data-pick]').forEach(b => b.onclick = () => this.pick(b.dataset.pick));
    view.querySelectorAll('[data-pch]').forEach(b => b.onclick = () => { const [s, id] = b.dataset.pch.split(':'); useSide(s); S.chapter = id; go('learn'); });
    view.querySelectorAll('[data-leak]').forEach(b => b.onclick = () => { const [s, line, kid] = b.dataset.leak.split(':'); useSide(s); openLine(line, Math.max(0, LINES[line].n.indexOf(+kid)), 'games'); });
    const cb = view.querySelector('[data-cback]'); if (cb) cb.onclick = () => { this.ci--; render(); };
    const op = view.querySelector('[data-open]'); if (op) op.onclick = () => { try { history.replaceState(null, '', '#course'); } catch(e){} location.reload(); };
    const f = document.getElementById('uform'); if (f) f.onsubmit = e => { e.preventDefault(); if (!this.busy) this.fetchUser(); };
    const inp = document.getElementById('pgnFile'), drop = document.getElementById('drop');
    if (inp) inp.onchange = () => { if (inp.files.length) this.addFiles(inp.files); };
    if (drop){ drop.ondragover = e => { e.preventDefault(); drop.classList.add('over'); }; drop.ondragleave = () => drop.classList.remove('over'); drop.ondrop = e => { e.preventDefault(); drop.classList.remove('over'); if (e.dataTransfer.files.length) this.addFiles(e.dataTransfer.files); }; }
  }
};

/* ---- the coach: a few words in a speech bubble, bottom right. Never a hint while you are being tested. */
const Coach = {
  seen: (() => { try { return JSON.parse(localStorage.getItem('playbook-coach') || '{}'); } catch(e){ return {}; } })(), timer: null, last: null, n: 0,
  el(){ let e = document.getElementById('coach'); if (!e){ e = document.createElement('div'); e.id = 'coach'; e.className = 'coach'; document.body.appendChild(e);
      e.addEventListener('click', ev => { if (ev.target.closest('.cx')) return this.hush(); const a = ev.target.closest('[data-cgo]'); if (a){ this.hush(); return go(a.dataset.cgo); } if (ev.target.closest('.cav')) this.last && !e.querySelector('.cbub') ? this.say(this.last.t, this.last.o) : e.querySelector('.cbub') ? this.hush() : this.say(this.tip()); }); }
    return e; },
  // on the welcome, reading, findings and choice screens the coach is part of the page, so the corner one stays away
  draw(bub){ const e = this.el(); e.hidden = !SET.coach || (PVIEWS.includes(S.view) && S.view !== 'setup'); e.classList.toggle('quiet', ['drill', 'quiz', 'sandbox', 'study', 'explore'].includes(S.view));
    e.innerHTML = (bub || '') + `<button class="cav" type="button" aria-label="${coachName()}, your coach">${knightSVG(this.mood)}</button>`; },
  say(t, o = {}){
    if (!SET.coach) return; clearTimeout(this.timer); this.last = {t, o}; this.mood = o.mood;
    this.draw(`<div class="cbub" role="status"><button class="cx" type="button" aria-label="Close">×</button><span class="cwho">${coachName()}</span>${esc(t)}${o.cta ? `<div class="cacts"><button class="btn small primary" data-cgo="${o.cta[0]}">${esc(o.cta[1])}</button></div>` : ''}</div>`);
    if (!o.stay) this.timer = setTimeout(() => this.hush(), 9000 + t.length * 45);
  },
  hush(){ clearTimeout(this.timer); this.mood = null; this.draw(''); },
  once(key, t, o){ if (this.seen[key]) return false; this.seen[key] = 1; try { localStorage.setItem('playbook-coach', JSON.stringify(this.seen)); } catch(e){} this.say(t, o); return true; },
  refresh(){ this.hush(); },
  tip(){
    const T = {start: `Bring me ${TARGET} of your games and I'll build your course around them.`, setup: 'A username is the quickest way. I only read your public games.', sandbox: 'Play your side. The other side answers the way club players really do.',
      course: 'Work down the path. Each checkpoint you pass opens the next unit.', learn: 'Pick an opening, then step through a lesson with the arrow keys.', drill: 'Clean runs come back in days. Slips come back today.',
      games: 'This is where your moves and your playbook part ways.', cheat: 'Their move is highlighted. The green arrow is your answer.', study: 'Step through with the arrow keys. Switch the engine on under the board if a position looks scary.'};
    return T[S.view] || T[tabOf(S.view, S.studyFrom)] || 'Keep going.';
  },
  // called after every full render: at most one thing to say, and only the first time
  onView(){
    const v = S.view, e = this.el(); if (e.querySelector('.cbub') && this.lastView === v) return this.draw(e.querySelector('.cbub').outerHTML); this.lastView = v;
    if (v === 'reading' || v === 'choices' || v === 'built' || v === 'findings') return this.hush(); // the coach is already on the page there
    if (S.drill && S.drill.state === 'play') return this.hush(); // never while a drill, a practice game or a checkpoint is being played
    if (PERSONA === 'new'){
      if (v === 'start') return this.hush();
      if (v === 'setup') return this.once('setup', this.tip()) || this.hush();
      if (v === 'sandbox') return this.once('sb-new', `This is the sandbox: pick an opening and play. I'll stop you where the playbook has a better move. Bring your games and the rest opens.`, {cta: Product.signedOut() ? null : ['setup', 'Bring my games']}) || this.hush();
      if (!OPEN_NEW.includes(v)) return this.say('This opens once I\'ve read your games.', {cta: Product.signedOut() ? null : ['setup', 'Bring my games']});
      return this.hush();
    }
    if (PERSONA === 'ready' && v === 'course' && this.once('ready-course', 'This is your course, in the order your games asked for. Start with the unit at the top.')) return;
    if (['course', 'learn', 'drill', 'games', 'cheat', 'sandbox'].includes(v) && this.once('tab-' + v, this.tip())) return;
    this.hush();
  },
  event(kind, ok){
    if (kind === 'line' && S.view === 'drill'){ this.n++;
      if (!ok) return this.say('That one comes back today. The second time is where it sticks.');
      if (this.n % 3 === 1) return this.say(['Clean. That line is yours for a few days.', 'No slips. On to the next one.', 'Clean run. I\'ll bring it back before you forget it.'][Math.floor(this.n / 3) % 3], {mood: 'cheer'}); }
  }
};

/* ---- hooks into the app */
const render0 = render;
render = function(){
  if (PERSONA === 'new' && !OPEN_NEW.includes(S.view)){ stopPlay(); setTab(S.view); renderChrome(); S.drill = null; EngineUI.detach(); Product.locked(tabOf(S.view, S.studyFrom)); return Coach.onView(); }
  if (PVIEWS.includes(S.view)){ setTab(S.view); renderChrome(); S.drill = null; EngineUI.detach(); document.getElementById('dueBadge').hidden = true; Product.render(); return Coach.onView(); }
  render0(); Coach.onView();
};
const renderGames0 = renderGames;
renderGames = function(){ if (PERSONA === 'ready' && Product.me().P) return Product.games(); renderGames0(); };
const record0 = Prog.record.bind(Prog);
Prog.record = function(id, clean){ record0(id, clean); Coach.event('line', clean); };
