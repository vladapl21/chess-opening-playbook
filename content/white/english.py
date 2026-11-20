"""White from the side: the English Opening, a third pack for the slot 'white' (see PACKS in content2_meta.py).

One setup, one order: c-pawn two squares, queen's knight, g-pawn one square, bishop to the long diagonal, e-pawn two
squares, king's knight tucked in behind it, castle, small d-pawn move. When Black's d-pawn comes two squares, take it;
once the c-pawn is gone the e-pawn stays home and the king's knight comes out in front of the f-pawn. The lines were
drafted with pipeline/draft.py: Black's moves by the Maia 1300/1500 odds, yours from the setup's order wherever
Stockfish 17.1 accepts it and the engine's move elsewhere. SAN is internal; notes are plain English."""
from content import n, J, L, PARTS

PARTS.extend([
  dict(id='en-rev', ch='english', title="The e-pawn and the king's knight", kicker="King's English",
       blurb="Black takes the middle the way you would with White. C-pawn, knight, g-pawn, bishop, then the e-pawn two squares and the king's knight tucked in behind it."),
  dict(id='en-revside', ch='english', title='Other second moves', kicker='The early bishop, the other knight',
       blurb='Black changes the order. Yours stays the same, and one early queen move needs the small e-pawn move.'),
  dict(id='en-sym', ch='engsym', title='Black copies you', kicker='Symmetrical English',
       blurb='C-pawn against c-pawn. The setup comes out in the same order.'),
  dict(id='en-ind', ch='engsym', title='The knight and the fianchetto', kicker='Anglo-Indian',
       blurb="Black develops first and shows the pawns later. Against a fianchetto the whole setup; against the e-pawn one square, the king's knight comes out first."),
  dict(id='en-dp', ch='engrare', title="Black's d-pawn comes two squares", kicker='Anglo-Scandinavian, Agincourt, Caro-Kann setup',
       blurb='At once, or backed up by a pawn first. The rule is the same: take it.'),
  dict(id='en-rare', ch='engrare', title='Rare first moves', kicker='Sidelines',
       blurb='The small d-pawn, the f-pawn, the b-pawn. The setup does the work.'),
])

L('en-main', 'en-rev', 'The setup: fianchetto, then the e-pawn', 'Bishop to the long diagonal, e-pawn two squares, knight tucked in, castle', 'core',
  'c4 e5 Nc3 Nf6 g3 Nc6 Bg2 Bc5 e4 O-O Nge2 d6 O-O Bg4 d3',
  alts=[('en-main-bb4', 'Bishop comes at the knight', 'c4 e5 Nc3 Nf6 g3 Nc6 Bg2 Bb4 e4 Bxc3 bxc3 O-O d3 d6 h3'),
        ('en-main-bb4bxc3', 'Bishop comes at the knight, then bishop takes the knight', 'c4 e5 Nc3 Nf6 g3 Nc6 Bg2 Bb4 e4 Bxc3 bxc3 d6 d3 Bg4 Nf3'),
        ('en-main-b6', 'Small b-pawn move', 'c4 e5 Nc3 Nf6 g3 Nc6 Bg2 b6 Nf3 Bb7 Nxe5 Nxe5 Bxb7 Rb8 Bg2'),
        ('en-main-d6', 'Small d-pawn move', 'c4 e5 Nc3 Nf6 g3 Nc6 Bg2 Bc5 e4 d6 h3 Be6 d3 Qd7 Nge2'),
        ('en-main-bb4oo', 'Bishop comes at the knight, then castles', 'c4 e5 Nc3 Nf6 g3 Nc6 Bg2 Bb4 e4 O-O Nge2 d6 O-O Bg4 d3'),
        ('en-main-d6be6', 'Small d-pawn move, then bishop behind the center pawns', 'c4 e5 Nc3 Nf6 g3 Nc6 Bg2 d6 e4 Be6 d3 Be7 Nge2 O-O O-O'),
        ('en-main-d6bg4', 'Small d-pawn move, then bishop out to the side', 'c4 e5 Nc3 Nf6 g3 Nc6 Bg2 d6 e4 Bg4 Nge2 Nd4 d3 Nxe2 Nxe2 Be7 O-O')],
  why='Four in ten club players answer with the e-pawn, and both knights usually follow. The whole setup comes out here, in its usual order.', outcome='A slow game on your terms')
L('en-open', 'en-rev', 'Black opens the middle', 'Take the d-pawn; then the king\'s knight comes out the usual way', 'core',
  'c4 e5 Nc3 Nf6 g3 d5 cxd5 Nxd5 Bg2 Nxc3 bxc3 Nc6 Nf3 Bd6 O-O',
  alts=[('en-open-be6', 'Bishop behind the center pawns', 'c4 e5 Nc3 Nf6 g3 d5 cxd5 Nxd5 Bg2 Be6 Nf3 Nc6 O-O Qd7 Ng5'),
        ('en-open-c6', 'Small c-pawn move', 'c4 e5 Nc3 Nf6 g3 d5 cxd5 Nxd5 Bg2 Nxc3 bxc3 c6 Nf3 Bd6 O-O'),
        ('en-open-bc5', 'Bishop aims at f2', 'c4 e5 Nc3 Nf6 g3 d5 cxd5 Nxd5 Bg2 Nxc3 bxc3 Bc5 Nf3 Nc6 O-O'),
        ('en-open-c6v2', 'Small c-pawn move on move 5', 'c4 e5 Nc3 Nf6 g3 d5 cxd5 Nxd5 Bg2 c6 Nf3 Nxc3 bxc3'),
        ('en-open-bd6', 'Bishop to the middle', 'c4 e5 Nc3 Nf6 g3 d5 cxd5 Nxd5 Bg2 Nxc3 bxc3 Bd6 Nf3 O-O O-O Nc6 d3')],
  why='One in five pushes the d-pawn at once. Take it, and your bishop\'s diagonal is wide open.', outcome='Equal, with an open diagonal')
