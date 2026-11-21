"""Black against the e-pawn, the Sicilian's second variation: the Dragon. C-pawn two squares, take the d-pawn when
it comes, then one setup: d-pawn one square, knight, g-pawn, bishop to the long diagonal, castle, queen's knight. A
separate pack (see PACKS in bmeta.py). The lines were drafted with pipeline/draft.py: White's moves by the Maia 1300/1500
odds, yours from the setup's order wherever Stockfish 17.1 accepts it and the engine's move elsewhere. SAN is internal
only; notes are plain English."""
from bcontent import L, P, J, n

P('bdr-open', 'dragon', 'White opens the middle', 'Open Sicilian', 'White trades the d-pawn for your c-pawn. Your bishop goes to the long diagonal, you castle, and the half-open file belongs to your rook.')
P('bdr-third', 'dragon', 'White holds the d-pawn back', 'Third-move tries', 'A check, the Italian bishop, a small pawn move. The setup comes out in the same order.')
P('bdr-second', 'dragon', 'White skips the knight', 'Second-move tries', 'The bishop, the other knight, the small c-pawn, a gambit. One setup answers them all.')

L('bdr-yugo', 'bdr-open', 'The Yugoslav Attack', 'Bishop, castle, knight, then the rook to the open file', 'core',
  'e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 g6 Be3 Bg7 f3 O-O Qd2 Nc6 Bc4 Bd7 O-O-O Rc8 Bb3 Ne5 h4 h5',
  alts=[('bdr-yugo-bc4', 'Bishop aims at f7', 'e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 g6 Be3 Bg7 Bc4 Ng4'),
        ('bdr-yugo-qd2', 'Queen comes out', 'e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 g6 Be3 Bg7 Qd2 Nc6 O-O-O Ng4'),
        ('bdr-yugo-bd3', 'Bishop to the middle', 'e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 g6 Be3 Bg7 Bd3 O-O'),
        ('bdr-yugo-ooo', 'Castles long', 'e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 g6 Be3 Bg7 f3 O-O Qd2 Nc6 O-O-O d5')],
  why='White sets up to castle long and push the edge pawn at your king. Your pieces come out in one order and the open file points at White\'s king.', outcome='A race you are ready for')
L('bdr-classical', 'bdr-open', 'The Classical Dragon', 'The same setup; White castles short', 'core',
  'e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 g6 Be2 Bg7 O-O O-O',
  alts=[('bdr-classical-be3', 'Bishop behind the center pawns', 'e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 g6 Be2 Bg7 Be3 O-O')],
  why='The quiet way to meet the Dragon. Nothing changes in your setup, and the long diagonal is yours.', outcome='Equal and easy to play')
L('bdr-sixth', 'bdr-open', 'Other sixth moves', 'The Italian bishop, the pin, a bishop check', 'common',
  'e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 g6 Bc4 Bg7 O-O O-O Re1 Nc6',
  alts=[('bdr-sixth-be3', 'Bishop behind the center pawns', 'e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 g6 Bc4 Bg7 Be3 Ng4'),
        ('bdr-sixth-bg5', 'Bishop comes at the knight', 'e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 g6 Bg5 Bg7 Bxf6 Bxf6'),
        ('bdr-sixth-bg5bc4', 'Bishop comes at the knight, then bishop aims at f7', 'e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 g6 Bg5 Bg7 Bc4 O-O O-O Nc6'),
        ('bdr-sixth-bg5v2', 'Bishop comes at the knight on move 7', 'e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 g6 Bc4 Bg7 Bg5 O-O'),
        ('bdr-sixth-bg5qd2', 'Bishop comes at the knight, then queen comes out', 'e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 g6 Bg5 Bg7 Qd2 O-O O-O-O Nc6'),
        ('bdr-sixth-bg5qd2bh6', 'Bishop comes at the knight, then queen comes out, then bishop slides over', 'e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 g6 Bg5 Bg7 Qd2 O-O Bh6 Nc6'),
        ('bdr-sixth-bg5v3', 'Bishop comes at the knight on move 8', 'e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 g6 Bc4 Bg7 O-O O-O Bg5 Nc6'),
        ('bdr-sixth-be3v2', 'Bishop behind the center pawns on move 8', 'e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 g6 Bc4 Bg7 O-O O-O Be3 Nc6'),
        ('bdr-sixth-bg5bb5', 'Bishop comes at the knight, then bishop gives check', 'e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 g6 Bg5 Bg7 Bb5+ Bd7 Bxd7+ Nbxd7'),
        ('bdr-sixth-f4', 'F-pawn two squares', 'e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 g6 Bc4 Bg7 O-O O-O f4 Qb6'),
        ('bdr-sixth-bg5bb5oo', 'Bishop comes at the knight, then bishop gives check, then castles', 'e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 g6 Bg5 Bg7 Bb5+ Bd7 O-O O-O')],
  why='Whatever White plays on move six, the bishop goes to the long diagonal and you castle.', outcome='Equal')
