"""Black repertoire: lessons (lines) and the DSL. Same format as content.py, but "you" are Black.
SAN is internal only. Notes are plain English; f7 and f2 are the only squares ever named."""
NOTES = {}
def n(path, label=None, text=None, tags=None, arrows=None, circles=None):
    path = ' '.join(path.split())
    if isinstance(text, list):
        tags, text = text, None
    assert path not in NOTES, f"duplicate note: {path}"
    NOTES[path] = dict(label=label, text=text, tags=tags or [], arrows=arrows or [], circles=circles or [])

def J(*parts):
    return ' '.join(' '.join(parts).split())

LESSONS = []
def L(id, part, title, sub, pri, path, alts=None, why=None, start=None, tags=None, outcome=None):
    LESSONS.append(dict(id=id, part=part, title=title, sub=sub, pri=pri, path=J(path), alts=[(a, t, J(p)) for a, t, p in (alts or [])],
                        why=why, start=start, tags=tags or [], outcome=outcome))

PARTS = []
def P(id, ch, title, kicker, blurb):
    PARTS.append(dict(id=id, ch=ch, title=title, kicker=kicker, blurb=blurb))

# ============================================================== THE ITALIAN (3.Bc4 Bc5)
E = "e4 e5"
KN = "e4 e5 Nf3 Nc6"
IT = J(KN, "Bc4 Bc5")
GP = J(IT, "c3 Nf6 d4 exd4 cxd4 Bb4+")

P('bi-center', 'italian', 'White builds the big center', 'Giuoco Piano',
  'White prepares the d-pawn push with the small c-pawn move. Take, check, trade bishops, then hit back in the center with your own d-pawn.')
P('bi-slow', 'italian', 'The slow Italian', 'Quiet setups',
  'White keeps the center closed and develops. You use one setup against all of it, and you watch out for the early knight jump at f7.')
P('bi-gambits', 'italian', 'Gambits and cheap shots', 'Sidelines',
  'Early pawn sacrifices and lunges at f7. Each one has a calm answer that leaves you better.')

L('bi-main', 'bi-center', 'Check, trade, then strike', 'Bishop check, swap bishops, then your d-pawn hits back', 'core',
  J(GP, "Bd2 Bxd2+ Nbxd2 d5 exd5 Nxd5 O-O O-O"),
  alts=[('bi-main-qb3', 'Queen hits the knight', J(GP, "Bd2 Bxd2+ Nbxd2 d5 exd5 Nxd5 Qb3 Nce7 O-O O-O")),
        ('bi-main-qe2', 'Queen check', J(GP, "Bd2 Bxd2+ Nbxd2 d5 exd5 Nxd5 Qe2+ Be6 O-O O-O")),
        ('bi-main-bxd5', 'Bishop takes the knight', J(GP, "Bd2 Bxd2+ Nbxd2 d5 exd5 Nxd5 Bxd5 Qxd5 O-O Be6")),
        ('bi-main-e5', 'Pawn hits your knight: take the bishop', J(GP, "Bd2 Bxd2+ Nbxd2 d5 e5 dxc4 exf6 Qxf6"))],
  why='The main line of the Giuoco Piano, and the one White players at your level aim for.', outcome='Equal, with easy development')
L('bi-qxd2', 'bi-center', 'Queen takes back: grab the e-pawn', 'The queen left the e-pawn alone; take it, then guard the knight', 'core',
  J(GP, "Bd2 Bxd2+ Qxd2 Nxe4 Qe3 d5"),
  alts=[('bi-qxd2-qf4', 'Queen to the side', J(GP, "Bd2 Bxd2+ Qxd2 Nxe4 Qf4 d5")),
        ('bi-qxd2-qe2', 'Queen to the e-file', J(GP, "Bd2 Bxd2+ Qxd2 Nxe4 Qe2 d5"))],
  why='Almost four in ten club players take back with the queen here. It drops a pawn.', outcome='You are a pawn up')
L('bi-nc3', 'bi-center', 'Knight blocks the check', 'Take the e-pawn, trade, then strike with the d-pawn', 'core',
  J(GP, "Nc3 Nxe4 O-O Bxc3 bxc3 d5 Bb3 O-O"),
  alts=[('bi-nc3-bd3', 'Bishop retreats to the middle', J(GP, "Nc3 Nxe4 O-O Bxc3 bxc3 d5 Bd3 O-O")),
        ('bi-nc3-bb5', 'Bishop pins your knight', J(GP, "Nc3 Nxe4 O-O Bxc3 bxc3 d5 Bb5 O-O")),
        ('bi-nc3-ba3', 'Bishop stops you castling: take the other bishop', J(GP, "Nc3 Nxe4 O-O Bxc3 bxc3 d5 Ba3 dxc4")),
        ('bi-nc3-qe2', 'Queen pins your knight', J(GP, "Nc3 Nxe4 Qe2 d5")),
        ('bi-nc3-bd2', 'Bishop blocks too', J(GP, "Nc3 Nxe4 Bd2 Nxd2 Qxd2 O-O"))],
  why='More than half of club players block the check with the knight. That leaves their e-pawn loose.', outcome='You keep an extra pawn')
L('bi-e5', 'bi-center', 'Pawn hits your knight', 'Strike back with the d-pawn', 'common',
  J(IT, "c3 Nf6 d4 exd4 e5 d5 Bb5 Ne4 cxd4 Bb6"),
  alts=[('bi-e5-exf6', 'Pawn takes the knight', J(IT, "c3 Nf6 d4 exd4 e5 d5 exf6 dxc4 fxg7 Rg8")),
        ('bi-e5-bxc6', 'Bishop takes your knight', J(IT, "c3 Nf6 d4 exd4 e5 d5 Bb5 Ne4 Bxc6+ bxc6")),
        ('bi-e5-bb3', 'Bishop steps back', J(IT, "c3 Nf6 d4 exd4 e5 d5 Bb3 Ne4 cxd4 Bb4+"))],
  why='White pushes past instead of taking back. The answer is the same idea: your d-pawn hits back.', outcome='Equal, and your pieces are active')

L('bi-slow', 'bi-slow', 'One setup for the slow Italian', 'Small d-pawn move, a-pawn, bishop back, castle', 'core',
  J(IT, "c3 Nf6 d3 d6 O-O a6 Re1 Ba7 h3 O-O"),
  alts=[('bi-slow-bg5', 'Bishop pins your knight', J(IT, "c3 Nf6 d3 d6 Bg5 h6 Bh4 a6")),
        ('bi-slow-b4', 'Pawn hits your bishop', J(IT, "c3 Nf6 d3 d6 b4 Bb6 a4 a5")),
        ('bi-slow-h3', 'Small pawn first', J(IT, "c3 Nf6 d3 d6 h3 a6 O-O Ba7"))],
  why='The quiet d-pawn move is White\'s most common fourth move at your level.', outcome='Equal; you have a plan and White often doesn\'t')
L('bi-ng5', 'bi-slow', 'Knight jumps at f7: castle', 'Castle, then kick it with the h-pawn; the sacrifice on f7 hands you two pieces for a rook', 'core',
  J(IT, "d3 Nf6 Ng5 O-O O-O h6 Nf3 d6"),
  alts=[('bi-ng5-nxf7', 'Knight takes on f7', J(IT, "d3 Nf6 Ng5 O-O Nxf7 Rxf7 Bxf7+ Kxf7")),
        ('bi-ng5-bxf7', 'Bishop takes on f7', J(IT, "d3 Nf6 Ng5 O-O Bxf7+ Rxf7 Nxf7 Kxf7")),
        ('bi-ng5-late', 'Knight takes after the kick', J(IT, "d3 Nf6 Ng5 O-O O-O h6 Nxf7 Rxf7 Bxf7+ Kxf7")),
        ('bi-ng5-qf3', 'Queen joins the attack', J(IT, "d3 Nf6 Ng5 O-O Qf3 h6")),
        ('bi-ng5-h4', 'Edge pawn backs up the knight', J(IT, "d3 Nf6 Ng5 O-O h4 h6")),
        ('bi-ng5-nc3', 'Knight out first', J(IT, "d3 Nf6 Ng5 O-O Nc3 h6 Nf3 d6")),
        ('bi-ng5-c3', 'After the small c-pawn move', J(IT, "c3 Nf6 Ng5 O-O d3 h6 Nf3 d5"))],
  why='At your level more than a third of White players jump the knight forward as soon as the d-pawn moves.', outcome='You are better: White has moved one piece twice')
L('bi-bg5', 'bi-slow', 'Bishop pins your knight', 'Ask the bishop at once with the h-pawn', 'common',
  J(IT, "d3 Nf6 Bg5 h6 Bh4 d6"),
  alts=[('bi-bg5-bxf6', 'Bishop takes your knight', J(IT, "d3 Nf6 Bg5 h6 Bxf6 Qxf6 O-O d6")),
        ('bi-bg5-nc3', 'Knight first, then the pin', J(IT, "d3 Nf6 Nc3 d6 Bg5 h6 Bxf6 Qxf6 Nd5 Qd8 O-O a6"))],
  why='The pin is the second most common idea White tries in the slow Italian.', outcome='Equal; you keep two bishops')
L('bi-4n', 'bi-slow', 'Knight out first', 'Same setup; the knight jump to the edge kills White\'s bishop', 'common',
  J(IT, "Nc3 Nf6 d3 d6 h3 a6 O-O Na5"),
  alts=[('bi-4n-bg5', 'Bishop pins your knight', J(IT, "Nc3 Nf6 d3 d6 Bg5 h6 Bxf6 Qxf6 Nd5 Qd8")),
        ('bi-4n-ng5', 'Knight jumps at f7', J(IT, "Nc3 Nf6 d3 d6 Ng5 O-O Nd5 Na5")),
        ('bi-4n-oo', 'White castles', J(IT, "Nc3 Nf6 O-O d6 d3 Na5 Bb3 Nxb3")),
        ('bi-4n-early', 'Knight jumps before the d-pawn moves', J(IT, "Nc3 Nf6 Ng5 O-O O-O h6 Nf3 d6")),
        ('bi-4n-nxe5', 'Knight grabs your pawn: the fork fails', J(IT, "Nc3 Nf6 Nxe5 Nxe5 d4 Nxc4 dxc5 d5"))],
  why='The four-knights version of the slow Italian. You lost two games in it, in July and in October.', outcome='Equal; you get rid of White\'s best bishop', tags=['game'])
