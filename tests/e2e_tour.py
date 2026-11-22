"""The tour is three steps: pick a coach, play one move, see the button that leads on. It starts by itself for a player
who hasn't taken it, has no close button and no Fast forward, and holds Next for a moment behind a bar (not on a step
come back to). The step that asks for a move goes on once it's played, by hand or with Show me; Back goes a step back.
It says little (a word count is checked) and nothing about the shop. Finished, it leaves no progress behind, is marked
in the progress record and on the device, and doesn't come back after a reload. Settings plays it again without the coach
pick and without the bar, ending where it began. The rest of the app is explained where it is met: the coach has one
short tip for each place, said once on the first visit. Phone width in dark mode: the card is a sheet across the bottom
of the screen, never over the thing it points at, and nothing scrolls sideways. Over local HTTP, the website's own page."""
import sys, json, time
sys.path.insert(0, __import__('os').path.dirname(__file__))
from playwright.sync_api import sync_playwright
from e2e_white import launch, out, click_move
from serve import Site
site = Site(docs=True); URL = site.start()
errors = []


def hook(pg):
    pg.on('pageerror', lambda e: errors.append(f'pageerror: {e}'))
    pg.on('console', lambda m: errors.append(f'console: {m.text}') if m.type == 'error' and 'ERR_' not in m.text else None)


def step(pg):
    return pg.evaluate("Tour.on ? [Tour.k, Tour.words(Tour.cur()).h] : null")


