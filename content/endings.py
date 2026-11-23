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

# The kinds, in the order the Endings tab shows them. goal: mate (play to mate), queen (promote and keep the win),
# hold (keep the draw for `hold` of your moves), win (reach a won position: a mate, or the engine at +9 or better).
# how: the exact table that judges it, or 'engine'.
KINDS = [
  dict(id='q', group='Mates', name='Queen mate', goal='mate', how='kqk', n=12),
  dict(id='r', group='Mates', name='Rook mate', goal='mate', how='krk', n=12),
  dict(id='rr', group='Mates', name='Two rooks', goal='mate', how='bare', n=6),
  dict(id='bb', group='Mates', name='Two bishops', goal='mate', how='bare', n=4, cap=35),
  dict(id='bn', group='Mates', name='Bishop and knight', goal='mate', how='bare', n=4, cap=50),
  dict(id='br', group='Mates', name='Back rank', goal='win', how='engine'),
  dict(id='kp', group='Pawn endings', name='King and pawn', goal='queen', how='kpk', n=12),
  dict(id='kpd', group='Pawn endings', name='Stop the pawn', goal='hold', how='kpk', n=10, hold=10),
  dict(id='race', group='Pawn endings', name='Races', goal='win', how='engine'),
  dict(id='bt', group='Pawn endings', name='Breakthrough', goal='queen', how='engine'),
  dict(id='luc', group='Rook endings', name='Lucena', goal='queen', how='engine', n=6),
  dict(id='phi', group='Rook endings', name='Philidor', goal='hold', how='engine', n=6, hold=10),
  dict(id='cut', group='Rook endings', name='King cut off', goal='queen', how='engine', n=6),
  dict(id='qp', group='Queen endings', name='Queen against a pawn', goal='win', how='engine', n=6),
  dict(id='mine', group='From your games', name='Your endings', goal='win', how='engine'),
]

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
  dict(key='2026.07.09 gfrasti', fen='8/p2R4/1p3p1p/2p5/1P1R2P1/4kPK1/2r4P/8 w - - 0 40', why='A rook check mated here.'),
  dict(key='2026.07.13 Datmo', fen='3r2k1/1RB2ppp/1p2p3/b2p4/3P4/4P2P/5PPK/r7 b - - 7 29', why='One rook move let a mate in on your back row.'),
  dict(key='2026.07.09 TiepiMT', fen='3r2k1/5p2/R3bBp1/7p/1KP4P/1P4P1/8/1r6 b - - 1 34', why='One rook move let a mate in on your back row.'),
  dict(key='2026.10.14 abood_almuss', fen='Q7/5p1p/4pBpk/1p2Pq2/1P3P2/2p5/5PKP/8 w - - 3 37', why='A queen check let the other queen check forever.'),
  dict(key='2026.07.09 TheLuisGambit25', fen='8/8/4b2R/p1r2k2/K7/1P6/P7/8 w - - 7 78', why='A rook check would have won the rook behind the king.'),
  dict(key='2026.07.11 quzibek', fen='8/p3k1pp/1pN5/8/P7/1b4P1/5K1P/8 b - - 0 34', why='The king stepped into a knight fork.'),
  dict(key='2026.07.12 zz_ny', fen='8/7p/5K2/1p6/8/PPk5/2P5/8 w - - 1 42', why='A pawn push let the black king back. The king had to race.'),
  dict(key='2026.10.14 Eschoir', fen='8/2p2p2/8/p1pk3p/5p1P/1PK2P2/P4P2/8 b - - 1 32', why='A pawn step instead of a king step threw the win away.'),
  dict(key='2026.07.10 steny35', fen='8/p1k3p1/p4p1p/4rp1P/3N4/b1PK4/P1P2PP1/1R6 w - - 6 30', why='The wrong pawn moved and the edge was gone.'),
]