L('bi-oo', 'bi-slow', 'White castles at once', 'Same setup; take with the bishop if the d-pawn rushes', 'common',
  J(IT, "O-O Nf6 d3 d6 c3 a6 Re1 Ba7"),
  alts=[('bi-oo-bg5', 'Bishop pins your knight', J(IT, "O-O Nf6 d3 d6 Bg5 h6 Bh4 g5")),
        ('bi-oo-h3', 'Small pawn first', J(IT, "O-O Nf6 d3 d6 h3 h6 c3 a6")),
        ('bi-oo-nc3', 'Knight out', J(IT, "O-O Nf6 Nc3 d6 d3 Na5 Bb3 Nxb3")),
        ('bi-oo-re1', 'Rook to the center file', J(IT, "O-O Nf6 Re1 d6 c3 O-O")),
        ('bi-oo-c3d4', 'Small pawn, then the push', J(IT, "O-O Nf6 c3 d6 d4 Bb6")),
        ('bi-oo-ng5', 'Knight jumps at f7', J(IT, "O-O Nf6 Ng5 O-O d3 h6 Nf3 d6")),
        ('bi-oo-d4', 'Center push after castling', J(IT, "O-O Nf6 d4 Bxd4 Nxd4 Nxd4 c3 Nc6"))],
  why='Castling first is White\'s second most common fourth move at your level.', outcome='Equal')

L('bi-evans', 'bi-gambits', 'The b-pawn gambit', 'Take the pawn, tuck the bishop back, then hit the Italian bishop', 'common',
  J(IT, "b4 Bxb4 c3 Be7 d4 Na5 Bd3 d6"),
  alts=[('bi-evans-be2', 'Bishop steps back', J(IT, "b4 Bxb4 c3 Be7 d4 Na5 Be2 d6")),
        ('bi-evans-qb3', 'Queen hits f7', J(IT, "b4 Bxb4 c3 Be7 Qb3 Nh6")),
        ('bi-evans-oo', 'White castles', J(IT, "b4 Bxb4 c3 Be7 O-O Nf6"))],
  why='The Evans Gambit is a fast-attack weapon. You took the pawn against CaptEvans88 and won; this is the safe way to keep it.', outcome='You are a pawn up', tags=['game'])
L('bi-d4', 'bi-gambits', 'Early center push', 'Bishop takes, then the knight, then develop', 'common',
  J(IT, "d4 Bxd4 Nxd4 Nxd4 c3 Nc6 O-O Nf6"),
  alts=[('bi-d4-oo', 'White castles', J(IT, "d4 Bxd4 Nxd4 Nxd4 O-O d6")),
        ('bi-d4-qh5', 'Queen lunges', J(IT, "d4 Bxd4 Nxd4 Nxd4 Qh5 Qe7")),
        ('bi-d4-bxf7', 'Bishop takes on f7', J(IT, "d4 Bxd4 Nxd4 Nxd4 Bxf7+ Kxf7 Qh5+ Kf8")),
        ('bi-d4-c3', 'Pawn hits your bishop', J(IT, "d4 Bxd4 c3 Bb6")),
        ('bi-d4-ng5', 'Knight jumps at f7', J(IT, "d4 Bxd4 Ng5 Nh6"))],
  why='White gives a pawn to open lines. You take it with pieces and keep it.', outcome='You are a pawn up')
L('bi-cheap', 'bi-gambits', 'Cheap shots at f7', 'Count the attackers: your queen wins the knight', 'common',
  J(IT, "Ng5 Qxg5 O-O Qg6"),
  alts=[('bi-cheap-d4', 'Pawn attacks your bishop', J(IT, "Ng5 Qxg5 d4 Qxg2 Rf1 Qxe4+")),
        ('bi-cheap-d3', 'Pawn opens the bishop', J(IT, "Ng5 Qxg5 d3 Qxg2")),
        ('bi-cheap-qf3', 'Queen hits f7', J(IT, "Ng5 Qxg5 Qf3 Nf6")),
        ('bi-bxf7', 'Bishop takes on f7', J(IT, "Bxf7+ Kxf7 Nxe5+ Nxe5 Qh5+ Ng6")),
        ('bi-bxf7-ng5', 'Bishop sacrifice, then the knight check', J(IT, "Bxf7+ Kxf7 Ng5+ Qxg5"))],
  why='At your level these come up a few times in every hundred games. Each one loses material for White.', outcome='You are a piece up')

# ============================================================== RUY LOPEZ (3.Bb5 Nf6)
RL = J(KN, "Bb5 Nf6")
P('br-castle', 'ruy', 'White castles', 'Berlin',
  'White leaves the e-pawn hanging to castle fast. Take it, then step the knight back and trade.')
P('br-quiet', 'ruy', 'Quiet fourth moves', 'Slow Spanish',
  'White guards the e-pawn and develops. Your bishop goes to the same diagonal as in the Italian.')
P('br-swap', 'ruy', 'Bishop takes your knight', 'Exchange',
  'White trades the bishop for your knight. Take back toward the center, then win your pawn back.')

L('br-oo', 'br-castle', 'Take the e-pawn, then step back', 'Knight takes, retreats, and trades', 'core',
  J(RL, "O-O Nxe4 Re1 Nd6 Bxc6 dxc6 Nxe5 Be7"),
  alts=[('br-oo-nxe5', 'Knight takes first', J(RL, "O-O Nxe4 Re1 Nd6 Nxe5 Be7 Nxc6 dxc6")),
        ('br-oo-rxe5', 'Rook takes with check', J(RL, "O-O Nxe4 Re1 Nd6 Bxc6 dxc6 Rxe5+ Be7")),
        ('br-oo-bxc6', 'Bishop takes at once', J(RL, "O-O Nxe4 Bxc6 dxc6 Nxe5 Nd6")),
        ('br-oo-bxc6d3', 'Bishop takes, then the pawn hits your knight', J(RL, "O-O Nxe4 Bxc6 dxc6 d3 Nd6 Nxe5 Be7")),
        ('br-oo-d3', 'Pawn hits your knight', J(RL, "O-O Nxe4 d3 Nd6 Bxc6 dxc6 Nxe5 Be7")),
        ('br-oo-d4', 'Center push: the queen trade', J(RL, "O-O Nxe4 d4 Nd6 Bxc6 dxc6 dxe5 Nf5 Qxd8+ Kxd8")),
        ('br-oo-dxe5', 'Center push, then pawn takes: grab the bishop', J(RL, "O-O Nxe4 d4 Nd6 dxe5 Nxb5")),
        ('br-oo-qe2', 'Queen pins your knight, then the knight grabs', J(RL, "O-O Nxe4 Qe2 Nd6 Nxe5 Nd4")),
        ('br-oo-qe2b', 'Queen pins, bishop takes', J(RL, "O-O Nxe4 Qe2 Nd6 Bxc6 dxc6 Qxe5+ Qe7"))],
  why='The Berlin is your move against the Spanish. About a quarter of White players castle here and leave the e-pawn hanging.', outcome='Equal; you have the bishop pair')
L('br-d3', 'br-quiet', 'Pawn guards the e-pawn', 'Bishop out to the same diagonal as in the Italian', 'core',
  J(RL, "d3 Bc5 O-O d6 h3 O-O"),
  alts=[('br-d3-trap', 'Bishop takes, knight grabs: the queen fork', J(RL, "d3 Bc5 Bxc6 dxc6 Nxe5 Qd4")),
        ('br-d3-bxc6', 'Bishop takes your knight', J(RL, "d3 Bc5 Bxc6 dxc6 O-O Nd7")),
        ('br-d3-bg5', 'Bishop pins your knight', J(RL, "d3 Bc5 Bg5 h6 Bh4 O-O")),
        ('br-d3-oobg5', 'Castle, then the pin', J(RL, "d3 Bc5 O-O d6 Bg5 h6")),
        ('br-d3-oobxc6', 'Castle, then bishop takes with check', J(RL, "d3 Bc5 O-O d6 Bxc6+ bxc6")),
        ('br-d3-oonc3', 'Castle, then the knight', J(RL, "d3 Bc5 O-O d6 Nc3 h6")),
        ('br-d3-c3', 'Small c-pawn move', J(RL, "d3 Bc5 c3 O-O O-O d6"))],
  why='You played the bishop out against this in both of your games and won both.', outcome='Equal', tags=['game'])
L('br-nc3', 'br-quiet', 'Knight out: copy the pin', 'Your bishop pins back; castle and keep it simple', 'common',
  J(RL, "Nc3 Bb4 O-O O-O d3 d6"),
  alts=[('br-nc3-d3', 'Pawn guards first', J(RL, "Nc3 Bb4 d3 d6 Bd2 O-O")),
        ('br-nc3-d3bg5', 'Pawn guards, then the pin', J(RL, "Nc3 Bb4 d3 d6 Bg5 h6")),
        ('br-nc3-bxc6', 'Bishop takes your knight', J(RL, "Nc3 Bb4 Bxc6 dxc6 d3 Nd7")),
        ('br-nc3-bxc6e5', 'Bishop takes, knight grabs the pawn', J(RL, "Nc3 Bb4 Bxc6 dxc6 Nxe5 Qe7")),
        ('br-nc3-a3', 'Pawn hits your bishop', J(RL, "Nc3 Bb4 a3 Bxc3 dxc3 d6")),
        ('br-nc3-a3b', 'Pawn hits your bishop, b-pawn takes back', J(RL, "Nc3 Bb4 a3 Bxc3 bxc3 O-O")),
        ('br-nc3-ooa3', 'Castle, then the pawn hits your bishop', J(RL, "Nc3 Bb4 O-O O-O a3 Bxc3 dxc3 Nxe4")),
        ('br-nc3-nd5', 'Knight jumps to the center', J(RL, "Nc3 Bb4 Nd5 Nxd5 exd5 e4"))],
  why='The Four Knights version of the Spanish. Symmetry is fine for you.', outcome='Equal')
