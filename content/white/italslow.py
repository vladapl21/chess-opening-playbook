"""White's Italian, a second variation: the slow Italian, a pack for the slot 'whiteItalian' beside the center attack
(see PACKS in content2_meta.py).

One setup, one order: bishop, d-pawn one square, c-pawn one square, castle, rook beside the king, queen's knight behind
the d-pawn, the small h-pawn move, bishop back out of reach, then the knight round to the kingside. The lines were
drafted with pipeline/draft.py: Black's moves by the Maia 1300/1500 odds, yours from the setup's order wherever
Stockfish 17.1 accepts it and the engine's move elsewhere. SAN is internal; notes are plain English."""
from content import n, J, L, PARTS

PARTS.extend([
  dict(id='sl-bishop', ch='italians', title='Black mirrors your bishop', kicker='Giuoco Pianissimo',
       blurb="Both bishops out, and no rush in the middle. Two small pawn moves, castle, the rook beside the king, and the queen's knight goes the long way round to the kingside."),
  dict(id='sl-knight', ch='italians', title="Black's knight comes out", kicker='Two Knights, the quiet way',
       blurb='The knight hits your e-pawn and the d-pawn guards it. From there the setup is the same, and it usually runs into the lines of the first part.'),
  dict(id='sl-odd', ch='italians', title='Other third moves', kicker='Anti-Fried Liver, Paris, Hungarian, Blackburne-Kostić',
       blurb='What club players try on move three. The setup answers all but one: when the knight jumps into the middle, take it.'),
])

L('sl-main', 'sl-bishop', 'The slow Italian: one setup', 'D-pawn, c-pawn, castle, rook, then the knight goes round', 'core',
  'e4 e5 Nf3 Nc6 Bc4 Bc5 d3 Nf6 c3 d6 O-O O-O Re1 a6 Nbd2',
  alts=[('sl-main-h6', 'Small h-pawn move', 'e4 e5 Nf3 Nc6 Bc4 Bc5 d3 h6 c3 Nf6 O-O'),
        ('sl-main-d6', 'Small d-pawn move', 'e4 e5 Nf3 Nc6 Bc4 Bc5 d3 d6 c3 Nf6 O-O'),
        ('sl-main-oo', 'Castles', 'e4 e5 Nf3 Nc6 Bc4 Bc5 d3 Nf6 c3 O-O O-O d6 Re1 Bg4 Nbd2'),
        ('sl-main-d6h6', 'Small d-pawn move, then small h-pawn move', 'e4 e5 Nf3 Nc6 Bc4 Bc5 d3 d6 c3 h6 O-O'),
        ('sl-main-d6bg4', 'Small d-pawn move, then bishop pins the knight', 'e4 e5 Nf3 Nc6 Bc4 Bc5 d3 d6 c3 Bg4 O-O Nf6 Re1'),
        ('sl-main-h6a6', 'Small h-pawn move, then small a-pawn move', 'e4 e5 Nf3 Nc6 Bc4 Bc5 d3 h6 c3 a6 d4 exd4 cxd4'),
        ('sl-main-ng4', 'Knight jumps forward', 'e4 e5 Nf3 Nc6 Bc4 Bc5 d3 Nf6 c3 Ng4 d4 exd4 cxd4 Bb4+ Nc3'),
        ('sl-main-a6', 'Small a-pawn move', 'e4 e5 Nf3 Nc6 Bc4 Bc5 d3 Nf6 c3 a6 O-O'),
        ('sl-main-h6d6', 'Small h-pawn move, then small d-pawn move', 'e4 e5 Nf3 Nc6 Bc4 Bc5 d3 h6 c3 d6 O-O Nf6 Re1'),
        ('sl-main-ooh6', 'Castles, then small h-pawn move', 'e4 e5 Nf3 Nc6 Bc4 Bc5 d3 Nf6 c3 O-O O-O h6 Re1'),
        ('sl-main-d5', 'D-pawn two squares', 'e4 e5 Nf3 Nc6 Bc4 Bc5 d3 Nf6 c3 d5 exd5 Nxd5 Qb3 Be6 Qxb7'),
        ('sl-main-h6oo', 'Small h-pawn move, then castles', 'e4 e5 Nf3 Nc6 Bc4 Bc5 d3 Nf6 c3 h6 O-O O-O Re1'),
        ('sl-main-bg4', 'Bishop pins the knight', 'e4 e5 Nf3 Nc6 Bc4 Bc5 d3 Nf6 c3 d6 O-O Bg4 Re1 O-O Nbd2'),
        ('sl-main-d6be6', 'Small d-pawn move, then bishop behind the center pawns', 'e4 e5 Nf3 Nc6 Bc4 Bc5 d3 d6 c3 Be6 Nbd2'),
        ('sl-main-d6a6', 'Small d-pawn move, then small a-pawn move', 'e4 e5 Nf3 Nc6 Bc4 Bc5 d3 d6 c3 a6 O-O'),
        ('sl-main-h6d6v2', 'Small h-pawn move, then small d-pawn move on move 5', 'e4 e5 Nf3 Nc6 Bc4 Bc5 d3 Nf6 c3 h6 O-O d6 Re1'),
        ('sl-main-d6bg4qf6', 'Small d-pawn move, then bishop pins the knight, then queen comes out', 'e4 e5 Nf3 Nc6 Bc4 Bc5 d3 d6 c3 Bg4 O-O Qf6 Re1'),
        ('sl-main-ooa6', 'Castles, then small a-pawn move', 'e4 e5 Nf3 Nc6 Bc4 Bc5 d3 Nf6 c3 O-O O-O a6 Re1 b5 Bb3'),
        ('sl-main-ood5', 'Castles, then Giuoco Pianissimo', 'e4 e5 Nf3 Nc6 Bc4 Bc5 d3 Nf6 c3 O-O O-O d5 exd5 Nxd5 Re1 Re8 d4'),
        ('sl-main-ng4bb6', 'Knight jumps forward, then bishop steps back', 'e4 e5 Nf3 Nc6 Bc4 Bc5 d3 Nf6 c3 Ng4 d4 exd4 cxd4 Bb6 h3'),
        ('sl-main-h6d6bg4', 'Small h-pawn move, then small d-pawn move, then bishop pins the knight', 'e4 e5 Nf3 Nc6 Bc4 Bc5 d3 h6 c3 d6 O-O Bg4 Re1 Nf6 Nbd2')],
  why='Black mirrors your bishop. No early fight in the middle: both small pawn moves, castle, and every piece finds its square before anything is traded.', outcome='A full game with the easier plan')
