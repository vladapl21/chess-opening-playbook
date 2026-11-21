"""Black against the e-pawn: the French. E-pawn one square, then the d-pawn two. When White's pawn pushes past, the
c-pawn hits the chain with the knight and the queen behind it; when a knight guards the pawn, yours hits it and steps
back if it is pushed; when the pawns are traded, knight, bishop, castle. A separate pack (see PACKS in bmeta.py). The
lines were drafted with pipeline/draft.py: White's moves by the Maia 1300/1500 odds, yours from the setup's order
wherever Stockfish 17.1 accepts it and the engine's move elsewhere. SAN is internal only; notes are plain English."""
from bcontent import L, P, J, n

P('bfr-adv', 'french', 'The pawn pushes past', 'Advance Variation', "White's e-pawn steps past yours and the middle is locked. The chain points at your king's side, so you play on the other: the c-pawn hits the pawn that holds the chain up, and the knight and the queen join in.")
P('bfr-exch', 'french', 'The pawns are traded', 'Exchange Variation', 'White takes and you take back with the e-pawn. Both bishops are free and the position is the same for both sides: knight, bishop, castle.')
P('bfr-knight', 'french', 'White holds the pawn', 'Classical, Burn and Tarrasch', 'A knight guards the e-pawn. Yours comes out and hits it: if the pawn pushes past, the knight steps back and the c-pawn goes at the chain; if the bishop pins the knight, you take the e-pawn and break the pin.')
P('bfr-second', 'french', 'No two pawns in the middle', 'Second-move sidelines', 'White holds the d-pawn back. Yours goes two squares all the same, and the pieces come out the usual way.')

L('bfr-adv', 'bfr-adv', 'The Advance: hit the chain', 'C-pawn, knight, queen: three pieces on one pawn', 'core',
  'e4 e6 d4 d5 e5 c5 c3 Nc6 Nf3 Qb6 Be2 cxd4 cxd4 Bd7 O-O Nge7',
  alts=[('bfr-adv-bb5', 'Bishop pins the knight', 'e4 e6 d4 d5 e5 c5 c3 Nc6 Bb5 Qb6 Bxc6+ bxc6 Nf3 Ba6'),
        ('bfr-adv-b3', 'Small b-pawn move', 'e4 e6 d4 d5 e5 c5 c3 Nc6 Nf3 Qb6 b3 cxd4 cxd4 Bb4+ Bd2 Bd7'),
        ('bfr-adv-a3', 'Small a-pawn move', 'e4 e6 d4 d5 e5 c5 c3 Nc6 Nf3 Qb6 a3 c4'),
        ('bfr-adv-bb5a4', 'Bishop pins the knight, then a-pawn two squares', 'e4 e6 d4 d5 e5 c5 c3 Nc6 Bb5 Qb6 a4 cxd4 cxd4 Bd7'),
        ('bfr-adv-be3', 'Bishop behind the center pawns', 'e4 e6 d4 d5 e5 c5 c3 Nc6 Nf3 Qb6 Be3 Qxb2 Nbd2 c4 Be2 Qxc3 O-O Bd7'),
        ('bfr-adv-be3rb1', 'Bishop behind the center pawns, then rook to a new file', 'e4 e6 d4 d5 e5 c5 c3 Nc6 Nf3 Qb6 Be3 Qxb2 Nbd2 c4 Rb1 Qxc3'),
        ('bfr-adv-nc3', 'Queen\'s knight out', 'e4 e6 d4 d5 e5 c5 c3 Nc6 Nf3 Qb6 Be2 cxd4 cxd4 Bd7 Nc3 Nge7'),
        ('bfr-adv-bd3', 'Milner-Barry Gambit', 'e4 e6 d4 d5 e5 c5 c3 Nc6 Nf3 Qb6 Bd3 cxd4 cxd4 Bd7 O-O Nxd4 Nxd4 Qxd4'),
        ('bfr-adv-be3qc2', 'Kupreichik Variation, then queen comes out', 'e4 e6 d4 d5 e5 c5 c3 Nc6 Be3 Qb6 Qc2 Nh6'),
        ('bfr-adv-be3b3', 'Kupreichik Variation, then small b-pawn move', 'e4 e6 d4 d5 e5 c5 c3 Nc6 Be3 Qb6 b3 cxd4 cxd4 Bb4+ Nd2 Bd7'),
        ('bfr-adv-bd3be3', 'Milner-Barry Gambit, then bishop behind the center pawns', 'e4 e6 d4 d5 e5 c5 c3 Nc6 Nf3 Qb6 Bd3 cxd4 cxd4 Bd7 Be3 Qxb2'),
        ('bfr-adv-nxd4', 'Knight takes back', 'e4 e6 d4 d5 e5 c5 c3 Nc6 Nf3 Qb6 Be2 cxd4 Nxd4 Nxe5 O-O Nf6')],
  why='The most common French at club level. White\'s pawns point at your king\'s side, and the pawn that holds them up is your target.', outcome='Pressure on the d-pawn')
