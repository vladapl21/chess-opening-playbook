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
// A repertoire needs a real picture of what someone plays: NEED games that are not bullet, at most TAKE of the newest are read.
// Neither number is shown to the player.
const NEED = 200, TAKE = 300;
// bullet (and faster): too quick to show what someone knows. A clock of base + 40 increments under three minutes.
function isFast(g){ const tc = String(g.h.TimeControl || ''); if (/^\d+(\+\d+)?$/.test(tc)){ const [b, i] = tc.split('+').map(Number); return b + 40 * (i || 0) < 180; } return /bullet/i.test(g.h.Event || ''); }
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
  pawn(mood, L){
    return `${L && L.head ? '' : '<path class="kn-crown" d="M22.5 13.5 21 4l6.2 4.6L32 2.5l4.8 6.1L43 4l-1.5 9.5z"/>'}<path class="kn-body" d="M17 58c0-10 5-16 15-16s15 6 15 16z"/><circle class="kn-body" cx="32" cy="26" r="15.5"/>
    <rect class="kn-mane" x="19" y="39.5" width="26" height="5.6" rx="2.8"/>${eyes2(26, 38, 25, 4.8, mood)}<path class="kn-line" d="M${mood === 'think' ? '29 33.5q3 1.4 6 0' : '27.5 32.5q4.5 4.4 9 0'}"/>
    <circle class="kn-blush" cx="20.5" cy="31" r="2.4"/><circle class="kn-blush" cx="43.5" cy="31" r="2.4"/><rect class="kn-base" x="12" y="56" width="40" height="7" rx="3.5"/>`;
  }
};
// What the coach wears (the Shop tab). Colours are CSS tokens; each piece is drawn once around its own anchor and
// placed on each character: hats on the head, glasses over the eyes, ties at the neck.
const SKINS = {'c-midnight': 'mid', 'c-ruby': 'ruby', 'c-plum': 'plum', 'c-tangerine': 'tang', 'c-gold': 'gold'};
const SPOT = {
  knight: {head: 'translate(35.5 11.5) rotate(16) scale(.78)', eyes: [[28.5, 21, 5]], side: true, neck: 'translate(30.5 39.5) rotate(-18) scale(.8)'},
  rook: {head: 'translate(32 7.4)', eyes: [[25, 35.5, 5.2], [39, 35.5, 5.2]], neck: 'translate(32 28.6) scale(.9)'},
  pawn: {head: 'translate(32 12.2) scale(.95)', eyes: [[26, 25, 4.8], [38, 25, 4.8]], neck: 'translate(32 42.3) scale(.86)'}
};
const HATS = {
  'h-cap': '<path class="g-blu" d="M-10.5 0C-10.5-11.5 10.5-11.5 10.5 0Z"/><ellipse class="g-blu2" cx="3.5" cy=".4" rx="14" ry="2.6"/><circle class="g-surf" cx="0" cy="-9.2" r="1.3"/>',
  'h-beanie': '<path class="g-ros" d="M-10.5 0C-10.5-12.5 10.5-12.5 10.5 0Z"/><path class="g-dash" d="M-5-2.5v-6M0-2.5v-8M5-2.5v-6"/><rect class="g-surf g-edge" x="-11.5" y="-3.4" width="23" height="4.8" rx="2.4"/><circle class="g-surf g-edge" cx="0" cy="-11.6" r="3.2"/>',
  'h-party': '<path class="g-vio" d="M-7.5 0L0-17L7.5 0Z"/><circle class="g-oro" cx="-2.6" cy="-4.5" r="1.3"/><circle class="g-oro" cx="2.4" cy="-8.6" r="1.2"/><circle class="g-oro" cx="-.4" cy="-12.6" r="1"/><circle class="g-oro" cx="0" cy="-17.4" r="2.3"/>',
  'h-tophat': '<rect class="g-ink" x="-7.5" y="-15.5" width="15" height="14.5" rx="1.2"/><rect class="g-ros" x="-7.5" y="-5.6" width="15" height="2.8"/><rect class="g-ink" x="-12.5" y="-2" width="25" height="3.2" rx="1.6"/>',
  'h-wizard': '<path class="g-vio" d="M-11 0Q-4-8 1.5-23.5Q5.5-9 11 0Z"/><ellipse class="g-vio2" cx="0" cy="0" rx="13.5" ry="2.4"/><path class="g-oro" d="M1.5-13.8l1.2 2.5 2.7.4-2 1.9.5 2.7-2.4-1.3-2.4 1.3.5-2.7-2-1.9 2.7-.4z"/>',
  'h-grad': '<path class="g-ink" d="M-7.5-1v-5.5h15V-1q-7.5 3.2-15 0z"/><path class="g-ink" d="M-14.5-7.2L0-11.8L14.5-7.2L0-2.6Z"/><path class="g-tass" d="M0-7.2L9.5-5.8V1.6"/><circle class="g-oro" cx="9.5" cy="2.4" r="1.6"/>',
  'h-crown': '<path class="g-oro g-edge2" d="M-10.5 0L-12-11.5L-5.8-5.8L0-13.8L5.8-5.8L12-11.5L10.5 0Z"/><circle class="g-ros" cx="0" cy="-4" r="1.7"/><circle class="g-blu" cx="-6.2" cy="-3" r="1.2"/><circle class="g-blu" cx="6.2" cy="-3" r="1.2"/>'
};
const NECKS = {
  'n-bowtie': '<path class="g-ros" d="M0 0L-7.5-4.6V4.6ZM0 0L7.5-4.6V4.6Z"/><circle class="g-ros2" cx="0" cy="0" r="2"/>',
  'n-scarf': '<rect class="g-blu" x="-12.5" y="-3.2" width="25" height="6.4" rx="3.2"/><path class="g-dash2" d="M-6-3v6M0-3v6M6-3v6"/><path class="g-blu" d="M4.5 1.5l2.5 11.5 5-1.2-2.6-10.8z"/>',
  'n-medal': '<path class="g-rib1" d="M-4.5-3.5L-.6 6.5H2.4L-1.5-3.5Z"/><path class="g-rib2" d="M4.5-3.5L.6 6.5H-2.4L1.5-3.5Z"/><circle class="g-oro g-edge2" cx="0" cy="9.6" r="4.4"/>'
};
function gearSVG(who, L){
  const P = SPOT[who] || SPOT.knight, E = P.eyes; let s = '';
  if (L.neck && NECKS[L.neck]) s += `<g transform="${P.neck}">${NECKS[L.neck]}</g>`;
  if (L.face === 'f-glasses') s += E.map(([x, y, r]) => `<circle class="g-lens" cx="${x}" cy="${y}" r="${r + 1.6}"/>`).join('') + (E.length > 1 ? `<path class="g-wire" d="M${E[0][0] + E[0][2] + 1.6} ${E[0][1]}H${E[1][0] - E[1][2] - 1.6}"/>` : `<path class="g-wire" d="M${E[0][0] + E[0][2] + 1.5} ${E[0][1] - .6}L${E[0][0] + 13} ${E[0][1] - 2}"/>`);
  if (L.face === 'f-shades') s += E.map(([x, y, r]) => `<rect class="g-shade" x="${x - r - 1.8}" y="${y - r + .2}" width="${2 * r + 3.6}" height="${2 * r - .6}" rx="${r - .4}"/><path class="g-glint" d="M${x - r + .4} ${y - 1.6}l2.4-2.2"/>`).join('') + (E.length > 1 ? `<path class="g-wire" d="M${E[0][0] + E[0][2] + 1.8} ${E[0][1] - 1}H${E[1][0] - E[1][2] - 1.8}"/>` : `<path class="g-wire" d="M${E[0][0] + E[0][2] + 1.8} ${E[0][1] - 1}L${E[0][0] + 13} ${E[0][1] - 2.4}"/>`);
  if (L.face === 'f-monocle'){ const [x, y, r] = E[E.length - 1]; s += `<circle class="g-mono" cx="${x}" cy="${y}" r="${r + 1.4}"/><path class="g-chain" d="M${x + r * .7} ${y + r + .6}q3 6 -1 12"/>`; }
  if (L.head && HATS[L.head]) s += `<g transform="${P.head}">${HATS[L.head]}</g>`;
  return s;
}
function knightSVG(mood, who, look){
  const w = who || coachWho().id, L = look || (typeof Shop !== 'undefined' ? Shop.worn() : {}), sk = SKINS[L.skin];
  return `<svg viewBox="${L.head ? '-6 -12 76 76' : '0 0 64 64'}" aria-hidden="true"${sk ? ` class="sk-${sk}"` : ''}>${(FACES[w] || FACES.knight)(mood, L)}${gearSVG(w, L)}</svg>`;
}
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
// a system is ready when the library has a pack for it (or it is the system the books were first written for)
for (const C of CATALOG) for (const o of C.opts) o.ready = o.ready || [BOOKS.w, BOOKS.b].some(D => ((D.packs || {})[C.slot] || {packs: {}}).packs[o.id]);
const packSlots = () => [BOOKS.w, BOOKS.b].flatMap(D => Object.entries(D.packs || {}).filter(([, v]) => Object.keys(v.packs).length > 1).map(([slot, v]) => ({slot, D, v})));
// the systems this player has chosen, for the slots where the library offers a choice
function wantPacks(){ const src = PERSONA === 'ready' ? (meOf(Prog.d) || {}).picks : Prog.d.packs, out = {}; for (const {slot, v} of packSlots()) if (src && v.packs[src[slot]] && src[slot] !== v.default) out[slot] = src[slot]; return out; }
// the books on this page were cut to the packs remembered on this device. If the progress says otherwise, remember that and load again.
function syncPacks(){
  if (PVIEWS.includes(S.view) && S.view !== 'start') return;
  const want = wantPacks(), have = {}; for (const {slot, v} of packSlots()) if (v.packs[PICKS[slot]] && PICKS[slot] !== v.default) have[slot] = PICKS[slot];
  if (JSON.stringify(want) === JSON.stringify(have)) return;
  try { localStorage.setItem(PACKS_KEY, JSON.stringify(want)); if (sessionStorage.getItem('packs-reload') === JSON.stringify(want)) return; sessionStorage.setItem('packs-reload', JSON.stringify(want)); } catch(e){ return; }
  // give the browser a moment to commit what was just stored: a reload in the same tick can lose it
  document.documentElement.setAttribute('aria-busy', 'true'); setTimeout(() => location.reload(), 350);
}
// Settings, folded away at the bottom: the system for each slot the library has more than one of. A switch swaps whole
// units, so it is never one tap: the player types their username first.
const Rep = {ask: null, open: false};
const slotName = slot => slot === 'white' ? 'With White' : slot === 'blackE4' ? 'Against the e-pawn' : 'Against the d-pawn';
function repNames(){
  const me = meOf(Prog.d) || {}, out = [(me.P || {}).user, (me.src || {}).user];
  if (PERSONA === 'house') for (const D of [BOOKS.w, BOOKS.b]) for (const G of (D.games || [])) out.push(G.acct);
  return [...new Set(out.filter(Boolean).map(x => String(x).toLowerCase()))];
}
function packRowsHTML(){
  if (PERSONA === 'new') return '';
  const slots = packSlots(); if (!slots.length) return '';
  const names = repNames(), word = names[0] || 'switch', A = Rep.ask;
  const rows = slots.map(({slot, D, v}) => {
    const C = CATALOG.find(x => x.slot === slot), cur = packOf(D, slot), nm = id => ((C && C.opts.find(o => o.id === id)) || {name: id}).name;
    const ask = A && A.slot === slot ? `<form class="repask" data-repform><label for="repName">${names.length > 1 ? 'Type one of your usernames' : `Type <b>${esc(word)}</b>`} to switch to <b>${esc(nm(A.id))}</b>.</label>
        <div class="reprow"><input id="repName" type="text" autocomplete="off" autocapitalize="off" spellcheck="false" aria-label="Your username"><button class="btn primary small" type="submit" disabled>Switch</button><button class="btn small ghost" type="button" data-repcancel>Cancel</button></div></form>` : '';
    return `<div class="setrow"><b>${slotName(slot)}</b><div class="setseg" role="group">${Object.keys(v.packs).map(id => `<button type="button" data-packask="${slot}:${id}" aria-pressed="${cur === id}">${esc(nm(id))}</button>`).join('')}</div>${ask}</div>`; }).join('');
  return `<details class="repdet" ${Rep.open || A ? 'open' : ''}><summary><span><b>Your repertoire</b><span>Which system you play in each part of the playbook</span></span></summary>
    <div class="repbody"><p>Switching swaps the lessons, drills and course units for that part. Your progress in the other system is kept, and you can switch back.</p>${rows}</div></details>`;
}
function setPack(slot, id){
  if (PERSONA === 'ready'){ const me = meOf(Prog.d); me.picks = Object.assign({}, me.picks, {[slot]: id}); me.updated = Date.now(); }
  else Prog.d.packs = Object.assign({}, Prog.d.packs, {[slot]: id, updated: Date.now()});
  Prog.save(); try { sessionStorage.removeItem('packs-reload'); } catch(e2){} Rep.ask = null; Settings.close(); syncPacks();
}
const repOk = v => { const t = String(v || '').trim().toLowerCase(), names = repNames(); return !!t && (names.length ? names.includes(t) : t === 'switch'); };
document.addEventListener('click', e => {
  const b = e.target.closest('[data-packask]');
  if (b){ const [slot, id] = b.dataset.packask.split(':'), D = packSlots().find(x => x.slot === slot);
    Rep.ask = D && packOf(D.D, slot) !== id ? {slot, id} : null; Settings.render(); const i = document.getElementById('repName'); if (i) i.focus(); return; }
  if (e.target.closest('[data-repcancel]')){ Rep.ask = null; Settings.render(); }
});
document.addEventListener('toggle', e => { if (e.target.classList && e.target.classList.contains('repdet')) Rep.open = e.target.open; }, true);
document.addEventListener('input', e => { if (e.target.id === 'repName'){ const f = e.target.closest('form'), sb = f && f.querySelector('[type=submit]'); if (sb) sb.disabled = !repOk(e.target.value); } });
document.addEventListener('submit', e => {
  const f = e.target.closest('[data-repform]'); if (!f) return; e.preventDefault();
  const i = f.querySelector('#repName'); if (!Rep.ask || !i || !repOk(i.value)){ if (i){ i.setAttribute('aria-invalid', 'true'); i.focus(); } return; }
  setPack(Rep.ask.slot, Rep.ask.id);
});