L('en-bb4', 'en-rev', 'The bishop comes at your knight', 'Carry on; if it takes, the b-pawn takes back', 'common',
  'c4 e5 Nc3 Nf6 g3 Bb4 Bg2 Bxc3 bxc3 O-O e4 d6 d3 Bg4 Ne2',
  alts=[('en-bb4-nc6', 'Queen\'s knight out', 'c4 e5 Nc3 Nf6 g3 Bb4 Bg2 Nc6 e4'),
        ('en-bb4-oo', 'Castles', 'c4 e5 Nc3 Nf6 g3 Bb4 Bg2 O-O e4 Bxc3 bxc3'),
        ('en-bb4-nc6v2', 'Queen\'s knight out on move 5', 'c4 e5 Nc3 Nf6 g3 Bb4 Bg2 Bxc3 bxc3 Nc6 e4'),
        ('en-bb4-oonc6', 'Castles, then queen\'s knight out', 'c4 e5 Nc3 Nf6 g3 Bb4 Bg2 O-O e4 Nc6 Nge2'),
        ('en-bb4-c6', 'Small c-pawn move', 'c4 e5 Nc3 Nf6 g3 Bb4 Bg2 c6 e4 O-O Nge2'),
        ('en-bb4-d6', 'Small d-pawn move', 'c4 e5 Nc3 Nf6 g3 Bb4 Bg2 d6 Qa4+ Nc6 Bxc6+ bxc6 Qxb4 c5 Qa4+ Bd7 Qd1'),
        ('en-bb4-d5', 'D-pawn two squares', 'c4 e5 Nc3 Nf6 g3 Bb4 Bg2 Bxc3 bxc3 d5 cxd5 Nxd5 Nf3 Nc6 O-O'),
        ('en-bb4-c6v2', 'Small c-pawn move on move 5', 'c4 e5 Nc3 Nf6 g3 Bb4 Bg2 Bxc3 bxc3 c6 e4 d5 cxd5 cxd5 exd5 Nxd5 Ba3'),
        ('en-bb4-d6v2', 'Small d-pawn move on move 5', 'c4 e5 Nc3 Nf6 g3 Bb4 Bg2 Bxc3 bxc3 d6 e4 O-O d3'),
        ('en-bb4-ood6', 'Castles, then small d-pawn move', 'c4 e5 Nc3 Nf6 g3 Bb4 Bg2 O-O e4 d6 Nge2 Bg4 O-O Nc6 d3'),
        ('en-bb4-ooc6', 'Castles, then small c-pawn move', 'c4 e5 Nc3 Nf6 g3 Bb4 Bg2 O-O e4 c6 Nge2 d5 cxd5 cxd5 exd5 Bxc3 dxc3 Bg4 O-O')],
  why='One in five brings the bishop out to trade it for your knight. Let it: you get the two bishops and another pawn for the middle.', outcome='Slightly better for you')
L('en-bc5', 'en-rev', 'The bishop aims at f2', 'Bishop out, then the small e-pawn move if the knight jumps', 'common',
  'c4 e5 Nc3 Nf6 g3 Bc5 Bg2 O-O e4 d6 Nge2 Bg4 O-O Nc6 d3',
  alts=[('en-bc5-nc6', 'Queen\'s knight out', 'c4 e5 Nc3 Nf6 g3 Bc5 Bg2 Nc6 e4'),
        ('en-bc5-nc6v2', 'Queen\'s knight out on move 5', 'c4 e5 Nc3 Nf6 g3 Bc5 Bg2 O-O e4 Nc6 Nge2'),
        ('en-bc5-c6', 'Keres Variation', 'c4 e5 Nc3 Nf6 g3 Bc5 Bg2 c6 e4 O-O Nge2'),
        ('en-bc5-ng4', 'Knight jumps forward', 'c4 e5 Nc3 Nf6 g3 Bc5 Bg2 Ng4 e3 Qf6 Qxg4 O-O Qe2'),
        ('en-bc5-ng4d6', 'Knight jumps forward, then small d-pawn move', 'c4 e5 Nc3 Nf6 g3 Bc5 Bg2 Ng4 e3 d6 Nge2 Qf6 O-O Qh6 h3'),
        ('en-bc5-c6d6', 'Keres Variation, then small d-pawn move', 'c4 e5 Nc3 Nf6 g3 Bc5 Bg2 c6 e4 d6 Nge2 Ng4 O-O Qf6 Qe1'),
        ('en-bc5-c6v2', 'Small c-pawn move', 'c4 e5 Nc3 Nf6 g3 Bc5 Bg2 O-O e4 c6 Nge2 d5 cxd5 cxd5 exd5 Ng4 O-O'),
        ('en-bc5-d6', 'Small d-pawn move', 'c4 e5 Nc3 Nf6 g3 Bc5 Bg2 d6 d3 Nc6 e3 O-O Nge2 Bg4 h3')],
  why='One in five aims the bishop at f2. Your setup doesn\'t change; one knight jump needs a careful answer.', outcome='Equal')
L('en-3rd', 'en-rev', 'Other third moves', 'The c-pawn gets ready for the d-pawn: go at the e-pawn first', 'common',
  'c4 e5 Nc3 Nf6 g3 c6 Nf3 d5 cxd5 cxd5 Nxe5 d4 Qa4+ Bd7 Qxd4 Nc6 Nxc6 Bxc6 Qxd8+',
  alts=[('en-3rd-e4', 'Small e-pawn move', 'c4 e5 Nc3 Nf6 g3 c6 Nf3 e4 Nd4 d5 cxd5 cxd5 d3 Bc5 dxe4 dxe4 Be3'),
        ('en-3rd-d6', 'Small d-pawn move', 'c4 e5 Nc3 Nf6 g3 c6 Nf3 d6 Bg2 Be7 O-O O-O d3 h6 e4')],
  why='One in twelve plays the c-pawn one square here, to push the d-pawn next. Your king\'s knight goes at the e-pawn before that happens.', outcome='Equal')
L('en-nc6', 'en-revside', 'Queen\'s knight first', 'The same setup, by another road', 'common',
  'c4 e5 Nc3 Nc6 g3 d6 Bg2 Bd7 e4 Nf6 Nge2 Be7 O-O O-O d3',
  alts=[('en-nc6-nf6', 'King\'s knight out', 'c4 e5 Nc3 Nc6 g3 Nf6 Bg2 Bc5 e4'),
        ('en-nc6-nf6bb4', 'King\'s knight out, then bishop comes at the knight', 'c4 e5 Nc3 Nc6 g3 Nf6 Bg2 Bb4 e4'),
        ('en-nc6-nf6d6', 'King\'s knight out, then small d-pawn move', 'c4 e5 Nc3 Nc6 g3 Nf6 Bg2 d6 e4'),
        ('en-nc6-bc5', 'Bishop aims at f2', 'c4 e5 Nc3 Nc6 g3 Bc5 Bg2 Nf6 e4'),
        ('en-nc6-nf6v2', 'King\'s knight out on move 4', 'c4 e5 Nc3 Nc6 g3 d6 Bg2 Nf6 e4'),
        ('en-nc6-bb4', 'Bishop comes at the knight', 'c4 e5 Nc3 Nc6 g3 Bb4 Bg2 Nf6 e4'),
        ('en-nc6-bb4bxc3', 'Bishop comes at the knight, then bishop takes the knight', 'c4 e5 Nc3 Nc6 g3 Bb4 Bg2 Bxc3 bxc3 Nf6 e4'),
        ('en-nc6-bc5d6', 'Bishop aims at f2, then small d-pawn move', 'c4 e5 Nc3 Nc6 g3 Bc5 Bg2 d6 d3 Nf6 e3'),
        ('en-nc6-bc5qf6', 'Bishop aims at f2, then queen comes out', 'c4 e5 Nc3 Nc6 g3 Bc5 Bg2 Qf6 e3 Nge7 Ne4 Qg6 Nxc5 d6 Ne4')],
  why='One in seven brings the other knight out first. Nothing changes for you.', outcome='Equal')
