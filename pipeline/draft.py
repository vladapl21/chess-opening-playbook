"""Draft the lines of a system. An authoring aid, not part of the build: its output is pasted into a content module and
edited by hand (titles, notes, the order of the lessons).

walk() follows the other side's human replies (the Maia odds of pipeline/expand.py) and picks your side's move at every
turn, in this order:
  1. a move fixed by hand for that exact path (`fixed`),
  2. the move already chosen from the same position (one position, one move), in this walk or in `known`,
  3. the first move of the system's order (`system(board, path)` gives the candidates, best first) that the engine
     accepts: within `tol` centipawns of its best move,
  4. the engine's best move.
Every line ends on your move. emit() groups the leaves into lessons by their roots and writes the L(...) entries, each
side line titled after the move where it leaves the lesson's main line (its opening name when it has one).
"""
import json, re
from common import *
import paths, expand as X, names
from label2 import label as auto_label

CACHE = paths.CACHE / 'draft_cache.json'
_c = json.load(open(CACHE)) if CACHE.exists() else {}
_eng = None


def save():
    json.dump(_c, open(CACHE, 'w'), sort_keys=True); X.save()


def engine():
    global _eng
    if _eng is None:
        _eng = chess.engine.SimpleEngine.popen_uci(SF); _eng.configure({'Threads': 2, 'Hash': 256})
    return _eng


def done():
    global _eng
    if _eng is not None: _eng.quit(); _eng = None
    save()


def board_of(path):
    b = chess.Board()
    for s in path.split(): b.push_san(s)
    return b


def cp(score, turn):
    s = score.pov(turn)
    return (10000 - abs(s.mate()) * 10) * (1 if s.mate() > 0 else -1) if s.is_mate() else s.score()


def best(b, depth=15, n=3):
    """[(san, centipawns for the side to move)] for the engine's n best moves."""
    k = f'{b.fen()}|b|{depth}|{n}'
    if k not in _c:
        inf = engine().analyse(b, chess.engine.Limit(depth=depth), multipv=n)
        _c[k] = [(b.san(i['pv'][0]), cp(i['score'], b.turn)) for i in inf if i.get('pv')]
    return _c[k]


def value(b, san, depth=15):
    """Centipawns for the side to move after playing san."""
    for s, v in best(b, depth):
        if s == san: return v
    k = f'{b.fen()}|v|{depth}|{san}'
    if k not in _c:
        inf = engine().analyse(b, chess.engine.Limit(depth=depth), root_moves=[b.parse_san(san)])
        _c[k] = cp(inf['score'], b.turn)
    return _c[k]


class Walk:
    def __init__(self, me, system=None, fixed=None, known=None, tol=45, thr=0.1, min_reach=0.004, depth=lambda reach: 16, win=350, eng_depth=15):
        self.me = chess.WHITE if me == 'w' else chess.BLACK
        self.system, self.fixed, self.seen = system or (lambda b, p: []), {' '.join(k.split()): v for k, v in (fixed or {}).items()}, dict(known or {})
        self.tol, self.thr, self.min_reach, self.depth, self.win, self.ed = tol, thr, min_reach, depth, win, eng_depth
        self.leaves, self.why, self.flags = [], {}, []

    def choose(self, path, b):
        if path in self.fixed: return self.fixed[path], 'fixed'
        e = b.epd()
        if e in self.seen and self.seen[e] in [b.san(m) for m in b.legal_moves]: return self.seen[e], 'same'
        top = best(b, self.ed)
        legal = {b.san(m) for m in b.legal_moves}
        for s in self.system(b, path):
            if s in legal and top[0][1] - value(b, s, self.ed) <= self.tol: return s, 'system'
        return top[0][0], 'engine'

    def go(self, path='', reach=1.0, extra=0):
        b = board_of(path); n = len(path.split())
        if b.is_game_over(): return
        if b.turn != self.me:
            hs = [(s, p) for s, p in X.human(path) if p >= self.thr and reach * p >= self.min_reach]
            for s, p in hs: self.go((path + ' ' + s).strip(), reach * p)
            return
        san, how = self.choose(path, b)
        self.seen[b.epd()] = san; self.why[(path + ' ' + san).strip()] = how
        v = value(b, san, self.ed); mv = b.parse_san(san); forcing = b.is_capture(mv) or b.gives_check(mv)
        new = (path + ' ' + san).strip(); a = b.copy(); a.push(mv)
        lim = self.depth(reach)
        over = a.is_game_over() or (v >= self.win and n + 1 >= 8 and not forcing) or (n + 1 >= lim and not (forcing and extra < 2)) or n + 1 >= lim + 4
        hs = [] if over else [(s, p) for s, p in X.human(new) if p >= self.thr and reach * p >= self.min_reach]
        if n + 1 >= lim and hs: hs = hs[:1]                     # past the limit only to finish an exchange: the likeliest reply
        if not hs:
            self.leaves.append(dict(path=new, reach=reach, v=v)); return
        for s, p in hs: self.go(new + ' ' + s, reach * p, extra + 1 if n + 1 >= lim else 0)

    def run(self, roots):
        """roots: [(path, reach)] to start from (your move or theirs)."""
        for path, reach in roots: self.go(' '.join(path.split()), reach)
        save()
        return self.leaves


