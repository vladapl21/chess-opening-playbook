"""Every count the README quotes, worked out again from the built books and compared with what is written there.

A new line, lesson, system or unit changes these numbers, and nothing else reminds anyone to change the text. This check
fails when a quoted number is out of date and names it; `python3 pipeline/lint_counts.py --write` puts the numbers right.
`assemble.py` runs it once the page is written and ends with exit code 3 on a stale count, so a build can't pass by it.
The page never quotes a count of its own: what it shows (the Sandbox's "lines met here", a unit's lessons, the lines
due) is counted from the book on the page, which `e2e_sandbox_switch.py` checks.

The house playbook is the first system in every slot; the library is everything.
  At a glance      chapters, lessons, lines you can drill, positions on those lines, positions with a note, lessons with
                   a written plan, lines that end with a plan, game reviews, missed shots, patterns, cards at a glance
  the course       units, core and optional lessons, checkpoint positions, the skill units, deep dives and their parts
  the library      chapters, lessons and lines per book, units and deep dives
  Systems          chapters, lessons and lines of every system that isn't the first in its slot
  the shop         pieces on a day's shelf, pieces for sale, pieces that need a badge (read from app/product.js)"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'content'))
import plans  # noqa: E402  (the written plans: W and B by lesson, LW and LB by line)

BOOK = {s: json.load(open(ROOT / f'data/build/data_{s}.json')) for s in ('white', 'black')}
COURSE = json.load(open(ROOT / 'data/build/data_course.json'))
LINE_PLANS = json.load(open(ROOT / 'data/line_plans.json'))


def pack_lessons(d, chapters):
    parts = {p for c in d['chapters'] if c['id'] in chapters for p in c['parts']}
    return [l for l in d['lessons'] if l['part'] in parts]


def house(side):
    """The book as the house player has it: the default pack of every slot, plus the chapters outside the slots."""
    d = BOOK[side]; packs = d.get('packs') or {}
    chapters = [c['id'] for c in d['chapters'] if not c.get('slot') or c.get('pack') == packs[c['slot']]['default']]
    lessons = pack_lessons(d, chapters); ids = {l['id'] for l in lessons}
    lines = [l for l in d['lines'] if l['lesson'] in ids]
    me = 1 if side == 'white' else 0; N = d['nodes']
    # a line that shows a mistake of your own on purpose is studied, not drilled (drillableOf in the template)
    drill = [l for l in lines if not any('warn' in (N[i].get('g') or []) and N[i].get('w') == me for i in l['n'])]
    used = {i for l in lines for i in l['n']}
    written = plans.W if side == 'white' else plans.B
    return dict(chapters=len(chapters), lessons=len(lessons), drill=len(drill), positions=len(used),
                noted=sum(1 for i in used if N[i].get('t')), planned=sum(1 for l in lessons if l['id'] in written),
                line_plans=sum(1 for l in lines if (l['main'] and l['lesson'] in written) or l['id'] in LINE_PLANS or l['id'] in plans.LW or l['id'] in plans.LB),
                games=len(d['games']), puzzles=len(d['puzzles']), patterns=len(d.get('insights') or []),
                cards=sum(1 for r in d['cheat'] if r.get('lesson') in ids), ids=ids)


def shop():
    """The shop as app/product.js has it: a day's shelf (SHELF), the pieces with a price, and the ones behind a badge."""
    js = (ROOT / 'app/product.js').read_text()
    shelf = sum(int(x) for x in re.findall(r':\s*(\d+)', re.search(r'const SHELF = \{([^}]*)\}', js).group(1)))
    a = js.index('const SHOP = ['); rows = re.findall(r"\{id: '[^']+', slot: '[^']+'[^\n]*", js[a:js.index('\n];', a)])
    priced = [r for r in rows if re.search(r'price: [1-9]', r)]
    return dict(shelf=shelf, priced=len(priced), badge=sum(1 for r in priced if 'needs:' in r))