L('bfr-adv4', 'bfr-adv', 'The Advance: no c-pawn behind it', 'The knight first, a pawn taken, the queen out', 'common',
  'e4 e6 d4 d5 e5 c5 Nf3 cxd4 Nxd4 Nc6 Nxc6 bxc6 Nc3 c5',
  alts=[('bfr-adv4-qxd4', 'Queen takes back', 'e4 e6 d4 d5 e5 c5 Nf3 cxd4 Qxd4 Nc6 Qa4 Qb6'),
        ('bfr-adv4-qxd4bb5', 'Queen takes back, then bishop pins the knight', 'e4 e6 d4 d5 e5 c5 Nf3 cxd4 Qxd4 Nc6 Bb5 Bd7 Bxc6 bxc6 O-O c5'),
        ('bfr-adv4-bd3', 'Bishop to the middle', 'e4 e6 d4 d5 e5 c5 Nf3 cxd4 Nxd4 Nc6 Nxc6 bxc6 Bd3 Qb6'),
        ('bfr-adv4-qxd4qd1', 'Queen takes back, then queen steps back', 'e4 e6 d4 d5 e5 c5 Nf3 cxd4 Qxd4 Nc6 Qd1 Bd7'),
        ('bfr-adv4-bb5', 'Bishop pins the knight', 'e4 e6 d4 d5 e5 c5 Nf3 cxd4 Nxd4 Nc6 Bb5 Bd7 Nxc6 Bxc6 Bxc6+ bxc6 O-O Ne7'),
        ('bfr-adv4-bb5bxc6', 'Bishop pins the knight, then bishop takes the knight', 'e4 e6 d4 d5 e5 c5 Nf3 cxd4 Nxd4 Nc6 Bb5 Bd7 Bxc6 bxc6 O-O c5'),
        ('bfr-adv4-bb5oo', 'Bishop pins the knight, then castles', 'e4 e6 d4 d5 e5 c5 Nf3 cxd4 Nxd4 Nc6 Bb5 Bd7 O-O Nxe5 Bxd7+ Qxd7')],
  why='White doesn\'t back the chain up with the c-pawn. Its base is weaker still, and the same three pieces go at it.', outcome='Equal or better')
