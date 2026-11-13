"""Black against the e-pawn, third system: the Sicilian with the small e-pawn and a-pawn moves (the Kan setup).
One recipe: c-pawn two squares, e-pawn one, take the d-pawn when it comes, a-pawn one, queen beside the bishop,
king's knight, b-pawn two. A separate pack (see PACKS in bmeta.py). SAN is internal; notes are plain English."""
from bcontent import L, P, J, n

SI = "e4 c5"
OP = J(SI, "Nf3 e6 d4 cxd4 Nxd4 a6")       # the open game

# ============================================================== THE OPEN GAME
P('bsi-open', 'sicilian', 'White opens the middle', 'Open Sicilian',
  'White trades the d-pawn for your c-pawn. You get a half-open c-file and two middle pawns; the small a-pawn move keeps knights and bishops off your queenside.')
L('bsi-open', 'bsi-open', 'The open game', 'A-pawn, queen, knight, then the b-pawn', 'core',
  J(OP, "Nc3 Qc7 Be3 Nf6 Bd3 b5"),
  alts=[('bsi-open-bd3', 'Bishop in front of the queen', J(OP, "Nc3 Qc7 Bd3 Nf6 O-O d6")),
        ('bsi-open-be2', 'Bishop one square', J(OP, "Nc3 Qc7 Be2 Nf6 O-O d6")),
        ('bsi-open-g3', 'Bishop to the long diagonal', J(OP, "Nc3 Qc7 g3 Nf6 Bg2 d6")),
        ('bsi-open-bd3first', 'Bishop before the knight', J(OP, "Bd3 Nf6 O-O Qc7")),
        ('bsi-open-c4', 'C-pawn clamps the middle', J(OP, "c4 Qc7 Nc3 Nf6")),
        ('bsi-open-bc4', 'Bishop aims at your e-pawn', J(OP, "Bc4 b5 Bb3 Bb7")),
        ('bsi-open-be3', 'Bishop beside the queen first', J(OP, "Be3 Nf6 Bd3 Qc7")),
        ('bsi-open-qxd4', 'Queen takes back', J(SI, "Nf3 e6 d4 cxd4 Qxd4 Nc6 Qd1 Nf6")),
        ('bsi-open-c3', 'White offers a pawn instead', J(SI, "Nf3 e6 d4 cxd4 c3 Nf6 e5 Nd5")),
        ('bsi-open-nc3', 'Knight first, then the d-pawn', J(SI, "Nf3 e6 Nc3 a6 d4 cxd4 Nxd4 Qc7")),
        ('bsi-open-nc3first', 'Queen\'s knight on move two', J(SI, "Nc3 e6 Nf3 a6 d4 cxd4 Nxd4 Qc7"))],
  why='Half your games start with the knight, and half of those open the middle. The same six moves answer every version.',
  outcome='A fighting, level game')

# ============================================================== THE ITALIAN BISHOP
P('bsi-bc4', 'sicilian', 'The bishop comes out early', 'Bishop on the fourth rank',
  'The most common mistake against the Sicilian at club level. Your e-pawn blocks the bishop and the d-pawn hits it.')
L('bsi-bc4', 'bsi-bc4', 'Bishop out on move two', 'E-pawn blocks it, d-pawn hits it', 'core',
  J(SI, "Bc4 e6 Nf3 d5 exd5 exd5 Bb5+ Nc6"),
  alts=[('bsi-bc4-nf3', 'Knight first, then the bishop', J(SI, "Nf3 e6 Bc4 d5 exd5 exd5 Bb5+ Nc6")),
        ('bsi-bc4-d3', 'Bishop, then the small d-pawn', J(SI, "Bc4 e6 d3 d5 exd5 exd5 Bb5+ Nc6")),
        ('bsi-bc4-nc3', 'Bishop and knight', J(SI, "Bc4 e6 Nc3 a6 a4 Nf6")),
        ('bsi-bc4-nc3first', 'Knight, then the bishop', J(SI, "Nc3 e6 Bc4 a6 a4 Nf6")),
        ('bsi-bc4-qf3', 'Queen and bishop at f7', J(SI, "Bc4 e6 Qf3 Nc6"))],
  why='One opponent in six plays the Italian bishop against everything. Here it runs into a wall and loses a move.',
  outcome='Comfortable for you')

