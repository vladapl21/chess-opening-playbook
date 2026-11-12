"""Checks for the skill units (Spot the threat and the two after it) and for the engine's numbers.

- "Show me the danger" draws the threat and gives up the first-try point.
- A move that loses nothing is accepted even when it is not the engine's own answer.
- A wrong move gets its reason in words; a longer trick is listed move by move and can be played out on the board.
- In a practice set the engine opens on the position once it is answered; in a checkpoint it does not.
- Engine numbers are from White's side whichever colour you play; the words are from yours."""
import re
from playwright.sync_api import sync_playwright
from e2e_white import launch, URL, out
errors = []
NOTATION = re.compile(r'\b[KQRBN]?x?[a-h][1-8]\b|O-O')


def hook(pg):
    pg.on('pageerror', lambda e: errors.append(f'pageerror: {e}'))
    pg.on('console', lambda m: errors.append(f'console {m.type}: {m.text}') if m.type == 'error' and 'ERR_' not in m.text else None)


def at(pg, k):
    pg.evaluate(f"(() => {{ const Q = S.quizState; Object.assign(Q, {{k: {k}, tries: 0, state: 'play', busy: false, flash: null, hint: null, msg: '', view: null, lastU: null, arrows: null, peeked: false, lastTry: null}}); render(); }})()")
    pg.wait_for_timeout(200)


def try_move(pg, u):
    pg.evaluate(f"quizTry('{u}', '{u[2:4]}')"); pg.wait_for_timeout(1300)


