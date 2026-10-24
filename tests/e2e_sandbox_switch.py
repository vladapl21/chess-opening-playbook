"""Regression: switching the Sandbox opening mid-game must not block moves."""
import os, random
from playwright.sync_api import sync_playwright
from e2e_white import drag, play_sandbox, launch, URL  # noqa
errors = []
with sync_playwright() as p:
    b = launch(p)
    pg = b.new_page(viewport={'width': 1280, 'height': 900})
    pg.on('pageerror', lambda e: errors.append(str(e)))
    pg.goto(URL + '#sandbox'); pg.wait_for_timeout(1000)
    pg.click('[data-sbf="scope:caro"]'); pg.click('#sbGo'); pg.wait_for_timeout(1500)
    # play two correct moves, then switch the chips mid-game
    for _ in range(2):
        for _ in range(20):
            st = pg.evaluate("({busy:S.drill.busy, wtm: myTurnAt(S.drill.node)})")
            if not st['busy'] and st['wtm']: break
            pg.wait_for_timeout(200)
        u = pg.evaluate("sbMyKids(S.drill.node).map(c => N[c].u)[0]"); drag(pg, u[:2], u[2:4]); pg.wait_for_timeout(900)
    pg.click('[data-sbf="scope:sic"]'); pg.click('[data-sbf="odds:even"]'); pg.wait_for_timeout(300)
    print('pending note:', pg.inner_text('.sbpend') if pg.query_selector('.sbpend') else None)
    random.seed(1)
    r = play_sandbox(pg, 0.0, 'after switch')
    assert r['state'] == 'done' and r['slips'] == 0, r
    print('game scope kept:', pg.evaluate("S.drill.scope"), '| next game scope:', pg.evaluate("SBS.scope"))
    pg.click('#sbAgain'); pg.wait_for_timeout(1500)
    print('new game scope:', pg.evaluate("S.drill.scope"), pg.evaluate("S.drill.odds"))
    # start-now button path
    pg.click('[data-sbf="scope:french"]'); pg.wait_for_timeout(200)
    pg.click('#sbNow'); pg.wait_for_timeout(1500)
    print('after start-now:', pg.evaluate("S.drill.scope"))
    r = play_sandbox(pg, 0.0, 'french')
    assert r['state'] == 'done'
    print('errors', errors)
    b.close()