// which cards to show: a system card where the player's own habit is not the library's first system, or where the library
// has more than one system to offer; the two style cards always
function makeChoices(P){
  const out = [];
  for (const C of CATALOG){
    const s = P.slots[C.slot]; if (!s || s.n < 5) continue;
    const share = o => o.keys.reduce((a, k) => a + ((s.opts[k] || {}).n || 0), 0), tal = o => o.keys.reduce((a, k) => { const t = s.opts[k]; if (t){ a.n += t.n; a.w += t.w; a.l += t.l; a.d += t.d; } return a; }, {n: 0, w: 0, l: 0, d: 0});
    const top = C.opts.slice().sort((a, b) => share(b) - share(a))[0], own = share(top) / s.n >= 0.3 ? top : null, ready = C.opts.filter(o => o.ready);
    const opts = (own ? [own] : []).concat(ready.filter(o => o !== own)).slice(0, 3);
    if (opts.length < 2) continue;
    out.push({id: C.slot, ask: C.ask, kind: 'system', flip: C.flip, opts: opts.map(o => Object.assign({}, o, {t: tal(o), of: s.n}))});
  }
  for (const Q of STYLE) out.push(Object.assign({kind: 'style'}, Q));
  return out;
}
const defaultPicks = () => ({white: 'e4', blackE4: 'e5', blackD4: 'slav', order: 'leaks', depth: 'core'});

