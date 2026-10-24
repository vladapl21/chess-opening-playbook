"""New chapters: everything after 1.e4 that isn't the Italian. Same DSL as content.py.
SAN is internal only. Notes are plain English; the only square ever named is f7."""
import content
from content import n, J, L, LESSONS, NOTES, PARTS

PARTS.extend([
  dict(id='e5x-phil', ch='e5x', title='The d-pawn defends', kicker='Philidor',
       blurb='Black guards the center pawn with the d-pawn. That shuts in Black\'s own bishop. Take the center and look at f7.'),
  dict(id='e5x-pet', ch='e5x', title='Black\'s knight hits back', kicker='Petrov',
       blurb='Black ignores your attack on the pawn and attacks yours. Take first, then watch for the copycat trap.'),
  dict(id='e5x-misc', ch='e5x', title='Odd second moves', kicker='Sidelines',
       blurb='Early queen moves and pawn lunges. Each one has a punishing answer.'),
  dict(id='caro-main', ch='caro', title='Black\'s bishop comes out', kicker='Main line',
       blurb='The most common Caro-Kann at your level. Your h-pawn chases the bishop, you trade it off, then your king goes to the queenside.'),
  dict(id='caro-other4', ch='caro', title='Black\'s knight or pawn instead', kicker='Fourth-move options',
       blurb='Black keeps the bishop home. Trade knights, then finish your development.'),
  dict(id='caro-third', ch='caro', title='Black keeps the center pawn', kicker='Third-move options',
       blurb='Black doesn\'t take your e-pawn. Push past with it and grab space.'),
  dict(id='sic-knight', ch='sic', title='Black\'s knight comes out', kicker='The most common reply',
       blurb='After the pawn trade, Black\'s knight sits within reach of your d-pawn. Push the pawn at it.'),
  dict(id='sic-pawn', ch='sic', title='Black moves a center pawn', kicker='Second-move pawn moves',
       blurb='Black supports the c-pawn with a center pawn. You still build the big center.'),
  dict(id='sic-rare', ch='sic', title='Other second moves', kicker='Sidelines',
       blurb='The queen comes out early, or Black fianchettoes. Same center, same plan.'),
  dict(id='scandi-queen', ch='scandi', title='The queen takes back', kicker='The most common reply',
       blurb='Black\'s queen comes out on move two. Hit it with your knight and develop with tempo every time it moves.'),
  dict(id='scandi-other', ch='scandi', title='Knight or pawn gambit', kicker='Second-move options',
       blurb='Black delays taking back. Keep the extra pawn or build the big center.'),
  dict(id='pirc-150', ch='pirc', title='The fianchetto', kicker='Pirc and Modern',
       blurb='Black puts the bishop on the long diagonal and castles behind it. Trade that bishop off and attack the king.'),
  dict(id='pirc-other', ch='pirc', title='Other setups', kicker='Sidelines',
       blurb='Black skips the fianchetto. Keep the big center and develop.'),
  dict(id='french-adv', ch='french', title='Lock the center', kicker='Advance variation',
       blurb='Push your e-pawn past Black\'s pawns. Black attacks your chain from the front; you support it from behind.'),
  dict(id='french-other', ch='french', title='Other second moves', kicker='Sidelines',
       blurb='Black hits your center with the c-pawn first. Same answer as in the Sicilian: the small pawn move.'),
  dict(id='rare-all', ch='rare', title='Rare first moves', kicker='Sidelines',
       blurb='Take the whole center, develop, castle. Each lesson shows the one trick to know.'),
])

# ============================================================== e5 without the knight
E5 = "e4 e5 Nf3"
PH = J(E5, "d6 d4")
L('ph-main', 'e5x-phil', 'Black takes in the center', 'Knight takes back, then a calm setup', 'core',
  J(PH, "exd4 Nxd4 Nf6 Nc3 Be7 Bf4 O-O Qd2"),
  alts=[('ph-main-c5', 'Pawn hits your knight', J(PH, "exd4 Nxd4 c5 Nf3")),
        ('ph-main-nc6', 'Knight comes out', J(PH, "exd4 Nxd4 Nc6 Nc3 Nf6 Bf4"))],
  why='The usual Philidor at your level. You went 1–3 against it.', outcome='Your pieces are freer; Black is cramped')
L('ph-bg4', 'e5x-phil', 'The pin: Morphy\'s answer', 'Take twice, then hit f7 and the loose pawn', 'common',
  J(PH, "Bg4 dxe5 Bxf3 Qxf3 dxe5 Bc4 Nf6 Qb3 Qe7 Nc3"),
  alts=[('ph-bg4-qd7', 'Queen guards: grab the pawn', J(PH, "Bg4 dxe5 Bxf3 Qxf3 dxe5 Bc4 Nf6 Qb3 Qd7 Qxb7")),
        ('ph-bg4-qf6', 'Queen to the side', J(PH, "Bg4 dxe5 Bxf3 Qxf3 dxe5 Bc4 Qf6 Qb3")),
        ('ph-bg4-dxe5', 'Pawn takes back: queen trade wins a pawn', J(PH, "Bg4 dxe5 dxe5 Qxd8+ Kxd8 Nxe5"))],
  why='Morphy beat a duke and a count with exactly this idea in 1858.', outcome='Black\'s queenside is falling')
L('ph-nf6', 'e5x-phil', 'Knight hits your e-pawn', 'Take, then the queen forks the knight and f7', 'common',
  J(PH, "Nf6 dxe5 Nxe4 Qd5 Nc5 Bg5 Be7 exd6 cxd6 Nc3"),
  alts=[('ph-nf6-dxe5', 'Pawn takes back: queen trade wins a pawn', J(PH, "Nf6 dxe5 dxe5 Qxd8+ Kxd8 Nxe5 Be6 f3")),
        ('ph-nf6-bf5', 'Bishop guards the knight', J(PH, "Nf6 dxe5 Nxe4 Qd5 Bf5 Bc4"))],
  why='A natural move that walks into a queen fork.', outcome='You are a tempo up with Black\'s king still home')