L('br-bxc6', 'br-swap', 'Take back with the d-pawn', 'Open lines for your queen and bishop, then win the pawn back', 'core',
  J(RL, "Bxc6 dxc6 Nxe5 Qd4 Nf3 Qxe4+ Qe2 Qxe2+ Kxe2 Bd6"),
  alts=[('br-bxc6-nd3', 'Knight steps back to guard', J(RL, "Bxc6 dxc6 Nxe5 Qd4 Nd3 Qxe4+")),
        ('br-bxc6-d3', 'Pawn guards the e-pawn', J(RL, "Bxc6 dxc6 d3 Bd6 O-O Qe7")),
        ('br-bxc6-d3bg5', 'Pawn guards, then the pin', J(RL, "Bxc6 dxc6 d3 Bd6 Bg5 h6")),
        ('br-bxc6-nc3', 'Knight guards the e-pawn', J(RL, "Bxc6 dxc6 Nc3 Bd6 O-O Bg4")),
        ('br-bxc6-oo', 'White castles', J(RL, "Bxc6 dxc6 O-O Bd6 Re1 Be6"))],
  why='The bishop trade is the most common reply at your level. Against vasylsaienko in July you took back with the b-pawn and lost your bishop four moves later. The d-pawn recapture brings your queen and bishop out at once.', outcome='Equal; your bishops get open lines', tags=['game', 'swap'])

# ============================================================== SCOTCH & CENTER GAMBITS
SC = J(KN, "d4 exd4")
SN = J(SC, "Nxd4 Nf6")
P('bs-scotch', 'scotch', 'Knight takes back', 'Scotch',
  'White trades in the center and takes back with the knight. Your knight hits the e-pawn at once.')
P('bs-gambits', 'scotch', 'White gives a pawn', 'Scotch gambits',
  'White leaves your extra pawn alone to develop fast. Develop with tempo and hit back in the center.')
P('bs-center', 'scotch', 'The d-pawn on move two', 'Center Game & Danish',
  'White pushes the d-pawn before the knight comes out. Take, then either kick the queen or decline the gambit with your own d-pawn.')

L('bs-mieses', 'bs-scotch', 'Pawn hits your knight: move it first', 'Queen to the e-file, knight to the center, never the d-pawn first', 'core',
  J(SN, "Nxc6 bxc6 e5 Qe7 Qe2 Nd5 c4 Nb6 Nc3 Qe6"),
  alts=[('bs-mieses-bf4', 'Bishop guards the pawn', J(SN, "Nxc6 bxc6 e5 Qe7 Bf4 d6")),
        ('bs-mieses-be2', 'Bishop out: take the pawn', J(SN, "Nxc6 bxc6 e5 Qe7 Be2 Qxe5")),
        ('bs-mieses-f4', 'The f-pawn guards', J(SN, "Nxc6 bxc6 e5 Qe7 f4 d6")),
        ('bs-mieses-nc3', 'Knight hits your knight', J(SN, "Nxc6 bxc6 e5 Qe7 Qe2 Nd5 Nc3 Nxc3"))],
  why='Against ZhoskaStreezh in July you pushed the d-pawn first and the e-pawn took your knight. Knight first, every time.', outcome='Equal', tags=['game', 'swap'])
L('bs-quiet', 'bs-scotch', 'Knight trade without the pawn push', 'Strike the center with your d-pawn', 'core',
  J(SN, "Nxc6 bxc6 Nc3 Bb4 Bd3 d5"),
  alts=[('bs-quiet-bd3', 'Bishop guards the e-pawn', J(SN, "Nxc6 bxc6 Bd3 d5 exd5 cxd5")),
        ('bs-quiet-bg5', 'Bishop pins your knight', J(SN, "Nxc6 bxc6 Bg5 h6")),
        ('bs-quiet-f3', 'Pawn guards the e-pawn', J(SN, "Nxc6 bxc6 f3 d5"))],
  why='After the knight trade most White players keep the e-pawn home. Against quzibek in July your queen came out first; the d-pawn strike is simpler.', outcome='Equal; you own the center', tags=['game'])
L('bs-4n', 'bs-scotch', 'Knight out: pin it', 'Bishop pins, then the d-pawn strikes', 'core',
  J(SN, "Nc3 Bb4 Nxc6 bxc6 Bd3 d5 exd5 cxd5 O-O O-O"),
  alts=[('bs-4n-bd2', 'Bishop breaks the pin', J(SN, "Nc3 Bb4 Nxc6 bxc6 Bd2 O-O")),
        ('bs-4n-e5', 'Pawn hits your knight', J(SN, "Nc3 Bb4 Nxc6 bxc6 e5 Qe7")),
        ('bs-4n-bg5', 'Bishop pins back', J(SN, "Nc3 Bb4 Bg5 h6"))],
  why='A third of White players develop the knight instead of trading.', outcome='Equal')
L('bs-tricks', 'bs-scotch', 'Fifth-move slips', 'Two of them simply lose a piece', 'rare',
  J(SN, "Bd3 Nxd4"),
  alts=[('bs-tricks-bc4', 'Bishop to the Italian diagonal', J(SN, "Bc4 Nxe4")),
        ('bs-tricks-bg5', 'Bishop pins at once', J(SN, "Bg5 h6"))],
  why='Rare, but worth knowing: one natural bishop move hangs the knight.', outcome='You win material')

L('bs-gambit', 'bs-gambits', 'Bishop out instead of taking', 'Bishop out, knight out, then the check and the d-pawn', 'core',
  J(SC, "Bc4 Bc5 c3 Nf6 cxd4 Bb4+ Bd2 Bxd2+ Nbxd2 d5"),
  alts=[('bs-gambit-e5', 'Pawn hits your knight', J(SC, "Bc4 Bc5 c3 Nf6 e5 d5 Bb5 Ne4 cxd4 Bb6")),
        ('bs-gambit-oo', 'White castles', J(SC, "Bc4 Bc5 O-O d6 c3 Bg4")),
        ('bs-gambit-ng5', 'Knight jumps at f7', J(SC, "Bc4 Bc5 Ng5 Nh6 O-O d6")),
        ('bs-gambit-nxf7', 'Knight takes on f7', J(SC, "Bc4 Bc5 Ng5 Nh6 Nxf7 Nxf7 Bxf7+ Kxf7 Qh5+ g6 Qxc5 d5")),
        ('bs-gambit-qf3', 'Queen joins the knight', J(SC, "Bc4 Bc5 Ng5 Nh6 Qf3 O-O")),
        ('bs-gambit-qh5', 'Queen to the edge', J(SC, "Bc4 Bc5 Ng5 Nh6 Qh5 Qe7")),
        ('bs-gambit-ong5', 'Castle, then the knight jump', J(SC, "Bc4 Bc5 O-O d6 Ng5 Ne5")),
        ('bs-gambit-nc3', 'Check, then the knight blocks', J(SC, "Bc4 Bc5 c3 Nf6 cxd4 Bb4+ Nc3 Nxe4 O-O Bxc3 bxc3 d5")),
        ('bs-gambit-exf6', 'Pawn hits your knight, then takes it', J(SC, "Bc4 Bc5 c3 Nf6 e5 d5 exf6 dxc4 fxg7 Rg8"))],
  why='Against themobun (2050) in July you took the second pawn, and the bishop sacrifice on f7 won your bishop back with a queen check. Developing the knight keeps it simple.', outcome='Equal', tags=['game'])
L('bs-goring', 'bs-gambits', 'The small c-pawn gambit', 'Hit back with your d-pawn and swap off White\'s knight', 'common',
  J(SC, "c3 d5 exd5 Qxd5 cxd4 Bg4 Be2 Bb4+ Nc3 Bxf3 Bxf3 Qc4"),
  alts=[('bs-goring-nc3', 'Knight hits your queen', J(SC, "c3 d5 exd5 Qxd5 cxd4 Bg4 Nc3 Bxf3 gxf3 Qxd4")),
        ('bs-goring-e5', 'Pawn pushes past', J(SC, "c3 d5 e5 dxc3 Nxc3 Bc5")),
        ('bs-goring-nxd4', 'Knight takes back', J(SC, "c3 d5 exd5 Qxd5 Nxd4 Nf6")),
        ('bs-goring-c4', 'Pawn hits your queen', J(SC, "c3 d5 exd5 Qxd5 c4 Qe4+")),
        ('bs-goring-cxd4', 'Pawn takes in the center', J(SC, "c3 d5 cxd4 dxe4"))],
  why='A gambit that works best when you take everything. Strike back instead.', outcome='Equal; White\'s center pawn is isolated')
L('bs-center', 'bs-center', 'Queen takes back: kick it', 'Knight hits the queen, then pin the knight and castle', 'core',
  J(E, "d4 exd4 Qxd4 Nc6 Qe3 Nf6 Nc3 Bb4 Bd2 O-O O-O-O Re8"),
  alts=[('bs-center-e5', 'Pawn hits your knight', J(E, "d4 exd4 Qxd4 Nc6 Qe3 Nf6 e5 Ng4")),
        ('bs-center-qd1', 'Queen goes home', J(E, "d4 exd4 Qxd4 Nc6 Qd1 Nf6")),
        ('bs-center-qa4', 'Queen to the side', J(E, "d4 exd4 Qxd4 Nc6 Qa4 Nf6")),
        ('bs-center-qd3', 'Queen to the middle', J(E, "d4 exd4 Qxd4 Nc6 Qd3 Nf6")),
        ('bs-center-qc3', 'Queen in front of the c-pawn: pin it', J(E, "d4 exd4 Qxd4 Nc6 Qc3 Bb4")),
        ('bs-center-a3', 'Pawn hits your bishop: take, then the e-pawn', J(E, "d4 exd4 Qxd4 Nc6 Qe3 Nf6 Nc3 Bb4 Bd2 O-O a3 Bxc3 Bxc3 Nxe4")),
        ('bs-center-a3q', 'Pawn hits your bishop at once', J(E, "d4 exd4 Qxd4 Nc6 Qe3 Nf6 Nc3 Bb4 a3 Bxc3+ Qxc3 O-O")),
        ('bs-center-bb5', 'Bishop pins your knight', J(E, "d4 exd4 Qxd4 Nc6 Qe3 Nf6 Bb5 Be7"))],
  why='At your level more than half of White players who push the d-pawn take back with the queen.', outcome='You are ahead in development')
L('bs-danish', 'bs-center', 'The Danish: hit back with the d-pawn', 'Don\'t take the second pawn; strike the center instead', 'core',
  J(E, "d4 exd4 c3 d5 exd5 Qxd5 cxd4 Nc6 Nf3 Bg4 Be2 Bb4+"),
  alts=[('bs-danish-qxd4', 'Queen takes back', J(E, "d4 exd4 c3 d5 exd5 Qxd5 Qxd4 Qxd4 cxd4 Nc6")),
        ('bs-danish-nf3', 'Knight out first', J(E, "d4 exd4 c3 d5 exd5 Qxd5 Nf3 Nc6")),
        ('bs-danish-nc3', 'Knight hits your queen: take the pawn', J(E, "d4 exd4 c3 d5 exd5 Qxd5 cxd4 Nc6 Nc3 Qxd4")),
        ('bs-danish-e5', 'Pawn pushes past', J(E, "d4 exd4 c3 d5 e5 dxc3 Nxc3 d4")),
        ('bs-danish-cxd4', 'Pawn takes back', J(E, "d4 exd4 c3 d5 cxd4 dxe4")),
        ('bs-danish-be3', 'Bishop guards the pawn', J(E, "d4 exd4 c3 d5 exd5 Qxd5 cxd4 Nc6 Be3 Bb4+"))],
  why='Against yonatha32 in October you took the second pawn, White developed fast, and you lost on time. The d-pawn strike turns the gambit off.', outcome='Equal; White\'s center pawn is isolated', tags=['game', 'swap'])
