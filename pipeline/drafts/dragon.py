"""The Dragon for Black (content/black/bdragon.py): the setup's order, the moves fixed by hand, the lessons and the notes.
Run it to redraft the pack (python3 pipeline/drafts/dragon.py); it overwrites the module, so notes are edited here."""
import sys, re, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import paths, chess, draft
def system(b, path):
    # one setup against everything: take the d-pawn when it comes, d-pawn one square, knight, g-pawn, bishop, castle, queen's knight
    order = ['cxd4', 'd6', 'Nf6', 'g6', 'Bg7', 'O-O', 'Nc6', 'Bd7', 'Rc8', 'Ne5', 'Nc4']
    q = b.piece_at(chess.D4)
    if q and q.piece_type == chess.QUEEN and q.color == chess.WHITE: order = ['Nc6'] + order      # the queen in the middle: the knight hits her
    if b.is_check(): order = ['Bd7'] + order                                                      # a bishop check is blocked by the bishop
    return order
O = 'e4 c5 Nf3 d6 d4 cxd4'
D = O + ' Nxd4 Nf6 Nc3 g6'
fixed = {'e4': 'c5', 'e4 c5 Nf3': 'd6', 'e4 c5 Nf3 d6 d4': 'cxd4', O + ' Nxd4': 'Nf6', O + ' Nxd4 Nf6 Nc3': 'g6',
         O + ' Qxd4': 'Nc6', 'e4 c5 d4': 'cxd4', 'e4 c5 d4 cxd4 Qxd4': 'Nc6', 'e4 c5 Nf3 d6 Bb5+': 'Bd7', 'e4 c5 b4': 'cxb4',
         'e4 c5 f4': 'd6', 'e4 c5 d4 cxd4 c3': 'Nf6', 'e4 c5 e5 d6 exd6': 'exd6'}
W = draft.Walk('b', system, fixed, known=draft.known_from('black', skip_chapters=('dragon', 'sicilian')), tol=35, thr=lambda n, r: 0.012 if n <= 3 else 0.03 if n <= 5 else 0.06 if n <= 9 else 0.10, min_reach=0.0015,
               depth=lambda r: 18 if r >= 0.02 else 16 if r >= 0.005 else 14 if r >= 0.002 else 12)
