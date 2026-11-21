"""The Queen's Gambit Declined for Black (content/black/bqgd.py): the setup's order, the moves fixed by hand, the lessons
and the notes. Run it to redraft the pack (python3 pipeline/drafts/qgd.py); it overwrites the module, so notes are edited here."""
import sys, re, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import paths, chess, draft
def system(b, path):
    # d-pawn, e-pawn beside it, knight, bishop one square, castle. Against the c-pawn: the h-pawn asks the pinning bishop,
    # and the knight jumps into the middle to trade pieces; after a trade of pawns the c-pawn backs the d-pawn and the
    # knights come behind it. Against a system without the c-pawn, yours goes two squares and the bishops are traded.
    W, B, P, N, Bi = chess.WHITE, chess.BLACK, chess.PAWN, chess.KNIGHT, chess.BISHOP
    def on(sq, pt, col=B):
        x = b.piece_at(sq)
        return x is not None and x.piece_type == pt and x.color == col
    order = ['d5'] if on(chess.D7, P) else []
    gambit = on(chess.C4, P, W) or not (on(chess.C2, P, W) or on(chess.C3, P, W))     # White's c-pawn is at your d-pawn (or has been traded)
    if gambit:
        order += ['e6', 'exd5', 'Nf6', 'Be7', 'O-O']
        if on(chess.G5, Bi, W): order.append('h6')
        if on(chess.H4, Bi, W) and on(chess.H6, P): order.append('Ne4')
        order += ['c6', 'Nbd7', 'Re8', 'Nf8', 'b6', 'Bb7', 'c5', 'dxc4']
    else:
        order += ['Nf6', 'e6', 'c5', 'Nc6', 'Bd6', 'Be7', 'O-O', 'b6', 'Bb7', 'Nbd7']
    # a knight or a bishop is only brought out from home by the setup: a second move with it is the engine's call
    def dev(san):
        if san in ('Ne4', 'Nf8'): return True
        try: mv = b.parse_san(san)
        except ValueError: return True
        x = b.piece_at(mv.from_square)
        return x.piece_type not in (N, Bi) or chess.square_rank(mv.from_square) == 7
    return [s_ for s_ in order if dev(s_)]
Q = 'd4 d5 c4 e6'
M = Q + ' Nc3 Nf6 Bg5 Be7 e3 O-O Nf3 h6 Bh4 Ne4'
X = Q + ' Nc3 Nf6 cxd5 exd5 Bg5'
fixed = {'d4': 'd5', 'd4 d5 c4': 'e6', Q + ' Nc3': 'Nf6', Q + ' Nf3': 'Nf6', Q + ' Nc3 Nf6 Bg5': 'Be7', Q + ' Nc3 Nf6 Nf3': 'Be7', Q + ' Nf3 Nf6 Nc3': 'Be7',
         Q + ' Nc3 Nf6 cxd5': 'exd5', Q + ' cxd5': 'exd5', X: 'c6', M + ' Bxe7': 'Qxe7'}
SKIP = ('qgd', 'qgdx', 'slav', 'london', 'd4x', 'kid', 'kidx')
W = draft.Walk('b', system, fixed, known=draft.known_from('black', skip_chapters=SKIP), tol=35, thr=lambda n, r: 0.012 if n <= 3 else 0.03 if n <= 5 else 0.06 if n <= 9 else 0.10, min_reach=0.0015,
               depth=lambda r: 18 if r >= 0.02 else 16 if r >= 0.005 else 14 if r >= 0.002 else 12)
