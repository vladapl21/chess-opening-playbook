"""Give every wrong move in the skill units (threats, finish, endings) a reason that can be shown on the board.

For each position in data/course_{threats,finish,endings}.json and each legal move that is not one of its answers,
the engine plays the move and gives its line. From that line:

  reply   the opponent's answer, with its label
  tail    the moves after the reply, up to the move where the material is actually lost (or mate), at most 6;
          empty when the reply itself wins the material
  lost    material lost by the end of that line, in pawns (0: nothing is lost on the board in this line)
  cp      the engine's number after the wrong move, from White's side ('M3' / 'M-3' for a forced mate)

A wrong move becomes  refute[move] = [reply, label, material won by the reply, tail, lost, cp].

Threat positions also get `fine`: moves that are not the engine's answers but lose nothing in the engine's line and
cost less than 30 points of winning chance. The page accepts those: "a safe move" should mean what it says.

Needs Stockfish (STOCKFISH). Results are written into the data files, which are committed, so the build needs no engine.
    python3 pipeline/explain_skills.py [depth]      the engine pass
    python3 pipeline/explain_skills.py recut        cut the stored lines again after a change to cut_line (no engine)"""
import sys, json, math
import paths
from common import *
from eng import engine
from label2 import label

DEPTH = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 14
FINE_DROP = 30      # a threat answer that loses nothing on the board is accepted unless it gives up this much winning chance
VAL = {chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3, chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 0}
material = lambda b, c: sum(VAL[p.piece_type] * (1 if p.color == c else -1) for p in b.piece_map().values())
win = lambda c: 50 + 50 * (2 / (1 + math.exp(-0.00368208 * max(-1500, min(1500, c)))) - 1)


def pov_cp(score, color):
    s = score.pov(color)
    return (10000 - 10 * abs(s.mate())) * (1 if s.mate() > 0 else -1) if s.is_mate() else s.score()


def white_num(score):
    s = score.white()
    return f'M{s.mate()}' if s.is_mate() else s.score()


def cut_line(a, me, pv):
    """Where a line makes its point. a: the board after the wrong move; pv: the opponent's reply and what follows.
    Returns (plies to keep, material lost at that point, material the reply wins at once, ends in mate)."""
    base = material(a, me); c = a.copy(); loss_at = []      # the mover's loss after each ply (even: their move, odd: the mover's)
    for m in pv:
        c.push(m); loss_at.append(base - material(c, me))
        if c.is_checkmate(): break
    n = len(loss_at); mate = c.is_checkmate() and c.turn == me
    if mate: return n, max(loss_at), max(0, loss_at[0]), True
    # what is still missing after the mover's last move in the line, so a trade in progress is not counted as a loss
    # (a line that stops on their capture counts in full when the mover has no way to take back on that square)
    odd = [k for k in range(n) if k % 2 == 1]; final = max(0, loss_at[odd[-1]] if odd else loss_at[-1])
    if n % 2 == 1 and not any(m.to_square == pv[n - 1].to_square for m in c.legal_moves): final = max(0, loss_at[-1])
    if final == 0: return min(n, 4), 0, max(0, loss_at[0]), False
    # the point is made at the first loss that the mover cannot take straight back: a piece if a piece goes, else the pawn
    need = min(final, 2); holds = lambda k: loss_at[k] >= need and (k + 1 >= n or loss_at[k + 1] >= need)
    k = next((k for k in range(n) if holds(k)), n - 1)
    return min(k + 1, 7), max(1, min(loss_at[k], loss_at[k + 1]) if k + 1 < n else loss_at[k]), max(0, loss_at[0]), False


def explain(b, mv):
    """The engine's line after a move, cut at the point where the mover's loss is on the board."""
    me = b.turn; a = b.copy(); a.push(mv)
    if a.is_checkmate(): return None
    if a.is_game_over(): return dict(reply=None)
    inf = engine().analyse(a, chess.engine.Limit(depth=DEPTH)); pv = inf.get('pv', [])[:8]
    cut, lost, mat, mate = cut_line(a, me, pv)
    return dict(reply=pv[0], label=label(a.copy(), pv[0]), mat=mat, tail=[m.uci() for m in pv[1:cut]], lost=lost,
                cp=white_num(inf['score']), mine=pov_cp(inf['score'], me), mate=mate)


