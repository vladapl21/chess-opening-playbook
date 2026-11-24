"""Build the endings data for the page: python3 pipeline/build_endings.py  ->  data/build/data_endings.json

From content/endings.py:
  - the positions of every kind of ending the Endings tab plays: made at random for the generated kinds (a fixed seed,
    so the same positions every time) and kept only when the exact tables (pipeline/endtb.py) or Stockfish agree they
    are what the kind says (won, drawn, a forced mate); the positions given by hand and the house player's own are
    checked the same way;
  - the course: each unit's slides (checked to be legal positions), its lines to play along (worked out from the
    tables with the human method, or Stockfish's line, or moves given by hand and checked) and its checkpoint (every
    legal move judged: the moves that answer the question, and for each other move the reply that punishes it).
Stockfish's results are kept in data/cache/end_build_cache.json, so a second run needs no engine (STOCKFISH otherwise).
"""
import json, math, os, random, re, sys
import paths
import chess, chess.engine
import endtb
import endings as E

CACHE = paths.CACHE / 'end_build_cache.json'
OUT = paths.BUILD / 'data_endings.json'
_c = json.load(open(CACHE)) if CACHE.exists() else {}
_used = set()      # the keys this run read: a full build writes back only those
_eng = None
MATE = 100000
WIN = 300          # a position counts as won from +3 for the player
DRAWN = 80         # and as a draw within 0.8 of level


def engine():
    global _eng
    if _eng is None:
        _eng = chess.engine.SimpleEngine.popen_uci(paths.STOCKFISH)
        _eng.configure({'Threads': 2, 'Hash': 256})
    return _eng


def num(s):
    """A python-chess score as one number from White's side: a mate in n is +-(100000 - 100 n)."""
    s = s.white()
    if s.is_mate(): return (MATE - 100 * abs(s.mate())) * (1 if s.mate() > 0 else -1)
    return s.score()


def sf(b, depth=20, multipv=1):
    """Stockfish's lines for the position: [[score from White's side, [moves]], ...], best first (cached)."""
    key = f'{b.epd()}|{depth}|{multipv}'
    _used.add(key)
    if key not in _c:
        if b.is_game_over():
            v = (-MATE if b.turn == chess.WHITE else MATE) if b.is_checkmate() else 0
            _c[key] = [[v, []]]
        else:
            infos = engine().analyse(b, chess.engine.Limit(depth=depth), multipv=multipv)
            _c[key] = [[num(i['score']), [m.uci() for m in i.get('pv', [])[:24]]] for i in infos]
            if len(_c) % 50 == 0: save()
    return _c[key]


def sfall(b, depth=18):
    """Every legal move scored: {move: score for the side to move} (cached; a mate as +-(100000 - 100 n))."""
    key = f'{b.epd()}|{depth}|all'
    _used.add(key)
    if key not in _c:
        n = b.legal_moves.count()
        if not n: return {}
        infos = engine().analyse(b, chess.engine.Limit(depth=depth), multipv=n)
        _c[key] = {i['pv'][0].uci(): pov(num(i['score']), b.turn) for i in infos if i.get('pv')}
        if len(_c) % 50 == 0: save()
    return _c[key]


def save(full=False):
    """Write the cache (to a new file first, so an interrupted write never empties it); after a whole build, only
    the entries it used, so the file holds what the build needs."""
    tmp = CACHE.with_suffix('.tmp')
    json.dump({k: v for k, v in _c.items() if k in _used} if full else _c, open(tmp, 'w'))
    os.replace(tmp, CACHE)


def pov(v, color): return v if color == chess.WHITE else -v
def dist(a, b): return chess.square_distance(a, b)
def edge(s): return chess.square_file(s) in (0, 7) or chess.square_rank(s) in (0, 7)
def sq(f, r): return chess.square(f, r)


def board(pieces, turn):
    b = chess.Board(None)
    for s, p in pieces: b.set_piece_at(s, chess.Piece.from_symbol(p))
    b.turn = turn
    return b if b.is_valid() else None


# ---------------------------------------------------------------- the human method, driven by the tables
def other_sq(b, strong):
    return next(s for s, p in b.piece_map().items() if p.color == strong and p.piece_type != chess.KING)


def box(b, strong):
    """How many squares the rectangle holds that the strong piece's row and file keep the lone king in."""
    x, k = other_sq(b, strong), b.king(not strong)
    xf, xr, kf, kr = chess.square_file(x), chess.square_rank(x), chess.square_file(k), chess.square_rank(k)
    if xf == kf or xr == kr: return 64
    return (xf if kf < xf else 7 - xf) * (xr if kr < xr else 7 - xr)


def method_move(b, strong, seen):
    """The move a person plays: mate when there is one, else shrink the box, else bring the king; always one that keeps
    the win, and never back to a position the line has had."""
    a0 = box(b, strong); best = None
    for m in b.legal_moves:
        r = endtb.after(b, m)
        if not r or r[0] != 1: continue
        if r[1] == 0: return m
        b.push(m); k = b.board_fen() + str(b.turn); a = box(b, strong); d = dist(b.king(strong), b.king(not strong)); b.pop()
        if k in seen: continue
        king = b.piece_type_at(m.from_square) == chess.KING
        key = (a0, 0, d, r[1]) if king else (a, 0, 0, r[1]) if a < a0 else (a0, 1, d, r[1])
        if best is None or key < best[0]: best = (key, m)
    if best: return best[1]
    return min((m for m in b.legal_moves if (endtb.after(b, m) or (0,))[0] == 1), key=lambda m: endtb.after(b, m)[1])


def defend_move(b):
    """The longest defence by the table; among equals, the move toward the middle."""
    best = None
    for m in b.legal_moves:
        r = endtb.after(b, m)            # from the defender's side: (-1, plies) lost, (0, None) a draw
        d = 999 if not r or r[0] != -1 else r[1]
        f, rk = chess.square_file(m.to_square), chess.square_rank(m.to_square)
        key = (d, -max(abs(3.5 - f), abs(3.5 - rk)))
        if best is None or key > best[0]: best = (key, m)
    return best[1]


