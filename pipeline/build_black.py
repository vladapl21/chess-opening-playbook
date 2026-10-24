"""Build data/build/data_black.json for the Black book: repertoire tree, lessons, games, puzzles, cheat sheet, stats."""
import sys, json, os, collections
import paths
from common import *
from tree import Tree
from label2 import label as auto_label
import bcontent as BC
import bnotes  # noqa: F401  registers notes into BC.NOTES
import bmeta as BM
from black_chapters import chapter_of
import expand as X

OUT = str(paths.BUILD / 'data_black.json')
EVAL_CACHE = str(paths.CACHE / 'eval_cache.json')
cache = json.load(open(EVAL_CACHE)) if os.path.exists(EVAL_CACHE) else {}
PIECE_LETTER = {chess.PAWN: 'p', chess.KNIGHT: 'n', chess.BISHOP: 'b', chess.ROOK: 'r', chess.QUEEN: 'q', chess.KING: 'k'}

nodes = []
FULLFEN = {}
def add_node(parent_idx, board_before, move, board_after, label, note):
    piece = board_before.piece_at(move.from_square)
    meta = {}
    if board_before.is_castling(move):
        rank = '1' if piece.color == chess.WHITE else '8'
        meta['x'] = ('h' + rank + 'f' + rank) if chess.square_file(move.to_square) > 4 else ('a' + rank + 'd' + rank)
    if board_before.is_en_passant(move):
        meta['ep'] = chess.square_name(chess.square(chess.square_file(move.to_square), chess.square_rank(move.from_square)))
    cap = board_before.piece_at(move.to_square)
    if cap: meta['cap'] = PIECE_LETTER[cap.piece_type]
    if board_after.is_checkmate(): meta['mate'] = 1
    elif board_after.is_check(): meta['chk'] = 1
    nd = dict(p=parent_idx, u=move.uci(), pc=PIECE_LETTER[piece.piece_type],
              w=1 if piece.color == chess.WHITE else 0, f=board_after.board_fen(), l=label, k=[])
    nd.update(meta)
    if note:
        if note.get('text'): nd['t'] = note['text']
        if note.get('tags'): nd['g'] = note['tags']
        if note.get('arrows'): nd['a'] = note['arrows']
        if note.get('circles'): nd['c'] = note['circles']
    nodes.append(nd)
    idx = len(nodes) - 1
    FULLFEN[idx] = board_after.fen()
    if parent_idx is not None: nodes[parent_idx]['k'].append(idx)
    return idx

# ---------------- repertoire tree
T = Tree()
for les in BC.LESSONS:
    T.add_line(les['path'].split(), les['id'])
    for aid, _, p in les['alts']: T.add_line(p.split(), aid)
missing = [p for p in BC.NOTES if T.get(p.split()) is None]
if missing:
    print('NOTES WITHOUT NODE:'); [print('   ', m) for m in missing]; raise SystemExit(1)
ids = [l['id'] for l in BC.LESSONS] + [a[0] for l in BC.LESSONS for a in l['alts']]
dup = [k for k, v in collections.Counter(ids).items() if v > 1]
assert not dup, dup

nodes.append(dict(p=None, f=chess.Board().board_fen(), k=[], l='Start'))
FULLFEN[0] = chess.Board().fen()
path_to_idx = {(): 0}
def emit(tnode, pidx, prev_move=None, prev_cap=False):
    for ch in tnode.children:
        note = BC.NOTES.get(' '.join(ch.path))
        label = (note or {}).get('label') or auto_label(tnode.board, ch.move, prev_move, prev_cap)
        idx = add_node(pidx, tnode.board, ch.move, ch.board, label, note)
        path_to_idx[ch.path] = idx
        emit(ch, idx, ch.move, tnode.board.is_capture(ch.move))
emit(T.root, 0)
REP_COUNT = len(nodes)

