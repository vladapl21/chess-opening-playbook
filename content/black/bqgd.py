"""Black against the d-pawn: the Queen's Gambit Declined. D-pawn two squares, the e-pawn beside it, knight, bishop one
square, castle. Against the pin: the h-pawn asks the bishop and the knight jumps into the middle (the Lasker Defense).
After a trade of pawns: the c-pawn backs the d-pawn. Against a system without the c-pawn, yours goes two squares. A
separate pack with two chapters (see PACKS in bmeta.py). The lines were drafted with pipeline/draft.py: White's moves by
the Maia 1300/1500 odds, yours from the setup's order wherever Stockfish 17.1 accepts it and the engine's move
elsewhere. SAN is internal only; notes are plain English."""
from bcontent import L, P, J, n

P('bqg-pin', 'qgd', 'The bishop pins your knight', 'Lasker Defense', "White's bishop comes out to pin your knight. Bishop one square, castle, ask the bishop with the h-pawn, and then the knight jumps into the middle: two pairs of pieces come off and your position has room to breathe.")
P('bqg-exch', 'qgd', 'The pawns are traded', 'Exchange Variation', 'White takes in the middle and you take back with the e-pawn. Your light bishop is free, the c-pawn backs up the d-pawn, and the knights come behind it.')
P('bqg-quiet', 'qgd', 'No pin', 'Knights first, the Catalan, quiet lines', 'White develops without pinning the knight, or brings the knights out first. The same five moves, and then the c-pawn frees your game.')
P('bqx-bishop', 'qgdx', 'The London and the knight first', 'White plays without the c-pawn', 'No c-pawn hits your center, so yours goes two squares. Knight, e-pawn, c-pawn, knight, and the bishop offers a trade to the London bishop.')
P('bqx-other', 'qgdx', 'The Colle, the Jobava and the rest', 'Second-move sidelines', "The slow systems and the gambits. Your first moves don't change.")

L('bqg-main', 'bqg-pin', 'The bishop pins your knight', 'Bishop, castle, the h-pawn, then the knight jumps in', 'core',
  'd4 d5 c4 e6 Nc3 Nf6 Bg5 Be7 e3 O-O Nf3 h6 Bh4 Ne4 Bxe7 Qxe7 Nxe4 dxe4',
  alts=[('bqg-main-nf3', 'King\'s knight out', 'd4 d5 c4 e6 Nc3 Nf6 Bg5 Be7 Nf3 O-O e3 h6 Bh4 Ne4 Bxe7 Qxe7 Nxe4 dxe4'),
        ('bqg-main-nf3bxf6', 'King\'s knight out, then Anti-Tartakower Variation', 'd4 d5 c4 e6 Nc3 Nf6 Bg5 Be7 Nf3 O-O e3 h6 Bxf6 Bxf6'),
        ('bqg-main-bd3', 'Bishop to the middle', 'd4 d5 c4 e6 Nc3 Nf6 Bg5 Be7 e3 O-O Bd3 h6 Bh4 Nbd7'),
        ('bqg-main-bxf6', 'Heral Variation', 'd4 d5 c4 e6 Nc3 Nf6 Bg5 Be7 Bxf6 Bxf6 e3 O-O'),
        ('bqg-main-bxf6cxd5', 'Heral Variation, then pawn takes the pawn', 'd4 d5 c4 e6 Nc3 Nf6 Bg5 Be7 Bxf6 Bxf6 cxd5 exd5'),
        ('bqg-main-cxd5', 'Pawn takes the pawn', 'd4 d5 c4 e6 Nc3 Nf6 Bg5 Be7 cxd5 exd5 e3 O-O'),
        ('bqg-main-cxd5v2', 'Pawn takes the pawn on move 9', 'd4 d5 c4 e6 Nc3 Nf6 Bg5 Be7 e3 O-O Nf3 h6 Bh4 Ne4 Bxe7 Qxe7 cxd5 Nxc3'),
        ('bqg-main-nf3bh4', 'King\'s knight out, then bishop steps back', 'd4 d5 c4 e6 Nc3 Nf6 Bg5 Be7 Nf3 O-O e3 h6 Bh4 Ne4 Nxe4 dxe4'),
        ('bqg-main-bxf6nf3', 'Heral Variation, then king\'s knight out', 'd4 d5 c4 e6 Nc3 Nf6 Bg5 Be7 Bxf6 Bxf6 Nf3 O-O e3 c6'),
        ('bqg-main-bd3bxf6', 'Bishop to the middle, then bishop takes the knight', 'd4 d5 c4 e6 Nc3 Nf6 Bg5 Be7 e3 O-O Bd3 h6 Bxf6 Bxf6')],
  why='The oldest line of the Queen\'s Gambit. Your bishop breaks the pin, you castle, and the knight jump trades two pairs of pieces: a cramped position needs fewer pieces.', outcome='Equal, with an easy game')