L('ph-nd7', 'e5x-phil', 'Knight to the side: the f7 shot', 'Bishop out, and the sacrifice when Black slips', 'core',
  J(PH, "Nd7 Bc4 h6 dxe5 dxe5 Bxf7+ Kxf7 Nxe5+"),
  alts=[('ph-nd7-nxe5', 'Knight takes back', J(PH, "Nd7 Bc4 h6 dxe5 Nxe5 Nxe5 dxe5 Bxf7+ Ke7 Qf3")),
        ('ph-nd7-ngf6', 'Both knights out: the queen trap', J(PH, "Nd7 Bc4 Ngf6 dxe5 dxe5 Ng5")),
        ('ph-nd7-be7', 'Bishop out: queen to the center', J(PH, "Nd7 Bc4 Be7 dxe5 dxe5 Qd5")),
        ('ph-nd7-c6', 'Pawn to the side', J(PH, "Nd7 Bc4 c6 Ng5 Nh6 O-O"))],
  why='You missed this exact shot against Nona_Zulfa on Oct 14.', outcome='You win material on f7', tags=['game'])
L('ph-nc6', 'e5x-phil', 'The knight defends', 'Push past it and grab space', 'rare',
  J(PH, "Nc6 d5 Nce7 c4"),
  why='Black\'s knight blocks its own c-pawn.', outcome='More space for you')

PT = J(E5, "Nf6")
L('pt-main', 'e5x-pet', 'Take the pawn, then build', 'Grab first, chase the knight, take the center', 'core',
  J(PT, "Nxe5 d6 Nf3 Nxe4 d4 d5 Bd3 Bd6 O-O O-O c4"),
  alts=[('pt-main-nc6', 'Knight to the center', J(PT, "Nxe5 d6 Nf3 Nxe4 d4 d5 Bd3 Nc6 O-O Be7 c4")),
        ('pt-main-bf5', 'Bishop offers a trade', J(PT, "Nxe5 d6 Nf3 Nxe4 d4 d5 Bd3 Bf5 O-O")),
        ('pt-main-qe7', 'Queen pins the knight', J(PT, "Nxe5 d6 Nf3 Nxe4 d4 Qe7 Be2")),
        ('pt-main-bg4', 'Bishop pins your knight', J(PT, "Nxe5 d6 Nf3 Nxe4 d4 Bg4 Bd3")),
        ('pt-main-be7', 'Bishop to the quiet square', J(PT, "Nxe5 d6 Nf3 Nxe4 d4 Be7 Bd3"))],
  why='The normal Petrov. Calm, but your pieces come out faster.', outcome='A small, safe edge')
L('pt-copy', 'e5x-pet', 'The copycat trap', 'Black copies you and loses the queen', 'core',
  J(PT, "Nxe5 Nxe4 Qe2 Qe7 Qxe4 d6 d4 dxe5 dxe5 Nc6 Bb5"),
  alts=[('pt-copy-nf6', 'Knight retreats: discovered check', J(PT, "Nxe5 Nxe4 Qe2 Nf6 Nc6+")),
        ('pt-copy-d5', 'Pawn defends, then the knight retreats', J(PT, "Nxe5 Nxe4 Qe2 d5 d3 Nf6 Nc6+"))],
  why='Club players grab back the pawn about one time in five. It costs them.', outcome='You are a pawn up, or Black\'s queen is gone', tags=['trap'])
L('pt-stafford', 'e5x-pet', 'The knight gambit', 'Take the knight, then one safe pawn move', 'common',
  J(PT, "Nxe5 Nc6 Nxc6 dxc6 d3 Bc5 Be2 O-O O-O"),
  alts=[('pt-stafford-ng4', 'Knight jumps at f2', J(PT, "Nxe5 Nc6 Nxc6 dxc6 d3 Bc5 Be2 Ng4 Bxg4 Bxg4 Qxg4")),
        ('pt-stafford-qd4', 'Queen hits f2', J(PT, "Nxe5 Nc6 Nxc6 dxc6 d3 Bc5 Be2 Qd4 O-O")),
        ('pt-stafford-h5', 'The h-pawn trick', J(PT, "Nxe5 Nc6 Nxc6 dxc6 d3 Bc5 Be2 h5 c3 Ng4 d4")),
        ('pt-stafford-bxc6', 'Other pawn takes back', J(PT, "Nxe5 Nc6 Nxc6 bxc6 Nc3"))],
  why='A popular online trap. The safe pawn move and the bishop kill it.', outcome='You are a pawn up and safe')
L('pt-qe7', 'e5x-pet', 'Queen comes out early', 'Take the center; the queen grabs a pawn but falls behind', 'rare',
  J(PT, "Nxe5 Qe7 d4 d6 Nf3 Nxe4 Be2"),
  alts=[('pt-qe7-nxe4', 'Knight grabs at once', J(PT, "Nxe5 Qe7 d4 Nxe4 Bd3"))],
  why='The queen blocks Black\'s own bishop.', outcome='You are well ahead in development')

L('x-qf6', 'e5x-misc', 'The queen guards the pawn', 'Develop with threats; the queen gets kicked', 'common',
  J(E5, "Qf6 Nc3 c6 d4 exd4 Bg5 Qg6 Qxd4"),
  alts=[('x-qf6-d6', 'The d-pawn guards', J(E5, "Qf6 Nc3 c6 d4 d6 Bg5")),
        ('x-qf6-nc6', 'Knight defends instead', J(E5, "Qf6 Nc3 Nc6 Nd5"))],
  why='You won both games against it. Here is the cleanest answer.', outcome='Black\'s queen has been kicked around')
