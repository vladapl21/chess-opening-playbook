"""Plans for the end of every book line, not only the main lines.

A main line keeps its lesson's hand-written plan (content/plans.py W and B). A side line gets, in this order:
  1. its own hand-written plan (content/plans.py LW and LB, keyed by line id);
  2. the plan of a main line that ends on the same position;
  3. a plan read off the board and the engine's line from there (data/cache/plan_cache.json, pipeline/plan_pv.py).
Lines that end in mate have none.

The read-off plans use the same kinds and the same voice as the written ones. Every bullet states something the board or
the engine's line shows: a move the engine plays next (put in words, never in notation), a piece still at home, a king
that can't castle, a pawn with no neighbour, the material. Nothing is said that the position does not back up.
Written to data/line_plans.json, which assemble.py attaches to the lines.
"""
import json
from common import *
import paths
from plans import W as PLAN_W, B as PLAN_B, LW, LB

OUT = paths.DATA / 'line_plans.json'
CACHE = paths.CACHE / 'plan_cache.json'
PN = {chess.PAWN: 'pawn', chess.KNIGHT: 'knight', chess.BISHOP: 'bishop', chess.ROOK: 'rook', chess.QUEEN: 'queen', chess.KING: 'king'}
VAL = {chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3, chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 0}
NUM = {1: 'a', 2: 'two', 3: 'three', 4: 'four'}
CENTER = [chess.D4, chess.E4, chess.D5, chess.E5]
LONG = {chess.square(i, i) for i in range(8)} | {chess.square(i, 7 - i) for i in range(8)}


def cap(s): return s[:1].upper() + s[1:]


def join(xs):
    xs = [x for x in xs if x]
    return xs[0] if len(xs) == 1 else ', '.join(xs[:-1]) + ' and ' + xs[-1]