L('bdr-fourth', 'bdr-open', 'The queen takes back', 'Your knight hits her and gains a move', 'common',
  'e4 c5 Nf3 d6 d4 cxd4 Qxd4 Nc6 Bb5 Nf6 Bxc6+ bxc6',
  alts=[('bdr-fourth-qa4', 'Queen moves', 'e4 c5 Nf3 d6 d4 cxd4 Qxd4 Nc6 Qa4 Nf6'),
        ('bdr-fourth-qd1', 'Queen steps back', 'e4 c5 Nf3 d6 d4 cxd4 Qxd4 Nc6 Qd1 Nf6 Nc3 g6'),
        ('bdr-fourth-qc3', 'Queen steps back on move 5', 'e4 c5 Nf3 d6 d4 cxd4 Qxd4 Nc6 Qc3 Nf6')],
  why='One in six takes back with the queen. She stands in the open, and your knight comes out with a hit on her.', outcome='Comfortable')
L('bdr-moscow', 'bdr-third', 'The Moscow: a bishop check', 'Block with the bishop and trade it off', 'common',
  'e4 c5 Nf3 d6 Bb5+ Bd7 Bxd7+ Qxd7 O-O Nf6 d3 g6',
  alts=[('bdr-moscow-bc4', 'Bishop steps back', 'e4 c5 Nf3 d6 Bb5+ Bd7 Bc4 Nf6'),
        ('bdr-moscow-nc3', 'Queen\'s knight out', 'e4 c5 Nf3 d6 Bb5+ Bd7 Nc3 Nf6'),
        ('bdr-moscow-nc3v2', 'Queen\'s knight out on move 5', 'e4 c5 Nf3 d6 Bb5+ Bd7 Bxd7+ Qxd7 Nc3 Nf6'),
        ('bdr-moscow-d3', 'Small d-pawn move', 'e4 c5 Nf3 d6 Bb5+ Bd7 Bxd7+ Qxd7 d3 Nf6'),
        ('bdr-moscow-d4', 'D-pawn two squares', 'e4 c5 Nf3 d6 Bb5+ Bd7 Bxd7+ Qxd7 d4 cxd4 Nxd4 Nf6 Nc3 g6'),
        ('bdr-moscow-re1', 'Rook to a new file', 'e4 c5 Nf3 d6 Bb5+ Bd7 Bxd7+ Qxd7 O-O Nf6 Re1 g6'),
        ('bdr-moscow-nc3v3', 'Queen\'s knight out on move 6', 'e4 c5 Nf3 d6 Bb5+ Bd7 Bxd7+ Qxd7 O-O Nf6 Nc3 Nc6')],
  why='A check that skips the open game. Your bishop blocks, the bishops come off, and the setup goes on.', outcome='Equal')