Y = D + ' Be3 Bg7 f3 O-O Qd2 Nc6'
# the Yugoslav as it is played when White knows it (rare at club level, so it is given by hand), then the tree by the odds
leaves = W.run([(Y + ' Bc4 Bd7 O-O-O Rc8 Bb3 Ne5 h4', None), (Y + ' O-O-O', None), (D + ' Be3', None), (D + ' Be2', None), ('e4', 1.0)])
LESSONS = [
  dict(id='bdr-yugo', part='bdr-open', root=D + ' Be3', main=D + ' Be3 Bg7 f3 O-O Qd2 Nc6 Bc4', title='The Yugoslav Attack', sub='Bishop, castle, knight, then the rook to the open file', pri='core',
       why='White sets up to castle long and push the edge pawn at your king. Your pieces come out in one order and the open file points at White\'s king.', outcome='A race you are ready for'),
  dict(id='bdr-classical', part='bdr-open', root=D + ' Be2', title='The Classical Dragon', sub='The same setup; White castles short', pri='core',
       why='The quiet way to meet the Dragon. Nothing changes in your setup, and the long diagonal is yours.', outcome='Equal and easy to play'),
  dict(id='bdr-sixth', part='bdr-open', root=D, main=D + ' Bc4', title='Other sixth moves', sub='The Italian bishop, the pin, a bishop check', pri='common',
       why='Whatever White plays on move six, the bishop goes to the long diagonal and you castle.', outcome='Equal'),
  dict(id='bdr-fourth', part='bdr-open', root=O, title='The queen takes back', sub='Your knight hits her and gains a move', pri='common',
       why='One in six takes back with the queen. She stands in the open, and your knight comes out with a hit on her.', outcome='Comfortable'),
  dict(id='bdr-moscow', part='bdr-third', root='e4 c5 Nf3 d6 Bb5+', main='e4 c5 Nf3 d6 Bb5+ Bd7 Bxd7+ Qxd7 O-O', title='The Moscow: a bishop check', sub='Block with the bishop and trade it off', pri='common',
       why='A check that skips the open game. Your bishop blocks, the bishops come off, and the setup goes on.', outcome='Equal'),
  dict(id='bdr-bc4', part='bdr-third', root='e4 c5 Nf3 d6 Bc4', title='The Italian bishop', sub='Knight out; the bishop is aimed at a wall', pri='common',
       why='Club players love this bishop. Against the Sicilian it has little to aim at, and your setup comes out untouched.', outcome='Comfortable'),
  dict(id='bdr-third', part='bdr-third', root='e4 c5 Nf3 d6', title='Other third moves', sub='The small c-pawn, the knight, the quiet d-pawn', pri='common',
       why='White holds the d-pawn back. Knight out, g-pawn, bishop: the same order.', outcome='Equal'),
  dict(id='bdr-bowdler', part='bdr-second', root='e4 c5 Bc4', main='e4 c5 Bc4 d6 Nc3 Nf6 d3', title='The bishop out on move two', sub='The same setup, one move earlier', pri='core',
       why='The most common second move at club level after the knight. Nothing changes for you.', outcome='Comfortable'),
  dict(id='bdr-closed', part='bdr-second', root='e4 c5 Nc3', main='e4 c5 Nc3 d6 g3', title='The Closed Sicilian', sub='White keeps the middle shut; the same setup', pri='common',
       why='One in eight brings the queen\'s knight out and keeps the d-pawn home. Your setup is the same, move for move.', outcome='Equal'),
  dict(id='bdr-alapin', part='bdr-second', root='e4 c5 c3', main='e4 c5 c3 Nf6 e5', title='The Alapin: the small c-pawn', sub='White builds a center; your bishop aims at it', pri='common',
       why='White wants two pawns in the middle. Let them come, trade one off, and aim the bishop at the other.', outcome='A full game'),
  dict(id='bdr-morra', part='bdr-second', root='e4 c5 d4', main='e4 c5 d4 cxd4 Qxd4 Nc6 Qd1', title='The d-pawn on move two', sub='Take it; then the setup', pri='common',
       why='One in ten pushes the d-pawn at once. Take it, and whatever White takes back with, the setup comes out.', outcome='Equal or better'),
  dict(id='bdr-f4', part='bdr-second', root='e4 c5 f4', main='e4 c5 f4 d6 Nf3 Nf6 Nc3', title='The f-pawn on move two', sub='The same setup against the Grand Prix', pri='rare',
       why='White plans a pawn storm. Your bishop on the long diagonal and an early castle take the sting out of it.', outcome='Equal'),
  dict(id='bdr-second', part='bdr-second', root='e4 c5', main='e4 c5 d3 d6 Nf3', title='Other second moves', sub='The quiet d-pawn, the early queen, the second c-pawn', pri='rare',
       why='Whatever White tries on move two, the answer starts the same way: d-pawn, knight, g-pawn, bishop.', outcome='Equal or better'),
]
text, table = draft.emit(leaves, LESSONS, 'b')
PARTS = [
  ('bdr-open', 'dragon', 'White opens the middle', 'Open Sicilian', 'White trades the d-pawn for your c-pawn. Your bishop goes to the long diagonal, you castle, and the half-open file belongs to your rook.'),
  ('bdr-third', 'dragon', 'White holds the d-pawn back', 'Third-move tries', 'A check, the Italian bishop, a small pawn move. The setup comes out in the same order.'),
  ('bdr-second', 'dragon', 'White skips the knight', 'Second-move tries', 'The bishop, the other knight, the small c-pawn, a gambit. One setup answers them all.'),
]
NOTES = {
  'e4 c5': ('Sicilian Defense', 'Your c-pawn fights for the middle from the side. When White pushes the d-pawn you trade it off and keep both of your own center pawns.', ['key'], dict(arrows=['c5d4g'])),
  'e4 c5 Nf3 d6': ('D-pawn one square', 'The first move of the setup. It keeps White\'s e-pawn from pushing at your knight and opens the way for the bishop.', ['key']),
  O: ('Take the d-pawn', 'A wing pawn for a center pawn. The file it leaves half open belongs to your rook later.', ['key']),
  O + ' Nxd4 Nf6': ('Knight hits the e-pawn', 'White has to guard it, and nearly always does it with the knight.', ['key'], dict(arrows=['f6e4r'])),
  D: ('The Dragon', 'The g-pawn makes room for the bishop. From the long diagonal it looks across the whole board at White\'s queenside.', ['key'], dict(arrows=['f8g7g'])),
  D + ' Be3 Bg7': ('Bishop to the long diagonal', 'Bishop first, then castle. Your knight waits: jumping at White\'s bishop a move earlier would run into a bishop check.', ['key']),
  D + ' Be3 Bg7 f3': ('F-pawn one square', 'It takes the jumping square from your knight. White means to castle long and push the edge pawn at your king.'),
  D + ' Be3 Bg7 f3 O-O': ('Castle', 'King safe before the race starts.', ['key']),
  Y: ('Queen\'s knight out', 'A second piece on White\'s knight in the middle.'),
  Y + ' Bc4 Bd7': ('Bishop off the back rank', 'The last piece out, and the rook can now reach the half-open file.', ['key'], dict(arrows=['a8c8g'])),
  Y + ' Bc4 Bd7 O-O-O Rc8': ('Rook to the half-open file', 'It looks straight down at White\'s king. The knight goes to the middle next.', ['key']),
  Y + ' Bc4 Bd7 O-O-O Rc8 Bb3 Ne5': ('Knight to the middle', 'From here it can jump in beside White\'s king, and your attack runs down the open file.', ['key']),
  Y + ' Bc4 Bd7 O-O-O Rc8 Bb3 Ne5 h4': ('The edge pawn starts', 'White wants to open the file in front of your king.'),
  Y + ' Bc4 Bd7 O-O-O Rc8 Bb3 Ne5 h4 h5': ('Stop the edge pawn', 'One pawn move holds the wing. To open a file now White has to give something up.', ['key']),
  D + ' Be3 Bg7 Bc4 Ng4': ('Knight jumps at the bishop', 'White left the f-pawn at home, so the square is free. The bishop that guards the knight in the middle is hit and has no good place to go.', ['key']),
  D + ' Be2 Bg7': ('Bishop to the long diagonal', 'The same move whatever White plays on move six.', ['key']),
  D + ' Be2 Bg7 O-O O-O': ('Castle', 'The same four moves as always. The queen\'s knight comes next.'),
  D + ' Bc4 Bg7': ('Bishop to the long diagonal', 'White\'s bishop aims at f7. Castling covers it, and your bishop is out first.', ['key']),
  O + ' Qxd4 Nc6': ('Knight hits the queen', 'She has to move again, and you have a piece out for free.', ['key'], dict(arrows=['c6d4r'])),
  'e4 c5 Nf3 d6 Bb5+ Bd7': ('Block with the bishop', 'If White trades, your queen takes back and the setup goes on.', ['key']),
  'e4 c5 Nf3 d6 Bb5+ Bd7 Bxd7+ Qxd7': ('Queen takes back', 'The queen\'s knight keeps its best square. Next: knight, g-pawn, bishop.'),
  'e4 c5 Nf3 d6 Bc4 Nf6': ('Knight hits the e-pawn', 'The bishop aims at f7, and your e-pawn can shut it out whenever it has to.', ['key']),
  'e4 c5 Nf3 d6 Bc4 Nf6 Ng5 e6': ('E-pawn shuts the bishop out', 'F7 is covered, and the knight has nothing to do out there.', ['key']),
  'e4 c5 Nf3 d6 Bc4 Nf6 O-O Nxe4': ('Take the e-pawn', 'Nothing guards it. When the rook comes at the knight, it steps back.', ['key']),
  'e4 c5 Nf3 d6 c3 Nf6': ('Knight hits the e-pawn', 'White\'s knight can no longer guard it from its usual square: a pawn is standing there.', ['key']),
  'e4 c5 Bc4 d6': ('D-pawn one square', 'The same first move. The bishop came out early, and your e-pawn can block it when it has to.'),
  'e4 c5 Qh5 d6 Bc4 g6': ('G-pawn hits the queen', 'Queen and bishop were both aimed at f7. The g-pawn shuts her line and hits her, and it is a move of your setup anyway.', ['key']),
  'e4 c5 c3 Nf6': ('Knight hits the e-pawn', 'White\'s knight can\'t guard it from its usual square: the c-pawn is standing there.', ['key'], dict(arrows=['f6e4r'])),
  'e4 c5 c3 Nf6 e5 Nd5': ('Knight to the middle', 'It can\'t be chased for long, and White\'s pawn has run ahead of its helpers.', ['key']),
  'e4 c5 c3 Nf6 e5 Nd5 d4 cxd4': ('Take the d-pawn', 'One of White\'s two center pawns comes off. Your d-pawn hits the other next.'),
  'e4 c5 c3 Nf6 d4 Nxe4': ('Take the e-pawn', 'White left it without a guard. A clean pawn.', ['key']),
  'e4 c5 d4 cxd4': ('Take the pawn', 'A center pawn for a wing pawn.'),
  'e4 c5 d4 cxd4 c3 Nf6': ('Leave the gambit pawn', 'Knight out with a hit on the e-pawn, and the game turns into the small c-pawn line you already know.', ['key']),
  'e4 c5 Nc3 d6': ('D-pawn one square', 'The setup starts the same way whatever White does on move two.'),
  'e4 c5 f4 d6': ('D-pawn one square', 'The same first move. Your bishop on the long diagonal and an early castle meet the pawn storm.'),
}
allp = set()
for _, _, path, _ in table:
    t = path.split()
    for k in range(1, len(t) + 1): allp.add(' '.join(t[:k]))
