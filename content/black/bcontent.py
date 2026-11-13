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
P('br-castle', 'ruy', 'White castles', 'Main line',
  'White castles and leaves the e-pawn to its fate. Ignore it: your bishop goes to the same diagonal as in the Italian and you castle too.')
P('br-quiet', 'ruy', 'Quiet fourth moves', 'Slow Spanish',
  'White guards the e-pawn and develops. Your bishop goes to the same diagonal as in the Italian.')
P('br-swap', 'ruy', 'Bishop takes your knight', 'Exchange',
  'White trades the bishop for your knight. Take back toward the center, then win your pawn back.')

L('br-oo', 'br-castle', 'White castles: bishop out, castle', 'Same setup as the Italian: bishop to its diagonal, castle, small d-pawn', 'core',
  J(RL, "O-O Bc5 c3 O-O d4 Bb6"),
  alts=[('br-oo-re1', 'Small c-pawn, then the rook', J(RL, "O-O Bc5 c3 O-O Re1 d6")),
        ('br-oo-re1first', 'Rook to the e-file first', J(RL, "O-O Bc5 Re1 O-O c3 d6")),
        ('br-oo-bxc6', 'Bishop takes, knight grabs your pawn: grab White\'s', J(RL, "O-O Bc5 Bxc6 dxc6 Nxe5 Nxe4")),
        ('br-oo-bxc6d3', 'Bishop takes, then the small d-pawn', J(RL, "O-O Bc5 Bxc6 dxc6 d3 Qe7")),
        ('br-oo-c3bxc6', 'Small c-pawn, then bishop takes', J(RL, "O-O Bc5 c3 O-O Bxc6 dxc6")),
        ('br-oo-d3', 'Small d-pawn move', J(RL, "O-O Bc5 d3 d6 Bg5 h6")),
        ('br-oo-d3c3', 'Small d-pawn, then the c-pawn', J(RL, "O-O Bc5 d3 d6 c3 O-O")),
        ('br-oo-nc3', 'Knight out', J(RL, "O-O Bc5 Nc3 O-O d3 d6"))],
  why='About a quarter of White players castle here. You already play the bishop out against the Spanish by instinct; this makes it the rule.', outcome='About equal; the same position type as your Italian')
L('br-d3', 'br-quiet', 'Pawn guards the e-pawn', 'Bishop out to the same diagonal as in the Italian', 'core',
  J(RL, "d3 Bc5 O-O d6 h3 O-O"),
  alts=[('br-d3-trap', 'Bishop takes, knight grabs: the queen fork', J(RL, "d3 Bc5 Bxc6 dxc6 Nxe5 Qd4")),
        ('br-d3-bxc6', 'Bishop takes your knight', J(RL, "d3 Bc5 Bxc6 dxc6 O-O Qe7")),
        ('br-d3-bg5', 'Bishop pins your knight', J(RL, "d3 Bc5 Bg5 h6 Bh4 O-O")),
        ('br-d3-oobg5', 'Castle, then the pin', J(RL, "d3 Bc5 O-O d6 Bg5 h6")),
        ('br-d3-oobxc6', 'Castle, then bishop takes with check', J(RL, "d3 Bc5 O-O d6 Bxc6+ bxc6")),
        ('br-d3-oonc3', 'Castle, then the knight', J(RL, "d3 Bc5 O-O d6 Nc3 h6")),
        ('br-d3-c3', 'Small c-pawn move', J(RL, "d3 Bc5 c3 O-O O-O d6"))],
  why='You played the bishop out against this in both of your games and won both.', outcome='Equal', tags=['game'])