def table_line(fen, plies=120):
    """A line to play along: the human method for the player, the longest defence for the other side; a king and pawn
    line plays the quickest win and stops when the pawn has queened."""
    b = chess.Board(fen); strong = b.turn; out = []; seen = {b.board_fen() + str(b.turn)}
    kpk = endtb.which(b)[0] == 'kpk'
    for _ in range(plies):
        if b.is_game_over(): break
        if b.turn == strong:
            if kpk:
                win = [(m, endtb.after(b, m)) for m in b.legal_moves if m.promotion in (None, chess.QUEEN)]
                m = min(((m, r) for m, r in win if r and r[0] == 1), key=lambda x: (0 if x[0].promotion else 1, x[1][1]))[0]
            else: m = method_move(b, strong, seen)
        else: m = defend_move(b)
        out.append(m.uci()); b.push(m); seen.add(b.board_fen() + str(b.turn))
        if kpk and m.promotion: break
    assert b.is_checkmate() or kpk, ('the line did not mate', fen)
    return out


# ---------------------------------------------------------------- the kinds of ending
def gen_kxk(kind, piece, lo, hi, n, seed):
    rnd = random.Random(seed); out = []; tries = 0
    while len(out) < n and tries < 200000:
        tries += 1
        wk, x, bk = rnd.sample(range(64), 3)
        if dist(wk, bk) < 3 or edge(bk) or dist(x, bk) < 2: continue
        b = board([(wk, 'K'), (x, piece), (bk, 'k')], chess.WHITE)
        if not b: continue
        r = endtb.probe(b)
        if not r or r[0] != 1 or not lo <= r[1] <= hi: continue
        out.append(b.mirror() if len(out) % 3 == 2 else b)
    return out


def gen_kpk(n, seed, hold=False):
    rnd = random.Random(seed); out = []; tries = 0
    while len(out) < n and tries < 400000:
        tries += 1
        wk, bk = rnd.sample(range(64), 2)
        p = sq(rnd.randrange(1, 7), rnd.randrange(1, 5) if not hold else rnd.randrange(2, 6))
        if p in (wk, bk): continue
        b = board([(wk, 'K'), (p, 'P'), (bk, 'k')], chess.BLACK if hold else chess.WHITE)
        if not b: continue
        r = endtb.probe(b)
        if not r: continue
        res = [endtb.after(b, m) for m in b.legal_moves]
        if hold:
            keep = [x for x in res if x and x[0] == 0]
            if r[0] != 0 or not 1 <= len(keep) <= 2 or len(res) < 4: continue
        else:
            keep = [x for x in res if x and x[0] == 1]
            if r[0] != 1 or r[1] < 9 or not 1 <= len(keep) <= 2: continue
        out.append(b.mirror() if len(out) % 3 == 2 else b)
    return out


def gen_engine(kind, n, seed, make, ok, depth=20):
    """Positions from `make(rnd)` that Stockfish agrees with (`ok(score for the side to move, lines)`)."""
    rnd = random.Random(seed); out = []; tries = 0
    while len(out) < n and tries < 400:
        tries += 1
        b = make(rnd)
        if not b or b.is_game_over() or any(x.epd() == b.epd() for x in out): continue
        L = sf(b, depth)
        if ok(pov(L[0][0], b.turn), L): out.append(b.mirror() if len(out) % 3 == 2 else b)
    if len(out) < n: print(f'  {kind}: only {len(out)} of {n} after {tries} tries')
    return out


def gen_bare(n, seed, make):
    """Bare-king mates with two minor pieces: always a win, as long as no piece hangs and it isn't stalemate."""
    rnd = random.Random(seed); out = []
    while len(out) < n:
        b = make(rnd)
        if not b or b.is_game_over(): continue
        k = b.king(chess.BLACK)
        if any(b.is_attacked_by(chess.BLACK, s) and not b.is_attacked_by(chess.WHITE, s) for s in b.pieces(chess.BISHOP, chess.WHITE) | b.pieces(chess.KNIGHT, chess.WHITE)): continue
        out.append(b.mirror() if len(out) % 3 == 2 else b)
    return out


def make_outside(rnd):
    """An outside passed pawn: your edge pawn and three on the other wing against their two or three."""
    left = rnd.random() < .5
    a = 0 if left else 7
    mine = [sq(a, rnd.randrange(2, 4))] + [sq(f, 1 + rnd.randrange(0, 2)) for f in ([5, 6, 7] if left else [0, 1, 2])]
    theirs = [sq(f, 6 - rnd.randrange(0, 2)) for f in ([5, 6, 7] if left else [0, 1, 2])][:rnd.choice([2, 3])]
    wk = sq(rnd.randrange(2, 6), rnd.randrange(1, 4)); bk = sq(rnd.randrange(2, 6), rnd.randrange(4, 7))
    pcs = [(wk, 'K'), (bk, 'k')] + [(s, 'P') for s in mine] + [(s, 'p') for s in theirs]
    if len({s for s, _ in pcs}) < len(pcs): return None
    return board(pcs, chess.WHITE)


def make_rr(rnd):
    wk, r1, r2, bk = rnd.sample(range(64), 4)
    if edge(bk) or dist(wk, bk) < 3 or min(dist(r1, bk), dist(r2, bk)) < 2: return None
    return board([(wk, 'K'), (r1, 'R'), (r2, 'R'), (bk, 'k')], chess.WHITE)


def make_bb(rnd):
    wk, b1, b2, bk = rnd.sample(range(64), 4)
    light = lambda s: (chess.square_file(s) + chess.square_rank(s)) % 2
    if light(b1) == light(b2) or edge(bk) or dist(wk, bk) < 3 or min(dist(b1, bk), dist(b2, bk)) < 2: return None
    return board([(wk, 'K'), (b1, 'B'), (b2, 'B'), (bk, 'k')], chess.WHITE)


def make_bn(rnd):
    wk, bs, ns, bk = rnd.sample(range(64), 4)
    if edge(bk) or dist(wk, bk) < 3 or min(dist(bs, bk), dist(ns, bk)) < 2: return None
    return board([(wk, 'K'), (bs, 'B'), (ns, 'N'), (bk, 'k')], chess.WHITE)


def make_luc(rnd):
    f = rnd.randrange(1, 7)
    side = rnd.choice([-1, 1]) if 2 <= f <= 5 else (1 if f < 3 else -1)
    fk, fr = f + side * rnd.choice([2, 3]), f + side
    if not 0 <= fk <= 7: return None
    long = 0 if side > 0 else 7                     # their rook checks from the long side
    if abs(long - f) < 3: return None
    return board([(sq(f, 7), 'K'), (sq(f, 6), 'P'), (sq(fr, rnd.randrange(0, 2)), 'R'), (sq(fk, rnd.randrange(5, 7)), 'k'),
                  (sq(long, rnd.randrange(1, 3)), 'r')], chess.WHITE)