def path_idx_list(path_str):
    toks = path_str.split()
    return [path_to_idx[tuple(toks[:i])] for i in range(len(toks) + 1)]

lines, lesson_out, seen_prefixes = [], [], set()
def auto_start(toks):
    k = 0
    for i in range(1, len(toks) + 1):
        if tuple(toks[:i]) in seen_prefixes: k = i
        else: break
    return max(k, 1)
for les in BC.LESSONS:
    lid = les['id']
    start = les['start'] if les['start'] is not None else auto_start(les['path'].split())
    for p in [les['path']] + [a[2] for a in les['alts']]:
        t = p.split()
        for i in range(1, len(t) + 1): seen_prefixes.add(tuple(t[:i]))
    lines.append(dict(id=lid, lesson=lid, title=les['title'], n=path_idx_list(les['path']), main=1))
    alt_ids = []
    for aid, atitle, p in les['alts']:
        lines.append(dict(id=aid, lesson=lid, title=atitle, n=path_idx_list(p), main=0)); alt_ids.append(aid)
    lesson_out.append(dict(id=lid, part=les['part'], title=les['title'], sub=les['sub'], pri=les['pri'], start=start or 0,
                           why=les['why'], tags=les['tags'], outcome=les['outcome'], lines=[lid] + alt_ids))

# ---------------- games
ALLG = json.load(open(paths.DATA / 'black_games.json'))
def find_game(opp, date_key):
    gs = [g for g in ALLG if g['opp'] == opp and g['date'] == date_key]
    assert len(gs) == 1, (opp, date_key, len(gs))
    return gs[0]
games_out, game_sans = [], {}
for G in BM.GAMES:
    g = find_game(G['opp'], G['date_key'])
    assert g['res'] == G['result'], (G['id'], g['res'])
    sans = g['sans']; game_sans[G['id']] = sans
    b = chess.Board()
    nodes.append(dict(p=None, f=b.board_fen(), k=[], l='Start')); root = len(nodes) - 1; FULLFEN[root] = b.fen()
    seq = [root]; boards = [b.copy()]; prev = None; pcap = False
    for i, s in enumerate(sans):
        ply = i + 1
        before = b.copy(); mv = b.parse_san(s); b.push(mv)
        mom = G['moments'].get(ply)
        lab = (mom or {}).get('label') or auto_label(before, mv, prev, pcap)
        idx = add_node(seq[-1], before, mv, b.copy(), lab, mom)
        seq.append(idx); boards.append(b.copy()); prev = mv; pcap = before.is_capture(mv)
    for ply in G['moments']:
        assert 1 <= ply <= len(sans), (G['id'], ply)
        mover_black = (ply % 2 == 0)
    glines = [dict(id=G['id'], lesson=G['id'], title='The game', n=seq, main=1)]
    for ply, (aid, atitle, san) in sorted(G['better'].items()):
        bb = boards[ply - 1].copy(); cur = seq[ply - 1]; ids_ = seq[:ply]
        assert bb.turn == chess.BLACK, (aid, 'better line must replace one of your moves')
        notes = G['better_notes'].get(aid, {})
        prev = None; pcap = False
        for j, s in enumerate(san.split()):
            mv = bb.parse_san(s); before = bb.copy(); bb.push(mv)
            nt = notes.get(j + 1)
            lab = (nt or {}).get('label') or auto_label(before, mv, prev, pcap)
            cur = add_node(cur, before, mv, bb.copy(), lab, nt); ids_.append(cur); prev = mv; pcap = before.is_capture(mv)
        glines.append(dict(id=aid, lesson=G['id'], title=atitle, n=ids_, main=0, at=ply))
    lines.extend(glines)
    games_out.append(dict(id=G['id'], opp=G['opp'], oppElo=G['opp_elo'], meElo=G['me_elo'], result=G['result'], tc=G['tc'], date=G['date'], acct=G['acct'],
                          title=G['title'], lesson=G['lesson'], summary=G['summary'], lines=[l['id'] for l in glines], moments=sorted(G['moments'].keys())))
