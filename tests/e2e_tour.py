"""The tour: it starts by itself for a player who hasn't taken it and can't be skipped (no close button; Escape and taps
outside the card do nothing) or sped up: a first run has no Fast forward, and Next is held behind a bar that fills while
the step is read (not on a step come back to). A step that asks for a tap goes on once it's done, by hand or with Show
me; Back goes a step back. Walked to its end it shows the arrow's move in Play along, a punished slip from memory, Play
on with the engine and a lesson's list of the other side's answers, leaves no progress behind, is marked in the progress
record and on the device, and doesn't come back after a reload. Settings plays it again (ending where it began): then
there is no bar and Fast forward plays it by itself. It names every tab, every part of Your games, every setting and
every feature listed in FEATURES. Phone width in dark mode: the card is a sheet across the bottom of the screen (the top
when the thing it points at is at the bottom), never over that thing, and nothing scrolls sideways. Over local HTTP, the
website's own page."""
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


def ff_to_end(pg, seen, limit=180, fast=True):
    """Fast forward until the tour closes (or, with fast=False, Next by Next), noting what each step showed."""
    if fast: pg.click('[data-tour="fast"]')
    t0 = time.time(); last = None
    while time.time() - t0 < limit:
        st = pg.evaluate("""Tour.on ? {k: Tour.k, h: Tour.words(Tour.cur()).h, view: S.view, ring: !!Tour.target(),
          go: !Tour.holdLeft() && !Tour.ok && (!Tour.cur().ready || Tour.cur().ready()) && !!document.querySelector('[data-tour="next"]:not([disabled])'),
          along: !!(S.drill && S.drill.guided && S.drill.tour && LINES[S.drill.id].n.slice(S.drill.s0 + 1, S.drill.i + 1).some(i => isMine(N[i]))),
          pun: !!document.querySelector('#dpanel .feedback .pun'), arrow: !!(S.drill && S.drill.tour && !S.drill.guided && S.drill.hint),
          opts: !!document.querySelector('.opts .opt')} : null""")
        if not st: return time.time() - t0
        if st['k'] != last: last = st['k']; seen.append(st['h'])
        for f in ('along', 'pun', 'arrow', 'opts'):
            if st[f]: seen.append('#' + f)
        if st['view'] == 'explore': seen.append('#explore')
        if not fast and st['go']:
            pg.wait_for_timeout(350)   # what the step shows is on the page before it is left
            pg.evaluate("""(k => { if (Tour.on && Tour.k === k && !Tour.ok) document.querySelector('[data-tour="next"]').click(); })""", st['k'])
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

    # ---- a first run can't be sped up: no Fast forward, and Next waits behind its bar (the Enter key too)
    assert pg.locator('[data-tour="fast"]').count() == 0, 'no Fast forward on a first run'
    pg.evaluate('Tour.prev(); Tour.k = 0; Tour.held = {}; Tour.show()'); pg.wait_for_timeout(250)
    held = pg.evaluate("(() => { const b = document.querySelector('[data-tour=\"next\"]'), i = b.querySelector('i'); return {off: b.disabled, cls: b.classList.contains('holding'), bar: !!i && getComputedStyle(i).animationName, ms: Tour.held[0][1], left: Tour.holdLeft()}; })()")
    print('Next held:', held); assert held['off'] and held['cls'] and held['bar'] == 'twhold' and 1300 <= held['ms'] <= 4200 and held['left'] > 0, held
    pg.keyboard.press('Enter'); pg.keyboard.press('ArrowRight'); pg.evaluate("document.querySelector('[data-tour=\"next\"]').click()"); pg.wait_for_timeout(200)
    assert pg.evaluate('Tour.k') == 0, 'a held step stays'
    pg.screenshot(path=out + 't_held.png')
    pg.wait_for_function("!document.querySelector('[data-tour=\"next\"]').disabled", timeout=6000)
    assert pg.evaluate("[Tour.holdLeft(), !!document.querySelector('.twnext i'), document.activeElement === document.querySelector('[data-tour=\"next\"]')]") == [0, False, True]

    # ---- the tabs: both books are in every one of them, and there is no colour to switch to
    pg.click('[data-tour="next"]'); pg.wait_for_function('Tour.k === 1'); pg.wait_for_timeout(500)
    # a step come back to isn't held again
    assert pg.evaluate('Tour.holdLeft()') > 0
    pg.wait_for_function('!Tour.holdLeft()', timeout=6000); pg.click('[data-tour="back"]'); pg.wait_for_function('Tour.k === 0'); pg.wait_for_timeout(200)
    assert pg.evaluate("[Tour.holdLeft(), document.querySelector('[data-tour=\"next\"]').disabled]") == [0, False], 'no bar on a step already read'
    pg.click('[data-tour="next"]'); pg.wait_for_function('Tour.k === 1'); pg.wait_for_timeout(300)
    assert pg.evaluate('Tour.holdLeft()') == 0
    pg.evaluate('Tour.HOLD = {per: 3, min: 250, max: 500}')   # the rest of the walk with a short bar
    card = pg.inner_text('.twcard'); assert 'Five tabs' in card and 'both in here' in card and 'Tap Black' not in card, card
    assert pg.locator('.top .sidesw, #brandKick').count() == 0, 'no White/Black switch in the header'
    ring = pg.evaluate("(() => { const a = document.querySelector('.twring').getBoundingClientRect(), b = document.querySelector('.tabs').getBoundingClientRect(); return a.left <= b.left && a.right >= b.right && a.top <= b.top && a.bottom >= b.bottom; })()")
    assert ring, 'the ring goes round the tabs'
    pg.screenshot(path=out + 't_tabs.png')
    # ---- inside the spotlight of a step that only explains, the page can't be tapped either
    tab = pg.locator('.tabs [data-view="drill"]').bounding_box()
    pg.mouse.click(tab['x'] + tab['width'] / 2, tab['y'] + tab['height'] / 2); pg.wait_for_timeout(300)
    assert pg.evaluate('[Tour.k, S.view]') == [1, v0]
    # ---- a step that asks for a move: played by hand, it goes on by itself
    ka = pg.evaluate("Tour.steps.findIndex(st => Tour.words(st).h === 'Play along')"); assert ka > 1, ka
    while pg.evaluate('Tour.k') < ka:
        k0 = pg.evaluate('Tour.k'); pg.click('[data-tour="next"]'); pg.wait_for_function(f'Tour.k === {k0 + 1}', timeout=5000); pg.wait_for_timeout(400)
    pg.wait_for_function("S.drill && S.drill.guided && !S.drill.busy && S.drill.state === 'play' && !!document.querySelector('#db svg')", timeout=5000); pg.wait_for_timeout(700)
    assert "Play the arrow's move" in pg.inner_text('.twcard') and pg.inner_text('[data-tour="next"]') == 'Show me'
    u = pg.evaluate("N[LINES[S.drill.id].n[S.drill.i + 1]].u"); click_move(pg, u[:2], u[2:4])
    pg.wait_for_function(f'Tour.k === {ka + 1}', timeout=5000)
    pg.screenshot(path=out + 't_along.png')
    # ---- Back: the step before, set up again. Show me: the coach plays the move
    pg.click('[data-tour="back"]'); pg.wait_for_function(f"Tour.k === {ka} && S.drill && S.drill.guided && S.drill.i === S.drill.s0", timeout=5000); pg.wait_for_timeout(400)
    pg.click('[data-tour="next"]'); pg.wait_for_function(f'Tour.k === {ka + 1}', timeout=6000)

    # ---- the rest, Next by Next (Show me where a step asks for a tap)
    seen = []; secs = ff_to_end(pg, seen, fast=False)
    titles = [s for s in seen if not s.startswith('#')]; marks = set(s for s in seen if s.startswith('#'))
    print(f'walked: {len(set(titles))} steps in {secs:.0f} s; seen:', sorted(marks))
    assert {'#along', '#pun', '#arrow', '#explore', '#opts'} <= marks, marks
    assert {'I explain every move', 'Play on with the engine', 'The explore board', 'Your games', 'The Sandbox', 'The daily shop', 'Crates', 'Settings'} <= set(titles), titles

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
    # taken again there is no bar, and Fast forward plays it by itself
    assert pg.evaluate("[Tour.holdLeft(), document.querySelector('[data-tour=\"next\"]').disabled, !!document.querySelector('[data-tour=\"fast\"]')]") == [0, False, True]
    seen2 = []; secs = ff_to_end(pg, seen2); print(f'fast forward (taken again): {len(set(s for s in seen2 if not s.startswith("#")))} steps in {secs:.0f} s')
    assert {'#along', '#pun', '#arrow', '#explore', '#opts'} <= set(seen2), seen2
    assert pg.evaluate('[S.view, Tour.on]') == ['games', False], pg.evaluate('[S.view, Tour.on]')

    # ---- the tour keeps up with the app: every tab, every part of Your games, every setting and every feature in
    #      FEATURES is named in it. A new tab, part or setting fails here until the tour speaks of it; a new feature
    #      gets a step or a line in Tour.build (app/product.js) and its words in FEATURES.
    said = pg.evaluate("Tour.build().map(st => { const w = Tour.words(st); return [w.h].concat(w.say).join(' '); }).join(' ').toLowerCase()")
    tabs = pg.evaluate("[...document.querySelectorAll('.tabs [data-view]')].map(b => ((b.querySelector('.lg') || b).childNodes[0].textContent || '').trim())")
    pg.evaluate("go('games')"); pg.wait_for_timeout(300)
    segs = pg.evaluate("[...document.querySelectorAll('.gseg button')].map(b => (b.querySelector('.lg') || b.childNodes[0]).textContent.trim())")
    pg.click('#setBtn'); pg.wait_for_timeout(300)
    rows = pg.evaluate("[...document.querySelectorAll('.setrow > b')].map(b => b.textContent.trim())")
    pg.keyboard.press('Escape'); pg.wait_for_timeout(200)
    SETTINGS = {'Appearance': 'light or dark', 'Text size': 'text size', 'Board colour': 'board colours', 'Your coach': 'your coach',
                'The tour': 'this tour'}
    slots = pg.evaluate("Object.keys(DATA_W.packs || {}).concat(Object.keys(DATA_B.packs || {})).map(k => slotName(k))")
    FEATURES = {'both colours in one place': 'both in here', 'the Sandbox with both colours': 'white and black in turn', 'play along': 'play along', 'move explanations': 'what it does',
                'a slip and its punishment': 'punishes', 'play on with the engine': 'play on with the engine',
                'the explore board': 'explore board', 'the engine in lessons': 'the engine in lessons',
                'the plan at the end of every line': 'plan', 'opening names': "opening's real name",
                'practice from a position': 'set up a position', 'the last three games': 'last 3 games',
                'levels': 'level', 'the streak': 'streak', 'the flame\'s colours': 'takes a new colour', 'the daily shop': 'new pieces every day', 'rarities on the shelf': 'an epic one about once a week', 'crates and rarities': 'crates hold pieces the shop never sells', 'a crate opened with a tap': 'tap the crate to open it', 'the locker': 'from your locker', 'the account': 'sign in',
                'the coach': 'tap me', 'marks on the moves': 'key move', 'marks on the board': 'on the board beside the piece', 'move numbers on the pieces': 'number of the move', 'a lesson board that takes moves': 'move any piece', 'the material count': 'pieces each side has taken', 'piece animations': 'how pieces slide', 'advanced settings and the reset': 'reset your account', 'variations of a system': 'variations inside them', 'sounds': 'sounds in three themes', 'the engine on a finished Sandbox game': 'when a game ends the engine is on its board', 'where the added moves begin': 'how it usually goes on',
                'a game that left the book': 'leaves your book',
                'a move played too early': 'wrong moment'}
    missing = [f'tab {t}' for t in tabs if t.lower() not in said] + [f'Your games: {g}' for g in segs if g.lower() not in said] \
        + [f'setting {r}' for r in rows if r not in SETTINGS and r not in slots] \
        + [f'setting {r}' for r, w in SETTINGS.items() if r in rows and w not in said] \
        + (['your systems'] if any(r in slots for r in rows) and 'your systems' not in said else []) \
        + [f'feature {k}' for k, w in FEATURES.items() if w not in said]
    print('the tour names:', len(tabs), 'tabs,', len(segs), 'parts of Your games,', len(rows), 'settings,', len(FEATURES), 'features')
    assert not missing, f'not in the tour: {missing}'
    ctx.close()

    # ---- phone, dark: the card is a sheet across the bottom (the top for a thing at the bottom of the screen), never
    #      over the thing it points at; nothing scrolls sideways; the bar holds Next here too
    ph = b.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True, color_scheme='dark'); q = ph.new_page(); hook(q)
    q.goto(URL); q.wait_for_function('Tour.on', timeout=8000); q.wait_for_timeout(500)
    assert q.locator('[data-tour="fast"]').count() == 0 and q.evaluate("document.querySelector('[data-tour=\"next\"]').disabled"), 'a first run on a phone: held, no Fast forward'
    q.evaluate('Tour.HOLD = {per: 3, min: 250, max: 500}')
    n = q.evaluate('Tour.steps.length'); tops = []
    for k in range(n - 1):
        q.wait_for_function("!Tour.holdLeft() && !!document.querySelector('[data-tour=\"next\"]:not([disabled])')", timeout=8000); q.wait_for_timeout(650)
        m = q.evaluate("""(() => { const c = document.querySelector('.twcard'), r = c.getBoundingClientRect(), g = document.querySelector('.twring'), a = g.style.display !== 'none' ? g.getBoundingClientRect() : null, t = Tour.target(), tr = t && t.getBoundingClientRect();
          return {l: r.left, r: r.right, t: r.top, b: r.bottom, w: document.documentElement.scrollWidth, k: Tour.k, h: Tour.words(Tour.cur()).h, top: c.classList.contains('attop'),
            ring: a ? [a.top, a.bottom] : null, seen: tr ? Math.min(tr.bottom, c.classList.contains('attop') ? 844 : r.top) - Math.max(tr.top, c.classList.contains('attop') ? r.bottom : 0) : null,
th: tr ? tr.height : 0,
            acts: [...c.querySelectorAll('.twacts .btn')].map(x => Math.round(x.getBoundingClientRect().top))}; })()""")
        assert m['l'] == 0 and m['r'] == 390 and m['t'] >= 0 and m['b'] <= 844.5 and m['w'] <= 390, m
        assert (m['t'] == 0) if m['top'] else (m['b'] >= 843.5), ('the sheet is docked to an edge', m)
        assert len(set(m['acts'])) == 1, ('the buttons share one row', m)
        if m['ring']:
            assert (m['ring'][0] >= m['b'] - 1) if m['top'] else (m['ring'][1] <= m['t'] + 1), ('the sheet is clear of the ring', m)
            assert m['seen'] >= min(40, m['th'] - 1), ('the thing the step is about shows beside the sheet', m)
        if m['top']: tops.append(m['h'])
        if k in (0, 6): q.screenshot(path=out + f't_phone_{k}.png')
        k0 = q.evaluate('Tour.k'); q.tap('[data-tour="next"]')   # Next, or Show me on a step that asks for a tap
        q.wait_for_function(f'Tour.k !== {k0}', timeout=12000); q.wait_for_timeout(250)
    print('phone: the sheet clear of its target through', q.evaluate('Tour.k'), 'steps; at the top for', tops)
    assert "That's me" in tops, tops
    ph.close()
    b.close()

site.stop()
print('ERRORS:', errors[:10]); assert not errors
print('tour checks passed')