class Pos:
    """The end of a line, seen from the player's side (me)."""

    def __init__(self, b, me, pv, score):
        self.b, self.me, self.them = b, me, not me
        self.opp = 'Black' if me == chess.WHITE else 'White'
        self.pv = pv
        # the engine's number turned to the player's side: ('cp', n) or ('mate', n), n > 0 good for the player
        if isinstance(score, str):
            n = int(score[1:]); self.score = ('mate', n if me == chess.WHITE else -n)
        else:
            self.score = ('cp', score if me == chess.WHITE else -score)

    # ------------------------------------------------------------------ names
    def pname(self, b, sq):
        """What a piece is called: "dark bishop", "queen's knight" (only at home), "d-pawn"."""
        p = b.piece_at(sq); t = p.piece_type
        if t == chess.PAWN: return chess.FILE_NAMES[chess.square_file(sq)] + '-pawn'
        if t == chess.BISHOP: return ('light' if chess.BB_SQUARES[sq] & chess.BB_LIGHT_SQUARES else 'dark') + ' bishop'
        return PN[t]

    def whose(self, color, name):
        return f'your {name}' if color == self.me else f"{self.opp}'s {name}"

    def home_minors(self, color):
        r = 0 if color == chess.WHITE else 7
        out = []
        for f, t, nm in ((1, chess.KNIGHT, "queen's knight"), (6, chess.KNIGHT, "king's knight"), (2, chess.BISHOP, None), (5, chess.BISHOP, None)):
            sq = chess.square(f, r); p = self.b.piece_at(sq)
            if p and p.color == color and p.piece_type == t:
                out.append(nm or self.pname(self.b, sq))
        return out

    # ------------------------------------------------------------------ material
    def counts(self, color):
        return {t: len(self.b.pieces(t, color)) for t in VAL}

    def material(self):
        """The material balance in words from the player's side, or None when it is level."""
        a, z = self.counts(self.me), self.counts(self.them)
        d = {t: a[t] - z[t] for t in VAL}
        minors = d[chess.KNIGHT] + d[chess.BISHOP]; p = d[chess.PAWN]
        pawns = lambda n: f"{NUM.get(abs(n), str(abs(n)))} pawn{'s' if abs(n) > 1 else ''}"
        if not d[chess.QUEEN] and not d[chess.ROOK] and not minors:
            if not p: return None
            return f'{pawns(p)} {"up" if p > 0 else "down"}'
        if not d[chess.QUEEN] and not d[chess.ROOK] and abs(minors) == 1:
            up = minors > 0
            if (p < 0) == up and abs(p) >= 1:
                return f'a piece for {pawns(p)}' if up else f'{pawns(p)} for a piece'
            return 'a piece up' if up else 'a piece down'
        if not d[chess.QUEEN] and d[chess.ROOK] == 1 and minors == -1: return 'the exchange up'
        if not d[chess.QUEEN] and d[chess.ROOK] == -1 and minors == 1: return 'the exchange down'
        if not d[chess.QUEEN] and abs(d[chess.ROOK]) == 1 and not minors: return 'a rook up' if d[chess.ROOK] > 0 else 'a rook down'
        if not d[chess.QUEEN] and not d[chess.ROOK] and abs(minors) == 2: return 'two pieces up' if minors > 0 else 'two pieces down'
        tot = sum(VAL[t] * d[t] for t in VAL)
        if tot >= 2: return 'ahead in material'
        if tot <= -2: return 'behind in material'
        return None

    def mat_diff(self):
        a, z = self.counts(self.me), self.counts(self.them)
        return sum(VAL[t] * (a[t] - z[t]) for t in VAL)

    # ------------------------------------------------------------------ kings
    def king_state(self, color):
        k = self.b.king(color); r = 0 if color == chess.WHITE else 7
        if chess.square_rank(k) == r and chess.square_file(k) >= 6: return 'short'
        if chess.square_rank(k) == r and chess.square_file(k) <= 2: return 'long'
        if k == chess.square(4, r):
            ks, qs = self.b.has_kingside_castling_rights(color), self.b.has_queenside_castling_rights(color)
            return 'home' if ks or qs else 'stuck'
        return 'moved'

    def file_kind(self, f, color):
        """'open' (no pawns), 'half' (none of color's pawns) or None."""
        mine = any(chess.square_file(s) == f for s in self.b.pieces(chess.PAWN, color))
        theirs = any(chess.square_file(s) == f for s in self.b.pieces(chess.PAWN, not color))
        return 'open' if not mine and not theirs else 'half' if not mine else None

    # ------------------------------------------------------------------ one move in words
    def hit(self, after, sq, color):
        """The best enemy piece the piece on sq now attacks that is worth more than it or has no guard."""
        me_p = after.piece_at(sq); best = None
        for t in after.attacks(sq):
            q = after.piece_at(t)
            if not q or q.color == color or q.piece_type == chess.KING: continue
            loose = not after.attackers(q.color, t)
            if VAL[q.piece_type] > VAL[me_p.piece_type] or (loose and q.piece_type != chess.PAWN):
                if not best or VAL[q.piece_type] > VAL[after.piece_at(best).piece_type]: best = t
        return best

    def trade(self, b, sq, tgt):
        """The plural name when the piece on sq and the one on tgt are the same kind (a trade on offer), else None."""
        a, z = b.piece_at(sq), b.piece_at(tgt)
        if a.piece_type != z.piece_type or a.piece_type == chess.PAWN: return None
        if a.piece_type == chess.BISHOP and self.pname(b, sq) != self.pname(b, tgt): return None
        return self.pname(b, sq) + 's'

    def move(self, b, mv, prev):
        """(verb phrase, kind) for a move, from the mover's side: "castle short", "push the d-pawn at your knight"."""
        p = b.piece_at(mv.from_square); t = p.piece_type; c = p.color
        after = b.copy(); after.push(mv)
        nm = self.pname(b, mv.from_square)
        if b.is_castling(mv):
            return ('castle short' if chess.square_file(mv.to_square) > 4 else 'castle long'), 'castle'
        if b.is_capture(mv):
            vname = 'pawn' if b.is_en_passant(mv) else self.pname(b, mv.to_square)
            if prev is not None and prev.to_square == mv.to_square and b.move_stack and b.peek() == prev and self.was_capture(b, prev):
                return ('take back' + ('' if t == chess.PAWN else f' with the {PN[t]}')), 'retake'
            with_ = '' if t == chess.PAWN else f' with the {PN[t]}'
            return f'take {self.whose(not c, vname)}{with_}', 'capture'
        if after.is_check():
            return (f'check with the {PN[t]}' if t != chess.PAWN else 'check with a pawn'), 'check'
        tgt = self.hit(after, mv.to_square, c)
        if t == chess.PAWN:
            s = f'push the {nm}'
            if tgt is not None: return f'{s} at {self.whose(not c, self.pname(after, tgt))}', 'pawn'
            lever = [x for x in after.attacks(mv.to_square) if after.piece_at(x) and after.piece_at(x).color != c]
            if lever: return f'{s} to hit {self.whose(not c, self.pname(after, lever[0]))}', 'pawn'
            steps = abs(chess.square_rank(mv.to_square) - chess.square_rank(mv.from_square))
            central = 2 <= chess.square_file(mv.from_square) <= 5
            return s + (' two squares' if steps == 2 else ' one square'), ('pawn' if central else 'pawn-weak')
        r0 = 0 if c == chess.WHITE else 7
        fr, tr = chess.square_rank(mv.from_square), chess.square_rank(mv.to_square)
        tr_ = self.trade(after, mv.to_square, tgt) if tgt is not None else None
        if t in (chess.KNIGHT, chess.BISHOP) and fr == r0:
            who = ("queen's knight" if chess.square_file(mv.from_square) < 4 else "king's knight") if t == chess.KNIGHT else nm
            s = f'bring the {who} out'
            if tr_: s += f' to offer a trade of {tr_}'
            elif tgt is not None: s += f' at {self.whose(not c, self.pname(after, tgt))}'
            return s, 'develop'
        if tr_:
            return f'offer a trade of {tr_}', 'trade'
        if tgt is not None and t == chess.KING:
            return f'step the king up to hit {self.whose(not c, self.pname(after, tgt))}', 'king'
        if tgt is not None:
            return f'hit {self.whose(not c, self.pname(after, tgt))} with the {nm}', 'attack'
        back = tr < fr if c == chess.WHITE else tr > fr
        if t == chess.ROOK:
            k = self.file_kind(chess.square_file(mv.to_square), c)
            f = chess.FILE_NAMES[chess.square_file(mv.to_square)]
            if chess.square_file(mv.to_square) != chess.square_file(mv.from_square) and k:
                return f'put a rook on the {"open" if k == "open" else "half-open"} {f}-file', 'rook'
            return f'bring a rook to the {f}-file', 'rook'
        if t == chess.QUEEN:
            if fr == r0 and not back: return 'bring the queen out', 'queen'
            return ('pull the queen back' if back else 'move the queen up'), 'queen-weak'
        if t == chess.KING:
            return 'step the king aside', 'king'
        if back: return f'pull the {nm} back', 'retreat'
        if t == chess.KNIGHT and mv.to_square in CENTER: return 'jump the knight to the center', 'center'
        if t == chess.BISHOP and mv.to_square in LONG:
            return 'put the bishop on the long diagonal', 'diag'
        return f'bring the {nm} forward' if t == chess.KNIGHT else f'move the {nm}', 'weak'

    @staticmethod
    def was_capture(b, prev):
        x = b.copy(); x.pop(); return x.is_capture(prev)

    def line(self):
        """The engine's line split by side: [(phrase, kind, move, board before)] for the player and for the opponent."""
        b = self.b.copy(); mine, theirs = [], []; prev = b.peek() if b.move_stack else None
        for mv in self.pv[:8]:
            if mv not in b.legal_moves: break
            ph, kind = self.move(b, mv, prev)
            (mine if b.turn == self.me else theirs).append((ph, kind, mv, b.copy()))
            prev = mv; b.push(mv)
        return mine, theirs

    # ------------------------------------------------------------------ structure
    def isolated(self, color):
        fs = [chess.square_file(s) for s in self.b.pieces(chess.PAWN, color)]
        return sorted({f for f in fs if f - 1 not in fs and f + 1 not in fs})

    def doubled(self, color):
        fs = [chess.square_file(s) for s in self.b.pieces(chess.PAWN, color)]
        return sorted({f for f in fs if fs.count(f) > 1})

    def passed(self, color):
        out = []
        for s in self.b.pieces(chess.PAWN, color):
            f, r = chess.square_file(s), chess.square_rank(s)
            ahead = [x for x in self.b.pieces(chess.PAWN, not color) if abs(chess.square_file(x) - f) <= 1 and
                     ((chess.square_rank(x) > r) if color == chess.WHITE else (chess.square_rank(x) < r))]
            if not ahead: out.append(s)
        return out

    def loose(self, color):
        """color's pieces (not pawns or the king) that the other side attacks and nothing guards."""
        out = []
        for s, p in self.b.piece_map().items():
            if p.color != color or p.piece_type in (chess.PAWN, chess.KING): continue
            if self.b.attackers(not color, s) and not self.b.attackers(color, s): out.append(s)
        return out