/* ---- text that speaks about the house player's own games is taken out for everyone else */
const PERS = /\b(your games?|in your game|you (lost|won|played|pushed|took|missed|resigned|blundered|had|met|faced)\b|against \S+ (in|on) (jul|aug|sep|oct|nov)|both of your|you have (won|lost)|your last|this exact shot against|your study|(on|in) (jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.? \d|against [a-z][\w-]*\d[\w-]*)/i;
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
  }
  FOOT = '';
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
  }
  const ts = (P.games || []).map(g => g.t).filter(Boolean), a = new Date(Math.min(...ts)), z = new Date(Math.max(...ts)), mo = (d, y) => d.toLocaleDateString(undefined, y ? {month: 'long', year: 'numeric'} : {month: 'long'});
  const span = !ts.length ? '' : mo(a, 1) === mo(z, 1) ? mo(z, 1) : a.getFullYear() === z.getFullYear() ? `${mo(a)} to ${mo(z, 1)}` : `${mo(a, 1)} to ${mo(z, 1)}`;
  const site = (me.src || {}).site === 'lichess' ? 'Lichess' : (me.src || {}).site === 'chess.com' ? 'chess.com' : '';
  FOOT = `${P.user ? P.user + '\'s playbook' : 'Your playbook'}, built from your${site ? ' ' + site : ''} games${span ? ', ' + span : ''}.`;
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
    const months = ((await this.json(base + '/games/archives')).archives || []).reverse().slice(0, 120), out = [];
    for (const m of months){
      const gs = ((await this.json(m)).games || []).filter(g => g.rules === 'chess' && g.pgn && g.time_class !== 'daily' && g.time_class !== 'bullet').reverse();
      for (const g of gs) out.push(g.pgn); tick(out.length); if (out.length >= want) break;
    }
    return out.slice(0, want).join('\n\n');
  },
  async lichess(user, want, tick){
    const r = await fetch(`https://lichess.org/api/games/user/${encodeURIComponent(user.trim())}?max=${want}&perfType=blitz,rapid,classical&clocks=false&evals=false&opening=false`, {headers: {Accept: 'application/x-chess-pgn'}});
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
    if (!Prog.d.badges && PERSONA !== 'new'){ Badges.check(); Prog.saveLocal(); }
    document.querySelectorAll('.tabs button').forEach(b => b.classList.toggle('lock', PERSONA === 'new' && b.dataset.view !== 'sandbox'));
    syncPacks();
  },
  landing(h){ if (PERSONA === 'ready' && (this.me().picks || {}).depth === 'core' && S.dfilter){ DF_PRI = 'core'; S.dfilter.pri = 'core'; }   // drills start with the core lines
    if (PERSONA === 'new' && !OPEN_NEW.includes(S.view)) S.view = 'start'; if (PERSONA === 'new' && PVIEWS.includes(h) && h !== 'reading' && h !== 'built') S.view = (h === 'findings' || h === 'choices') && !this.me().P ? 'start' : h; },
  // after a sign-in merge: if the account turns out to be someone else's kind of playbook, start over with it
  afterMerge(){ if (SITE && !meOf(Prog.d)) Prog.d.me = {state: 'new', since: Date.now()}; if (personaOf(Prog.d) !== PERSONA){ Prog.saveLocal(); location.reload(); return true; } return false; },
  signedOut(){ return Cloud.on() && !Cloud.user; },
  // the chess account named at sign-up: read its games as soon as the account is there (once)
  pendingConnect(){
    const m = (Cloud.user && Cloud.user.user_metadata) || {}; let L = null; try { L = JSON.parse(localStorage.getItem(CONNECT_KEY) || 'null'); } catch(e){}
    return m.chess_user ? {site: m.chess_site, user: m.chess_user} : L && L.user ? L : null;
  },
  autoConnect(){
    if (PERSONA !== 'new' || !Cloud.user || this.busy || this.me().P || this.me().short || this.me().auto || ['reading', 'findings', 'choices', 'built'].includes(S.view)) return false;
    const c = this.pendingConnect(); if (!c) return false;
    try { localStorage.removeItem(CONNECT_KEY); } catch(e){}
    Prog.d.me = Object.assign({}, this.me(), {auto: 1}); Prog.save();
    this.site = c.site === 'lichess' ? 'lichess' : 'chess.com'; this.user = c.user; S.view = 'setup'; setHash(); this.fetchUser(c.user); return true;
  },
  render(){
    const v = S.view;
    view.innerHTML = `<div class="pv">${v === 'start' ? this.startHTML() : v === 'setup' ? this.setupHTML() : v === 'reading' ? this.readingHTML() : v === 'findings' ? this.findingsHTML() : v === 'choices' ? this.choiceHTML() : this.builtHTML()}</div>`;
    this.wire();
  },
  /* -- welcome */
  startHTML(){
    const out = this.signedOut(), has = !!this.me().P, short = !has && this.me().short, step = out ? 1 : has ? 3 : 2, w = fenOf('e4 e5 Nf3 Nc6 Bc4 Bc5 c3 Nf6 d4');
    const cta = out ? `<button class="btn primary" data-acct="signup">Create your account</button><button class="btn" data-acct="signin">I already have an account</button>`
      : has ? `<button class="btn primary" data-pgo="findings">Continue: see what I found</button>` : short ? `<button class="btn primary" data-pgo="setup">Check my games again</button>` : `<button class="btn primary" data-pgo="setup">Connect your account</button>`;
    const li = (k, h, p) => `<li class="${k < step ? 'done' : k === step ? 'now' : ''}"><b>${h}</b><span>${p}</span></li>`;
    const lock = (v, h, p) => `<button class="lockcard" data-view="${v}"><b>${ICON.lock}${h}</b>${p}</button>`;
    return `<section class="whero"><div><p class="kicker">An opening course built from your own games</p>
        <h2>Connect your account.<br>Get <em>your</em> playbook.</h2>
        <p class="lede" style="margin-top:14px">It reads what you already play, where you score and where you leave the book, asks you a few would-you-rather questions, and builds a course in that order. No notation anywhere.</p>
        <div class="cta">${cta}<button class="btn ghost" data-view="sandbox">Try the sandbox first</button></div></div>
      <div class="wart"><div class="board">${boardSVG(w.fen, {coords: false, last: w.last, arrows: ['c4f7r'], flip: false})}</div><p class="wbub">${short ? `Not enough games yet. Play some more and I'll be here.` : `Hi, I'm ${coachName()}. Connect your account and I'll show you your openings.`}</p><div class="wcoach cface">${knightSVG()}</div></div></section>
      <ol class="steps3">${li(1, 'Make an account', 'So your playbook follows you to every device.')}${li(2, 'Connect your chess account', 'Your chess.com or Lichess username. Only your public games are read.')}${li(3, 'Pick your lines', 'A few would-you-rather questions, then your course opens.')}</ol>
      <div><p class="kicker" style="margin-bottom:10px">Opens with your games</p><div class="lockgrid">${lock('course', 'Course', 'One path, ordered by what your games say matters most.')}${lock('drill', 'Drill', 'Five lines a day from memory. Slips come back first.')}${lock('games', 'Your games', 'Results by opening, every lesson, and where you leave the book.')}${lock('cheat', 'Cheat sheet', 'One card per decision.')}</div></div>`;
  },
  locked(tab){
    const T = {course: ['Your course', 'One path through your openings, in the order your games say matters most: the idea, the lines, a drill, practice games and a checkpoint for each.'],
      drill: ['Drill', 'Five lines a day from memory, the ones you slipped on first. Do them every day to keep your streak.'],
      games: ['Your games', 'Your results by opening, every lesson in each one, and the exact positions where you leave your playbook most often.'], cheat: ['Cheat sheet', 'One card per decision: their move, your answer.'],
      shop: ['Shop', 'A wardrobe for your coach, bought with tokens from badges and days in a row.']}[tab] || ['This section', ''];
    const out = this.signedOut(), idx = [LINES[DATA.lessons[0].lines[0]].n.slice(-1)[0], LINES[DATA.lessons[1].lines[0]].n.slice(-1)[0], LINES[DATA.lessons[2].lines[0]].n.slice(-1)[0]];
    view.innerHTML = `<div class="pv"><section class="plocked"><div class="lk">${ICON.lock}</div><p class="kicker">Locked until your games are in</p><h3>${T[0]}</h3><p>${T[1]}</p>
      <div class="cta">${out ? `<button class="btn primary" data-acct="signup">Create your account</button>` : `<button class="btn primary" data-pgo="setup">Connect your account</button>`}<button class="btn" data-view="sandbox">Open the sandbox</button></div>
      <div class="ghost3" aria-hidden="true">${idx.map(i => thumb(i, {coords: false})).join('')}</div></section></div>`;
    this.wire();
  },
  /* -- games in */
  count(){ return this.pool ? (this.pool.match(/^\[Event /gm) || this.pool.match(/^\[White /gm) || []).length : 0; },
  siteName(x){ return (x || this.site) === 'lichess' ? 'Lichess' : 'chess.com'; },
  // too few games that are not bullet: the repertoire waits until there are more
  shortHTML(){
    const sh = this.short || this.me().short || {}, who = sh.user ? `${esc(sh.user)} on ${this.siteName(sh.site)} has so far` : 'these files hold';
    return `<section class="pshort pcard"><div class="say"><div class="cface">${knightSVG('think')}</div><p>Not enough games yet.</p></div>
      <div><h3>Play some more first</h3><p>To build a repertoire I need more of your games than ${who}. Play some more blitz, rapid or classical games, then come back and check again. Bullet games don't count: they're too fast to show what you really know.</p>
        <p class="kicker" style="margin-top:14px">How close you are</p><div class="pbar" style="margin-top:6px" aria-hidden="true"><i style="width:${Math.max(4, Math.min(96, pc(sh.n || 0, NEED)))}%"></i></div>
        <div class="cta" style="display:flex;flex-wrap:wrap;gap:10px;margin-top:16px">${sh.user ? `<button class="btn primary" data-recheck>Check again</button>` : ''}<button class="btn" data-other>Use another username</button><button class="btn ghost" data-view="sandbox">Open the sandbox</button></div></div></section>`;
  },
  setupHTML(){
    if (this.signedOut()) return `<section class="plocked"><div class="lk">${ICON.lock}</div><h3>First, an account</h3><p>Your games and your playbook are kept with your account, so they are there on every device.</p><div class="cta"><button class="btn primary" data-acct="signup">Create your account</button><button class="btn" data-acct="signin">Sign in</button></div></section>`;
    const seg = (v, l) => `<button type="button" data-site="${v}" aria-pressed="${this.site === v}">${l}</button>`;
    const month = new Date().toISOString().slice(0, 7).replace('-', '/');
    if (!this.busy && (this.short || (this.me().short && !this.fresh))) return `<div class="chead"><div><p class="kicker">Step 2 of 3</p><h2 style="font-size:clamp(30px,4vw,46px)">Connect your chess account</h2></div></div>${this.shortHTML()}`;
    return `<div class="chead"><div><p class="kicker">Step 2 of 3</p><h2 style="font-size:clamp(30px,4vw,46px)">Connect your chess account</h2><p>I read your recent blitz, rapid and classical games to see what you really play. Bullet is skipped: it's too fast to show what you know.</p></div></div>
      ${this.msg ? `<p class="pmsg ${this.msg.bad ? 'bad' : 'ok'}" role="status">${esc(this.msg.t)}</p>` : ''}${this.busy ? `<div class="pbar" aria-hidden="true" style="margin-top:0"><i id="fetchbar" style="width:3%"></i></div>` : ''}
      <div class="pcard pickc"><div><h3>Pick your coach</h3><p>They say the same things. Change your mind any time in Settings.</p></div>${coachPickHTML()}</div>
      ${this.names ? `<div class="pcard"><b>Which one is you?</b><div class="pwho" style="margin-top:10px">${this.names.map(x => `<button class="btn" data-who="${esc(x)}">${esc(x)}</button>`).join('')}</div></div>` : ''}
      <div class="setup"><form class="pcard" id="uform"><h3>Your username</h3>
          <div class="setseg" role="group" aria-label="Where you play">${seg('chess.com', 'chess.com')}${seg('lichess', 'Lichess')}</div>
          <div class="pfield"><label for="uname">Your username on ${this.site === 'lichess' ? 'Lichess' : 'chess.com'}</label><input type="text" id="uname" autocomplete="off" autocapitalize="off" spellcheck="false" value="${esc(this.user)}" placeholder="for example: ${this.site === 'lichess' ? 'your_lichess_name' : 'your_chesscom_name'}"></div>
          <button class="btn primary" type="submit" ${this.busy ? 'disabled' : ''} style="justify-content:center;min-height:46px">${this.busy ? 'Reading your games…' : 'Connect and read my games'}</button>
          <p style="color:var(--muted);font-size:13.5px">Only your public games are read, straight from ${this.site === 'lichess' ? 'Lichess' : 'chess.com'} to this page. Nothing is posted and no password is needed.</p></form>
        <div class="pcard"><h3>No account online? Drop a PGN file</h3>
          <label class="drop" id="drop"><input type="file" id="pgnFile" accept=".pgn,.txt,text/plain" multiple><b>Drop PGN files here, or tap to choose</b><span>Several files are fine. They add up.</span></label>
          <details class="how"><summary>How do I get a PGN file?</summary>
            <ol><li><b>chess.com:</b> open this address in your browser with your own name in it, once for each month you need. Each one downloads a file.<br><code>api.chess.com/pub/player/YOUR_NAME/games/${month}/pgn</code></li>
              <li><b>Lichess:</b> open your profile, press the download button above your games, and choose "Export games".</li><li>Drop every file you got into the box above.</li></ol></details></div></div>`;
  },
  async fetchUser(name){
    const u = String(name !== undefined ? name : ((document.getElementById('uname') || {}).value || '')).trim(); this.user = u; if (!u){ this.msg = {bad: 1, t: 'Type your username first.'}; return render(); }
    this.busy = true; this.short = null; this.fresh = true; this.pool = ''; this.msg = {t: `Looking for ${u} on ${this.siteName()}…`}; render();
    try {
      const text = await Importer[this.site === 'lichess' ? 'lichess' : 'chesscom'](u, TAKE, n => { const r = document.getElementById('fetchbar'); if (r) r.style.width = Math.max(3, Math.min(100, pc(n, NEED))) + '%'; });
      this.busy = false; this.pool = text; this.src = {site: this.site, user: u.toLowerCase()}; this.ingest(u.toLowerCase());
    } catch(e){
      this.busy = false;
      this.msg = {bad: 1, t: e.missing ? `There is no player called "${u}" on ${this.siteName()}. Check the spelling.` : `Couldn't reach ${this.siteName()} from this page. Use a PGN file instead: the steps are under "How do I get a PGN file?"`}; render();
    }
  },
  async addFiles(files){
    const texts = await Promise.all([...files].map(f => f.text().catch(() => '')));
    this.pool = [this.pool].concat(texts).filter(Boolean).join('\n\n'); this.src = this.src && this.src.site !== 'pgn' ? this.src : {site: 'pgn', user: ''}; this.ingest(this.src.user);
  },
  // enough games and a known player: read them. Otherwise say what is missing.
  ingest(user){
    const raw = Analyze.parsePGN(this.pool); this.names = null;
    if (!raw.length){ this.msg = {bad: 1, t: this.src && this.src.site !== 'pgn' ? 'No games came back for that name.' : 'No games found in that. A PGN file starts with lines like [Event "…"].'}; if (this.src && this.src.site !== 'pgn') return this.tooFew(this.src.user, 0); return render(); }
    user = (user || Analyze.guessUser(raw) || '').toLowerCase();
    if (!user){ const c = {}; for (const g of raw) for (const k of ['White', 'Black']) if (g.h[k]) c[g.h[k]] = (c[g.h[k]] || 0) + 1; this.names = Object.keys(c).sort((a, b) => c[b] - c[a]).slice(0, 4); this.msg = {t: 'Those games are not all by one player, so tell me who you are.'}; return render(); }
    const all = raw.filter(g => (g.h.White || '').toLowerCase() === user || (g.h.Black || '').toLowerCase() === user), mine = all.filter(g => !isFast(g));
    const key = g => (g.h.UTCDate || g.h.Date || '') + (g.h.UTCTime || g.h.StartTime || ''); mine.sort((a, b) => key(b) < key(a) ? -1 : 1);
    if (!all.length){ this.msg = {bad: 1, t: `None of those games were played by "${user}".`}; return render(); }
    if (mine.length < this.need) return this.tooFew(user, mine.length);
    if (this.me().short){ const m = Object.assign({}, this.me()); delete m.short; Prog.d.me = m; }
    this.read(mine.slice(0, TAKE), user);
  },
  need: NEED,
  // not enough games yet: say so, keep it with the account so the welcome screen remembers, and wait
  tooFew(user, n){
    this.short = {site: (this.src || {}).site || this.site, user: (this.src || {}).site === 'pgn' ? '' : user, n, at: Date.now()};
    Prog.d.me = Object.assign({}, this.me(), {state: 'new', short: this.short}); Prog.save(); this.msg = null; this.pool = (this.src || {}).site === 'pgn' ? this.pool : '';
    S.view = 'setup'; render(); setHash();
  },
  /* -- the reading screen: the analysis runs while the board plays through the games */
  STAGES: ['Reading your games', 'Sorting them by opening', 'Measuring where you score', 'Finding where you leave the book', 'Building your playbook'],
  readingHTML(){
    return `<section class="proc"><div class="board" id="pboard">${boardSVG(N[0].f, {coords: false})}</div>
      <div><p class="kicker">Step 2 of 3 · a few seconds</p><h2 style="font-size:clamp(30px,4vw,48px)">Reading your games</h2>
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
    const P = await Analyze.run(raw, user, {w: BOOKS.w.full, b: BOOKS.b.full}, p => { if (p.last && queue.length < 40) queue.push(p.last.ucis); stage(0, `${p.done} of ${p.of}`); const b = document.getElementById('pbar'); if (b) b.style.width = (p.done / p.of * 20) + '%'; });
    if (S.view !== 'reading'){ clearInterval(anim); return; }
    await wait(Math.max(0, 1500 - (Date.now() - t0)));
    const top = side => Object.entries(side.systems).sort((a, b) => b[1].n - a[1].n)[0], cn = (s, id) => (BOOKS[s].chapters.find(c => c.id === id) || {}).name || id;
    stage(1, `${Object.keys(P.white.systems).length + Object.keys(P.black.systems).length} openings`);
    const tw = top(P.white), tb = top(P.black); say(tw ? `With White you land in the ${cn('w', tw[0])} most: ${plural(tw[1].n, 'game')}.` : `${P.white.all.n} games with White, ${P.black.all.n} with Black.`); await wait(1500);
    stage(2, `${pc(P.all.w + P.all.d / 2, P.all.n)}% overall`); say(P.facts[0] ? P.facts[0].text : `You score ${pc(P.all.w + P.all.d / 2, P.all.n)}% over these ${P.n} games.`); await wait(1700);
    stage(3, plural(P.leaks.length, 'spot')); say(P.leaks[0] ? `One position came up ${plural(P.leaks[0].n, 'time')} and you left the playbook the same way each time. We'll fix that one first.` : 'You stay in the book longer than most.'); await wait(1700);
    stage(4); say(tb ? `Against you, White goes for the ${cn('b', tb[0])} most. Nearly done.` : 'Nearly done.'); await wait(1300);
    stage(5); clearInterval(anim);
    this.pool = ''; this.short = null; Prog.d.me = {state: 'new', since: this.me().since || Date.now(), updated: Date.now(), src: this.src || {site: 'pgn', user}, P}; Prog.save();
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
      <div class="duo${Q.opts.length > 2 ? ' trio' : ''}">${Q.opts.map(opt).join('<span class="or">or</span>')}</div>
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
    return `<section class="done-art"><div class="cface pop">${knightSVG('cheer')}</div><p class="kicker">Built from your games</p><h2>Your playbook is <em>ready</em>.</h2>
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
    view.innerHTML = `<div class="pv"><div class="chead"><div><p class="kicker">Your games${P.user ? ' · ' + esc(P.user) : ''}</p><h2 style="font-size:clamp(30px,4vw,44px)">What actually happened</h2><p>Your games, read without an engine: what you met, how it went, and where your moves and your playbook part ways. Open an opening for every lesson in it.</p></div>
        <button class="btn" data-pgo="setup">Read my newer games</button></div>
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
    const rc = view.querySelector('[data-recheck]'); if (rc) rc.onclick = () => { const sh = this.short || this.me().short || {}; this.site = sh.site === 'lichess' ? 'lichess' : 'chess.com'; this.fetchUser(sh.user); };
    const ot = view.querySelector('[data-other]'); if (ot) ot.onclick = () => { this.short = null; this.fresh = true; this.pool = ''; this.msg = null; render(); };
    const op = view.querySelector('[data-open]'); if (op) op.onclick = () => { try { history.replaceState(null, '', '#course'); } catch(e){} location.reload(); };
    const f = document.getElementById('uform'); if (f) f.onsubmit = e => { e.preventDefault(); if (!this.busy) this.fetchUser(); };
    const inp = document.getElementById('pgnFile'), drop = document.getElementById('drop');
    if (inp) inp.onchange = () => { if (inp.files.length) this.addFiles(inp.files); };
    if (drop){ drop.ondragover = e => { e.preventDefault(); drop.classList.add('over'); }; drop.ondragleave = () => drop.classList.remove('over'); drop.ondrop = e => { e.preventDefault(); drop.classList.remove('over'); if (e.dataTransfer.files.length) this.addFiles(e.dataTransfer.files); }; }
  }
};

