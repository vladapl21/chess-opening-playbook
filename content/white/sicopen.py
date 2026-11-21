"""White against the Sicilian, a second variation: the Open Sicilian, a pack for the slot 'whiteSic' beside the Alapin
(see PACKS in content2_meta.py).

One setup, one order: knight, d-pawn two squares, take back with the knight, queen's knight, bishop beside the queen,
f-pawn one square, queen, castle long, then the g-pawn. When Black's e-pawn hits the knight in the middle it steps
back, or jumps forward when the square in front is free. The lines were drafted with pipeline/draft.py: Black's moves by the Maia 1300/1500 odds, yours from the
setup's order wherever Stockfish 17.1 accepts it and the engine's move elsewhere. SAN is internal; notes are plain
English."""
from content import n, J, L, PARTS

PARTS.extend([
  dict(id='so-d6', ch='sico', title="Black's d-pawn first", kicker='Najdorf, Dragon, Classical, Scheveningen',
       blurb='The most common way to play the Sicilian. You open the middle, take back with the knight and bring out the same pieces in the same order: bishop, f-pawn, queen, castle long.'),
  dict(id='so-nc6', ch='sico', title="Black's knight first", kicker='Accelerated Dragon, Sveshnikov, Kalashnikov',
       blurb='With the knight out early Black can hit your knight with the e-pawn. Here the square in front is free, so the knight jumps forward. Otherwise the setup is the same.'),
  dict(id='so-e6', ch='sico', title="Black's e-pawn first", kicker='Kan, Taimanov',
       blurb='Small pawn moves and a flexible setup for Black. Yours comes out untouched.'),
  dict(id='so-rare', ch='sico', title='Other second moves', kicker="Hyperaccelerated Dragon, O'Kelly, Nimzowitsch",
       blurb='The rare tries on move two, each with the one move worth knowing.'),
])

L('so-najdorf', 'so-d6', 'The Najdorf', 'F-pawn, bishop, queen, castle long, then the g-pawn', 'core',
  'e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 a6 f3 e5 Nb3 Be7 Be3',
  alts=[('so-najdorf-g6', 'Small g-pawn move', 'e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 a6 f3 g6 Be3 Bg7 Qd2'),
        ('so-najdorf-nc6', 'Queen\'s knight out', 'e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 a6 f3 Nc6 Be3'),
        ('so-najdorf-e6', 'Small e-pawn move', 'e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 a6 f3 e6 Be3 Be7 Qd2 O-O O-O-O'),
        ('so-najdorf-nc6v2', 'Queen\'s knight out on move 7', 'e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 a6 f3 e5 Nb3 Nc6 Be3'),
        ('so-najdorf-b5', 'B-pawn two squares', 'e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 a6 f3 b5 Be3 Bb7 Qd2'),
        ('so-najdorf-be6', 'Bishop behind the center pawns', 'e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 a6 f3 e5 Nb3 Be6 Be3'),
        ('so-najdorf-e6b5', 'Small e-pawn move, then b-pawn two squares', 'e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 a6 f3 e6 Be3 b5 Qd2 Bb7 O-O-O Nbd7 g4'),
        ('so-najdorf-be6v2', 'Bishop behind the center pawns on move 7', 'e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 a6 f3 e5 Nb3 Be6 Be3 Be7 Qd2 O-O O-O-O Nbd7 g4')],
  why='Black\'s small a-pawn move is the most famous Sicilian. Your setup doesn\'t care: the same five moves, then the pawns roll at Black\'s king.', outcome='An attack with the pieces behind it')
L('so-dragon', 'so-d6', 'The Dragon', 'The same setup; trade off the bishop on the long diagonal', 'core',
  'e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 g6 f3 Bg7 Be3 O-O Qd2 Nc6 O-O-O Bd7 g4',
  alts=[('so-dragon-a6', 'Small a-pawn move', 'e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 g6 f3 Bg7 Be3 O-O Qd2 a6 O-O-O'),
        ('so-dragon-a6v2', 'Small a-pawn move on move 7', 'e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 g6 f3 Bg7 Be3 a6 Qd2'),
        ('so-dragon-nc6', 'Belezky Line', 'e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 g6 f3 Bg7 Be3 Nc6 Qd2'),
        ('so-dragon-d5', 'Small d-pawn move', 'e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 g6 f3 Bg7 Be3 O-O Qd2 Nc6 O-O-O d5 exd5')],
  why='Black\'s bishop goes to the long diagonal. Your setup is made for it: queen and bishop line up to trade that bishop, and the edge pawn opens the file.', outcome='A race you start first')
