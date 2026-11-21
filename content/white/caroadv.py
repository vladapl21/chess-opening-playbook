"""White against the Caro-Kann, a second variation: the Advance, a pack for the slot 'whiteCaro' beside the main line
(see PACKS in content2_meta.py).

One setup: push past the d-pawn, then knight, bishop one square, castle; the c-pawn backs the chain when Black's
c-pawn hits it, and the queen's knight and the bishop follow. The lines were drafted with pipeline/draft.py: Black's
moves by the Maia 1300/1500 odds, yours from the setup's order wherever Stockfish 17.1 accepts it and the engine's
move elsewhere. SAN is internal; notes are plain English."""
from content import n, J, L, PARTS

PARTS.extend([
  dict(id='ca-push', ch='caroadv', title='The pawn pushes past', kicker='Advance Variation',
       blurb="Black's d-pawn comes to meet yours and the e-pawn steps past it. Behind the chain your pieces come out the quiet way: knight, bishop one square, castle. When the c-pawn hits the chain, yours backs it up."),
  dict(id='ca-other', ch='caroadv', title='No d-pawn to push past', kicker='Second-move sidelines',
       blurb='The rare second moves. Take the middle with both pawns and develop.'),
])

L('ca-main', 'ca-push', 'The bishop comes out: the quiet setup', 'Knight, bishop one square, castle, then the c-pawn backs the chain', 'core',
  'e4 c6 d4 d5 e5 Bf5 Nf3 e6 Be2 c5 O-O Nc6 c3 Qb6 dxc5 Bxc5 b4',
  alts=[('ca-main-bb4', 'Bishop gives check', 'e4 c6 d4 d5 e5 Bf5 Nf3 e6 Be2 Bb4+ Nc3'),
        ('ca-main-cxd4', 'Pawn takes the pawn', 'e4 c6 d4 d5 e5 Bf5 Nf3 e6 Be2 c5 O-O cxd4 Nxd4 Bg6 Be3'),
        ('ca-main-ne7', 'King\'s knight tucked in', 'e4 c6 d4 d5 e5 Bf5 Nf3 e6 Be2 Ne7 O-O Ng6 Nc3'),
        ('ca-main-nd7', 'Queen\'s knight tucked in', 'e4 c6 d4 d5 e5 Bf5 Nf3 e6 Be2 Nd7 O-O c5 c3 cxd4 Nxd4'),
        ('ca-main-nd7ne7', 'Queen\'s knight tucked in, then king\'s knight tucked in', 'e4 c6 d4 d5 e5 Bf5 Nf3 e6 Be2 Nd7 O-O Ne7 Nc3'),
        ('ca-main-cxd4v2', 'Pawn takes the pawn on move 7', 'e4 c6 d4 d5 e5 Bf5 Nf3 e6 Be2 c5 O-O Nc6 c3 cxd4 Nxd4'),
        ('ca-main-h6', 'Small h-pawn move', 'e4 c6 d4 d5 e5 Bf5 Nf3 e6 Be2 h6 O-O Ne7 Nc3'),
        ('ca-main-h6nd7', 'Small h-pawn move, then queen\'s knight tucked in', 'e4 c6 d4 d5 e5 Bf5 Nf3 e6 Be2 h6 O-O Nd7 Nc3'),
        ('ca-main-ne7nd7', 'King\'s knight tucked in, then queen\'s knight tucked in', 'e4 c6 d4 d5 e5 Bf5 Nf3 e6 Be2 Ne7 O-O Nd7 Nc3'),
        ('ca-main-cxd4bc5', 'Pawn takes the pawn, then bishop aims at f2', 'e4 c6 d4 d5 e5 Bf5 Nf3 e6 Be2 c5 O-O cxd4 Nxd4 Bc5 Bb5+'),
        ('ca-main-nge7', 'King\'s knight tucked in on move 7', 'e4 c6 d4 d5 e5 Bf5 Nf3 e6 Be2 c5 O-O Nc6 c3 Nge7 dxc5 Ng6 Be3')],
  why='Seven in ten bring the bishop out before the e-pawn shuts it in. You let it sit there: knight, bishop, castle, and the space is yours for good.', outcome='More room and an easy game')
L('ca-fourth', 'ca-push', 'The bishop comes out: other tries', 'The edge pawn, the queen, a pin on your knight', 'common',
  'e4 c6 d4 d5 e5 Bf5 Nf3 h6 Be2 e6 O-O',
  why='After the bishop Black doesn\'t always play the e-pawn. The setup comes out the same way.', outcome='More room')