/* ---- badges: earned from the progress, kept with it (d.badges: id -> when), shown in the profile. Locked ones are grey. */
const BADGES = [
  {id: 'l1', group: 'Lines you know', name: 'First line', need: 'Play a line from memory without a slip.', tier: 'bronze', glyph: '1', n: x => x.clean, at: 1},
  {id: 'l10', group: 'Lines you know', name: 'Ten lines', need: 'Ten lines played without a slip.', tier: 'bronze', glyph: '10', n: x => x.clean, at: 10},
  {id: 'l25', group: 'Lines you know', name: 'Twenty-five lines', need: 'Twenty-five lines played without a slip.', tier: 'silver', glyph: '25', n: x => x.clean, at: 25},
  {id: 'l50', group: 'Lines you know', name: 'Fifty lines', need: 'Fifty lines played without a slip.', tier: 'silver', glyph: '50', n: x => x.clean, at: 50},
  {id: 'l100', group: 'Lines you know', name: 'A hundred lines', need: 'A hundred lines played without a slip.', tier: 'gold', glyph: '100', n: x => x.clean, at: 100},
  {id: 'l250', group: 'Lines you know', name: 'The whole library', need: 'Two hundred and fifty lines played without a slip.', tier: 'gold', glyph: '250', n: x => x.clean, at: 250},
  {id: 's3', group: 'Streak', name: 'Three in a row', need: 'Five lines a day, three days running.', tier: 'bronze', glyph: 'flame', n: x => x.best, at: 3},
  {id: 's7', group: 'Streak', name: 'A full week', need: 'Five lines a day for a week.', tier: 'silver', glyph: 'flame', n: x => x.best, at: 7},
  {id: 's30', group: 'Streak', name: 'A month', need: 'Five lines a day for thirty days.', tier: 'gold', glyph: 'flame', n: x => x.best, at: 30},
  {id: 's100', group: 'Streak', name: 'A hundred days', need: 'Five lines a day for a hundred days.', tier: 'gold', glyph: 'crown', n: x => x.best, at: 100},
  {id: 'u1', group: 'Course', name: 'First checkpoint', need: 'Pass a unit\'s checkpoint.', tier: 'bronze', glyph: 'flag', n: x => x.units, at: 1},
  {id: 'u5', group: 'Course', name: 'Five units', need: 'Pass five units of your course.', tier: 'silver', glyph: 'flag', n: x => x.units, at: 5},
  {id: 'uall', group: 'Course', name: 'Course complete', need: 'Pass every open unit of your course.', tier: 'gold', glyph: 'star', n: x => x.units, at: x => x.open},
  {id: 'x1', group: 'Course', name: 'Deep diver', need: 'Finish a deep dive.', tier: 'silver', glyph: 'flag', n: x => x.deep, at: 1},
  {id: 'x3', group: 'Course', name: 'Three deep dives', need: 'Finish three deep dives.', tier: 'gold', glyph: 'crown', n: x => x.deep, at: 3},
  {id: 'm10', group: 'Practice', name: 'Solid ten', need: 'Ten lines clean on four reviews in a row.', tier: 'silver', glyph: 'star', n: x => x.solid, at: 10},
  {id: 'm50', group: 'Practice', name: 'Solid fifty', need: 'Fifty lines clean on four reviews in a row.', tier: 'gold', glyph: 'star', n: x => x.solid, at: 50},
  {id: 'g10', group: 'Practice', name: 'Sparring partner', need: 'Ten practice games in the Sandbox.', tier: 'bronze', glyph: 'board', n: x => x.spar, at: 10}
];
const badgeNeed = (B, x) => typeof B.at === 'function' ? B.at(x) : B.at;
function badgeStats(){
  let clean = 0, solid = 0; for (const id in (Prog.d.lines || {})){ const r = Prog.rec(id); if (!r) continue; if (r.clean) clean++; if ((r.box || 0) >= 4) solid++; }
  const open = COURSE.filter(U => !U.soon);
  return {clean, solid, best: Daily.best(), units: open.filter(unitPassed).length, open: Math.max(1, open.length), spar: (Prog.d.sb || {}).games || 0, deep: DEEP.filter(deepDone).length};
}
// a medal: two ribbons and a struck disc; the glyph is a number or a small picture. Locked ones are drawn in grey.
function medalSVG(tier, glyph){
  const t = tier === 'locked' ? ['locked', 'locked-2', 'locked', 'locked'] : [tier, tier + '-2', 'ribbon-1', 'ribbon-2'], c = k => `var(--${t[k]})`;
  const G = {flame: '<path d="M33 31c.3 2.6-.9 4-2.3 5.5-1.5 1.6-3 3.2-3 5.9 0 3.2 2.1 5.6 4.6 5.6s4.7-2.2 4.7-5.3c0-2.3-1.2-3.8-2-4.8-.2 1.2-.7 2.2-1.6 2.6.5-3.1-.2-6.1-.4-9.5z"/>',
    crown: '<path d="M23 50l-2-12 6 5 5-8 5 8 6-5-2 12z"/>', flag: '<path d="M27 52V32h2v1.5c4-2.5 7 1.5 11-.5v10c-4 2-7-2-11 .5V52z"/>',
    star: '<path d="M32 31.5l3.1 6.4 7 1-5.1 4.9 1.2 7-6.2-3.3-6.2 3.3 1.2-7-5.1-4.9 7-1z"/>', board: '<path d="M24 34h8v8h-8zM32 42h8v8h-8z"/><path d="M24 34h16v16H24z" fill="none" stroke-width="1.6"/>',
    lock: '<rect x="26" y="40" width="12" height="9" rx="1.6"/><path d="M28.5 40v-3a3.5 3.5 0 0 1 7 0v3" fill="none" stroke-width="2"/>'};
  const g = tier === 'locked' ? G.lock : G[glyph] || `<text x="32" y="${glyph.length > 2 ? 46.5 : 47.5}" text-anchor="middle" font-size="${glyph.length > 2 ? 12.5 : 15}">${glyph}</text>`;
  return `<svg class="medal" viewBox="0 0 64 76" aria-hidden="true"><path d="M16 2h14l6 26-12 4z" style="fill:${c(2)}"/><path d="M48 2H34l-6 26 12 4z" style="fill:${c(3)}"/>
    <circle cx="32" cy="45" r="22" style="fill:${c(1)};stroke:${c(0)}" stroke-width="3"/><circle cx="32" cy="45" r="16.5" fill="none" style="stroke:${c(0)}" stroke-width="1.2" stroke-dasharray="2 2.2"/>
    <g class="mg" style="fill:${c(0)};stroke:${c(0)}" font-family="var(--f-display)" font-weight="700">${g}</g><path d="M17.5 37a16 16 0 0 1 9-9.5" fill="none" stroke="#fff" stroke-opacity=".55" stroke-width="2.4" stroke-linecap="round"/></svg>`;
}
const Badges = {
  queue: [], n: 0,
  // stamp what has just been earned; the coach shows it at the next quiet moment. The first check after an update
  // stamps what was earned before it quietly.
  check(){
    const first = !Prog.d.badges, have = Prog.d.badges || {}, x = badgeStats(), now = Date.now(), got = [];
    for (const B of BADGES) if (!have[B.id] && B.n(x) >= badgeNeed(B, x)) { have[B.id] = now; got.push(B); }
    if (!got.length && !first) return false;
    Prog.d.badges = have;
    const loud = got.filter(B => !(B.id === 'uall' && S.gradNow));
    if (!first && loud.length && PERSONA !== 'new'){ this.n++; this.queue.push(...loud); if (!(S.drill && S.drill.state === 'play')) this.show(); }
    return true;
  },
  show(){
    if (S.view === 'grad' || libOn()) return;                                      // the coach is on that page already; it waits
    const rank = x => x.id === 's7' ? -1 : {gold: 0, silver: 1, bronze: 2}[x.tier];   // the week that opens the wardrobe says so first
    const B = this.queue.slice().sort((a, b) => rank(a) - rank(b))[0]; if (!B) return;
    const more = this.queue.length - 1; this.queue = [];
    if (!SET.coach){ toast(`New badge: ${B.name}${more ? ` and ${more} more` : ''}.`); return; }
    Coach.say(`${B.need} ${more ? `And ${more} more ${more === 1 ? 'badge' : 'badges'} with it: ${more + 1} shop tokens.` : 'That\'s a shop token too.'}${B.id === 's7' ? ' And my wardrobe is open now.' : ''}`, {mood: 'cheer', stay: true, head: `New badge: ${B.name}`, art: `<span class="cmedal">${medalSVG(B.tier, B.glyph)}</span>`, cta: B.id === 's7' ? ['shop', 'Open the shop'] : ['me', 'See your badges']});
  }
};
// the profile: the streak, the last seven days and every badge, earned or not
function profileHTML(){
  const st = Daily.streak(), best = Math.max(st, Daily.best()), k = Math.min(DAILY, Daily.count()), have = Prog.d.badges || {}, x = badgeStats();
  const got = BADGES.filter(B => have[B.id]).length, groups = [...new Set(BADGES.map(B => B.group))];
  const week = [-6, -5, -4, -3, -2, -1, 0].map(o => { const d = dayDate(o), on = Daily.done(o); return `<li class="${on ? 'on' : ''} ${o === 0 ? 'now' : ''}"><i>${on ? ICON.check : ''}</i><span>${d.toLocaleDateString(undefined, {weekday: 'narrow'})}</span></li>`; }).join('');
  const one = B => { const at = have[B.id], need = badgeNeed(B, x), cur = Math.min(need, B.n(x));
    return `<li class="bdg ${at ? 'got' : 'lock'}" title="${esc(B.need)}">${medalSVG(at ? B.tier : 'locked', B.glyph)}<b>${esc(B.name)}</b><span>${at ? 'Earned ' + new Date(at).toLocaleDateString(undefined, {month: 'short', day: 'numeric', year: 'numeric'}) : esc(B.need)}</span>${at ? '' : `<i class="bprog" aria-hidden="true"><i style="width:${Math.round(cur / need * 100)}%"></i></i>`}</li>`; };
  return `<div class="prof"><div class="pstreak ${st ? '' : 'zero'}">${FLAME}<div><b class="tnum">${st}</b><span>${st === 1 ? 'day' : 'days'} in a row</span></div><p>Best: ${best} · today: ${k} of ${DAILY} lines</p></div>
    <ol class="week" aria-label="The last seven days">${week}</ol>
    <div class="bdgs"><p class="kicker">Badges · ${got} of ${BADGES.length}</p>${groups.map(g => `<div><p class="bgh">${esc(g)}</p><ul class="bgrid">${BADGES.filter(B => B.group === g).map(one).join('')}</ul></div>`).join('')}</div></div>`;
}