def say_all(phrases):
    """Join verb phrases, folding repeats: "bring the knight out" + "bring the bishop out" -> "bring the knight and the
    bishop out"."""
    out = []
    for ph in phrases:
        if ph in out: continue
        if out and out[-1].startswith('bring the ') and out[-1].endswith(' out') and ph.startswith('bring the ') and ph.endswith(' out'):
            out[-1] = out[-1][:-4] + ' and ' + ph[6:]
        else: out.append(ph)
    return join(out)


def minors_words(home):
    """The subject of "... still at home": "Your queen's knight and both bishops are", "Both your bishops are"."""
    if len(home) == 4: return 'Your knights and bishops are all'
    bs = [x for x in home if x.endswith('bishop')]; ns = [x for x in home if x.endswith('knight')]
    if len(home) == 2 and len(bs) == 2: return 'Both your bishops are'
    if len(home) == 2 and len(ns) == 2: return 'Both your knights are'
    if len(ns) == 2: return f'Both your knights and your {bs[0]} are'
    parts = (['both knights'] if len(ns) == 2 else ns) + (['both bishops'] if len(bs) == 2 else bs)
    return 'Your ' + join(parts) + (' is' if len(home) == 1 else ' are')


def what_out(ph):
    """'bring the light bishop out at your knight' -> 'light bishop'."""
    x = ph[len('bring the '):]
    for cut in (' to offer', ' at ', ' out'):
        x = x.split(cut)[0]
    return x


