"""White, the house book: odd moves that were missing. Black's odd first moves (the Borg, the Barnes, the Ware, the
Goldsmith, the Lemming, the Adams, the Duras Gambit, the Carr), odd second moves after the knight (the Gunderam and
others) and odd third moves in the Italian. Drafted with pipeline/draft.py from the positions the book already answers:
a known position keeps its move, a new one takes the first developing move Stockfish 17.1 accepts. SAN is internal."""
from content import n, J, L, PARTS


L('it-odd', 'odd', 'Odd third moves', 'Center pawns first; when a piece hangs, take it', 'rare',
  'e4 e5 Nf3 Nc6 Bc4 g6 d4 exd4 c3 dxc3 Qb3 Qe7 O-O',
  alts=[('it-odd-bb4', 'Bishop out to the side', 'e4 e5 Nf3 Nc6 Bc4 Bb4 c3 Bc5 d4 exd4 O-O dxc3 Qb3'),
        ('it-odd-bb4ba5', 'Bishop out to the side, then bishop steps back', 'e4 e5 Nf3 Nc6 Bc4 Bb4 c3 Ba5 d4 exd4 O-O dxc3 Qb3'),
        ('it-odd-na5', 'Knight jumps forward', 'e4 e5 Nf3 Nc6 Bc4 Na5 Nxe5 Nxc4 Nxc4 d5 exd5 Qxd5 Ne3'),
        ('it-odd-bg7', 'Fianchetto', 'e4 e5 Nf3 Nc6 Bc4 g6 d4 Bg7 dxe5 Nxe5 Nxe5 Bxe5 Bxf7+ Kxf7 Qd5+ Ke8 Qxe5+'),
        ('it-odd-qf6', 'Queen comes out', 'e4 e5 Nf3 Nc6 Bc4 Qf6 O-O Bc5 Nc3 d6 Nd5 Qd8 c3'),
        ('it-odd-na5nf6', 'Knight jumps forward, then king\'s knight out', 'e4 e5 Nf3 Nc6 Bc4 Na5 Nxe5 Nxc4 Nxc4 Nf6 O-O Nxe4 Nc3'),
        ('it-odd-bd6', 'Bishop to the middle', 'e4 e5 Nf3 Nc6 Bc4 Bd6 d4 exd4 O-O Nf6 e5 Nxe5 Re1'),
        ('it-odd-qf6bc5', 'Queen comes out, then bishop aims at f2', 'e4 e5 Nf3 Nc6 Bc4 Qf6 O-O Bc5 Nc3 Nge7 Nd5 Nxd5 exd5 Nd4 Nxe5 Qxe5 Re1'),
        ('it-odd-a6', 'Small a-pawn move', 'e4 e5 Nf3 Nc6 Bc4 a6 d4 exd4 c3 dxc3 O-O cxb2 Bxb2 Nf6 Ng5'),
        ('it-odd-na5bc5', 'Knight jumps forward, then bishop aims at f2', 'e4 e5 Nf3 Nc6 Bc4 Na5 Nxe5 Nxc4 Nxc4 Bc5 d4 Bb4+ c3'),
        ('it-odd-bg7v2', 'Fianchetto on move 5', 'e4 e5 Nf3 Nc6 Bc4 g6 d4 exd4 c3 Bg7 cxd4 Nge7 O-O'),
        ('it-odd-bb4ba5d6', 'Bishop out to the side, then bishop steps back, then small d-pawn move', 'e4 e5 Nf3 Nc6 Bc4 Bb4 c3 Ba5 d4 d6 a4 Bg4 b4'),
        ('it-odd-qe7nf6', 'Queen comes out, then king\'s knight out', 'e4 e5 Nf3 Nc6 Bc4 Qe7 c3 Nf6 d4 Nxe4 O-O exd4 Re1'),
        ('it-odd-qe7nf6exd4', 'Queen comes out, then king\'s knight out, then pawn takes the pawn', 'e4 e5 Nf3 Nc6 Bc4 Qe7 c3 Nf6 d4 exd4 O-O dxc3 Nxc3 Nxe4 Nxe4 Qxe4 Re1'),
        ('it-odd-a6b5', 'Small a-pawn move, then b-pawn two squares', 'e4 e5 Nf3 Nc6 Bc4 a6 d4 b5 Bd5 Bb7 Nxe5 Nxe5 Bxb7 Rb8 Bxa6 Nc6 Nc3'),
        ('it-odd-bd6nf6', 'Bishop to the middle, then king\'s knight out', 'e4 e5 Nf3 Nc6 Bc4 Bd6 d4 Nf6 c3 Nxe4 Qe2 Nf6 dxe5 Nxe5 O-O'),
        ('it-odd-qe7d6', 'Queen comes out, then small d-pawn move', 'e4 e5 Nf3 Nc6 Bc4 Qe7 c3 d6 d4 exd4 O-O dxc3 Nxc3 Be6 Nd5'),
        ('it-odd-qe7h6', 'Queen comes out, then small h-pawn move', 'e4 e5 Nf3 Nc6 Bc4 Qe7 c3 h6 d4 exd4 O-O dxc3 Nxc3 d6 Nd5'),
        ('it-odd-qf6d6', 'Queen comes out, then small d-pawn move on move 3', 'e4 e5 Nf3 Nc6 Bc4 Qf6 O-O d6 Nc3 Be6 Nd5 Bxd5 exd5 Nd4 Nxd4 exd4 Bb5+')],
  why='The fianchetto, the early queen, the knight to the rim. Each leaves something loose, and the same c-pawn and d-pawn plan finds it.', outcome='Better for you')