L('bqg-exch', 'bqg-exch', 'The Exchange: pawns come off', 'E-pawn takes back; the c-pawn backs the d-pawn', 'core',
  'd4 d5 c4 e6 Nc3 Nf6 cxd5 exd5 Bg5 c6 e3 Be7 Bd3 O-O Qc2 h6',
  alts=[('bqg-exch-nf3', 'King\'s knight out', 'd4 d5 c4 e6 Nc3 Nf6 cxd5 exd5 Nf3 Be7'),
        ('bqg-exch-nf3v2', 'King\'s knight out on move 6', 'd4 d5 c4 e6 Nc3 Nf6 cxd5 exd5 Bg5 c6 Nf3 Be7')],
  why='White trades in the middle. Your light bishop has an open line, and the c-pawn makes the d-pawn safe for good.', outcome='Solid and equal')
L('bqg-exch3', 'bqg-exch', 'The Exchange on move three', 'The same pawns; knight, bishop, castle', 'common',
  'd4 d5 c4 e6 cxd5 exd5 Nf3 Nf6 Bg5 Be7',
  alts=[('bqg-exch3-nc3', 'Queen\'s knight out', 'd4 d5 c4 e6 cxd5 exd5 Nc3 Nf6'),
        ('bqg-exch3-e3', 'Small e-pawn move', 'd4 d5 c4 e6 cxd5 exd5 e3 Nf6'),
        ('bqg-exch3-nc3v2', 'Queen\'s knight out on move 5', 'd4 d5 c4 e6 cxd5 exd5 Nf3 Nf6 Nc3 Be7')],
  why='The trade comes a move earlier. Nothing changes in your setup.', outcome='Equal')
L('bqg-nf3', 'bqg-quiet', 'Both knights out', 'Bishop one square, castle; the London bishop or the pin', 'core',
  'd4 d5 c4 e6 Nc3 Nf6 Nf3 Be7 Bf4 O-O e3 c6 Bd3 Nbd7',
  alts=[('bqg-nf3-bg5', 'Queen\'s Gambit Declined', 'd4 d5 c4 e6 Nc3 Nf6 Nf3 Be7 Bg5 O-O'),
        ('bqg-nf3-e3', 'Small e-pawn move', 'd4 d5 c4 e6 Nc3 Nf6 Nf3 Be7 e3 O-O Bd3 Nbd7 O-O c6'),
        ('bqg-nf3-cxd5', 'Pawn takes the pawn', 'd4 d5 c4 e6 Nc3 Nf6 Nf3 Be7 cxd5 exd5'),
        ('bqg-nf3-e3be2', 'Small e-pawn move, then bishop to the quiet square', 'd4 d5 c4 e6 Nc3 Nf6 Nf3 Be7 e3 O-O Be2 c6 O-O Nbd7'),
        ('bqg-nf3-e3cxd5', 'Small e-pawn move, then pawn takes the pawn', 'd4 d5 c4 e6 Nc3 Nf6 Nf3 Be7 e3 O-O cxd5 exd5'),
        ('bqg-nf3-be2', 'Bishop to the quiet square', 'd4 d5 c4 e6 Nc3 Nf6 Nf3 Be7 Bf4 O-O e3 c6 Be2 Nbd7')],
  why='White brings the second knight before the bishop. Bishop one square and castle, and you are ready for whichever bishop move comes.', outcome='Equal')
