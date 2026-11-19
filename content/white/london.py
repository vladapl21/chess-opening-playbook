"""White with the d-pawn: the London System, a second pack for the slot 'white' (see PACKS in content2_meta.py).

One setup, one order: d-pawn two squares, dark bishop out, e-pawn one square, king's knight, c-pawn one square,
queen's knight beside the queen, light bishop, castle. Where a line leaves that order, the note at that move says why
(README, "One setup, one order"). Black's moves were picked with the Maia 1300/1500 odds and every White move was
checked with Stockfish 17.1. SAN is internal; notes are plain English and name no square but f7 and f2."""
from content import n, J, L, PARTS

PARTS.extend([
  dict(id='ld-setup', ch='london', title='The setup', kicker='Moves 1–8',
       blurb='Bishop out before the e-pawn shuts it in, then knight, c-pawn, the other knight and the light bishop. The same order against almost everything Black does.'),
  dict(id='ld-cpawn', ch='london', title='The queen goes for the b-pawn', kicker='The c-pawn and the queen',
       blurb='Once your dark bishop has left, the b-pawn has no guard. Black\'s c-pawn and queen go after it. Two answers, decided by where your c-pawn stands.'),
  dict(id='ld-knight', ch='london', title='Black\'s knight comes first', kicker='The most common reply at club level',
       blurb='A third of club players bring the queen\'s knight out at once. Your setup does not change; two tricks make it pay.'),
  dict(id='ld-bishop', ch='london', title='Black\'s bishop comes out', kicker='The light bishop to the side',
       blurb='Black copies your idea and brings the light bishop out early. Offer yours, and take it if it stays.'),
  dict(id='ld-side', ch='london', title='The c-pawn one square', kicker='The Slav setup',
       blurb='Black guards the d-pawn with the c-pawn. Same setup, and the same answer to the bishop.'),
  dict(id='ln-fian', ch='lindian', title='The fianchetto', kicker='King\'s Indian setup',
       blurb='Black hides the dark bishop behind the g-pawn and castles. Your light bishop goes one square, not two, and the h-pawn makes a way back for the London bishop.'),
  dict(id='ln-epawn', ch='lindian', title='The e-pawn and the d-pawn', kicker='The London in disguise',
       blurb='Most of these come back to the setup you already know. A few small differences are worth a look.'),
  dict(id='ln-cpawn', ch='lindian', title='The c-pawn at once', kicker='Benoni setups',
       blurb='Black hits the d-pawn before anything else. Push it past, then take the middle with the knight and the e-pawn.'),
  dict(id='lr-epawn', ch='lrare', title='The e-pawn one square', kicker='A quiet first move',
       blurb='Black waits with the e-pawn. Almost always it turns into the setup lesson, by another road.'),
  dict(id='lr-gambit', ch='lrare', title='The e-pawn gambit', kicker='Englund',
       blurb='Black throws the e-pawn at yours. Take it, keep it, and know the one queen trick that catches club players.'),
  dict(id='lr-cpawn', ch='lrare', title='The c-pawn two squares', kicker='Old Benoni',
       blurb='Same answer as after the knight: push past, then the e-pawn takes the rest of the middle.'),
  dict(id='lr-fian', ch='lrare', title='Fianchetto and the small d-pawn', kicker='Modern and Pirc',
       blurb='The same King\'s Indian setup, reached another way, and one gambit try to know.'),
  dict(id='lr-other', ch='lrare', title='Rare first moves', kicker='Sidelines',
       blurb='The c-pawn, the b-pawn, the f-pawn and the knight. The setup does the work.'),
])

D5 = "d4 d5 Bf4"
SET = J(D5, "Nf6 e3 e6 Nf3 c5 c3 Nc6 Nbd2 Bd6 Bg3 O-O Bd3")          # the setup, complete
HX = J(D5, "e6 e3 Bd6 Bg3 Bxg3 hxg3")                                  # Black offers the bishops and takes
QB = J(D5, "Nf6 e3 e6 Nf3 c5 c3 Qb6")                                  # the queen at the b-pawn
TR = J(D5, "c5 e3 Nc6 Nf3 Qb6 Nc3 Qxb2 Nxd5")                          # the knight trick
NC = J(D5, "Nc6 e3 Nf6 Nf3 Bg4 c3 e6 Qb3")                             # knight first, bishop at your knight
NB = J(D5, "Nc6 e3 Bf5 Bd3")                                           # knight first, then the bishop
BF = J(D5, "Bf5 e3 e6 Bd3")                                            # the bishop first
KI = "d4 Nf6 Bf4 g6 e3 Bg7 Nf3 O-O Be2 d6 h3"                          # the fianchetto
NE = "d4 Nf6 Bf4 e6 e3"
BN = "d4 Nf6 Bf4 c5 d5"
EN = "d4 e5 dxe5 Nc6 Nf3 Qe7 Bf4 Qb4+ Bd2 Qxb2"                        # the gambit, queen takes the b-pawn
OB = "d4 c5 d5"

# ============================================================== THE SETUP
L('ld-setup', 'ld-setup', 'The London setup', 'Bishop out first, then e-pawn, knight, c-pawn, knight, bishop', 'core', SET,
  alts=[('ld-setup-re8', 'Rook behind the e-pawn: knight into the hole', J(SET, "Re8 Ne5")),
        ('ld-setup-c4', 'The c-pawn hits your bishop', J(SET, "c4 Bc2")),
        ('ld-setup-qc7', 'Queen behind the bishop: the trap', J(SET, "Qc7 dxc5 Bxc5 Bxc7")),
        ('ld-setup-cxd4', 'Black trades the c-pawn', J(SET, "cxd4 exd4")),
        ('ld-setup-be7', 'Bishop one square', J(D5, "Nf6 e3 e6 Nf3 Be7 c3 O-O Nbd2 c5 Bd3")),
        ('ld-setup-e6', 'E-pawn before the knight', J(D5, "e6 e3 Nf6 Nf3 c5 c3 Nc6 Nbd2")),
        ('ld-setup-cxd4early', 'Early trade in the middle', J(D5, "Nf6 e3 e6 Nf3 c5 c3 cxd4 exd4 Nc6 Nbd2")),
        ('ld-setup-c5early', 'C-pawn before the knights', J(D5, "e6 e3 c5 Nf3 Nc6 c3 Nf6 Nbd2"))],
  start=0, why='Half of club players answer the d-pawn with theirs. This order of moves meets almost all of them.',
  outcome='A solid position where you choose the plan')
