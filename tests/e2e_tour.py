"""The tour: it starts by itself for a player who hasn't taken it and can't be skipped (no close button; Escape and taps
outside the card do nothing). A step that asks for a tap goes on once it's done, by hand or with Show me; Back goes a step
back; Fast forward plays the rest by itself: the arrow's move in Play along, a punished slip from memory, Play on with
the engine, a lesson's list of the other side's answers. It leaves no progress behind, is marked in the progress record
and on the device, doesn't come back after a reload, and Settings plays it again (ending where it began). Phone width in
dark mode: the card stays on the screen and nothing scrolls sideways. Over local HTTP, the website's own page."""
import sys, json, time
sys.path.insert(0, __import__('os').path.dirname(__file__))
from playwright.sync_api import sync_playwright
from e2e_white import launch, out
from serve import Site
site = Site(docs=True); URL = site.start()
errors = []


def hook(pg):
    pg.on('pageerror', lambda e: errors.append(f'pageerror: {e}'))
    pg.on('console', lambda m: errors.append(f'console: {m.text}') if m.type == 'error' and 'ERR_' not in m.text else None)


def step(pg):
    return pg.evaluate("Tour.on ? [Tour.k, Tour.words(Tour.cur()).h] : null")


def ff_to_end(pg, seen, limit=180):
    """Fast forward until the tour closes, noting what each step showed."""
    pg.click('[data-tour="fast"]'); t0 = time.time(); last = None
    while time.time() - t0 < limit:
        st = pg.evaluate("""Tour.on ? {k: Tour.k, h: Tour.words(Tour.cur()).h, view: S.view, ring: !!Tour.target(),
          along: !!(S.drill && S.drill.guided && S.drill.tour && LINES[S.drill.id].n.slice(S.drill.s0 + 1, S.drill.i + 1).some(i => isMine(N[i]))),
          pun: !!document.querySelector('#dpanel .feedback .pun'), arrow: !!(S.drill && S.drill.tour && !S.drill.guided && S.drill.hint),
          opts: !!document.querySelector('.opts .opt')} : null""")
        if not st: return time.time() - t0
        if st['k'] != last: last = st['k']; seen.append(st['h'])
        for f in ('along', 'pun', 'arrow', 'opts'):
            if st[f]: seen.append('#' + f)
        if st['view'] == 'explore': seen.append('#explore')
        pg.wait_for_timeout(200)
    raise AssertionError('the tour did not finish on fast forward: ' + str(step(pg)))


