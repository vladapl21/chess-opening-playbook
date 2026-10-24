"""Collect the Black games from both accounts into data/black_games.json and summarize the openings."""
import sys, os, json, collections, io
import paths
from common import *
FILES = [str(paths.GAMES / f) for f in ('aqua_alpaca.pgn', 'vladapl_1.pgn', 'vladapl_2.pgn')]
ME = {'aqua_alpaca', 'vladapl'}
games = []
seen = set()
for f in FILES:
    fh = open(f)
    while True:
        g = chess.pgn.read_game(fh)
        if g is None: break
        h = g.headers
        if h.get('Black') not in ME: continue
        key = (h.get('Black'), h.get('White'), h.get('Date'), h.get('StartTime', h.get('UTCTime', '')))
        if key in seen: continue
        seen.add(key)
        sans = []
        b = g.board()
        for mv in g.mainline_moves():
            sans.append(b.san(mv)); b.push(mv)
        res = h.get('Result')
        r = 'W' if res == '0-1' else 'L' if res == '1-0' else 'D'
        games.append(dict(file=os.path.basename(f), me=h['Black'], opp=h['White'], date=h.get('Date'), welo=h.get('WhiteElo'), belo=h.get('BlackElo'),
                          tc=h.get('TimeControl'), res=r, term=h.get('Termination'), sans=sans, eco=h.get('ECO'), url=h.get('Link', h.get('Site'))))
json.dump(games, open(paths.DATA / 'black_games.json', 'w'), indent=0)
print('black games', len(games), collections.Counter(g['me'] for g in games))
print('results', collections.Counter(g['res'] for g in games))
c1 = collections.Counter(g['sans'][0] if g['sans'] else '-' for g in games)
print('White first move', c1.most_common())
for fm, _ in c1.most_common():
    sub = [g for g in games if g['sans'] and g['sans'][0] == fm]
    rep = collections.Counter(g['sans'][1] if len(g['sans']) > 1 else '-' for g in sub)
    w = sum(g['res'] == 'W' for g in sub); l = sum(g['res'] == 'L' for g in sub); d = sum(g['res'] == 'D' for g in sub)
    print(f'\n== 1.{fm}: {len(sub)} games  {w}-{l}-{d}  replies {rep.most_common()}')
    seqs = collections.Counter(' '.join(g['sans'][:8]) for g in sub)
    for s, n in seqs.most_common(40): print('  ', n, s)
print('\nelos', sorted(int(g['welo']) for g in games if g['welo'])[:5], '...', sorted(int(g['welo']) for g in games if g['welo'])[-5:])
print('my elo', collections.Counter((g['me'], g['belo']) for g in games).most_common(6))
print('tc', collections.Counter(g['tc'] for g in games))
print('dates', min(g['date'] for g in games), max(g['date'] for g in games))