L('bs-d4other', 'bs-center', 'Other third moves', 'Knight back to the Scotch, or hit the bishop line', 'common',
  J(E, "d4 exd4 Nf3 Nc6 Nxd4 Nf6"),
  alts=[('bs-d4other-bc4', 'Bishop out', J(E, "d4 exd4 Bc4 Nf6 e5 d5")),
        ('bs-d4other-bc4n', 'Bishop out, then the knight', J(E, "d4 exd4 Bc4 Nf6 Nf3 Nxe4")),
        ('bs-d4other-nf3bc4', 'Knight out, then the bishop', J(E, "d4 exd4 Nf3 Nc6 Bc4 Bc5 c3 Nf6"))],
  why='Move orders that land back in positions you know.', outcome='Equal')

# ============================================================== FOUR KNIGHTS, VIENNA & QUIET LINES
FK = J(KN, "Nc3 Nf6")
VI = "e4 e5 Nc3 Nc6"
P('bv-4n', 'vienna', 'Four Knights', 'Both queen\'s knights out',
  'White brings the other knight out on move three. Copy the pin, take the center, or slide into the Italian setup you already know.')
P('bv-vienna', 'vienna', 'Knight out on move two', 'Vienna',
  'White develops the queen\'s knight first, often to push the f-pawn. Meet the bishop with the knight jump and the gambit with a pawn of your own.')
P('bv-quiet', 'vienna', 'Quiet third moves', 'Sidelines',
  'Slow moves like the small d-pawn or c-pawn. Hit the center with your d-pawn as soon as it is safe.')

L('bv-spanish', 'bv-4n', 'Bishop pins your knight: copy it', 'Pin back, castle, and keep the symmetry', 'core',
  J(FK, "Bb5 Bb4 O-O O-O d3 d6"),
  alts=[('bv-spanish-bxc6', 'Bishop takes your knight', J(FK, "Bb5 Bb4 Bxc6 dxc6 Nxe5 Qe7")),
        ('bv-spanish-d3', 'Pawn guards first', J(FK, "Bb5 Bb4 d3 d6 O-O O-O")),
        ('bv-spanish-a3', 'Pawn hits your bishop', J(FK, "Bb5 Bb4 a3 Bxc3 dxc3 d6")),
        ('bv-spanish-nd5', 'Knight jumps to the center', J(FK, "Bb5 Bb4 Nd5 Nxd5 exd5 e4"))],
  why='The Spanish Four Knights. The copy-cat answer is as safe as it gets.', outcome='Equal')
L('bv-scotch4n', 'bv-4n', 'Center push: pin, then strike', 'Take, pin the knight, then push your d-pawn', 'core',
  J(FK, "d4 exd4 Nxd4 Bb4 Nxc6 bxc6 Bd3 d5 exd5 cxd5 O-O O-O"),
  alts=[('bv-scotch4n-bg5', 'Bishop pins back', J(FK, "d4 exd4 Nxd4 Bb4 Bg5 h6")),
        ('bv-scotch4n-nd5', 'Knight jumps into the center', J(FK, "d4 exd4 Nd5 Be7"))],
  why='Two of your games went exactly this way: a win against Jaydenh625 in July, and an equal opening against Eschoir in October.', outcome='Equal', tags=['game'])
L('bv-italian4n', 'bv-4n', 'Bishop to the long diagonal', 'Your Italian bishop, same plan', 'core',
  J(FK, "Bc4 Bc5 d3 d6 Bg5 h6 Bxf6 Qxf6 Nd5 Qd8"),
  alts=[('bv-italian4n-oo', 'White castles', J(FK, "Bc4 Bc5 O-O d6 d3 Na5")),
        ('bv-italian4n-nxe5', 'Knight grabs your pawn: the fork fails', J(FK, "Bc4 Bc5 Nxe5 Nxe5 d4 Nxc4 dxc5 d5"))],
  why='The same position as the Italian with the knights out. You won against bessauro14 from here.', outcome='Equal', tags=['game'])
L('bv-quiet4n', 'bv-4n', 'Slow fourth moves', 'Strike in the center with the d-pawn', 'common',
  J(FK, "d3 d5 exd5 Nxd5"),
  alts=[('bv-quiet4n-a3', 'Edge pawn', J(FK, "a3 d5 exd5 Nxd5")),
        ('bv-quiet4n-be2', 'Bishop to the quiet square', J(FK, "Be2 d5 exd5 Nxd5")),
        ('bv-quiet4n-g3', 'Fianchetto', J(FK, "g3 d5 exd5 Nxd5"))],
  why='When White wastes a move, your d-pawn takes the center for free.', outcome='Equal; you have the center')

L('bv-bc4', 'bv-vienna', 'Bishop out: knight jumps to the edge', 'Knight takes White\'s Italian bishop, then the d-pawn strikes', 'core',
  J(VI, "Bc4 Nf6 d3 Na5 Bb3 Nxb3 axb3 d5"),
  alts=[('bv-bc4-nf3', 'Knight out: back in the Four Knights', J(VI, "Bc4 Nf6 Nf3 Bc5 d3 d6")),
        ('bv-bc4-bg5', 'Bishop pins your knight', J(VI, "Bc4 Nf6 d3 Na5 Bg5 Nxc4 dxc4 h6")),
        ('bv-bc4-qf3', 'Queen comes out: jump into the center', J(VI, "Bc4 Nf6 Qf3 Nd4 Qd1 c6")),
        ('bv-bc4-qd3', 'Queen out, then to the middle', J(VI, "Bc4 Nf6 Qf3 Nd4 Qd3 c6")),
        ('bv-bc4-qf3g3', 'Queen out, then to the side: the fork', J(VI, "Bc4 Nf6 Qf3 Nd4 Qg3 Nxc2+"))],
  why='Against irekmary in July your bishop came out first and White\'s queen hit your g-pawn on move four. With the knight out first, the queen can\'t come.', outcome='Equal; you get the bishop pair', tags=['game', 'swap'])
L('bv-f4', 'bv-vienna', 'The Vienna Gambit', 'Take the f-pawn, then push the g-pawn and kick the knight', 'core',
  J(VI, "f4 exf4 Nf3 g5 d4 g4 Bc4 gxf3"),
  alts=[('bv-f4-ne5', 'Knight jumps forward', J(VI, "f4 exf4 Nf3 g5 d4 g4 Ne5 Qh4+")),
        ('bv-f4-bxf4', 'Bishop takes back the pawn', J(VI, "f4 exf4 Nf3 g5 d4 g4 Bxf4 gxf3")),
        ('bv-f4-d5', 'Pawn hits your knight', J(VI, "f4 exf4 Nf3 g5 d4 g4 d5 gxf3")),
        ('bv-f4-nd2', 'Knight steps back', J(VI, "f4 exf4 Nf3 g5 d4 g4 Nd2 Qh4+")),
        ('bv-f4-bc4', 'Bishop out, then castle', J(VI, "f4 exf4 Nf3 g5 Bc4 g4 O-O gxf3 Qxf3 Bc5+")),
        ('bv-f4-bc4r', 'Bishop out, castle, rook takes back', J(VI, "f4 exf4 Nf3 g5 Bc4 g4 O-O gxf3 Rxf3 Ne5")),
        ('bv-f4-ng1', 'Bishop out, knight goes home', J(VI, "f4 exf4 Nf3 g5 Bc4 g4 Ng1 Qh4+")),
        ('bv-f4-bxf7', 'Bishop takes on f7', J(VI, "f4 exf4 Nf3 g5 Bc4 g4 Bxf7+ Kxf7")),
        ('bv-f4-h4', 'Edge pawn hits your pawn', J(VI, "f4 exf4 Nf3 g5 h4 g4 Ng5 h6 Nxf7 Kxf7")),
        ('bv-f4-qxg4', 'Edge pawn, then the queen grabs', J(VI, "f4 exf4 Nf3 g5 h4 g4 Ng5 h6 Qxg4 hxg5")),
        ('bv-f4-d4', 'Center first: queen check', J(VI, "f4 exf4 d4 Qh4+ Ke2 d5")),
        ('bv-f4-g3', 'Center first, then the block', J(VI, "f4 exf4 d4 Qh4+ g3 fxg3")),
        ('bv-f4-kd2', 'Center first, king steps up', J(VI, "f4 exf4 d4 Qh4+ Kd2 Nxd4"))],
  why='You won with this pawn push against Mathzombie10 and lost after the quieter knight move against Danichondo.', outcome='You are a pawn up with an attack', tags=['game'])
L('bv-vmisc', 'bv-vienna', 'Other Vienna moves', 'Knight out and take the center', 'common',
  J(VI, "Nf3 Nf6 Bb5 Bb4"),
  alts=[('bv-vmisc-d4', 'Knight out, then the center push', J(VI, "Nf3 Nf6 d4 exd4 Nxd4 Bb4")),
        ('bv-vmisc-bc4', 'Knight out, then the Italian bishop', J(VI, "Nf3 Nf6 Bc4 Bc5 d3 d6")),
        ('bv-vmisc-bb5', 'Bishop pins first', J(VI, "Bb5 Nf6 Nf3 Bb4")),
        ('bv-vmisc-bxc6', 'Bishop takes your knight', J(VI, "Bb5 Nf6 Bxc6 dxc6")),
        ('bv-vmisc-d3', 'Small d-pawn move', J(VI, "d3 Nf6 Nf3 d5")),
        ('bv-vmisc-d3bg5', 'Small d-pawn, then the pin', J(VI, "d3 Nf6 Bg5 Be7")),
        ('bv-vmisc-g3', 'Fianchetto', J(VI, "g3 Bc5 Bg2 d6"))],
  why='The other ways White develops the queen\'s knight first.', outcome='Equal')

