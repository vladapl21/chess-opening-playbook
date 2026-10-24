"""Build data/build/data_white.json for the White book: repertoire tree, lessons, games, puzzles, cheat sheet, stats."""
import sys, json, os, collections
import paths
from common import *
from tree import Tree, auto_label
import content, content2, content2_meta as CM, games_content as GC
import expand as X
ALL_GAMES = GC.GAMES + CM.GAMES2
ALL_PUZZLES = GC.PUZZLES + CM.PUZZLES2
ALL_CHEAT = GC.CHEAT + CM.CHEAT2

EVAL_CACHE = str(paths.CACHE / 'eval_cache.json')
cache = json.load(open(EVAL_CACHE)) if os.path.exists(EVAL_CACHE) else {}

PIECE_LETTER = {chess.PAWN: 'p', chess.KNIGHT: 'n', chess.BISHOP: 'b', chess.ROOK: 'r', chess.QUEEN: 'q', chess.KING: 'k'}

nodes = []          # output nodes
FULLFEN = {}
def add_node(parent_idx, board_before, move, board_after, label, note):
    piece = board_before.piece_at(move.from_square)
    meta = {}
    if board_before.is_castling(move):
        rank = '1' if piece.color == chess.WHITE else '8'
        meta['x'] = ('h'+rank+'f'+rank) if chess.square_file(move.to_square) > 4 else ('a'+rank+'d'+rank)
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
for les in content.LESSONS:
    T.add_line(les['path'].split(), les['id'])
    for aid, _, p in les['alts']:
        T.add_line(p.split(), aid)

missing = [p for p in content.NOTES if T.get(p.split()) is None]
if missing:
    print("NOTES WITHOUT NODE:"); [print('   ', m) for m in missing]
    raise SystemExit(1)

nodes.append(dict(p=None, f=chess.Board().board_fen(), k=[], l='Start'))
FULLFEN[0] = chess.Board().fen()
path_to_idx = {(): 0}
def emit(tnode, pidx):
    for ch in tnode.children:
        key = ' '.join(ch.path)
        note = content.NOTES.get(key)
        label = (note or {}).get('label') or auto_label(tnode.board, ch.move)
        idx = add_node(pidx, tnode.board, ch.move, ch.board, label, note)
        path_to_idx[ch.path] = idx
        emit(ch, idx)
emit(T.root, 0)
REP_COUNT = len(nodes)

def path_idx_list(path_str):
    toks = path_str.split()
    return [path_to_idx[tuple(toks[:i])] for i in range(len(toks)+1)]

# lines
lines = []
lesson_out = []
seen_prefixes = set()
def auto_start(toks):
    k = 0
    for i in range(1, len(toks) + 1):
        if tuple(toks[:i]) in seen_prefixes: k = i
        else: break
    return max(k, 1)
for les in content.LESSONS:
    main_ids = path_idx_list(les['path'])
    lid = les['id']
    if les['start'] is None:
        les['start'] = auto_start(les['path'].split())
    for p in [les['path']] + [a[2] for a in les['alts']]:
        t = p.split()
        for i in range(1, len(t) + 1): seen_prefixes.add(tuple(t[:i]))
    lines.append(dict(id=lid, lesson=lid, title=les['title'], n=main_ids, main=1))
    alt_ids = []
    for aid, atitle, p in les['alts']:
        ids = path_idx_list(p)
        lines.append(dict(id=aid, lesson=lid, title=atitle, n=ids, main=0))
        alt_ids.append(aid)
    lesson_out.append(dict(id=lid, part=les['part'], title=les['title'], sub=les['sub'], pri=les['pri'], start=les['start'] or 0,
                           why=les['why'], tags=les['tags'], outcome=les['outcome'], lines=[lid]+alt_ids))

# white moves that are warnings (never drilled)
def is_warn(idx): return 'warn' in nodes[idx].get('g', [])

# ---------------- games
games_out = []
games_raw = {}
GAME_FILES = [(paths.GAMES / 'aqua_alpaca.pgn', 'aqua_alpaca'), (paths.GAMES / 'vladapl_1.pgn', 'vladapl'), (paths.GAMES / 'vladapl_2.pgn', 'vladapl')]
for fn, me in GAME_FILES:
    with open(fn) as f:
        while True:
            g = chess.pgn.read_game(f)
            if g is None: break
            if g.headers['White'] == me and g.headers['Black'] not in games_raw: games_raw[g.headers['Black']] = g
