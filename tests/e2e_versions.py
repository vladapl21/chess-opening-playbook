"""Checks for the two things that keep the course repeatable.

1. The claims check (pipeline/lint_claims.py) on boards where the answer is known: a bishop that comes at a knight
   with the pawn still behind it is not a pin; the same bishop with the queen behind the knight is.
2. Line versions in the page: a progress record made before a line's moves changed stands as it was, and nothing on
   the page says the line changed; the next run counts on top of it and stamps the new moves. Two copies of a record
   merge to the one made on the current moves."""
import json, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
from e2e_white import drag, click_move, launch, URL, out
errors = []

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'pipeline'))
import paths                                              # noqa: E402  (puts pipeline/ and content/ on the path)
try:
    import chess                                          # noqa: E402
    from lint_claims import pins, lint_labels, lint_pins, lint_repeats     # noqa: E402
except ImportError:                                       # no python-chess here: see part 1
    chess = None


def hook(pg):
    pg.on('pageerror', lambda e: errors.append(f'pageerror: {e}'))
    pg.on('console', lambda m: errors.append(f'console {m.type}: {m.text}') if m.type == 'error' and 'ERR_' not in m.text else None)


def drill_clean(pg):
    """Finish the running drill line without a slip."""
    k = '1' if pg.evaluate('ME') == 1 else '8'
    for _ in range(150):
        st = pg.evaluate("({state: S.drill.state, busy: S.drill.busy})")
        if st['state'] == 'done': break
        if st['busy']: pg.wait_for_timeout(200); continue
        u = pg.evaluate("N[LINES[S.drill.id].n[S.drill.i + 1]].u")
        if u in (f'e{k}g{k}', f'e{k}c{k}'): drag(pg, f'e{k}', f'h{k}' if u[2] == 'g' else f'a{k}')
        else: click_move(pg, u[:2], u[2:4])
        pg.wait_for_timeout(800)
    return pg.evaluate("S.drill.state")


def after(sans):
    b = chess.Board()
    for s in sans.split(): b.push_san(s)
    return b


# ---- 1. the claims check. Without python-chess it can't run; the books must then be the ones it last passed
# (data/build/lint.ok, written by assemble.py), the same rule assemble.py follows.
if chess:
    no_pin = after('d4 d5 c4 c6 Nf3 Nf6 Bg5')            # the e-pawn is still behind the knight: nothing is pinned
    assert not pins(no_pin), [chess.square_name(a) + '<' + chess.square_name(b) for a, b in pins(no_pin)]
    real = after('d4 d5 c4 e6 Nc3 Nf6 Bg5')              # the e-pawn has moved: the queen is behind the knight
    assert (chess.F6, chess.G5) in pins(real)
    king = after('e4 e5 Nf3 Nc6 Bb5 d6 d4')              # knight pinned to the king
    assert (chess.C6, chess.B5) in pins(king)
    for side in ('white', 'black'):
        assert lint_repeats(side) == [] and lint_pins(side) == [] and lint_labels(side) == [], side
    print('claims: bishop at the knight with the pawn behind it is no pin; both books clean')
else:
    import hashlib
    books = hashlib.sha256((paths.BUILD / 'data_white.json').read_bytes() + (paths.BUILD / 'data_black.json').read_bytes()).hexdigest()
    assert (paths.BUILD / 'lint.ok').read_text().strip() == books, 'python-chess is missing and the books changed since the claims check last passed'
    print('claims: python-chess is missing here; the books are the ones the check last passed')

# ---- 2. line versions
vers = json.load(open(paths.DATA / 'line_versions.json'))
# a Black unit of the house course that drills a line whose moves have changed since it was first released and one
# whose moves never have (most lines changed when the build began to play them on); the units before it count as passed
units = json.load(open(paths.BUILD / 'data_course.json'))['units']
UNIT, CHANGED, SAME = 'b-italian', 'bi-qxd2', 'bi-main'
U = next(u for u in units if u['id'] == UNIT); assert {CHANGED, SAME} <= set(U['lines']), U['lines']
V = vers[CHANGED][0]
assert V >= 2 and vers[SAME][0] == 1, (vers[CHANGED], vers[SAME])
PASSED = json.dumps({u['id']: {'idea': 1, 'cp': 6, 'pass': 1} for u in units[:units.index(U)]})
SEED = """(() => { const K = 'italian-playbook-progress-v1'; if (sessionStorage.getItem('seeded')) return; sessionStorage.setItem('seeded', '1');
  const now = Date.now(), day = 864e5, old = {box: 4, seen: 5, clean: 4, last: now - 3 * day, due: now + 20 * day};
  localStorage.setItem(K, JSON.stringify({lines: {'%s': old, '%s': old}, puz: {}, updated: now - 3 * day,
    course: {u: %s, seen: {}}})); })()""" % (CHANGED, SAME, PASSED)

