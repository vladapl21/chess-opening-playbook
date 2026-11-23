"""The exact tables (data/endings/tables.json, from pipeline/endtables.mjs) for python-chess boards.

probe(board) gives the value for the side to move: (+1, plies) a win, (-1, plies) a loss, (0, None) a draw, or None
when the position isn't one of the three endings (a lone king against king and queen, king and rook, king and pawn).
For king and pawn the plies count to the promotion that wins; for the other two, to mate.
"""
import base64, json, zlib
import paths
import chess

_T = None


def tables():
    global _T
    if _T is None:
        T = json.load(open(paths.DATA / 'endings' / 'tables.json'))
        _T = {k: zlib.decompress(base64.b64decode(T[k])) for k in ('kqk', 'krk', 'kpk')}
    return _T


NAME = {chess.QUEEN: 'kqk', chess.ROOK: 'krk', chess.PAWN: 'kpk'}


def which(b):
    """(table name, strong colour, its piece's square) or None."""
    pm = b.piece_map()
    if len(pm) != 3: return None
    extra = [(s, p) for s, p in pm.items() if p.piece_type != chess.KING]
    if len(extra) != 1 or extra[0][1].piece_type not in NAME: return None
    s, p = extra[0]
    return NAME[p.piece_type], p.color, s


def probe(b):
    w = which(b)
    if not w: return None
    name, strong, x = w
    wk, bk = b.king(strong), b.king(not strong)
    if strong == chess.BLACK:                      # the tables have the stronger side as White: turn the board over
        wk, bk, x = chess.square_mirror(wk), chess.square_mirror(bk), chess.square_mirror(x)
    stm = 0 if b.turn == strong else 1
    v = tables()[name][(((wk * 64 + x) * 64 + bk) * 2) + stm]
    if not v: return (0, None)
    return (1, v - 1) if stm == 0 else (-1, v - 1)


def after(b, m):
    """The value for the side that played m, after it (the same scale as probe, turned to the mover)."""
    b.push(m)
    try:
        if b.is_checkmate(): return (1, 0)
        if b.is_stalemate() or b.is_insufficient_material(): return (0, None)
        r = probe(b)
        if r is None:
            # a promotion leaves king and pawn: the queen or rook table answers for the new piece
            return None
        return (-r[0], r[1])
    finally:
        b.pop()