L('ld-bd6', 'ld-setup', 'Black offers the dark bishops', 'Step back; if Black takes, the h-pawn takes back', 'core',
  J(HX, "Nf6 Nf3 O-O c3 c5 Nbd2 Nc6 Bd3"),
  alts=[('ld-bd6-nc6', 'Black keeps the king in the middle', J(HX, "Nf6 Nf3 Nc6 c3 Bd7 Nbd2 Qe7 Bd3")),
        ('ld-bd6-nf6', 'Knight first, then the offer', J(D5, "Nf6 e3 e6 Nf3 Bd6 Bg3 Bxg3 hxg3 Nbd7 c3")),
        ('ld-bd6-keep', 'Black doesn\'t take', J(D5, "Nf6 e3 e6 Nf3 Bd6 Bg3 O-O c3 Nbd7 Nbd2")),
        ('ld-bd6-e6nf6', 'E-pawn, knight, then the offer', J(D5, "e6 e3 Nf6 Nf3 Bd6 Bg3 Bxg3 hxg3")),
        ('ld-bd6-nf6late', 'The offer, then the knight', J(D5, "e6 e3 Bd6 Bg3 Nf6 Nf3 O-O c3"))],
  why='One club player in four puts the bishop opposite yours as soon as the e-pawn moves. Keep yours, and the trade costs Black a semi-open h-file.',
  outcome='Your rook already looks at the h-pawn')

# ============================================================== THE C-PAWN AND THE QUEEN
L('ld-qb6', 'ld-cpawn', 'The queen goes for the b-pawn', 'Queen out in front of the b-pawn: offer the trade', 'core',
  J(QB, "Qb3 c4 Qc2 Nc6 Nbd2"),
  alts=[('ld-qb6-trade', 'Black trades queens', J(QB, "Qb3 Qxb3 axb3 Nc6 Nbd2")),
        ('ld-qb6-nc6', 'Knight first, then the queen', J(D5, "Nf6 e3 e6 Nf3 c5 c3 Nc6 Nbd2 Qb6 Qb3"))],
  why='The one real try against the setup: your dark bishop has left the queenside and the b-pawn has no guard.',
  outcome='Equal, and Black has spent time on the queen')
L('ld-trick', 'ld-cpawn', 'The c-pawn at once: the knight trick', 'C-pawn at home? Knight out, and the pawn grab loses', 'common',
  J(TR, "cxd4 Rb1 Qxa2 Nc7+ Kd8 Nxa8"),
  alts=[('ld-trick-e6', 'Black guards the d-pawn first', J(TR, "e6 Rb1 Qxa2 Nc7+ Kd8 Nxa8")),
        ('ld-trick-early', 'The queen at once', J(D5, "c5 e3 Qb6 Nc3 Qxb2 Nxd5 Na6 Bxa6 bxa6 Rb1 Qxa2 Nc7+")),
        ('ld-trick-quiet', 'Black develops instead', J(D5, "c5 e3 Nc6 Nf3 Nf6 c3 Bg4 Nbd2 e6 Qb3")),
        ('ld-trick-cxd4', 'Black trades the c-pawn', J(D5, "c5 e3 cxd4 exd4 Nc6 Nf3 Bg4 c3"))],
  why='When Black\'s c-pawn goes two squares before your c-pawn has moved, the queen raid on the b-pawn walks into a knight. Six in ten club players take the pawn.',
  outcome='You win the corner rook')

# ============================================================== KNIGHT FIRST
L('ld-nc6', 'ld-knight', 'Knight first, then the bishop at your knight', 'C-pawn, then the queen hits the b-pawn', 'core',
  J(NC, "Rb8 Nbd2 Bd6 Bg3 Bxg3 hxg3"),
  alts=[('ld-nc6-b6', 'The b-pawn steps up: bishop and queen at the knight', J(NC, "b6 Bb5 Qd7 Qa4 Bxf3 gxf3 Bd6 Bxc6")),
        ('ld-nc6-bd6', 'Black leaves the b-pawn: take it', J(NC, "Bd6 Qxb7")),
        ('ld-nc6-bxf3', 'Bishop takes the knight', J(NC, "Bxf3 gxf3 Rb8 Nd2")),
        ('ld-nc6-na5', 'Knight hits the queen', J(NC, "Na5 Qa4+ c6 Nbd2")),
        ('ld-nc6-e6', 'E-pawn instead of the bishop', J(D5, "Nc6 e3 Nf6 Nf3 e6 c3 Bd6 Bg3 Bxg3 hxg3")),
        ('ld-nc6-nf6first', 'The other knight first', J(D5, "Nf6 e3 Nc6 Nf3 Bg4 c3 e6 Qb3")),
        ('ld-nc6-e6second', 'E-pawn, then the knight', J(D5, "e6 e3 Nc6 Nf3 Nf6 c3")),
        ('ld-nc6-bd6x', 'E-pawn and the bishop offer', J(D5, "Nc6 e3 e6 Nf3 Bd6 Bg3 Bxg3 hxg3")),
        ('ld-nc6-e6first', 'E-pawn before the king\'s knight', J(D5, "Nc6 e3 e6 Nf3 Nf6 c3 Bd6 Bg3 Bxg3 hxg3")),
        ('ld-nc6-a6', 'The a-pawn', J(D5, "Nc6 e3 a6 Nf3 Nf6 c3 Bf5 Bd3"))],
  why='A third of club players bring the queen\'s knight out on move two. When the light bishop then comes at your knight, it leaves the b-pawn behind.',
  outcome='Black has to give up the b-pawn or bend the queenside')
L('ld-nb4', 'ld-knight', 'Knight and bishop at the c-pawn', 'Offer the bishops; the queen check wins the knight', 'core',
  J(NB, "Bxd3 Qxd3 Nb4 Qb5+ c6 Qxb4"),
  alts=[('ld-nb4-nf6', 'Black develops', J(NB, "Bxd3 Qxd3 Nf6 Nf3 e6 c3 Bd6 Bg3")),
        ('ld-nb4-e6', 'Black leaves the bishop: take it', J(NB, "e6 Bxf5 exf5 Nf3 Nf6 c3")),
        ('ld-nb4-bg6', 'The bishop steps back', J(NB, "Bg6 Nf3 Nf6 c3 e6 Bxg6 hxg6 Nbd2")),
        ('ld-nb4-qd7', 'Queen behind the bishop', J(NB, "Qd7 Nf3 O-O-O c3")),
        ('ld-nb4-e6x', 'Black trades and plays the e-pawn', J(NB, "Bxd3 Qxd3 e6 Nf3 Nf6 c3")),
        ('ld-nb4-nf3', 'Both knights, then the bishop', J(D5, "Nc6 e3 Nf6 Nf3 Bf5 Bd3 Bxd3 Qxd3 e6 c3"))],
  why='With the knight out, Black\'s bishop and knight can both aim at your c-pawn. Trading the bishop takes that away, and one club player in eight jumps the knight at your queen anyway.',
  outcome='Equal, or a knight up')

