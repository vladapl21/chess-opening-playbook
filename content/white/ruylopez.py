"""White after both knights come out, a third way: the Ruy Lopez, a pack for the slot 'whiteItalian' beside the two
Italians (see PACKS in content2_meta.py).

The bishop comes at the knight that guards the e-pawn. When a pawn asks, it steps back, and again to the diagonal at
f7. Then one setup: castle, rook beside the king, c-pawn one square, the small h-pawn move, d-pawn two squares. The
lines were drafted with pipeline/draft.py: Black's moves by the Maia 1300/1500 odds, yours from the setup's order
wherever Stockfish 17.1 accepts it and the engine's move elsewhere. SAN is internal; notes are plain English."""
from content import n, J, L, PARTS

PARTS.extend([
  dict(id='rl-morphy', ch='ruy', title='The a-pawn asks the bishop', kicker='Morphy Defense',
       blurb="Black's a-pawn asks your bishop what it wants, and it steps back; if the b-pawn follows, it steps back again and stands on the diagonal at f7. Then the setup: castle, rook beside the king, c-pawn one square, the small h-pawn move, and the d-pawn two squares."),
  dict(id='rl-third', ch='ruy', title='Black leaves the bishop alone', kicker='Berlin, Steinitz, Classical, Bird',
       blurb='The third moves without the a-pawn. Castle first almost every time; the small d-pawn is met by opening the middle, and the knight that jumps in is taken.'),
])

L('rl-main', 'rl-morphy', 'The Closed Ruy Lopez', 'Castle, rook, bishop back, c-pawn, h-pawn, then the d-pawn', 'core',
  'e4 e5 Nf3 Nc6 Bb5 a6 Ba4 Nf6 O-O Be7 Re1 b5 Bb3 d6 c3 O-O h3 Na5 Bc2',
  alts=[('rl-main-d6', 'Steinitz Deferred', 'e4 e5 Nf3 Nc6 Bb5 a6 Ba4 Nf6 O-O d6 Re1'),
        ('rl-main-bc5', 'Møller Variation', 'e4 e5 Nf3 Nc6 Bb5 a6 Ba4 Nf6 O-O Bc5 Re1 O-O c3'),
        ('rl-main-nxe4', 'Knight takes the pawn', 'e4 e5 Nf3 Nc6 Bb5 a6 Ba4 Nf6 O-O Nxe4 Re1 Nf6 d4'),
        ('rl-main-bc5d6', 'Møller Variation, then small d-pawn move', 'e4 e5 Nf3 Nc6 Bb5 a6 Ba4 Nf6 O-O Bc5 Re1 d6 c3'),
        ('rl-main-b5', 'B-pawn two squares', 'e4 e5 Nf3 Nc6 Bb5 a6 Ba4 Nf6 O-O b5 Bb3 Bc5 Re1'),
        ('rl-main-nxe4d5', 'Knight takes the pawn, then Skipworth Gambit', 'e4 e5 Nf3 Nc6 Bb5 a6 Ba4 Nf6 O-O Nxe4 Re1 d5 Bxc6+ bxc6 d3'),
        ('rl-main-nxe4nc5', 'Knight takes the pawn, then knight steps back', 'e4 e5 Nf3 Nc6 Bb5 a6 Ba4 Nf6 O-O Nxe4 Re1 Nc5 Bxc6'),
        ('rl-main-oo', 'Castles', 'e4 e5 Nf3 Nc6 Bb5 a6 Ba4 Nf6 O-O Be7 Re1 O-O Bxc6 dxc6 Nxe5'),
        ('rl-main-oov2', 'Castles on move 7', 'e4 e5 Nf3 Nc6 Bb5 a6 Ba4 Nf6 O-O Be7 Re1 b5 Bb3 O-O h3'),
        ('rl-main-bb7', 'Flohr System', 'e4 e5 Nf3 Nc6 Bb5 a6 Ba4 Nf6 O-O Be7 Re1 b5 Bb3 d6 c3 O-O h3 Bb7 d4'),
        ('rl-main-nb8', 'Breyer Defense', 'e4 e5 Nf3 Nc6 Bb5 a6 Ba4 Nf6 O-O Be7 Re1 b5 Bb3 d6 c3 O-O h3 Nb8 d4')],
  why='The most famous position in chess. Your bishop has stepped back twice and still looks at f7, the king is safe, and the c-pawn is ready to back the d-pawn up.', outcome='A lasting edge in the middle')
