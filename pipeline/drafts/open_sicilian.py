"""The Open Sicilian for White (content/white/sicopen.py): the setup's order, the moves fixed by hand, the lessons and the notes.
Run it to redraft the pack (python3 pipeline/drafts/open_sicilian.py); it overwrites the module, so notes are edited here."""
import sys, re, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import paths, chess, draft
def system(b, path):
    # one setup in one order: knight, d-pawn two squares, take back with the knight, queen's knight, f-pawn one square
    # (it guards the e-pawn and keeps Black's knight off the bishop), bishop beside the queen, queen, castle long, g-pawn
    W, P, N, Bi, Q = chess.WHITE, chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.QUEEN
    def on(sq, pt):
        x = b.piece_at(sq)
        return x is not None and x.piece_type == pt and x.color == W
    order = (['Nf3'] if on(chess.G1, N) else []) + (['d4'] if on(chess.D2, P) else []) + ['Nxd4'] + (['Nc3'] if on(chess.B1, N) else [])
    order += (['f3'] if on(chess.F2, P) else []) + (['Be3'] if on(chess.C1, Bi) else []) + (['Qd2'] if on(chess.D1, Q) else [])
    return order + ['O-O-O'] + (['g4', 'Kb1', 'h4'] if on(chess.C1, chess.KING) else [])       # the pawns go only once the king is tucked away
S = 'e4 c5 Nf3'
D = S + ' d6 d4 cxd4 Nxd4 Nf6 Nc3'
N = S + ' Nc6 d4 cxd4 Nxd4'
E = S + ' e6 d4 cxd4 Nxd4'
# the Accelerated Dragon: Black saved the d-pawn's move to push it two squares at once, so the bishop stops that first
fixed = {'e4 c5': 'Nf3', N + ' g6 Nc3 Bg7 Be3 Nf6': 'Bc4', N + ' g6 Nc3 Bg7 Be3 Nf6 Bc4 O-O': 'Bb3',
         D + ' g6 f3 Bg7 Be3 O-O Qd2 Nc6 O-O-O d5': 'exd5'}
W = draft.Walk('w', system, fixed, known=draft.known_from('white', skip_chapters=('sic', 'sico')), tol=45,
               thr=lambda n, r: 0.012 if n <= 4 else 0.04 if n <= 6 else 0.05 if n <= 10 else 0.09, min_reach=0.0004,
               depth=lambda r: 18 if r >= 0.01 else 16 if r >= 0.002 else 14 if r >= 0.001 else 12)
# the main lines as they go when Black knows them (rare at club level, so they are given by hand), then the tree by the odds
leaves = W.run([(D + ' a6 f3 e5 Nb3 Be6 Be3 Be7 Qd2 O-O O-O-O Nbd7', None), (D + ' a6 f3 e6 Be3 b5 Qd2 Bb7 O-O-O Nbd7', None),
                (D + ' g6 f3 Bg7 Be3 O-O Qd2 Nc6 O-O-O d5', None), (D + ' g6 f3 Bg7 Be3 O-O Qd2 Nc6 O-O-O Bd7', None),
                (D + ' Nc6 f3 e5 Nb3 Be7 Be3 O-O Qd2 Be6 O-O-O a5', None), (D + ' e6 f3 Be7 Be3 O-O Qd2 Nc6 O-O-O a6', None),
                (N + ' Nf6 Nc3 e5', None), (D + ' a6', None), (D + ' g6', None), (E + ' Nc6', None), (E + ' a6', None), ('e4 c5', None)])
