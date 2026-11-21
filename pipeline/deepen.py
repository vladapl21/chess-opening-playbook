"""Lines that stop while the opening is still going on are played on. Part of both book builds.

A line as written often ends when the pieces are out. From there it is continued, two moves at a time:
  the other side plays the reply a player at this level picks most often (the Maia odds of pipeline/expand.py),
  your side plays, in this order,
    1. a move fixed by hand for that exact path (`FIXED` in content/deepen_fixes.py),
    2. the move the book already plays from that position, in any line you can hold together with this one
       (one position, one move),
    3. the engine's best move when it is a capture, a check, or clearly better than the next one (a check that takes
       nothing gives way to a capture that is as good: checks that only mark time lead in circles),
    4. castling, then a knight or a bishop coming off its home square, if the engine has it within TOL of its best,
    5. the engine's best move.
A line never comes back to a position it has had. It goes on until the line is MIN plies long and the next step is not a forced or only move (a capture to take back, or a
position where the second-best move is ONLY centipawns worse), and never past MAX plies. Left alone: a line that
already ends with a won game, a mate, or on the other side's move (a line that shows a mistake on purpose), and a stem,
a line whose last position other lines go on from (a lesson on the first three moves is not played on into one of the
openings that follow it).

The result for every line is kept in data/cache/deepen_cache.json, keyed by the side and the line's written moves, so a
rebuild reads it and needs no engine; a new or changed line needs Stockfish and the Maia weights once (pipeline/draft.py's
engine and cache do the work). `KEEP` in content/deepen_fixes.py lists lines that stay as written.

    apply(lessons, me, parts, packs)      in a build: puts the longer paths in place
    python3 pipeline/deepen.py            a report: how many lines grew and by how much
"""
import json
import chess
import paths
import expand as X

CACHE = paths.CACHE / 'deepen_cache.json'
MIN, MAX, TOL, WIN, ONLY, DEPTH, PV = 18, 26, 30, 350, 70, 15, 4
RULES = f'{MIN}.{MAX}.{TOL}.{WIN}.{ONLY}'              # part of every cache key: other limits, other lines
_c = json.load(open(CACHE)) if CACHE.exists() else {}
_dirty = False

try:
    import deepen_fixes as F
except ImportError:                                    # no hand fixes yet
    class F: FIXED, REPLY, KEEP = {}, {}, set()


def board_of(path):
    b = chess.Board()
    for s in path.split(): b.push_san(s)
    return b


def _best(b):
    import draft
    return draft.best(b, DEPTH, PV)


_fx = None
def _fixed_at():
    """FIXED by position: a move fixed for one path holds for every order of moves that reaches the same position."""
    global _fx
    if _fx is None: _fx = {board_of(p).epd(): san for p, san in F.FIXED.items()}
    return _fx


def choose(b):
    """Your move from a position the book has no move for yet (rules 3 to 5)."""
    top = _best(b); s0, v0 = top[0]; m0 = b.parse_san(s0)
    if b.gives_check(m0) and not b.is_capture(m0):            # a check that only marks time: a capture as good as it comes first
        for s, v in top[1:]:
            if v0 - v <= (15 if v0 < WIN else 60) and b.is_capture(b.parse_san(s)): return s    # won already: the numbers are loose
    if len(top) == 1 or b.is_capture(m0) or b.gives_check(m0) or v0 - top[1][1] >= 40: return s0
    ok = [s for s, v in top if v0 - v <= TOL]
    for s in ok:
        if s in ('O-O', 'O-O-O'): return s
    home = 0 if b.turn == chess.WHITE else 7
    for s in ok:
        m = b.parse_san(s); p = b.piece_at(m.from_square)
        if p.piece_type in (chess.KNIGHT, chess.BISHOP) and chess.square_rank(m.from_square) == home and not b.is_capture(m): return s
    return s0


class Seen:
    """The move the book plays from a position, for the lines a player can hold together: a line of one pack never
    takes its move from another pack of the same slot."""
    def __init__(self): self.d = {}
    def add(self, epd, ctx, san): self.d.setdefault(epd, []).append((ctx, san))
    def get(self, epd, ctx):
        for c, san in self.d.get(epd, []):
            if c is None or ctx is None or c == ctx or c[0] != ctx[0]: return san
        return None


def extension(path, me, ctx, seen):
    """The moves to add to a line that ends at `path` (your move was the last one)."""
    toks = path.split(); b = board_of(path); out = []
    if b.turn == me or b.is_game_over(): return out          # ends on the other side's move, or the game is over
    been = set(); w = chess.Board(); been.add(w.epd())       # every position this line has had: it never walks in a circle
    for s in toks: w.push_san(s); been.add(w.epd())
    def circles(san):
        b.push_san(san); r = b.epd() in been; b.pop(); return r
    last = b.peek(); b.pop(); forcing = b.is_capture(last) or b.gives_check(last); b.push(last)
    while True:
        n = len(toks) + len(out); cur = ' '.join(toks + out)
        if n >= MAX or b.is_game_over(): break
        mine = -_best(b)[0][1]                                # the position for your side, the other side to move
        if mine >= WIN and n >= 8 and not forcing: break      # won already: nothing left to learn by heart
        if not out and mine <= -200: break                    # a line that shows what goes wrong stays as written
        hs = X.human(cur)
        opp = F.REPLY.get(cur) or (hs[0][0] if hs else None)
        if not opp: break
        mo = b.parse_san(opp); cap = b.is_capture(mo)
        b.push(mo)
        if b.is_game_over(): b.pop(); break
        nxt = cur + ' ' + opp; epd = b.epd(); legal = {b.san(m) for m in b.legal_moves}
        known = F.FIXED.get(nxt) or _fixed_at().get(epd) or seen.get(epd, ctx)
        if known in legal and circles(known): known = None                  # the book's move here leads back: play on instead
        if n >= MIN and not forcing and not cap and known is None:
            top = _best(b)
            if len(top) < 2 or top[0][1] - top[1][1] < ONLY: b.pop(); break    # nothing forced comes next: the line can end here
        san = known if known in legal else choose(b)
        if circles(san):                                      # a check that only repeats: the best move that goes somewhere new
            top = _best(b); fresh = [s for s, v in top if not circles(s) and top[0][1] - v <= 150]
            if not fresh: b.pop(); break                      # repeating is all there is: the line ends before it
            san = fresh[0]
        m = b.parse_san(san); forcing = b.is_capture(m) or b.gives_check(m)
        been.add(epd); seen.add(epd, ctx, san); b.push(m); been.add(b.epd()); out += [opp, san]
    return out


