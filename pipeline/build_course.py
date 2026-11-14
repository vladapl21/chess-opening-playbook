"""Build the course from content/course.py, both built books and data/course_threats.json.

    python3 pipeline/build_course.py   ->  data/build/data_course.json

Every move path is resolved against the unit's book, so a path that leaves the repertoire fails the build.
"""
import json, datetime
import paths
import chess
from course import UNITS, QUIZ, SKILL_IDEAS, DEEP

BOOK = {s: json.load(open(paths.BUILD / f'data_{n}.json')) for s, n in (('w', 'white'), ('b', 'black'))}
# skill units: positions from your own games (data/course_<skill>.json, picked by the scripts in the README)
SKILL_SRC = {'threats': 'course_threats.json', 'finish': 'course_finish.json', 'endings': 'course_endings.json'}
ME = {'w': 1, 'b': 0}


def node_at(side, path):
    N = BOOK[side]['nodes']; i = 0; b = chess.Board()
    for san in path.split():
        mv = b.parse_san(san); b.push(mv)
        kids = [c for c in N[i].get('k', []) if N[c].get('u') == mv.uci()]
        assert kids, f'{side}: "{path}" leaves the book at {san}'
        i = kids[0]
    return i


def warn(N, i): return 'warn' in (N[i].get('g') or [])


def drillable(side):
    D = BOOK[side]; N = D['nodes']; les = {l['id'] for l in D['lessons']}
    return {l['id'] for l in D['lines'] if l['lesson'] in les and not any(warn(N, i) and N[i].get('w') == ME[side] for i in l['n'])}


def my_kids(side, i):
    D = BOOK[side]; N = D['nodes']
    return [c for c in N[i].get('k', []) if c < D['repCount'] and N[c].get('w') == ME[side] and not warn(N, c)]


def short_date(d):
    return datetime.date(*map(int, d.split('.'))).strftime('%b %-d')


def slide(side, s):
    out = dict(node=node_at(side, s['path']), h=s['h'], t=s['t'])
    if s.get('arrows'): out['arrows'] = s['arrows']
    if s.get('circles'): out['circles'] = s['circles']
    return out


def quiz_item(side, path, main_lines):
    D = BOOK[side]; N = D['nodes']; i = node_at(side, path)
    kids = my_kids(side, i)
    assert kids, f'{side}: no move of yours after "{path}"'
    assert str(i) in D['legal'], f'{side}: no legal moves stored after "{path}"'
    on_line = [c for c in kids if any(c in ln for ln in main_lines)]
    ans = (on_line or kids)[0]
    cheat = next((c for c in D['cheat'] if c['node'] == i and c['mv'] == N[ans]['u']), None)
    return dict(node=i, ok=[N[c]['u'] for c in kids], ans=N[ans]['u'], label=N[ans]['l'],
                rule=cheat['rule'] if cheat else N[ans]['l'], note=N[ans].get('t', ''))


def threat_item(t):
    return dict(id=t['id'], fen=t['fen'].split()[0], ff=t['fen'], me=t['me'], last=t['last'], lastLabel=t['lastLabel'], safe=t['safe'], legal=t['legal'],
                played=t['played'], playedLabel=t['playedLabel'], reply=t['reply'], replyLabel=t['replyLabel'],
                threat=t['threat'], threatLabel=t['threatLabel'], refute=t['refute'], fine=t.get('fine', []),
                opp=t['opp'], date=short_date(t['date']), **({'best': t['best']} if 'best' in t else {}))