drop = [k for k in NOTES if ' '.join(k.split()) not in allp]
print('notes without a node (dropped):', drop)
# a position the rest of the book already has a note for keeps that note (the first moves are shared with the Kan)
import types
for m in ('bdragon', 'bfill'): sys.modules[m] = types.ModuleType(m)
sys.path.insert(0, str(paths.ROOT / 'content/black')); import bcontent, bnotes  # noqa: F401  (bnotes registers the house notes)
have = set(bcontent.NOTES); shared = [k for k in NOTES if ' '.join(k.split()) in have]
print('notes the book already has (kept as they are):', shared)
NOTES = {k: v for k, v in NOTES.items() if k not in drop and k not in shared}
auto = draft.named_moves([t[2] for t in table], 'b', skip=have)
mod = draft.module_text("""Black against the e-pawn, the Sicilian's second variation: the Dragon. C-pawn two squares, take the d-pawn when
it comes, then one setup: d-pawn one square, knight, g-pawn, bishop to the long diagonal, castle, queen's knight. A
separate pack (see PACKS in bmeta.py). The lines were drafted with pipeline/draft.py: White's moves by the Maia 1300/1500
odds, yours from the setup's order wherever Stockfish 17.1 accepts it and the engine's move elsewhere. SAN is internal
only; notes are plain English.""", 'from bcontent import L, P, J, n', PARTS, text, NOTES, auto, lambda p: f"P({', '.join(repr(x) for x in p)})")
open(paths.ROOT / 'content/black/bdragon.py', 'w').write(mod)
for lid, title, path, reach in table: print(f"{reach*100:5.2f} {lid:28s} {title:44s} {path[6:]}")
print(len(leaves), 'leaves'); print('flags:'); [print(' ', f) for f in W.flags]
draft.done()