L('so-classical', 'so-d6', 'The Classical', 'Both knights out: the same setup', 'common',
  'e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 Nc6 f3 e5 Nb3 Be7 Be3 O-O Qd2 Be6 O-O-O a5 Bb5',
  why='Black develops the natural way. Bishop, f-pawn, queen, castle long.', outcome='More space and the safer king')
L('so-schev', 'so-d6', 'The Scheveningen', 'Two small center pawns: the setup, then the g-pawn', 'common',
  'e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 e6 f3 Be7 Be3',
  alts=[('so-schev-oo', 'Castles', 'e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 e6 f3 Be7 Be3 O-O Qd2 Nc6 O-O-O a6 g4')],
  why='Black keeps two pawns side by side in the middle. Your pieces come out behind the f-pawn and the g-pawn goes at the knight.', outcome='An attack on the kingside')
L('so-d6x', 'so-d6', 'The d-pawn first: early tries', 'When Black leaves the usual path', 'common',
  'e4 c5 Nf3 d6 d4 cxd4 Nxd4 e5 Bb5+ Bd7 Bxd7+ Nxd7 Nf5',
  alts=[('so-d6x-nc6', 'Queen\'s knight out', 'e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nc6 Nc3'),
        ('so-d6x-a6', 'Small a-pawn move', 'e4 c5 Nf3 d6 d4 cxd4 Nxd4 a6 Nc3 Nf6 f3'),
        ('so-d6x-g6', 'Accelerated Dragon', 'e4 c5 Nf3 d6 d4 cxd4 Nxd4 g6 Nc3 Bg7 f3 Nf6 Be3'),
        ('so-d6x-nf6', 'King\'s knight out', 'e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 e5 Bb5+ Bd7 Bxd7+ Nbxd7 Nf5'),
        ('so-d6x-nf6qxd7', 'King\'s knight out, then queen takes back', 'e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 e5 Bb5+ Bd7 Bxd7+ Qxd7 Nde2'),
        ('so-d6x-qxd7', 'Queen takes back', 'e4 c5 Nf3 d6 d4 cxd4 Nxd4 e5 Bb5+ Bd7 Bxd7+ Qxd7 Ne2 Nf6 Nbc3'),
        ('so-d6x-a6nc6', 'Small a-pawn move, then queen\'s knight out', 'e4 c5 Nf3 d6 d4 cxd4 Nxd4 a6 Nc3 Nc6 f3'),
        ('so-d6x-g6nc6', 'Accelerated Dragon, then queen\'s knight out', 'e4 c5 Nf3 d6 d4 cxd4 Nxd4 g6 Nc3 Bg7 f3 Nc6 Be3'),
        ('so-d6x-qxd7nc6', 'Queen takes back, then queen\'s knight out', 'e4 c5 Nf3 d6 d4 cxd4 Nxd4 e5 Bb5+ Bd7 Bxd7+ Qxd7 Ne2 Nc6 f3')],
  why='Before the main lines there are a few side roads: the e-pawn pushed at your knight, the knight left at home. The setup still comes out.', outcome='Better for you')
L('so-accel', 'so-nc6', 'The Accelerated Dragon', 'The bishop comes to the long diagonal a move early', 'common',
  'e4 c5 Nf3 Nc6 d4 cxd4 Nxd4 g6 Nc3 Bg7 Be3 Nf6 Bc4 O-O Bb3',
  alts=[('so-accel-e5', 'E-pawn two squares', 'e4 c5 Nf3 Nc6 d4 cxd4 Nxd4 g6 Nc3 Bg7 Be3 e5 Ndb5'),
        ('so-accel-d6', 'Small d-pawn move', 'e4 c5 Nf3 Nc6 d4 cxd4 Nxd4 g6 Nc3 Bg7 Be3 d6 f3 Nf6 Qd2'),
        ('so-accel-e6', 'Small e-pawn move', 'e4 c5 Nf3 Nc6 d4 cxd4 Nxd4 g6 Nc3 Bg7 Be3 e6 Ndb5 a6 Nd6+')],
  why='Black skips the d-pawn move to get the bishop out fast. Your bishop takes its best square before the f-pawn moves.', outcome='A small, steady edge')
