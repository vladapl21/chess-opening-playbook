"""The Ruy Lopez for White (content/white/ruylopez.py): the setup's order, the moves fixed by hand, the lessons and the
notes. Run it to redraft the pack (python3 pipeline/drafts/ruy_lopez.py); it overwrites the module, so notes are edited here."""
import sys, re, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import paths, chess, draft
def system(b, path):
    # the bishop comes at the knight; when a pawn asks, it steps back, and again to the diagonal at f7. Then one setup:
    # castle, rook beside the king, c-pawn one square, the small h-pawn, d-pawn two squares, and the queen's knight
    # goes round behind them to the kingside
    W, B, P, N, Bi, R, K = chess.WHITE, chess.BLACK, chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.KING
    def on(sq, pt, col=W):
        x = b.piece_at(sq)
        return x is not None and x.piece_type == pt and x.color == col
    order = ['Bb5'] if on(chess.F1, Bi) else []
    if on(chess.B5, Bi) and on(chess.A6, P, B): order.append('Ba4')
    if on(chess.A4, Bi) and on(chess.B5, P, B): order.append('Bb3')
    order.append('O-O')
    if on(chess.G1, K) and on(chess.F1, R): order.append('Re1')
    if on(chess.C2, P): order.append('c3')
    if on(chess.H2, P) and on(chess.C3, P): order.append('h3')
    if on(chess.D2, P): order.append('d4')
    if on(chess.B1, N) and on(chess.C3, P): order.append('Nbd2')
    if on(chess.D2, N) and on(chess.E1, R): order.append('Nf1')
    if on(chess.F1, N): order.append('Ng3')
    return order
K2 = 'e4 e5 Nf3 Nc6'
R0 = K2 + ' Bb5'
M = R0 + ' a6 Ba4 Nf6'
C = M + ' O-O Be7 Re1 b5 Bb3 d6 c3 O-O h3'
# the small d-pawn shuts Black's bishop in: open the middle at once; the knight that jumps in is taken; before the
# d-pawn gambit (the Marshall) the small h-pawn comes first
fixed = {K2: 'Bb5', R0 + ' a6': 'Ba4', R0 + ' a6 Ba4 b5': 'Bb3', R0 + ' d6': 'd4', R0 + ' d6 d4 exd4': 'Nxd4', R0 + ' Nd4': 'Nxd4', M + ' O-O Be7 Re1 b5 Bb3 O-O': 'h3'}
W = draft.Walk('w', system, fixed, known=draft.known_from('white', skip_chapters=('italian', 'italians', 'ruy')), tol=45,
               thr=lambda n, r: 0.03 if n <= 6 else 0.05 if n <= 10 else 0.08 if n <= 14 else 0.10, min_reach=0.001,
               depth=lambda r: 20 if r >= 0.02 else 18 if r >= 0.005 else 16 if r >= 0.002 else 14)