L('rl-b5', 'rl-morphy', 'The pawns chase the bishop', 'Two steps back, and it stands on the diagonal it wanted', 'core',
  'e4 e5 Nf3 Nc6 Bb5 a6 Ba4 b5 Bb3 Nf6 O-O',
  alts=[('rl-b5-d6', 'Small d-pawn move', 'e4 e5 Nf3 Nc6 Bb5 a6 Ba4 b5 Bb3 d6 O-O'),
        ('rl-b5-bc5', 'Graz Variation', 'e4 e5 Nf3 Nc6 Bb5 a6 Ba4 b5 Bb3 Bc5 O-O Nf6 Re1'),
        ('rl-b5-bb7', 'Fianchetto', 'e4 e5 Nf3 Nc6 Bb5 a6 Ba4 b5 Bb3 Bb7 O-O'),
        ('rl-b5-na5', 'Norwegian Variation', 'e4 e5 Nf3 Nc6 Bb5 a6 Ba4 b5 Bb3 Na5 O-O Nxb3 axb3'),
        ('rl-b5-h6', 'Small h-pawn move', 'e4 e5 Nf3 Nc6 Bb5 a6 Ba4 b5 Bb3 h6 O-O Nf6 d4 exd4 e5'),
        ('rl-b5-nd4', 'Knight jumps forward', 'e4 e5 Nf3 Nc6 Bb5 a6 Ba4 b5 Bb3 Nd4 Nxd4 exd4 Bxf7+ Kxf7 Qh5+ g6 Qd5+ Kg7 Qxa8'),
        ('rl-b5-bc5d6', 'Graz Variation, then small d-pawn move', 'e4 e5 Nf3 Nc6 Bb5 a6 Ba4 b5 Bb3 Bc5 O-O d6 Re1')],
  why='Four in ten club players push the second pawn at once. The bishop lands on the diagonal at f7 with nothing lost, and Black\'s pawns are a target for your a-pawn.', outcome='A better Italian')
L('rl-a6', 'rl-morphy', 'After the a-pawn: other tries', 'The bishop out, the small d-pawn', 'common',
  'e4 e5 Nf3 Nc6 Bb5 a6 Ba4 d6 O-O Bd7 Re1',
  alts=[('rl-a6-bc5', 'Classical Defense Deferred', 'e4 e5 Nf3 Nc6 Bb5 a6 Ba4 Bc5 O-O Nf6 Re1'),
        ('rl-a6-bc5d6', 'Classical Defense Deferred, then small d-pawn move', 'e4 e5 Nf3 Nc6 Bb5 a6 Ba4 Bc5 O-O d6 Re1'),
        ('rl-a6-nf6', 'Steinitz Deferred', 'e4 e5 Nf3 Nc6 Bb5 a6 Ba4 d6 O-O Nf6 Re1'),
        ('rl-a6-bg4', 'Bishop pins the knight', 'e4 e5 Nf3 Nc6 Bb5 a6 Ba4 d6 O-O Bg4 c3')],
  why='Black asks the bishop and then develops another way. Castle, and the setup comes out in its order.', outcome='A small edge')
