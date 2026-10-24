from common import *
import sys, json, time
_engine=None
def engine():
    global _engine
    if _engine is None:
        _engine=chess.engine.SimpleEngine.popen_uci(SF)
        _engine.configure({'Threads':2,'Hash':512})
    return _engine
def board_from(moves):
    b=chess.Board()
    for s in moves.split():
        b.push_san(s)
    return b
def fmt(score):
    s=score.white()
    if s.is_mate(): return f"#{s.mate()}"
    return f"{s.score()/100:+.2f}"
def analyze(moves, depth=20, multipv=3, t=None):
    b=board_from(moves) if isinstance(moves,str) else moves
    lim=chess.engine.Limit(depth=depth) if t is None else chess.engine.Limit(time=t)
    infos=engine().analyse(b, lim, multipv=multipv)
    out=[]
    for inf in infos:
        pv=inf.get('pv',[])
        bb=b.copy(); sans=[]
        for m in pv[:8]:
            sans.append(bb.san(m)); bb.push(m)
        out.append((fmt(inf['score']), ' '.join(sans)))
    return out
def show(moves, depth=20, multipv=3, label=None):
    res=analyze(moves, depth, multipv)
    print(f"--- {label or moves}")
    for e,pv in res: print(f"   {e:>7}  {pv}")
    sys.stdout.flush()
def evalmove(moves, cand, depth=18):
    # eval of position after cand played
    b=board_from(moves); b.push_san(cand)
    inf=engine().analyse(b, chess.engine.Limit(depth=depth))
    return fmt(inf['score'])
import os
def done():
    """Flush and hard-exit (python-chess engine threads can hang interpreter shutdown)."""
    sys.stdout.flush(); sys.stderr.flush()
    try:
        if _engine is not None: _engine.close()
    except Exception: pass
    os._exit(0)
