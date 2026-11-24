"""Endings: the kinds of ending the Endings tab plays, and the endings course built from the house player's games.

Everything the player reads follows the house rules: plain words from the player's side, no notation. Positions are
FEN strings; arrows and circles are squares with a colour letter (g green, r red, b blue, y amber) and never shown as
text. pipeline/build_endings.py checks every position (legal, and won, drawn or mate as the text says, with the exact
tables or Stockfish), makes the positions of each kind, the lines to play along and the checkpoint answers, and writes
data/build/data_endings.json.

The house player's games (pipeline/scan_endings.py, data/endings_scan.json): 68 of 150 games reached an ending, 51 of
them with the house player winning, and 41 of those were won. The ten that got away: four on the clock, two with mate
on the back rank let in, a mate in one missed, a check that let a perpetual in, a rook skewer missed, a king that
walked into a knight fork, and two pawn endings (a pawn pushed when the king had to go).
"""

# The kinds, in the order the Endings tab shows them, group by group. goal: mate (play to mate), queen (promote and keep
# the win), hold (keep the draw for `hold` of your moves), win (a mate, a pawn queened, their king left alone, or from a
# start short of +8, the engine at +9). how: the exact table that judges it ('kqk', 'krk', 'kpk'), 'bare' (a lone king against two pieces: only a
# stalemate or a piece left to be taken throws it away), 'mate' (a mate to find: a move counts only while the mate is
# still there within the moves it should take) or 'engine'. idea: the pictures the tab shows before a game (a board,
# a heading, one line), checked by the build: every green arrow that is a move for the side to move must be a good one.
KINDS = [
  # ---- the mates every player needs
  dict(id='q', r=800, group='Mates', name='Queen mate', goal='mate', how='kqk', n=12, idea=[
    dict(fen='8/8/8/3k4/8/2Q5/8/4K3 b - - 0 1', arrows=['c3c8g', 'c3h3g'], h='Box the king in',
         t="Put the queen a knight's jump from the king. It holds a row and a file, and the king can't reach it."),
    dict(fen='7k/8/8/6Q1/8/2K5/8/8 b - - 0 1', circles=['h7y', 'h8y'], h='Stop at two squares',
         t='Once the king is down to two squares on the edge, stop squeezing: one more and it is stalemate.'),
    dict(fen='7k/6Q1/6K1/8/8/8/8/8 b - - 0 1', circles=['g7g'], h='The mate',
         t='The queen checks next to the king with your king guarding it.')]),
  dict(id='r', r=900, group='Mates', name='Rook mate', goal='mate', how='krk', n=12, idea=[
    dict(fen='8/8/3k4/8/7R/8/4K3/8 b - - 0 1', arrows=['h4a4g'], h='Cut the king off',
         t="The rook holds a row. Their king can't cross it."),
    dict(fen='8/8/3k4/8/3K3R/8/8/8 w - - 0 1', arrows=['h4h6g'], h='Check when the kings face each other',
         t='Kings face to face with one square between: a check on the row pushes their king back.'),
    dict(fen='3k4/8/3K4/8/8/8/8/7R w - - 0 1', arrows=['h1h8g'], h='The mate',
         t='On the edge with the kings face to face, the check on the last row mates.')]),
  dict(id='rr', r=700, group='Mates', name='Two rooks', goal='mate', how='bare', n=8, idea=[
    dict(fen='8/8/3k4/R7/8/8/8/1R2K3 w - - 0 1', arrows=['b1b6g'], h='The ladder',
         t='One rook holds a row, the other checks on the next one. The king steps back each time.'),
    dict(fen='3k4/R7/8/8/8/8/8/1R2K3 w - - 0 1', arrows=['b1b8g'], h='Mate on the edge',
         t='When the king reaches the edge, the next check mates. A rook the king comes at moves to the far end of its row.')]),
  dict(id='bb', r=1400, group='Mates', name='Two bishops', goal='mate', how='bare', n=8, idea=[
    dict(fen='8/8/8/3k4/8/2BB4/8/4K3 b - - 0 1', arrows=['c3h8b', 'd3h7b'], h='A wall of bishops',
         t="Side by side, the two bishops cover two diagonals the king can't cross."),
    dict(fen='7k/5B2/6K1/4B3/8/8/8/8 b - - 0 1', arrows=['e5h8g'], h='Mate in the corner',
         t='Your king comes close, one bishop takes the last free square and the other checks.')]),
  dict(id='bn', r=1900, group='Mates', name='Bishop and knight', goal='mate', how='bare', n=8, idea=[
    dict(fen='8/8/8/4k3/8/8/8/2K1NB2 w - - 0 1', circles=['a8g', 'h1g'], h='The right corner',
         t='The mate only works in a corner of your bishop\'s colour. Drive the king to one of those two.'),
    dict(fen='k7/3N4/1K6/3B4/8/8/8/8 b - - 0 1', arrows=['d5a8g'], h='The mate',
         t='Your king in front, the knight on the square next to the corner, the bishop checks along the diagonal.')]),
  # ---- named mating patterns: find the mate
  dict(id='br', r=900, group='Mating patterns', name='Back-rank mate', goal='win', how='engine', idea=[
    dict(fen='6k1/5ppp/8/8/8/8/5PPP/R5K1 w - - 0 1', arrows=['a1a8g'], h='The back-rank mate',
         t='A king behind its own pawns has no square. A rook check on the last row mates.'),
    dict(fen='r5k1/5ppp/8/8/8/8/5PPP/3R2K1 w - - 0 1', arrows=['h2h3g'], circles=['h2g'], h='Give your king air',
         t='One pawn step gives your king a square. Make it before your rook leaves the back row.')]),
  dict(id='smo', r=1000, group='Mating patterns', name='Smothered mate', goal='mate', how='mate', n=8, idea=[
    dict(fen='6rk/6pp/8/4N3/8/8/6PP/6K1 w - - 0 1', arrows=['e5f7g'], h='Smothered mate',
         t='The king is walled in by its own pieces. A knight check is mate.'),
    dict(fen='5r1k/6pp/7N/3Q4/8/8/6PP/6K1 w - - 0 1', arrows=['d5g8g', 'h6f7g'], h='Give the queen to close the wall',
         t='The queen checks on the corner square. The rook has to take it, and the knight mates.')]),
  dict(id='ana', r=1100, group='Mating patterns', name="Anastasia's mate", goal='mate', how='mate', n=8, idea=[
    dict(fen='5r2/4N1pk/8/8/8/3R4/6PP/6K1 w - - 0 1', arrows=['d3h3g'], circles=['g8b', 'g6b'], h="Anastasia's mate",
         t="The knight takes the squares beside the king, its own pawn the one in front. A rook check down the edge mates."),
    dict(fen='5r1k/4N1pp/8/7Q/8/3R4/6PP/6K1 w - - 0 1', arrows=['h5h7g', 'd3h3g'], h='Clear the edge first',
         t='The queen takes the pawn in front of the king with check. When the king takes back, the rook mates.')]),
  dict(id='ara', r=1000, group='Mating patterns', name='Arabian mate', goal='mate', how='mate', n=8, idea=[
    dict(fen='7k/1R6/5N2/8/8/8/6PP/6K1 w - - 0 1', arrows=['b7h7g'], h='Arabian mate',
         t='The rook checks next to the cornered king. The knight guards it and takes the other square.'),
    dict(fen='7k/1R6/8/p7/6N1/8/6PP/6K1 w - - 0 1', arrows=['g4f6g'], h='Bring the knight first',
         t='With the rook on the seventh row, the knight step leaves the king no square. The rook mates next.')]),
  dict(id='hook', r=1100, group='Mating patterns', name='Hook mate', goal='mate', how='mate', n=8, idea=[
    dict(fen='5k2/4R1pp/3N4/4P3/8/8/6PP/6K1 w - - 0 1', arrows=['e7e8g'], h='Hook mate',
         t='The rook checks beside the king, the knight guards the rook, and the pawn guards the knight.')]),
  dict(id='vuk', r=1200, group='Mating patterns', name="Vuković's mate", goal='mate', how='mate', n=8, idea=[
    dict(fen='4k3/R7/4NK2/8/8/8/8/8 w - - 0 1', arrows=['a7e7g'], circles=['d8b', 'f8b'], h="Vuković's mate",
         t='A rook check next to the king on the edge, guarded by your king. The knight takes the squares on both sides.')]),
  dict(id='bod', r=1200, group='Mating patterns', name="Boden's mate", goal='mate', how='mate', n=8, idea=[
    dict(fen='2kr4/p2n1ppp/8/8/5B2/8/PP2BPPP/6K1 w - - 0 1', arrows=['e2a6g'], circles=['b8b', 'c7b'], h="Boden's mate",
         t="Two bishops on crossing diagonals. The king's own rook and knight block it in."),
    dict(fen='2kr3r/pp1n1ppp/2p5/8/5B2/5Q2/PPP1BPPP/6K1 w - - 0 1', arrows=['f3c6g', 'e2a6g'], h='Open the diagonal',
         t='Give the queen on the pawn in front of the king. When a pawn takes it, the bishop mates.')]),
  dict(id='dbm', r=1100, group='Mating patterns', name='Double bishop mate', goal='mate', how='mate', n=8, idea=[
    dict(fen='r6k/7p/8/8/2B5/8/6PP/2B3K1 w - - 0 1', arrows=['c1b2g'], circles=['g8b'], h='Double bishop mate',
         t='One bishop checks down the long diagonal, the other takes the square next to the king.')]),
  dict(id='blk', r=1200, group='Mating patterns', name="Blackburne's mate", goal='mate', how='mate', n=8, idea=[
    dict(fen='5rk1/5p2/8/6N1/8/3B4/1B4PP/6K1 w - - 0 1', arrows=['d3h7g'], circles=['g7b', 'h8b'], h="Blackburne's mate",
         t='A bishop on the long diagonal holds the corner. The other bishop checks next to the king, guarded by the knight.')]),
  dict(id='mor', r=1100, group='Mating patterns', name="Morphy's mate", goal='mate', how='mate', n=8, idea=[
    dict(fen='7k/7p/8/8/8/4B3/PPP5/2K3R1 w - - 0 1', arrows=['e3d4g'], h="Morphy's mate",
         t='The rook holds the file next to the cornered king, its own pawn blocks the rest, and the bishop checks.'),
    dict(fen='5rk1/5ppp/5B2/8/8/6R1/5PPP/6K1 w - - 0 1', arrows=['g3g7g'], h='Open the long diagonal',
         t='The rook takes next to the king with check. Once the king is in the corner, the rook steps aside and the bishop mates.')]),
  dict(id='gre', r=1100, group='Mating patterns', name="Greco's mate", goal='mate', how='mate', n=8, idea=[
    dict(fen='7k/6p1/8/8/2B5/3R4/6PP/6K1 w - - 0 1', arrows=['d3h3g'], circles=['g8b'], h="Greco's mate",
         t='The bishop takes the square in front of the king, its own pawn blocks the other, and a rook mates on the edge.'),
    dict(fen='5r1k/6pp/8/5P1Q/2B5/3R4/6PP/6K1 w - - 0 1', arrows=['h5h7g', 'd3h3g'], h='Sacrifice on the edge first',
         t='The queen takes the pawn next to the king with check. After the king takes, the rook mates on that file.')]),
  dict(id='ope', r=1200, group='Mating patterns', name='Opera mate', goal='mate', how='mate', n=8, idea=[
    dict(fen='4kb1r/5ppp/8/6B1/8/8/5PPP/3R2K1 w - - 0 1', arrows=['d1d8g'], circles=['e7b'], h='Opera mate',
         t='A rook check on the back row, guarded by a bishop that also takes the square in front of the king.'),
    dict(fen='4kb1r/3n1ppp/4p3/6B1/8/1Q6/5PPP/2KR4 w - - 0 1', arrows=['b3b8g', 'd1d8g'], h='Pull the guard away',
         t='The queen check makes the knight take it, and that opens the file for the rook.')]),
  dict(id='epa', r=1000, group='Mating patterns', name='Epaulette mate', goal='mate', how='mate', n=8, idea=[
    dict(fen='3rkr2/pp4pp/8/8/8/1Q6/6PP/6K1 w - - 0 1', arrows=['b3e6g'], circles=['d7b', 'f7b'], h='Epaulette mate',
         t="The king's own rooks stand on both sides of it. A queen check from two squares in front mates.")]),
  dict(id='dam', r=1000, group='Mating patterns', name="Damiano's mate", goal='mate', how='mate', n=8, idea=[
    dict(fen='5rk1/5p2/6P1/8/8/8/5PP1/6KQ w - - 0 1', arrows=['h1h7g'], circles=['g6g'], h="Damiano's mate",
         t='A pawn guards the square next to the king. The queen goes there and mates.')]),
  dict(id='lol', r=1000, group='Mating patterns', name="Lolli's mate", goal='mate', how='mate', n=8, idea=[
    dict(fen='6k1/5p1p/5PpQ/8/8/8/5PPP/6K1 w - - 0 1', arrows=['h6g7g'], circles=['f6g'], h="Lolli's mate",
         t='A pawn deep in their camp guards the square in front of the king. The queen lands on it with mate.'),
    dict(fen='5rk1/5p1p/5Pp1/8/8/8/3Q1PPP/6K1 w - - 0 1', arrows=['d2h6g'], h='Bring the queen first',
         t='The queen step threatens the mate, and nothing stops it.')]),
  dict(id='kbx', r=1100, group='Mating patterns', name='Kill box mate', goal='mate', how='mate', n=8, idea=[
    dict(fen='1R6/7k/5Q2/8/8/8/6PP/6K1 w - - 0 1', arrows=['b8h8g'], h='Kill box mate',
         t='The rook checks next to the king and the queen guards it from one square away on the diagonal: the king is boxed in.')]),
  dict(id='bsw', r=1300, group='Mating patterns', name='Blind swine mate', goal='mate', how='mate', n=8, idea=[
    dict(fen='5rk1/1RR3pp/8/8/8/8/6PP/6K1 w - - 0 1', arrows=['c7g7g'], h='Two rooks on the seventh',
         t='Doubled on the seventh row, the rooks take the pawns in front of the king with check until it has no square.')]),
  # ---- king and pawn
  dict(id='kp', r=1000, group='Pawn endings', name='King and pawn', goal='queen', how='kpk', n=12, idea=[
    dict(fen='8/4k3/8/8/4P3/8/4K3/8 w - - 0 1', circles=['d6g', 'e6g', 'f6g'], h='The key squares',
         t='Get your king to one of the three squares two rows in front of the pawn, and the pawn queens.'),
    dict(fen='8/8/4k3/8/3K4/4P3/8/8 w - - 0 1', arrows=['d4e4g', 'e3e4r'], h='King first',
         t='Step the king up and take the opposition (green). The pawn push (red) lets their king stand in front of it.')]),
  dict(id='kpd', r=1100, group='Pawn endings', name='Stop the pawn', goal='hold', how='kpk', n=10, hold=10, idea=[
    dict(fen='8/8/8/4k3/P7/8/8/7K b - - 0 1', arrows=['a4a8b', 'a4e8b'], h='The square of the pawn',
         t='Draw the square from the pawn to the last row. A king that can step into it catches the pawn.'),
    dict(fen='4k3/8/8/4K3/4P3/8/8/8 b - - 0 1', arrows=['e8e7g'], h='Keep the opposition',
         t='In front of the pawn, keep your king facing theirs with one square between. Then their king has to give way.')]),
  dict(id='opp', r=1200, group='Pawn endings', name='The opposition', goal='queen', how='kpk', n=10, idea=[
    dict(fen='8/8/4k3/8/4K3/4P3/8/8 b - - 0 1', circles=['e5y'], h='The opposition',
         t='Kings face to face with one square between: the side that has to move gives way.'),
    dict(fen='2k5/8/8/8/8/1K2P3/8/8 w - - 0 1', arrows=['b3c4g'], circles=['c5y', 'c6y', 'c7y'], h='From afar',
         t='Three squares between the kings works the same way. Take it from afar and their king has to give way first.')]),
  dict(id='rpk', r=1100, group='Pawn endings', name='The edge pawn', goal='hold', how='kpk', n=10, hold=8, idea=[
    dict(fen='k7/8/K7/P7/8/8/8/8 w - - 0 1', circles=['a8r'], h='The edge pawn',
         t='With a pawn on the edge, a king that gets to the corner holds the draw.'),
    dict(fen='8/8/8/2k5/7P/5K2/8/8 b - - 0 1', arrows=['c5d6g'], circles=['h8g'], h='Run for the corner',
         t='Head straight for the corner in front of the pawn, or for the squares beside it.')]),
  dict(id='race', r=1300, group='Pawn endings', name='Races', goal='win', how='engine', idea=[
    dict(fen='8/7p/5K2/1p6/8/PPk5/2P5/8 w - - 1 42', arrows=['f6g5g', 'a3a4r'], h='Count the race',
         t='Count the moves each side needs. Here your king had to go and take their last pawn (green).')]),
  dict(id='bt', r=1400, group='Pawn endings', name='Breakthrough', goal='queen', how='engine', idea=[
    dict(fen='7k/ppp5/8/PPP5/8/8/8/7K w - - 0 1', arrows=['b5b6g'], h='The breakthrough',
         t='Three pawns against three: give one, and another of yours runs through.')]),
  dict(id='tri', r=1700, group='Pawn endings', name='Triangulation', goal='win', how='engine', n=8, idea=[
    dict(fen='8/1p1k4/1P6/2PK4/8/8/8/8 w - - 0 1', circles=['d5g', 'e5g', 'd4g'], h='Triangulation',
         t='Your king has three squares where theirs has two. Walk the triangle, and the same position comes back with them to move.'),
    dict(fen='8/1p1k4/1P6/2PK4/8/8/8/8 w - - 0 1', arrows=['c5c6r'], h="Don't push yet",
         t='The pawn push lets their king block it. Win the move first, then walk in.')]),
  dict(id='reti', r=1800, group='Pawn endings', name='The Réti manoeuvre', goal='hold', how='engine', n=4, hold=8, idea=[
    dict(fen='7K/8/k1P5/7p/8/8/8/8 w - - 0 1', arrows=['h8g7g', 'g7f6g'], h='Two jobs at once',
         t='Walk the diagonal: the king closes in on their pawn and on your own at the same time.')]),
  # ---- passed pawns
  dict(id='out', r=1300, group='Passed pawns', name='Outside passed pawn', goal='win', how='engine', n=8, idea=[
    dict(fen='8/5p1p/4k1p1/8/P7/4K1P1/5P1P/8 w - - 0 1', arrows=['a4a5g'], h='The outside passed pawn',
         t='A passed pawn far from the kings pulls their king away. Then yours takes the other pawns.')]),
  dict(id='pro', r=1400, group='Passed pawns', name='Protected passed pawn', goal='win', how='engine', n=8, idea=[
    dict(fen='8/5p1p/6p1/3k4/1P6/2P2K2/5P1P/8 w - - 0 1', arrows=['f3g4g'], circles=['b4g'], h='The protected passed pawn',
         t='A passed pawn guarded by a pawn keeps their king busy for good. Your king walks over and takes the other wing.')]),
  dict(id='con', r=1500, group='Passed pawns', name='Two pawns against a rook', goal='queen', how='engine', n=8, idea=[
    dict(fen='8/2K5/8/3PP3/8/8/1r6/6k1 w - - 0 1', arrows=['e5e6g'], h='Two pawns against a rook',
         t='Two pawns side by side, far from their king, can beat a rook. Push the front one and keep them together.')]),
  dict(id='tar', r=1500, group='Passed pawns', name='Rook behind the passed pawn', goal='win', how='engine', n=8, idea=[
    dict(fen='r2k4/6p1/5p1p/P7/8/4KP2/R5PP/8 w - - 0 1', arrows=['a5a6g'], circles=['a2g', 'a8r'], h='Behind the passed pawn',
         t='Your rook behind your passed pawn gets stronger with every push. Theirs in front of it only gets more stuck.')]),
  # ---- rook endings
  dict(id='luc', r=1400, group='Rook endings', name='Lucena', goal='queen', how='engine', n=6, idea=[
    dict(fen='3K4/3P2k1/8/8/5R2/8/2r5/8 b - - 0 1', arrows=['d8e7g'], circles=['f4g'], h='Build a bridge',
         t='Rook to the fourth row first. Then your king walks out, and when the checks run out the rook blocks them.')]),
  dict(id='phi', r=1500, group='Rook endings', name='Philidor', goal='hold', how='engine', n=6, hold=10, idea=[
    dict(fen='4k3/7R/r7/4P3/4K3/8/8/8 b - - 0 1', me='b', circles=['a6g', 'b6g', 'c6g', 'd6g', 'e6g', 'f6g', 'g6g'], h='Hold the third row',
         t="Defending, keep your rook on your third row so their king can't come up."),
    dict(fen='4k3/7R/r3P3/4K3/8/8/8/8 b - - 0 1', me='b', arrows=['a6a1g'], h='Then check from behind',
         t='Once their pawn steps up, your rook goes to the far end and checks from behind.')]),
  dict(id='cut', r=1300, group='Rook endings', name='King cut off', goal='queen', how='engine', n=6, idea=[
    dict(fen='r7/8/6k1/8/3P4/8/3K4/4R3 b - - 0 1', arrows=['e1e8g'], h='Cut the king off',
         t='Your rook on the file between the kings keeps their king away from your pawn.')]),
  dict(id='van', r=1800, group='Rook endings', name='Vančura', goal='hold', how='engine', n=8, hold=8, idea=[
    dict(fen='R7/2r3k1/P7/8/3K4/8/8/8 b - - 0 1', me='b', arrows=['c7c6g'], h='Hit the pawn from the side',
         t='Against a rook in front of its edge pawn, attack the pawn from the side and keep your king near the other corner.')]),
  dict(id='ssd', r=1800, group='Rook endings', name='Short side defence', goal='hold', how='engine', n=8, hold=8, idea=[
    dict(fen='7k/4K3/r4P2/8/8/8/1R6/8 b - - 0 1', me='b', arrows=['a6a7g'], h='Check from the long side',
         t='Your king on the short side of the pawn, your rook on the long side: from far away its checks never run out.')]),
  dict(id='rp', r=1600, group='Rook endings', name='Rook against pawn', goal='win', how='engine', n=8, idea=[
    dict(fen='8/8/6R1/8/8/kp6/5K2/8 w - - 0 1', arrows=['g6a6g'], h='Push the king off the pawn',
         t='Use the rook to keep their king away from the pawn while yours comes back to take it.')]),
  dict(id='r7', r=1500, group='Rook endings', name='Rook on the seventh', goal='win', how='engine', n=8, idea=[
    dict(fen='3r2k1/1R3ppp/p7/8/8/6P1/5P1P/6K1 w - - 0 1', arrows=['b7a7g'], h='Rook on the seventh',
         t='On the seventh row your rook takes pawns from the side and keeps their king on its back row.')]),
  # ---- minor pieces
  dict(id='wb', r=1500, group='Minor pieces', name='The wrong bishop', goal='hold', how='engine', n=8, hold=8, idea=[
    dict(fen='8/8/4k3/P7/8/2B5/7K/8 b - - 0 1', me='b', arrows=['e6d7g'], circles=['a8g'], h='The wrong bishop',
         t="An edge pawn and a bishop that can't cover the corner: get your king into that corner and it is a draw.")]),
  dict(id='np', r=1700, group='Minor pieces', name='Knight against pawn', goal='hold', how='engine', n=8, hold=8, idea=[
    dict(fen='8/8/8/8/3k4/8/1K1p4/6N1 w - - 0 1', arrows=['g1f3g'], circles=['d1g'], h='Knight against pawn',
         t='The knight stops a pawn by guarding a square in front of it. Check first when the king would cover that square.')]),
  dict(id='stm', r=1800, group='Minor pieces', name="Stamma's mate", goal='mate', how='mate', n=6, idea=[
    dict(fen='8/8/8/N7/8/p7/8/k2K4 w - - 0 1', arrows=['d1c2g'], h="Stamma's mate",
         t='A king stuck in front of its own edge pawn can be mated by a king and knight. Box it in, then the knight checks.')]),
  # ---- queens
  dict(id='qp', r=1500, group='Queen endings', name='Queen against a pawn', goal='win', how='engine', n=6, idea=[
    dict(fen='8/8/8/8/5Q2/6K1/3p4/3k4 w - - 0 1', arrows=['g3f2g'], h='Check it into the way',
         t='Check until their king has to stand in front of its pawn. Then bring your king one step closer.')]),
  dict(id='qpd', r=1800, group='Queen endings', name='Queen against an edge pawn', goal='hold', how='engine', n=8, hold=8, idea=[
    dict(fen='8/2K5/8/8/8/k7/p7/7Q b - - 0 1', me='b', arrows=['a3b2g'], h='The stalemate trick',
         t='With a bishop or rook pawn on the seventh, hide your king beside it: taking the pawn would be stalemate.')]),
  dict(id='qr', r=2000, group='Queen endings', name='Queen against rook', goal='mate', how='engine', n=8, idea=[
    dict(fen='2rk4/6K1/Q7/8/8/8/8/8 w - - 0 1', arrows=['a6d6g'], h='Fork the rook',
         t="Push their king to the edge, then look for the check that also hits the rook. A rook that strays from its king is lost.")]),
  dict(id='mine', r=1200, group='From your games', name='Your endings', goal='win', how='engine'),
]

