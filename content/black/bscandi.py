"""Black against the e-pawn, another system: the Scandinavian. D-pawn two squares on move one, the queen takes back
and steps to the side, then one setup: knight, c-pawn one square, light bishop out, e-pawn one square. A separate pack
(see PACKS in bmeta.py). The lines were drafted with pipeline/draft.py: White's moves by the Maia 1300/1500 odds, yours
from the setup's order wherever Stockfish 17.1 accepts it and the engine's move elsewhere. SAN is internal only; notes
are plain English."""
from bcontent import L, P, J, n

P('bsc-queen', 'scandi', 'The queen to the side', 'Main Line', 'White takes, your queen takes back, and when the knight hits her she steps to the side. Then one setup: knight, c-pawn, bishop, e-pawn.')
P('bsc-third', 'scandi', 'White skips the knight', 'Third-move tries', 'No knight hits the queen yet. Carry on with the setup; against the d-pawn at once, your e-pawn strikes.')
P('bsc-push', 'scandi', 'White pushes past', 'Advance', 'The e-pawn steps past your d-pawn. Bishop out, e-pawn one square, then the c-pawn hits the chain.')
P('bsc-second', 'scandi', "White doesn't take", 'Second-move tries', 'A gambit knight, a guarding knight, a slow pawn. Take the e-pawn whenever it is offered.')

L('bsc-main', 'bsc-queen', 'The Main Line: one setup', 'Knight, c-pawn one square, bishop out, then the e-pawn', 'core',
  'e4 d5 exd5 Qxd5 Nc3 Qa5 d4 Nf6 Bd2 c6 Nf3 Bf5 Bc4 e6',
  alts=[('bsc-main-nf3', 'King\'s knight out', 'e4 d5 exd5 Qxd5 Nc3 Qa5 d4 Nf6 Nf3 c6 Bd2 Bf5'),
        ('bsc-main-ne4', 'Knight jumps forward', 'e4 d5 exd5 Qxd5 Nc3 Qa5 d4 Nf6 Bd2 c6 Ne4 Qd8 Nxf6+ exf6 Nf3 Bf5'),
        ('bsc-main-bd3', 'Bishop to the middle', 'e4 d5 exd5 Qxd5 Nc3 Qa5 d4 Nf6 Bd2 c6 Nf3 Bf5 Bd3 Bxd3 cxd3 e6'),
        ('bsc-main-be2', 'Bishop to the quiet square', 'e4 d5 exd5 Qxd5 Nc3 Qa5 d4 Nf6 Bd2 c6 Nf3 Bf5 Be2 e6'),
        ('bsc-main-nf3bc4', 'King\'s knight out, then bishop aims at f7', 'e4 d5 exd5 Qxd5 Nc3 Qa5 d4 Nf6 Nf3 c6 Bc4 Bf5 O-O e6'),
        ('bsc-main-nf3bd3', 'King\'s knight out, then bishop to the middle', 'e4 d5 exd5 Qxd5 Nc3 Qa5 d4 Nf6 Nf3 c6 Bd3 Bf5 O-O Bxd3 Qxd3 e6'),
        ('bsc-main-nf3bd3bxf5', 'King\'s knight out, then bishop to the middle, then bishop takes the bishop', 'e4 d5 exd5 Qxd5 Nc3 Qa5 d4 Nf6 Nf3 c6 Bd3 Bf5 Bxf5 Qxf5'),
        ('bsc-main-nf3bc4bd2', 'King\'s knight out, then bishop aims at f7, then bishop beside the queen', 'e4 d5 exd5 Qxd5 Nc3 Qa5 d4 Nf6 Nf3 c6 Bc4 Bf5 Bd2 e6'),
        ('bsc-main-nf3bd3bd2', 'King\'s knight out, then bishop to the middle, then bishop beside the queen', 'e4 d5 exd5 Qxd5 Nc3 Qa5 d4 Nf6 Nf3 c6 Bd3 Bf5 Bd2 Bxd3')],
  why='A quarter of club players put the d-pawn in the middle on move four. Your setup comes out in the same order every game.', outcome='Solid, with every piece out')