L('x-bc5', 'e5x-misc', 'Bishop out, pawn hangs', 'Take the pawn; the fork trick doesn\'t work', 'common',
  J(E5, "Bc5 Nxe5 Qe7 d4 Bb6 Nc3"),
  alts=[('x-bc5-bxf2', 'Bishop takes f2', J(E5, "Bc5 Nxe5 Bxf2+ Kxf2 Qh4+ g3 Qxe4 Qe2"))],
  why='Black forgets to defend the e-pawn.', outcome='You are a pawn up with the better position')
L('x-f6', 'e5x-misc', 'The pawn guard', 'Take the pawn anyway; Black\'s king or rook pays', 'rare',
  J(E5, "f6 Nxe5 fxe5 Qh5+ g6 Qxe5+ Qe7 Qxh8"),
  alts=[('x-f6-ke7', 'The king walks', J(E5, "f6 Nxe5 fxe5 Qh5+ Ke7 Qxe5+ Kf7 Bc4+ Kg6 Qf5+ Kh6 h4")),
        ('x-f6-qe7', 'Black\'s best: queen counters', J(E5, "f6 Nxe5 Qe7 Nf3 Qxe4+ Be2"))],
  why='Guarding with the f-pawn weakens Black\'s king for good.', outcome='A winning attack')
L('x-f5', 'e5x-misc', 'The pawn lunge', 'Take in the center and develop with threats', 'rare',
  J(E5, "f5 Nxe5 Nf6 Bc4 d5 exd5 Nxd5 O-O"),
  alts=[('x-f5-qf6', 'Queen to the edge of the attack', J(E5, "f5 Nxe5 Qf6 d4 d6 Nc4 fxe4 Nc3")),
        ('x-f5-fxe4', 'Queen out, then the pawn grab', J(E5, "f5 Nxe5 Qf6 d4 fxe4 Bc4"))],
  why='A gambit that leaves Black\'s king open.', outcome='Fast attack on the open king')
L('x-d5', 'e5x-misc', 'The pawn counter', 'Take, then put your queen in front', 'rare',
  J(E5, "d5 exd5 e4 Qe2 Nf6 Nc3"),
  alts=[('x-d5-qxd5', 'Queen takes back', J(E5, "d5 exd5 Qxd5 Nc3"))],
  why='Black gambits a center pawn.', outcome='You are a pawn up')

# ============================================================== Caro-Kann
CK = "e4 c6 d4 d5 Nc3"
CKX = J(CK, "dxe4 Nxe4")
CKG = J(CKX, "Bf5 Ng3 Bg6 h4")
L('ck-march', 'caro-main', 'The h-pawn march', 'Chase the bishop, trade it, castle long', 'core',
  J(CKG, "h6 Nf3 e6 h5 Bh7 Bd3 Bxd3 Qxd3 Nf6 Bd2 Nbd7 O-O-O"),
  alts=[('ck-march-nf6', 'Knight out first', J(CKG, "h6 Nf3 Nf6 h5 Bh7 Bd3 Bxd3 Qxd3 e6 Bd2")),
        ('ck-march-nd7', 'Queen\'s knight first', J(CKG, "h6 Nf3 Nd7 h5 Bh7 Bd3 Bxd3 Qxd3 e6 Bd2 Ngf6 O-O-O")),
        ('ck-march-qnd7', 'Knight after the trade', J(CKG, "h6 Nf3 e6 h5 Bh7 Bd3 Bxd3 Qxd3 Nd7 Bd2 Ngf6 O-O-O")),
        ('ck-march-keep', 'Black won\'t trade', J(CKG, "h6 Nf3 e6 h5 Bh7 Bd3 Nf6 Bxh7 Nxh7 Bf4"))],
  why='The most common Caro-Kann at your level, and the one you play already.', outcome='Kings on opposite sides; your pieces are freer')
L('ck-h5', 'caro-main', 'Black stops the h-pawn', 'Knight to the edge, then hunt the bishop', 'common',
  J(CKG, "h5 Nh3 e6 Nf4 Bh7 Bc4 Nf6 O-O"),
  alts=[('ck-h5-bd6', 'Bishop offers a trade', J(CKG, "h5 Nh3 e6 Nf4 Bd6 Nxg6 fxg6 Bd3")),
        ('ck-h5-nf6', 'Knight first', J(CKG, "h5 Nh3 Nf6 Nf4 Bh7 Bc4 e6 O-O"))],
  why='Black blocks your pawn for good, so the knight does the chasing.', outcome='The bishop is stuck on the edge')
L('ck-bishop6', 'caro-main', 'Black ignores the h-pawn', 'The bishop gets chased, traded or lost', 'common',
  J(CKG, "e6 h5 Bf5 Nxf5 exf5 Bd3"),
  alts=[('ck-bishop6-be4', 'Knight out: bishop runs to the center', J(CKG, "Nf6 h5 Be4 Nxe4 Nxe4 h6")),
        ('ck-bishop6-bxh5', 'Bishop grabs the pawn: free piece', J(CKG, "Nf6 h5 Bxh5 Nxh5 Nxh5 Rxh5")),
        ('ck-bishop6-nxh5', 'Knight grabs the pawn: free piece', J(CKG, "Nf6 h5 Nxh5 Nxh5 Bxh5 Rxh5"))],
  why='The h-pawn push is a real threat. Black has to answer it.', outcome='You keep both bishops, or win a piece')
L('ck-takes', 'caro-main', 'Black lets you take the bishop', 'Your knight takes it; Black\'s pawns are wrecked', 'common',
  J(CKX, "Bf5 Ng3 e6 Nxf5 exf5 Nf3 Nf6 Bd3"),
  alts=[('ck-takes-nf6', 'Knight out: the bishop hangs', J(CKX, "Bf5 Ng3 Nf6 Nxf5 e6 Ne3")),
        ('ck-takes-qa5', 'The queen-check rescue', J(CKX, "Bf5 Ng3 Nf6 Nxf5 Qa5+ Bd2 Qxf5 Nf3"))],
  why='You won a whole piece this way against ykayyy in July.', outcome='Two bishops for you, weak pawns for Black', tags=['game'])
