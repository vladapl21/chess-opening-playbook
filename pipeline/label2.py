"""Context-aware plain-English move labels (no notation). Used for nodes without a hand-written label."""
from common import *

PIECE_NAME = {chess.PAWN: 'pawn', chess.KNIGHT: 'knight', chess.BISHOP: 'bishop', chess.ROOK: 'rook', chess.QUEEN: 'queen', chess.KING: 'king'}
VAL = {chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3, chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 100}


def _target(after, sq, piece):
    """Most valuable enemy piece the moved piece now attacks that is worth more or hanging."""
    best = None; bestv = 0
    for t in after.attacks(sq):
        tp = after.piece_at(t)
        if not tp or tp.color == piece.color or tp.piece_type == chess.KING: continue
        v = VAL[tp.piece_type]
        defended = bool(after.attackers(tp.color, t))
        if v > VAL[piece.piece_type] or not defended:
            if v > bestv: best, bestv = PIECE_NAME[tp.piece_type], v
    return best


def _pin(after, sq, piece):
    """Name of an enemy piece pinned by the slider that just moved to sq (to king or queen)."""
    if piece.piece_type not in (chess.BISHOP, chess.ROOK, chess.QUEEN): return None
    enemy = not piece.color
    for t in after.attacks(sq):
        tp = after.piece_at(t)
        if not tp or tp.color != enemy or tp.piece_type in (chess.KING, chess.PAWN): continue
        # look beyond t along the ray sq->t
        ray = chess.SquareSet(chess.ray(sq, t))
        between_sq_t = chess.SquareSet(chess.between(sq, t))
        if any(after.piece_at(x) for x in between_sq_t): continue
        beyond = [x for x in ray if chess.square_distance(sq, x) > chess.square_distance(sq, t)
                  and ((chess.square_file(x) - chess.square_file(sq)) * (chess.square_file(t) - chess.square_file(sq)) >= 0)
                  and ((chess.square_rank(x) - chess.square_rank(sq)) * (chess.square_rank(t) - chess.square_rank(sq)) >= 0)]
        beyond.sort(key=lambda x: chess.square_distance(sq, x))
        for x in beyond:
            bp = after.piece_at(x)
            if not bp: continue
            if bp.color == enemy and bp.piece_type in (chess.KING, chess.QUEEN) and VAL[bp.piece_type] > VAL[tp.piece_type]:
                return PIECE_NAME[tp.piece_type]
            break
    return None


def label(before, move, prev=None, prev_cap=False):
    """before: board before the move. prev: the previous move (chess.Move) or None; prev_cap: it was a capture."""
    b = before
    piece = b.piece_at(move.from_square)
    pn = PIECE_NAME[piece.piece_type]
    P = pn.capitalize()
    after = b.copy(); after.push(move)
    check = after.is_check(); mate = after.is_checkmate()
    if b.is_castling(move):
        s = 'Castles kingside' if chess.square_file(move.to_square) > 4 else 'Castles queenside'
        return s + (' with check' if check else '')
    cap = b.piece_at(move.to_square)
    if b.is_en_passant(move): cap = chess.Piece(chess.PAWN, not piece.color)
    if mate:
        return f"{P} {'takes and ' if cap else ''}gives checkmate"
    if cap:
        retake = prev is not None and prev_cap and prev.to_square == move.to_square and before.piece_at(move.to_square) is not None
        if retake and not check:
            return f"{P} takes back"
        s = f"{P} takes the {PIECE_NAME[cap.piece_type]}"
        if check: s += " with check"
        else:
            pin = _pin(after, move.to_square, piece)
            if pin: s += f", pinning the {pin}"
        return s
    if b.is_check() and piece.piece_type != chess.KING:
        return f"{P} blocks the check"
    if piece.piece_type == chess.KING:
        return 'King steps out of check' if b.is_check() else 'King steps aside'
    if piece.piece_type == chess.PAWN:
        f = chess.FILE_NAMES[chess.square_file(move.from_square)]
        steps = abs(chess.square_rank(move.to_square) - chess.square_rank(move.from_square))
        if move.promotion: return f"Pawn promotes to a {PIECE_NAME[move.promotion]}"
        s = f"{f.upper()}-pawn {'two squares' if steps == 2 else 'one square'}"
        if check: return s + ', check'
        tgt = _target(after, move.to_square, piece)
        if tgt: s += f", hits the {tgt}"
        return s
    if check:
        return f"{P} gives check"
    home_rank = 0 if piece.color == chess.WHITE else 7
    fr, tr = chess.square_rank(move.from_square), chess.square_rank(move.to_square)
    developing = fr == home_rank and piece.piece_type in (chess.KNIGHT, chess.BISHOP)
    backward = (tr < fr) if piece.color == chess.WHITE else (tr > fr)
    pin = _pin(after, move.to_square, piece)
    tgt = _target(after, move.to_square, piece)
    if developing:
        s = f"{P} comes out"
    elif backward:
        s = f"{P} steps back"
    else:
        s = {'knight': 'Knight jumps forward', 'bishop': 'Bishop slides over', 'rook': 'Rook to a new file', 'queen': 'Queen comes out' if fr == home_rank else 'Queen moves'}[pn]
    if pin: s += f", pins the {pin}"
    elif tgt: s += f", hits the {tgt}"
    return s