L('bfr-exch', 'bfr-exch', 'The Exchange', 'Take back with the e-pawn; knight, bishop, castle', 'core',
  'e4 e6 d4 d5 exd5 exd5 Nf3 Nf6 Bd3 Bd6 O-O O-O Bg5 Bg4',
  alts=[('bfr-exch-nc3', 'Queen\'s knight out', 'e4 e6 d4 d5 exd5 exd5 Nc3 Nf6 Nf3 Bd6'),
        ('bfr-exch-c4', 'Monte Carlo Variation', 'e4 e6 d4 d5 exd5 exd5 c4 Nf6 Nc3 Bd6'),
        ('bfr-exch-nc3bg5', 'Queen\'s knight out, then Svenonius Variation', 'e4 e6 d4 d5 exd5 exd5 Nc3 Nf6 Bg5 Be7 Bxf6 Bxf6'),
        ('bfr-exch-be2', 'Bishop to the quiet square', 'e4 e6 d4 d5 exd5 exd5 Nf3 Nf6 Be2 Bd6 O-O O-O'),
        ('bfr-exch-qe2', 'Queen gives check', 'e4 e6 d4 d5 exd5 exd5 Qe2+ Be7 Nc3 Nf6'),
        ('bfr-exch-qe2nf3', 'Queen gives check, then king\'s knight out', 'e4 e6 d4 d5 exd5 exd5 Qe2+ Be7 Nf3 Nf6'),
        ('bfr-exch-nc3bg5nf3', 'Queen\'s knight out, then Svenonius Variation, then king\'s knight out', 'e4 e6 d4 d5 exd5 exd5 Nc3 Nf6 Bg5 Be7 Nf3 O-O Bd3 c5'),
        ('bfr-exch-bg5', 'Bishop pins the knight', 'e4 e6 d4 d5 exd5 exd5 Nf3 Nf6 Bg5 Bd6 Nc3 c6'),
        ('bfr-exch-nc3bd3', 'Queen\'s knight out, then bishop to the middle', 'e4 e6 d4 d5 exd5 exd5 Nf3 Nf6 Nc3 Bd6 Bd3 O-O'),
        ('bfr-exch-c4cxd5', 'Monte Carlo Variation, then pawn takes the pawn', 'e4 e6 d4 d5 exd5 exd5 c4 Nf6 cxd5 Bb4+'),
        ('bfr-exch-nc3bg5v2', 'Queen\'s knight out, then bishop pins the knight', 'e4 e6 d4 d5 exd5 exd5 Nf3 Nf6 Nc3 Bd6 Bg5 c6 Bd3 O-O'),
        ('bfr-exch-qe2bg5', 'Queen gives check, then bishop pins the bishop', 'e4 e6 d4 d5 exd5 exd5 Qe2+ Be7 Bg5 Nc6'),
        ('bfr-exch-c4v2', 'C-pawn two squares', 'e4 e6 d4 d5 exd5 exd5 Nf3 Nf6 c4 Bb4+ Bd2 c5')],
  why='One in four trades the pawns. Your light bishop is free at last, and the position is level and easy to play.', outcome='Equal')
L('bfr-steinitz', 'bfr-knight', 'The Steinitz: knight out, then the push', 'The knight steps back; the c-pawn hits the chain', 'core',
  'e4 e6 d4 d5 Nc3 Nf6 e5 Nfd7 f4 c5 Nf3 Nc6 Be3 Qb6',
  alts=[('bfr-steinitz-exd5', 'Delayed Exchange Variation', 'e4 e6 d4 d5 Nc3 Nf6 exd5 exd5'),
        ('bfr-steinitz-bd3', 'Swiss Variation', 'e4 e6 d4 d5 Nc3 Nf6 Bd3 c5'),
        ('bfr-steinitz-nf3', 'King\'s knight out', 'e4 e6 d4 d5 Nc3 Nf6 e5 Nfd7 Nf3 c5 Bg5 Qb6'),
        ('bfr-steinitz-bb5', 'Bishop pins the knight', 'e4 e6 d4 d5 Nc3 Nf6 e5 Nfd7 Bb5 c5'),
        ('bfr-steinitz-nf3be3', 'King\'s knight out, then bishop behind the center pawns', 'e4 e6 d4 d5 Nc3 Nf6 e5 Nfd7 Nf3 c5 Be3 Nc6 Bb5 cxd4'),
        ('bfr-steinitz-nf3bb5', 'King\'s knight out, then bishop pins the knight', 'e4 e6 d4 d5 Nc3 Nf6 e5 Nfd7 Nf3 c5 Bb5 Nc6 Bxc6 bxc6'),
        ('bfr-steinitz-bd3v2', 'Bishop to the middle', 'e4 e6 d4 d5 Nc3 Nf6 e5 Nfd7 Bd3 c5'),
        ('bfr-steinitz-nf3dxc5', 'King\'s knight out, then pawn takes the pawn', 'e4 e6 d4 d5 Nc3 Nf6 e5 Nfd7 Nf3 c5 dxc5 Nc6')],
  why='White guards the e-pawn with a knight, and pushes when yours hits it. The knight steps back and the plan is the one you know: c-pawn, knight, queen at the base of the chain.', outcome='A fight on your terms')
