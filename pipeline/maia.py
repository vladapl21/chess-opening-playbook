"""Minimal numpy inference for Maia (lc0-format SE-ResNet) policy heads.

Gives the probability that a human at a given rating plays each legal move.
Weights: CSSLab/maia-chess (maia-XXXX.pb.gz). Policy index: lczero-training.
"""
import gzip, struct, sys, functools
import numpy as np
import paths
from common import *  # noqa  (python-chess on path)
import chess

sys.path.insert(0, str(paths.LCZERO_TF))
from policy_index import policy_index  # 1858 uci moves, white's point of view
POLICY_IDX = {m: i for i, m in enumerate(policy_index)}
assert len(policy_index) == 1858

# ---------------------------------------------------------------- protobuf wire decoding
def _varint(b, i):
    r = s = 0
    while True:
        c = b[i]; i += 1
        r |= (c & 0x7F) << s; s += 7
        if c < 0x80: return r, i

def fields(b):
    """Yield (field_number, wire_type, value) for a serialized message."""
    i, n = 0, len(b)
    while i < n:
        key, i = _varint(b, i)
        f, wt = key >> 3, key & 7
        if wt == 0: v, i = _varint(b, i)
        elif wt == 1: v = b[i:i+8]; i += 8
        elif wt == 2:
            ln, i = _varint(b, i); v = b[i:i+ln]; i += ln
        elif wt == 5: v = b[i:i+4]; i += 4
        else: raise ValueError(f'wire type {wt}')
        yield f, wt, v

def msg(b):
    d = {}
    for f, wt, v in fields(b): d.setdefault(f, []).append(v)
    return d

def layer(b):
    if b is None: return None
    d = msg(b)
    mn = struct.unpack('<f', d[1][0])[0] if 1 in d else 0.0
    mx = struct.unpack('<f', d[2][0])[0] if 2 in d else 0.0
    raw = d.get(3, [b''])[0]
    enc = d.get(4, [1])[0]
    if not raw: return np.zeros(0, np.float32)
    if enc in (0, 1):  # LINEAR16
        q = np.frombuffer(raw, dtype='<u2').astype(np.float32)
        return (mn + (mx - mn) * q / 65535.0).astype(np.float32)
    if enc == 2: return np.frombuffer(raw, dtype='<f2').astype(np.float32)
    raise ValueError(f'encoding {enc}')

def first(d, f): return d[f][0] if f in d else None

def convblock(b, kernel):
    d = msg(b)
    w = layer(first(d, 1)); bias = layer(first(d, 2))
    means = layer(first(d, 3)); var = layer(first(d, 4))
    gam = layer(first(d, 5)); bet = layer(first(d, 6))
    out = len(means) if means is not None and len(means) else len(bias)
    if bias is None or len(bias) == 0: bias = np.zeros(out, np.float32)
    w = w.reshape(out, -1, kernel, kernel).copy()
    if means is not None and len(means):
        if gam is None or len(gam) == 0: gam = np.ones(out, np.float32)
        if bet is None or len(bet) == 0: bet = np.zeros(out, np.float32)
        g = gam / np.sqrt(var + 1e-5)
        m = means - bias
        w *= g[:, None, None, None]
        bias = -g * m + bet
    return w.astype(np.float32), bias.astype(np.float32)

class Maia:
    def __init__(self, path):
        net = msg(gzip.open(path).read())
        fmt = msg(net[4][0]); nf = msg(fmt[2][0]) if 2 in fmt else {}
        self.fmt = {k: v[0] for k, v in nf.items() if isinstance(v[0], int)}
        W = msg(net[10][0])
        self.inp = convblock(W[1][0], 3)
        self.res = []
        for rb in W.get(2, []):
            r = msg(rb)
            c1 = convblock(r[1][0], 3); c2 = convblock(r[2][0], 3)
            se = None
            if 3 in r:
                s = msg(r[3][0])
                C = c1[0].shape[0]
                w1 = layer(s[1][0]); b1 = layer(s[2][0]); w2 = layer(s[3][0]); b2 = layer(s[4][0])
                se = (w1.reshape(len(b1), C), b1, w2.reshape(len(b2), len(b1)), b2)
            self.res.append((c1, c2, se))
        self.policy_format = self.fmt.get(4, 1)
        if self.policy_format == 2:   # convolutional policy
            self.pol1 = convblock(W[11][0], 3)
            pw = msg(W[3][0])
            w = layer(pw[1][0]); b = layer(pw[2][0])
            self.pol = (w.reshape(len(b), -1, 3, 3), b)
            sys.path.insert(0, str(paths.LCZERO_TF))
            from lc0_az_policy_map import make_map
            self.polmap = make_map()  # (80*64) x 1858
        else:
            self.pol = convblock(W[3][0], 1)
            self.ip_w = layer(W[4][0]); self.ip_b = layer(W[5][0])
            self.ip_w = self.ip_w.reshape(len(self.ip_b), -1)
        self.C = self.inp[0].shape[0]

    @staticmethod
    def conv(x, wb, relu=True):
        w, b = wb
        k = w.shape[2]
        if k == 1:
            y = np.einsum('oi,ihw->ohw', w[:, :, 0, 0], x)
        else:
            p = np.pad(x, ((0, 0), (1, 1), (1, 1)))
            # im2col
            cols = np.stack([p[:, dy:dy+8, dx:dx+8] for dy in range(3) for dx in range(3)], axis=1)  # i,9,8,8
            y = np.einsum('oik,ikhw->ohw', w.reshape(w.shape[0], w.shape[1], 9), cols)
        y = y + b[:, None, None]
        return np.maximum(y, 0) if relu else y

    def forward(self, planes):
        x = self.conv(planes, self.inp)
        for c1, c2, se in self.res:
            y = self.conv(x, c1)
            y = self.conv(y, c2, relu=False)
            if se is not None:
                w1, b1, w2, b2 = se
                pool = y.mean(axis=(1, 2))
                h = np.maximum(w1 @ pool + b1, 0)
                z = w2 @ h + b2
                C = y.shape[0]
                g = 1 / (1 + np.exp(-z[:C])); beta = z[C:]
                y = g[:, None, None] * y + beta[:, None, None]
            x = np.maximum(y + x, 0)
        if self.policy_format == 2:
            p = self.conv(x, self.pol1)
            p = self.conv(p, self.pol, relu=False)
            flat = p.reshape(-1)
            return flat @ self.polmap
        p = self.conv(x, self.pol)
        return self.ip_w @ p.reshape(-1) + self.ip_b