def plan_for(pos):
    """A plan dict (h, b) for one position, or None when there is nothing honest to say."""
    b, me, them, opp = pos.b, pos.me, pos.them, pos.opp
    mine, theirs = pos.line()
    mine_x = [m for m in mine if m[1] != 'retake']
    weak = ('weak', 'queen-weak', 'pawn-weak', 'retake', 'king')
    bullets = []
    mat = pos.material()
    kind, n = pos.score

    # a forced mate on the board
    if kind == 'mate' and 0 < n <= 5 and mine:
        h = 'Mate in ' + ['one', 'two', 'three', 'four', 'five'][n - 1]
        return dict(h=h, b=[('target', f"{opp}'s king is caught: there is a forced mate. First move: {mine[0][0]}."),
                            ('them', f'{opp} can only delay it.')])

    ks_me, ks_them = pos.king_state(me), pos.king_state(them)
    castle_at = next((k for k, m in enumerate(mine_x[:3]) if m[1] == 'castle'), None)
    home = pos.home_minors(me)

    # king: yours
    if ks_me == 'home' and castle_at is not None:
        side = mine_x[castle_at][0].split()[-1]
        if castle_at == 0: bullets.append(('king', f'Castle {side} next.'))
        elif mine_x[0][1] == 'develop': bullets.append(('king', f'Castle {side} once the {what_out(mine_x[0][0])} is out.'))
        else: bullets.append(('king', f'Castle {side} soon.'))
    elif ks_me in ('stuck', 'moved'):
        q = bool(b.pieces(chess.QUEEN, them))
        bullets.append(('king', "Your king can't castle any more." + (' Keep it covered and keep the middle closed.' if q else ' With the queens off, it is safe enough in the middle.')))

    # their king
    if ks_them in ('stuck', 'moved'):
        f = chess.square_file(b.king(them))
        tail = f' The {chess.FILE_NAMES[f]}-file in front of it is open.' if pos.file_kind(f, me) == 'open' else ''
        bullets.append(('target', f"{opp}'s king can't castle any more.{tail} Bring your pieces at it."))
    elif ks_them == 'home' and not any(m[1] == 'castle' for m in theirs[:2]):
        e, d = pos.file_kind(4, me), pos.file_kind(3, me)
        if e == 'open' or d == 'open':
            f = 'e' if e == 'open' else 'd'
            bullets.append(('target', f"{opp}'s king is still in the middle, on the open {f}-file. Get a rook there before it castles."))

    # pieces still at home, else the engine's next piece move
    if home:
        first = mine_x[0][1] if mine_x else None
        it = 'it' if len(home) == 1 else 'them'
        when = 'next' if first == 'develop' else 'soon' if first in ('castle', 'pawn', 'capture', 'check', 'retake') else 'next'
        bullets.append(('pieces', f"{minors_words(home)} still at home. " +
                        (f'Bring {it} out {when}.' if len(home) <= 2 or first not in ('develop', None) else 'Bring them out before anything else.')))
    else:
        good = [m for m in mine_x[:3] if m[1] in ('rook', 'attack', 'center', 'diag', 'develop', 'queen', 'trade', 'capture', 'check')] or \
               [m for m in mine_x[:2] if m[1] == 'retreat']
        if good:
            ph = good[0][0]
            bullets.append(('pieces', f'{cap(ph)} next.' if good[0] is mine_x[0] else f'Then {ph}.'))

    # pawns: the material first, then the engine's pawn move, then a passed pawn
    md = pos.mat_diff()
    if mat and md >= 1:
        what = 'pawn' if mat.endswith('pawn up') else 'pawns' if mat.endswith('pawns up') else None
        bullets.append(('pawns', f'Trade pieces, not pawns: your extra {what} counts for more with every trade.' if what else
                        'Trade pieces when you can: every trade makes your extra material count for more.'))
    elif mat and md <= -1 and kind == 'cp' and n >= -60:
        bullets.append(('pawns', 'Keep the pieces on: your active pieces make up for the material while they are on the board.'))
    else:
        pm = next((m for m in mine_x[:3] if m[1] == 'pawn'), None)
        if pm:
            bullets.append(('pawns', f'{cap(pm[0])} next.' if pm is mine_x[0] else f'Then {pm[0]}.'))
        else:
            pp = [s for s in pos.passed(me) if (chess.square_rank(s) >= 4 if me == chess.WHITE else chess.square_rank(s) <= 3)]
            if pp:
                f = chess.FILE_NAMES[chess.square_file(pp[0])]
                bullets.append(('pawns', f"Your {f}-pawn is passed: no {opp} pawn can stop it. Push it when it is guarded."))

    # a target in the other side's pawns or pieces
    if not any(k == 'target' for k, _ in bullets):
        iso = [f for f in pos.isolated(them) if 2 <= f <= 5]
        dbl = pos.doubled(them)
        f7 = chess.F7 if me == chess.WHITE else chess.F2
        att = b.attackers(me, f7); dfn = b.attackers(them, f7)
        if len(att) >= 2 and len(dfn) == 1 and b.piece_at(next(iter(dfn))).piece_type == chess.KING and b.piece_at(f7):
            sqn = 'f7' if me == chess.WHITE else 'f2'
            bullets.append(('target', f'{sqn}: only the king guards it, and {NUM.get(len(att), str(len(att)))} of your pieces aim at it.'))
        elif iso:
            bullets.append(('target', f"{opp}'s {chess.FILE_NAMES[iso[0]]}-pawn has no pawn beside it: only pieces can guard it."))
        elif dbl:
            bullets.append(('target', f"{opp}'s pawns are doubled on the {chess.FILE_NAMES[dbl[0]]}-file."))

    # what the other side wants: its next two moves in the engine's line
    ph = [m[0] for m in theirs[:2] if m[1] not in weak]
    if len(theirs) >= 2 and all(m[1] in ('pawn', 'pawn-weak') for m in theirs[:2]):
        ph = [m[0] for m in theirs[:2]]      # two pawn moves in a row are a plan of their own (the a-pawn, then the b-pawn)
    if ph: bullets.append(('them', f'{opp} wants to {say_all(ph)}.'))

    # keep it short: at most four, the other side's plan always in when there is one
    order = {'king': 0, 'target': 1, 'pieces': 2, 'pawns': 3, 'them': 4, 'watch': 5}
    th = [x for x in bullets if x[0] == 'them']
    rest = sorted([x for x in bullets if x[0] != 'them'], key=lambda x: order[x[0]])
    bullets = rest[:4 - len(th[:1])] + th[:1]
    # "Then ..." needs a bullet before it that says what comes first; without one it becomes "... soon"
    first_said = False; fixed = []
    for k, t in bullets:
        if t.startswith('Then ') and not first_said: t = cap(t[5:-1]) + ' soon.'
        if t.endswith(' next.') or ' next. ' in t or t.startswith('Then '): first_said = True
        fixed.append((k, t))
    bullets = fixed
    if len(bullets) < 2:
        nxt = [m[0] for m in mine_x[:2] if m[1] not in weak]
        if nxt and not any(k in ('pieces', 'pawns') for k, _ in bullets):
            bullets.insert(0, ('pieces', f'Next: {say_all(nxt)}.'))
    if len(bullets) < 2: return None

    # the headline: the material (or the engine's verdict), then the first two things to do, in the engine's order
    acts = []
    def add(a):
        if a and a not in acts: acts.append(a)
    if any(k == 'target' and "can't castle" in t for k, t in bullets): add('go after the king')
    for m in mine_x[:3]:
        if m[1] == 'castle': add('castle')
        elif m[1] == 'develop' and home: add('finish your setup')
        elif m[1] in ('trade', 'capture', 'attack', 'center', 'diag', 'check'): add(m[0])
        elif m[1] == 'pawn': add(m[0].split(' at ')[0].split(' to hit ')[0].replace(' two squares', '').replace(' one square', ''))
        elif m[1] == 'rook': add('take the open file' if ' open ' in m[0] else 'bring a rook in')
    if home: add('finish your setup')
    if mat and md >= 1: add('trade pieces')
    if mat and md <= -1 and kind == 'cp' and n >= -60: add('keep the pieces on')
    def head(act):
        if mat: return cap(mat) + (': ' + ' and '.join(act) if act else '')
        if kind == 'cp' and n >= 150: return 'Better for you' + (': ' + ', then '.join(act) if act else '')
        return cap(', then '.join(act)) if act else None
    if not acts: acts = [m[0] for m in mine_x[:2] if m[1] not in weak]
    h = head(acts[:2])
    if h and len(h) > 60: h = head(acts[:1])      # a headline is read at a glance: one thing to do when two run long
    if not h: return None
    return dict(h=h, b=bullets)


