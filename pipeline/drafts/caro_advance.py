"""The Advance against the Caro-Kann for White (content/white/caroadv.py): the setup's order, the lessons and the notes.
Run it to redraft the pack (python3 pipeline/drafts/caro_advance.py); it overwrites the module, so notes are edited here."""
import sys, re, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import paths, chess, draft
def system(b, path):
    # push past the d-pawn, then the quiet setup behind the chain: knight, bishop one square, castle; the c-pawn backs
    # the chain when Black's c-pawn hits it; then the queen's knight and the bishop
    W, B, P, N, Bi = chess.WHITE, chess.BLACK, chess.PAWN, chess.KNIGHT, chess.BISHOP
    def on(sq, pt, col=W):
        x = b.piece_at(sq)
        return x is not None and x.piece_type == pt and x.color == col
    order = (['d4'] if on(chess.D2, P) else []) + (['e5'] if on(chess.E4, P) and on(chess.D4, P) and on(chess.D5, P, B) else [])
    order += (['Nf3'] if on(chess.G1, N) else []) + (['Be2'] if on(chess.F1, Bi) else []) + ['O-O']
    if on(chess.C5, P, B) and on(chess.C2, P): order.append('c3')
    if on(chess.B1, N): order.append('Nbd2' if on(chess.C3, P) else 'Nc3')
    return order + (['Be3'] if on(chess.C1, Bi) else [])
A = 'e4 c6 d4 d5 e5'
M = A + ' Bf5 Nf3 e6 Be2'
fixed = {}
W = draft.Walk('w', system, fixed, known=draft.known_from('white', skip_chapters=('caro', 'caroadv')), tol=45,
               thr=lambda n, r: 0.02 if n <= 6 else 0.05 if n <= 10 else 0.09, min_reach=0.0003,
               depth=lambda r: 18 if r >= 0.005 else 16 if r >= 0.001 else 14)
leaves = W.run([(M, None), (A + ' c5', None), ('e4 c6', None)])
LESSONS = [
  dict(id='ca-main', part='ca-push', root=M, main=M + ' c5', title='The bishop comes out: the quiet setup', sub='Knight, bishop one square, castle, then the c-pawn backs the chain', pri='core',
       why='Seven in ten bring the bishop out before the e-pawn shuts it in. You let it sit there: knight, bishop, castle, and the space is yours for good.', outcome='More room and an easy game'),
  dict(id='ca-fourth', part='ca-push', root=A + ' Bf5', title='The bishop comes out: other tries', sub='The edge pawn, the queen, a pin on your knight', pri='common',
       why='After the bishop Black doesn\'t always play the e-pawn. The setup comes out the same way.', outcome='More room'),
  dict(id='ca-c5', part='ca-push', root=A + ' c5', title='The c-pawn hits the chain at once', sub='The Botvinnik-Carls: develop, and take the pawn when it helps', pri='common',
       why='One in ten hits your d-pawn straight away, a move that usually waits. The c-pawn has now moved twice.', outcome='A move ahead'),
  dict(id='ca-e6', part='ca-push', root=A + ' e6', title='The e-pawn shuts the bishop in', sub='A French a move behind: the same setup', pri='common',
       why='One in ten locks the bishop in behind the pawns. Black is playing a French with a move lost on the c-pawn.', outcome='More room and a move ahead'),
  dict(id='ca-third', part='ca-push', root=A, title='Other third moves', sub='The f-pawn at your chain, the fianchetto, the queen out', pri='rare',
       why='Whatever Black tries against the chain, the pieces come out behind it in the same order.', outcome='Better for you'),
  dict(id='ca-second', part='ca-other', root='e4 c6', title='Black skips the d-pawn', sub='The small d-pawn, the e-pawn, the fianchetto', pri='rare',
       why='Without the d-pawn in the middle there is nothing to push past. Two pawns side by side and the usual pieces.', outcome='A big center'),
]
text, table = draft.emit(leaves, LESSONS, 'w')
PARTS = [
  dict(id='ca-push', ch='caroadv', title='The pawn pushes past', kicker='Advance Variation', blurb='Black\'s d-pawn comes to meet yours and the e-pawn steps past it. Behind the chain your pieces come out the quiet way: knight, bishop one square, castle. When the c-pawn hits the chain, yours backs it up.'),
  dict(id='ca-other', ch='caroadv', title='No d-pawn to push past', kicker='Second-move sidelines', blurb='The rare second moves. Take the middle with both pawns and develop.'),
]
NOTES = {
  'e4 c6 d4': ('D-pawn two squares', 'Two pawns in the middle. Black\'s d-pawn nearly always comes to meet them.'),
  A: ('Push past', 'The e-pawn steps past instead of trading. The two pawns take room from Black for the rest of the game.', ['key']),
  A + ' Bf5 Nf3': ('Knight out', 'Let the bishop sit there. Knight, then the bishop one square, then castle.', ['key']),
  M: ('Bishop one square', 'Out of the way and out of reach. You castle next.', ['key']),
  M + ' c5 O-O': ('Castle', 'King safe first. The c-pawn backs up the chain on the next move.', ['key']),
  M + ' c5 O-O Nc6 c3': ('C-pawn backs the chain', 'Black is hitting the base of your chain. If the pawns are traded there, another pawn stands in the same place.', ['key'], dict(arrows=['c3d4g'])),
  M + ' c5 O-O Nc6 c3 cxd4 Nxd4': ('Knight takes back', 'It lands in the middle with a hit on the bishop, and the c-pawn still keeps Black\'s knight out of the squares in front of it.', ['key']),
  M + ' c5 O-O cxd4 Nxd4': ('Knight takes back', 'A hit on the bishop, and the knight stands in the middle of the board.', ['key']),
  A + ' c5 Nf3': ('Knight out', 'The same first move of the setup. Black\'s c-pawn has now moved twice, and you are a move ahead.', ['key']),
  A + ' e6 Nf3': ('Knight out', 'Black has shut the bishop in. The setup is the same, with more room than ever.'),
}
allp = set()
for _, _, path, _ in table:
    t = path.split()
    for k in range(1, len(t) + 1): allp.add(' '.join(t[:k]))