L('br-nc3', 'br-quiet', 'Knight out: bishop out, castle', 'Same setup; one trick if White grabs your e-pawn', 'common',
  J(RL, "Nc3 Bc5 O-O O-O d3 d6"),
  alts=[('br-nc3-bxc6', 'Bishop takes your knight', J(RL, "Nc3 Bc5 Bxc6 dxc6 O-O Bg4")),
        ('br-nc3-bxc6e5', 'Bishop takes, knight grabs the pawn: bishop check, queen fork', J(RL, "Nc3 Bc5 Bxc6 dxc6 Nxe5 Bxf2+ Kxf2 Qd4+ Ke1 Qxe5")),
        ('br-nc3-d3', 'Small d-pawn, then the pin', J(RL, "Nc3 Bc5 d3 O-O Bg5 h6")),
        ('br-nc3-d3oo', 'Small d-pawn, then castle', J(RL, "Nc3 Bc5 d3 O-O O-O d6")),
        ('br-nc3-ooxc6', 'Castle, then bishop takes', J(RL, "Nc3 Bc5 O-O O-O Bxc6 dxc6")),
        ('br-nc3-re1', 'Castle, then the rook', J(RL, "Nc3 Bc5 O-O O-O Re1 d6")),
        ('br-nc3-h3', 'Edge pawn', J(RL, "Nc3 Bc5 h3 O-O")),
        ('br-nc3-nxe5', 'Knight grabs your e-pawn at once', J(RL, "Nc3 Bc5 Nxe5 Nxe5 d4 Bd6 dxe5 Bxe5"))],
  why='The Four Knights version of the Spanish. You won with this exact setup on Oct 31.', outcome='Equal')
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
SB = J(SC, "Nxd4 Bc5")   # the Classical Scotch: the bishop goes straight to its diagonal, as in the Italian
P('bs-scotch', 'scotch', 'Knight takes back', 'Scotch',
  'White trades in the center and takes back with the knight. Your bishop goes straight to its Italian diagonal and the queen joins it against f2.')
P('bs-gambits', 'scotch', 'White gives a pawn', 'Scotch gambits',
  'White leaves your extra pawn alone to develop fast. Develop with tempo and hit back in the center.')
P('bs-center', 'scotch', 'The d-pawn on move two', 'Center Game & Danish',
  'White pushes the d-pawn before the knight comes out. Take, then either kick the queen or decline the gambit with your own d-pawn.')

L('bs-classical', 'bs-scotch', 'Knight trade: the queen hits f2', 'Queen out with a mate threat, the d-pawn takes back, then castle long', 'core',
  J(SB, "Nxc6 Qf6 f3 dxc6 Nc3 Be6 Bd2 O-O-O"),
  alts=[('bs-classical-bd3', 'Bishop to the middle', J(SB, "Nxc6 Qf6 f3 dxc6 Nc3 Be6 Bd3 O-O-O")),
        ('bs-classical-qf3', 'Queen blocks: trade queens', J(SB, "Nxc6 Qf6 Qf3 dxc6 Qxf6 Nxf6 Nc3 Be6")),
        ('bs-classical-qe2', 'Queen guards f2', J(SB, "Nxc6 Qf6 Qe2 dxc6 Nc3 Be6")),
        ('bs-classical-e5', 'Queen guards, then the pawn kicks', J(SB, "Nxc6 Qf6 Qe2 dxc6 e5 Qg6")),
        ('bs-classical-qe2be3', 'Queen guards, then the bishop: grab the b-pawn', J(SB, "Nxc6 Qf6 Qe2 dxc6 Be3 Qxb2 Bxc5 Qxa1")),
        ('bs-classical-bxe3', 'Bishop blocks: trade it', J(SB, "Nxc6 Qf6 Be3 Bxe3 fxe3 dxc6")),
        ('bs-classical-na4', 'Knight hits your bishop', J(SB, "Nxc6 Qf6 f3 dxc6 Nc3 Be6 Na4 Bd6")),
        ('bs-classical-bc4', 'Bishop to the Italian diagonal: offer the trade', J(SB, "Nxc6 Qf6 f3 dxc6 Bc4 Be6")),
        ('bs-classical-qe5', 'Queens off, then the pawn kicks: jump forward', J(SB, "Nxc6 Qf6 Qf3 dxc6 Qxf6 Nxf6 e5 Ng4")),
        ('bs-classical-qbd3', 'Queens off, bishop to the middle', J(SB, "Nxc6 Qf6 Qf3 dxc6 Qxf6 Nxf6 Bd3 Be6"))],
  why='Over half of club players trade knights at once. Against maopfar and alwayssurrender31 your bishop checked first and then went back to this diagonal: a move lost. It goes there straight away.', outcome='Equal; your rook owns the open d-file', tags=['game', 'swap'])