L('bfr-burn', 'bfr-knight', 'The Burn: the bishop pins your knight', 'Take the e-pawn, then break the pin', 'common',
  'e4 e6 d4 d5 Nc3 Nf6 Bg5 dxe4 Nxe4 Be7 Bxf6 Bxf6',
  alts=[('bfr-burn-bxf6', 'Bishop takes the knight', 'e4 e6 d4 d5 Nc3 Nf6 Bg5 dxe4 Bxf6 gxf6 Nxe4 f5'),
        ('bfr-burn-nxf6', 'Knight takes the knight with check', 'e4 e6 d4 d5 Nc3 Nf6 Bg5 dxe4 Nxe4 Be7 Nxf6+ Bxf6 Bxf6 Qxf6 Nf3 c5')],
  why='The bishop pins your knight to the queen. Taking the e-pawn clears the middle, and the bishop one square breaks the pin.', outcome='Solid and equal')
L('bfr-tarrasch', 'bfr-knight', 'The Tarrasch: the knight goes the other way', 'The same answer: knight out, then back, then the c-pawn', 'common',
  'e4 e6 d4 d5 Nd2 Nf6 e5 Nfd7 Bd3 c5 c3 Nc6 Ne2 Qb6',
  why='The knight guards the pawn from a square where it can\'t be pinned. Your answer doesn\'t change.', outcome='Equal')
L('bfr-nf3', 'bfr-second', 'The knight before the d-pawn', 'D-pawn two squares all the same', 'core',
  'e4 e6 Nf3 d5 exd5 exd5 d4 Nf6',
  alts=[('bfr-nf3-e5', 'Small e-pawn move', 'e4 e6 Nf3 d5 e5 c5 d4 cxd4'),
        ('bfr-nf3-nc3', 'Queen\'s knight out', 'e4 e6 Nf3 d5 exd5 exd5 Nc3 Nf6 d4 Bd6'),
        ('bfr-nf3-e5c3', 'Small e-pawn move, then small c-pawn move', 'e4 e6 Nf3 d5 e5 c5 c3 Nc6 d4 Qb6'),
        ('bfr-nf3-nc3exd5', 'Two Knights Variation, then pawn takes the pawn', 'e4 e6 Nf3 d5 Nc3 Nf6 exd5 exd5'),
        ('bfr-nf3-nc3e5', 'Two Knights Variation, then small e-pawn move', 'e4 e6 Nf3 d5 Nc3 Nf6 e5 Nfd7 d4 c5'),
        ('bfr-nf3-qe2', 'Queen gives check', 'e4 e6 Nf3 d5 exd5 exd5 Qe2+ Be7 d4 Nf6'),
        ('bfr-nf3-qe2nc3', 'Queen gives check, then queen\'s knight out', 'e4 e6 Nf3 d5 exd5 exd5 Qe2+ Be7 Nc3 Nf6'),
        ('bfr-nf3-e5bb5', 'Small e-pawn move, then bishop gives check', 'e4 e6 Nf3 d5 e5 c5 Bb5+ Bd7 Bxd7+ Nxd7 O-O Qb6'),
        ('bfr-nf3-e5c3bb5', 'Small e-pawn move, then small c-pawn move, then bishop pins the knight', 'e4 e6 Nf3 d5 e5 c5 c3 Nc6 Bb5 Qb6 Bxc6+ Qxc6'),
        ('bfr-nf3-nc3d3', 'Two Knights Variation, then small d-pawn move', 'e4 e6 Nf3 d5 Nc3 Nf6 d3 c5'),
        ('bfr-nf3-d3', 'Small d-pawn move', 'e4 e6 Nf3 d5 d3 Nf6 Bg5 dxe4'),
        ('bfr-nf3-e5bb5d4', 'Small e-pawn move, then bishop gives check, then d-pawn two squares', 'e4 e6 Nf3 d5 e5 c5 Bb5+ Bd7 Bxd7+ Nxd7 d4 cxd4'),
        ('bfr-nf3-d3nc3', 'Small d-pawn move, then queen\'s knight out', 'e4 e6 Nf3 d5 d3 Nf6 Nc3 c5'),
        ('bfr-nf3-nc3bb5', 'Queen\'s knight out, then bishop gives check', 'e4 e6 Nf3 d5 exd5 exd5 Nc3 Nf6 Bb5+ c6 Ba4 Bd6'),
        ('bfr-nf3-nc3d3v2', 'Queen\'s knight out, then small d-pawn move', 'e4 e6 Nf3 d5 exd5 exd5 Nc3 Nf6 d3 Bd6'),
        ('bfr-nf3-nc3d4', 'Two Knights Variation, then d-pawn two squares', 'e4 e6 Nf3 d5 Nc3 Nf6 d4 Nxe4'),
        ('bfr-nf3-nc3qe2', 'Queen\'s knight out, then queen gives check', 'e4 e6 Nf3 d5 exd5 exd5 Nc3 Nf6 Qe2+ Be7'),
        ('bfr-nf3-d3e5', 'Small d-pawn move, then small e-pawn move', 'e4 e6 Nf3 d5 d3 Nf6 e5 Nfd7 d4 c5')],
  why='One in four develops first. Your d-pawn goes two squares anyway, and the game is an Advance or an Exchange a move later.', outcome='Equal')
