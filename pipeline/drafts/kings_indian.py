"""The King's Indian for Black (content/black/bkid.py): the setup's order, the moves fixed by hand, the lessons and the notes.
Run it to redraft the pack (python3 pipeline/drafts/kings_indian.py); it overwrites the module, so notes are edited here."""
import sys, re, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import paths, chess, draft
def system(b, path):
    # one setup in one order: knight, g-pawn, bishop, d-pawn, castle, then the e-pawn; the knight in front of it, and
    # when White closes the middle the knight drops back beside the king and the f-pawn goes
    base = ['Nf6', 'g6', 'Bg7', 'd6', 'O-O', 'e5', 'Nc6', 'Ne7', 'Nd7', 'Nfd7', 'f5', 'Nbd7', 'c6', 'Re8']
    W, B, P, N, Bi = chess.WHITE, chess.BLACK, chess.PAWN, chess.KNIGHT, chess.BISHOP
    def on(sq, pt, col):
        x = b.piece_at(sq)
        return x is not None and x.piece_type == pt and x.color == col
    # the queen's knight in front of White's own c-pawn, and the e-pawn free to go two: your d-pawn goes two squares
    if on(chess.C3, N, W) and on(chess.C2, P, W) and on(chess.D7, P, B) and not on(chess.E4, P, W):
        return ['d5'] + base
    # the bishop at your knight: the queen's knight backs up the e-pawn before it goes
    if on(chess.G5, Bi, W) and on(chess.E7, P, B) and on(chess.B8, N, B) and on(chess.D6, P, B) and b.castling_rights & chess.BB_H8 == 0:
        i = base.index('e5')
        return base[:i] + ['Nbd7'] + base[i:]
    return base
fixed = {'d4': 'Nf6', 'd4 Nf6 c4 g6 Bg5': 'Bg7',
         'd4 Nf6 c4 g6 Nc3 Bg7 e4 d6 f4 O-O Nf3 e5 dxe5': 'dxe5',
         'd4 Nf6 e3 g6 Bd3 Bg7 f4 d6 Nf3 O-O O-O': 'c5',
         'd4 Nf6 c4 g6 Nc3 Bg7 e4 d6 f4 O-O e5': 'dxe5',
         'd4 Nf6 Nf3 g6 e3 Bg7 Bd3': 'd6', 'd4 Nf6 e3 g6 Bd3 Bg7 Nf3': 'd6', 'd4 Nf6 e3 g6 Nf3 Bg7 Bd3': 'd6'}
W = draft.Walk('b', system, fixed, known=draft.known_from('black', skip_chapters=('kid', 'kidx')), tol=40,
               thr=lambda n, r: 0.03 if n <= 3 else 0.04 if n <= 5 else 0.06 if n <= 9 else 0.09, min_reach=0.0010,
               depth=lambda r: 18 if r >= 0.02 else 16 if r >= 0.006 else 14 if r >= 0.002 else 12)