L('bsc-nf3', 'bsc-queen', 'White develops first', 'The same four moves, whatever White does', 'core',
  'e4 d5 exd5 Qxd5 Nc3 Qa5 Nf3 Nf6 d3 c6 Bd2 Bf5 Ne4 Qb6',
  alts=[('bsc-nf3-d4', 'D-pawn two squares', 'e4 d5 exd5 Qxd5 Nc3 Qa5 Nf3 Nf6 d4 c6'),
        ('bsc-nf3-bc4', 'Bishop aims at f7', 'e4 d5 exd5 Qxd5 Nc3 Qa5 Nf3 Nf6 Bc4 c6 O-O Bf5 d3 e6'),
        ('bsc-nf3-be2', 'Bishop to the quiet square', 'e4 d5 exd5 Qxd5 Nc3 Qa5 Nf3 Nf6 d3 c6 Bd2 Bf5 Be2 e6'),
        ('bsc-nf3-be2oo', 'Bishop to the quiet square, then castles', 'e4 d5 exd5 Qxd5 Nc3 Qa5 Nf3 Nf6 Be2 c6 O-O Bf5 d3 e6'),
        ('bsc-nf3-bc4d4', 'Bishop aims at f7, then d-pawn two squares', 'e4 d5 exd5 Qxd5 Nc3 Qa5 Nf3 Nf6 Bc4 c6 d4 Bf5'),
        ('bsc-nf3-bc4oo', 'Bishop aims at f7, then castles', 'e4 d5 exd5 Qxd5 Nc3 Qa5 Nf3 Nf6 Bc4 c6 O-O Bf5 Re1 e6'),
        ('bsc-nf3-be2v2', 'Bishop to the quiet square on move 6', 'e4 d5 exd5 Qxd5 Nc3 Qa5 Nf3 Nf6 d3 c6 Be2 Bf5'),
        ('bsc-nf3-bc4ood4', 'Bishop aims at f7, then castles, then d-pawn two squares', 'e4 d5 exd5 Qxd5 Nc3 Qa5 Nf3 Nf6 Bc4 c6 O-O Bf5 d4 e6'),
        ('bsc-nf3-be2ood4', 'Bishop to the quiet square, then castles, then d-pawn two squares', 'e4 d5 exd5 Qxd5 Nc3 Qa5 Nf3 Nf6 Be2 c6 O-O Bf5 d4 e6'),
        ('bsc-nf3-bc4d3', 'Bishop aims at f7, then small d-pawn move', 'e4 d5 exd5 Qxd5 Nc3 Qa5 Nf3 Nf6 Bc4 c6 d3 Bf5 Bd2 e6'),
        ('bsc-nf3-bc4d3oo', 'Bishop aims at f7, then small d-pawn move, then castles', 'e4 d5 exd5 Qxd5 Nc3 Qa5 Nf3 Nf6 Bc4 c6 d3 Bf5 O-O e6'),
        ('bsc-nf3-be2d4', 'Bishop to the quiet square, then d-pawn two squares', 'e4 d5 exd5 Qxd5 Nc3 Qa5 Nf3 Nf6 Be2 c6 d4 Bf5'),
        ('bsc-nf3-be2d3', 'Bishop to the quiet square, then small d-pawn move', 'e4 d5 exd5 Qxd5 Nc3 Qa5 Nf3 Nf6 Be2 c6 d3 Bf5'),
        ('bsc-nf3-bc4oong5', 'Bishop aims at f7, then castles, then knight jumps forward', 'e4 d5 exd5 Qxd5 Nc3 Qa5 Nf3 Nf6 Bc4 c6 O-O Bf5 Ng5 e6'),
        ('bsc-nf3-be2ooa3', 'Bishop to the quiet square, then castles, then small a-pawn move', 'e4 d5 exd5 Qxd5 Nc3 Qa5 Nf3 Nf6 Be2 c6 O-O Bf5 a3 e6'),
        ('bsc-nf3-bc4ng5', 'Bishop aims at f7, then knight jumps forward', 'e4 d5 exd5 Qxd5 Nc3 Qa5 Nf3 Nf6 Bc4 c6 Ng5 Qxg5 d4 Qxg2 Rf1 Bf5'),
        ('bsc-nf3-bc4ng5oo', 'Bishop aims at f7, then knight jumps forward, then castles', 'e4 d5 exd5 Qxd5 Nc3 Qa5 Nf3 Nf6 Bc4 c6 Ng5 Qxg5 O-O Qg4'),
        ('bsc-nf3-bc4ng5d3', 'Bishop aims at f7, then knight jumps forward, then small d-pawn move', 'e4 d5 exd5 Qxd5 Nc3 Qa5 Nf3 Nf6 Bc4 c6 Ng5 Qxg5 d3 Qxg2')],
  why='Four in ten bring the king\'s knight out first. Nothing changes: knight, c-pawn, bishop, e-pawn.', outcome='Solid')