L('bv-ponziani', 'bv-quiet', 'Small c-pawn move', 'Knight takes the e-pawn; meet the push with the knight retreat', 'common',
  J(KN, "c3 Nf6 d4 Nxe4 dxe5 d5"),
  alts=[('bv-ponziani-d5', 'Pawn pushes past your knight', J(KN, "c3 Nf6 d4 Nxe4 d5 Bc5")),
        ('bv-ponziani-d3', 'Small d-pawn move', J(KN, "c3 Nf6 d3 d5"))],
  why='The Ponziani. Rare, but the knight grab leaves you comfortable.', outcome='Equal')
L('bv-d3', 'bv-quiet', 'Small d-pawn move', 'Knight out, then strike with the d-pawn', 'common',
  J(KN, "d3 Nf6 Be2 d5 exd5 Nxd5"),
  alts=[('bv-d3-bg5', 'Bishop pins your knight', J(KN, "d3 Nf6 Bg5 h6 Bxf6 Qxf6")),
        ('bv-d3-nc3', 'Knight out', J(KN, "d3 Nf6 Nc3 d5 exd5 Nxd5")),
        ('bv-be2', 'Bishop to the quiet square', J(KN, "Be2 Nf6 d3 d5 exd5 Nxd5")),
        ('bv-be2nc3', 'Bishop, then the knight', J(KN, "Be2 Nf6 Nc3 d5 exd5 Nxd5")),
        ('bv-2d3', 'Small d-pawn move on move two', J(E, "d3 Nc6 Nf3 Nf6"))],
  why='Slow moves give you the center for free.', outcome='Equal; you own the center')
L('bv-tricks', 'bv-quiet', 'Odd third moves', 'Two of them lose material', 'rare',
  J(KN, "Nxe5 Nxe5 d4 Ng6"),
  alts=[('bv-tricks-c4', 'Side pawn', J(KN, "c4 Bc5 Nc3 d6")),
        ('bv-2c3', 'Small c-pawn on move two', J(E, "c3 Nc6 d4 exd4 cxd4 d5"))],
  why='Rare tries. The knight grab simply drops a piece.', outcome='Equal or better')

# ============================================================== EARLY ATTACKS
QH = J(E, "Qh5 Nc6")
P('ba-queen', 'attacks', 'The early queen', 'Wayward Queen',
  'White brings the queen out on move two to aim at f7. Guard with the pawn and knight, then kick the queen around with tempo.')
P('ba-kg', 'attacks', 'The f-pawn gambit', 'King\'s Gambit',
  'White offers the f-pawn to rip open the f-file. Take it, then hit back in the center with your d-pawn.')
P('ba-bishop', 'attacks', 'Bishop out on move two', 'Bishop\'s Opening',
  'White puts the bishop on the f7 diagonal before the knight. Most of the time you are back in the Italian.')

L('ba-qh5', 'ba-queen', 'Queen hits f7 twice', 'Pawn blocks, knight blocks, then castle or jump into the center', 'core',
  J(QH, "Bc4 g6 Qf3 Nf6 c3 Bg7 d3 O-O"),
  alts=[('ba-qh5-d3', 'Small d-pawn: jump into the center', J(QH, "Bc4 g6 Qf3 Nf6 d3 Nd4 Qd1 d5")),
        ('ba-qh5-d3g3', 'Small d-pawn, queen to the side: fork', J(QH, "Bc4 g6 Qf3 Nf6 d3 Nd4 Qg3 Nxc2+")),
        ('ba-qh5-ne2', 'Knight guards the center square', J(QH, "Bc4 g6 Qf3 Nf6 Ne2 Bg7 d3 O-O")),
        ('ba-qh5-c3ne2', 'Small c-pawn, then the knight', J(QH, "Bc4 g6 Qf3 Nf6 c3 Bg7 Ne2 O-O")),
        ('ba-qh5-c3g4', 'Small c-pawn, then the pawn storm', J(QH, "Bc4 g6 Qf3 Nf6 c3 Bg7 g4 d5")),
        ('ba-qh5-nc3', 'Knight out', J(QH, "Bc4 g6 Qf3 Nf6 Nc3 Nd4 Qd1 c6")),
        ('ba-qh5-nc3d3', 'Knight out, queen to the middle', J(QH, "Bc4 g6 Qf3 Nf6 Nc3 Nd4 Qd3 c6")),
        ('ba-qh5-g4', 'Pawn storm: the knight jump wins', J(QH, "Bc4 g6 Qf3 Nf6 g4 Nd4 Qd1 d5")),
        ('ba-qh5-nh3', 'Knight to the edge', J(QH, "Bc4 g6 Qf3 Nf6 Nh3 Nd4")),
        ('ba-qh5-qb3', 'Queen switches to f7 again', J(QH, "Bc4 g6 Qf3 Nf6 Qb3 Nd4"))],
  why='You lost twice to this on Oct 14, against GambitTwojejKozy and Nona_Zulfa. Both times your bishop went to the Italian diagonal and White\'s queen and bishop won your knight. The bishop belongs next to your king.', outcome='You are better', tags=['game', 'swap'])
L('ba-qh5-other', 'ba-queen', 'Other queen moves', 'Knight out with a threat every time', 'common',
  J(QH, "Nf3 Nf6 Qh4 Be7"),
  alts=[('ba-qh5-qg5', 'Knight out, queen to the side', J(QH, "Nf3 Nf6 Qg5 h6")),
        ('ba-qh5-qf5', 'Knight out, queen to the light square', J(QH, "Nf3 Nf6 Qf5 d5")),
        ('ba-qh5-bb5', 'Bishop pins your knight', J(QH, "Bb5 Nf6")),
        ('ba-qh5-nc3x', 'Knight guards', J(QH, "Nc3 Nf6 Qf3 Nd4")),
        ('ba-qh5-c3', 'Small c-pawn move', J(QH, "c3 Nf6 Qf3 d5")),
        ('ba-qh5-d3x', 'Small d-pawn move', J(QH, "d3 Nf6 Qf3 d5")),
        ('ba-qf3', 'Queen to the other side', J(E, "Qf3 Nc6 Bc4 Nf6 c3 Be7")),
        ('ba-qf3-d3', 'Queen out, then the d-pawn', J(E, "Qf3 Nc6 Bc4 Nf6 d3 Nd4")),
        ('ba-qf3-ne2', 'Queen out, then the knight', J(E, "Qf3 Nc6 Bc4 Nf6 Ne2 d5")),
        ('ba-qf3-g4', 'Queen out, then the pawn storm', J(E, "Qf3 Nc6 Bc4 Nf6 g4 Nd4"))],
  why='Early queen moves come up a few times in every hundred games at your level.', outcome='You are better')
L('ba-kg', 'ba-kg', 'Take, then hit back in the center', 'Pawn takes, d-pawn strikes, knight takes back', 'core',
  J(E, "f4 exf4 Nf3 d5 exd5 Nf6 Bc4 Nxd5 O-O Be6"),
  alts=[('ba-kg-bc4d4', 'Bishop out, then the center push', J(E, "f4 exf4 Nf3 d5 exd5 Nf6 Bc4 Nxd5 d4 Be6")),
        ('ba-kg-nc3', 'Knight out', J(E, "f4 exf4 Nf3 d5 exd5 Nf6 Nc3 Nxd5 Nxd5 Qxd5")),
        ('ba-kg-d4', 'Center push', J(E, "f4 exf4 Nf3 d5 exd5 Nf6 d4 Nxd5 Bc4 Be6")),
        ('ba-kg-d4c4', 'Center push, then the c-pawn: bishop check', J(E, "f4 exf4 Nf3 d5 exd5 Nf6 d4 Nxd5 c4 Bb4+")),
        ('ba-kg-c4', 'Pawn guards the pawn', J(E, "f4 exf4 Nf3 d5 exd5 Nf6 c4 c6")),
        ('ba-kg-bb5', 'Bishop check', J(E, "f4 exf4 Nf3 d5 exd5 Nf6 Bb5+ c6 dxc6 Nxc6")),
        ('ba-kg-e5', 'Pawn pushes past', J(E, "f4 exf4 Nf3 d5 e5 g5")),
        ('ba-kg-bc4', 'Bishop out first', J(E, "f4 exf4 Bc4 Nf6 Nc3 c6")),
        ('ba-kg-bc4nf3', 'Bishop out, then the knight: take the e-pawn', J(E, "f4 exf4 Bc4 Nf6 Nf3 Nxe4")),
        ('ba-kg-bc4e5', 'Bishop out, then the push', J(E, "f4 exf4 Bc4 Nf6 e5 d5"))],
  why='Against TiepiMT in July the knight went behind the pawns; you still got a winning position and lost on time. The d-pawn strike is the classic answer.', outcome='Equal; you keep the extra pawn for now', tags=['game'])
L('ba-bc4', 'ba-bishop', 'Bishop out on move two', 'Knight out; back to your Italian or the center grab', 'common',
  J(E, "Bc4 Nc6 d3 Nf6 Nf3 Bc5"),
  alts=[('ba-bc4-bg5', 'Small d-pawn, then the pin', J(E, "Bc4 Nc6 d3 Nf6 Bg5 h6")),
        ('ba-bc4-nf3', 'Knight out: the Italian', J(E, "Bc4 Nc6 Nf3 Bc5 c3 Nf6")),
        ('ba-bc4-nf3d3', 'Knight out, small d-pawn', J(E, "Bc4 Nc6 Nf3 Bc5 d3 Nf6")),
        ('ba-bc4-nf3oo', 'Knight out, castle', J(E, "Bc4 Nc6 Nf3 Bc5 O-O Nf6")),
        ('ba-bc4-c3', 'Small c-pawn move', J(E, "Bc4 Nc6 c3 Nf6 d3 d5")),
        ('ba-bc4-c3d4', 'Small c-pawn, then the push', J(E, "Bc4 Nc6 c3 Nf6 d4 Nxe4")),
        ('ba-bc4-qf3', 'Queen out', J(E, "Bc4 Nc6 Qf3 Nf6 Ne2 Na5")),
        ('ba-bc4-qf3c3', 'Queen out, small c-pawn', J(E, "Bc4 Nc6 Qf3 Nf6 c3 Na5")),
        ('ba-bc4-qf3d3', 'Queen out, small d-pawn', J(E, "Bc4 Nc6 Qf3 Nf6 d3 Nd4")),
        ('ba-bc4-qh5', 'Queen hits f7', J(E, "Bc4 Nc6 Qh5 g6 Qf3 Nf6")),
        ('ba-bc4-bxf7', 'Bishop takes on f7', J(E, "Bc4 Nc6 Bxf7+ Kxf7 Qh5+ g6")),
        ('ba-bc4-bxf7n', 'Bishop takes on f7, then the knight', J(E, "Bc4 Nc6 Bxf7+ Kxf7 Nf3 d6")),
        ('ba-bc4-bxf7q', 'Bishop takes on f7, then queen check', J(E, "Bc4 Nc6 Bxf7+ Kxf7 Qf3+ Nf6")),
        ('ba-bc4-nc3', 'Knight out: back in the Vienna', J(E, "Bc4 Nc6 Nc3 Nf6 d3 Na5")),
        ('ba-bc4-nc3nf3', 'Both knights out: the Four Knights', J(E, "Bc4 Nc6 Nc3 Nf6 Nf3 Bc5")),
        ('ba-bc4-nf3nc3', 'Knight out, then the other knight', J(E, "Bc4 Nc6 Nf3 Bc5 Nc3 Nf6"))],
  why='Three of your games started this way. Most move orders lead back to the Italian or the Vienna.', outcome='Equal', tags=['game'])