L('bfr-qn', 'bfr-second', 'The queen\'s knight on move two', 'D-pawn two squares; knight out when the pawn is guarded', 'common',
  'e4 e6 Nc3 d5 exd5 exd5 d4 Nf6',
  alts=[('bfr-qn-d4', 'Paulsen Variation', 'e4 e6 Nc3 d5 d4 Nf6'),
        ('bfr-qn-nf3', 'King\'s knight out', 'e4 e6 Nc3 d5 exd5 exd5 Nf3 Nf6'),
        ('bfr-qn-nf3v2', 'Two Knights Variation', 'e4 e6 Nc3 d5 Nf3 Nf6'),
        ('bfr-qn-qe2', 'Queen gives check', 'e4 e6 Nc3 d5 exd5 exd5 Qe2+ Be7'),
        ('bfr-qn-e5', 'Small e-pawn move', 'e4 e6 Nc3 d5 e5 c5 d4 Nc6'),
        ('bfr-qn-d3', 'Small d-pawn move', 'e4 e6 Nc3 d5 d3 Nf6')],
  why='The knight comes before the d-pawn. Nothing changes: your d-pawn hits the e-pawn, and your knight follows.', outcome='Equal')
L('bfr-f4', 'bfr-second', 'The f-pawn on move two', 'The La Bourdonnais: the chain without a d-pawn', 'common',
  'e4 e6 f4 d5 Nf3 dxe4',
  alts=[('bfr-f4-e5', 'Small e-pawn move', 'e4 e6 f4 d5 e5 c5 d4 Nc6'),
        ('bfr-f4-e5nf3', 'Small e-pawn move, then king\'s knight out', 'e4 e6 f4 d5 e5 c5 Nf3 Nc6 Bb5 Qb6 Bxc6+ Qxc6'),
        ('bfr-f4-e5nf3c3', 'Small e-pawn move, then king\'s knight out, then small c-pawn move', 'e4 e6 f4 d5 e5 c5 Nf3 Nc6 c3 Qb6'),
        ('bfr-f4-e5c3', 'Small e-pawn move, then small c-pawn move', 'e4 e6 f4 d5 e5 c5 c3 Nc6'),
        ('bfr-f4-exd5', 'Pawn takes the pawn', 'e4 e6 f4 d5 exd5 exd5 Nf3 Nf6 d4 Bd6'),
        ('bfr-f4-exd5d4', 'Pawn takes the pawn, then d-pawn two squares', 'e4 e6 f4 d5 exd5 exd5 d4 Nf6'),
        ('bfr-f4-nc3', 'Pelikan Variation', 'e4 e6 f4 d5 Nc3 c5')],
  why='White wants a chain with the f-pawn behind it. The c-pawn and the knight go at it the usual way.', outcome='Comfortable')
