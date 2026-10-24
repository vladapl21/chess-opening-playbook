"""Expand Black's human replies (Maia) under a White policy.  Usage in scripts:
   expand(root, policy, thr=0.1, max_ply=20, reach=1.0)
policy: dict path -> White SAN (path = space-joined SAN from start)."""
import json, os
import paths
import chess
CACHE = str(paths.CACHE / 'maia_cache.json')
_c = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
def human(path):
    if path in _c: return _c[path]
    from maia import blended  # only needed for positions missing from the cache
    b = chess.Board()
    for s in path.split(): b.push_san(s)
    r = [(s, round(v, 4)) for s, v, _ in blended(b)[:12]]
    _c[path] = r
    return r
def save(): json.dump(_c, open(CACHE, 'w'))
def expand(root, policy, thr=0.1, max_ply=22, reach=1.0, min_reach=0.004, out=None, depth=0):
    out = out if out is not None else []
    b = chess.Board()
    toks = root.split() if root else []
    for s in toks: b.push_san(s)
    if len(toks) >= max_ply or b.is_game_over(): return out
    if b.turn == chess.WHITE:
        mv = policy.get(root)
        if mv is None:
            out.append(('  ' * depth) + f"?? WHITE to move after: {root}   (reach {reach*100:.2f}%)")
            return out
        if mv == 'END':
            out.append(('  ' * depth) + f"END {root} (reach {reach*100:.2f}%)"); return out
        for m in (mv if isinstance(mv, list) else [mv]):
            expand((root + ' ' + m).strip(), policy, thr, max_ply, reach, min_reach, out, depth)
        return out
    hs = human(root)
    for s, p in hs:
        if p < thr or reach * p < min_reach: continue
        out.append(('  ' * depth) + f"{s:6s} {p*100:4.0f}%  reach {reach*p*100:5.2f}%   [{root} {s}]")
        expand((root + ' ' + s).strip(), policy, thr, max_ply, reach * p, min_reach, out, depth + 1)
    return out
