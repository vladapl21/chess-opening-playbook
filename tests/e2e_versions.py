"""Checks for the two things that keep the course repeatable.

1. The claims check (pipeline/lint_claims.py) on boards where the answer is known: a bishop that comes at a knight
   with the pawn still behind it is not a pin; the same bishop with the queen behind the knight is.
2. Line versions in the page: a progress record made before a line's moves changed counts as due again, says so,
   and a clean run on the new moves replaces it. Two copies of a record merge to the one made on the current moves."""
import json, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
from e2e_white import drag, click_move, launch, URL, out
errors = []

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'pipeline'))
import paths                                              # noqa: E402  (puts pipeline/ and content/ on the path)
import chess                                              # noqa: E402
from lint_claims import pins, lint_labels, lint_pins, lint_repeats     # noqa: E402


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


# ---- 1. the claims check
no_pin = after('d4 d5 c4 c6 Nf3 Nf6 Bg5')            # the e-pawn is still behind the knight: nothing is pinned
assert not pins(no_pin), [chess.square_name(a) + '<' + chess.square_name(b) for a, b in pins(no_pin)]
real = after('d4 d5 c4 e6 Nc3 Nf6 Bg5')              # the e-pawn has moved: the queen is behind the knight
assert (chess.F6, chess.G5) in pins(real)
king = after('e4 e5 Nf3 Nc6 Bb5 d6 d4')              # knight pinned to the king
assert (chess.C6, chess.B5) in pins(king)
for side in ('white', 'black'):
    assert lint_repeats(side) == [] and lint_pins(side) == [] and lint_labels(side) == [], side
print('claims: bishop at the knight with the pawn behind it is no pin; both books clean')

# ---- 2. line versions
vers = json.load(open(paths.DATA / 'line_versions.json'))
CHANGED, SAME = 'bsl-slow2', 'bsl-slow'
assert vers[CHANGED][0] == 2 and vers[SAME][0] == 1, (vers[CHANGED], vers[SAME])
SEED = """(() => { const K = 'italian-playbook-progress-v1'; if (sessionStorage.getItem('seeded')) return; sessionStorage.setItem('seeded', '1');
  const now = Date.now(), day = 864e5, old = {box: 4, seen: 5, clean: 4, last: now - 3 * day, due: now + 20 * day};
  localStorage.setItem(K, JSON.stringify({lines: {'%s': old, '%s': old}, puz: {}, updated: now - 3 * day,
    course: {u: {'w-italian': {idea: 1, cp: 6, pass: 1}}, seen: {}}})); })()""" % (CHANGED, SAME)

with sync_playwright() as p:
    b = launch(p)
    ctx = b.new_context(viewport={'width': 1280, 'height': 900}); ctx.add_init_script(SEED)
    pg = ctx.new_page(); hook(pg)
    pg.goto(URL); pg.wait_for_timeout(1200)
    st = pg.evaluate(f"({{ver: VER['{CHANGED}'], stale: Prog.stale('{CHANGED}'), same: Prog.stale('{SAME}'), rec: Prog.rec('{CHANGED}'), keep: Prog.rec('{SAME}').box,"
                     f" due: Prog.dueCount('b'), n: Prog.staleCount(), clean: lineClean('{CHANGED}')}})")
    print('old record on a changed line:', st)
    assert st['ver'] == 2 and st['stale'] and not st['same'] and st['rec']['changed'] and st['rec']['box'] == 0 and st['keep'] == 4
    assert st['due'] == 1 and st['n'] == 1 and not st['clean']
    note = pg.inner_text('#changed'); print('course note:', note.replace('\n', ' | '))
    assert note.startswith('1 line you drilled has changed.')
    pg.screenshot(path=out + 'v_course_note.png')

    pg.click('[data-unit="b-slav"]'); pg.wait_for_timeout(500)
    row = pg.inner_text(f'[data-udrill="{CHANGED}"]').replace('\n', ' | '); print('unit row:', row)
    assert 'Changed' in row and 'Changed' not in pg.inner_text(f'[data-udrill="{SAME}"]')
    pg.screenshot(path=out + 'v_unit.png', full_page=True)

    pg.evaluate("go('course')"); pg.wait_for_timeout(400)
    pg.click('#changedGo'); pg.wait_for_timeout(900)
    assert pg.evaluate('[S.view, S.drill.id, SIDE]') == ['drill', CHANGED, 'b']
    txt = pg.inner_text('.dpanel'); print('drill panel:', txt.replace('\n', ' | ')[:230])
    assert 'CHANGED LINE' in txt.upper() and 'has changed since you last drilled it' in txt and 'arrow shows' in txt
    pg.screenshot(path=out + 'v_drill.png')
    assert drill_clean(pg) == 'done'
    rec = pg.evaluate(f"Prog.d.lines['{CHANGED}']"); print('new record:', {k: rec[k] for k in ('v', 'box', 'seen', 'clean')})
    assert rec['v'] == 2 and rec['box'] == 1 and rec['seen'] == 1 and rec['clean'] == 1
    assert pg.evaluate(f"!Prog.stale('{CHANGED}') && Prog.staleCount() === 0 && lineClean('{CHANGED}')")
    pg.evaluate("go('course')"); pg.wait_for_timeout(400)
    assert pg.query_selector('#changed') is None

    # two devices: the copy made on the current moves wins, even when the old copy was touched later
    m = pg.evaluate(f"""(() => {{ const t = Date.now(), a = {{lines: {{'{CHANGED}': {{box: 5, clean: 9, last: t}}}}, puz: {{}}}},
        b = {{lines: {{'{CHANGED}': {{v: 2, box: 1, clean: 1, last: t - 1e6}}}}, puz: {{}}}};
        return [mergeProg(a, b).lines['{CHANGED}'].box, mergeProg(b, a).lines['{CHANGED}'].box]; }})()""")
    print('merge old + new copy:', m); assert m == [1, 1]

    # phone width: the note wraps, the page does not scroll sideways
    ctx2 = b.new_context(viewport={'width': 390, 'height': 844}); ctx2.add_init_script(SEED)
    ph = ctx2.new_page(); hook(ph); ph.goto(URL); ph.wait_for_timeout(1000)
    w = ph.evaluate('document.documentElement.scrollWidth'); print('phone scrollWidth', w); assert w <= 390
    ph.screenshot(path=out + 'v_phone.png')
    b.close()

print('ERRORS:', errors); assert not errors
print('version checks passed')
