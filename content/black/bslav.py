"""Black against the d-pawn: the Slav setup. D-pawn two squares, c-pawn one, bishop out before the e-pawn,
e-pawn one, knights out, castle. Same picture against the Queen's Gambit, the London, the Colle and the rest.
SAN is internal only; notes live in bslav_notes.py."""
from bcontent import L, P, J

SD = "d4 d5"
SQ = J(SD, "c4 c6")              # Queen's Gambit: the Slav
SQN = J(SQ, "Nc3 Nf6")
SQF = J(SQ, "Nf3 Nf6")
SL = J(SD, "Bf4 Nf6 e3 Bf5")      # London
SN = J(SD, "Nf3 Nf6")
SC = J(SN, "e3 Bf5")             # Colle with your bishop already out
SJ = J(SD, "Nc3 Nf6")            # queen's knight first

# ============================================================== QUEEN'S GAMBIT: THE SLAV
P('bsl-quiet', 'slav', 'The small e-pawn move', 'Slow Slav',
  'White guards the c-pawn with the small e-pawn move. Your bishop comes out before your e-pawn, and the same pieces go to the same squares every game.')
P('bsl-knights', 'slav', 'Both knights out', 'Main line',
  'With both White knights out, your bishop cannot come out safely yet. Take the c-pawn first and hold it with the b-pawn; the bishop follows.')
P('bsl-exch', 'slav', 'White trades pawns', 'Exchange Slav',
  'White takes on your d-pawn. Take back with the c-pawn, put the queen\'s knight beside it and bring the bishop out again.')
P('bsl-bishop', 'slav', 'White\'s bishop comes out early', 'Bishop sorties',
  'White\'s dark bishop leaves before the e-pawn moves. Against the pin, jump the knight to the middle; against the long-diagonal bishop, take the c-pawn.')

L('bsl-slow', 'bsl-quiet', 'Small e-pawn: bishop out at once', 'Bishop out, e-pawn, knights, then trade White\'s bishop', 'core',
  J(SQ, "e3 Bf5 Nc3 e6 Nf3 Nd7 Bd3 Bxd3 Qxd3 Ngf6 O-O Bd6"),
  alts=[('bsl-slow-nf3', 'Knight out first', J(SQ, "e3 Bf5 Nf3 e6 Nc3 Nd7 Bd3 Bxd3 Qxd3 Ngf6")),
        ('bsl-slow-nf3bd3', 'Knight out, then the bishop', J(SQ, "e3 Bf5 Nf3 e6 Bd3 Bxd3 Qxd3 Nf6 O-O Nbd7")),
        ('bsl-slow-bd3', 'Bishop challenges yours at once: trade it', J(SQ, "e3 Bf5 Bd3 Bxd3 Qxd3 e6 Nf3 Nf6 O-O Nbd7")),
        ('bsl-slow-nc3bd3', 'Queen\'s knight, then the bishop', J(SQ, "e3 Bf5 Nc3 e6 Bd3 Bxd3 Qxd3 Nd7 Nf3 Ngf6")),
        ('bsl-slow-a3', 'Edge pawn', J(SQ, "e3 Bf5 Nc3 e6 a3 Nd7 Nf3 Ngf6")),
        ('bsl-slow-qb3', 'Queen hits your b-pawn: offer the queen trade', J(SQ, "e3 Bf5 Nc3 e6 Qb3 Qb6")),
        ('bsl-slow-cxd5', 'Pawn trade: take back with the c-pawn', J(SQ, "e3 Bf5 Nc3 e6 cxd5 cxd5 Nf3 Nc6"))],
  why='About one Queen\'s Gambit player in seven at your level guards the c-pawn with the small e-pawn move. Nothing stops your bishop.', outcome='Equal and solid')