L('so-four', 'so-nc6', 'Both knights, then the e-pawn', 'The Sveshnikov and its cousins: the knight jumps forward', 'common',
  'e4 c5 Nf3 Nc6 d4 cxd4 Nxd4 Nf6 Nc3 e5 Ndb5 Bb4 Bg5',
  alts=[('so-four-e6', 'Four Knights Variation', 'e4 c5 Nf3 Nc6 d4 cxd4 Nxd4 Nf6 Nc3 e6 Nxc6'),
        ('so-four-d6', 'Small d-pawn move', 'e4 c5 Nf3 Nc6 d4 cxd4 Nxd4 Nf6 Nc3 d6 f3'),
        ('so-four-g6', 'Small g-pawn move', 'e4 c5 Nf3 Nc6 d4 cxd4 Nxd4 Nf6 Nc3 g6 f3 Bg7 Be3 O-O Qd2'),
        ('so-four-a6', 'Small a-pawn move', 'e4 c5 Nf3 Nc6 d4 cxd4 Nxd4 Nf6 Nc3 a6 Be3'),
        ('so-four-a6v2', 'Small a-pawn move on move 6', 'e4 c5 Nf3 Nc6 d4 cxd4 Nxd4 Nf6 Nc3 e5 Ndb5 a6 Nd6+ Bxd6 Qxd6 Qe7 Qxe7+')],
  why='Black hits your knight with the e-pawn. The square in front is free, so the knight jumps in, at the hole the pawn left behind it.', outcome='A hole in Black\'s camp to use')
L('so-e5', 'so-nc6', 'The e-pawn hits your knight at once', 'The Löwenthal and the Kalashnikov: the knight jumps forward', 'rare',
  'e4 c5 Nf3 Nc6 d4 cxd4 Nxd4 e5 Nb5 a6 Nd6+ Bxd6 Qxd6 Qe7 Qd1',
  alts=[('so-e5-nf6', 'King\'s knight out', 'e4 c5 Nf3 Nc6 d4 cxd4 Nxd4 e5 Nb5 a6 Nd6+ Bxd6 Qxd6 Nf6 Nc3'),
        ('so-e5-d6', 'Kalashnikov Variation', 'e4 c5 Nf3 Nc6 d4 cxd4 Nxd4 e5 Nb5 d6 c4 a6 N5c3 Nf6 f3'),
        ('so-e5-nge7', 'King\'s knight tucked in', 'e4 c5 Nf3 Nc6 d4 cxd4 Nxd4 e5 Nb5 a6 Nd6+ Bxd6 Qxd6 Nge7 Nc3'),
        ('so-e5-d6nf6', 'Kalashnikov Variation, then king\'s knight out', 'e4 c5 Nf3 Nc6 d4 cxd4 Nxd4 e5 Nb5 d6 c4 Nf6 f3'),
        ('so-e5-qa5', 'Queen gives check', 'e4 c5 Nf3 Nc6 d4 cxd4 Nxd4 e5 Nb5 Qa5+ Qd2 Bb4 c3 Bc5 Qg5'),
        ('so-e5-nf6a6', 'King\'s knight out, then small a-pawn move', 'e4 c5 Nf3 Nc6 d4 cxd4 Nxd4 e5 Nb5 Nf6 Bg5 a6 Bxf6 Qxf6 Nc7+ Kd8 Nxa8'),
        ('so-e5-nf6be7', 'King\'s knight out, then bishop to the quiet square', 'e4 c5 Nf3 Nc6 d4 cxd4 Nxd4 e5 Nb5 Nf6 Bg5 Be7 Bxf6 Bxf6 Nd6+ Ke7 Nc3')],
  why='The same idea a move earlier. The knight jumps forward, at the hole in front of Black\'s d-pawn.', outcome='Better for you')