L('bsc-d3', 'bsc-queen', 'The small d-pawn', 'Same setup; watch the knight jump that uncovers the bishop', 'common',
  'e4 d5 exd5 Qxd5 Nc3 Qa5 d3 Nf6 Bd2 c6 Ne4 Qb6 Nxf6+ exf6 Qe2+ Be6',
  alts=[('bsc-d3-nf3', 'King\'s knight out', 'e4 d5 exd5 Qxd5 Nc3 Qa5 d3 Nf6 Bd2 c6 Nf3 Bf5'),
        ('bsc-d3-nf3v2', 'King\'s knight out on move 5', 'e4 d5 exd5 Qxd5 Nc3 Qa5 d3 Nf6 Nf3 c6')],
  why='One in eight plays it slow. The bishop behind the knight is aimed at your queen, so the c-pawn move matters most.', outcome='Equal')
L('bsc-4th', 'bsc-queen', 'Other fourth moves', 'The Italian bishop, the edge pawn, an early check', 'rare',
  'e4 d5 exd5 Qxd5 Nc3 Qa5 Bc4 Nf6 d3 c6 Bd2 Qc7',
  alts=[('bsc-4th-nf3', 'King\'s knight out', 'e4 d5 exd5 Qxd5 Nc3 Qa5 Bc4 Nf6 Nf3 c6'),
        ('bsc-4th-nf3v2', 'King\'s knight out on move 6', 'e4 d5 exd5 Qxd5 Nc3 Qa5 Bc4 Nf6 d3 c6 Nf3 Bf5'),
        ('bsc-4th-qf3', 'Queen comes out', 'e4 d5 exd5 Qxd5 Nc3 Qa5 Bc4 Nf6 Qf3 Nc6 Nge2 Ne5')],
  why='Whatever comes on move four, the knight comes out and the c-pawn gives the queen a way home.', outcome='Equal')
L('bsc-3nf3', 'bsc-third', 'White waits with the knight', 'Knight out, c-pawn; when the knight hits the queen, she goes to the side', 'common',
  'e4 d5 exd5 Qxd5 Nf3 Nf6 c4 Qa5 Nc3 e5',
  alts=[('bsc-3nf3-nc3', 'Queen\'s knight out', 'e4 d5 exd5 Qxd5 Nf3 Nf6 Nc3 Qa5'),
        ('bsc-3nf3-d4', 'D-pawn two squares', 'e4 d5 exd5 Qxd5 Nf3 Nf6 d4 c6 Nc3 Qa5'),
        ('bsc-3nf3-be2', 'Bishop to the quiet square', 'e4 d5 exd5 Qxd5 Nf3 Nf6 Be2 c6 Nc3 Qa5'),
        ('bsc-3nf3-be2oo', 'Bishop to the quiet square, then castles', 'e4 d5 exd5 Qxd5 Nf3 Nf6 Be2 c6 O-O Bf5 Nc3 Qa5'),
        ('bsc-3nf3-d4c4', 'D-pawn two squares, then c-pawn two squares', 'e4 d5 exd5 Qxd5 Nf3 Nf6 d4 c6 c4 Qa5+')],
  why='One in twelve keeps the queen\'s knight home for a move. It usually comes out next, and you are back in the main line.', outcome='Back in the main line')