L('bsl-slow2', 'bsl-quiet', 'Knights out, then the small e-pawn', 'Same setup; trade White\'s bishop when it comes to the middle', 'core',
  J(SQF, "e3 Bf5 Nc3 e6 Bd3 Bxd3 Qxd3 Nbd7 O-O Bb4"),
  alts=[('bsl-slow2-be2', 'Bishop to the quiet square', J(SQF, "e3 Bf5 Nc3 e6 Be2 Nbd7 O-O Be7")),
        ('bsl-slow2-a3', 'Edge pawn', J(SQF, "e3 Bf5 Nc3 e6 a3 Nbd7 Bd3 Bxd3 Qxd3 Bd6")),
        ('bsl-slow2-cxd5', 'Pawn trade: take back with the e-pawn', J(SQF, "e3 Bf5 Nc3 e6 cxd5 exd5 Bd3 Bxd3 Qxd3 Bd6")),
        ('bsl-slow2-qb3', 'Queen hits your b-pawn: offer the queen trade', J(SQF, "e3 Bf5 Nc3 e6 Qb3 Qb6")),
        ('bsl-slow2-bd3', 'Bishop out before the queen\'s knight', J(SQF, "e3 Bf5 Bd3 Bxd3 Qxd3 e6 O-O Nbd7 Nc3 Bd6")),
        ('bsl-slow2-nc3', 'Queen\'s knight first, then the small e-pawn', J(SQN, "e3 Bf5 Nf3 e6 Bd3 Bxd3 Qxd3 Nbd7 O-O Bd6")),
        ('bsl-slow2-nc3e2', 'Queen\'s knight, then the quiet bishop', J(SQN, "e3 Bf5 Nf3 e6 Be2 Nbd7 O-O Bd6")),
        ('bsl-slow2-nc3x', 'Queen\'s knight, then the pawn trade', J(SQN, "e3 Bf5 cxd5 cxd5 Qb3 Bc8 Nf3 e6")),
        ('bsl-slow2-nc3bd3', 'Queen\'s knight, then the bishop at once', J(SQN, "e3 Bf5 Bd3 Bxd3 Qxd3 e6 Nf3 Nbd7")),
        ('bsl-slow2-sn', 'King\'s knight before the c-pawn', J(SN, "c4 c6 e3 Bf5 Nc3 e6 Bd3 Bxd3 Qxd3 Nbd7"))],
  why='The most common way White reaches the small e-pawn position. Every piece goes where it went in the first lesson.', outcome='Equal')

L('bsl-main', 'bsl-knights', 'Both knights out: take the c-pawn', 'Take, hold it with the b-pawn, and grab the e-pawn if the knight runs to the edge', 'common',
  J(SQN, "Nf3 dxc4 e4 b5 a4 b4 Na2 Nxe4 Bxc4 e6"),
  alts=[('bsl-main-e5', 'Pawn hits your knight: jump to the middle', J(SQN, "Nf3 dxc4 e4 b5 e5 Nd5 Be2 Bf5")),
        ('bsl-main-e5x', 'Pawn hits your knight, then knight takes knight', J(SQN, "Nf3 dxc4 e4 b5 e5 Nd5 Nxd5 cxd5")),
        ('bsl-main-e5a4', 'Pawn hits your knight, then the edge pawn', J(SQN, "Nf3 dxc4 e4 b5 e5 Nd5 a4 e6")),
        ('bsl-main-e3', 'Small e-pawn: hold the extra pawn', J(SQN, "Nf3 dxc4 e3 b5 a4 b4 Na2 e6 Bxc4 Bb7")),
        ('bsl-main-e3nb1', 'Small e-pawn, knight goes home', J(SQN, "Nf3 dxc4 e3 b5 a4 b4 Nb1 Ba6")),
        ('bsl-main-e3ne2', 'Small e-pawn, knight to the quiet square', J(SQN, "Nf3 dxc4 e3 b5 a4 b4 Ne2 e6")),
        ('bsl-main-a4', 'Edge pawn first: now the bishop comes out', J(SQN, "Nf3 dxc4 a4 Bf5 e3 e6 Bxc4 Bb4 O-O O-O")),
        ('bsl-main-bg5', 'Bishop pins your knight', J(SQN, "Nf3 dxc4 Bg5 h6 Bxf6 exf6 e3 b5")),
        ('bsl-main-bg5h4', 'Bishop pins, then steps back', J(SQN, "Nf3 dxc4 Bg5 h6 Bh4 b5")),
        ('bsl-main-nf3', 'King\'s knight first', J(SQF, "Nc3 dxc4 e4 b5 a4 b4 Na2 Nxe4"))],
  why='The main line of the Slav. Three in four players at your level push the e-pawn here instead of the edge pawn; then your b-pawn holds the extra pawn.', outcome='Equal; often a pawn up')

