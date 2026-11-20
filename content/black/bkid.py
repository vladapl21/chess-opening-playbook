"""Black against the d-pawn, another system: the King's Indian. One setup in one order against nearly everything: knight,
g-pawn one square, bishop to the long diagonal, d-pawn one square, castle, then the e-pawn two squares. A separate pack
(see PACKS in bmeta.py) with two chapters: White's c-pawn systems, and the London, Colle, Trompowsky and Jobava. The
lines were drafted with pipeline/draft.py: White's moves by the Maia 1300/1500 odds, yours from the setup's order
wherever Stockfish 17.1 accepts it and the engine's move elsewhere. SAN is internal only; notes are plain English."""
from bcontent import L, P, J, n

P('bki-center', 'kid', 'White takes the whole center', 'Classical & Four Pawns', 'Three or four pawns in a row. Castle, then the e-pawn strikes; when the middle closes, your knight steps back and the f-pawn starts the attack.')
P('bki-quiet', 'kid', 'White holds the e-pawn back', 'Quiet setups', 'No big center, so no hurry. The same five moves, then the e-pawn when a knight backs it up.')
P('bkx-bishop', 'kidx', 'The bishop comes out first', 'London & Torre', "White's dark bishop leaves before the e-pawn. Your setup stays the same, and the e-pawn push gains a move on that bishop.")
P('bkx-other', 'kidx', 'Other second moves', 'Colle, Jobava, Trompowsky', "The small e-pawn, the queen's knight, the bishop at your knight. One of them needs your d-pawn to go two squares.")

L('bki-main', 'bki-center', 'The Classical: castle, then the e-pawn', 'Castle, e-pawn two squares, then the knight in front of the c-pawn', 'core',
  'd4 Nf6 c4 g6 Nc3 Bg7 e4 d6 Nf3 O-O Be2 e5 d5 Nbd7 O-O Nc5',
  alts=[('bki-main-bd3', 'Bishop to the middle', 'd4 Nf6 c4 g6 Nc3 Bg7 e4 d6 Nf3 O-O Bd3 e5 d5 Nfd7 O-O f5'),
        ('bki-main-be3', 'Larsen Variation', 'd4 Nf6 c4 g6 Nc3 Bg7 e4 d6 Nf3 O-O Be3 e5 d5 c6'),
        ('bki-main-oo', 'White castles and keeps the middle open', 'd4 Nf6 c4 g6 Nc3 Bg7 e4 d6 Nf3 O-O Be2 e5 O-O Nc6'),
        ('bki-main-dxe5', 'D-pawn takes, queens come off', 'd4 Nf6 c4 g6 Nc3 Bg7 e4 d6 Nf3 O-O Be2 e5 dxe5 dxe5 Qxd8 Rxd8'),
        ('bki-main-bg5', 'Zinnowitz Variation', 'd4 Nf6 c4 g6 Nc3 Bg7 e4 d6 Nf3 O-O Bg5 Nbd7 Bd3 e5'),
        ('bki-main-bd3dxe5', 'Bishop to the middle, then pawn takes the pawn', 'd4 Nf6 c4 g6 Nc3 Bg7 e4 d6 Nf3 O-O Bd3 e5 dxe5 dxe5 Nxe5 Re8'),
        ('bki-main-bg5be2', 'Zinnowitz Variation, then bishop to the quiet square', 'd4 Nf6 c4 g6 Nc3 Bg7 e4 d6 Nf3 O-O Bg5 Nbd7 Be2 e5'),
        ('bki-main-be3dxe5', 'Larsen Variation, then pawn takes the pawn', 'd4 Nf6 c4 g6 Nc3 Bg7 e4 d6 Nf3 O-O Be3 e5 dxe5 dxe5'),
        ('bki-main-bd3d5', 'Bishop to the middle, then small d-pawn move', 'd4 Nf6 c4 g6 Nc3 Bg7 e4 d6 Nf3 O-O Bd3 e5 d5 Nfd7 Be3 f5'),
        ('bki-main-bg5qd2', 'Zinnowitz Variation, then queen comes out', 'd4 Nf6 c4 g6 Nc3 Bg7 e4 d6 Nf3 O-O Bg5 Nbd7 Qd2 e5'),
        ('bki-main-bg5v2', 'Bishop pins the knight', 'd4 Nf6 c4 g6 Nc3 Bg7 e4 d6 Nf3 O-O Be2 e5 d5 Nbd7 Bg5 h6')],
  why='The setup White players aim for: three pawns in the middle and both knights out. You castle and hit that middle with the e-pawn.', outcome='A full fight; your play is on the kingside')