L('bqg-4th', 'bqg-quiet', 'Other fourth moves', 'The quiet e-pawn, the bishop to the other diagonal', 'common',
  'd4 d5 c4 e6 Nc3 Nf6 e3 Be7 Nf3 O-O',
  alts=[('bqg-4th-bf4', 'Harrwitz Attack', 'd4 d5 c4 e6 Nc3 Nf6 Bf4 Be7 Nf3 O-O'),
        ('bqg-4th-bf4e3', 'Harrwitz Attack, then small e-pawn move', 'd4 d5 c4 e6 Nc3 Nf6 Bf4 Be7 e3 O-O Nf3 c6'),
        ('bqg-4th-bd3', 'Bishop to the middle', 'd4 d5 c4 e6 Nc3 Nf6 e3 Be7 Bd3 O-O'),
        ('bqg-4th-cxd5', 'Pawn takes the pawn', 'd4 d5 c4 e6 Nc3 Nf6 e3 Be7 cxd5 exd5'),
        ('bqg-4th-bf4e3bd3', 'Harrwitz Attack, then small e-pawn move, then bishop to the middle', 'd4 d5 c4 e6 Nc3 Nf6 Bf4 Be7 e3 O-O Bd3 c5')],
  why='White develops without the pin. Your setup is the same five moves.', outcome='Equal')
L('bqg-knight', 'bqg-quiet', 'The king\'s knight first', 'The same setup; the fianchetto, the quiet e-pawn', 'core',
  'd4 d5 c4 e6 Nf3 Nf6 g3 Be7 Bg2 O-O',
  alts=[('bqg-knight-nc3', 'Three Knights Variation', 'd4 d5 c4 e6 Nf3 Nf6 Nc3 Be7'),
        ('bqg-knight-bg5', 'Traditional Variation', 'd4 d5 c4 e6 Nf3 Nf6 Bg5 Be7 Nc3 O-O'),
        ('bqg-knight-e3', 'Small e-pawn move', 'd4 d5 c4 e6 Nf3 Nf6 e3 Be7 Nc3 O-O'),
        ('bqg-knight-bg5e3', 'Traditional Variation, then small e-pawn move', 'd4 d5 c4 e6 Nf3 Nf6 Bg5 Be7 e3 O-O Nc3 h6'),
        ('bqg-knight-bg5e3bd3', 'Traditional Variation, then small e-pawn move, then bishop to the middle', 'd4 d5 c4 e6 Nf3 Nf6 Bg5 Be7 e3 O-O Bd3 h6')],
  why='Half of club players bring this knight first. The setup comes out the same way, and the bishop on the long diagonal is met by taking the c-pawn.', outcome='Equal')
L('bqg-third', 'bqg-quiet', 'Other third moves', 'The quiet e-pawn, the fianchetto, a bishop out early', 'common',
  'd4 d5 c4 e6 e3 Nf6 Nf3 Be7',
  alts=[('bqg-third-nc3', 'Queen\'s knight out', 'd4 d5 c4 e6 e3 Nf6 Nc3 Be7'),
        ('bqg-third-cxd5', 'Pawn takes the pawn', 'd4 d5 c4 e6 e3 Nf6 cxd5 exd5'),
        ('bqg-third-a3', 'Small a-pawn move', 'd4 d5 c4 e6 a3 Nf6 Nc3 c6 Nf3 dxc4'),
        ('bqg-third-a3nf3', 'Small a-pawn move, then king\'s knight out', 'd4 d5 c4 e6 a3 Nf6 Nf3 Be7'),
        ('bqg-third-a3bg5', 'Small a-pawn move, then bishop pins the knight', 'd4 d5 c4 e6 a3 Nf6 Bg5 c5'),
        ('bqg-third-a3nc3', 'Small a-pawn move, then queen\'s knight out', 'd4 d5 c4 e6 a3 Nf6 Nc3 c6 Bg5 dxc4 e4 b5'),
        ('bqg-third-a3e3', 'Small a-pawn move, then small e-pawn move', 'd4 d5 c4 e6 a3 Nf6 e3 Be7'),
        ('bqg-third-a3nc3e3', 'Small a-pawn move, then queen\'s knight out, then small e-pawn move', 'd4 d5 c4 e6 a3 Nf6 Nc3 c6 e3 Be7'),
        ('bqg-third-a3v2', 'Small a-pawn move on move 4', 'd4 d5 c4 e6 e3 Nf6 a3 Be7 Nc3 O-O')],
  why='White holds the knights back. Knight, bishop, castle.', outcome='Equal')