L('en-2bc5', 'en-revside', 'The early bishop and the queen', 'G-pawn, then the small e-pawn move when the queen comes at f2', 'common',
  'c4 e5 Nc3 Bc5 g3 Qf6 e3 Ne7 Bg2 O-O Nge2 c6 Ne4',
  alts=[('en-2bc5-nf6', 'King\'s knight out', 'c4 e5 Nc3 Bc5 g3 Nf6 Bg2'),
        ('en-2bc5-nc6', 'Queen\'s knight out', 'c4 e5 Nc3 Bc5 g3 Nc6 Bg2'),
        ('en-2bc5-d6', 'Small d-pawn move', 'c4 e5 Nc3 Bc5 g3 d6 Bg2 Nf6 d3'),
        ('en-2bc5-d6nc6', 'Small d-pawn move, then queen\'s knight out', 'c4 e5 Nc3 Bc5 g3 d6 Bg2 Nc6 d3'),
        ('en-2bc5-c6', 'Small c-pawn move', 'c4 e5 Nc3 Bc5 g3 c6 Bg2 Nf6 e4'),
        ('en-2bc5-nc6v2', 'Queen\'s knight out on move 4', 'c4 e5 Nc3 Bc5 g3 Qf6 e3 Nc6 Bg2'),
        ('en-2bc5-c6v2', 'Small c-pawn move on move 4', 'c4 e5 Nc3 Bc5 g3 Qf6 e3 c6 Bg2 d6 Nge2'),
        ('en-2bc5-nh6', 'King\'s knight to the edge', 'c4 e5 Nc3 Bc5 g3 Qf6 e3 Nh6 Bg2 Ng4 Qxg4'),
        ('en-2bc5-d6v2', 'Small d-pawn move on move 4', 'c4 e5 Nc3 Bc5 g3 Qf6 e3 d6 Bg2 c6 Nge2 Bg4 O-O Ne7 d4'),
        ('en-2bc5-d6c6', 'Small d-pawn move, then small c-pawn move', 'c4 e5 Nc3 Bc5 g3 d6 Bg2 c6 d3 Nf6 Nf3 O-O O-O Bg4 h3')],
  why='One in eight brings the bishop out on move two, often with the queen behind it aiming at f2.', outcome='Equal or better')
L('en-2nd', 'en-revside', 'Other second moves', 'The bishop at your knight, the small d-pawn, the c-pawn', 'common',
  'c4 e5 Nc3 d6 g3 Nf6 Bg2 Be7 e4 O-O Nge2 Nc6 O-O Bg4 d3',
  alts=[('en-2nd-bb4', 'Kramnik-Shirov Counterattack', 'c4 e5 Nc3 Bb4 g3 Bxc3 bxc3 Nf6 Bg2'),
        ('en-2nd-nc6', 'Queen\'s knight out', 'c4 e5 Nc3 d6 g3 Nc6 Bg2'),
        ('en-2nd-bb4nf6', 'Kramnik-Shirov Counterattack, then Smyslov System', 'c4 e5 Nc3 Bb4 g3 Nf6 Bg2'),
        ('en-2nd-nc6v2', 'Queen\'s knight out on move 4', 'c4 e5 Nc3 d6 g3 Nf6 Bg2 Nc6 e4'),
        ('en-2nd-bb4bxc3', 'Kramnik-Shirov Counterattack, then bishop takes the knight', 'c4 e5 Nc3 Bb4 g3 Bxc3 bxc3 Nc6 Bg2'),
        ('en-2nd-bb4nc6', 'Kramnik-Shirov Counterattack, then queen\'s knight out', 'c4 e5 Nc3 Bb4 g3 Nc6 Bg2'),
        ('en-2nd-bb4bxc3d6', 'Kramnik-Shirov Counterattack, then bishop takes the knight, then small d-pawn move', 'c4 e5 Nc3 Bb4 g3 Bxc3 bxc3 d6 Bg2 Nf6 e4'),
        ('en-2nd-c6', 'Keres Defense', 'c4 e5 Nc3 d6 g3 c6 Bg2 Nf6 e4'),
        ('en-2nd-c6d6', 'Small c-pawn move, then small d-pawn move', 'c4 e5 Nc3 c6 Nf3 d6 d4 exd4 Nxd4 Nf6 g3 Be7 Bg2 O-O e4'),
        ('en-2nd-bb4d6', 'Kramnik-Shirov Counterattack, then small d-pawn move', 'c4 e5 Nc3 Bb4 g3 d6 Bg2 Nf6 Qa4+'),
        ('en-2nd-bb4bxc3d5', 'Kramnik-Shirov Counterattack, then bishop takes the knight, then d-pawn two squares', 'c4 e5 Nc3 Bb4 g3 Bxc3 bxc3 d5 cxd5 Qxd5 Nf3 e4 Nd4 e3 f3'),
        ('en-2nd-c6d5', 'Small c-pawn move, then d-pawn two squares', 'c4 e5 Nc3 c6 Nf3 d5 cxd5 cxd5 Nxe5 d4 Qa4+ Bd7 Qxd4 Nc6 Qxd7+ Qxd7 Nxd7 Kxd7 g3'),
        ('en-2nd-be6', 'Bishop behind the center pawns', 'c4 e5 Nc3 d6 g3 Be6 Bg2 c6 d3 Nf6 e4 Be7 Nge2 O-O O-O'),
        ('en-2nd-c6v2', 'Small c-pawn move', 'c4 e5 Nc3 d6 g3 Nf6 Bg2 c6 e4 Be7 Nge2 O-O O-O Bg4 d3'),
        ('en-2nd-c6d6nd7', 'Small c-pawn move, then small d-pawn move, then queen\'s knight tucked in', 'c4 e5 Nc3 c6 Nf3 d6 d4 Nd7 g3 Ngf6 Bg2 Be7 O-O O-O e4'),
        ('en-2nd-c6f6', 'Small c-pawn move, then small f-pawn move', 'c4 e5 Nc3 c6 Nf3 f6 d4 exd4 Nxd4 Bc5 Nf5 Kf7 Nd6+ Bxd6 Qxd6 Ne7 e4'),
        ('en-2nd-c6bd6', 'Small c-pawn move, then bishop to the middle', 'c4 e5 Nc3 c6 Nf3 Bd6 d4 exd4 Qxd4 Qf6 Qd3 Bb4 Bd2 Ne7 a3')],
  why='The bishop on move two, the small d-pawn move, and the c-pawn that gets ready to push the d-pawn.', outcome='Equal')
