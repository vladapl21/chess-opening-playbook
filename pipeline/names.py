"""Real opening names (data/openings, lichess-org/chess-openings, CC0).

  table()           EPD -> name, for every named position
  book_names(D)     node index -> the name of that exact position, for one book's nodes
  in_force(D)       node index -> the name in force there: the last named position on the way to it
  apply(D, side)    the curated names of content/opening_names.py: move labels and lesson titles become real names
  page_table()      the compact table the page uses to name any position (hash of the EPD, family, variation)

A position is named the way lichess.org names it: walk back through the moves to the last position that has a name.
"""
import csv, json
from common import *
import paths

DIR = paths.DATA / 'openings'
_T = None


def table():
    global _T
    if _T is None:
        _T = {}
        for f in 'abcde':
            for row in csv.DictReader(open(DIR / f'{f}.tsv', encoding='utf-8'), delimiter='\t'):
                b = chess.Board()
                for tok in row['pgn'].split():
                    if not tok.endswith('.'): b.push_san(tok)
                _T.setdefault(b.epd(), row['name'])
    return _T


def boards(D):
    """node index -> board, walking the tree from the start."""
    N = D['nodes']; out = {0: chess.Board()}; todo = [0]
    for i in todo:
        for c in N[i].get('k', []):
            if c in out or c >= len(N): continue
            b = out[i].copy(); b.push(chess.Move.from_uci(N[c]['u'])); out[c] = b; todo.append(c)
    return out


def book_names(D):
    T = table()
    return {i: T.get(b.epd()) for i, b in boards(D).items()}


def in_force(D):
    T = table(); N = D['nodes']; B = boards(D); out = {}
    for i in sorted(B, key=lambda i: len(B[i].move_stack)):
        p = N[i]['p']
        out[i] = T.get(B[i].epd()) or (out.get(p) if p is not None else None)
    return out


def san_path(D, i):
    """'1.e4 c5 2.c3' for a node: how content/opening_names.py names a position."""
    N = D['nodes']; path = []
    while N[i]['p'] is not None: path.append(i); i = N[i]['p']
    b = chess.Board(); out = []
    for k, j in enumerate(reversed(path)):
        m = chess.Move.from_uci(N[j]['u'])
        out.append((f'{k // 2 + 1}.' if k % 2 == 0 else '') + b.san(m)); b.push(m)
    return ' '.join(out)


def apply(D, side):
    """Put the curated real names (content/opening_names.py) in place of move descriptions: labels by the moves that
    reach them, lesson titles (and their main lines'), and side lines named after a renamed move. Every path and id must
    be in the book."""
    import opening_names as NC
    labels, titles, ltitles = NC.LABELS[side], NC.TITLES[side], NC.LINE_TITLES[side]
    N = D['nodes']
    at = {}
    for i in range(1, len(N)):
        if N[i].get('p') is None or 'u' not in N[i]: continue
        at.setdefault(san_path(D, i), []).append(i)
    missing = [p for p in labels if p not in at]
    assert not missing, f'content/opening_names.py: not in the {side} book: {missing}'
    renamed = {}                       # node -> (old label, new label)
    for p, lab in labels.items():
        for i in at[p]:
            renamed[i] = (N[i].get('l'), lab); N[i]['l'] = lab
    les = {L['id']: L for L in D['lessons']}
    missing = [k for k in titles if k not in les]
    assert not missing, f'content/opening_names.py: no such {side} lesson: {missing}'
    for k, t in titles.items(): les[k]['title'] = t
    lines = {l['id']: l for l in D['lines']}
    missing = [k for k in ltitles if k not in lines]
    assert not missing, f'content/opening_names.py: no such {side} line: {missing}'
    parts, P = NC.PARTS[side], D.get('parts')
    if P is not None:
        P = {x['id']: x for x in P} if isinstance(P, list) else P
        missing = [k for k in parts if k not in P]
        assert not missing, f'content/opening_names.py: no such {side} part: {missing}'
        for k, t in parts.items():
            if P[k]['title'] != t: P[k]['kicker'], P[k]['title'] = P[k]['title'], t
    for l in D['lines']:
        if l['main'] and l['lesson'] in titles: l['title'] = titles[l['lesson']]
        elif l['id'] in ltitles: l['title'] = ltitles[l['id']]
        else:
            for i in l['n']:
                if i in renamed and renamed[i][0] == l['title']: l['title'] = renamed[i][1]
    return D


def fnv(s):
    h = 0x811c9dc5
    for ch in s.encode():
        h ^= ch; h = (h * 0x01000193) & 0xffffffff
    return h


def b36(n):
    s = ''
    while True:
        n, r = divmod(n, 36); s = '0123456789abcdefghijklmnopqrstuvwxyz'[r] + s
        if not n: return s


def page_table():
    """'["family", ...]\\nhash,family,variation\\n...': the page decodes it into a Map (hash -> name)."""
    T = table(); hs = {}
    for epd, name in T.items():
        h = fnv(epd)
        assert h not in hs or hs[h] == name, ('hash collision', epd)
        hs[h] = name
    fams = sorted({n.split(': ')[0] for n in hs.values()})
    fi = {f: i for i, f in enumerate(fams)}
    rows = []
    for h, n in sorted(hs.items()):
        fam, _, var = n.partition(': ')
        rows.append(f'{b36(h)},{b36(fi[fam])},{var}')
    return json.dumps(fams, ensure_ascii=False) + '\n' + '\n'.join(rows)