L('bki-f4', 'bki-center', 'The Four Pawns Attack', 'Castle, then the e-pawn hits the wall', 'common',
  'd4 Nf6 c4 g6 Nc3 Bg7 e4 d6 f4 O-O Nf3 e5 d5 exf4 Bxf4 Re8',
  alts=[('bki-f4-e5', 'E-pawn pushes at your knight', 'd4 Nf6 c4 g6 Nc3 Bg7 e4 d6 f4 O-O e5 dxe5 fxe5 Nfd7'),
        ('bki-f4-fxe5', 'F-pawn takes your e-pawn', 'd4 Nf6 c4 g6 Nc3 Bg7 e4 d6 f4 O-O Nf3 e5 fxe5 dxe5 dxe5 Qxd1+'),
        ('bki-f4-dxe5', 'D-pawn takes, queens come off', 'd4 Nf6 c4 g6 Nc3 Bg7 e4 d6 f4 O-O Nf3 e5 dxe5 dxe5 Qxd8 Rxd8')],
  why='One in nine pushes a fourth pawn. A wall that wide is hard to guard, and your e-pawn hits it at once.', outcome='A sharp, open fight')
L('bki-bg5', 'bki-center', 'The bishop comes at your knight', 'Castle; the queen\'s knight backs up the e-pawn', 'common',
  'd4 Nf6 c4 g6 Nc3 Bg7 e4 d6 Bg5 O-O Qd2 Nbd7',
  alts=[('bki-bg5-nf3', 'Zinnowitz Variation', 'd4 Nf6 c4 g6 Nc3 Bg7 e4 d6 Bg5 O-O Nf3 Nbd7'),
        ('bki-bg5-bxf6', 'Bishop takes the knight', 'd4 Nf6 c4 g6 Nc3 Bg7 e4 d6 Bg5 O-O Bxf6 Bxf6'),
        ('bki-bg5-bd3', 'Bishop to the middle', 'd4 Nf6 c4 g6 Nc3 Bg7 e4 d6 Bg5 O-O Bd3 Nbd7')],
  why='One in ten brings the bishop out first. Castle as usual, and get the queen\'s knight behind the e-pawn before it goes.', outcome='Equal')
L('bki-5th', 'bki-center', 'Other fifth moves', 'The same two moves: castle, then the e-pawn', 'common',
  'd4 Nf6 c4 g6 Nc3 Bg7 e4 d6 Bd3 O-O Be3 Ng4',
  alts=[('bki-5th-nf3', 'King\'s knight out', 'd4 Nf6 c4 g6 Nc3 Bg7 e4 d6 Bd3 O-O Nf3 e5'),
        ('bki-5th-nge2', 'King\'s knight tucked in', 'd4 Nf6 c4 g6 Nc3 Bg7 e4 d6 Bd3 O-O Nge2 e5 d5 Nfd7')],
  why='The bishop in the middle, the small edge pawn, the pawn that guards the e-pawn. Castle and strike with the e-pawn.', outcome='Equal')
L('bki-nf3', 'bki-quiet', 'Knights out, no big center', 'D-pawn, castle, and the e-pawn when the knight backs it up', 'core',
  'd4 Nf6 c4 g6 Nc3 Bg7 Nf3 d6 Bg5 O-O e3 Nbd7 Bd3 e5',
  alts=[('bki-nf3-e4', 'E-pawn two squares after all', 'd4 Nf6 c4 g6 Nc3 Bg7 Nf3 d6 e4 O-O'),
        ('bki-nf3-e4v2', 'Zinnowitz Variation', 'd4 Nf6 c4 g6 Nc3 Bg7 Nf3 d6 Bg5 O-O e4 Nbd7'),
        ('bki-nf3-be2', 'Bishop to the quiet square', 'd4 Nf6 c4 g6 Nc3 Bg7 Nf3 d6 Bg5 O-O e3 Nbd7 Be2 e5'),
        ('bki-nf3-bf4', 'Dark bishop out', 'd4 Nf6 c4 g6 Nc3 Bg7 Nf3 d6 Bf4 O-O e3 Nc6 Bd3 e5'),
        ('bki-nf3-qd2', 'Queen comes out', 'd4 Nf6 c4 g6 Nc3 Bg7 Nf3 d6 Bg5 O-O Qd2 Nbd7'),
        ('bki-nf3-e3', 'Small e-pawn move', 'd4 Nf6 c4 g6 Nc3 Bg7 Nf3 d6 e3 O-O Be2 e5 dxe5 dxe5'),
        ('bki-nf3-e3bd3', 'Small e-pawn move, then bishop to the middle', 'd4 Nf6 c4 g6 Nc3 Bg7 Nf3 d6 e3 O-O Bd3 e5 dxe5 dxe5 Nxe5 Nfd7'),
        ('bki-nf3-e3be2', 'Small e-pawn move, then Semi-Classical Variation', 'd4 Nf6 c4 g6 Nc3 Bg7 Nf3 d6 e3 O-O Be2 e5 O-O Nc6'),
        ('bki-nf3-bf4e4', 'Dark bishop out, then e-pawn two squares', 'd4 Nf6 c4 g6 Nc3 Bg7 Nf3 d6 Bf4 O-O e4 e5'),
        ('bki-nf3-bf4e3', 'Dark bishop out, then small e-pawn move', 'd4 Nf6 c4 g6 Nc3 Bg7 Nf3 d6 Bf4 O-O e3 Nc6 Be2 Nd7'),
        ('bki-nf3-e3bd3d5', 'Small e-pawn move, then bishop to the middle, then small d-pawn move', 'd4 Nf6 c4 g6 Nc3 Bg7 Nf3 d6 e3 O-O Bd3 e5 d5 Nfd7')],
  why='A quarter of club players leave the e-pawn at home. Your five moves don\'t change.', outcome='Equal')