L('bfr-bc4', 'bfr-second', 'The Italian bishop', 'Your d-pawn hits it with a move gained', 'common',
  'e4 e6 Bc4 d5 exd5 exd5 Bb3 Nf6 Nc3 Bd6',
  alts=[('bfr-bc4-qe2', 'Queen gives check', 'e4 e6 Bc4 d5 exd5 exd5 Qe2+ Be7 Bb3 Nf6'),
        ('bfr-bc4-d4', 'D-pawn two squares', 'e4 e6 Bc4 d5 exd5 exd5 Bb3 Nf6 d4 Bd6 Nf3 O-O'),
        ('bfr-bc4-h3', 'Small h-pawn move', 'e4 e6 Bc4 d5 exd5 exd5 Bb3 Nf6 h3 Bd6'),
        ('bfr-bc4-qe2v2', 'Queen gives check on move 5', 'e4 e6 Bc4 d5 exd5 exd5 Bb3 Nf6 Qe2+ Be7'),
        ('bfr-bc4-d3', 'Small d-pawn move', 'e4 e6 Bc4 d5 exd5 exd5 Bb3 Nf6 d3 Bd6 Bg5 O-O'),
        ('bfr-bc4-bb5', 'Bishop gives check', 'e4 e6 Bc4 d5 exd5 exd5 Bb5+ Nc6 Bxc6+ bxc6'),
        ('bfr-bc4-d4bg5', 'D-pawn two squares, then bishop pins the knight', 'e4 e6 Bc4 d5 exd5 exd5 Bb3 Nf6 d4 Bd6 Bg5 O-O'),
        ('bfr-bc4-nf3', 'King\'s knight out', 'e4 e6 Bc4 d5 exd5 exd5 Bb3 Nf6 Nf3 Bd6 d4 O-O'),
        ('bfr-bc4-nf3oo', 'King\'s knight out, then castles', 'e4 e6 Bc4 d5 exd5 exd5 Bb3 Nf6 Nf3 Bd6 O-O O-O d4 Nc6')],
  why='Club players love this bishop. Against the French it runs into a pawn at once.', outcome='A move ahead')
L('bfr-e5', 'bfr-second', 'The e-pawn pushes at once', 'D-pawn two squares: the Advance a move early', 'common',
  'e4 e6 e5 d5 exd6 Bxd6 Nf3 Nf6',
  alts=[('bfr-e5-d4', 'Advance Variation', 'e4 e6 e5 d5 d4 c5'),
        ('bfr-e5-nf3', 'King\'s knight out', 'e4 e6 e5 d5 Nf3 c5'),
        ('bfr-e5-d4v2', 'D-pawn two squares', 'e4 e6 e5 d5 exd6 Bxd6 d4 Nf6'),
        ('bfr-e5-nc3', 'Queen\'s knight out', 'e4 e6 e5 d5 exd6 Bxd6 Nc3 Nf6')],
  why='The pawn pushes before yours is there to push past. Play the d-pawn all the same and it is the chain you know.', outcome='Equal')
