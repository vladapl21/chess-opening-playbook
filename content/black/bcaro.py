"""Black against the e-pawn, second system: the Caro-Kann. The Slav setup's twin: c-pawn one square, d-pawn two,
light bishop out before the e-pawn, then the e-pawn. A separate pack (see PACKS in bmeta.py): a player has either
this or the e-pawn reply, never both. SAN is internal only; notes are plain English and sit at the end of this file."""
from bcontent import L, P, J, n

CK = "e4 c6"
CD = J(CK, "d4 d5")
ADV = J(CD, "e5 Bf5")                    # White pushes past
EX = J(CD, "exd5 cxd5")                  # White trades
CL = J(CD, "Nc3 dxe4 Nxe4 Bf5")          # White lets you take
KN = J(CK, "Nf3 d5 Nc3 Bg4")             # both knights, no d-pawn

# ============================================================== THE E-PAWN PUSHES PAST
P('bck-adv', 'caro', 'White pushes past', 'Advance',
  'White\'s e-pawn steps past your d-pawn. Bishop out first, then the e-pawn, then the c-pawn hits the base of the chain.')
L('bck-adv', 'bck-adv', 'The e-pawn pushes past', 'Bishop out, e-pawn, then the c-pawn two squares', 'core',
  J(ADV, "Nf3 e6 Be2 c5 c3 Nc6 O-O cxd4 cxd4 Nge7"),
  alts=[('bck-adv-oo', 'White castles before the c-pawn', J(ADV, "Nf3 e6 Be2 c5 O-O Nc6 c3 cxd4")),
        ('bck-adv-bd3', 'Bishop challenges yours: trade it', J(ADV, "Bd3 Bxd3 Qxd3 e6 Nf3 c5")),
        ('bck-adv-nf3bd3', 'Knight first, then the bishop offer', J(ADV, "Nf3 e6 Bd3 Bxd3 Qxd3 c5")),
        ('bck-adv-nc3', 'Queen\'s knight out', J(ADV, "Nc3 e6 Nf3 c5")),
        ('bck-adv-g4', 'The g-pawn chases your bishop', J(ADV, "Nc3 e6 g4 Bg6 h4 h5")),
        ('bck-adv-g4now', 'The g-pawn at once: step forward first', J(ADV, "g4 Be4 f3 Bg6 h4 h5")),
        ('bck-adv-f4', 'F-pawn behind the chain', J(ADV, "f4 e6 Nf3 c5")),
        ('bck-adv-f4g4', 'F-pawn, then the g-pawn: queen check', J(ADV, "f4 e6 g4 Qh4+ Kd2 Be4")),
        ('bck-adv-f4g4k', 'The king steps the other way', J(ADV, "f4 e6 g4 Qh4+ Ke2 Bxg4+")),
        ('bck-adv-c3', 'Small c-pawn move', J(ADV, "c3 e6 Nf3 c5")),
        ('bck-adv-c3bd3', 'Small c-pawn move, then the bishop offer', J(ADV, "c3 e6 Bd3 Bxd3 Qxd3 c5")),
        ('bck-adv-c4', 'C-pawn two squares', J(ADV, "c4 e6 Nc3 Ne7")),
        ('bck-adv-nf3first', 'Knight on move two, then the push', J(CK, "Nf3 d5 e5 Bf5 d4 e6 Be2 c5")),
        ('bck-adv-nc3first', 'Queen\'s knight on move two, then the push', J(CK, "Nc3 d5 e5 Bf5 d4 e6 Nf3 c5"))],
  why='Half the club players who put both pawns in the middle push the e-pawn past. Your bishop is already outside the chain, which is the whole point of this opening.',
  outcome='Equal, with a clear plan')

# ============================================================== WHITE TRADES PAWNS
P('bck-exch', 'caro', 'White trades pawns', 'Exchange and Panov',
  'White takes your d-pawn. Take back with the c-pawn, then both knights before the bishop, exactly as in the Slav pawn-trade lesson.')
