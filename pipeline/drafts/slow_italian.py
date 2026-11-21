"""The slow Italian for White (content/white/italslow.py): the setup's order, the lessons and the notes.
Run it to redraft the pack (python3 pipeline/drafts/slow_italian.py); it overwrites the module, so notes are edited here."""
import sys, re, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import paths, chess, draft
def system(b, path):
    # one setup in one order: bishop, d-pawn one square, c-pawn one square, castle, rook beside the king, queen's knight
    # behind the d-pawn, the small h-pawn move, bishop back out of reach, then the knight round to the kingside
    W, P, N, Bi, R, K = chess.WHITE, chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.KING
    def on(sq, pt):
        x = b.piece_at(sq)
        return x is not None and x.piece_type == pt and x.color == W
    order = (['Bc4'] if on(chess.F1, Bi) else []) + (['d3'] if on(chess.D2, P) else []) + (['c3'] if on(chess.C2, P) else []) + ['O-O']
    if on(chess.G1, K) and on(chess.F1, R): order.append('Re1')
    if on(chess.B1, N): order.append('Nbd2')
    if on(chess.H2, P): order.append('h3')
    if on(chess.C4, Bi): order.append('Bb3')
    if on(chess.D2, N) and on(chess.E1, R): order.append('Nf1')
    if on(chess.F1, N): order.append('Ng3')
    return order
I = 'e4 e5 Nf3 Nc6 Bc4'
G = I + ' Bc5 d3 Nf6 c3'
# the knight that jumps into the middle is taken (never the e-pawn it offers)
fixed = {'e4 e5 Nf3 Nc6': 'Bc4', I + ' Nd4': 'Nxd4'}
W = draft.Walk('w', system, fixed, known=draft.known_from('white', skip_chapters=('italian', 'italians')), tol=45,
               thr=lambda n, r: 0.03 if n <= 6 else 0.05 if n <= 10 else 0.08 if n <= 14 else 0.10, min_reach=0.001,
               depth=lambda r: 20 if r >= 0.02 else 18 if r >= 0.005 else 16 if r >= 0.002 else 14)