L('bqx-london', 'bqx-bishop', 'The London', 'E-pawn, c-pawn two squares, knight, and the bishop offers a trade', 'core',
  'd4 d5 Bf4 Nf6 e3 e6 Nf3 c5 c3 Nc6 Nbd2 Bd6 Bg3 O-O',
  alts=[('bqx-london-c3', 'Small c-pawn move', 'd4 d5 Bf4 Nf6 e3 e6 c3 c5 Nf3 Nc6'),
        ('bqx-london-bd3', 'Bishop to the middle', 'd4 d5 Bf4 Nf6 e3 e6 Bd3 c5 c3 Nc6 Nf3 Nh5'),
        ('bqx-london-nf3', 'London System', 'd4 d5 Bf4 Nf6 Nf3 Bf5 e3 e6 c3 c5'),
        ('bqx-london-nc3', 'Rapport-Jobava System', 'd4 d5 Bf4 Nf6 Nc3 e6 e3 Bd6'),
        ('bqx-london-nf3e3', 'London System, then small e-pawn move', 'd4 d5 Bf4 Nf6 Nf3 Bf5 e3 e6 c4 Be7'),
        ('bqx-london-nc3nb5', 'Rapport-Jobava System, then knight jumps forward', 'd4 d5 Bf4 Nf6 Nc3 e6 Nb5 Bd6 Nxd6+ cxd6'),
        ('bqx-london-nf3nc3', 'London System, then queen\'s knight out', 'd4 d5 Bf4 Nf6 Nf3 Bf5 Nc3 e6'),
        ('bqx-london-bd3v2', 'Bishop to the middle on move 6', 'd4 d5 Bf4 Nf6 e3 e6 Nf3 c5 c3 Nc6 Bd3 Nh5 Bg3 Be7'),
        ('bqx-london-c3bd3', 'Small c-pawn move, then bishop to the middle', 'd4 d5 Bf4 Nf6 e3 e6 c3 c5 Bd3 Nc6'),
        ('bqx-london-bb5', 'Bishop pins the knight', 'd4 d5 Bf4 Nf6 e3 e6 Nf3 c5 c3 Nc6 Bb5 Bd6'),
        ('bqx-london-nc3nb5bxd6', 'Rapport-Jobava System, then knight jumps forward, then bishop takes the bishop', 'd4 d5 Bf4 Nf6 Nc3 e6 Nb5 Bd6 Bxd6 cxd6'),
        ('bqx-london-nc3nf3', 'Rapport-Jobava System, then king\'s knight out', 'd4 d5 Bf4 Nf6 Nc3 e6 Nf3 c5'),
        ('bqx-london-dxc5', 'Pawn takes the pawn', 'd4 d5 Bf4 Nf6 e3 e6 Nf3 c5 dxc5 Nc6'),
        ('bqx-london-h3', 'Small h-pawn move', 'd4 d5 Bf4 Nf6 h3 e6 e3 c5'),
        ('bqx-london-c4', 'C-pawn two squares', 'd4 d5 Bf4 Nf6 e3 e6 Nf3 c5 c4 Be7'),
        ('bqx-london-nc3a3', 'Rapport-Jobava System, then small a-pawn move', 'd4 d5 Bf4 Nf6 Nc3 e6 a3 c5'),
        ('bqx-london-nf3e3bd3', 'London System, then small e-pawn move, then bishop to the middle', 'd4 d5 Bf4 Nf6 Nf3 Bf5 e3 e6 Bd3 Bxd3 Qxd3 Bd6 Bxd6 Qxd6'),
        ('bqx-london-nf3e3nbd2', 'London System, then small e-pawn move, then queen\'s knight tucked in', 'd4 d5 Bf4 Nf6 Nf3 Bf5 e3 e6 Nbd2 c5 c3 Nc6'),
        ('bqx-london-bd3nd2', 'Bishop to the middle, then queen\'s knight tucked in', 'd4 d5 Bf4 Nf6 e3 e6 Bd3 c5 c3 Nc6 Nd2 Bd6 Bg3 e5'),
        ('bqx-london-nf3e3bd3bg3', 'London System, then small e-pawn move, then bishop to the middle, then bishop steps back', 'd4 d5 Bf4 Nf6 Nf3 Bf5 e3 e6 Bd3 Bxd3 Qxd3 Bd6 Bg3 c5'),
        ('bqx-london-c4v2', 'C-pawn two squares on move 4', 'd4 d5 Bf4 Nf6 e3 e6 c4 Be7 Nc3 O-O'),
        ('bqx-london-h3nf3', 'Small h-pawn move, then king\'s knight out', 'd4 d5 Bf4 Nf6 h3 e6 Nf3 c5'),
        ('bqx-london-c3nd2', 'Small c-pawn move, then queen\'s knight tucked in', 'd4 d5 Bf4 Nf6 e3 e6 c3 c5 Nd2 Nc6 Ngf3 Bd6')],
  why='One in five club players set up the London. Without a c-pawn hitting your center you have a free hand: the c-pawn goes two squares, and your bishop offers a trade to White\'s best piece.', outcome='Equal and easy')
