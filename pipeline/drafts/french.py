"""The French for Black (content/black/bfrench.py): the setup's order, the moves fixed by hand, the lessons and the notes.
Run it to redraft the pack (python3 pipeline/drafts/french.py); it overwrites the module, so notes are edited here."""
import sys, re, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import paths, chess, draft
def system(b, path):
    # e-pawn one square, d-pawn two. When White's pawn pushes past, the knight it hits steps back and the c-pawn hits the
    # chain, with the knight and the queen behind it; when the pawns are traded or held, knight, bishop, castle.
    W, B, P, N, Bi = chess.WHITE, chess.BLACK, chess.PAWN, chess.KNIGHT, chess.BISHOP
    def on(sq, pt, col=B):
        x = b.piece_at(sq)
        return x is not None and x.piece_type == pt and x.color == col
    order = (['e6'] if on(chess.E7, P) else []) + (['d5'] if on(chess.D7, P) else [])
    if on(chess.E5, P, W) and on(chess.D5, P):                           # the chain is on the board
        order += (['Nfd7', 'Nd7'] if on(chess.F6, N) else []) + ['c5', 'Nc6', 'Qb6', 'cxd4', 'Bd7', 'Nh6', 'Nge7', 'Nf5', 'Be7', 'O-O', 'f6']
    else:
        order += ['exd5', 'Nf6', 'Bd6', 'c5', 'Be7', 'O-O', 'Nc6', 'Nbd7']
    # a knight or a bishop is only brought out from home by the setup: a second move with it is the engine's call
    def dev(san):
        if san in ('Nfd7', 'Nd7', 'Nf5'): return True
        try: mv = b.parse_san(san)
        except ValueError: return True
        x = b.piece_at(mv.from_square)
        return x.piece_type not in (N, Bi) or chess.square_rank(mv.from_square) == 7
    return [s_ for s_ in order if dev(s_)]
F = 'e4 e6 d4 d5'
A = F + ' e5'
N3 = F + ' Nc3'
fixed = {'e4': 'e6', 'e4 e6 d4': 'd5', A: 'c5', A + ' c5 c3': 'Nc6', A + ' c5 c3 Nc6 Nf3': 'Qb6', A + ' c5 c3 Nc6 Nf3 Qb6 a3': 'c4', F + ' exd5': 'exd5',
         N3: 'Nf6', N3 + ' Nf6 e5': 'Nfd7', N3 + ' Nf6 Bg5': 'dxe4', N3 + ' Nf6 Bg5 dxe4 Nxe4': 'Be7', F + ' Nd2': 'Nf6', F + ' Nd2 Nf6 e5': 'Nfd7', 'e4 e6 e5': 'd5', 'e4 e6 e5 d5 exd6': 'Bxd6'}
SKIP = ('french', 'caro', 'sicilian', 'dragon', 'scandi', 'italian', 'ruy', 'scotch', 'vienna', 'attacks')
W = draft.Walk('b', system, fixed, known=draft.known_from('black', skip_chapters=SKIP), tol=35, thr=lambda n, r: 0.012 if n <= 3 else 0.03 if n <= 5 else 0.06 if n <= 9 else 0.10, min_reach=0.0015,
               depth=lambda r: 18 if r >= 0.02 else 16 if r >= 0.005 else 14 if r >= 0.002 else 12)