for G in ALL_GAMES:
    g = games_raw[G['opp']]
    b = g.board()
    parent = add_node_root = None
    nodes.append(dict(p=None, f=b.board_fen(), k=[], l='Start')); root = len(nodes)-1; FULLFEN[root] = b.fen()
    seq = [root]; boards = [b.copy()]
    for i, mv in enumerate(g.mainline_moves()):
        ply = i + 1
        before = b.copy(); b.push(mv)
        mom = G['moments'].get(ply)
        label = (mom or {}).get('label') or auto_label(before, mv)
        idx = add_node(seq[-1], before, mv, b.copy(), label, mom)
        seq.append(idx); boards.append(b.copy())
    glines = [dict(id=G['id'], lesson=G['id'], title='The game', n=seq, main=1)]
    for ply, (aid, atitle, san) in G['better'].items():
        start_idx = seq[ply-1]  # position before the improved move
        bb = boards[ply-1].copy(); cur = start_idx; ids = seq[:ply]
        notes = G['better_notes'].get(aid, {})
        for j, s in enumerate(san.split()):
            mv = bb.parse_san(s); before = bb.copy(); bb.push(mv)
            nt = notes.get(j+1)
            label = (nt or {}).get('label') or auto_label(before, mv)
            cur = add_node(cur, before, mv, bb.copy(), label, nt); ids.append(cur)
        glines.append(dict(id=aid, lesson=G['id'], title=atitle, n=ids, main=0, at=ply))
    lines.extend(glines)
    h = g.headers
    games_out.append(dict(id=G['id'], opp=G['opp'], oppElo=G['opp_elo'], meElo=G['me_elo'], result=G['result'], tc=G['tc'], date=G['date'], acct=G.get('acct', 'aqua_alpaca'),
                          title=G['title'], lesson=G['lesson'], summary=G['summary'], lines=[l['id'] for l in glines],
                          moments=sorted(G['moments'].keys())))

# ---------------- puzzles (from game positions)
puzzles = []
gl = {l['id']: l for l in lines}
for gid, ply, accepted, title, text in ALL_PUZZLES:
    line = gl[gid]
    node_idx = line['n'][ply]          # position after `ply` plies (white to move)
    b = chess.Board(); # reconstruct board for legal moves
    g = games_raw[[G['opp'] for G in ALL_GAMES if G['id'] == gid][0]]
    bb = g.board()
    for i, mv in enumerate(g.mainline_moves()):
        if i == ply: break
        bb.push(mv)
    assert bb.turn == chess.WHITE, (gid, ply)
    acc = [bb.parse_san(s).uci() for s in accepted]
    puzzles.append(dict(id=f"{gid}-{ply}", game=gid, node=node_idx, ok=acc, title=title, t=text,
                        legal=[m.uci() for m in bb.legal_moves]))

# ---------------- legal moves for drill positions (white to move, repertoire, non-warn white child)
legal = {}
for path, idx in path_to_idx.items():
    tnode = T.get(list(path)) if path else T.root
    if tnode.board.turn != chess.WHITE: continue
    kids = [c for c in nodes[idx]['k'] if not is_warn(c)]
    if not kids: continue
    legal[idx] = [m.uci() for m in tnode.board.legal_moves]

# ---------------- cheat sheet
cheat = []
for before, san, rule, lid in ALL_CHEAT:
    toks = before.split()
    idx = path_to_idx[tuple(toks)]
    b = T.get(toks).board
    mv = b.parse_san(san).uci()
    child = path_to_idx[tuple(toks + [san])]
    cheat.append(dict(node=idx, mv=mv, child=child, rule=rule, lesson=lid))

# ---------------- evals (engine, cached by FEN) for every node
_ev14 = json.load(open(paths.CACHE / 'ev_cache.json')) if os.path.exists(paths.CACHE / 'ev_cache.json') else {}
for k, v in _ev14.items():
    fen = k.rsplit('|', 1)[0]
    if fen in cache: continue
    val = v[0]
    if abs(val) >= 90000:
        m = round((100000 - abs(val)) / 100)
        cache[fen] = f"M{m if val > 0 else -m}" if m > 0 else 'M0'
    else: cache[fen] = val
need = [idx for idx, fen in FULLFEN.items() if fen not in cache]
print(f"{len(need)} positions need evals")
if need:
    import eng
    for k, idx in enumerate(need):
        b = chess.Board(FULLFEN[idx])
        if b.is_game_over():
            cache[b.fen()] = 'M0'; continue
        inf = eng.engine().analyse(b, chess.engine.Limit(depth=14))
        sc = inf['score'].white()
        cache[b.fen()] = (f"M{sc.mate()}" if sc.is_mate() else sc.score())
        if k % 25 == 0:
            json.dump(cache, open(EVAL_CACHE, 'w')); print('  evals', k, flush=True)
    json.dump(cache, open(EVAL_CACHE, 'w'))
for idx, fen in FULLFEN.items():
    v = cache.get(fen)
    if v is None: continue
    if v == 'M0':
        b = chess.Board(fen)
        v = ('#W' if b.turn == chess.BLACK else '#B') if b.is_checkmate() else 'M0'
    nodes[idx]['e'] = v