# ============================================================== QUEEN'S GAMBIT (1.d4 Nf6 2.c4 e6)
D = "d4 Nf6"
QG = J(D, "c4 e6")
QC = J(QG, "Nc3 d5")
P('bq-classic', 'qgd', 'The classical setup', 'Queen\'s Gambit Declined',
  'Knight, e-pawn, d-pawn, bishop, castle. Then the h-pawn asks the bishop and your knight jumps forward to trade.')
P('bq-exchange', 'qgd', 'White trades in the center', 'Exchange',
  'White takes on your d-pawn early. Take back with the e-pawn, castle, and put a pawn beside your d-pawn.')
P('bq-other', 'qgd', 'Other third moves', 'Catalan & sidelines',
  'White develops the king\'s knight or fianchettoes. Same setup, and take the c-pawn when White can\'t win it back fast.')

L('bq-ortho', 'bq-classic', 'Bishop pins: the trade trick', 'Castle, ask the bishop, then the knight jump trades two pairs', 'core',
  J(QC, "Bg5 Be7 e3 O-O Nf3 h6 Bh4 Ne4 Bxe7 Qxe7 cxd5 Nxc3 bxc3 exd5"),
  alts=[('bq-ortho-bxf6', 'Bishop takes your knight', J(QC, "Bg5 Be7 e3 O-O Nf3 h6 Bxf6 Bxf6")),
        ('bq-ortho-nxe4', 'Knight takes knight', J(QC, "Bg5 Be7 e3 O-O Nf3 h6 Bh4 Ne4 Nxe4 Bxh4")),
        ('bq-ortho-bd3', 'Bishop out before the knight', J(QC, "Bg5 Be7 e3 O-O Bd3 h6 Bxf6 Bxf6")),
        ('bq-ortho-bd3h4', 'Bishop out, then back on the pin: take the c-pawn', J(QC, "Bg5 Be7 e3 O-O Bd3 h6 Bh4 dxc4")),
        ('bq-ortho-nxe4b', 'Bishops trade, then knight takes knight', J(QC, "Bg5 Be7 e3 O-O Nf3 h6 Bh4 Ne4 Bxe7 Qxe7 Nxe4 dxe4")),
        ('bq-ortho-nf3', 'Knight first', J(QC, "Bg5 Be7 Nf3 O-O e3 h6 Bh4 Ne4")),
        ('bq-ortho-early', 'Bishop takes at once', J(QC, "Bg5 Be7 Bxf6 Bxf6")),
        ('bq-ortho-cxd5', 'Pawn trade after the pin', J(QC, "Bg5 Be7 cxd5 exd5 e3 O-O"))],
  why='The classical Queen\'s Gambit. You played the same first moves in your July games.', outcome='Equal and solid')
L('bq-nf3', 'bq-classic', 'Knight out first', 'Same setup; strike with the c-pawn if the bishop goes to the side', 'common',
  J(QC, "Nf3 Be7 Bg5 O-O e3 h6 Bh4 Ne4"),
  alts=[('bq-nf3-e3', 'Small e-pawn move', J(QC, "Nf3 Be7 e3 O-O Bd3 dxc4 Bxc4 c5")),
        ('bq-nf3-bf4', 'Bishop to the long diagonal', J(QC, "Nf3 Be7 Bf4 O-O e3 c5")),
        ('bq-nf3-cxd5', 'Pawn trade', J(QC, "Nf3 Be7 cxd5 exd5"))],
  why='The knight comes out first in about a quarter of games.', outcome='Equal')
L('bq-quiet', 'bq-classic', 'Small e-pawn or bishop out', 'Strike with the c-pawn', 'common',
  J(QC, "e3 Be7 Nf3 O-O Bd3 dxc4 Bxc4 c5"),
  alts=[('bq-quiet-bf4', 'Bishop to the long diagonal', J(QC, "Bf4 c5 e3 cxd4 exd4 Be7")),
        ('bq-quiet-a3', 'Edge pawn', J(QC, "a3 c5 e3 cxd4 exd4 Be7"))],
  why='When White\'s dark bishop stays home or goes to the side, the c-pawn strike frees your game.', outcome='Equal')
L('bq-exch', 'bq-exchange', 'Pawn trade: take back with the e-pawn', 'Bishop, castle, then the c-pawn beside your d-pawn', 'core',
  J(QC, "cxd5 exd5 Bg5 Be7 e3 O-O Bd3 c6"),
  alts=[('bq-exch-nf3', 'Knight out after the trade', J(QC, "cxd5 exd5 Nf3 Be7 Bg5 O-O")),
        ('bq-exch-nf3bf4', 'Knight out, then the bishop', J(QC, "cxd5 exd5 Nf3 Be7 Bf4 c6")),
        ('bq-exch-nf3e3', 'Knight out, then the e-pawn', J(QC, "cxd5 exd5 Nf3 Be7 e3 O-O")),
        ('bq-exch-bg5nf3', 'Bishop pins, then the knight', J(QC, "cxd5 exd5 Bg5 Be7 Nf3 O-O")),
        ('bq-exch-e3nf3', 'Bishop pins, e-pawn, then the knight', J(QC, "cxd5 exd5 Bg5 Be7 e3 O-O Nf3 c6")),
        ('bq-exch-bxf6', 'Bishop takes your knight', J(QC, "cxd5 exd5 Bg5 Be7 Bxf6 Bxf6")),
        ('bq-exch-bf4', 'Bishop to the long diagonal', J(QC, "cxd5 exd5 Bf4 c6 e3 Bd6")),
        ('bq-exch-e3', 'Small e-pawn move', J(QC, "cxd5 exd5 e3 Bd6"))],
  why='The pawn trade gives you an open file for your rook and easy development.', outcome='Equal')
L('bq-3nf3', 'bq-other', 'Knight out on move three', 'Same setup; take the c-pawn if White fianchettoes', 'common',
  J(QG, "Nf3 d5 Nc3 Be7 Bg5 O-O e3 h6"),
  alts=[('bq-3nf3-e3', 'Small e-pawn move', J(QG, "Nf3 d5 e3 Be7 Bd3 O-O")),
        ('bq-3nf3-e3nc3', 'Small e-pawn, then the knight', J(QG, "Nf3 d5 e3 Be7 Nc3 O-O")),
        ('bq-3nf3-nc3e3', 'Knight, then the small e-pawn', J(QG, "Nf3 d5 Nc3 Be7 e3 O-O")),
        ('bq-3nf3-g3', 'Fianchetto: the Catalan', J(QG, "Nf3 d5 g3 Be7 Bg2 O-O O-O dxc4")),
        ('bq-3nf3-bg5', 'Bishop pins your knight', J(QG, "Nf3 d5 Bg5 Be7 e3 O-O")),
        ('bq-3nf3-bf4', 'Bishop to the long diagonal', J(QG, "Nf3 d5 Bf4 dxc4")),
        ('bq-3nf3-cxd5', 'Pawn trade', J(QG, "Nf3 d5 cxd5 exd5 Nc3 c6"))],
  why='About one game in seven goes this way.', outcome='Equal')
L('bq-3other', 'bq-other', 'Odd third moves', 'Same setup against everything', 'common',
  J(QG, "e3 d5 Nc3 Be7 Nf3 O-O"),
  alts=[('bq-3other-g3', 'Fianchetto', J(QG, "g3 d5 Bg2 Be7 Nf3 O-O")),
        ('bq-3other-g3nc3', 'Fianchetto, then the knight', J(QG, "g3 d5 Bg2 Be7 Nc3 O-O")),
        ('bq-3other-bg5', 'Bishop pins at once', J(QG, "Bg5 h6 Bxf6 Qxf6")),
        ('bq-3other-bh4', 'Bishop pins, then stays', J(QG, "Bg5 h6 Bh4 Be7")),
        ('bq-3other-a3', 'Edge pawn', J(QG, "a3 d5 Nc3 c5")),
        ('bq-3other-bf4', 'Bishop to the long diagonal', J(QG, "Bf4 d5 Nc3 c5"))],
  why='Rarer third moves. You keep the same pieces on the same squares.', outcome='Equal')

# ============================================================== LONDON SYSTEM
LD = J(D, "Bf4 d5")
LC = J(LD, "e3 c5 c3 Nc6")
P('bl-main', 'london', 'Bishop out before the e-pawn', 'London System',
  'White plays the same setup every game. Put your d-pawn in the middle first, then hit with the c-pawn and trade off the London bishop.')
P('bl-other', 'london', 'Other London move orders', 'Knight first & Jobava',
  'The knight comes out first, or the queen\'s knight joins the bishop. Same plan.')