# Named mating patterns: the positions the build starts from, each a mate in one, two or three for the side to move,
# with one first move that mates in time. The build turns each one around (mirrored, and with the colours swapped),
# adds a few pawns away from the king, and keeps the ones Stockfish says still have that one quickest mate.
PATTERNS = {
  'smo': ['6rk/6pp/8/4N3/8/8/6PP/6K1 w - - 0 1', '5r1k/6pp/7N/3Q4/8/8/6PP/6K1 w - - 0 1', '5rk1/5Npp/8/8/8/1Q6/6PP/6K1 w - - 0 1'],
  'ana': ['5r2/4N1pk/8/8/8/3R4/6PP/6K1 w - - 0 1', '5r1k/4N1pp/8/7Q/8/3R4/6PP/6K1 w - - 0 1'],
  'ara': ['7k/1R6/5N2/8/8/8/6PP/6K1 w - - 0 1', '7k/1R6/8/p7/6N1/8/6PP/6K1 w - - 0 1'],
  'hook': ['5k2/4R1pp/3N4/4P3/8/8/6PP/6K1 w - - 0 1', '5k2/6pp/3N4/2P5/8/8/6PP/4R1K1 w - - 0 1'],
  'vuk': ['4k3/R7/4NK2/8/8/8/8/8 w - - 0 1', '4k3/R7/5K2/8/3N4/8/8/8 w - - 0 1'],
  'bod': ['2kr4/p2n1ppp/8/8/5B2/8/PP2BPPP/6K1 w - - 0 1', '2kr3r/pp1n1ppp/2p5/8/5B2/5Q2/PPP1BPPP/6K1 w - - 0 1'],
  'dbm': ['r6k/7p/8/8/2B5/8/6PP/2B3K1 w - - 0 1'],
  'blk': ['5rk1/5p2/8/6N1/8/3B4/1B4PP/6K1 w - - 0 1'],
  'mor': ['7k/7p/8/8/8/4B3/PPP5/2K3R1 w - - 0 1', '5rk1/5ppp/5B2/8/8/6R1/5PPP/6K1 w - - 0 1'],
  'gre': ['7k/6p1/8/8/2B5/3R4/6PP/6K1 w - - 0 1', '5r1k/6pp/8/5P1Q/2B5/3R4/6PP/6K1 w - - 0 1'],
  'ope': ['4kb1r/5ppp/8/6B1/8/8/5PPP/3R2K1 w - - 0 1', '4kb1r/3n1ppp/4p3/6B1/8/1Q6/5PPP/2KR4 w - - 0 1'],
  'epa': ['3rkr2/pp4pp/8/8/8/1Q6/6PP/6K1 w - - 0 1'],
  'dam': ['5rk1/5p2/6P1/8/8/8/5PP1/6KQ w - - 0 1'],
  'lol': ['6k1/5p1p/5PpQ/8/8/8/5PPP/6K1 w - - 0 1', '5rk1/5p1p/5Pp1/8/8/8/3Q1PPP/6K1 w - - 0 1'],
  'kbx': ['1R6/7k/5Q2/8/8/8/6PP/6K1 w - - 0 1'],
  'bsw': ['5rk1/1RR3pp/8/8/8/8/6PP/6K1 w - - 0 1'],
}