L('bqx-nf3', 'bqx-bishop', 'The knight first', 'Your bishop comes out before the e-pawn shuts it in', 'core',
  'd4 d5 Nf3 Nf6 e3 Bf5 Bd3 Bxd3 Qxd3 c6 O-O e6',
  alts=[('bqx-nf3-bf4', 'London System', 'd4 d5 Nf3 Nf6 Bf4 Bf5'),
        ('bqx-nf3-c4', 'C-pawn two squares', 'd4 d5 Nf3 Nf6 c4 e6'),
        ('bqx-nf3-h3', 'Small h-pawn move', 'd4 d5 Nf3 Nf6 h3 e6'),
        ('bqx-nf3-nc3', 'Queen\'s knight out', 'd4 d5 Nf3 Nf6 Nc3 e6 Bf4 c5'),
        ('bqx-nf3-nc3bg5', 'Queen\'s knight out, then bishop pins the knight', 'd4 d5 Nf3 Nf6 Nc3 e6 Bg5 Be7 e3 c5'),
        ('bqx-nf3-c4v2', 'C-pawn two squares on move 4', 'd4 d5 Nf3 Nf6 e3 Bf5 c4 e6 Nc3 Be7'),
        ('bqx-nf3-nc3e3', 'Queen\'s knight out, then small e-pawn move', 'd4 d5 Nf3 Nf6 Nc3 e6 e3 c5'),
        ('bqx-nf3-g3', 'Pseudo-Catalan', 'd4 d5 Nf3 Nf6 g3 e6 Bg2 c5 O-O Nc6'),
        ('bqx-nf3-nc3v2', 'Queen\'s knight out on move 4', 'd4 d5 Nf3 Nf6 e3 Bf5 Nc3 e6'),
        ('bqx-nf3-bg5', 'Torre Attack', 'd4 d5 Nf3 Nf6 Bg5 c5 dxc5 e6'),
        ('bqx-nf3-bg5bxf6', 'Torre Attack, then bishop takes the knight', 'd4 d5 Nf3 Nf6 Bg5 c5 Bxf6 exf6 e3 Nc6'),
        ('bqx-nf3-be2', 'Bishop to the quiet square', 'd4 d5 Nf3 Nf6 e3 Bf5 Be2 e6'),
        ('bqx-nf3-nc3a3', 'Queen\'s knight out, then small a-pawn move', 'd4 d5 Nf3 Nf6 Nc3 e6 a3 c5'),
        ('bqx-nf3-g3c3', 'Pseudo-Catalan, then small c-pawn move', 'd4 d5 Nf3 Nf6 g3 e6 Bg2 c5 c3 Nc6 O-O Bd6'),
        ('bqx-nf3-bg5e3', 'Torre Attack, then small e-pawn move', 'd4 d5 Nf3 Nf6 Bg5 c5 e3 Nc6 Bb5 Qa5+ Nc3 Ne4'),
        ('bqx-nf3-nc3v3', 'Queen\'s knight out on move 6', 'd4 d5 Nf3 Nf6 e3 Bf5 Bd3 Bxd3 Qxd3 c6 Nc3 e6'),
        ('bqx-nf3-bg5c3', 'Torre Attack, then small c-pawn move', 'd4 d5 Nf3 Nf6 Bg5 c5 c3 Nc6 e3 Qb6'),
        ('bqx-nf3-g3dxc5', 'Pseudo-Catalan, then pawn takes the pawn', 'd4 d5 Nf3 Nf6 g3 e6 Bg2 c5 dxc5 Nc6')],
  why='White waits with the c-pawn. With no pawn hitting your center the light bishop has time to come out first, and the e-pawn closes the door behind it.', outcome='Equal')