# the lines that are rare at club level but everyone asks about are given by hand, then the tree by the odds
ST = N3 + ' Nf6 e5 Nfd7 f4 c5 Nf3 Nc6 Be3'
TA = F + ' Nd2 Nf6 e5 Nfd7 Bd3 c5 c3 Nc6 Ne2'
KI = 'e4 e6 d3 d5 Nd2 Nf6 Ngf3 c5 g3 Nc6 Bg2 Be7 O-O'
EX = F + ' exd5 exd5 Nf3 Nf6 Bd3 Bd6 O-O O-O'
leaves = W.run([(ST, None), (N3 + ' Nf6 Bg5', None), (TA, None), (A + ' c5 c3 Nc6 Nf3 Qb6 a3', None), (A + ' c5 c3 Nc6 Nf3 Qb6 Be2', None), (A + ' c5 c3 Nc6 Nf3 Qb6 Bd3', None), (KI, None), ('e4', 1.0)])
LESSONS = [
  dict(id='bfr-adv', part='bfr-adv', root=A + ' c5 c3', main=A + ' c5 c3 Nc6 Nf3 Qb6 Be2', title='The Advance: hit the chain', sub='C-pawn, knight, queen: three pieces on one pawn', pri='core',
       why='The most common French at club level. White\'s pawns point at your king\'s side, and the pawn that holds them up is your target.', outcome='Pressure on the d-pawn'),
  dict(id='bfr-adv4', part='bfr-adv', root=A + ' c5', title='The Advance: no c-pawn behind it', sub='The knight first, a pawn taken, the queen out', pri='common',
       why='White doesn\'t back the chain up with the c-pawn. Its base is weaker still, and the same three pieces go at it.', outcome='Equal or better'),
  dict(id='bfr-exch', part='bfr-exch', root=F + ' exd5', main=EX, title='The Exchange', sub='Take back with the e-pawn; knight, bishop, castle', pri='core',
       why='One in four trades the pawns. Your light bishop is free at last, and the position is level and easy to play.', outcome='Equal'),
  dict(id='bfr-steinitz', part='bfr-knight', root=N3, main=ST, title='The Steinitz: knight out, then the push', sub='The knight steps back; the c-pawn hits the chain', pri='core',
       why='White guards the e-pawn with a knight, and pushes when yours hits it. The knight steps back and the plan is the one you know: c-pawn, knight, queen at the base of the chain.', outcome='A fight on your terms'),
  dict(id='bfr-burn', part='bfr-knight', root=N3 + ' Nf6 Bg5', title='The Burn: the bishop pins your knight', sub='Take the e-pawn, then break the pin', pri='common',
       why='The bishop pins your knight to the queen. Taking the e-pawn clears the middle, and the bishop one square breaks the pin.', outcome='Solid and equal'),
  dict(id='bfr-tarrasch', part='bfr-knight', root=F + ' Nd2', main=TA, title='The Tarrasch: the knight goes the other way', sub='The same answer: knight out, then back, then the c-pawn', pri='common',
       why='The knight guards the pawn from a square where it can\'t be pinned. Your answer doesn\'t change.', outcome='Equal'),
  dict(id='bfr-nf3', part='bfr-second', root='e4 e6 Nf3', main='e4 e6 Nf3 d5 exd5 exd5 d4 Nf6', title='The knight before the d-pawn', sub='D-pawn two squares all the same', pri='core',
       why='One in four develops first. Your d-pawn goes two squares anyway, and the game is an Advance or an Exchange a move later.', outcome='Equal'),
  dict(id='bfr-qn', part='bfr-second', root='e4 e6 Nc3', main='e4 e6 Nc3 d5 exd5 exd5 d4 Nf6', title='The queen\'s knight on move two', sub='D-pawn two squares; knight out when the pawn is guarded', pri='common',
       why='The knight comes before the d-pawn. Nothing changes: your d-pawn hits the e-pawn, and your knight follows.', outcome='Equal'),
  dict(id='bfr-f4', part='bfr-second', root='e4 e6 f4', title='The f-pawn on move two', sub='The La Bourdonnais: the chain without a d-pawn', pri='common',
       why='White wants a chain with the f-pawn behind it. The c-pawn and the knight go at it the usual way.', outcome='Comfortable'),
  dict(id='bfr-bc4', part='bfr-second', root='e4 e6 Bc4', title='The Italian bishop', sub='Your d-pawn hits it with a move gained', pri='common',
       why='Club players love this bishop. Against the French it runs into a pawn at once.', outcome='A move ahead'),
  dict(id='bfr-e5', part='bfr-second', root='e4 e6 e5', title='The e-pawn pushes at once', sub='D-pawn two squares: the Advance a move early', pri='common',
       why='The pawn pushes before yours is there to push past. Play the d-pawn all the same and it is the chain you know.', outcome='Equal'),
  dict(id='bfr-kia', part='bfr-second', root='e4 e6 d3', main=KI, title='The small d-pawn', sub='The King\'s Indian Attack: take the middle', pri='common',
       why='White keeps the middle shut and builds behind it. You take the room that is on offer.', outcome='Comfortable'),
  dict(id='bfr-second', part='bfr-second', root='e4 e6', title='Other second moves', sub='The queen out early, the c-pawn', pri='rare',
       why='Without the d-pawn beside the e-pawn there is nothing to lock. D-pawn two squares, and develop.', outcome='Equal or better'),
]
text, table = draft.emit(leaves, LESSONS, 'b')
PARTS = [
  ('bfr-adv', 'french', 'The pawn pushes past', 'Advance Variation', 'White\'s e-pawn steps past yours and the middle is locked. The chain points at your king\'s side, so you play on the other: the c-pawn hits the pawn that holds the chain up, and the knight and the queen join in.'),
  ('bfr-exch', 'french', 'The pawns are traded', 'Exchange Variation', 'White takes and you take back with the e-pawn. Both bishops are free and the position is the same for both sides: knight, bishop, castle.'),
  ('bfr-knight', 'french', 'White holds the pawn', 'Classical, Burn and Tarrasch', 'A knight guards the e-pawn. Yours comes out and hits it: if the pawn pushes past, the knight steps back and the c-pawn goes at the chain; if the bishop pins the knight, you take the e-pawn and break the pin.'),
  ('bfr-second', 'french', 'No two pawns in the middle', 'Second-move sidelines', 'White holds the d-pawn back. Yours goes two squares all the same, and the pieces come out the usual way.'),
]
NOTES = {
  'e4 e6': ('E-pawn one square', 'It backs the d-pawn up. On the next move that pawn goes two squares and hits White\'s e-pawn.', ['key']),
  F: ('D-pawn two squares', 'It hits the e-pawn. White has to push past, trade or guard it.', ['key'], dict(arrows=['d5e4r'])),
  A + ' c5': ('C-pawn hits the chain', 'White\'s d-pawn holds the pushed pawn up. Hit the chain at its base.', ['key'], dict(arrows=['c5d4r'])),
  A + ' c5 c3 Nc6': ('Knight out', 'A second piece on the d-pawn.', ['key'], dict(arrows=['c6d4r', 'c5d4r'])),
  A + ' c5 c3 Nc6 Nf3 Qb6': ('Queen behind the c-pawn', 'A third piece on the d-pawn, and she looks at the b-pawn too: White\'s dark bishop can\'t leave home without losing it.', ['key'], dict(arrows=['b6d4r', 'b6b2r'])),
  A + ' c5 c3 Nc6 Nf3 Qb6 a3 c4': ('C-pawn steps past', 'The a-pawn was getting ready to push the b-pawn at your c-pawn. Step past first: that side is shut, and your knight has a square behind White\'s pawns to aim for.', ['key'], dict(arrows=['c6a5g', 'a5b3g'])),
  F + ' exd5 exd5': ('E-pawn takes back', 'The light bishop has an open line now. Knight, bishop, castle.', ['key']),
  N3 + ' Nf6': ('Knight hits the e-pawn', 'A second piece on it. White has to push the pawn past, trade it, or bring the bishop out at your knight.', ['key'], dict(arrows=['f6e4r'])),
  N3 + ' Nf6 e5 Nfd7': ('Knight steps back', 'It makes room for the f-pawn and backs up the c-pawn\'s push. The chain is on the board, and you know what to do with it.', ['key']),
  N3 + ' Nf6 e5 Nfd7 f4 c5': ('C-pawn hits the chain', 'The same move as in the Advance. Knight and queen come behind it.', ['key'], dict(arrows=['c5d4r'])),
  'e4 e6 e5 d5': ('D-pawn two squares', 'The same second move. If White takes it in passing, your bishop takes back with a piece out; if not, it is the Advance.', ['key']),
  'e4 e6 e5 d5 exd6 Bxd6': ('Bishop takes back', 'A piece out with a move gained, and White has no pawn left in the middle.', ['key']),
  'e4 e6 Nc3 d5': ('D-pawn two squares', 'The same second move whatever White has played.', ['key']),
  'e4 e6 Bc4 d5': ('D-pawn hits the bishop', 'It has to move again, and you have the middle.', ['key'], dict(arrows=['d5c4r'])),
  N3 + ' Nf6 Bg5 dxe4': ('Take the e-pawn', 'The pinned knight couldn\'t hold the middle. With the pawn gone, the bishop one square breaks the pin.', ['key']),
  N3 + ' Nf6 Bg5 dxe4 Nxe4 Be7': ('Bishop breaks the pin', 'Now the knight is free, and a trade on that square leaves you with the two bishops.', ['key']),
  F + ' Nd2 Nf6': ('Knight hits the e-pawn', 'The same answer as against the other knight.', ['key'], dict(arrows=['f6e4r'])),
  F + ' Nd2 Nf6 e5 Nfd7': ('Knight steps back', 'The chain again: the c-pawn hits its base next.', ['key']),
  'e4 e6 Nf3 d5': ('D-pawn two squares', 'The same second move whatever White has played.', ['key']),
  'e4 e6 d3 d5': ('D-pawn two squares', 'White isn\'t fighting for the middle, so you take it.', ['key']),
}
allp = set()
for _, _, path, _ in table:
    t = path.split()
    for k in range(1, len(t) + 1): allp.add(' '.join(t[:k]))
