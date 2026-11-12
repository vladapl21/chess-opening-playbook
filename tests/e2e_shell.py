"""The shell of the app: tab order, the White/Black switch keeping the tab, and Settings."""
from playwright.sync_api import sync_playwright
from e2e_white import launch, URL, out
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
    print('tabs:', tabs); assert tabs[:3] == ['Sandbox', 'Course', 'Learn'] and tabs[3].startswith('Drill')

    # the colour switch stays on the tab: Drill on White, Course on Black, then switch back and forth
    pg.click('.tabs [data-view="drill"]'); pg.wait_for_timeout(300)
    pg.click('.sidesw [data-side="b"]'); pg.wait_for_timeout(400)
    assert pg.evaluate('[SIDE, S.view]') == ['b', 'drill'], pg.evaluate('[SIDE, S.view]')
    pg.click('.tabs [data-view="course"]'); pg.wait_for_timeout(300)
    pg.click('.sidesw [data-side="w"]'); pg.wait_for_timeout(400)
    assert pg.evaluate('[SIDE, S.view]') == ['w', 'course'] and tab(pg) == 'Course', pg.evaluate('[SIDE, S.view]')
    for v in ('sandbox', 'learn', 'games', 'cheat'):
        pg.click(f'.tabs [data-view="{v}"]'); pg.wait_for_timeout(300)
        pg.click('.sidesw [data-side="b"]'); pg.wait_for_timeout(400)
        assert pg.evaluate('[SIDE, S.view]') == ['b', v], (v, pg.evaluate('[SIDE, S.view]'))
        pg.click('.sidesw [data-side="w"]'); pg.wait_for_timeout(400)
        assert pg.evaluate('[SIDE, S.view]') == ['w', v], (v, pg.evaluate('[SIDE, S.view]'))
    # inside a lesson: the other book has no such lesson, so the switch lands on Learn; switching back returns to the lesson
    pg.evaluate("openLine('setup', undefined, 'learn')"); pg.wait_for_timeout(300)
    pg.click('.sidesw [data-side="b"]'); pg.wait_for_timeout(400)
    assert pg.evaluate('[SIDE, S.view]') == ['b', 'learn'], pg.evaluate('[SIDE, S.view, S.studyFrom, S.line]')
    pg.click('.sidesw [data-side="w"]'); pg.wait_for_timeout(400)
    assert pg.evaluate('[SIDE, S.view, S.line]') == ['w', 'study', 'setup']
    print('switch keeps the tab')

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
    for v in ('sandbox', 'course', 'learn', 'drill', 'games', 'cheat'):
        ph.evaluate(f"go('{v}')"); ph.wait_for_timeout(350)
        w = ph.evaluate('document.documentElement.scrollWidth'); print('  phone xl', v, w); assert w <= 390, (v, w)
    ph.click('#setBtn'); ph.wait_for_timeout(300); ph.screenshot(path=out + 's_settings_phone.png')
    assert ph.evaluate("document.getElementById('setPanel').scrollWidth <= document.getElementById('setPanel').clientWidth + 1")
    b.close()
print('ERRORS:', errors); assert not errors
print('shell checks passed')