L('ck-nf6', 'caro-other4', 'Knight trade, broken pawns', 'Take the knight, then bishop and queen at the king', 'core',
  J(CKX, "Nf6 Nxf6+ exf6 c3 Bd6 Bd3 O-O Ne2 Re8 Qc2"),
  alts=[('ck-nf6-be7', 'Quiet bishop', J(CKX, "Nf6 Nxf6+ exf6 c3 Be7 Bd3 O-O Ne2 Re8 Qc2")),
        ('ck-nf6-gxf6', 'Pawn takes toward the side', J(CKX, "Nf6 Nxf6+ gxf6 c3 Bf5 Nf3 e6 Be2")),
        ('ck-nf6-bg7', 'Bishop to the long diagonal', J(CKX, "Nf6 Nxf6+ gxf6 c3 Bg7 Bd3")),
        ('ck-nf6-e5', 'Pawn hits the center', J(CKX, "Nf6 Nxf6+ gxf6 c3 e5 Nf3 exd4 Nxd4"))],
  why='The second most common Caro-Kann. You retreated the knight here every time and went 2–3.', outcome='Healthier pawns for you', tags=['swap'])
L('ck-quiet', 'caro-other4', 'Black keeps the bishop home', 'Develop, trade knights, hit the queen', 'rare',
  J(CKX, "e6 Nf3 Nf6 Nxf6+ Qxf6 Bg5"),
  alts=[('ck-quiet-nd7', 'Knight first', J(CKX, "e6 Nf3 Nd7 Bd3 Ngf6 O-O")),
        ('ck-quiet-karpov', 'Queen\'s knight first', J(CKX, "Nd7 Nf3 Ngf6 Nxf6+ Nxf6 c3"))],
  why='Solid but passive. Your pieces come out faster.', outcome='More space for you')
L('ck-nf6-3', 'caro-third', 'Knight hits your e-pawn', 'Push past the knight', 'common',
  J(CK, "Nf6 e5 Ne4 Nxe4 dxe4 Bc4 e6 Ne2"),
  alts=[('ck-nf6-3-bf5', 'Bishop guards the pawn', J(CK, "Nf6 e5 Ne4 Nxe4 dxe4 Bc4 Bf5 Ne2")),
        ('ck-nf6-3-nfd7', 'Knight retreats', J(CK, "Nf6 e5 Nfd7 Nf3 e6 Ng5"))],
  why='About one Caro-Kann in five goes this way.', outcome='You have more space')
L('ck-e6-3', 'caro-third', 'The pawn to the side', 'Knight out, then push past', 'common',
  J(CK, "e6 Nf3 Bb4 e5 Ne7 a3 Bxc3+ bxc3"),
  alts=[('ck-e6-3-bxc3', 'Bishop takes at once', J(CK, "e6 Nf3 Bb4 e5 Bxc3+ bxc3")),
        ('ck-e6-3-nf6', 'Knight hits your e-pawn', J(CK, "e6 Nf3 Nf6 e5 Nfd7 Ng5")),
        ('ck-e6-3-dxe4', 'Black takes after all', J(CK, "e6 Nf3 dxe4 Nxe4 Nf6 Nxf6+ Qxf6 Bg5"))],
  why='A French-style setup. You get space for free.', outcome='Space and the two bishops')

# ============================================================== Sicilian (small pawn move)
SC = "e4 c5 c3"
SN = J(SC, "Nc6 d4 cxd4 cxd4")
L('sc-push', 'sic-knight', 'Push past the knight', 'Kick the knight from the center and chase it', 'core',
  J(SN, "Nf6 d5 Ne5 f4 Ng6 e5"),
  alts=[('sc-push-qa5', 'Queen check', J(SN, "Nf6 d5 Ne5 f4 Qa5+ Bd2 Qb6 fxe5")),
        ('sc-push-neg4', 'Knight jumps forward', J(SN, "Nf6 d5 Ne5 f4 Neg4 Nc3")),
        ('sc-push-nb4', 'Knight to the edge', J(SN, "Nf6 d5 Nb4 a3 Na6 e5")),
        ('sc-push-g6', 'Fianchetto first', J(SN, "g6 d5 Ne5 f4 Qa5+ Bd2 Qb6 fxe5")),
        ('sc-push-g6b', 'Fianchetto, the knight is lost', J(SN, "g6 d5 Ne5 f4 Bg7 fxe5")),
        ('sc-push-d6', 'Pawn guards first', J(SN, "d6 d5 Ne5 f4 Ng6 Nc3")),
        ('sc-push-d6b', 'Pawn guards, knight to the side', J(SN, "d6 d5 Ne5 f4 Nd7 Nc3"))],
  why='You had this shot three times and played a quiet move instead.', outcome='Black\'s knight has nowhere to go', tags=['game'])
L('sc-e5push', 'sic-knight', 'Black pushes the e-pawn', 'Push past again; the knight jumps to the center', 'common',
  J(SN, "e5 d5 Nd4 Nf3 Nxf3+ Qxf3"),
  alts=[('sc-e5push-nce7', 'Knight retreats', J(SN, "e5 d5 Nce7 Nc3"))],
  why='Black copies your pawn move. Same answer: push past.', outcome='Space for you')
L('sc-e6', 'sic-knight', 'The French-style setup', 'Develop, then push past when Black hits the center', 'common',
  J(SN, "e6 Nf3 d5 e5 Bb4+ Nc3 Nge7 Bd3"),
  alts=[('sc-e6-nge7', 'Knight heads for your d-pawn', J(SN, "e6 Nf3 d5 e5 Nge7 a3")),
        ('sc-e6-f6', 'Black hits your chain', J(SN, "e6 Nf3 d5 e5 f6 Nc3")),
        ('sc-e6-nf6', 'Knight out', J(SN, "e6 Nf3 Nf6 Nc3 Bb4 Bd3")),
        ('sc-e6-bb4', 'Bishop check', J(SN, "e6 Nf3 Bb4+ Nc3 Nf6 Bd3"))],
  why='The most common reply after the knight, at your level.', outcome='Space and a free game')