# ============================================================== THE SMALL C-PAWN
P('bsi-c3', 'sicilian', 'White builds a center first', 'Alapin and the pawn offer',
  'White wants two pawns in the middle. Your d-pawn goes two squares at once, and the game looks like a French where your bad bishop has more room.')
L('bsi-c3', 'bsi-c3', 'The small c-pawn', 'D-pawn two squares, then pile up on the d-pawn', 'common',
  J(SI, "c3 e6 d4 d5 e5 Nc6 Nf3 Qb6"),
  alts=[('bsi-c3-exd5', 'White trades in the middle', J(SI, "c3 e6 d4 d5 exd5 exd5 Nf3 Nc6")),
        ('bsi-c3-nf3', 'Knight, then the c-pawn', J(SI, "Nf3 e6 c3 d5 e5 Nc6 d4 Qb6")),
        ('bsi-c3-nf3x', 'Knight, c-pawn, then the trade', J(SI, "Nf3 e6 c3 d5 exd5 exd5 d4 Nc6")),
        ('bsi-c3-morra', 'White offers the c-pawn', J(SI, "d4 cxd4 c3 Nf6 e5 Nd5 cxd4 d6"))],
  why='About one game in ten. You already know the plan from playing White against the French: hit the pawn that holds the chain.',
  outcome='Equal')

# ============================================================== QUEEN OUT, F-PAWN
P('bsi-other', 'sicilian', 'Other second moves', 'Sidelines',
  'The d-pawn at once, or the f-pawn. Develop with a hit on the queen, or put the d-pawn in the middle.')
L('bsi-d4', 'bsi-other', 'D-pawn on move two', 'Take it; the knight hits the queen', 'common',
  J(SI, "d4 cxd4 Qxd4 Nc6 Qd1 Nf6"),
  alts=[('bsi-d4-qe3', 'Queen steps one square', J(SI, "d4 cxd4 Qxd4 Nc6 Qe3 Nf6")),
        ('bsi-d4-qa4', 'Queen to the edge', J(SI, "d4 cxd4 Qxd4 Nc6 Qa4 Nf6")),
        ('bsi-d4-nf3', 'Knight wins the pawn back', J(SI, "d4 cxd4 Nf3 e6 Nxd4 a6"))],
  why='One in twelve. The queen comes out too early and your knight gains a move on her.', outcome='Comfortable')
L('bsi-f4', 'bsi-other', 'F-pawn on move two', 'E-pawn, then the d-pawn two squares', 'rare',
  J(SI, "f4 e6 Nf3 d5 e5 Nc6"),
  alts=[('bsi-f4-exd5', 'White trades', J(SI, "f4 e6 Nf3 d5 exd5 exd5")),
        ('bsi-f4-nc3', 'Knight and f-pawn', J(SI, "Nc3 e6 f4 d5")),
        ('bsi-f4-g3', 'Knight and a slow bishop', J(SI, "Nc3 e6 g3 d5"))],
  why='Slow attacking setups. The d-pawn in the middle takes the sting out of all of them.', outcome='Equal or better')