L('bdr-bc4', 'bdr-third', 'The Italian bishop', 'Knight out; the bishop is aimed at a wall', 'common',
  'e4 c5 Nf3 d6 Bc4 Nf6 d3 Nc6 O-O g6',
  alts=[('bdr-bc4-nc3', 'Queen\'s knight out', 'e4 c5 Nf3 d6 Bc4 Nf6 d3 Nc6 Nc3 g6'),
        ('bdr-bc4-ng5', 'Knight jumps forward', 'e4 c5 Nf3 d6 Bc4 Nf6 Ng5 e6 Nc3 Nc6'),
        ('bdr-bc4-c3', 'Small c-pawn move', 'e4 c5 Nf3 d6 Bc4 Nf6 d3 Nc6 c3 g6'),
        ('bdr-bc4-bg5', 'Bishop comes at the knight', 'e4 c5 Nf3 d6 Bc4 Nf6 d3 Nc6 Bg5 g6'),
        ('bdr-bc4-nc3d3', 'Queen\'s knight out, then small d-pawn move', 'e4 c5 Nf3 d6 Bc4 Nf6 Nc3 Nc6 d3 g6 Bg5 Bg7'),
        ('bdr-bc4-ng5qf3', 'Knight jumps forward, then queen comes out', 'e4 c5 Nf3 d6 Bc4 Nf6 Ng5 e6 Qf3 Nc6'),
        ('bdr-bc4-oo', 'Castles', 'e4 c5 Nf3 d6 Bc4 Nf6 O-O Nxe4 Re1 Nf6'),
        ('bdr-bc4-nc3d4', 'Queen\'s knight out, then d-pawn two squares', 'e4 c5 Nf3 d6 Bc4 Nf6 Nc3 Nc6 d4 cxd4 Nxd4 g6 Nxc6 bxc6'),
        ('bdr-bc4-nc3a3', 'Queen\'s knight out, then small a-pawn move', 'e4 c5 Nf3 d6 Bc4 Nf6 Nc3 Nc6 a3 g6'),
        ('bdr-bc4-e5', 'Small e-pawn move', 'e4 c5 Nf3 d6 Bc4 Nf6 e5 dxe5 Nxe5 e6 O-O Bd7'),
        ('bdr-bc4-a3', 'Small a-pawn move', 'e4 c5 Nf3 d6 Bc4 Nf6 d3 Nc6 a3 g6'),
        ('bdr-bc4-ood3', 'Castles, then small d-pawn move', 'e4 c5 Nf3 d6 Bc4 Nf6 O-O Nxe4 d3 Nf6'),
        ('bdr-bc4-ng5d3', 'Knight jumps forward, then small d-pawn move', 'e4 c5 Nf3 d6 Bc4 Nf6 Ng5 e6 d3 g6 O-O Bg7'),
        ('bdr-bc4-ng5oo', 'Knight jumps forward, then castles', 'e4 c5 Nf3 d6 Bc4 Nf6 d3 Nc6 Ng5 e6 O-O g6'),
        ('bdr-bc4-nc3oo', 'Queen\'s knight out, then castles', 'e4 c5 Nf3 d6 Bc4 Nf6 Nc3 Nc6 O-O g6 d3 Bg7'),
        ('bdr-bc4-nc3d3ng5', 'Queen\'s knight out, then small d-pawn move, then knight jumps forward', 'e4 c5 Nf3 d6 Bc4 Nf6 Nc3 Nc6 d3 g6 Ng5 e6'),
        ('bdr-bc4-nc3ood4', 'Queen\'s knight out, then castles, then d-pawn two squares', 'e4 c5 Nf3 d6 Bc4 Nf6 Nc3 Nc6 O-O g6 d4 cxd4 Nxd4 Bg7'),
        ('bdr-bc4-nc3ng5', 'Queen\'s knight out, then knight jumps forward', 'e4 c5 Nf3 d6 Bc4 Nf6 Nc3 Nc6 Ng5 e6 d3 g6'),
        ('bdr-bc4-ng5nc3', 'Knight jumps forward, then queen\'s knight out', 'e4 c5 Nf3 d6 Bc4 Nf6 d3 Nc6 Ng5 e6 Nc3 g6'),
        ('bdr-bc4-nc3d3oo', 'Queen\'s knight out, then small d-pawn move, then castles', 'e4 c5 Nf3 d6 Bc4 Nf6 Nc3 Nc6 d3 g6 O-O Bg7'),
        ('bdr-bc4-ng5oov2', 'Knight jumps forward, then castles on move 4', 'e4 c5 Nf3 d6 Bc4 Nf6 Ng5 e6 O-O h6 Nf3 Nxe4 d3 Nf6'),
        ('bdr-bc4-ng5d4', 'Knight jumps forward, then d-pawn two squares', 'e4 c5 Nf3 d6 Bc4 Nf6 Ng5 e6 d4 h6 Nf3 Nxe4'),
        ('bdr-bc4-ng5d3nc3', 'Knight jumps forward, then small d-pawn move, then queen\'s knight out', 'e4 c5 Nf3 d6 Bc4 Nf6 Ng5 e6 d3 g6 Nc3 Bg7')],
  why='Club players love this bishop. Against the Sicilian it has little to aim at, and your setup comes out untouched.', outcome='Comfortable')