L('en-sym', 'en-sym', 'The Symmetrical', 'The same setup; Black often copies it', 'core',
  'c4 c5 Nc3 Nc6 g3 g6 Bg2 Bg7 e4 e6 Nge2 Nge7 O-O O-O d3 a6 Be3',
  alts=[('en-sym-nf6', 'King\'s knight out', 'c4 c5 Nc3 Nc6 g3 Nf6 Bg2'),
        ('en-sym-nf6v2', 'King\'s knight out on move 2', 'c4 c5 Nc3 Nf6 g3'),
        ('en-sym-d6', 'Small d-pawn move', 'c4 c5 Nc3 d6 g3 Nc6 Bg2'),
        ('en-sym-e6', 'Small e-pawn move', 'c4 c5 Nc3 Nc6 g3 e6 Bg2 Nf6 e4'),
        ('en-sym-e6nf6', 'Small e-pawn move, then king\'s knight out', 'c4 c5 Nc3 e6 Nf3 Nf6 g3'),
        ('en-sym-g6', 'Small g-pawn move', 'c4 c5 Nc3 g6 g3 Bg7 Bg2 Nc6 e4'),
        ('en-sym-e6nc6', 'Small e-pawn move, then queen\'s knight out', 'c4 c5 Nc3 e6 Nf3 Nc6 g3 Nf6 Bg2'),
        ('en-sym-e5', 'E-pawn two squares', 'c4 c5 Nc3 e5 g3 d6 Bg2'),
        ('en-sym-d6nf6', 'Small d-pawn move, then king\'s knight out', 'c4 c5 Nc3 d6 g3 Nf6 Bg2 Nc6 d3'),
        ('en-sym-d6nf6g6', 'Small d-pawn move, then king\'s knight out, then small g-pawn move', 'c4 c5 Nc3 d6 g3 Nf6 Bg2 g6 e4 Bg7 Nge2 O-O O-O'),
        ('en-sym-d6v2', 'Small d-pawn move on move 5', 'c4 c5 Nc3 Nc6 g3 g6 Bg2 Bg7 e4 d6 Nge2 Nf6 O-O O-O d3'),
        ('en-sym-d6g6', 'Small d-pawn move, then small g-pawn move', 'c4 c5 Nc3 d6 g3 g6 Bg2 Bg7 e4 Nf6 Nge2'),
        ('en-sym-e5d6', 'E-pawn two squares, then small d-pawn move', 'c4 c5 Nc3 Nc6 g3 e5 Bg2 d6 e4 Nf6 Nge2'),
        ('en-sym-e5nf6', 'E-pawn two squares, then king\'s knight out', 'c4 c5 Nc3 e5 g3 Nf6 Bg2 Nc6 e4'),
        ('en-sym-d6nf6v2', 'Small d-pawn move, then king\'s knight out on move 3', 'c4 c5 Nc3 Nc6 g3 d6 Bg2 Nf6 d3 g6 e4 Bg7 Nge2 O-O O-O'),
        ('en-sym-nf6v3', 'King\'s knight out on move 5', 'c4 c5 Nc3 Nc6 g3 g6 Bg2 Bg7 e4 Nf6 Nge2 O-O O-O d6 d3'),
        ('en-sym-e6d5', 'Small e-pawn move, then d-pawn two squares', 'c4 c5 Nc3 Nc6 g3 e6 Bg2 d5 cxd5 exd5 Bxd5 Nf6 Bg2 Be7 Nf3'),
        ('en-sym-g6nf6', 'Small g-pawn move, then king\'s knight out', 'c4 c5 Nc3 g6 g3 Bg7 Bg2 Nf6 e4 O-O Nge2 Nc6 O-O'),
        ('en-sym-d6bd7', 'Small d-pawn move, then bishop beside the queen', 'c4 c5 Nc3 Nc6 g3 d6 Bg2 Bd7 e4 Nf6 Nge2 g6 O-O Bg7 d3'),
        ('en-sym-e5nf6v2', 'E-pawn two squares, then king\'s knight out on move 3', 'c4 c5 Nc3 Nc6 g3 e5 Bg2 Nf6 e4 d6 Nge2 Bg4 O-O Nd4 d3'),
        ('en-sym-e6d5v2', 'Small e-pawn move, then d-pawn two squares on move 2', 'c4 c5 Nc3 e6 Nf3 d5 cxd5 exd5 d4 c4 e4 Bb4 exd5 Qxd5 Be2'),
        ('en-sym-d6e6', 'Small d-pawn move, then small e-pawn move', 'c4 c5 Nc3 d6 g3 e6 Bg2 Nf6 e4 Be7 Nge2 O-O O-O Nc6 d3'),
        ('en-sym-d6e5', 'Small d-pawn move, then e-pawn two squares', 'c4 c5 Nc3 d6 g3 e5 Bg2 Nf6 e4 Be7 Nge2 O-O O-O Nc6 d3'),
        ('en-sym-e6a6', 'Small e-pawn move, then small a-pawn move', 'c4 c5 Nc3 e6 Nf3 a6 g3 Nc6 Bg2 Nf6 O-O Be7 d3 O-O d4')],
  why='One in ten copies your first move. Your setup comes out move for move.', outcome='Equal, and you know the plan')
