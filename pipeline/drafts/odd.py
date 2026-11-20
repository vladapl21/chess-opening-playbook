"""Odd first, second and third moves for the two house books: named sidelines that were missing. Writes
content/black/bodd.py and content/white/odd.py."""
import sys, re, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import paths, chess, draft
which = sys.argv[1]
if which == 'black':
    def system(b, path):
        if path.startswith('e4 e5'): return ['Nf6', 'Nc6', 'Bc5', 'd5', 'O-O', 'd6']
        return ['e5', 'd5', 'Nf6', 'Nc6', 'Bc5', 'Bd6', 'O-O']
    ROOTS1 = ['h4', 'a4', 'f3', 'Nh3', 'Na3']
    ROOTS2 = ['e4 e5 ' + m for m in ['Ke2', 'Bb5', 'Ne2', 'a3', 'c4', 'Qe2', 'Bd3', 'b3', 'g3']]
    ROOTS3 = ['e4 e5 Nf3 Nc6 Nc3 Nf6 Nxe5']
    W = draft.Walk('b', system, {}, known=draft.known_from('black', skip_chapters=('scandi', 'kid', 'kidx')), tol=30, thr=0.12, min_reach=0.0009,
                   depth=lambda r: 12, follow=True)
    leaves = W.run([(r, 0.02) for r in ROOTS3] + [(r, 0.012) for r in ROOTS2 + ROOTS1])
    LESSONS = [
      dict(id='bv-halloween', part='bv-4n', roots=ROOTS3, title='The Halloween Gambit', sub='Take the knight; when the pawns come, the knights step back and you keep the piece', pri='rare',
           why='White gives a knight for your e-pawn and a wall of pawns. It only works if you panic.', outcome='A piece up'),
      dict(id='ba-odd2', part='ba-odd', roots=ROOTS2, main='e4 e5 Ke2', title='The Bongcloud and other odd second moves', sub='Knights out, bishop out, castle: the same moves as always', pri='rare',
           why='The king walks, a bishop pokes, a knight tucks in. None of them needs a special answer: develop and take the middle.', outcome='Better for you'),
      dict(id='bo-odd', part='bo-rare', roots=ROOTS1, main='h4', title='The Kádas, the Ware and the knights on the rim', sub='E-pawn and d-pawn in the middle, then the knights', pri='rare',
           why='Edge pawns and edge knights on move one. Take the middle with both pawns and develop behind them.', outcome='Better for you'),
    ]
    PARTS = [('ba-odd', 'attacks', 'Odd second moves', 'Bongcloud, Portuguese, Alapin', 'The king walks, the bishop pokes at nothing, the knight tucks in. Your own moves don\'t change.')]
    DOC = """Black, the house books: odd moves that were missing. The Halloween Gambit in the Four Knights, White's odd second moves
after the e-pawns (the Bongcloud, the Portuguese, the Alapin and others) and odd first moves (the Kádas, the Ware, the
Barnes, the Amar, the Sodium Attack). Drafted with pipeline/draft.py from the positions the book already answers:
a known position keeps its move, a new one takes the first developing move Stockfish 17.1 accepts. SAN is internal."""
    IMP, part_call, out, me, skip = 'from bcontent import L, P, J, n', (lambda p: f"P({', '.join(repr(x) for x in p)})"), 'content/black/bodd.py', 'b', 'black'
    NOTES = {
      'e4 e5 Nf3 Nc6 Nc3 Nf6 Nxe5 Nxe5': ('Take the knight', 'A piece for a pawn. White gets two moves with the pawns for it, and that is all.', ['key']),
    }
else:
    def system(b, path):
        if path.startswith('e4 e5 Nf3'): return ['Bc4', 'd4', 'c3', 'O-O', 'Nc3']
        return ['d4', 'Nf3', 'Nc3', 'Bc4', 'Bd3', 'O-O']
    ROOTS1 = ['e4 ' + m for m in ['g5', 'f6', 'a5', 'h5', 'Na6', 'Nh6', 'f5', 'h6']]
    ROOTS2 = ['e4 e5 Nf3 ' + m for m in ['Qe7', 'Bd6', 'Bb4', 'c6', 'g6', 'h6', 'a6']]
    ROOTS3 = ['e4 e5 Nf3 Nc6 Bc4 ' + m for m in ['g6', 'Qf6', 'Qe7', 'Bb4', 'Na5', 'a6', 'Bd6']]
    W = draft.Walk('w', system, {}, known=draft.known_from('white', skip_chapters=('english', 'engsym', 'engrare', 'london', 'lindian', 'lrare')), tol=30, thr=0.12, min_reach=0.0009,
                   depth=lambda r: 12, follow=True)
    leaves = W.run([(r, 0.012) for r in ROOTS3 + ROOTS2 + ROOTS1])
    LESSONS = [
      dict(id='it-odd', part='odd', roots=ROOTS3, main='e4 e5 Nf3 Nc6 Bc4 g6', title='Odd third moves', sub='Center pawns first; when a piece hangs, take it', pri='rare',
           why='The fianchetto, the early queen, the knight to the rim. Each leaves something loose, and the same c-pawn and d-pawn plan finds it.', outcome='Better for you'),
      dict(id='x-odd', part='e5x-misc', roots=ROOTS2, main='e4 e5 Nf3 Qe7', title='The Gunderam and other odd second moves', sub='Bishop out or d-pawn two squares, then castle', pri='rare',
           why='The queen in front of the bishop, the bishop in front of the d-pawn. Black blocks their own pieces: develop and open the middle.', outcome='Better for you'),
      dict(id='rr-odd', part='rare-all', roots=ROOTS1, main='e4 g5', title='The Borg, the Barnes and other odd first moves', sub='Both center pawns, then knights and bishops', pri='rare',
           why='Edge pawns and the f-pawn on move one. Take the middle with both pawns; one of these loses at once to the queen.', outcome='Winning or close to it'),
    ]
    PARTS = []
    DOC = """White, the house book: odd moves that were missing. Black's odd first moves (the Borg, the Barnes, the Ware, the
Goldsmith, the Lemming, the Adams, the Duras Gambit, the Carr), odd second moves after the knight (the Gunderam and
others) and odd third moves in the Italian. Drafted with pipeline/draft.py from the positions the book already answers:
a known position keeps its move, a new one takes the first developing move Stockfish 17.1 accepts. SAN is internal."""
    IMP, part_call, out, me, skip = 'from content import n, J, L, PARTS', None, 'content/white/odd.py', 'w', 'white'
    NOTES = {}
text, table = draft.emit(leaves, LESSONS, me)
text = text.replace("'King\\'s Pawn Opening", "'Small b-pawn move")       # 2.b3 has no name of its own
allp = set()
for _, _, path, _ in table:
    t = path.split()
    for k in range(1, len(t) + 1): allp.add(' '.join(t[:k]))
drop = [k for k in NOTES if ' '.join(k.split()) not in allp]
print('notes without a node (dropped):', drop)
NOTES = {k: v for k, v in NOTES.items() if k not in drop}
auto = draft.named_moves([t[2] for t in table], me, skip=draft.base_paths(skip))
auto = {k: v for k, v in auto.items() if v != "King's Pawn Opening"}   # the family's name, not a line's
mod = draft.module_text(DOC, IMP, PARTS, text, NOTES, auto, part_call)
open(paths.ROOT / out, 'w').write(mod)
for lid, title, path, reach in table: print(f"{lid:26s} {title:58s} {path}")
print(len(leaves), 'leaves')
print('FLAGS'); [print('  ', f) for f in W.flags]
draft.done()