leaves = W.run([('d4 Nf6 c4 g6 Nc3 Bg7 e4 d6 Nf3 O-O Be2', None), ('d4 Nf6 c4 g6 Nc3 Bg7 e4', None), ('d4 Nf6 c4', None), ('d4', 1.0)])
C4 = 'd4 Nf6 c4 g6 Nc3 Bg7'
LESSONS = [
  dict(id='bki-main', part='bki-center', root=C4 + ' e4 d6 Nf3', title='The Classical: castle, then the e-pawn', sub='Castle, e-pawn two squares, then the knight in front of the c-pawn', pri='core',
       why='The setup White players aim for: three pawns in the middle and both knights out. You castle and hit that middle with the e-pawn.', outcome='A full fight; your play is on the kingside'),
  dict(id='bki-f4', part='bki-center', root=C4 + ' e4 d6 f4', main=C4 + ' e4 d6 f4 O-O Nf3', title='The Four Pawns Attack', sub='Castle, then the e-pawn hits the wall', pri='common',
       why='One in nine pushes a fourth pawn. A wall that wide is hard to guard, and your e-pawn hits it at once.', outcome='A sharp, open fight'),
  dict(id='bki-bg5', part='bki-center', root=C4 + ' e4 d6 Bg5', title='The bishop comes at your knight', sub='Castle; the queen\'s knight backs up the e-pawn', pri='common',
       why='One in ten brings the bishop out first. Castle as usual, and get the queen\'s knight behind the e-pawn before it goes.', outcome='Equal'),
  dict(id='bki-5th', part='bki-center', root=C4 + ' e4 d6', title='Other fifth moves', sub='The same two moves: castle, then the e-pawn', pri='common',
       why='The bishop in the middle, the small edge pawn, the pawn that guards the e-pawn. Castle and strike with the e-pawn.', outcome='Equal'),
  dict(id='bki-nf3', part='bki-quiet', root=C4 + ' Nf3', title='Knights out without a big center', sub='D-pawn, castle, and the e-pawn when the knight backs it up', pri='core',
       why='A quarter of club players leave the e-pawn at home. Your five moves don\'t change.', outcome='Equal'),
  dict(id='bki-4th', part='bki-quiet', root=C4, title='Other fourth moves', sub='The early bishop, the small e-pawn', pri='common',
       why='Whatever White does on move four, the d-pawn and castling come next.', outcome='Equal'),
  dict(id='bki-3rd', part='bki-quiet', root='d4 Nf6 c4 g6', title='Other third moves', sub='King\'s knight first, the small e-pawn, the early bishop', pri='common',
       why='One in three holds the queen\'s knight back. Bishop to the long diagonal, d-pawn, castle.', outcome='Equal'),
  dict(id='bkx-london', part='bkx-bishop', root='d4 Nf6 Bf4', title='The London System', sub='The same five moves; then the knight and the e-pawn', pri='core',
       why='One in seven plays the London. Your bishop on the long diagonal is a good piece against it, and the e-pawn push hits the London bishop.', outcome='Equal, with easy moves'),
  dict(id='bkx-nf3', part='bkx-bishop', root='d4 Nf6 Nf3', title='King\'s knight first', sub='The setup against the London, the Torre and the Colle by this move order', pri='core',
       why='One in eight starts with the knight and chooses a system on move three. Your setup is the same against all of them.', outcome='Equal'),
  dict(id='bkx-e3', part='bkx-other', root='d4 Nf6 e3', title='The small e-pawn', sub='Colle setups: fianchetto, d-pawn, castle', pri='common',
       why='One in ten shuts the dark bishop in. Nothing to fear, and nothing changes.', outcome='Equal'),
  dict(id='bkx-nc3', part='bkx-other', root='d4 Nf6 Nc3', title='Queen\'s knight first: stop the e-pawn', sub='D-pawn two squares, then the bishop out', pri='common',
       why='White wants the e-pawn in the middle next. This is the one time your d-pawn goes two squares: it stops that, and your light bishop comes out.', outcome='Equal'),
  dict(id='bkx-tromp', part='bkx-other', root='d4 Nf6 Bg5', title='The Trompowsky', sub='G-pawn anyway; if the bishop takes, the e-pawn takes back', pri='rare',
       why='The bishop comes at your knight on move two. Carry on: if it takes, you get the two bishops and an open file.', outcome='Equal'),
]
text, table = draft.emit(leaves, LESSONS, 'b')
RETITLE = {'bki-nf3-e4': 'E-pawn two squares after all', 'bki-f4-e5': 'E-pawn pushes at your knight', 'bki-f4-fxe5': 'F-pawn takes your e-pawn',
           'bki-f4-dxe5': 'D-pawn takes, queens come off', 'bki-main-dxe5': 'D-pawn takes, queens come off',
           'bki-main-oo': 'White castles and keeps the middle open'}
for lid, t in RETITLE.items():
    text, k = re.subn(r"\('" + lid + r"', '(?:[^'\\]|\\.)*',", "('" + lid + "', '" + t.replace("'", "\\'") + "',", text)
    assert k == 1, lid