# Endings made from a few classic positions turned around (and, for triangulation, moved along the board), each kept
# only when Stockfish agrees.
VARIANTS = {
  'tri': ['8/1p1k4/1P6/2PK4/8/8/8/8 w - - 0 1'],
  'reti': ['7K/8/k1P5/7p/8/8/8/8 w - - 0 1'],
}

# Positions given by hand, kind by kind. The side to move is the player. Each is checked by the build.
FIXED = {
  'br': [
    '6k1/5ppp/8/8/8/8/r4PPP/1R4K1 w - - 0 1',            # mate on the last row
    '2r3k1/5ppp/8/8/8/8/3R1PPP/3R2K1 w - - 0 1',          # doubled rooks: the first check is taken, the second mates
    'r5k1/5ppp/8/8/8/8/1Q3PPP/1R4K1 w - - 0 1',           # queen and rook: the queen check is taken, the rook mates
    '6k1/1R3ppp/8/8/8/8/r4PPP/6K1 w - - 0 1',             # rook on the seventh
    '3r2k1/1RB2ppp/1p2p3/b2p4/3P4/4P2P/5PPK/r7 b - - 7 29',   # your game: keep your back row covered
    '3r2k1/5p2/R3bBp1/7p/1KP4P/1P4P1/8/1r6 b - - 1 34',       # your game: keep your back row covered
  ],
  'race': [
    '8/7p/5K2/1p6/8/PPk5/2P5/8 w - - 1 42',               # your game: the king has to go and take the last pawn
    '8/2p2p2/8/p1pk3p/5p1P/1PK2P2/P4P2/8 b - - 1 32',     # your game: the king leads, not the pawn
    '8/5p1p/4k1p1/8/P7/4K1P1/5P1P/8 w - - 0 1',           # the outside passed pawn
    '8/5pk1/6p1/7p/7P/6P1/1p3PK1/8 b - - 0 1',
  ],
  'bt': [
    '7k/ppp5/8/PPP5/8/8/8/7K w - - 0 1',
    'k7/5ppp/8/5PPP/8/8/8/K7 w - - 0 1',
    '7k/8/ppp5/8/PPP5/8/8/K7 w - - 0 1',
  ],
}