L('ca-c5', 'ca-push', 'The c-pawn hits the chain at once', 'The Botvinnik-Carls: develop, and take the pawn when it helps', 'common',
  'e4 c6 d4 d5 e5 c5 Nf3 Bg4 c3',
  alts=[('ca-c5-cxd4', 'Pawn takes the pawn', 'e4 c6 d4 d5 e5 c5 Nf3 cxd4 Qxd4 Nc6 Qf4'),
        ('ca-c5-nc6', 'Queen\'s knight out', 'e4 c6 d4 d5 e5 c5 Nf3 Nc6 dxc5 e6 Nc3 Bxc5 Be2'),
        ('ca-c5-e6', 'Small e-pawn move', 'e4 c6 d4 d5 e5 c5 Nf3 e6 Bd3')],
  why='One in ten hits your d-pawn straight away, a move that usually waits. The c-pawn has now moved twice.', outcome='A move ahead')
L('ca-e6', 'ca-push', 'The e-pawn shuts the bishop in', 'A French a move behind: the same setup', 'common',
  'e4 c6 d4 d5 e5 e6 Nf3 Ne7 Be2',
  alts=[('ca-e6-c5', 'Small c-pawn move', 'e4 c6 d4 d5 e5 e6 Nf3 c5 Bd3'),
        ('ca-e6-nd7', 'Queen\'s knight tucked in', 'e4 c6 d4 d5 e5 e6 Nf3 Nd7 Be2')],
  why='One in ten locks the bishop in behind the pawns. Black is playing a French with a move lost on the c-pawn.', outcome='More room and a move ahead')
L('ca-third', 'ca-push', 'Other third moves', 'The f-pawn at your chain, the fianchetto, the queen out', 'rare',
  'e4 c6 d4 d5 e5 f6 Nf3 Bg4 Be2',
  alts=[('ca-third-fxe5', 'Pawn takes the pawn', 'e4 c6 d4 d5 e5 f6 Nf3 fxe5 dxe5')],
  why='Whatever Black tries against the chain, the pieces come out behind it in the same order.', outcome='Better for you')
L('ca-second', 'ca-other', 'Black skips the d-pawn', 'The small d-pawn, the e-pawn, the fianchetto', 'rare',
  'e4 c6 d4 d6 Nf3 h6 Be2',
  alts=[('ca-second-e6', 'Small e-pawn move', 'e4 c6 d4 e6 Nf3 d5 e5'),
        ('ca-second-nd7', 'Queen\'s knight tucked in', 'e4 c6 d4 d6 Nf3 Nd7 Be2')],
  why='Without the d-pawn in the middle there is nothing to push past. Two pawns side by side and the usual pieces.', outcome='A big center')

# ============================================================== notes
n('e4 c6 d4 d5 e5', 'Push past', 'The e-pawn steps past instead of trading. The two pawns take room from Black for the rest of the game.', ['key'])
n('e4 c6 d4 d5 e5 Bf5 Nf3', 'Knight out', 'Let the bishop sit there. Knight, then the bishop one square, then castle.', ['key'])
n('e4 c6 d4 d5 e5 Bf5 Nf3 e6 Be2', 'Bishop one square', 'Out of the way and out of reach. You castle next.', ['key'])
n('e4 c6 d4 d5 e5 Bf5 Nf3 e6 Be2 c5 O-O', 'Castle', 'King safe first. The c-pawn backs up the chain on the next move.', ['key'])
n('e4 c6 d4 d5 e5 Bf5 Nf3 e6 Be2 c5 O-O Nc6 c3', 'C-pawn backs the chain', 'Black is hitting the base of your chain. If the pawns are traded there, another pawn stands in the same place.', ['key'], arrows=['c3d4g'])
n('e4 c6 d4 d5 e5 Bf5 Nf3 e6 Be2 c5 O-O Nc6 c3 cxd4 Nxd4', 'Knight takes back', 'It lands in the middle with a hit on the bishop, and the c-pawn still keeps Black\'s knight out of the squares in front of it.', ['key'])
n('e4 c6 d4 d5 e5 Bf5 Nf3 e6 Be2 c5 O-O cxd4 Nxd4', 'Knight takes back', 'A hit on the bishop, and the knight stands in the middle of the board.', ['key'])
n('e4 c6 d4 d5 e5 c5 Nf3', 'Knight out', 'The same first move of the setup. Black\'s c-pawn has now moved twice, and you are a move ahead.', ['key'])
n('e4 c6 d4 d5 e5 e6 Nf3', 'Knight out', 'Black has shut the bishop in. The setup is the same, with more room than ever.')
# the other side's moves that start a named line
n('e4 c6 d4 d5 e5 c5', 'Botvinnik-Carls Defense')