L('bs-classical-be3', 'bs-scotch', 'Bishop guards the knight: castle', 'Queen out, the other knight behind it, castle; trade bishops if the knights come off', 'core',
  J(SB, "Be3 Qf6 c3 Nge7 Bc4 O-O O-O Bb6"),
  alts=[('bs-be3-b4', 'Pawn hits your bishop', J(SB, "Be3 Qf6 c3 Nge7 b4 Bb6")),
        ('bs-be3-be2', 'Bishop to the quiet square', J(SB, "Be3 Qf6 c3 Nge7 Be2 O-O")),
        ('bs-be3-bb5', 'Bishop hits your knight', J(SB, "Be3 Qf6 c3 Nge7 Bb5 O-O")),
        ('bs-be3-nd2', 'Knight to the middle', J(SB, "Be3 Qf6 c3 Nge7 Nd2 O-O")),
        ('bs-be3-nxc6', 'Knight trade: swap bishops first', J(SB, "Be3 Qf6 c3 Nge7 Nxc6 Bxe3 fxe3 Nxc6")),
        ('bs-be3-nxc6x', 'Knight trade at once', J(SB, "Be3 Qf6 Nxc6 Bxe3 fxe3 dxc6")),
        ('bs-be3-nc3', 'Knight out: the knight in the middle falls', J(SB, "Be3 Qf6 Nc3 Bxd4 Bxd4 Nxd4 Nd5 Qe5")),
        ('bs-be3-nc3d5', 'Knight out, then it jumps at once', J(SB, "Be3 Qf6 Nc3 Bxd4 Nd5 Qe5")),
        ('bs-be3-nxe7', 'Knight trade, then the knight grabs again: mate', J(SB, "Be3 Qf6 c3 Nge7 Nxc6 Bxe3 Nxe7 Qxf2#")),
        ('bs-be3-cnd2', 'Castled, then the knight to the middle: grab a pawn', J(SB, "Be3 Qf6 c3 Nge7 Bc4 O-O Nd2 Nxd4 cxd4 Bxd4"))],
  why='About three club players in ten guard the knight with the bishop. Six in ten then play the small c-pawn move, and the same calm setup answers everything.', outcome='Equal; everything is developed')
L('bs-classical-c3', 'bs-scotch', 'Small c-pawn: knight out', 'Knight hits the e-pawn; a bishop pin walks into the check on f2', 'common',
  J(SB, "c3 Nf6 Nxc6 bxc6 Bd3 d5"),
  alts=[('bs-c3-e5', 'Pawn hits your knight: pin it', J(SB, "c3 Nf6 Nxc6 bxc6 e5 Qe7")),
        ('bs-c3-bg5', 'Knight trade, then the pin: check on f2', J(SB, "c3 Nf6 Nxc6 bxc6 Bg5 Bxf2+ Kxf2 Nxe4+ Kg1 Qxg5")),
        ('bs-c3-bg5ke1', 'Check on f2, king goes home', J(SB, "c3 Nf6 Nxc6 bxc6 Bg5 Bxf2+ Kxf2 Nxe4+ Ke1 Qxg5")),
        ('bs-c3-bg5ke2', 'Check on f2, king steps up', J(SB, "c3 Nf6 Nxc6 bxc6 Bg5 Bxf2+ Ke2 Bb6")),
        ('bs-c3-bd3', 'Bishop guards the e-pawn', J(SB, "c3 Nf6 Bd3 O-O")),
        ('bs-c3-f3', 'Pawn guards the e-pawn', J(SB, "c3 Nf6 f3 d5")),
        ('bs-c3-pinbxf6', 'Pin, then the bishop takes: the knight in the middle falls', J(SB, "c3 Nf6 Bg5 O-O Bxf6 Qxf6")),
        ('bs-c3-pin', 'Bishop pins first: castle', J(SB, "c3 Nf6 Bg5 O-O")),
        ('bs-c3-pinx', 'Pin, then the knight trade: check on f2 first', J(SB, "c3 Nf6 Bg5 O-O Nxc6 Bxf2+ Kxf2 Nxe4+ Ke1 Qxg5"))],
  why='The pawn guards the knight, but it costs White a move. Hit the e-pawn at once.', outcome='You are better')