L('bsc-3rd', 'bsc-third', 'Other third moves', 'The d-pawn at once: hit it with your e-pawn', 'rare',
  'e4 d5 exd5 Qxd5 d4 e5 Nc3 Bb4 Bd2 Qxd4 Nf3 Qc5',
  alts=[('bsc-3rd-nf3', 'King\'s knight out', 'e4 d5 exd5 Qxd5 d4 e5 Nf3 exd4 Nxd4 Nf6 Nc3 Bb4'),
        ('bsc-3rd-nf3v2', 'King\'s knight out on move 5', 'e4 d5 exd5 Qxd5 d4 e5 Nc3 Bb4 Nf3 Nf6'),
        ('bsc-3rd-dxe5', 'Pawn takes the pawn', 'e4 d5 exd5 Qxd5 d4 e5 Nc3 Bb4 dxe5 Qxd1+ Kxd1 Nc6'),
        ('bsc-3rd-nf3qxd4', 'King\'s knight out, then queen takes back', 'e4 d5 exd5 Qxd5 d4 e5 Nf3 exd4 Qxd4 Nf6 Qxd5 Nxd5 Bc4 Nb6'),
        ('bsc-3rd-dxe5nf3', 'Pawn takes the pawn, then king\'s knight out', 'e4 d5 exd5 Qxd5 d4 e5 dxe5 Qxd1+ Kxd1 Nc6 Nf3 Bf5'),
        ('bsc-3rd-c4', 'C-pawn two squares', 'e4 d5 exd5 Qxd5 d4 e5 c4 Qxd4 Qxd4 exd4 Nf3 c5'),
        ('bsc-3rd-be3', 'Bishop behind the center pawns', 'e4 d5 exd5 Qxd5 d4 e5 Be3 Nf6 Nc3 Bb4'),
        ('bsc-3rd-ne2', 'King\'s knight tucked in', 'e4 d5 exd5 Qxd5 d4 e5 Nc3 Bb4 Ne2 Nf6'),
        ('bsc-3rd-c3', 'Small c-pawn move', 'e4 d5 exd5 Qxd5 d4 e5 c3 Nf6 Nf3 Nc6'),
        ('bsc-3rd-dxe5bb5', 'Pawn takes the pawn, then bishop pins the knight', 'e4 d5 exd5 Qxd5 d4 e5 dxe5 Qxd1+ Kxd1 Nc6 Bb5 Bg4+'),
        ('bsc-3rd-dxe5f4', 'Pawn takes the pawn, then f-pawn two squares', 'e4 d5 exd5 Qxd5 d4 e5 dxe5 Qxd1+ Kxd1 Nc6 f4 Bf5')],
  why='With no knight hitting your queen, she stays in the middle and the e-pawn strikes.', outcome='Equal or better')