L('rl-berlin', 'rl-third', 'The Berlin: the knight hits your e-pawn', 'Castle anyway; the pawn comes back', 'core',
  'e4 e5 Nf3 Nc6 Bb5 Nf6 O-O Nxe4 Re1 Nd6 Nxe5 Nxe5 Rxe5+ Be7 Bf1',
  alts=[('rl-berlin-a6', 'Small a-pawn move', 'e4 e5 Nf3 Nc6 Bb5 Nf6 O-O a6 Bxc6 bxc6 Nxe5'),
        ('rl-berlin-a6dxc6', 'Small a-pawn move, then pawn takes back', 'e4 e5 Nf3 Nc6 Bb5 Nf6 O-O a6 Bxc6 dxc6 Nxe5 Bd6 Nf3'),
        ('rl-berlin-bc5', 'Beverwijk Variation', 'e4 e5 Nf3 Nc6 Bb5 Nf6 O-O Bc5 c3 d6 d4 exd4 cxd4 Bb6 d5'),
        ('rl-berlin-d6', 'Improved Steinitz Defense', 'e4 e5 Nf3 Nc6 Bb5 Nf6 O-O d6 Re1 Bg4 c3'),
        ('rl-berlin-d5', 'D-pawn two squares', 'e4 e5 Nf3 Nc6 Bb5 Nf6 O-O Nxe4 Re1 d5 d3 Nf6 Nxe5'),
        ('rl-berlin-bc5a6', 'Beverwijk Variation, then small a-pawn move', 'e4 e5 Nf3 Nc6 Bb5 Nf6 O-O Bc5 c3 a6 Bxc6 dxc6 Nxe5'),
        ('rl-berlin-a6dxc6nxe4', 'Small a-pawn move, then pawn takes back, then knight takes the pawn', 'e4 e5 Nf3 Nc6 Bb5 Nf6 O-O a6 Bxc6 dxc6 Nxe5 Nxe4 Re1'),
        ('rl-berlin-d6a6', 'Improved Steinitz Defense, then small a-pawn move', 'e4 e5 Nf3 Nc6 Bb5 Nf6 O-O d6 Re1 a6 Ba4'),
        ('rl-berlin-d6bd7', 'Improved Steinitz Defense, then bishop beside the queen', 'e4 e5 Nf3 Nc6 Bb5 Nf6 O-O d6 Re1 Bd7 c3 a6 Ba4 b5 Bb3'),
        ('rl-berlin-a6dxc6qd4', 'Small a-pawn move, then pawn takes back, then queen comes out', 'e4 e5 Nf3 Nc6 Bb5 Nf6 O-O a6 Bxc6 dxc6 Nxe5 Qd4 Nf3 Qxe4 Re1'),
        ('rl-berlin-bc5oo', 'Beverwijk Variation, then castles', 'e4 e5 Nf3 Nc6 Bb5 Nf6 O-O Bc5 c3 O-O Re1 d6 h3'),
        ('rl-berlin-bc5nxe4', 'Beverwijk Variation, then knight takes the pawn', 'e4 e5 Nf3 Nc6 Bb5 Nf6 O-O Bc5 c3 Nxe4 d4 exd4 cxd4 Bb6 d5'),
        ('rl-berlin-d6be7', 'Improved Steinitz Defense, then bishop to the quiet square', 'e4 e5 Nf3 Nc6 Bb5 Nf6 O-O d6 Re1 Be7 c3 O-O h3'),
        ('rl-berlin-f5', 'F-pawn two squares', 'e4 e5 Nf3 Nc6 Bb5 Nf6 O-O Nxe4 Re1 f5 Bxc6'),
        ('rl-berlin-d6bd7be7', 'Improved Steinitz Defense, then bishop beside the queen, then bishop to the quiet square', 'e4 e5 Nf3 Nc6 Bb5 Nf6 O-O d6 Re1 Bd7 c3 Be7 h3 O-O d4'),
        ('rl-berlin-nf6', 'Knight steps back', 'e4 e5 Nf3 Nc6 Bb5 Nf6 O-O Nxe4 Re1 Nf6 d4 d6 Nc3'),
        ('rl-berlin-bc5ooa6', 'Beverwijk Variation, then castles, then small a-pawn move', 'e4 e5 Nf3 Nc6 Bb5 Nf6 O-O Bc5 c3 O-O Re1 a6 Bxc6'),
        ('rl-berlin-nf6e4', 'Knight steps back, then small e-pawn move', 'e4 e5 Nf3 Nc6 Bb5 Nf6 O-O Nxe4 Re1 Nf6 d4 e4 Nc3 d5 Ne5')],
  why='One in five hits the e-pawn at once. Castle: if the knight takes, the open file in front of Black\'s king gets you the pawn back with a move gained.', outcome='A small edge')