L('bfr-kia', 'bfr-second', 'The small d-pawn', 'The King\'s Indian Attack: take the middle', 'common',
  'e4 e6 d3 d5 Nd2 Nf6 Ngf3 c5 g3 Nc6 Bg2 Be7 O-O O-O',
  alts=[('bfr-kia-e5', 'Small e-pawn move', 'e4 e6 d3 d5 e5 c5'),
        ('bfr-kia-exd5', 'Pawn takes the pawn', 'e4 e6 d3 d5 exd5 exd5 Nf3 Nf6'),
        ('bfr-kia-nc3', 'Queen\'s knight out', 'e4 e6 d3 d5 Nc3 Nf6'),
        ('bfr-kia-exd5qe2', 'Pawn takes the pawn, then queen gives check', 'e4 e6 d3 d5 exd5 exd5 Qe2+ Be7'),
        ('bfr-kia-nf3', 'King\'s knight out', 'e4 e6 d3 d5 Nf3 Nf6')],
  why='White keeps the middle shut and builds behind it. You take the room that is on offer.', outcome='Comfortable')
L('bfr-second', 'bfr-second', 'Other second moves', 'The queen out early, the c-pawn', 'rare',
  'e4 e6 Qf3 d5 exd5 exd5 Nc3 Nf6',
  alts=[('bfr-second-e5', 'Small e-pawn move', 'e4 e6 Qf3 d5 e5 c5'),
        ('bfr-second-d4', 'D-pawn two squares', 'e4 e6 Qf3 d5 exd5 exd5 d4 Nf6')],
  why='Without the d-pawn beside the e-pawn there is nothing to lock. D-pawn two squares, and develop.', outcome='Equal or better')

