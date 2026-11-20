"""The English for White (content/white/english.py): the setup's order, the moves fixed by hand, the lessons and the notes.
Run it to redraft the pack (python3 pipeline/drafts/english.py); it overwrites the module, so notes are edited here."""
import sys, re, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import paths, chess, draft
def system(b, path):
    # one setup in one order: c-pawn, queen's knight, g-pawn, bishop to the long diagonal, e-pawn two squares,
    # king's knight tucked in, castle, small d-pawn move. When Black's d-pawn comes two squares, take it; once the
    # c-pawn is gone the e-pawn stays home and the king's knight comes out in front of the f-pawn.
    W, B, P, N, Bi, K = chess.WHITE, chess.BLACK, chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.KING
    def on(sq, pt, col):
        x = b.piece_at(sq)
        return x is not None and x.piece_type == pt and x.color == col
    if on(chess.D5, P, B): return ['cxd5']                       # a pawn on the long diagonal's square: take it or let the engine say
    if not on(chess.C4, P, W) and not on(chess.E4, P, W):         # open: no wall to build
        return ['Nc3', 'g3', 'Bg2', 'Nf3', 'O-O', 'd3']
    if on(chess.F3, N, W): return ['Nc3', 'g3', 'Bg2', 'O-O', 'd3']   # the knight is already out in front of the f-pawn: no wedge
    base = ['c4', 'Nc3', 'g3', 'Bg2'] + (['e4', 'Nge2', 'O-O', 'd3'] if on(chess.G2, Bi, W) else [])
    done = on(chess.E4, P, W) and on(chess.E2, N, W) and on(chess.D3, P, W) and on(chess.G1, K, W)
    return base + (['Be3', 'Qd2', 'f4', 'Nd5', 'h3', 'Rb1'] if done else [])
# Black's e-pawn one square backs up the d-pawn push: the king's knight comes out first. The c-pawn one square with
# the knight on its way to hit your e-pawn square: go at Black's e-pawn first.
fixed = {'': 'c4', 'c4 Nf6 Nc3 e6': 'Nf3', 'c4 e6 Nc3 Nf6': 'Nf3', 'c4 c5 Nc3 e6': 'Nf3', 'c4 e6 Nc3 c5': 'Nf3', 'c4 e5 Nc3 Nf6 g3 c6': 'Nf3'}
W = draft.Walk('w', system, fixed, known={}, tol=45,
               thr=lambda n, r: 0.012 if n <= 2 else 0.04 if n <= 4 else 0.06 if n <= 8 else 0.09, min_reach=0.0012,
               depth=lambda r: 18 if r >= 0.02 else 16 if r >= 0.0015 else 14, follow=True)