units, seen_lessons = [], {}
for U in UNITS:
    u = {k: U[k] for k in ('id', 'title', 'kicker', 'why') if k in U}
    u['kind'] = U.get('kind', 'lessons')
    if U.get('soon'):
        u['soon'] = True
        if U.get('side'): u['side'] = U['side']
        if U.get('chapter'):
            assert any(c['id'] == U['chapter'] for c in BOOK[U['side']]['chapters']), U['chapter']
            u['chapter'] = U['chapter']
        units.append(u); continue
    if u['kind'] == 'skill':
        sk = u['skill'] = U.get('skill', 'threats')
        T = json.load(open(paths.DATA / SKILL_SRC[sk])); ex = T['examples']; cards = SKILL_IDEAS[sk]
        assert len(ex) == len(cards), (sk, len(ex), len(cards))
        def card_arrows(e, c):
            if c.get('show') == 'move': return [e['played'][:4] + 'b', e['reply'][:4] + 'r']
            if c.get('show') == 'keep': return [e['safe'][0][:4] + 'g', e['played'][:4] + 'b']
            return [(e['threat'] or e['reply'])[:4] + 'r']
        u['idea'] = [dict(fen=e['fen'].split()[0], me=e['me'], last=e['last'], h=c['h'], t=c['t'], arrows=card_arrows(e, c),
                          game=f"vs {e['opp']}, {short_date(e['date'])}")
                     for e, c in zip(ex, cards)]
        u['sets'] = [[threat_item(t) for t in s] for s in T['sets']]
        u['check'] = [threat_item(t) for t in T['check']]
        u['passSet'], u['passCheck'] = U['pass_set'], U['pass_check']
        units.append(u); continue
    side = U['side']; D = BOOK[side]; L = {l['id']: l for l in D['lessons']}; LN = {l['id']: l for l in D['lines']}
    ok_lines = drillable(side)
    for lid in U['lessons'] + U['deeper']:
        assert lid in L, f'{U["id"]}: no lesson {lid}'
        assert lid not in seen_lessons, f'{lid} is in {seen_lessons[lid]} and {U["id"]}'
        seen_lessons[lid] = U['id']
    mains = [L[lid]['lines'][0] for lid in U['lessons']]
    for m in mains: assert m in ok_lines, f'{U["id"]}: main line {m} is not drillable'
    u['side'] = side
    u['lessons'], u['deeper'], u['lines'] = U['lessons'], U['deeper'], mains
    u['spar'] = sorted(x for lid in U['lessons'] for x in L[lid]['lines'] if x in ok_lines)
    u['idea'] = [slide(side, s) for s in U['idea']]
    main_nodes = [set(LN[m]['n']) for m in mains]
    u['quiz'] = [quiz_item(side, p, main_nodes) for p in QUIZ[U['id']]]
    assert len(u['quiz']) == 6, U['id']
    u['pass'] = 5
    units.append(u)

# every lesson of both books shows up somewhere in the course, or is in a unit marked 'soon'
for s in ('w', 'b'):
    soon_ch = {c for U in UNITS if U.get('soon') and U.get('side') == s for c in [U.get('chapter')] + U.get('also', []) if c}
    missing = [l['id'] for l in BOOK[s]['lessons'] if l['id'] not in seen_lessons
               and BOOK[s]['parts'][[p['id'] for p in BOOK[s]['parts']].index(l['part'])]['ch'] not in soon_ch]
    if missing: print(f'note: {s} lessons outside the course: {missing}')

# ---- deep dives (content/course.py DEEP): one opening each, its 'deeper' lessons in parts
def branch_at(side, les):
    """The lesson's main line and the index of its first new move by the other side, with your answer after it."""
    D = BOOK[side]; N = D['nodes']; n = next(l for l in D['lines'] if l['id'] == les['lines'][0])['n']
    for j in range(max(les.get('start', 0), 1), len(n) - 1):
        if N[n[j]].get('w') != ME[side] and N[n[j + 1]].get('w') == ME[side]: return n, j
    raise AssertionError(f'{les["id"]}: no move of yours after a new move')


def decisions(side, n, frm):
    """Positions on a line, from index frm on, where the line's next move is yours (and not a move to avoid)."""
    N = BOOK[side]['nodes']
    return [n[j] for j in range(frm, len(n) - 1) if N[n[j + 1]].get('w') == ME[side] and not warn(N, n[j + 1])]


def deep_quiz(side, lids, br, want=6):
    """Checkpoint positions: each lesson's first answer, then the first answer of each of its other lines, then the
    later moves, taken in turn from the part's lessons."""
    D = BOOK[side]; L = {l['id']: l for l in D['lessons']}; LN = {l['id']: l for l in D['lines']}
    queues = []
    for lid in lids:
        les = L[lid]; n0, j0 = br[lid]; main = decisions(side, n0, j0); alts = []
        for x in les['lines'][1:]:
            n = LN[x]['n']; k = next((k for k in range(len(n)) if k >= len(n0) or n[k] != n0[k]), len(n))
            alts.append(decisions(side, n, max(k - 1, j0)))
        queues.append(main[:1] + [a[0] for a in alts if a] + main[1:] + [y for a in alts for y in a[1:]])
    N = D['nodes']; out, seen, kinds = [], set(), set()
    kind = lambda i: (N[i].get('l'), N[my_kids(side, i)[0]]['u'])        # the same reply met with the same answer counts once
    for strict in (True, False):                                     # first a different question each time, then repeats
        qs = [q[:] for q in queues]
        while len(out) < want and any(qs):
            for q in qs:
                while q and (q[0] in seen or not my_kids(side, q[0]) or str(q[0]) not in D['legal'] or (strict and kind(q[0]) in kinds)): q.pop(0)
                if q: i = q.pop(0); seen.add(i); kinds.add(kind(i)); out.append(i)
                if len(out) >= want: break
    return out


def quiz_at(side, i, prefer):
    D = BOOK[side]; N = D['nodes']; kids = my_kids(side, i)
    ans = ([c for c in kids if c in prefer] or kids)[0]
    cheat = next((c for c in D['cheat'] if c['node'] == i and c['mv'] == N[ans]['u']), None)
    return dict(node=i, ok=[N[c]['u'] for c in kids], ans=N[ans]['u'], label=N[ans]['l'],
                rule=cheat['rule'] if cheat else N[ans]['l'], note=N[ans].get('t', ''))


