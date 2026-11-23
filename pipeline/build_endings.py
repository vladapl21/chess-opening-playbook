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
import json, math, os, random, sys
import paths
import chess, chess.engine
import endtb
import endings as E

CACHE = paths.CACHE / 'end_build_cache.json'
OUT = paths.BUILD / 'data_endings.json'
_c = json.load(open(CACHE)) if CACHE.exists() else {}
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
    if key not in _c:
        if b.is_game_over():
            v = (-MATE if b.turn == chess.WHITE else MATE) if b.is_checkmate() else 0
            _c[key] = [[v, []]]
        else:
            infos = engine().analyse(b, chess.engine.Limit(depth=depth), multipv=multipv)
            _c[key] = [[num(i['score']), [m.uci() for m in i.get('pv', [])[:24]]] for i in infos]
            if len(_c) % 50 == 0: save()
    return _c[key]


def save(): json.dump(_c, open(CACHE, 'w'))


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


def item(kind, i, b, **x):
    return dict(id=f'{kind}-{i + 1}', k=kind, fen=b.fen(), me='w' if b.turn == chess.WHITE else 'b', **x)


def kinds():
    K = {k['id']: k for k in E.KINDS}
    items = []; count = {}
    def add(kind, boards, **x):
        for b in boards:
            i = count[kind] = count.get(kind, 0) + 1
            it = item(kind, i - 1, b, **x)
            if K[kind]['how'] in ('kqk', 'krk'):
                it['par'] = (endtb.probe(b)[1] + 1) // 2
            elif K[kind]['goal'] == 'mate':
                v = pov(sf(b)[0][0], b.turn)
                if v > MATE - 10000: it['par'] = (MATE - v) // 100
            items.append(it)
    add('q', gen_kxk('q', 'Q', 13, 19, 12, 11))
    add('r', gen_kxk('r', 'R', 21, 31, 12, 12))
    add('rr', gen_engine('rr', 6, 13, make_rr, lambda v, L: v > MATE - 2000))
    add('bb', gen_bare(4, 14, make_bb))
    add('bn', gen_bare(4, 15, make_bn))
    add('race', gen_engine('race', 4, 22, make_outside, lambda v, L: 400 <= v < MATE - 3000))
    add('kp', gen_kpk(12, 16))
    add('kpd', gen_kpk(10, 17, hold=True))
    add('luc', gen_engine('luc', 6, 18, make_luc, lambda v, L: v >= 500))
    add('phi', gen_engine('phi', 6, 19, make_phi, lambda v, L: abs(v) <= 60, depth=22))
    add('cut', gen_engine('cut', 6, 20, make_cut, lambda v, L: v >= 400))
    add('qp', gen_engine('qp', 6, 21, make_qp, lambda v, L: 500 <= v < MATE - 3000))
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
    mate2 = 'mate in two' in ask
    mate1 = 'Find the mate' in ask and not mate2
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
    elif mate2: ok = [m for m, v in vals.items() if v >= MATE - 100]
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
    while len(out) < n and tries < 300000:
        tries += 1
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


def unit_checks(U):
    items = []
    for c in U['check']:
        if 'gen' in c:
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
                    items.append(judge(b.fen(), c['ask'], hold=c['gen'] == 'kpk-hold'))
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
        elif a.get('pv'): moves = sf(b, 24)[0][1][:a['pv']]
        else:
            moves = a['moves'].split()
            bb = b.copy()
            for u in moves: m = chess.Move.from_uci(u); assert m in bb.legal_moves, (fen, u); bb.push(m)
            v = pov(sf(bb)[0][0], b.turn)
            assert v >= WIN, ('the line given by hand is not won at its end', fen, v)
        out.append(dict(id=f"{U['id']}-a{k + 1}", fen=b.fen(), me='w' if b.turn == chess.WHITE else 'b', moves=moves))
    return out


def unit_slides(U):
    out = []
    for s in U['slides']:
        b = chess.Board(s['fen']); assert b.is_valid(), s['fen']
        for a in s.get('arrows', []) + s.get('circles', []):
            chess.parse_square(a[:2]); assert a[-1] in 'grby', a
        out.append(dict(fen=s['fen'], me=s.get('me', 'w'), arrows=s.get('arrows', []), circles=s.get('circles', []), h=s['h'], t=s['t']))
    return out


def main():
    items = kinds()
    units = [dict(id=U['id'], title=U['title'], why=U['why'], kinds=U['kinds'], need=U['need'], slides=unit_slides(U),
                  along=unit_lines(U), check=unit_checks(U)) for U in E.UNITS]
    data = dict(kinds=[{k: v for k, v in K.items() if k not in ('n',)} for K in E.KINDS], items=items, units=units)
    OUT.write_text(json.dumps(data, separators=(',', ':')))
    from collections import Counter
    print('items', dict(Counter(i['k'] for i in items)), '| units', len(units), '| checks', sum(len(u['check']) for u in units),
          '| lines', sum(len(u['along']) for u in units), '|', len(OUT.read_text()), 'bytes')


if __name__ == '__main__':
    try: main()
    finally:
        save()
        if _eng: _eng.quit()
        os._exit(0)