L('bki-4th', 'bki-quiet', 'Other fourth moves', 'The early bishop, the small e-pawn', 'common',
  'd4 Nf6 c4 g6 Nc3 Bg7 Bg5 d6 e3 O-O Bd3 Nbd7',
  alts=[('bki-4th-e3', 'Small e-pawn move', 'd4 Nf6 c4 g6 Nc3 Bg7 e3 d6 Nf3 O-O'),
        ('bki-4th-nf3', 'Smyslov Variation', 'd4 Nf6 c4 g6 Nc3 Bg7 Bg5 d6 Nf3 O-O'),
        ('bki-4th-e4', 'Accelerated Averbakh Variation', 'd4 Nf6 c4 g6 Nc3 Bg7 Bg5 d6 e4 O-O'),
        ('bki-4th-nf3v2', 'King\'s knight out', 'd4 Nf6 c4 g6 Nc3 Bg7 Bg5 d6 e3 O-O Nf3 Nbd7'),
        ('bki-4th-bxf6', 'Bishop takes the knight', 'd4 Nf6 c4 g6 Nc3 Bg7 Bg5 d6 Bxf6 Bxf6'),
        ('bki-4th-e3bd3', 'Small e-pawn move, then bishop to the middle', 'd4 Nf6 c4 g6 Nc3 Bg7 e3 d6 Bd3 O-O Nf3 e5'),
        ('bki-4th-e3bd3nge2', 'Small e-pawn move, then bishop to the middle, then king\'s knight tucked in', 'd4 Nf6 c4 g6 Nc3 Bg7 e3 d6 Bd3 O-O Nge2 e5')],
  why='Whatever White does on move four, the d-pawn and castling come next.', outcome='Equal')
L('bki-3rd', 'bki-quiet', 'Other third moves', 'King\'s knight first, the small e-pawn, the early bishop', 'common',
  'd4 Nf6 c4 g6 e3 Bg7 Bd3 d6',
  alts=[('bki-3rd-nf3', 'King\'s Knight Variation', 'd4 Nf6 c4 g6 Nf3 Bg7 Nc3 d6'),
        ('bki-3rd-nf3v2', 'King\'s knight out', 'd4 Nf6 c4 g6 e3 Bg7 Nf3 d6'),
        ('bki-3rd-nc3', 'Queen\'s knight out', 'd4 Nf6 c4 g6 e3 Bg7 Nc3 d6'),
        ('bki-3rd-bg5', 'Bishop comes at the knight', 'd4 Nf6 c4 g6 Bg5 Bg7 Nc3 d6'),
        ('bki-3rd-bg5nf3', 'Bishop comes at the knight, then king\'s knight out', 'd4 Nf6 c4 g6 Bg5 Bg7 Nf3 Ne4'),
        ('bki-3rd-nf3e3', 'King\'s Knight Variation, then small e-pawn move', 'd4 Nf6 c4 g6 Nf3 Bg7 e3 d6 Nc3 O-O'),
        ('bki-3rd-bg5bxf6', 'Bishop comes at the knight, then bishop takes the knight', 'd4 Nf6 c4 g6 Bg5 Bg7 Bxf6 Bxf6'),
        ('bki-3rd-nf3bf4', 'King\'s Knight Variation, then dark bishop out', 'd4 Nf6 c4 g6 Nf3 Bg7 Bf4 d6 e3 O-O'),
        ('bki-3rd-nf3bg5', 'King\'s Knight Variation, then bishop comes at the knight', 'd4 Nf6 c4 g6 Nf3 Bg7 Bg5 Ne4 Bf4 d6'),
        ('bki-3rd-bg5e3', 'Bishop comes at the knight, then small e-pawn move', 'd4 Nf6 c4 g6 Bg5 Bg7 e3 d6 Nc3 O-O'),
        ('bki-3rd-nf3bg5e3', 'King\'s Knight Variation, then bishop comes at the knight, then small e-pawn move', 'd4 Nf6 c4 g6 Nf3 Bg7 Bg5 Ne4 e3 Nxg5 Nxg5 O-O'),
        ('bki-3rd-nf3bf4nc3', 'King\'s Knight Variation, then dark bishop out, then queen\'s knight out', 'd4 Nf6 c4 g6 Nf3 Bg7 Bf4 d6 Nc3 O-O'),
        ('bki-3rd-bg5e3nf3', 'Bishop comes at the knight, then small e-pawn move, then king\'s knight out', 'd4 Nf6 c4 g6 Bg5 Bg7 e3 d6 Nf3 Ne4'),
        ('bki-3rd-nf3g3', 'King\'s Knight Variation, then Fianchetto Variation', 'd4 Nf6 c4 g6 Nf3 Bg7 g3 d6 Bg2 O-O O-O Nc6 Nc3 e5'),
        ('bki-3rd-nf3e3be2', 'King\'s Knight Variation, then small e-pawn move, then bishop to the quiet square', 'd4 Nf6 c4 g6 Nf3 Bg7 e3 d6 Be2 O-O O-O e5'),
        ('bki-3rd-nf3e3bd3', 'King\'s Knight Variation, then small e-pawn move, then bishop to the middle', 'd4 Nf6 c4 g6 Nf3 Bg7 e3 d6 Bd3 O-O O-O e5')],
  why='One in three holds the queen\'s knight back. Bishop to the long diagonal, d-pawn, castle.', outcome='Equal')