# ============================================================== THE BISHOP FIRST
L('ld-bf5', 'ld-bishop', 'Black\'s bishop comes out first', 'Light bishop out at once; the queen takes back', 'common',
  J(BF, "Bxd3 Qxd3 Nf6 Nf3 Bd6 Bg3 O-O c3"),
  alts=[('ld-bf5-bg6', 'The bishop steps back', J(BF, "Bg6 Nf3 Nf6 c3 Bd6 Bg3")),
        ('ld-bf5-nf6', 'Knight before the e-pawn', J(D5, "Bf5 e3 Nf6 Bd3 Bxd3 Qxd3 e6 Nf3")),
        ('ld-bf5-nf6x', 'Knight first, then the bishop', J(D5, "Nf6 e3 Bf5 Bd3 Bxd3 Qxd3 e6 Nf3")),
        ('ld-bf5-nc6', 'Bishop, then the knight', J(D5, "Bf5 e3 Nc6 Bd3 Bxd3 Qxd3")),
        ('ld-bf5-bg6x', 'Knight, bishop, then the step back', J(D5, "Nf6 e3 Bf5 Bd3 Bg6 Nf3 e6 c3 Bd6 Bg3"))],
  why='One club player in eight copies your idea and brings the light bishop out on move two. It is Black\'s best minor piece: offer yours for it.',
  outcome='Equal and easy to play')

# ============================================================== THE SLAV SETUP
L('ld-c6', 'ld-side', 'The c-pawn guards the d-pawn', 'Same setup; offer the bishops, take if it stays', 'common',
  J(D5, "c6 e3 Nf6 Nf3 Bf5 Bd3 e6 Bxf5 exf5 c3 Nbd7 Nbd2"),
  alts=[('ld-c6-qb6', 'The queen at once', J(D5, "c6 e3 Qb6 Qc1 Bf5 Bd3 e6 Bxf5 exf5 Nf3")),
        ('ld-c6-bf5', 'Bishop out before the knight', J(D5, "c6 e3 Bf5 Bd3 Bxd3 Qxd3 e6 Nf3"))],
  why='A small share of club players, but it is your own Black setup from the other side. The bishop rule is the same as everywhere.',
  outcome='Black\'s pawns are doubled; you are slightly better')

# ============================================================== THE FIANCHETTO
L('ln-kid', 'ln-fian', 'The fianchetto', 'Bishop one square, h-pawn one square, castle', 'core',
  J(KI, "Nbd7 O-O e5 dxe5 dxe5 Nxe5"),
  alts=[('ln-kid-nh5', 'Knight to the edge at your bishop', J(KI, "Nh5 Bh2")),
        ('ln-kid-d6', 'D-pawn before castling', "d4 Nf6 Bf4 g6 e3 Bg7 Nf3 d6 h3 O-O Be2 Nbd7 O-O"),
        ('ln-kid-c5', 'The c-pawn hits the center', J(KI, "c5 O-O Nc6 c3")),
        ('ln-kid-nc6', 'Queen\'s knight out, then the e-pawn', J(KI, "Nc6 O-O e5 dxe5 dxe5 Nxe5")),
        ('ln-kid-d5', 'D-pawn two squares', "d4 Nf6 Bf4 g6 e3 Bg7 Nf3 O-O Be2 d5 O-O c5 c3")],
  why='The most common answer to your bishop after the knight: three club players in ten put their bishop behind the g-pawn.',
  outcome='Comfortable, and the e-pawn push costs Black a pawn')

# ============================================================== THE E-PAWN AND THE D-PAWN
L('ln-e6', 'ln-epawn', 'The e-pawn: back to the setup', 'Same moves, same position', 'core',
  J(NE, "d5 Nf3 c5 c3 Nc6 Nbd2 Bd6 Bg3 O-O Bd3"),
  alts=[('ln-e6-bd6', 'The bishop offer', J(NE, "d5 Nf3 Bd6 Bg3 Bxg3 hxg3")),
        ('ln-e6-c5', 'C-pawn and the trade', J(NE, "c5 Nf3 cxd4 exd4 Nc6 c3")),
        ('ln-e6-c5d5', 'C-pawn, then the d-pawn', J(NE, "c5 Nf3 d5 c3 Nc6 Nbd2")),
        ('ln-e6-b6', 'The b-pawn and the long diagonal', J(NE, "b6 Nf3 Bb7 c3 Be7 Nbd2 O-O Bd3")),
        ('ln-e6-be7', 'Bishop one square', J(NE, "Be7 Nf3 O-O c3 d5 Nbd2"))],
  why='Two club players in ten answer your bishop with the e-pawn. Most of the time the d-pawn follows and you are in the setup lesson.',
  outcome='The setup you know')
L('ln-d6', 'ln-epawn', 'The small d-pawn', 'The e-pawn push loses a pawn', 'common',
  "d4 Nf6 Bf4 d6 e3 Nbd7 Nf3 e5 dxe5 dxe5 Nxe5",
  alts=[('ln-d6-g6', 'The fianchetto after all', "d4 Nf6 Bf4 d6 e3 g6 Nf3 Bg7 h3 O-O Be2"),
        ('ln-d6-nc6', 'Knight, then the bishop at your knight', "d4 Nf6 Bf4 d6 e3 Nc6 Nf3 Bg4 c3 e6 Qb3")],
  why='One in seven. Black wants the e-pawn push; with your bishop on the diagonal, it just drops a pawn.',
  outcome='A pawn up, or the fianchetto lesson')
L('ln-d5', 'ln-epawn', 'The d-pawn two squares', 'Back to the London by another road', 'common',
  "d4 Nf6 Bf4 d5 e3 e6 Nf3 c5 c3 Nc6 Nbd2",
  alts=[('ln-d5-nc6', 'Knight, then the bishop at your knight', "d4 Nf6 Bf4 d5 e3 Nc6 Nf3 Bg4 c3 e6 Qb3"),
        ('ln-d5-bf5', 'The bishop out', "d4 Nf6 Bf4 d5 e3 Bf5 Bd3 Bxd3 Qxd3 e6 Nf3")],
  why='Two in ten. Every position here is one you already know from the first chapter.',
  outcome='The setup you know')

# ============================================================== THE C-PAWN AT ONCE
L('ln-c5', 'ln-cpawn', 'The c-pawn hits the d-pawn', 'Push past, knight out, then the e-pawn', 'common',
  J(BN, "d6 Nc3 g6 e4 Bg7 Nf3"),
  alts=[('ln-c5-e6', 'The e-pawn hits back', J(BN, "e6 Nc3 exd5 Nxd5 Nxd5 Qxd5"))],
  why='Rare, but sharp. Pushing past gains space and keeps Black\'s c-pawn out of the game.',
  outcome='More space for you')