def make_phi(rnd):
    f = rnd.randrange(1, 7)
    wk = sq(min(7, max(0, f + rnd.choice([-1, 0, 1]))), 3)
    wr = sq(rnd.choice([x for x in range(8) if abs(x - f) >= 3]), 6)
    br = sq(rnd.choice([x for x in range(8) if abs(x - f) >= 3]), 5)
    if len({wk, wr, br, sq(f, 4), sq(f, 7)}) < 5: return None
    return board([(sq(f, 7), 'k'), (sq(f, 4), 'P'), (wk, 'K'), (wr, 'R'), (br, 'r')], chess.BLACK)


def make_cut(rnd):
    f = rnd.randrange(2, 6); pr = rnd.randrange(3, 5); side = rnd.choice([-1, 1])
    fk = f + side * rnd.choice([2, 3])
    if not 0 <= fk <= 7: return None
    wk = sq(f + rnd.choice([-1, 0]) * side, pr - 1)
    wr = sq(f + side, rnd.choice([0, 7]))
    bk = sq(fk, rnd.randrange(3, 7))
    br = sq(rnd.choice([x for x in range(8) if x not in (f, f + side, fk)]), rnd.choice([0, 1, 7]))
    if len({wk, wr, bk, br, sq(f, pr)}) < 5: return None
    return board([(wk, 'K'), (sq(f, pr), 'P'), (wr, 'R'), (bk, 'k'), (br, 'r')], chess.WHITE)


def make_qp(rnd):
    f = rnd.choice([1, 3, 4, 6])
    bk = sq(min(7, max(0, f + rnd.choice([-1, 1]))), rnd.randrange(0, 3))
    wq = rnd.randrange(64); wk = rnd.randrange(64)
    if dist(wk, sq(f, 0)) < 5 or len({bk, wq, wk, sq(f, 1)}) < 4: return None
    return board([(sq(f, 1), 'p'), (bk, 'k'), (wq, 'Q'), (wk, 'K')], chess.WHITE)


# ---------------------------------------------------------------- named mating patterns
def mate_n(v): return (MATE - v) // 100 if v > MATE - 5000 else None


def solve(b, depth=18):
    """(n, the moves that mate in n) for the quickest mate Stockfish finds, or (None, []): the best move, then a
    second search without it (a second move that mates as quickly is all that matters, not which)."""
    key = f'{b.epd()}|{depth}|solve'
    _used.add(key)
    if key not in _c:
        i1 = engine().analyse(b, chess.engine.Limit(depth=depth))
        n = mate_n(pov(num(i1['score']), b.turn)); sols = []
        if n:
            first = i1['pv'][0]; sols = [first.uci()]
            rest = [m for m in b.legal_moves if m != first]
            if rest:
                i2 = engine().analyse(b, chess.engine.Limit(depth=depth), root_moves=rest)
                if mate_n(pov(num(i2['score']), b.turn)) == n: sols.append(i2['pv'][0].uci())
        _c[key] = [n, sorted(sols)]
        if len(_c) % 50 == 0: save()
    return tuple(_c[key])


def turned(b):
    """The position, mirrored left to right, with the colours swapped, and both."""
    h = b.transform(chess.flip_horizontal)
    return [b.copy(), h, b.mirror(), h.mirror()]


def noise(b, rnd):
    """One to three pawns for each side on the ranks pawns stand on, three files or more from the king being mated."""
    k = b.king(not b.turn); kf = chess.square_file(k); bb = b.copy()
    for color in (chess.WHITE, chess.BLACK):
        ranks = (1, 2) if color == chess.WHITE else (6, 5)
        want = rnd.randint(1, 3)
        for _ in range(40):
            if not want: break
            f = rnd.randrange(8)
            if abs(f - kf) < 3: continue
            s = sq(f, rnd.choice(ranks))
            if bb.piece_at(s) or any(bb.piece_at(sq(f, r)) == chess.Piece(chess.PAWN, color) for r in range(8)): continue
            bb.set_piece_at(s, chess.Piece(chess.PAWN, color)); want -= 1
    return bb if bb.is_valid() and not bb.is_check() else None


def gen_pattern(kind, bases, n, seed):
    """From each base (a mate in one to three with one quickest first move): the base turned four ways, and two of each
    with pawns added, kept while Stockfish finds the same mate with the same one first move; then taken in turn, so
    the first n mix the bases and the turns."""
    rnd = random.Random(seed); lanes = []
    for fen in bases:
        b0 = chess.Board(fen); n0, s0 = solve(b0)
        assert b0.is_valid() and n0 and len(s0) == 1, (kind, fen, n0, s0)
        for b in turned(b0):
            lane = []
            for x in [b] + [noise(b, rnd) for _ in range(2)]:
                if x is None or any(o.epd() == x.epd() for l in lanes for o in l) or any(o.epd() == x.epd() for o in lane): continue
                nn, ss = solve(x)
                if nn == n0 and len(ss) == 1: lane.append(x)
            lanes.append(lane)
    out = []
    for k in range(max(len(l) for l in lanes)):
        out += [l[k] for l in lanes if k < len(l)]
    if len(out) < n: print(f'  {kind}: only {len(out)} of {n}')
    return out[:n]


# ---------------------------------------------------------------- the other new endings, checked move by move
def meaningful(b, goal, lo, hi, depth=18, shallow=None):
    """The best move's value is in [lo, hi] (for the player), some moves throw it away and some don't; for an ending to
    hold, a shallow search (what the page runs) agrees with the deep one about every move."""
    v0 = pov(sf(b, 12)[0][0], b.turn)
    if not lo - 150 <= v0 <= hi + 150: return False
    a = sfall(b, depth)
    if not a or not lo <= max(a.values()) <= hi: return False
    good = lambda v: v > -200 if goal == 'hold' else v >= 200
    ok = {u: good(v) for u, v in a.items()}
    if all(ok.values()) or not any(ok.values()): return False
    if shallow:
        a2 = sfall(b, shallow)
        if any(good(a2.get(u, -MATE)) != ok[u] for u in ok): return False
    return True