# the main lines as they are played when Black knows them (rare at club level, so given by hand), then the tree by the odds
leaves = W.run([(C + ' Na5', None), (C + ' Nb8', None), (C + ' Bb7', None), (M + ' O-O Be7 Re1 b5 Bb3 O-O', None), (M + ' O-O Nxe4', None), (R0 + ' Nf6 O-O Nxe4', None), (R0 + ' f5', None), (M, None), (R0 + ' a6 Ba4 b5', None), (R0 + ' a6', None), (K2, None)])
LESSONS = [
  dict(id='rl-main', part='rl-morphy', root=M, main=C + ' Na5', title='The Closed Ruy Lopez', sub='Castle, rook, bishop back, c-pawn, h-pawn, then the d-pawn', pri='core',
       why='The most famous position in chess. Your bishop has stepped back twice and still looks at f7, the king is safe, and the c-pawn is ready to back the d-pawn up.', outcome='A lasting edge in the middle'),
  dict(id='rl-b5', part='rl-morphy', root=R0 + ' a6 Ba4 b5', main=R0 + ' a6 Ba4 b5 Bb3 Nf6 O-O', title='The pawns chase the bishop', sub='Two steps back, and it stands on the diagonal it wanted', pri='core',
       why='Four in ten club players push the second pawn at once. The bishop lands on the diagonal at f7 with nothing lost, and Black\'s pawns are a target for your a-pawn.', outcome='A better Italian'),
  dict(id='rl-a6', part='rl-morphy', root=R0 + ' a6', title='After the a-pawn: other tries', sub='The bishop out, the small d-pawn', pri='common',
       why='Black asks the bishop and then develops another way. Castle, and the setup comes out in its order.', outcome='A small edge'),
  dict(id='rl-berlin', part='rl-third', root=R0 + ' Nf6', main=R0 + ' Nf6 O-O Nxe4 Re1 Nd6 Nxe5', title='The Berlin: the knight hits your e-pawn', sub='Castle anyway; the pawn comes back', pri='core',
       why='One in five hits the e-pawn at once. Castle: if the knight takes, the open file in front of Black\'s king gets you the pawn back with a move gained.', outcome='A small edge'),
  dict(id='rl-steinitz', part='rl-third', root=R0 + ' d6', title='The Steinitz: the small d-pawn', sub='Open the middle while the knight is pinned', pri='core',
       why='One in four guards the e-pawn this way. The d-pawn has left the knight pinned to the king, so you open the middle at once.', outcome='More room'),
  dict(id='rl-classical', part='rl-third', root=R0 + ' Bc5', main=R0 + ' Bc5 O-O d6 Re1 Nf6 c3', title='The Classical: the bishop comes out', sub='Castle, then the c-pawn and the d-pawn hit it', pri='common',
       why='Black develops as in the Italian. The c-pawn and the d-pawn come at the bishop with a move gained.', outcome='A big center'),
  dict(id='rl-bird', part='rl-third', root=R0 + ' Nd4', title='The Bird: the knight jumps in', sub='Take it, castle, and play round the pawn', pri='common',
       why='The knight moves twice to hit your bishop. Take it: Black\'s pawn ends up alone in the middle.', outcome='Better for you'),
  dict(id='rl-cozio', part='rl-third', root=R0 + ' Nge7', title='The Cozio: the other knight', sub='Castle, then c-pawn and d-pawn', pri='common',
       why='Black backs one knight up with the other and blocks the bishop. The setup comes out untouched.', outcome='More room'),
  dict(id='rl-schliemann', part='rl-third', root=R0 + ' f5', title='The Schliemann: the f-pawn gambit', sub='Leave the pawn and bring the knight out', pri='rare',
       why='Black offers a pawn to open the f-file. You don\'t need it: the knight comes out and Black\'s king is the one in the draught.', outcome='Better for you'),
  dict(id='rl-third', part='rl-third', root=R0, title='Other third moves', sub='The queen out, the fianchetto, the bishop check', pri='common',
       why='Whatever Black tries on move three, you castle and the pawns take the middle.', outcome='Better for you'),
]
text, table = draft.emit(leaves, LESSONS, 'w')
PARTS = [
  dict(id='rl-morphy', ch='ruy', title='The a-pawn asks the bishop', kicker='Morphy Defense', blurb='Black\'s a-pawn asks your bishop what it wants, and it steps back; if the b-pawn follows, it steps back again and stands on the diagonal at f7. Then the setup: castle, rook beside the king, c-pawn one square, the small h-pawn move, and the d-pawn two squares.'),
  dict(id='rl-third', ch='ruy', title='Black leaves the bishop alone', kicker='Berlin, Steinitz, Classical, Bird', blurb='The third moves without the a-pawn. Castle first almost every time; the small d-pawn is met by opening the middle, and the knight that jumps in is taken.'),
]
NOTES = {
  R0: ('Bishop comes at the knight', 'That knight guards the e-pawn. Nothing is threatened yet, but every move Black makes has to keep it in mind.', ['key'], dict(arrows=['b5c6r', 'c6e5g'])),
  R0 + ' a6 Ba4': ('Bishop steps back', 'It still looks at the knight. Taking it would give up the bishop for little.', ['key']),
  R0 + ' a6 Ba4 b5 Bb3': ('Bishop steps back again', 'Now it stands on the diagonal at f7, and Black\'s pawns on the wing have moved forward for nothing.', ['key'], dict(arrows=['b3f7r'])),
  M + ' O-O': ('Castle', 'The e-pawn can be left: if the knight takes it, the rook comes to the open file in front of Black\'s king.', ['key']),
  M + ' O-O Be7 Re1': ('Rook beside the king', 'Now the e-pawn is guarded, and the threat to win Black\'s e-pawn is real.', ['key'], dict(arrows=['e1e4g'])),
  M + ' O-O Be7 Re1 b5 Bb3 d6 c3': ('C-pawn one square', 'It backs up the d-pawn\'s push, and gives the bishop a way back if a knight comes after it.', ['key'], dict(arrows=['c3d4g'])),
  C: ('The small h-pawn move', 'Black\'s bishop can\'t pin your knight now. Next the d-pawn goes two squares.', ['key']),
  R0 + ' Nf6 O-O': ('Castle', 'Leave the e-pawn. If the knight takes it, your rook or your d-pawn opens the middle in front of Black\'s king.', ['key']),
  R0 + ' d6 d4': ('D-pawn two squares', 'The d-pawn move left the knight pinned to the king. Open the middle while it can\'t move.', ['key'], dict(arrows=['b5e8r', 'd4e5r'])),
  R0 + ' d6 d4 exd4 Nxd4': ('Knight takes back', 'It stands in the middle and adds to the weight on the pinned knight.', ['key'], dict(arrows=['d4c6r', 'b5c6r'])),
  R0 + ' Nd4 Nxd4': ('Take the knight', 'It moved twice to get there. After the trade Black\'s pawn stands alone in the middle.', ['key']),
  R0 + ' Bc5 O-O': ('Castle', 'Then the c-pawn and the d-pawn come at the bishop.', ['key']),
}
allp = set()
for _, _, path, _ in table:
    t = path.split()
    for k in range(1, len(t) + 1): allp.add(' '.join(t[:k]))