L('bkx-london', 'bkx-bishop', 'The London System', 'The same five moves; then the knight and the e-pawn', 'core',
  'd4 Nf6 Bf4 g6 e3 Bg7 Nf3 d6 h3 O-O',
  alts=[('bkx-london-nf3', 'London System', 'd4 Nf6 Bf4 g6 Nf3 Bg7 e3 d6'),
        ('bkx-london-bd3', 'Bishop to the middle', 'd4 Nf6 Bf4 g6 e3 Bg7 Bd3 d6 Nf3 O-O'),
        ('bkx-london-c3', 'Small c-pawn move', 'd4 Nf6 Bf4 g6 e3 Bg7 c3 d6 Bd3 O-O'),
        ('bkx-london-c3nf3', 'Small c-pawn move, then king\'s knight out', 'd4 Nf6 Bf4 g6 e3 Bg7 c3 d6 Nf3 O-O'),
        ('bkx-london-c4', 'C-pawn two squares', 'd4 Nf6 Bf4 g6 e3 Bg7 Nf3 d6 c4 O-O'),
        ('bkx-london-bd3nd2', 'Bishop to the middle, then queen\'s knight tucked in', 'd4 Nf6 Bf4 g6 e3 Bg7 Bd3 d6 Nd2 O-O'),
        ('bkx-london-nc3', 'Queen\'s knight out', 'd4 Nf6 Bf4 g6 Nc3 d5 Nf3 Bg7'),
        ('bkx-london-c3bd3', 'Small c-pawn move, then bishop to the middle', 'd4 Nf6 Bf4 g6 e3 Bg7 Nf3 d6 c3 O-O Bd3 Nc6'),
        ('bkx-london-bd3nbd2', 'Bishop to the middle, then queen\'s knight tucked in on move 5', 'd4 Nf6 Bf4 g6 e3 Bg7 Nf3 d6 Bd3 O-O Nbd2 Nc6'),
        ('bkx-london-bd3oo', 'Bishop to the middle, then castles', 'd4 Nf6 Bf4 g6 e3 Bg7 Nf3 d6 Bd3 O-O O-O Nc6'),
        ('bkx-london-nc3v2', 'Queen\'s knight out on move 5', 'd4 Nf6 Bf4 g6 e3 Bg7 Nf3 d6 Nc3 O-O'),
        ('bkx-london-nc3nb5', 'Queen\'s knight out, then knight jumps forward', 'd4 Nf6 Bf4 g6 Nc3 d5 Nb5 Na6 e3 Bg7 Nf3 O-O'),
        ('bkx-london-bd3c3', 'Bishop to the middle, then small c-pawn move', 'd4 Nf6 Bf4 g6 e3 Bg7 Nf3 d6 Bd3 O-O c3 Nc6'),
        ('bkx-london-nf3nc3', 'London System, then queen\'s knight out', 'd4 Nf6 Bf4 g6 Nf3 Bg7 Nc3 d5 e3 O-O'),
        ('bkx-london-be2', 'Bishop to the quiet square', 'd4 Nf6 Bf4 g6 e3 Bg7 Nf3 d6 Be2 O-O O-O Nc6'),
        ('bkx-london-nbd2', 'Queen\'s knight tucked in', 'd4 Nf6 Bf4 g6 e3 Bg7 Nf3 d6 Nbd2 O-O c3 Nc6'),
        ('bkx-london-bd3c3v2', 'Bishop to the middle, then small c-pawn move on move 4', 'd4 Nf6 Bf4 g6 e3 Bg7 Bd3 d6 c3 O-O Nd2 e5'),
        ('bkx-london-nbd2bd3', 'Queen\'s knight tucked in, then bishop to the middle', 'd4 Nf6 Bf4 g6 e3 Bg7 Nf3 d6 Nbd2 O-O Bd3 Nc6'),
        ('bkx-london-c3nbd2', 'Small c-pawn move, then queen\'s knight tucked in', 'd4 Nf6 Bf4 g6 e3 Bg7 Nf3 d6 c3 O-O Nbd2 Nc6 Bd3 e5'),
        ('bkx-london-nf3nc3nb5', 'London System, then queen\'s knight out, then knight jumps forward', 'd4 Nf6 Bf4 g6 Nf3 Bg7 Nc3 d5 Nb5 Na6'),
        ('bkx-london-nc3e3', 'Queen\'s knight out, then small e-pawn move', 'd4 Nf6 Bf4 g6 Nc3 d5 e3 Bg7 Nf3 O-O'),
        ('bkx-london-c3nd2', 'Small c-pawn move, then queen\'s knight tucked in on move 4', 'd4 Nf6 Bf4 g6 e3 Bg7 c3 d6 Nd2 O-O Ngf3 Nc6'),
        ('bkx-london-nc3nb5nc3', 'Queen\'s knight out, then knight jumps forward, then knight steps back', 'd4 Nf6 Bf4 g6 Nc3 d5 Nb5 Na6 e3 Bg7 Nc3 O-O'),
        ('bkx-london-c3h3', 'Small c-pawn move, then small h-pawn move', 'd4 Nf6 Bf4 g6 e3 Bg7 c3 d6 h3 O-O')],
  why='One in seven plays the London. Your bishop on the long diagonal is a good piece against it, and the e-pawn push hits the London bishop.', outcome='Equal, with easy moves')
