"""Find clean missed shots in Black games: Black to move, played move lost >=180cp (depth-10 scan),
and depth-16 multipv shows a unique best (gap >=150 to the 2nd best, best not worse than +50)."""
import sys, json
import paths
from eng import *
G = json.load(open(paths.DATA / 'black_games.json'))
F = json.load(open(paths.DATA / 'black_scan.json'))
out = []
for g in G:
    k = f"{g['opp']}|{g['date']}"; ev = F[k]['ev']; s = g['sans']
    for i in range(1, min(len(s), 70), 2):
        a, b = max(-2000, min(2000, ev[i])), max(-2000, min(2000, ev[i + 1]))
        if b - a < 180 or a > 150: continue
        bd = chess.Board()
        for x in s[:i]: bd.push_san(x)
        infos = engine().analyse(bd, chess.engine.Limit(depth=16), multipv=3)
        vals = []
        for inf in infos:
            sc = inf['score'].white(); v = (-10000 if sc.mate() < 0 else 10000) if sc.is_mate() else sc.score()
            vals.append((bd.san(inf['pv'][0]), v))
        if len(vals) < 2: continue
        gap = vals[1][1] - vals[0][1]
        if gap >= 150 and vals[0][1] <= 50:
            row = dict(opp=g['opp'], date=g['date'], ply=i, played=s[i], best=vals, res=g['res'], before=' '.join(s[max(0, i-4):i]))
            out.append(row); print(row, flush=True)
json.dump(out, open(paths.DATA / 'black_shots.json', 'w'), indent=0)
done()