# the main lines as they are played when White knows them (given by hand), then the tree by the odds
leaves = W.run([(M + ' Bxe7 Qxe7', None), (X + ' c6 e3 Be7 Bd3 O-O Qc2', None), (Q + ' Nc3 Nf6 Bg5', None), (Q + ' Nc3 Nf6 Nf3 Be7 Bf4', None), (Q + ' Nf3 Nf6 g3', None), ('d4', 1.0)])
LESSONS = [
  dict(id='bqg-main', part='bqg-pin', root=Q + ' Nc3 Nf6 Bg5', main=M + ' Bxe7 Qxe7', title='The bishop pins your knight', sub='Bishop, castle, the h-pawn, then the knight jumps in', pri='core',
       why='The oldest line of the Queen\'s Gambit. Your bishop breaks the pin, you castle, and the knight jump trades two pairs of pieces: a cramped position needs fewer pieces.', outcome='Equal, with an easy game'),
  dict(id='bqg-exch', part='bqg-exch', root=Q + ' Nc3 Nf6 cxd5', main=X + ' c6 e3 Be7 Bd3 O-O Qc2', title='The Exchange: pawns come off', sub='E-pawn takes back; the c-pawn backs the d-pawn', pri='core',
       why='White trades in the middle. Your light bishop has an open line, and the c-pawn makes the d-pawn safe for good.', outcome='Solid and equal'),
  dict(id='bqg-exch3', part='bqg-exch', root=Q + ' cxd5', title='The Exchange on move three', sub='The same pawns; knight, bishop, castle', pri='common',
       why='The trade comes a move earlier. Nothing changes in your setup.', outcome='Equal'),
  dict(id='bqg-nf3', part='bqg-quiet', root=Q + ' Nc3 Nf6 Nf3', main=Q + ' Nc3 Nf6 Nf3 Be7 Bf4 O-O e3 c6 Bd3 Nbd7', title='Both knights out', sub='Bishop one square, castle; the London bishop or the pin', pri='core',
       why='White brings the second knight before the bishop. Bishop one square and castle, and you are ready for whichever bishop move comes.', outcome='Equal'),
  dict(id='bqg-4th', part='bqg-quiet', root=Q + ' Nc3 Nf6', main=Q + ' Nc3 Nf6 e3 Be7 Nf3 O-O', title='Other fourth moves', sub='The quiet e-pawn, the bishop to the other diagonal', pri='common',
       why='White develops without the pin. Your setup is the same five moves.', outcome='Equal'),
  dict(id='bqg-knight', part='bqg-quiet', root=Q + ' Nf3', title='The king\'s knight first', sub='The same setup; the fianchetto, the quiet e-pawn', pri='core',
       why='Half of club players bring this knight first. The setup comes out the same way, and the bishop on the long diagonal is met by taking the c-pawn.', outcome='Equal'),
  dict(id='bqg-third', part='bqg-quiet', root=Q, main=Q + ' e3 Nf6 Nf3 Be7', title='Other third moves', sub='The quiet e-pawn, the fianchetto, a bishop out early', pri='common',
       why='White holds the knights back. Knight, bishop, castle.', outcome='Equal'),
  dict(id='bqx-london', part='bqx-bishop', root='d4 d5 Bf4', main='d4 d5 Bf4 Nf6 e3 e6 Nf3 c5 c3 Nc6 Nbd2 Bd6 Bg3 O-O', title='The London', sub='E-pawn, c-pawn two squares, knight, and the bishop offers a trade', pri='core',
       why='One in five club players set up the London. Without a c-pawn hitting your center you have a free hand: the c-pawn goes two squares, and your bishop offers a trade to White\'s best piece.', outcome='Equal and easy'),
  dict(id='bqx-nf3', part='bqx-bishop', root='d4 d5 Nf3', main='d4 d5 Nf3 Nf6 e3 Bf5 Bd3 Bxd3 Qxd3 c6 O-O e6', title='The knight first', sub='Your bishop comes out before the e-pawn shuts it in', pri='core',
       why='White waits with the c-pawn. With no pawn hitting your center the light bishop has time to come out first, and the e-pawn closes the door behind it.', outcome='Equal'),
  dict(id='bqx-colle', part='bqx-other', root='d4 d5 e3', main='d4 d5 e3 Nf6 Bd3 e6 Nf3 c5 c3 Nc6', title='The quiet e-pawn', sub='The Colle and the Stonewall: c-pawn two squares', pri='common',
       why='White shuts the bishop in and builds slowly. You take the room on the queen\'s side.', outcome='Comfortable'),
  dict(id='bqx-nc3', part='bqx-other', root='d4 d5 Nc3', main='d4 d5 Nc3 Nf6 Bf4 e6', title='The queen\'s knight on move two', sub='The Jobava and the Veresov: knight out, then the e-pawn', pri='common',
       why='The knight blocks White\'s own c-pawn and aims at a quick e-pawn push. Your knight stops it.', outcome='Equal'),
  dict(id='bqx-bg5', part='bqx-other', root='d4 d5 Bg5', title='The bishop out to the edge', sub='Nothing to pin yet: develop around it', pri='rare',
       why='The bishop comes out before there is a knight to pin.', outcome='Equal'),
  dict(id='bqx-second', part='bqx-other', root='d4 d5', main='d4 d5 g3 Nf6 Bg2 e6 Nf3 c5', title='Other second moves', sub='A pawn offered, the fianchetto', pri='common',
       why='The gambits and the slow second moves. Take what is safe to take, and develop.', outcome='Equal or better'),
]
text, table = draft.emit(leaves, LESSONS, 'b')
PARTS = [
  ('bqg-pin', 'qgd', 'The bishop pins your knight', 'Lasker Defense', 'White\'s bishop comes out to pin your knight. Bishop one square, castle, ask the bishop with the h-pawn, and then the knight jumps into the middle: two pairs of pieces come off and your position has room to breathe.'),
  ('bqg-exch', 'qgd', 'The pawns are traded', 'Exchange Variation', 'White takes in the middle and you take back with the e-pawn. Your light bishop is free, the c-pawn backs up the d-pawn, and the knights come behind it.'),
  ('bqg-quiet', 'qgd', 'No pin', 'Knights first, the Catalan, quiet lines', 'White develops without pinning the knight, or brings the knights out first. The same five moves, and then the c-pawn frees your game.'),
  ('bqx-bishop', 'qgdx', 'The London and the knight first', 'White plays without the c-pawn', 'No c-pawn hits your center, so yours goes two squares. Knight, e-pawn, c-pawn, knight, and the bishop offers a trade to the London bishop.'),
  ('bqx-other', 'qgdx', 'The Colle, the Jobava and the rest', 'Second-move sidelines', 'The slow systems and the gambits. Your first moves don\'t change.'),
]
NOTES = {
  'd4 d5 c4 e6': ('E-pawn one square', 'You keep the pawn in the middle and say no to the gambit. The d-pawn is as safe as it gets.', ['key']),
  Q + ' Nc3 Nf6': ('Knight out', 'A second guard for the d-pawn.', ['key']),
  Q + ' Nc3 Nf6 Bg5 Be7': ('Bishop one square', 'The pin is broken before it can hurt. You castle next.', ['key']),
  Q + ' Nc3 Nf6 Bg5 Be7 e3 O-O': ('Castle', 'King safe. Now ask the bishop what it wants.', ['key']),
  Q + ' Nc3 Nf6 Bg5 Be7 e3 O-O Nf3 h6': ('H-pawn asks the bishop', 'It has to take or step back, and your king gets a square for later.', ['key'], dict(arrows=['h6g5r'])),
  M: ('Knight jumps in', 'It offers two trades at once: the bishops, and the knights. With fewer pieces your position has room.', ['key'], dict(arrows=['e7h4g', 'e4c3g'])),
  M + ' Bxe7 Qxe7': ('Queen takes back', 'She comes out with a move gained, and the knight still stands in the middle.', ['key']),
  Q + ' Nc3 Nf6 cxd5 exd5': ('E-pawn takes back', 'The line of your light bishop opens, and you keep a pawn in the middle.', ['key']),
  X + ' c6': ('C-pawn backs the d-pawn', 'The d-pawn can\'t be won now, and your queen has a diagonal.', ['key']),
  Q + ' Nf3 Nf6': ('Knight out', 'The same move whichever knight White brought first.', ['key']),
  'd4 d5 Bf4 Nf6': ('Knight out', 'White plays without the c-pawn. So yours will go two squares.', ['key']),
  'd4 d5 Bf4 Nf6 e3 e6': ('E-pawn one square', 'The same pawns as against the gambit. With no c-pawn hitting your center, yours goes two squares next.', ['key']),
  'd4 d5 Bf4 Nf6 e3 e6 Nf3 c5': ('C-pawn two squares', 'It hits the d-pawn, and the knight comes out behind it.', ['key'], dict(arrows=['c5d4r'])),
  'd4 d5 Bf4 Nf6 e3 e6 Nf3 c5 c3 Nc6 Nbd2 Bd6': ('Bishop offers a trade', 'The London bishop is White\'s best piece. If it takes, your queen takes back and stands well; if it steps back, you castle.', ['key'], dict(arrows=['d6f4g'])),
  'd4 d5 Nf3 Nf6': ('Knight out', 'The same first moves. If the c-pawn comes, the e-pawn backs yours up.', ['key']),
}
allp = set()
for _, _, path, _ in table:
    t = path.split()
    for k in range(1, len(t) + 1): allp.add(' '.join(t[:k]))
