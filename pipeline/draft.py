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
    def __init__(self, me, system=None, fixed=None, known=None, tol=45, thr=0.1, min_reach=0.004, depth=lambda reach: 16, win=350, eng_depth=15, follow=False):
        self.me = chess.WHITE if me == 'w' else chess.BLACK
        self.system, self.fixed, self.seen = system or (lambda b, p: []), {' '.join(k.split()): v for k, v in (fixed or {}).items()}, dict(known or {})
        self.tol, self.thr, self.min_reach, self.depth, self.win, self.ed = tol, thr, min_reach, depth, win, eng_depth
        self.leaves, self.why, self.flags, self.visited, self.walked = [], {}, [], set(), set()
        self.follow = follow          # past the last branch, play on along the likeliest replies to the line's full length

    def choose(self, path, b):
        if path in self.fixed: return self.fixed[path], 'fixed'
        e = b.epd()
        if e in self.seen and self.seen[e] in [b.san(m) for m in b.legal_moves]: return self.seen[e], 'same'
        top = best(b, self.ed)
        legal = {b.san(m) for m in b.legal_moves}; tried = []
        for s in self.system(b, path):
            if s not in legal: continue
            d = top[0][1] - value(b, s, self.ed)
            if d <= self.tol: return s, 'system'
            tried.append((s, d))
        if tried: self.flags.append((path, top[0][0], tried[:3]))      # the engine overruled the system here: worth a look
        return top[0][0], 'engine'

    def reach_of(self, path):
        """How often a game gets to path, by the other side's odds along it."""
        t = path.split(); r = 1.0; b = chess.Board()
        for k, s_ in enumerate(t):
            if b.turn != self.me and k > 0: r *= dict(X.human(' '.join(t[:k]))).get(s_, 0.003)
            b.push_san(s_)
        return r

    def replies(self, path, reach, n):
        thr = self.thr(n, reach) if callable(self.thr) else self.thr
        return [(s, p) for s, p in X.human(path) if p >= thr and reach * p >= self.min_reach]

    def go(self, path='', reach=1.0, extra=0):
        b = board_of(path); n = len(path.split())
        if b.is_game_over() or path in self.walked: return
        if b.turn != self.me:
            for s, p in self.replies(path, reach, n): self.go((path + ' ' + s).strip(), reach * p)
            return
        san, how = self.choose(path, b)
        self.seen[b.epd()] = san; self.why[(path + ' ' + san).strip()] = how
        v = value(b, san, self.ed); mv = b.parse_san(san); forcing = b.is_capture(mv) or b.gives_check(mv)
        new = (path + ' ' + san).strip(); a = b.copy(); a.push(mv)
        lim = self.depth(reach)
        if new in self.walked: return                             # a root already walked from here
        if a.epd() in self.visited:                               # another move order got here first: the line ends where they meet
            self.leaves.append(dict(path=new, reach=reach, v=v, meets=True)); return
        self.visited.add(a.epd())
        over = a.is_game_over() or (v >= self.win and n + 1 >= 8 and not forcing) or (n + 1 >= lim and not (forcing and extra < 2)) or n + 1 >= lim + 4
        hs = [] if over else self.replies(new, reach, n + 1)
        if n + 1 >= lim and hs: hs = hs[:1]                     # past the limit only to finish an exchange: the likeliest reply
        if not hs and not over and self.follow: hs = X.human(new)[:1]
        if not hs:
            self.leaves.append(dict(path=new, reach=reach, v=v)); return
        for s, p in hs: self.go(new + ' ' + s, reach * p, extra + 1 if n + 1 >= lim else 0)

    def run(self, roots):
        """roots: [(path, reach)] to start from (your move or theirs)."""
        for path, reach in roots:
            path = ' '.join(path.split()); self.go(path, reach if reach is not None else self.reach_of(path)); self.walked.add(path)
        save()
        return self.leaves