L('rl-steinitz', 'rl-third', 'The Steinitz: the small d-pawn', 'Open the middle while the knight is pinned', 'core',
  'e4 e5 Nf3 Nc6 Bb5 d6 d4 exd4 Nxd4 Bd7 O-O Nf6 Re1 Be7 c3 O-O h3',
  alts=[('rl-steinitz-nxd4', 'Knight takes the knight', 'e4 e5 Nf3 Nc6 Bb5 d6 d4 exd4 Nxd4 Bd7 O-O Nxd4 Bxd7+ Qxd7 Qxd4'),
        ('rl-steinitz-a6', 'Small a-pawn move', 'e4 e5 Nf3 Nc6 Bb5 d6 d4 exd4 Nxd4 Bd7 O-O a6 Bxc6 Bxc6 Re1'),
        ('rl-steinitz-a6d5', 'Small a-pawn move, then small d-pawn move', 'e4 e5 Nf3 Nc6 Bb5 d6 d4 a6 Bxc6+ bxc6 dxe5 d5 O-O'),
        ('rl-steinitz-bd7', 'Bishop beside the queen', 'e4 e5 Nf3 Nc6 Bb5 d6 d4 Bd7 O-O Nxd4 Nxd4 exd4 Bxd7+ Qxd7 Qxd4 Nf6 Re1'),
        ('rl-steinitz-a6bg4', 'Small a-pawn move, then bishop pins the knight', 'e4 e5 Nf3 Nc6 Bb5 d6 d4 a6 Bxc6+ bxc6 dxe5 Bg4 O-O dxe5 Qxd8+ Rxd8 Nxe5'),
        ('rl-steinitz-bd7exd4', 'Bishop beside the queen, then pawn takes the pawn', 'e4 e5 Nf3 Nc6 Bb5 d6 d4 Bd7 O-O exd4 Re1 Be7 c3'),
        ('rl-steinitz-a6bxc6', 'Small a-pawn move, then pawn takes back', 'e4 e5 Nf3 Nc6 Bb5 d6 d4 exd4 Nxd4 Bd7 O-O a6 Bxc6 bxc6 Re1'),
        ('rl-steinitz-a6dxe5', 'Small a-pawn move, then pawn takes back on move 4', 'e4 e5 Nf3 Nc6 Bb5 d6 d4 a6 Bxc6+ bxc6 dxe5 dxe5 Qxd8+ Kxd8 Nxe5 Be6 Nxc6+'),
        ('rl-steinitz-bg4', 'Bishop pins the knight', 'e4 e5 Nf3 Nc6 Bb5 d6 d4 Bg4 c3 a6 Ba4 b5 Bb3'),
        ('rl-steinitz-a6bg4bxf3', 'Small a-pawn move, then bishop pins the knight, then bishop takes the knight', 'e4 e5 Nf3 Nc6 Bb5 d6 d4 a6 Bxc6+ bxc6 dxe5 Bg4 O-O Bxf3 Qxf3 dxe5 Re1'),
        ('rl-steinitz-bd7exd4nf6', 'Bishop beside the queen, then pawn takes the pawn, then king\'s knight out', 'e4 e5 Nf3 Nc6 Bb5 d6 d4 Bd7 O-O exd4 Re1 Nf6 Bxc6 Bxc6 Nxd4'),
        ('rl-steinitz-bd7exd4a6', 'Bishop beside the queen, then pawn takes the pawn, then small a-pawn move', 'e4 e5 Nf3 Nc6 Bb5 d6 d4 Bd7 O-O exd4 Re1 a6 Bxc6 Bxc6 Qxd4'),
        ('rl-steinitz-bd7nf6', 'Bishop beside the queen, then king\'s knight out', 'e4 e5 Nf3 Nc6 Bb5 d6 d4 Bd7 O-O Nf6 Re1 Be7 c3 O-O Ba4'),
        ('rl-steinitz-bd7a6', 'Bishop beside the queen, then small a-pawn move', 'e4 e5 Nf3 Nc6 Bb5 d6 d4 Bd7 O-O a6 Bxc6 Bxc6 dxe5 dxe5 Nxe5 Qxd1 Rxd1 Bxe4 Re1'),
        ('rl-steinitz-bg4exd4', 'Bishop pins the knight, then pawn takes the pawn', 'e4 e5 Nf3 Nc6 Bb5 d6 d4 Bg4 c3 exd4 O-O'),
        ('rl-steinitz-be7', 'Bishop to the quiet square', 'e4 e5 Nf3 Nc6 Bb5 d6 d4 exd4 Nxd4 Bd7 O-O Be7 Re1 Nf6 c3'),
        ('rl-steinitz-bd7a6bxe4', 'Bishop beside the queen, then small a-pawn move, then bishop takes the pawn', 'e4 e5 Nf3 Nc6 Bb5 d6 d4 Bd7 O-O a6 Bxc6 Bxc6 dxe5 Bxe4 Re1 Bxf3 exd6+ Kd7 Qxf3')],
  why='One in four guards the e-pawn this way. The d-pawn has left the knight pinned to the king, so you open the middle at once.', outcome='More room')