L('bdr-third', 'bdr-third', 'Other third moves', 'The small c-pawn, the knight, the quiet d-pawn', 'common',
  'e4 c5 Nf3 d6 c3 Nf6 e5 dxe5 Nxe5 Nbd7',
  alts=[('bdr-third-nc3', 'Queen\'s knight out', 'e4 c5 Nf3 d6 Nc3 Nf6 d4 cxd4 Nxd4 g6'),
        ('bdr-third-nc3bc4', 'Queen\'s knight out, then bishop aims at f7', 'e4 c5 Nf3 d6 Nc3 Nf6 Bc4 Nc6'),
        ('bdr-third-nc3d4', 'Queen\'s knight out, then d-pawn two squares', 'e4 c5 Nf3 d6 Nc3 Nf6 d4 cxd4 Qxd4 Nc6'),
        ('bdr-third-nc3bb5', 'Queen\'s knight out, then bishop gives check', 'e4 c5 Nf3 d6 Nc3 Nf6 Bb5+ Bd7 Bxd7+ Qxd7'),
        ('bdr-third-bd3', 'Bishop to the middle', 'e4 c5 Nf3 d6 c3 Nf6 Bd3 g6'),
        ('bdr-third-d3', 'Small d-pawn move', 'e4 c5 Nf3 d6 c3 Nf6 d3 g6 Bg5 Bg7'),
        ('bdr-third-qc2', 'Queen comes out', 'e4 c5 Nf3 d6 c3 Nf6 Qc2 g6'),
        ('bdr-third-d3be2', 'Small d-pawn move, then bishop to the quiet square', 'e4 c5 Nf3 d6 c3 Nf6 d3 g6 Be2 Bg7'),
        ('bdr-third-nc3d3', 'Queen\'s knight out, then small d-pawn move', 'e4 c5 Nf3 d6 Nc3 Nf6 d3 g6 Bg5 Bg7'),
        ('bdr-third-d4', 'D-pawn two squares', 'e4 c5 Nf3 d6 c3 Nf6 d4 cxd4 cxd4 Nxe4 Bd3 Nf6 O-O g6')],
  why='White holds the d-pawn back. Knight out, g-pawn, bishop: the same order.', outcome='Equal')
L('bdr-bowdler', 'bdr-second', 'The bishop out on move two', 'The same setup, one move earlier', 'core',
  'e4 c5 Bc4 d6 Nc3 Nf6 d3 g6',
  alts=[('bdr-bowdler-nf3', 'King\'s knight out', 'e4 c5 Bc4 d6 Nf3 Nf6'),
        ('bdr-bowdler-nf3v2', 'King\'s knight out on move 4', 'e4 c5 Bc4 d6 Nc3 Nf6 Nf3 Nc6'),
        ('bdr-bowdler-d3', 'Small d-pawn move', 'e4 c5 Bc4 d6 d3 Nf6 Nf3 Nc6'),
        ('bdr-bowdler-d4', 'D-pawn two squares', 'e4 c5 Bc4 d6 d4 cxd4 Qxd4 Nc6'),
        ('bdr-bowdler-qf3', 'Queen comes out', 'e4 c5 Bc4 d6 Qf3 Nf6 Nc3 g6'),
        ('bdr-bowdler-c3', 'Small c-pawn move', 'e4 c5 Bc4 d6 c3 Nf6 d3 g6'),
        ('bdr-bowdler-d3bg5', 'Small d-pawn move, then bishop comes at the knight', 'e4 c5 Bc4 d6 d3 Nf6 Bg5 g6'),
        ('bdr-bowdler-d3nc3', 'Small d-pawn move, then queen\'s knight out', 'e4 c5 Bc4 d6 d3 Nf6 Nc3 g6'),
        ('bdr-bowdler-d3h3', 'Small d-pawn move, then small h-pawn move', 'e4 c5 Bc4 d6 d3 Nf6 h3 g6'),
        ('bdr-bowdler-a3', 'Small a-pawn move', 'e4 c5 Bc4 d6 a3 Nf6 d3 g6'),
        ('bdr-bowdler-qf3nh3', 'Queen comes out, then king\'s knight to the edge', 'e4 c5 Bc4 d6 Qf3 Nf6 Nh3 g6 Ng5 e6'),
        ('bdr-bowdler-qf3d3', 'Queen comes out, then small d-pawn move', 'e4 c5 Bc4 d6 Qf3 Nf6 d3 g6 Bg5 Bg7 Nc3 O-O'),
        ('bdr-bowdler-qf3h3', 'Queen comes out, then small h-pawn move', 'e4 c5 Bc4 d6 Qf3 Nf6 h3 g6 d3 Bg7'),
        ('bdr-bowdler-qh5', 'Queen comes out on move 3', 'e4 c5 Bc4 d6 Qh5 g6 Qf3 Nf6 d3 Bg7 Bg5 O-O'),
        ('bdr-bowdler-qf3d3h3', 'Queen comes out, then small d-pawn move, then small h-pawn move', 'e4 c5 Bc4 d6 Qf3 Nf6 d3 g6 h3 Bg7')],
  why='The most common second move at club level after the knight. Nothing changes for you.', outcome='Comfortable')