GENERIC = re.compile(r'^(Normal|Main|Standard|Classical|Modern|Symmetrical|Exchange|Open|Closed|Declined|Accepted)( Variation| Line| Defense| System)?$|^with |, with ')
NAMED = re.compile(r'^(\S+\s+[A-Z]|[A-Z][^\s-]*-[A-Z])')
HOME = {chess.WHITE: 0, chess.BLACK: 7}


def opening_started(b, mv):
    """The name of the line this move starts, when it starts one worth saying."""
    T = names.table(); a = b.copy(); a.push(mv); nm = T.get(a.epd())
    if nm and nm != T.get(b.epd()):
        tail = nm.split(': ')[-1].split(', ')[-1]
        if not GENERIC.search(tail) and len(tail) <= 34: return tail
    return None


def short(b, mv, prev, plain=False):
    """A short name for the other side's move, for a side line's title (plain: what the move is, never a line's name)."""
    nm = None if plain else opening_started(b, mv)
    if nm: return nm
    pc = b.piece_at(mv.from_square); t = pc.piece_type
    if b.is_castling(mv): return 'Castles' if chess.square_file(mv.to_square) > 4 else 'Castles long'
    a = b.copy(); a.push(mv)
    if b.is_capture(mv) or a.is_check():
        return auto_label(b, mv, prev, bool(prev and b.move_stack and _was_cap(b))).split(', ')[0]
    home = chess.square_rank(mv.from_square) == HOME[pc.color]
    if t == chess.PAWN:
        f = chess.FILE_NAMES[chess.square_file(mv.from_square)].upper()
        two = abs(chess.square_rank(mv.to_square) - chess.square_rank(mv.from_square)) == 2
        return f'{f}-pawn two squares' if two else f'Small {f.lower()}-pawn move'
    lab = auto_label(b, mv, prev, False)
    # ranks and files as the mover sees them: 1 is the home rank
    r = chess.square_rank(mv.to_square) + 1 if pc.color == chess.WHITE else 8 - chess.square_rank(mv.to_square); f = chess.FILE_NAMES[chess.square_file(mv.to_square)]
    if t == chess.KNIGHT and home:
        who = "Queen's" if chess.square_file(mv.from_square) < 4 else "King's"
        return f'{who} knight out' if f in 'cf' else f'{who} knight tucked in' if f in 'de' else f'{who} knight to the edge'
    if t == chess.BISHOP and home:
        if ', pins the ' in lab: return 'Bishop pins the ' + lab.split(', pins the ')[1]
        if r == 2 and f in 'bg': return 'Fianchetto'
        if r == 2: return 'Bishop to the quiet square' if f == 'e' else 'Bishop beside the queen'
        if r == 3: return 'Bishop to the middle' if f == 'd' else 'Bishop behind the center pawns' if f == 'e' else 'Bishop out'
        if r == 4: return ('Bishop aims at f7' if pc.color == chess.WHITE else 'Bishop aims at f2') if f == 'c' else ('Light' if (chess.square_file(mv.to_square) + chess.square_rank(mv.to_square)) % 2 else 'Dark') + ' bishop out'
        if r == 5:
            tg = [x for x in a.attacks(mv.to_square) if a.piece_at(x) and a.piece_at(x).color != pc.color and a.piece_at(x).piece_type == chess.KNIGHT]
            return 'Bishop comes at the knight' if tg else 'Bishop out to the side'
        return 'Bishop out'
    return lab.split(', ')[0]


def _was_cap(b):
    x = b.copy(); m = x.pop(); return x.is_capture(m)


def slug(san): return re.sub(r'[^a-z0-9]', '', san.lower().replace('o-o-o', 'ooo').replace('o-o', 'oo'))


def low(t): return t if NAMED.match(t) else t[0].lower() + t[1:]