# ---------------- stats from the user's games
stats = dict(white=0, wins=0, losses=0, draws=0, e5=0, italian=0, it_w=0, it_l=0, third=collections.Counter(), second=collections.Counter(), first=collections.Counter())
chstats = collections.defaultdict(lambda: dict(n=0, w=0, l=0, d=0))
def chapter_of(sans):
    if len(sans) < 2: return 'rare'
    if sans[1] == 'e5': return 'italian' if len(sans) > 3 and sans[2] == 'Nf3' and sans[3] == 'Nc6' else 'e5x'
    return {'c6': 'caro', 'c5': 'sic', 'd5': 'scandi', 'd6': 'pirc', 'g6': 'pirc', 'e6': 'french'}.get(sans[1], 'rare')
def _games():
    for fn, me in GAME_FILES:
        with open(fn) as f:
            while True:
                g = chess.pgn.read_game(f)
                if g is None: break
                if g.headers['White'] == me: yield g
for g in _games():
    if True:
        stats['white'] += 1
        r = g.headers['Result']
        stats['wins' if r == '1-0' else 'losses' if r == '0-1' else 'draws'] += 1
        mv = []; bb = g.board()
        for m in list(g.mainline_moves())[:6]:
            mv.append(bb.san(m)); bb.push(m)
        stats['first'][mv[1]] += 1
        cs = chstats[chapter_of(mv)]; cs['n'] += 1; cs['w' if r == '1-0' else 'l' if r == '0-1' else 'd'] += 1
        if mv[1] == 'e5':
            stats['e5'] += 1; stats['second'][mv[3]] += 1
            if mv[2:5] == ['Nf3', 'Nc6', 'Bc4']:
                stats['italian'] += 1; stats['third'][mv[5]] += 1
                if r == '1-0': stats['it_w'] += 1
                elif r == '0-1': stats['it_l'] += 1
stats = {k: (dict(v) if isinstance(v, collections.Counter) else v) for k, v in stats.items()}
stats['total'] = stats['white']

# ---------------- human odds for every Black move in the repertoire tree
E4 = path_to_idx[('e4',)]
idx_to_path = {v: k for k, v in path_to_idx.items()}
first_counts = collections.Counter(stats['first'])
for idx in range(1, REP_COUNT):
    nd = nodes[idx]
    if nd.get('w') != 0: continue
    p = idx_to_path[idx]
    if nd['p'] == E4:
        nd['q'] = round(max(first_counts.get(p[-1], 0), 0.3) / stats['white'], 4)
    else:
        hs = dict(X.human(' '.join(p[:-1])))
        nd['q'] = round(hs.get(p[-1], 0.004), 4)
X.save()

# ---------------- chapters
def pidx(path): return path_to_idx[tuple(path.split())]
chapters_out = []
for C in content2.CHAPTERS:
    M = CM.CH_META[C['id']]; st = dict(chstats[C['id']])
    d = dict(id=C['id'], name=C['name'], move=C['move'], parts=C['parts'], stats=st, tile=pidx(M['tile']),
             roots=[pidx(r) for r in M['roots']], first=M['first'])
    assert M['first'] in {l['id'] for l in content.LESSONS}, M['first']
    if C['id'] != 'italian':
        fmt = lambda t: t.format(**st)
        d.update(hero=pidx(M['hero']), arrows=M['arrows'], circles=M['circles'], cap=M['cap'], kicker=M['kicker'],
                 headline=M['headline'], lede=M['lede'], facts=[dict(big=fmt(f['big']), text=fmt(f['text']), alert=f.get('alert', False)) for f in M['facts']],
                 notes=M['notes'])
        lids = {l['id'] for l in content.LESSONS}; lineids = {l['id'] for l in lines}
        for nn in M['notes']:
            assert ('lesson' not in nn or nn['lesson'] in lids) and ('line' not in nn or nn['line'] in lineids), nn
    chapters_out.append(d)
print('chapters', [(c['id'], c['stats']) for c in chapters_out])
print('stats', stats)

out = dict(nodes=nodes, lines=lines, lessons=lesson_out, parts=content.PARTS, games=games_out, puzzles=puzzles,
           legal={str(k): v for k, v in legal.items()}, cheat=cheat, stats=stats, repCount=REP_COUNT, e4=E4, chapters=chapters_out)
OUT = paths.BUILD / 'data_white.json'
json.dump(out, open(OUT, 'w'), separators=(',', ':'))
print(f"nodes={len(nodes)} rep={REP_COUNT} lines={len(lines)} lessons={len(lesson_out)} games={len(games_out)} puzzles={len(puzzles)} cheat={len(cheat)} legal={len(legal)}")
print('size', os.path.getsize(OUT))
try:
    import eng; eng.done()
except Exception:
    os._exit(0)