L('x-odd', 'e5x-misc', 'The Gunderam and other odd second moves', 'Bishop out or d-pawn two squares, then castle', 'rare',
  'e4 e5 Nf3 Qe7 Bc4 Nf6 d4 exd4 O-O Nxe4 Re1',
  alts=[('x-odd-g6', 'Small g-pawn move', 'e4 e5 Nf3 g6 d4 exd4 Qxd4 Nf6 Bg5 Bg7 e5'),
        ('x-odd-bb4', 'Bishop out to the side', 'e4 e5 Nf3 Bb4 c3 Bc5 Nxe5 Qf6 d4'),
        ('x-odd-g6bg7', 'Small g-pawn move, then fianchetto', 'e4 e5 Nf3 g6 d4 Bg7 dxe5 Qe7 Nc3 Bxe5 Nd5'),
        ('x-odd-h6', 'Small h-pawn move', 'e4 e5 Nf3 h6 Nxe5 Qe7 d4 d6 Nf3 Qxe4+ Be3 Bg4 c4'),
        ('x-odd-a6', 'Small a-pawn move', 'e4 e5 Nf3 a6 Nxe5 Qe7 d4 d6 Nf3 Qxe4+ Be3 Bg4 Nc3'),
        ('x-odd-bd6', 'Bishop to the middle', 'e4 e5 Nf3 Bd6 Bc4 Nf6 d4 Nxe4 dxe5 Bc5 Qd5'),
        ('x-odd-bb4ba5', 'Bishop out to the side, then bishop steps back', 'e4 e5 Nf3 Bb4 c3 Ba5 Nxe5 Qe7 d4 d6 Qa4+ Nc6 Nxc6 bxc6 Qxa5 Qxe4+ Be3'),
        ('x-odd-c6', 'Gunderam Gambit', 'e4 e5 Nf3 c6 d4 exd4 Qxd4 c5 Qe5+ Qe7 Qxe7+ Bxe7 Nc3'),
        ('x-odd-bd6nf6', 'Bishop to the middle, then king\'s knight out', 'e4 e5 Nf3 Bd6 Bc4 Nf6 d4 exd4 e5 Qe7 O-O Bxe5 Nxe5 Qxe5 Re1'),
        ('x-odd-g6bg7nc6', 'Small g-pawn move, then fianchetto, then queen\'s knight out', 'e4 e5 Nf3 g6 d4 Bg7 dxe5 Nc6 Bg5 f6 exf6 Bxf6 Qd2'),
        ('x-odd-bb4ba5d6', 'Bishop out to the side, then bishop steps back, then small d-pawn move', 'e4 e5 Nf3 Bb4 c3 Ba5 Nxe5 d6 Nxf7 Kxf7 Qh5+ g6 Qxa5 Nc6 Qb5'),
        ('x-odd-bd6h6', 'Bishop to the middle, then small h-pawn move', 'e4 e5 Nf3 Bd6 Bc4 h6 d4 exd4 O-O Nc6 c3 dxc3 e5'),
        ('x-odd-c6d6', 'Gunderam Gambit, then small d-pawn move', 'e4 e5 Nf3 c6 d4 d6 dxe5 dxe5 Qxd8+ Kxd8 Nxe5 Be6 Bc4'),
        ('x-odd-c6exd4', 'Gunderam Gambit, then pawn takes the pawn', 'e4 e5 Nf3 c6 d4 exd4 Qxd4 d5 Nc3 Nf6 exd5 cxd5 Bg5'),
        ('x-odd-h6d6', 'Small h-pawn move, then small d-pawn move', 'e4 e5 Nf3 h6 Nxe5 d6 Nf3 Nf6 Nc3 Be7 d4 O-O Bd3'),
        ('x-odd-h6nf6', 'Small h-pawn move, then king\'s knight out', 'e4 e5 Nf3 h6 Nxe5 Nf6 Bc4 d5 exd5 Nxd5 Nc3 Be6 Nxf7 Bxf7 Nxd5 Bxd5 Qh5+'),
        ('x-odd-c6exd4d6', 'Gunderam Gambit, then pawn takes the pawn, then small d-pawn move', 'e4 e5 Nf3 c6 d4 exd4 Qxd4 d6 Nc3 Nf6 Bf4 Be7 O-O-O'),
        ('x-odd-g6exd4', 'Small g-pawn move, then pawn takes the pawn', 'e4 e5 Nf3 g6 d4 exd4 Qxd4 Qf6 Qc4 Nc6 Nc3 Bb4 Bd2'),
        ('x-odd-c6exd4nf6', 'Gunderam Gambit, then pawn takes the pawn, then king\'s knight out', 'e4 e5 Nf3 c6 d4 exd4 Qxd4 Nf6 Nc3 Be7 e5 Nd5 Nxd5 cxd5 Qxd5 O-O Be3'),
        ('x-odd-h6d6bg4', 'Small h-pawn move, then small d-pawn move, then bishop pins the knight', 'e4 e5 Nf3 h6 Nxe5 d6 Nf3 Bg4 d4 Nf6 Nc3 Be7 h3'),
        ('x-odd-h6exd4', 'Small h-pawn move, then pawn takes the pawn', 'e4 e5 Nf3 Qe7 Bc4 h6 d4 exd4 O-O Nc6 Nxd4 Nxd4 Qxd4 d6 Nc3'),
        ('x-odd-g6exd4f6', 'Small g-pawn move, then pawn takes the pawn, then small f-pawn move', 'e4 e5 Nf3 g6 d4 exd4 Qxd4 f6 Bc4 Nc6 Qd3 d6 Nc3'),
        ('x-odd-a6d6', 'Small a-pawn move, then small d-pawn move', 'e4 e5 Nf3 a6 Nxe5 d6 Nf3 Bg4 d4 Nf6 Nc3 Be7 h3'),
        ('x-odd-h6d6v2', 'Small h-pawn move, then small d-pawn move on move 3', 'e4 e5 Nf3 Qe7 Bc4 h6 d4 d6 c3 Be6 Qb3 Bxc4 Qxb7 Ba6 Qxa8 Qd8 Be3'),
        ('x-odd-d6', 'Small d-pawn move', 'e4 e5 Nf3 Qe7 Bc4 d6 d4 exd4 O-O c5 c3 dxc3 Nxc3 Be6 Nd5')],
  why='The queen in front of the bishop, the bishop in front of the d-pawn. Black blocks their own pieces: develop and open the middle.', outcome='Better for you')