L('sc-d5', 'sic-knight', 'Black strikes the center', 'Take, develop, and watch for the queen grab', 'common',
  J(SN, "d5 exd5 Qxd5 Nf3 Bg4 Be2 Bxf3 Bxf3 Qxd4 Bxc6+ bxc6 Qxd4"),
  alts=[('sc-d5-nf6', 'Knight out after the pin', J(SN, "d5 exd5 Qxd5 Nf3 Bg4 Be2 Nf6 Nc3")),
        ('sc-d5-ooo', 'Black castles long', J(SN, "d5 exd5 Qxd5 Nf3 Bg4 Be2 O-O-O Nc3")),
        ('sc-d5-e6', 'Pawn to the side', J(SN, "d5 exd5 Qxd5 Nf3 Bg4 Be2 e6 O-O")),
        ('sc-d5-nf6b', 'Knight out first', J(SN, "d5 exd5 Qxd5 Nf3 Nf6 Nc3"))],
  why='Black opens the game for the queen. One greedy capture loses it.', outcome='Free development, or Black\'s queen', tags=['trap'])
L('sc-d6', 'sic-pawn', 'The d-pawn first', 'Same big center, same push', 'core',
  J(SC, "d6 d4 cxd4 cxd4 Nf6 Nc3 g6 Nf3 Bg7 Be2 O-O O-O"),
  alts=[('sc-d6-e6', 'Pawn to the side', J(SC, "d6 d4 cxd4 cxd4 Nf6 Nc3 e6 Nf3 Be7 Bd3")),
        ('sc-d6-nc6', 'Knight in front of the pawn', J(SC, "d6 d4 cxd4 cxd4 Nf6 Nc3 Nc6 d5 Ne5 f4")),
        ('sc-d6-nc6b', 'Knight first', J(SC, "d6 d4 cxd4 cxd4 Nc6 d5 Ne5 f4")),
        ('sc-d6-e6b', 'The e-pawn first', J(SC, "d6 d4 cxd4 cxd4 e6 Nf3")),
        ('sc-d6-g6', 'Fianchetto first', J(SC, "d6 d4 cxd4 cxd4 g6 Nc3 Bg7 Nf3"))],
  why='The second most common reply at your level.', outcome='The big center is yours')
L('sc-e6p', 'sic-pawn', 'The e-pawn first', 'Push past: the French structure', 'common',
  J(SC, "e6 d4 d5 e5 Nc6 Nf3"),
  alts=[('sc-e6p-cxd4', 'Trade first, then the center pawn', J(SC, "e6 d4 cxd4 cxd4 d5 e5 Nc6 Nf3")),
        ('sc-e6p-nc6', 'Knight out', J(SC, "e6 d4 cxd4 cxd4 Nc6 Nf3")),
        ('sc-e6p-x', 'Black trades on move four', J(SC, "e6 d4 d5 e5 cxd4 cxd4"))],
  why='This reaches the same position as your French chapter.', outcome='A French with your space advantage')
L('sc-e5', 'sic-pawn', 'Black\'s e-pawn goes two', 'Bishop out: an Italian with a hole for your knight', 'common',
  J(SC, "e5 Nf3 Nc6 Bc4 Nf6 Ng5 d5 exd5 Nxd5 d4"),
  alts=[('sc-e5-na5', 'Knight to the edge: check first', J(SC, "e5 Nf3 Nc6 Bc4 Nf6 Ng5 d5 exd5 Na5 Bb5+")),
        ('sc-e5-h6', 'Black stops your knight', J(SC, "e5 Nf3 Nc6 Bc4 h6 O-O")),
        ('sc-e5-d6', 'The d-pawn first', J(SC, "e5 Nf3 Nc6 Bc4 d6 O-O")),
        ('sc-e5-d6b', 'The d-pawn before the knight', J(SC, "e5 Nf3 d6 Bc4 h6 d4"))],
  why='This looks like your Italian, and the knight jump at f7 is back.', outcome='Italian-style pressure on f7')
L('sc-qd5', 'sic-rare', 'The center counter', 'Take, then the big center', 'common',
  J(SC, "d5 exd5 Qxd5 d4 Nf6 Nf3 Bg4 Be2 e6 O-O"),
  alts=[('sc-qd5-cxd4', 'Black trades first', J(SC, "d5 exd5 Qxd5 d4 cxd4 cxd4 Nc6 Nf3"))],
  why='The textbook answer to your small pawn move. You played the d-pawn first and lost.', outcome='Easy development for you', tags=['swap'])
L('sc-g6', 'sic-rare', 'The fianchetto', 'Big center, then push past the knight', 'common',
  J(SC, "g6 d4 cxd4 cxd4 Bg7 Nc3 Nc6 d5"),
  alts=[('sc-g6-d6', 'Pawn guards', J(SC, "g6 d4 cxd4 cxd4 Bg7 Nc3 d6 Nf3")),
        ('sc-g6-e6', 'Pawn to the side', J(SC, "g6 d4 cxd4 cxd4 Bg7 Nc3 e6 Bf4"))],
  why='You faced this three times.', outcome='Black\'s knight gets pushed around')
L('sc-nf6', 'sic-rare', 'Knight hits your e-pawn', 'Push past, then the bishop', 'rare',
  J(SC, "Nf6 e5 Nd5 d4 cxd4 cxd4 d6 Nf3 dxe5 dxe5 Nc6 Bc4"),
  alts=[('sc-nf6-nc6', 'Knight out', J(SC, "Nf6 e5 Nd5 d4 cxd4 cxd4 Nc6 Nc3")),
        ('sc-nf6-e6', 'Pawn to the side', J(SC, "Nf6 e5 Nd5 d4 cxd4 cxd4 e6 Nf3 Nc6 Bc4")),
        ('sc-nf6-bb4', 'Bishop check', J(SC, "Nf6 e5 Nd5 d4 cxd4 cxd4 e6 Nf3 Bb4+ Nbd2"))],
  why='The other textbook answer. Your bishop goes to the f7 diagonal again.', outcome='Space for you')