L('sl-2n', 'sl-knight', 'Black\'s knight comes out: guard the e-pawn', 'The small d-pawn move, then the same setup', 'core',
  'e4 e5 Nf3 Nc6 Bc4 Nf6 d3 d5 exd5 Nxd5 O-O Be6 c3',
  alts=[('sl-2n-bc5', 'Bishop aims at f2', 'e4 e5 Nf3 Nc6 Bc4 Nf6 d3 Bc5 c3'),
        ('sl-2n-h6', 'Small h-pawn move', 'e4 e5 Nf3 Nc6 Bc4 Nf6 d3 h6 c3 Bc5 O-O'),
        ('sl-2n-d6', 'Small d-pawn move', 'e4 e5 Nf3 Nc6 Bc4 Nf6 d3 d6 Ng5 d5 exd5 Nxd5 O-O'),
        ('sl-2n-d6be6', 'Small d-pawn move, then bishop behind the center pawns', 'e4 e5 Nf3 Nc6 Bc4 Nf6 d3 d6 Ng5 Be6 Nxe6 fxe6 Bxe6 Qe7 Bh3'),
        ('sl-2n-h6d5', 'Small h-pawn move, then d-pawn two squares', 'e4 e5 Nf3 Nc6 Bc4 Nf6 d3 h6 c3 d5 exd5 Nxd5 O-O'),
        ('sl-2n-be7', 'Bishop to the quiet square', 'e4 e5 Nf3 Nc6 Bc4 Nf6 d3 d5 exd5 Nxd5 O-O Be7 c3'),
        ('sl-2n-be7oo', 'Bishop to the quiet square, then castles', 'e4 e5 Nf3 Nc6 Bc4 Nf6 d3 Be7 c3 O-O O-O d5 exd5 Nxd5 Re1'),
        ('sl-2n-h6be7', 'Small h-pawn move, then bishop to the quiet square', 'e4 e5 Nf3 Nc6 Bc4 Nf6 d3 h6 c3 Be7 O-O'),
        ('sl-2n-h6d6', 'Small h-pawn move, then small d-pawn move', 'e4 e5 Nf3 Nc6 Bc4 Nf6 d3 h6 c3 d6 O-O Bg4 Re1'),
        ('sl-2n-h6a6', 'Small h-pawn move, then small a-pawn move', 'e4 e5 Nf3 Nc6 Bc4 Nf6 d3 h6 c3 a6 O-O b5 Bb3'),
        ('sl-2n-be7d6', 'Bishop to the quiet square, then small d-pawn move', 'e4 e5 Nf3 Nc6 Bc4 Nf6 d3 Be7 c3 d6 O-O'),
        ('sl-2n-bc5v2', 'Bishop aims at f2 on move 6', 'e4 e5 Nf3 Nc6 Bc4 Nf6 d3 d5 exd5 Nxd5 O-O Bc5 c3 O-O Re1'),
        ('sl-2n-be7ood6', 'Bishop to the quiet square, then castles, then small d-pawn move', 'e4 e5 Nf3 Nc6 Bc4 Nf6 d3 Be7 c3 O-O O-O d6 Re1 Bg4 Nbd2'),
        ('sl-2n-bg4', 'Bishop pins the knight', 'e4 e5 Nf3 Nc6 Bc4 Nf6 d3 d5 exd5 Nxd5 O-O Bg4 Re1 Bd6 Bxd5')],
  why='Three in ten bring the knight out at your e-pawn. The d-pawn guards it, and no knight jump is needed: the setup is the same.', outcome='A quiet edge')