def emit(leaves, lessons, me):
    """lessons: [dict(id, part, title, sub, pri, root, why, outcome, main=)], most specific roots win. Returns the L(...) text
    and a list of (line id, title, path, reach) for a look. A lesson's main line is its likeliest line that runs its
    full length; a side line is named after the other side's moves at the points where it leaves its neighbours."""
    for L in lessons:                                                   # 'roots': a lesson that gathers lines from several starts
        L['roots'] = [' '.join(r.split()) for r in (L.get('roots') or [L['root']])]; L['root'] = L['roots'][0]; L['leaves'] = []
    hit = lambda L, lf: max([len(r) for r in L['roots'] if (lf['path'] + ' ').startswith(r + ' ') or not r], default=-1)
    for lf in leaves:
        fits = [L for L in lessons if hit(L, lf) >= 0]
        assert fits, lf['path']
        max(fits, key=lambda L: hit(L, lf))['leaves'].append(lf)
    out, table = [], []
    q = lambda s: "'" + s.replace("\\", "\\\\").replace("'", "\\'") + "'"
    for L in lessons:
        ls = sorted(L['leaves'], key=lambda x: -x['reach'])
        if not ls: out.append(f"# !! no lines under {L['id']} ({L['root']})"); continue
        pre = ' '.join(L.get('main', '').split())                     # 'main': the main line has to start with these moves
        ok = [x for x in ls if (x['path'] + ' ').startswith(pre + ' ')] if pre else ls
        main = next((x for x in ok if not x.get('meets')), (ok or ls)[0]); mt = main['path'].split()
        toks = {id(x): x['path'].split() for x in ls}; alts, used_t, used_i = [], set(), set()
        for lf in ls:
            if lf is main: continue
            t = toks[id(lf)]
            k = next(i for i in range(len(t) + 1) if i >= len(t) or i >= len(mt) or t[i] != mt[i])
            if k >= len(t): continue                                  # a prefix of the main line: nothing of its own
            # the other side's moves where this line parts from a neighbour that shares its moves up to there
            cut = [k] + [j for j in range(k + 1, len(t)) if (j - k) % 2 == 0 and any(o is not lf and len(toks[id(o)]) > j and toks[id(o)][:j] == t[:j] and toks[id(o)][j] != t[j] for o in ls)]
            def name(j, plain=False):
                b = chess.Board(); pv = None
                for s_ in t[:j]: pv = b.parse_san(s_); b.push(pv)
                return short(b, b.parse_san(t[j]), pv, plain)
            parts_ = [name(j) for j in cut]
            for i_, j in enumerate(cut):                                # one name once in a title
                if parts_[i_] in parts_[:i_]: parts_[i_] = name(j, True)
            title = parts_[0]; sid = slug(t[cut[0]]); n = 1
            while (title in used_t or sid in used_i) and n < len(cut):
                title += ', then ' + low(parts_[n]); sid += slug(t[cut[n]]); n += 1
            if title in used_t: title += f' on move {k // 2 + 1}'      # the same move at another point of the line
            x = 2; base = title
            while title in used_t: title = f'{base} ({x})'; x += 1
            x = 2; base = sid
            while sid in used_i: sid = f'{base}v{x}'; x += 1
            used_t.add(title); used_i.add(sid); alts.append((sid, title, lf))
        out.append(f"L({q(L['id'])}, {q(L['part'])}, {q(L['title'])}, {q(L['sub'])}, {q(L['pri'])},\n  {q(main['path'])},")
        if alts:
            out.append('  alts=[' + ',\n        '.join(f"({q(L['id'] + '-' + sid)}, {q(title)}, {q(lf['path'])})" for sid, title, lf in alts) + '],')
        out.append(f"  why={q(L['why'])}, outcome={q(L['outcome'])})")
        table.append((L['id'], L['title'], main['path'], main['reach']))
        table += [(L['id'] + '-' + sid, title, lf['path'], lf['reach']) for sid, title, lf in alts]
    return '\n'.join(out), table


