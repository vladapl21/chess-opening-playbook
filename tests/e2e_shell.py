"""The shell of the app: tab order, the White/Black switch keeping the tab, and Settings."""
from playwright.sync_api import sync_playwright
from e2e_white import launch, out
from serve import Site
# the website's own page, over local HTTP: headless Chromium sometimes drops a file:// page's storage across a scripted reload
site = Site(docs=True); URL = site.start()
errors = []


def hook(pg):
    pg.on('pageerror', lambda e: errors.append(f'pageerror: {e}'))
    pg.on('console', lambda m: errors.append(f'console {m.type}: {m.text}') if m.type == 'error' and 'ERR_' not in m.text else None)


def tab(pg): return pg.inner_text('.tabs button[aria-selected="true"]').split('\n')[0].strip()


with sync_playwright() as p:
    b = launch(p)
    ctx = b.new_context(viewport={'width': 1280, 'height': 900})
    pg = ctx.new_page(); hook(pg); pg.goto(URL); pg.wait_for_timeout(1000)
    tabs = [t.split('\n')[0].strip() for t in pg.locator('.tabs button').all_inner_texts()]
    print('tabs:', tabs); assert tabs[:2] == ['Sandbox', 'Course'] and tabs[2].startswith('Drill') and tabs[3] == 'Your games' and tabs[4] == 'Shop' and len(tabs) == 5

    # the colour switch stays on the tab: Drill on White, Course on Black, then switch back and forth
    pg.click('.tabs [data-view="drill"]'); pg.wait_for_timeout(300)
    pg.click('.sidesw [data-side="b"]'); pg.wait_for_timeout(400)
    assert pg.evaluate('[SIDE, S.view]') == ['b', 'drill'], pg.evaluate('[SIDE, S.view]')
    pg.click('.tabs [data-view="course"]'); pg.wait_for_timeout(300)
    pg.click('.sidesw [data-side="w"]'); pg.wait_for_timeout(400)
    assert pg.evaluate('[SIDE, S.view]') == ['w', 'course'] and tab(pg) == 'Course', pg.evaluate('[SIDE, S.view]')
    for v in ('sandbox', 'games'):
        pg.click(f'.tabs [data-view="{v}"]'); pg.wait_for_timeout(300)
        pg.click('.sidesw [data-side="b"]'); pg.wait_for_timeout(400)
        assert pg.evaluate('[SIDE, S.view]') == ['b', v], (v, pg.evaluate('[SIDE, S.view]'))
        pg.click('.sidesw [data-side="w"]'); pg.wait_for_timeout(400)
        assert pg.evaluate('[SIDE, S.view]') == ['w', v], (v, pg.evaluate('[SIDE, S.view]'))
    # inside a lesson opened from an opening's page: the other book has no such lesson, so the switch lands on Your games
    # (where the opening pages live); switching back returns to the lesson
    pg.evaluate("openLine('setup', undefined, 'learn')"); pg.wait_for_timeout(300)
    assert tab(pg) == 'Your games'
    pg.click('.sidesw [data-side="b"]'); pg.wait_for_timeout(400)
    assert pg.evaluate('[SIDE, S.view]') == ['b', 'games'], pg.evaluate('[SIDE, S.view, S.studyFrom, S.line]')
    pg.click('.sidesw [data-side="w"]'); pg.wait_for_timeout(400)
    assert pg.evaluate('[SIDE, S.view, S.line]') == ['w', 'study', 'setup']
    print('switch keeps the tab')
    # the cheat sheet lives on each opening's page now: an old link opens that page at a glance, under Your games
    lp = ctx.new_page(); hook(lp); lp.goto(URL + '#cheat'); lp.wait_for_timeout(900)
    assert lp.evaluate('[S.view, S.lview]') == ['learn', 'glance'] and tab(lp) == 'Your games' and lp.locator('#view .ccard').count() > 0
    lp.close()

    # settings
    pg.evaluate("go('learn')"); pg.wait_for_timeout(300)
    pg.click('#setBtn'); pg.wait_for_timeout(300)
    pg.screenshot(path=out + 's_settings.png')
    bg0 = pg.evaluate("getComputedStyle(document.body).backgroundColor")
    pg.click('[data-set="theme:dark"]'); pg.wait_for_timeout(200)
    bg1 = pg.evaluate("getComputedStyle(document.body).backgroundColor"); assert bg0 != bg1 and pg.evaluate("document.documentElement.dataset.theme") == 'dark'
    pg.click('[data-set="board:wood"]'); pg.wait_for_timeout(200)
    sq = pg.evaluate("getComputedStyle(document.querySelector('.sq-d')).fill"); print('dark theme', bg1, '| wood square', sq)
    assert sq == 'rgb(156, 117, 81)', sq
    pg.click('[data-set="size:xl"]'); pg.wait_for_timeout(200)
    assert pg.evaluate("document.getElementById('app').style.zoom") == '1.16'
    n0 = pg.locator('#view .coord').count()
    pg.click('[data-set^="coords:"]'); pg.wait_for_timeout(300)
    n1 = pg.locator('#view .coord').count(); print('coords', n0, '->', n1); assert n0 > 0 and n1 == 0
    pg.screenshot(path=out + 's_settings_dark.png')
    pg.keyboard.press('Escape'); pg.wait_for_timeout(200)
    assert pg.evaluate("document.getElementById('setSheet').hidden")
    pg.reload(); pg.wait_for_timeout(900)
    assert pg.evaluate("[SET.theme, SET.board, SET.size, SET.coords, document.documentElement.dataset.board]") == ['dark', 'wood', 'xl', False, 'wood']
    # a drill still takes moves at the largest size
    pg.evaluate("useSide('w'); startDrillLine('setup')"); pg.wait_for_timeout(1200)
    from e2e_white import click_move
    u = pg.evaluate("N[LINES[S.drill.id].n[S.drill.i + 1]].u"); i0 = pg.evaluate('S.drill.i')
    click_move(pg, u[:2], u[2:4]); pg.wait_for_timeout(900)
    assert pg.evaluate('S.drill.i') > i0 and pg.evaluate('S.drill.mistakes') == 0, 'move not taken at the largest size'
    pg.screenshot(path=out + 's_drill_xl.png')
    pg.evaluate("setSetting('theme', 'system')"); pg.wait_for_timeout(100)
    assert pg.evaluate("document.documentElement.dataset.theme") is None

    # phone: largest text, no sideways scroll on any tab; the settings sheet fits
    c2 = b.new_context(viewport={'width': 390, 'height': 844}); ph = c2.new_page(); hook(ph)
    ph.add_init_script("localStorage.setItem('playbook-settings', JSON.stringify({size: 'xl', board: 'plum'}))")
    ph.goto(URL); ph.wait_for_timeout(900)
    for v in ('sandbox', 'course', 'learn', 'drill', 'games', 'shop'):
        ph.evaluate(f"go('{v}')"); ph.wait_for_timeout(350)
        w = ph.evaluate('document.documentElement.scrollWidth'); print('  phone xl', v, w); assert w <= 390, (v, w)
    ph.click('#setBtn'); ph.wait_for_timeout(300); ph.screenshot(path=out + 's_settings_phone.png')
    assert ph.evaluate("document.getElementById('setPanel').scrollWidth <= document.getElementById('setPanel').clientWidth + 1")

    # ---- the header: brand and the player's things (level, streak, settings, account) on one row, the tabs on a row of
    # their own under it, so nothing ever sits on a tab; on a phone the White/Black switch gets the middle row.
    # Shown with everything a signed-in player on a streak has, at every width from a small phone to a wide monitor.
    SEED = """(() => { const now = Date.now(); for (const id of DRILLABLE.slice(0, 120)) Prog.d.lines[id] = {box: 3, seen: 3, clean: 3, last: now, due: now + 2 * DAY, v: VER[id] || 1};
      const D = Prog.d.days = Prog.d.days || {}; for (let k = 0; k <= 5; k++) D[dayKey(-k)] = ['a', 'b', 'c', 'd', 'e']; Prog.d.lvl = 99; Prog.save(); Badges.queue = []; Coach.hush();
      const a = document.getElementById('acctBtn'); a.hidden = false; a.className = 'acct in ok'; a.innerHTML = '<span class=av>V</span><span class=acctx>Saved</span>'; renderChrome(); })()"""
    LAYOUT = """(() => { const R = e => e.getBoundingClientRect(), hit = (a, b) => !(a.right <= b.left + 1 || b.right <= a.left + 1 || a.bottom <= b.top + 1 || b.bottom <= a.top + 1);
      const vis = e => e && !e.hidden && R(e).width > 0 && getComputedStyle(e).display !== 'none';
      const mine = [...document.querySelectorAll('.corner > *')].filter(vis), tabs = [...document.querySelectorAll('.tabs button')];
      const parts = [...mine, document.querySelector('.brand'), document.querySelector('.top .sidesw')].filter(vis);
      const name = e => e.id || e.dataset.view || e.className.split(' ')[0];
      const over = parts.flatMap((x, i) => [...parts.slice(i + 1), ...tabs].filter(y => hit(R(x), R(y))).map(y => name(x) + ' x ' + name(y)));
      const t = document.querySelector('.tabs'), g = R(document.getElementById('setBtn')), tr = R(t), lv = document.getElementById('lvN');
      return {over, mine: mine.map(name), page: document.documentElement.scrollWidth, tabsFit: t.scrollWidth <= t.clientWidth + 1,
        tabsInView: tabs.every(b => R(b).left >= -1 && R(b).right <= innerWidth + 1), gearAboveTabs: g.bottom <= tr.top + 1, gearInHeader: !!document.querySelector('.top #setBtn'),
        ring: getComputedStyle(lv).backgroundImage.includes('conic-gradient'), num: getComputedStyle(lv).color, ink: getComputedStyle(document.body).color}; })()"""
    for w in (360, 390, 600, 700, 761, 1000, 1280, 1536, 1920):   # phone, tablet (the switch on a middle row), one row from 761px
        hc = b.new_context(viewport={'width': w, 'height': 800}); lp = hc.new_page(); hook(lp); lp.goto(URL + '#b.drill'); lp.wait_for_timeout(800)
        lp.evaluate(SEED); lp.wait_for_timeout(400); lp.evaluate("document.querySelectorAll('#lvup,.lvfloat').forEach(e => e.remove())")
        m = lp.evaluate(LAYOUT); print('header at', w, {k: m[k] for k in ('over', 'mine', 'page', 'tabsFit')})
        assert not m['over'] and m['page'] <= w and m['tabsFit'] and m['tabsInView'] and m['gearAboveTabs'] and m['gearInHeader'], (w, m)
        assert len(m['mine']) >= 4, ('level, streak, settings and account all showing', m['mine'])
        assert m['ring'] and m['num'] == m['ink'], 'the level number is in ink on the page colour, the green is the ring around it'
        if w in (390, 1280): lp.screenshot(path=out + f's_header_{w}.png', clip={'x': 0, 'y': 0, 'width': w, 'height': 200})
        hc.close()

    # ---- three coaches: the face and the name change, the words do not
    cp = ctx.new_page(); hook(cp); cp.goto(URL); cp.wait_for_timeout(900)
    cp.evaluate("setSetting('who', 'knight'); setSetting('coach', true); setSetting('size', 'm'); setSetting('theme', 'light'); Coach.say('One tip.')"); cp.wait_for_timeout(300)
    box = cp.evaluate("(() => { const b = document.querySelector('.cbub').getBoundingClientRect(), a = document.querySelector('.cav').getBoundingClientRect(); return [Math.round(b.width), Math.round(a.width), document.querySelector('.cwho').innerText]; })()")
    print('coach bubble, face, name:', box); assert box[0] <= 232 and box[1] >= 76 and box[2].upper() == 'PIP'
    cp.click('#setBtn'); cp.wait_for_timeout(250)
    assert cp.locator('#setPanel [data-coachwho]').count() == 3
    names = []
    for who in ('rook', 'pawn', 'knight'):
        cp.click(f'#setPanel [data-coachwho="{who}"]'); cp.wait_for_timeout(250)
        names.append(cp.evaluate("[SET.who, coachName(), document.querySelector('#setPanel [data-coachwho][aria-pressed=\"true\"]').dataset.coachwho, document.querySelector('.cav svg').innerHTML.length]"))
    print('coaches:', names); assert [n[:3] for n in names] == [['rook', 'Rocco', 'rook'], ['pawn', 'Dot', 'pawn'], ['knight', 'Pip', 'knight']] and len({n[3] for n in names}) == 3
    cp.screenshot(path=out + 's_coaches.png'); cp.keyboard.press('Escape')

    # ---- a lesson opened from a unit: the way forward is at the top, and skipping ahead doesn't count as studying.
    # A lesson counts once its moves are played along with the arrows, or stepped through to the end on its page.
    cp.evaluate("openUnitLesson(UNIT['w-italian'], UNIT['w-italian'].lessons[0])"); cp.wait_for_timeout(500)
    first = cp.evaluate("UNIT['w-italian'].lessons")
    assert cp.inner_text('#topNext').startswith('Next lesson') and cp.evaluate("document.getElementById('topNext').getBoundingClientRect().top") < 260
    assert cp.locator('#playAlong').count() == 1, 'Play along sits beside the drill button'
    assert not cp.evaluate(f"lessonSeen('w', '{first[0]}')")
    cp.keyboard.press('End'); cp.wait_for_timeout(300)
    assert not cp.evaluate(f"lessonSeen('w', '{first[0]}')"), 'jumping to the end is not studying it'
    cp.keyboard.press('Home'); cp.wait_for_timeout(200)
    for _ in range(cp.evaluate('LINES[S.line].n.length')): cp.keyboard.press('ArrowRight'); cp.wait_for_timeout(40)
    cp.wait_for_timeout(300); assert cp.evaluate(f"lessonSeen('w', '{first[0]}')"), 'stepped through to the end: studied'
    cp.click('#topNext'); cp.wait_for_timeout(500)
    assert cp.evaluate(f"[lessonSeen('w', '{first[1]}'), LINES[S.line].lesson, S.studyFrom]") == [False, first[1], 'unit']
    for _ in range(len(first) - 2): cp.click('#topNext'); cp.wait_for_timeout(350)
    assert cp.inner_text('#topNext').startswith('Done'); cp.click('#topNext'); cp.wait_for_timeout(400)
    assert cp.evaluate("[S.view, S.unit]") == ['unit', 'w-italian'] and cp.evaluate("UNIT['w-italian'].lessons.filter(l => lessonSeen('w', l)).length") == 1
    # Play along from the lesson page: the same line on the drill board with the arrow, still under the Course tab
    cp.evaluate("openUnitLesson(UNIT['w-italian'], UNIT['w-italian'].lessons[1])"); cp.wait_for_timeout(500)
    cp.click('#playAlong'); cp.wait_for_timeout(600)
    assert cp.evaluate("[S.view, !!S.drill.guided, S.drill.unit, LINES[S.drill.id].lesson]") == ['drill', True, 'w-italian', first[1]]
    assert tab(cp) == 'Course'

    # ---- a practice game from the course, then free play in the Sandbox
    cp.evaluate("doStep(UNIT['w-italian'], 'spar')"); cp.wait_for_timeout(700)
    assert cp.evaluate("[S.view, S.drill.scope]") == ['sandbox', 'u:w-italian'] and cp.locator('.sbcourse').count() == 1 and cp.locator('.cban').count() == 0
    cp.evaluate("go('course')"); cp.wait_for_timeout(300); cp.evaluate("go('sandbox')"); cp.wait_for_timeout(400)
    assert cp.locator('.sbcourse').count() == 1, 'the course game is still there when you come back'
    cp.click('#sbFree'); cp.wait_for_timeout(400)
    st = cp.evaluate("[S.view, S.drill, S.sbState, document.querySelectorAll('.sbcourse, #sbFree').length, document.querySelectorAll('[data-sbf^=\"pick:\"]').length > 3, !!document.getElementById('sbGo')]")
    print('free play:', st); assert st == ['sandbox', None, None, 0, True, True]
    cp.click('#sbGo'); cp.wait_for_timeout(600); assert cp.evaluate("S.drill.scope") == cp.evaluate("SBS.scope") and cp.locator('.sbcourse, #sbFree').count() == 0
    b.close()
site.stop()
print('ERRORS:', errors); assert not errors
print('shell checks passed')