L('bs-classical-nb3', 'bs-scotch', 'Knight steps back: so does the bishop', 'Bishop back out of reach, knight out, castle', 'common',
  J(SB, "Nb3 Bb6 Nc3 Nf6 Bg5 h6 Bh4 O-O"),
  alts=[('bs-nb3-bxf6', 'Pin, then the bishop takes', J(SB, "Nb3 Bb6 Nc3 Nf6 Bg5 h6 Bxf6 Qxf6")),
        ('bs-nb3-bd3', 'Bishop to the middle', J(SB, "Nb3 Bb6 Nc3 Nf6 Bd3 O-O")),
        ('bs-nb3-bc4', 'Bishop to the Italian diagonal', J(SB, "Nb3 Bb6 Bc4 Nf6")),
        ('bs-nb3-bd3x', 'Bishop to the middle at once', J(SB, "Nb3 Bb6 Bd3 Nf6"))],
  why='The knight hits your bishop, so it steps back to safety and keeps its aim at f2.', outcome='Equal')

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
  why='Twice the c-pawn capture let White\'s bishop take on f7 and the queen win your bishop back with check: against themobun (2050) in July and trijhg on Oct 31. Developing the knight keeps it simple.', outcome='Equal', tags=['game'])
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
        ('bs-center-bb5', 'Bishop hits your knight', J(E, "d4 exd4 Qxd4 Nc6 Qe3 Nf6 Bb5 Be7"))],
  why='At your level more than half of White players who push the d-pawn take back with the queen.', outcome='You are ahead in development')
L('bs-danish', 'bs-center', 'The Danish: hit back with the d-pawn', 'Don\'t take the second pawn; strike the center instead', 'core',
  J(E, "d4 exd4 c3 d5 exd5 Qxd5 cxd4 Nc6 Nf3 Bg4 Be2 Bb4+"),
  alts=[('bs-danish-qxd4', 'Queen takes back', J(E, "d4 exd4 c3 d5 exd5 Qxd5 Qxd4 Qxd4 cxd4 Nc6")),
        ('bs-danish-nf3', 'Knight out first', J(E, "d4 exd4 c3 d5 exd5 Qxd5 Nf3 Nc6")),
        ('bs-danish-nc3', 'Knight hits your queen: take the pawn', J(E, "d4 exd4 c3 d5 exd5 Qxd5 cxd4 Nc6 Nc3 Qxd4")),
        ('bs-danish-e5', 'Pawn pushes past', J(E, "d4 exd4 c3 d5 e5 dxc3 Nxc3 d4")),
        ('bs-danish-cxd4', 'Pawn takes back', J(E, "d4 exd4 c3 d5 cxd4 dxe4")),
        ('bs-danish-be3', 'Bishop guards the pawn', J(E, "d4 exd4 c3 d5 exd5 Qxd5 cxd4 Nc6 Be3 Bb4+"))],
  why='Three times you took the second pawn and twice White\'s pieces came out fast and won: against yonatha32 in October and abodeh7 on Nov 1. The d-pawn strike turns the gambit off.', outcome='Equal; White\'s center pawn is isolated', tags=['game', 'swap'])