def numbers():
    H = {'w': house('white'), 'b': house('black')}
    units = COURSE['units']
    mine = [u for u in units if u['kind'] != 'lessons' or all(l in H[u['side']]['ids'] for l in u['lessons'])]
    opening = [u for u in mine if u['kind'] == 'lessons']; skill = {u['id']: u for u in mine if u['kind'] != 'lessons'}
    names = {u['id'] for u in mine}
    deep = [d for d in COURSE['deep'] if d['base'] in names]; dn = {d['id'] for d in deep}
    parts = [p for p in COURSE['deepUnits'] if p['deep'] in dn]
    positions = lambda u: sum(len(s) for s in u['sets']) + len(u['check'])
    systems = {}
    for side in ('white', 'black'):
        d = BOOK[side]
        for slot, P in d['packs'].items():
            for pk, chs in P['packs'].items():
                ls = {l['id'] for l in pack_lessons(d, chs)}
                systems[(slot, pk)] = dict(chapters=len(chs), lessons=len(ls), lines=sum(1 for l in d['lines'] if l['lesson'] in ls), first=pk == P['default'])
    return dict(H=H, units=len(mine), opening=len(opening), core=sum(len(u['lessons']) for u in opening),
                optional=sum(len(u.get('deeper') or []) for u in opening), checkpoints=sum(len(u.get('quiz') or []) for u in opening),
                skill=len(skill), threats=positions(skill['threats']), finish=positions(skill['finish']), endings=positions(skill['endings']),
                deep=len(deep), parts=len(parts), deep_checks=sum(len(p.get('quiz') or []) for p in parts),
                lib={s: (len(BOOK[s]['chapters']), len(BOOK[s]['lessons']), len(BOOK[s]['lines'])) for s in BOOK},
                all_units=len(units), all_deep=len(COURSE['deep']), systems=systems, shop=shop())


WORDS = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen',
         'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty']
word = lambda n: WORDS[n].capitalize() if n < len(WORDS) else str(n)
num = lambda n: f'{n:,}' if n else '–'

# the rows of "At a glance" this check owns: label, key in house()
ROWS = [('Chapters (openings)', 'chapters'), ('Lessons', 'lessons'), ('Lines you can drill', 'drill'), ('Positions on those lines', 'positions'),
        ('Positions with a written note', 'noted'), ('Lessons with a written plan', 'planned'), ('Lines that end with a plan', 'line_plans'),
        ('Game reviews', 'games'), ('Missed-shot puzzles', 'puzzles'), ('Patterns across games', 'patterns'), ('Cards at a glance', 'cards')]
# rows that used to carry these numbers under another label
OLD = {'Positions in the tree': 'Positions on those lines', 'Lessons that end with a plan': 'Lessons with a written plan'}
# the system rows of the Systems table: (slot, pack) and a word that is only in that row
SYSTEMS = [(('white', 'd4'), 'The London'), (('white', 'flank'), 'The English'), (('blackE4', 'caro'), 'Caro-Kann'), (('blackE4', 'sicilian'), 'Sicilian'),
           (('blackE4', 'scandi'), 'Scandinavian'), (('blackD4', 'kid'), "King's Indian"),
           (('white', 'e4'), 'Open with the e-pawn'), (('blackE4', 'e5'), 'Meet it head-on'), (('blackD4', 'slav'), 'The Slav setup')]


def table_row(label, w, b): return f'| {label:<33} | {w:<25} | {b:<32} |'


def expected(n):
    """(what it is, a pattern with one group per number, the numbers) for everything quoted in prose."""
    W, B = n['lib']['white'], n['lib']['black']
    return [
        ('units in the course', r'The course on top of both books has \*\*(\d+) units\*\*', [n['units']]),
        ('opening units', r'(\w+) are opening units: (\d+) core lessons, (\d+) optional ones and (\d+) checkpoint positions',
         [word(n['opening']), n['core'], n['optional'], n['checkpoints']]),
        ('skill units', r'(\w+) are skill units made of positions from my own games: (\d+) threats I walked into, (\d+) winning positions I let slip and (\d+) endings',
         [word(n['skill']), n['threats'], n['finish'], n['endings']]),
        ('deep dives', r'a library of \*\*(\d+) deep dives\*\*: the optional lessons in (\d+) parts, with (\d+) more checkpoint positions', [n['deep'], n['parts'], n['deep_checks']]),
        ('the library', r'the books have (\d+) chapters, (\d+) lessons and (\d+) lines for White, (\d+) chapters, (\d+) lessons and (\d+) lines for Black, and the course has (\d+) units and (\d+) deep dives',
         [*W, *B, n['all_units'], n['all_deep']]),
        ('the daily shop', r'(\d+) pieces a day \(two hats, two colours, one pair of glasses, one thing for the neck\) out of (\d+)', [n['shop']['shelf'], n['shop']['priced']]),
        ('pieces behind a badge', r'(\w+) pieces need a badge first', [word(n['shop']['badge'])]),
    ]