# ============================================================== OTHER FIRST MOVES
L('lr-e6', 'lr-epawn', 'The e-pawn first', 'The same setup by another road', 'common',
  "d4 e6 Bf4 d5 e3 Nf6 Nf3 c5 c3 Nc6 Nbd2 Bd6 Bg3 O-O Bd3",
  alts=[('lr-e6-c5', 'The c-pawn and the trade', "d4 e6 Bf4 c5 e3 cxd4 exd4 Nc6 Nf3 Nf6 c3"),
        ('lr-e6-nf6', 'The knight next', "d4 e6 Bf4 Nf6 e3 d5 Nf3 c5 c3"),
        ('lr-e6-d5c5', 'D-pawn, then the c-pawn', "d4 e6 Bf4 d5 e3 c5 Nf3 Nc6 c3"),
        ('lr-e6-bd6', 'D-pawn, then the bishop offer', "d4 e6 Bf4 d5 e3 Bd6 Bg3 Bxg3 hxg3"),
        ('lr-e6-d6', 'The small d-pawn', "d4 e6 Bf4 d6 e3 Nf6 Nf3 Be7 c3")],
  why='One club player in nine starts with the e-pawn. It nearly always ends in the setup.',
  outcome='The setup you know')
L('lr-englund', 'lr-gambit', 'The e-pawn gambit', 'Take the pawn; when the queen grabs, the knight comes out', 'common',
  J(EN, "Nc3 Bb4 Rb1 Qa3 Rb3 Qa5 a3"),
  alts=[('lr-englund-trap', 'The trap: bishop in front of the knight', J(EN, "Bc3 Bb4 Qd2 Bxc3 Qxc3 Qc1#")),
        ('lr-englund-nxe5', 'Knight takes the pawn back', "d4 e5 dxe5 Nc6 Nf3 Qe7 Bf4 Nxe5 Bxe5"),
        ('lr-englund-d6', 'The d-pawn hits back', "d4 e5 dxe5 Nc6 Nf3 d6 Bf4 dxe5 Nxe5"),
        ('lr-englund-bc5', 'The bishop at f2', "d4 e5 dxe5 Nc6 Nf3 Bc5 Bf4"),
        ('lr-englund-f6', 'The f-pawn hits back', "d4 e5 dxe5 f6 Nf3 fxe5 Nxe5 Nc6 Bf4"),
        ('lr-englund-d6first', 'The d-pawn first', "d4 e5 dxe5 d6 Bf4 dxe5 Qxd8+ Kxd8 Bxe5"),
        ('lr-nc6-e5', 'Knight first, then the gambit', "d4 Nc6 Bf4 e5 dxe5 Qe7 Nf3 Qb4+ Bd2 Qxb2 Nc3"),
        ('lr-nc6-e5d6', 'Knight first, then the d-pawn', "d4 Nc6 Bf4 e5 dxe5 d6 exd6 Bxd6 Bg3"),
        ('lr-nc6-e5f6', 'Knight first, then the f-pawn', "d4 Nc6 Bf4 e5 dxe5 f6 Nf3 fxe5 Nxe5"),
        ('lr-nc6-e5g5', 'Knight first, then the g-pawn', "d4 Nc6 Bf4 e5 dxe5 g5 Bg3 Bg7 e3")],
  why='One in thirty-five, and the players who choose it are hoping for the trap. Know the one move that avoids it and you are a clean pawn up.',
  outcome='A pawn up and a safer king')
L('lr-c5', 'lr-cpawn', 'The c-pawn two squares', 'Push past it, then knight and e-pawn', 'common',
  J(OB, "d6 Nc3 Nf6 e4 g6 Nf3 Bg7 Be2 O-O O-O"),
  alts=[('lr-c5-e6', 'The e-pawn hits back', J(OB, "e6 Nc3 exd5 Nxd5 Nf6 Bf4 Nxd5 Qxd5")),
        ('lr-c5-nf6', 'Knight first', J(OB, "Nf6 Nc3 d6 e4 g6 Nf3")),
        ('lr-c5-e5', 'The e-pawn two squares', J(OB, "e5 Nc3 d6 e4 Nf6 Nf3"))],
  why='One in thirty-five. Bringing the bishop out first would walk into the queen raid on the b-pawn; the push past takes the space instead.',
  outcome='More space for you')
L('lr-g6', 'lr-fian', 'The fianchetto first', 'The King\'s Indian setup by another road', 'common',
  "d4 g6 Bf4 Bg7 e3 d6 Nf3 Nf6 h3 O-O Be2",
  alts=[('lr-g6-c5', 'The c-pawn and the trade', "d4 g6 Bf4 Bg7 e3 c5 Nf3 cxd4 exd4"),
        ('lr-g6-nf6', 'The knight after the bishop', "d4 g6 Bf4 Bg7 e3 Nf6 Nf3 O-O Be2 d6 h3"),
        ('lr-d6', 'The small d-pawn first', "d4 d6 Bf4 Nf6 e3 g6 Nf3 Bg7 h3 O-O Be2"),
        ('lr-d6-e5', 'The small d-pawn, then the gambit', "d4 d6 Bf4 e5 dxe5 Nc6 exd6 Bxd6 Bg3"),
        ('lr-d6-e5x', 'The pawn takes back: trade queens, take the pawn', "d4 d6 Bf4 e5 dxe5 dxe5 Qxd8+ Kxd8 Bxe5")],
  why='One in fourteen between them. They meet the fianchetto lesson, apart from one e-pawn push to know.',
  outcome='The fianchetto lesson, or a pawn up')
L('lr-other', 'lr-other', 'Rare first moves', 'Same setup, same bishop rule', 'rare',
  "d4 c6 Bf4 d5 e3 Bf5 Bd3 e6 Bxf5 exf5 Nf3",
  alts=[('lr-b6', 'The b-pawn and the long diagonal', "d4 b6 Bf4 Bb7 e3 e6 Nf3 Nf6 c3 Be7 Nbd2"),
        ('lr-f5', 'The f-pawn two squares', "d4 f5 Bf4 Nf6 e3 e6 Nf3 Be7 c3 O-O Nbd2"),
        ('lr-f5-g6', 'The f-pawn and the fianchetto', "d4 f5 Bf4 Nf6 e3 g6 Nf3 Bg7 Be2 O-O O-O"),
        ('lr-nc6', 'The knight first', "d4 Nc6 Bf4 d5 e3 Bf5 Bd3 Bxd3 Qxd3")],
  why='About one game in fifteen between them. None needs anything new.', outcome='The setup you know')