L('bdr-closed', 'bdr-second', 'The Closed Sicilian', 'White keeps the middle shut; the same setup', 'common',
  'e4 c5 Nc3 d6 g3 Nf6 Bg2 g6',
  alts=[('bdr-closed-nf3', 'King\'s knight out', 'e4 c5 Nc3 d6 Nf3 Nf6'),
        ('bdr-closed-bc4', 'Bishop aims at f7', 'e4 c5 Nc3 d6 Bc4 Nf6'),
        ('bdr-closed-d3', 'Small d-pawn move', 'e4 c5 Nc3 d6 d3 Nf6'),
        ('bdr-closed-d4', 'D-pawn two squares', 'e4 c5 Nc3 d6 d4 cxd4 Qxd4 Nc6'),
        ('bdr-closed-bb5', 'Bishop gives check', 'e4 c5 Nc3 d6 Bb5+ Bd7 Bxd7+ Qxd7'),
        ('bdr-closed-f4', 'F-pawn two squares', 'e4 c5 Nc3 d6 f4 Nf6 Nf3 g6 Bc4 Bg7')],
  why='One in eight brings the queen\'s knight out and keeps the d-pawn home. Your setup is the same, move for move.', outcome='Equal')
L('bdr-alapin', 'bdr-second', 'The Alapin: the small c-pawn', 'White builds a center; your bishop aims at it', 'common',
  'e4 c5 c3 Nf6 e5 Nd5 Bc4 Nb6',
  alts=[('bdr-alapin-d4', 'D-pawn two squares', 'e4 c5 c3 Nf6 e5 Nd5 d4 cxd4'),
        ('bdr-alapin-f3', 'Small f-pawn move', 'e4 c5 c3 Nf6 f3 e5'),
        ('bdr-alapin-d4v2', 'D-pawn two squares on move 3', 'e4 c5 c3 Nf6 d4 Nxe4'),
        ('bdr-alapin-bd3', 'Bishop to the middle', 'e4 c5 c3 Nf6 Bd3 Nc6'),
        ('bdr-alapin-d3', 'Small d-pawn move', 'e4 c5 c3 Nf6 d3 d6 h3 g6'),
        ('bdr-alapin-qf3', 'Queen comes out', 'e4 c5 c3 Nf6 Qf3 Nc6')],
  why='White wants two pawns in the middle. Let them come, trade one off, and aim the bishop at the other.', outcome='A full game')
