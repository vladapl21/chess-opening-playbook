"""The endings in the house player's games: which won endings slipped, and how (data/endings_scan.json).

Every game in data/games is replayed. From the first position that counts as an ending (each side with 14 points of
pieces or less, pawns not counted, and 22 or less for both), every position is scored by Stockfish at depth 14
(data/cache/end_cache.json, so a second run needs no engine). A won ending is one where the house player stands at +3
or better, or has a mate. For each game with one, the scan keeps:

  won   the first won position of the ending (its kind, by the material on the board then);
  slip  the first move of the house player's after which the score fell under +1.5 (the position before it, the move,
        the engine's move there, the scores before and after), when there is one;
  bare  the first position where the other side had only its king (and maybe pawns), and how many moves the game
        went on from there;
  how   how the game ended (won, or lost or drawn: on time, stalemate, repetition, a blunder ...).

Usage: python3 pipeline/scan_endings.py   (needs STOCKFISH unless the cache covers every position)
"""
import json, os, collections
import paths
from common import chess
ME = {'aqua_alpaca', 'vladapl'}
FILES = ['aqua_alpaca.pgn', 'vladapl_1.pgn', 'vladapl_2.pgn']
CACHE = paths.CACHE / 'end_cache.json'
OUT = paths.DATA / 'endings_scan.json'
DEPTH = 14
VAL = {chess.KNIGHT: 3, chess.BISHOP: 3, chess.ROOK: 5, chess.QUEEN: 9}
WIN, LOST = 300, 150

_c = json.load(open(CACHE)) if CACHE.exists() else {}
_eng = None


def engine():
    global _eng
    if _eng is None:
        _eng = chess.engine.SimpleEngine.popen_uci(paths.STOCKFISH)
        _eng.configure({'Threads': 2, 'Hash': 256})
    return _eng


def score(b):
    """White's score in centipawns (mate: +-10000 less the distance), and the engine's move."""
    key = b.epd()
    if key in _c: return _c[key]
    if b.is_checkmate(): r = [-10000 if b.turn == chess.WHITE else 10000, None]
    elif b.is_stalemate() or b.is_insufficient_material(): r = [0, None]
    else:
        inf = engine().analyse(b, chess.engine.Limit(depth=DEPTH))
        s = inf['score'].white()
        v = (10000 - abs(s.mate())) * (1 if s.mate() > 0 else -1) if s.is_mate() else s.score()
        r = [v, inf['pv'][0].uci() if inf.get('pv') else None]
    _c[key] = r
    return r


def pieces(b, color):
    return sum(VAL.get(p.piece_type, 0) for p in b.piece_map().values() if p.color == color)


def is_ending(b):
    w, k = pieces(b, chess.WHITE), pieces(b, chess.BLACK)
    return w <= 14 and k <= 14 and w + k <= 22


def kind(b, me):
    """The kind of ending, from the side of the house player (me: a colour)."""
    def has(color):
        c = collections.Counter(p.piece_type for p in b.piece_map().values() if p.color == color)
        return c
    a, o = has(me), has(not me)
    heavy = lambda c: c[chess.QUEEN] + c[chess.ROOK]
    minors = lambda c: c[chess.BISHOP] + c[chess.KNIGHT]
    bare = sum(v for t, v in o.items() if t not in (chess.KING, chess.PAWN)) == 0
    if bare and o[chess.PAWN] == 0:
        if a[chess.QUEEN] and not a[chess.ROOK] and not minors(a): return 'mate-q'
        if a[chess.ROOK] == 1 and not a[chess.QUEEN] and not minors(a): return 'mate-r'
        if heavy(a) >= 2: return 'mate-2'
        if a[chess.BISHOP] == 2 and not heavy(a): return 'mate-bb'
        if a[chess.BISHOP] and a[chess.KNIGHT] and not heavy(a): return 'mate-bn'
    if bare: return 'bare'                                   # their king and pawns against your pieces
    if not heavy(a) and not minors(a) and not heavy(o) and not minors(o): return 'pawn'
    if a[chess.QUEEN] and o[chess.QUEEN] == 0 and heavy(o) + minors(o) <= 1 and not o[chess.ROOK]: return 'queen-v'
    if a[chess.ROOK] and o[chess.ROOK] and not a[chess.QUEEN] and not o[chess.QUEEN] and not minors(a) and not minors(o): return 'rook'
    if a[chess.QUEEN] or o[chess.QUEEN]: return 'queen'
    if not heavy(a) and not heavy(o): return 'minor'
    return 'mixed'