with sync_playwright() as p:
    b = launch(p)
    pg = b.new_page(viewport={'width': 1280, 'height': 900}); hook(pg)
    pg.goto(URL); pg.wait_for_timeout(1000)

    # ---- engine numbers
    n = pg.evaluate("(() => { useSide('b'); const a = evalInfo(-40), c = evalInfo(-200), s = evalShort(-130); useSide('w'); const w = evalInfo(-200); return [a.num, a.txt, c.num, c.txt, s.t, s.good, w.num, w.txt]; })()")
    print('numbers:', n)
    assert n == ['−0.4', 'Equal', '−2.0', 'Clearly better for you', '−1.3', True, '−2.0', 'Clearly better for Black'], n

    # ---- a practice set
    pg.evaluate("startQuiz('threats', 's1')"); pg.wait_for_timeout(500)
    items = pg.evaluate("S.quizState.items.map(it => ({fine: it.fine || [], safe: it.safe, deep: Object.keys(it.refute).filter(u => (it.refute[u][3] || []).length), now: Object.keys(it.refute).filter(u => !(it.refute[u][3] || []).length && it.refute[u][4] > 0), played: it.played}))")
    assert all(it['played'] not in it['fine'] and not set(it['fine']) & set(it['safe']) for it in items)
    # show me the danger
    assert pg.locator('#qPeek').count() == 1 and pg.locator('#qEngine').count() == 0, 'before answering: a hint, no engine'
    pg.click('#qPeek'); pg.wait_for_timeout(200)
    st = pg.evaluate("[S.quizState.res[0], S.quizState.arrows.length, document.querySelector('#qpanel .feedback').innerText]"); print('peek:', st)
    assert st[0] is False and st[1] == 1 and st[2].startswith('The danger:')
    try_move(pg, items[0]['safe'][0]); assert pg.evaluate("[S.quizState.state, S.quizState.res[0]]") == ['shown', False]
    # a move that loses nothing counts
    k = next(i for i, it in enumerate(items) if it['fine']); at(pg, k); try_move(pg, items[k]['fine'][0])
    msg = pg.inner_text('#qpanel .feedback'); print('fine move:', msg[:150].replace('\n', ' '))
    assert pg.evaluate(f"[S.quizState.state, S.quizState.res[{k}]]") == ['shown', True] and 'loses nothing' in msg and not NOTATION.search(msg)
    assert pg.locator('#qEngine').count() == 1
    # a wrong move with a longer point
    k = next(i for i, it in enumerate(items) if it['deep']); at(pg, k); u = items[k]['deep'][0]; try_move(pg, u)
    msg = pg.inner_text('#qpanel .feedback'); print('deep:', msg[:330].replace('\n', ' | '))
    assert pg.evaluate("S.quizState.state") == 'refuted' and pg.locator('#qpanel .qline li').count() >= 1 and not NOTATION.search(msg)
    assert 'answers:' in msg and ('The engine now calls it' in msg or 'That costs you' in msg)
    pg.screenshot(path=out + 'k_deep.png')
    pg.click('#qPlay'); pg.wait_for_timeout(400); assert pg.evaluate('S.quizState.busy')
    for _ in range(40):
        if not pg.evaluate('S.quizState.busy'): break
        pg.wait_for_timeout(300)
    assert not pg.evaluate('S.quizState.busy') and pg.evaluate('S.quizState.state') == 'refuted'
    pg.screenshot(path=out + 'k_played_out.png')
    pg.click('#qEngine'); pg.wait_for_timeout(500)
    ex = pg.evaluate("({view: S.view, moves: S.ex.moves.length, i: S.ex.i, first: S.ex.moves[0]})"); print('engine board:', ex)
    assert ex['view'] == 'explore' and ex['first'] == u and ex['i'] == 2 and ex['moves'] >= 3
    pg.evaluate('exBack()'); pg.wait_for_timeout(400)
    assert pg.evaluate("[S.view, S.quizState.k, S.quizState.state]") == ['quiz', k, 'refuted'], pg.evaluate("[S.view, S.quizState && S.quizState.k, S.quizState && S.quizState.state]")
    pg.click('#qRetry'); pg.wait_for_timeout(200); assert pg.evaluate('S.quizState.state') == 'play'
    # a wrong move that loses at once: one sentence, no list
    k = next(i for i, it in enumerate(items) if it['now']); at(pg, k); try_move(pg, items[k]['now'][0])
    msg = pg.inner_text('#qpanel .feedback'); print('at once:', msg[:200].replace('\n', ' | '))
    assert ('That costs you' in msg or 'checkmate' in msg) and pg.locator('#qpanel .qline').count() == 0 and pg.locator('#qPlay').count() == 0

    # ---- a checkpoint: reasons in words, no engine until it is over
    pg.evaluate("startQuiz('threats', 'cp')"); pg.wait_for_timeout(400)
    it = pg.evaluate("(() => { const it = S.quizState.items[0]; return Object.keys(it.refute)[0]; })()"); try_move(pg, it)
    assert pg.evaluate('S.quizState.state') == 'refuted' and pg.locator('#qEngine').count() == 0 and 'answers:' in pg.inner_text('#qpanel .feedback')

    # ---- the other two skill units have reasons too
    for uid in ('finish', 'endings'):
        pg.evaluate(f"startQuiz('{uid}', 's1')"); pg.wait_for_timeout(400)
        u = pg.evaluate("(() => { const it = S.quizState.items[0]; return Object.keys(it.refute).find(u => (it.refute[u][3] || []).length) || Object.keys(it.refute)[0]; })()"); try_move(pg, u)
        msg = pg.inner_text('#qpanel .feedback'); print(uid + ':', msg[:260].replace('\n', ' | '))
        assert 'The engine now calls it' in msg or 'checkmate' in msg.lower(), msg
        assert not NOTATION.search(msg), NOTATION.search(msg)
        assert pg.locator('#qPeek').count() == 0

    # phone width
    ph = b.new_page(viewport={'width': 390, 'height': 844}); hook(ph); ph.goto(URL); ph.wait_for_timeout(800)
    ph.evaluate("startQuiz('threats', 's1')"); ph.wait_for_timeout(300)
    k = next(i for i, it in enumerate(items) if it['deep']); at(ph, k); try_move(ph, items[k]['deep'][0])
    w = ph.evaluate('document.documentElement.scrollWidth'); print('phone scrollWidth', w); assert w <= 390
    ph.screenshot(path=out + 'k_phone.png', full_page=True)
    b.close()

print('ERRORS:', errors); assert not errors
print('skill checks passed')
