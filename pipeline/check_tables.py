"""Check data/endings/tables.json against python-chess's own move rules: python3 pipeline/check_tables.py [samples]

For random positions of each table (all of them with 'all'), every legal move is played with python-chess and the
stored value must follow from the values of the positions the moves reach: White to move wins in n plies when the
quickest win is a move to a position lost in n - 1; Black to move is lost in n when every move reaches a White win and
the longest is n - 1; a mate is lost in 0; anything else is a draw. In king and pawn against king, a promotion that
wins (by the queen and rook tables) is a win in one ply.
"""
import base64, json, random, sys, zlib
import paths
import chess

T = json.load(open(paths.DATA / 'endings' / 'tables.json'))
TB = {k: zlib.decompress(base64.b64decode(T[k])) for k in ('kqk', 'krk', 'kpk')}
PIECE = {'kqk': chess.QUEEN, 'krk': chess.ROOK, 'kpk': chess.PAWN}


def val(name, wk, x, bk, stm):
    v = TB[name][(((wk * 64 + x) * 64 + bk) * 2) + stm]
    return v - 1 if v else None


def board(name, wk, x, bk, stm):
    b = chess.Board(None)
    b.set_piece_at(wk, chess.Piece(chess.KING, chess.WHITE))
    b.set_piece_at(x, chess.Piece(PIECE[name], chess.WHITE))
    b.set_piece_at(bk, chess.Piece(chess.KING, chess.BLACK))
    b.turn = chess.WHITE if stm == 0 else chess.BLACK
    return b


def expect(name, b):
    """The value the rules give, from the stored values of the positions one move on."""
    wk, bk = b.king(chess.WHITE), b.king(chess.BLACK)
    if b.turn == chess.WHITE:
        best = None
        for m in b.legal_moves:
            if m.promotion:
                if m.promotion in (chess.QUEEN, chess.ROOK):
                    t = 'kqk' if m.promotion == chess.QUEEN else 'krk'
                    if val(t, wk, m.to_square, bk, 1) is not None: best = 1
                continue
            b.push(m)
            x = next(s for s, p in b.piece_map().items() if p.color == chess.WHITE and p.piece_type != chess.KING)
            v = val(name, b.king(chess.WHITE), x, bk, 1)
            b.pop()
            if v is not None and (name != 'kpk' or best != 1):
                c = v + 1
                if best is None or c < best: best = c
        return best
    moves = list(b.legal_moves)
    if not moves: return 0 if b.is_check() else None
    worst = -1
    for m in moves:
        b.push(m)
        if len(b.piece_map()) == 2: b.pop(); return None          # the piece is gone: a draw
        x = next(s for s, p in b.piece_map().items() if p.color == chess.WHITE and p.piece_type != chess.KING)
        v = val(name, b.king(chess.WHITE), x, b.king(chess.BLACK), 0)
        b.pop()
        if v is None: return None
        worst = max(worst, v)
    return worst + 1


def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else '40000'
    rnd = random.Random(7)
    for name in ('kqk', 'krk', 'kpk'):
        bad = n = 0
        xs = range(8, 56) if name == 'kpk' else range(64)
        if arg == 'all': todo = ((wk, x, bk, s) for wk in range(64) for x in xs for bk in range(64) for s in (0, 1))
        else: todo = ((rnd.randrange(64), rnd.choice(list(xs)), rnd.randrange(64), rnd.randrange(2)) for _ in range(int(arg)))
        for wk, x, bk, s in todo:
            if len({wk, x, bk}) < 3 or chess.square_distance(wk, bk) < 2: continue
            b = board(name, wk, x, bk, s)
            if not b.is_valid(): continue
            n += 1
            e, v = expect(name, b), val(name, wk, x, bk, s)
            if e != v:
                bad += 1
                if bad <= 5: print('  MISMATCH', name, b.fen(), 'stored', v, 'expected', e)
        print(name, 'checked', n, 'positions,', bad, 'wrong', '| longest', T['meta'][name]['max'], 'plies')
        assert not bad


if __name__ == '__main__':
    main()