L('bsc-e5', 'bsc-push', 'The e-pawn pushes past', 'Bishop out, e-pawn, then the c-pawn two squares', 'core',
  'e4 d5 e5 Bf5 d4 e6 Nf3 c5 c3 Nc6 Bd3 Bxd3 Qxd3 Rc8',
  alts=[('bsc-e5-nf3', 'King\'s knight out', 'e4 d5 e5 Bf5 Nf3 e6 d4 c5'),
        ('bsc-e5-bd3', 'Bishop to the middle', 'e4 d5 e5 Bf5 d4 e6 Bd3 Bxd3 Qxd3 c5 Nf3 Nc6'),
        ('bsc-e5-c3', 'Small c-pawn move', 'e4 d5 e5 Bf5 d4 e6 c3 c5 Nf3 Nc6'),
        ('bsc-e5-bb5', 'Bishop pins the knight', 'e4 d5 e5 Bf5 d4 e6 Nf3 c5 c3 Nc6 Bb5 Rc8 O-O a6'),
        ('bsc-e5-bd3c3', 'Bishop to the middle, then small c-pawn move', 'e4 d5 e5 Bf5 d4 e6 Bd3 Bxd3 Qxd3 c5 c3 Nc6 Nf3 Rc8'),
        ('bsc-e5-nc3', 'Queen\'s knight out', 'e4 d5 e5 Bf5 d4 e6 Nc3 c5 Nf3 Nc6 Bb5 Bg4'),
        ('bsc-e5-bd3qb5', 'Bishop to the middle, then queen gives check', 'e4 d5 e5 Bf5 d4 e6 Bd3 Bxd3 Qxd3 c5 Qb5+ Nc6'),
        ('bsc-e5-be3', 'Bishop behind the center pawns', 'e4 d5 e5 Bf5 d4 e6 Nf3 c5 c3 Nc6 Be3 Qb6'),
        ('bsc-e5-bd3dxc5', 'Bishop to the middle, then pawn takes the pawn', 'e4 d5 e5 Bf5 d4 e6 Bd3 Bxd3 Qxd3 c5 dxc5 Nc6'),
        ('bsc-e5-f4', 'F-pawn two squares', 'e4 d5 e5 Bf5 f4 e6 d4 c5'),
        ('bsc-e5-nc3be3', 'Queen\'s knight out, then bishop behind the center pawns', 'e4 d5 e5 Bf5 d4 e6 Nc3 c5 Be3 Nc6'),
        ('bsc-e5-bb5oo', 'Bishop gives check, then castles', 'e4 d5 e5 Bf5 d4 e6 Nf3 c5 Bb5+ Nc6 O-O Bg4'),
        ('bsc-e5-a3', 'Small a-pawn move', 'e4 d5 e5 Bf5 d4 e6 a3 c5 Nf3 Nc6'),
        ('bsc-e5-nc3dxc5', 'Queen\'s knight out, then pawn takes the pawn', 'e4 d5 e5 Bf5 d4 e6 Nc3 c5 dxc5 Nc6'),
        ('bsc-e5-bb5bxc6', 'Bishop pins the knight, then bishop takes the knight with check', 'e4 d5 e5 Bf5 d4 e6 Nf3 c5 c3 Nc6 Bb5 Rc8 Bxc6+ Rxc6'),
        ('bsc-e5-f4c3', 'F-pawn two squares, then small c-pawn move', 'e4 d5 e5 Bf5 d4 e6 f4 c5 c3 Nc6 Nf3 Qb6'),
        ('bsc-e5-nf3nc3', 'King\'s knight out, then queen\'s knight out', 'e4 d5 e5 Bf5 Nf3 e6 Nc3 c5'),
        ('bsc-e5-f4nf3', 'F-pawn two squares, then king\'s knight out', 'e4 d5 e5 Bf5 f4 e6 Nf3 c5 d4 Nc6'),
        ('bsc-e5-bb5qa4', 'Bishop pins the knight, then queen comes out', 'e4 d5 e5 Bf5 d4 e6 Nf3 c5 c3 Nc6 Bb5 Rc8 Qa4 a6'),
        ('bsc-e5-nc3nf3', 'Queen\'s knight out, then king\'s knight out', 'e4 d5 e5 Bf5 d4 e6 Nc3 c5 Nf3 Nc6 Be3 Bg4'),
        ('bsc-e5-a3c3', 'Small a-pawn move, then small c-pawn move', 'e4 d5 e5 Bf5 d4 e6 a3 c5 c3 Nc6 Nf3 Bg4'),
        ('bsc-e5-nc3bb5', 'Queen\'s knight out, then bishop gives check', 'e4 d5 e5 Bf5 d4 e6 Nc3 c5 Bb5+ Nc6 Nf3 Bg4'),
        ('bsc-e5-f4nf3v2', 'F-pawn two squares, then king\'s knight out on move 4', 'e4 d5 e5 Bf5 d4 e6 f4 c5 Nf3 Nc6 c3 Qb6'),
        ('bsc-e5-c3bb5', 'Small c-pawn move, then bishop gives check', 'e4 d5 e5 Bf5 d4 e6 c3 c5 Bb5+ Nc6'),
        ('bsc-e5-bb5bxc6v2', 'Bishop gives check, then bishop takes the knight with check', 'e4 d5 e5 Bf5 d4 e6 Nf3 c5 Bb5+ Nc6 Bxc6+ bxc6 O-O Qb6'),
        ('bsc-e5-f4nf3bb5', 'F-pawn two squares, then king\'s knight out, then bishop gives check', 'e4 d5 e5 Bf5 f4 e6 Nf3 c5 Bb5+ Nc6')],
  why='Almost one in five won\'t take. Your bishop gets out before the e-pawn moves, and then the c-pawn hits the chain.', outcome='Comfortable')