VAL = {chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3, chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 100}


def calm(b, pawns=True):
    """No check, and nothing of theirs to take for free or for less (a loose pawn too, unless pawns=False, where
    taking pawns is what the ending is about): the exercise is the ending, not a piece left hanging."""
    if b.is_check(): return False
    for m in b.legal_moves:
        v = b.piece_at(m.to_square)
        if v is None or (v.piece_type == chess.PAWN and not pawns): continue
        if not b.is_attacked_by(not b.turn, m.to_square) or VAL[v.piece_type] > VAL[b.piece_type_at(m.from_square)]: return False
    return True


def gen_moves(kind, n, seed, make, goal, lo, hi, shallow=None, tries=1500, pawns=True):
    rnd = random.Random(seed); out = []; t = 0
    while len(out) < n and t < tries:
        t += 1
        b = make(rnd)
        if not b or b.is_game_over() or not calm(b, pawns) or any(x.epd() == b.epd() for x in out): continue
        if meaningful(b, goal, lo, hi, shallow=shallow): out.append(b.mirror() if len(out) % 3 == 2 else b)
    if len(out) < n: print(f'  {kind}: only {len(out)} of {n} after {t} tries')
    return out


def make_van(rnd):
    # your rook to place: theirs in front of its edge pawn on the sixth, their king near; yours on the far side
    wk = sq(rnd.randrange(1, 4), rnd.randrange(2, 6)); bk = sq(rnd.randrange(5, 8), rnd.randrange(5, 8))
    return board([(sq(0, 5), 'P'), (sq(0, 7), 'R'), (wk, 'K'), (bk, 'k'), (sq(rnd.randrange(2, 8), rnd.randrange(0, 8)), 'r')], chess.BLACK)


def make_ssd(rnd):
    # their pawn on the fifth or sixth with its king beside it; your king near the corner on the short side
    f = rnd.randrange(2, 6); r = rnd.choice([4, 5]); short = 1 if f >= 4 else -1
    wk = sq(f + rnd.choice([-1, 0, 1]), min(7, r + 1))
    bk = sq(min(7, max(0, f + short * rnd.choice([1, 2]))), rnd.choice([6, 7])); br = sq(0 if short > 0 else 7, rnd.randrange(0, 8))
    return board([(sq(f, r), 'P'), (wk, 'K'), (rnd.randrange(64), 'R'), (bk, 'k'), (br, 'r')], chess.BLACK)


def make_rp(rnd):
    f = rnd.randrange(1, 7); pr = rnd.randrange(1, 4)
    bk = sq(min(7, max(0, f + rnd.choice([-1, 0, 1]))), min(7, pr + rnd.choice([0, 1])))
    return board([(sq(f, pr), 'p'), (bk, 'k'), (rnd.randrange(64), 'R'), (rnd.randrange(64), 'K')], chess.WHITE)


def make_r7(rnd):
    wr = sq(rnd.randrange(0, 5), 6); br = sq(rnd.randrange(0, 8), rnd.choice([0, 1, 2, 7]))
    mine = [sq(f, rnd.choice([1, 2])) for f in (5, 6, 7)] + ([sq(0, rnd.choice([1, 2, 3]))] if rnd.random() < .5 else [])
    theirs = [sq(f, rnd.choice([5, 6])) for f in (5, 6, 7)] + ([sq(0, rnd.choice([5, 6]))] if rnd.random() < .5 else [])
    wk = sq(rnd.randrange(4, 8), rnd.randrange(0, 2)); bk = sq(rnd.randrange(4, 8), 7)
    return board([(wk, 'K'), (bk, 'k'), (wr, 'R'), (br, 'r')] + [(x, 'P') for x in mine] + [(x, 'p') for x in theirs], chess.WHITE)


def make_wb(rnd):
    # an edge pawn and the bishop that doesn't cover its corner; you to move with the lone king
    a = rnd.choice([0, 7]); p = sq(a, rnd.randrange(3, 6)); corner = sq(a, 7)
    light = lambda x: (chess.square_file(x) + chess.square_rank(x)) % 2 == 1
    bs = rnd.choice([x for x in range(64) if light(x) != light(corner) and x != p])
    return board([(p, 'P'), (bs, 'B'), (rnd.randrange(64), 'K'), (sq(rnd.randrange(8), rnd.randrange(4, 8)), 'k')], chess.BLACK)


def make_np(rnd):
    f = rnd.randrange(1, 7); pr = rnd.randrange(1, 3)
    bk = sq(min(7, max(0, f + rnd.choice([-1, 0, 1]))), pr + rnd.choice([0, 1, 2]))
    return board([(sq(f, pr), 'p'), (bk, 'k'), (rnd.randrange(64), 'N'), (rnd.randrange(64), 'K')], chess.WHITE)


def make_qpd(rnd):
    f = rnd.choice([0, 2, 5, 7]); bk = sq(min(7, max(0, f + rnd.choice([-1, 0, 1]))), rnd.randrange(0, 3))
    return board([(sq(f, 1), 'p'), (bk, 'k'), (rnd.randrange(64), 'Q'), (rnd.randrange(64), 'K')], chess.BLACK)


def make_qr(rnd):
    wk, wq, bk, br = rnd.sample(range(64), 4)
    if dist(wk, bk) > 3 or dist(br, bk) > 2: return None
    return board([(wk, 'K'), (wq, 'Q'), (bk, 'k'), (br, 'r')], chess.WHITE)


def make_con(rnd):
    f = rnd.randrange(1, 6); r = rnd.choice([4, 5])
    return board([(sq(f, r), 'P'), (sq(f + 1, r), 'P'), (rnd.randrange(64), 'K'), (rnd.randrange(64), 'k'), (rnd.randrange(64), 'r')], chess.WHITE)


def make_stm(rnd):
    a = rnd.choice([0, 7]); pr = rnd.randrange(1, 4)
    bk = sq(a + (1 if a == 0 else -1) * rnd.choice([0, 1]), rnd.randrange(0, pr + 1))
    return board([(sq(a, pr), 'p'), (bk, 'k'), (rnd.randrange(64), 'K'), (rnd.randrange(64), 'N')], chess.WHITE)