L('bck-exch', 'bck-exch', 'The pawn trade', 'Take back with the c-pawn, both knights, then the bishop', 'core',
  J(EX, "Nc3 Nc6 Nf3 Nf6 Bb5 Bg4"),
  alts=[('bck-exch-nf3', 'King\'s knight first', J(EX, "Nf3 Nc6 Nc3 Nf6 Bf4 Bg4")),
        ('bck-exch-bb5', 'Bishop comes at your knight', J(EX, "Nf3 Nc6 Bb5 Nf6 O-O Bg4")),
        ('bck-exch-ne5', 'Knight jumps into the middle', J(EX, "Nf3 Nc6 Bb5 Nf6 Ne5 Bd7")),
        ('bck-exch-check', 'Bishop check', J(EX, "Bb5+ Nc6 Nf3 Nf6")),
        ('bck-exch-checkx', 'Check, then the bishop takes your knight', J(EX, "Bb5+ Nc6 Bxc6+ bxc6 Nf3 Nf6")),
        ('bck-exch-nc3bb5', 'Queen\'s knight, then the bishop at yours', J(EX, "Nc3 Nc6 Bb5 Nf6 Nf3 Bg4")),
        ('bck-exch-be3', 'Bishop beside the queen', J(EX, "Nc3 Nc6 Be3 Nf6")),
        ('bck-exch-bd3', 'Bishop takes your bishop\'s square', J(EX, "Bd3 Nc6 c3 Nf6 Bf4 Bg4")),
        ('bck-exch-c3', 'Small c-pawn move', J(EX, "Nf3 Nc6 c3 Nf6 Bd3 Bg4")),
        ('bck-exch-nf3first', 'Knight on move two, then the trade', J(CK, "Nf3 d5 exd5 cxd5 d4 Nc6 Nc3 Nf6")),
        ('bck-exch-nc3first', 'Queen\'s knight on move two, then the trade', J(CK, "Nc3 d5 exd5 cxd5 d4 Nc6 Nf3 Nf6")),
        ('bck-exch-nod4', 'Trade and check, no d-pawn', J(CK, "Nf3 d5 exd5 cxd5 Bb5+ Nc6 O-O Nf6"))],
  why='One in four trades pawns on move three. You get the open c-file and an easy game.', outcome='Equal')
L('bck-panov', 'bck-exch', 'The c-pawn attacks your d-pawn', 'Knight out, then guard the d-pawn with the e-pawn', 'common',
  J(EX, "c4 Nf6 Nc3 e6 Nf3 Be7 cxd5 Nxd5"),
  alts=[('bck-panov-cxd5', 'White takes at once', J(EX, "c4 Nf6 cxd5 Nxd5 Nc3 e6")),
        ('bck-panov-c5', 'The pawn pushes past', J(EX, "c4 Nf6 Nc3 e6 c5 Be7")),
        ('bck-panov-bg5', 'Bishop pins the knight', J(EX, "c4 Nf6 Nc3 e6 Bg5 Be7")),
        ('bck-panov-late', 'The c-pawn after the knights', J(EX, "Nf3 Nc6 c4 Nf6 Nc3 e6")),
        ('bck-panov-early', 'C-pawn on move two', J(CK, "c4 d5 exd5 cxd5 d4 Nf6 Nc3 e6")),
        ('bck-panov-early2', 'C-pawn on move two, both pawns traded', J(CK, "c4 d5 exd5 cxd5 cxd5 Nf6"))],
  why='About one in ten follows the trade with the c-pawn. This is the one line where the bishop stays home: the d-pawn needs the e-pawn at once.',
  outcome='Equal; White has a lone d-pawn to defend')

# ============================================================== WHITE LETS YOU TAKE
P('bck-main', 'caro', 'White lets you take', 'Classical',
  'White guards the e-pawn with a knight. Take it, bring the bishop out with a hit on the knight, and step back when it is chased.')