L('bsc-tennison', 'bsc-second', 'The Tennison Gambit', 'Take the pawn; when the knight jumps, the bishop guards it', 'rare',
  'e4 d5 Nf3 dxe4 Ng5 Bf5 d3 exd3 Bxd3 Bxd3 Qxd3 Qxd3 cxd3 Nf6',
  alts=[('bsc-tennison-cxd3', 'Pawn takes back', 'e4 d5 Nf3 dxe4 Ng5 Bf5 d3 exd3 Bxd3 Bxd3 cxd3 Nf6'),
        ('bsc-tennison-g4', 'G-pawn two squares', 'e4 d5 Nf3 dxe4 Ng5 Bf5 g4 Bg6'),
        ('bsc-tennison-ne5', 'Knight jumps forward', 'e4 d5 Nf3 dxe4 Ne5 Nf6 Bc4 e6'),
        ('bsc-tennison-nc3', 'Queen\'s knight out', 'e4 d5 Nf3 dxe4 Ng5 Bf5 Nc3 Nf6 Qe2 Nc6'),
        ('bsc-tennison-cxd3v2', 'Pawn takes back on move 5', 'e4 d5 Nf3 dxe4 Ng5 Bf5 d3 exd3 cxd3 Nf6'),
        ('bsc-tennison-ng1', 'Knight steps back', 'e4 d5 Nf3 dxe4 Ng1 Nf6 Nc3 Bf5'),
        ('bsc-tennison-bc4', 'Bishop aims at f7', 'e4 d5 Nf3 dxe4 Ng5 Bf5 Bc4 e6 Nc3 Qxg5'),
        ('bsc-tennison-nd4', 'Knight jumps forward on move 3', 'e4 d5 Nf3 dxe4 Nd4 Qxd4'),
        ('bsc-tennison-nc3bc4', 'Queen\'s knight out, then bishop aims at f7', 'e4 d5 Nf3 dxe4 Ng5 Bf5 Nc3 Nf6 Bc4 e6 O-O h6'),
        ('bsc-tennison-nc3d3', 'Queen\'s knight out, then small d-pawn move', 'e4 d5 Nf3 dxe4 Ng5 Bf5 Nc3 Nf6 d3 exd3 Bxd3 Bxd3'),
        ('bsc-tennison-nh4', 'Knight jumps forward on move 3 (2)', 'e4 d5 Nf3 dxe4 Nh4 g5'),
        ('bsc-tennison-ne5d3', 'Knight jumps forward, then small d-pawn move', 'e4 d5 Nf3 dxe4 Ne5 Nf6 d3 Nbd7'),
        ('bsc-tennison-ne5nc3', 'Knight jumps forward, then queen\'s knight out', 'e4 d5 Nf3 dxe4 Ne5 Nf6 Nc3 Nbd7'),
        ('bsc-tennison-bc4oo', 'Bishop aims at f7, then castles', 'e4 d5 Nf3 dxe4 Ng5 Bf5 Bc4 e6 O-O Qxg5 d3 Qd8'),
        ('bsc-tennison-ng1d3', 'Knight steps back, then small d-pawn move', 'e4 d5 Nf3 dxe4 Ng1 Nf6 d3 Bf5'),
        ('bsc-tennison-bc4d3', 'Bishop aims at f7, then small d-pawn move', 'e4 d5 Nf3 dxe4 Ng5 Bf5 Bc4 e6 d3 Nf6 Nc3 Bb4')],
  why='One in twenty gives the e-pawn away. Take it and bring the bishop out behind it.', outcome='A pawn up')
L('bsc-nc3', 'bsc-second', 'Knight guards the e-pawn', 'Take, then the bishop out at the knight', 'rare',
  'e4 d5 Nc3 dxe4 Nxe4 Bf5 Qf3 e6',
  alts=[('bsc-nc3-ng3', 'Knight steps back', 'e4 d5 Nc3 dxe4 Nxe4 Bf5 Ng3 Bg6 d3 Nf6'),
        ('bsc-nc3-bd3', 'Bishop to the middle', 'e4 d5 Nc3 dxe4 Nxe4 Bf5 Bd3 e6 Nf3 Nf6'),
        ('bsc-nc3-nc3', 'Knight steps back on move 4', 'e4 d5 Nc3 dxe4 Nxe4 Bf5 Nc3 Nf6 Nf3 c6'),
        ('bsc-nc3-ng3nf3', 'Knight steps back, then king\'s knight out', 'e4 d5 Nc3 dxe4 Nxe4 Bf5 Ng3 Bg6 Nf3 Nf6 Bc4 e6'),
        ('bsc-nc3-d3', 'Small d-pawn move', 'e4 d5 Nc3 dxe4 Nxe4 Bf5 d3 Nf6 Nxf6+ exf6 Nf3 Be7'),
        ('bsc-nc3-ng3bc4', 'Knight steps back, then bishop aims at f7', 'e4 d5 Nc3 dxe4 Nxe4 Bf5 Ng3 Bg6 Bc4 Nf6'),
        ('bsc-nc3-ng3d4', 'Knight steps back, then d-pawn two squares', 'e4 d5 Nc3 dxe4 Nxe4 Bf5 Ng3 Bg6 d4 Nf6')],
  why='Take the pawn, and when the knight takes back your bishop comes out with a hit on it.', outcome='Equal')