L('bkx-nf3', 'bkx-bishop', 'King\'s knight first', 'The setup against the London, the Torre and the Colle by this move order', 'core',
  'd4 Nf6 Nf3 g6 e3 Bg7 Bd3 d6 O-O O-O',
  alts=[('bkx-nf3-bf4', 'London System', 'd4 Nf6 Nf3 g6 Bf4 Bg7'),
        ('bkx-nf3-c4', 'King\'s Knight Variation', 'd4 Nf6 Nf3 g6 c4 Bg7'),
        ('bkx-nf3-nc3', 'Queen\'s knight out', 'd4 Nf6 Nf3 g6 Nc3 d5 Bf4 Bg7'),
        ('bkx-nf3-c4v2', 'C-pawn two squares', 'd4 Nf6 Nf3 g6 e3 Bg7 c4 d6'),
        ('bkx-nf3-nc3e3', 'Queen\'s knight out, then small e-pawn move', 'd4 Nf6 Nf3 g6 Nc3 d5 e3 Bg7'),
        ('bkx-nf3-bg5', 'Fianchetto Defense', 'd4 Nf6 Nf3 g6 Bg5 Bg7 Nc3 d5'),
        ('bkx-nf3-nc3v2', 'Queen\'s knight out on move 4', 'd4 Nf6 Nf3 g6 e3 Bg7 Nc3 d5'),
        ('bkx-nf3-bg5e3', 'Fianchetto Defense, then small e-pawn move', 'd4 Nf6 Nf3 g6 Bg5 Bg7 e3 d6 Bd3 O-O'),
        ('bkx-nf3-be2', 'Bishop to the quiet square', 'd4 Nf6 Nf3 g6 e3 Bg7 Be2 d6 O-O O-O'),
        ('bkx-nf3-nc3bg5', 'Queen\'s knight out, then bishop comes at the knight', 'd4 Nf6 Nf3 g6 Nc3 d5 Bg5 Bg7 e3 O-O Bd3 Nbd7'),
        ('bkx-nf3-bc4', 'Bishop aims at f7', 'd4 Nf6 Nf3 g6 e3 Bg7 Bc4 d6'),
        ('bkx-nf3-g3', 'Przepiorka Variation', 'd4 Nf6 Nf3 g6 g3 Bg7 Bg2 d6 O-O O-O c4 Nc6'),
        ('bkx-nf3-g3nc3', 'Przepiorka Variation, then queen\'s knight out', 'd4 Nf6 Nf3 g6 g3 Bg7 Bg2 d6 O-O O-O Nc3 Nc6'),
        ('bkx-nf3-bg5bxf6', 'Fianchetto Defense, then bishop takes the knight', 'd4 Nf6 Nf3 g6 Bg5 Bg7 Bxf6 exf6 e3 d6'),
        ('bkx-nf3-nc3bg5bxf6', 'Queen\'s knight out, then bishop comes at the knight, then bishop takes the knight', 'd4 Nf6 Nf3 g6 Nc3 d5 Bg5 Bg7 Bxf6 exf6'),
        ('bkx-nf3-nbd2', 'Queen\'s knight tucked in', 'd4 Nf6 Nf3 g6 e3 Bg7 Bd3 d6 Nbd2 O-O')],
  why='One in eight starts with the knight and chooses a system on move three. Your setup is the same against all of them.', outcome='Equal')