/* ---- the shop. Tokens are worked out from the progress (badges earned, days in a row) minus what has been bought,
   so every device shows the same number. d.shop.own: item -> when bought; d.shop.wear: slot -> [item, when]. */
const SHOP = [
  {id: 'c-classic', slot: 'skin', name: 'Classic', price: 0},
  {id: 'c-midnight', slot: 'skin', name: 'Midnight', price: 2},
  {id: 'c-ruby', slot: 'skin', name: 'Ruby', price: 2},
  {id: 'c-plum', slot: 'skin', name: 'Plum', price: 2},
  {id: 'c-tangerine', slot: 'skin', name: 'Tangerine', price: 2},
  {id: 'c-gold', slot: 'skin', name: 'Gold leaf', price: 4, needs: 's30'},
  {id: 'h-cap', slot: 'head', name: 'Cap', price: 1},
  {id: 'h-beanie', slot: 'head', name: 'Beanie', price: 1},
  {id: 'h-party', slot: 'head', name: 'Party hat', price: 1},
  {id: 'h-tophat', slot: 'head', name: 'Top hat', price: 3},
  {id: 'h-wizard', slot: 'head', name: 'Wizard hat', price: 3, needs: 'l50'},
  {id: 'h-grad', slot: 'head', name: 'Graduation cap', price: 2, needs: 'uall'},
  {id: 'h-crown', slot: 'head', name: 'Crown', price: 5, needs: 's30'},
  {id: 'f-glasses', slot: 'face', name: 'Reading glasses', price: 1},
  {id: 'f-shades', slot: 'face', name: 'Sunglasses', price: 2},
  {id: 'f-monocle', slot: 'face', name: 'Monocle', price: 2, needs: 'm10'},
  {id: 'n-bowtie', slot: 'neck', name: 'Bow tie', price: 1},
  {id: 'n-scarf', slot: 'neck', name: 'Scarf', price: 2},
  {id: 'n-medal', slot: 'neck', name: 'Medal', price: 2, needs: 'u1'}
];
const SLOTS = [['skin', 'Colours'], ['head', 'Hats'], ['face', 'Glasses'], ['neck', 'Round the neck']];
const COIN = '<svg class="coin" viewBox="0 0 20 20" aria-hidden="true"><circle cx="10" cy="10" r="9"/><circle class="c2" cx="10" cy="10" r="6.4"/><path class="c3" d="M10 5.6l1.3 2.7 3 .4-2.2 2.1.5 2.9L10 12.3l-2.6 1.4.5-2.9-2.2-2.1 3-.4z"/></svg>';
const Shop = {
  st(){ const s = Prog.d.shop || (Prog.d.shop = {own: {}, wear: {}}); s.own = s.own || {}; s.wear = s.wear || {}; return s; },
  // every run of days with five lines, oldest first
  runs(){ const ks = Object.keys(Prog.d.days || {}).filter(k => Daily.n(k) >= DAILY).sort(), out = []; let prev = null;
    for (const k of ks){ if (prev && dkey(dayDate(1, prev)) === k) out[out.length - 1]++; else out.push(1); prev = k; } return out; },
  earned(){ const have = Prog.d.badges || {}, r = this.runs();
    return {badges: BADGES.filter(B => have[B.id]).length, streak: r.reduce((a, n) => a + Math.floor(n / 3), 0), week: Math.max(0, ...r) >= 7 ? 1 : 0}; },
  spent(){ return Object.keys(this.st().own).reduce((a, id) => a + ((SHOP.find(i => i.id === id) || {}).price || 0), 0); },
  total(){ const e = this.earned(); return e.badges + e.streak + e.week; },
  balance(){ return Math.max(0, this.total() - this.spent()); },
  isOpen(){ return Math.max(...this.runs(), 0) >= 7; },
  owns(id){ return id === 'c-classic' || !!this.st().own[id]; },
  worn(){ const w = (Prog.d.shop || {}).wear || {}, g = s => (w[s] || [])[0] || null; return {skin: g('skin') || 'c-classic', head: g('head'), face: g('face'), neck: g('neck')}; },
  lockOf(I){ if (!I.price) return ''; if (!this.isOpen()) return 'week'; if (I.needs && !(Prog.d.badges || {})[I.needs]) return 'badge'; return ''; },
  put(id){ const I = SHOP.find(x => x.id === id); if (!I || !this.owns(id)) return; this.st().wear[I.slot] = [id, Date.now()]; Prog.save(); },
  off(slot){ this.st().wear[slot] = [slot === 'skin' ? 'c-classic' : null, Date.now()]; Prog.save(); },
  buy(id){
    const I = SHOP.find(x => x.id === id); if (!I || this.owns(id) || this.lockOf(I) || this.balance() < I.price) return false;
    this.st().own[id] = Date.now(); this.st().wear[I.slot] = [id, Date.now()]; Prog.save(); return true;
  }
};
// the shop page: the coach in what they wear, the tokens and where they come from, then every item by slot
function renderShop(){
  const view = document.getElementById('view'), bal = Shop.balance(), e = Shop.earned(), open = Shop.isOpen(), L = Shop.worn(), who = coachWho().id;
  const st = Daily.streak(), toNext = 3 - (st % 3), best = Math.max(0, ...Shop.runs());
  const card = I => {
    const lk = Shop.lockOf(I), own = Shop.owns(I.id), on = L[I.slot] === I.id, B = I.needs && BADGES.find(x => x.id === I.needs);
    const look = Object.assign({}, L, {[I.slot]: I.id});
    const needB = B && !(Prog.d.badges || {})[B.id];
    const act = needB ? `<span class="need">Needs the badge “${esc(B.name)}”</span>` : lk ? '' : on ? (I.slot === 'skin' && I.id === 'c-classic' ? '<span class="wearing">Wearing</span>' : `<button class="btn small" data-off="${I.slot}">Take off</button>`)
      : own ? `<button class="btn small" data-wear="${I.id}">Wear</button>` : `<button class="btn small primary" data-buy="${I.id}" ${bal < I.price ? 'disabled' : ''}>${COIN}${I.price}</button>`;
    return `<li class="item ${lk ? 'lock' : ''} ${on ? 'on' : ''}"><span class="ipv">${knightSVG('', who, look)}</span><b>${esc(I.name)}</b>${own && !on && I.id !== 'c-classic' ? '<span class="owned">Yours</span>' : !own && lk === 'week' && I.price && !needB ? `<span class="price">${COIN}${I.price}</span>` : ''}${act}</li>`;
  };
  const days = Array.from({length: 7}, (_, k) => `<i class="${k < Math.min(7, st) ? 'on' : ''}"></i>`).join('');
  view.innerHTML = `<div class="chead"><div><p class="kicker">Shop</p><h2 style="font-size:clamp(30px,4vw,46px)">${esc(coachName())}'s wardrobe</h2><p>Tokens come from badges and from days in a row. Spend them on a new look for your coach.</p></div></div>
    <div class="shop">
      <aside class="shopside">
        <div class="mannequin">${knightSVG('cheer', who, L)}</div>
        <p class="bal">${COIN}<b class="tnum">${bal}</b><span>${bal === 1 ? 'token' : 'tokens'}</span></p>
        <ul class="earn"><li><span>Badges</span><b class="tnum">${e.badges}</b></li><li><span>Every three days in a row</span><b class="tnum">${e.streak}</b></li><li><span>Your first full week</span><b class="tnum">${e.week}</b></li>${Shop.spent() ? `<li class="sp"><span>Spent</span><b class="tnum">−${Shop.spent()}</b></li>` : ''}</ul>
        <p class="nextt">${st ? `${toNext === 3 ? 'Three' : toNext === 2 ? 'Two' : 'One'} more ${toNext === 1 ? 'day' : 'days'} in a row for the next token.` : 'Five lines today starts a streak: every third day in a row is a token.'}</p>
        <div class="coachpick mini">${COACHES.map(c => `<button type="button" data-coachwho="${c.id}" aria-pressed="${who === c.id}"><span class="cface">${knightSVG('', c.id, L)}</span><b>${c.name}</b></button>`).join('')}</div>
      </aside>
      <div class="shopmain">
        ${open ? '' : `<section class="wlock"><div><p class="kicker">Locked</p><h3>The wardrobe opens after a week in a row</h3><p>Five lines a day for seven days running, and every item here can be bought. Your tokens wait for you until then.</p></div>
          <div class="wdays" aria-label="${Math.min(7, st)} of 7 days">${days}<span>${best >= 7 ? '' : `${Math.min(7, st)} of 7`}</span></div></section>`}
        ${SLOTS.map(([slot, name]) => `<section class="slot"><h3>${name}</h3><ul class="items">${SHOP.filter(I => I.slot === slot).map(card).join('')}</ul></section>`).join('')}
      </div>
    </div>`;
  view.querySelectorAll('[data-buy]').forEach(b => b.onclick = () => { const I = SHOP.find(x => x.id === b.dataset.buy); if (Shop.buy(I.id)){ renderShop(); Coach.say(`${I.name}? Suits me. Thank you.`, {mood: 'cheer', ms: 5000}); } });
  view.querySelectorAll('[data-wear]').forEach(b => b.onclick = () => { Shop.put(b.dataset.wear); renderShop(); Coach.refresh(); });
  view.querySelectorAll('[data-off]').forEach(b => b.onclick = () => { Shop.off(b.dataset.off); renderShop(); Coach.refresh(); });
}

