"""The Scandinavian for Black (content/black/bscandi.py): the setup's order, the moves fixed by hand, the lessons and the notes.
Run it to redraft the pack (python3 pipeline/drafts/scandinavian.py); it overwrites the module, so notes are edited here."""
import sys, re, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import paths, chess, draft
def system(b, path):
    if path.startswith('e4 d5 e5'): return ['Bxd3', 'Bf5', 'e6', 'c5', 'Nc6']            # the pawn pushed past: bishop out, then hit the chain
    order = ['Bxd3', 'Nf6', 'c6', 'Bf5', 'e6', 'Nbd7', 'Be7', 'O-O', 'Bd6', 'Bb4']       # a bishop offered for yours is traded
    # a knight on the square in front of your e-pawn's file: the bishop comes out at it first
    if b.piece_at(chess.E4) and b.piece_at(chess.E4).piece_type == chess.KNIGHT and b.piece_at(chess.E4).color == chess.WHITE: order = ['Bf5'] + order
    # the queen in the middle is hit: to the side, as in the main line
    q = b.king(chess.BLACK) is not None and b.pieces(chess.QUEEN, chess.BLACK)
    if chess.D5 in q and b.attackers(chess.WHITE, chess.D5): order = ['Qa5'] + order
    return order
fixed = {'e4 d5 exd5 Qxd5 Nc3 Qa5 Bc4 Nf6 d3 c6 Bd2': 'Qc7', 'e4 d5 exd5 Qxd5 d4 e5 dxe5 Qxd1+ Kxd1': 'Nc6', 'e4 d5 exd5 Qxd5 Nc3 Qa5 d3 Nf6 Bd2': 'c6', 'e4 d5 d3': 'dxe4', 'e4 d5 d3 dxe4 dxe4': 'Qxd1+', 'e4 d5 f3': 'dxe4', 'e4 d5 exd5 Qxd5 Nc3 Qa5 d4 Nf6 Bd2': 'c6', 'e4': 'd5', 'e4 d5 exd5': 'Qxd5', 'e4 d5 exd5 Qxd5 Nc3': 'Qa5', 'e4 d5 e5': 'Bf5', 'e4 d5 Nc3': 'dxe4', 'e4 d5 d4': 'dxe4'}
W = draft.Walk('b', system, fixed, known=draft.known_from('black', skip_chapters=('scandi',)), tol=35, thr=lambda n, r: 0.01 if n <= 3 else 0.02 if n <= 5 else 0.05 if n <= 7 else 0.09, min_reach=0.0008,
               depth=lambda r: 16 if r >= 0.02 else 14 if r >= 0.005 else 12 if r >= 0.002 else 10)