def make_pro(rnd):
    # your protected passed pawn on one wing; their extra pawn on the other
    f = rnd.choice([1, 2]); r = rnd.choice([3, 4]); pf = f + rnd.choice([-1, 1])
    mine = [sq(f, r), sq(pf, r - 1)] + [sq(x, rnd.choice([1, 2])) for x in rnd.sample([5, 6, 7], 2)]
    theirs = [sq(x, rnd.choice([5, 6])) for x in (5, 6, 7)]
    wk = sq(rnd.randrange(3, 8), rnd.randrange(0, 4)); bk = sq(rnd.randrange(0, 5), rnd.randrange(4, 8))
    return board([(wk, 'K'), (bk, 'k')] + [(x, 'P') for x in mine] + [(x, 'p') for x in theirs], chess.WHITE)


def make_tar(rnd):
    # your rook behind your passed edge pawn, theirs in front of it or on its back row; three pawns each on the other wing
    pr = rnd.choice([3, 4, 5]); wr = sq(0, rnd.randrange(0, pr)); br = sq(0, rnd.randrange(pr + 1, 8)) if rnd.random() < .7 else sq(rnd.randrange(1, 8), 7)
    mine = [sq(0, pr)] + [sq(f, rnd.choice([1, 2])) for f in (5, 6, 7)]
    theirs = [sq(f, rnd.choice([5, 6])) for f in (5, 6, 7)]
    wk = sq(rnd.randrange(4, 8), rnd.randrange(0, 3)); bk = sq(rnd.randrange(3, 8), rnd.randrange(5, 8))
    return board([(wk, 'K'), (bk, 'k'), (wr, 'R'), (br, 'r')] + [(x, 'P') for x in mine] + [(x, 'p') for x in theirs], chess.WHITE)


def gen_won(kind, n, seed, make, lo):
    """Positions Stockfish calls won (from lo, short of a mate it already sees), with no check on single moves."""
    rnd = random.Random(seed); out = []; t = 0
    while len(out) < n and t < 600:
        t += 1
        b = make(rnd)
        if not b or b.is_game_over() or not calm(b, pawns=False) or any(x.epd() == b.epd() for x in out): continue
        v = pov(sf(b, 12)[0][0], b.turn)
        if not lo - 150 <= v < 2000: continue
        v = pov(sf(b, 20)[0][0], b.turn)
        if lo <= v < MATE - 3000: out.append(b.mirror() if len(out) % 3 == 2 else b)
    if len(out) < n: print(f'  {kind}: only {len(out)} of {n}')
    return out


def gen_classic(kind, fens, n, goal, lo, hi, shift=0):
    """A few classic positions, turned four ways (and moved up to `shift` files along the board), kept while Stockfish
    agrees: the result in [lo, hi] for the player and some moves that throw it away."""
    out = []
    for fen in fens:
        b0 = chess.Board(fen)
        for d in range(shift + 1):
            pm = b0.piece_map()
            if any(chess.square_file(x) + d > 7 for x in pm): continue
            b = chess.Board(None)
            for x, p in pm.items(): b.set_piece_at(sq(chess.square_file(x) + d, chess.square_rank(x)), p)
            b.turn = b0.turn
            for x in turned(b):
                if x.is_valid() and not any(o.epd() == x.epd() for o in out) and meaningful(x, goal, lo, hi): out.append(x)
    if len(out) < n: print(f'  {kind}: only {len(out)} of {n}')
    return out[:n]


def gen_kpk_opp(n, seed):
    """King and pawn: the one winning move is a king move that takes the opposition, face to face or from afar."""
    rnd = random.Random(seed); out = []; t = 0
    while len(out) < n and t < 600000:
        t += 1
        wk, bk = rnd.sample(range(64), 2); p = sq(rnd.randrange(1, 7), rnd.randrange(1, 5))
        if p in (wk, bk): continue
        b = board([(wk, 'K'), (p, 'P'), (bk, 'k')], chess.WHITE)
        if not b: continue
        r = endtb.probe(b)
        if not r or r[0] != 1 or r[1] < 9 or b.legal_moves.count() < 5: continue
        wins = [m for m in b.legal_moves if (endtb.after(b, m) or (0,))[0] == 1]
        if len(wins) != 1 or b.piece_type_at(wins[0].from_square) != chess.KING: continue
        b.push(wins[0]); k1, k2 = b.king(chess.WHITE), b.king(chess.BLACK); b.pop()
        df, dr = abs(chess.square_file(k1) - chess.square_file(k2)), abs(chess.square_rank(k1) - chess.square_rank(k2))
        if not ((df == 0 and dr % 2 == 0) or (dr == 0 and df % 2 == 0)) or any(o.epd() == b.epd() for o in out): continue
        out.append(b.mirror() if len(out) % 3 == 2 else b)
    assert len(out) == n, ('opp', len(out))
    return out


def gen_kpk_edge(n, seed, one=False):
    """An edge pawn, you to move with the lone king: the draw is there, with one or two moves that keep it."""
    rnd = random.Random(seed); out = []; t = 0
    while len(out) < n and t < 600000:
        t += 1
        wk, bk = rnd.sample(range(64), 2); p = sq(rnd.choice([0, 7]), rnd.randrange(1, 6))
        if p in (wk, bk): continue
        b = board([(wk, 'K'), (p, 'P'), (bk, 'k')], chess.BLACK)
        if not b: continue
        r = endtb.probe(b)
        if not r or r[0] != 0 or b.legal_moves.count() < 5: continue
        keep = [m for m in b.legal_moves if (endtb.after(b, m) or (None,))[0] == 0]
        if not 1 <= len(keep) <= (1 if one else 2) or any(o.epd() == b.epd() for o in out): continue
        out.append(b.mirror() if len(out) % 3 == 2 else b)
    assert len(out) == n, ('edge', len(out))
    return out


def item(kind, i, b, **x):
    return dict(id=f'{kind}-{i + 1}', k=kind, fen=b.fen(), me='w' if b.turn == chess.WHITE else 'b', **x)