L('bs-d4move', 'bs-center', 'Other third moves', 'Knight out: back in the Scotch, bishop out at once', 'common',
  J(E, "d4 exd4 Nf3 Nc6 Nxd4 Bc5"),
  alts=[('bs-d4move-bc4', 'Bishop out', J(E, "d4 exd4 Bc4 Nf6 e5 d5")),
        ('bs-d4move-bc4n', 'Bishop out, then the knight', J(E, "d4 exd4 Bc4 Nf6 Nf3 Nxe4")),
        ('bs-d4move-nf3bc4', 'Knight out, then the bishop', J(E, "d4 exd4 Nf3 Nc6 Bc4 Bc5 c3 Nf6"))],
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

L('bv-spanish', 'bv-4n', 'The Spanish bishop: you are in your Spanish lesson', 'The same position as your Spanish lesson: bishop out, castle, small d-pawn', 'core',
  J(FK, "Bb5 Bc5 O-O O-O d3 d6"),
  alts=[('bv-spanish-bxc6', 'Bishop takes your knight', J(FK, "Bb5 Bc5 Bxc6 dxc6 O-O Bg4")),
        ('bv-spanish-fork', 'Bishop takes, knight grabs the pawn: bishop check, queen fork', J(FK, "Bb5 Bc5 Bxc6 dxc6 Nxe5 Bxf2+ Kxf2 Qd4+ Ke1 Qxe5")),
        ('bv-spanish-ooxc6', 'Both castle, then the bishop takes', J(FK, "Bb5 Bc5 O-O O-O Bxc6 dxc6")),
        ('bv-spanish-d3', 'Pawn guards first', J(FK, "Bb5 Bc5 d3 O-O O-O d6")),
        ('bv-spanish-d3bg5', 'Pawn guards, then the pin', J(FK, "Bb5 Bc5 d3 O-O Bg5 h6")),
        ('bv-spanish-nxe5', 'Knight grabs your e-pawn at once', J(FK, "Bb5 Bc5 Nxe5 Nxe5 d4 Bd6 dxe5 Bxe5"))],
  why='The Spanish Four Knights is the Spanish with the knights out first. Your bishop goes to the same diagonal as always.', outcome='Equal')
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

L('bv-bc5', 'bv-vienna', 'Bishop out: knights first, then yours', 'Knight out, then your bishop to its diagonal, then the small d-pawn', 'core',
  J(VI, "Bc4 Nf6 d3 Bc5 Bg5 h6 Bh4 d6"),
  alts=[('bv-bc5-bxf6', 'Bishop takes your knight', J(VI, "Bc4 Nf6 d3 Bc5 Bg5 h6 Bxf6 Qxf6")),
        ('bv-bc5-nf3', 'Knight out: your Italian setup', J(VI, "Bc4 Nf6 d3 Bc5 Nf3 d6")),
        ('bv-bc5-h3', 'Small h-pawn move: castle', J(VI, "Bc4 Nf6 d3 Bc5 h3 O-O")),
        ('bv-bc5-be3', 'Bishop offers a trade: take it', J(VI, "Bc4 Nf6 d3 Bc5 Be3 Bxe3 fxe3 d6")),
        ('bv-bc5-f4', 'The f-pawn push', J(VI, "Bc4 Nf6 d3 Bc5 f4 d6 Nf3 Na5")),
        ('bv-bc5-f4x', 'The f-pawn push, then it takes', J(VI, "Bc4 Nf6 d3 Bc5 f4 d6 fxe5 dxe5")),
        ('bv-bc5-f5', 'The f-pawn rushes past', J(VI, "Bc4 Nf6 d3 Bc5 f4 d6 f5 Nd4")),
        ('bv-bc4-nf3', 'Knight out at once: the Four Knights', J(VI, "Bc4 Nf6 Nf3 Bc5 d3 d6")),
        ('bv-bc4-qf3', 'Queen comes out: jump into the center', J(VI, "Bc4 Nf6 Qf3 Nd4 Qd1 c6")),
        ('bv-bc4-qd3', 'Queen out, then to the middle', J(VI, "Bc4 Nf6 Qf3 Nd4 Qd3 c6")),
        ('bv-bc4-qf3g3', 'Queen out, then to the side: the fork', J(VI, "Bc4 Nf6 Qf3 Nd4 Qg3 Nxc2+"))],
  why='Against irekmary in July your bishop came out first and White\'s queen hit your g-pawn on move four. With the knight out first, the queen can\'t come, and then the bishop goes to its usual diagonal.', outcome='Equal; the same setup as your Italian', tags=['game', 'swap'])
L('bv-f4bc5', 'bv-vienna', 'The Vienna Gambit: bishop out, don\'t take', 'Bishop to its diagonal, small d-pawn, knight out, then the knight jumps at the Italian bishop', 'core',
  J(VI, "f4 Bc5 Nf3 d6 Bc4 Nf6 d3 Na5"),
  alts=[('bv-f4bc5-fxe5', 'Bishop out, then the pawn takes', J(VI, "f4 Bc5 Nf3 d6 Bc4 Nf6 fxe5 dxe5")),
        ('bv-f4bc5-ng5', 'Knight jumps at f7: castle', J(VI, "f4 Bc5 Nf3 d6 Bc4 Nf6 Ng5 O-O")),
        ('bv-f4bc5-xd3', 'Pawn takes, then the small d-pawn', J(VI, "f4 Bc5 Nf3 d6 fxe5 dxe5 d3 Nf6")),
        ('bv-f4bc5-x', 'Pawn takes: take back', J(VI, "f4 Bc5 Nf3 d6 fxe5 dxe5 Bc4 Nf6")),
        ('bv-f4bc5-bb5x', 'Pawn takes, then the pin', J(VI, "f4 Bc5 Nf3 d6 fxe5 dxe5 Bb5 Ne7")),
        ('bv-f4bc5-bb5', 'Bishop pins your knight', J(VI, "f4 Bc5 Nf3 d6 Bb5 Ne7")),
        ('bv-f4bc5-d3', 'Small d-pawn move', J(VI, "f4 Bc5 Nf3 d6 d3 a6")),
        ('bv-f4bc5-at', 'Pawn takes at once', J(VI, "f4 Bc5 fxe5 d6 exd6 Qxd6")),
        ('bv-f4bc5-atn', 'Pawn takes, then the knight', J(VI, "f4 Bc5 fxe5 d6 Nf3 dxe5"))],
  why='Three Vienna gambits, one win. Against Skrammande the bishop came out as here, then your own f-pawn push opened your king. Keep to the setup: bishop, small d-pawn, knight out, castle. White\'s king can\'t castle short while your bishop eyes it.', outcome='Equal; White\'s king has nowhere safe to go', tags=['game', 'swap'])
L('bv-vmisc', 'bv-vienna', 'Other Vienna moves', 'Knight out and take the center', 'common',
  J(VI, "Nf3 Nf6 Bb5 Bc5"),
  alts=[('bv-vmisc-d4', 'Knight out, then the center push', J(VI, "Nf3 Nf6 d4 exd4 Nxd4 Bb4")),
        ('bv-vmisc-bc4', 'Knight out, then the Italian bishop', J(VI, "Nf3 Nf6 Bc4 Bc5 d3 d6")),
        ('bv-vmisc-bb5', 'Spanish bishop first', J(VI, "Bb5 Nf6 Nf3 Bc5")),
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
        ('ba-qf3', 'Queen to the other side', J(E, "Qf3 Nc6 Bc4 Nf6 c3 Na5")),
        ('ba-qf3-d3', 'Queen out, then the d-pawn', J(E, "Qf3 Nc6 Bc4 Nf6 d3 Nd4")),
        ('ba-qf3-ne2', 'Queen out, then the knight', J(E, "Qf3 Nc6 Bc4 Nf6 Ne2 Na5")),
        ('ba-qf3-g4', 'Queen out, then the pawn storm', J(E, "Qf3 Nc6 Bc4 Nf6 g4 Nd4"))],
  why='Early queen moves come up a few times in every hundred games at your level.', outcome='You are better')
L('ba-kgd', 'ba-kg', 'Bishop out, don\'t take', 'Bishop to its diagonal stops White castling; small d-pawn, both knights out, then the knight jumps at White\'s bishop', 'core',
  J(E, "f4 Bc5 Nf3 d6 Bc4 Nf6 Nc3 Nc6 d3 Na5"),
  alts=[('ba-kgd-d3', 'Small d-pawn move', J(E, "f4 Bc5 Nf3 d6 Bc4 Nf6 d3 Nc6 Nc3 Na5")),
        ('ba-kgd-d3c3', 'Small d-pawn, then the small c-pawn: castle', J(E, "f4 Bc5 Nf3 d6 Bc4 Nf6 d3 Nc6 c3 O-O")),
        ('ba-kgd-bx', 'Bishop out, then the pawn takes', J(E, "f4 Bc5 Nf3 d6 Bc4 Nf6 fxe5 dxe5")),
        ('ba-kgd-fxe5', 'Pawn takes, then the bishop', J(E, "f4 Bc5 Nf3 d6 fxe5 dxe5 Bc4 Nf6")),
        ('ba-kgd-nxe5', 'Pawn takes, knight grabs: the queen check', J(E, "f4 Bc5 Nf3 d6 fxe5 dxe5 Nxe5 Qh4+ g3 Qxe4+ Qe2 Qxh1")),
        ('ba-kgd-d4', 'Center push: take it', J(E, "f4 Bc5 Nf3 d6 d4 exd4")),
        ('ba-kgd-c3', 'Small c-pawn move', J(E, "f4 Bc5 Nf3 d6 c3 Nf6")),
        ('ba-kgd-nc3', 'Knight out', J(E, "f4 Bc5 Nf3 d6 Nc3 Nf6")),
        ('ba-kgd-grab', 'Pawn grabs at once: the queen check', J(E, "f4 Bc5 fxe5 Qh4+ g3 Qxe4+ Qe2 Qxh1")),
        ('ba-kgd-grabne2', 'Pawn grabs, then the knight blocks', J(E, "f4 Bc5 fxe5 Qh4+ g3 Qxe4+ Ne2 Qxh1")),
        ('ba-kgd-grabbe2', 'Pawn grabs, then the bishop blocks', J(E, "f4 Bc5 fxe5 Qh4+ g3 Qxe4+ Be2 Qxh1")),
        ('ba-kgd-grabke2', 'Pawn grabs, king steps up: mate', J(E, "f4 Bc5 fxe5 Qh4+ Ke2 Qxe4#")),
        ('ba-kgd-nke2', 'Knight grabs, king steps up: mate', J(E, "f4 Bc5 Nf3 d6 fxe5 dxe5 Nxe5 Qh4+ Ke2 Qxe4#")),
        ('ba-kgd-nbe2', 'Knight grabs, then the bishop blocks', J(E, "f4 Bc5 Nf3 d6 fxe5 dxe5 Nxe5 Qh4+ g3 Qxe4+ Be2 Qxh1"))],
  why='Three King\'s Gambits, one win: against TiepiMT the knight went behind the pawns and you lost on time, and against tbergosmede on Nov 1 your knight went back home on move three. The bishop on its usual diagonal keeps White\'s king in the middle, and if the pawn grabs your e-pawn, the queen check wins a rook.', outcome='Equal; White can\'t castle short', tags=['game', 'swap'])
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
        ('ba-bc4-nc3', 'Knight out: back in the Vienna', J(E, "Bc4 Nc6 Nc3 Nf6 d3 Bc5")),
        ('ba-bc4-nc3nf3', 'Both knights out: the Four Knights', J(E, "Bc4 Nc6 Nc3 Nf6 Nf3 Bc5")),
        ('ba-bc4-nf3nc3', 'Knight out, then the other knight', J(E, "Bc4 Nc6 Nf3 Bc5 Nc3 Nf6"))],
  why='Four of your games started this way, three of them against JChav3z on Oct 29. The two losses came after an early edge-pawn move; knight out, then the bishop, won. Most move orders lead back to the Italian or the Vienna.', outcome='Equal', tags=['game'])

