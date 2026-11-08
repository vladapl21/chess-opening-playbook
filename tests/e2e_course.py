"""End-to-end checks for the course: the path, unit pages, unit drills, practice games, checkpoints and the threat sets."""
import random
from playwright.sync_api import sync_playwright
from e2e_white import drag, click_move, launch, URL, out
errors = []


def hook(pg):
    pg.on('pageerror', lambda e: errors.append(f'pageerror: {e}'))
    pg.on('console', lambda m: errors.append(f'console {m.type}: {m.text}') if m.type == 'error' and 'ERR_' not in m.text else None)


def play(pg, u):
    """Play a move on the drill board (drag for castling, tap-tap otherwise)."""
    k = '1' if pg.evaluate('ME') == 1 else '8'
    if u in (f'e{k}g{k}', f'e{k}c{k}'): drag(pg, f'e{k}', f'h{k}' if u[2] == 'g' else f'a{k}')
    else: click_move(pg, u[:2], u[2:4])


def drill_unit_line(pg):
    """Finish the running drill line without a slip."""
    for _ in range(150):
        st = pg.evaluate("({state: S.drill.state, busy: S.drill.busy})")
        if st['state'] == 'done': break
        if st['busy']: pg.wait_for_timeout(200); continue
        play(pg, pg.evaluate("N[LINES[S.drill.id].n[S.drill.i + 1]].u")); pg.wait_for_timeout(800)
    return pg.evaluate("S.drill.state")


def spar_clean(pg):
    """Play the running sandbox game to the end with the prep moves."""
    for _ in range(200):
        st = pg.evaluate("({state: S.drill.state, busy: S.drill.busy, mine: myTurnAt(S.drill.node)})")
        if st['state'] == 'done': break
        if st['busy'] or not st['mine']: pg.wait_for_timeout(220); continue
        play(pg, pg.evaluate("sbMyKids(S.drill.node).map(c => N[c].u)[0]")); pg.wait_for_timeout(600)
    return pg.evaluate("({state: S.drill.state, slips: S.drill.slips.length})")


def quiz(pg, wrong_first=()):
    """Answer every position of the running quiz; items whose index is in wrong_first get one wrong move first."""
    n = pg.evaluate('S.quizState.items.length')
    for k in range(n):
        pg.wait_for_timeout(250)
        it = pg.evaluate('S.quizState.items[S.quizState.k]')
        good = (it.get('ok') or it.get('safe'))
        if k in wrong_first:
            bad = [m for m in (it.get('legal') or pg.evaluate('legalFor()')) if m not in good and len(m) == 4]
            play(pg, bad[0]); pg.wait_for_timeout(1300)
            if pg.evaluate('S.quizState.state') == 'refuted':
                assert pg.inner_text('#qpanel').count('answers') >= 1, pg.inner_text('#qpanel')
                pg.click('#qRetry'); pg.wait_for_timeout(250)
        play(pg, good[0]); pg.wait_for_timeout(450)
        assert pg.evaluate('S.quizState.state') == 'shown', pg.evaluate('S.quizState.state')
        pg.click('#qNext'); pg.wait_for_timeout(350)
    return pg.evaluate("({state: S.quizState.state, res: S.quizState.res})")


