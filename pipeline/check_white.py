"""Check White-book lessons of the packs added after the first one (the London): legality, White (your) move quality with
Stockfish, Black move realism and coverage with Maia.
    python3 pipeline/check_white.py [depth] [lesson-or-part ids, comma separated]
With ids, those lessons are checked whatever pack they are in (the first pack's hand-built lessons are not in the
default run: many show a trap on purpose).

The same report as check_black.py, from the other side. W-LOSS, ILLEGAL and ENDS-ON-BLACK need a look; B-RARE and
B-MISS are information. A line with a move tagged 'warn' shows a mistake on purpose and is skipped from the move check."""
import sys, json, os, fcntl
import paths
import content, content2, content2_meta as CM  # noqa: F401  (content2 registers the London)
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


# the lessons of every chapter that belongs to a pack other than the slot's first one
later = {c for s in CM.PACKS.values() for p, chs in s['packs'].items() if p != s['default'] for c in chs}
part_ch = {p['id']: p['ch'] for p in content.PARTS}
lessons = [l for l in content.LESSONS if (l['id'] in only or l['part'] in only if only else part_ch[l['part']] in later)]   # named ids: any pack
warn = {p for p, nt in content.NOTES.items() if 'warn' in (nt.get('tags') or [])}
lines = []
for l in lessons:
    lines.append((l['id'], l['path']))
    for aid, _, p in l['alts']: lines.append((aid, p))
tree, bad = {}, False
for lid, p in lines:
    b = chess.Board(); toks = p.split()
    for i, s in enumerate(toks):
        try: b.push_san(s)
        except Exception:
            print(f"ILLEGAL {lid}: ply {i + 1} {s!r} after {' '.join(toks[:i])}"); bad = True; break
        tree.setdefault(' '.join(toks[:i]), set()).add(s)
    if not bad and b.turn == chess.WHITE and not b.is_checkmate():
        print(f"ENDS-ON-BLACK {lid}: line should end with your move")
if bad: sys.exit(1)
seen, issues = set(), []
for lid, p in lines:
    b = chess.Board(); toks = p.split(); reach = 1.0; shown = False
    for i, s in enumerate(toks):
        before = b.copy(); b.push_san(s); pre = ' '.join(toks[:i]); key = (pre + ' ' + s).strip()
        if key in warn: shown = True
        if before.turn == chess.BLACK:
            pr = dict(X.human(pre)).get(s, 0); reach *= max(pr, 0.001)
            if pr < 0.03 and key not in seen: issues.append(f"B-RARE {lid}: {pre} || {s} p={pr * 100:.1f}%")
        elif not shown and key not in seen:
            bv, bm = score(before); av, _ = score(b)
            loss = bv - av      # White-POV drop = worse for you
            if ((loss > 45 and av < -30) or loss > 150) and abs(bv) < 5000:
                issues.append(f"W-LOSS {lid}: {pre} || {s} ({av / 100:+.2f}) best {bm} ({bv / 100:+.2f}) loss {loss}")
        seen.add(key)
    save()
    end = score(b)[0]
    print(f"{lid:20s} end {end / 100:+.2f}  plies {len(toks):2d}  reach {reach * 100:.3f}%" + ('  (shows a mistake)' if shown else ''), flush=True)
# coverage where Black is to move inside the pack: a reply club players choose 8% of the time or more with no answer
for path, kids in sorted(tree.items(), key=lambda kv: (len(kv[0]), kv[0])):
    b = chess.Board()
    for s in path.split() if path else []: b.push_san(s)
    if b.turn != chess.BLACK or not path: continue
    hs = X.human(path)
    cov = sum(pp for s, pp in hs if s in kids)
    miss = [(s, pp) for s, pp in hs if s not in kids and pp >= 0.08]
    if miss:
        issues.append(f"B-MISS {path} | covered {cov * 100:.0f}% | missing " + ', '.join(f"{s} {pp * 100:.0f}%" for s, pp in miss))
X.save(); save()
print('\n'.join(issues))
done()
