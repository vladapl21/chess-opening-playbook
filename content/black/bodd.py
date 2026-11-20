"""Black, the house books: odd moves that were missing. The Halloween Gambit in the Four Knights, White's odd second moves
after the e-pawns (the Bongcloud, the Portuguese, the Alapin and others) and odd first moves (the Kádas, the Ware, the
Barnes, the Amar, the Sodium Attack). Drafted with pipeline/draft.py from the positions the book already answers:
a known position keeps its move, a new one takes the first developing move Stockfish 17.1 accepts. SAN is internal."""
from bcontent import L, P, J, n

P('ba-odd', 'attacks', 'Odd second moves', 'Bongcloud, Portuguese, Alapin', "The king walks, the bishop pokes at nothing, the knight tucks in. Your own moves don't change.")

L('bv-halloween', 'bv-4n', 'The Halloween Gambit', 'Take the knight; when the pawns come, the knights step back and you keep the piece', 'rare',
  'e4 e5 Nf3 Nc6 Nc3 Nf6 Nxe5 Nxe5 d4 Ng6 e5 Ng8',
  alts=[('bv-halloween-bg5', 'Bishop pins the knight', 'e4 e5 Nf3 Nc6 Nc3 Nf6 Nxe5 Nxe5 d4 Ng6 Bg5 Be7')],
  why='White gives a knight for your e-pawn and a wall of pawns. It only works if you panic.', outcome='A piece up')
