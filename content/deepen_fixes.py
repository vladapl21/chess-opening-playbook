"""Hand fixes for the lines the build plays on (pipeline/deepen.py) and the side lines pipeline/fill.py drafts.

FIXED   path (the moves so far, the other side's move last) -> your move, where the pick misses the point. It holds for
        the position, so every order of moves that reaches it gets the same move.
REPLY   path (your move last) -> the other side's move to follow, where the likeliest reply isn't the one worth learning.
KEEP    line ids that stay as written.

The build sees a kept answer that a fix here has overtaken and works that line out again (it needs the engines for
that one line). SAN is internal."""
FIXED = {
    # the Milner-Barry with the bishop behind the pawns: after the knight check the queen takes a second pawn
    'e4 e6 d4 d5 e5 c5 c3 Nc6 Nf3 Qb6 Bd3 cxd4 cxd4 Bd7 Be3 Qxb2 Nbd2 Nb4 Rb1 Nxd3+ Ke2': 'Qxa2',
    # the bishop comes at the knight in front of the castled king's square: the h-pawn asks it first, as everywhere in this book
    'e4 e5 Nf3 Nc6 Nc3 Nf6 Bb5 Bc5 Nxe5 Nxe5 d4 Bd6 dxe5 Bxe5 Bg5': 'h6',
    # the Slav setup against the London: with the knights traded off, the c-pawn hits the middle before the knight blocks it
    'd4 d5 Bf4 Nf6 e3 Bf5 Bd3 Bxd3 cxd3 e6 Nf3 Bd6 Ne5 O-O O-O Nfd7 Nc3 Bxe5 dxe5': 'c5',
    # the Scandinavian: a bishop lined up on the queen from behind its knight, and she steps off the line (the pack's own rule)
    'e4 d5 exd5 Qxd5 Nc3 Qa5 Nf3 Nf6 Bc4 c6 O-O Bf5 Ng5 e6 d3 Be7 Bd2': 'Qc7',
}
REPLY = {}
# rr-nimzo reaches the position after both knights by another move order and is held with every variation of White's
# third move (the two Italians and the Ruy Lopez), so it stops where they part: on Black's e-pawn move
KEEP = {'rr-nimzo'}
