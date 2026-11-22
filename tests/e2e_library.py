"""After the first course: the big moment, the library with the coach's picks, deep dives and their parts.

The last unit's checkpoint finishes the course and opens the congratulations screen (once, stamped in the progress).
From then on the Course tab is a library: the coach's pick and two more deep dives chosen from how the course went,
the finished course with its path one click away, and the other deep dives folded away. A deep dive's parts work like
units: idea cards, lessons, drills, practice games and a checkpoint that opens the next part.
"""
import re
from playwright.sync_api import sync_playwright
from e2e_white import drag, click_move, launch, out
from serve import Site   # over local HTTP: headless Chromium sometimes drops a file:// page's storage across a scripted reload
site = Site(); URL = site.start()
errors = []


def hook(pg):
    pg.on('pageerror', lambda e: errors.append(f'pageerror: {e}'))
    pg.on('console', lambda m: errors.append(f'console {m.type}: {m.text}') if m.type == 'error' and 'ERR_' not in m.text else None)


def play(pg, u):
    k = '1' if pg.evaluate('ME') == 1 else '8'
    if u in (f'e{k}g{k}', f'e{k}c{k}'): drag(pg, f'e{k}', f'h{k}' if u[2] == 'g' else f'a{k}')
    else: click_move(pg, u[:2], u[2:4])


def quiz(pg):
    """Answer every position of the running checkpoint on the first try."""
    for _ in range(pg.evaluate('S.quizState.items.length')):
        pg.wait_for_timeout(250)
        it = pg.evaluate('S.quizState.items[S.quizState.k]')
        play(pg, it['ok'][0]); pg.wait_for_timeout(450)
        assert pg.evaluate('S.quizState.state') == 'shown', pg.evaluate('S.quizState.state')
        pg.click('#qNext'); pg.wait_for_timeout(350)


def spar_clean(pg):
    for _ in range(200):
        st = pg.evaluate("({state: S.drill.state, busy: S.drill.busy, mine: myTurnAt(S.drill.node)})")
        if st['state'] == 'done': break
        if st['busy'] or not st['mine']: pg.wait_for_timeout(220); continue
        play(pg, pg.evaluate("sbMyKids(S.drill.node).map(c => N[c].u)[0]")); pg.wait_for_timeout(600)
    return pg.evaluate("({state: S.drill.state, slips: S.drill.slips.length})")


def no_notation(t, where):
    bad = [m for m in re.findall(r'\b[a-h][1-8]\b', t) if m not in ('f7', 'f2')] + re.findall(r'\b[KQRBN]x?[a-h][1-8]\b|O-O', t)
    assert not bad, (where, bad)


# every open unit passed but the last; slips on the Scotch unit's lines and a 5 of 6 checkpoint in the Sicilian
SEED = """(() => { const t = Date.now() - 20 * 864e5, open = COURSE.filter(U => !U.soon), last = open[open.length - 1];
  const c = Prog.d.course = {u: {}, seen: {}};
  for (const U of open) if (U !== last) c.u[U.id] = {idea: t, pass: t + 864e5 * (U.k + 1), cp: U.id === 'w-sicilian' ? 5 : 6, spar: 3, sparGames: 3};
  for (const id of unitAllLines(UNIT['b-scotch'])) Prog.d.lines[id] = {box: 0, seen: 3, clean: 1, due: Date.now() + 864e5, last: t, v: VER[id] || 1};
  Prog.save(); return last.id; })()"""