L('so-nc6x', 'so-nc6', 'The knight first: other tries', 'The Taimanov setup, an early queen, the trade in the middle', 'common',
  'e4 c5 Nf3 Nc6 d4 cxd4 Nxd4 Nxd4 Qxd4 d6 Nc3 e5 Qa4+ Bd7 Qb3',
  alts=[('so-nc6x-e6', 'Taimanov Variation', 'e4 c5 Nf3 Nc6 d4 cxd4 Nxd4 e6 Nc3'),
        ('so-nc6x-e6v2', 'Small e-pawn move', 'e4 c5 Nf3 Nc6 d4 cxd4 Nxd4 Nxd4 Qxd4 e6 Nc3'),
        ('so-nc6x-d6', 'Small d-pawn move', 'e4 c5 Nf3 Nc6 d4 cxd4 Nxd4 d6 Nc3 Nf6 f3'),
        ('so-nc6x-e6exd5', 'Franco-Sicilian Variation, then pawn takes the pawn', 'e4 c5 Nf3 Nc6 d4 e6 d5 exd5 exd5 Nce7 d6'),
        ('so-nc6x-e6exd5nb4', 'Franco-Sicilian Variation, then pawn takes the pawn, then knight jumps forward', 'e4 c5 Nf3 Nc6 d4 e6 d5 exd5 exd5 Nb4 a3'),
        ('so-nc6x-d6a6', 'Small d-pawn move, then small a-pawn move', 'e4 c5 Nf3 Nc6 d4 cxd4 Nxd4 d6 Nc3 a6 f3'),
        ('so-nc6x-nf6', 'King\'s knight out', 'e4 c5 Nf3 Nc6 d4 cxd4 Nxd4 Nxd4 Qxd4 Nf6 e5 Ng8 Nc3'),
        ('so-nc6x-d6g6', 'Small d-pawn move, then small g-pawn move', 'e4 c5 Nf3 Nc6 d4 cxd4 Nxd4 d6 Nc3 g6 f3 Bg7 Be3'),
        ('so-nc6x-e6exd5qe7', 'Franco-Sicilian Variation, then pawn takes the pawn, then queen gives check', 'e4 c5 Nf3 Nc6 d4 e6 d5 exd5 exd5 Qe7+ Be2'),
        ('so-nc6x-nf6nh5', 'King\'s knight out, then knight jumps forward', 'e4 c5 Nf3 Nc6 d4 cxd4 Nxd4 Nxd4 Qxd4 Nf6 e5 Nh5 g4'),
        ('so-nc6x-d6e5', 'Small d-pawn move, then e-pawn two squares', 'e4 c5 Nf3 Nc6 d4 cxd4 Nxd4 d6 Nc3 e5 Nf5'),
        ('so-nc6x-nf6e5', 'King\'s knight out, then e-pawn two squares', 'e4 c5 Nf3 Nc6 d4 cxd4 Nxd4 Nxd4 Qxd4 d6 Nc3 Nf6 Be3 e5 Bb5+ Bd7 Qd3'),
        ('so-nc6x-nf6g6', 'King\'s knight out, then small g-pawn move', 'e4 c5 Nf3 Nc6 d4 cxd4 Nxd4 Nxd4 Qxd4 d6 Nc3 Nf6 Be3 g6 e5'),
        ('so-nc6x-e6nce7', 'Franco-Sicilian Variation, then knight steps back', 'e4 c5 Nf3 Nc6 d4 e6 d5 Nce7 d6'),
        ('so-nc6x-e6exd5nd4', 'Franco-Sicilian Variation, then pawn takes the pawn, then knight jumps forward on move 3', 'e4 c5 Nf3 Nc6 d4 e6 d5 exd5 exd5 Nd4 Nxd4 cxd4 Qxd4'),
        ('so-nc6x-nf6qa5', 'King\'s knight out, then queen gives check', 'e4 c5 Nf3 Nc6 d4 cxd4 Nxd4 Nxd4 Qxd4 Nf6 e5 Qa5+ Nc3')],
  why='Black has a few more ways to play after the knight comes out. Knight out, bishop, and the setup again.', outcome='Better for you')
