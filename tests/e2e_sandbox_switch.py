"""The Sandbox plays both books: with everything picked, games come with White and with Black in turn, and openings from
either book narrow it. Regression: switching the Sandbox opening mid-game must not block moves. Then practice from a chosen position: set up
by hand with the book's moves for both sides (back and forward with the arrows under the board and on the keyboard, a tap
on a move in the list), or picked in a lesson; games start there and only its lines come up. A game that ends on a side
line ends with that line's plan. Also: the player's own move lands at once and only the reply slides, the set-up board
never slides, "What else … plays here" folds away with its arrow and stays the way it was left, the start position
sits under the board, and the count of lines met is the number of lines a game can end on, counted from the book."""
import os, random
from playwright.sync_api import sync_playwright
from e2e_white import drag, play_sandbox, launch, URL, out  # noqa
errors = []
ANIMS = "document.getElementById('db').getAnimations({subtree: true}).length"


def own_move(pg):
    """Play the book's move through the page and say how many pieces were sliding straight after it, then whether the
    reply slid in."""
    for _ in range(30):
        st = pg.evaluate("({busy: S.drill.busy, mine: myTurnAt(S.drill.node)})")
        if not st['busy'] and st['mine']: break
        pg.wait_for_timeout(150)
    at_once = pg.evaluate(f"(() => {{ const u = expectedMove()[0]; tryMove(u.slice(0, 2), u.slice(2, 4)); return {ANIMS}; }})()")
    reply = pg.evaluate(f"new Promise(r => {{ let k = 0; const t = setInterval(() => {{ const a = {ANIMS}; if (a || ++k > 80){{ clearInterval(t); r(a); }} }}, 15); }})")
    return at_once, reply