# Positions from the house player's own games (pipeline/scan_endings.py), the position before the move that let the
# win go, with the house player to move. key: date and opponent. why: one line about what happened.
MINE = [
  dict(key='2026.07.09 gfrasti', fen='8/p2R4/1p3p1p/2p5/1P1R2P1/4kPK1/2r4P/8 w - - 0 40', why='The other rook gave check and the king took the rook that had the mate.'),
  dict(key='2026.07.13 Datmo', fen='3r2k1/1RB2ppp/1p2p3/b2p4/3P4/4P2P/5PPK/r7 b - - 7 29', why='One rook move let a mate in on your back row.'),
  dict(key='2026.07.09 TiepiMT', fen='3r2k1/5p2/R3bBp1/7p/1KP4P/1P4P1/8/1r6 b - - 1 34', why='One rook move let a mate in on your back row.'),
  dict(key='2026.10.14 abood_almuss', fen='Q7/5p1p/4pBpk/1p2Pq2/1P3P2/2p5/5PKP/8 w - - 3 37', why='A queen check let the other queen check forever.'),
  dict(key='2026.07.09 TheLuisGambit25', fen='8/8/4b2R/p1r2k2/K7/1P6/P7/8 w - - 7 78', why='A rook check would have won the rook behind the king.'),
  dict(key='2026.07.11 quzibek', fen='8/p3k1pp/1pN5/8/P7/1b4P1/5K1P/8 b - - 0 34', why='The king stepped into a knight fork.'),
  dict(key='2026.07.12 zz_ny', fen='8/7p/5K2/1p6/8/PPk5/2P5/8 w - - 1 42', why='A pawn push let their king take your pawns. Your king had to come back first.'),
  dict(key='2026.10.14 Eschoir', fen='8/2p2p2/8/p1pk3p/5p1P/1PK2P2/P4P2/8 b - - 1 32', why='A pawn step instead of a king step threw the win away.'),
  dict(key='2026.07.10 steny35', fen='8/p1k3p1/p4p1p/4rp1P/3N4/b1PK4/P1P2PP1/1R6 w - - 6 30', why='The pawn took one step where two would have hit the rook.'),
]

# The course, in the order this player needs it. Each unit: slides to learn from (a board, a heading, one line),
# lines to play along (moves given, or 'method': worked out by the build from the tables), the kinds its practice
# positions come from (`practice`, with how many to win clean: `need`) and its checkpoint (positions with one point
# to find: `ask` is the question; the build works out the answers).
UNITS = [
  dict(id='eg-r', title='The rook mate', kinds=['r'], need=3,
       why='You had mate in one with a rook and played a check that lost it.',
       slides=['r',
         dict(fen='8/p2R4/1p3p1p/2p5/1P1R2P1/4kPK1/2r4P/8 w - - 0 40', arrows=['d4e4g', 'd7e7r'], h='Your game: look for mate first',
              t='The rook check beside their king was mate (green): your pawn guards the rook, and your other rook takes the squares behind. The check you played (red) let the king take a rook.'),
       ],
       along=[dict(fen='8/8/2k5/8/8/8/8/R3K3 w - - 0 1', method=True)],
       check=[
         dict(fen='8/p2R4/1p3p1p/2p5/1P1R2P1/4kPK1/2r4P/8 w - - 0 40', ask='Your game. Find the mate.'),
         dict(gen='krk-mate1', n=2, ask='Find the mate.'),
         dict(gen='krk-box', n=2, ask='Shrink the box: the rook move that leaves their king the fewest squares.'),
       ]),
  dict(id='eg-back', title='Your back rank', kinds=['br'], need=3,
       why='Twice a rook move off your back row let a mate in.',
       slides=[
         dict(fen='6k1/5ppp/8/8/8/8/5PPP/R5K1 w - - 0 1', arrows=['a1a8g'], h='The back-rank mate',
              t='A king behind its own pawns has no square. A rook check on the last row mates.'),
         dict(fen='r5k1/5ppp/8/8/8/8/5PPP/3R2K1 w - - 0 1', arrows=['h2h3g'], circles=['h2g'], h='Give your king air',
              t='One pawn step gives your king a square. Make it before your rook leaves the back row.'),
         dict(fen='3r2k1/5p2/R3bBp1/7p/1KP4P/1P4P1/8/1r6 b - - 1 34', me='b', arrows=['d8d3r', 'a6a8r'], h='Your game: check their checks',
              t='Your rook left the back row (red) and their rook came in with mate.'),
         dict(fen='6k1/5ppp/8/8/8/8/r4PPP/1R4K1 w - - 0 1', arrows=['b1b8g'], h='Use it yourself',
              t='Their king stuck behind its pawns? Look at the check on the last row first.'),
       ],
       along=[],
       check=[
         dict(fen='3r2k1/1RB2ppp/1p2p3/b2p4/3P4/4P2P/5PPK/r7 b - - 7 29', ask='Your game. Keep the win: mind your back row.'),
         dict(fen='3r2k1/5p2/R3bBp1/7p/1KP4P/1P4P1/8/1r6 b - - 1 34', ask='Your game. Keep the win: mind your back row.'),
         dict(fen='6k1/5ppp/8/8/8/8/r4PPP/1R4K1 w - - 0 1', ask='Find the mate.'),
         dict(fen='2r3k1/5ppp/8/8/8/8/3R1PPP/3R2K1 w - - 0 1', ask='Find the mate in two.'),
       ]),
  dict(id='eg-kp', title='King and pawn', kinds=['kp', 'kpd', 'pzz'], need=3,
       why='Two of your pawn endings got away. Every pawn ending ends up here.',
       slides=['kp', 'kpd',
         dict(fen='k7/8/K7/P7/8/8/8/8 w - - 0 1', me='b', circles=['a8r'], h='The edge pawn',
              t="An edge pawn is the exception. If the defending king reaches the corner in front of it, it is a draw: nothing can drive it out without stalemate."),
       ],
       along=[dict(gen='kpk-demo', method=True)],
       check=[
         dict(gen='kpk-only', n=2, ask='Find the move that wins.'),
         dict(kind='pzz', band=True),
         dict(kind='pzz', band=True),
         dict(gen='kpk-hold', n=1, ask='Find the move that holds the draw.'),
       ]),
  dict(id='eg-race', title='Pawn races', kinds=['race', 'bt', 'pzr'], need=3,
       why='Two pawn endings slipped on one move each: a pawn pushed where the king had to go.',
       slides=['race', 'out', 'bt'],
       along=[dict(fen='8/5p1p/4k1p1/8/P7/4K1P1/5P1P/8 w - - 0 1', pv=16)],
       check=[
         dict(fen='8/7p/5K2/1p6/8/PPk5/2P5/8 w - - 1 42', ask='Your game. Find the move that wins the race.',
              why='Their pawn is slow: your king can catch it later. It comes back for your pawns first.'),
         dict(fen='8/2p2p2/8/p1pk3p/5p1P/1PK2P2/P4P2/8 b - - 1 32', ask='Your game. Keep the win.',
              why='Your king walks to the queenside, where you have three pawns to two.'),
         dict(fen='7k/ppp5/8/PPP5/8/8/8/7K w - - 0 1', ask='Find the breakthrough.', ok=['b5b6'],
              why='Push the middle pawn. Whichever pawn takes, the other outside pawn goes, and one of yours runs through.'),
         dict(kind='pzr', band=True),
       ]),
  dict(id='eg-checks', title='Checks, forks and skewers', kinds=['mine'], need=3,
       why='Three won endings slipped on one move: a check that let theirs in, a skewer missed and a knight fork.',
       slides=[
         dict(fen='Q7/5p1p/4pBpk/1p2Pq2/1P3P2/2p5/5PKP/8 w - - 3 37', arrows=['f6g5g', 'a8f8r'], h='Your game: count their checks',
              t='Your queen check (red) let their queen check forever. The bishop check (green) wins.'),
         dict(fen='8/8/4b2R/p1r2k2/K7/1P6/P7/8 w - - 7 78', arrows=['h6h5g'], circles=['c5r'], h='Your game: the skewer',
              t='The check on the row the king shares with their rook: the king steps away and the rook behind it falls.'),
         dict(fen='8/p3k1pp/1pN5/8/P7/1b4P1/5K1P/8 b - - 0 34', me='b', arrows=['e7e6r', 'c6d4r'], h='Your game: the knight fork',
              t='The king step (red) walked into a knight check that also hit the bishop.'),
       ],
       along=[],
       check=[
         dict(fen='Q7/5p1p/4pBpk/1p2Pq2/1P3P2/2p5/5PKP/8 w - - 3 37', ask='Your game. Find the move that keeps the win.'),
         dict(fen='8/8/4b2R/p1r2k2/K7/1P6/P7/8 w - - 7 78', ask='Your game. Find the move that wins the rook.'),
         dict(fen='8/p3k1pp/1pN5/8/P7/1b4P1/5K1P/8 b - - 0 34', ask='Your game. Keep the win: mind the knight.'),
       ]),
  dict(id='eg-q', title='The queen mate', kinds=['q'], need=3,
       why='Four won endings ran out of time. A mate you can play without thinking saves the clock.',
       slides=['q'],
       along=[dict(fen='8/8/8/3k4/8/8/8/Q3K3 w - - 0 1', method=True)],
       check=[
         dict(gen='kqk-mate1', n=2, ask='Find the mate.'),
         dict(gen='kqk-mate1s', n=3, ask='Find the mate. Careful: some queen moves are stalemate.'),
       ]),
  dict(id='eg-rook', title='Rook endings', kinds=['luc', 'phi', 'cut', 'pzk'], need=3,
       why='Every rook ending with one pawn left heads for one of two positions.',
       slides=['cut', 'luc', 'phi',
         dict(fen='6k1/8/r7/P7/8/8/6K1/R7 w - - 0 1', circles=['a1g', 'a6r'], h='Rook behind the passed pawn',
              t='Rooks go behind passed pawns: behind yours to push it, behind theirs to stop it.'),
       ],
       along=[dict(fen='3K4/3P1k2/8/8/8/8/2r5/4R3 w - - 0 1', moves='e1f1 f7g7 f1f4 c2c1 d8e7 c1e1 e7d6 e1d1 d6e6 d1e1 e6d5 e1d1 f4d4')],
       check=[
         dict(fen='3K4/3P2k1/8/8/8/8/2r5/5R2 w - - 0 1', ask='Lucena. Find the move that builds the bridge.', ok=['f1f4'],
              why='Rook to the fourth row: when your king walks out, it blocks the checks there.'),
         dict(fen='4k3/7R/r3P3/4K3/8/8/8/8 b - - 0 1', ask='Philidor. Find the move that holds the draw.',
              why='Their pawn has stepped up, so your rook goes to the far end and checks from behind.'),
         dict(kind='pzk', band=True),
       ]),
]