L('bqx-colle', 'bqx-other', 'The quiet e-pawn', 'The Colle and the Stonewall: c-pawn two squares', 'common',
  'd4 d5 e3 Nf6 Bd3 e6 Nf3 c5 c3 Nc6',
  alts=[('bqx-colle-nf3', 'Colle System', 'd4 d5 e3 Nf6 Nf3 Bf5'),
        ('bqx-colle-c4', 'C-pawn two squares', 'd4 d5 e3 Nf6 c4 e6'),
        ('bqx-colle-c3', 'Small c-pawn move', 'd4 d5 e3 Nf6 c3 e6'),
        ('bqx-colle-nc3', 'Queen\'s knight out', 'd4 d5 e3 Nf6 Nc3 e6 Nf3 c5'),
        ('bqx-colle-f4', 'F-pawn two squares', 'd4 d5 e3 Nf6 f4 Bf5 Nf3 e6'),
        ('bqx-colle-h3', 'Small h-pawn move', 'd4 d5 e3 Nf6 h3 e6 Nf3 c5'),
        ('bqx-colle-h3a3', 'Small h-pawn move, then small a-pawn move', 'd4 d5 e3 Nf6 h3 e6 a3 c5'),
        ('bqx-colle-nd2', 'Queen\'s knight tucked in', 'd4 d5 e3 Nf6 Bd3 e6 Nd2 c5'),
        ('bqx-colle-c3v2', 'Small c-pawn move on move 4', 'd4 d5 e3 Nf6 Bd3 e6 c3 c5'),
        ('bqx-colle-f4nf3', 'F-pawn two squares, then king\'s knight out', 'd4 d5 e3 Nf6 Bd3 e6 f4 c5 Nf3 Nc6'),
        ('bqx-colle-f4c3', 'F-pawn two squares, then small c-pawn move', 'd4 d5 e3 Nf6 Bd3 e6 f4 c5 c3 Nc6 Nf3 Bd6'),
        ('bqx-colle-nc3a3', 'Queen\'s knight out, then small a-pawn move', 'd4 d5 e3 Nf6 Nc3 e6 a3 c5')],
  why='White shuts the bishop in and builds slowly. You take the room on the queen\'s side.', outcome='Comfortable')
L('bqx-nc3', 'bqx-other', 'The queen\'s knight on move two', 'The Jobava and the Veresov: knight out, then the e-pawn', 'common',
  'd4 d5 Nc3 Nf6 Bf4 e6',
  alts=[('bqx-nc3-nf3', 'King\'s knight out', 'd4 d5 Nc3 Nf6 Nf3 e6'),
        ('bqx-nc3-e3', 'Small e-pawn move', 'd4 d5 Nc3 Nf6 e3 e6'),
        ('bqx-nc3-bg5', 'Richter-Veresov Attack', 'd4 d5 Nc3 Nf6 Bg5 c5 Bxf6 gxf6 dxc5 d4 Ne4 Nc6'),
        ('bqx-nc3-e4', 'Hübsch Gambit', 'd4 d5 Nc3 Nf6 e4 Nxe4 Nxe4 dxe4'),
        ('bqx-nc3-f3', 'Richter Attack', 'd4 d5 Nc3 Nf6 f3 e6 e4 c5'),
        ('bqx-nc3-bg5dxc5', 'Richter-Veresov Attack, then pawn takes the pawn', 'd4 d5 Nc3 Nf6 Bg5 c5 dxc5 d4 Bxf6 exf6'),
        ('bqx-nc3-bg5e3', 'Richter-Veresov Attack, then small e-pawn move', 'd4 d5 Nc3 Nf6 Bg5 c5 e3 e6')],
  why='The knight blocks White\'s own c-pawn and aims at a quick e-pawn push. Your knight stops it.', outcome='Equal')