def kinds():
    K = {k['id']: k for k in E.KINDS}
    items = []; count = {}
    def add(kind, boards, v=False, **x):
        start = v
        for b in boards:
            i = count[kind] = count.get(kind, 0) + 1
            it = item(kind, i - 1, b, **x)
            if start: it['v'] = pov(sf(b)[0][0], b.turn)      # the value it starts from: the page lets a move drop to half of it
            if K[kind]['how'] in ('kqk', 'krk'):
                it['par'] = (endtb.probe(b)[1] + 1) // 2
            elif K[kind]['goal'] == 'mate':
                v = pov(sf(b)[0][0], b.turn)
                if v > MATE - 10000: it['par'] = (MATE - v) // 100
            items.append(it)
    add('q', gen_kxk('q', 'Q', 13, 19, 12, 11))
    add('r', gen_kxk('r', 'R', 21, 31, 12, 12))
    add('rr', gen_engine('rr', K['rr']['n'], 13, make_rr, lambda v, L: v > MATE - 2000))
    add('bb', gen_bare(K['bb']['n'], 14, make_bb))
    add('bn', gen_bare(K['bn']['n'], 15, make_bn))
    add('race', gen_engine('race', 4, 22, make_outside, lambda v, L: 400 <= v < MATE - 3000))
    add('kp', gen_kpk(12, 16))
    add('kpd', gen_kpk(10, 17, hold=True))
    add('luc', gen_engine('luc', 6, 18, make_luc, lambda v, L: v >= 500))
    add('phi', gen_engine('phi', 6, 19, make_phi, lambda v, L: abs(v) <= 60, depth=22))
    add('cut', gen_engine('cut', 6, 20, make_cut, lambda v, L: v >= 400))
    add('qp', gen_engine('qp', 6, 21, make_qp, lambda v, L: 500 <= v < MATE - 3000))
    # the kinds added later: named mates, then endings checked move by move (a later kind never shifts an earlier one)
    for kind, bases in E.PATTERNS.items():
        add(kind, gen_pattern(kind, bases, K[kind]['n'], 100 + sum(map(ord, kind))))
    add('opp', gen_kpk_opp(K['opp']['n'], 41))
    add('rpk', gen_kpk_edge(K['rpk']['n'], 42))
    add('tri', gen_classic('tri', E.VARIANTS['tri'], K['tri']['n'], 'win', 400, MATE, shift=4), v=True)
    add('reti', gen_classic('reti', E.VARIANTS['reti'], K['reti']['n'], 'hold', -60, 60))
    add('out', gen_won('out', K['out']['n'], 31, make_outside, 400), v=True)
    add('pro', gen_moves('pro', K['pro']['n'], 32, make_pro, 'win', 350, 2000, pawns=False), v=True)
    add('con', gen_moves('con', K['con']['n'], 33, make_con, 'queen', 400, MATE), v=True)
    add('tar', gen_moves('tar', K['tar']['n'], 34, make_tar, 'win', 250, 2000, pawns=False), v=True)
    add('van', gen_moves('van', K['van']['n'], 35, make_van, 'hold', -60, 60, shallow=12))
    add('ssd', gen_moves('ssd', K['ssd']['n'], 36, make_ssd, 'hold', -60, 60, shallow=12))
    add('rp', gen_moves('rp', K['rp']['n'], 37, make_rp, 'win', 400, 2000, tries=3000), v=True)
    add('r7', gen_moves('r7', K['r7']['n'], 38, make_r7, 'win', 250, 2000, pawns=False), v=True)
    add('wb', gen_moves('wb', K['wb']['n'], 39, make_wb, 'hold', -60, 60, shallow=12))
    add('np', gen_moves('np', K['np']['n'], 40, make_np, 'hold', -60, 60, shallow=12))
    add('stm', gen_moves('stm', K['stm']['n'], 43, make_stm, 'win', MATE - 900, MATE, tries=3000))
    add('qpd', gen_moves('qpd', K['qpd']['n'], 44, make_qpd, 'hold', -60, 60, shallow=12))
    add('qr', gen_moves('qr', K['qr']['n'], 45, make_qr, 'win', 400, MATE), v=True)
    for kind, fens in E.FIXED.items():
        keep = []
        for fen in fens:
            b = chess.Board(fen); assert b.is_valid(), fen
            v = pov(sf(b)[0][0], b.turn)
            if v >= WIN: keep.append(b)
            else: print(f'  {kind}: left out {fen} ({v})')
        add(kind, keep)
    for i, g in enumerate(E.MINE):
        b = chess.Board(g['fen']); assert b.is_valid(), g['fen']
        it = item('mine', i, b, src=g['key'], why=g['why'])
        it['v'] = pov(sf(b)[0][0], b.turn)
        items.append(it)
    for it in items:
        k = K[it['k']]
        if k.get('hold'): it['hold'] = k['hold']
    return items


# ---------------------------------------------------------------- the checkpoint: every legal move judged
def outcome(b, m, me):
    """What a move that isn't the answer does: [their reply, what follows]. stale: stalemate; mated: their reply mates;
    lose, draw: where it leaves you; less: still good, but not what was asked."""
    b.push(m)
    try:
        if b.is_stalemate(): return [None, 'stale']
        if b.is_insufficient_material(): return [None, 'draw']
        r = endtb.probe(b)
        if r is not None:
            reply = defend_move(b) if r[0] == -1 else best_table(b)
            v = -r[0]
        else:
            L = sf(b, 16)
            reply = chess.Move.from_uci(L[0][1][0]) if L[0][1] else None
            s = pov(L[0][0], me)
            v = 1 if s >= WIN else -1 if s <= -WIN else 0
            if reply is not None:
                b.push(reply); mated = b.is_checkmate(); b.pop()
                if mated: return [reply.uci(), 'mated']
        return [reply.uci() if reply else None, 'less' if v == 1 else 'lose' if v == -1 else 'draw']
    finally:
        b.pop()


def best_table(b):
    """The table's best move for the side to move: the quickest win, else a move that keeps the draw."""
    best = None
    for m in b.legal_moves:
        r = endtb.after(b, m)
        key = (0 if r and r[0] == 1 else 1 if r and r[0] == 0 else 2, (r[1] or 0) if r and r[0] == 1 else 0, 0 if b.is_capture(m) else 1)
        if best is None or key < best[0]: best = (key, m)
    return best[1]