L('bsl-exch', 'bsl-exch', 'Pawn trade: knight beside the d-pawn', 'Take back with the c-pawn, knight to its square, bishop out', 'core',
  J(SQ, "cxd5 cxd5 Nc3 Nf6 Bf4 Nc6 e3 Bf5 Nf3 e6"),
  alts=[('bsl-exch-nb5', 'Knight jumps next to your c-pawn square: hit back', J(SQ, "cxd5 cxd5 Nc3 Nf6 Bf4 Nc6 Nb5 e5")),
        ('bsl-exch-nf3', 'Knight out before the bishop', J(SQ, "cxd5 cxd5 Nc3 Nf6 Nf3 Nc6 Bf4 Bf5 e3 e6")),
        ('bsl-exch-nf3b', 'Bishop, then the king\'s knight', J(SQ, "cxd5 cxd5 Nc3 Nf6 Bf4 Nc6 Nf3 Bf5 e3 e6")),
        ('bsl-exch-bg5', 'Bishop pins your knight: jump, then the queen check', J(SQ, "cxd5 cxd5 Nc3 Nf6 Bg5 Ne4 Nxe4 dxe4 e3 Qa5+")),
        ('bsl-exch-bg5f4', 'Bishop pins, then steps back', J(SQ, "cxd5 cxd5 Nc3 Nf6 Bg5 Ne4 Bf4 Nc6")),
        ('bsl-exch-e3', 'Small e-pawn move', J(SQ, "cxd5 cxd5 Nc3 Nf6 e3 Nc6 Nf3 Bf5")),
        ('bsl-exch-nf3first', 'King\'s knight first', J(SQ, "cxd5 cxd5 Nf3 Nf6 Nc3 Nc6 Bf4 Bf5")),
        ('bsl-exch-e3first', 'Small e-pawn first', J(SQ, "cxd5 cxd5 e3 Nc6 Nc3 Nf6 Nf3 Bf5")),
        ('bsl-exch-late', 'Knight out, then the trade', J(SQN, "cxd5 cxd5 Bf4 Nc6 e3 Bf5 Nf3 e6"))],
  why='About one in ten Queen\'s Gambit players trade at once. The position is symmetrical, your pieces copy White\'s, and the game stays calm.', outcome='Equal')

L('bsl-pin', 'bsl-bishop', 'Bishop pins your knight: jump to the middle', 'Knight jump; if White moves the e-pawn, the queen check wins the bishop', 'common',
  J(SQN, "Bg5 Ne4 Nxe4 dxe4 e3 Qa5+ Qd2 Qxg5"),
  alts=[('bsl-pin-qc2', 'Queen attacks your pawn: take the d-pawn', J(SQN, "Bg5 Ne4 Nxe4 dxe4 Qc2 Qxd4")),
        ('bsl-pin-bf4', 'Bishop steps back to the long diagonal', J(SQN, "Bg5 Ne4 Bf4 Nxc3 bxc3 dxc4")),
        ('bsl-pin-bh4', 'Bishop steps back on the pin line', J(SQN, "Bg5 Ne4 Bh4 Nxc3 bxc3 dxc4")),
        ('bsl-pin-nf3', 'King\'s knight first, then the pin', J(SQF, "Bg5 Ne4 Bf4 dxc4")),
        ('bsl-pin-nf3h4', 'King\'s knight, pin, then the bishop steps back', J(SQF, "Bg5 Ne4 Bh4 dxc4")),
        ('bsl-pin-nf3e3', 'King\'s knight, pin, then the small e-pawn', J(SQF, "Bg5 Ne4 e3 Nxg5 Nxg5 dxc4"))],
  why='A quarter of club players pin your knight here, and three in four of them then play the natural e-pawn move that loses the bishop.', outcome='Equal, often a piece up')