drop = [k for k in NOTES if ' '.join(k.split()) not in allp]
print('notes without a node (dropped):', drop)
# a position the rest of the book already has a note for keeps that note (the first moves are shared with the Slav)
import types
for m in ('bqgd', 'bfill'): sys.modules[m] = types.ModuleType(m)
sys.path.insert(0, str(paths.ROOT / 'content/black')); import bcontent, bnotes  # noqa: F401  (bnotes registers the house notes)
have = set(bcontent.NOTES); shared = [k for k in NOTES if ' '.join(k.split()) in have]
print('notes the book already has (kept as they are):', shared)
NOTES = {k: v for k, v in NOTES.items() if k not in drop and k not in shared}
auto = draft.named_moves([t[2] for t in table], 'b', skip=have)
mod = draft.module_text("""Black against the d-pawn: the Queen's Gambit Declined. D-pawn two squares, the e-pawn beside it, knight, bishop one
square, castle. Against the pin: the h-pawn asks the bishop and the knight jumps into the middle (the Lasker Defense).
After a trade of pawns: the c-pawn backs the d-pawn. Against a system without the c-pawn, yours goes two squares. A
separate pack with two chapters (see PACKS in bmeta.py). The lines were drafted with pipeline/draft.py: White's moves by
the Maia 1300/1500 odds, yours from the setup's order wherever Stockfish 17.1 accepts it and the engine's move
elsewhere. SAN is internal only; notes are plain English.""",
  'from bcontent import L, P, J, n', PARTS, text, NOTES, auto, lambda p: f"P({', '.join(repr(x) for x in p)})")
open(paths.ROOT / 'content/black/bqgd.py', 'w').write(mod)
for lid, title, path, reach in table: print(f"{reach*100:5.2f} {lid:28s} {title:44s} {path[6:]}")
print(len(leaves), 'leaves'); print('flags:'); [print(' ', f) for f in W.flags]
draft.done()