L('so-kan', 'so-e6', 'The Kan', 'Two small pawn moves; your pieces come out freely', 'common',
  'e4 c5 Nf3 e6 d4 cxd4 Nxd4 a6 Nc3 Qc7 Be3',
  alts=[('so-kan-b5', 'Wing Attack', 'e4 c5 Nf3 e6 d4 cxd4 Nxd4 a6 Nc3 b5 f3')],
  why='Black plays the e-pawn and the a-pawn one square and waits. Nothing stops your setup.', outcome='More space')
L('so-taim', 'so-e6', 'The Taimanov', 'The knight comes out behind the e-pawn', 'common',
  'e4 c5 Nf3 e6 d4 cxd4 Nxd4 Nc6 Nc3 a6 f3',
  alts=[('so-taim-nf6', 'Four Knights Variation', 'e4 c5 Nf3 e6 d4 cxd4 Nxd4 Nc6 Nc3 Nf6 Nxc6 bxc6 e5'),
        ('so-taim-bb4', 'Bishop pins the knight', 'e4 c5 Nf3 e6 d4 cxd4 Nxd4 Nc6 Nc3 Bb4 Nxc6 bxc6 Qd4'),
        ('so-taim-nxd4', 'Knight takes the knight', 'e4 c5 Nf3 e6 d4 cxd4 Nxd4 Nc6 Nc3 Nxd4 Qxd4'),
        ('so-taim-bc5', 'Bishop aims at f2', 'e4 c5 Nf3 e6 d4 cxd4 Nxd4 Nc6 Nc3 Bc5 Ndb5')],
  why='A flexible setup for Black. Yours is the same as ever.', outcome='More space')
L('so-e6x', 'so-e6', 'The e-pawn first: other tries', 'The knight at once, the bishop out, the French-style d-pawn', 'common',
  'e4 c5 Nf3 e6 d4 cxd4 Nxd4 Bc5 Nc3',
  alts=[('so-e6x-nc6', 'Franco-Sicilian Variation', 'e4 c5 Nf3 e6 d4 Nc6 d5'),
        ('so-e6x-a6', 'Drazic Variation', 'e4 c5 Nf3 e6 d4 a6 d5'),
        ('so-e6x-d5', 'Marshall Counterattack', 'e4 c5 Nf3 e6 d4 d5 Nc3 Nc6 Be3'),
        ('so-e6x-nf6', 'King\'s knight out', 'e4 c5 Nf3 e6 d4 cxd4 Nxd4 Nf6 Nc3 Bb4 e5'),
        ('so-e6x-d5nf6', 'Marshall Counterattack, then king\'s knight out', 'e4 c5 Nf3 e6 d4 d5 Nc3 Nf6 exd5'),
        ('so-e6x-d5dxe4', 'Marshall Counterattack, then pawn takes the pawn', 'e4 c5 Nf3 e6 d4 d5 Nc3 dxe4 Nxe4')],
  why='After the e-pawn move Black can still go several ways. The knight and the d-pawn come first, whatever follows.', outcome='Better for you')
L('so-g6', 'so-rare', 'The fianchetto on move two', 'The Hyperaccelerated Dragon: take the middle', 'rare',
  'e4 c5 Nf3 g6 d4 cxd4 Nxd4 Bg7 Nc3 Nc6 Be3',
  alts=[('so-g6-nc6', 'Accelerated Dragon', 'e4 c5 Nf3 g6 d4 cxd4 Nxd4 Nc6 Nc3'),
        ('so-g6-bg7', 'Hyperaccelerated Pterodactyl', 'e4 c5 Nf3 g6 d4 Bg7 Nc3 cxd4 Nxd4')],
  why='Black starts with the g-pawn. The d-pawn goes two squares all the same.', outcome='A big center')
L('so-rare', 'so-rare', 'Other second moves', 'The a-pawn, the knight at your e-pawn, the queen out', 'rare',
  'e4 c5 Nf3 a6 d4 cxd4 Nxd4 Nc6 Nc3',
  alts=[('so-rare-e6', 'Drazic Variation', 'e4 c5 Nf3 a6 d4 e6 d5'),
        ('so-rare-e5', 'Taimanov Line', 'e4 c5 Nf3 a6 d4 cxd4 Nxd4 e5 Nb3'),
        ('so-rare-nf6', 'Nimzowitsch Variation', 'e4 c5 Nf3 Nf6 Nc3 Nc6 d4 cxd4 Nxd4'),
        ('so-rare-nf6d6', 'Nimzowitsch Variation, then small d-pawn move', 'e4 c5 Nf3 Nf6 Nc3 d6 d4')],
  why='The O\'Kelly, the Nimzowitsch and the rest. Each has one move to know.', outcome='Better for you')