L('bsl-bf4', 'bsl-bishop', 'Bishop to the long diagonal: take the c-pawn', 'Take, hold it with the b-pawn, then the e-pawn', 'common',
  J(SQN, "Bf4 dxc4 e3 b5 a4 Qb6 Nf3 e6"),
  alts=[('bsl-bf4-nf3', 'King\'s knight instead of the edge pawn', J(SQN, "Bf4 dxc4 e3 b5 Nf3 e6")),
        ('bsl-bf4-e4', 'Big e-pawn', J(SQN, "Bf4 dxc4 e4 b5 Nf3 e6")),
        ('bsl-bf4-kn', 'King\'s knight first', J(SQF, "Bf4 dxc4 e3 b5 a4 e6")),
        ('bsl-bf4-knc3', 'King\'s knight, then the queen\'s knight: jump to the middle', J(SQF, "Bf4 dxc4 Nc3 Nd5 Bg3 Nxc3 bxc3 e6")),
        ('bsl-bf4-knx', 'Knight takes your knight', J(SQF, "Bf4 dxc4 Nc3 Nd5 Nxd5 cxd5"))],
  why='Once White\'s dark bishop has left, your queen and knight can hit the squares it no longer guards. Take the c-pawn.', outcome='Equal, often a pawn up')

# ============================================================== LONDON SYSTEM
P('bln-main', 'london', 'Bishop out before the e-pawn', 'London System',
  'White\'s bishop comes out first. Yours comes out too, then the e-pawn, and your dark bishop offers to trade off the London bishop.')
P('bln-jobava', 'london', 'The knight joins the bishop', 'Jobava London',
  'White adds the queen\'s knight beside the bishop. One trick to know: the knight jump at your c-pawn.')

L('bln-main', 'bln-main', 'Copy the bishop', 'Bishop out, e-pawn, trade White\'s other bishop, then offer the dark one', 'core',
  J(SL, "Nf3 e6 Bd3 Bxd3 Qxd3 Bd6 Bxd6 Qxd6 O-O O-O"),
  alts=[('bln-main-cxd3', 'Pawn takes back', J(SL, "Nf3 e6 Bd3 Bxd3 cxd3 Bd6 Bxd6 Qxd6")),
        ('bln-main-bg3', 'London bishop steps back', J(SL, "Nf3 e6 Bd3 Bxd3 Qxd3 Bd6 Bg3 O-O")),
        ('bln-main-ne5', 'Knight jumps forward', J(SL, "Nf3 e6 Bd3 Bxd3 Qxd3 Bd6 Ne5 Nbd7")),
        ('bln-main-nbd2', 'Knight to the quiet square', J(SL, "Nf3 e6 Nbd2 Bd6 Bxd6 cxd6")),
        ('bln-main-c3', 'Small c-pawn move', J(SL, "Nf3 e6 c3 Bd6 Bxd6 Qxd6 Bd3 Bxd3 Qxd3 O-O")),
        ('bln-main-c4', 'The c-pawn push', J(SL, "Nf3 e6 c4 Bd6 Bxd6 cxd6 Nc3 O-O")),
        ('bln-main-h3', 'Edge pawn makes room for the bishop', J(SL, "Nf3 e6 h3 Bd6 Bxd6 Qxd6")),
        ('bln-main-be2', 'Bishop to the quiet square', J(SL, "Nf3 e6 Be2 Bd6 Bxd6 Qxd6")),
        ('bln-main-bd3', 'Bishop challenges yours at once: trade it', J(SL, "Bd3 Bxd3 Qxd3 e6 Nf3 Bd6")),
        ('bln-main-qb5', 'Queen check, then she grabs your b-pawn', J(SL, "Bd3 Bxd3 Qxd3 e6 Qb5+ Nbd7 Qxb7 Rb8 Qxa7 Rxb2")),
        ('bln-main-bd3c', 'Bishop challenges yours, pawn takes back', J(SL, "Bd3 Bxd3 cxd3 e6 Nf3 Bd6")),
        ('bln-main-c3b', 'Small c-pawn before the knight', J(SL, "c3 e6 Nf3 Bd6 Bxd6 Qxd6")),
        ('bln-main-nd2', 'Queen\'s knight first', J(SL, "Nd2 e6 Ngf3 Bd6 Bxd6 Qxd6")),
        ('bln-main-nf3b', 'Knight before the small e-pawn', J(SD, "Bf4 Nf6 Nf3 Bf5 e3 e6 Bd3 Bxd3 Qxd3 Bd6"))],
  why='Mirror White, trade both bishops, and the game is equal and calm. In July this setup beat a London player in fourteen moves.', outcome='Equal; nothing to fear', tags=['game'])