# The basics: units after the ones made from the games, in the same format. `slides` names kinds (their idea pictures
# are the unit's pictures) or gives pictures; a checkpoint entry with `kind` takes a position of that kind (`par`: a
# mate in that many) and the build writes the question; `sfline` plays Stockfish's line for both sides to the mate.
LIB = [
  dict(id='eg-knm', title='Knight mates', kinds=['smo', 'ana', 'ara', 'hook', 'vuk'], need=3,
       why="Mates where the knight takes the squares the other pieces can't.",
       slides=['smo', 'ana', 'ara', 'hook', 'vuk'],
       along=[dict(fen='5rk1/5Npp/8/8/8/1Q6/6PP/6K1 w - - 0 1', moves='f7h6 g8h8 b3g8 f8g8 h6f7')],
       check=[dict(kind='smo', band=True), dict(kind='ana', band=True), dict(kind='ara', band=True), dict(kind='hook', band=True), dict(kind='vuk', par=1)]),
  dict(id='eg-bim', title='Bishop mates', kinds=['bod', 'dbm', 'blk', 'mor', 'gre'], need=3,
       why='Mates along the diagonals, often with a sacrifice to open one.',
       slides=['bod', 'dbm', 'blk', 'mor', 'gre'],
       along=[dict(fen='2kr3r/pp1n1ppp/2p5/8/5B2/5Q2/PPP1BPPP/6K1 w - - 0 1', moves='f3c6 b7c6 e2a6')],
       check=[dict(kind='bod', band=True), dict(kind='mor', par=2), dict(kind='gre', par=2), dict(kind='dbm', band=True), dict(kind='blk', par=1)]),
  dict(id='eg-hvm', title='Queen and rook mates', kinds=['ope', 'epa', 'dam', 'lol', 'kbx', 'bsw', 'dov'], need=3,
       why='Mates on the edge with the heavy pieces.',
       slides=['ope', 'epa', 'dam', 'lol', 'kbx', 'bsw', 'dov'],
       along=[dict(fen='5rk1/1RR3pp/8/8/8/8/6PP/6K1 w - - 0 1', moves='c7g7 g8h8 g7h7 h8g8 b7g7')],
       check=[dict(kind='ope', par=2), dict(kind='lol', par=2), dict(kind='epa', par=1), dict(kind='kbx', par=1), dict(kind='bsw', par=3), dict(kind='dov', band=True)]),
  dict(id='eg-2b', title='Two bishops', kinds=['bb'], need=3,
       why='Two diagonals side by side push the king into a corner.',
       slides=['bb'],
       along=[dict(fen='8/8/8/4k3/8/8/2BB4/4K3 w - - 0 1', sfline=True)],
       check=[dict(gen='kbbk-mate1', n=3, ask='Find the mate.')]),
  dict(id='eg-bnm', title='Bishop and knight', kinds=['bn'], need=2,
       why="The hardest of the basic mates: find the right corner and drive the king to it.",
       slides=['bn'],
       along=[dict(fen='6k1/8/5K2/8/8/8/3N4/2B5 w - - 0 1', sfline=True)],
       check=[dict(gen='kbnk-mate1', n=3, ask='Find the mate.')]),
  dict(id='eg-opp', title='Opposition and the edge pawn', kinds=['opp', 'rpk', 'kpd', 'pzz'], need=3,
       why='Which king has to give way decides most pawn endings.',
       slides=['opp', 'kpd', 'rpk', 'pzz'],
       along=[dict(fen='2k5/8/8/8/8/1K2P3/8/8 w - - 0 1', method=True)],
       check=[dict(gen='kpk-only', n=2, ask='Find the move that wins.'), dict(gen='kpk-edge', n=2, ask='Find the move that holds the draw.'), dict(kind='pzz', band=True)]),
  dict(id='eg-tri', title='Triangulation and the Réti', kinds=['tri', 'reti'], need=2,
       why='Two king walks that win a move or save a lost-looking pawn ending.',
       slides=['tri', 'reti'],
       along=[dict(fen='7K/8/k1P5/7p/8/8/8/8 w - - 0 1', pv=10)],
       check=[dict(kind='reti', ask='Find the move that holds the draw.'), dict(kind='tri', ask='Find the move that wins.')]),
  dict(id='eg-pas', title='Passed pawns', kinds=['out', 'pro', 'con', 'tar', 'pzr'], need=3,
       why='Make one, guard it, and put a rook behind it.',
       slides=['out', 'pro', 'con', 'tar', 'pzr'],
       along=[],
       check=[dict(kind='con', ask='Find the move that wins.'), dict(kind='tar', ask='Find the move that keeps the win.'), dict(kind='pro', ask='Find the move that keeps the win.'), dict(kind='pzr', band=True)]),
  dict(id='eg-rkh', title='Rook endings: hold and win', kinds=['van', 'ssd', 'rp', 'r7', 'pzk'], need=3,
       why='The defences rook endings come down to, and the rook against a lone pawn.',
       slides=['van', 'ssd', 'rp', 'r7', 'pzk'],
       along=[],
       check=[dict(kind='van', ask='Find the move that holds the draw.'), dict(kind='ssd', ask='Find the move that holds the draw.'), dict(kind='rp', ask='Find the move that wins.'), dict(kind='pzk', band=True)]),
  dict(id='eg-min', title='Minor pieces', kinds=['wb', 'np', 'stm', 'pzm'], need=3,
       why='Bishops and knights against pawns: what holds and what mates.',
       slides=['wb', 'np', 'stm', 'pzm'],
       along=[dict(fen='8/8/8/N7/8/p7/8/k2K4 w - - 0 1', sfline=True)],
       check=[dict(kind='wb', ask='Find the move that holds the draw.'), dict(kind='np', ask='Find the move that holds the draw.'), dict(kind='stm', ask='Find the first move of the mate.'), dict(kind='pzm', band=True)]),
  dict(id='eg-qen', title='Queen endings', kinds=['qp', 'qpd', 'qr', 'pzq'], need=3,
       why='When a queen wins, and when a pawn on the seventh holds it off.',
       slides=['qp', 'qpd', 'qr', 'pzq'],
       along=[],
       check=[dict(kind='qpd', ask='Find the move that holds the draw.'), dict(kind='qr', ask='Find the move that wins the rook.'), dict(kind='pzq', band=True)]),
]


