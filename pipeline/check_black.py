"""Check Black-book lessons: legality, Black (your) move quality with Stockfish, White move realism and
coverage with Maia.  python3 pipeline/check_black.py [depth] [lesson-or-part ids, comma separated]"""
import sys, json, os, fcntl
import paths
import importlib
import bcontent as BC
try:
    import bnotes  # noqa  (registers notes; optional while drafting)
except ImportError:
    pass
import expand as X
from eng import engine, chess, done
DEPTH = int(sys.argv[1]) if len(sys.argv) > 1 else 14
only = set(sys.argv[2].split(',')) if len(sys.argv) > 2 and sys.argv[2] else None
CACHE = str(paths.CACHE / 'ev_cache.json')
ev = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
def save():
    lock = open(CACHE + '.lock', 'w'); fcntl.flock(lock, fcntl.LOCK_EX)
    try:
        disk = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
        disk.update(ev); tmp = CACHE + '.tmp'; json.dump(disk, open(tmp, 'w')); os.replace(tmp, CACHE)
    finally: fcntl.flock(lock, fcntl.LOCK_UN)
def score(b):
    k = b.fen() + f'|{DEPTH}'
    if k in ev: return ev[k]
    if b.is_checkmate(): v = [-100000 if b.turn == chess.WHITE else 100000, None]
    elif b.is_game_over(): v = [0, None]
    else:
        inf = engine().analyse(b, chess.engine.Limit(depth=DEPTH))
        s = inf['score'].white()
        val = (100000 - abs(s.mate()) * 100) * (1 if s.mate() > 0 else -1) if s.is_mate() else s.score()
        v = [val, b.san(inf['pv'][0]) if inf.get('pv') else None]
    ev[k] = v
    return v
ROOT = {'e4': 44/73, 'd4': 24/73, 'Nf3': 2/73, 'c4': 1/73, 'g3': 1/73, 'e3': 1/73}
lessons = [l for l in BC.LESSONS if not only or l['id'] in only or l['part'] in only]
paths = []
for l in lessons:
    paths.append((l['id'], l['path'], set(l['tags'])))
    for aid, _, p in l['alts']: paths.append((aid, p, set(l['tags'])))
tree = {}
bad = False
for lid, p, _ in paths:
    b = chess.Board(); toks = p.split()
    for i, s in enumerate(toks):
        try: b.push_san(s)
        except Exception as e:
            print(f"ILLEGAL {lid}: ply {i+1} {s!r} after {' '.join(toks[:i])}"); bad = True; break
        tree.setdefault(' '.join(toks[:i]), set()).add(s)
    if b.turn == chess.BLACK and not bad:
        print(f"ENDS-ON-WHITE {lid}: line should end with your move")
if bad: sys.exit(1)
def wprob(path, s):
    if not path: return ROOT.get(s, 0.003)
    return dict(X.human(path)).get(s, 0)
seen = set(); issues = []
for lid, p, tags in paths:
    b = chess.Board(); toks = p.split(); reach = 1.0
    for i, s in enumerate(toks):
        before = b.copy(); b.push_san(s)
        pre = ' '.join(toks[:i])
        if before.turn == chess.WHITE:
            pr = wprob(pre, s); reach *= max(pr, 0.001)
            if pr < 0.03 and (pre, s) not in seen:
                issues.append(f"W-RARE {lid}: {pre} || {s} p={pr*100:.1f}%")
        else:
            key = pre + ' ' + s
            if key in seen: continue
            bv, bm = score(before); av, _ = score(b)
            loss = av - bv  # white-POV increase = worse for you
            if ((loss > 45 and av > 30) or loss > 150) and abs(bv) < 5000:
                issues.append(f"B-LOSS {lid}: {pre} || {s} ({av/100:+.2f}) best {bm} ({bv/100:+.2f}) loss {loss}")
        seen.add((pre, s)); seen.add(pre + ' ' + s)
    save()
    end = score(b)[0]
    print(f"{lid:22s} end {end/100:+.2f}  plies {len(toks):2d}  reach {reach*100:.3f}%", flush=True)
# coverage at White-to-move nodes
for path, kids in sorted(tree.items(), key=lambda kv: (len(kv[0]), kv[0])):
    b = chess.Board()
    for s in path.split() if path else []: b.push_san(s)
    if b.turn != chess.WHITE or not path: continue
    hs = X.human(path)
    cov = sum(pp for s, pp in hs if s in kids)
    miss = [(s, pp) for s, pp in hs if s not in kids and pp >= 0.08]
    if miss:
        issues.append(f"W-MISS {path} | covered {cov*100:.0f}% | missing " + ', '.join(f"{s} {pp*100:.0f}%" for s, pp in miss))
X.save(); save()
print('\n'.join(issues))
done()