L('bln-c4', 'bln-main', 'The c-pawn push: pin the knight', 'E-pawn, then the bishop pins; one queen check to know', 'common',
  J(SL, "c4 e6 Nc3 Bb4 Nf3 O-O a3 Bxc3+ bxc3 c5"),
  alts=[('bln-c4-be2', 'Bishop to the quiet square', J(SL, "c4 e6 Nc3 Bb4 Nf3 O-O Be2 Ne4")),
        ('bln-c4-bd3', 'Bishop challenges yours', J(SL, "c4 e6 Nc3 Bb4 Nf3 O-O Bd3 Bxd3 Qxd3 c5")),
        ('bln-c4-qa4', 'Queen check: block with the knight', J(SL, "c4 e6 Nc3 Bb4 Qa4+ Nc6 cxd5 Nxd5")),
        ('bln-c4-qa4a3', 'Queen check, then the edge pawn', J(SL, "c4 e6 Nc3 Bb4 Qa4+ Nc6 a3 Bxc3+ bxc3 dxc4")),
        ('bln-c4-a3', 'Edge pawn asks your bishop: take the knight', J(SL, "c4 e6 Nc3 Bb4 a3 Bxc3+ bxc3 O-O")),
        ('bln-c4-qb3', 'Queen hits your b-pawn: knight out', J(SL, "c4 e6 Nc3 Bb4 Qb3 Nc6 a3 Bxc3+ bxc3 O-O")),
        ('bln-c4-qb3first', 'Queen out before the knight: let her take', J(SL, "c4 e6 Qb3 Nc6 Qxb7 Nb4 Na3 dxc4")),
        ('bln-c4-qb3n', 'Queen out, then the knight', J(SL, "c4 e6 Qb3 Nc6 Nc3 Bb4")),
        ('bln-c4-cxd5', 'Pawn trade: knight takes back', J(SL, "c4 e6 cxd5 Nxd5 Bg3 Nb4 Na3 c5")),
        ('bln-c4-cxd5q', 'Pawn trade, then the queen check', J(SL, "c4 e6 cxd5 Nxd5 Bg3 Nb4 Qa4+ N8c6")),
        ('bln-c4-c5', 'Pawn pushes past', J(SL, "c4 e6 c5 Be7")),
        ('bln-c4-nf3', 'Knight out before the queen\'s knight', J(SL, "c4 e6 Nf3 Bd6 Bxd6 cxd6 Nc3 O-O"))],
  why='About one London player in ten pushes the c-pawn early. The pin is fine, but the queen check on the edge needs the right block.', outcome='Equal')