L('bsc-2nd', 'bsc-second', 'Other second moves', 'Take the e-pawn when you can', 'rare',
  'e4 d5 d3 dxe4 dxe4 Qxd1+ Kxd1 Nf6 Nc3 c6',
  alts=[('bsc-2nd-f3', 'Small f-pawn move', 'e4 d5 d3 dxe4 dxe4 Qxd1+ Kxd1 Nf6 f3 e6'),
        ('bsc-2nd-f3d3', 'Small f-pawn move, then small d-pawn move', 'e4 d5 f3 dxe4 fxe4 Nf6 d3 e5'),
        ('bsc-2nd-bd3', 'Bishop to the middle', 'e4 d5 d3 dxe4 dxe4 Qxd1+ Kxd1 Nf6 Bd3 c6'),
        ('bsc-2nd-f3e5', 'Small f-pawn move, then small e-pawn move', 'e4 d5 f3 dxe4 fxe4 Nf6 e5 Nd5'),
        ('bsc-2nd-d4', 'Blackmar-Diemer Gambit', 'e4 d5 d4 dxe4 Nc3 Nf6 Bg5 Bf5 Bxf6 exf6'),
        ('bsc-2nd-nc3', 'Dunst-Perrenet Gambit', 'e4 d5 d3 dxe4 Nc3 Nf6 dxe4 Qxd1+'),
        ('bsc-2nd-d4nc3', 'Blackmar-Diemer Gambit, then queen\'s knight out', 'e4 d5 d4 dxe4 Nc3 Nf6 f3 Bf5 fxe4 Nxe4 Nxe4 Bxe4'),
        ('bsc-2nd-f3nc3', 'Small f-pawn move, then queen\'s knight out', 'e4 d5 f3 dxe4 fxe4 Nf6 Nc3 e5 Nf3 Bc5 Bc4 O-O'),
        ('bsc-2nd-e5', 'Small e-pawn move', 'e4 d5 d3 dxe4 dxe4 Qxd1+ Kxd1 Nf6 e5 Ng4'),
        ('bsc-2nd-d4v2', 'Small d-pawn move', 'e4 d5 d3 dxe4 d4 Nf6 Nc3 c6'),
        ('bsc-2nd-nc3bg5', 'Dunst-Perrenet Gambit, then Myers Gambit', 'e4 d5 d3 dxe4 Nc3 Nf6 Bg5 h6'),
        ('bsc-2nd-d4f3', 'Blackmar-Diemer Gambit, then Blackmar Gambit', 'e4 d5 d4 dxe4 f3 e5 fxe4 Qh4+'),
        ('bsc-2nd-d4nc3f3', 'Blackmar-Diemer Gambit, then queen\'s knight out, then small f-pawn move', 'e4 d5 d4 dxe4 Nc3 Nf6 f3 Bf5 g4 Bg6')],
  why='The small d-pawn, the f-pawn, the d-pawn gambit. Take the e-pawn each time.', outcome='Equal or better')

