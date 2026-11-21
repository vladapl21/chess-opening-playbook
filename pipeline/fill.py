"""Replies the book has no answer to. A drafting aid, not part of the build (it needs Stockfish and the Maia weights).

    python3 pipeline/fill.py white|black          writes content/white/wfill.py or content/black/bfill.py

For every position of the book (every system in the library) where the other side is to move, the replies a player at this level picks often
(the Maia odds) are set against the lines the book has. A reply that comes up often enough and has no line gets one:
it is filed as a side line of the lesson it leaves, named after the move (its opening name when it has one), and your
answer is the move the book already plays from that position, else what pipeline/deepen.py would pick. The build's
deepening pass then plays the new line on like every other.

How often is often enough is set per chapter in RULES: the reply's own odds, and how many of your games with that
colour reach it (the odds of every move the other side made on the way). The chapters asked for by name get the finer
net. `FIXED` in content/deepen_fixes.py gives a
reply by hand where the pick misses the point; run this script again after changing it (data/cache holds the engine's
answers, so a second run is quick and gives the same file)."""
import sys, json, re
import chess
import paths
import expand as X
import deepen, draft
import packs as PK

SIDE = sys.argv[1] if len(sys.argv) > 1 else 'white'
ME = chess.WHITE if SIDE == 'white' else chess.BLACK
# chapter -> (a reply's own odds, how many of your games with this colour reach the reply, the deepest ply a new line may start at)
DEFAULT = (0.10, 0.0030, 18)
RULES = {'white': {'italian': (0.07, 0.0012, 22)},
         'black': {'vienna': (0.07, 0.0012, 22)}}[SIDE]
# Named gambits and attacks the other side can spring that had no line. Rare by the odds, so the net above misses
# them, and exactly the kind of move that costs a game when it has never been seen. The last move of each is theirs.
EXTRA = {'white': ['e4 e5 Nf3 f5 Nxe5 Qe7', 'e4 e5 Nf3 f5 Nxe5 Nc6',                      # the Latvian: Greco, Fraser
                   'e4 e5 Nf3 d5 exd5 Bd6', 'e4 e5 Nf3 Bc5 Nxe5 Nc6',                     # the Elephant: Maróczy; Busch-Gass: Chiodini
                   'e4 e5 Nf3 d6 d4 Bd7', 'e4 e5 Nf3 d6 d4 Bg4 dxe5 Nd7',                 # Philidor Gambit; Albin-Blackburne
                   'e4 d5 exd5 Nf6 d4 Bg4', 'e4 d5 exd5 c6 dxc6 e5',                      # the Portuguese; Kloosterboer
                   'e4 c5 c3 d5 exd5 Nf6',                                                # the Anti-Alapin Gambit
                   'e4 e5 Nf3 Nc6 Bc4 Nf6 Ng5 d5 exd5 Nd4', 'e4 e5 Nf3 Nc6 Bc4 Nf6 Ng5 d5 exd5 b5',   # the Fritz, the Ulvestad
                   'e4 e5 Nf3 Nc6 Bc4 Nf6 Ng5 d5 exd5 Nb4', 'e4 e5 Nf3 Nc6 Bc4 Nd4', 'e4 e5 Nf3 Nc6 Bc4 f5']   # Kloss; Blackburne Shilling; Rousseau
                  # the Two Knights, asked for by name: every reply with real odds at each turn of its lines, the ones
                  # that leave a line drafted here included (the net above doesn't read its own lines)
                  + ['e4 e5 Nf3 Nc6 Bc4 Nf6 Ng5 ' + x for x in (
                      'Be7', 'd6', 'Qe7 Bxf7+ Qxf7', 'Qe7 Bxf7+ Kd8 Bb3 Nd4', 'Qe7 Bxf7+ Kd8 Bb3 d6', 'Qe7 Bxf7+ Kd8 Bb3 d5', 'h6 Nxf7 d5',
                      'Na5 Bxf7+ Ke7 Bd5 Nxd5', 'Na5 Bxf7+ Ke7 Bd5 Qe8', 'Na5 Bxf7+ Ke7 Bd5 h6',
                      'Bc5 Bxf7+ Ke7 Bc4 d5', 'Bc5 Bxf7+ Ke7 Bc4 h6', 'Bc5 Bxf7+ Ke7 Bc4 Rf8', 'Bc5 Bxf7+ Ke7 Bc4 d6', 'Bc5 Bxf7+ Kf8 Bb3 h6', 'Bc5 Bxf7+ Kf8 Bb3 d6',
                      'd5 exd5 Nxd5 Nxf7 Qf6', 'd5 exd5 Nxd5 Nxf7 Kxf7 Qf3+ Ke7', 'd5 exd5 Nxd5 Nxf7 Kxf7 Qf3+ Qf6 Bxd5+ Ke7',
                      'd5 exd5 Nxd5 Nxf7 Kxf7 Qf3+ Ke6 Nc3 Ne7 d4 e4', 'd5 exd5 Nxd5 Nxf7 Kxf7 Qf3+ Ke6 Nc3 Nd4 Bxd5+ Qxd5',
                      'd5 exd5 Nxd5 Nxf7 Kxf7 Qf3+ Ke6 Nc3 Nd4 Bxd5+ Ke7', 'd5 exd5 Nxd5 Nxf7 Kxf7 Qf3+ Ke6 Nc3 Nd4 Bxd5+ Kd6 Qd3 c6',
                      'd5 exd5 Nd4 c3 b5', 'd5 exd5 Nd4 c3 Nxd5', 'd5 exd5 Nd4 c3 Bg4', 'd5 exd5 b5 Bf1 Qxd5', 'd5 exd5 b5 Bf1 Nd4', 'd5 exd5 Nb4 O-O Nbxd5',
                      'd5 exd5 Na5 Bb5+ c6 dxc6 bxc6 Qf3 Rb8', 'd5 exd5 Na5 Bb5+ c6 dxc6 bxc6 Qf3 e4', 'd5 exd5 Na5 Bb5+ c6 dxc6 bxc6 Qf3 h6 Ne4 cxb5',
                      'd5 exd5 Na5 Bb5+ c6 dxc6 bxc6 Qf3 h6 Ne4 Bg4', 'd5 exd5 Na5 Bb5+ Bd7 Qe2 a6', 'd5 exd5 Na5 Bb5+ Bd7 Qe2 Nxd5', 'd5 exd5 Na5 Bb5+ Bd7 Qe2 c6')],
         'black': ['d4 d5 e4 dxe4 Nc3 Nf6 Be3', 'd4 d5 e4 dxe4 Be3', 'd4 d5 e4 dxe4 Bc4', # Blackmar-Diemer: Rasa-Studier, Diemer-Rosenberg, Fritz
                   'd4 d5 c4 c6 e4',                                                      # the Slav: Diemer Gambit
                   'e4 e5 d4 exd4 f4', 'e4 e5 Nc3 Nc6 d4', 'e4 e5 Nf3 Nc6 b4',            # Halasz; Fyfe; Pachman Wing
                   'e4 e5 Nf3 Nc6 c3 Nf6 Bc4', 'e4 e5 Nf3 Nc6 d4 exd4 Bb5',               # Ponziani: Neumann; Scotch: Relfsson
                   'e4 e5 Nf3 Nc6 Bc4 Bc5 c3 Nf6 d4 exd4 b4', 'e4 e5 Nf3 Nc6 Bc4 Bc5 c3 Nf6 d4 exd4 O-O',   # the Dubov Italian; Walbrodt-Baird
                   'e4 e5 f4 Bc5 Qh5', 'e4 e5 f4 Bc5 Nf3 d6 b4',                          # King's Gambit Declined: Walthoffen, Rotlewi
                   'f4 d5 e4', 'g4 d5 Bg2 Bxg4 c4', 'b3 e5 Bb2 Nc6 f4']}[SIDE]            # Bird: Williams; Grob: Fritz; Nimzo-Larsen: Pachman