with sync_playwright() as p:
    b = launch(p)
    ctx = b.new_context(viewport={'width': 1280, 'height': 900})
    pg = ctx.new_page(); hook(pg)
    pg.goto(URL); pg.wait_for_timeout(1200)
    assert pg.evaluate('S.view') == 'course', pg.evaluate('S.view')
    rows = pg.locator('.urow').count(); print('units', rows, '| locked', pg.locator('.ucard.locked').count(), '| soon', pg.locator('.ucard.soon').count())
    assert rows == 17 and pg.locator('button.ucard').count() == 1
    pg.screenshot(path=out + 'c_course.png', full_page=True)

    # ---- unit 1: idea, a lesson, a drill line, the checkpoint
    pg.click('#cGo'); pg.wait_for_timeout(500)
    assert pg.evaluate('[S.view, S.unit, SIDE]') == ['unit', 'w-italian', 'w']
    for _ in range(3): pg.keyboard.press('ArrowRight'); pg.wait_for_timeout(120)
    assert pg.evaluate("!!up('w-italian').idea")
    pg.click('[data-ulesson="center"]'); pg.wait_for_timeout(400)
    assert pg.evaluate('[S.view, S.studyFrom]') == ['study', 'unit']
    print('lesson crumbs:', pg.inner_text('.crumbs').replace('\n', ' | '))
    pg.keyboard.press('End'); pg.wait_for_timeout(300)
    assert pg.evaluate("lessonSeen('w', 'center')")
    pg.screenshot(path=out + 'c_lesson_end.png')
    pg.click('.lesson-actions [data-unit="w-italian"]'); pg.wait_for_timeout(400)
    assert pg.evaluate('S.view') == 'unit'
    print('learn step:', pg.locator('.step').nth(1).locator('.cnt').inner_text())
    pg.click('[data-ustep="drill"]'); pg.wait_for_timeout(700)
    assert pg.evaluate('[S.view, S.drill.unit]') == ['drill', 'w-italian']
    assert drill_unit_line(pg) == 'done'
    print('drill done box:', pg.inner_text('.donebox').replace('\n', ' | ')[:200])
    assert pg.query_selector('#dNextU') is not None
    pg.click('.donebox [data-unit="w-italian"]'); pg.wait_for_timeout(400)
    print('drill step:', pg.locator('.step').nth(2).locator('.cnt').inner_text())
    pg.click('[data-ustep="cp"]'); pg.wait_for_timeout(500)
    pg.screenshot(path=out + 'c_checkpoint.png')
    r = quiz(pg, wrong_first=(2,)); print('checkpoint 1:', r)
    assert r['state'] == 'done' and r['res'].count(True) == 5
    pg.screenshot(path=out + 'c_checkpoint_done.png')
    assert pg.evaluate("unitPassed(UNIT['w-italian']) && unitOpen(UNIT['b-slav'])")
    pg.click('.donebox [data-unit="b-slav"]'); pg.wait_for_timeout(500)
    assert pg.evaluate('[S.view, S.unit, SIDE, FLIP]') == ['unit', 'b-slav', 'b', True]
    pg.screenshot(path=out + 'c_unit_slav.png', full_page=True)

    # ---- unit 2: a practice game against the unit's lines, then the checkpoint
    pg.click('[data-ustep="spar"]'); pg.wait_for_timeout(600)
    assert pg.evaluate("S.drill.scope") == 'u:b-slav'
    random.seed(3)
    for g in range(2):
        r = spar_clean(pg); assert r['state'] == 'done' and r['slips'] == 0, r
        first = pg.evaluate("N[S.drill.hist[1]].u"); assert first == 'd2d4', first
        if g == 0: pg.click('#sbAgain'); pg.wait_for_timeout(500)
    print('practice games:', pg.evaluate("up('b-slav')"))
    assert pg.evaluate("up('b-slav').spar") == 2
    print('sandbox banner:', pg.inner_text('.cban').replace('\n', ' | '))
    pg.screenshot(path=out + 'c_spar_report.png', full_page=True)
    pg.click('.donebox [data-unit="b-slav"]'); pg.wait_for_timeout(400)
    pg.click('[data-ustep="cp"]'); pg.wait_for_timeout(500)
    r = quiz(pg); print('checkpoint 2:', r); assert r['res'].count(True) == 6

    # ---- unit 3: the threat sets face whichever colour you had in that game
    pg.evaluate("openUnit('threats')"); pg.wait_for_timeout(400)
    assert pg.evaluate("unitOpen(UNIT['threats'])")
    pg.screenshot(path=out + 'c_unit_threats.png', full_page=True)
    pg.click('[data-ustep="s1"]'); pg.wait_for_timeout(500)
    sides = pg.evaluate("S.quizState.items.map(i => i.me)")
    pg.screenshot(path=out + 'c_threat_q1.png')
    # first position: a wrong move gets played out and punished, then the retry counts as a miss
    r = quiz(pg, wrong_first=(0, 3)); print('set 1:', r, '| colours', ''.join(sides))
    assert r['res'] == [False, True, True, False] + [True] * (len(r['res']) - 4)
    assert pg.evaluate("up('threats').s1") == len(r['res']) - 2
    pg.screenshot(path=out + 'c_threat_done.png')
    # the board turned for each position: after the set, the loaded book's colour is back
    pg.click('.donebox [data-unit="threats"]'); pg.wait_for_timeout(400)
    assert pg.evaluate('[ME, FLIP]') == [0, True], pg.evaluate('[ME, FLIP, SIDE]')

    # ---- the path now: two passed, unit 3 current, review chips appear once lines are due
    pg.click('.tabs button[data-view="course"]'); pg.wait_for_timeout(400)
    print('meter:', pg.inner_text('.cmeter'), '| current:', pg.inner_text('.ucard.cur b'))
    assert pg.locator('.ubub.pass').count() == 2
    pg.screenshot(path=out + 'c_course_after.png', full_page=True)

    # ---- links and reloads keep the course place; switching colour goes back to the path
    pg.goto(URL + '#unit.b-italian'); pg.reload(); pg.wait_for_timeout(900)
    print('deep link b-italian ->', pg.evaluate('[S.view, S.unit, SIDE]'))
    assert pg.evaluate('[S.view, S.unit, SIDE]') == ['unit', 'b-italian', 'b']
    assert 'opens when you pass' in pg.inner_text('.lockednote')
    pg.click('.sidesw [data-side="w"]'); pg.wait_for_timeout(400)
    assert pg.evaluate('[S.view, SIDE]') == ['course', 'w']
    stored = pg.evaluate("JSON.parse(localStorage.getItem('italian-playbook-progress-v1')).course")
    print('stored course progress:', {k: v for k, v in stored['u'].items()}, '| lessons seen', list(stored['seen']))
    ctx.close()

    # ---- phone, light and dark: no sideways scroll on the path, a unit page or a quiz
    for scheme in ['light', 'dark']:
        ph = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2, color_scheme=scheme, is_mobile=True, has_touch=True)
        q = ph.new_page(); hook(q)
        q.goto(URL + '#course'); q.wait_for_timeout(900)
        for what, js in [('course', None), ('unit', "openUnit('w-italian')"), ('quiz', "startQuiz('w-italian', 'cp')"), ('threat', "startQuiz('threats', 's2')")]:
            if js: q.evaluate(js); q.wait_for_timeout(500)
            ow = q.evaluate('document.documentElement.scrollWidth'); assert ow <= 390, (scheme, what, ow)
            q.screenshot(path=out + f'c_phone_{what}_{scheme}.png', full_page=what in ('course', 'unit'))
        ph.close()
    print('ERRORS:', errors[:10])
    assert not errors
    b.close()