with sync_playwright() as p:
    b = launch(p)
    pg = b.new_page(viewport={'width': 1280, 'height': 900})
    pg.on('pageerror', lambda e: errors.append(str(e)))
    pg.goto(URL + '#sandbox'); pg.wait_for_timeout(1000)
    # ---- everything: both colours, taking turns, and the count is every line of both books
    ev = pg.evaluate("[sbEverything(), sbSides(), document.querySelector('[data-sbf=\"scope:all\"]').getAttribute('aria-pressed'), document.querySelector('#sbside .queue div:nth-child(3) small').innerText, BOOKS.w.drillable.length + BOOKS.b.drillable.length, document.querySelector('#sbside .queue div:nth-child(3) span').innerText, document.querySelectorAll('.top .sidesw').length]")
    print('everything:', ev); assert ev[:3] == [True, ['w', 'b'], 'true'] and ev[3] == '/' + str(ev[4]) and ev[5] == 'lines met' and ev[6] == 0, ev
    rows = pg.evaluate("[...document.querySelectorAll('#sbside .sbrow')].map(r => [r.querySelector('.sbcol').innerText.trim(), r.querySelectorAll('[data-sbf^=\"pick:\"]').length])")
    assert rows == [['White', pg.evaluate('BOOKS.w.chapters.length')], ['Black', pg.evaluate('BOOKS.b.chapters.length')]], rows
    turns = []
    for k in range(4):
        pg.click('#sbGo' if pg.query_selector('#sbGo') else '#sbAgain'); pg.wait_for_timeout(500)
        turns.append(pg.evaluate("[S.drill.side, SIDE, FLIP, S.drill.scope]"))
        r = play_sandbox(pg, 0.0, f'both {k}'); assert r['state'] == 'done' and pg.evaluate(f"!!LINES['{r['line']}'] && BOOKS[SIDE].drillSet.has('{r['line']}')"), r
    print('four games:', turns)
    assert [t[0] for t in turns] in (['w', 'b', 'w', 'b'], ['b', 'w', 'b', 'w']) and all(t[0] == t[1] and t[2] == (t[0] == 'b') and t[3] == 'all' for t in turns), 'White and Black in turn, the board turned to match'
    assert pg.evaluate("S.sbSession.games") == 4, 'one session for both colours'
    # a whole colour, then one opening of it; the last pick taken away is everything again
    pg.click('[data-sbf="side:b"]'); pg.wait_for_timeout(150)
    assert pg.evaluate("[SB_STATE.w.scope, SB_STATE.b.scope, sbSides()]") == ['none', 'all', ['b']] and pg.inner_text('#sbside .queue div:nth-child(3) small') == '/' + str(pg.evaluate('BOOKS.b.drillable.length'))
    pg.click('[data-sbf="side:w"]'); pg.wait_for_timeout(150); assert pg.evaluate("sbEverything()"), 'both colours picked is everything'
    pg.click('[data-sbf="pick:b:ruy"]'); pg.wait_for_timeout(150)
    assert pg.evaluate("[SB_STATE.w.scope, SB_STATE.b.scope]") == ['none', 'ruy'] and pg.evaluate("sbPool().length") == pg.evaluate("chLines('b', BOOKS.b.chapters.find(c => c.id === 'ruy')).length")
    pg.click('[data-sbf="pick:w:french"]'); pg.wait_for_timeout(150)
    assert pg.evaluate("[SB_STATE.w.scope, SB_STATE.b.scope, sbSides()]") == ['french', 'ruy', ['w', 'b']], 'openings from both books at once'
    both = set()
    for k in range(4):
        pg.click('#sbAgain' if pg.query_selector('#sbAgain') else '#sbGo'); pg.wait_for_timeout(500)
        r = play_sandbox(pg, 0.0, f'two openings {k}'); assert r['state'] == 'done'
        both.add(pg.evaluate(f"SIDE + ':' + chapterOf(lessonOf('{r['line']}')).id"))
    print('a French and a Ruy Lopez session:', sorted(both)); assert both == {'w:french', 'b:ruy'}, both
    pg.click('[data-sbf="pick:b:ruy"]'); pg.click('[data-sbf="pick:w:french"]'); pg.wait_for_timeout(150); assert pg.evaluate("sbEverything()"), 'nothing picked is everything'
    # an opening's lines are the lines of its lessons, the odd ones filed under it too: every one of them can come up
    for sd in ('w', 'b'):
        pg.evaluate(f"useSide('{sd}')")
        diff = pg.evaluate("DATA.chapters.map(C => [C.id, chLines(SIDE, C).length, DRILLABLE.filter(id => inScopeLine(id, C.id)).length, DRILLABLE.filter(id => inScopeLine(id, C.id)).every(id => LINES[id].n.every(i => !i || inScope(i, C.id)))]).filter(x => x[1] !== x[2] || !x[3])")
        assert not diff, diff
    pg.evaluate("useSide('w'); S.drill = S.sbState = null; S.sbSession = null; go('sandbox')"); pg.wait_for_timeout(300)
    pg.click('[data-sbf="pick:w:caro"]'); pg.click('#sbGo'); pg.wait_for_timeout(1500)
    # your own move lands at once; the other side's reply slides in
    snap = own_move(pg); print('own move, then the reply (pieces sliding):', snap); assert snap[0] == 0 and snap[1] > 0, snap
    pg.wait_for_timeout(700)
    # "What else Black plays here": folded until asked for, an arrow on it, and it stays as it was left
    for _ in range(6):
        if pg.locator('#sbElse').count(): break
        own_move(pg); pg.wait_for_timeout(700)
    fold = lambda: pg.evaluate("[document.getElementById('sbElse').open, !!S.sbElse, getComputedStyle(document.querySelector('#sbElse > summary'), '::before').borderRightWidth, document.querySelector('#sbElse > summary').innerText]")
    f0 = fold(); print('the fold-out:', f0); assert f0[:3] == [False, False, '2px'] and 'WHAT ELSE BLACK PLAYS HERE' in f0[3].upper(), f0
    pg.click('#sbElse > summary'); pg.wait_for_timeout(200); assert fold()[:2] == [True, True], 'a tap opens it'
    assert pg.locator('#sbElse > div > *').count() > 0, 'with the other moves in it'
    pg.evaluate("renderSbPanel()"); assert fold()[:2] == [True, True], 'it stays open when the panel is drawn again'
    pg.click('#sbElse > summary'); pg.wait_for_timeout(200); assert fold()[:2] == [False, False], 'and a tap on the arrow folds it away'
    # the count beside the session numbers: every line a game can end on with these settings, counted from the book
    cnt = pg.evaluate("[document.querySelector('#sbside .queue div:nth-child(3) small').innerText, DRILLABLE.filter(id => inScopeLine(id, 'caro')).length, document.querySelector('#sbside .queue div:nth-child(3) span').innerText]")
    print('lines met, of:', cnt); assert cnt[0] == '/' + str(cnt[1]) and 0 < cnt[1] < pg.evaluate('DRILLABLE.length') and cnt[2] == 'lines met', cnt
    # play two correct moves, then switch the chips mid-game
    for _ in range(2):
        for _ in range(20):
            st = pg.evaluate("({busy:S.drill.busy, wtm: myTurnAt(S.drill.node)})")
            if not st['busy'] and st['wtm']: break
            pg.wait_for_timeout(200)
        u = pg.evaluate("sbMyKids(S.drill.node).map(c => N[c].u)[0]"); drag(pg, u[:2], u[2:4]); pg.wait_for_timeout(900)
    pg.click('[data-sbf="pick:w:sic"]'); pg.click('[data-sbf="pick:w:caro"]'); pg.click('[data-sbf="odds:even"]')   # add the Sicilian, take the Caro-Kann out; pg.wait_for_timeout(300)
    print('pending note:', pg.inner_text('.sbpend') if pg.query_selector('.sbpend') else None); assert 'Applies from the next game' in pg.inner_text('.sbpend')
    random.seed(1)
    r = play_sandbox(pg, 0.0, 'after switch')
    assert r['state'] == 'done' and r['slips'] == 0, r
    print('game scope kept:', pg.evaluate("S.drill.scope"), '| next game scope:', pg.evaluate("SB_STATE.w.scope")); assert pg.evaluate("[S.drill.scope, SB_STATE.w.scope, SB_STATE.b.scope]") == ['caro', 'sic', 'none']
    pg.click('#sbAgain'); pg.wait_for_timeout(1500)
    print('new game scope:', pg.evaluate("S.drill.scope"), pg.evaluate("S.drill.odds"))
    # start-now button path
    pg.click('[data-sbf="scope:all"]'); pg.click('[data-sbf="pick:w:french"]'); pg.wait_for_timeout(200)
    pg.click('#sbNow'); pg.wait_for_timeout(1500)
    print('after start-now:', pg.evaluate("S.drill.scope"))
    r = play_sandbox(pg, 0.0, 'french')
    assert r['state'] == 'done'
    # several openings at once: every game stays inside the ones that are picked, and both come up
    pg.click('[data-sbf="pick:w:caro"]'); pg.wait_for_timeout(150)
    assert pg.evaluate('SB_STATE.w.scope') == 'm:caro,french', pg.evaluate('SB_STATE.w.scope')
    assert pg.evaluate("[...document.querySelectorAll('[data-sbf^=\"pick:\"][aria-pressed=\"true\"]')].map(b => b.dataset.sbf)") == ['pick:w:caro', 'pick:w:french']
    met = set()
    for k in range(24):                                   # the Caro-Kann is twice as common: play on until the French has come up too
        if k >= 8 and len(met) == 2: break
        pg.click('#sbNow' if pg.query_selector('#sbNow') else '#sbAgain'); pg.wait_for_timeout(300)
        r = play_sandbox(pg, 0.0, f'mix {k}'); assert r['state'] == 'done'
        met.add(pg.evaluate(f"chapterOf(lessonOf('{r['line']}')).id"))
    print('mixed session met:', sorted(met), '| label:', pg.evaluate('scopeLabel(SB_STATE.w.scope)')); assert met == {'caro', 'french'}, met
    pg.screenshot(path=out + 'sb_mix.png')
    pg.click('[data-sbf="pick:w:french"]'); assert pg.evaluate('SB_STATE.w.scope') == 'caro'
    for c in pg.evaluate('BOOKS.w.chapters.map(C => C.id)'):
        if c != 'caro': pg.click(f'[data-sbf="pick:w:{c}"]')
    assert pg.evaluate('[SB_STATE.w.scope, SB_STATE.b.scope]') == ['all', 'none'] and pg.get_attribute('[data-sbf="side:w"]', 'aria-pressed') == 'true', 'every White opening picked is the whole colour'
    kept = pg.evaluate("['w', 'b'].map(s => JSON.parse(localStorage.getItem(SBK(s)) || '{}').scope)"); assert kept == ['all', 'none'], ('the pick is kept on this device', kept)
    pg.reload(); pg.wait_for_timeout(800)
    if pg.evaluate("!!localStorage.getItem(SBK('w'))"):          # headless Chromium sometimes drops a file:// page's storage across a reload
        assert pg.evaluate('[SB_STATE.w.scope, SB_STATE.b.scope]') == ['all', 'none'], 'and read back when the page opens'
    else: pg.evaluate("SB_STATE.w.scope = 'all'; SB_STATE.b.scope = 'none'; sbSave(); renderSbSide()")
    allc = pg.evaluate("[document.querySelector('#sbside .queue div:nth-child(3) small').innerText, DRILLABLE.length, DATA.lines.filter(l => LESSONS[l.lesson] && !l.n.some(i => (N[i].g || []).includes('warn') && isMine(N[i]))).length, SIDE]")
    print('every White opening:', allc); assert allc[0] == '/' + str(allc[1]) and allc[1] == allc[2] and allc[1] > 300 and allc[3] == 'w', 'every drillable line of the book in play'
    # the start position has its place under the board, not at the bottom of the side column
    where = pg.evaluate("(() => { const b = document.getElementById('db').getBoundingClientRect(), w = document.getElementById('sbwhere').getBoundingClientRect(), s = document.getElementById('sbside').getBoundingClientRect(), u = document.getElementById('sbSetUp').getBoundingClientRect(); return [w.top >= b.bottom, Math.abs(w.left - b.left) < 30, w.right <= s.left + 2, Math.abs((u.left + u.right) / 2 - (b.left + b.right) / 2) < 3, document.getElementById('sbwhere').innerText]; })()")
    print('under the board, centred:', where[:4], ' '.join(where[4].split())[:90]); assert where[:4] == [True, True, True, True] and 'Set up a position' in where[4] and pg.locator('#sbwhere .thumb').count() == 0, where

    # ---- practice from a chosen position: set it up with the book's moves for both sides, by the board or the chips
    pg.click('#sbSetUp'); pg.wait_for_timeout(400)
    # whose book the position is in: a switch on the set-up panel, and the board turns with it
    assert pg.evaluate("[SIDE, document.querySelector('[data-sbset=\"w\"]').getAttribute('aria-pressed')]") == ['w', 'true']
    pg.click('[data-sbset="b"]'); pg.wait_for_timeout(300); assert pg.evaluate("[SIDE, S.drill.kind, S.drill.node, FLIP]") == ['b', 'sbset', 0, True]
    pg.click('[data-sbset="w"]'); pg.wait_for_timeout(300); assert pg.evaluate("[SIDE, S.drill.kind, S.drill.node, FLIP]") == ['w', 'sbset', 0, False]
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
    h3 = pg.inner_text('#sbpanel h3'); assert pg.inner_text('#sbside').strip() == '' and h3.startswith('After move 2 · ') and h3.endswith('lines') and pg.locator('#sbpanel .opn').count() == 1, h3
    drag(pg, 'b8', 'c6'); pg.wait_for_timeout(500)
    # the set-up board never slides: a move for either side, a step back and a step forward are there at once
    slide = pg.evaluate(f"(() => {{ let n = 0; sbSetStep(-1); n += {ANIMS}; sbSetStep(-1); n += {ANIMS}; sbSetStep(1); n += {ANIMS}; sbSetGo(S.drill.fwd[S.drill.fwd.length - 1] ?? sbBookKids(S.drill.node)[0]); n += {ANIMS}; return [n, ply(S.drill.node)]; }})()")
    print('set-up board, pieces sliding over four steps:', slide); assert slide == [0, 4], slide
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
    wh = ' '.join(pg.inner_text('#sbwhere').split()); print('under the board:', wh[:120])
    assert 'From move 2' in wh and 'Change the position' in wh and 'Start from move one' in wh and pg.locator('#sbwhere .thumb').count() == 1
    assert pg.locator('[data-sbf^="pick:"]').count() == 0 and 'After move' not in pg.inner_text('#sbside'), 'the side panel leaves the openings out and no longer carries the position'
    frm = pg.evaluate(f"[document.querySelector('#sbside .queue div:nth-child(3) small').innerText, DRILLABLE.filter(id => LINES[id].n.includes({at})).length, document.querySelector('#sbside .queue div:nth-child(3) span').innerText]")
    print('lines from the position:', frm); assert frm[0] == '/' + str(frm[1]) and frm[1] >= len(lines) and frm[2] == 'lines met', frm
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
    pg.evaluate(f"sbSetFrom(SIDE, {pick['at']}); sbStart()"); pg.wait_for_timeout(1200)
    r = play_sandbox(pg, 0.0, 'to the end of a side line'); assert r['state'] == 'done' and r['line'] == pick['line'], r
    plan = pg.locator('#sbpanel .plan h4').all_inner_texts(); print('its plan:', plan)
    assert plan == [pick['h']], plan
    pg.screenshot(path=out + 'sb_plan.png')
    # ---- never the same line twice in a row. From a position with two or three lines behind it, ten games: every game
    #      ends on another line than the one before. With one line behind the position it is that line every time.
    PLAY = """async at => { sbSetFrom(SIDE, at); const got = [];
        for (let g = 0; g < GAMES; g++){ sbStart();
          for (let t = 0; t < 500; t++){ await new Promise(r => setTimeout(r, 50)); const D = S.drill; if (D.state === 'done') break;
            if (!D.busy && myTurnAt(D.node)){ const ks = sbMyKids(D.node); if (ks.length) sbGo(ks[0], false); } }
          got.push(S.drill.line); }
        return got; }"""
    pg.evaluate("useSide('w'); S.drill = S.sbState = null; SB_STATE.w.scope = 'all'; go('sandbox')"); pg.wait_for_timeout(300)
    spot = pg.evaluate("""(() => { const ends = c => { const ks = myTurnAt(c) ? sbMyKids(c) : sbOppKids(c); return ks.length ? ks.flatMap(ends) : [sbLineFor(c)]; };
        for (const l of Object.values(LINES)){ if (!l.main) continue;
          for (let k = l.n.length - 2; k > 3; k--){ const c = l.n[k]; if (!sbCanFrom(c)) continue; const e = new Set(ends(c)); if (e.size === 2 || e.size === 3) return {at: c, lines: [...e]}; } }
        return null; })()""")
    print('a position with a few lines behind it:', spot); assert spot
    seq = pg.evaluate(PLAY.replace('GAMES', '10'), spot['at']); print('ten games from it:', seq)
    assert len(seq) == 10 and set(seq) <= set(spot['lines']) and all(x != y for x, y in zip(seq, seq[1:])), seq
    one = pg.evaluate(PLAY.replace('GAMES', '3'), pick['at']); print('three games with one line to play:', one)
    assert one == [pick['line']] * 3, one
    pg.evaluate("sbSetFrom(SIDE, null); S.drill = S.sbState = null")
    print('errors', errors)
    assert not [e for e in errors if 'ERR_' not in e], 'page errors'
    b.close()