def system_cell(S):
    if S['first']: return f"the first system; {S['chapters']} chapters"
    return (f"{S['chapters']} chapters, " if S['chapters'] > 1 else '') + f"{S['lessons']} lessons, {S['lines']} lines"


def run(write=False):
    p = ROOT / 'README.md'; text = p.read_text(); n = numbers(); bad = []
    lines = text.split('\n')
    # ---- At a glance
    for label, key in ROWS:
        want = table_row(label, num(n['H']['w'][key]), num(n['H']['b'][key]))
        at = [i for i, l in enumerate(lines) if re.match(r'\|\s*' + re.escape(label) + r'\s*\|', l)]
        old = [i for i, l in enumerate(lines) for o, new in OLD.items() if new == label and re.match(r'\|\s*' + re.escape(o) + r'\s*\|', l)]
        if not at and old: at = old
        if not at:
            prev = [i for i, l in enumerate(lines) if re.match(r'\|\s*' + re.escape(ROWS[ROWS.index((label, key)) - 1][0]) + r'\s*\|', l)]
            bad.append(f'At a glance has no row "{label}"')
            if write and prev: lines.insert(prev[0] + 1, want)
            continue
        cells = [c.strip() for c in lines[at[0]].strip('|').split('|')]
        if cells != [label, num(n['H']['w'][key]), num(n['H']['b'][key])]:
            bad.append(f'At a glance, {label}: README has {cells[1]} and {cells[2]}, the books have {num(n["H"]["w"][key])} and {num(n["H"]["b"][key])}')
            if write: lines[at[0]] = want
    text = '\n'.join(lines)
    # ---- the course and the library, in prose
    for what, pat, want in expected(n):
        m = re.search(pat, text)
        if not m: bad.append(f'{what}: the sentence is gone from the README (pattern: {pat[:60]}…)'); continue
        if [str(g) for g in m.groups()] != [str(x) for x in want]:
            bad.append(f'{what}: README has {", ".join(m.groups())}; it is {", ".join(str(x) for x in want)}')
            if write:
                s = m.group(0)
                for k in range(len(want), 0, -1): s = s[:m.start(k) - m.start()] + str(want[k - 1]) + s[m.end(k) - m.start():]
                text = text[:m.start()] + s + text[m.end():]
    # ---- Systems
    lines = text.split('\n'); top = next((i for i, l in enumerate(lines) if re.match(r'\|\s*Slot\s*\|', l)), len(lines))
    for key, name in SYSTEMS:
        S = n['systems'][key]; want = system_cell(S)
        at = [i for i, l in enumerate(lines) if i > top and l.startswith('|') and f'**{name}**' in l]
        if not at: bad.append(f'Systems has no row for {name}'); continue
        cells = lines[at[0]].rstrip().rstrip('|').split('|')
        if cells[-1].strip() != want:
            bad.append(f'Systems, {name}: README has "{cells[-1].strip()}", it is "{want}"')
            if write: cells[-1] = f' {want} '; lines[at[0]] = '|'.join(cells) + '|'
    text = '\n'.join(lines)
    if write and bad: p.write_text(text)
    return n, bad


if __name__ == '__main__':
    write = '--write' in sys.argv
    n, bad = run(write)
    H = n['H']
    print('house books:', {s: {k: v for k, v in H[s].items() if k != 'ids'} for s in H})
    print('course:', {k: n[k] for k in ('units', 'opening', 'core', 'optional', 'checkpoints', 'threats', 'finish', 'endings', 'deep', 'parts', 'deep_checks')})
    print('library:', n['lib'], n['all_units'], 'units,', n['all_deep'], 'deep dives')
    for b in bad: print(('fixed: ' if write else 'STALE: ') + b)
    if bad and not write:
        print(f'\n{len(bad)} counts in the README are out of date. Run: python3 pipeline/lint_counts.py --write')
        sys.exit(1)
    if write:
        n2, left = run(False)
        assert not left, left
    print('counts check passed' if not bad else 'README counts rewritten')