L('bkx-e3', 'bkx-other', 'The small e-pawn', 'Colle setups: fianchetto, d-pawn, castle', 'common',
  'd4 Nf6 e3 g6 f4 Bg7 Nf3 d6',
  alts=[('bkx-e3-nf3', 'King\'s knight out', 'd4 Nf6 e3 g6 Nf3 Bg7'),
        ('bkx-e3-c4', 'C-pawn two squares', 'd4 Nf6 e3 g6 c4 Bg7'),
        ('bkx-e3-bd3', 'Bishop to the middle', 'd4 Nf6 e3 g6 Bd3 Bg7 Nf3 d6'),
        ('bkx-e3-nc3', 'Queen\'s knight out', 'd4 Nf6 e3 g6 Nc3 d5 Nf3 Bg7'),
        ('bkx-e3-bd3nd2', 'Bishop to the middle, then queen\'s knight tucked in', 'd4 Nf6 e3 g6 Bd3 Bg7 Nd2 d6'),
        ('bkx-e3-bd3f4', 'Bishop to the middle, then f-pawn two squares', 'd4 Nf6 e3 g6 Bd3 Bg7 f4 d6 Nf3 O-O O-O c5'),
        ('bkx-e3-bd3c3', 'Bishop to the middle, then small c-pawn move', 'd4 Nf6 e3 g6 Bd3 Bg7 c3 d6'),
        ('bkx-e3-nc3bd3', 'Queen\'s knight out, then bishop to the middle', 'd4 Nf6 e3 g6 Nc3 d5 Bd3 Bg7'),
        ('bkx-e3-c3', 'Small c-pawn move', 'd4 Nf6 e3 g6 c3 Bg7 Nf3 d6'),
        ('bkx-e3-c3bd3', 'Small c-pawn move, then bishop to the middle', 'd4 Nf6 e3 g6 c3 Bg7 Bd3 d6')],
  why='One in ten shuts the dark bishop in. Nothing to fear, and nothing changes.', outcome='Equal')
L('bkx-nc3', 'bkx-other', 'Queen\'s knight first: stop the e-pawn', 'D-pawn two squares, then the bishop out', 'common',
  'd4 Nf6 Nc3 d5 Bg5 Bf5 e3 e6',
  alts=[('bkx-nc3-e3', 'Small e-pawn move', 'd4 Nf6 Nc3 d5 e3 g6'),
        ('bkx-nc3-nf3', 'King\'s knight out', 'd4 Nf6 Nc3 d5 Nf3 Bf5 Bf4 e6'),
        ('bkx-nc3-nf3bg5', 'King\'s knight out, then bishop comes at the knight', 'd4 Nf6 Nc3 d5 Nf3 Bf5 Bg5 e6'),
        ('bkx-nc3-bf4', 'Rapport-Jobava System', 'd4 Nf6 Nc3 d5 Bf4 Bf5 Nf3 e6 e3 c6'),
        ('bkx-nc3-nf3v2', 'King\'s knight out on move 4', 'd4 Nf6 Nc3 d5 Bg5 Bf5 Nf3 e6 e3 Nbd7'),
        ('bkx-nc3-bxf6', 'Veresov Variation', 'd4 Nf6 Nc3 d5 Bg5 Bf5 Bxf6 exf6 e3 c6 Bd3 Bxd3 Qxd3 Bd6'),
        ('bkx-nc3-bf4e3', 'Rapport-Jobava System, then small e-pawn move', 'd4 Nf6 Nc3 d5 Bf4 Bf5 e3 e6 Bd3 Bxd3 Qxd3 c6'),
        ('bkx-nc3-bf4nb5', 'Rapport-Jobava System, then knight jumps forward', 'd4 Nf6 Nc3 d5 Bf4 Bf5 Nb5 Na6 e3 e6 Nf3 c6'),
        ('bkx-nc3-bxf6nf3', 'Veresov Variation, then king\'s knight out', 'd4 Nf6 Nc3 d5 Bg5 Bf5 Bxf6 exf6 Nf3 c6 e3 g6 Bd3 Be6'),
        ('bkx-nc3-e4', 'Hübsch Gambit', 'd4 Nf6 Nc3 d5 e4 dxe4 f3 Bf5 fxe4 Nxe4'),
        ('bkx-nc3-bxf6f3', 'Veresov Variation, then small f-pawn move', 'd4 Nf6 Nc3 d5 Bg5 Bf5 Bxf6 exf6 f3 g6'),
        ('bkx-nc3-nf3g3', 'King\'s knight out, then small g-pawn move', 'd4 Nf6 Nc3 d5 Nf3 Bf5 g3 h6 Bg2 c6'),
        ('bkx-nc3-nf3e3', 'King\'s knight out, then small e-pawn move', 'd4 Nf6 Nc3 d5 Nf3 Bf5 e3 e6 Bd3 Bxd3 Qxd3 c6 O-O Nbd7'),
        ('bkx-nc3-bf4e3nf3', 'Rapport-Jobava System, then small e-pawn move, then king\'s knight out', 'd4 Nf6 Nc3 d5 Bf4 Bf5 e3 e6 Nf3 c6 Bd3 Bxd3')],
  why='White wants the e-pawn in the middle next. This is the one time your d-pawn goes two squares: it stops that, and your light bishop comes out.', outcome='Equal')