PARTS = [
  ('bki-center', 'kid', 'White takes the whole center', 'Classical & Four Pawns', 'Three or four pawns in a row. Castle, then the e-pawn strikes; when the middle closes, your knight steps back and the f-pawn starts the attack.'),
  ('bki-quiet', 'kid', 'White holds the e-pawn back', 'Quiet setups', 'No big center, so no hurry. The same five moves, then the e-pawn when a knight backs it up.'),
  ('bkx-bishop', 'kidx', 'The bishop comes out first', 'London & Torre', 'White\'s dark bishop leaves before the e-pawn. Your setup stays the same, and the e-pawn push gains a move on that bishop.'),
  ('bkx-other', 'kidx', 'Other second moves', 'Colle, Jobava, Trompowsky', 'The small e-pawn, the queen\'s knight, the bishop at your knight. One of them needs your d-pawn to go two squares.'),
]
NOTES = {
  'd4 Nf6': ('Knight first', 'The first move of the King\'s Indian setup: knight, g-pawn, bishop, d-pawn, castle. The same five moves against almost everything.', ['key']),
  'd4 Nf6 c4 g6': ('G-pawn one square', 'It makes room for the bishop on the long diagonal.', ['key'], dict(arrows=['f8g7g'])),
  C4: ('Bishop to the long diagonal', 'It looks through the middle at White\'s d-pawn. Everything you do later is about opening this diagonal.', ['key']),
  C4 + ' e4 d6': ('D-pawn one square', 'It keeps White\'s e-pawn from pushing on at your knight, and gets your own e-pawn ready.', ['key']),
  C4 + ' e4 d6 Nf3 O-O': ('Castle', 'King safe before the middle opens.'),
  C4 + ' e4 d6 Nf3 O-O Be2 e5': ('E-pawn two squares', 'The strike the whole setup was built for.', ['key'], dict(arrows=['e5d4g'])),
  C4 + ' e4 d6 Nf3 O-O Be2 e5 O-O Nc6': ('Knight in front of the c-pawn', 'More pressure on the d-pawn. When White pushes it past, the knight drops back beside the king and your f-pawn goes.', ['key']),
  C4 + ' e4 d6 Nf3 O-O Be2 e5 d5': ('White closes the middle', 'Now the play is on the wings, and yours is the king\'s side.'),
  C4 + ' e4 d6 f4': ('Four Pawns Attack', 'A fourth pawn joins the wall. It takes time, and the wall has to be guarded.'),
  C4 + ' e4 d6 f4 O-O': ('Castle', 'Let White build. Your e-pawn hits the wall next.'),
  'd4 Nf6 Bf4 g6': ('G-pawn one square', 'The same setup against the London. Your bishop will look straight down the long diagonal.'),
  'd4 Nf6 Bg5 g6': ('G-pawn anyway', 'If the bishop takes the knight, the e-pawn takes back and your bishop has the long diagonal to itself.', ['key']),
  'd4 Nf6 Bg5 g6 Bxf6 exf6': ('E-pawn takes back', 'Toward the middle. You have the two bishops and an open file for the rook.', ['key']),
  'd4 Nf6 Nc3 d5': ('D-pawn two squares', 'The one time the d-pawn goes two. White\'s e-pawn can no longer walk into the middle for free.', ['key'], dict(arrows=['d5e4r'])),
  'd4 Nf6 Nf3 g6 Nc3 d5': ('D-pawn two squares', 'The queen\'s knight is out with the c-pawn still at home, so the e-pawn wants to go two squares next. Your d-pawn stops it.', ['key'], dict(arrows=['d5e4r'])),
  'd4 Nf6 Bf4 g6 Nc3 d5': ('D-pawn two squares', 'Queen\'s knight in front of the c-pawn: the e-pawn is coming. Stop it, then carry on with the bishop and castling.', ['key'], dict(arrows=['d5e4r'])),
  'd4 Nf6 e3 g6 Bd3 Bg7 f4 d6 Nf3 O-O O-O c5': ('C-pawn two squares', 'White\'s f-pawn holds the square your e-pawn wants. Hit the d-pawn from the other side instead.', ['key'], dict(arrows=['c5d4g'])),
  C4 + ' e4 d6 f4 O-O e5 dxe5': ('Take it', 'The pawn came at your knight a move too early. Take it, and the wall has a hole in it whichever way White takes back.', ['key']),
  C4 + ' e4 d6 Bg5 O-O Qd2 Nbd7': ('Queen\'s knight behind the e-pawn', 'With the bishop at your knight, the e-pawn waits one move: this knight guards the other one first.', ['key']),
  'd4 Nf6 c4 g6 Nf3 Bg7 Bg5 Ne4': ('Knight jumps at the bishop', 'The bishop has to move again, and the long diagonal is open for yours.', ['key']),
}
allp = set()
for _, _, path, _ in table:
    t = path.split()
    for k in range(1, len(t) + 1): allp.add(' '.join(t[:k]))
drop = [k for k in NOTES if ' '.join(k.split()) not in allp]
print('notes without a node (dropped):', drop)
NOTES = {k: v for k, v in NOTES.items() if k not in drop}
auto = draft.named_moves([t[2] for t in table], 'b', skip=draft.base_paths('black'))
mod = draft.module_text("""Black against the d-pawn, another system: the King's Indian. One setup in one order against nearly everything: knight,
g-pawn one square, bishop to the long diagonal, d-pawn one square, castle, then the e-pawn two squares. A separate pack
(see PACKS in bmeta.py) with two chapters: White's c-pawn systems, and the London, Colle, Trompowsky and Jobava. The
lines were drafted with pipeline/draft.py: White's moves by the Maia 1300/1500 odds, yours from the setup's order
wherever Stockfish 17.1 accepts it and the engine's move elsewhere. SAN is internal only; notes are plain English.""",
  'from bcontent import L, P, J, n', PARTS, text, NOTES, auto, lambda p: f"P({', '.join(repr(x) for x in p)})")
open(paths.ROOT / 'content/black/bkid.py', 'w').write(mod)
for lid, title, path, reach in table: print(f"{reach*100:5.2f} {lid:26s} {title:50s} {path[7:]}")
print(len(leaves), 'leaves')
print('FLAGS'); [print('  ', f) for f in W.flags]

draft.done()