L('en-nf6', 'en-ind', 'Knight first', 'Against the fianchetto the whole setup; against the e-pawn one square, the king\'s knight first', 'core',
  'c4 Nf6 Nc3 g6 g3 Bg7 Bg2 O-O e4 d6 Nge2 c5 O-O Nc6 d3',
  alts=[('en-nf6-e5', 'Two Knights Variation', 'c4 Nf6 Nc3 e5 g3 Bb4 Bg2'),
        ('en-nf6-e5d5', 'Two Knights Variation, then Reversed Dragon', 'c4 Nf6 Nc3 e5 g3 d5 cxd5'),
        ('en-nf6-e5bc5', 'Two Knights Variation, then bishop aims at f2', 'c4 Nf6 Nc3 e5 g3 Bc5 Bg2'),
        ('en-nf6-e5nc6', 'Two Knights Variation, then queen\'s knight out', 'c4 Nf6 Nc3 e5 g3 Nc6 Bg2'),
        ('en-nf6-nc6', 'Queen\'s knight out', 'c4 Nf6 Nc3 Nc6 g3 e5 Bg2'),
        ('en-nf6-e5v2', 'E-pawn two squares', 'c4 Nf6 Nc3 g6 g3 Bg7 Bg2 O-O e4 e5 Nge2 d6 O-O'),
        ('en-nf6-d6', 'Small d-pawn move', 'c4 Nf6 Nc3 d6 g3 g6 Bg2 Bg7 d3'),
        ('en-nf6-e5c6', 'Two Knights Variation, then Keres Variation', 'c4 Nf6 Nc3 e5 g3 c6 Nf3'),
        ('en-nf6-nc6d5', 'Queen\'s knight out, then d-pawn two squares', 'c4 Nf6 Nc3 Nc6 g3 d5 cxd5 Nxd5 Bg2'),
        ('en-nf6-e5d6', 'Two Knights Variation, then small d-pawn move', 'c4 Nf6 Nc3 e5 g3 d6 Bg2'),
        ('en-nf6-d5', 'Anglo-Grünfeld Defense', 'c4 Nf6 Nc3 d5 cxd5 Nxd5 g3 Nxc3 bxc3 e5 Bg2'),
        ('en-nf6-e5v3', 'E-pawn two squares on move 6', 'c4 Nf6 Nc3 g6 g3 Bg7 Bg2 O-O e4 d6 Nge2 e5 O-O Nc6 d3'),
        ('en-nf6-nbd7', 'Queen\'s knight tucked in', 'c4 Nf6 Nc3 g6 g3 Bg7 Bg2 O-O e4 d6 Nge2 Nbd7 O-O e5 d3'),
        ('en-nf6-nc6v2', 'Queen\'s knight out on move 6', 'c4 Nf6 Nc3 g6 g3 Bg7 Bg2 O-O e4 d6 Nge2 Nc6 O-O Bg4 d3'),
        ('en-nf6-bg4', 'Bishop pins the knight', 'c4 Nf6 Nc3 g6 g3 Bg7 Bg2 O-O e4 d6 Nge2 Bg4 d4 Nbd7 f3'),
        ('en-nf6-d6v2', 'Small d-pawn move on move 4', 'c4 Nf6 Nc3 g6 g3 Bg7 Bg2 d6 d3 O-O e4 e5 Nge2 Nc6 O-O'),
        ('en-nf6-d5nc6', 'Anglo-Grünfeld Defense, then queen\'s knight out', 'c4 Nf6 Nc3 d5 cxd5 Nxd5 g3 Nc6 Bg2 Nxc3 bxc3 e5 Nf3'),
        ('en-nf6-e6', 'Hedgehog System', 'c4 Nf6 Nc3 e6 Nf3 Bb4 g3 Bxc3 bxc3 O-O Bg2 d5 cxd5 exd5 O-O'),
        ('en-nf6-e6d5', 'Hedgehog System, then d-pawn two squares', 'c4 Nf6 Nc3 e6 Nf3 d5 cxd5 Nxd5 g3 Nxc3 bxc3 Nc6 Bg2 Bd7 O-O'),
        ('en-nf6-c6', 'Small c-pawn move', 'c4 Nf6 Nc3 g6 g3 Bg7 Bg2 c6 e4 d6 Nge2 O-O O-O Nbd7 d3'),
        ('en-nf6-d5e6', 'Anglo-Grünfeld Defense, then small e-pawn move', 'c4 Nf6 Nc3 d5 cxd5 Nxd5 g3 e6 Bg2 Nxc3 bxc3 Nc6 Nf3'),
        ('en-nf6-e6d5exd5', 'Hedgehog System, then d-pawn two squares, then pawn takes back', 'c4 Nf6 Nc3 e6 Nf3 d5 cxd5 exd5 d4 Bb4 Bg5 O-O Qb3 Bxc3+ Qxc3 Nc6 Ne5'),
        ('en-nf6-e6be7', 'Hedgehog System, then bishop to the quiet square', 'c4 Nf6 Nc3 e6 Nf3 Be7 e4 O-O e5 Ne8 d4 d6 Bd3 dxe5 dxe5 Nc6 a3'),
        ('en-nf6-c5', 'C-pawn two squares', 'c4 Nf6 Nc3 c5 g3 Nc6 Bg2 e6 e4 Be7 Nge2 O-O O-O b6 d3'),
        ('en-nf6-e6bb4', 'Hedgehog System, then Nimzo-English', 'c4 Nf6 Nc3 e6 Nf3 Bb4 g3 O-O Bg2 d5 cxd5 exd5 a3 Bxc3 dxc3 c6 Qc2'),
        ('en-nf6-e6c5', 'Hedgehog System, then c-pawn two squares', 'c4 Nf6 Nc3 e6 Nf3 c5 g3 Nc6 Bg2 d5 cxd5 exd5 d4 cxd4 Nxd4 Nxd4 Qxd4 Be6 O-O')],
  why='One in nine starts with the knight and chooses a setup later. Yours is the same against all of them.', outcome='Equal')
L('en-g6', 'en-ind', 'The fianchetto at once', 'Bishop against bishop on the long diagonals', 'rare',
  'c4 g6 Nc3 Bg7 g3 e6 Bg2 Ne7 d3 O-O e4 c6 Nge2 d5 cxd5 cxd5 exd5 exd5 O-O',
  alts=[('en-g6-nf6', 'King\'s knight out', 'c4 g6 Nc3 Bg7 g3 Nf6 Bg2'),
        ('en-g6-d6', 'Small d-pawn move', 'c4 g6 Nc3 Bg7 g3 d6 Bg2 Nf6 d3'),
        ('en-g6-c6', 'Small c-pawn move', 'c4 g6 Nc3 Bg7 g3 c6 Bg2 Nf6 e4'),
        ('en-g6-b6', 'Small b-pawn move', 'c4 g6 Nc3 Bg7 g3 b6 Bg2 Nc6 e4 Bb7 Nge2 e6 O-O Nge7 d3'),
        ('en-g6-b6c6', 'Small b-pawn move, then small c-pawn move', 'c4 g6 Nc3 Bg7 g3 b6 Bg2 c6 d4 Bb7 e4 e6 h4 Ne7 Nge2')],
  why='Black fianchettoes first. The same eight moves.', outcome='Equal')
L('en-d5', 'en-dp', 'The d-pawn at once', 'Take it; when the queen takes back, the knight comes out with tempo', 'core',
  'c4 d5 cxd5 Qxd5 Nc3 Qd8 Nf3 Nf6 d4 e6 e4 Bb4 Bd3 O-O e5',
  alts=[('en-d5-nf6', 'Schulz Gambit', 'c4 d5 cxd5 Nf6 Nc3'),
        ('en-d5-e6', 'Small e-pawn move', 'c4 d5 cxd5 Qxd5 Nc3 Qd8 Nf3 e6 e4 Nf6 d4'),
        ('en-d5-nc6', 'Queen\'s knight out', 'c4 d5 cxd5 Qxd5 Nc3 Qd8 Nf3 Nc6 d4 Nf6 e4'),
        ('en-d5-qa5', 'Malvinas Variation', 'c4 d5 cxd5 Qxd5 Nc3 Qa5 g3 c6 Bg2 Nf6 Nf3'),
        ('en-d5-nc6bg4', 'Queen\'s knight out, then bishop comes at the knight', 'c4 d5 cxd5 Qxd5 Nc3 Qd8 Nf3 Nc6 d4 Bg4 d5 Bxf3 exf3 Ne5 Bf4'),
        ('en-d5-nc6e6', 'Queen\'s knight out, then small e-pawn move', 'c4 d5 cxd5 Qxd5 Nc3 Qd8 Nf3 Nc6 d4 e6 a3 Nf6 e4 Be7 Be3'),
        ('en-d5-nc6v2', 'Queen\'s knight out on move 5', 'c4 d5 cxd5 Qxd5 Nc3 Qd8 Nf3 Nf6 d4 Nc6 e4 Bg4 d5 Ne5 Nxe5 Bxd1 Bb5+ c6 dxc6'),
        ('en-d5-bf5', 'Light bishop out', 'c4 d5 cxd5 Qxd5 Nc3 Qd8 Nf3 Bf5 e4 Bg6 h4 h5 Ne5 Bh7 Qb3'),
        ('en-d5-bg4', 'Bishop comes at the knight', 'c4 d5 cxd5 Qxd5 Nc3 Qd8 Nf3 Bg4 Qb3 Bxf3 gxf3 b6 Bg2 c6 O-O'),
        ('en-d5-qa5nf6', 'Malvinas Variation, then king\'s knight out', 'c4 d5 cxd5 Qxd5 Nc3 Qa5 g3 Nf6 Bg2 c6 Nf3 Bg4 O-O e6 d3'),
        ('en-d5-e6bb4', 'Small e-pawn move, then bishop comes at the knight', 'c4 d5 cxd5 Qxd5 Nc3 Qd8 Nf3 e6 e4 Bb4 Qa4+ Nc6 Bb5 Bd7 Bxc6 Bxc6 Qxb4 Nf6 O-O'),
        ('en-d5-bg4b6', 'Bishop comes at the knight, then small b-pawn move', 'c4 d5 cxd5 Qxd5 Nc3 Qd8 Nf3 Bg4 Qb3 b6 Ng5 e6 Qa4+ c6 Qxg4 Nf6 Qf3'),
        ('en-d5-bg4v2', 'Bishop comes at the knight on move 5', 'c4 d5 cxd5 Qxd5 Nc3 Qd8 Nf3 Nf6 d4 Bg4 Qb3 b6 e4 Bxf3 gxf3 Qxd4 Be3'),
        ('en-d5-qa5nc6', 'Malvinas Variation, then queen\'s knight out', 'c4 d5 cxd5 Qxd5 Nc3 Qa5 g3 Nc6 Bg2 Bd7 Nf3 O-O-O O-O e5 d3'),
        ('en-d5-qa5bf5', 'Malvinas Variation, then light bishop out', 'c4 d5 cxd5 Qxd5 Nc3 Qa5 g3 Bf5 Bg2 c6 Nf3 e6 O-O Nd7 d3'),
        ('en-d5-qd6', 'Queen steps back', 'c4 d5 cxd5 Qxd5 Nc3 Qd6 Nf3 Nf6 d4 Bg4 Ne5 Nc6 Nxg4 Nxg4 d5'),
        ('en-d5-qa5e6', 'Malvinas Variation, then small e-pawn move', 'c4 d5 cxd5 Qxd5 Nc3 Qa5 g3 e6 Bg2 c6 Nf3 Nf6 O-O Be7 d4'),
        ('en-d5-qa5e5', 'Malvinas Variation, then e-pawn two squares', 'c4 d5 cxd5 Qxd5 Nc3 Qa5 g3 e5 Bg2 c6 Nf3 Nf6 O-O Bd6 d4')],
  why='One in ten pushes the d-pawn on move one. Take it: the queen that takes back loses time to your knight.', outcome='Better for you')