# ============================================================== notes
n('e4 c5 Nf3', 'Knight out', 'The d-pawn goes two squares next, and this knight takes back when Black trades it.', ['key'])
n('e4 c5 Nf3 d6 d4', 'D-pawn two squares', 'Open the middle. Black nearly always takes.', ['key'])
n('e4 c5 Nf3 d6 d4 cxd4 Nxd4', 'Knight takes back', 'It stands in the middle of the board, and nothing can chase it yet.', ['key'])
n('e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3', 'Queen\'s knight guards the e-pawn', 'The setup starts here: f-pawn, bishop, queen, castle long.', ['key'])
n('e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 a6 f3', 'F-pawn one square', 'It guards the e-pawn a second time and keeps Black\'s knight from jumping at the bishop that comes next.', ['key'], arrows=['c1e3g'])
n('e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 a6 f3 e5 Nb3', 'Knight steps back', 'The a-pawn guards the square in front, so the knight goes back toward the queenside. Black has left a hole in front of the d-pawn.', ['key'])
n('e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 a6 f3 e6 Be3', 'Bishop beside the queen', 'Behind the f-pawn nothing can chase it. The queen comes next, then the king castles long.', ['key'])
n('e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 a6 f3 e6 Be3 Be7 Qd2 O-O O-O-O', 'Castle long', 'The kings are on opposite wings, so your kingside pawns are free to run.', ['key'])
n('e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 a6 f3 e6 Be3 b5 Qd2 Bb7 O-O-O Nbd7 g4', 'G-pawn two squares', 'It is going on to hit the knight in front of Black\'s king. The edge pawn follows.', ['key'], arrows=['g4g5g'])
n('e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 g6 f3', 'F-pawn one square', 'The same move against the Dragon. Bishop and queen line up next, to trade off the bishop Black is about to put on the long diagonal.', ['key'])
n('e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 g6 f3 Bg7 Be3 O-O Qd2 Nc6 O-O-O', 'Castle long', 'The setup is done. The edge pawn is next, to open the file in front of Black\'s king.', ['key'])
n('e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 g6 f3 Bg7 Be3 O-O Qd2 Nc6 O-O-O d5 exd5', 'Take it', 'Black strikes in the middle before your pawns get going. Take, and the trades that follow leave you the safer king.', ['key'])
n('e4 c5 Nf3 Nc6 d4 cxd4 Nxd4 Nf6 Nc3 e5 Ndb5', 'Knight jumps forward', 'The square in front is free, and Black\'s e-pawn has left a hole behind it. The knight is headed there.', ['key'], arrows=['b5d6g'])
n('e4 c5 Nf3 Nc6 d4 cxd4 Nxd4 e5 Nb5', 'Knight jumps forward', 'The same jump a move earlier. The hole in front of Black\'s d-pawn is the target.', ['key'], arrows=['b5d6g'])
n('e4 c5 Nf3 Nc6 d4 cxd4 Nxd4 g6 Nc3 Bg7 Be3', 'Bishop first', 'Black\'s bishop is aimed at your knight in the middle, so the bishop guards it before the f-pawn moves.', ['key'])
n('e4 c5 Nf3 Nc6 d4 cxd4 Nxd4 g6 Nc3 Bg7 Be3 Nf6 Bc4', 'Bishop out before the f-pawn', 'Black saved a move with the d-pawn to push it two squares in one go. Your bishop stops that first.', ['key'])
n('e4 c5 Nf3 Nc6 d4 cxd4 Nxd4 g6 Nc3 Bg7 Be3 Nf6 Bc4 O-O Bb3', 'Bishop steps back', 'Out of reach of the tricks against the knight in the middle. Then the f-pawn, the queen, and castle long as usual.', ['key'])
n('e4 c5 Nf3 Nc6 d4 cxd4 Nxd4 Nxd4 Qxd4', 'Queen takes back', 'No knight is left to chase her, so she stands well in the middle.', ['key'])
n('e4 c5 Nf3 e6 d4 cxd4 Nxd4 Nc6 Nc3', 'Queen\'s knight out', 'The setup starts the same way against the small pawn moves.')
n('e4 c5 Nf3 g6 d4', 'D-pawn two squares', 'The same move against the early fianchetto.')
# the other side's moves that start a named line
n('e4 c5 Nf3 Nc6', 'Old Sicilian')
n('e4 c5 Nf3 Nf6', 'Nimzowitsch Variation')
n('e4 c5 Nf3 a6', 'O\'Kelly Variation')
n('e4 c5 Nf3 d6', 'Modern Variations')
n('e4 c5 Nf3 e6', 'French Variation')
n('e4 c5 Nf3 g6', 'Hyperaccelerated Dragon')
n('e4 c5 Nf3 Nc6 d4 e6', 'Franco-Sicilian Variation')
n('e4 c5 Nf3 a6 d4 e6', 'Drazic Variation')
n('e4 c5 Nf3 e6 d4 Nc6', 'Franco-Sicilian Variation')
n('e4 c5 Nf3 e6 d4 a6', 'Drazic Variation')
n('e4 c5 Nf3 e6 d4 d5', 'Marshall Counterattack')
n('e4 c5 Nf3 g6 d4 Bg7', 'Hyperaccelerated Pterodactyl')
n('e4 c5 Nf3 Nc6 d4 cxd4 Nxd4 e5', 'Löwenthal Variation')
n('e4 c5 Nf3 Nc6 d4 cxd4 Nxd4 e6', 'Taimanov Variation')
n('e4 c5 Nf3 Nc6 d4 cxd4 Nxd4 g6', 'Accelerated Dragon')
n('e4 c5 Nf3 a6 d4 cxd4 Nxd4 e5', 'Taimanov Line')
n('e4 c5 Nf3 d6 d4 cxd4 Nxd4 g6', 'Accelerated Dragon')
n('e4 c5 Nf3 e6 d4 cxd4 Nxd4 Bc5', 'Paulsen-Basman Defense')
n('e4 c5 Nf3 e6 d4 cxd4 Nxd4 Nc6', 'Taimanov Variation')
n('e4 c5 Nf3 e6 d4 cxd4 Nxd4 a6', 'Kan Variation')
n('e4 c5 Nf3 g6 d4 cxd4 Nxd4 Nc6', 'Accelerated Dragon')
n('e4 c5 Nf3 Nc6 d4 cxd4 Nxd4 Nf6 Nc3 e5', 'Lasker-Pelikan Variation')
n('e4 c5 Nf3 Nc6 d4 cxd4 Nxd4 Nf6 Nc3 e6', 'Four Knights Variation')
n('e4 c5 Nf3 Nc6 d4 cxd4 Nxd4 e5 Nb5 d6', 'Kalashnikov Variation')
n('e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 a6', 'Najdorf Variation')
n('e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 e6', 'Scheveningen Variation')
n('e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 g6', 'Dragon Variation')
n('e4 c5 Nf3 d6 d4 cxd4 Nxd4 a6 Nc3 Nf6', 'Najdorf Variation')
n('e4 c5 Nf3 e6 d4 cxd4 Nxd4 Nc6 Nc3 Nf6', 'Four Knights Variation')
n('e4 c5 Nf3 e6 d4 cxd4 Nxd4 Nf6 Nc3 Bb4', 'Pin Variation')
n('e4 c5 Nf3 e6 d4 cxd4 Nxd4 a6 Nc3 b5', 'Wing Attack')
n('e4 c5 Nf3 Nc6 d4 cxd4 Nxd4 g6 Nc3 Bg7 Be3 d6 f3 Nf6', 'Belezky Line')
n('e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 g6 f3 Bg7 Be3 Nc6', 'Belezky Line')
n('e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 g6 f3 Bg7 Be3 O-O', 'Yugoslav Attack')
n('e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 g6 f3 Bg7 Be3 O-O Qd2 Nc6', 'Yugoslav Attack')