# ============================================================== notes
n('e4 e6', 'E-pawn one square', 'It backs the d-pawn up. On the next move that pawn goes two squares and hits White\'s e-pawn.', ['key'])
n('e4 e6 d4 d5', 'D-pawn two squares', 'It hits the e-pawn. White has to push past, trade or guard it.', ['key'], arrows=['d5e4r'])
n('e4 e6 d4 d5 e5 c5', 'C-pawn hits the chain', 'White\'s d-pawn holds the pushed pawn up. Hit the chain at its base.', ['key'], arrows=['c5d4r'])
n('e4 e6 d4 d5 e5 c5 c3 Nc6', 'Knight out', 'A second piece on the d-pawn.', ['key'], arrows=['c6d4r', 'c5d4r'])
n('e4 e6 d4 d5 e5 c5 c3 Nc6 Nf3 Qb6', 'Queen behind the c-pawn', 'A third piece on the d-pawn, and she looks at the b-pawn too: White\'s dark bishop can\'t leave home without losing it.', ['key'], arrows=['b6d4r', 'b6b2r'])
n('e4 e6 d4 d5 e5 c5 c3 Nc6 Nf3 Qb6 a3 c4', 'C-pawn steps past', 'The a-pawn was getting ready to push the b-pawn at your c-pawn. Step past first: that side is shut, and your knight has a square behind White\'s pawns to aim for.', ['key'], arrows=['c6a5g', 'a5b3g'])
n('e4 e6 d4 d5 exd5 exd5', 'E-pawn takes back', 'The light bishop has an open line now. Knight, bishop, castle.', ['key'])
n('e4 e6 d4 d5 Nc3 Nf6', 'Knight hits the e-pawn', 'A second piece on it. White has to push the pawn past, trade it, or bring the bishop out at your knight.', ['key'], arrows=['f6e4r'])
n('e4 e6 d4 d5 Nc3 Nf6 e5 Nfd7', 'Knight steps back', 'It makes room for the f-pawn and backs up the c-pawn\'s push. The chain is on the board, and you know what to do with it.', ['key'])
n('e4 e6 d4 d5 Nc3 Nf6 e5 Nfd7 f4 c5', 'C-pawn hits the chain', 'The same move as in the Advance. Knight and queen come behind it.', ['key'], arrows=['c5d4r'])
n('e4 e6 e5 d5', 'D-pawn two squares', 'The same second move. If White takes it in passing, your bishop takes back with a piece out; if not, it is the Advance.', ['key'])
n('e4 e6 e5 d5 exd6 Bxd6', 'Bishop takes back', 'A piece out with a move gained, and White has no pawn left in the middle.', ['key'])
n('e4 e6 Nc3 d5', 'D-pawn two squares', 'The same second move whatever White has played.', ['key'])
n('e4 e6 Bc4 d5', 'D-pawn hits the bishop', 'It has to move again, and you have the middle.', ['key'], arrows=['d5c4r'])
n('e4 e6 d4 d5 Nc3 Nf6 Bg5 dxe4', 'Take the e-pawn', 'The pinned knight couldn\'t hold the middle. With the pawn gone, the bishop one square breaks the pin.', ['key'])
n('e4 e6 d4 d5 Nc3 Nf6 Bg5 dxe4 Nxe4 Be7', 'Bishop breaks the pin', 'Now the knight is free, and a trade on that square leaves you with the two bishops.', ['key'])
n('e4 e6 d4 d5 Nd2 Nf6', 'Knight hits the e-pawn', 'The same answer as against the other knight.', ['key'], arrows=['f6e4r'])
n('e4 e6 d4 d5 Nd2 Nf6 e5 Nfd7', 'Knight steps back', 'The chain again: the c-pawn hits its base next.', ['key'])
n('e4 e6 Nf3 d5', 'D-pawn two squares', 'The same second move whatever White has played.', ['key'])
n('e4 e6 d3 d5', 'D-pawn two squares', 'White isn\'t fighting for the middle, so you take it.', ['key'])
# the other side's moves that start a named line
n('e4 e6 Nc3', 'Queen\'s Knight')
n('e4 e6 Nf3', 'Knight Variation')
n('e4 e6 d3', 'King\'s Indian Attack')
n('e4 e6 e5', 'Steinitz Attack')
n('e4 e6 f4', 'La Bourdonnais Variation')
n('e4 e6 Nc3 d5 Nf3', 'Two Knights Variation')
n('e4 e6 Nc3 d5 d4', 'Paulsen Variation')
n('e4 e6 Nf3 d5 Nc3', 'Two Knights Variation')
n('e4 e6 d4 d5 Nc3', 'Paulsen Variation')
n('e4 e6 d4 d5 Nd2', 'Tarrasch Variation')
n('e4 e6 d4 d5 e5', 'Advance Variation')
n('e4 e6 e5 d5 d4', 'Advance Variation')
n('e4 e6 f4 d5 Nc3', 'Pelikan Variation')
n('e4 e6 Nf3 d5 e5 c5 d4', 'Nimzowitsch System')
n('e4 e6 d4 d5 Nc3 Nf6 Bd3', 'Swiss Variation')
n('e4 e6 d4 d5 Nc3 Nf6 Bg5', '4. Bg5')
n('e4 e6 d4 d5 Nc3 Nf6 e5', 'Steinitz Variation')
n('e4 e6 d4 d5 Nc3 Nf6 exd5', 'Delayed Exchange Variation')
n('e4 e6 d4 d5 e5 c5 Nf3', 'Nimzowitsch System')
n('e4 e6 d4 d5 exd5 exd5 c4', 'Monte Carlo Variation')
n('e4 e6 Nf3 d5 e5 c5 c3 Nc6 d4', 'Paulsen Attack')
n('e4 e6 d4 d5 e5 c5 c3 Nc6 Be3', 'Kupreichik Variation')
n('e4 e6 d4 d5 e5 c5 c3 Nc6 Nf3', 'Paulsen Attack')
n('e4 e6 d4 d5 exd5 exd5 Nc3 Nf6 Bg5', 'Svenonius Variation')
n('e4 e6 d4 d5 Nc3 Nf6 e5 Nfd7 f4 c5 Nf3', 'Steinitz Variation')
n('e4 e6 d4 d5 e5 c5 c3 Nc6 Nf3 Qb6 Bd3', 'Milner-Barry Gambit')
n('e4 e6 d4 d5 Nc3 Nf6 e5 Nfd7 f4 c5 Nf3 Nc6 Be3', 'Boleslavsky Variation')