L('en-e6', 'en-dp', 'The e-pawn one square', 'Knight, then take the d-pawn when it comes', 'common',
  'c4 e6 Nc3 d5 cxd5 exd5 d4 Nf6 Bg5 Be7 e3 O-O Bd3 h6 Bh4',
  alts=[('en-e6-nf6', 'Hedgehog System', 'c4 e6 Nc3 Nf6 Nf3'),
        ('en-e6-c5', 'C-pawn two squares', 'c4 e6 Nc3 c5 Nf3'),
        ('en-e6-c5v2', 'Tarrasch Defense', 'c4 e6 Nc3 d5 cxd5 exd5 d4 c5 Nf3'),
        ('en-e6-bb4', 'Bishop pins the knight', 'c4 e6 Nc3 d5 cxd5 exd5 d4 Bb4 a3 Bxc3+ bxc3 Nf6 e3 O-O Bd3'),
        ('en-e6-h6', 'Small h-pawn move', 'c4 e6 Nc3 d5 cxd5 exd5 d4 Nf6 Bg5 h6 Bxf6 Qxf6 Nxd5 Qd6 Nc3'),
        ('en-e6-c6', 'Small c-pawn move', 'c4 e6 Nc3 d5 cxd5 exd5 d4 c6 Bf4 Nf6 e3 Bd6 Bxd6 Qxd6 Bd3'),
        ('en-e6-nc6', 'Queen\'s knight out', 'c4 e6 Nc3 d5 cxd5 exd5 d4 Nc6 Nf3 Nf6 Bg5 Be7 e3 O-O Bd3'),
        ('en-e6-b6', 'Small b-pawn move', 'c4 e6 Nc3 b6 g3 Bb7 e4 Bb4 Bg2 Bxc3 bxc3 Nf6 d3 O-O f4'),
        ('en-e6-bb4v2', 'Bishop pins the knight on move 5', 'c4 e6 Nc3 d5 cxd5 exd5 d4 Nf6 Bg5 Bb4 e3 O-O Bd3 h6 Bh4'),
        ('en-e6-b6nf6', 'Small b-pawn move, then king\'s knight out', 'c4 e6 Nc3 b6 g3 Bb7 e4 Nf6 Bg2 Bb4 Nge2 Bxc3 Nxc3 O-O O-O'),
        ('en-e6-c6v2', 'Small c-pawn move on move 2', 'c4 e6 Nc3 c6 g3 d5 cxd5 cxd5 Nf3 Nf6 d4 Bb4 Bg2 O-O Bf4'),
        ('en-e6-bb4v3', 'Bishop comes at the knight', 'c4 e6 Nc3 Bb4 g3 Bxc3 bxc3 Nf6 Bg2 O-O e4 d6 d3 e5 Ne2'),
        ('en-e6-d6', 'Small d-pawn move', 'c4 e6 Nc3 d6 g3 Be7 Bg2 Nf6 e4 O-O Nge2 Nc6 O-O e5 d3')],
  why='One in eleven gets ready for the d-pawn push. When it comes, take it and put your own d-pawn in the middle.', outcome='Equal')
L('en-c6', 'en-dp', 'The c-pawn one square', 'Knight, take the d-pawn, king\'s knight out', 'rare',
  'c4 c6 Nc3 d5 cxd5 cxd5 Nf3 Nf6 d4 Nc6 Bf4 e6 e3 Bb4 Bd3',
  alts=[('en-c6-e6', 'Small e-pawn move', 'c4 c6 Nc3 e6 g3'),
        ('en-c6-nc6', 'Queen\'s knight out', 'c4 c6 Nc3 d5 cxd5 cxd5 Nf3 Nc6 d4 Nf6 Bf4'),
        ('en-c6-e6v2', 'Small e-pawn move on move 4', 'c4 c6 Nc3 d5 cxd5 cxd5 Nf3 e6 d4 Nf6 Bf4'),
        ('en-c6-bg4', 'Bishop comes at the knight', 'c4 c6 Nc3 d5 cxd5 cxd5 Nf3 Bg4 Ne5 Bf5 e4 dxe4 Qb3 e6 Qxb7 Nd7 Nxd7 Qxd7 Qxa8+'),
        ('en-c6-bf5', 'Light bishop out', 'c4 c6 Nc3 d5 cxd5 cxd5 Nf3 Bf5 Qb3 e6 Qxb7 Nd7 Nb5 Rb8 Nc7+ Ke7 Qxa7 Ngf6 Nd4'),
        ('en-c6-d4', 'Small d-pawn move', 'c4 c6 Nc3 d5 cxd5 cxd5 Nf3 d4 Qa4+ Nc6 Nb5 e5 Nxe5 Nxe5 Nc7+ Ke7 Nxa8 Bd7 Qxa7'),
        ('en-c6-e6v3', 'Small e-pawn move on move 5', 'c4 c6 Nc3 d5 cxd5 cxd5 Nf3 Nf6 d4 e6 Bf4 Bb4 e3 O-O Bd3'),
        ('en-c6-d6', 'Small d-pawn move on move 2', 'c4 c6 Nc3 d6 g3 Nd7 Bg2 Ngf6 e4 e5 Nge2 Be7 O-O O-O d3'),
        ('en-c6-nf6', 'King\'s knight out', 'c4 c6 Nc3 Nf6 g3 d5 cxd5 cxd5 d4 Nc6 Nf3 Bg4 Ne5 Nxe5 dxe5 Ne4 Nxd5 e6 Qa4+')],
  why='The same idea with the c-pawn. Take the d-pawn when it comes; the king\'s knight comes out in front of the f-pawn.', outcome='Equal')
