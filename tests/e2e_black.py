"""End-to-end checks for the Black book and the White | Black switch (desktop, phone, dark)."""
import random, json
from playwright.sync_api import sync_playwright
from e2e_white import sq_xy, drag, click_move, play_sandbox, launch, URL, out  # noqa
errors = []

def hook(pg):
    pg.on('pageerror', lambda e: errors.append(f'pageerror: {e}'))
    pg.on('console', lambda m: errors.append(f'console {m.type}: {m.text}') if m.type == 'error' else None)

def drill_line(pg, lid, slip=False):
    pg.evaluate(f"startDrillLine('{lid}')"); pg.wait_for_timeout(700)
    tries = 0
    for _ in range(120):
        st = pg.evaluate("({state:S.drill.state, busy:S.drill.busy, i:S.drill.i})")
        if st['state'] == 'done': break
        if st['busy']: pg.wait_for_timeout(250); continue
        u = pg.evaluate("N[LINES[S.drill.id].n[S.drill.i + 1]].u")
        if slip and tries == 0:
            legal = pg.evaluate("DATA.legal[String(dNode())] || []")
            wrong = [m for m in legal if m != u and len(m) == 4]
            m = wrong[0]; drag(pg, m[:2], m[2:4]); tries += 1; pg.wait_for_timeout(800); continue
        if u in ('e8g8', 'e8c8'): drag(pg, 'e8', 'h8' if u == 'e8g8' else 'a8')
        else: click_move(pg, u[:2], u[2:4])
        pg.wait_for_timeout(900)
    return pg.evaluate("({state:S.drill.state, mistakes:S.drill.mistakes, rec: Prog.rec(S.drill.id)})")