L('bln-nf3', 'bln-main', 'Knight out first', 'Same plan: bishop out, e-pawn, trade the bishops', 'core',
  J(SN, "Bf4 Bf5 e3 e6 Bd3 Bxd3 Qxd3 Bd6"),
  alts=[('bln-nf3-nbd2', 'Knight to the quiet square', J(SN, "Bf4 Bf5 e3 e6 Nbd2 Bd6 Bxd6 cxd6")),
        ('bln-nf3-c4', 'The c-pawn push', J(SN, "Bf4 Bf5 e3 e6 c4 Bb4+ Nc3 O-O")),
        ('bln-nf3-c3', 'Small c-pawn move', J(SN, "Bf4 Bf5 e3 e6 c3 Bd6 Bxd6 Qxd6")),
        ('bln-nf3-nc3', 'Queen\'s knight out', J(SN, "Bf4 Bf5 Nc3 e6 e3 Bb4")),
        ('bln-nf3-nb5', 'Queen\'s knight jumps at your c-pawn', J(SN, "Bf4 Bf5 Nc3 e6 Nb5 Na6")),
        ('bln-nf3-h3', 'Edge pawn', J(SN, "Bf4 Bf5 e3 e6 h3 Bd6"))],
  why='A fifth of London players bring the knight out first. Same squares for every piece.', outcome='Equal')
L('bln-jobava', 'bln-jobava', 'Knight in front of the c-pawn', 'Same setup; when the knight jumps at your c-pawn, guard it from the edge', 'common',
  J(SJ, "Bf4 Bf5 e3 e6 Nf3 c6 Bd3 Bxd3 Qxd3 Nbd7"),
  alts=[('bln-jobava-nb5', 'Knight jumps at your c-pawn', J(SJ, "Bf4 Bf5 Nb5 Na6 e3 e6 Nf3 c6 Nc3 Qb6")),
        ('bln-jobava-nb5b', 'Knight jumps after the e-pawn move', J(SJ, "Bf4 Bf5 e3 e6 Nb5 Na6 Nf3 c6 Nc3 Qb6")),
        ('bln-jobava-bd3', 'Bishop challenges yours: trade it', J(SJ, "Bf4 Bf5 e3 e6 Bd3 Bxd3 Qxd3 c6")),
        ('bln-jobava-nf3', 'King\'s knight out', J(SJ, "Bf4 Bf5 Nf3 e6 e3 c6")),
        ('bln-jobava-f3', 'Small f-pawn: the e-pawn push is coming', J(SJ, "Bf4 Bf5 f3 e6 e4 dxe4 fxe4 Bg6")),
        ('bln-jobava-nf3b', 'King\'s knight before the bishop', J(SJ, "Nf3 Bf5 Bf4 e6 e3 c6")),
        ('bln-jobava-bf4', 'Bishop first, then the queen\'s knight', J(SD, "Bf4 Nf6 Nc3 Bf5 e3 e6 Nb5 Na6")),
        ('bln-jobava-bf4nb5', 'Bishop, queen\'s knight, then the jump at once', J(SD, "Bf4 Nf6 Nc3 Bf5 Nb5 Na6 e3 e6"))],
  why='A third of club players jump the knight at your c-pawn the very next move. Guard it with the knight from the edge.', outcome='Equal')

# ============================================================== OTHER D-PAWN SYSTEMS
P('bdx-colle', 'd4x', 'Small e-pawn systems', 'Colle',
  'White builds a quiet pawn triangle and aims the bishop at your king. Get your bishop out first, trade it, then hit the center with the c-pawn.')
P('bdx-pins', 'd4x', 'Bishop pins your knight', 'Torre & Veresov',
  'White pins your knight early. Jump it forward, or take back with the e-pawn if White takes it.')
P('bdx-gambits', 'd4x', 'E-pawn gambits', 'Blackmar-Diemer',
  'White offers the e-pawn to open lines. Take it, develop, and give back nothing.')
P('bdx-misc', 'd4x', 'Odd second moves', 'Sidelines',
  'Rare moves. Same setup.')