L('en-first', 'en-rare', 'Rare first moves', 'The small d-pawn, the f-pawn, the b-pawn', 'rare',
  'c4 b6 Nc3 Bb7 d4 e6 f3 Nf6 e4 Bb4 Bd2 Bxc3 Bxc3 O-O Bd3',
  alts=[('en-first-nc6', 'Anglo-Lithuanian Variation', 'c4 Nc6 Nc3 e5 g3'),
        ('en-first-nc6nf6', 'Anglo-Lithuanian Variation, then king\'s knight out', 'c4 Nc6 Nc3 Nf6 g3'),
        ('en-first-d6', 'Small d-pawn move', 'c4 d6 Nc3 Nf6 g3'),
        ('en-first-d6e5', 'Small d-pawn move, then e-pawn two squares', 'c4 d6 Nc3 e5 g3'),
        ('en-first-d6e6', 'Small d-pawn move, then small e-pawn move', 'c4 d6 Nc3 e6 g3'),
        ('en-first-d6g6', 'Small d-pawn move, then small g-pawn move', 'c4 d6 Nc3 g6 g3 Bg7 Bg2'),
        ('en-first-d6c6', 'Small d-pawn move, then small c-pawn move', 'c4 d6 Nc3 c6 g3'),
        ('en-first-d6c5', 'Small d-pawn move, then c-pawn two squares', 'c4 d6 Nc3 c5 g3'),
        ('en-first-g6', 'Small g-pawn move', 'c4 b6 Nc3 Bb7 d4 g6 e4 Bg7 g3 e6 Bg2 Ne7 Nge2 O-O O-O'),
        ('en-first-bb4', 'Bishop pins the knight', 'c4 b6 Nc3 Bb7 d4 e6 f3 Bb4 e4 Bxc3+ bxc3 Nf6 Nh3 O-O e5'),
        ('en-first-nf6', 'King\'s knight out', 'c4 b6 Nc3 Bb7 d4 Nf6 Qc2 e6 e4 Bb4 Bd3 Bxc3+ bxc3 O-O e5'),
        ('en-first-nc6e6', 'Anglo-Lithuanian Variation, then small e-pawn move', 'c4 Nc6 Nc3 e6 g3 Nf6 Bg2 d5 cxd5 exd5 d4 Bb4 Bg5 O-O e3')],
  why='Everything else. The setup does the work.', outcome='Equal')