# ============================================================== notes: the setup
n("d4", "Pawn to the center", "The d-pawn takes the middle and opens the road for your dark bishop.", ['key'])
n("d4 d5", "Black copies you", "About half of club players answer this way.")
n(D5, "Bishop out first", "The London bishop. It leaves before your e-pawn moves, so it is never shut in behind the pawns.", ['key'], arrows=['f4c7g'])
n(J(D5, "Nf6"), "Knight out", "The most natural reply. Your setup carries on.")
n(J(D5, "Nf6 e3"), "E-pawn one square", "It guards the d-pawn and opens the road for the light bishop. The dark bishop is already outside the pawns.", ['key'])
n(J(D5, "Nf6 e3 e6"), "Black closes the light bishop in", "Black's bishop is now behind its own pawns. Yours is outside.")
n(J(D5, "Nf6 e3 e6 Nf3"), "King's knight", "It guards the middle and gets your king ready to castle.", ['key'])
n(J(D5, "Nf6 e3 e6 Nf3 c5"), "The c-pawn hits the d-pawn", "Black's usual plan: pressure on your d-pawn and, later, on the b-pawn.")
n(J(D5, "Nf6 e3 e6 Nf3 c5 c3"), "C-pawn one square", "Now the d-pawn has a pawn behind it, whatever Black takes. The setup is a pyramid of pawns.", ['key'], circles=['c3g', 'd4g', 'e3g'])
n(J(D5, "Nf6 e3 e6 Nf3 c5 c3 Nc6"), "Knight joins the attack on the d-pawn", "Two Black pieces hit it now. Two pawns, your knight and your queen guard it.")
n(J(D5, "Nf6 e3 e6 Nf3 c5 c3 Nc6 Nbd2"), "Queen's knight beside the queen", "On this square it guards the other knight and can jump to the middle later. It goes here before the light bishop.", ['key'])
n(J(D5, "Nf6 e3 e6 Nf3 c5 c3 Nc6 Nbd2 Bd6"), "Black's bishop offers a trade", "It stands opposite yours. A trade would take away the London bishop.")
n(J(D5, "Nf6 e3 e6 Nf3 c5 c3 Nc6 Nbd2 Bd6 Bg3"), "Step back, keep it", "Your bishop stays on its diagonal. If Black takes it, your h-pawn takes back and your rook gets the h-file.", ['key'], arrows=['h2g3g'])
n(SET, "Light bishop out", "The last piece. It aims at the king's side, where Black has just castled. Castling is next unless Black does something first.", ['key'], arrows=['d3h7g'])
n(J(SET, "Re8"), "Rook behind the e-pawn", "Black wants to push the e-pawn and hit your bishop.")
n(J(SET, "Re8 Ne5"), "Knight jumps into the hole", "Before the e-pawn can move, your knight takes the square in front of it, and the push is stopped.", ['key'], arrows=['f3e5g'])
n(J(SET, "c4"), "The c-pawn hits your bishop", "Black closes the queenside.")
n(J(SET, "c4 Bc2"), "Bishop steps back", "It keeps its diagonal toward Black's king. Next, castle, and the e-pawn push is your plan.", ['key'])
n(J(SET, "Qc7"), "Queen behind the bishop", "Look along your bishop's diagonal: Black's bishop, then Black's queen.", arrows=['g3c7r'])
n(J(SET, "Qc7 dxc5"), "Take the c-pawn", "The pawn hits Black's bishop. If the bishop takes back, it leaves the diagonal.", ['key', 'trap'], arrows=['g3c7r'])
n(J(SET, "Qc7 dxc5 Bxc5"), "The bishop takes back", "The most natural move, and half of club players play it. It opens the diagonal.", ['mistake'])
n(J(SET, "Qc7 dxc5 Bxc5 Bxc7"), "Bishop takes the queen", "Black's queen was on your bishop's diagonal the whole time.", ['key', 'trap'])
n(J(SET, "cxd4"), "Black trades in the middle", None)
n(J(SET, "cxd4 exd4"), "Take back with the e-pawn", "Always the e-pawn: it keeps a pawn in the middle and opens the e-file for your rook.", ['key'])
n(J(D5, "Nf6 e3 e6 Nf3 Be7"), "Bishop one square", "Quieter. Nothing changes for you.")
n(J(D5, "Nf6 e3 e6 Nf3 c5 c3 cxd4"), "Black trades early", None)
n(J(D5, "Nf6 e3 e6 Nf3 c5 c3 cxd4 exd4"), "Take back with the e-pawn", "Same rule as later in the game: the e-pawn takes back, the knight goes beside the queen.", ['key'])

# ============================================================== notes: the bishop offer
n(J(D5, "e6"), "E-pawn one square", "Black's light bishop is shut in. Carry on.")
n(J(D5, "e6 e3 Bd6"), "Bishop opposite yours", "Black offers the trade at once.")
n(J(D5, "e6 e3 Bd6 Bg3"), "Step back, keep it", "Your bishop stays on its diagonal. If Black takes, you take back toward the middle with the h-pawn.", ['key'], arrows=['d6g3r', 'h2g3g'])
n(HX, "H-pawn takes back", "Your pawns stay healthy, and the rook behind the h-pawn now looks straight at Black's h-pawn.", ['key'], arrows=['h1h7g'])
n(J(HX, "Nf6 Nf3 O-O"), "Black castles into it", "The king is next to the file your rook looks down.")
n(J(HX, "Nf6 Nf3 O-O c3 c5 Nbd2 Nc6 Bd3"), "Light bishop at the king", "Bishop and rook aim at the same pawn. Black can't push the e-pawn or the b-pawn now without losing material.", ['key'], arrows=['d3h7g', 'h1h7g'])
n(J(HX, "Nf6 Nf3 Nc6 c3 Bd7 Nbd2 Qe7"), "Black waits to castle", "Black is thinking of castling on the queenside, away from your rook.")
n(J(HX, "Nf6 Nf3 Nc6 c3 Bd7 Nbd2 Qe7 Bd3"), "Bishop out as usual", "Finish the setup. Your king can wait: with the h-file half open, it is safe in the middle for now.")
n(J(D5, "Nf6 e3 e6 Nf3 Bd6 Bg3 O-O"), "Black castles instead", "Fine: your bishop stays where it is and the setup goes on.")

# ============================================================== notes: the queen at the b-pawn
n(QB, "Queen at your b-pawn", "Your dark bishop left the queenside, so nothing guards the b-pawn now. One club player in twenty goes for it.", arrows=['b6b2r'])
n(J(QB, "Qb3"), "Queen out: offer the trade", "Your c-pawn has already moved, so the queen can step out in front of the b-pawn. If Black trades, you take back toward the middle and your rook gets the a-file.", ['key'], arrows=['b3b6g'])
n(J(QB, "Qb3 c4"), "The c-pawn hits your queen", None)
n(J(QB, "Qb3 c4 Qc2"), "Queen steps back", "She looks along the diagonal toward Black's king side, and Black's c-pawn has stopped hitting your d-pawn.", ['key'])
n(J(QB, "Qb3 Qxb3"), "Black trades queens", None)
n(J(QB, "Qb3 Qxb3 axb3"), "Take back toward the middle", "The a-pawn takes back and the rook in the corner has an open file at once.", ['key'], arrows=['a1a7g'])
n(J(D5, "Nf6 e3 e6 Nf3 c5 c3 Nc6 Nbd2 Qb6"), "Queen at your b-pawn", "The same idea one move later.")
n(J(D5, "Nf6 e3 e6 Nf3 c5 c3 Nc6 Nbd2 Qb6 Qb3"), "Queen out: same answer", "Same reply, same reason.", ['key'])