L('ba-odd2', 'ba-odd', 'The Bongcloud and other odd second moves', 'Knights out, bishop out, castle: the same moves as always', 'rare',
  'e4 e5 Ke2 Nf6 f3 Nc6 c3 Bc5 b4 Bb6 a4 d5',
  alts=[('ba-odd2-bb5', 'Portuguese Opening', 'e4 e5 Bb5 c6 Bc4 Nf6 d3 d5 exd5 cxd5 Bb3 Nc6'),
        ('ba-odd2-g3', 'Small g-pawn move', 'e4 e5 g3 d5 Bg2 dxe4 Bxe4 Nf6 Bg2 Nc6 d3 Bg4'),
        ('ba-odd2-bd3', 'Tortoise Opening', 'e4 e5 Bd3 Nf6 Nf3 d5 exd5 e4 Qe2 Qe7 Bb5+ c6'),
        ('ba-odd2-bb5ba4', 'Portuguese Opening, then bishop steps back', 'e4 e5 Bb5 c6 Ba4 Nf6 d3 Bc5 h3 d5 exd5 O-O'),
        ('ba-odd2-c4', 'The Whale', 'e4 e5 c4 Nf6 Nc3 Bc5 h3 Nc6 Nf3 O-O d3 d6'),
        ('ba-odd2-a3', 'Mengarini\'s Opening', 'e4 e5 a3 Nf6 Nc3 Nc6 Bc4 Nxe4 Nxe4 d5 Bxd5 Qxd5 d3 Be7'),
        ('ba-odd2-g3exd5', 'Small g-pawn move, then pawn takes the pawn', 'e4 e5 g3 d5 exd5 Qxd5 Nf3 Bg4 Bg2 e4 Nc3 exf3 Nxd5 fxg2 Qxg4 gxh1=Q+'),
        ('ba-odd2-a3nc3', 'Mengarini\'s Opening, then Mengarini Variation', 'e4 e5 a3 Nf6 Nc3 Nc6 Nf3 d5 exd5 Nxd5 Nxd5 Qxd5 d3 b6'),
        ('ba-odd2-bd3nf3', 'Tortoise Opening, then king\'s knight out', 'e4 e5 Bd3 Nf6 Nf3 d5 Nxe5 Qe7 Nf3 dxe4 Qe2 exd3 Qxe7+ Bxe7 cxd3 Nc6'),
        ('ba-odd2-b3', 'Small b-pawn move', 'e4 e5 b3 Nf6 Bb2 Bc5 Bxe5 Nc6 Bb2 Qe7 d3 d5'),
        ('ba-odd2-c4d3', 'The Whale, then small d-pawn move', 'e4 e5 c4 Nf6 d3 Bc5 h3 Nc6 Nf3 O-O Be2 d6'),
        ('ba-odd2-bb5ba4nc3', 'Portuguese Opening, then bishop steps back, then queen\'s knight out', 'e4 e5 Bb5 c6 Ba4 Nf6 Nc3 Bc5 Nf3 d6 O-O O-O'),
        ('ba-odd2-ne2', 'Alapin Opening', 'e4 e5 Ne2 Nf6 Ng3 Nc6 Bc4 Nxe4 Nxe4 d5 Bxd5 Qxd5 Nbc3 Qe6'),
        ('ba-odd2-c4nc3', 'The Whale, then queen\'s knight out', 'e4 e5 c4 Nf6 Nc3 Bc5 Nf3 d6 h3 Nc6 d3 O-O'),
        ('ba-odd2-g3exd5qf3', 'Small g-pawn move, then pawn takes the pawn, then queen comes out', 'e4 e5 g3 d5 exd5 Qxd5 Qf3 Qc5 Nc3 Nf6 d3 Nc6'),
        ('ba-odd2-ne2d3', 'Alapin Opening, then small d-pawn move', 'e4 e5 Ne2 Nf6 d3 Nc6 g3 d5 Bg2 dxe4 dxe4 Qxd1+ Kxd1 Bc5'),
        ('ba-odd2-bd3nc3', 'Tortoise Opening, then queen\'s knight out', 'e4 e5 Bd3 Nf6 Nc3 Nc6 Nf3 Bc5 O-O O-O a3 d6'),
        ('ba-odd2-a3d3', 'Mengarini\'s Opening, then small d-pawn move', 'e4 e5 a3 Nf6 d3 Nc6 h3 d5 exd5 Nxd5 Nf3 Bf5'),
        ('ba-odd2-nc3', 'Queen\'s knight out', 'e4 e5 Ke2 Nf6 Nc3 Nc6 Nf3 d5 exd5 Nxd5 Nxd5 Qxd5 d3 Bc5'),
        ('ba-odd2-b3nc3', 'Small b-pawn move, then queen\'s knight out', 'e4 e5 b3 Nf6 Nc3 Nc6 Bb2 Bc5 Nf3 O-O Bc4 d6'),
        ('ba-odd2-c4nc3d3', 'The Whale, then queen\'s knight out, then small d-pawn move', 'e4 e5 c4 Nf6 Nc3 Bc5 d3 Nc6 Nf3 Ng4 Be3 Nxe3 fxe3 Bxe3 Qe2 Bc5'),
        ('ba-odd2-qe2', 'Queen comes out', 'e4 e5 Qe2 Nf6 d3 Nc6 c3 Bc5 h3 d5 exd5 Qxd5 Nf3 Bb6'),
        ('ba-odd2-qe2nc3', 'Queen comes out, then queen\'s knight out', 'e4 e5 Qe2 Nf6 Nc3 Nc6 Nf3 Bc5 h3 O-O d3 d5'),
        ('ba-odd2-d3', 'Small d-pawn move', 'e4 e5 Ke2 Nf6 d3 Bc5 Nf3 d5 exd5 O-O c4 e4'),
        ('ba-odd2-b3d3', 'Small b-pawn move, then small d-pawn move', 'e4 e5 b3 Nf6 d3 Bc5 Bb2 Nc6 Nf3 d5 exd5 Nxd5 Nxe5 O-O'),
        ('ba-odd2-ne2nbc3', 'Alapin Opening, then queen\'s knight out', 'e4 e5 Ne2 Nf6 Nbc3 Bc5 h3 Nc6 d3 d5 exd5 Nxd5 Nxd5 Qxd5 Nc3 Qe6'),
        ('ba-odd2-qe2nf3', 'Queen comes out, then king\'s knight out', 'e4 e5 Qe2 Nf6 Nf3 Nc6 c3 Bc5 d4 exd4 cxd4 Nxd4 Nxd4 Bxd4 e5 O-O')],
  why='The king walks, a bishop pokes, a knight tucks in. None of them needs a special answer: develop and take the middle.', outcome='Better for you')