leaves = W.run([('c4 e5 Nc3 Nf6 g3 Nc6 Bg2', None), ('c4 e5 Nc3 Nf6 g3', None), ('c4', 1.0)])
S = 'c4 e5 Nc3 Nf6 g3'
LESSONS = [
  dict(id='en-main', main=S + ' Nc6 Bg2 Bc5 e4 O-O', part='en-rev', root=S + ' Nc6', title='The setup: fianchetto, then the e-pawn', sub='Bishop to the long diagonal, e-pawn two squares, knight tucked in, castle', pri='core',
       why='Four in ten club players answer with the e-pawn, and both knights usually follow. The whole setup comes out here, in its usual order.', outcome='A slow game on your terms'),
  dict(id='en-open', main=S + ' d5 cxd5 Nxd5 Bg2 Nxc3 bxc3 Nc6', part='en-rev', root=S + ' d5', title='Black opens the middle', sub='Take the d-pawn; then the king\'s knight comes out the usual way', pri='core',
       why='One in five pushes the d-pawn at once. Take it, and your bishop\'s diagonal is wide open.', outcome='Equal, with an open diagonal'),
  dict(id='en-bb4', main=S + ' Bb4 Bg2 Bxc3 bxc3 O-O', part='en-rev', root=S + ' Bb4', title='The bishop comes at your knight', sub='Carry on; if it takes, the b-pawn takes back', pri='common',
       why='One in five brings the bishop out to trade it for your knight. Let it: you get the two bishops and another pawn for the middle.', outcome='Slightly better for you'),
  dict(id='en-bc5', main=S + ' Bc5 Bg2 O-O e4 d6', part='en-rev', root=S + ' Bc5', title='The bishop aims at f2', sub='Bishop out, then the small e-pawn move if the knight jumps', pri='common',
       why='One in five aims the bishop at f2. Your setup doesn\'t change; one knight jump needs a careful answer.', outcome='Equal'),
  dict(id='en-3rd', part='en-rev', root=S, title='Other third moves', sub='The c-pawn gets ready for the d-pawn: go at the e-pawn first', pri='common',
       why='One in twelve plays the c-pawn one square here, to push the d-pawn next. Your king\'s knight goes at the e-pawn before that happens.', outcome='Equal'),
  dict(id='en-nc6', part='en-revside', root='c4 e5 Nc3 Nc6', title='Queen\'s knight first', sub='The same setup, by another road', pri='common',
       why='One in seven brings the other knight out first. Nothing changes for you.', outcome='Equal'),
  dict(id='en-2bc5', part='en-revside', root='c4 e5 Nc3 Bc5', title='The early bishop and the queen', sub='G-pawn, then the small e-pawn move when the queen comes at f2', pri='common',
       why='One in eight brings the bishop out on move two, often with the queen behind it aiming at f2.', outcome='Equal or better'),
  dict(id='en-2nd', main='c4 e5 Nc3 d6 g3 Nf6 Bg2 Be7', part='en-revside', root='c4 e5', title='Other second moves', sub='The bishop at your knight, the small d-pawn, the c-pawn', pri='common',
       why='The bishop on move two, the small d-pawn move, and the c-pawn that gets ready to push the d-pawn.', outcome='Equal'),
  dict(id='en-sym', part='en-sym', root='c4 c5', title='The Symmetrical', sub='The same setup; Black often copies it', pri='core',
       why='One in ten copies your first move. Your setup comes out move for move.', outcome='Equal, and you know the plan'),
  dict(id='en-nf6', part='en-ind', root='c4 Nf6', title='Knight first', sub='Against the fianchetto the whole setup; against the e-pawn one square, the king\'s knight first', pri='core',
       why='One in nine starts with the knight and chooses a setup later. Yours is the same against all of them.', outcome='Equal'),
  dict(id='en-g6', part='en-ind', root='c4 g6', title='The fianchetto at once', sub='Bishop against bishop on the long diagonals', pri='rare',
       why='Black fianchettoes first. The same eight moves.', outcome='Equal'),
  dict(id='en-d5', part='en-dp', root='c4 d5', title='The d-pawn at once', sub='Take it; when the queen takes back, the knight comes out with tempo', pri='core',
       why='One in ten pushes the d-pawn on move one. Take it: the queen that takes back loses time to your knight.', outcome='Better for you'),
  dict(id='en-e6', main='c4 e6 Nc3 d5 cxd5 exd5 d4 Nf6 Bg5 Be7', part='en-dp', root='c4 e6', title='The e-pawn one square', sub='Knight, then take the d-pawn when it comes', pri='common',
       why='One in eleven gets ready for the d-pawn push. When it comes, take it and put your own d-pawn in the middle.', outcome='Equal'),
  dict(id='en-c6', main='c4 c6 Nc3 d5 cxd5 cxd5 Nf3 Nf6', part='en-dp', root='c4 c6', title='The c-pawn one square', sub='Knight, take the d-pawn, king\'s knight out', pri='rare',
       why='The same idea with the c-pawn. Take the d-pawn when it comes; the king\'s knight comes out in front of the f-pawn.', outcome='Equal'),
  dict(id='en-first', main='c4 b6 Nc3 Bb7 d4 e6', part='en-rare', root='c4', title='Rare first moves', sub='The small d-pawn, the f-pawn, the b-pawn', pri='rare',
       why='Everything else. The setup does the work.', outcome='Equal'),
]
text, table = draft.emit(leaves, LESSONS, 'w')
RETITLE = {}
for lid, t in RETITLE.items():
    text, k = re.subn(r"\('" + lid + r"', '(?:[^'\\]|\\.)*',", "('" + lid + "', '" + t.replace("'", "\\'") + "',", text)
    assert k == 1, lid