L('rr-odd', 'rare-all', 'The Borg, the Barnes and other odd first moves', 'Both center pawns, then knights and bishops', 'rare',
  'e4 g5 d4 h6 Nc3 Bg7 h4 gxh4 Nf3 e6 Nxh4 Bf6 Nf3',
  alts=[('rr-odd-h6', 'Carr Defense', 'e4 h6 d4 g5 Nc3'),
        ('rr-odd-h6a6', 'Carr Defense, then small a-pawn move', 'e4 h6 d4 a6 Nf3 e6 Nc3'),
        ('rr-odd-f5', 'Duras Gambit', 'e4 f5 exf5 Nf6 d4 d5 Bd3 Nc6 Nf3 e6 O-O exf5 Re1+ Be7 c4'),
        ('rr-odd-f5nf6', 'Duras Gambit, then king\'s knight out', 'e4 f5 exf5 Nf6 d4 d5 Bd3 e6 Nf3 exf5 O-O Be7 Re1'),
        ('rr-odd-na6', 'Lemming Defense', 'e4 Na6 d4 d5 exd5 Qxd5 Nf3 Bg4 Be2 O-O-O Nc3 Qa5 Ne5'),
        ('rr-odd-na6e6', 'Lemming Defense, then small e-pawn move', 'e4 Na6 d4 e6 Nf3 d5 Nc3 Bb4 Bb5+ c6 Bxa6 bxa6 O-O'),
        ('rr-odd-f5d5', 'Duras Gambit, then d-pawn two squares', 'e4 f5 exf5 d5 Qh5+ g6 fxg6 Nf6 g7+ Nxh5 gxh8=Q Bf5 Qe5'),
        ('rr-odd-a5', 'Ware Defense', 'e4 a5 d4 a4 Nf3 e6 Nc3 Bb4 a3 Bxc3+ bxc3 Nf6 Bd3'),
        ('rr-odd-f6', 'Barnes Defense', 'e4 f6 d4 e5 Nf3 exd4 Bc4 Nc6 O-O Bc5 c3 dxc3 Bxg8 Rxg8 Qd5'),
        ('rr-odd-nh6', 'Hippopotamus Defense', 'e4 Nh6 d4 g6 Nc3 Bg7 Nf3 O-O h4 d6 h5 Bg4 hxg6 fxg6 Bxh6 Bxf3 Qd2'),
        ('rr-odd-f5d5kd7', 'Duras Gambit, then d-pawn two squares, then king steps out of check', 'e4 f5 exf5 d5 Qh5+ Kd7 d4 Nf6 Qd1 Nc6 Nf3 Ke8 Bd3'),
        ('rr-odd-nh6e6', 'Hippopotamus Defense, then small e-pawn move', 'e4 Nh6 d4 e6 Nf3 d5 Nc3 Bb4 Bxh6 gxh6 Bd3 Nc6 O-O'),
        ('rr-odd-a5b6', 'Ware Defense, then small b-pawn move', 'e4 a5 d4 b6 Nf3 Bb7 Nc3 e6 Bd3 Bb4 O-O Bxc3 bxc3 Nf6 e5'),
        ('rr-odd-nh6d5', 'Hippopotamus Defense, then d-pawn two squares', 'e4 Nh6 d4 d5 exd5 Qxd5 Nc3 Qd8 Nf3 Bg4 h3 Bxf3 Qxf3 Qxd4 Qxb7 Qe5+ Be3'),
        ('rr-odd-f6d6', 'Barnes Defense, then small d-pawn move', 'e4 f6 d4 d6 Nf3 e5 Nc3 c6 Bc4 b5 Nxb5 cxb5 Bd5'),
        ('rr-odd-bg7', 'Borg Gambit', 'e4 g5 d4 Bg7 Nc3 d6 Bxg5 h6 Be3 Nf6 Nf3 Bg4 Bc4'),
        ('rr-odd-h5', 'Goldsmith Defense', 'e4 h5 d4 h4 Nf3 h3 Nc3 hxg2 Bxg2 d6 Qd3 Bh3 Bxh3 Rxh3 Qb5+ c6 Qxb7'),
        ('rr-odd-h5g6', 'Goldsmith Defense, then small g-pawn move', 'e4 h5 d4 g6 Nf3 Bg7 Nc3 d6 Bc4 Bg4 Bg5 f6 h3'),
        ('rr-odd-f6e6', 'Barnes Defense, then small e-pawn move', 'e4 f6 d4 e6 Nf3 d5 Nc3 Bb4 Bd3 Bxc3+ bxc3 dxe4 Bxe4 f5 Bd3'),
        ('rr-odd-h6e6', 'Carr Defense, then small e-pawn move', 'e4 h6 d4 e6 Nf3 a6 Nc3 Bb4 Bd3 Bxc3+ bxc3 b5 O-O'),
        ('rr-odd-a5e6', 'Ware Defense, then small e-pawn move', 'e4 a5 d4 e6 Nf3 d5 Nc3 Bb4 Bd3 Bxc3+ bxc3 dxe4 Bxe4 Nf6 Bd3'),
        ('rr-odd-h5e6', 'Goldsmith Defense, then small e-pawn move', 'e4 h5 d4 e6 Nf3 d5 Nc3 Bb4 Bd3 Bxc3+ bxc3 dxe4 Bxe4 Nf6 Bd3')],
  why='Edge pawns and the f-pawn on move one. Take the middle with both pawns; one of these loses at once to the queen.', outcome='Winning or close to it')

# ============================================================== notes
# the other side's moves that start a named line
n('e4 Na6', 'Lemming Defense')
n('e4 Nh6', 'Hippopotamus Defense')
n('e4 a5', 'Ware Defense')
n('e4 f5', 'Duras Gambit')
n('e4 f6', 'Barnes Defense')
n('e4 g5', 'Borg Defense')
n('e4 h5', 'Goldsmith Defense')
n('e4 h6', 'Carr Defense')
n('e4 e5 Nf3 Qe7', 'Gunderam Defense')
n('e4 e5 Nf3 c6', 'Gunderam Gambit')
n('e4 g5 d4 Bg7', 'Borg Gambit')