L('bo-odd', 'bo-rare', 'The Kádas, the Ware and the knights on the rim', 'E-pawn and d-pawn in the middle, then the knights', 'rare',
  'h4 e5 g4 d5 g5 Nc6 Bg2 Bc5 e3 h6 gxh6 Nxh6 Nc3 Bg4',
  alts=[('bo-odd-nh3', 'Amar Opening', 'Nh3 e5 e4 d5 exd5 Bxh3 gxh3 Qxd5 Rg1 Nc6 Nc3 Qd7'),
        ('bo-odd-na3', 'Sodium Attack', 'Na3 e5 e4 d5 exd5 Nf6 c4 c6 dxc6 Nxc6 d3 Bc5'),
        ('bo-odd-f3', 'Barnes Opening', 'f3 e5 e4 d5 exd5 Nf6 Nc3 Nxd5 Nxd5 Qxd5 d3 Nc6'),
        ('bo-odd-nh3d4', 'Amar Opening, then d-pawn two squares', 'Nh3 e5 d4 exd4 Qxd4 d5 Nc3 Nf6 Bg5 Nc6 Bxf6 Nxd4 Bxd8 Nxc2+ Kd2 Nxa1'),
        ('bo-odd-na3nc4', 'Sodium Attack, then knight jumps forward', 'Na3 e5 Nc4 Nc6 e4 d5 exd5 Qxd5 Ne3 Qd6 Nf3 e4'),
        ('bo-odd-a4', 'Ware Opening', 'a4 e5 b3 d5 Bb2 Nc6 e3 Nf6 Bb5 Bd6 Bxc6+ bxc6 Nf3 Nd7'),
        ('bo-odd-f3d3', 'Barnes Opening, then small d-pawn move', 'f3 e5 e4 d5 d3 Nf6 Bg5 Nc6 Bxf6 gxf6 Nc3 d4'),
        ('bo-odd-nh3g3', 'Amar Opening, then small g-pawn move', 'Nh3 e5 g3 d5 Bg2 Nc6 O-O h5 d3 h4 e4 hxg3 fxg3 Bxh3 Bxh3 Rxh3'),
        ('bo-odd-a4e4', 'Ware Opening, then e-pawn two squares', 'a4 e5 e4 Nf6 Nc3 d5 exd5 Bc5 h3 Nxd5 Nxd5 Qxd5 d3 Nc6'),
        ('bo-odd-a4a5', 'Ware Opening, then small a-pawn move', 'a4 e5 a5 d5 e3 Nf6 c3 Bd6 b4 O-O Ba3 Nc6'),
        ('bo-odd-h5', 'Small h-pawn move', 'h4 e5 h5 d5 e3 Nf6 Be2 Nc6 d3 Bc5 Bd2 h6')],
  why='Edge pawns and edge knights on move one. Take the middle with both pawns and develop behind them.', outcome='Better for you')

# ============================================================== notes
n('e4 e5 Nf3 Nc6 Nc3 Nf6 Nxe5 Nxe5', 'Take the knight', 'A piece for a pawn. White gets two moves with the pawns for it, and that is all.', ['key'])
# the other side's moves that start a named line
n('Na3', 'Sodium Attack')
n('Nh3', 'Amar Opening')
n('a4', 'Ware Opening')
n('f3', 'Barnes Opening')
n('h4', 'Kádas Opening')
n('e4 e5 Bb5', 'Portuguese Opening')
n('e4 e5 Bd3', 'Tortoise Opening')
n('e4 e5 Ke2', 'Bongcloud Attack')
n('e4 e5 Ne2', 'Alapin Opening')
n('e4 e5 a3', 'Mengarini\'s Opening')
n('e4 e5 c4', 'The Whale')
n('f3 e5 e4', 'King\'s Head Opening')
n('e4 e5 a3 Nf6 Nc3', 'Mengarini Variation')
n('e4 e5 Nf3 Nc6 Nc3 Nf6 Nxe5', 'Halloween Gambit')
n('e4 e5 a3 Nf6 Nc3 Nc6 Nf3', 'Gunsberg Variation')