L('bdx-colle', 'bdx-colle', 'Bishop out before White\'s bishop', 'Trade bishops, then the c-pawn hits the center', 'core',
  J(SC, "Bd3 Bxd3 Qxd3 e6 O-O c5 c3 Nc6"),
  alts=[('bdx-colle-cxd3', 'Pawn takes back', J(SC, "Bd3 Bxd3 cxd3 e6 O-O c5")),
        ('bdx-colle-dxc5', 'Pawn takes your c-pawn', J(SC, "Bd3 Bxd3 Qxd3 e6 O-O c5 dxc5 Bxc5")),
        ('bdx-colle-qb5', 'Queen check', J(SC, "Bd3 Bxd3 Qxd3 e6 O-O c5 Qb5+ Qd7")),
        ('bdx-colle-c4', 'The c-pawn push: back in the Slav', J(SC, "c4 c6 Nc3 e6 Bd3 Bxd3 Qxd3 Nbd7")),
        ('bdx-colle-c4qb3', 'C-pawn push, then the queen hits your b-pawn', J(SC, "c4 c6 Nc3 e6 Qb3 Qb6")),
        ('bdx-colle-nc3', 'Queen\'s knight out', J(SC, "Nc3 e6 Bd3 Bxd3 Qxd3 c5")),
        ('bdx-colle-be2', 'Bishop to the quiet square', J(SC, "Be2 e6 O-O Bd6")),
        ('bdx-colle-nbd2', 'Knight to the quiet square', J(SC, "Nbd2 e6 Bd3 Bxd3 cxd3 c5")),
        ('bdx-colle-c3', 'Small c-pawn move', J(SC, "c3 e6 Bd3 Bxd3 Qxd3 c5")),
        ('bdx-colle-e3', 'Small e-pawn on move two: bishop out at once', J(SD, "e3 Bf5 Bd3 Bxd3 Qxd3 e6 Nf3 Nf6")),
        ('bdx-colle-e3nf3', 'Small e-pawn, then the knight', J(SD, "e3 Bf5 Nf3 e6 Bd3 Bxd3 Qxd3 Nf6")),
        ('bdx-colle-e3c4', 'Small e-pawn, then the c-pawn', J(SD, "e3 Bf5 c4 c6 Nc3 e6 Nf3 Nf6")),
        ('bdx-colle-nc3first', 'Queen\'s knight after the king\'s knight', J(SN, "Nc3 Bf5 Bf4 e6 e3 c6")),
        ('bdx-colle-g3', 'Fianchetto', J(SN, "g3 Bf5 Bg2 e6 O-O Be7"))],
  why='The Colle is the quiet system club players love. With your bishop out first, its best attacking piece gets traded.', outcome='Equal')
L('bdx-torre', 'bdx-pins', 'Knight out, then the pin', 'Jump the knight at the bishop, then bring your bishop out', 'common',
  J(SN, "Bg5 Ne4 Bf4 Bf5 e3 e6 Bd3 Bd6"),
  alts=[('bdx-torre-bh4', 'Bishop steps back on the pin line', J(SN, "Bg5 Ne4 Bh4 c5 e3 Nc6")),
        ('bdx-torre-e3', 'Small e-pawn: take the bishop', J(SN, "Bg5 Ne4 e3 Nxg5 Nxg5 e5")),
        ('bdx-torre-nbd2', 'Knight to the quiet square: take the bishop', J(SN, "Bg5 Ne4 Nbd2 Nxg5 Nxg5 e5")),
        ('bdx-torre-nc3', 'Queen\'s knight first, then the pin', J(SJ, "Nf3 Bf5 Bg5 Ne4 Nxe4 dxe4"))],
  why='About one club player in eight pins your knight after the king\'s knight comes out. The knight jump makes White decide at once.', outcome='Equal')