GENERIC = re.compile(r'^(Normal|Main|Standard|Classical|Modern|Symmetrical|Exchange|Open|Closed|Declined|Accepted)( Variation| Line| Defense| System)?$|^with |, with ')


def move_title(b, mv, prev):
    """What a side line is called after the move where it leaves the main line: the opening it starts, or the move in words."""
    T = names.table(); a = b.copy(); a.push(mv)
    nm = T.get(a.epd()); before = T.get(b.epd())
    if nm and nm != before:
        tail = nm.split(': ')[-1].split(', ')[-1]
        if not GENERIC.search(tail) and len(tail) <= 34: return tail
    return auto_label(b, mv, prev, bool(prev and b.move_stack and _was_cap(b)))


def _was_cap(b):
    x = b.copy(); m = x.pop(); return x.is_capture(m)


def slug(san): return re.sub(r'[^a-z0-9]', '', san.lower().replace('o-o-o', 'ooo').replace('o-o', 'oo'))


def emit(leaves, lessons, me):
    """lessons: [dict(id, part, title, sub, pri, root, why, outcome)], most specific roots win. Returns the L(...) text
    and a list of (line id, title, path, reach) for a look."""
    mine = chess.WHITE if me == 'w' else chess.BLACK
    for L in lessons: L['root'] = ' '.join(L['root'].split()); L['leaves'] = []
    for lf in leaves:
        fits = [L for L in lessons if (lf['path'] + ' ').startswith(L['root'] + ' ') or not L['root']]
        assert fits, lf['path']
        max(fits, key=lambda L: len(L['root']))['leaves'].append(lf)
    out, table = [], []
    for L in lessons:
        ls = sorted(L['leaves'], key=lambda x: -x['reach'])
        if not ls: out.append(f"# !! no lines under {L['id']} ({L['root']})"); continue
        main = ls[0]; mt = main['path'].split(); used, alts = {}, []
        for lf in ls[1:]:
            t = lf['path'].split(); k = next(i for i in range(min(len(t), len(mt)) + 1) if i >= len(t) or i >= len(mt) or t[i] != mt[i])
            b = chess.Board(); prev = None
            for s in t[:k]: prev = b.parse_san(s); b.push(prev)
            if k >= len(t): continue                                  # a prefix of the main line: nothing of its own
            mv = b.parse_san(t[k]); title = move_title(b, mv, prev); sid = slug(t[k])
            # the same first move as another side line: name the next move of the other side too
            j = k
            while (title in used or sid in {x[0] for x in alts}) and j + 2 < len(t):
                j += 2; bb = chess.Board(); pv = None
                for s in t[:j]: pv = bb.parse_san(s); bb.push(pv)
                nxt = move_title(bb, bb.parse_san(t[j]), pv)
                title = f"{title.split(', then ')[0] if j == k + 2 else title}, then {nxt[0].lower() + nxt[1:] if not re.match(r'^(\\S+\\s+[A-Z]|[A-Z][^\\s-]*-[A-Z])', nxt) else nxt}"; sid += slug(t[j])
            n = 2
            while sid in {x[0] for x in alts}: sid = f'{sid}{n}'; n += 1
            used[title] = 1; alts.append((sid, title, lf))
        q = lambda s: "'" + s.replace("\\", "\\\\").replace("'", "\\'") + "'"
        out.append(f"L({q(L['id'])}, {q(L['part'])}, {q(L['title'])}, {q(L['sub'])}, {q(L['pri'])},\n  {q(main['path'])},")
        if alts:
            out.append('  alts=[' + ',\n        '.join(f"({q(L['id'] + '-' + sid)}, {q(title)}, {q(lf['path'])})" for sid, title, lf in alts) + '],')
        out.append(f"  why={q(L['why'])}, outcome={q(L['outcome'])})")
        table.append((L['id'], L['title'], main['path'], main['reach']))
        table += [(L['id'] + '-' + sid, title, lf['path'], lf['reach']) for sid, title, lf in alts]
    return '\n'.join(out), table