def main_plans(D, P):
    """Main-line end position -> lesson id, for the lessons that have a written plan."""
    out = {}
    for l in D['lines']:
        if l['main'] and l['lesson'] in P:
            out.setdefault(D['nodes'][l['n'][-1]]['f'], l['lesson'])
    return out


def build():
    import plan_pv
    cache = plan_pv.run()          # the engine runs only for line ends that are not in the cache yet
    out = {}; stats = {}
    for s, P, L, me in (('white', PLAN_W, LW, chess.WHITE), ('black', PLAN_B, LB, chess.BLACK)):
        D = json.load(open(paths.BUILD / f'data_{s}.json'))
        N = D['nodes']; ends = main_plans(D, P); les = {x['id']: x for x in D['lessons']}
        st = dict(written=0, same=0, read=0, none=0, mate=0, missing=0)
        assert set(L) <= {l['id'] for l in D['lines']}, sorted(set(L) - {l['id'] for l in D['lines']})
        for l in D['lines']:
            if l['main'] and l['lesson'] in P: continue
            if l['id'] in L:
                out[l['id']] = dict(L[l['id']]); st['written'] += 1; continue
            b = chess.Board()
            for i in l['n'][1:]: b.push(chess.Move.from_uci(N[i]['u']))
            if b.is_game_over(): st['mate'] += 1; continue
            f = N[l['n'][-1]]['f']
            if f in ends:
                out[l['id']] = dict(same=ends[f]); st['same'] += 1; continue
            c = cache.get(b.fen())
            if not c: st['missing'] += 1; continue
            p = plan_for(Pos(b, me, [chess.Move.from_uci(u) for u in c['pv']], c['s']))
            if p: out[l['id']] = dict(p, gen=1); st['read'] += 1
            else: st['none'] += 1
        stats[s] = st
    return out, stats


if __name__ == '__main__':
    out, stats = build()
    print(stats)
    text = json.dumps(out, sort_keys=True, indent=0, ensure_ascii=False) + '\n'
    if not OUT.exists() or OUT.read_text() != text: OUT.write_text(text)