# ---------------------------------------------------------------- the manual
# Every kind's pictures, written as a manual: the plan, then each step with its board, then what to watch for. A
# picture's lines are short sentences, shown one bullet each. They replace the shorter ideas above (the build checks
# the first green arrow of every picture the same way).
MANUAL = {
  # ---- the basic mates
  'q': [
    dict(fen='8/8/8/3k4/8/8/8/Q3K3 w - - 0 1', h='The plan',
         t="Box the king in with your queen. Squeeze it to the edge. Then bring your king, and mate. The queen can't mate alone: your king has to help."),
    dict(fen='8/8/8/3k4/8/2Q5/8/4K3 b - - 0 1', arrows=['c3c8b', 'c3h3b'], h="1. A knight's jump away",
         t="Put your queen a knight's jump from their king. Its row and its file fence the king into one part of the board. From there the king can never attack the queen."),
    dict(fen='8/8/4k3/8/8/2Q5/8/4K3 w - - 0 1', arrows=['c3d4g'], h='2. Follow the king',
         t="Each time the king steps, put the queen a knight's jump away again. Every such move makes the box smaller. Don't give check: checks let the king out."),
    dict(fen='7k/8/8/6Q1/8/2K5/8/8 b - - 0 1', circles=['h7y', 'h8y'], h='3. Stop at two squares',
         t="Once the king is on the edge with two squares left, stop squeezing. One more square taken is stalemate, and only a draw."),
    dict(fen='7k/8/8/6Q1/3K4/8/8/8 w - - 0 1', arrows=['d4e5g'], circles=['f7y', 'g6y'], h='4. Bring your king',
         t="Walk your king over while theirs steps between its two squares. Head for one of the squares a knight's jump from their corner."),
    dict(fen='7k/6Q1/6K1/8/8/8/8/8 b - - 0 1', circles=['g7g'], h='5. Mate',
         t="Mate comes with the queen next to their king, guarded by yours. Or along the edge, with your king facing theirs."),
    dict(fen='k7/2K5/8/1Q6/8/8/8/8 w - - 0 1', arrows=['b5b7g', 'b5b6r'], h='Watch for stalemate',
         t="Before every queen move, ask: will their king still have a move, or is it check? If neither, it is stalemate."),
  ],
  'r': [
    dict(fen='8/8/2k5/8/8/8/8/R3K3 w - - 0 1', h='The plan',
         t="Your rook cuts the king off along a row. Your king walks up to face theirs. Then a check pushes it back one row. Again and again, until the check on the edge is mate."),
    dict(fen='8/8/3k4/8/7R/8/4K3/8 b - - 0 1', arrows=['h4a4b'], h='1. Cut the king off',
         t="The rook holds a row their king can't cross. Keep the rook far from their king so it can't be attacked."),
    dict(fen='8/8/3k4/8/7R/8/3K4/8 w - - 0 1', arrows=['d2d3g'], h='2. Bring your king up',
         t="Walk your king up the board on your side of the rook's row, straight toward their king."),
    dict(fen='8/8/3k4/8/3K3R/8/8/8 w - - 0 1', arrows=['h4h6g'], h='3. Check when the kings face each other',
         t="Kings face to face with one square between: now check along the row. Their king has to step back."),
    dict(fen='8/4k3/7R/3K4/8/8/8/8 w - - 0 1', arrows=['h6a6g'], h="4. Not facing? Wait",
         t="If the kings aren't facing, don't check. Move the rook along its row, out of their king's reach. Their king has to step, and soon the kings face each other."),
    dict(fen='3k4/8/3K4/8/8/8/8/7R w - - 0 1', arrows=['h1h8g'], h='5. The mate',
         t="On the edge with the kings face to face, the check on the last row is mate."),
  ],
  'rr': [
    dict(fen='8/8/3k4/R7/8/8/8/1R2K3 w - - 0 1', arrows=['b1b6g'], h='The ladder',
         t="One rook holds a row. The other checks on the next row up. The king steps back, and the rooks take turns."),
    dict(fen='8/8/1k6/R7/8/8/6R1/4K3 w - - 0 1', arrows=['a5h5g'], h='Keep away from the king',
         t="When their king comes at a rook, move that rook to the far end of its row and carry on."),
    dict(fen='3k4/R7/8/8/8/8/8/1R2K3 w - - 0 1', arrows=['b1b8g'], h='Mate on the edge',
         t="When the king reaches the edge, the next check mates. Your own king isn't needed."),
  ],
  'bb': [
    dict(fen='8/8/8/3k4/8/2BB4/8/4K3 b - - 0 1', arrows=['c3h8b', 'd3h7b'], h='A wall of bishops',
         t="Side by side, the two bishops cover two diagonals their king can't cross. Together they fence it like a rook."),
    dict(fen='8/8/8/3k4/8/2BB4/4K3/8 w - - 0 1', arrows=['e2e3g'], h='Your king joins in',
         t="Two bishops can't mate alone. Bring your king up close: it takes the squares the bishops can't reach."),
    dict(fen='7k/5B2/6K1/4B3/8/8/8/8 b - - 0 1', arrows=['e5h8g'], h='Mate in the corner',
         t="Push the king into a corner. Then one bishop takes the last free square and the other checks."),
    dict(fen='7k/5K2/3B4/8/4B3/8/8/8 w - - 0 1', arrows=['d6e5g', 'e4f5r'], h='Watch for stalemate',
         t="In the corner their king has no square left. A quiet move now (red) is stalemate. Give check (green), and it is mate."),
  ],
  'bn': [
    dict(fen='8/8/8/4k3/8/8/8/2K1NB2 w - - 0 1', circles=['a8g', 'h1g'], h='The right corner',
         t="The mate only works in a corner of your bishop's colour. A light bishop mates in the two light corners."),
    dict(fen='7k/8/5K2/8/8/3B4/8/4N3 w - - 0 1', circles=['h8r', 'a8g'], h='From the wrong corner',
         t="If the king runs to the wrong corner, push it along the edge to the right one. The knight goes round in a W while your king and bishop keep it boxed."),
    dict(fen='k7/3N4/1K6/3B4/8/8/8/8 b - - 0 1', arrows=['d5a8g'], h='The mate',
         t="Your king in front, the knight guarding the square next to the corner, and the bishop checks along the diagonal."),
  ],
  # ---- king and pawn
  'kp': [
    dict(fen='8/8/4k3/8/8/4P3/4K3/8 w - - 0 1', circles=['d5g', 'e5g', 'f5g'], h='The goal',
         t="King and pawn against a king wins only if your king gets ahead of its pawn. Push too soon and their king stands in front of it: a draw."),
    dict(fen='8/4k3/8/8/4P3/8/4K3/8 w - - 0 1', circles=['d6g', 'e6g', 'f6g'], h='The key squares',
         t="For a pawn on your half of the board, the key squares are the three squares two rows in front of it. Get your king onto one and the pawn queens, whoever is to move."),
    dict(fen='8/8/4k3/8/3K4/4P3/8/8 w - - 0 1', arrows=['d4e4g', 'e3e4r'], h='Take the opposition',
         t="Kings face to face with one square between: the side to move has to give way. Step up so it is their move (green). The pawn push (red) lets their king stand in front of it."),
    dict(fen='8/8/3k4/8/4K3/4P3/8/8 w - - 0 1', arrows=['e4f5g'], h='Then step round',
         t="When their king gives way to one side, step diagonally to the other. Your king lands on a key square."),
    dict(fen='4k3/8/4K3/8/4P3/8/8/8 w - - 0 1', arrows=['e4e5g'], h='Then the pawn',
         t="Push the pawn only once your king stands on a key square. Then they walk up together: the king in front, the pawn behind it."),
  ],
  'opp': [
    dict(fen='8/8/4k3/8/4K3/4P3/8/8 b - - 0 1', circles=['e5y'], h='Face to face',
         t="Kings on the same file with one square between are in opposition. Whoever has to move must give way. When it is their move, you have the opposition."),
    dict(fen='2k5/8/8/8/8/1K2P3/8/8 w - - 0 1', arrows=['b3c4g'], circles=['c5y', 'c6y', 'c7y'], h='From afar',
         t="With three or five squares between the kings, the rule is the same: that is the distant opposition. Take it early and keep it as the kings come closer."),
    dict(fen='8/2k5/8/8/2K5/4P3/8/8 w - - 0 1', arrows=['c4c5g'], h='Keep it as you close in',
         t="When their king steps closer, step closer too and keep the kings facing. Don't push the pawn until your king stands on a key square."),
  ],
  'kpd': [
    dict(fen='8/8/8/4k3/P7/8/8/7K b - - 0 1', me='b', arrows=['a4a8b', 'a4e8b'], h='The square of the pawn',
         t="Picture a square with the pawn in one corner and the last row as its side. If your king can step into it, it catches the pawn. A pawn on its first square counts from the square in front, since it can jump two."),
    dict(fen='4k3/8/8/4K3/4P3/8/8/8 b - - 0 1', me='b', arrows=['e8e7g'], h='Keep the opposition',
         t="In front of the pawn, keep your king facing theirs with one square between. Then their king has to give way."),
    dict(fen='8/4k3/8/4K3/4P3/8/8/8 w - - 0 1', me='b', circles=['e6y'], h='Why it holds',
         t="Here it is their move. Whatever their king does, yours steps to face it again. They never reach a key square."),
    dict(fen='4k3/4P3/4K3/8/8/8/8/8 b - - 0 1', me='b', circles=['e8g'], h='The end',
         t="Stay in front to the last row. With the pawn on the seventh and their king behind it, you are stalemated: a draw."),
  ],
  'rpk': [
    dict(fen='k7/8/K7/P7/8/8/8/8 w - - 0 1', me='b', circles=['a8r'], h='The edge pawn',
         t="A pawn on the edge can't be won if your king reaches the corner in front of it. Their king can't drive it out without stalemate."),
    dict(fen='8/8/8/2k5/7P/5K2/8/8 b - - 0 1', me='b', arrows=['c5d6g'], circles=['h8g'], h='Run for the corner',
         t="Head straight for the corner in front of the pawn, or the squares beside it. Count: you need to get there before their king closes the door."),
    dict(fen='k7/8/1K6/P7/8/8/8/8 b - - 0 1', me='b', arrows=['a8b8g'], h='Then shuffle',
         t="In the corner, step between the corner and the square next to it. If they push the pawn up close, you are stalemated."),
    dict(fen='3k4/1K6/8/8/P7/8/8/8 b - - 0 1', me='b', circles=['c8r', 'b8r'], h="Their only chance",
         t="With an edge pawn the stronger side wins only by shutting your king out of the corner, its king standing in front. Don't let it get there first."),
  ],
  'race': [
    dict(fen='8/8/8/2k5/7P/5K2/8/8 b - - 0 1', arrows=['h4h8b', 'h4d8b'], h='The square of the pawn',
         t="Picture a square with the pawn in one corner and the last row as one side. A king that can step into it catches the pawn. A king outside it can't."),
    dict(fen='8/7p/5K2/1p6/8/PPk5/2P5/8 w - - 1 42', arrows=['f6e5g', 'a3a4r'], h='Your game: count before you push',
         t="Their pawn was slow: your king could catch it later. So the king came back to help your pawns first (green). The push you played (red) let their king take your pawns."),
    dict(fen='8/2p2p2/8/p1pk3p/5p1P/1PK2P2/P4P2/8 b - - 1 32', me='b', arrows=['d5c6g', 'f7f5r'], h='Your game: the king leads',
         t="You had three pawns to two on the queenside. Your king had to walk over there (green) and eat their pawns. The pawn step you played (red) gave the win away."),
  ],
  'bt': [
    dict(fen='7k/ppp5/8/PPP5/8/8/8/7K w - - 0 1', arrows=['b5b6g'], h='The breakthrough',
         t="Three pawns against three, all on the fifth row: push the middle one. Whichever pawn takes, push the other outside pawn. One of yours runs through."),
    dict(fen='7k/ppp5/8/PPP5/8/8/8/7K w - - 0 1', circles=['h8r'], h='When it works',
         t="It works when their king is too far to catch the pawn that gets through. Count before you give the first pawn away."),
  ],
  'tri': [
    dict(fen='8/1p1k4/1P6/2PK4/8/8/8/8 w - - 0 1', circles=['d5g', 'e5g', 'd4g'], h='Triangulation',
         t="Here you want it to be their move: their king would have to give way. Your king has three squares where it is fine, theirs only two."),
    dict(fen='8/1p1k4/1P6/2PK4/8/8/8/8 w - - 0 1', arrows=['d5e5g', 'e5d4b', 'd4d5b'], h='Walk the triangle',
         t="Walk round the three squares and come back. Their king has gone there and back on its two, and now it is their move in the same position."),
    dict(fen='8/1p1k4/1P6/2PK4/8/8/8/8 w - - 0 1', arrows=['c5c6r'], h="Don't push yet",
         t="The pawn push lets their king block it for good. Win the move first, then walk in."),
  ],
  'reti': [
    dict(fen='7K/8/k1P5/7p/8/8/8/8 w - - 0 1', arrows=['h8g7g', 'g7f6g'], h='Two jobs at once',
         t="Your king looks lost: too far from both pawns. Walk the diagonal: each step brings it closer to their pawn and to yours at the same time."),
    dict(fen='7K/8/k1P5/7p/8/8/8/8 w - - 0 1', circles=['d7g', 'g7g'], h='Why the diagonal',
         t="Going diagonally, a king covers as much ground towards two places as going straight. If they chase your pawn, you catch theirs. If they run, your pawn queens with your king beside it."),
  ],
  # ---- passed pawns
  'out': [
    dict(fen='8/5p1p/4k1p1/8/P7/4K1P1/5P1P/8 w - - 0 1', arrows=['a4a5g'], h='The outside passed pawn',
         t="A passed pawn far from the kings pulls their king away. While it chases the pawn, your king walks in and takes the pawns it left behind."),
    dict(fen='8/5p1p/4k1p1/8/P7/4K1P1/5P1P/8 w - - 0 1', circles=['f7r', 'g6r', 'h7r'], h='The plan',
         t="Push it until their king has to go after it. Then your king goes for their pawns on the other side."),
  ],
  'pro': [
    dict(fen='8/5p1p/6p1/3k4/1P6/2P2K2/5P1P/8 w - - 0 1', arrows=['f3g4g'], circles=['b4g'], h='The protected passed pawn',
         t="A passed pawn guarded by a pawn ties their king to it for good. Their king can't take it, and can't leave it."),
    dict(fen='8/5p1p/6p1/3k4/1P6/2P2K2/5P1P/8 w - - 0 1', circles=['f7r', 'g6r', 'h7r'], h='Your king is free',
         t="So your king can walk to the other side and take their pawns there."),
  ],
  'con': [
    dict(fen='8/2K5/8/3PP3/8/8/1r6/6k1 w - - 0 1', arrows=['e5e6g'], h='Two pawns against a rook',
         t="Two pawns side by side, far from their king, can beat a rook. Push the front one first and keep them together so they guard each other."),
    dict(fen='8/2K5/8/3PP3/8/8/1r6/6k1 w - - 0 1', circles=['g1r'], h='When they win',
         t="On the sixth row, two connected pawns beat a lone rook. With their king close, the rook usually wins them."),
  ],
  'tar': [
    dict(fen='r2k4/6p1/5p1p/P7/8/4KP2/R5PP/8 w - - 0 1', arrows=['a5a6g'], circles=['a2g', 'a8r'], h='Behind the passed pawn',
         t="Your rook behind your passed pawn gets stronger with every push. Theirs in front of it only gets more stuck."),
    dict(fen='6k1/8/r7/P7/8/8/6K1/R7 w - - 0 1', circles=['a1g', 'a6r'], h='The rule',
         t="Rooks go behind passed pawns: behind yours to push it, behind theirs to stop it."),
  ],
  # ---- rook endings
  'cut': [
    dict(fen='r7/8/6k1/8/3P4/8/3K4/4R3 b - - 0 1', arrows=['e1e8g'], h='Cut the king off',
         t="Your rook on the file between the kings keeps their king away from your pawn. Then your king and pawn walk up together."),
    dict(fen='r7/8/6k1/8/3P4/8/3K4/4R3 b - - 0 1', circles=['e8g', 'e7g', 'e6g'], h='How far',
         t="Cut off by two files or more, their king is usually too slow. Cut off by one, the defence often holds."),
  ],
  'luc': [
    dict(fen='3K4/3P1k2/8/8/8/8/2r5/4R3 w - - 0 1', arrows=['e1f1g'], h='The Lucena position',
         t="Your king in front of your pawn on the seventh, their king cut off, their rook checking from the side. First push their king one file further with a check."),
    dict(fen='3K4/3P2k1/8/8/8/8/2r5/5R2 w - - 2 2', arrows=['f1f4g'], h='Rook to the fourth row',
         t="Before your king walks out, put the rook on the fourth row. That is where it will block the checks."),
    dict(fen='8/3P2k1/8/3K4/5R2/8/8/3r4 w - - 12 7', arrows=['f4d4g'], h='Build the bridge',
         t="Walk your king out towards their rook. When the checks reach the rook's row, block with the rook: the bridge. The pawn queens."),
  ],
  'phi': [
    dict(fen='4k3/7R/r7/4P3/4K3/8/8/8 b - - 0 1', me='b', circles=['a6g', 'b6g', 'c6g', 'd6g', 'e6g', 'f6g', 'g6g'], h='Hold the third row',
         t="Defending, with your king in front of their pawn, keep your rook on your third row. Their king can't come up without walking into checks."),
    dict(fen='4k3/7R/r3P3/4K3/8/8/8/8 b - - 0 1', me='b', arrows=['a6a1g'], h='Then check from behind',
         t="Once their pawn steps onto your third row, your rook goes to the far end and checks from behind."),
    dict(fen='4k3/7R/4P3/4K3/8/8/8/r7 w - - 0 1', me='b', circles=['e6y'], h='Why it holds',
         t="The pawn no longer shelters their king. From far behind the checks never run out."),
  ],
  'van': [
    dict(fen='R7/2r3k1/P7/8/3K4/8/8/8 b - - 0 1', me='b', arrows=['c7c6g'], h='The Vančura',
         t="Against a rook in front of its edge pawn on the sixth, attack the pawn from the side. Keep your king near the other corner."),
    dict(fen='R7/6k1/P4r2/8/8/8/8/2K5 b - - 0 1', me='b', circles=['f6g'], h='Why it holds',
         t="From the side, your rook guards the pawn's path and checks their king whenever it comes to help."),
  ],
  'ssd': [
    dict(fen='7k/4K3/r4P2/8/8/8/1R6/8 b - - 0 1', me='b', arrows=['a6a7g'], h='Short side, long side',
         t="Your king goes to the short side of the pawn, the side nearer the edge. Your rook goes to the long side, far away."),
    dict(fen='7k/4K3/r4P2/8/8/8/1R6/8 b - - 0 1', me='b', circles=['a6g'], h='Why far away',
         t="From far away the rook checks from the side, and their king can't come close enough to stop the checks."),
  ],
  'rp': [
    dict(fen='8/8/6R1/8/8/kp6/5K2/8 w - - 0 1', arrows=['g6a6g'], h='Rook against pawn',
         t="Use the rook to keep their king away from the pawn while yours comes back to take it."),
    dict(fen='8/8/6R1/8/8/kp6/5K2/8 w - - 0 1', circles=['b2r'], h='Count first',
         t="If their king and pawn are far up the board and yours is far away, it may be a draw. A check that drives their king back gains the move you need."),
  ],
  'r7': [
    dict(fen='3r2k1/1R3ppp/p7/8/8/6P1/5P1P/6K1 w - - 0 1', arrows=['b7a7g'], h='Rook on the seventh',
         t="On the seventh row your rook takes pawns from the side and keeps their king on its back row."),
    dict(fen='3r2k1/1R3ppp/p7/8/8/6P1/5P1P/6K1 w - - 0 1', circles=['b7g', 'd8r'], h='Active against passive',
         t="An active rook, attacking pawns or cutting the king off, is worth more than a pawn. A rook tied to guarding loses."),
  ],
  'pzk': [
    dict(fen='r2k4/6p1/5p1p/P7/8/4KP2/R5PP/8 w - - 0 1', circles=['a2g'], h='Rook endings: four rules',
         t="Rooks behind passed pawns. An active rook beats a passive one. Your king fights too: bring it up. Cut their king off from the pawns."),
    dict(fen='r7/8/6k1/8/3P4/8/3K4/4R3 b - - 0 1', arrows=['e1e8g'], h='Before you move',
         t="Ask: can my rook get behind a passed pawn, cut their king off, or attack a pawn? Can my king come closer? Find the move that does the most."),
  ],
  # ---- minor pieces
  'wb': [
    dict(fen='8/8/4k3/P7/8/2B5/7K/8 b - - 0 1', me='b', arrows=['e6d7g'], circles=['a8g'], h='The wrong bishop',
         t="An edge pawn and a bishop that doesn't cover the queening square: if your king gets into that corner, it is a draw."),
    dict(fen='8/8/4k3/P7/8/2B5/7K/8 b - - 0 1', me='b', circles=['a8g', 'b7g', 'b8g'], h='Get there first',
         t="Count the race to the corner. Once you are in, shuffle in front of the pawn: nothing can drive you out."),
  ],
  'np': [
    dict(fen='8/8/8/8/3k4/8/1K1p4/6N1 w - - 0 1', arrows=['g1f3g'], circles=['d1g'], h='Knight against pawn',
         t="The knight stops a pawn by guarding a square in front of it. Check first when their king would take that square."),
    dict(fen='8/8/8/8/3k4/8/1K1p4/6N1 w - - 0 1', circles=['b2g'], h='Your king helps',
         t="Bring your king towards the pawn: once it guards the queening square, the knight is free."),
  ],
  'stm': [
    dict(fen='8/8/8/N7/8/p7/8/k2K4 w - - 0 1', arrows=['d1c2g'], h="Stamma's mate",
         t="A king stuck in front of its own edge pawn can be mated by a king and a knight. Box it in with your king first."),
    dict(fen='8/8/8/N7/8/p7/8/k2K4 w - - 0 1', circles=['a2r', 'b1r'], h='Then the knight',
         t="With their king trapped, the knight comes round and checks. Leave them a pawn move, or it is stalemate."),
  ],
  'pzm': [
    dict(fen='8/8/4k3/P7/8/2B5/7K/8 b - - 0 1', me='b', circles=['a8g'], h='Bishops and knights: rules',
         t="A bishop is good against pawns on both wings. A knight is good when the pawns are on one side. Put your pawns on the other colour from your bishop."),
    dict(fen='8/8/8/8/3k4/8/1K1p4/6N1 w - - 0 1', circles=['d1g'], h='Before you move',
         t="Ask: can my king go in? Can a pawn run? Is there a square their piece can't guard?"),
  ],
  # ---- queens
  'qp': [
    dict(fen='8/8/8/8/5Q2/6K1/3p4/3k4 w - - 0 1', arrows=['g3f2g'], h='Check it into the way',
         t="Check and pin until their king has to stand in front of its pawn. Then bring your king one step closer."),
    dict(fen='8/8/8/8/5Q2/6K1/3p4/3k4 w - - 0 1', circles=['d1y'], h='Again and again',
         t="Each time their king blocks its own pawn, your king gets a free move. Repeat until your king helps take the pawn."),
  ],
  'qpd': [
    dict(fen='8/2K5/8/8/8/k7/p7/7Q b - - 0 1', me='b', arrows=['a3b2g'], h='The stalemate trick',
         t="With a bishop or rook pawn on the seventh, hide your king beside it. If their queen takes the pawn, it is stalemate."),
    dict(fen='8/2K5/8/8/8/k7/p7/7Q b - - 0 1', me='b', circles=['a1g'], h='Only those pawns',
         t="It works only for the edge pawns and the pawns next to the bishops' files. Against the others, the queen wins."),
  ],
  'qr': [
    dict(fen='2rk4/6K1/Q7/8/8/8/8/8 w - - 0 1', arrows=['a6d6g'], h='Fork the rook',
         t="Push their king to the edge, then look for a check that also hits the rook. A rook that strays from its king is lost."),
    dict(fen='2rk4/6K1/Q7/8/8/8/8/8 w - - 0 1', circles=['c8r'], h='Watch the checks',
         t="Their rook will check and try to pin your king against your queen. Keep your king and queen on different lines."),
  ],
  'pzq': [
    dict(fen='8/8/8/8/5Q2/6K1/3p4/3k4 w - - 0 1', circles=['g3g'], h='Queen endings: rules',
         t="Your king hides from checks near its pawns. A passed pawn is worth more than in any other ending. Check only when it gains something."),
    dict(fen='2rk4/6K1/Q7/8/8/8/8/8 w - - 0 1', arrows=['a6d6g'], h='Before you move',
         t="Look for checks that also attack something. Then look at theirs: can their queen give checks forever?"),
  ],
  # ---- pawn endings from real games
  'pzz': [
    dict(fen='8/8/8/4k1p1/3pP1P1/8/4K3/8 w - - 3 55', arrows=['e2d3g'], h='The right king move',
         t="In pawn endings the king decides. Before you move, ask: which king reaches the pawns first? Can I take the opposition? Is there a waiting move?"),
    dict(fen='8/8/4k3/8/4K3/4P3/8/8 b - - 0 1', circles=['e5y'], h='The opposition',
         t="Kings facing with one square between: whoever must move gives way. Take it to get in; take it to keep them out."),
    dict(fen='8/2K5/p7/1p6/2k5/8/PP6/8 w - - 0 1', arrows=['c7b6g'], h='Go for their pawns',
         t="Count: if your king eats their pawns before theirs eats yours, and your pawn then queens first, go."),
    dict(fen='8/1p1k4/1P6/2PK4/8/8/8/8 w - - 0 1', circles=['d5g', 'e5g', 'd4g'], h='Waste a move',
         t="When the position would win if it were their move, lose a move with your king: walk a triangle, or make a spare pawn move."),
  ],
  'pzr': [
    dict(fen='7k/ppp5/8/PPP5/8/8/8/7K w - - 0 1', arrows=['b5b6g'], h='The right pawn move',
         t="A pawn move can't be taken back. Push when it breaks through, when it drags their king away, or when your pawn queens first."),
    dict(fen='8/5p1p/4k1p1/8/P7/4K1P1/5P1P/8 w - - 0 1', arrows=['a4a5g'], h='Drag their king away',
         t="A passed pawn on the edge pulls their king over. Your king then takes their other pawns."),
    dict(fen='8/8/k2K4/6Pp/1p2P3/8/8/8 w - - 0 1', arrows=['g5g6g'], h='Race and count',
         t="Count the moves to queen for both sides. Then look one move further: does a new queen give check, or attack the other one?"),
  ],
  # ---- named mates: the pattern, then how it is set up
  'dov': [
    dict(fen='3Q4/8/2q1p3/ppk2p2/8/4PPP1/P5K1/8 w - - 5 47', arrows=['d8d4g'], h='Dovetail mate',
         t="The queen checks from a square touching the king's corner, guarded. The king's own pieces fill the squares it would run to."),
  ],
}
for _k in KINDS:
    if _k['id'] in MANUAL: _k['idea'] = MANUAL[_k['id']]