L('rl-classical', 'rl-third', 'The Classical: the bishop comes out', 'Castle, then the c-pawn and the d-pawn hit it', 'common',
  'e4 e5 Nf3 Nc6 Bb5 Bc5 O-O d6 Re1 Nf6 c3',
  alts=[('rl-classical-nf6', 'Beverwijk Variation', 'e4 e5 Nf3 Nc6 Bb5 Bc5 O-O Nf6 c3'),
        ('rl-classical-a6', 'Small a-pawn move', 'e4 e5 Nf3 Nc6 Bb5 Bc5 O-O a6 Bxc6 dxc6 Nxe5'),
        ('rl-classical-bd7', 'Bishop beside the queen', 'e4 e5 Nf3 Nc6 Bb5 Bc5 O-O d6 Re1 Bd7 c3'),
        ('rl-classical-bg4', 'Bishop pins the knight', 'e4 e5 Nf3 Nc6 Bb5 Bc5 O-O d6 Re1 Bg4 c3'),
        ('rl-classical-a6bxc6', 'Small a-pawn move, then pawn takes back', 'e4 e5 Nf3 Nc6 Bb5 Bc5 O-O a6 Bxc6 bxc6 Nxe5'),
        ('rl-classical-nge7', 'King\'s knight tucked in', 'e4 e5 Nf3 Nc6 Bb5 Bc5 O-O Nge7 c3 O-O d4 exd4 cxd4'),
        ('rl-classical-a6v2', 'Small a-pawn move on move 5', 'e4 e5 Nf3 Nc6 Bb5 Bc5 O-O d6 Re1 a6 Ba4')],
  why='Black develops as in the Italian. The c-pawn and the d-pawn come at the bishop with a move gained.', outcome='A big center')
L('rl-bird', 'rl-third', 'The Bird: the knight jumps in', 'Take it, castle, and play round the pawn', 'common',
  'e4 e5 Nf3 Nc6 Bb5 Nd4 Nxd4 exd4 O-O Bc5 Re1',
  alts=[('rl-bird-c6', 'Small c-pawn move', 'e4 e5 Nf3 Nc6 Bb5 Nd4 Nxd4 exd4 O-O c6 Bc4 d5 exd5 cxd5 Bb5+ Bd7 Re1+ Be7 Qg4'),
        ('rl-bird-c6b5', 'Small c-pawn move, then b-pawn two squares', 'e4 e5 Nf3 Nc6 Bb5 Nd4 Nxd4 exd4 O-O c6 Bc4 b5 Bb3'),
        ('rl-bird-nf6', 'King\'s knight out', 'e4 e5 Nf3 Nc6 Bb5 Nd4 Nxd4 exd4 O-O Nf6 e5 Nd5 d3'),
        ('rl-bird-qg5', 'Queen comes out', 'e4 e5 Nf3 Nc6 Bb5 Nd4 Nxd4 exd4 O-O Qg5 Bc4'),
        ('rl-bird-c6nf6', 'Small c-pawn move, then king\'s knight out', 'e4 e5 Nf3 Nc6 Bb5 Nd4 Nxd4 exd4 O-O c6 Bc4 Nf6 Re1'),
        ('rl-bird-a6', 'Small a-pawn move', 'e4 e5 Nf3 Nc6 Bb5 Nd4 Nxd4 exd4 O-O a6 Ba4 b5 Bb3 c5 d3')],
  why='The knight moves twice to hit your bishop. Take it: Black\'s pawn ends up alone in the middle.', outcome='Better for you')