# ============================================================== notes: the knight trick
n(J(D5, "c5"), "The c-pawn at once", "Black hits the d-pawn before anything else.")
n(J(D5, "c5 e3"), "E-pawn one square", "Your d-pawn is guarded. The setup carries on.")
n(J(D5, "c5 e3 Nc6 Nf3 Qb6"), "Queen at your b-pawn", "Your c-pawn is still at home, so your queen can't step out to meet her.", arrows=['b6b2r'])
n(J(D5, "c5 e3 Nc6 Nf3 Qb6 Nc3"), "Knight out: let her take", "If the queen takes the b-pawn, the knight jumps at the d-pawn and the queen is far from home.", ['key', 'trap'], arrows=['c3d5g'])
n(J(D5, "c5 e3 Nc6 Nf3 Qb6 Nc3 Qxb2"), "The queen takes the pawn", "Six club players in ten take it.", ['mistake'])
n(TR, "Knight takes the d-pawn", "It threatens to jump to the square next to Black's king, hitting the king and the rook in the corner.", ['key', 'trap'], arrows=['d5c7r'])
n(J(TR, "cxd4 Rb1"), "Rook hits the queen", "She has to keep running. Wherever she goes, the knight check comes.", ['key'], arrows=['b1b2r'])
n(J(TR, "cxd4 Rb1 Qxa2 Nc7+"), "Knight check, two at once", "The king and the rook in the corner are both hit.", ['key'], arrows=['c7a8r', 'c7e8r'])
n(J(TR, "cxd4 Rb1 Qxa2 Nc7+ Kd8 Nxa8"), "Knight takes the rook", "A whole rook up. The knight may be stuck in the corner for a while; bring your other pieces out first.", ['key'])
n(J(TR, "e6 Rb1"), "Rook hits the queen", "Same as before: the queen runs, the knight checks.", ['key'])
n(J(TR, "e6 Rb1 Qxa2 Nc7+ Kd8 Nxa8"), "Knight takes the rook", "Same result. Black's e-pawn move came too late.", ['key'])
n(J(D5, "c5 e3 Qb6 Nc3"), "Knight out: let her take", "The same trick one move sooner.", ['key', 'trap'])
n(J(D5, "c5 e3 Qb6 Nc3 Qxb2 Nxd5"), "Knight takes the d-pawn", "The knight check next to Black's king is coming.", ['key'])
n(J(D5, "c5 e3 Qb6 Nc3 Qxb2 Nxd5 Na6 Bxa6"), "Bishop takes the knight", "Black guarded the check square with the knight. Take the guard away.", ['key'])
n(J(D5, "c5 e3 Qb6 Nc3 Qxb2 Nxd5 Na6 Bxa6 bxa6 Rb1"), "Rook hits the queen", "Same as in the main line: the queen runs, and the check square is free again.", ['key'])
n(J(D5, "c5 e3 Qb6 Nc3 Qxb2 Nxd5 Na6 Bxa6 bxa6 Rb1 Qxa2 Nc7+"), "Knight check, two at once", "The king and the rook in the corner. The rook falls next move.", ['key'])
n(J(D5, "c5 e3 Nc6 Nf3 Nf6 c3"), "C-pawn one square", "With no queen raid yet, back to the setup.", ['key'])
n(J(D5, "c5 e3 Nc6 Nf3 Nf6 c3 Bg4 Nbd2 e6 Qb3"), "Queen hits the b-pawn", "Black's light bishop has left, so nothing guards it. The same idea as in the knight-first lesson.", ['key'], arrows=['b3b7g'])
n(J(D5, "c5 e3 cxd4 exd4"), "Take back with the e-pawn", "As always. The setup carries on with the knight and the c-pawn.", ['key'])

# ============================================================== notes: knight first
n(J(D5, "Nc6"), "Knight first", "A third of club players do this. It gets ready to push the e-pawn, and to jump at your c-pawn.")
n(J(D5, "Nc6 e3"), "E-pawn one square", "Nothing changes. Your setup comes out in the same order.", ['key'])
n(J(D5, "Nc6 e3 Nf6 Nf3 Bg4"), "Bishop comes at your knight", "It leaves the queenside, and with it the guard on Black's b-pawn.")
n(J(D5, "Nc6 e3 Nf6 Nf3 Bg4 c3"), "C-pawn one square", "The usual move, and it opens the road from your queen to the b-pawn.", ['key'])
n(NC, "Queen hits the b-pawn", "Black's light bishop used to guard it. Now Black has to spend a move on it.", ['key'], arrows=['b3b7g'])
n(J(NC, "Rb8"), "Rook guards the b-pawn", "The most solid answer. Your setup goes on as normal.")
n(J(NC, "Rb8 Nbd2 Bd6 Bg3 Bxg3 hxg3"), "H-pawn takes back", "Same as always after the bishop trade: the rook gets the h-file.", ['key'])
n(J(NC, "b6"), "The b-pawn steps up", "It looks safe, but the knight in front of it has lost its only guard.", ['mistake'])
n(J(NC, "b6 Bb5"), "Bishop hits the knight", "The knight can't move: Black's king stands behind it.", ['key', 'trap'], arrows=['b5e8r'])
n(J(NC, "b6 Bb5 Qd7"), "Queen guards the knight", None)
n(J(NC, "b6 Bb5 Qd7 Qa4"), "Queen piles on the knight", "Two of your pieces hit it and only the queen guards it.", ['key'], arrows=['a4c6g', 'b5c6g'])
n(J(NC, "b6 Bb5 Qd7 Qa4 Bxf3 gxf3 Bd6 Bxc6"), "Bishop takes the knight", "A clean piece up.", ['key'])
n(J(NC, "Bd6"), "Black ignores the b-pawn", None, ['mistake'])
n(J(NC, "Bd6 Qxb7"), "Queen takes the b-pawn", "A free pawn. Next she steps back, out of reach of Black's rook.", ['key'])
n(J(NC, "Bxf3"), "Bishop takes your knight", None)
n(J(NC, "Bxf3 gxf3"), "Take back with the g-pawn", "Your queen is busy hitting the b-pawn. The g-pawn takes back and your rook gets the g-file.", ['key'])
n(J(NC, "Na5"), "Knight hits the queen", None)
n(J(NC, "Na5 Qa4+"), "Queen to the side with check", "She keeps an eye on the knight on the edge.", ['key'])
n(J(D5, "Nc6 e3 Nf6 Nf3 e6"), "E-pawn one square", "The light bishop stays at home. Your setup goes on.")
n(J(D5, "Nc6 e3 a6"), "The a-pawn", "Black keeps your bishop off the knight's diagonal. Carry on.")