# ============================================================== Scandinavian
SD = "e4 d5 exd5"
SQ = J(SD, "Qxd5 Nc3")
L('sd-qa5', 'scandi-queen', 'The queen to the side', 'Develop, break the pin, castle long', 'core',
  J(SQ, "Qa5 d4 Nf6 Nf3 Bg4 h3 Bxf3 Qxf3 c6 Bd2"),
  alts=[('sd-qa5-nc6', 'Knight out after the trade', J(SQ, "Qa5 d4 Nf6 Nf3 Bg4 h3 Bxf3 Qxf3 Nc6 Bb5")),
        ('sd-qa5-bh5', 'Bishop keeps the pin', J(SQ, "Qa5 d4 Nf6 Nf3 Bg4 h3 Bh5 g4 Bg6 Ne5")),
        ('sd-qa5-c6', 'The c-pawn first', J(SQ, "Qa5 d4 c6 Bc4 Nf6 Nf3 Bg4 h3")),
        ('sd-qa5-c6b', 'Knight, then the c-pawn', J(SQ, "Qa5 d4 Nf6 Nf3 c6 Bc4 Bg4 h3")),
        ('sd-qa5-bf5', 'Bishop out first', J(SQ, "Qa5 d4 Bf5 Nf3 e6 Bd2"))],
  why='A main line. Your old pawn gambit here is shown too, so you know why to drop it.', outcome='Free, quick development for you', tags=['swap'])
L('sd-qd8', 'scandi-queen', 'The queen goes home', 'Big center, easy development', 'core',
  J(SQ, "Qd8 d4 Nf6 Nf3 e6 Bd3 Bb4 O-O"),
  alts=[('sd-qd8-bg4', 'Bishop pins your knight', J(SQ, "Qd8 d4 Nf6 Nf3 Bg4 h3")),
        ('sd-qd8-e6', 'Pawn first', J(SQ, "Qd8 d4 e6 Nf3 Bb4 Bd3")),
        ('sd-qd8-nc6', 'Knight out: push past it', J(SQ, "Qd8 d4 Nc6 d5")),
        ('sd-qd8-bf5', 'Bishop out', J(SQ, "Qd8 d4 Nf6 Nf3 Bf5 Bd3")),
        ('sd-qd8-bf5b', 'Bishop out before the knight', J(SQ, "Qd8 d4 Bf5 Qf3"))],
  why='The most common queen move at your level.', outcome='A clean edge in space and time')
L('sd-qe6', 'scandi-queen', 'Queen check down the file', 'Block with the bishop, not the queen', 'core',
  J(SQ, "Qe6+ Be2 Nf6 Nf3 Nc6 d4"),
  alts=[('sd-qe6-nc6', 'Knight first', J(SQ, "Qe6+ Be2 Nc6 d4")),
        ('sd-qe6-qg6', 'Queen grabs your pawn', J(SQ, "Qe6+ Be2 Qg6 Nf3 Qxg2 Rg1 Qh3 Rg3"))],
  why='You blocked with your queen against FernandoUK and lost the game.', outcome='You are well ahead in development', tags=['swap', 'game'])
L('sd-qe5', 'scandi-queen', 'Queen check from the center', 'Bishop blocks, then the big center', 'common',
  J(SQ, "Qe5+ Be2 Bg4 d4"),
  alts=[('sd-qe5-c6', 'The c-pawn first', J(SQ, "Qe5+ Be2 c6 d4 Qc7 Nf3 Nf6 O-O")),
        ('sd-qe5-nf6', 'Knight first', J(SQ, "Qe5+ Be2 Nf6 d4 Qa5 Nf3"))],
  why='The queen gets hit again on the next move.', outcome='You are well ahead in development')
L('sd-qd6', 'scandi-queen', 'The queen in front', 'Knight jumps at it', 'rare',
  J(SQ, "Qd6 d4 Nf6 Nf3 Bg4 h3"),
  alts=[('sd-qd6-nc6', 'Knight out: the queen gets chased', J(SQ, "Qd6 d4 Nc6 Nb5")),
        ('sd-qd6-g6', 'Fianchetto', J(SQ, "Qd6 d4 Nf6 Nf3 g6 Nb5 Qb6 a4"))],
  why='The queen blocks Black\'s own pawn. Hit it.', outcome='Black\'s queen keeps moving')
L('sd-b4', 'scandi-queen', 'Your old pawn gambit', 'Why to drop it', 'rare',
  J(SQ, "Qa5 b4 Qxb4 Nb5"),
  why='You won three games with this, but a careful player just takes the pawn.', outcome='Black is better')
L('sd-nf6', 'scandi-other', 'The knight takes back', 'Big center: two pawns side by side', 'common',
  J(SD, "Nf6 d4 Nxd5 Nf3 Bg4 c4 Nf6 Be2"),
  alts=[('sd-nf6-nc6', 'Knight out', J(SD, "Nf6 d4 Nxd5 Nf3 Nc6 c4 Nf6 Be2")),
        ('sd-nf6-e6', 'Pawn to the side', J(SD, "Nf6 d4 Nxd5 Nf3 e6 c4 Nf6 Nc3")),
        ('sd-nf6-nb6', 'Knight retreats to the side', J(SD, "Nf6 d4 Nxd5 Nf3 e6 c4 Nb6 Nc3")),
        ('sd-nf6-qxd5', 'Queen takes instead', J(SD, "Nf6 d4 Qxd5 Nc3 Qa5 Nf3")),
        ('sd-nf6-qd8', 'Queen takes, then goes home', J(SD, "Nf6 d4 Qxd5 Nc3 Qd8 Nf3"))],
  why='Black takes back with the knight. You get the big center for free.', outcome='Space and an easy game')