# ============================================================== notes
n(SI, 'C-pawn two squares', 'It fights for the middle from the side. When White\'s d-pawn comes forward you take it, and you are left with more pawns in the middle than White.', ['key'], arrows=['c5d4g'])
n(J(SI, 'Nf3'), 'Knight out', 'Half of club players. The d-pawn usually follows.')
n(J(SI, 'Nf3 e6'), 'E-pawn one square', 'Always your second move. It opens the dark bishop and blunts any bishop that aims at f7.', ['key'])
n(J(SI, 'Nf3 e6 d4'), 'White opens the middle', 'The main line.')
n(J(SI, 'Nf3 e6 d4 cxd4'), 'Take it', 'A side pawn for a middle pawn is a good trade, and the c-file opens for your rook and queen.', ['key'])
n(OP, 'A-pawn one square', 'The move that names the setup. No knight or bishop can land on the square beside it, and the b-pawn is ready to go two squares.', ['key'], arrows=['b7b5g'])
n(J(OP, 'Nc3 Qc7'), 'Queen beside the bishop', 'On the open file, guarding the middle square White\'s e-pawn wants to reach. It comes before the knight so that pawn push never arrives with a hit.', ['key'])
n(J(OP, 'Nc3 Qc7 Be3 Nf6'), 'King\'s knight', 'Safe now: the queen covers the square in front of White\'s e-pawn.')
n(J(OP, 'Nc3 Qc7 Be3 Nf6 Bd3 b5'), 'B-pawn two squares', 'It makes room for the bishop on the long diagonal and gets ready to chase White\'s knight.', ['key'], arrows=['c8b7g'])
n(J(OP, 'Nc3 Qc7 Bd3 Nf6 O-O d6'), 'D-pawn one square', 'A small pawn wall. Bishop out, castle, and the queen\'s knight goes beside the queen.')
n(J(OP, 'Bc4'), 'Bishop aims at your e-pawn', 'The a-pawn move was made for this.')
n(J(OP, 'Bc4 b5'), 'B-pawn hits the bishop', 'It has to move again, and your bishop gets the long diagonal with a hit on the e-pawn.', ['key'], arrows=['b5c4r'])
n(J(OP, 'c4 Qc7'), 'Queen out as usual', 'White has clamped the middle with two pawns. Your setup does not change: queen, knight, then small moves behind the wall.')
n(J(SI, 'Nf3 e6 d4 cxd4 Qxd4 Nc6'), 'Knight hits the queen', 'She has to move again.', ['key'])
n(J(SI, 'Nf3 e6 d4 cxd4 c3'), 'White offers a pawn', 'Taking it gives White fast development. You do not need it.')
n(J(SI, 'Nf3 e6 d4 cxd4 c3 Nf6'), 'Decline: hit the e-pawn', 'If it pushes past, the knight takes the fine square in the middle.', ['key'])

n(J(SI, 'Bc4'), 'Bishop out on move two', 'It aims at f7, and your e-pawn closes that road at once.')
n(J(SI, 'Bc4 e6'), 'E-pawn one square', 'The bishop now looks at a wall. The d-pawn comes next with a hit on it.', ['key'], arrows=['d7d5g'])
n(J(SI, 'Bc4 e6 Nf3 d5'), 'D-pawn hits the bishop', 'You take the middle and gain a move.', ['key'], arrows=['d5c4r'])
n(J(SI, 'Bc4 e6 Nf3 d5 exd5 exd5'), 'Take back with the e-pawn', 'It hits the bishop again and opens your own bishop.')
n(J(SI, 'Bc4 e6 Nf3 d5 exd5 exd5 Bb5+ Nc6'), 'Block with the knight', 'A piece comes out and the check is over. White has moved the bishop three times.')
n(J(SI, 'Bc4 e6 Nc3 a6'), 'A-pawn one square', 'The b-pawn is coming to hit the bishop.', arrows=['b7b5g'])
n(J(SI, 'Bc4 e6 Nc3 a6 a4 Nf6'), 'Knight out', 'White spent a move stopping your b-pawn. Now the d-pawn push is back on.')

n(J(SI, 'c3'), 'Small c-pawn move', 'White wants to put a second pawn in the middle and take back with a pawn.')
n(J(SI, 'c3 e6 d4 d5'), 'D-pawn two squares', 'Meet the center head on, before it is set.', ['key'])
n(J(SI, 'c3 e6 d4 d5 e5 Nc6'), 'Knight at the d-pawn', 'The chain\'s base is the d-pawn. Knight, then queen, both aim at it.', arrows=['c6d4g'])
n(J(SI, 'c3 e6 d4 d5 e5 Nc6 Nf3 Qb6'), 'Queen joins in', 'Three attackers on the d-pawn, and an eye on the b-pawn.', ['key'], arrows=['b6d4g', 'b6b2g'])
n(J(SI, 'c3 e6 d4 d5 exd5 exd5'), 'Take back with the e-pawn', 'Both bishops are open. An easy, level game.')
n(J(SI, 'd4 cxd4 c3 Nf6'), 'Decline the pawn', 'Hit the e-pawn instead. The game turns into the small c-pawn lesson.', ['key'])

n(J(SI, 'd4 cxd4'), 'Take it', 'Always.')
n(J(SI, 'd4 cxd4 Qxd4 Nc6'), 'Knight hits the queen', 'A free developing move.', ['key'], arrows=['c6d4r'])
n(J(SI, 'f4 e6 Nf3 d5'), 'D-pawn two squares', 'White was getting ready to attack on the kingside. A pawn in the middle is the answer to that.', ['key'])