n(J(D5, "Nc6 e3 Bf5"), "Bishop out too", "Now knight and bishop can both aim at your c-pawn.", arrows=['f5c2r'])
n(NB, "Light bishop out at once", "Offer the trade before Black's knight can join in. Your bishop guards the c-pawn on the way.", ['key'], arrows=['d3f5g'])
n(J(NB, "Bxd3"), "Black trades", None)
n(J(NB, "Bxd3 Qxd3"), "The queen takes back", "She comes out with the move and keeps the c-pawn covered.", ['key'])
n(J(NB, "Bxd3 Qxd3 Nb4"), "Knight hits the queen", "And the c-pawn. One club player in eight tries it.", ['mistake'])
n(J(NB, "Bxd3 Qxd3 Nb4 Qb5+"), "Queen check", "The check also hits the knight. Block with the pawn or the queen, and the knight falls; send the knight back to block, and the b-pawn falls.", ['key', 'trap'], arrows=['b5b4r', 'b5e8r'])
n(J(NB, "Bxd3 Qxd3 Nb4 Qb5+ c6 Qxb4"), "Queen takes the knight", "A piece up.", ['key'])
n(J(NB, "e6"), "Black lets it stand", None)
n(J(NB, "e6 Bxf5"), "Take the bishop", "Black has to take back with the e-pawn and ends up with two pawns on one file.", ['key'])
n(J(NB, "Bg6"), "Bishop steps back", "It still faces your bishop.")
n(J(NB, "Bg6 Nf3 Nf6 c3 e6 Bxg6"), "Take it before the queen's knight comes out", "With the knight beside the queen, she would no longer guard your bishop, and Black's bishop would take it for free.", ['key'])
n(J(NB, "Bg6 Nf3 Nf6 c3 e6 Bxg6 hxg6"), "Black takes back toward the middle", "Black's rook gets the h-file too, but your king isn't there yet.")
n(J(NB, "Qd7"), "Queen behind the bishop", "Black is thinking about castling on the queenside.")

# ============================================================== notes: the bishop first
n(J(D5, "Bf5"), "Black's bishop comes out", "One club player in eight copies your idea.")
n(J(D5, "Bf5 e3"), "E-pawn one square", "Now your light bishop can come out too.", ['key'])
n(BF, "Light bishop out: offer the trade", "Black's bishop is outside its pawns and is Black's best minor piece. Offer yours for it.", ['key'], arrows=['d3f5g'])
n(J(BF, "Bxd3"), "Black trades", None)
n(J(BF, "Bxd3 Qxd3"), "The queen takes back", "She comes out with the move. The king's knight comes next.", ['key'])
n(J(BF, "Bg6"), "Bishop steps back", "It still faces yours. Bring the knight out first.")
n(J(D5, "Bf5 e3 Nf6 Bd3"), "Light bishop out: offer the trade", "Same rule in every order.", ['key'])
n(J(D5, "Nf6 e3 Bf5"), "Bishop out after the knight", None)
n(J(D5, "Nf6 e3 Bf5 Bd3"), "Light bishop out: offer the trade", "Same rule in every order.", ['key'])

# ============================================================== notes: the Slav setup
n(J(D5, "c6"), "C-pawn one square", "The Slav setup.")
n(J(D5, "c6 e3 Nf6 Nf3 Bf5 Bd3"), "Light bishop out: offer the trade", "The bishop rule again.", ['key'])
n(J(D5, "c6 e3 Nf6 Nf3 Bf5 Bd3 e6 Bxf5"), "Take the bishop", "Black left it standing, so take it: two Black pawns on one file.", ['key'])
n(J(D5, "c6 e3 Qb6"), "Queen at your b-pawn", "With Black's c-pawn only one square forward, there is no knight trick.")
n(J(D5, "c6 e3 Qb6 Qc1"), "Queen guards the b-pawn", "Quiet and safe. The knight trick only works when Black's c-pawn has gone two squares.", ['key'])

# ============================================================== notes: the fianchetto
n("d4 Nf6", "Knight first", "One club player in six. Nothing changes on move two.")
n("d4 Nf6 Bf4", "Bishop out first", "Same move as against the d-pawn.", ['key'])
n("d4 Nf6 Bf4 g6", "Black prepares the fianchetto", "The bishop will stand behind the g-pawn and look down the long diagonal.")
n("d4 Nf6 Bf4 g6 e3 Bg7 Nf3 O-O Be2", "Light bishop one square", "Not two squares: there Black's e-pawn could come forward and fork it with your knight. One square back it stays out of the way.", ['key'])
n("d4 Nf6 Bf4 g6 e3 Bg7 Nf3 O-O Be2 d6", "D-pawn one square", "Black is ready for the e-pawn push, or the knight to the edge, both at your bishop.")
n(KI, "H-pawn one square", "Now your bishop has a way back when it is hit.", ['key'], arrows=['f4h2g'])
n(J(KI, "Nbd7 O-O"), "Castle", "The setup is complete. The c-pawn comes next.", ['key'])
n(J(KI, "Nbd7 O-O e5"), "The e-pawn push", "It hits your bishop, but the pawn can be taken and can't be held.")
n(J(KI, "Nbd7 O-O e5 dxe5"), "Take it", "Your d-pawn takes, and Black has to take back.", ['key'])
n(J(KI, "Nbd7 O-O e5 dxe5 dxe5 Nxe5"), "Knight takes the pawn", "Your knight and bishop both hit it and only Black's knight guards it. A clean pawn up.", ['key'])
n(J(KI, "Nh5"), "Knight to the edge, at your bishop", None)
n(J(KI, "Nh5 Bh2"), "Bishop steps back", "This is what the h-pawn move was for. Your bishop keeps its diagonal.", ['key'])
n(J(KI, "Nc6 O-O e5 dxe5 dxe5 Nxe5"), "Knight takes the pawn", "Two of your pieces hit it and one of Black's guards it. A pawn up.", ['key'])
n("d4 Nf6 Bf4 g6 e3 Bg7 Nf3 d6 h3", "H-pawn one square", "Same move, other order: the d-pawn has moved, so make the way back for your bishop now.", ['key'])
n(J(KI, "c5 O-O"), "Castle", "Black's c-pawn hits your d-pawn. Castle, then support the d-pawn with the c-pawn.", ['key'])

# ============================================================== notes: the e-pawn and the d-pawn
n(NE, "E-pawn one square", "The setup as always.", ['key'])
n(J(NE, "d5"), "D-pawn two squares", "The same position as in the setup lesson, by another road.")
n(J(NE, "c5 Nf3 cxd4 exd4"), "Take back with the e-pawn", "Same rule as in the setup.", ['key'])
n(J(NE, "b6"), "The b-pawn", "Black's light bishop goes to the long diagonal instead.")
n(J(NE, "b6 Nf3 Bb7 c3 Be7 Nbd2 O-O Bd3"), "Light bishop out", "The setup is complete. Your e-pawn push is the plan.")
n("d4 Nf6 Bf4 d6", "The small d-pawn", "Black wants to push the e-pawn two squares.")
n("d4 Nf6 Bf4 d6 e3 Nbd7 Nf3 e5", "The e-pawn push", "It hits your bishop, but your d-pawn can take it first.", ['mistake'])
n("d4 Nf6 Bf4 d6 e3 Nbd7 Nf3 e5 dxe5", "Take it", "Black has to take back, and that pawn stands where your knight can take it.", ['key'])
n("d4 Nf6 Bf4 d6 e3 Nbd7 Nf3 e5 dxe5 dxe5 Nxe5", "Knight takes the pawn", "Two of your pieces hit it and only Black's knight guards it. A clean pawn up, and your bishop is still on its diagonal.", ['key'])
n("d4 Nf6 Bf4 d5", "D-pawn two squares", "Back to the first chapter.")

