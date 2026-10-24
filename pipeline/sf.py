"""Cached Stockfish multipv: python3 pipeline/sf.py [-d 18] "path" ...  (prints top moves, white-POV evals)"""
import sys, json, os
import paths
from eng import engine, chess, done
CACHE = str(paths.CACHE / 'sf_cache.json')
_c = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
def save(): json.dump(_c, open(CACHE, 'w'))
def board(path):
    b = chess.Board()
    for s in path.split(): b.push_san(s)
    return b
def ev(score):
    s = score.white()
    return f"#{s.mate()}" if s.is_mate() else s.score()
def top(path, depth=18, multipv=3):
    b = board(path)
    key = f"{b.fen()}|{depth}|{multipv}"
    if key in _c: return _c[key]
    infos = engine().analyse(b, chess.engine.Limit(depth=depth), multipv=multipv)
    out = []
    for inf in infos:
        pv = inf.get('pv', []); bb = b.copy(); sans = []
        for m in pv[:7]:
            sans.append(bb.san(m)); bb.push(m)
        out.append((ev(inf['score']), ' '.join(sans)))
    _c[key] = out
    return out
def fmt(e): return e if isinstance(e, str) else f"{e/100:+.2f}"
if __name__ == '__main__':
    args = sys.argv[1:]; depth = 18; mpv = 3
    if args and args[0] == '-d': depth = int(args[1]); args = args[2:]
    if args and args[0] == '-m': mpv = int(args[1]); args = args[2:]
    for p in args:
        r = top(p, depth, mpv)
        print(f"--- {p}")
        for e, pv in r: print(f"    {fmt(e):>7}  {pv}")
        sys.stdout.flush()
    save(); done()