L('bdr-morra', 'bdr-second', 'The d-pawn on move two', 'Take it; then the setup', 'common',
  'e4 c5 d4 cxd4 Qxd4 Nc6 Qd1 d6 Bb5 Nf6 Nc3 g6',
  alts=[('bdr-morra-nf3', 'Morphy Gambit', 'e4 c5 d4 cxd4 Nf3 d6'),
        ('bdr-morra-nf3v2', 'King\'s knight out', 'e4 c5 d4 cxd4 Qxd4 Nc6 Qd1 d6 Nf3 Nf6'),
        ('bdr-morra-c3', 'Smith-Morra Gambit', 'e4 c5 d4 cxd4 c3 Nf6 e5 Nd5 cxd4 d6'),
        ('bdr-morra-c3cxd4', 'Smith-Morra Gambit, then pawn takes the pawn', 'e4 c5 d4 cxd4 c3 Nf6 cxd4 Nxe4'),
        ('bdr-morra-qd3', 'Queen steps back', 'e4 c5 d4 cxd4 Qxd4 Nc6 Qd3 d6'),
        ('bdr-morra-qe3bb5', 'Queen steps back, then bishop pins the knight', 'e4 c5 d4 cxd4 Qxd4 Nc6 Qe3 d6 Bb5 Nf6'),
        ('bdr-morra-qc3', 'Queen steps back on move 4', 'e4 c5 d4 cxd4 Qxd4 Nc6 Qc3 Nf6'),
        ('bdr-morra-qe3nc3', 'Queen steps back, then queen\'s knight out', 'e4 c5 d4 cxd4 Qxd4 Nc6 Qe3 d6 Nc3 Nf6'),
        ('bdr-morra-qa4', 'Queen moves', 'e4 c5 d4 cxd4 Qxd4 Nc6 Qa4 d6 Bb5 Nf6 Bxc6+ bxc6 Qxc6+ Bd7'),
        ('bdr-morra-c3qxd4', 'Smith-Morra Gambit, then queen takes the pawn', 'e4 c5 d4 cxd4 c3 Nf6 Qxd4 Nc6'),
        ('bdr-morra-nc3', 'Queen\'s knight out', 'e4 c5 d4 cxd4 Qxd4 Nc6 Qd1 d6 Nc3 Nf6 Nf3 g6'),
        ('bdr-morra-c3e5', 'Smith-Morra Gambit, then small e-pawn move', 'e4 c5 d4 cxd4 c3 Nf6 e5 Nd5 Qxd4 e6')],
  why='One in ten pushes the d-pawn at once. Take it, and whatever White takes back with, the setup comes out.', outcome='Equal or better')
L('bdr-f4', 'bdr-second', 'The f-pawn on move two', 'The same setup against the Grand Prix', 'rare',
  'e4 c5 f4 d6 Nf3 Nf6 Nc3 g6',
  alts=[('bdr-f4-bc4', 'Bishop aims at f7', 'e4 c5 f4 d6 Bc4 Nf6'),
        ('bdr-f4-bc4v2', 'Bishop aims at f7 on move 4', 'e4 c5 f4 d6 Nf3 Nf6 Bc4 Nxe4 O-O Nf6'),
        ('bdr-f4-d3', 'Small d-pawn move', 'e4 c5 f4 d6 Nf3 Nf6 d3 g6 Be2 Bg7'),
        ('bdr-f4-e5', 'Small e-pawn move', 'e4 c5 f4 d6 Nf3 Nf6 e5 dxe5 fxe5 Nd5 Bc4 Nc6')],
  why='White plans a pawn storm. Your bishop on the long diagonal and an early castle take the sting out of it.', outcome='Equal')