L('sd-c6', 'scandi-other', 'The pawn gambit', 'Take it and keep it', 'rare',
  J(SD, "c6 dxc6 Nxc6 Nf3 e5 Nc3"),
  alts=[('sd-c6-nf6', 'Knight out', J(SD, "c6 dxc6 Nxc6 Nf3 Nf6 Bb5")),
        ('sd-c6-bg4', 'Bishop pins', J(SD, "c6 dxc6 Nxc6 Nf3 Bg4 h3"))],
  why='You lost to this in July. Take the pawn, develop, don\'t rush.', outcome='A pawn up', tags=['game'])

# ============================================================== Pirc and Modern
PD = "e4 d6 d4"
PN = J(PD, "Nf6 Nc3 g6 Be3 Bg7 Qd2")
L('pc-150', 'pirc-150', 'Trade the bishop, go for the king', 'Queen and bishop line up; castle long and push', 'core',
  J(PN, "O-O O-O-O"),
  alts=[('pc-150-nc6', 'Knight out', J(PN, "O-O O-O-O Nc6 f3 e5 d5 Ne7 g4")),
        ('pc-150-nbd7', 'Knight behind the pawn', J(PN, "O-O O-O-O Nbd7 Bh6")),
        ('pc-150-c6b', 'The c-pawn after castling', J(PN, "O-O O-O-O c6 Bh6 b5 f3")),
        ('pc-150-c6', 'Black waits with the c-pawn', J(PN, "c6 Bh6 O-O h4")),
        ('pc-150-ng4', 'Knight hits your bishop', J(PN, "Ng4 Bg5 O-O h3"))],
  why='The plan that wins the most club games against this setup.', outcome='Black\'s king is in danger')
L('pc-modern', 'pirc-150', 'Bishop first: the Modern', 'Same setup, same plan', 'common',
  J("e4 g6 d4 Bg7 Nc3 d6 Be3 Nf6 Qd2"),
  alts=[('pc-modern-e6', 'Pawn to the side', J("e4 g6 d4 Bg7 Nc3 e6 Be3 Ne7 Qd2")),
        ('pc-modern-c6', 'The c-pawn, then the center', J("e4 g6 d4 Bg7 Nc3 c6 Be3 d5 e5")),
        ('pc-modern-c6d6', 'The c-pawn, then the d-pawn', J("e4 g6 d4 Bg7 Nc3 c6 Be3 d6 Qd2")),
        ('pc-modern-b6', 'Second fianchetto', J("e4 g6 d4 Bg7 Nc3 b6 Bc4"))],
  why='Black starts with the bishop. You still trade it off.', outcome='Same plan as the Pirc')
L('pc-e5', 'pirc-other', 'Black strikes with the e-pawn', 'Trade queens: Black can\'t castle', 'common',
  J(PD, "e5 dxe5 dxe5 Qxd8+ Kxd8 Bc4"),
  alts=[('pc-e5-nc6', 'Knight hits your pawn: take another', J(PD, "e5 dxe5 Nc6 exd6 Bxd6 Nc3"))],
  why='You met this in July. Take the pawn; Black doesn\'t get enough for it.', outcome='Black\'s king is stuck in the middle', tags=['game'])
L('pc-other', 'pirc-other', 'Other second moves', 'Big center, knights out, castle', 'rare',
  J(PD, "e6 Nf3 d5 e5"),
  alts=[('pc-other-c6', 'The c-pawn', J(PD, "c6 Nf3 Nf6 Nc3")),
        ('pc-other-g6', 'Fianchetto: back to the plan', J(PD, "g6 Nc3 Bg7 Be3")),
        ('pc-other-nbd7', 'Knight behind the pawn', J(PD, "Nf6 Nc3 Nbd7 f4")),
        ('pc-other-e5', 'Pawn strike after the knight', J(PD, "Nf6 Nc3 e5 Nf3"))],
  why='Rarer setups. The same principles work.', outcome='The big center is yours')

# ============================================================== French (advance)
FR = "e4 e6 d4 d5 e5"
FC = J(FR, "c5 c3 Nc6 Nf3")
L('fr-qb6', 'french-adv', 'The queen hits your chain', 'Small pawn move, then hit the queen with your knight', 'core',
  J(FC, "Qb6 a3 cxd4 cxd4 Nge7 Nc3 Nf5 Na4 Qa5+ b4"),
  alts=[('fr-qb6-bd7', 'Bishop out first', J(FC, "Qb6 a3 Bd7 b4 cxd4 cxd4 Rc8 Bb2")),
        ('fr-qb6-cxb4', 'Bishop out, then the pawn grab', J(FC, "Qb6 a3 Bd7 b4 cxb4 axb4")),
        ('fr-qb6-ne7', 'Knight first', J(FC, "Qb6 a3 Nge7 b4 Nf5 bxc5")),
        ('fr-qb6-ne7x', 'Knight, then the trade', J(FC, "Qb6 a3 Nge7 b4 cxd4 cxd4 Nf5 Bb2")),
        ('fr-qb6-bd7x', 'Trade, then the bishop', J(FC, "Qb6 a3 cxd4 cxd4 Bd7 b4"))],
  why='The main French at your level. One plan covers it.', outcome='Space on both sides of the board')
L('fr-other5', 'french-adv', 'Black develops instead', 'Bishop out and castle', 'common',
  J(FC, "Bd7 Be2 Qb6 O-O"),
  alts=[('fr-other5-ne7b', 'Bishop, then the knight', J(FC, "Bd7 Be2 Nge7 O-O")),
        ('fr-other5-ne7', 'Knight first', J(FC, "Nge7 Bd3 Nf5 dxc5")),
        ('fr-other5-cxd4', 'Black trades and checks', J(FC, "cxd4 cxd4 Bb4+ Nc3")),
        ('fr-other5-cxne7', 'Black trades, knight out', J(FC, "cxd4 cxd4 Nge7 Nc3 Nf5 a3"))],
  why='Calm development. Keep your pawn chain and finish your setup.', outcome='A space edge')