LESSONS = [
  dict(id='so-najdorf', part='so-d6', root=D + ' a6', main=D + ' a6 f3 e5', title='The Najdorf', sub='F-pawn, bishop, queen, castle long, then the g-pawn', pri='core',
       why='Black\'s small a-pawn move is the most famous Sicilian. Your setup doesn\'t care: the same five moves, then the pawns roll at Black\'s king.', outcome='An attack with the pieces behind it'),
  dict(id='so-dragon', part='so-d6', root=D + ' g6', main=D + ' g6 f3 Bg7 Be3 O-O Qd2 Nc6 O-O-O Bd7', title='The Dragon', sub='The same setup; trade off the bishop on the long diagonal', pri='core',
       why='Black\'s bishop goes to the long diagonal. Your setup is made for it: queen and bishop line up to trade that bishop, and the edge pawn opens the file.', outcome='A race you start first'),
  dict(id='so-classical', part='so-d6', root=D + ' Nc6', main=D + ' Nc6 f3 e5', title='The Classical', sub='Both knights out: the same setup', pri='common',
       why='Black develops the natural way. Bishop, f-pawn, queen, castle long.', outcome='More space and the safer king'),
  dict(id='so-schev', part='so-d6', root=D + ' e6', main=D + ' e6 f3 Be7', title='The Scheveningen', sub='Two small center pawns: the setup, then the g-pawn', pri='common',
       why='Black keeps two pawns side by side in the middle. Your pieces come out behind the f-pawn and the g-pawn goes at the knight.', outcome='An attack on the kingside'),
  dict(id='so-d6x', part='so-d6', root=S + ' d6', title='The d-pawn first: early tries', sub='When Black leaves the usual path', pri='common',
       why='Before the main lines there are a few side roads: the e-pawn pushed at your knight, the knight left at home. The setup still comes out.', outcome='Better for you'),
  dict(id='so-accel', part='so-nc6', root=N + ' g6', title='The Accelerated Dragon', sub='The bishop comes to the long diagonal a move early', pri='common',
       why='Black skips the d-pawn move to get the bishop out fast. Your bishop takes its best square before the f-pawn moves.', outcome='A small, steady edge'),
  dict(id='so-four', part='so-nc6', root=N + ' Nf6', main=N + ' Nf6 Nc3 e5', title='Both knights, then the e-pawn', sub='The Sveshnikov and its cousins: the knight jumps forward', pri='common',
       why='Black hits your knight with the e-pawn. The square in front is free, so the knight jumps in, at the hole the pawn left behind it.', outcome='A hole in Black\'s camp to use'),
  dict(id='so-e5', part='so-nc6', root=N + ' e5', title='The e-pawn hits your knight at once', sub='The Löwenthal and the Kalashnikov: the knight jumps forward', pri='rare',
       why='The same idea a move earlier. The knight jumps forward, at the hole in front of Black\'s d-pawn.', outcome='Better for you'),
  dict(id='so-nc6x', part='so-nc6', root=S + ' Nc6', title='The knight first: other tries', sub='The Taimanov setup, an early queen, the trade in the middle', pri='common',
       why='Black has a few more ways to play after the knight comes out. Knight out, bishop, and the setup again.', outcome='Better for you'),
  dict(id='so-kan', part='so-e6', root=E + ' a6', title='The Kan', sub='Two small pawn moves; your pieces come out freely', pri='common',
       why='Black plays the e-pawn and the a-pawn one square and waits. Nothing stops your setup.', outcome='More space'),
  dict(id='so-taim', part='so-e6', root=E + ' Nc6', title='The Taimanov', sub='The knight comes out behind the e-pawn', pri='common',
       why='A flexible setup for Black. Yours is the same as ever.', outcome='More space'),
  dict(id='so-e6x', part='so-e6', root=S + ' e6', title='The e-pawn first: other tries', sub='The knight at once, the bishop out, the French-style d-pawn', pri='common',
       why='After the e-pawn move Black can still go several ways. The knight and the d-pawn come first, whatever follows.', outcome='Better for you'),
  dict(id='so-g6', part='so-rare', root=S + ' g6', title='The fianchetto on move two', sub='The Hyperaccelerated Dragon: take the middle', pri='rare',
       why='Black starts with the g-pawn. The d-pawn goes two squares all the same.', outcome='A big center'),
  dict(id='so-rare', part='so-rare', root=S, title='Other second moves', sub='The a-pawn, the knight at your e-pawn, the queen out', pri='rare',
       why='The O\'Kelly, the Nimzowitsch and the rest. Each has one move to know.', outcome='Better for you'),
]
text, table = draft.emit(leaves, LESSONS, 'w')
PARTS = [
  dict(id='so-d6', ch='sico', title='Black\'s d-pawn first', kicker='Najdorf, Dragon, Classical, Scheveningen', blurb='The most common way to play the Sicilian. You open the middle, take back with the knight and bring out the same pieces in the same order: bishop, f-pawn, queen, castle long.'),
  dict(id='so-nc6', ch='sico', title='Black\'s knight first', kicker='Accelerated Dragon, Sveshnikov, Kalashnikov', blurb='With the knight out early Black can hit your knight with the e-pawn. Here the square in front is free, so the knight jumps forward. Otherwise the setup is the same.'),
  dict(id='so-e6', ch='sico', title='Black\'s e-pawn first', kicker='Kan, Taimanov', blurb='Small pawn moves and a flexible setup for Black. Yours comes out untouched.'),
  dict(id='so-rare', ch='sico', title='Other second moves', kicker='Hyperaccelerated Dragon, O\'Kelly, Nimzowitsch', blurb='The rare tries on move two, each with the one move worth knowing.'),
]
NOTES = {
  S: ('Knight out', 'The d-pawn goes two squares next, and this knight takes back when Black trades it.', ['key']),
  S + ' d6 d4': ('D-pawn two squares', 'Open the middle. Black nearly always takes.', ['key']),
  S + ' d6 d4 cxd4 Nxd4': ('Knight takes back', 'It stands in the middle of the board, and nothing can chase it yet.', ['key']),
  D: ('Queen\'s knight guards the e-pawn', 'The setup starts here: f-pawn, bishop, queen, castle long.', ['key']),
  D + ' a6 f3': ('F-pawn one square', 'It guards the e-pawn a second time and keeps Black\'s knight from jumping at the bishop that comes next.', ['key'], dict(arrows=['c1e3g'])),
  D + ' a6 f3 e5 Nb3': ('Knight steps back', 'The a-pawn guards the square in front, so the knight goes back toward the queenside. Black has left a hole in front of the d-pawn.', ['key']),
  D + ' a6 f3 e6 Be3': ('Bishop beside the queen', 'Behind the f-pawn nothing can chase it. The queen comes next, then the king castles long.', ['key']),
  D + ' a6 f3 e6 Be3 Be7 Qd2 O-O O-O-O': ('Castle long', 'The kings are on opposite wings, so your kingside pawns are free to run.', ['key']),
  D + ' a6 f3 e6 Be3 b5 Qd2 Bb7 O-O-O Nbd7 g4': ('G-pawn two squares', 'It is going on to hit the knight in front of Black\'s king. The edge pawn follows.', ['key'], dict(arrows=['g4g5g'])),
  D + ' g6 f3': ('F-pawn one square', 'The same move against the Dragon. Bishop and queen line up next, to trade off the bishop Black is about to put on the long diagonal.', ['key']),
  D + ' g6 f3 Bg7 Be3 O-O Qd2 Nc6 O-O-O': ('Castle long', 'The setup is done. The edge pawn is next, to open the file in front of Black\'s king.', ['key']),
  D + ' g6 f3 Bg7 Be3 O-O Qd2 Nc6 O-O-O d5 exd5': ('Take it', 'Black strikes in the middle before your pawns get going. Take, and the trades that follow leave you the safer king.', ['key']),
  N + ' Nf6 Nc3 e5 Ndb5': ('Knight jumps forward', 'The square in front is free, and Black\'s e-pawn has left a hole behind it. The knight is headed there.', ['key'], dict(arrows=['b5d6g'])),
  N + ' e5 Nb5': ('Knight jumps forward', 'The same jump a move earlier. The hole in front of Black\'s d-pawn is the target.', ['key'], dict(arrows=['b5d6g'])),
  N + ' g6 Nc3 Bg7 Be3': ('Bishop first', 'Black\'s bishop is aimed at your knight in the middle, so the bishop guards it before the f-pawn moves.', ['key']),
  N + ' g6 Nc3 Bg7 Be3 Nf6 Bc4': ('Bishop out before the f-pawn', 'Black saved a move with the d-pawn to push it two squares in one go. Your bishop stops that first.', ['key']),
  N + ' g6 Nc3 Bg7 Be3 Nf6 Bc4 O-O Bb3': ('Bishop steps back', 'Out of reach of the tricks against the knight in the middle. Then the f-pawn, the queen, and castle long as usual.', ['key']),
  N + ' Nxd4 Qxd4': ('Queen takes back', 'No knight is left to chase her, so she stands well in the middle.', ['key']),
  E + ' Nc6 Nc3': ('Queen\'s knight out', 'The setup starts the same way against the small pawn moves.'),
  S + ' g6 d4': ('D-pawn two squares', 'The same move against the early fianchetto.'),
}
allp = set()
for _, _, path, _ in table:
    t = path.split()
    for k in range(1, len(t) + 1): allp.add(' '.join(t[:k]))