drop = [k for k in NOTES if ' '.join(k.split()) not in allp]
print('notes without a node (dropped):', drop)
# a position the rest of the book already has a note for keeps that note (the first moves are shared with the main line)
import types
for m in ('caroadv', 'wfill'): sys.modules[m] = types.ModuleType(m)
sys.path.insert(0, str(paths.ROOT / 'content/white')); import content, content2  # noqa: F401  (content2 registers the later chapters' notes)
have = set(content.NOTES); shared = [k for k in NOTES if ' '.join(k.split()) in have]
print('notes the book already has (kept as they are):', shared)
NOTES = {k: v for k, v in NOTES.items() if k not in drop and k not in shared}
auto = draft.named_moves([t[2] for t in table], 'w', skip=have)
mod = draft.module_text("""White against the Caro-Kann, a second variation: the Advance, a pack for the slot 'whiteCaro' beside the main line
(see PACKS in content2_meta.py).

One setup: push past the d-pawn, then knight, bishop one square, castle; the c-pawn backs the chain when Black's
c-pawn hits it, and the queen's knight and the bishop follow. The lines were drafted with pipeline/draft.py: Black's
moves by the Maia 1300/1500 odds, yours from the setup's order wherever Stockfish 17.1 accepts it and the engine's
move elsewhere. SAN is internal; notes are plain English.""",
  'from content import n, J, L, PARTS', [PARTS], text, NOTES, auto, lambda ps: 'PARTS.extend([\n' + ''.join(f"  dict(id={p['id']!r}, ch={p['ch']!r}, title={p['title']!r}, kicker={p['kicker']!r},\n       blurb={p['blurb']!r}),\n" for p in ps) + '])')
open(paths.ROOT / 'content/white/caroadv.py', 'w').write(mod)
for lid, title, path, reach in table: print(f"{reach*100:5.2f} {lid:24s} {title:58s} {path[6:]}")
print(len(leaves), 'leaves')
print('FLAGS'); [print('  ', f) for f in W.flags]
draft.done()
