"""Regression: switching the Sandbox opening mid-game must not block moves. Then practice from a chosen position: set up
by hand with the book's moves for both sides (back and forward with the arrows under the board and on the keyboard, a tap
on a move in the list), or picked in a lesson; games start there and only its lines come up. A game that ends on a side
line ends with that line's plan."""
import os, random
from playwright.sync_api import sync_playwright
from e2e_white import drag, play_sandbox, launch, URL, out  # noqa
errors = []
with sync_playwright() as p:
    b = launch(p)
    pg = b.new_page(viewport={'width': 1280, 'height': 900})
    pg.on('pageerror', lambda e: errors.append(str(e)))
    pg.goto(URL + '#sandbox'); pg.wait_for_timeout(1000)
    pg.click('[data-sbf="pick:caro"]'); pg.click('#sbGo'); pg.wait_for_timeout(1500)
    # play two correct moves, then switch the chips mid-game
    for _ in range(2):
        for _ in range(20):
            st = pg.evaluate("({busy:S.drill.busy, wtm: myTurnAt(S.drill.node)})")
            if not st['busy'] and st['wtm']: break
            pg.wait_for_timeout(200)
        u = pg.evaluate("sbMyKids(S.drill.node).map(c => N[c].u)[0]"); drag(pg, u[:2], u[2:4]); pg.wait_for_timeout(900)
    pg.click('[data-sbf="pick:sic"]'); pg.click('[data-sbf="pick:caro"]'); pg.click('[data-sbf="odds:even"]')   # add the Sicilian, take the Caro-Kann out; pg.wait_for_timeout(300)
    print('pending note:', pg.inner_text('.sbpend') if pg.query_selector('.sbpend') else None)
    random.seed(1)
    r = play_sandbox(pg, 0.0, 'after switch')
    assert r['state'] == 'done' and r['slips'] == 0, r
    print('game scope kept:', pg.evaluate("S.drill.scope"), '| next game scope:', pg.evaluate("SBS.scope"))
    pg.click('#sbAgain'); pg.wait_for_timeout(1500)
    print('new game scope:', pg.evaluate("S.drill.scope"), pg.evaluate("S.drill.odds"))
    # start-now button path
    pg.click('[data-sbf="scope:all"]'); pg.click('[data-sbf="pick:french"]'); pg.wait_for_timeout(200)
    pg.click('#sbNow'); pg.wait_for_timeout(1500)
    print('after start-now:', pg.evaluate("S.drill.scope"))
    r = play_sandbox(pg, 0.0, 'french')
    assert r['state'] == 'done'
    # several openings at once: every game stays inside the ones that are picked, and both come up
    pg.click('[data-sbf="pick:caro"]'); pg.wait_for_timeout(150)
    assert pg.evaluate('SBS.scope') == 'm:caro,french', pg.evaluate('SBS.scope')
    assert pg.evaluate("[...document.querySelectorAll('[data-sbf^=\"pick:\"][aria-pressed=\"true\"]')].map(b => b.dataset.sbf)") == ['pick:caro', 'pick:french']
    met = set()
    for k in range(24):                                   # the Caro-Kann is twice as common: play on until the French has come up too
        if k >= 8 and len(met) == 2: break
        pg.click('#sbNow' if pg.query_selector('#sbNow') else '#sbAgain'); pg.wait_for_timeout(300)
        r = play_sandbox(pg, 0.0, f'mix {k}'); assert r['state'] == 'done'
        met.add(pg.evaluate(f"chapterOf(lessonOf('{r['line']}')).id"))
    print('mixed session met:', sorted(met), '| label:', pg.evaluate('scopeLabel(SBS.scope)')); assert met == {'caro', 'french'}, met
    pg.screenshot(path=out + 'sb_mix.png')
    pg.click('[data-sbf="pick:french"]'); assert pg.evaluate('SBS.scope') == 'caro'
    for c in pg.evaluate('DATA.chapters.map(C => C.id)'):
        if c != 'caro': pg.click(f'[data-sbf="pick:{c}"]')
    assert pg.evaluate('SBS.scope') == 'all', 'every opening picked is the same as Every opening'
    pg.reload(); pg.wait_for_timeout(800); assert pg.evaluate('SBS.scope') == 'all'

    # ---- practice from a chosen position: set it up with the book's moves for both sides, by the board or the chips
    pg.click('#sbSetUp'); pg.wait_for_timeout(400)
    assert pg.evaluate("[S.drill.kind, S.drill.node, document.getElementById('sbFromGo').disabled]") == ['sbset', 0, True], 'nothing to practise from the start'
    drag(pg, 'e2', 'e4'); pg.wait_for_timeout(500)
    pg.click('[data-sbk] >> nth=0'); pg.wait_for_timeout(500)                      # Black's most common book move, from the chips
    drag(pg, 'b1', 'a3'); pg.wait_for_timeout(400)                               # not in the book: it doesn't go
    assert pg.evaluate("ply(S.drill.node)") == 2 and "isn't in your book" in pg.inner_text('#sbpanel')
    drag(pg, 'g1', 'f3'); pg.wait_for_timeout(500); drag(pg, 'b8', 'c6'); pg.wait_for_timeout(500)
    pg.click('#sbSetBack'); pg.wait_for_timeout(300); assert pg.evaluate("ply(S.drill.node)") == 3, 'back a move'
    # the arrows under the board and on the keyboard step through the moves made; a tap on a move in the list jumps there
    at = lambda: pg.evaluate("[ply(S.drill.node), S.drill.fwd.length]")
    pg.click('#sbSetFwd'); pg.wait_for_timeout(300); assert at() == [4, 0], 'forward again'
    pg.keyboard.press('ArrowLeft'); pg.wait_for_timeout(200); pg.keyboard.press('ArrowLeft'); pg.wait_for_timeout(200); assert at() == [2, 2]
    pg.keyboard.press('ArrowRight'); pg.wait_for_timeout(200); assert at() == [3, 1]
    pg.keyboard.press('Home'); pg.wait_for_timeout(200); assert at() == [0, 4] and pg.evaluate("document.getElementById('sbFromGo').disabled")
    pg.keyboard.press('End'); pg.wait_for_timeout(200); assert at() == [4, 0]
    pg.click('[data-sbj="2"]'); pg.wait_for_timeout(200); assert at() == [2, 2], 'a tap on the second move in the list'
    drag(pg, 'g1', 'f3'); pg.wait_for_timeout(400); assert at() == [3, 1], 'the same move again keeps what came after it'
    assert pg.inner_text('#sbside').strip() == '' and 'lines go on from here' in pg.inner_text('#sbpanel') and pg.locator('#sbpanel .opn').count() == 1
    drag(pg, 'b8', 'c6'); pg.wait_for_timeout(500)
    at = pg.evaluate("S.drill.node"); pg.screenshot(path=out + 'sb_setup.png')
    pg.click('#sbFromGo'); pg.wait_for_timeout(1400)
    st = pg.evaluate("[S.drill.kind, S.drill.from, S.drill.node, S.drill.scope]"); print('a game from the position:', st)
    assert st[:3] == ['sb', at, at] and st[3] == 'all'
    lines = set()
    for k in range(4):
        if k: pg.click('#sbAgain'); pg.wait_for_timeout(300)
        r = play_sandbox(pg, 0.0, f'from the position {k}'); assert r['state'] == 'done'
        assert pg.evaluate(f"LINES['{r['line']}'].n.includes({at}) && S.drill.hist.indexOf({at}) === 4"), 'every game goes through the position'
        lines.add(r['line'])
    print('lines from the position:', sorted(lines))
    assert 'After move 2' in pg.inner_text('#sbside') and pg.locator('[data-sbf^="pick:"]').count() == 0, 'the side panel shows the position, not the openings'
    pg.click('#sbFromClear'); pg.wait_for_timeout(300)
    assert pg.evaluate("sbFrom()") is None and pg.locator('[data-sbf^="pick:"]').count() > 0
    # from a lesson: Practise from here
    pg.evaluate("useSide('b'); openLine(DATA.lessons[3].lines[0], 6)"); pg.wait_for_timeout(600)
    idx = pg.evaluate("LINES[S.line].n[S.i]")
    pg.click('#sbHere'); pg.wait_for_timeout(1400)
    assert pg.evaluate("[S.view, SIDE, S.drill.from]") == ['sandbox', 'b', idx]
    r = play_sandbox(pg, 0.0, 'from a lesson'); assert r['state'] == 'done' and pg.evaluate(f"LINES['{r['line']}'].n.includes({idx})")
    # ---- every game ends with the plan from its last position, side lines too: a position from which the book has
    #      one way on, to the end of a side line with a plan read off the board
    pg.evaluate("useSide('w'); S.drill = S.sbState = null; go('sandbox')"); pg.wait_for_timeout(400)
    pick = pg.evaluate("""(() => { for (const l of Object.values(LINES)){ if (l.main || !l.plan || !DRILLABLE.includes(l.id)) continue;
        let k = l.n.length - 1; while (k > 2 && sbBookKids(l.n[k - 1]).length === 1) k--;
        if (k < l.n.length - 2 && sbCanFrom(l.n[k])) return {line: l.id, at: l.n[k], h: l.plan.h}; } return null; })()""")
    print('a side line to the end:', pick); assert pick
    pg.evaluate(f"SB_FROM[SIDE] = {pick['at']}; sbStart()"); pg.wait_for_timeout(1200)
    r = play_sandbox(pg, 0.0, 'to the end of a side line'); assert r['state'] == 'done' and r['line'] == pick['line'], r
    plan = pg.locator('#sbpanel .plan h4').all_inner_texts(); print('its plan:', plan)
    assert plan == [pick['h']], plan
    pg.screenshot(path=out + 'sb_plan.png')
    print('errors', errors)
    assert not [e for e in errors if 'ERR_' not in e], 'page errors'
    b.close()
