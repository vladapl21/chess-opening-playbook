"""Build a merged repertoire tree from study chapters + added lines."""
from common import *
import io, re
PIECE_NAME = {chess.PAWN:'pawn', chess.KNIGHT:'knight', chess.BISHOP:'bishop', chess.ROOK:'rook', chess.QUEEN:'queen', chess.KING:'king'}
COLOR_MAP = {'G':'g','R':'r','B':'b','Y':'y'}

class Node:
    __slots__=('path','move','san','board','children','arrows','circles','src','parent','id')
    def __init__(self, path, move, san, board, parent):
        self.path=path; self.move=move; self.san=san; self.board=board; self.parent=parent
        self.children=[]; self.arrows=[]; self.circles=[]; self.src=set(); self.id=None

class Tree:
    def __init__(self):
        self.root=Node((), None, None, chess.Board(), None)
        self.index={(): self.root}
    def get(self, path):
        return self.index.get(tuple(path))
    def add_line(self, sans, src, annotations=None):
        """sans: list of SAN strings from the initial position. annotations: dict ply->(arrows,circles)"""
        node=self.root
        for i,s in enumerate(sans):
            p=node.path+(s,)
            if p not in self.index:
                b=node.board.copy(); mv=b.parse_san(s); b.push(mv)
                child=Node(p, mv, s, b, node)
                node.children.append(child); self.index[p]=child
            node=self.index[p]
            node.src.add(src)
        return node
    def add_pgn_game(self, game, src):
        def rec(gnode, tnode):
            for var in gnode.variations:
                b=tnode.board
                s=b.san(var.move)
                p=tnode.path+(s,)
                if p not in self.index:
                    nb=b.copy(); nb.push(var.move)
                    child=Node(p, var.move, s, nb, tnode)
                    tnode.children.append(child); self.index[p]=child
                child=self.index[p]; child.src.add(src)
                for a in var.arrows():
                    col=COLOR_MAP.get(a.color[0].upper() if a.color else 'G','g')
                    if a.tail==a.head:
                        item=(chess.square_name(a.tail), col)
                        if item not in child.circles: child.circles.append(item)
                    else:
                        item=(chess.square_name(a.tail), chess.square_name(a.head), col)
                        if item not in child.arrows: child.arrows.append(item)
                rec(var, child)
        rec(game, self.root)
    def walk(self, node=None):
        node=node or self.root
        yield node
        for c in node.children:
            yield from self.walk(c)

def auto_label(parent_board, move):
    """Plain-English, notation-light description of a move."""
    b=parent_board
    piece=b.piece_at(move.from_square)
    pn=PIECE_NAME[piece.piece_type]
    me = 'White' if piece.color==chess.WHITE else 'Black'
    after=b.copy(); after.push(move)
    check=after.is_check(); mate=after.is_checkmate()
    if b.is_castling(move):
        s='Castles kingside' if chess.square_file(move.to_square)>4 else 'Castles queenside'
        return s+(' with check' if check else '')
    cap=b.piece_at(move.to_square)
    if b.is_en_passant(move): cap=chess.Piece(chess.PAWN, not piece.color)
    if mate:
        return f"{pn.capitalize()} {'takes and ' if cap else ''}delivers checkmate"
    if cap:
        s=f"{pn.capitalize()} takes the {PIECE_NAME[cap.piece_type]}"
        if check: s+=" with check"
        return s
    if piece.piece_type==chess.PAWN:
        f=chess.FILE_NAMES[chess.square_file(move.from_square)]
        steps=abs(chess.square_rank(move.to_square)-chess.square_rank(move.from_square))
        s=f"{f}-pawn forward {'two' if steps==2 else 'one'}"
        s=s[0].upper()+s[1:]
        if move.promotion: s=f"Pawn promotes to a {PIECE_NAME[move.promotion]}"
        if check: s+=", check"
        else:
            tgt=attack_target(after, move.to_square, piece)
            if tgt: s+=f", attacks the {tgt}"
        return s
    if check:
        return f"{pn.capitalize()} gives check"
    if b.is_check() and piece.piece_type!=chess.KING:
        return f"{pn.capitalize()} blocks the check"
    home_rank = 0 if piece.color==chess.WHITE else 7
    developing = chess.square_rank(move.from_square)==home_rank and piece.piece_type in (chess.KNIGHT, chess.BISHOP)
    verb={'knight':'jumps','bishop':'slides','rook':'slides','queen':'moves','king':'steps'}[pn]
    s=f"{pn.capitalize()} {'comes out' if developing else verb}"
    tgt=attack_target(after, move.to_square, piece)
    if tgt: s+=f", attacks the {tgt}"
    return s

VAL={chess.PAWN:1,chess.KNIGHT:3,chess.BISHOP:3,chess.ROOK:5,chess.QUEEN:9,chess.KING:100}
def attack_target(after, sq, piece):
    best=None; bestv=0
    for t in after.attacks(sq):
        tp=after.piece_at(t)
        if not tp or tp.color==piece.color or tp.piece_type==chess.KING: continue
        v=VAL[tp.piece_type]
        defended=bool(after.attackers(tp.color, t))
        if v>VAL[piece.piece_type] or not defended:
            if v>bestv: best, bestv = PIECE_NAME[tp.piece_type], v
    return best
