"""Build the course from content/course.py, both built books and data/course_threats.json.

    python3 pipeline/build_course.py   ->  data/build/data_course.json

Every move path is resolved against the unit's book, so a path that leaves the repertoire fails the build.
"""
import json, datetime
import paths
import chess
from course import UNITS, THREAT_IDEA, QUIZ

BOOK = {s: json.load(open(paths.BUILD / f'data_{n}.json')) for s, n in (('w', 'white'), ('b', 'black'))}
THREATS = json.load(open(paths.DATA / 'course_threats.json'))
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
    return dict(id=t['id'], fen=t['fen'].split()[0], me=t['me'], last=t['last'], lastLabel=t['lastLabel'], safe=t['safe'], legal=t['legal'],
                played=t['played'], playedLabel=t['playedLabel'], reply=t['reply'], replyLabel=t['replyLabel'],
                threat=t['threat'], threatLabel=t['threatLabel'], refute={u: r[:2] for u, r in t['refute'].items()},
                opp=t['opp'], date=short_date(t['date']))


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
        ex = THREATS['examples']
        u['idea'] = [dict(fen=e['fen'].split()[0], me=e['me'], last=e['last'], h=c['h'], t=c['t'],
                          arrows=[e['played'][:4] + 'b', e['reply'][:4] + 'r'] if c.get('show') == 'move' else [(e['threat'] or e['reply'])[:4] + 'r'],
                          game=f"vs {e['opp']}, {short_date(e['date'])}")
                     for e, c in zip(ex, THREAT_IDEA)]
        u['sets'] = [[threat_item(t) for t in s] for s in THREATS['sets']]
        u['check'] = [threat_item(t) for t in THREATS['check']]
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

out = dict(units=units)
(paths.BUILD / 'data_course.json').write_text(json.dumps(out, separators=(',', ':')))
n_les = sum(len(u.get('lessons', [])) for u in units)
print(f"course: {len(units)} units ({sum(1 for u in units if u.get('soon'))} soon), {n_les} core lessons, "
      f"{sum(len(u.get('deeper', [])) for u in units)} deeper, {sum(len(u.get('quiz', [])) for u in units)} checkpoint positions, "
      f"{sum(len(s) for u in units for s in u.get('sets', []))}+{sum(len(u.get('check', [])) for u in units)} threat positions")