def recut(kind):
    """Apply cut_line again to the lines already in the data (no engine): a stored line is never shorter than its cut."""
    path = paths.DATA / f'course_{kind}.json'; T = json.load(open(path)); n = 0
    for it in [i for s in T['sets'] for i in s] + T['check'] + T.get('examples', []):
        b = chess.Board(it['fen'])
        for u, r in it['refute'].items():
            if len(r) < 6 or r.__class__ is not list: continue
            a = b.copy(); a.push_uci(u); pv = [chess.Move.from_uci(x) for x in [r[0]] + r[3]]
            cut, lost, mat, mate = cut_line(a, b.turn, pv)
            new = [r[0], r[1], mat, r[3][:cut - 1], lost, r[5]]
            if new != r: it['refute'][u] = new; n += 1
    json.dump(T, open(path, 'w'), separators=(',', ':')); print(f'{kind}: {n} lines shortened')


def run(kind):
    path = paths.DATA / f'course_{kind}.json'; T = json.load(open(path))
    items = [i for s in T['sets'] for i in s] + T['check'] + T.get('examples', [])
    seen = {}; n = fine_n = 0
    for it in items:
        if it['fen'] in seen: it['refute'], it['fine'] = seen[it['fen']]; continue
        b = chess.Board(it['fen']); me = b.turn
        best = pov_cp(engine().analyse(b, chess.engine.Limit(depth=DEPTH))['score'], me)
        ref, fine = {}, []
        for u in it['legal']:
            if u in it['safe']: continue
            x = explain(b, chess.Move.from_uci(u)); n += 1
            if x is None or x['reply'] is None: continue
            if kind == 'threats' and u != it['played'] and x['lost'] == 0 and not x['mate'] and win(best) - win(x['mine']) < FINE_DROP: fine.append(u); fine_n += 1; continue
            ref[u] = [x['reply'].uci(), x['label'], x['mat'], x['tail'], x['lost'], x['cp']]
        it['refute'] = ref; it['fine'] = fine; seen[it['fen']] = (ref, fine)
        print(f"  {kind} {it['id'][:28]:28s} answers {len(it['safe'])} fine {len(fine)} wrong {len(ref)} deep {sum(1 for r in ref.values() if r[3])}", flush=True)
    json.dump(T, open(path, 'w'), separators=(',', ':'))
    print(f'{kind}: {len(items)} positions, {n} moves checked, {fine_n} now accepted')


def regrade():
    """Threat positions: move the wrong answers that lose nothing on the board and little in the engine's eyes to `fine`."""
    path = paths.DATA / 'course_threats.json'; T = json.load(open(path)); n = 0
    for it in [i for s in T['sets'] for i in s] + T['check'] + T.get('examples', []):
        b = chess.Board(it['fen']); me = b.turn
        best = pov_cp(engine().analyse(b, chess.engine.Limit(depth=DEPTH))['score'], me)
        for u, r in list(it['refute'].items()):
            if r[4] or isinstance(r[5], str) or u == it['played'] or 'checkmate' in r[1]: continue
            if win(best) - win(r[5] if me == chess.WHITE else -r[5]) < FINE_DROP: it.setdefault('fine', []).append(u); del it['refute'][u]; n += 1
    json.dump(T, open(path, 'w'), separators=(',', ':')); print('threats:', n, 'more moves accepted')


if __name__ == '__main__':
    if 'regrade' in sys.argv: regrade(); engine().quit()
    elif 'recut' in sys.argv:
        for kind in ('threats', 'finish', 'endings'): recut(kind)
    else:
        for kind in ('threats', 'finish', 'endings'): run(kind)
        engine().quit()