def encode(board):
    """112 input planes for INPUT_CLASSICAL_112_PLANE from a python-chess board with move stack."""
    planes = np.zeros((112, 8, 8), np.float32)
    us = board.turn
    flip = us == chess.BLACK
    hist = [board.copy()]
    b = board.copy()
    while len(hist) < 8 and b.move_stack:
        b.pop(); hist.append(b.copy())
    def put(plane, sq):
        if flip: sq = chess.square_mirror(sq)
        planes[plane, sq // 8, sq % 8] = 1
    order = [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING]
    for i, pos in enumerate(hist):
        base = i * 13
        for k, pt in enumerate(order):
            for sq in pos.pieces(pt, us): put(base + k, sq)
            for sq in pos.pieces(pt, not us): put(base + 6 + k, sq)
    if board.has_queenside_castling_rights(us): planes[104] = 1
    if board.has_kingside_castling_rights(us): planes[105] = 1
    if board.has_queenside_castling_rights(not us): planes[106] = 1
    if board.has_kingside_castling_rights(not us): planes[107] = 1
    if us == chess.BLACK: planes[108] = 1
    planes[109] = board.halfmove_clock
    planes[111] = 1
    return planes

def nn_uci(board, move):
    m = move
    if board.is_castling(m):
        # lc0 encodes castling as king-takes-own-rook
        rank = chess.square_rank(m.from_square)
        to = chess.square(7 if chess.square_file(m.to_square) > 4 else 0, rank)
        m = chess.Move(m.from_square, to)
    fr, to = m.from_square, m.to_square
    if board.turn == chess.BLACK:
        fr, to = chess.square_mirror(fr), chess.square_mirror(to)
    u = chess.square_name(fr) + chess.square_name(to)
    if m.promotion and m.promotion != chess.QUEEN:
        u += chess.piece_symbol(m.promotion)
    return u

@functools.lru_cache(maxsize=None)
def model(level):
    return Maia(str(paths.MAIA_WEIGHTS / f'maia-{level}.pb.gz'))

def policy(board, level=1300):
    logits = model(level).forward(encode(board))
    moves = list(board.legal_moves)
    idx = [POLICY_IDX[nn_uci(board, m)] for m in moves]
    l = np.array([logits[i] for i in idx], np.float64)
    p = np.exp(l - l.max()); p /= p.sum()
    return sorted(((board.san(m), float(pp), m.uci()) for m, pp in zip(moves, p)), key=lambda x: -x[1])

def blended(board, levels=(1300, 1500)):
    acc = {}
    for lv in levels:
        for san, p, u in policy(board, lv):
            a = acc.setdefault(san, [0.0, u]); a[0] += p / len(levels)
    return sorted(((s, v[0], v[1]) for s, v in acc.items()), key=lambda x: -x[1])

if __name__ == '__main__':
    m = model(1100)
    print('format', m.fmt, 'blocks', len(m.res), 'filters', m.C, 'policy fmt', m.policy_format,
          'se', m.res[0][2][0].shape if m.res[0][2] else None)
    for seq in ['', 'e4', 'e4 e5 Nf3', 'e4 c5', 'e4 e5 Nf3 Nc6 Bc4', 'e4 c6 d4 d5 Nc3 dxe4 Nxe4', 'd4']:
        b = chess.Board()
        for s in seq.split(): b.push_san(s)
        top = policy(b, 1100)[:6]
        print(f'{seq or "start":40s}', '  '.join(f'{s} {p:.2f}' for s, p, _ in top))