with sync_playwright() as p:
    b = launch(p, tour=True)
    ctx = b.new_context(viewport={'width': 1280, 'height': 860}); pg = ctx.new_page(); hook(pg)
    pg.goto(URL); pg.wait_for_function('Tour.on', timeout=8000); pg.wait_for_timeout(400)
    keep = "JSON.stringify({lines: Prog.d.lines || {}, course: Prog.d.course || {}, days: Prog.d.days || {}, puz: Prog.d.puz || {}, sb: Prog.d.sb || {}})"
    before, xp0 = pg.evaluate(keep), pg.evaluate('Level.xp()')
    n = pg.evaluate('Tour.steps.length'); print('tour steps:', n, '| first:', step(pg)); assert n == 3, n
    said = pg.evaluate("Tour.steps.map(st => { const w = Tour.words(st); return [w.h].concat(w.say, st.act ? [st.act.ask] : []).join(' '); }).join(' ')")
    print('all it says:', said); assert len(said.split()) <= 45 and 'shop' not in said.lower() and 'crate' not in said.lower(), said

    # ---- step one: pick the coach
    assert pg.locator('.twcard .coachpick [data-coachwho]').count() == 3 and 'Pick your coach' in pg.inner_text('.twcard')
    pg.click('.twcard [data-coachwho="rook"]'); pg.wait_for_timeout(300)
    assert pg.evaluate('SET.who') == 'rook' and 'Rocco' in pg.inner_text('.twcard .twstep'), pg.inner_text('.twcard')
    pg.screenshot(path=out + 't_hello.png')
    # ---- nothing to close it, Escape only says how short it is, taps outside the card do nothing; no Fast forward
    assert pg.locator('.twcard .x, .twcard [aria-label="Close"], .twcard [data-skip], [data-tour="fast"]').count() == 0
    pg.keyboard.press('Escape'); pg.wait_for_timeout(200)
    assert pg.evaluate('Tour.on') and "Three steps and you're in" in pg.inner_text('.twcard')
    v0 = pg.evaluate('S.view'); tab = pg.locator('.tabs [data-view="shop"]').bounding_box()
    pg.mouse.click(tab['x'] + tab['width'] / 2, tab['y'] + tab['height'] / 2); pg.mouse.click(20, 840); pg.wait_for_timeout(300)
    assert pg.evaluate('[Tour.on, Tour.k, S.view]') == [True, 0, v0], pg.evaluate('[Tour.on, Tour.k, S.view]')

    # ---- Next waits a moment behind its bar (the Enter key too)
    pg.evaluate('Tour.k = 0; Tour.held = {}; Tour.HOLD = {per: 16, min: 1400, max: 1400}; Tour.show()'); pg.wait_for_timeout(250)
    held = pg.evaluate("(() => { const b = document.querySelector('[data-tour=\"next\"]'), i = b.querySelector('i'); return {off: b.disabled, cls: b.classList.contains('holding'), bar: !!i && getComputedStyle(i).animationName, ms: Tour.held[0][1], left: Tour.holdLeft()}; })()")
    print('Next held:', held); assert held['off'] and held['cls'] and held['bar'] == 'twhold' and held['left'] > 0, held
    pg.keyboard.press('Enter'); pg.keyboard.press('ArrowRight'); pg.evaluate("document.querySelector('[data-tour=\"next\"]').click()"); pg.wait_for_timeout(200)
    assert pg.evaluate('Tour.k') == 0, 'a held step stays'
    pg.screenshot(path=out + 't_held.png')
    pg.wait_for_function("!document.querySelector('[data-tour=\"next\"]').disabled", timeout=6000)
    assert pg.evaluate("[Tour.holdLeft(), !!document.querySelector('.twnext i'), document.activeElement === document.querySelector('[data-tour=\"next\"]')]") == [0, False, True]
    pg.evaluate('Tour.HOLD = {per: 16, min: 600, max: 1400}')   # the real one back
    assert pg.evaluate("Tour.steps.every((st, k) => { const w = Tour.words(st), ms = Math.min(Tour.HOLD.max, Math.max(Tour.HOLD.min, Tour.HOLD.per * (w.h.length + w.say.join('').length))); return ms <= 1400; })"), 'no step is held longer than a moment'

    # ---- step two: one move on the board. Played by hand, the tour goes on by itself
    pg.click('[data-tour="next"]'); pg.wait_for_function('Tour.k === 1'); pg.wait_for_timeout(300)
    # a step come back to isn't held again
    pg.wait_for_function('!Tour.holdLeft()', timeout=6000); pg.click('[data-tour="back"]'); pg.wait_for_function('Tour.k === 0'); pg.wait_for_timeout(200)
    assert pg.evaluate("[Tour.holdLeft(), document.querySelector('[data-tour=\"next\"]').disabled]") == [0, False], 'no bar on a step already read'
    pg.click('[data-tour="next"]'); pg.wait_for_function('Tour.k === 1'); pg.wait_for_timeout(300)
    assert pg.locator('.top .sidesw, #brandKick').count() == 0, 'no White/Black switch in the header'
    pg.wait_for_function("S.drill && S.drill.guided && S.drill.tour && !S.drill.busy && S.drill.state === 'play' && !!document.querySelector('#db svg')", timeout=5000); pg.wait_for_timeout(700)
    assert "Play the green arrow's move" in pg.inner_text('.twcard') and pg.inner_text('[data-tour="next"]') == 'Show me' and pg.evaluate('!!S.drill.hint')
    ring = pg.evaluate("(() => { const a = document.querySelector('.twring').getBoundingClientRect(), b = document.querySelector('#db').getBoundingClientRect(); return a.left <= b.left && a.right >= b.right && a.top <= b.top && a.bottom >= b.bottom; })()")
    assert ring, 'the ring goes round the board'
    pg.screenshot(path=out + 't_along.png')
    u = pg.evaluate("N[LINES[S.drill.id].n[S.drill.i + 1]].u"); click_move(pg, u[:2], u[2:4])
    pg.wait_for_function('Tour.k === 2', timeout=5000)
    # ---- Back: the step before, set up again. Show me: the coach plays the move
    pg.click('[data-tour="back"]'); pg.wait_for_function("Tour.k === 1 && S.drill && S.drill.guided && S.drill.i === S.drill.s0", timeout=5000); pg.wait_for_timeout(400)
    pg.click('[data-tour="next"]'); pg.wait_for_function('Tour.k === 2', timeout=6000); pg.wait_for_timeout(500)

    # ---- step three: the button that leads on, and that's it
    last = pg.evaluate("(() => { const a = document.querySelector('.twring').getBoundingClientRect(), b = document.getElementById('cGo').getBoundingClientRect(); return [S.view, Tour.words(Tour.cur()).h, a.left <= b.left && a.right >= b.right && a.top <= b.top && a.bottom >= b.bottom, document.querySelector('[data-tour=\"next\"]').innerText.trim()]; })()")
    print('the last step:', last); assert last == ['course', 'Start here', True, "Let's go"], last
    pg.screenshot(path=out + 't_start.png')
    pg.wait_for_function('!Tour.holdLeft()', timeout=6000); pg.click('[data-tour="next"]'); pg.wait_for_function('!Tour.on', timeout=4000); pg.wait_for_timeout(400)

    # ---- nothing from the tour is kept as progress; the tour itself is
    assert pg.evaluate(keep) == before and pg.evaluate('Level.xp()') == xp0, 'the tour leaves no progress behind'
    got = pg.evaluate("[!!(Prog.d.tour && Prog.d.tour.done), !!JSON.parse(localStorage.getItem(PKEY)).tour, localStorage.getItem('playbook-tour'), S.view, SIDE, SET.who, !!document.getElementById('tour')]")
    print('after the tour:', got); assert got == [True, True, 'done', 'course', 'w', 'rook', False], got

    # ---- the app is explained where it is met: the coach's tip on the first visit to each place, one or two short
    #      lines, said once. Every tab has one.
    def bubble():
        return pg.evaluate("(() => { const b = document.querySelector('#coach .cbub'); if (!b) return null; const li = [...b.querySelectorAll('li')].map(x => x.innerText.trim()); return li.length ? li : [b.innerText.replace(/^×\\s*/, '').replace(document.querySelector('#coach .cwho').innerText, '').trim()]; })()")
    assert bubble() is None, ('the course page right after the tour: its last step just said it', bubble())
    tips = {}
    lid = pg.evaluate("LIDX.w[UNIT['w-italian'].lessons[0]].lines[0]")
    for name, js in [('sandbox', "go('sandbox')"), ('drill', "go('drill')"), ('games', "go('games')"), ('shop', "go('shop')"), ('learn', "useSide('w'); go('learn')"), ('last games', "S.gseg = 'last'; go('games')"),
                     ('study', f"openLine('{lid}', 2, 'games')"), ('explore', f"exploreNode(LINES['{lid}'].n[3], {{title: 'x'}})")]:
        pg.evaluate("Coach.hush()"); pg.evaluate(js); pg.wait_for_timeout(450); tips[name] = bubble()
    for k, t in tips.items(): print(f'  first visit, {k}:', t)
    assert all(t and len(t) <= 2 and sum(len(x.split()) for x in t) <= 14 for t in tips.values()), tips
    assert not any('Keep going' in ' '.join(t) for t in tips.values()), 'every place has its own word'
    again = {}
    for name, js in [('course', "S.gseg = 'open'; go('course')"), ('sandbox', "go('sandbox')"), ('drill', "go('drill')"), ('games', "go('games')"), ('shop', "go('shop')")]:
        pg.evaluate("Coach.hush()"); pg.evaluate(js); pg.wait_for_timeout(350); again[name] = bubble()
    assert not any(again.values()), ('a tip is said once', again)
    assert pg.evaluate("VIEWS.every(v => { S.view = v; return Coach.tip() !== 'Keep going.'; })"), 'every tab has a tip'
    pg.evaluate("go('course')")
    pg.reload(); pg.wait_for_timeout(2600)
    assert not pg.evaluate('Tour.on'), 'taken once, it does not start again'

    # ---- Settings: take it again. No coach pick (Settings has it), no bar, and it ends where it began
    pg.evaluate("go('games')"); pg.wait_for_timeout(300)
    pg.click('#setBtn'); pg.wait_for_timeout(300); pg.click('[data-tourgo]'); pg.wait_for_function('Tour.on', timeout=4000)
    assert pg.evaluate("[Tour.replay, Tour.k, Tour.steps.length, Tour.steps.some(st => st.pick)]") == [True, 0, 2, False]
    assert pg.evaluate("[Tour.holdLeft(), !!document.querySelector('[data-tour=\"fast\"]')]") == [0, False]
    pg.wait_for_function("S.drill && S.drill.guided && !S.drill.busy && !!document.querySelector('#db svg')", timeout=5000); pg.wait_for_timeout(500)
    pg.click('[data-tour="next"]'); pg.wait_for_function('Tour.k === 1', timeout=6000); pg.wait_for_timeout(500)
    assert pg.inner_text('[data-tour="next"]') == 'Done'
    pg.click('[data-tour="next"]'); pg.wait_for_function('!Tour.on', timeout=4000); pg.wait_for_timeout(300)
    assert pg.evaluate('[S.view, Tour.on]') == ['games', False], pg.evaluate('[S.view, Tour.on]')
    # taken again, Escape closes it
    pg.click('#setBtn'); pg.wait_for_timeout(300); pg.click('[data-tourgo]'); pg.wait_for_function('Tour.on', timeout=4000); pg.wait_for_timeout(300)
    pg.keyboard.press('Escape'); pg.wait_for_function('!Tour.on', timeout=3000); pg.wait_for_timeout(300)
    assert pg.evaluate('S.view') == 'games' and not pg.evaluate("!!document.getElementById('tour')")
    # a player who picked a coach on the welcome screens isn't asked again
    assert pg.evaluate("(() => { Tour.replay = false; const n = Tour.build().filter(st => !st.skip || !st.skip()).length; return [n, !!SET.ts.who]; })()") == [2, True]
    ctx.close()

    # ---- phone, dark: the card is a sheet across the bottom (the top for a thing at the bottom of the screen), never
    #      over the thing it points at; nothing scrolls sideways; the bar holds Next here too
    ph = b.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True, color_scheme='dark'); q = ph.new_page(); hook(q)
    q.goto(URL); q.wait_for_function('Tour.on', timeout=8000); q.wait_for_timeout(300)
    assert q.locator('[data-tour="fast"]').count() == 0 and q.evaluate("Tour.held[0] && Tour.held[0][1] >= 600"), 'a first run on a phone: held, no Fast forward'
    n = q.evaluate('Tour.steps.length'); assert n == 3, n
    for k in range(n):
        q.wait_for_function("!Tour.holdLeft() && !!document.querySelector('[data-tour=\"next\"]:not([disabled])')", timeout=8000); q.wait_for_timeout(650)
        m = q.evaluate("""(() => { const c = document.querySelector('.twcard'), r = c.getBoundingClientRect(), g = document.querySelector('.twring'), a = g.style.display !== 'none' ? g.getBoundingClientRect() : null, t = Tour.target(), tr = t && t.getBoundingClientRect();
          return {l: r.left, r: r.right, t: r.top, b: r.bottom, w: document.documentElement.scrollWidth, k: Tour.k, h: Tour.words(Tour.cur()).h, top: c.classList.contains('attop'),
            ring: a ? [a.top, a.bottom] : null, seen: tr ? Math.min(tr.bottom, c.classList.contains('attop') ? 844 : r.top) - Math.max(tr.top, c.classList.contains('attop') ? r.bottom : 0) : null,
            th: tr ? tr.height : 0, ch: r.height,
            acts: [...c.querySelectorAll('.twacts .btn')].map(x => Math.round(x.getBoundingClientRect().top))}; })()""")
        print('  phone step', m['k'], m['h'], '| sheet', round(m['ch']), 'px high')
        assert m['l'] == 0 and m['r'] == 390 and m['t'] >= 0 and m['b'] <= 844.5 and m['w'] <= 390, m
        assert (m['t'] == 0) if m['top'] else (m['b'] >= 843.5), ('the sheet is docked to an edge', m)
        assert len(set(m['acts'])) == 1, ('the buttons share one row', m)
        if m['ring']:
            assert (m['ring'][0] >= m['b'] - 1) if m['top'] else (m['ring'][1] <= m['t'] + 1), ('the sheet is clear of the ring', m)
            assert m['seen'] >= min(40, m['th'] - 1), ('the thing the step is about shows beside the sheet', m)
        if k == 1: assert m['seen'] >= 300, ('the whole board shows above the sheet', m)
        q.screenshot(path=out + f't_phone_{k}.png')
        k0 = q.evaluate('Tour.k'); q.tap('[data-tour="next"]')   # Next, Show me on the step that asks for a move, then Let's go
        if k < n - 1: q.wait_for_function(f'Tour.k !== {k0}', timeout=12000); q.wait_for_timeout(250)
    q.wait_for_function('!Tour.on', timeout=5000)
    print('phone: three steps, the sheet clear of its target in each')
    ph.close()
    b.close()

site.stop()
print('ERRORS:', errors[:10]); assert not errors
print('tour checks passed')