L('sl-h6', 'sl-odd', 'The Anti-Fried Liver Defense', 'A move spent on the edge: the same setup, a move ahead', 'common',
  'e4 e5 Nf3 Nc6 Bc4 h6 d3 a6 c3 b5 Bb3',
  alts=[('sl-h6-nf6', 'King\'s knight out', 'e4 e5 Nf3 Nc6 Bc4 h6 d3 Nf6 c3'),
        ('sl-h6-bc5', 'Bishop aims at f2', 'e4 e5 Nf3 Nc6 Bc4 h6 d3 Bc5 c3'),
        ('sl-h6-d6', 'Small d-pawn move', 'e4 e5 Nf3 Nc6 Bc4 h6 d3 d6 c3 Nf6 O-O'),
        ('sl-h6-d6bg4', 'Small d-pawn move, then bishop pins the knight', 'e4 e5 Nf3 Nc6 Bc4 h6 d3 d6 c3 Bg4 Nbd2 Nf6 O-O'),
        ('sl-h6-nf6v2', 'King\'s knight out on move 5', 'e4 e5 Nf3 Nc6 Bc4 h6 d3 a6 c3 Nf6 O-O')],
  why='One in five club players stops a knight jump you never meant to make. Carry on with the setup.', outcome='A move ahead')
L('sl-d6', 'sl-odd', 'The Paris Defense', 'The d-pawn first: the same setup', 'rare',
  'e4 e5 Nf3 Nc6 Bc4 d6 d3 Be6 O-O Bxc4 dxc4 Nf6 Re1',
  alts=[('sl-d6-h6', 'Small h-pawn move', 'e4 e5 Nf3 Nc6 Bc4 d6 d3 h6 c3'),
        ('sl-d6-nf6', 'King\'s knight out', 'e4 e5 Nf3 Nc6 Bc4 d6 d3 Nf6 Ng5'),
        ('sl-d6-be7', 'Bishop to the quiet square', 'e4 e5 Nf3 Nc6 Bc4 d6 d3 Be7 c3'),
        ('sl-d6-bg4', 'Bishop pins the knight', 'e4 e5 Nf3 Nc6 Bc4 d6 d3 Bg4 c3 Nf6 O-O Be7 Re1 O-O Nbd2')],
  why='Black guards the e-pawn before anything else. Nothing changes for you.', outcome='More room')
L('sl-nd4', 'sl-odd', 'The Blackburne-Kostić Gambit', 'Take the knight; never the e-pawn', 'rare',
  'e4 e5 Nf3 Nc6 Bc4 Nd4 Nxd4 exd4 d3 Nf6 O-O',
  alts=[('sl-nd4-c5', 'C-pawn two squares', 'e4 e5 Nf3 Nc6 Bc4 Nd4 Nxd4 exd4 d3 c5 c3'),
        ('sl-nd4-bc5', 'Bishop aims at f2', 'e4 e5 Nf3 Nc6 Bc4 Nd4 Nxd4 exd4 d3 Bc5 Bxf7+ Kxf7 Qh5+ g6 Qxc5'),
        ('sl-nd4-c6', 'Small c-pawn move', 'e4 e5 Nf3 Nc6 Bc4 Nd4 Nxd4 exd4 d3 c6 O-O'),
        ('sl-nd4-d6', 'Small d-pawn move', 'e4 e5 Nf3 Nc6 Bc4 Nd4 Nxd4 exd4 d3 d6 c3 dxc3 O-O cxb2 Bxb2'),
        ('sl-nd4-h6', 'Small h-pawn move', 'e4 e5 Nf3 Nc6 Bc4 Nd4 Nxd4 exd4 d3 h6 c3'),
        ('sl-nd4-bb4', 'Bishop gives check', 'e4 e5 Nf3 Nc6 Bc4 Nd4 Nxd4 exd4 d3 Bb4+ c3 dxc3 bxc3')],
  why='Black offers the e-pawn as bait. Taking it loses to the queen. Take the knight instead and you are simply better.', outcome='Better for you')