L('bkx-tromp', 'bkx-other', 'The Trompowsky', 'G-pawn anyway; if the bishop takes, the e-pawn takes back', 'rare',
  'd4 Nf6 Bg5 g6 Bxf6 exf6 e4 Bg7 Nf3 d6',
  alts=[('bkx-tromp-nf3', 'Fianchetto Defense', 'd4 Nf6 Bg5 g6 Nf3 Bg7'),
        ('bkx-tromp-nf3v2', 'King\'s knight out', 'd4 Nf6 Bg5 g6 Bxf6 exf6 Nf3 Bg7'),
        ('bkx-tromp-e3', 'Small e-pawn move', 'd4 Nf6 Bg5 g6 e3 Bg7 Nf3 d6'),
        ('bkx-tromp-e3v2', 'Small e-pawn move on move 4', 'd4 Nf6 Bg5 g6 Bxf6 exf6 e3 Bg7 Nf3 d6'),
        ('bkx-tromp-e3bd3', 'Small e-pawn move, then bishop to the middle', 'd4 Nf6 Bg5 g6 e3 Bg7 Bd3 d6'),
        ('bkx-tromp-nc3', 'Queen\'s knight out', 'd4 Nf6 Bg5 g6 Nc3 d5 Bxf6 exf6'),
        ('bkx-tromp-nc3v2', 'Queen\'s knight out on move 4', 'd4 Nf6 Bg5 g6 Bxf6 exf6 Nc3 d5 e4 dxe4')],
  why='The bishop comes at your knight on move two. Carry on: if it takes, you get the two bishops and an open file.', outcome='Equal')