drop = [k for k in NOTES if ' '.join(k.split()) not in allp]
print('notes without a node (dropped):', drop)
# a position the rest of the book already has a note for keeps that note (the first moves are shared with the Italian)
import types
for m in ('ruylopez', 'wfill'): sys.modules[m] = types.ModuleType(m)
sys.path.insert(0, str(paths.ROOT / 'content/white')); import content, content2  # noqa: F401  (content2 registers the later chapters' notes)
have = set(content.NOTES); shared = [k for k in NOTES if ' '.join(k.split()) in have]
print('notes the book already has (kept as they are):', shared)
NOTES = {k: v for k, v in NOTES.items() if k not in drop and k not in shared}
auto = draft.named_moves([t[2] for t in table], 'w', skip=have)
mod = draft.module_text("""White after both knights come out, a third way: the Ruy Lopez, a pack for the slot 'whiteItalian' beside the two
Italians (see PACKS in content2_meta.py).

The bishop comes at the knight that guards the e-pawn. When a pawn asks, it steps back, and again to the diagonal at
f7. Then one setup: castle, rook beside the king, c-pawn one square, the small h-pawn move, d-pawn two squares. The
lines were drafted with pipeline/draft.py: Black's moves by the Maia 1300/1500 odds, yours from the setup's order
wherever Stockfish 17.1 accepts it and the engine's move elsewhere. SAN is internal; notes are plain English.""",
  'from content import n, J, L, PARTS', [PARTS], text, NOTES, auto, lambda ps: 'PARTS.extend([\n' + ''.join(f"  dict(id={p['id']!r}, ch={p['ch']!r}, title={p['title']!r}, kicker={p['kicker']!r},\n       blurb={p['blurb']!r}),\n" for p in ps) + '])')
open(paths.ROOT / 'content/white/ruylopez.py', 'w').write(mod)
for lid, title, path, reach in table: print(f"{reach*100:5.2f} {lid:24s} {title:58s} {path[6:]}")
print(len(leaves), 'leaves')
print('FLAGS'); [print('  ', f) for f in W.flags]
draft.done()