def judge(fen, ask, hold=False, only=None):
    """The moves that answer the question, and what every other legal move runs into. only: the answers narrowed by
    hand to the move the question is about (the others that still win count as 'less')."""
    b = chess.Board(fen); me = b.turn; ok = []; vals = {}
    mn = re.search(r'mate in (two|three|four)', ask)
    mateN = {'two': 2, 'three': 3, 'four': 4}[mn.group(1)] if mn else None
    mate1 = 'Find the mate' in ask and not mateN
    first = 'first move of the mate' in ask
    r0 = endtb.probe(b)
    for m in b.legal_moves:
        b.push(m); mate = b.is_checkmate(); b.pop()
        if mate1: vals[m] = MATE if mate else 0; continue
        if r0 is not None:
            r = endtb.after(b, m)
            vals[m] = (1 if r and r[0] == 1 else 0 if r and r[0] == 0 else -1) * (1000 - (r[1] or 0) if r and r[0] == 1 else 1000)
        else:
            b.push(m); L = sf(b, 18); b.pop()
            vals[m] = pov(L[0][0], me)
    top = max(vals.values())
    if mate1: ok = [m for m, v in vals.items() if v == MATE]
    elif mateN: ok = [m for m, v in vals.items() if v >= MATE - 100 * (mateN - 1)]
    elif first: ok = [m for m, v in vals.items() if v >= top > MATE - 5000]
    elif hold: ok = [m for m, v in vals.items() if v >= -DRAWN]
    elif r0 is not None: ok = [m for m, v in vals.items() if v > 0]
    else: ok = [m for m, v in vals.items() if v >= WIN and v >= top - (150 if top < MATE - 10000 else 10 ** 9)]
    if only: ok = [m for m in ok if m.uci() in only]
    assert ok, ('no answer', fen)
    bad = {m.uci(): outcome(b, m, me) for m in b.legal_moves if m not in ok}
    return dict(fen=fen, me='w' if me == chess.WHITE else 'b', ask=ask, ok=sorted(m.uci() for m in ok), bad=bad)


def gen_checks(gen, n, seed):
    """Checkpoint positions from the tables, by kind of question."""
    rnd = random.Random(seed); out = []; tries = 0
    piece = {'krk': 'R', 'kqk': 'Q'}.get(gen.split('-')[0])
    if gen == 'kpk-edge': return gen_kpk_edge(n, seed, one=True)
    while len(out) < n and tries < 300000:
        tries += 1
        if gen in ('kbbk-mate1', 'kbnk-mate1'):
            wk, x1, x2, bk = rnd.sample(range(64), 4)
            light = lambda s: (chess.square_file(s) + chess.square_rank(s)) % 2
            if gen == 'kbbk-mate1' and light(x1) == light(x2): continue
            b = board([(wk, 'K'), (x1, 'B'), (x2, 'B' if gen == 'kbbk-mate1' else 'N'), (bk, 'k')], chess.WHITE)
            if not b or not edge(bk): continue
            mates = [m for m in b.legal_moves if b.gives_check(m) and (b.push(m) or True) and (b.is_checkmate(), b.pop())[0]]
            if len(mates) != 1 or sum(1 for m in b.legal_moves if b.gives_check(m)) < 3: continue
            if any(b.is_attacked_by(chess.BLACK, s) and not b.is_attacked_by(chess.WHITE, s) for s in (x1, x2)): continue
            if any(o.epd() == b.epd() for o in out): continue
            out.append(b); continue
        if gen.startswith('kpk'):
            hold = gen == 'kpk-hold'
            wk, bk = rnd.sample(range(64), 2); p = sq(rnd.randrange(1, 7), rnd.randrange(1, 5))
            if p in (wk, bk): continue
            b = board([(wk, 'K'), (p, 'P'), (bk, 'k')], chess.BLACK if hold else chess.WHITE)
            if not b: continue
            r = endtb.probe(b); res = {m: endtb.after(b, m) for m in b.legal_moves}
            if hold:
                keep = [m for m, x in res.items() if x and x[0] == 0]
                if not r or r[0] != 0 or len(keep) != 1 or len(res) < 5: continue
            else:
                keep = [m for m, x in res.items() if x and x[0] == 1]
                if not r or r[0] != 1 or r[1] < 7 or len(keep) != 1 or len(res) < 6: continue
        else:
            wk, x, bk = rnd.sample(range(64), 3)
            b = board([(wk, 'K'), (x, piece), (bk, 'k')], chess.WHITE)
            if not b: continue
            r = endtb.probe(b)
            if not r or r[0] != 1: continue
            if gen.endswith('mate1') or gen == 'kqk-mate1s':
                mates = [m for m in b.legal_moves if endtb.after(b, m) == (1, 0)]
                checks = [m for m in b.legal_moves if b.gives_check(m)]
                if len(mates) != 1 or len(checks) < (3 if piece == 'Q' else 2): continue
                if gen == 'kqk-mate1s':
                    stale = 0
                    for m in b.legal_moves:
                        b.push(m); stale += b.is_stalemate(); b.pop()
                    if stale < 2: continue
            elif gen == 'krk-box':
                a0 = box(b, chess.WHITE); best = {}
                for m in b.legal_moves:
                    if b.piece_type_at(m.from_square) != chess.ROOK: continue
                    rr = endtb.after(b, m)
                    if not rr or rr[0] != 1: continue
                    b.push(m); best[m] = box(b, chess.WHITE); b.pop()
                if not best: continue
                lo = min(best.values())
                if lo >= a0 or lo > 12 or list(best.values()).count(lo) != 1 or dist(wk, bk) < 3: continue
            elif gen == 'kqk-stale':
                stale = 0
                for m in b.legal_moves:
                    b.push(m); stale += b.is_stalemate(); b.pop()
                if stale < 2 or r[1] < 3: continue
        if any(o.epd() == b.epd() for o in out): continue
        out.append(b)
    assert len(out) == n, (gen, len(out))
    return out


ASK = {1: 'Find the mate.', 2: 'Find the mate in two.', 3: 'Find the mate in three.', 4: 'Find the mate in four.'}