L('bck-main', 'bck-main', 'Take, then the bishop out', 'Bishop out, step back, queen\'s knight, e-pawn', 'core',
  J(CL, "Ng3 Bg6 Nf3 Nd7 Bd3 Bxd3 Qxd3 e6 O-O Ngf6"),
  alts=[('bck-main-h4', 'The h-pawn chases your bishop', J(CL, "Ng3 Bg6 h4 h6 Nf3 Nd7 h5 Bh7 Bd3 Bxd3 Qxd3 e6")),
        ('bck-main-h4h5', 'H-pawn all the way first', J(CL, "Ng3 Bg6 h4 h6 h5 Bh7 Nf3 Nd7")),
        ('bck-main-bd3', 'Bishop guards the knight: take the d-pawn', J(CL, "Bd3 Qxd4 Nf3 Qd8")),
        ('bck-main-bd3qf3', 'Queen comes at your bishop', J(CL, "Bd3 Qxd4 Qf3 Bxe4 Qxe4 Qxe4+ Bxe4 Nf6")),
        ('bck-main-ng3bd3', 'Knight back, then the bishop: the d-pawn again', J(CL, "Ng3 Bg6 Bd3 Qxd4 N1e2 Qd6")),
        ('bck-main-bc4', 'Bishop aims at f7', J(CL, "Ng3 Bg6 Bc4 e6 N1e2 Nf6")),
        ('bck-main-nc5', 'Knight jumps forward', J(CL, "Nc5 b6 Nb3 e6")),
        ('bck-main-nc3', 'Knight goes back', J(CL, "Nc3 e6 Nf3 Nd7")),
        ('bck-main-qf3', 'Queen guards the knight', J(CL, "Qf3 e6 c3 Nd7")),
        ('bck-main-nd2', 'The other knight square', J(CD, "Nd2 dxe4 Nxe4 Bf5 Ng3 Bg6")),
        ('bck-main-nc3first', 'Queen\'s knight on move two', J(CK, "Nc3 d5 d4 dxe4 Nxe4 Bf5 Ng3 Bg6"))],
  why='The oldest main line. A third of club players then guard the knight with the bishop, and that loses the d-pawn.',
  outcome='Equal; a pawn up if White slips')

# ============================================================== BOTH KNIGHTS, NO D-PAWN
P('bck-knights', 'caro', 'Both knights, no d-pawn', 'Two Knights',
  'White brings both knights out and holds the d-pawn back. Your bishop goes to the other side and takes the knight when asked.')
L('bck-2kn', 'bck-knights', 'Both knights out', 'Bishop out at the knight, then the e-pawn', 'common',
  J(KN, "Be2 e6 d4 Nf6"),
  alts=[('bck-2kn-h3', 'Edge pawn asks the bishop: take the knight', J(KN, "h3 Bxf3 Qxf3 e6 d4 Nf6")),
        ('bck-2kn-exd5', 'White trades first', J(KN, "exd5 cxd5 Bb5+ Nc6 h3 Bxf3 Qxf3 e6")),
        ('bck-2kn-d4', 'D-pawn now', J(KN, "d4 e6 h3 Bxf3 Qxf3 Nf6")),
        ('bck-2kn-nc3first', 'Queen\'s knight first', J(CK, "Nc3 d5 Nf3 Bg4 h3 Bxf3"))],
  why='A fifth of your games will start with a knight on move two. When both knights are out your bishop has a target.',
  outcome='Equal and solid')

# ============================================================== EVERYTHING ELSE
P('bck-other', 'caro', 'Other second moves', 'Sidelines',
  'A bishop, the f-pawn or a slow d-pawn on move two. The d-pawn goes two squares all the same.')
L('bck-bc4', 'bck-other', 'Bishop out on move two', 'D-pawn hits it and you gain a move', 'common',
  J(CK, "Bc4 d5 exd5 cxd5 Bb3 Nf6 d4 Nc6"),
  alts=[('bck-bc4-check', 'Bishop gives check instead', J(CK, "Bc4 d5 exd5 cxd5 Bb5+ Nc6 d4 Nf6"))],
  why='One in nine brings the Italian bishop out against this too. Your d-pawn arrives with a hit on it.', outcome='Comfortable')