leaves = W.run([('e4 d5 exd5 Qxd5 Nc3 Qa5 d4', None), ('e4 d5 e5 Bf5 d4', None), ('e4', 1.0)])
LESSONS = [
  dict(id='bsc-main', part='bsc-queen', root='e4 d5 exd5 Qxd5 Nc3 Qa5 d4', title='The Main Line: one setup', sub='Knight, c-pawn one square, bishop out, then the e-pawn', pri='core',
       why='A quarter of club players put the d-pawn in the middle on move four. Your setup comes out in the same order every game.', outcome='Solid, with every piece out'),
  dict(id='bsc-nf3', part='bsc-queen', root='e4 d5 exd5 Qxd5 Nc3 Qa5 Nf3', title='White develops first', sub='The same four moves, whatever White does', pri='core',
       why='Four in ten bring the king\'s knight out first. Nothing changes: knight, c-pawn, bishop, e-pawn.', outcome='Solid'),
  dict(id='bsc-d3', part='bsc-queen', root='e4 d5 exd5 Qxd5 Nc3 Qa5 d3', title='The small d-pawn', sub='Same setup; watch the knight jump that uncovers the bishop', pri='common',
       why='One in eight plays it slow. The bishop behind the knight is aimed at your queen, so the c-pawn move matters most.', outcome='Equal'),
  dict(id='bsc-4th', part='bsc-queen', root='e4 d5 exd5 Qxd5 Nc3 Qa5', title='Other fourth moves', sub='The Italian bishop, the edge pawn, an early check', pri='rare',
       why='Whatever comes on move four, the knight comes out and the c-pawn gives the queen a way home.', outcome='Equal'),
  dict(id='bsc-3nf3', part='bsc-third', root='e4 d5 exd5 Qxd5 Nf3', title='White waits with the knight', sub='Knight out, c-pawn; when the knight hits the queen, she goes to the side', pri='common',
       why='One in twelve keeps the queen\'s knight home for a move. It usually comes out next, and you are back in the main line.', outcome='Back in the main line'),
  dict(id='bsc-3rd', part='bsc-third', root='e4 d5 exd5 Qxd5', title='Other third moves', sub='The d-pawn at once: hit it with your e-pawn', pri='rare',
       why='With no knight hitting your queen, she stays in the middle and the e-pawn strikes.', outcome='Equal or better'),
  dict(id='bsc-e5', part='bsc-push', root='e4 d5 e5', title='The e-pawn pushes past', sub='Bishop out, e-pawn, then the c-pawn two squares', pri='core',
       why='Almost one in five won\'t take. Your bishop gets out before the e-pawn moves, and then the c-pawn hits the chain.', outcome='Comfortable'),
  dict(id='bsc-tennison', part='bsc-second', root='e4 d5 Nf3', title='The Tennison Gambit', sub='Take the pawn; when the knight jumps, the bishop guards it', pri='rare',
       why='One in twenty gives the e-pawn away. Take it and bring the bishop out behind it.', outcome='A pawn up'),
  dict(id='bsc-nc3', part='bsc-second', root='e4 d5 Nc3', title='Knight guards the e-pawn', sub='Take, then the bishop out at the knight', pri='rare',
       why='Take the pawn, and when the knight takes back your bishop comes out with a hit on it.', outcome='Equal'),
  dict(id='bsc-2nd', part='bsc-second', root='e4 d5', title='Other second moves', sub='Take the e-pawn when you can', pri='rare',
       why='The small d-pawn, the f-pawn, the d-pawn gambit. Take the e-pawn each time.', outcome='Equal or better'),
]
text, table = draft.emit(leaves, LESSONS, 'b')
PARTS = [
  ('bsc-queen', 'scandi', 'The queen to the side', 'Main Line', 'White takes, your queen takes back, and when the knight hits her she steps to the side. Then one setup: knight, c-pawn, bishop, e-pawn.'),
  ('bsc-third', 'scandi', 'White skips the knight', 'Third-move tries', 'No knight hits the queen yet. Carry on with the setup; against the d-pawn at once, your e-pawn strikes.'),
  ('bsc-push', 'scandi', 'White pushes past', 'Advance', 'The e-pawn steps past your d-pawn. Bishop out, e-pawn one square, then the c-pawn hits the chain.'),
  ('bsc-second', 'scandi', 'White doesn\'t take', 'Second-move tries', 'A gambit knight, a guarding knight, a slow pawn. Take the e-pawn whenever it is offered.'),
]
M = 'e4 d5 exd5 Qxd5 Nc3 Qa5'
NOTES = {
  'e4 d5': ('Scandinavian Defense', 'Hit the e-pawn on move one. White nearly always takes, and your queen comes out to take back.', ['key'], dict(arrows=['d5e4g'])),
  'e4 d5 exd5': ('White takes', 'Two in three take the pawn.'),
  'e4 d5 exd5 Qxd5': ('Queen takes back', 'She stands in the middle for one move. When the knight hits her, she steps to the side.', ['key']),
  'e4 d5 exd5 Qxd5 Nc3': ('Knight hits your queen', 'Eight in ten play this. The queen has to move, and she has a good square.'),
  M: ('Queen to the side', 'Nothing can hit her here yet. Next comes the setup, in the same order every game: knight, c-pawn, bishop, e-pawn.', ['key'], dict(arrows=['g8f6g', 'c7c6g'])),
  M + ' d4 Nf6': ('Knight out', 'The first move of the setup, every game.'),
  M + ' d4 Nf6 Bd2': ('Bishop beside the queen', 'It lines up on your queen from behind the knight. When the knight jumps, the bishop hits her.'),
  M + ' d4 Nf6 Bd2 c6': ('C-pawn one square', 'The queen gets a way home, and White\'s knight loses its best square in the middle. Play it before the bishop comes out.', ['key'], dict(arrows=['a5d8g'])),
  M + ' d4 Nf6 Bd2 c6 Nf3 Bf5': ('Bishop out', 'Outside the pawns before the e-pawn moves, the same idea as in the Caro-Kann and the Slav.', ['key']),
  M + ' d4 Nf6 Bd2 c6 Nf3 Bf5 Bc4 e6': ('E-pawn one square', 'The setup is complete. The queen\'s knight and the dark bishop come next, then castle.'),
  M + ' d4 Nf6 Bd2 c6 Ne4': ('Knight jumps and uncovers the bishop', 'The bishop now hits your queen. The c-pawn move gave her the way home.'),
  M + ' d4 Nf6 Bd2 c6 Ne4 Qd8': ('Queen goes home', 'Safe, and the knight in the middle will be traded.', ['key']),
  M + ' Nf3 Nf6': ('Knight out', 'The same first move of the setup.'),
  M + ' Nf3 Nf6 Bc4 c6 Ng5': ('Knight jumps at f7', 'It leaves the knight where your queen can take it.', ['warn']),
  M + ' Nf3 Nf6 Bc4 c6 Ng5 Qxg5': ('Take the knight', 'Your queen was looking along the rank the whole time. A clean piece.', ['key', 'trap'], dict(arrows=['a5g5g'])),
  'e4 d5 exd5 Qxd5 Nf3 Nf6 Nc3 Qa5': ('Queen to the side', 'The knight came out a move later, and you are in the main line.', ['key']),
  'e4 d5 exd5 Qxd5 d4 e5': ('E-pawn strikes', 'With no knight hitting your queen she holds the middle, and the e-pawn hits White\'s d-pawn at once.', ['key'], dict(arrows=['e5d4g'])),
  'e4 d5 e5': ('The e-pawn pushes past', 'White keeps the pawns on the board. Your bishop is free to leave first.'),
  'e4 d5 e5 Bf5': ('Bishop out first', 'Before the e-pawn shuts it in. Then the e-pawn one square and the c-pawn two.', ['key'], dict(arrows=['e7e6g', 'c7c5g'])),
  'e4 d5 e5 Bf5 d4 e6': ('E-pawn one square', 'The door closes behind the bishop.'),
  'e4 d5 e5 Bf5 d4 e6 Nf3 c5': ('C-pawn two squares', 'It hits the pawn that holds White\'s chain together. The queen\'s knight comes behind it.', ['key'], dict(arrows=['c5d4g'])),
  'e4 d5 Nf3 dxe4': ('Take the pawn', 'A free center pawn. The knight has to move again.', ['key']),
  'e4 d5 Nf3 dxe4 Ng5 Bf5': ('Bishop guards the pawn', 'Out before the e-pawn moves, and it holds the extra pawn.', ['key']),
  'e4 d5 Nc3 dxe4': ('Take the pawn', 'When the knight takes back, your bishop comes out with a hit on it.'),
  'e4 d5 Nc3 dxe4 Nxe4 Bf5': ('Bishop out at the knight', 'It gains a move: the knight has to step away.', ['key'], dict(arrows=['f5e4r'])),
  'e4 d5 d3 dxe4': ('Take the pawn', 'If White takes back, the queens come off and White can no longer castle.', ['key']),
  'e4 d5 d3 dxe4 dxe4 Qxd1+': ('Trade queens', 'The king has to take back and stays in the middle for the rest of the game.', ['key']),
}
allp = set()
for _, _, path, _ in table:
    t = path.split()
    for k in range(1, len(t) + 1): allp.add(' '.join(t[:k]))
drop = [k for k in NOTES if ' '.join(k.split()) not in allp]
print('notes without a node (dropped):', drop)
NOTES = {k: v for k, v in NOTES.items() if k not in drop}
auto = draft.named_moves([t[2] for t in table], 'b', skip=draft.base_paths('black'))
mod = draft.module_text("""Black against the e-pawn, another system: the Scandinavian. D-pawn two squares on move one, the queen takes back
and steps to the side, then one setup: knight, c-pawn one square, light bishop out, e-pawn one square. A separate pack
(see PACKS in bmeta.py). The lines were drafted with pipeline/draft.py: White's moves by the Maia 1300/1500 odds, yours
from the setup's order wherever Stockfish 17.1 accepts it and the engine's move elsewhere. SAN is internal only; notes
are plain English.""", 'from bcontent import L, P, J, n', PARTS, text, NOTES, auto, lambda p: f"P({', '.join(repr(x) for x in p)})")
open(paths.ROOT / 'content/black/bscandi.py', 'w').write(mod)
for lid, title, path, reach in table: print(f"{reach*100:5.2f} {lid:28s} {title:44s} {path[6:]}")
print(len(leaves), 'leaves')
draft.done()