L('bl-main', 'bl-main', 'Center pawn first, then the c-pawn', 'Knight out, e-pawn, then the bishop that trades White\'s', 'core',
  J(LC, "Nd2 e6 Ngf3 Bd6 Bg3 O-O"),
  alts=[('bl-main-bxd6', 'Bishop takes your bishop', J(LC, "Nd2 e6 Ngf3 Bd6 Bxd6 Qxd6")),
        ('bl-main-ne5', 'Knight jumps forward', J(LC, "Nd2 e6 Ngf3 Bd6 Ne5 O-O")),
        ('bl-main-nf3', 'Knight out before the queen\'s knight', J(LC, "Nf3 e6 Nbd2 Bd6 Bg3 O-O")),
        ('bl-main-nf3bd3', 'Knight, then the bishop', J(LC, "Nf3 e6 Bd3 Bd6")),
        ('bl-main-nf3bxd6', 'Knight, then the bishop trade', J(LC, "Nf3 e6 Nbd2 Bd6 Bxd6 Qxd6")),
        ('bl-main-bd3', 'Bishop out', J(LC, "Bd3 e6 Nf3 Bd6")),
        ('bl-main-bb5', 'Bishop pins your knight', J(LC, "Bb5 Qb6")),
        ('bl-main-nd2bd3', 'Knight, then the bishop', J(LC, "Nd2 e6 Bd3 Bd6"))],
  why='Three of your London games went wrong after an early knight jump to the center and a queen check. This keeps it simple.', outcome='Equal; you are never worse', tags=['game', 'swap'])
L('bl-early', 'bl-main', 'White skips the small c-pawn move', 'Trade in the center or develop, then the same bishop trade', 'common',
  J(LD, "e3 c5 Nf3 e6 c3 Nc6"),
  alts=[('bl-early-dxc5', 'Pawn takes your c-pawn', J(LD, "e3 c5 dxc5 e6")),
        ('bl-early-c4', 'Pawn hits your d-pawn', J(LD, "e3 c5 c4 cxd4 exd4 Nc6")),
        ('bl-early-c4q', 'Pawn hits your d-pawn, queen takes back', J(LD, "e3 c5 c4 cxd4 Qxd4 Nc6")),
        ('bl-early-bb5', 'Bishop check', J(LD, "e3 c5 Bb5+ Bd7")),
        ('bl-early-bd3', 'Bishop out', J(LD, "e3 c5 Bd3 Nc6")),
        ('bl-early-nd2', 'Knight out', J(LD, "e3 c5 Nd2 Nc6")),
        ('bl-early-nc3', 'Knight in front of the c-pawn', J(LD, "e3 c5 Nc3 cxd4 exd4 a6")),
        ('bl-early-nc3q', 'Knight in front of the c-pawn, queen takes back', J(LD, "e3 c5 Nc3 cxd4 Qxd4 Nc6"))],
  why='White doesn\'t always play the small c-pawn move. Your pieces go to the same squares.', outcome='Equal')
L('bl-nf3', 'bl-other', 'Knight out first', 'Same plan: d-pawn, c-pawn, knight, e-pawn', 'core',
  J(D, "Nf3 d5 Bf4 c5 e3 Nc6 c3 e6"),
  alts=[('bl-nf3-c3', 'Small c-pawn first', J(D, "Nf3 d5 Bf4 c5 c3 Nc6 e3 e6")),
        ('bl-nf3-bb5', 'Bishop pins your knight', J(D, "Nf3 d5 Bf4 c5 e3 Nc6 Bb5 e6")),
        ('bl-nf3-dxc5', 'Pawn takes your c-pawn', J(D, "Nf3 d5 Bf4 c5 dxc5 e6")),
        ('bl-nf3-bf4nf3', 'Bishop first, then the knight', J(LD, "Nf3 c5 e3 e6")),
        ('bl-nf3-nf3c3', 'Bishop, knight, then the small c-pawn', J(LD, "Nf3 c5 c3 Nc6"))],
  why='A fifth of London players bring the knight out before the bishop.', outcome='Equal')
L('bl-jobava', 'bl-other', 'Both knights and bishops: the Jobava', 'E-pawn one square, then pin the knight', 'common',
  J(LD, "Nc3 e6 e3 Bb4"),
  alts=[('bl-jobava-nb5', 'Knight jumps at your c-pawn', J(LD, "Nc3 e6 Nb5 Na6")),
        ('bl-jobava-nf3', 'Knight out', J(LD, "Nc3 e6 Nf3 Bb4")),
        ('bl-jobava-a3', 'Edge pawn', J(LD, "Nc3 e6 a3 c5"))],
  why='The queen\'s knight comes out next to the London bishop. Watch for the jump at your c-pawn.', outcome='Equal')

# ============================================================== OTHER D-PAWN SYSTEMS
P('bd-colle', 'd4x', 'Small e-pawn systems', 'Colle',
  'White builds a quiet triangle of pawns and aims the bishop at your king. Copy the setup and hit with the c-pawn.')
P('bd-bg5', 'd4x', 'Early bishop pin', 'Trompowsky & Torre',
  'White pins or takes your knight on move two or three. Take back toward the center and use your two bishops.')
P('bd-nc3', 'd4x', 'The queen\'s knight comes out early', 'Jobava & Veresov',
  'White puts the queen\'s knight in front of the c-pawn. Keep your d-pawn in the middle and develop.')

L('bd-colle', 'bd-colle', 'The Colle setup', 'Copy it, then strike with the c-pawn; never close the center', 'core',
  J(D, "Nf3 d5 e3 e6 Bd3 c5 c3 Nc6 Nbd2 Bd6 O-O O-O"),
  alts=[('bd-colle-dxc5', 'Pawn takes your c-pawn', J(D, "Nf3 d5 e3 e6 Bd3 c5 c3 Nc6 Nbd2 Bd6 O-O O-O dxc5 Bxc5")),
        ('bd-colle-e4', 'The e-pawn push', J(D, "Nf3 d5 e3 e6 Bd3 c5 c3 Nc6 Nbd2 Bd6 e4 dxe4")),
        ('bd-colle-re1', 'Rook to the e-file', J(D, "Nf3 d5 e3 e6 Bd3 c5 c3 Nc6 Nbd2 Bd6 O-O O-O Re1 Qc7")),
        ('bd-colle-oo', 'Castle before the knight', J(D, "Nf3 d5 e3 e6 Bd3 c5 c3 Nc6 O-O Bd6")),
        ('bd-colle-dx', 'Early pawn trade', J(D, "Nf3 d5 e3 e6 Bd3 c5 dxc5 Bxc5")),
        ('bd-colle-c4', 'Pawn hits your d-pawn', J(D, "Nf3 d5 e3 e6 c4 Be7")),
        ('bd-colle-be2', 'Bishop to the quiet square', J(D, "Nf3 d5 e3 e6 Be2 c5")),
        ('bd-colle-e3', 'Small e-pawn on move two', J(D, "e3 d5 Nf3 e6")),
        ('bd-colle-e3bd3', 'Small e-pawn, then the bishop', J(D, "e3 d5 Bd3 c5"))],
  why='Against CamiloS8 in July you pushed the c-pawn past and shut your own pieces in. Keep the tension.', outcome='Equal', tags=['game'])
L('bd-nf3', 'bd-colle', 'Knight out, then something else', 'D-pawn in the middle, then e-pawn and c-pawn', 'common',
  J(D, "Nf3 d5 Nc3 e6 Bg5 Nbd7"),
  alts=[('bd-nf3-g3', 'Fianchetto', J(D, "Nf3 d5 g3 e6 Bg2 Be7")),
        ('bd-nf3-c3', 'Small c-pawn move', J(D, "Nf3 d5 c3 e6 Bf4 c5")),
        ('bd-nf3-c3bg5', 'Small c-pawn, then the pin', J(D, "Nf3 d5 c3 e6 Bg5 Be7")),
        ('bd-nf3-b3', 'Queen\'s fianchetto', J(D, "Nf3 d5 b3 c5")),
        ('bd-nf3-c4', 'Pawn hits your d-pawn: back to the Queen\'s Gambit', J(D, "Nf3 d5 c4 e6 Nc3 Be7"))],
  why='Every second-move knight leads to a setup you know from the London or the Queen\'s Gambit.', outcome='Equal')
L('bd-tromp', 'bd-bg5', 'Bishop takes your knight', 'Take back with the e-pawn; your bishops get open lines', 'core',
  J(D, "Bg5 d5 Bxf6 exf6 e3 Bd6 Nf3 O-O"),
  alts=[('bd-tromp-c4b', 'Small e-pawn, then the c-pawn', J(D, "Bg5 d5 Bxf6 exf6 e3 Bd6 c4 dxc4 Bxc4 O-O")),
        ('bd-tromp-bd3', 'Small e-pawn, then the bishop', J(D, "Bg5 d5 Bxf6 exf6 e3 Bd6 Bd3 O-O")),
        ('bd-tromp-nf3', 'Knight out', J(D, "Bg5 d5 Bxf6 exf6 Nf3 Nd7")),
        ('bd-tromp-nc3', 'Knight in front of the c-pawn', J(D, "Bg5 d5 Bxf6 exf6 Nc3 c6")),
        ('bd-tromp-c4', 'Pawn hits your d-pawn', J(D, "Bg5 d5 Bxf6 exf6 c4 dxc4")),
        ('bd-tromp-e3', 'Bishop stays: c-pawn strike', J(D, "Bg5 d5 e3 c5 c3 Qb6")),
        ('bd-tromp-nd2', 'The other knight comes out', J(D, "Bg5 d5 Nd2 c5")),
        ('bd-tromp-nf3x', 'Knight out: knight jump', J(D, "Bg5 d5 Nf3 Ne4 Bf4 c5")),
        ('bd-tromp-nc3x', 'Knight in front of the c-pawn first', J(D, "Bg5 d5 Nc3 Nbd7"))],
  why='Against youssefdabbech in July you took back with the g-pawn, castled behind the broken pawns, and White\'s h-pawn broke through. Take with the e-pawn.', outcome='Equal; you have two bishops', tags=['game', 'swap'])
L('bd-torre', 'bd-bg5', 'Knight out, then the pin', 'Knight jumps forward and hits the bishop', 'common',
  J(D, "Nf3 d5 Bg5 Ne4 Bf4 c5"),
  alts=[('bd-torre-bh4', 'Bishop steps back on the pin line', J(D, "Nf3 d5 Bg5 Ne4 Bh4 c5"))],
  why='The Torre. The knight jump makes White decide about the bishop.', outcome='Equal')
L('bd-jobava', 'bd-nc3', 'Queen\'s knight out on move two', 'D-pawn in the middle, then develop', 'common',
  J(D, "Nc3 d5 Bf4 e6 e3 Bb4"),
  alts=[('bd-jobava-bg5', 'Bishop pins your knight', J(D, "Nc3 d5 Bg5 Nbd7 Nf3 h6")),
        ('bd-jobava-bxf6', 'Pin, then take', J(D, "Nc3 d5 Bg5 Nbd7 Bxf6 Nxf6")),
        ('bd-jobava-bg5e3', 'Pin, then the e-pawn', J(D, "Nc3 d5 Bg5 Nbd7 e3 e6")),
        ('bd-jobava-nf3', 'Knight out', J(D, "Nc3 d5 Nf3 e6")),
        ('bd-jobava-f3', 'Small f-pawn: the gambit idea', J(D, "Nc3 d5 f3 c5")),
        ('bd-jobava-e4', 'The e-pawn gambit', J(D, "Nc3 d5 e4 Nxe4"))],
  why='You beat Vitavolo and drew with Void_max in these lines. The setup is the same as always.', outcome='Equal', tags=['game'])