# The course, in the order this player needs it. Each unit: slides to learn from (a board, a heading, one line),
# lines to play along (moves given, or 'method': worked out by the build from the tables), the kinds its practice
# positions come from (`practice`, with how many to win clean: `need`) and its checkpoint (positions with one point
# to find: `ask` is the question; the build works out the answers).
UNITS = [
  dict(id='eg-r', title='The rook mate', kinds=['r'], need=3,
       why='You had mate in one with a rook and played a check that lost it.',
       slides=[
         dict(fen='8/8/3k4/8/7R/8/4K3/8 b - - 0 1', arrows=['h4a4g'], h='Cut the king off',
              t='The rook holds a row. Their king can\'t cross it.'),
         dict(fen='8/8/3k4/8/3K3R/8/8/8 w - - 0 1', arrows=['h4h6g'], h='Check when the kings face each other',
              t='Kings face to face with one square between: a check on the row pushes their king back.'),
         dict(fen='8/4k3/7R/3K4/8/8/8/8 w - - 0 1', arrows=['h6g6g'], h='Not facing yet? Wait',
              t='Move the rook along its row, out of the king\'s reach. Their king has to step.'),
         dict(fen='3k4/8/3K4/8/8/8/8/7R w - - 0 1', arrows=['h1h8g'], h='The mate',
              t='On the edge with the kings face to face, the check on the last row mates.'),
         dict(fen='8/p2R4/1p3p1p/2p5/1P1R2P1/4kPK1/2r4P/8 w - - 0 40', arrows=['d4e4g', 'd7e7r'], h='Your game: look for mate first',
              t='The rook check beside the king mated (green). The check you played lost a rook.'),
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
         dict(fen='6k1/5ppp/8/8/8/8/5PPP/3R2K1 w - - 0 1', arrows=['h2h3g'], circles=['h2g'], h='Give your king air',
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
  dict(id='eg-kp', title='King and pawn', kinds=['kp', 'kpd'], need=3,
       why='Two of your pawn endings got away. Every pawn ending ends up here.',
       slides=[
         dict(fen='8/4k3/8/8/4P3/8/4K3/8 w - - 0 1', circles=['d6g', 'e6g', 'f6g'], h='The key squares',
              t='Get your king to one of the three squares two rows in front of the pawn, and the pawn queens.'),
         dict(fen='8/8/4k3/8/4K3/4P3/8/8 b - - 0 1', circles=['e5y'], h='The opposition',
              t='Kings face to face with one square between: the side that has to move gives way.'),
         dict(fen='8/8/4k3/8/3K4/4P3/8/8 w - - 0 1', arrows=['d4e4g', 'e3e4r'], h='King first',
              t='Step the king up and take the opposition (green). The pawn push (red) lets their king stand in front of it: a draw.'),
         dict(fen='k7/8/K7/P7/8/8/8/8 w - - 0 1', circles=['a8r'], h='The edge pawn',
              t='With a pawn on the edge, a king that gets to the corner holds the draw.'),
         dict(fen='8/8/8/4k3/P7/8/8/7K b - - 0 1', arrows=['a4a8b', 'a4e8b'], h='The square of the pawn',
              t='Draw the square from the pawn to the last row. A king that can step into it catches the pawn.'),
       ],
       along=[dict(gen='kpk-demo', method=True)],
       check=[
         dict(gen='kpk-only', n=3, ask='Find the move that wins.'),
         dict(gen='kpk-hold', n=2, ask='Find the move that holds the draw.'),
       ]),
  dict(id='eg-race', title='Pawn races', kinds=['race', 'bt'], need=3,
       why='Two pawn endings slipped on one move each: a pawn pushed where the king had to go.',
       slides=[
         dict(fen='8/7p/5K2/1p6/8/PPk5/2P5/8 w - - 1 42', arrows=['f6g5g', 'a3a4r'], h='Your game: count the race',
              t='Your king had to go and take their last pawn (green). The push (red) let their king back.'),
         dict(fen='8/5p1p/4k1p1/8/P7/4K1P1/5P1P/8 w - - 0 1', arrows=['a4a5g'], h='The outside passed pawn',
              t='A passed pawn far from the kings pulls their king away. Then yours takes the other pawns.'),
         dict(fen='8/2p2p2/8/p1pk3p/5p1P/1PK2P2/P4P2/8 b - - 1 32', me='b', arrows=['d5c6g', 'f7f5r'], h='Your game: the king leads',
              t='Your king had to walk to your passed pawns (green). The pawn step (red) threw the win away.'),
         dict(fen='7k/ppp5/8/PPP5/8/8/8/7K w - - 0 1', arrows=['b5b6g'], h='The breakthrough',
              t='Three pawns against three: give one, and another of yours runs through.'),
       ],
       along=[dict(fen='8/5p1p/4k1p1/8/P7/4K1P1/5P1P/8 w - - 0 1', pv=16)],
       check=[
         dict(fen='8/7p/5K2/1p6/8/PPk5/2P5/8 w - - 1 42', ask='Your game. Find the move that wins the race.'),
         dict(fen='8/2p2p2/8/p1pk3p/5p1P/1PK2P2/P4P2/8 b - - 1 32', ask='Your game. Keep the win.'),
         dict(fen='7k/ppp5/8/PPP5/8/8/8/7K w - - 0 1', ask='Find the breakthrough.', ok=['b5b6']),
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
       slides=[
         dict(fen='8/8/8/3k4/8/2Q5/8/4K3 b - - 0 1', arrows=['c3c8g', 'c3h3g'], h='Box the king in',
              t='Put the queen a knight\'s jump from the king. It holds a row and a file, and the king can\'t reach it.'),
         dict(fen='7k/8/8/6Q1/8/2K5/8/8 b - - 0 1', circles=['h7y', 'h8y'], h='Stop at two squares',
              t='Once the king is down to two squares on the edge, stop squeezing: one more and it is stalemate.'),
         dict(fen='7k/8/8/6Q1/3K4/8/8/8 b - - 0 1', arrows=['d4f6g'], h='Bring your king',
              t='Walk your king over while theirs steps between its two squares.'),
         dict(fen='7k/6Q1/6K1/8/8/8/8/8 b - - 0 1', circles=['g7g'], h='The mate',
              t='The queen checks next to the king with your king guarding it.'),
         dict(fen='k7/2K5/8/1Q6/8/8/8/8 w - - 0 1', arrows=['b5b7g', 'b5b6r'], h='Watch for stalemate',
              t='No check and no square is a draw. Before each queen move, give check or leave the king a square.'),
       ],
       along=[dict(fen='8/8/8/3k4/8/8/8/Q3K3 w - - 0 1', method=True)],
       check=[
         dict(gen='kqk-mate1', n=2, ask='Find the mate.'),
         dict(gen='kqk-mate1s', n=3, ask='Find the mate. Careful: some queen moves are stalemate.'),
       ]),
  dict(id='eg-rook', title='Rook endings', kinds=['luc', 'phi', 'cut'], need=3,
       why='Every rook ending with one pawn left heads for one of two positions.',
       slides=[
         dict(fen='r7/8/6k1/8/3P4/8/3K4/4R3 b - - 0 1', arrows=['e1e8g'], h='Cut the king off',
              t='Your rook on the file between the kings keeps their king away from your pawn.'),
         dict(fen='3K4/3P2k1/8/8/5R2/8/2r5/8 b - - 0 1', arrows=['d8e7g'], circles=['f4g'], h='Lucena: build a bridge',
              t='Rook to the fourth row first. Then your king walks out, and when the checks run out the rook blocks them.'),
         dict(fen='4k3/7R/r7/4P3/4K3/8/8/8 b - - 0 1', me='b', arrows=['a6h6g'], h='Philidor: hold the third row',
              t='Defending, keep your rook on your third row so their king can\'t come up.'),
         dict(fen='4k3/7R/r3P3/4K3/8/8/8/8 b - - 0 1', me='b', arrows=['a6a1g'], h='Philidor: then check from behind',
              t='Once their pawn steps up, your rook goes to the far end and checks from behind. Their king has nowhere to hide.'),
         dict(fen='6k1/8/r7/P7/8/8/6K1/R7 w - - 0 1', circles=['a1g', 'a6r'], h='Rook behind the passed pawn',
              t='Rooks go behind passed pawns: behind yours to push it, behind theirs to stop it.'),
       ],
       along=[dict(fen='3K4/3P1k2/8/8/8/8/2r5/4R3 w - - 0 1', moves='e1f1 f7g7 f1f4 c2c1 d8e7 c1e1 e7d6 e1d1 d6e6 d1e1 e6d5 e1d1 f4d4')],
       check=[
         dict(fen='3K4/3P2k1/8/8/8/8/2r5/5R2 w - - 0 1', ask='Lucena. Find the move that builds the bridge.', ok=['f1f4']),
         dict(fen='4k3/7R/r3P3/4K3/8/8/8/8 b - - 0 1', ask='Philidor. Find the move that holds the draw.'),
       ]),
]