L('bqx-bg5', 'bqx-other', 'The bishop out to the edge', 'Nothing to pin yet: develop around it', 'rare',
  'd4 d5 Bg5 Nf6 e3 e6',
  alts=[('bqx-bg5-bxf6', 'Bishop takes the knight', 'd4 d5 Bg5 Nf6 Bxf6 exf6 e3 c5'),
        ('bqx-bg5-nf3', 'Torre Attack', 'd4 d5 Bg5 Nf6 Nf3 c5')],
  why='The bishop comes out before there is a knight to pin.', outcome='Equal')
L('bqx-second', 'bqx-other', 'Other second moves', 'A pawn offered, the fianchetto', 'common',
  'd4 d5 g3 Nf6 Bg2 e6 Nf3 c5',
  alts=[('bqx-second-c3', 'Small c-pawn move', 'd4 d5 c3 Nf6 Nf3 e6'),
        ('bqx-second-e4', 'Blackmar-Diemer Gambit', 'd4 d5 e4 dxe4 Nc3 Nf6 Bg5 Bf5'),
        ('bqx-second-c3e3', 'Small c-pawn move, then small e-pawn move', 'd4 d5 c3 Nf6 e3 e6'),
        ('bqx-second-c3bf4', 'Small c-pawn move, then dark bishop out', 'd4 d5 c3 Nf6 Bf4 e6'),
        ('bqx-second-e4nc3', 'Blackmar-Diemer Gambit, then queen\'s knight out', 'd4 d5 e4 dxe4 Nc3 Nf6 f3 Bf5 fxe4 Nxe4 Nxe4 Bxe4'),
        ('bqx-second-e4f3', 'Blackmar-Diemer Gambit, then Blackmar Gambit', 'd4 d5 e4 dxe4 f3 e5 fxe4 Qh4+'),
        ('bqx-second-c3bg5', 'Small c-pawn move, then bishop comes at the knight', 'd4 d5 c3 Nf6 Bg5 e6')],
  why='The gambits and the slow second moves. Take what is safe to take, and develop.', outcome='Equal or better')