with sync_playwright() as p:
    b = launch(p)
    pg = b.new_page(viewport={'width': 1280, 'height': 900}); hook(pg)
    pg.goto(URL); pg.wait_for_timeout(900)
    n_deep = pg.evaluate('DEEP.length')
    assert n_deep >= 8 and pg.evaluate("DEEP.every(X => X.units.every(U => U.deep === X.id && UNIT[U.id] === U))"), n_deep
    # ---- before the course is finished: deep dives stay shut, the Course tab is the path
    pg.evaluate("openUnit('x-w-italian-1')"); pg.wait_for_timeout(300)
    assert pg.evaluate('unitOpen(UNIT["x-w-italian-1"])') is False and 'Finish your first course to open this' in pg.inner_text('#view')
    last = pg.evaluate(SEED); pg.reload(); pg.wait_for_timeout(900)
    pg.click('.tabs [data-view="course"]'); pg.wait_for_timeout(300)
    assert pg.evaluate('gradAt()') == 0 and pg.locator('.path').count() == 1 and pg.locator('.libcoach').count() == 0
    print('before the last checkpoint: the path, deep dives shut;', n_deep, 'deep dives in the library')

    # ---- the last checkpoint finishes the course: straight to the big moment, the medal stamped quietly
    pg.evaluate(f"startQuiz('{last}', 'cp')"); pg.wait_for_timeout(400)
    quiz(pg); pg.wait_for_timeout(700)
    assert pg.evaluate('S.view') == 'grad' and pg.evaluate('location.hash') == '#grad', pg.evaluate('S.view')
    assert pg.evaluate('gradAt() > 0') and pg.evaluate("!!Prog.d.badges.uall") and not pg.evaluate("Badges.queue.some(B => B.id === 'uall')")
    assert pg.evaluate("document.getElementById('coach').hidden"), 'the corner coach stays away: the page has the coach in it'
    g = pg.inner_text('#view'); no_notation(g, 'grad')
    open_n = pg.evaluate('COURSE.filter(U => !U.soon).length')
    assert 'You finished your course.' in g and pg.inner_text('.grstats li:first-child b') == str(open_n) and 'New badge: Course complete' in g and 'Next: go deeper on' in g, g
    assert pg.locator('.grconf i').count() > 20 and pg.locator('.grstats li').count() == 5
    pg.wait_for_timeout(900); pg.screenshot(path=out + 'lib_grad.png', full_page=True)
    pg.click('#grQuiz'); pg.wait_for_timeout(300)
    assert pg.evaluate('S.view') == 'quiz' and 'Course finished' in pg.inner_text('#qpanel')
    pg.click('[data-grad]'); pg.wait_for_timeout(300)
    assert pg.evaluate('S.view') == 'grad' and pg.locator('.grconf').count() == 0, 'the confetti falls once'
    print('grad screen: medal, five numbers, the coach\'s pick; the last checkpoint one click away')

    # ---- the Course tab is a library now: the coach's pick, two more beside it, the finished course, the rest folded
    pg.click('.tabs [data-view="course"]'); pg.wait_for_timeout(400)
    v = pg.inner_text('#view'); no_notation(v, 'library')
    assert "What's next" in v and 'Also for you' in v.replace('ALSO FOR YOU', 'Also for you') and 'Your first course' in v, v[:600]
    assert pg.locator('.dcard').count() == 2 and pg.locator('.dcard.dpick').count() == 0 and pg.locator('.libmore li').count() == n_deep - 3, 'the coach\'s pick once, two more beside it'
    rank = pg.evaluate("deepRank().map(o => [o.X.id, o.why, o.slips])")
    pick = rank[0][0]; assert pg.evaluate("document.querySelector('.libcoach [data-deep]').dataset.deep") == pick and pg.locator(f'.dcard [data-deep="{pick}"]').count() == 0
    scot = next(r for r in rank if r[0] == 'x-b-scotch')
    assert 'slipped on its lines more than anywhere else' in scot[1] and scot[2] > 0, scot
    assert next(r for r in rank if r[0] == 'x-w-sicilian')[1].endswith('its checkpoint was your lowest, 5 of 6.'), rank
    assert all(r[1] for r in rank) and pg.evaluate("document.getElementById('coach').hidden")
    pg.screenshot(path=out + 'lib_library.png', full_page=True)
    # the reasons follow the course: clean every Scotch line and that reason goes away
    pg.evaluate("for (const id of unitAllLines(UNIT['b-scotch'])) Prog.d.lines[id].clean = Prog.d.lines[id].seen")
    assert 'slipped' not in pg.evaluate("deepRank().find(o => o.X.id === 'x-b-scotch').why")
    pg.evaluate("for (const id of unitAllLines(UNIT['b-scotch'])) Prog.d.lines[id].clean = 1")
    print('library: pick', pick, '| reasons:', rank[0][1], '|', scot[1])

    # ---- the path of the first course is one click away, and its units point to their deep dives
    pg.click('[data-cpath]'); pg.wait_for_timeout(300)
    assert pg.evaluate('location.hash') == '#course.path' and pg.locator('.path .urow').count() == pg.evaluate('COURSE.length') and '← Library' in pg.inner_text('.crumbs')
    pg.evaluate("openUnit('w-italian')"); pg.wait_for_timeout(300)
    assert '← Your course' in pg.inner_text('.crumbs') and pg.locator('[data-deep="x-w-italian"]').count() == 1
    pg.click('[data-deep="x-w-italian"]'); pg.wait_for_timeout(300)
    assert pg.evaluate('location.hash') == '#deep.x-w-italian'

    # ---- a deep dive's page: why it's here for this player, the next part, every part
    d = pg.inner_text('#view'); no_notation(d, 'deep page')
    assert 'Up next · Part 1 of 4' in d and pg.locator('.path .ucard.locked').count() == 3, d[:900]
    pg.screenshot(path=out + 'lib_deep.png', full_page=True)
    pg.click('#dGo'); pg.wait_for_timeout(300)
    assert pg.evaluate('S.view') == 'unit' and pg.evaluate('S.unit') == 'x-w-italian-1' and pg.evaluate("Prog.d.course.u['x-w-italian-1'].o > 0"), 'starting a step marks the deep dive as started'
    u = pg.inner_text('#view'); no_notation(u, 'part page')
    assert 'Deep dive · Part 1 of 4' in u and '← The Italian' in u and 'to pass' in u, u[:800]
    cards = pg.evaluate("UNIT['x-w-italian-1'].idea.map(s => slideOf(UNIT['x-w-italian-1'], s))")
    assert cards[0]['h'] == 'Black steps off early' and all(a.endswith('b') for a in cards[0]['arrows']) and len(cards[0]['arrows']) >= 2
    assert all(c['t'].startswith('Green:') for c in cards[1:]) and len(cards) == 1 + len(pg.evaluate("UNIT['x-w-italian-1'].lessons"))
    for c in cards: no_notation(c['h'] + ' ' + c['t'], 'card')
    for _ in range(len(cards)): pg.click('#iNext') if pg.evaluate("!document.getElementById('iNext').disabled") else None; pg.wait_for_timeout(150)
    assert pg.evaluate("!!up('x-w-italian-1').idea"), 'the last card completes the idea step'
    pg.screenshot(path=out + 'lib_part.png')
    # a lesson card for a move to leave alone: red for it, green for the move to play
    warn = pg.evaluate("slideOf(UNIT['x-w-defences-1'], UNIT['x-w-defences-1'].idea.find(s => s.avoid))")
    assert warn['t'].startswith('Red:') and [a[-1] for a in warn['arrows']] == ['r', 'g'], warn

    # ---- practice games in a part: the opponent plays only the part's moves; the strip names the deep dive
    pg.evaluate("doStep(UNIT['x-w-italian-1'], 'spar')"); pg.wait_for_timeout(500)
    s = pg.inner_text('#sbpanel').lower()
    assert 'part 1 · black steps off early' in s and 'back to the part' in s, s[:300]
    r = spar_clean(pg); assert r == {'state': 'done', 'slips': 0}, r
    assert pg.evaluate("up('x-w-italian-1').spar") == 1 and pg.evaluate("UNIT['x-w-italian-1'].spar.includes(S.drill.line)")
    print('part: cards, practice game in the part\'s lines')

    # ---- the checkpoint opens the next part; the last part finishes the deep dive (a badge, the shelf)
    pg.evaluate("startQuiz('x-w-italian-1', 'cp')"); pg.wait_for_timeout(400); quiz(pg); pg.wait_for_timeout(400)
    assert 'Part 2 is open' in pg.inner_text('#qpanel') and pg.evaluate("unitOpen(UNIT['x-w-italian-2'])")
    X = pg.evaluate("DEEP.find(X => X.units.length === 2 && X.side === 'w').id")
    for part in pg.evaluate(f"DEEPOF['{X}'].units.map(U => U.id)"):
        pg.evaluate(f"startQuiz('{part}', 'cp')"); pg.wait_for_timeout(400); quiz(pg); pg.wait_for_timeout(500)
    q = pg.inner_text('#qpanel')
    assert 'Deep dive finished' in q and pg.locator('#qpanel [data-lib]').count() == 1, q
    assert pg.evaluate("deepDone(DEEPOF['" + X + "']) && !!Prog.d.badges.x1"), 'the deep diver badge'
    pg.click('#qpanel [data-lib]'); pg.wait_for_timeout(400)
    assert pg.locator(f'.libshelf [data-deep="{X}"]').count() == 1 and pg.locator(f'.dcard [data-deep="{X}"]').count() == 0
    started = pg.evaluate("libCards(deepRank()).cards.map(o => [o.X.id, !!o.touched])")
    assert ['x-w-italian', True] in started, started
    print('deep dive', X, 'finished: badge, on the shelf; the Italian shows as started')

    # ---- hashes bring each view back
    for h, want, check in (('#grad', 'grad', "!!document.querySelector('.gradv')"), ('#deep.x-w-italian', 'course', "S.deep === 'x-w-italian' && !!document.querySelector('.chero')"),
                           ('#course.path', 'course', "S.coursePath && !S.deep && !!document.querySelector('.path') && !document.querySelector('.libcoach')"),
                           ('#unit.x-w-italian-2', 'unit', "S.unit === 'x-w-italian-2' && unitOpen(UNIT['x-w-italian-2'])")):
        pg.goto(URL + h); pg.reload(); pg.wait_for_timeout(700)
        assert pg.evaluate('S.view') == want and pg.evaluate(check), (h, pg.evaluate('S.view'))

    # ---- phone, dark: no sideways scrolling anywhere new
    prog = pg.evaluate("JSON.stringify(Prog.d)")
    ph = b.new_page(viewport={'width': 390, 'height': 844}, color_scheme='dark'); hook(ph)
    ph.goto(URL); ph.evaluate("p => localStorage.setItem(PKEY, p)", prog); ph.reload(); ph.wait_for_timeout(700)
    for js, name in (("go('grad')", 'grad'), ("openLibrary()", 'library'), ("openDeep('x-w-italian')", 'deep'), ("openUnit('x-w-italian-2')", 'part')):
        ph.evaluate(js); ph.wait_for_timeout(400)
        w = ph.evaluate('document.documentElement.scrollWidth'); assert w <= 390, (name, w)
        ph.screenshot(path=out + f'lib_phone_{name}.png', full_page=True)
    print('phone dark: grad, library, deep dive and part fit 390px')
    b.close()
site.stop()

print('ERRORS:', errors); assert not errors
print('library checks passed')