# ============================================================== notes
n('d4 Nf6', 'Knight first', 'The first move of the King\'s Indian setup: knight, g-pawn, bishop, d-pawn, castle. The same five moves against almost everything.', ['key'])
n('d4 Nf6 c4 g6', 'G-pawn one square', 'It makes room for the bishop on the long diagonal.', ['key'], arrows=['f8g7g'])
n('d4 Nf6 c4 g6 Nc3 Bg7', 'Bishop to the long diagonal', 'It looks through the middle at White\'s d-pawn. Everything you do later is about opening this diagonal.', ['key'])
n('d4 Nf6 c4 g6 Nc3 Bg7 e4 d6', 'D-pawn one square', 'It keeps White\'s e-pawn from pushing on at your knight, and gets your own e-pawn ready.', ['key'])
n('d4 Nf6 c4 g6 Nc3 Bg7 e4 d6 Nf3 O-O', 'Castle', 'King safe before the middle opens.')
n('d4 Nf6 c4 g6 Nc3 Bg7 e4 d6 Nf3 O-O Be2 e5', 'E-pawn two squares', 'The strike the whole setup was built for.', ['key'], arrows=['e5d4g'])
n('d4 Nf6 c4 g6 Nc3 Bg7 e4 d6 Nf3 O-O Be2 e5 O-O Nc6', 'Knight in front of the c-pawn', 'More pressure on the d-pawn. When White pushes it past, the knight drops back beside the king and your f-pawn goes.', ['key'])
n('d4 Nf6 c4 g6 Nc3 Bg7 e4 d6 Nf3 O-O Be2 e5 d5', 'White closes the middle', 'Now the play is on the wings, and yours is the king\'s side.')
n('d4 Nf6 c4 g6 Nc3 Bg7 e4 d6 f4', 'Four Pawns Attack', 'A fourth pawn joins the wall. It takes time, and the wall has to be guarded.')
n('d4 Nf6 c4 g6 Nc3 Bg7 e4 d6 f4 O-O', 'Castle', 'Let White build. Your e-pawn hits the wall next.')
n('d4 Nf6 Bf4 g6', 'G-pawn one square', 'The same setup against the London. Your bishop will look straight down the long diagonal.')
n('d4 Nf6 Bg5 g6', 'G-pawn anyway', 'If the bishop takes the knight, the e-pawn takes back and your bishop has the long diagonal to itself.', ['key'])
n('d4 Nf6 Bg5 g6 Bxf6 exf6', 'E-pawn takes back', 'Toward the middle. You have the two bishops and an open file for the rook.', ['key'])
n('d4 Nf6 Nc3 d5', 'D-pawn two squares', 'The one time the d-pawn goes two. White\'s e-pawn can no longer walk into the middle for free.', ['key'], arrows=['d5e4r'])
n('d4 Nf6 Nf3 g6 Nc3 d5', 'D-pawn two squares', 'The queen\'s knight is out with the c-pawn still at home, so the e-pawn wants to go two squares next. Your d-pawn stops it.', ['key'], arrows=['d5e4r'])
n('d4 Nf6 Bf4 g6 Nc3 d5', 'D-pawn two squares', 'Queen\'s knight in front of the c-pawn: the e-pawn is coming. Stop it, then carry on with the bishop and castling.', ['key'], arrows=['d5e4r'])
n('d4 Nf6 e3 g6 Bd3 Bg7 f4 d6 Nf3 O-O O-O c5', 'C-pawn two squares', 'White\'s f-pawn holds the square your e-pawn wants. Hit the d-pawn from the other side instead.', ['key'], arrows=['c5d4g'])
n('d4 Nf6 c4 g6 Nc3 Bg7 e4 d6 f4 O-O e5 dxe5', 'Take it', 'The pawn came at your knight a move too early. Take it, and the wall has a hole in it whichever way White takes back.', ['key'])
n('d4 Nf6 c4 g6 Nc3 Bg7 e4 d6 Bg5 O-O Qd2 Nbd7', 'Queen\'s knight behind the e-pawn', 'With the bishop at your knight, the e-pawn waits one move: this knight guards the other one first.', ['key'])
n('d4 Nf6 c4 g6 Nf3 Bg7 Bg5 Ne4', 'Knight jumps at the bishop', 'The bishop has to move again, and the long diagonal is open for yours.', ['key'])
# the other side's moves that start a named line
n('d4 Nf6 Bf4', 'Accelerated London System')
n('d4 Nf6 Bg5', 'Trompowsky Attack')
n('d4 Nf6 Nf3', 'Knights Variation')
n('d4 Nf6 Bf4 g6 Nf3', 'London System')
n('d4 Nf6 Bg5 g6 Nf3', 'Fianchetto Defense')
n('d4 Nf6 Nc3 d5 Bf4', 'Rapport-Jobava System')
n('d4 Nf6 Nc3 d5 Bg5', 'Richter-Veresov Attack')
n('d4 Nf6 Nc3 d5 e4', 'Hübsch Gambit')
n('d4 Nf6 Nf3 g6 Bf4', 'London System')
n('d4 Nf6 Nf3 g6 Bg5', 'Fianchetto Defense')
n('d4 Nf6 Nf3 g6 c4', 'King\'s Knight Variation')
n('d4 Nf6 Nf3 g6 g3', 'Przepiorka Variation')
n('d4 Nf6 c4 g6 Nc3', 'King\'s Indian Defense')
n('d4 Nf6 c4 g6 Nf3', 'King\'s Knight Variation')
n('d4 Nf6 Bf4 g6 Nc3 d5 Nf3', 'Barry Attack')
n('d4 Nf6 Bf4 g6 Nf3 Bg7 e3', 'London System')
n('d4 Nf6 Bf4 g6 e3 Bg7 Nf3', 'London System')
n('d4 Nf6 Nc3 d5 Bg5 Bf5 Bxf6', 'Veresov Variation')
n('d4 Nf6 Nf3 g6 Nc3 d5 Bf4', 'Barry Attack')
n('d4 Nf6 c4 g6 Nf3 Bg7 g3', 'Fianchetto Variation')
n('d4 Nf6 c4 g6 Nc3 Bg7 Bg5 d6 Nf3', 'Smyslov Variation')
n('d4 Nf6 c4 g6 Nc3 Bg7 Bg5 d6 e4', 'Accelerated Averbakh Variation')
n('d4 Nf6 c4 g6 Nc3 Bg7 Nf3 d6 Bg5', 'Smyslov Variation')
n('d4 Nf6 c4 g6 Nc3 Bg7 Nf3 d6 e4', 'Rare Defenses')
n('d4 Nf6 c4 g6 Nc3 Bg7 e4 d6 Bg5', 'Accelerated Averbakh Variation')
n('d4 Nf6 c4 g6 Nc3 Bg7 e4 d6 Nf3', 'Rare Defenses')
n('d4 Nf6 c4 g6 Nc3 Bg7 Nf3 d6 Bg5 O-O e4', 'Zinnowitz Variation')
n('d4 Nf6 c4 g6 Nc3 Bg7 Nf3 d6 e3 O-O Be2', 'Semi-Classical Variation')
n('d4 Nf6 c4 g6 Nc3 Bg7 e4 d6 Bg5 O-O Nf3', 'Zinnowitz Variation')
n('d4 Nf6 c4 g6 Nc3 Bg7 e4 d6 Nf3 O-O Be2', 'Orthodox Variation')
n('d4 Nf6 c4 g6 Nc3 Bg7 e4 d6 Nf3 O-O Be3', 'Larsen Variation')
n('d4 Nf6 c4 g6 Nc3 Bg7 e4 d6 Nf3 O-O Bg5', 'Zinnowitz Variation')