L('bdx-veresov', 'bdx-pins', 'Queen\'s knight out, then the pin', 'Bishop out; if White takes the knight, take back with the e-pawn', 'common',
  J(SJ, "Bg5 Bf5 Bxf6 exf6 e3 c6 Bd3 Bxd3 Qxd3 Bd6"),
  alts=[('bdx-veresov-nf3x', 'Takes your knight, then the king\'s knight', J(SJ, "Bg5 Bf5 Bxf6 exf6 Nf3 c6")),
        ('bdx-veresov-nf3', 'Knight out instead of taking', J(SJ, "Bg5 Bf5 Nf3 e6 e3 Be7")),
        ('bdx-veresov-e3', 'Small e-pawn instead of taking', J(SJ, "Bg5 Bf5 e3 e6 Bd3 Bxd3 Qxd3 Nbd7")),
        ('bdx-veresov-e3nf3', 'Small e-pawn, then the knight', J(SJ, "Bg5 Bf5 e3 e6 Nf3 Be7")),
        ('bdx-veresov-nf3first', 'King\'s knight before the pin', J(SJ, "Nf3 Bf5 e3 e6 Bd3 Bxd3 Qxd3 c5")),
        ('bdx-veresov-f3', 'Small f-pawn: hit the center with the c-pawn', J(SJ, "f3 c5 e4 e6 e5 Nfd7")),
        ('bdx-veresov-f3x', 'Small f-pawn, then pawn takes your c-pawn', J(SJ, "f3 c5 dxc5 e6")),
        ('bdx-veresov-f3e3', 'Small f-pawn, then the small e-pawn', J(SJ, "f3 c5 e3 Nc6"))],
  why='About one club player in five pins the knight here. Taking back with the e-pawn keeps your king safe and your dark bishop free.', outcome='Equal')
L('bdx-bdg', 'bdx-gambits', 'The e-pawn gambit', 'Take the pawn, bring the bishop out, keep the extra pawn or return it with a better game', 'common',
  J(SD, "e4 dxe4 Nc3 Nf6 f3 Bf5 fxe4 Nxe4 Qf3 Nxc3"),
  alts=[('bdx-bdg-g4', 'Pawn chases your bishop', J(SD, "e4 dxe4 Nc3 Nf6 f3 Bf5 g4 Bg6 g5 Nd5")),
        ('bdx-bdg-bg5', 'Bishop pins your knight', J(SD, "e4 dxe4 Nc3 Nf6 f3 Bf5 Bg5 Nbd7")),
        ('bdx-bdg-f3', 'Small f-pawn at once: hit back with the e-pawn', J(SD, "e4 dxe4 f3 e5 fxe4 Qh4+")),
        ('bdx-bdg-f3d5', 'Small f-pawn, then the d-pawn pushes', J(SD, "e4 dxe4 f3 e5 d5 Nf6")),
        ('bdx-bdg-f3dxe5', 'Small f-pawn, then pawn takes: trade queens', J(SD, "e4 dxe4 f3 e5 dxe5 Qxd1+ Kxd1 Nc6")),
        ('bdx-bdg-nc3', 'Queen\'s knight first, then the gambit', J(SJ, "e4 dxe4 f3 Bf5 fxe4 Nxe4")),
        ('bdx-bdg-nc3bg5', 'Queen\'s knight first, then the pin', J(SJ, "e4 dxe4 Bg5 Bf5 Bxf6 exf6"))],
  why='A rare gambit, but the players who use it play it every game. Taking and developing is all you need.', outcome='You are better')
L('bdx-misc', 'bdx-misc', 'Odd second moves', 'Same setup against everything', 'rare',
  J(SD, "g3 Nf6 Bg2 Bf5 Nf3 e6 O-O Be7"),
  alts=[('bdx-misc-c3', 'Small c-pawn move', J(SD, "c3 Nf6 Bf4 Bf5 e3 e6")),
        ('bdx-misc-f4', 'The f-pawn: Stonewall', J(SD, "f4 Nf6 Nf3 Bf5 e3 e6")),
        ('bdx-misc-nd2', 'Queen\'s knight to the quiet square', J(SD, "Nd2 Nf6 Ngf3 Bf5 e3 e6")),
        ('bdx-misc-bg5', 'Bishop out on move two', J(SD, "Bg5 h6 Bh4 c6 e3 Qb6")),
        ('bdx-misc-bg5f4', 'Bishop out, then the long diagonal', J(SD, "Bg5 h6 Bf4 Bf5 e3 e6")),
        ('bdx-misc-h3', 'Edge pawn', J(SD, "h3 Nf6 Nf3 Bf5"))],
  why='Rare second moves. Your pieces still go to the same squares.', outcome='Equal')