/* ---- the coach: a few words in a speech bubble, bottom right. Never a hint while you are being tested. */
/* ---- after the first course: the big moment, then a library. The coach picks three deep dives for each player: the
   openings they meet most, weighed by how the course went there (slips in drills and practice games, the checkpoint,
   the results in those games). The reason shown is the strongest of them. */
const libOn = () => S.view === 'course' && !!gradAt() && !S.coursePath && !(S.deep && DEEPOF[S.deep]);
const shareWords = s => s >= .45 ? 'Nearly half' : s >= .3 ? 'About a third' : s >= .22 ? 'About a quarter' : s >= .17 ? 'About one in five'
  : s >= .12 ? 'About one in eight' : s >= .07 ? 'About one in twelve' : s >= .02 ? 'A few' : '';
const chaptersOfAll = U => [...new Set(U.lessons.concat(U.deeper || []).map(l => { const L = LIDX[U.side][l], p = L && BOOKS[U.side].parts.find(x => x.id === L.part); return p && p.ch; }).filter(Boolean))];
const dayFmt = t => new Date(t).toLocaleDateString(undefined, {month: 'short', day: 'numeric', year: 'numeric'});
function deepRank(){
  const rows = [], held = {};   // a chapter's games are shared among the units that teach it, by how many of its lessons each holds
  for (const U of COURSE) if (U.lessons && !U.soon) for (const l of U.lessons.concat(U.deeper || [])){
    const L = LIDX[U.side][l], p = L && BOOKS[U.side].parts.find(x => x.id === L.part); if (!p) continue;
    const k = U.side + ':' + p.ch, h = held[k] || (held[k] = {}); h[U.id] = (h[U.id] || 0) + 1; }
  for (const X of DEEP){
    const B = UNIT[X.base]; if (!B || B.soon) continue;
    const D = BOOKS[X.side], t = {n: 0, w: 0, l: 0, d: 0};
    for (const c of chaptersOfAll(B)){ const C = D.chapters.find(x => x.id === c), st = C && C.stats, h = held[X.side + ':' + c] || {}, f = (h[B.id] || 0) / (Object.values(h).reduce((a, v) => a + v, 0) || 1);
      if (st){ t.n += (st.n || 0) * f; t.w += (st.w || 0) * f; t.l += (st.l || 0) * f; t.d += (st.d || 0) * f; } }
    const tot = (D.stats && D.stats.total) || D.chapters.reduce((a, C) => a + ((C.stats || {}).n || 0), 0);
    let seen = 0, slips = 0;
    for (const id of unitAllLines(B)){ const r = Prog.d.lines[id]; if (r){ seen += r.seen || 0; slips += Math.max(0, (r.seen || 0) - (r.clean || 0)); } }
    const p = up(B.id), games = p.sparGames || 0, bad = Math.max(0, games - (p.spar || 0)), of = B.quiz ? B.quiz.length : 6, cp = Math.min(of, p.cp || 0), share = tot ? t.n / tot : 0;
    const weak = .4 * (seen ? slips / seen : 0) + .25 * (games ? bad / games : 0) + .2 * Math.min(1, 3 * (of - cp) / of) + .15 * (t.n ? 1 - scoreOf(t) : .5);
    rows.push({X, B, t, share, seen, slips, games, bad, cp, of, need: (share + .03) * (.5 + weak), done: deepDone(X), touched: deepTouched(X), cur: deepCur(X)});
  }
  const most = Math.max(0, ...rows.map(o => o.slips)), low = Math.min(1, ...rows.map(o => o.cp ? o.cp / o.of : 1));
  for (const o of rows) o.why = deepWhy(o, most, low);
  return rows.sort((a, b) => b.need - a.need);
}
function deepWhy(o, most, low){
  const a = shareWords(o.share), side = o.X.side === 'w' ? 'White' : 'Black';
  const b = o.slips >= 3 && o.slips === most ? 'you slipped on its lines more than anywhere else in your course'
    : o.cp && o.cp < o.of && o.cp / o.of === low ? `its checkpoint was your lowest, ${o.cp} of ${o.of}`
    : o.bad >= 2 ? `${o.bad} of your practice games there had a slip`
    : o.slips >= 3 ? `you slipped on its lines ${o.slips} times`
    : o.t.n >= 5 && o.t.l > o.t.w ? 'you lose more of those games than you win' : '';
  return a && b ? `${a} of your ${side} games go this way, and ${b}.` : a ? `${a} of your ${side} games go this way.` : b ? `${b[0].toUpperCase()}${b.slice(1)}.` : 'More lines from an opening in your course.';
}
const deepLessons = X => X.units.reduce((a, U) => a + U.lessons.length, 0);
// the deep dives shown: the coach's pick, then up to two already started, then the next best; the rest wait folded away
function libCards(rank){
  const live = rank.filter(o => !o.done), pick = live[0] || null, out = pick ? [pick] : [];
  for (const o of live.filter(o => o.touched && o !== pick).sort((a, b) => b.touched - a.touched).slice(0, 2)) out.push(o);
  for (const o of live) if (out.length < 3 && !out.includes(o)) out.push(o);
  return {pick, cards: out, rest: live.filter(o => !out.includes(o))};
}
function deepCard(o, top){
  const X = o.X, U0 = X.units[0], cur = o.cur;
  const cta = o.touched && cur ? `Continue: ${unitNo(cur).toLowerCase()}` : 'Start';
  return `<li class="dcard ${top ? 'dpick' : ''}"><button type="button" data-deep="${X.id}" aria-label="${esc(X.title)}, deep dive${top ? ', the coach\'s pick' : ''}">
    <span class="dtop"><span class="dthumb">${slideSVG(U0, U0.idea[0], {coords: false, mini: true})}</span>
      <span class="dhead"><span class="chips">${sideChip(U0)}${top ? `<span class="chip pick">${esc(coachName())}'s pick</span>` : o.touched ? '<span class="chip">Started</span>' : ''}</span><b>${esc(X.title)}</b><span class="dtag">${esc(X.tag)}</span></span></span>
    <span class="dwhy">${esc(o.why)}</span>
    <span class="dfoot"><span class="dmeta"><span class="pips" aria-hidden="true">${X.units.map(U => `<i class="${unitPassed(U) ? 'on' : ''}"></i>`).join('')}</span>${X.units.length} parts · ${deepLessons(X)} lessons</span>
      <span class="btn small ${top ? 'primary' : ''}">${cta}</span></span></button></li>`;
}
function renderLibrary(){
  const view = document.getElementById('view'), rank = deepRank(), {pick, cards, rest} = libCards(rank), done = rank.filter(o => o.done), open = COURSE.filter(U => !U.soon);
  const say = pick ? `<section class="libcoach"><span class="libav">${knightSVG('cheer')}</span><div class="libsay"><p class="kicker">${esc(coachName())}'s pick for you</p>
      <p><b>${pick.touched ? `Keep going with ${esc(pick.X.name)}.` : `Go deeper on ${esc(pick.X.name)} next.`}</b> ${esc(pick.why)}</p>
      <div class="lesson-actions"><button class="btn primary" type="button" data-deep="${pick.X.id}">${pick.touched ? 'Pick up where you left off' : `Start: ${esc(pick.X.title)}`}</button></div></div></section>`
    : `<section class="libcoach"><span class="libav">${knightSVG('cheer')}</span><div class="libsay"><p class="kicker">${esc(coachName())}</p><p><b>Every deep dive finished.</b> That's the whole library for now. Your lines stay in the Drill tab, and today's five keep them fresh.</p></div></section>`;
  const shelf = `<section class="libshelf"><p class="kicker">Finished</p><ul>
      <li><button type="button" class="lmed" data-grad aria-label="Your first course, complete">${medalSVG('gold', 'star')}</button><div><b>Your first course</b><span>${open.length} units · finished ${dayFmt(gradAt())}</span></div><button class="btn small" type="button" data-cpath>Review the path</button></li>
      ${done.map(o => `<li><span class="lmed">${medalSVG('silver', 'flag')}</span><div><b>${esc(o.X.title)}</b><span>Deep dive · ${o.X.units.length} parts</span></div><button class="btn small" type="button" data-deep="${o.X.id}">Open</button></li>`).join('')}</ul></section>`;
  const more = rest.length ? `<details class="libmore"><summary>Not these? Every other deep dive (${rest.length})</summary><ul>${rest.map(o => `<li><button type="button" data-deep="${o.X.id}">${sideChip(o.X.units[0])}<b>${esc(o.X.title)}</b><span>${esc(o.X.tag)}</span><span class="lm">${o.touched && o.cur ? `${unitNo(o.cur)} of ${o.X.units.length}` : `${o.X.units.length} parts`}</span></button></li>`).join('')}</ul></details>` : '';
  view.innerHTML = `<div class="nudge" id="nudge" hidden></div>${changedNote()}<div class="chead"><div><p class="kicker">Course · your library</p><h2 style="font-size:clamp(30px,4vw,46px)">What's next</h2>
      <p>You finished your first course on ${dayFmt(gradAt())}. From here it's depth: one opening at a time, picked from how your course went.</p></div></div>
    ${say}
    ${cards.length ? `<section class="libpicks"><p class="kicker">Picked for you</p><ul class="dcards">${cards.map((o, k) => deepCard(o, k === 0 && o === pick)).join('')}</ul></section>` : ''}
    ${shelf}${more}`;
  courseNotes();
}
// one deep dive: what it covers, why it's here for this player, the part to do next and all the parts
function renderDeep(X){
  const view = document.getElementById('view'), o = deepRank().find(r => r.X === X), cur = deepCur(X), word = X.side === 'w' ? 'White' : 'Black';
  let hero;
  if (cur){
    const steps = unitSteps(cur), nx = steps.find(s => !s.done), open = unitOpen(cur);
    hero = `<section class="chero"><div class="board">${slideSVG(cur, cur.idea[0])}</div>
      <div><div class="chips">${sideChip(cur)}<span class="chip">Up next · ${unitNo(cur)} of ${X.units.length}</span></div>
        <h3>${esc(cur.title)}</h3><p class="lede">${esc(cur.why)}</p>
        <ol class="ministeps" aria-label="Steps in this part">${steps.map(s => `<li class="${s.done ? 'done' : s === nx ? 'next' : ''}">${s.done ? ICON.check : ''}${esc(s.title)}</li>`).join('')}</ol>
        <div class="cta">${open ? `<button class="btn primary" id="dGo">${esc(stepCta(cur, nx))}</button>` : ''}<button class="btn" data-unit="${cur.id}">See the whole part</button></div></div></section>`;
  } else hero = `<section class="chero done dfin"><span class="dmedal">${medalSVG('silver', 'flag')}</span><div><p class="kicker">Deep dive finished</p><h3>Every part passed.</h3><p class="lede">Its lines stay in your reviews, and today's five bring them back. The library has more picks waiting.</p><div class="cta"><button class="btn primary" data-lib>Back to the library</button></div></div></section>`;
  view.innerHTML = `<div class="crumbs"><button class="btn small" data-lib>← Library</button><span class="where">Deep dive · ${word}</span></div>
    <div class="chead"><div><div class="chips">${sideChip(X.units[0])}<span class="chip deep">Deep dive</span><span class="chip">${X.units.length} parts · ${deepLessons(X)} lessons</span></div>
      <h2 style="font-size:clamp(30px,4vw,46px)">${esc(X.title)}</h2><p>${esc(X.why)}</p>${o ? `<p class="dfor"><span class="libav sm">${knightSVG('')}</span><span><b>Why it's here for you:</b> ${esc(o.why)}</span></p>` : ''}</div></div>
    <div class="nudge" id="nudge" hidden></div>${changedNote()}${hero}<ol class="path" aria-label="Parts of this deep dive">${X.units.map(U => unitRow(U, cur)).join('')}</ol>`;
  courseNotes();
  const g = document.getElementById('dGo'); if (g) g.onclick = () => { const nx = unitSteps(cur).find(s => !s.done); if (nx) doStep(cur, nx.key); else openUnit(cur.id); };
}
// the big moment: the coach in a graduation cap, the gold medal, the numbers of the course, and what to do next
function renderGrad(){
  if (!gradAt()){ if (stampGrad()) Prog.save(); else { S.view = 'course'; setHash(); return renderCourse(); } }
  const view = document.getElementById('view'), open = COURSE.filter(U => !U.soon), at = gradAt(), fresh = !!S.gradNow && !S.gradSeen && !reduced;
  S.gradSeen = true;                                                                 // the confetti falls once
  const cpOf = U => U.kind === 'skill' ? U.check.length : U.quiz.length;
  const cpR = open.reduce((a, U) => a + Math.min(up(U.id).cp || 0, cpOf(U)), 0), cpN = open.reduce((a, U) => a + cpOf(U), 0);
  const games = open.reduce((a, U) => a + (up(U.id).sparGames || 0), 0), c = Prog.d.course || {};
  const stamps = Object.values(c.u || {}).flatMap(p => Object.values(p).filter(v => v > 1e12)).concat(Object.values(c.seen || {}).filter(v => v > 1e12));
  const days = Math.max(1, Math.round((at - Math.min(at, ...stamps)) / DAY));
  const pick = deepRank().find(o => !o.done), look = Object.assign({}, Shop.worn(), {head: 'h-grad'});
  const cap = Shop.owns('h-grad') ? '' : Shop.isOpen() ? ' The graduation cap is in the shop now.' : ' The graduation cap is waiting in the shop for when the wardrobe opens (a week in a row).';
  const bits = ['--gold', '--accent', '--rosso', '--blu', '--viola', '--oro', '--gold-2'];
  const conf = fresh ? `<div class="grconf" aria-hidden="true">${Array.from({length: 42}, (_, k) => `<i style="--x:${(k * 37) % 100}%;--d:${(k % 7) * .17}s;--s:${2.6 + (k % 5) * .35}s;--r:${(k * 53) % 360}deg;background:var(${bits[k % bits.length]})"></i>`).join('')}</div>` : '';
  const stat = (n, t) => `<li><b class="tnum">${n}</b><span>${t}</span></li>`;
  view.innerHTML = `<section class="gradv ${fresh ? 'fresh' : ''}">${conf}
    <div class="grhero"><div class="grstage"><span class="grcoach">${knightSVG('cheer', null, look)}</span><span class="grmedal">${medalSVG('gold', 'star')}</span></div>
      <p class="kicker">Course complete · ${dayFmt(at)}</p><h2>You finished your course.</h2>
      <p class="lede">${open.length} units, every checkpoint passed. The openings in it are yours now; next comes depth.</p></div>
    <ul class="grstats">${stat(open.length, 'units passed')}${stat(badgeStats().clean, 'lines played clean')}${stat(`${cpR}<small>/${cpN}</small>`, 'checkpoint positions right first time')}${stat(games, games === 1 ? 'practice game' : 'practice games')}${stat(days, days === 1 ? 'day, start to finish' : 'days, start to finish')}</ul>
    <div class="grearn"><span class="grbadge">${medalSVG('gold', 'star')}</span><div><b>New badge: Course complete</b><span>That's a shop token too.${esc(cap)}</span></div>${Shop.isOpen() && !Shop.owns('h-grad') ? '<button class="btn small" type="button" data-go="shop">Open the shop</button>' : ''}</div>
    ${pick ? `<div class="grnext"><span class="libav">${knightSVG('')}</span><div><p class="kicker">${esc(coachName())} says</p><p><b>What next? Go deeper on ${esc(pick.X.name)}.</b> ${esc(pick.why)} Your Course tab is a library now, and I've picked three deep dives for you.</p>
      <div class="lesson-actions"><button class="btn primary" type="button" data-deep="${pick.X.id}">Start: ${esc(pick.X.title)}</button><button class="btn" type="button" data-lib>See the library</button></div></div></div>` : ''}
    ${S.quizState && S.quizState.state === 'done' && UNIT[S.quizState.unit] && !UNIT[S.quizState.unit].deep ? '<p class="grback"><button class="linkish" type="button" id="grQuiz">See the last checkpoint</button></p>' : ''}
  </section>`;
  const q = document.getElementById('grQuiz'); if (q) q.onclick = () => { S.view = 'quiz'; render(); setHash(); };
}

const Coach = {
  seen: (() => { try { return JSON.parse(localStorage.getItem('playbook-coach') || '{}'); } catch(e){ return {}; } })(), timer: null, last: null, n: 0,
  el(){ let e = document.getElementById('coach'); if (!e){ e = document.createElement('div'); e.id = 'coach'; e.className = 'coach'; document.body.appendChild(e);
      e.addEventListener('click', ev => { if (ev.target.closest('.cx')) return this.hush(); const a = ev.target.closest('[data-cgo]'); if (a){ this.hush(); return a.dataset.cgo === 'me' ? Acct.open(Cloud.user ? 'in' : 'me') : go(a.dataset.cgo); } if (ev.target.closest('.cav')) this.last && !e.querySelector('.cbub') ? this.say(this.last.t, this.last.o) : e.querySelector('.cbub') ? this.hush() : this.say(this.tip()); }); }
    return e; },
  // on the welcome, reading, findings and choice screens the coach is part of the page, so the corner one stays away
  draw(bub){ const e = this.el(); e.hidden = !SET.coach || (PVIEWS.includes(S.view) && S.view !== 'setup') || S.view === 'grad' || libOn(); e.classList.toggle('quiet', ['drill', 'quiz', 'sandbox', 'study', 'explore'].includes(S.view));
    e.innerHTML = (bub || '') + `<button class="cav" type="button" aria-label="${coachName()}, your coach">${knightSVG(this.mood)}</button>`; },
  say(t, o = {}){
    if (!SET.coach) return; clearTimeout(this.timer); this.last = {t, o}; this.mood = o.mood;
    this.draw(`<div class="cbub ${o.art ? 'art' : ''}" role="status"><button class="cx" type="button" aria-label="Close">×</button>${o.art ? `<span class="cart">${o.art}</span>` : ''}<span class="cwho">${coachName()}</span>${o.head ? `<b class="chead2">${esc(o.head)}</b>` : ''}${esc(t)}${o.cta ? `<div class="cacts"><button class="btn small primary" data-cgo="${o.cta[0]}">${esc(o.cta[1])}</button></div>` : ''}</div>`);
    if (!o.stay) this.timer = setTimeout(() => this.hush(), 9000 + t.length * 45);
  },
  hush(){ clearTimeout(this.timer); this.mood = null; this.draw(''); },
  once(key, t, o){ if (this.seen[key]) return false; this.seen[key] = 1; try { localStorage.setItem('playbook-coach', JSON.stringify(this.seen)); } catch(e){} this.say(t, o); return true; },
  refresh(){ this.hush(); },
  tip(){
    const T = {start: 'Connect your chess account and I\'ll build your course around your games.', setup: 'A username is the quickest way. I only read your public games.', sandbox: 'Play your side. The other side answers the way club players really do.',
      course: 'Work down the path. Each checkpoint you pass opens the next unit.', learn: 'Pick a lesson, then step through it with the arrow keys.', drill: 'Five lines a day keeps your streak. The ones you slipped on come first.',
      games: 'This is where your moves and your playbook part ways.', cheat: 'Their move is highlighted. The green arrow is your answer.', study: 'Step through with the arrow keys. Switch the engine on under the board if a position looks scary.'};
    return T[S.view] || T[tabOf(S.view, S.studyFrom)] || 'Keep going.';
  },
  // called after every full render: at most one thing to say, and only the first time
  onView(){
    const v = S.view, e = this.el();
    if (S.drill && S.drill.state === 'play'){ this.lastView = v; return this.hush(); } // never while a drill, a practice game or a checkpoint is being played
    if (v === 'grad' || libOn()){ this.lastView = v; return this.hush(); }            // the coach is part of those pages
    if (Badges.queue.length && PERSONA !== 'new') return Badges.show();
    if (e.querySelector('.cbub') && this.lastView === v) return this.draw(e.querySelector('.cbub').outerHTML); this.lastView = v;
    if (v === 'reading' || v === 'choices' || v === 'built' || v === 'findings') return this.hush(); // the coach is already on the page there
    if (PERSONA === 'new'){
      if (v === 'start') return this.hush();
      if (v === 'setup') return this.once('setup', this.tip()) || this.hush();
      if (v === 'sandbox') return this.once('sb-new', `This is the sandbox: pick an opening and play. I'll stop you where the playbook has a better move. Connect your account and the rest opens.`, {cta: Product.signedOut() ? null : ['setup', 'Connect my account']}) || this.hush();
      if (!OPEN_NEW.includes(v)) return this.say('This opens once I\'ve read your games.', {cta: Product.signedOut() ? null : ['setup', 'Connect my account']});
      return this.hush();
    }
    if (PERSONA === 'ready' && v === 'course' && this.once('ready-course', 'This is your course, in the order your games asked for. Start with the unit at the top.')) return;
    if (['course', 'learn', 'drill', 'games', 'cheat', 'sandbox'].includes(v) && this.once('tab-' + v, this.tip())) return;
    this.hush();
  },
  // the fifth line of the day
  daily(){
    const st = Daily.streak(), week = st === 7 && Math.max(0, ...Shop.runs().slice(0, -1)) < 7;
    if (week) return this.say(`Seven days in a row. My wardrobe is open now, and that's two tokens for the week plus one for the first full week.`, {mood: 'cheer', stay: true, head: 'A week in a row', art: `<span class="cflame">${FLAME}<b>${st}</b></span>`, cta: ['shop', 'Open the shop']});
    this.say(st > 1 ? `That's today's five. ${st} days in a row${st % 3 === 0 ? ', and every third day is a shop token' : ''}: come back tomorrow for ${st + 1}.` : `That's today's five, and day one of your streak. Five more tomorrow keeps it going.`, {mood: 'cheer', ms: 9000, art: `<span class="cflame">${FLAME}<b>${st}</b></span>`, cta: st % 3 === 0 ? ['shop', 'Open the shop'] : null});
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
  if (PERSONA === 'new' && !OPEN_NEW.includes(S.view)){ stopPlay(); setTab(S.view); renderChrome(); S.drill = null; EngineUI.detach(); document.getElementById('drillDot').hidden = true; Product.locked(tabOf(S.view, S.studyFrom)); return Coach.onView(); }
  if (PVIEWS.includes(S.view)){ setTab(S.view); renderChrome(); S.drill = null; EngineUI.detach(); document.getElementById('drillDot').hidden = true; Product.render(); return Coach.onView(); }
  render0(); Coach.onView();
};
const renderGames0 = renderGames;
renderGames = function(){ if (PERSONA === 'ready' && Product.me().P) return Product.games(); renderGames0(); };
const record0 = Prog.record.bind(Prog);
Prog.record = function(id, clean){
  const before = Daily.count(), nb = Badges.n; record0(id, clean);
  if (Badges.n !== nb) return;                           // a new badge says it louder (now, or once the line is over)
  if (before < DAILY && Daily.count() >= DAILY) return Coach.daily();
  Coach.event('line', clean);
};
// every save is a moment something may have been earned
const save0 = Prog.save.bind(Prog);
Prog.save = function(){ save0(); if (Badges.check()) save0(); };
