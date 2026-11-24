"""End-to-end checks for the Endings tab and the endings course (app/endings.js), over local HTTP with the real engine.

The house player sees the tab; a new visitor doesn't. A rook mate is won with the exact table's moves (stars, the
record, the points, the engine on the board afterwards); a queen move that throws the win away is taken back with the
answer that punishes it, and the second miss shows the arrow; a king and pawn draw is held against the table's trickiest
tries; a Lucena position is won and a Philidor position held against the engine; a bishop left to be taken is a slip;
one of the house player's own endings is won and says what happened in the game. The course: the Openings | Endings
switch on the Course tab, a unit's pictures, its line to play along, its endings to win and its checkpoint (a wrong
answer shows both arrows), until the unit is passed. Then the phone at 390px in the dark, the deep links, the merge of
two copies of the record, and no notation anywhere the player reads."""
import re, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
sys.path.insert(0, str(Path(__file__).resolve().parent))
from e2e_white import launch, out  # noqa: E402
from serve import Site  # noqa: E402
errors = []


def hook(pg, name=''):
    pg.on('pageerror', lambda e: errors.append(f'{name} pageerror: {e}'))
    pg.on('console', lambda m: errors.append(f'{name} console: {m.text}') if m.type == 'error' and 'ERR_' not in m.text else None)


def notation(text):
    bad = [m for m in re.findall(r'\b[a-h][1-8]\b', text) if m not in ('f7', 'f2')]
    bad += re.findall(r'\b[KQRBN]x?[a-h][1-8]\b|\bO-O\b', text)
    return bad


def clean(pg, where):
    t = pg.inner_text('#app'); bad = notation(t)
    assert not bad, f'{where}: notation {bad}'


def idle(pg, secs=20):
    for _ in range(int(secs * 10)):
        if not pg.evaluate('S.drill && S.drill.busy'): return True
        pg.wait_for_timeout(100)
    return False


def play(pg, best, limit=40, secs=60):
    """Play `best` (a JS expression giving the player's move) until the ending is over."""
    for _ in range(limit):
        if pg.evaluate("S.drill.state") == 'done': break
        assert idle(pg, secs), 'the other side never answered'
        if pg.evaluate("S.drill.state") == 'done': break
        u = pg.evaluate(best)
        assert u, 'no move to play'
        pg.evaluate(f"tryMove('{u[:2]}', '{u[2:4]}')"); pg.wait_for_timeout(250)
    idle(pg, secs)
    return pg.evaluate("[S.drill.state, S.drill.res, S.drill.mine, S.drill.slips, S.drill.stars]")


ENGINE_BEST = "new Promise(r => egSearch(EG.fen(S.drill), x => r(x && x.pv[0]), 16, 900))"