drop = [k for k in NOTES if ' '.join(k.split()) not in allp]
print('notes without a node (dropped):', drop)
# a position the rest of the book already has a note for keeps that note (the first moves are shared with the Alapin)
import types
for m in ('sicopen', 'wfill'): sys.modules[m] = types.ModuleType(m)
sys.path.insert(0, str(paths.ROOT / 'content/white')); import content, content2  # noqa: F401  (content2 registers the later chapters' notes)
have = set(content.NOTES); shared = [k for k in NOTES if ' '.join(k.split()) in have]
print('notes the book already has (kept as they are):', shared)
NOTES = {k: v for k, v in NOTES.items() if k not in drop and k not in shared}
auto = draft.named_moves([t[2] for t in table], 'w', skip=have)
mod = draft.module_text("""White against the Sicilian, a second variation: the Open Sicilian, a pack for the slot 'whiteSic' beside the Alapin
(see PACKS in content2_meta.py).

One setup, one order: knight, d-pawn two squares, take back with the knight, queen's knight, bishop beside the queen,
f-pawn one square, queen, castle long, then the g-pawn. When Black's e-pawn hits the knight in the middle it steps
back, or jumps forward when the square in front is free. The lines were drafted with pipeline/draft.py: Black's moves by the Maia 1300/1500 odds, yours from the
setup's order wherever Stockfish 17.1 accepts it and the engine's move elsewhere. SAN is internal; notes are plain
English.""",
  'from content import n, J, L, PARTS', [PARTS], text, NOTES, auto, lambda ps: 'PARTS.extend([\n' + ''.join(f"  dict(id={p['id']!r}, ch={p['ch']!r}, title={p['title']!r}, kicker={p['kicker']!r},\n       blurb={p['blurb']!r}),\n" for p in ps) + '])')
open(paths.ROOT / 'content/white/sicopen.py', 'w').write(mod)
for lid, title, path, reach in table: print(f"{reach*100:5.2f} {lid:24s} {title:58s} {path[6:]}")
print(len(leaves), 'leaves')
print('FLAGS'); [print('  ', f) for f in W.flags]
draft.done()