def unit_checks(U, made=()):
    """made: the positions of the kinds; a question with `kind` takes the last one of that kind (with that `par`) not
    already asked, since practice games start from the first ones."""
    items = []; asked = set()
    for c in U['check']:
        if 'kind' in c:
            pool = [it for it in made if it['k'] == c['kind'] and (c.get('par') is None or it.get('par') == c['par']) and it['fen'] not in asked]
            assert pool, ('no position for the question', U['id'], c)
            it = pool[-1]; asked.add(it['fen'])
            ask = c.get('ask') or ASK[it['par']]
            items.append(judge(it['fen'], ask, hold='holds the draw' in ask))
        elif 'gen' in c:
            for b in gen_checks(c['gen'], c['n'], sum(map(ord, c['gen']))):
                if c['gen'] == 'krk-box':
                    a0 = box(b, chess.WHITE); vals = {}
                    for m in b.legal_moves:
                        rr = endtb.after(b, m)
                        if b.piece_type_at(m.from_square) == chess.ROOK and rr and rr[0] == 1:
                            b.push(m); vals[m] = box(b, chess.WHITE); b.pop()
                    lo = min(vals.values()); ok = [m for m, a in vals.items() if a == lo]
                    items.append(dict(fen=b.fen(), me='w', ask=c['ask'], ok=[m.uci() for m in ok],
                                      bad={m.uci(): outcome(b, m, chess.WHITE) for m in b.legal_moves if m not in ok}))
                else:
                    items.append(judge(b.fen(), c['ask'], hold=c['gen'] in ('kpk-hold', 'kpk-edge')))
        else:
            hold = 'holds the draw' in c['ask']
            items.append(judge(c['fen'], c['ask'], hold=hold, only=c.get('ok')))
    for k, it in enumerate(items): it['id'] = f"{U['id']}-c{k + 1}"
    return items


def unit_lines(U):
    out = []
    for k, a in enumerate(U['along']):
        fen = a.get('fen')
        if a.get('gen') == 'kpk-demo': fen = '8/8/8/4k3/8/3K4/4P3/8 w - - 0 1'
        b = chess.Board(fen); assert b.is_valid(), fen
        if a.get('method'): moves = table_line(fen)
        elif a.get('sfline'): moves = sf_line(fen)
        elif a.get('pv'): moves = sf(b, 24)[0][1][:a['pv']]
        else:
            moves = a['moves'].split()
            bb = b.copy()
            for u in moves: m = chess.Move.from_uci(u); assert m in bb.legal_moves, (fen, u); bb.push(m)
            v = pov(sf(bb)[0][0], b.turn)
            assert v >= WIN, ('the line given by hand is not won at its end', fen, v)
        out.append(dict(id=f"{U['id']}-a{k + 1}", fen=b.fen(), me='w' if b.turn == chess.WHITE else 'b', moves=moves))
    return out


def sf_line(fen, plies=140):
    """Stockfish's line for both sides to the mate (the tables once only three pieces are left). The side that mates
    never goes back to a position the line has had: of Stockfish's four best moves, the first that doesn't."""
    b = chess.Board(fen); out = []; me = b.turn; seen = {b.board_fen() + str(b.turn)}
    while not b.is_game_over() and len(out) < plies:
        r = endtb.probe(b)
        if r is not None: m = best_table(b) if r[0] >= 0 else defend_move(b)
        elif b.turn == me:
            for _, pv in sf(b, 20, 4):
                m = chess.Move.from_uci(pv[0]); b.push(m); k = b.board_fen() + str(b.turn); b.pop()
                if k not in seen: break
        else: m = chess.Move.from_uci(sf(b, 20)[0][1][0])
        out.append(m.uci()); b.push(m); seen.add(b.board_fen() + str(b.turn))
    assert b.is_checkmate(), ('the line did not mate', fen, len(out))
    return out


def good_move(b, m):
    """Is m as good as the position allows: the same result by the tables, or by Stockfish (a mate kept, a win kept
    within 2, a draw kept)?"""
    if endtb.which(b):
        res = lambda x: (endtb.after(b, x) or (0,))[0]
        return res(m) == max(res(x) for x in b.legal_moves)
    a = sfall(b, 18); v = a[m.uci()]; top = max(a.values())
    if top > MATE - 5000: return v > MATE - 5000
    if top >= WIN: return v >= WIN and v >= top - 200
    if top >= -DRAWN: return v >= -DRAWN
    return v >= top - 100


def slide(s):
    """A picture to learn from, checked: a legal position, squares and colours, and the first green arrow, when it is a
    move for the side to move, one that keeps what the position has."""
    b = chess.Board(s['fen']); assert b.is_valid(), s['fen']
    for a in s.get('arrows', []) + s.get('circles', []):
        chess.parse_square(a[:2]); assert a[-1] in 'grby', a
    g = [a for a in s.get('arrows', []) if a[-1] == 'g']
    if g:
        m = chess.Move.from_uci(g[0][:4])
        if m in b.legal_moves: assert good_move(b, m), ('a green arrow that throws something away', s['fen'], g[0])
    return dict(fen=s['fen'], me=s.get('me', 'w'), arrows=s.get('arrows', []), circles=s.get('circles', []), h=s['h'], t=s['t'])


def unit_slides(U, ideas=None):
    """A unit's pictures: its own, or a kind's idea pictures where it names a kind."""
    out = []
    for s in U['slides']:
        out += ideas[s] if isinstance(s, str) else [slide(s)]
    return out


def main():
    items = kinds()
    ideas = {K['id']: [slide(x) for x in K.get('idea', [])] for K in E.KINDS}
    units = [dict(id=U['id'], title=U['title'], why=U['why'], kinds=U['kinds'], need=U['need'], slides=unit_slides(U, ideas),
                  along=unit_lines(U), check=unit_checks(U, items), **({'lib': True} if U in E.LIB else {})) for U in E.UNITS + E.LIB]
    kinds_out = []
    for K in E.KINDS:
        k = {x: v for x, v in K.items() if x not in ('n', 'idea')}
        if ideas[K['id']]: k['idea'] = ideas[K['id']]
        kinds_out.append(k)
    data = dict(kinds=kinds_out, items=items, units=units)
    OUT.write_text(json.dumps(data, separators=(',', ':')))
    global FULL
    FULL = True
    from collections import Counter
    print('items', dict(Counter(i['k'] for i in items)), '| units', len(units), '| checks', sum(len(u['check']) for u in units),
          '| lines', sum(len(u['along']) for u in units), '|', len(OUT.read_text()), 'bytes')


FULL = False

if __name__ == '__main__':
    code = 0
    try: main()
    except BaseException:
        import traceback; traceback.print_exc(); code = 1     # os._exit below would swallow it otherwise
    finally:
        save(full=FULL)
        if _eng: _eng.quit()
        os._exit(code)