L('sl-be7', 'sl-odd', 'The Hungarian Defense', 'The quiet bishop: the same setup', 'rare',
  'e4 e5 Nf3 Nc6 Bc4 Be7 d3 d6 c3',
  alts=[('sl-be7-nf6', 'Modern Bishop\'s Opening', 'e4 e5 Nf3 Nc6 Bc4 Be7 d3 Nf6 c3')],
  why='Black keeps the bishop at home. The setup comes out untouched.', outcome='More room')
L('sl-odd', 'sl-odd', 'Odd third moves', 'The f-pawn, the fianchetto, the queen out early', 'rare',
  'e4 e5 Nf3 Nc6 Bc4 f5 d3',
  alts=[('sl-odd-g6', 'Small g-pawn move', 'e4 e5 Nf3 Nc6 Bc4 g6 d3')],
  why='The Rousseau Gambit and the rest. The small d-pawn move is the answer to nearly all of them.', outcome='Better for you')

# ============================================================== notes
n('e4 e5 Nf3 Nc6 Bc4 Bc5 d3', 'Small d-pawn move', 'One square, not two. It guards the e-pawn, and nothing gets traded early.', ['key'])
n('e4 e5 Nf3 Nc6 Bc4 Bc5 d3 Nf6 c3', 'Small c-pawn move', 'It keeps Black\'s knight out of the middle and gives your bishop a way back. The d-pawn can go forward later, when everything is ready.', ['key'])
n('e4 e5 Nf3 Nc6 Bc4 Bc5 d3 Nf6 c3 d6 O-O', 'Castle', 'King safe. The rook comes beside it next.', ['key'])
n('e4 e5 Nf3 Nc6 Bc4 Bc5 d3 Nf6 c3 d6 O-O O-O Re1', 'Rook beside the king', 'It stands behind the e-pawn, and leaves its square for the knight that is on its way round.', ['key'])
n('e4 e5 Nf3 Nc6 Bc4 Bc5 d3 Nf6 c3 d6 O-O O-O Re1 a6 Nbd2', 'Knight behind the d-pawn', 'The first step of its trip to the kingside: behind the rook next, then out in front of the king.', ['key'], arrows=['d2f1g', 'f1g3g'])
n('e4 e5 Nf3 Nc6 Bc4 Bc5 d3 Nf6 c3 Ng4 d4', 'D-pawn two squares', 'The knight left its post to go at f2. Now the middle is yours, with a hit on the bishop.', ['key'])
n('e4 e5 Nf3 Nc6 Bc4 Bc5 d3 Nf6 c3 d5 exd5', 'Take it', 'Black opens the middle before castling. After the trade your queen comes out with a hit on the knight in the middle.', ['key'])
n('e4 e5 Nf3 Nc6 Bc4 Nf6 d3', 'D-pawn guards the e-pawn', 'No knight jump is needed. The setup carries on, and it usually runs into the same positions as against the bishop.', ['key'])
n('e4 e5 Nf3 Nc6 Bc4 Nf6 d3 d6 Ng5', 'Now the knight jumps', 'Black spent a move on the d-pawn, so the pawn that would block your bishop gets there a move late. Bishop and knight both aim at f7.', ['key'], arrows=['g5f7r', 'c4f7r'])
n('e4 e5 Nf3 Nc6 Bc4 h6 d3', 'Carry on', 'Black stopped a knight jump you never meant to make. You are a move ahead in the same setup.', ['key'])
n('e4 e5 Nf3 Nc6 Bc4 f5 d3', 'Small d-pawn move', 'The Rousseau Gambit wants you to take. Guard the e-pawn and develop: the f-pawn has only opened lines to Black\'s own king.', ['key'])
# the other side's moves that start a named line
n('e4 e5 Nf3 Nc6 Bc4 Be7 d3 Nf6', 'Modern Bishop\'s Opening')
n('e4 e5 Nf3 Nc6 Bc4 Bc5 d3 d6 c3 Nf6', 'Giuoco Pianissimo')
n('e4 e5 Nf3 Nc6 Bc4 Bc5 d3 Nf6 c3 O-O O-O d5', 'Giuoco Pianissimo')
n('e4 e5 Nf3 Nc6 Bc4 Bc5 d3 Nf6 c3 O-O O-O d6', 'Giuoco Pianissimo')