def games():
    seen = set()
    for f in FILES:
        fh = open(paths.GAMES / f)
        while True:
            g = chess.pgn.read_game(fh)
            if g is None: break
            h = g.headers
            if h.get('White') in ME: me = chess.WHITE
            elif h.get('Black') in ME: me = chess.BLACK
            else: continue
            key = (h.get('White'), h.get('Black'), h.get('Date'), h.get('EndTime', ''))
            if key in seen: continue
            seen.add(key)
            yield g, me


def how(h, me, b):
    res = h.get('Result'); t = (h.get('Termination') or '').lower()
    mine = '1-0' if me == chess.WHITE else '0-1'
    if res == mine: return 'won'
    if 'stalemate' in t: return 'stalemate'
    if 'repetition' in t: return 'repetition'
    if 'insufficient' in t: return 'timeout-draw' if 'time' in t else 'insufficient'
    if 'time' in t: return 'timeout'
    if 'agreement' in t: return 'agreed'
    if 'abandon' in t: return 'abandoned'
    if 'checkmate' in t: return 'mated'
    if 'resignation' in t: return 'resigned'
    if '50' in t or 'fifty' in t: return 'fifty'
    return 'other'


def main():
    out = []
    n_games = n_end = 0
    for g, me in games():
        n_games += 1
        h = g.headers; b = g.board(); sign = 1 if me == chess.WHITE else -1
        moves = list(g.mainline_moves())
        rec = None; plies = []
        started = False
        for i, mv in enumerate(moves + [None]):
            if not started and is_ending(b): started = True
            if started:
                v, best = score(b)
                plies.append(dict(i=i, fen=b.fen(), v=v * sign, best=best, mv=mv.uci() if mv else None, mine=b.turn == me, kind=kind(b, me)))
            if mv is None: break
            b.push(mv)
        if not plies: continue
        n_end += 1
        won = next((p for p in plies if p['v'] >= WIN), None)
        if not won: continue
        k0 = won['kind']
        slip = None
        for a, p in zip(plies, plies[1:]):
            if a['i'] < won['i'] or not a['mine'] or a['v'] < WIN: continue
            if p['v'] < LOST:
                slip = dict(fen=a['fen'], move=a['mv'], best=a['best'], before=a['v'], after=p['v'], kind=a['kind'], ply=a['i'])
                break
        bare = next((p for p in plies if p['i'] >= won['i'] and p['kind'].startswith('mate-')), None)
        ending = how(h, me, b)
        rec = dict(opp=h.get('Black') if me == chess.WHITE else h.get('White'), date=h.get('Date'), tc=h.get('TimeControl'),
                   me='w' if me == chess.WHITE else 'b', res=ending, term=h.get('Termination'), plies=len(moves),
                   won=dict(fen=won['fen'], kind=k0, ply=won['i'], v=won['v']), slip=slip,
                   bare=dict(fen=bare['fen'], kind=bare['kind'], ply=bare['i'], left=(len(moves) - bare['i'] + 1) // 2) if bare else None)
        out.append(rec)
    json.dump(_c, open(CACHE, 'w'))
    summary = dict(games=n_games, endings=n_end, won=len(out),
                   converted=sum(r['res'] == 'won' for r in out),
                   by_kind={k: dict(won=sum(r['won']['kind'] == k for r in out), kept=sum(r['won']['kind'] == k and r['res'] == 'won' for r in out))
                            for k in sorted({r['won']['kind'] for r in out})},
                   slips=collections.Counter(r['slip']['kind'] for r in out if r['slip'] and r['res'] != 'won'),
                   how=collections.Counter(r['res'] for r in out))
    json.dump(dict(summary=summary, games=out), open(OUT, 'w'), indent=1)
    print(json.dumps(summary, indent=1))
    if _eng: _eng.quit()


if __name__ == '__main__':
    main()
    os._exit(0)