def stale(path, ext):
    """A kept answer that a hand fix has overtaken, or one that walks in a circle: it is worked out again."""
    if F.REPLY.get(path) and not ext: return True
    b = chess.Board(); been = {b.epd()}; toks = path.split(); fx = _fixed_at()
    for s in toks: b.push_san(s); been.add(b.epd())
    for k, s in enumerate(ext):
        cur = ' '.join(toks + ext[:k])
        if k % 2 == 0:
            if F.REPLY.get(cur) not in (None, s): return True               # the other side's move was set by hand since
        else:
            want = F.FIXED.get(cur) or fx.get(b.epd())
            if want and want != s: return True                              # yours was
        b.push_san(s)
        if b.epd() in been: return True
        been.add(b.epd())
    return False


def contexts(lessons, parts, packs):
    """lesson id -> (slot, pack), or None for a lesson outside the slots (it goes with every pack)."""
    part_ch = {p['id']: p['ch'] for p in parts}
    ch_ctx = {ch: (slot, pk) for slot, P in (packs or {}).items() for pk, chs in P['packs'].items() for ch in chs}
    return {l['id']: ch_ctx.get(part_ch.get(l['part'])) for l in lessons}


def apply(lessons, me, parts, packs, quiet=False):
    """Put the longer paths in place (lessons are changed where they stand). Returns {line id: plies added}."""
    global _dirty
    side = chess.WHITE if me == 'w' else chess.BLACK
    ctx = contexts(lessons, parts, packs); seen = Seen(); todo = []; grew = {}
    lines = [(l['id'], l['id'], l['path'], None) for l in lessons] + [(l['id'], a[0], a[2], k) for l in lessons for k, a in enumerate(l['alts'])]
    lines.sort(key=lambda x: (x[3] is not None,))            # every lesson's main line first, then the side lines
    def register(path, c):
        b = chess.Board()
        for s in path.split():
            if b.turn == side: seen.add(b.epd(), c, s)
            b.push_san(s)
    for les, lid, path, k in lines: register(path, ctx[les])                 # the book as written comes first
    # a stem: other lines go on from its end. The side lines pipeline/fill.py drafts (ids with -f-) don't count: they branch
    # off inside what the build adds, and the line they leave is still played on
    paths_ = sorted({p for _, lid, p, _ in lines if '-f-' not in lid})
    stems = {p for i, p in enumerate(paths_) if i + 1 < len(paths_) and paths_[i + 1].startswith(p + ' ')}
    key_of = lambda path: f'{me}|{RULES}|{path}'
    old = {path for _, _, path, _ in lines if key_of(path) in _c and stale(path, _c[key_of(path)])}
    for path in old: del _c[key_of(path)]                                    # overtaken by a hand fix: worked out again below
    for les, lid, path, k in lines:                                          # then what earlier builds worked out
        ext = _c.get(key_of(path))
        if ext and path not in stems: register(path + ' ' + ' '.join(ext), ctx[les])
    new = 0
    for les, lid, path, k in lines:
        key = key_of(path)
        if lid in F.KEEP or path in stems: ext = []
        elif key in _c: ext = _c[key]
        else:
            ext = _c[key] = extension(path, side, ctx[les], seen); _dirty = True; new += 1
            if new % 25 == 0: save(); print(f'  deepen {me}: {new} new lines', flush=True)
        if ext: grew[lid] = len(ext)
        full = (path + ' ' + ' '.join(ext)).strip()
        L = next(l for l in lessons if l['id'] == les)
        if k is None: L['path'] = full
        else: L['alts'][k] = (L['alts'][k][0], L['alts'][k][1], full)
    save()
    if new:                                                   # the engine was started for the new lines: quit it here, not at exit
        import draft
        if draft._eng is not None: draft._eng.quit(); draft._eng = None
    if not quiet: print(f'deepen {me}: {len(grew)} of {len(lines)} lines played on, {sum(grew.values())} plies added ({new} worked out now)', flush=True)
    return grew


def save():
    global _dirty
    if not _dirty: return
    json.dump(_c, open(CACHE, 'w'), sort_keys=True, indent=0, separators=(',', ':'))
    try:
        import draft; draft.save()
    except Exception: pass
    _dirty = False


if __name__ == '__main__':
    import collections
    n = collections.Counter(len(v) for v in _c.values())
    print(len(_c), 'lines in the cache; plies added:', dict(sorted(n.items())))
