"""Hand fixes for the lines the build plays on (pipeline/deepen.py) and the side lines pipeline/fill.py drafts.

FIXED   path (the moves so far, the other side's move last) -> your move, where the pick misses the point. It holds for
        the position, so every order of moves that reaches it gets the same move.
REPLY   path (your move last) -> the other side's move to follow, where the likeliest reply isn't the one worth learning.
KEEP    line ids that stay as written.

The build sees a kept answer that a fix here has overtaken and works that line out again (it needs the engines for
that one line). SAN is internal."""
FIXED = {
    # the bishop comes at the knight in front of the castled king's square: the h-pawn asks it first, as everywhere in this book
    'e4 e5 Nf3 Nc6 Nc3 Nf6 Bb5 Bc5 Nxe5 Nxe5 d4 Bd6 dxe5 Bxe5 Bg5': 'h6',
    # the Slav setup against the London: with the knights traded off, the c-pawn hits the middle before the knight blocks it
    'd4 d5 Bf4 Nf6 e3 Bf5 Bd3 Bxd3 cxd3 e6 Nf3 Bd6 Ne5 O-O O-O Nfd7 Nc3 Bxe5 dxe5': 'c5',
    # the Scandinavian: a bishop lined up on the queen from behind its knight, and she steps off the line (the pack's own rule)
    'e4 d5 exd5 Qxd5 Nc3 Qa5 Nf3 Nf6 Bc4 c6 O-O Bf5 Ng5 e6 d3 Be7 Bd2': 'Qc7',
}
REPLY = {}
# rr-nimzo runs into the Italian by another move order and is held with either Italian (the center attack or the slow
# one), so it stops where they part: its last move is the bishop's, and the Italian lessons take it from there
KEEP = {'rr-nimzo'}