with sync_playwright() as p:
    b = launch(p)
    ctx = b.new_context(viewport={'width': 1280, 'height': 900}); ctx.add_init_script(SEED)
    pg = ctx.new_page(); hook(pg)
    pg.goto(URL); pg.wait_for_timeout(1200)
    st = pg.evaluate(f"({{ver: VER['{CHANGED}'], stale: Prog.stale('{CHANGED}'), same: Prog.stale('{SAME}'), rec: Prog.rec('{CHANGED}'), keep: Prog.rec('{SAME}').box,"
                     f" due: Prog.dueCount('b'), clean: lineClean('{CHANGED}')}})")
    print('old record on a changed line:', st)
    # the record made on the old moves stands as it was: same box, same due date, still clean, nothing due because of it
    assert st['ver'] == V and st['stale'] and not st['same'] and st['rec']['box'] == 4 and 'changed' not in st['rec'] and st['keep'] == 4
    assert st['due'] == 0 and st['clean']
    # and nothing on the page says so: no note on the course, no label in the unit, no word in the drill panel
    assert pg.query_selector('#changed') is None and 'changed' not in pg.inner_text('#view').lower()
    pg.screenshot(path=out + 'v_course_note.png')
    pg.click(f'[data-unit="{UNIT}"]'); pg.wait_for_timeout(500)
    row = pg.inner_text(f'[data-udrill="{CHANGED}"]').replace('\n', ' | '); print('unit row:', row)
    assert 'Changed' not in row and row.split('|')[-1].strip() == pg.inner_text(f'[data-udrill="{SAME}"]').split('\n')[-1].strip(), 'both rows read the same'
    pg.screenshot(path=out + 'v_unit.png', full_page=True)
    pg.evaluate(f"useSide('b'); startDrillLine('{CHANGED}')"); pg.wait_for_timeout(900)
    txt = pg.inner_text('.dpanel'); print('drill panel:', txt.replace('\n', ' | ')[:160])
    assert 'changed' not in txt.lower()
    assert drill_clean(pg) == 'done'
    rec = pg.evaluate(f"Prog.d.lines['{CHANGED}']"); print('record after a clean run:', {k: rec.get(k) for k in ('v', 'box', 'seen', 'clean')})
    # the run counts on top of the old record, and stamps the moves it was played on
    assert rec['v'] == V and rec['box'] == 5 and rec['seen'] == 6 and rec['clean'] == 5 and 'ps' not in rec
    assert pg.evaluate(f"!Prog.stale('{CHANGED}') && lineClean('{CHANGED}')")

    # two devices: the copy made on the current moves wins, even when the old copy was touched later
    m = pg.evaluate(f"""(() => {{ const t = Date.now(), a = {{lines: {{'{CHANGED}': {{box: 5, clean: 9, last: t}}}}, puz: {{}}}},
        b = {{lines: {{'{CHANGED}': {{v: {V}, box: 1, clean: 1, last: t - 1e6}}}}, puz: {{}}}};
        return [mergeProg(a, b).lines['{CHANGED}'].box, mergeProg(b, a).lines['{CHANGED}'].box]; }})()""")
    print('merge old + new copy:', m); assert m == [1, 1]

    # phone width: the page does not scroll sideways
    ctx2 = b.new_context(viewport={'width': 390, 'height': 844}); ctx2.add_init_script(SEED)
    ph = ctx2.new_page(); hook(ph); ph.goto(URL); ph.wait_for_timeout(1000)
    w = ph.evaluate('document.documentElement.scrollWidth'); print('phone scrollWidth', w); assert w <= 390
    ph.screenshot(path=out + 'v_phone.png')
    b.close()

print('ERRORS:', errors); assert not errors
print('version checks passed')