# the kinds from real games (data/endings/puzzles.json, from the lichess puzzle database): their positions come with
# their own ratings, so the page picks the ones near the player's level
KINDS[KINDS.index(next(k for k in KINDS if k['id'] == 'reti')) + 1:KINDS.index(next(k for k in KINDS if k['id'] == 'reti')) + 1] = [
  dict(id='pzz', r=1500, group='Pawn endings', name='The right king move', goal='win', how='engine', idea=MANUAL['pzz']),
  dict(id='pzr', r=1500, group='Pawn endings', name='The right pawn move', goal='win', how='engine', idea=MANUAL['pzr']),
]
KINDS[KINDS.index(next(k for k in KINDS if k['id'] == 'r7')) + 1:KINDS.index(next(k for k in KINDS if k['id'] == 'r7')) + 1] = [
  dict(id='pzk', r=1500, group='Rook endings', name='Rook endings: find the move', goal='win', how='engine', idea=MANUAL['pzk']),
]
KINDS[KINDS.index(next(k for k in KINDS if k['id'] == 'stm')) + 1:KINDS.index(next(k for k in KINDS if k['id'] == 'stm')) + 1] = [
  dict(id='pzm', r=1500, group='Minor pieces', name='Bishops and knights: find the move', goal='win', how='engine', idea=MANUAL['pzm']),
]
KINDS[KINDS.index(next(k for k in KINDS if k['id'] == 'qr')) + 1:KINDS.index(next(k for k in KINDS if k['id'] == 'qr')) + 1] = [
  dict(id='pzq', r=1500, group='Queen endings', name='Queen endings: find the move', goal='win', how='engine', idea=MANUAL['pzq']),
]
KINDS[KINDS.index(next(k for k in KINDS if k['id'] == 'epa')) + 1:KINDS.index(next(k for k in KINDS if k['id'] == 'epa')) + 1] = [
  dict(id='dov', r=1000, group='Mating patterns', name='Dovetail mate', goal='mate', how='mate', idea=MANUAL['dov']),
]