PARTS = [
  dict(id='en-rev', ch='english', title='The e-pawn and the king\'s knight', kicker='King\'s English',
       blurb='Black takes the middle the way you would with White. C-pawn, knight, g-pawn, bishop, then the e-pawn two squares and the king\'s knight tucked in behind it.'),
  dict(id='en-revside', ch='english', title='Other second moves', kicker='The early bishop, the other knight',
       blurb='Black changes the order. Yours stays the same, and one early queen move needs the small e-pawn move.'),
  dict(id='en-sym', ch='engsym', title='Black copies you', kicker='Symmetrical English',
       blurb='C-pawn against c-pawn. The setup comes out in the same order.'),
  dict(id='en-ind', ch='engsym', title='The knight and the fianchetto', kicker='Anglo-Indian',
       blurb='Black develops first and shows the pawns later. Against a fianchetto the whole setup; against the e-pawn one square, the king\'s knight comes out first.'),
  dict(id='en-dp', ch='engrare', title='Black\'s d-pawn comes two squares', kicker='Anglo-Scandinavian, Agincourt, Caro-Kann setup',
       blurb='At once, or backed up by a pawn first. The rule is the same: take it.'),
  dict(id='en-rare', ch='engrare', title='Rare first moves', kicker='Sidelines',
       blurb='The small d-pawn, the f-pawn, the b-pawn. The setup does the work.'),
]
M = S + ' Nc6 Bg2 Bc5 e4 O-O Nge2 d6 O-O Bg4 d3'
NOTES = {
  'c4': ('C-pawn two squares', 'The first move of the setup. It watches the square Black\'s d-pawn wants to reach, from the side, and keeps your own center pawns back for later.', ['key']),
  'c4 e5 Nc3': ('Queen\'s knight out', 'The second move of the setup, whatever Black plays. Knight and c-pawn watch the same light square in the middle.', ['key']),
  S: ('G-pawn one square', 'It makes room for the bishop on the long diagonal.', ['key'], dict(arrows=['f1g2g'])),
  S + ' Nc6 Bg2': ('Bishop to the long diagonal', 'Bishop, knight and c-pawn now aim at the same light square. The whole setup is built around it.', ['key'], dict(arrows=['g2d5g', 'c3d5g', 'c4d5g'], circles=['d5g'])),
  S + ' Nc6 Bg2 Bc5 e4': ('E-pawn two squares', 'A fourth guard for the light square in the middle. The dark square in front of your d-pawn is the price, and your knight will cover it from behind the e-pawn.', ['key']),
  S + ' Nc6 Bg2 Bc5 e4 O-O Nge2': ('King\'s knight tucked in', 'Behind the e-pawn, not in front of the f-pawn: the bishop\'s diagonal stays open and the f-pawn is free to go later.', ['key']),
  S + ' Nc6 Bg2 Bc5 e4 O-O Nge2 d6 O-O': ('Castle', 'King safe, rook behind the f-pawn.'),
  M: ('Small d-pawn move', 'The setup is complete: three pawns in a wedge, the bishop behind them, the knights on the dark squares\' guard.', ['key']),
  S + ' Nc6 Bg2 Bc5 e4 d6 h3': ('Small h-pawn move first', 'Black\'s d-pawn has moved, so the light bishop now backs up a knight jump toward f2. Take that square away before your knight is tucked in.', ['key']),
  S + ' Bc5 Bg2 Ng4 e3': ('Small e-pawn move', 'Knight and bishop both aim at f2. One square shuts the bishop out, and your queen now looks at the knight.', ['key']),
  S + ' Bc5 Bg2 Ng4 e3 Qf6 Qxg4': ('Take the knight', 'It has no guard.', ['key']),
  S + ' Bc5 Bg2 d6 d3': ('Small d-pawn move first', 'The e-pawn waits. With the bishop aimed at f2 and Black\'s d-pawn moved, two squares would let the knight jump in.'),
  S + ' Bc5 Bg2 d6 d3 Nc6 e3': ('Small e-pawn move', 'It shuts the bishop\'s diagonal to f2. The knight goes behind the pawn as usual.', ['key']),
  S + ' Bb4 Bg2 Bxc3 bxc3': ('B-pawn takes back', 'Toward the middle. You have the two bishops, and the extra c-pawn will back up your d-pawn later.', ['key']),
  S + ' Bb4 Bg2 d6 Qa4+': ('Queen check', 'The bishop has no guard, and the check hits it too. Black can block with the knight to guard it, but your bishop takes that knight.', ['key'], dict(arrows=['a4e8r', 'a4b4r'])),
  S + ' Bb4 Bg2 d6 Qa4+ Nc6 Bxc6+ bxc6 Qxb4': ('A bishop up', 'Check, take the guard, take the bishop.'),
  S + ' d5 cxd5': ('Take it', 'The rule against the d-pawn: take it. Your bishop\'s diagonal will be open all the way.', ['key']),
  S + ' d5 cxd5 Nxd5 Bg2 Nxc3 bxc3': ('B-pawn takes back', 'Toward the middle: it will back up your d-pawn when that goes two squares.'),
  S + ' d5 cxd5 Nxd5 Bg2 Nxc3 bxc3 Nc6 Nf3': ('King\'s knight out', 'The c-pawn is gone, so there is no wedge to build. The knight goes in front of the f-pawn, and you castle.', ['key']),
  S + ' Nc6 Bg2 b6 Nf3': ('King\'s knight out', 'Black\'s bishop is coming to the long diagonal, where it will have no guard. Your knight gets ready to take the e-pawn.'),
  S + ' Nc6 Bg2 b6 Nf3 Bb7 Nxe5': ('Take the e-pawn', 'If the knight takes back, your bishop takes the bishop on the long diagonal: a clean pawn.', ['key']),
  'c4 e5 Nc3 Bc5 g3 Qf6 e3': ('Small e-pawn move', 'Queen and bishop aim at f2. One square stops both, and your bishop still goes to the long diagonal next.', ['key']),
  'c4 e5 Nc3 Bc5 g3 Qf6 e3 Ne7 Bg2 O-O Nge2 c6 Ne4': ('Knight jumps at queen and bishop', 'Both at once. The queen moves, and you take the bishop.', ['key']),
  'c4 e5 Nc3 c6 Nf3': ('King\'s knight out', 'Black\'s c-pawn gets ready to push the d-pawn. Go at the e-pawn first, before it has a second guard.', ['key']),
  'c4 d5 cxd5': ('Take it', 'The rule against the d-pawn, on move two as well.', ['key']),
  'c4 d5 cxd5 Qxd5 Nc3': ('Knight out', 'The queen has to move again, and you are a move ahead.', ['key']),
  'c4 d5 cxd5 Qxd5 Nc3 Qd8 Nf3 Nf6 d4': ('D-pawn two squares', 'No c-pawn, no wedge. With Black\'s queen back home, take the whole middle instead.', ['key']),
  'c4 d5 cxd5 Qxd5 Nc3 Qd8 Nf3 Nf6 d4 e6 e4 Bb4 Bd3 O-O e5': ('E-pawn pushes at the knight', 'The knight has to leave the king. If it goes to the middle, your bishop takes the h-pawn with check and the attack crashes through.', ['key'], dict(arrows=['d3h7r'])),
  'c4 e6 Nc3 d5 cxd5 exd5 d4': ('D-pawn two squares', 'After the trade Black has a pawn fixed in the middle. Put yours beside it; the dark bishop comes out next.', ['key']),
  'c4 b6 Nc3 Bb7 d4': ('D-pawn two squares', 'Black\'s bishop already owns the long diagonal, so your own g-pawn move would lose the corner rook. Take the middle with pawns instead.', ['key']),
  'c4 b6 Nc3 Bb7 d4 e6 f3': ('Small f-pawn move', 'It shuts the bishop\'s diagonal and gets the e-pawn ready to go two squares.', ['key']),
  'c4 Nf6 Nc3 e6 Nf3': ('King\'s knight out', 'Black\'s e-pawn has gone one square to back up the d-pawn. The wedge would be too slow, so the knight comes out the usual way, and the d-pawn is taken when it arrives.', ['key']),
  'c4 c5 Nc3 e6 Nf3': ('King\'s knight out', 'The e-pawn one square means the d-pawn is coming. Knight in front of the f-pawn first, then the g-pawn and the bishop.', ['key']),
  'c4 e5 Nc3 Nf6 g3 c6 Nf3': ('King\'s knight out', 'The c-pawn is getting the d-pawn ready. Go at the e-pawn before it has a second guard.', ['key']),
  'c4 c5 Nc3 Nc6 g3 g6 Bg2 Bg7 e4': ('E-pawn two squares', 'The same wedge against the mirror setup.'),
  'c4 c5 Nc3 Nc6 g3 g6 Bg2 Bg7 e4 e6 Nge2 Nge7 O-O O-O d3 a6 Be3': ('Bishop out', 'The setup is done. The bishop looks at the c-pawn, and your d-pawn push is next.', ['key']),
}
allp = set()
for _, _, path, _ in table:
    t = path.split()
    for k in range(1, len(t) + 1): allp.add(' '.join(t[:k]))