drop = [k for k in NOTES if ' '.join(k.split()) not in allp]
print('notes without a node (dropped):', drop)
# a position the rest of the book already has a note for keeps that note
import types
for m in ('bfrench', 'bfill'): sys.modules[m] = types.ModuleType(m)
sys.path.insert(0, str(paths.ROOT / 'content/black')); import bcontent, bnotes  # noqa: F401  (bnotes registers the house notes)
have = set(bcontent.NOTES); shared = [k for k in NOTES if ' '.join(k.split()) in have]
print('notes the book already has (kept as they are):', shared)
NOTES = {k: v for k, v in NOTES.items() if k not in drop and k not in shared}
auto = draft.named_moves([t[2] for t in table], 'b', skip=have)
mod = draft.module_text("""Black against the e-pawn: the French. E-pawn one square, then the d-pawn two. When White's pawn pushes past, the
c-pawn hits the chain with the knight and the queen behind it; when a knight guards the pawn, yours hits it and steps
back if it is pushed; when the pawns are traded, knight, bishop, castle. A separate pack (see PACKS in bmeta.py). The
lines were drafted with pipeline/draft.py: White's moves by the Maia 1300/1500 odds, yours from the setup's order
wherever Stockfish 17.1 accepts it and the engine's move elsewhere. SAN is internal only; notes are plain English.""",
  'from bcontent import L, P, J, n', PARTS, text, NOTES, auto, lambda p: f"P({', '.join(repr(x) for x in p)})")
open(paths.ROOT / 'content/black/bfrench.py', 'w').write(mod)
for lid, title, path, reach in table: print(f"{reach*100:5.2f} {lid:28s} {title:44s} {path[6:]}")
print(len(leaves), 'leaves'); print('flags:'); [print(' ', f) for f in W.flags]
draft.done()
