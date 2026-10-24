"""Sanity-check Black-book notes against the actual positions."""
import sys, re
import paths
from common import *
import bcontent as BC
import bnotes
from label2 import _pin
VAL = {chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3, chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 0}
NAME = {'pawn': chess.PAWN, 'knight': chess.KNIGHT, 'bishop': chess.BISHOP, 'rook': chess.ROOK, 'queen': chess.QUEEN, 'king': chess.KING}
def mat(b):  # black minus white
    return sum(VAL[p.piece_type] * (1 if p.color == chess.BLACK else -1) for p in b.piece_map().values())
issues = []
for path, nt in BC.NOTES.items():
    toks = path.split(); b = chess.Board()
    for s in toks[:-1]: b.push_san(s)
    before = b.copy(); mv = b.parse_san(toks[-1]); b.push(mv)
    lab = (nt['label'] or ''); txt = (nt['text'] or ''); L = lab.lower(); T = txt.lower()
    piece = before.piece_at(mv.from_square); cap = before.is_capture(mv); chk = b.is_check()
    mine = piece.color == chess.BLACK
    def bad(msg): issues.append(f"{msg:38s} | {lab} | {txt[:70]} | {' '.join(toks[-4:])}")
    if re.search(r'\bcheck\b', L) and 'blocks the check' not in L and 'stops the queen check' not in L and not chk and 'out of check' not in L: bad('label says check, no check')
    if re.search(r'\b(takes|take|grabs|grab)\b', L) and 'takes back' not in L and not cap and 'take the center' not in L: bad('label says take, not a capture')
    if L.startswith('castle') and not before.is_castling(mv): bad('castle label, not castling')
    if 'white castles' in L and not before.is_castling(mv): bad('castles label, not castling')
    if 'hits the queen' in L or 'hits your queen' in L:
        tgt = [s for s in b.attacks(mv.to_square) if b.piece_at(s) and b.piece_at(s).piece_type == chess.QUEEN and b.piece_at(s).color != piece.color]
        disc = any(b.piece_at(s) and b.piece_at(s).piece_type == chess.QUEEN and b.piece_at(s).color != piece.color for s in chess.SQUARES if b.is_attacked_by(piece.color, s))
        if not tgt and not disc: bad('says hits the queen, it does not')
    m = re.search(r'(?:pins|pin) (?:the|your) (knight|bishop|rook|queen|pawn)', L)
    if m:
        pn = _pin(b, mv.to_square, piece)
        if pn != m.group(1):
            # maybe the pin is on the king's file through other means; report
            bad(f'pin claim {m.group(1)} vs {pn}')
    m = re.search(r'(?:hits|kick|kicks|ask) (?:the|your) (knight|bishop|rook|pawn|queen)', L)
    if m and 'pin' not in L:
        want = NAME[m.group(1)]
        att = [s for s in b.attacks(mv.to_square) if b.piece_at(s) and b.piece_at(s).color != piece.color and b.piece_at(s).piece_type == want]
        if L.startswith('ask the bishop') or L.startswith('kick'):
            pass
        if not att:
            # discovered attack by another piece?
            disc = any(b.piece_at(s) and b.piece_at(s).color != piece.color and b.piece_at(s).piece_type == want and b.is_attacked_by(piece.color, s) for s in chess.SQUARES)
            if not disc: bad(f'says hits {m.group(1)}, no')
    for pat, need in ((r'piece up for a pawn|piece for a pawn', 2), (r'\ba piece up\b|whole piece', 3), (r'\ba pawn up\b|pawn ahead|pawn up\.', 1), (r'two pieces for a pawn', 5), (r'piece and two pawns up', 5)):
        if re.search(pat, T):
            mb = mat(b)
            if mb < need - 0.5: bad(f'material claim {pat[:18]} but bal {mb:+d}')
    if 'equal' in T.split('.')[0] and abs(mat(b)) >= 2: bad(f'says equal, material {mat(b):+d}')
print(len(issues), 'issues')
print('\n'.join(issues))