L('bck-misc', 'bck-other', 'F-pawn or a slow d-pawn', 'The same two pawn moves, then the bishop', 'rare',
  J(CK, "f4 d5 e5 Bf5 Nf3 e6 d4 c5"),
  alts=[('bck-misc-f4x', 'F-pawn, then the trade', J(CK, "f4 d5 exd5 cxd5 Nf3 Nc6")),
        ('bck-misc-d3', 'D-pawn one square', J(CK, "d3 d5 Nd2 e5 Ngf3 Bd6")),
        ('bck-misc-d3x', 'D-pawn one square, then the trade', J(CK, "d3 d5 exd5 cxd5 Nf3 Nc6")),
        ('bck-misc-qf3', 'Queen out early', J(CK, "Nc3 d5 Qf3 dxe4 Nxe4 Nd7"))],
  why='These come up now and then. Nothing changes: two pawn moves, then the bishop.', outcome='Equal or better')

# ============================================================== notes
n(CK, 'C-pawn one square', 'It gets ready to back up the d-pawn. The same two pawns as your setup against the d-pawn, in the other order.', ['key'], arrows=['d7d5g'])
n(J(CK, 'd4'), 'Both pawns in the middle', 'The main move. Four in ten club players choose it.')
n(CD, 'D-pawn two squares', 'Now White has to decide about the e-pawn: push it past, trade it, or guard it.', ['key'])

n(J(CD, 'e5'), 'The e-pawn pushes past', 'Half of club players play this. The middle is closed, and your bishop is still free to leave.')
n(ADV, 'Bishop out first', 'The whole point of the opening: the bishop leaves before the e-pawn shuts the door. Then e-pawn, then the c-pawn two squares.', ['key'], arrows=['e7e6g', 'c6c5g'])
n(J(ADV, 'Nf3 e6'), 'E-pawn one square', 'The door closes behind the bishop. Your pawns now point at the queenside, so that is where you play.')
n(J(ADV, 'Nf3 e6 Be2 c5'), 'C-pawn two squares', 'It hits the pawn that holds White\'s chain together. Queen\'s knight behind it next.', ['key'], arrows=['c5d4g'])
n(J(ADV, 'Nf3 e6 Be2 c5 c3 Nc6'), 'Knight behind the pawn', 'A second attacker on the d-pawn.')
n(J(ADV, 'Nf3 e6 Be2 c5 c3 Nc6 O-O cxd4'), 'Trade the c-pawns', 'It opens the c-file for your rook and fixes the d-pawn as a target.')
n(J(ADV, 'Nf3 e6 Be2 c5 c3 Nc6 O-O cxd4 cxd4 Nge7'), 'King\'s knight the short way', 'It is heading for the square beside your bishop, where it hits the d-pawn again.')
n(J(ADV, 'Bd3'), 'Bishop offers a trade', 'One in five does this. Trading suits you: White\'s good bishop goes.')
n(J(ADV, 'Bd3 Bxd3'), 'Trade the bishops', 'Always take. Your bishop has done its job by getting out, and White is left with the worse one.', ['key'])
n(J(ADV, 'Bd3 Bxd3 Qxd3 e6'), 'E-pawn one square', 'Nothing left to shut in. Then the c-pawn, as always.')
n(J(ADV, 'Nc3 e6 g4'), 'G-pawn chases the bishop', 'It gains space and weakens White\'s king.')
n(J(ADV, 'Nc3 e6 g4 Bg6'), 'Step back', 'The bishop keeps its diagonal. The pawns White pushed cannot go back.')
n(J(ADV, 'Nc3 e6 g4 Bg6 h4 h5'), 'Stop the h-pawn', 'The edge pawn was coming to trap the bishop. Meet it head on; if the g-pawn pushes past, the bishop has its squares back.', ['key'])
n(J(ADV, 'f4 e6 g4 Qh4+ Ke2 Bxg4+'), 'Take the pawn with check', 'A pawn up, and White\'s king is stuck in the middle.', ['key'])
n(J(EX, 'Bb5+ Nc6 Bxc6+ bxc6'), 'Take back with the b-pawn', 'It supports your d-pawn, and you have the two bishops.')
n(J(ADV, 'g4 Be4'), 'Step forward first', 'It hits the rook, so White has to spend a move blocking with a pawn. Only then step back.', ['key'], arrows=['e4h1g'])
n(J(ADV, 'g4 Be4 f3 Bg6'), 'Now step back', 'White\'s king side is full of holes and the knight has lost its best square.')
n(J(ADV, 'g4 Be4 f3 Bg6 h4 h5'), 'Stop the h-pawn', 'The edge pawn was coming to trap the bishop. Meet it head on.', ['key'])
n(J(ADV, 'f4 e6 g4'), 'G-pawn lunge', 'It opens the diagonal to White\'s own king.', ['warn'])
n(J(ADV, 'f4 e6 g4 Qh4+'), 'Queen check wins', 'The f-pawn and g-pawn have both left, so nothing can block. The king must walk.', ['key', 'trap'], arrows=['h4e1g'])
n(J(ADV, 'f4 e6 g4 Qh4+ Kd2 Be4'), 'Bishop hits the rook', 'The rook is attacked and the g-pawn falls next.')
n(J(ADV, 'c4 e6 Nc3 Ne7'), 'Knight guards the d-pawn first', 'With White\'s c-pawn hitting your d-pawn, the knight comes before your own c-pawn move.')