lesson_ids = {l['id'] for l in lesson_out}
for G in BM.GAMES: assert G['lesson'] in lesson_ids, G['lesson']

# ---------------- puzzles (Black to move in your own games)
puzzles = []
gl = {l['id']: l for l in lines}
for P in BM.PUZZLES:
    gid, ply, accepted, title, text = P[:5]
    prompt = P[5] if len(P) > 5 else None
    bb = chess.Board()
    for s in game_sans[gid][:ply]: bb.push_san(s)
    assert bb.turn == chess.BLACK, (gid, ply)
    acc = [bb.parse_san(s).uci() for s in accepted]
    d = dict(id=f"{gid}-{ply}", game=gid, node=gl[gid]['n'][ply], ok=acc, title=title, t=text, legal=[m.uci() for m in bb.legal_moves])
    if prompt: d['q'] = prompt
    puzzles.append(d)
pz_index = {p['id']: k for k, p in enumerate(puzzles)}

# ---------------- legal moves where it is your (Black's) turn in the repertoire
legal = {}
for path, idx in path_to_idx.items():
    tnode = T.get(list(path)) if path else T.root
    if tnode.board.turn != chess.BLACK: continue
    kids = [c for c in nodes[idx]['k'] if 'warn' not in nodes[c].get('g', [])]
    if not kids: continue
    legal[idx] = [m.uci() for m in tnode.board.legal_moves]

# ---------------- cheat sheet
cheat = []
for before, san, rule, lid in BM.CHEAT:
    toks = before.split()
    idx = path_to_idx[tuple(toks)]
    b = T.get(toks).board
    assert b.turn == chess.BLACK, before
    mv = b.parse_san(san).uci()
    child = path_to_idx[tuple(toks + [san])]
    assert lid in lesson_ids, lid
    cheat.append(dict(node=idx, mv=mv, child=child, rule=rule, lesson=lid))

# ---------------- evals
_ev14 = json.load(open(paths.CACHE / 'ev_cache.json')) if os.path.exists(paths.CACHE / 'ev_cache.json') else {}
for k, v in _ev14.items():
    fen = k.rsplit('|', 1)[0]
    if fen in cache or not k.endswith('|14'): continue
    val = v[0]
    if abs(val) >= 90000:
        m = round((100000 - abs(val)) / 100)
        cache[fen] = f"M{m if val > 0 else -m}" if m > 0 else 'M0'
    else: cache[fen] = val
need = [idx for idx, fen in FULLFEN.items() if fen not in cache]
print(f"{len(need)} positions need evals", flush=True)
if need:
    import eng
    for k, idx in enumerate(need):
        b = chess.Board(FULLFEN[idx])
        if b.is_game_over(): cache[b.fen()] = 'M0'; continue
        inf = eng.engine().analyse(b, chess.engine.Limit(depth=14))
        sc = inf['score'].white()
        cache[b.fen()] = (f"M{sc.mate()}" if sc.is_mate() else sc.score())
        if k % 50 == 0:
            json.dump(cache, open(EVAL_CACHE, 'w')); print('  evals', k, flush=True)
    json.dump(cache, open(EVAL_CACHE, 'w'))
for idx, fen in FULLFEN.items():
    v = cache.get(fen)
    if v is None: continue
    if v == 'M0':
        b = chess.Board(fen)
        v = ('#W' if b.turn == chess.BLACK else '#B') if b.is_checkmate() else 'M0'
    nodes[idx]['e'] = v