drop = [k for k in NOTES if ' '.join(k.split()) not in allp]
print('notes without a node (dropped):', drop)
NOTES = {k: v for k, v in NOTES.items() if k not in drop}
auto = draft.named_moves([t[2] for t in table], 'w', skip=draft.base_paths('white'))
mod = draft.module_text("""White from the side: the English Opening, a third pack for the slot 'white' (see PACKS in content2_meta.py).

One setup, one order: c-pawn two squares, queen's knight, g-pawn one square, bishop to the long diagonal, e-pawn two
squares, king's knight tucked in behind it, castle, small d-pawn move. When Black's d-pawn comes two squares, take it;
once the c-pawn is gone the e-pawn stays home and the king's knight comes out in front of the f-pawn. The lines were
drafted with pipeline/draft.py: Black's moves by the Maia 1300/1500 odds, yours from the setup's order wherever
Stockfish 17.1 accepts it and the engine's move elsewhere. SAN is internal; notes are plain English.""",
  'from content import n, J, L, PARTS', [PARTS], text, NOTES, auto, lambda ps: 'PARTS.extend([\n' + ''.join(f"  dict(id={p['id']!r}, ch={p['ch']!r}, title={p['title']!r}, kicker={p['kicker']!r},\n       blurb={p['blurb']!r}),\n" for p in ps) + '])')
open(paths.ROOT / 'content/white/english.py', 'w').write(mod)
for lid, title, path, reach in table: print(f"{reach*100:5.2f} {lid:24s} {title:58s} {path[3:]}")
print(len(leaves), 'leaves')
print('FLAGS'); [print('  ', f) for f in W.flags]
draft.done()