deep, deep_units = [], []
base_of = {U['id']: U for U in UNITS}
for X in DEEP:
    B = base_of[X['base']]; side = B['side']; D = BOOK[side]; N = D['nodes']
    L = {l['id']: l for l in D['lessons']}; LN = {l['id']: l for l in D['lines']}; ok_lines = drillable(side)
    used = [lid for P in X['parts'] for lid in P['lessons']]
    assert sorted(used) == sorted(B['deeper']), f'{X["id"]}: the parts must hold every deeper lesson of {B["id"]} once ({sorted(set(B["deeper"]) ^ set(used))})'
    word = 'White' if side == 'w' else 'Black'; pids = []
    for k, P in enumerate(X['parts']):
        pid = f'{X["id"]}-{k + 1}'; pids.append(pid)
        mains = [m for m in (next((x for x in L[lid]['lines'] if x in ok_lines), None) for lid in P['lessons']) if m]
        spar = sorted(x for lid in P['lessons'] for x in L[lid]['lines'] if x in ok_lines)
        assert mains and spar, f'{pid}: nothing to drill'
        # each lesson's own moment: its first move by the other side that no other lesson of the part shares
        br = {}
        for lid in P['lessons']:
            n, j0 = branch_at(side, L[lid])
            k = max((next((i for i in range(min(len(n), len(m))) if n[i] != m[i]), min(len(n), len(m))) for m in
                     (branch_at(side, L[o])[0] for o in P['lessons'] if o != lid)), default=0)
            br[lid] = (n, next((j for j in range(max(j0, k), len(n) - 1) if N[n[j]].get('w') != ME[side] and N[n[j + 1]].get('w') == ME[side]), j0))
        # the cards: where the part's lessons split (their first moves in blue), then one per lesson with your answer
        first_n, first_j = br[P['lessons'][0]]; at = first_n[first_j - 1]
        tries = []
        for lid in P['lessons']:
            n, j = br[lid]
            if n[j - 1] != at: continue
            for x in L[lid]['lines']:
                ln = LN[x]['n']
                if at in ln:
                    m = ln.index(at)
                    if m + 1 < len(ln) and N[ln[m + 1]].get('w') != ME[side] and ln[m + 1] not in tries: tries.append(ln[m + 1])
        tries = sorted(tries, key=lambda c: -(N[c].get('q') or 0))[:5]       # the most common five, so the board stays readable
        idea = [dict(node=at, h=P['title'], t=P['t'], arrows=[N[c]['u'][:4] + 'b' for c in tries])]
        for lid in P['lessons']:
            n, j = br[lid]; mv = n[j + 1]
            arrows, card = [N[mv]['u'][:4] + ('r' if warn(N, mv) else 'g')], dict(node=n[j], lesson=lid, say=N[mv]['l'])
            if warn(N, mv):                     # a lesson about a move to drop: red for it, green for the move to play
                good = my_kids(side, n[j]); card['avoid'] = N[mv]['l']; card['say'] = N[good[0]]['l'] if good else ''
                if good: arrows.append(N[good[0]]['u'][:4] + 'g')
            idea.append(dict(card, arrows=arrows))
        q = deep_quiz(side, P['lessons'], br)
        assert len(q) >= 4, f'{pid}: only {len(q)} checkpoint positions'
        prefer = {i for x in spar for i in LN[x]['n']}
        deep_units.append(dict(id=pid, deep=X['id'], kind='lessons', side=side, title=P['title'], kicker=f'{word} · {P["sub"]}', why=P['why'],
                               lessons=P['lessons'], deeper=[], lines=mains, spar=spar, idea=idea,
                               quiz=[quiz_at(side, i, prefer) for i in q], **{'pass': 5 if len(q) >= 6 else len(q) - 1}))
    deep.append(dict(id=X['id'], base=X['base'], side=side, title=X['title'], name=X['name'], tag=X['tag'], why=X['why'], parts=pids))
ids = [u['id'] for u in units] + [u['id'] for u in deep_units]
assert len(ids) == len(set(ids)), 'unit ids collide'

out = dict(units=units, deep=deep, deepUnits=deep_units)
(paths.BUILD / 'data_course.json').write_text(json.dumps(out, separators=(',', ':')))
n_les = sum(len(u.get('lessons', [])) for u in units)
print(f"course: {len(units)} units ({sum(1 for u in units if u.get('soon'))} soon), {n_les} core lessons, "
      f"{sum(len(u.get('deeper', [])) for u in units)} deeper, {sum(len(u.get('quiz', [])) for u in units)} checkpoint positions, "
      f"{sum(len(s) for u in units for s in u.get('sets', []))}+{sum(len(u.get('check', [])) for u in units)} threat positions; "
      f"{len(deep)} deep dives in {len(deep_units)} parts, {sum(len(u['quiz']) for u in deep_units)} checkpoint positions")