OUT = paths.ROOT / ('content/white/wfill.py' if SIDE == 'white' else 'content/black/bfill.py')

D = json.load(open(paths.BUILD / f'data_{SIDE}.json')); N = D['nodes']
packs = D.get('packs') or {}
house = {c['id'] for c in D['chapters']} - PK.off(packs)
part_ch = {p['id']: p['ch'] for p in D['parts']}; LES = {l['id']: l for l in D['lessons']}
ctx_of = deepen.contexts(D['lessons'], D['parts'], packs)


def san_path(line):
    b = chess.Board(); out = []
    for i in line['n'][1:]:
        mv = chess.Move.from_uci(N[i]['u']); out.append(b.san(mv)); b.push(mv)
    return out


# every system in the library, not only the house's; without this script's own lines (ids with -f-), so a second run on
# a book that already has them gives the same file
lines = [(l, san_path(l)) for l in D['lines'] if l['lesson'] in LES and '-f-' not in l['id']]
have = set()                                             # every path the book walks
for l, t in lines:
    for k in range(1, len(t) + 1): have.add(' '.join(t[:k]))
seen = deepen.Seen()
for l, t in lines:
    b = chess.Board()
    for i, s in zip(l['n'][1:], t):
        if b.turn == ME and 'warn' not in (N[i].get('g') or []): seen.add(b.epd(), ctx_of[l['lesson']], s)
        b.push_san(s)

found = {}
for l, t in sorted(lines, key=lambda x: (not x[0]['main'], x[0]['id'])):
    les = LES[l['lesson']]; ch = part_ch[les['part']]; p_min, r_min, ply_max = RULES.get(ch, DEFAULT)
    if any('warn' in (N[i].get('g') or []) for i in l['n']): continue          # a line that shows a mistake on purpose
    b = chess.Board(); reach = 1.0; first = None
    for k, s in enumerate(t + [None]):
        path = ' '.join(t[:k])
        if b.turn != ME and 2 <= k <= ply_max and k < len(t):          # not at the line's end: the build plays that on
            hs = X.human(path)
            for r, p in hs:
                new = (path + ' ' + r).strip()
                if p >= p_min and reach * p >= r_min and new not in have and new not in found:
                    found[new] = dict(lesson=les['id'], ch=ch, p=p, reach=reach * p, ply=k, off=l.get('title') or les['title'])
        if s is None: break
        if b.turn != ME: reach *= max(dict(X.human(path)).get(s, 0.003), 0.003)               # how often a game of yours gets here
        b.push_san(s)

