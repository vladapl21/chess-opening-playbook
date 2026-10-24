"""Depth-10 eval at every ply of every Black game -> data/black_scan.json (White-POV centipawns, mate = +-10000)."""
import sys, json, os
import paths
from eng import *
G = json.load(open(paths.DATA / 'black_games.json'))
out = str(paths.DATA / 'black_scan.json')
res = json.load(open(out)) if os.path.exists(out) else {}
for g in G:
    key = f"{g['opp']}|{g['date']}"
    if key in res: continue
    b = chess.Board(); evs = []; bests = []
    for s in g['sans'] + [None]:
        if b.is_game_over():
            v = (-10000 if b.turn == chess.WHITE else 10000) if b.is_checkmate() else 0
            evs.append(v); bests.append(None)
        else:
            inf = engine().analyse(b, chess.engine.Limit(depth=10))
            sc = inf['score'].white()
            v = (10000 if sc.mate() > 0 else -10000) if sc.is_mate() else sc.score()
            evs.append(v); bests.append(b.san(inf['pv'][0]) if inf.get('pv') else None)
        if s is None: break
        b.push_san(s)
    res[key] = dict(ev=evs, best=bests)
    json.dump(res, open(out, 'w'))
    print('done', key, len(evs), flush=True)
done()