L('fr-early', 'french-adv', 'Black skips the knight', 'Same structure, same ideas', 'common',
  J(FR, "c5 c3 Qb6 Nf3 Nc6 a3"),
  alts=[('fr-early-cxd4', 'Trade right away', J(FR, "c5 c3 cxd4 cxd4 Nc6 Nf3")),
        ('fr-early-bb4', 'Trade, then the bishop check', J(FR, "c5 c3 cxd4 cxd4 Bb4+ Nc3")),
        ('fr-early-nc6', 'Knight before the c-pawn', J(FR, "Nc6 Nf3 f6 Bb5"))],
  why='Move orders change; the plan doesn\'t.', outcome='Back in the main plan')
L('fr-c5', 'french-other', 'The c-pawn first', 'Small pawn move: the Sicilian answer', 'common',
  J("e4 e6 d4 c5 c3 d5 e5 Nc6 Nf3"),
  alts=[('fr-c5-cxd4', 'Black trades, then the center pawn', J("e4 e6 d4 c5 c3 cxd4 cxd4 d5 e5")),
        ('fr-c5-nc6', 'Black trades, knight out', J("e4 e6 d4 c5 c3 cxd4 cxd4 Nc6 Nf3"))],
  why='This transposes to your Sicilian or French lines.', outcome='Back in familiar structures')

# ============================================================== Rare first moves
L('rr-owen', 'rare-all', 'Bishop to the long diagonal', 'Guard your e-pawn with the bishop first', 'common',
  J("e4 b6 d4 Bb7 Bd3 e6 Nf3 Nf6 Qe2"),
  alts=[('rr-owen-c5', 'The c-pawn', J("e4 b6 d4 Bb7 Bd3 e6 Nf3 c5 c3")),
        ('rr-owen-bb4', 'Bishop check', J("e4 b6 d4 Bb7 Bd3 e6 Nf3 Bb4+ c3")),
        ('rr-owen-g6', 'Double fianchetto', J("e4 b6 d4 Bb7 Bd3 g6 Nf3 Bg7 O-O")),
        ('rr-owen-nf6', 'Knight hits your e-pawn', J("e4 b6 d4 Bb7 Bd3 Nf6 Qe2"))],
  why='You lost your e-pawn and the game in 6 moves against this in October.', outcome='A big center, safely guarded', tags=['game'])
L('rr-nimzo', 'rare-all', 'Knight first', 'Knight out too; often you are back in the Italian', 'common',
  J("e4 Nc6 Nf3 e5 Bc4"),
  alts=[('rr-nimzo-d5', 'Pawn strike', J("e4 Nc6 Nf3 d5 exd5 Qxd5 Nc3 Qd8 d4")),
        ('rr-nimzo-qe6', 'Pawn strike, queen check', J("e4 Nc6 Nf3 d5 exd5 Qxd5 Nc3 Qe6+ Be2")),
        ('rr-nimzo-nf6', 'Knight hits your e-pawn', J("e4 Nc6 Nf3 Nf6 e5 Nd5 d4 d6 c4 Nb6 exd6")),
        ('rr-nimzo-d6', 'Quiet pawn', J("e4 Nc6 Nf3 d6 d4 Nf6 Nc3"))],
  why='Black\'s knight move often transposes to the openings you know.', outcome='Familiar positions')
L('rr-alekhine', 'rare-all', 'Knight hits your e-pawn', 'Chase it with the pawn, then build', 'rare',
  J("e4 Nf6 e5 Nd5 d4 d6 Nf3 Bg4 Be2 Bxf3 Bxf3"),
  alts=[('rr-alekhine-nc6', 'Knight out', J("e4 Nf6 e5 Nd5 d4 d6 Nf3 Bg4 Be2 Nc6 c4")),
        ('rr-alekhine-dx', 'Black takes after the pin', J("e4 Nf6 e5 Nd5 d4 d6 Nf3 Bg4 Be2 dxe5 Nxe5")),
        ('rr-alekhine-dxe5', 'Black takes at once', J("e4 Nf6 e5 Nd5 d4 d6 Nf3 dxe5 Nxe5")),
        ('rr-alekhine-e6', 'Pawn to the side', J("e4 Nf6 e5 Nd5 d4 e6 c4 Nb6 Nf3"))],
  why='Black invites your pawns forward. Take the space.', outcome='Space for you')
L('rr-stgeorge', 'rare-all', 'The a-pawn and b-pawn', 'Take the center, then hit the pawns', 'rare',
  J("e4 a6 d4 b5 Nf3 Bb7 Bd3 e6 O-O"),
  why='Black spends early moves on the edge. Take the middle.', outcome='A big center and a lead in development')

CHAPTERS = [
  dict(id='italian', name='The Italian', move='e-pawn mirrors yours, then the knight', parts=['setup', 'bishop', 'knight', 'odd']),
  dict(id='e5x', name='Philidor & Petrov', move='e-pawn mirrors yours, no knight', parts=['e5x-phil', 'e5x-pet', 'e5x-misc']),
  dict(id='caro', name='Caro-Kann', move='c-pawn one square', parts=['caro-main', 'caro-other4', 'caro-third']),
  dict(id='sic', name='Sicilian', move='c-pawn two squares', parts=['sic-knight', 'sic-pawn', 'sic-rare']),
  dict(id='scandi', name='Scandinavian', move='d-pawn hits your e-pawn', parts=['scandi-queen', 'scandi-other']),
  dict(id='pirc', name='Pirc & Modern', move='d-pawn one square, or the fianchetto', parts=['pirc-150', 'pirc-other']),
  dict(id='french', name='French', move='e-pawn one square', parts=['french-adv', 'french-other']),
  dict(id='rare', name='Rare first moves', move='knights, b-pawn, a-pawn', parts=['rare-all']),
]

for _p in PARTS:
    _p.setdefault('ch', 'italian')
NEW_PARTS = {p['id'] for p in PARTS if p['ch'] != 'italian'}
import content2_notes  # noqa