n(J(CD, 'exd5'), 'White trades pawns', 'One in four does this.')
n(EX, 'Take back with the c-pawn', 'Toward the middle. The c-file opens for your rook.', ['key'])
n(J(EX, 'Nc3 Nc6'), 'Queen\'s knight first', 'With the c-pawns gone, White\'s queen can come out at your b-pawn the moment your bishop leaves. So both knights come out first, as in the Slav pawn trade.', ['key'])
n(J(EX, 'Nc3 Nc6 Nf3 Nf6'), 'King\'s knight', 'Both knights are out. Now the bishop can go.')
n(J(EX, 'Nc3 Nc6 Nf3 Nf6 Bb5 Bg4'), 'Bishop out at the knight', 'Outside the pawns before your e-pawn moves, the same idea as everywhere in this opening.', arrows=['e7e6g'])
n(J(EX, 'Nf3 Nc6 Bb5 Nf6 Ne5'), 'Knight jumps in', 'Two pieces now hit your knight.')
n(J(EX, 'Nf3 Nc6 Bb5 Nf6 Ne5 Bd7'), 'Bishop guards the knight', 'This time the bishop is needed at home. If White trades everything there, you are fine.', ['key'])
n(J(EX, 'Bb5+ Nc6'), 'Block with the knight', 'The square it was going to anyway.')
n(J(EX, 'c4'), 'C-pawn attacks your d-pawn', 'White accepts a lone d-pawn to get active pieces.')
n(J(EX, 'c4 Nf6'), 'Knight guards the d-pawn', 'If White takes, the knight takes back.')
n(J(EX, 'c4 Nf6 Nc3 e6'), 'E-pawn guards it too', 'The one line where your bishop stays inside: the d-pawn is attacked twice and needs the pawn now.', ['key'])
n(J(EX, 'c4 Nf6 Nc3 e6 Nf3 Be7'), 'Bishop out, castle next', 'Then aim everything at White\'s lone d-pawn.')
n(J(EX, 'c4 Nf6 Nc3 e6 c5 Be7'), 'Carry on', 'The pawn that pushed past no longer hits your middle. Castle, then hit it with the b-pawn.')