# ---------------- stats from your games with Black
stats = dict(total=len(ALLG), wins=0, losses=0, draws=0, first=collections.Counter(), covered=0)
chstats = collections.defaultdict(lambda: dict(n=0, w=0, l=0, d=0))
for g in ALLG:
    r = g['res']
    stats['wins' if r == 'W' else 'losses' if r == 'L' else 'draws'] += 1
    stats['first'][g['sans'][0]] += 1
    ch = chapter_of(g['sans'])
    if ch is None: continue
    stats['covered'] += 1
    cs = chstats[ch]; cs['n'] += 1; cs[{'W': 'w', 'L': 'l', 'D': 'd'}[r]] += 1
stats['first'] = dict(stats['first'])

# ---------------- odds for every White move in the tree (first move from your games, then Maia)
idx_to_path = {v: k for k, v in path_to_idx.items()}
for idx in range(1, REP_COUNT):
    nd = nodes[idx]
    if nd.get('w') != 1: continue
    p = idx_to_path[idx]
    if len(p) == 1:
        nd['q'] = round(max(stats['first'].get(p[0], 0), 0.3) / stats['total'], 4)
    else:
        hs = dict(X.human(' '.join(p[:-1])))
        nd['q'] = round(hs.get(p[-1], 0.004), 4)
X.save()

# ---------------- chapters
def pidx(path): return path_to_idx[tuple(path.split())]
lineids = {l['id'] for l in lines}
chapters_out = []
for C in BM.CHAPTERS:
    M = BM.CH_META[C['id']]; st = dict(chstats[C['id']])
    for pid in C['parts']: assert any(P['id'] == pid and P['ch'] == C['id'] for P in BC.PARTS), pid
    fmt = lambda t: t.format(**st)
    d = dict(id=C['id'], name=C['name'], move=C['move'], parts=C['parts'], stats=st, tile=pidx(M['tile']),
             roots=[pidx(r) for r in M['roots']], first=M['first'], hero=pidx(M['hero']), arrows=M['arrows'], circles=M['circles'],
             cap=M['cap'], kicker=M['kicker'], headline=M['headline'], lede=M['lede'],
             facts=[dict(big=fmt(f['big']), text=fmt(f['text']), alert=f.get('alert', False)) for f in M['facts']], notes=M['notes'])
    assert M['first'] in lesson_ids, M['first']
    for nn in M['notes']:
        assert ('lesson' not in nn or nn['lesson'] in lesson_ids) and ('line' not in nn or nn['line'] in lineids), nn
    chapters_out.append(d)
# every lesson's main line must sit inside its chapter's roots
for les in lesson_out:
    ch = [c for c in chapters_out if les['part'] in c['parts']][0]
    n_ = next(l for l in lines if l['id'] == les['id'])['n']
    assert any(r in n_ for r in ch['roots']), (les['id'], ch['id'])

# ---------------- insights
insights = []
for I in BM.INSIGHTS:
    d = dict(big=I['big'], unit=I['unit'], h=I['h'], p=I['p'])
    if I['puz']: d['puz'] = pz_index[I['puz']]
    else:
        d['game'] = I['game']; d['at'] = I['at']; assert I['game'] in lineids
    insights.append(d)

print('chapters', [(c['id'], c['stats']) for c in chapters_out])
print('stats', {k: v for k, v in stats.items() if k != 'first'}, sorted(stats['first'].items(), key=lambda kv: -kv[1]))
out = dict(side='b', nodes=nodes, lines=lines, lessons=lesson_out, parts=BC.PARTS, games=games_out, puzzles=puzzles,
           legal={str(k): v for k, v in legal.items()}, cheat=cheat, stats=stats, repCount=REP_COUNT, e4=0, oddsRoot=0,
           chapters=chapters_out, insights=insights)
json.dump(out, open(OUT, 'w'), separators=(',', ':'))
print(f"nodes={len(nodes)} rep={REP_COUNT} lines={len(lines)} lessons={len(lesson_out)} games={len(games_out)} puzzles={len(puzzles)} cheat={len(cheat)} legal={len(legal)}")
print('size', os.path.getsize(OUT))
try:
    import eng; eng.done()
except Exception:
    os._exit(0)