# ============================================================== notes: the c-pawn at once
n("d4 Nf6 Bf4 c5", "The c-pawn hits the d-pawn", "Black wants to take the d-pawn, or bring the queen out at your b-pawn.")
n(BN, "Push past it", "The d-pawn gains space and gets out of the c-pawn's reach.", ['key'])
n(J(BN, "d6 Nc3"), "Knight out", "It guards the d-pawn and gets ready for the e-pawn.", ['key'])
n(J(BN, "d6 Nc3 g6 e4"), "E-pawn two squares", "Two pawns in the middle. The king's knight comes out next.", ['key'])
n(J(BN, "e6 Nc3 exd5 Nxd5"), "Knight takes back", "It stands in the middle, where no Black pawn can chase it.", ['key'])

# ============================================================== notes: other first moves
n("d4 e6", "The e-pawn first", "One club player in nine.")
n("d4 e6 Bf4", "Bishop out first", "Same as always.", ['key'])
n("d4 e6 Bf4 c5 e3 cxd4 exd4", "Take back with the e-pawn", "As always.", ['key'])
n("d4 e5", "The e-pawn gambit", "Black offers a pawn for quick development.")
n("d4 e5 dxe5", "Take it", "A free pawn. Keep it if you can do so safely.", ['key'])
n("d4 e5 dxe5 Nc6 Nf3", "Knight guards the pawn", "Black's knight and queen are coming for it.", ['key'])
n("d4 e5 dxe5 Nc6 Nf3 Qe7", "Queen at the pawn", "The usual plan. Black hopes for the trick down the diagonal later.")
n("d4 e5 dxe5 Nc6 Nf3 Qe7 Bf4", "Bishop guards the pawn too", "Two guards for one pawn.", ['key'])
n("d4 e5 dxe5 Nc6 Nf3 Qe7 Bf4 Qb4+", "Queen check", "She hits your bishop and your b-pawn at once.")
n("d4 e5 dxe5 Nc6 Nf3 Qe7 Bf4 Qb4+ Bd2", "Block with the bishop", "The usual block. Black's queen takes the b-pawn next.", ['key'])
n(EN, "The queen takes the b-pawn", "This is the moment the gambit is played for.")
n(J(EN, "Nc3"), "Knight out", "Now your queen guards the corner rook and the knight guards the a-pawn. Never the bishop to the same square: that is the trap.", ['key'], arrows=['c3a2g', 'd1a1g'])
n(J(EN, "Nc3 Bb4 Rb1"), "Rook hits the queen", "She has to keep moving.", ['key'], arrows=['b1b4g'])
n(J(EN, "Nc3 Bb4 Rb1 Qa3 Rb3"), "Rook hits the queen again", "Every move she makes is another one for you.", ['key'])
n(J(EN, "Nc3 Bb4 Rb1 Qa3 Rb3 Qa5 a3"), "A-pawn at the bishop", "The bishop has to take your knight or run. Either way you keep the extra pawn and the two bishops.", ['key'])
n(J(EN, "Bc3"), "Bishop out instead of the knight?", "It looks like it hits the queen and guards the corner.", ['warn'])
n(J(EN, "Bc3 Bb4"), "Bishop pins your bishop", "Now your bishop can't move: your king stands behind it.")
n(J(EN, "Bc3 Bb4 Qd2"), "Queen guards the bishop", None, ['warn'])
n(J(EN, "Bc3 Bb4 Qd2 Bxc3 Qxc3"), "Queen takes back", "Your back row is left without a guard.", ['warn'])
n(J(EN, "Bc3 Bb4 Qd2 Bxc3 Qxc3 Qc1#"), "Black mates you", "The famous gambit trap. Against the queen raid on the b-pawn, the knight comes out, never the bishop.", ['mate', 'warn'])
n("d4 e5 dxe5 Nc6 Nf3 Qe7 Bf4 Nxe5 Bxe5", "Bishop takes the knight", "Black's knight took the pawn back. If the queen now takes your bishop, your knight takes the queen. A piece up.", ['key'])
n("d4 e5 dxe5 Nc6 Nf3 d6 Bf4 dxe5 Nxe5", "Knight takes back", "Still a pawn up.", ['key'])
n("d4 e5 dxe5 Nc6 Nf3 Bc5 Bf4", "Bishop guards the pawn", "Black's bishop looks at f2, but nothing else is coming. Keep developing.", ['key'])
n("d4 e5 dxe5 d6 Bf4 dxe5 Qxd8+ Kxd8 Bxe5", "Bishop takes the pawn", "The queens are off and Black's king has lost the right to castle. A pawn up.", ['key'])
n("d4 Nc6 Bf4 e5 dxe5", "Take it", "The same gambit with your bishop already out.", ['key'])
n("d4 Nc6 Bf4 e5 dxe5 Qe7 Nf3", "Knight guards the pawn", "Now it is the gambit lesson move for move.", ['key'])
n("d4 Nc6 Bf4 e5 dxe5 g5 Bg3", "Bishop steps back", "Still a pawn up, and Black's g-pawn has loosened the king.", ['key'])
n("d4 c5", "The c-pawn two squares", "One club player in thirty-five.")
n(OB, "Push past it", "The d-pawn gains space. Bringing the bishop out first would leave the b-pawn to Black's queen.", ['key'])
n(J(OB, "d6 Nc3"), "Knight out", "It guards the pawn and gets ready for the e-pawn.", ['key'])
n(J(OB, "d6 Nc3 Nf6 e4"), "E-pawn two squares", "Two pawns in the middle.", ['key'])
n(J(OB, "e6 Nc3 exd5 Nxd5"), "Knight takes back", "It stands in the middle, where no Black pawn can chase it.", ['key'])
n("d4 g6", "The fianchetto first", None)
n("d4 g6 Bf4", "Bishop out first", "Same as always.", ['key'])
n("d4 d6 Bf4 e5", "The e-pawn gambit", "The pawn is offered to chase your bishop.")
n("d4 d6 Bf4 e5 dxe5 dxe5 Qxd8+", "Trade queens", "Then your bishop takes the e-pawn.", ['key'])
n("d4 d6 Bf4 e5 dxe5 Nc6 exd6", "Take the second pawn", "Two pawns taken. Black takes one back and you stay a pawn up.", ['key'])
n("d4 c6 Bf4 d5 e3 Bf5 Bd3", "Light bishop out: offer the trade", "The bishop rule.", ['key'])
n("d4 f5", "The f-pawn two squares", "The Dutch. Your bishop is already where it wants to be.")
