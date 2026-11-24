"""Endgame positions from the lichess puzzle database (CC0, database.lichess.org), by rating.

Not part of the build: run it on the database file once and commit what it writes.
    python3 pipeline/lichess_endings.py <lichess_db_puzzle.csv or .csv.zst>  ->  data/endings/puzzles.json

A puzzle there is a position from a real game, the opponent's move that set it up, and the solution; its rating says
how hard players found it. This keeps the well-tried ones (popular, played often, a settled rating) in each kind of
ending and each band of ratings, so the page can give every player positions near their own level. The build checks
every one with Stockfish before it uses it (pipeline/build_endings.py)."""
import csv, io, json, sys
from collections import defaultdict
import chess
sys.path.insert(0, __import__('os').path.dirname(__file__))
import paths

OUT = paths.ROOT / 'data' / 'endings' / 'puzzles.json'
BANDS = [(400, 900), (900, 1200), (1200, 1500), (1500, 1800), (1800, 2100), (2100, 2500)]
# how many to offer the build in each band (it keeps fewer: the ones Stockfish agrees with)
TAKE = {'pzz': 12, 'pzr': 12, 'pzk': 10, 'pzm': 8, 'pzq': 8}
MATE_KIND = {'smotheredMate': 'smo', 'anastasiaMate': 'ana', 'arabianMate': 'ara', 'backRankMate': 'br', 'bodenMate': 'bod',
             'doubleBishopMate': 'dbm', 'hookMate': 'hook', 'dovetailMate': 'dov'}
MATE_TAKE = 6


def pieces(board):
    """The pieces besides kings and pawns, per side: {'w': 'qr', 'b': 'r'}."""
    out = {'w': '', 'b': ''}
    for p in board.piece_map().values():
        if p.piece_type not in (chess.KING, chess.PAWN): out['w' if p.color else 'b'] += p.symbol().lower()
    return {k: ''.join(sorted(v)) for k, v in out.items()}


def kind_of(row, board, first):
    """Which kind a puzzle belongs to, or None. board: the position the player starts from; first: their first move."""
    th = set(row['Themes'].split())
    for t, k in MATE_KIND.items():
        if t in th: return k
    if 'mate' in th or not ('crushing' in th or 'equality' in th): return None
    pc = pieces(board)
    if pc == {'w': '', 'b': ''}:
        return 'pzz' if board.piece_type_at(first.from_square) == chess.KING else 'pzr'
    if pc == {'w': 'r', 'b': 'r'}: return 'pzk'
    if pc == {'w': 'q', 'b': 'q'}: return 'pzq'
    if all(set(v) <= {'b', 'n'} and len(v) == 1 for v in pc.values()): return 'pzm'
    return None


def main(src):
    if src.endswith('.zst'):
        import zstandard
        fh = io.TextIOWrapper(zstandard.ZstdDecompressor().stream_reader(open(src, 'rb')), encoding='utf-8')
    else: fh = open(src, encoding='utf-8')
    got = defaultdict(list)
    for row in csv.DictReader(fh):
        if int(row['Popularity']) < 85 or int(row['NbPlays']) < 1500 or int(row['RatingDeviation']) > 80: continue
        th = set(row['Themes'].split())
        if not (th & {'pawnEndgame', 'rookEndgame', 'queenEndgame', 'bishopEndgame', 'knightEndgame'} or th & set(MATE_KIND)): continue
        r = int(row['Rating']); band = next((i for i, (lo, hi) in enumerate(BANDS) if lo <= r < hi), None)
        if band is None: continue
        moves = row['Moves'].split(); b = chess.Board(row['FEN']); b.push_uci(moves[0])
        k = kind_of(row, b, chess.Move.from_uci(moves[1]))
        if not k: continue
        got[(k, band)].append(dict(id=row['PuzzleId'], fen=row['FEN'], moves=moves, r=r, pop=int(row['Popularity']), n=int(row['NbPlays']),
                                   themes=sorted(th - {'endgame', 'short', 'long', 'veryLong', 'oneMove', 'master', 'masterVsMaster', 'superGM'}),
                                   url=row['GameUrl']))
    out = []
    for (k, band), rows in sorted(got.items()):
        rows.sort(key=lambda x: (-x['pop'], -x['n'], x['id']))           # the best liked and most played first
        for x in rows[:MATE_TAKE if k in MATE_KIND.values() else TAKE[k]]:
            x['k'] = k; x['band'] = band; del x['pop'], x['n']; out.append(x)
    OUT.write_text(json.dumps(out, separators=(',', ':')))
    from collections import Counter
    print(len(out), 'positions written to', OUT); print(sorted(Counter(x['k'] for x in out).items()))


if __name__ == '__main__':
    main(sys.argv[1])