# ============================================================== notes
n('d4 d5 c4 e6', 'E-pawn one square', 'You keep the pawn in the middle and say no to the gambit. The d-pawn is as safe as it gets.', ['key'])
n('d4 d5 c4 e6 Nc3 Nf6', 'Knight out', 'A second guard for the d-pawn.', ['key'])
n('d4 d5 c4 e6 Nc3 Nf6 Bg5 Be7', 'Bishop one square', 'The pin is broken before it can hurt. You castle next.', ['key'])
n('d4 d5 c4 e6 Nc3 Nf6 Bg5 Be7 e3 O-O', 'Castle', 'King safe. Now ask the bishop what it wants.', ['key'])
n('d4 d5 c4 e6 Nc3 Nf6 Bg5 Be7 e3 O-O Nf3 h6', 'H-pawn asks the bishop', 'It has to take or step back, and your king gets a square for later.', ['key'], arrows=['h6g5r'])
n('d4 d5 c4 e6 Nc3 Nf6 Bg5 Be7 e3 O-O Nf3 h6 Bh4 Ne4', 'Knight jumps in', 'It offers two trades at once: the bishops, and the knights. With fewer pieces your position has room.', ['key'], arrows=['e7h4g', 'e4c3g'])
n('d4 d5 c4 e6 Nc3 Nf6 Bg5 Be7 e3 O-O Nf3 h6 Bh4 Ne4 Bxe7 Qxe7', 'Queen takes back', 'She comes out with a move gained, and the knight still stands in the middle.', ['key'])
n('d4 d5 c4 e6 Nc3 Nf6 cxd5 exd5', 'E-pawn takes back', 'The line of your light bishop opens, and you keep a pawn in the middle.', ['key'])
n('d4 d5 c4 e6 Nc3 Nf6 cxd5 exd5 Bg5 c6', 'C-pawn backs the d-pawn', 'The d-pawn can\'t be won now, and your queen has a diagonal.', ['key'])
n('d4 d5 c4 e6 Nf3 Nf6', 'Knight out', 'The same move whichever knight White brought first.', ['key'])
n('d4 d5 Bf4 Nf6 e3 e6', 'E-pawn one square', 'The same pawns as against the gambit. With no c-pawn hitting your center, yours goes two squares next.', ['key'])
n('d4 d5 Bf4 Nf6 e3 e6 Nf3 c5', 'C-pawn two squares', 'It hits the d-pawn, and the knight comes out behind it.', ['key'], arrows=['c5d4r'])
n('d4 d5 Bf4 Nf6 e3 e6 Nf3 c5 c3 Nc6 Nbd2 Bd6', 'Bishop offers a trade', 'The London bishop is White\'s best piece. If it takes, your queen takes back and stands well; if it steps back, you castle.', ['key'], arrows=['d6f4g'])
# the other side's moves that start a named line
n('d4 d5 Bf4 Nf6 Nf3', 'London System')
n('d4 d5 Bg5 Nf6 Nf3', 'Torre Attack')
n('d4 d5 Nc3 Nf6 e4', 'Hübsch Gambit')
n('d4 d5 Nf3 Nf6 g3', 'Pseudo-Catalan')
n('d4 d5 c4 e6 Nc3', 'Queen\'s Knight Variation')
n('d4 d5 e3 Nf6 Bd3', 'Stonewall Attack')
n('d4 d5 e3 Nf6 Nf3', 'Colle System')
n('d4 d5 c4 e6 Nc3 Nf6 Bf4', 'Harrwitz Attack')
n('d4 d5 c4 e6 Nc3 Nf6 Nf3', 'Three Knights Variation')
n('d4 d5 c4 e6 Nf3 Nf6 Bg5', 'Traditional Variation')
n('d4 d5 c4 e6 Nf3 Nf6 Nc3', 'Three Knights Variation')
n('d4 d5 e3 Nf6 Bd3 e6 Nf3', 'Colle System')
n('d4 d5 e4 dxe4 Nc3 Nf6 Bg5', 'von Popiel Gambit')
n('d4 d5 c4 e6 Nc3 Nf6 Bf4 Be7 Nf3', 'Harrwitz Attack')
n('d4 d5 c4 e6 Nc3 Nf6 Bg5 Be7 Bxf6', 'Heral Variation')
n('d4 d5 c4 e6 Nc3 Nf6 Nf3 Be7 Bf4', 'Harrwitz Attack')
n('d4 d5 c4 e6 Nc3 Nf6 Nf3 Be7 Bg5', 'Queen\'s Gambit Declined')
n('d4 d5 c4 e6 Nc3 Nf6 cxd5 exd5 Bg5', 'Positional Variation')
n('d4 d5 c4 e6 Nf3 Nf6 Bg5 Be7 Nc3', 'Queen\'s Gambit Declined')
n('d4 d5 e3 Nf6 Bd3 e6 Nf3 c5 c3', 'Traditional Colle')
n('d4 d5 Bf4 Nf6 e3 e6 Nf3 c5 c3 Nc6 Nbd2', 'London System')
n('d4 d5 Bf4 Nf6 e3 e6 c3 c5 Nd2 Nc6 Ngf3', 'London System')
n('d4 d5 c4 e6 Nc3 Nf6 Bg5 Be7 Nf3 O-O e3 h6 Bxf6', 'Anti-Tartakower Variation')
n('d4 d5 c4 e6 Nc3 Nf6 cxd5 exd5 Bg5 c6 e3 Be7 Bd3 O-O Qc2', 'Reshevsky Variation')