# ============================================================== OTHER FIRST MOVES
P('bo-english', 'other', 'The c-pawn first', 'English',
  'White starts with the c-pawn. Play the e-pawn two squares, as you would against the e-pawn, and develop the knights.')
P('bo-flank', 'other', 'Knight or fianchetto first', 'Réti & King\'s fianchetto',
  'Against the knight, use your Queen\'s Gambit setup; against the g-pawn fianchetto, take the center with the e-pawn.')
P('bo-rare', 'other', 'Rare first moves', 'Sidelines',
  'Small pawn moves and edge moves. Take the center and develop, and punish the ones that weaken White\'s king.')

L('bo-english', 'bo-english', 'E-pawn against the c-pawn', 'Knights out, bishop at the knight, then push the e-pawn', 'core',
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
  alts=[('bo-english2-e4', 'E-pawn two squares', J("c4 e5 e4 Nf6 d3 Bc5")),
        ('bo-english2-e3', 'Small e-pawn move', J("c4 e5 e3 Nf6")),
        ('bo-english2-d3', 'Small d-pawn move', J("c4 e5 d3 Nf6")),
        ('bo-english2-d4', 'Center push', J("c4 e5 d4 exd4 Qxd4 Nc6")),
        ('bo-english2-nf3', 'Knight hits your pawn: push past', J("c4 e5 Nf3 e4 Nd4 Nc6"))],
  why='The fianchetto is the next most common second move.', outcome='Equal')