# the named third moves that are rare by the odds are given by hand: the Hungarian, the Rousseau, the fianchetto
leaves = W.run([(G + ' d6 O-O O-O Re1 a6', None), (I + ' Bc5', None), (I + ' Nf6', None), (I + ' Be7', None), (I + ' f5', None), (I + ' g6', None), ('e4 e5 Nf3 Nc6', None)])
LESSONS = [
  dict(id='sl-main', part='sl-bishop', root=I + ' Bc5', main=G + ' d6 O-O O-O Re1', title='The slow Italian: one setup', sub='D-pawn, c-pawn, castle, rook, then the knight goes round', pri='core',
       why='Black mirrors your bishop. No early fight in the middle: both small pawn moves, castle, and every piece finds its square before anything is traded.', outcome='A full game with the easier plan'),
  dict(id='sl-2n', part='sl-knight', root=I + ' Nf6', title='Black\'s knight comes out: guard the e-pawn', sub='The small d-pawn move, then the same setup', pri='core',
       why='Three in ten bring the knight out at your e-pawn. The d-pawn guards it, and no knight jump is needed: the setup is the same.', outcome='A quiet edge'),
  dict(id='sl-h6', part='sl-odd', root=I + ' h6', title='The Anti-Fried Liver Defense', sub='A move spent on the edge: the same setup, a move ahead', pri='common',
       why='One in five club players stops a knight jump you never meant to make. Carry on with the setup.', outcome='A move ahead'),
  dict(id='sl-d6', part='sl-odd', root=I + ' d6', title='The Paris Defense', sub='The d-pawn first: the same setup', pri='rare',
       why='Black guards the e-pawn before anything else. Nothing changes for you.', outcome='More room'),
  dict(id='sl-nd4', part='sl-odd', root=I + ' Nd4', title='The Blackburne-Kostić Gambit', sub='Take the knight; never the e-pawn', pri='rare',
       why='Black offers the e-pawn as bait. Taking it loses to the queen. Take the knight instead and you are simply better.', outcome='Better for you'),
  dict(id='sl-be7', part='sl-odd', root=I + ' Be7', title='The Hungarian Defense', sub='The quiet bishop: the same setup', pri='rare',
       why='Black keeps the bishop at home. The setup comes out untouched.', outcome='More room'),
  dict(id='sl-odd', part='sl-odd', root='e4 e5 Nf3 Nc6', title='Odd third moves', sub='The f-pawn, the fianchetto, the queen out early', pri='rare',
       why='The Rousseau Gambit and the rest. The small d-pawn move is the answer to nearly all of them.', outcome='Better for you'),
]
text, table = draft.emit(leaves, LESSONS, 'w')
PARTS = [
  dict(id='sl-bishop', ch='italians', title='Black mirrors your bishop', kicker='Giuoco Pianissimo', blurb='Both bishops out, and no rush in the middle. Two small pawn moves, castle, the rook beside the king, and the queen\'s knight goes the long way round to the kingside.'),
  dict(id='sl-knight', ch='italians', title='Black\'s knight comes out', kicker='Two Knights, the quiet way', blurb='The knight hits your e-pawn and the d-pawn guards it. From there the setup is the same, and it usually runs into the lines of the first part.'),
  dict(id='sl-odd', ch='italians', title='Other third moves', kicker='Anti-Fried Liver, Paris, Hungarian, Blackburne-Kostić', blurb='What club players try on move three. The setup answers all but one: when the knight jumps into the middle, take it.'),
]
NOTES = {
  I + ' Bc5 d3': ('Small d-pawn move', 'One square, not two. It guards the e-pawn, and nothing gets traded early.', ['key']),
  G: ('Small c-pawn move', 'It keeps Black\'s knight out of the middle and gives your bishop a way back. The d-pawn can go forward later, when everything is ready.', ['key']),
  G + ' d6 O-O': ('Castle', 'King safe. The rook comes beside it next.', ['key']),
  G + ' d6 O-O O-O Re1': ('Rook beside the king', 'It stands behind the e-pawn, and leaves its square for the knight that is on its way round.', ['key']),
  G + ' d6 O-O O-O Re1 a6 Nbd2': ('Knight behind the d-pawn', 'The first step of its trip to the kingside: behind the rook next, then out in front of the king.', ['key'], dict(arrows=['d2f1g', 'f1g3g'])),
  G + ' Ng4 d4': ('D-pawn two squares', 'The knight left its post to go at f2. Now the middle is yours, with a hit on the bishop.', ['key']),
  G + ' d5 exd5': ('Take it', 'Black opens the middle before castling. After the trade your queen comes out with a hit on the knight in the middle.', ['key']),
  I + ' Nf6 d3': ('D-pawn guards the e-pawn', 'No knight jump is needed. The setup carries on, and it usually runs into the same positions as against the bishop.', ['key']),
  I + ' Nf6 d3 d6 Ng5': ('Now the knight jumps', 'Black spent a move on the d-pawn, so the pawn that would block your bishop gets there a move late. Bishop and knight both aim at f7.', ['key'], dict(arrows=['g5f7r', 'c4f7r'])),
  I + ' Nd4 Nxd4': ('Take the knight', 'Never the e-pawn: Black\'s queen would come out and win a piece. After the trade Black has a pawn stuck in the middle and nothing developed.', ['key']),
  I + ' h6 d3': ('Carry on', 'Black stopped a knight jump you never meant to make. You are a move ahead in the same setup.', ['key']),
  I + ' f5 d3': ('Small d-pawn move', 'The Rousseau Gambit wants you to take. Guard the e-pawn and develop: the f-pawn has only opened lines to Black\'s own king.', ['key']),
}
allp = set()
for _, _, path, _ in table:
    t = path.split()
    for k in range(1, len(t) + 1): allp.add(' '.join(t[:k]))
drop = [k for k in NOTES if ' '.join(k.split()) not in allp]
print('notes without a node (dropped):', drop)
# a position the rest of the book already has a note for keeps that note (the first moves are shared with the center attack)
import types
for m in ('italslow', 'wfill'): sys.modules[m] = types.ModuleType(m)
sys.path.insert(0, str(paths.ROOT / 'content/white')); import content, content2  # noqa: F401  (content2 registers the later chapters' notes)
have = set(content.NOTES); shared = [k for k in NOTES if ' '.join(k.split()) in have]
print('notes the book already has (kept as they are):', shared)
NOTES = {k: v for k, v in NOTES.items() if k not in drop and k not in shared}
auto = draft.named_moves([t[2] for t in table], 'w', skip=have)
mod = draft.module_text("""White's Italian, a second variation: the slow Italian, a pack for the slot 'whiteItalian' beside the center attack
(see PACKS in content2_meta.py).

One setup, one order: bishop, d-pawn one square, c-pawn one square, castle, rook beside the king, queen's knight behind
the d-pawn, the small h-pawn move, bishop back out of reach, then the knight round to the kingside. The lines were
drafted with pipeline/draft.py: Black's moves by the Maia 1300/1500 odds, yours from the setup's order wherever
Stockfish 17.1 accepts it and the engine's move elsewhere. SAN is internal; notes are plain English.""",
  'from content import n, J, L, PARTS', [PARTS], text, NOTES, auto, lambda ps: 'PARTS.extend([\n' + ''.join(f"  dict(id={p['id']!r}, ch={p['ch']!r}, title={p['title']!r}, kicker={p['kicker']!r},\n       blurb={p['blurb']!r}),\n" for p in ps) + '])')
open(paths.ROOT / 'content/white/italslow.py', 'w').write(mod)
for lid, title, path, reach in table: print(f"{reach*100:5.2f} {lid:24s} {title:58s} {path[19:]}")
print(len(leaves), 'leaves')
print('FLAGS'); [print('  ', f) for f in W.flags]
draft.done()