n_odds = len(found); later = []
for root in EXTRA:
    root = ' '.join(root.split()); par = root.rsplit(' ', 1)[0]
    if root in have or root in found: continue
    if par not in have: later.append(root); continue                     # it may leave a line drafted below
    l = next((l for l, t in sorted(lines, key=lambda x: (not x[0]['main'], x[0]['id'])) if (' '.join(t) + ' ').startswith(par + ' ')), None)
    found[root] = dict(lesson=l['lesson'], ch=part_ch[LES[l['lesson']]['part']], p=dict(X.human(par)).get(root.rsplit(' ', 1)[1], 0), reach=0, ply=len(root.split()) - 1, named=True, off=l.get('title') or LES[l['lesson']]['title'])
print(n_odds, 'replies without a line by the odds,', len(found) - n_odds, 'named ones on top', flush=True)
rows, used = [], {}


def draft_row(path, m):
    t = path.split(); b = chess.Board(); prev = None
    for s in t[:-1]: prev = b.parse_san(s); b.push(prev)
    mv = b.parse_san(t[-1]); title = draft.short(b, mv, prev)
    b.push(mv)
    if b.is_game_over(): return
    legal = {b.san(x) for x in b.legal_moves}
    mine = deepen.F.FIXED.get(path) or deepen._fixed_at().get(b.epd()) or seen.get(b.epd(), ctx_of[m['lesson']])
    if mine not in legal: mine = deepen.choose(b)
    seen.add(b.epd(), ctx_of[m['lesson']], mine)
    v = draft.value(b, mine, deepen.DEPTH)
    n = used.setdefault(m['lesson'], {}); base = draft.slug(t[-1]); sid = base; k = 2
    while sid in n: sid = f'{base}v{k}'; k += 1
    # the same move twice in one lesson: say which move of the game it is, then which line it leaves
    ttl = title; k = 2; off = m['off'][0].lower() + m['off'][1:]
    while ttl in n.values(): ttl = f'{title} on move {(len(t) + 1) // 2}' if k == 2 else f'{title} ({off})' if k == 3 else f'{title} ({k})'; k += 1
    n[sid] = ttl
    rows.append((m['lesson'], f"{m['lesson']}-f-{sid}", ttl, path + ' ' + mine, m, v))
    print(f"  {m['ch']:9s} {m['lesson']:18s} {m['p'] * 100:4.0f}% reach {m['reach'] * 100:5.2f}%  {v / 100:+.2f}  {path} | {mine}   [{ttl}]", flush=True)


for path, m in sorted(found.items(), key=lambda kv: (kv[1]['lesson'], -kv[1]['reach'])): draft_row(path, m)
# the replies listed by hand that leave one of the lines just drafted (a second move in a gambit that had no line at all)
while later:
    for root in later:
        par = root.rsplit(' ', 1)[0]
        src = next((r for r in rows if (r[3] + ' ').startswith(par + ' ')), None)
        if src: break
    else: break
    later.remove(root)
    if any((r[3] + ' ').startswith(root + ' ') for r in rows): continue
    draft_row(root, dict(lesson=src[0], ch=src[4]['ch'], p=dict(X.human(par)).get(root.rsplit(' ', 1)[1], 0), reach=0, ply=len(root.split()) - 1, named=True, off=src[2]))
for root in later: print('  !! not reachable in the book as built:', root)

q = lambda s: "'" + s.replace('\\', '\\\\').replace("'", "\\'") + "'"
imp = 'from content import LESSONS' if SIDE == 'white' else 'from bcontent import LESSONS'
doc = f'''"""{'White' if SIDE == 'white' else 'Black'}: replies that came up often and had no line, and named gambits that had none. Written by pipeline/fill.py from the Maia
odds and the book as built: each is a side line of the lesson it leaves, answered with the move the book already plays
from that position, else a natural move Stockfish 17.1 accepts. The build plays every one of them on
(pipeline/deepen.py). Change a pick in content/deepen_fixes.py and run the script again, not here. SAN is internal."""
{imp}
_BY = {{l['id']: l for l in LESSONS}}
def add(lesson, alt, title, path): _BY[lesson]['alts'].append((alt, title, ' '.join(path.split())))

'''
body = '\n'.join(f"add({q(les)}, {q(aid)}, {q(ttl)}, {q(path)})" for les, aid, ttl, path, m, v in rows)
open(OUT, 'w').write(doc + body + '\n')
print(len(rows), 'side lines written to', OUT)
bad = [(aid, v) for les, aid, ttl, path, m, v in rows if v < -120]
if bad: print('WORSE THAN -1.2 FOR YOU (look at these):', bad)
draft.done()