L('rl-cozio', 'rl-third', 'The Cozio: the other knight', 'Castle, then c-pawn and d-pawn', 'common',
  'e4 e5 Nf3 Nc6 Bb5 Nge7 O-O g6 Re1 Bg7 c3 O-O h3',
  alts=[('rl-cozio-a6', 'Small a-pawn move', 'e4 e5 Nf3 Nc6 Bb5 Nge7 O-O a6 Ba4 b5 Bb3 d6 Ng5'),
        ('rl-cozio-a6bb7', 'Small a-pawn move, then fianchetto', 'e4 e5 Nf3 Nc6 Bb5 Nge7 O-O a6 Ba4 b5 Bb3 Bb7 Re1'),
        ('rl-cozio-d6', 'Small d-pawn move', 'e4 e5 Nf3 Nc6 Bb5 Nge7 O-O d6 Re1 Bd7 c3'),
        ('rl-cozio-a6ng6', 'Small a-pawn move, then knight jumps forward', 'e4 e5 Nf3 Nc6 Bb5 Nge7 O-O a6 Ba4 b5 Bb3 Ng6 c3'),
        ('rl-cozio-a6h6', 'Small a-pawn move, then small h-pawn move', 'e4 e5 Nf3 Nc6 Bb5 Nge7 O-O a6 Ba4 b5 Bb3 h6 Re1'),
        ('rl-cozio-a6na5', 'Small a-pawn move, then knight jumps forward on move 4', 'e4 e5 Nf3 Nc6 Bb5 Nge7 O-O a6 Ba4 b5 Bb3 Na5 Nxe5')],
  why='Black backs one knight up with the other and blocks the bishop. The setup comes out untouched.', outcome='More room')
L('rl-schliemann', 'rl-third', 'The Schliemann: the f-pawn gambit', 'Leave the pawn and bring the knight out', 'rare',
  'e4 e5 Nf3 Nc6 Bb5 f5 d4',
  why='Black offers a pawn to open the f-file. You don\'t need it: the knight comes out and Black\'s king is the one in the draught.', outcome='Better for you')
L('rl-third', 'rl-third', 'Other third moves', 'The queen out, the fianchetto, the bishop check', 'common',
  'e4 e5 Nf3 Nc6 Bb5 Qf6 O-O a6 Ba4 b5 Bb3',
  alts=[('rl-third-nd4', 'Knight jumps forward', 'e4 e5 Nf3 Nc6 Bb5 Qf6 O-O Nd4 Nxd4 exd4 Re1'),
        ('rl-third-d6', 'Small d-pawn move', 'e4 e5 Nf3 Nc6 Bb5 Qf6 O-O d6 d4'),
        ('rl-third-bc5', 'Bishop aims at f2', 'e4 e5 Nf3 Nc6 Bb5 Qf6 O-O Bc5 c3 a6 Ba4')],
  why='Whatever Black tries on move three, you castle and the pawns take the middle.', outcome='Better for you')

