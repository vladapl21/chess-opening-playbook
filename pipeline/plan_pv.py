"""Engine lines from the end of every book line, for the generated plans (pipeline/plan_lines.py).

Stockfish at depth 18 from each line's final position: the score (White's side, centipawns or "M<n>") and the first
ten moves of its line. Cached in data/cache/plan_cache.json by position, so a rebuild needs the engine only for new ends.
"""
import json
from common import *
import paths

CACHE = paths.CACHE / 'plan_cache.json'
DEPTH = 18


def full_fen(nodes, line):
    b = chess.Board()
    for i in line['n'][1:]:
        b.push(chess.Move.from_uci(nodes[i]['u']))
    return b


def need(sides=('white', 'black')):
    out = {}
    for s in sides:
        D = json.load(open(paths.BUILD / f'data_{s}.json'))
        for l in D['lines']:
            b = full_fen(D['nodes'], l)
            if b.is_game_over(): continue
            out[b.fen()] = b
    return out


def run():
    cache = json.load(open(CACHE)) if CACHE.exists() else {}
    todo = {f: b for f, b in need().items() if f not in cache}
    if not todo: return cache
    print(f'{len(todo)} line ends need an engine line ({len(cache)} cached)', flush=True)
    import eng
    for k, (f, b) in enumerate(todo.items()):
        inf = eng.engine().analyse(b, chess.engine.Limit(depth=DEPTH))
        sc = inf['score'].white()
        cache[f] = dict(s=(f'M{sc.mate()}' if sc.is_mate() else sc.score()), pv=[m.uci() for m in inf.get('pv', [])[:10]])
        if k % 20 == 0:
            json.dump(cache, open(CACHE, 'w'), sort_keys=True); print('  ', k, flush=True)
    json.dump(cache, open(CACHE, 'w'), sort_keys=True)
    eng.engine().quit()
    return cache


if __name__ == '__main__':
    run()