with sync_playwright() as p:
    b = launch(p)
    ctx = b.new_context(viewport={'width': 1280, 'height': 900})
    pg = ctx.new_page(); hook(pg)
    pg.goto(URL); pg.wait_for_timeout(1200)
    assert pg.evaluate('SIDE') == 'w'
    # ---- switch to Black
    pg.click('.sidesw [data-side="b"]'); pg.wait_for_timeout(600)
    assert pg.evaluate('SIDE') == 'b' and pg.evaluate('FLIP') is True
    print('hash after switch', pg.evaluate('location.hash'), '| kicker', pg.inner_text('#brandKick'))
    print('learn h2:', pg.inner_text('.reps h2'), '| tiles', pg.locator('.rtile').count())
    assert pg.locator('.rtile').count() == 9
    # hero board orientation: black king (e8) drawn below the white king (e1)
    yk = pg.evaluate("""(() => { const s = document.querySelector('.hero-board svg'); const e8 = s.querySelector('use[data-sq="e8"]'), e1 = s.querySelector('use[data-sq="e1"]'); return [e8 && +e8.getAttribute('y'), e1 && +e1.getAttribute('y')]; })()""")
    print('hero e8/e1 y:', yk)
    pg.screenshot(path=out + 'b_learn_italian.png')
    for ch in ['ruy', 'scotch', 'vienna', 'attacks', 'qgd', 'london', 'd4x', 'other', 'italian']:
        pg.click(f'.rtile[data-ch="{ch}"]'); pg.wait_for_timeout(300)
        assert pg.evaluate('S.chapter') == ch
        stats = pg.evaluate("[...document.querySelectorAll('.hero .stat')].map(s => s.innerText.replace(/\\n/g, ' '))")
        print(f'  {ch}:', stats)
        if ch in ('attacks', 'london'):
            pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(150); pg.screenshot(path=out + f'b_learn_{ch}.png', full_page=True)
    print('hash', pg.evaluate('location.hash'))
    # ---- study a lesson: options from White's side, flipped board, eval text
    pg.click('[data-lesson="bi-main"]'); pg.wait_for_timeout(400)
    for _ in range(6): pg.keyboard.press('ArrowRight'); pg.wait_for_timeout(110)
    print('study where:', pg.inner_text('.crumbs .where'), '| card:', pg.inner_text('.mcard').replace('\n', ' / ')[:160])
    opts_h = pg.inner_text('.opts h4') if pg.query_selector('.opts h4') else None
    print('options heading:', opts_h, '| eval:', pg.inner_text('.evaltext'))
    pg.screenshot(path=out + 'b_study.png')
    # first move options at the start (White's first move from your games)
    pg.evaluate("openLine('bo-english', 0)"); pg.wait_for_timeout(300)
    print('root options:', pg.inner_text('.opts h4') if pg.query_selector('.opts h4') else None, pg.evaluate("[...document.querySelectorAll('.opt')].slice(0,4).map(o => o.innerText.replace(/\\n/g,' '))"))
    # ---- drill: White's moves play themselves, you play Black's
    r = drill_line(pg, 'bi-main'); print('drill bi-main:', r); assert r['state'] == 'done' and r['mistakes'] == 0
    r = drill_line(pg, 'br-oo', slip=True); print('drill br-oo with a slip:', r); assert r['state'] == 'done' and r['mistakes'] == 1
    r = drill_line(pg, 'bq-ortho'); print('drill bq-ortho:', r); assert r['state'] == 'done'
    # castling line
    r = drill_line(pg, 'bi-ng5'); print('drill bi-ng5 (castles):', r); assert r['state'] == 'done' and r['mistakes'] == 0
    pg.screenshot(path=out + 'b_drill_done.png')
    # ---- puzzles
    n = pg.evaluate('DATA.puzzles.length'); solved = 0
    for k in range(n):
        pg.evaluate(f'startPuzzle({k})'); pg.wait_for_timeout(350)
        u = pg.evaluate(f'DATA.puzzles[{k}].ok[0]')
        if u in ('e8g8', 'e8c8'): drag(pg, 'e8', 'h8' if u == 'e8g8' else 'a8')
        else: click_move(pg, u[:2], u[2:4])
        pg.wait_for_timeout(350)
        st = pg.evaluate('S.drill.state'); solved += st == 'done'
        if k == 2: pg.screenshot(path=out + 'b_puzzle.png')
    print('puzzles solved', solved, 'of', n, '| prompt:', pg.evaluate("DATA.puzzles[2].q"))
    assert solved == n
    # ---- sandbox as Black
    pg.click('.tabs button[data-view="sandbox"]'); pg.wait_for_timeout(300)
    print('sandbox head:', pg.inner_text('.sechead p')[:90])
    pg.click('#sbGo'); pg.wait_for_timeout(300)
    random.seed(7)
    res = play_sandbox(pg, 0.25, 'b all/real'); assert res['state'] == 'done'
    roots = pg.evaluate("S.drill.choices.filter(c => c.at === 0).length"); print('choices at the start position:', roots); assert roots == 1
    pg.screenshot(path=out + 'b_sb_report.png', full_page=True)
    for scope, odds in [('london', 'real'), ('qgd', 'even'), ('scotch', 'weak'), ('attacks', 'real'), ('other', 'even'), ('vienna', 'real'), ('d4x', 'even'), ('ruy', 'real')]:
        pg.click(f'[data-sbf="scope:{scope}"]'); pg.click(f'[data-sbf="odds:{odds}"]'); pg.wait_for_timeout(100)
        pg.click('#sbAgain'); pg.wait_for_timeout(200)
        r = play_sandbox(pg, 0.1, f'b {scope}/{odds}'); assert r['state'] == 'done'
        first = pg.evaluate("N[S.drill.hist[1]].l")
        assert pg.evaluate(f"inScope(S.drill.hist[S.drill.hist.length-1], '{scope}')"), scope
    # ---- games + cheat
    pg.click('.tabs button[data-view="games"]'); pg.wait_for_timeout(400)
    print('games head:', pg.inner_text('.sechead p'))
    print('insights', pg.locator('.insight').count(), '| cards', pg.locator('.gcard').count(), '| table rows', pg.locator('.orow2').count() - 1)
    assert pg.locator('.insight').count() == 4 and pg.locator('.gcard').count() == 11
    pg.screenshot(path=out + 'b_games.png', full_page=True)
    pg.locator('.insight .btn').nth(3).click(); pg.wait_for_timeout(400)
    print('insight replay ->', pg.inner_text('.crumbs .where'))
    pg.click('.tabs button[data-view="games"]'); pg.wait_for_timeout(300)
    for k in range(11):
        pg.locator('.gcard .btn.primary').nth(k).click(); pg.wait_for_timeout(250)
        assert pg.evaluate("S.view") == 'study'
        pg.click('[data-go="games"]'); pg.wait_for_timeout(200)
    pg.click('.tabs button[data-view="cheat"]'); pg.wait_for_timeout(300)
    print('cheat cards', pg.locator('.ccard').count(), '| first:', pg.locator('.ccard .if').first.inner_text())
    pg.screenshot(path=out + 'b_cheat.png')
    pg.locator('.ccard').nth(20).click(); pg.wait_for_timeout(300); print('cheat ->', pg.inner_text('.crumbs .where'))
    # ---- switch back: White state restored, Black state kept
    pg.click('.tabs button[data-view="drill"]'); pg.wait_for_timeout(200)
    pg.click('.sidesw [data-side="w"]'); pg.wait_for_timeout(500)
    print('back to white:', pg.evaluate('SIDE'), pg.evaluate('S.view'), pg.evaluate('location.hash'), '| learn h2' , pg.inner_text('.reps h2') if pg.query_selector('.reps h2') else '-')
    assert pg.evaluate('FLIP') is False
    pg.click('.tabs button[data-view="learn"]'); pg.wait_for_timeout(300)
    pg.click('.rtile[data-ch="italian"]'); pg.wait_for_timeout(300)
    assert pg.query_selector('#heroReplay') is not None
    pg.click('.sidesw [data-side="b"]'); pg.wait_for_timeout(400)
    print('black again view:', pg.evaluate('S.view'), '| due badge W:', pg.inner_text('#dueW'), pg.is_hidden('#dueW'))
    # ---- deep links
    for h in ['#b.learn.london', '#b.line.bs-mieses', '#b.games', '#learn.sic', '#line.setup']:
        pg2 = ctx.new_page(); hook(pg2)
        pg2.goto(URL + h); pg2.wait_for_timeout(700)
        print('  link', h, '->', pg2.evaluate('[SIDE, S.view, S.chapter, S.line]'))
        pg2.close()
    # ---- phone + dark
    for scheme in ['light', 'dark']:
        ph = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2, color_scheme=scheme)
        q = ph.new_page(); hook(q)
        q.goto(URL + '#b.learn'); q.wait_for_timeout(900)
        ow = q.evaluate('document.documentElement.scrollWidth')
        print(f'phone {scheme}: scrollWidth', ow)
        assert ow <= 390
        q.screenshot(path=out + f'b_phone_learn_{scheme}.png')
        q.evaluate("openLine('bs-mieses')"); q.wait_for_timeout(400)
        for _ in range(5): q.keyboard.press('ArrowRight'); q.wait_for_timeout(100)
        q.screenshot(path=out + f'b_phone_study_{scheme}.png')
        for v in ['drill', 'sandbox', 'games', 'cheat']:
            q.evaluate(f"go('{v}')"); q.wait_for_timeout(300)
            ow = q.evaluate('document.documentElement.scrollWidth'); assert ow <= 390, (v, ow)
        q.evaluate("go('games')"); q.wait_for_timeout(300); q.screenshot(path=out + f'b_phone_games_{scheme}.png', full_page=True)
        ph.close()
    print('ERRORS:', errors[:10])
    b.close()