# ============================================================== notes
n('c4', 'C-pawn two squares', 'The first move of the setup. It watches the square Black\'s d-pawn wants to reach, from the side, and keeps your own center pawns back for later.', ['key'])
n('c4 e5 Nc3', 'Queen\'s knight out', 'The second move of the setup, whatever Black plays. Knight and c-pawn watch the same light square in the middle.', ['key'])
n('c4 e5 Nc3 Nf6 g3', 'G-pawn one square', 'It makes room for the bishop on the long diagonal.', ['key'], arrows=['f1g2g'])
n('c4 e5 Nc3 Nf6 g3 Nc6 Bg2', 'Bishop to the long diagonal', 'Bishop, knight and c-pawn now aim at the same light square. The whole setup is built around it.', ['key'], arrows=['g2d5g', 'c3d5g', 'c4d5g'], circles=['d5g'])
n('c4 e5 Nc3 Nf6 g3 Nc6 Bg2 Bc5 e4', 'E-pawn two squares', 'A fourth guard for the light square in the middle. The dark square in front of your d-pawn is the price, and your knight will cover it from behind the e-pawn.', ['key'])
n('c4 e5 Nc3 Nf6 g3 Nc6 Bg2 Bc5 e4 O-O Nge2', 'King\'s knight tucked in', 'Behind the e-pawn, not in front of the f-pawn: the bishop\'s diagonal stays open and the f-pawn is free to go later.', ['key'])
n('c4 e5 Nc3 Nf6 g3 Nc6 Bg2 Bc5 e4 O-O Nge2 d6 O-O', 'Castle', 'King safe, rook behind the f-pawn.')
n('c4 e5 Nc3 Nf6 g3 Nc6 Bg2 Bc5 e4 O-O Nge2 d6 O-O Bg4 d3', 'Small d-pawn move', 'The setup is complete: three pawns in a wedge, the bishop behind them, the knights on the dark squares\' guard.', ['key'])
n('c4 e5 Nc3 Nf6 g3 Nc6 Bg2 Bc5 e4 d6 h3', 'Small h-pawn move first', 'Black\'s d-pawn has moved, so the light bishop now backs up a knight jump toward f2. Take that square away before your knight is tucked in.', ['key'])
n('c4 e5 Nc3 Nf6 g3 Bc5 Bg2 Ng4 e3', 'Small e-pawn move', 'Knight and bishop both aim at f2. One square shuts the bishop out, and your queen now looks at the knight.', ['key'])
n('c4 e5 Nc3 Nf6 g3 Bc5 Bg2 Ng4 e3 Qf6 Qxg4', 'Take the knight', 'It has no guard.', ['key'])
n('c4 e5 Nc3 Nf6 g3 Bc5 Bg2 d6 d3', 'Small d-pawn move first', 'The e-pawn waits. With the bishop aimed at f2 and Black\'s d-pawn moved, two squares would let the knight jump in.')
n('c4 e5 Nc3 Nf6 g3 Bc5 Bg2 d6 d3 Nc6 e3', 'Small e-pawn move', 'It shuts the bishop\'s diagonal to f2. The knight goes behind the pawn as usual.', ['key'])
n('c4 e5 Nc3 Nf6 g3 Bb4 Bg2 Bxc3 bxc3', 'B-pawn takes back', 'Toward the middle. You have the two bishops, and the extra c-pawn will back up your d-pawn later.', ['key'])
n('c4 e5 Nc3 Nf6 g3 Bb4 Bg2 d6 Qa4+', 'Queen check', 'The bishop has no guard, and the check hits it too. Black can block with the knight to guard it, but your bishop takes that knight.', ['key'], arrows=['a4e8r', 'a4b4r'])
n('c4 e5 Nc3 Nf6 g3 Bb4 Bg2 d6 Qa4+ Nc6 Bxc6+ bxc6 Qxb4', 'A bishop up', 'Check, take the guard, take the bishop.')
n('c4 e5 Nc3 Nf6 g3 d5 cxd5', 'Take it', 'The rule against the d-pawn: take it. Your bishop\'s diagonal will be open all the way.', ['key'])
n('c4 e5 Nc3 Nf6 g3 d5 cxd5 Nxd5 Bg2 Nxc3 bxc3', 'B-pawn takes back', 'Toward the middle: it will back up your d-pawn when that goes two squares.')
n('c4 e5 Nc3 Nf6 g3 d5 cxd5 Nxd5 Bg2 Nxc3 bxc3 Nc6 Nf3', 'King\'s knight out', 'The c-pawn is gone, so there is no wedge to build. The knight goes in front of the f-pawn, and you castle.', ['key'])
n('c4 e5 Nc3 Nf6 g3 Nc6 Bg2 b6 Nf3', 'King\'s knight out', 'Black\'s bishop is coming to the long diagonal, where it will have no guard. Your knight gets ready to take the e-pawn.')
n('c4 e5 Nc3 Nf6 g3 Nc6 Bg2 b6 Nf3 Bb7 Nxe5', 'Take the e-pawn', 'If the knight takes back, your bishop takes the bishop on the long diagonal: a clean pawn.', ['key'])
n('c4 e5 Nc3 Bc5 g3 Qf6 e3', 'Small e-pawn move', 'Queen and bishop aim at f2. One square stops both, and your bishop still goes to the long diagonal next.', ['key'])
n('c4 e5 Nc3 Bc5 g3 Qf6 e3 Ne7 Bg2 O-O Nge2 c6 Ne4', 'Knight jumps at queen and bishop', 'Both at once. The queen moves, and you take the bishop.', ['key'])
n('c4 e5 Nc3 c6 Nf3', 'King\'s knight out', 'Black\'s c-pawn gets ready to push the d-pawn. Go at the e-pawn first, before it has a second guard.', ['key'])
n('c4 d5 cxd5', 'Take it', 'The rule against the d-pawn, on move two as well.', ['key'])
n('c4 d5 cxd5 Qxd5 Nc3', 'Knight out', 'The queen has to move again, and you are a move ahead.', ['key'])
n('c4 d5 cxd5 Qxd5 Nc3 Qd8 Nf3 Nf6 d4', 'D-pawn two squares', 'Without the c-pawn there is no wedge. With Black\'s queen back home, take the whole middle instead.', ['key'])
n('c4 d5 cxd5 Qxd5 Nc3 Qd8 Nf3 Nf6 d4 e6 e4 Bb4 Bd3 O-O e5', 'E-pawn pushes at the knight', 'The knight has to leave the king. If it goes to the middle, your bishop takes the h-pawn with check and the attack crashes through.', ['key'], arrows=['d3h7r'])
n('c4 e6 Nc3 d5 cxd5 exd5 d4', 'D-pawn two squares', 'After the trade Black has a pawn fixed in the middle. Put yours beside it; the dark bishop comes out next.', ['key'])
n('c4 b6 Nc3 Bb7 d4', 'D-pawn two squares', 'Black\'s bishop already owns the long diagonal, so your own g-pawn move would lose the corner rook. Take the middle with pawns instead.', ['key'])
n('c4 b6 Nc3 Bb7 d4 e6 f3', 'Small f-pawn move', 'It shuts the bishop\'s diagonal and gets the e-pawn ready to go two squares.', ['key'])
n('c4 Nf6 Nc3 e6 Nf3', 'King\'s knight out', 'Black\'s e-pawn has gone one square to back up the d-pawn. The wedge would be too slow, so the knight comes out the usual way, and the d-pawn is taken when it arrives.', ['key'])
n('c4 c5 Nc3 e6 Nf3', 'King\'s knight out', 'The e-pawn one square means the d-pawn is coming. Knight in front of the f-pawn first, then the g-pawn and the bishop.', ['key'])
n('c4 e5 Nc3 Nf6 g3 c6 Nf3', 'King\'s knight out', 'The c-pawn is getting the d-pawn ready. Go at the e-pawn before it has a second guard.', ['key'])
n('c4 c5 Nc3 Nc6 g3 g6 Bg2 Bg7 e4', 'E-pawn two squares', 'The same wedge against the mirror setup.')
n('c4 c5 Nc3 Nc6 g3 g6 Bg2 Bg7 e4 e6 Nge2 Nge7 O-O O-O d3 a6 Be3', 'Bishop out', 'The setup is done. The bishop looks at the c-pawn, and your d-pawn push is next.', ['key'])
# the other side's moves that start a named line
n('c4 Nc6', 'Anglo-Lithuanian Variation')
n('c4 Nf6', 'Anglo-Indian Defense')
n('c4 c6', 'Caro-Kann Defensive System')
n('c4 d5', 'Anglo-Scandinavian Defense')
n('c4 e5', 'King\'s English Variation')
n('c4 e6', 'Agincourt Defense')
n('c4 g6', 'Great Snake Variation')
n('c4 Nc6 Nc3 e5', 'Reversed Closed Sicilian')
n('c4 Nf6 Nc3 d5', 'Anglo-Grünfeld Defense')
n('c4 Nf6 Nc3 e5', 'Two Knights Variation')
n('c4 Nf6 Nc3 e6', 'Hedgehog System')
n('c4 c5 Nc3 Nc6', 'Two Knights Variation')
n('c4 d5 cxd5 Nf6', 'Schulz Gambit')
n('c4 e5 Nc3 Bb4', 'Kramnik-Shirov Counterattack')
n('c4 e5 Nc3 Nc6', 'Reversed Closed Sicilian')
n('c4 e5 Nc3 Nf6', 'Two Knights Variation')
n('c4 e6 Nc3 Nf6', 'Hedgehog System')
n('c4 Nf6 Nc3 e5 g3 Bb4', 'Smyslov System')
n('c4 Nf6 Nc3 e5 g3 c6', 'Keres Variation')
n('c4 Nf6 Nc3 e5 g3 d5', 'Reversed Dragon')
n('c4 Nf6 Nc3 e6 Nf3 Bb4', 'Nimzo-English')
n('c4 d5 cxd5 Qxd5 Nc3 Qa5', 'Malvinas Variation')
n('c4 e5 Nc3 Bb4 g3 Nf6', 'Smyslov System')
n('c4 e5 Nc3 Nf6 g3 Bb4', 'Smyslov System')
n('c4 e5 Nc3 Nf6 g3 c6', 'Keres Variation')
n('c4 e5 Nc3 Nf6 g3 d5', 'Reversed Dragon')
n('c4 e5 Nc3 d6 g3 c6', 'Keres Defense')
n('c4 Nf6 Nc3 e6 Nf3 c5 g3 Nc6', 'Keres-Parma System')
n('c4 c5 Nc3 Nc6 g3 g6 Bg2 Bg7', 'Ultra-Symmetrical Variation')
n('c4 c5 Nc3 e6 Nf3 Nc6 g3 Nf6', 'Keres-Parma System')
n('c4 c5 Nc3 g6 g3 Bg7 Bg2 Nc6', 'Ultra-Symmetrical Variation')
n('c4 e5 Nc3 Bc5 g3 c6 Bg2 Nf6', 'Keres Variation')
n('c4 e5 Nc3 Nf6 g3 Bc5 Bg2 c6', 'Keres Variation')
n('c4 e6 Nc3 d5 cxd5 exd5 d4 c5', 'Tarrasch Defense')