n(J(CD, 'Nc3'), 'Knight guards the e-pawn', 'White keeps the tension. One in five.')
n(J(CD, 'Nc3 dxe4'), 'Take the e-pawn', 'There is nothing better to do with the d-pawn, and it draws the knight into the open.', ['key'])
n(CL, 'Bishop out, hitting the knight', 'Outside the pawns, with a gain of time.', ['key'], arrows=['f5e4r'])
n(J(CL, 'Ng3'), 'Knight moves and hits the bishop', 'A third of club players find this.')
n(J(CL, 'Ng3 Bg6'), 'Step back', 'The bishop stays on its diagonal. From here the order is: queen\'s knight, e-pawn, king\'s knight.', ['key'])
n(J(CL, 'Ng3 Bg6 Nf3 Nd7'), 'Queen\'s knight first', 'It covers the middle square White\'s knight wants. Without it the knight jumps in and hits your bishop.', ['key'])
n(J(CL, 'Ng3 Bg6 Nf3 Nd7 Bd3 Bxd3'), 'Trade the bishops', 'Take whenever White offers.')
n(J(CL, 'Ng3 Bg6 Nf3 Nd7 Bd3 Bxd3 Qxd3 e6'), 'E-pawn one square', 'Now the king\'s knight and the dark bishop have their squares.')
n(J(CL, 'Ng3 Bg6 h4'), 'H-pawn threatens to trap the bishop', 'You know this from the White side: the pawn wants one more step.', ['warn'], arrows=['h4h5r'])
n(J(CL, 'Ng3 Bg6 h4 h6'), 'Make room', 'One square for the edge pawn gives the bishop a way back.', ['key'], arrows=['g6h7g'])
n(J(CL, 'Ng3 Bg6 h4 h6 h5 Bh7'), 'Into the corner', 'Safe, and still on the long diagonal.')
n(J(CL, 'Bd3'), 'Bishop guards the knight', 'Natural and wrong: a third of club players play it. The d-pawn has lost its guard.', ['warn'])
n(J(CL, 'Bd3 Qxd4'), 'Take the d-pawn', 'The bishop stepped in front of the queen, so nothing guards it. A clean pawn.', ['key', 'trap'], arrows=['d8d4g'])
n(J(CL, 'Bd3 Qxd4 Nf3 Qd8'), 'Queen goes home', 'A pawn up. Go back before the pieces start chasing her.')
n(J(CL, 'Ng3 Bg6 Bd3'), 'The same slip a move later', 'Nearly one in five. The d-pawn is loose again.', ['warn'])
n(J(CL, 'Ng3 Bg6 Bd3 Qxd4'), 'Take the d-pawn', 'The same pawn for the same reason.', ['key', 'trap'], arrows=['d8d4g'])
n(J(CL, 'Nc5 b6'), 'B-pawn hits the knight', 'It has to go back, and you have gained a useful move.')

n(J(CK, 'Nf3'), 'Knight first', 'As common as the d-pawn at club level. Your answer is the same.')
n(J(CK, 'Nf3 d5'), 'D-pawn two squares', 'Always the second move, whatever White did.', ['key'])
n(KN, 'Bishop out at the knight', 'With both knights out and no d-pawn in the middle, the bishop goes to this side instead and is ready to take.', ['key'])
n(J(KN, 'h3 Bxf3'), 'Take the knight', 'Do not step back: White\'s g-pawn would chase the bishop with gain of time. You give up the bishop and get an easy game.', ['key'])
n(J(KN, 'h3 Bxf3 Qxf3 e6'), 'E-pawn one square', 'A solid wall on the light squares, the colour of the bishop you just traded.')
n(J(KN, 'Be2 e6'), 'E-pawn one square', 'The bishop is already outside, so the door can close.')

n(J(CK, 'Bc4'), 'Bishop out on move two', 'It aims at f7, but your next move blocks it and hits it.')
n(J(CK, 'Bc4 d5'), 'D-pawn hits the bishop', 'It has to move again, and you have the middle.', ['key'], arrows=['d5c4r'])
n(J(CK, 'Bc4 d5 exd5 cxd5 Bb3 Nf6'), 'Knight out', 'White has spent three moves on one bishop.')