L('bdr-second', 'bdr-second', 'Other second moves', 'The quiet d-pawn, the early queen, the second c-pawn', 'rare',
  'e4 c5 d3 d6 Nf3 Nf6 Be2 g6',
  alts=[('bdr-second-qh5', 'Queen comes out', 'e4 c5 Qh5 d6 Bc4 g6'),
        ('bdr-second-e5', 'Small e-pawn move', 'e4 c5 e5 d6 exd6 exd6'),
        ('bdr-second-nc3', 'Queen\'s knight out', 'e4 c5 d3 d6 Nc3 Nf6'),
        ('bdr-second-e5nf3', 'Small e-pawn move, then king\'s knight out', 'e4 c5 e5 d6 Nf3 g6'),
        ('bdr-second-c4', 'Staunton-Cochrane Variation', 'e4 c5 c4 d6 Nc3 Nf6 d3 g6'),
        ('bdr-second-c4nc3', 'Staunton-Cochrane Variation, then queen\'s knight out', 'e4 c5 c4 d6 Nc3 Nf6 Nf3 Nc6'),
        ('bdr-second-be3', 'Bishop behind the center pawns', 'e4 c5 d3 d6 Be3 Nf6'),
        ('bdr-second-f4', 'F-pawn two squares', 'e4 c5 d3 d6 f4 Nf6'),
        ('bdr-second-h3', 'Small h-pawn move', 'e4 c5 d3 d6 h3 Nf6'),
        ('bdr-second-c4nf3', 'Staunton-Cochrane Variation, then king\'s knight out', 'e4 c5 c4 d6 Nf3 Nf6 Nc3 Nc6'),
        ('bdr-second-c3', 'Small c-pawn move', 'e4 c5 d3 d6 c3 Nf6'),
        ('bdr-second-e5f4', 'Small e-pawn move, then f-pawn two squares', 'e4 c5 e5 d6 f4 g6'),
        ('bdr-second-be2', 'Bishop to the quiet square', 'e4 c5 d3 d6 Be2 Nf6'),
        ('bdr-second-c4d3', 'Staunton-Cochrane Variation, then small d-pawn move', 'e4 c5 c4 d6 d3 Nf6 Nc3 g6')],
  why='Whatever White tries on move two, the answer starts the same way: d-pawn, knight, g-pawn, bishop.', outcome='Equal or better')