with sync_playwright() as p:
    b = launch(p, tour=True)
    ctx = b.new_context(viewport={'width': 1280, 'height': 860}); pg = ctx.new_page(); hook(pg)
    pg.goto(URL); pg.wait_for_function('Tour.on', timeout=8000); pg.wait_for_timeout(400)
    keep = "JSON.stringify({lines: Prog.d.lines || {}, course: Prog.d.course || {}, days: Prog.d.days || {}, puz: Prog.d.puz || {}, sb: Prog.d.sb || {}})"
    before, xp0 = pg.evaluate(keep), pg.evaluate('Level.xp()')
    n = pg.evaluate('Tour.steps.length'); print('tour steps:', n, '| first:', step(pg)); assert n >= 20, n

    # ---- step one: pick the coach; the card speaks as the one picked
    assert pg.locator('.twcard .coachpick [data-coachwho]').count() == 3
    pg.click('.twcard [data-coachwho="rook"]'); pg.wait_for_timeout(300)
    assert pg.evaluate('SET.who') == 'rook' and 'Rocco' in pg.inner_text('.twcard'), pg.inner_text('.twcard')
    pg.screenshot(path=out + 't_hello.png')
    # ---- it can't be skipped: nothing to close it, Escape only says so, taps outside the card do nothing
    assert pg.locator('.twcard .x, .twcard [aria-label="Close"], .twcard [data-skip]').count() == 0
    pg.keyboard.press('Escape'); pg.wait_for_timeout(200)
    assert pg.evaluate('Tour.on') and "can't be skipped" in pg.inner_text('.twcard')
    v0 = pg.evaluate('S.view'); tab = pg.locator('.tabs [data-view="shop"]').bounding_box()
    pg.mouse.click(tab['x'] + tab['width'] / 2, tab['y'] + tab['height'] / 2); pg.mouse.click(20, 840); pg.wait_for_timeout(300)
    assert pg.evaluate('[Tour.on, Tour.k, S.view]') == [True, 0, v0], pg.evaluate('[Tour.on, Tour.k, S.view]')

    # ---- a step that asks for a tap: done by hand, it goes on by itself
    pg.click('[data-tour="next"]'); pg.wait_for_function('Tour.k === 1'); pg.wait_for_timeout(500)
    assert 'Tap Black' in pg.inner_text('.twcard') and pg.inner_text('[data-tour="next"]') == 'Show me'
    ring = pg.evaluate("(() => { const a = document.querySelector('.twring').getBoundingClientRect(), b = document.querySelector('.top .sidesw').getBoundingClientRect(); return a.left <= b.left && a.right >= b.right && a.top <= b.top && a.bottom >= b.bottom; })()")
    assert ring, 'the ring goes round the colour switch'
    pg.click('.top .sidesw [data-side="b"]'); pg.wait_for_function('Tour.k === 2', timeout=5000)
    assert pg.evaluate('SIDE') == 'b'
    pg.screenshot(path=out + 't_side.png')
    # ---- Show me: the coach taps it
    pg.click('[data-tour="next"]'); pg.wait_for_function('Tour.k === 3 && SIDE === "w"', timeout=5000)
    # ---- inside the spotlight of a step that only explains, the page can't be tapped either
    tab = pg.locator('.tabs [data-view="drill"]').bounding_box()
    pg.mouse.click(tab['x'] + tab['width'] / 2, tab['y'] + tab['height'] / 2); pg.wait_for_timeout(300)
    assert pg.evaluate('[Tour.k, S.view]') == [3, v0]
    # ---- Back: the step before, set up again
    pg.click('[data-tour="back"]'); pg.wait_for_function('Tour.k === 2 && SIDE === "b"', timeout=5000)
    pg.click('[data-tour="next"]'); pg.wait_for_function('Tour.k === 3 && SIDE === "w"', timeout=5000)

    # ---- fast forward: the rest plays by itself
    seen = []; secs = ff_to_end(pg, seen)
    titles = [s for s in seen if not s.startswith('#')]; marks = set(s for s in seen if s.startswith('#'))
    print(f'fast forward: {len(set(titles))} steps in {secs:.0f} s; seen:', sorted(marks))
    assert {'#along', '#pun', '#arrow', '#explore', '#opts'} <= marks, marks
    assert {'Play along', 'Play on with the engine', 'The explore board', 'Your games', 'The Sandbox', 'Settings'} <= set(titles), titles

    # ---- nothing from the tour is kept as progress; the tour itself is
    assert pg.evaluate(keep) == before and pg.evaluate('Level.xp()') == xp0, 'the tour leaves no progress behind'
    got = pg.evaluate("[!!(Prog.d.tour && Prog.d.tour.done), !!JSON.parse(localStorage.getItem(PKEY)).tour, localStorage.getItem('playbook-tour'), S.view, SIDE, SET.who, !!document.getElementById('tour')]")
    print('after the tour:', got); assert got == [True, True, 'done', 'course', 'w', 'rook', False], got
    pg.reload(); pg.wait_for_timeout(2600)
    assert not pg.evaluate('Tour.on'), 'taken once, it does not start again'

    # ---- Settings: take it again; it ends where it began
    pg.evaluate("go('games')"); pg.wait_for_timeout(300)
    pg.click('#setBtn'); pg.wait_for_timeout(300); pg.click('[data-tourgo]'); pg.wait_for_function('Tour.on', timeout=4000)
    assert pg.evaluate('[Tour.replay, Tour.k]') == [True, 0]
    ff_to_end(pg, [])
    assert pg.evaluate('[S.view, Tour.on]') == ['games', False], pg.evaluate('[S.view, Tour.on]')
    ctx.close()

    # ---- phone, dark: the card stays on the screen, nothing scrolls sideways
    ph = b.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True, color_scheme='dark'); q = ph.new_page(); hook(q)
    q.goto(URL); q.wait_for_function('Tour.on', timeout=8000); q.wait_for_timeout(500)
    for k in range(9):
        q.wait_for_timeout(700)
        m = q.evaluate("(() => { const r = document.querySelector('.twcard').getBoundingClientRect(); return {l: r.left, r: r.right, t: r.top, b: r.bottom, w: document.documentElement.scrollWidth, k: Tour.k}; })()")
        assert m['l'] >= 0 and m['r'] <= 390 and m['t'] >= 0 and m['b'] <= 844 and m['w'] <= 390, m
        if k in (0, 6): q.screenshot(path=out + f't_phone_{k}.png')
        k0 = q.evaluate('Tour.k'); q.tap('[data-tour="next"]')   # Next, or Show me on a step that asks for a tap
        q.wait_for_function(f'Tour.k !== {k0}', timeout=8000); q.wait_for_timeout(300)
    print('phone: the card on the screen through', q.evaluate('Tour.k'), 'steps')
    ph.close()
    b.close()

site.stop()
print('ERRORS:', errors[:10]); assert not errors
print('tour checks passed')