# ============================================================== notes
n('e4 d5', 'Scandinavian Defense', 'Hit the e-pawn on move one. White nearly always takes, and your queen comes out to take back.', ['key'], arrows=['d5e4g'])
n('e4 d5 exd5', 'White takes', 'Two in three take the pawn.')
n('e4 d5 exd5 Qxd5', 'Queen takes back', 'She stands in the middle for one move. When the knight hits her, she steps to the side.', ['key'])
n('e4 d5 exd5 Qxd5 Nc3', 'Knight hits your queen', 'Eight in ten play this. The queen has to move, and she has a good square.')
n('e4 d5 exd5 Qxd5 Nc3 Qa5', 'Queen to the side', 'Nothing can hit her here yet. Next comes the setup, in the same order every game: knight, c-pawn, bishop, e-pawn.', ['key'], arrows=['g8f6g', 'c7c6g'])
n('e4 d5 exd5 Qxd5 Nc3 Qa5 d4 Nf6', 'Knight out', 'The first move of the setup, every game.')
n('e4 d5 exd5 Qxd5 Nc3 Qa5 d4 Nf6 Bd2', 'Bishop beside the queen', 'It lines up on your queen from behind the knight. When the knight jumps, the bishop hits her.')
n('e4 d5 exd5 Qxd5 Nc3 Qa5 d4 Nf6 Bd2 c6', 'C-pawn one square', 'The queen gets a way home, and White\'s knight loses its best square in the middle. Play it before the bishop comes out.', ['key'], arrows=['a5d8g'])
n('e4 d5 exd5 Qxd5 Nc3 Qa5 d4 Nf6 Bd2 c6 Nf3 Bf5', 'Bishop out', 'Outside the pawns before the e-pawn moves, the same idea as in the Caro-Kann and the Slav.', ['key'])
n('e4 d5 exd5 Qxd5 Nc3 Qa5 d4 Nf6 Bd2 c6 Nf3 Bf5 Bc4 e6', 'E-pawn one square', 'The setup is complete. The queen\'s knight and the dark bishop come next, then castle.')
n('e4 d5 exd5 Qxd5 Nc3 Qa5 d4 Nf6 Bd2 c6 Ne4', 'Knight jumps and uncovers the bishop', 'The bishop now hits your queen. The c-pawn move gave her the way home.')
n('e4 d5 exd5 Qxd5 Nc3 Qa5 d4 Nf6 Bd2 c6 Ne4 Qd8', 'Queen goes home', 'Safe, and the knight in the middle will be traded.', ['key'])
n('e4 d5 exd5 Qxd5 Nc3 Qa5 Nf3 Nf6', 'Knight out', 'The same first move of the setup.')
n('e4 d5 exd5 Qxd5 Nc3 Qa5 Nf3 Nf6 Bc4 c6 Ng5', 'Knight jumps at f7', 'It leaves the knight where your queen can take it.', ['warn'])
n('e4 d5 exd5 Qxd5 Nc3 Qa5 Nf3 Nf6 Bc4 c6 Ng5 Qxg5', 'Take the knight', 'Your queen was looking along the rank the whole time. A clean piece.', ['key', 'trap'], arrows=['a5g5g'])
n('e4 d5 exd5 Qxd5 Nf3 Nf6 Nc3 Qa5', 'Queen to the side', 'The knight came out a move later, and you are in the main line.', ['key'])
n('e4 d5 exd5 Qxd5 d4 e5', 'E-pawn strikes', 'With no knight hitting your queen she holds the middle, and the e-pawn hits White\'s d-pawn at once.', ['key'], arrows=['e5d4g'])
n('e4 d5 e5', 'The e-pawn pushes past', 'White keeps the pawns on the board. Your bishop is free to leave first.')
n('e4 d5 e5 Bf5', 'Bishop out first', 'Before the e-pawn shuts it in. Then the e-pawn one square and the c-pawn two.', ['key'], arrows=['e7e6g', 'c7c5g'])
n('e4 d5 e5 Bf5 d4 e6', 'E-pawn one square', 'The door closes behind the bishop.')
n('e4 d5 e5 Bf5 d4 e6 Nf3 c5', 'C-pawn two squares', 'It hits the pawn that holds White\'s chain together. The queen\'s knight comes behind it.', ['key'], arrows=['c5d4g'])
n('e4 d5 Nf3 dxe4', 'Take the pawn', 'A free center pawn. The knight has to move again.', ['key'])
n('e4 d5 Nf3 dxe4 Ng5 Bf5', 'Bishop guards the pawn', 'Out before the e-pawn moves, and it holds the extra pawn.', ['key'])
n('e4 d5 Nc3 dxe4', 'Take the pawn', 'When the knight takes back, your bishop comes out with a hit on it.')
n('e4 d5 Nc3 dxe4 Nxe4 Bf5', 'Bishop out at the knight', 'It gains a move: the knight has to step away.', ['key'], arrows=['f5e4r'])
n('e4 d5 d3 dxe4', 'Take the pawn', 'If White takes back, the queens come off and White can no longer castle.', ['key'])
n('e4 d5 d3 dxe4 dxe4 Qxd1+', 'Trade queens', 'The king has to take back and stays in the middle for the rest of the game.', ['key'])
# the other side's moves that start a named line
n('e4 d5 Nf3', 'Tennison Gambit')
n('e4 d5 d4', 'Blackmar-Diemer Gambit')
n('e4 d5 d3 dxe4 Nc3', 'Dunst-Perrenet Gambit')
n('e4 d5 d4 dxe4 f3', 'Blackmar Gambit')
n('e4 d5 d3 dxe4 Nc3 Nf6 Bg5', 'Myers Gambit')
n('e4 d5 d4 dxe4 Nc3 Nf6 Bg5', 'von Popiel Gambit')