site = Site(); APP = site.start()
try:
    with sync_playwright() as p:
        b = launch(p)
        ctx = b.new_context(viewport={'width': 1280, 'height': 900}); pg = ctx.new_page(); hook(pg, 'desktop')

        # ---- the tab: the house player's, with the kinds to pick from
        pg.goto(APP + '#endings'); pg.wait_for_timeout(1200)
        assert pg.evaluate('S.view') == 'endings' and pg.locator('.tabs [data-view="endings"]').is_visible()
        assert pg.locator('[data-egk="all"][aria-pressed="true"]').count() == 1 and pg.locator('[data-egk]').count() >= 15
        pg.screenshot(path=out + 'eg_home.png'); clean(pg, 'home')
        pg.click('[data-egk="r"]'); pg.wait_for_timeout(200)
        assert pg.evaluate('EG.pick') == ['r'] and pg.evaluate('EG.peek.k') == 'r'
        pg.click('[data-egk="all"]'); pg.wait_for_timeout(200)
        assert pg.evaluate('EG.pick') is None

        # ---- a rook mate, won with the table's moves: stars, the record, points, and the engine on the board after
        xp0 = pg.evaluate('Level.xp()')
        pg.evaluate("EG.start('r-1')"); pg.wait_for_timeout(500)
        assert pg.evaluate('EGTB.t !== null') and pg.locator('#egside .dpanel').count() == 0, 'while it is played the page is the board and its panel'
        st = play(pg, 'EGTB.best(EG.fen(S.drill))')
        print('rook mate:', st)
        assert st[0] == 'done' and st[1] == 'won' and st[3] == 0 and st[4] == 3
        assert pg.evaluate("EG.rd().p['r-1'][0]") == 1 and pg.evaluate("EG.rd().p['r-1'][1]") == 1 and pg.evaluate('Level.xp()') > xp0
        pg.wait_for_timeout(1200)
        assert pg.evaluate("EngineUI.host && EngineUI.host.board") == 'db' and pg.locator('#deng').count() == 1
        assert 'Mate in' in pg.inner_text('#dpanel')
        pg.screenshot(path=out + 'eg_mate.png'); clean(pg, 'mate')

        # ---- a slip: the move is taken back with the answer that punishes it; the second miss shows the arrow
        pg.evaluate("EG.start('q-1')"); pg.wait_for_timeout(500)
        fen = pg.evaluate('EG.fen(S.drill)')
        bad = pg.evaluate("(() => { const f = EG.fen(S.drill); for (const m of new Chess(f).moves({verbose: true})){ const u = m.from + m.to, r = EGTB.after(f, u); if (r && r.w !== 1) return u; } })()")
        pg.evaluate(f"tryMove('{bad[:2]}', '{bad[2:4]}')"); pg.wait_for_timeout(300)
        msg = pg.evaluate('S.drill.msg'); print('a slip:', msg)
        assert pg.evaluate('EG.fen(S.drill)') == fen and pg.evaluate('S.drill.slips') == 1 and not pg.evaluate('S.drill.hint')
        assert ('draw' in msg.lower() or 'win go' in msg) and not notation(msg)
        pg.evaluate(f"tryMove('{bad[:2]}', '{bad[2:4]}')"); pg.wait_for_timeout(300)
        assert pg.evaluate('S.drill.slips') == 1 and pg.evaluate('S.drill.hint') and "arrow" in pg.evaluate('S.drill.msg')
        pg.screenshot(path=out + 'eg_slip.png'); clean(pg, 'slip')
        st = play(pg, 'S.drill.hint || EGTB.best(EG.fen(S.drill))')
        assert st[1] == 'won' and st[3] == 1 and st[4] == 2, st
        assert pg.evaluate("EG.rd().p['q-1']")[:2] == [1, 0], 'a slip: played, not clean'

        # ---- hold a king and pawn draw against the table's trickiest tries
        pg.evaluate("EG.start('kpd-1')"); pg.wait_for_timeout(500)
        assert 'Hold the draw' in pg.inner_text('#dpanel')
        st = play(pg, 'EGTB.best(EG.fen(S.drill))')
        print('king and pawn held:', st)
        assert st[1] == 'held' and st[3] == 0

        # ---- the engine's endings: a Lucena won, a Philidor held
        pg.evaluate("EG.start('luc-1')"); pg.wait_for_timeout(800)
        st = play(pg, ENGINE_BEST, 30); print('Lucena:', st)
        assert st[1] == 'won' and 'Queened' in pg.inner_text('#dpanel')
        # a move on the finished board plays on from there on the explore board, material counted as an ending
        u = pg.evaluate('legalFor()[0]'); pg.evaluate(f"tryMove('{u[:2]}', '{u[2:4]}')"); pg.wait_for_timeout(500)
        assert pg.evaluate('S.view') == 'explore' and pg.evaluate('S.ex.rel') is True
        pg.click('#exBack'); pg.wait_for_timeout(400)
        assert pg.evaluate('S.view') == 'endings' and pg.evaluate('S.drill.state') == 'done'
        pg.evaluate("EG.start('phi-1')"); pg.wait_for_timeout(800)
        st = play(pg, ENGINE_BEST, 14); print('Philidor:', st)
        assert st[1] == 'held'
        pg.screenshot(path=out + 'eg_held.png'); clean(pg, 'held')

        # ---- a lone king against two bishops: a bishop left to be taken is a slip
        pg.evaluate("EG.start('bb-1')"); pg.wait_for_timeout(500)
        drop = pg.evaluate("""(() => { const f = EG.fen(S.drill);
          for (const m of new Chess(f).moves({verbose: true})){ const c = new Chess(f); c.move(m); if (c.moves({verbose: true}).some(x => x.captured) && !c.in_stalemate()) return m.from + m.to; } })()""")
        if drop:
            pg.evaluate(f"tryMove('{drop[:2]}', '{drop[2:4]}')"); pg.wait_for_timeout(1500); idle(pg)
            print('a bishop dropped:', pg.evaluate('S.drill.msg'))
            assert pg.evaluate('S.drill.slips') == 1 and 'throws the win away' in pg.evaluate('S.drill.msg')

        # ---- one of the house player's own endings, won: whose game, and what happened in it
        mine = pg.evaluate("EGD.items.find(i => i.k === 'mine' && i.src.includes('gfrasti')).id")
        pg.evaluate(f"EG.start('{mine}')"); pg.wait_for_timeout(500)
        assert 'vs gfrasti' in pg.inner_text('#dpanel').lower() or 'VS GFRASTI' in pg.inner_text('#dpanel')
        pg.evaluate("tryMove('d4', 'e4')"); pg.wait_for_timeout(600)
        assert pg.evaluate('[S.drill.state, S.drill.res]') == ['done', 'won']
        assert 'In the game: the other rook gave check and the king took the rook that had the mate.' in pg.inner_text('#dpanel')
        pg.screenshot(path=out + 'eg_mine.png'); clean(pg, 'mine')

        # ---- the course: a switch on the Course tab, the units, one unit all the way through
        pg.evaluate("S.drill = S.egState = null"); pg.click('.tabs [data-view="course"]'); pg.wait_for_timeout(500)
        assert pg.locator('[data-cseg]').count() == 2 and pg.locator('[data-cseg="open"][aria-selected="true"]').count() == 1
        pg.click('[data-cseg="end"]'); pg.wait_for_timeout(500)
        assert pg.locator('.path .urow').count() == 7 and 'egcourse' in pg.url
        pg.screenshot(path=out + 'eg_course.png', full_page=True); clean(pg, 'course')
        pg.click('[data-egunit="eg-r"]'); pg.wait_for_timeout(400)
        assert pg.evaluate('S.view') == 'egunit' and pg.evaluate("EG.steps(EG.unit('eg-r')).map(s => s.done)") == [False, False, False, False]
        for _ in range(6):
            if pg.locator('#iNext').is_disabled(): break
            pg.click('#iNext'); pg.wait_for_timeout(120)
        assert pg.evaluate("EG.steps(EG.unit('eg-r'))[0].done")
        pg.screenshot(path=out + 'eg_unit.png', full_page=True); clean(pg, 'unit')
        pg.click('[data-egalong="0"]'); pg.wait_for_timeout(500)
        assert pg.evaluate('S.drill.guided') and pg.evaluate('S.drill.hint')
        u = pg.evaluate('S.drill.hint'); wrong = pg.evaluate(f"legalFor().find(x => x !== '{u}')")
        pg.evaluate(f"tryMove('{wrong[:2]}', '{wrong[2:4]}')"); pg.wait_for_timeout(200)
        assert pg.evaluate('S.drill.moves.length') == 0 and 'green arrow' in pg.evaluate('S.drill.msg'), 'Play along: only the arrow\'s move goes'
        pg.screenshot(path=out + 'eg_along.png'); clean(pg, 'along')
        st = play(pg, 'S.drill.hint', 60)
        assert st[1] == 'along' and pg.evaluate("EG.steps(EG.unit('eg-r'))[1].done")
        # the endings to win: two more rook mates, clean
        for it in ('r-2', 'r-3'):
            pg.evaluate(f"EG.start('{it}', {{unit: 'eg-r'}})"); pg.wait_for_timeout(400)
            st = play(pg, 'EGTB.best(EG.fen(S.drill))'); assert st[1] == 'won' and st[3] == 0
        assert pg.evaluate("EG.steps(EG.unit('eg-r'))[2].done"), 'three rook mates won clean'
        assert pg.evaluate('setTab(S.view) || document.querySelector(\'.tabs [aria-selected="true"]\').dataset.view') == 'course', 'a course game stays under Course'
        # the checkpoint: one wrong answer shows both arrows, the rest right, and the unit is passed
        pg.evaluate("EG.quiz('eg-r')"); pg.wait_for_timeout(400)
        n = pg.evaluate('S.drill.items.length')
        for k in range(n):
            u = pg.evaluate('S.drill.items[S.drill.k].ok[0]') if k else pg.evaluate("Object.keys(S.drill.items[S.drill.k].bad)[0]")
            pg.evaluate(f"tryMove('{u[:2]}', '{u[2:4]}')"); pg.wait_for_timeout(200)
            if not k:
                assert pg.evaluate('S.drill.arrows.map(a => a[4])') == ['r', 'g']; pg.screenshot(path=out + 'eg_check_wrong.png'); clean(pg, 'checkpoint')
            pg.click('#egQNext'); pg.wait_for_timeout(200)
        assert pg.evaluate("EG.rd().u['eg-r'].q[0]") == n - 1 and pg.evaluate("EG.passed(EG.unit('eg-r'))")
        pg.screenshot(path=out + 'eg_check_done.png')
        pg.click('[data-egunit="eg-r"]'); pg.wait_for_timeout(400)
        assert 'Passed' in pg.inner_text('.uhead')

        # ---- the deep links come back to the same place
        for h, view in (('#egcourse', 'course'), ('#egunit.eg-kp', 'egunit'), ('#endings', 'endings')):
            pg.goto(APP + h); pg.reload(); pg.wait_for_timeout(900)
            assert pg.evaluate('S.view') == view, (h, pg.evaluate('S.view'))
        assert pg.evaluate('S.egUnit') == 'eg-kp' or h != '#egunit.eg-kp'

        # ---- two copies of the record: every position's best, every unit's steps
        got = pg.evaluate("""(() => { const a = {end: {p: {'r-1': [2, 1, 5, 2]}, u: {'eg-r': {l: 9, q: [3, 5, 8]}}, n: [2, 1]}}, b = {end: {p: {'r-1': [1, 1, 7, 3], 'q-1': [1, 0, 6, 0]}, u: {'eg-r': {l: 4, a: {'eg-r-a1': 3}, q: [4, 5, 9]}}, n: [1, 1]}};
          const o = mergeProg(a, b); return [o.end.p['r-1'], o.end.p['q-1'], o.end.u['eg-r'].l, o.end.u['eg-r'].a, o.end.u['eg-r'].q, o.end.n]; })()""")
        assert got == [[2, 1, 7, 3], [1, 0, 6, 0], 4, {'eg-r-a1': 3}, [4, 5, 9], [2, 1]], got

        # ---- a phone, in the dark: nothing scrolls sideways
        ph = b.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True, color_scheme='dark'); q = ph.new_page(); hook(q, 'phone')
        for h, shot in (('#endings', 'eg_phone_home'), ('#egcourse', 'eg_phone_course'), ('#egunit.eg-race', 'eg_phone_unit')):
            q.goto(APP + h); q.reload(); q.wait_for_timeout(900)
            assert q.evaluate('document.documentElement.scrollWidth') <= 390, h
            q.screenshot(path=out + shot + '.png', full_page=True)
        q.evaluate("EG.start('race-1')"); q.wait_for_timeout(600)
        assert q.evaluate('document.documentElement.scrollWidth') <= 390
        q.screenshot(path=out + 'eg_phone_game.png', full_page=True)
        ph.close()

        # ---- a new visitor on the website: no Endings tab, and the address of one goes elsewhere
        web = Site(docs=True); WEB = web.start()
        try:
            n2 = launch(p, house=False).new_context(viewport={'width': 1280, 'height': 900}).new_page(); hook(n2, 'new')
            n2.goto(WEB + '#endings'); n2.wait_for_timeout(1500)
            assert n2.evaluate('PERSONA') == 'new' and not n2.locator('.tabs [data-view="endings"]').is_visible() and n2.evaluate('S.view') != 'endings'
        finally:
            web.stop()
finally:
    site.stop()

errs = [e for e in errors if 'ERR_TUNNEL' not in e]
print('ERRORS:', errs)
assert not errs
print('endings checks passed')