def known_from(side, skip_chapters=()):
    """EPD -> your move, for every position of a book where you move (so a new line that reaches one plays the same)."""
    D = json.load(open(paths.BUILD / f'data_{side}.json')); N = D['nodes']; me = side == 'white'
    part_ch = {p['id']: p['ch'] for p in D['parts']}; les_ch = {l['id']: part_ch.get(l['part']) for l in D['lessons']}
    out = {}
    for l in D['lines']:
        if les_ch.get(l['lesson']) in skip_chapters or l['lesson'] not in les_ch: continue
        b = chess.Board()
        for i in l['n'][1:]:
            mv = chess.Move.from_uci(N[i]['u'])
            if b.turn == (chess.WHITE if me else chess.BLACK) and 'warn' not in (N[i].get('g') or []): out.setdefault(b.epd(), b.san(mv))
            b.push(mv)
    return out


def show(leaves, why, top=None):
    for lf in sorted(leaves, key=lambda x: -x['reach'])[:top]:
        t = lf['path'].split(); marks = ''.join({'fixed': 'F', 'same': '=', 'system': 's', 'engine': 'E'}.get(why.get(' '.join(t[:k + 1]), ''), '.') for k in range(len(t)))
        print(f"{lf['reach'] * 100:6.2f}% {lf['v']:5d}  {lf['path']}   [{marks}]")


def named_moves(paths_, me, skip=()):
    """{path: opening name} for the other side's moves that start a named line (the names lichess gives)."""
    mine = chess.WHITE if me == 'w' else chess.BLACK; out = {}
    for p in paths_:
        b = chess.Board(); t = p.split()
        for k, s in enumerate(t):
            mv = b.parse_san(s); key = ' '.join(t[:k + 1])
            if b.turn != mine and key not in out and key not in skip:
                nm = opening_started(b, mv)
                if nm: out[key] = nm
            b.push(mv)
    return out


def module_text(doc, imports, parts, lessons_text, notes, auto, part_call):
    """The text of a content module: parts, the lessons emit() wrote, the notes written by hand, then the names."""
    q = lambda s: "'" + s.replace("\\", "\\\\").replace("'", "\\'") + "'"
    out = ['"""' + doc.strip() + '"""', imports, '']
    out += [part_call(p) for p in parts] + ['', lessons_text, '', '# ============================================================== notes']
    for path, v in notes.items():
        label, text = v[0], v[1]; tags = v[2] if len(v) > 2 else None; extra = v[3] if len(v) > 3 else {}
        args = [q(' '.join(path.split())), q(label), q(text) if text else 'None']
        if tags: args.append(repr(tags))
        args += [f'{k}={v!r}' for k, v in extra.items()]
        out.append(f"n({', '.join(args)})")
    out.append('# the other side\'s moves that start a named line')
    done_ = {' '.join(k.split()) for k in notes}
    out += [f"n({q(p)}, {q(nm)})" for p, nm in sorted(auto.items(), key=lambda kv: (len(kv[0].split()), kv[0])) if p not in done_]
    return '\n'.join(out) + '\n'


def base_paths(side):
    """The SAN paths of every node of the book as it stands in the last commit (before the pack being drafted)."""
    import subprocess
    D = json.loads(subprocess.run(['git', 'show', f'HEAD:data/build/data_{side}.json'], capture_output=True, text=True, cwd=paths.ROOT).stdout)
    N = D['nodes']; out = set(); bs = {0: (chess.Board(), '')}; todo = [0]
    for i in todo:
        for c in N[i].get('k', []):
            if c in bs or c >= len(N): continue
            b = bs[i][0].copy(); mv = chess.Move.from_uci(N[c]['u']); p = (bs[i][1] + ' ' + b.san(mv)).strip(); b.push(mv)
            bs[c] = (b, p); out.add(p); todo.append(c)
    return out