L('bd-misc', 'bd-nc3', 'Odd second moves', 'Center pawn and develop', 'rare',
  J(D, "d5 e6 c4 exd5 cxd5 Bb4+"),
  alts=[('bd-misc-d5nc3', 'Pawn pushes, then the knight', J(D, "d5 e6 Nc3 Bb4")),
        ('bd-misc-dxe6', 'Pawn takes your e-pawn', J(D, "d5 e6 dxe6 fxe6")),
        ('bd-misc-f3', 'Small f-pawn move', J(D, "f3 d5")),
        ('bd-misc-g3', 'Fianchetto', J(D, "g3 d5")),
        ('bd-misc-f4', 'The f-pawn', J(D, "f4 d5"))],
  why='Rare second moves. Take the center.', outcome='Equal')

# ============================================================== OTHER FIRST MOVES
P('bo-english', 'other', 'The c-pawn first', 'English',
  'White starts with the c-pawn. Play the e-pawn two squares, as you would against the e-pawn, and develop the knights.')
P('bo-flank', 'other', 'Knight or fianchetto first', 'Réti & King\'s fianchetto',
  'Against the knight, use your Queen\'s Gambit setup; against the g-pawn fianchetto, take the center with the e-pawn.')
P('bo-rare', 'other', 'Rare first moves', 'Sidelines',
  'Small pawn moves and edge moves. Take the center and develop, and punish the ones that weaken White\'s king.')

L('bo-english', 'bo-english', 'E-pawn against the c-pawn', 'Knights out, pin with the bishop, then push the e-pawn', 'core',
  J("c4 e5 Nc3 Nf6 Nf3 Nc6 g3 Bb4 Bg2 O-O O-O e4"),
  alts=[('bo-english-e3', 'Small e-pawn move', J("c4 e5 Nc3 Nf6 Nf3 Nc6 e3 Bb4")),
        ('bo-english-d4', 'Center push', J("c4 e5 Nc3 Nf6 Nf3 Nc6 d4 e4")),
        ('bo-english-e4', 'E-pawn two squares', J("c4 e5 Nc3 Nf6 Nf3 Nc6 e4 Bb4")),
        ('bo-english-d3', 'Small d-pawn move', J("c4 e5 Nc3 Nf6 Nf3 Nc6 d3 d5")),
        ('bo-english-g3', 'Fianchetto before the knight', J("c4 e5 Nc3 Nf6 g3 d5 cxd5 Nxd5 Bg2 Nb6")),
        ('bo-english-e3b', 'Small e-pawn first', J("c4 e5 Nc3 Nf6 e3 Nc6")),
        ('bo-english-e4b', 'E-pawn two squares first', J("c4 e5 Nc3 Nf6 e4 Bc5")),
        ('bo-english-d3b', 'Small d-pawn first', J("c4 e5 Nc3 Nf6 d3 d5"))],
  why='You beat Mahm00dsaad with the e-pawn reply in October.', outcome='Equal', tags=['game'])
L('bo-english2', 'bo-english', 'Other second moves', 'Same e-pawn, then the d-pawn strike', 'common',
  J("c4 e5 g3 Nf6 Bg2 d5 cxd5 Nxd5"),
  alts=[('bo-english2-e4', 'E-pawn two squares', J("c4 e5 e4 Nc6")),
        ('bo-english2-e3', 'Small e-pawn move', J("c4 e5 e3 Nf6")),
        ('bo-english2-d3', 'Small d-pawn move', J("c4 e5 d3 Nf6")),
        ('bo-english2-d4', 'Center push', J("c4 e5 d4 exd4 Qxd4 Nc6")),
        ('bo-english2-nf3', 'Knight hits your pawn: push past', J("c4 e5 Nf3 e4 Nd4 Nc6"))],
  why='The fianchetto is the next most common second move.', outcome='Equal')
L('bo-reti', 'bo-flank', 'Knight out first', 'Knight out too, then your Queen\'s Gambit setup', 'core',
  J("Nf3 Nf6 g3 d5 Bg2 e6 O-O Be7"),
  alts=[('bo-reti-d4', 'Center push: back in your d-pawn lines', J("Nf3 Nf6 d4 d5 Bf4 c5")),
        ('bo-reti-d4e3', 'Center push, then the small e-pawn', J("Nf3 Nf6 d4 d5 e3 e6")),
        ('bo-reti-c4', 'The c-pawn', J("Nf3 Nf6 c4 e6 Nc3 d5")),
        ('bo-reti-c4d4', 'The c-pawn, then the center', J("Nf3 Nf6 c4 e6 d4 d5")),
        ('bo-reti-c4g3', 'The c-pawn, then the fianchetto', J("Nf3 Nf6 c4 e6 g3 d5")),
        ('bo-reti-nc3', 'The queen\'s knight comes out', J("Nf3 Nf6 Nc3 d5")),
        ('bo-reti-e3', 'Small e-pawn move', J("Nf3 Nf6 e3 d5")),
        ('bo-reti-b3', 'Queen\'s fianchetto', J("Nf3 Nf6 b3 d5"))],
  why='You played the queen\'s knight out against this twice. The king\'s knight keeps you in setups you already know.', outcome='Equal')
L('bo-g3', 'bo-flank', 'King\'s fianchetto first', 'E-pawn two squares, then the d-pawn', 'common',
  J("g3 e5 Bg2 d5 d3 Nf6"),
  alts=[('bo-g3-b3', 'Double fianchetto', J("g3 e5 Bg2 d5 b3 Nf6")),
        ('bo-g3-e3', 'Small e-pawn move', J("g3 e5 Bg2 d5 e3 Nf6")),
        ('bo-g3-c4', 'The c-pawn: push past', J("g3 e5 Bg2 d5 c4 d4")),
        ('bo-g3-c4b', 'The c-pawn on move two', J("g3 e5 c4 Nf6 Bg2 d5 cxd5 Nxd5"))],
  why='Against Server_goat9 in July a pawn move took a guard away from your knight, and the long-diagonal bishop and queen won it. Keep your knight guarded.', outcome='Equal', tags=['game'])
L('bo-e3', 'bo-rare', 'Small e-pawn first', 'E-pawn two squares, then the d-pawn', 'common',
  J("e3 e5 d4 exd4 exd4 d5"),
  alts=[('bo-e3-b3', 'Queen\'s fianchetto', J("e3 e5 b3 d5")),
        ('bo-e3-c3', 'Small c-pawn move', J("e3 e5 c3 d5")),
        ('bo-e3-qh5', 'Queen lunges', J("e3 e5 Qh5 Nc6")),
        ('bo-e3-nf3', 'Knight hits your pawn', J("e3 e5 Nf3 Nc6 e4 Nf6")),
        ('bo-e3-d3', 'Small d-pawn move', J("e3 e5 d3 d5"))],
  why='If the e-pawn later goes forward a second time, you are simply a move ahead, as in your bullet game against shiblifx1.', outcome='Equal', tags=['game'])
L('bo-b3', 'bo-rare', 'Queen\'s fianchetto', 'Knight guards your e-pawn, then the d-pawn', 'common',
  J("b3 e5 Bb2 Nc6 e3 d5 Bb5 Bd6"),
  alts=[('bo-b3-g3', 'Double fianchetto', J("b3 e5 Bb2 Nc6 g3 d5")),
        ('bo-b3-nf3', 'Knight hits your pawn: push past', J("b3 e5 Bb2 Nc6 Nf3 e4 Nd4 Nxd4 Bxd4 d5")),
        ('bo-b3-c4', 'The c-pawn', J("b3 e5 Bb2 Nc6 c4 Nf6"))],
  why='The Nimzo-Larsen. Guard the e-pawn with the knight and take the center.', outcome='Equal')
L('bo-f4', 'bo-rare', 'The f-pawn first', 'D-pawn two squares, knight out, then the c-pawn', 'common',
  J("f4 d5 Nf3 Nf6 e3 c5"),
  alts=[('bo-f4-d4', 'Center push', J("f4 d5 Nf3 Nf6 d4 Bf5")),
        ('bo-f4-g3', 'Fianchetto', J("f4 d5 Nf3 Nf6 g3 c5")),
        ('bo-f4-b3', 'Queen\'s fianchetto', J("f4 d5 Nf3 Nf6 b3 Bf5")),
        ('bo-f4-e3', 'Small e-pawn move', J("f4 d5 e3 Nf6")),
        ('bo-f4-d4b', 'Center push first', J("f4 d5 d4 Nf6"))],
  why='The Bird. The f-pawn weakens White\'s king a little; develop normally.', outcome='Equal')
L('bo-misc', 'bo-rare', 'Edge moves and the b-pawn', 'Take the center; the b-pawn can be grabbed', 'rare',
  J("b4 e5 Bb2 Bxb4 Bxe5 Nf6"),
  alts=[('bo-misc-a3', 'B-pawn, then the edge pawn', J("b4 e5 a3 d5")),
        ('bo-misc-b5', 'B-pawn pushes on', J("b4 e5 b5 d5")),
        ('bo-misc-nc3', 'Queen\'s knight first', J("Nc3 e5 Nf3 Nc6 d4 exd4 Nxd4 Nf6")),
        ('bo-misc-nc3e4', 'Queen\'s knight, then the e-pawn', J("Nc3 e5 e4 Nc6 Nf3 Nf6")),
        ('bo-misc-nc3d4', 'Queen\'s knight, then the center push', J("Nc3 e5 d4 exd4 Qxd4 Nc6")),
        ('bo-misc-d3', 'Small d-pawn move', J("d3 e5 e4 Nf6")),
        ('bo-misc-g4', 'The g-pawn lunge', J("g4 d5 Bg2 Bxg4")),
        ('bo-misc-edge', 'Edge pawn', J("a3 e5")),
        ('bo-misc-h3', 'Edge pawn on the king\'s side', J("h3 e5")),
        ('bo-misc-c3', 'Small c-pawn move', J("c3 e5"))],
  why='These come up once in a long while. Take the center and develop.', outcome='Equal or better')