L('bo-reti', 'bo-flank', 'Knight out first', 'D-pawn to the middle, then your Slav setup', 'core',
  J("Nf3 d5 g3 Nf6 Bg2 c6 O-O Bf5 d3 e6"),
  alts=[('bo-reti-d4', 'Center push: back in your d-pawn lines', J("Nf3 d5 d4 Nf6 Bf4 Bf5 e3 e6")),
        ('bo-reti-d4e3', 'Center push, then the small e-pawn', J("Nf3 d5 d4 Nf6 e3 Bf5 Bd3 Bxd3")),
        ('bo-reti-c4', 'The c-pawn: guard with yours', J("Nf3 d5 c4 c6 e3 Nf6 Nc3 Bf5")),
        ('bo-reti-cxd5', 'The c-pawn, then the pawn trade', J("Nf3 d5 c4 c6 cxd5 cxd5 d4 Nf6 Nc3 Nc6")),
        ('bo-reti-c4d4', 'The c-pawn, then the center push', J("Nf3 d5 c4 c6 d4 Nf6 e3 Bf5")),
        ('bo-reti-e3', 'Small e-pawn move', J("Nf3 d5 e3 Nf6 c4 c6")),
        ('bo-reti-b3', 'Queen\'s fianchetto', J("Nf3 d5 b3 Nf6 Bb2 Bf5"))],
  why='Against the king\'s knight first, the d-pawn goes to the middle and the same Slav setup follows.', outcome='Equal')
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
L('bo-f4', 'bo-rare', 'The f-pawn first', 'D-pawn two squares, knight out, then your bishop: the same setup as against the d-pawn', 'common',
  J("f4 d5 Nf3 Nf6 e3 Bf5 Be2 e6 O-O Bd6"),
  alts=[('bo-f4-d4', 'Center push', J("f4 d5 Nf3 Nf6 d4 Bf5")),
        ('bo-f4-g3', 'Fianchetto', J("f4 d5 Nf3 Nf6 g3 Bf5 Bg2 e6 O-O Be7")),
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
        ('bo-misc-d3', 'Small d-pawn move', J("d3 e5 e4 Nc6 Nf3 Nf6")),
        ('bo-misc-g4', 'The g-pawn lunge', J("g4 d5 Bg2 Bxg4")),
        ('bo-misc-edge', 'Edge pawn', J("a3 e5")),
        ('bo-misc-h3', 'Edge pawn on the king\'s side', J("h3 e5")),
        ('bo-misc-c3', 'Small c-pawn move', J("c3 e5"))],
  why='These come up once in a long while. Take the center and develop.', outcome='Equal or better')

import bslav  # noqa: E402,F401  the Slav setup against the d-pawn (registers its lessons)
import bsicilian  # noqa: E402,F401  the Sicilian with the small e-pawn and a-pawn moves (its own pack)
import bcaro  # noqa: E402,F401  the Caro-Kann: a second system against the e-pawn (its own pack)