# ============================================================== notes
n('e4 c5 Nf3 d6', 'D-pawn one square', 'The first move of the setup. It keeps White\'s e-pawn from pushing at your knight and opens the way for the bishop.', ['key'])
n('e4 c5 Nf3 d6 d4 cxd4', 'Take the d-pawn', 'A wing pawn for a center pawn. The file it leaves half open belongs to your rook later.', ['key'])
n('e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6', 'Knight hits the e-pawn', 'White has to guard it, and nearly always does it with the knight.', ['key'], arrows=['f6e4r'])
n('e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 g6', 'The Dragon', 'The g-pawn makes room for the bishop. From the long diagonal it looks across the whole board at White\'s queenside.', ['key'], arrows=['f8g7g'])
n('e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 g6 Be3 Bg7', 'Bishop to the long diagonal', 'Bishop first, then castle. Your knight waits: jumping at White\'s bishop a move earlier would run into a bishop check.', ['key'])
n('e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 g6 Be3 Bg7 f3', 'F-pawn one square', 'It takes the jumping square from your knight. White means to castle long and push the edge pawn at your king.')
n('e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 g6 Be3 Bg7 f3 O-O', 'Castle', 'King safe before the race starts.', ['key'])
n('e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 g6 Be3 Bg7 f3 O-O Qd2 Nc6', 'Queen\'s knight out', 'A second piece on White\'s knight in the middle.')
n('e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 g6 Be3 Bg7 f3 O-O Qd2 Nc6 Bc4 Bd7', 'Bishop off the back rank', 'The last piece out, and the rook can now reach the half-open file.', ['key'], arrows=['a8c8g'])
n('e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 g6 Be3 Bg7 f3 O-O Qd2 Nc6 Bc4 Bd7 O-O-O Rc8', 'Rook to the half-open file', 'It looks straight down at White\'s king. The knight goes to the middle next.', ['key'])
n('e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 g6 Be3 Bg7 f3 O-O Qd2 Nc6 Bc4 Bd7 O-O-O Rc8 Bb3 Ne5', 'Knight to the middle', 'From here it can jump in beside White\'s king, and your attack runs down the open file.', ['key'])
n('e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 g6 Be3 Bg7 f3 O-O Qd2 Nc6 Bc4 Bd7 O-O-O Rc8 Bb3 Ne5 h4', 'The edge pawn starts', 'White wants to open the file in front of your king.')
n('e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 g6 Be3 Bg7 f3 O-O Qd2 Nc6 Bc4 Bd7 O-O-O Rc8 Bb3 Ne5 h4 h5', 'Stop the edge pawn', 'One pawn move holds the wing. To open a file now White has to give something up.', ['key'])
n('e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 g6 Be3 Bg7 Bc4 Ng4', 'Knight jumps at the bishop', 'White left the f-pawn at home, so the square is free. The bishop that guards the knight in the middle is hit and has no good place to go.', ['key'])
n('e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 g6 Be2 Bg7', 'Bishop to the long diagonal', 'The same move whatever White plays on move six.', ['key'])
n('e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 g6 Be2 Bg7 O-O O-O', 'Castle', 'The same four moves as always. The queen\'s knight comes next.')
n('e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 g6 Bc4 Bg7', 'Bishop to the long diagonal', 'White\'s bishop aims at f7. Castling covers it, and your bishop is out first.', ['key'])
n('e4 c5 Nf3 d6 d4 cxd4 Qxd4 Nc6', 'Knight hits the queen', 'She has to move again, and you have a piece out for free.', ['key'], arrows=['c6d4r'])
n('e4 c5 Nf3 d6 Bb5+ Bd7', 'Block with the bishop', 'If White trades, your queen takes back and the setup goes on.', ['key'])
n('e4 c5 Nf3 d6 Bb5+ Bd7 Bxd7+ Qxd7', 'Queen takes back', 'The queen\'s knight keeps its best square. Next: knight, g-pawn, bishop.')
n('e4 c5 Nf3 d6 Bc4 Nf6', 'Knight hits the e-pawn', 'The bishop aims at f7, and your e-pawn can shut it out whenever it has to.', ['key'])
n('e4 c5 Nf3 d6 Bc4 Nf6 Ng5 e6', 'E-pawn shuts the bishop out', 'F7 is covered, and the knight has nothing to do out there.', ['key'])
n('e4 c5 Nf3 d6 Bc4 Nf6 O-O Nxe4', 'Take the e-pawn', 'Nothing guards it. When the rook comes at the knight, it steps back.', ['key'])
n('e4 c5 Nf3 d6 c3 Nf6', 'Knight hits the e-pawn', 'White\'s knight can no longer guard it from its usual square: a pawn is standing there.', ['key'])
n('e4 c5 Bc4 d6', 'D-pawn one square', 'The same first move. The bishop came out early, and your e-pawn can block it when it has to.')
n('e4 c5 Qh5 d6 Bc4 g6', 'G-pawn hits the queen', 'Queen and bishop were both aimed at f7. The g-pawn shuts her line and hits her, and it is a move of your setup anyway.', ['key'])
n('e4 c5 c3 Nf6', 'Knight hits the e-pawn', 'White\'s knight can\'t guard it from its usual square: the c-pawn is standing there.', ['key'], arrows=['f6e4r'])
n('e4 c5 c3 Nf6 e5 Nd5', 'Knight to the middle', 'It can\'t be chased for long, and White\'s pawn has run ahead of its helpers.', ['key'])
n('e4 c5 c3 Nf6 e5 Nd5 d4 cxd4', 'Take the d-pawn', 'One of White\'s two center pawns comes off. Your d-pawn hits the other next.')
n('e4 c5 c3 Nf6 d4 Nxe4', 'Take the e-pawn', 'White left it without a guard. A clean pawn.', ['key'])
n('e4 c5 Nc3 d6', 'D-pawn one square', 'The setup starts the same way whatever White does on move two.')
n('e4 c5 f4 d6', 'D-pawn one square', 'The same first move. Your bishop on the long diagonal and an early castle meet the pawn storm.')
# the other side's moves that start a named line
n('e4 c5 c4', 'Staunton-Cochrane Variation')
n('e4 c5 d4', 'Smith-Morra Gambit')
n('e4 c5 f4', 'McDonnell Attack')
n('e4 c5 Nf3 d6 Bb5+', 'Moscow Variation')
n('e4 c5 Nf3 d6 d4', 'Sicilian Defense')
n('e4 c5 d4 cxd4 Nf3', 'Morphy Gambit')
n('e4 c5 d4 cxd4 c3', 'Smith-Morra Gambit')
n('e4 c5 Nf3 d6 d4 cxd4 Qxd4', 'Chekhover Variation')
n('e4 c5 Nf3 d6 Bc4 Nf6 Nc3 Nc6 d4 cxd4 Nxd4', 'Sozin Attack')
n('e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 g6 Be3 Bg7 f3 O-O Qd2 Nc6 Bc4 Bd7 O-O-O', 'Yugoslav Attack')