# ---------------------------------------------------------------- why a move is played
# Show me how and Play along say why each of your moves is played. The build tags the moves of the lines it works out
# with one of these letters (the queen and rook mates by the method, king and pawn by the key squares and the
# opposition, a lone king against two pieces by what the move does); the page reads the moves of the other lines.
WHY = {
  'm': 'Mate.',
  'b': 'Shrink the box: their king has fewer squares.',
  'k': 'Bring your king closer.',
  'z': "Their king is down to two squares: bring yours, and don't take the last one.",
  'w': 'Wait: a move that keeps the box. Their king has to step.',
  'c': 'Check: their king has to step back.',
  'B': 'A piece move that keeps their king boxed in.',
  'o': 'Take the opposition: now their king has to give way.',
  'y': "Onto a key square: now the pawn can't be stopped.",
  'f': 'Lead with the king: it clears the way for the pawn.',
  'p': 'Push the pawn: your king in front clears its way.',
  'g': 'Push the pawn onto a square your king guards.',
  'r': "Push the pawn: their king can't catch it.",
  'P': 'Push the pawn one step closer to queening.',
  'Q': 'The pawn queens.',
  'O': "Keep the opposition: their king can't get past.",
  'F': 'Stay in front of the pawn.',
  'C': 'Head for the corner in front of the pawn.',
  'K': 'A king move that keeps the draw.',
  'X': 'Take it: nothing is left to win with.',
}

# What a position from the puzzle database is about, read from its themes on lichess: the first one listed here that
# it has. POINT: the kind's own line when none applies.
THEMES = [
  ('zugzwang', 'Zugzwang: they have to move, and every move makes it worse.'),
  ('skewer', 'A skewer: the check moves the king, and what stands behind it falls.'),
  ('deflection', 'Pull a defender away from what it guards.'),
  ('discoveredAttack', 'One piece steps aside and uncovers an attack by another.'),
  ('capturingDefender', 'Take the piece that guards.'),
  ('attraction', 'Draw a piece onto a square where it can be hit.'),
  ('trappedPiece', 'A piece with no square to go to.'),
  ('hangingPiece', 'A piece left unguarded.'),
  ('intermezzo', 'A move in between, before the take back.'),
  ('sacrifice', 'Give something to get more back.'),
  ('exposedKing', 'Their king has no cover: the checks win something.'),
  ('defensiveMove', 'First stop what they threaten. The win is still there after.'),
  ('promotion', 'The pawn gets through and queens.'),
  ('advancedPawn', 'The pawn nearest to queening decides it.'),
  ('quietMove', 'A quiet move: no check and nothing taken, and still the one that wins.'),
]
POINT = {
  'pzz': 'In a pawn ending the king decides: count which king gets where first.',
  'pzr': 'Count the race before you push: a pawn move never goes back.',
  'pzk': 'An active rook and an active king win rook endings.',
  'pzm': 'Kings and pawns decide minor piece endings: the pieces guard and block.',
  'pzq': 'In queen endings, check only when it wins something, and mind their checks.',
}