# ============================================================== notes
n('e4 e5 Nf3 Nc6 Bb5', 'Bishop comes at the knight', 'That knight guards the e-pawn. Nothing is threatened yet, but every move Black makes has to keep it in mind.', ['key'], arrows=['b5c6r', 'c6e5g'])
n('e4 e5 Nf3 Nc6 Bb5 a6 Ba4', 'Bishop steps back', 'It still looks at the knight. Taking it would give up the bishop for little.', ['key'])
n('e4 e5 Nf3 Nc6 Bb5 a6 Ba4 b5 Bb3', 'Bishop steps back again', 'Now it stands on the diagonal at f7, and Black\'s pawns on the wing have moved forward for nothing.', ['key'], arrows=['b3f7r'])
n('e4 e5 Nf3 Nc6 Bb5 a6 Ba4 Nf6 O-O', 'Castle', 'The e-pawn can be left: if the knight takes it, the rook comes to the open file in front of Black\'s king.', ['key'])
n('e4 e5 Nf3 Nc6 Bb5 a6 Ba4 Nf6 O-O Be7 Re1', 'Rook beside the king', 'Now the e-pawn is guarded, and the threat to win Black\'s e-pawn is real.', ['key'], arrows=['e1e4g'])
n('e4 e5 Nf3 Nc6 Bb5 a6 Ba4 Nf6 O-O Be7 Re1 b5 Bb3 d6 c3', 'C-pawn one square', 'It backs up the d-pawn\'s push, and gives the bishop a way back if a knight comes after it.', ['key'], arrows=['c3d4g'])
n('e4 e5 Nf3 Nc6 Bb5 a6 Ba4 Nf6 O-O Be7 Re1 b5 Bb3 d6 c3 O-O h3', 'The small h-pawn move', 'Black\'s bishop can\'t pin your knight now. Next the d-pawn goes two squares.', ['key'])
n('e4 e5 Nf3 Nc6 Bb5 Nf6 O-O', 'Castle', 'Leave the e-pawn. If the knight takes it, your rook or your d-pawn opens the middle in front of Black\'s king.', ['key'])
n('e4 e5 Nf3 Nc6 Bb5 d6 d4', 'D-pawn two squares', 'The d-pawn move left the knight pinned to the king. Open the middle while it can\'t move.', ['key'], arrows=['b5e8r', 'd4e5r'])
n('e4 e5 Nf3 Nc6 Bb5 d6 d4 exd4 Nxd4', 'Knight takes back', 'It stands in the middle and adds to the weight on the pinned knight.', ['key'], arrows=['d4c6r', 'b5c6r'])
n('e4 e5 Nf3 Nc6 Bb5 Nd4 Nxd4', 'Take the knight', 'It moved twice to get there. After the trade Black\'s pawn stands alone in the middle.', ['key'])
n('e4 e5 Nf3 Nc6 Bb5 Bc5 O-O', 'Castle', 'Then the c-pawn and the d-pawn come at the bishop.', ['key'])
# the other side's moves that start a named line
n('e4 e5 Nf3 Nc6 Bb5 Nd4', 'Bird Variation')
n('e4 e5 Nf3 Nc6 Bb5 Nf6', 'Berlin Defense')
n('e4 e5 Nf3 Nc6 Bb5 Nge7', 'Cozio Defense')
n('e4 e5 Nf3 Nc6 Bb5 a6', 'Morphy Defense')
n('e4 e5 Nf3 Nc6 Bb5 d6', 'Steinitz Defense')
n('e4 e5 Nf3 Nc6 Bb5 f5', 'Schliemann Defense')
n('e4 e5 Nf3 Nc6 Bb5 Bc5 O-O Nf6', 'Beverwijk Variation')
n('e4 e5 Nf3 Nc6 Bb5 Nf6 O-O Bc5', 'Beverwijk Variation')
n('e4 e5 Nf3 Nc6 Bb5 Nf6 O-O Nxe4', 'Rio Gambit Accepted')
n('e4 e5 Nf3 Nc6 Bb5 Nf6 O-O d6', 'Improved Steinitz Defense')
n('e4 e5 Nf3 Nc6 Bb5 a6 Ba4 Bc5', 'Classical Defense Deferred')
n('e4 e5 Nf3 Nc6 Bb5 a6 Ba4 b5', 'Caro Variation')
n('e4 e5 Nf3 Nc6 Bb5 a6 Ba4 d6', 'Modern Steinitz Defense')
n('e4 e5 Nf3 Nc6 Bb5 a6 Ba4 Bc5 O-O Nf6', 'Møller Variation')
n('e4 e5 Nf3 Nc6 Bb5 a6 Ba4 Nf6 O-O Bc5', 'Møller Variation')
n('e4 e5 Nf3 Nc6 Bb5 a6 Ba4 Nf6 O-O d6', 'Steinitz Deferred')
n('e4 e5 Nf3 Nc6 Bb5 a6 Ba4 b5 Bb3 Bc5', 'Graz Variation')
n('e4 e5 Nf3 Nc6 Bb5 a6 Ba4 b5 Bb3 Na5', 'Norwegian Variation')
n('e4 e5 Nf3 Nc6 Bb5 a6 Ba4 d6 O-O Nf6', 'Steinitz Deferred')
n('e4 e5 Nf3 Nc6 Bb5 a6 Ba4 Nf6 O-O Nxe4 Re1 d5', 'Skipworth Gambit')
n('e4 e5 Nf3 Nc6 Bb5 a6 Ba4 Nf6 O-O b5 Bb3 Bc5', 'Neo-Arkhangelsk Variation')
n('e4 e5 Nf3 Nc6 Bb5 a6 Ba4 b5 Bb3 Bc5 O-O Nf6', 'Neo-Arkhangelsk Variation')
n('e4 e5 Nf3 Nc6 Bb5 a6 Ba4 Nf6 O-O Be7 Re1 b5 Bb3 d6 c3 O-O h3 Bb7', 'Flohr System')
n('e4 e5 Nf3 Nc6 Bb5 a6 Ba4 Nf6 O-O Be7 Re1 b5 Bb3 d6 c3 O-O h3 Na5', 'Chigorin Defense')
n('e4 e5 Nf3 Nc6 Bb5 a6 Ba4 Nf6 O-O Be7 Re1 b5 Bb3 d6 c3 O-O h3 Nb8', 'Breyer Defense')
