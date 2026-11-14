"""The daily habit and what comes with it: today's five in Drill, the streak, the mark on the Drill tab, badges with the
coach's medal, the profile, settings that arrive from another device, the footer, and the engine board that steps back
to move one."""
from playwright.sync_api import sync_playwright
from e2e_white import launch, URL, out, click_move
errors = []


def hook(pg):
    pg.on('pageerror', lambda e: errors.append(f'pageerror: {e}'))
    pg.on('console', lambda m: errors.append(f'console {m.type}: {m.text}') if m.type == 'error' and 'ERR_' not in m.text else None)


def play_line(pg, slip=False):
    """Play the drill line on the board to its end; one wrong move first if asked."""
    for _ in range(160):
        st = pg.evaluate('({state: S.drill.state, busy: S.drill.busy})')
        if st['state'] == 'done': return
        if st['busy']: pg.wait_for_timeout(150); continue
        u = pg.evaluate('N[LINES[S.drill.id].n[S.drill.i + 1]].u')
        if slip:
            wrong = pg.evaluate(f"(DATA.legal[String(dNode())] || []).find(m => m !== '{u}' && m.length === 4)")
            pg.evaluate(f"tryMove('{wrong[:2]}', '{wrong[2:4]}')"); pg.wait_for_timeout(700); slip = False
            continue
        pg.evaluate(f"tryMove('{u[:2]}', '{u[2:4]}')"); pg.wait_for_timeout(720)
    raise AssertionError('line did not finish')


with sync_playwright() as p:
    b = launch(p)
    ctx = b.new_context(viewport={'width': 1280, 'height': 900}); pg = ctx.new_page(); hook(pg)
    pg.goto(URL); pg.wait_for_timeout(900)

    # ---- no counts beside White and Black or on Drill; a mark on Drill until today's five are done
    assert pg.locator('.sidesw .badge, .tabs .badge').count() == 0
    assert pg.is_visible('#drillDot') and pg.inner_text('#drillDot') == '!'
    assert pg.is_visible('#meBtn') and pg.inner_text('#meBtn').strip() == '0'
    foot = pg.inner_text('#foot'); print('footer:', foot.replace('\n', ' | ')); assert 'your coach' in foot and '© ' in foot and 'Stockfish' not in foot

    # ---- today's five: the oldest slip first, from either book, from move one
    pg.evaluate("""(() => { const t = Date.now();
        Prog.d.lines['bi-main'] = {box: 0, seen: 2, clean: 1, last: t - 5 * DAY, due: t - 5 * DAY};       // a Black line slipped on five days ago
        Prog.d.lines['center'] = {box: 0, seen: 1, clean: 0, last: t - 2 * DAY, due: t - 2 * DAY};        // a White line slipped on two days ago
        Prog.d.lines['grab'] = {box: 2, seen: 3, clean: 2, last: t - 3 * DAY, due: t - DAY};              // due, no slip
        Prog.saveLocal(); })()""")
    nxt = pg.evaluate('dailyNext()'); print('first of today:', nxt); assert nxt == {'s': 'b', 'id': 'bi-main', 'why': 'You slipped here last time'}
    pg.click('.tabs [data-view="drill"]'); pg.wait_for_timeout(400)
    t0 = pg.inner_text('.today'); assert 'Start today' in t0 and '0' in t0
    assert pg.locator('.dmore').get_attribute('open') is None, 'picking lines yourself is folded away'
    pg.screenshot(path=out + 'd_today.png')
    pg.click('#dailyGo'); pg.wait_for_timeout(600)
    d = pg.evaluate('[SIDE, S.drill.id, S.drill.s0, S.drill.daily, S.drill.msgWhy]'); print('drill:', d)
    assert d == ['b', 'bi-main', 0, True, 'You slipped here last time'], 'the Black slip, played from move one'
    assert pg.evaluate("document.getElementById('coach').querySelector('.cbub')") is None, 'the coach is quiet while a line is played'
    play_line(pg, slip=True)
    assert pg.evaluate('[Daily.count(), Prog.rec("bi-main").box]') == [1, 0]
    order = [pg.evaluate('S.drill.id')]
    for k in range(4):
        pg.click('#dDaily'); pg.wait_for_timeout(500)
        order.append(pg.evaluate('S.drill.id'))
        if k == 0: assert pg.evaluate('[SIDE, S.drill.id]') == ['w', 'center'], 'then the White slip'
        if k == 1: assert pg.evaluate('S.drill.id') == 'grab', 'then what is due'
        play_line(pg)
    print('today:', order); assert len(set(order)) == 5
    st = pg.evaluate('({n: Daily.count(), streak: Daily.streak(), dot: document.getElementById("drillDot").hidden, chip: document.getElementById("meN").textContent})')
    print('after five:', st); assert st == {'n': 5, 'streak': 1, 'dot': True, 'chip': '1'}
    bub = pg.inner_text('#coach .cbub'); print('coach:', bub.replace('\n', ' | ')); assert "today's five" in bub.lower() or 'New badge' in bub
    assert 'Keep going' in pg.inner_text('.donebox') and "today's five" in pg.inner_text('.donebox')
    pg.screenshot(path=out + 'd_five.png')
    pg.click('#dToday'); pg.wait_for_timeout(300); assert pg.evaluate('S.drill') is None and 'done' in pg.inner_text('.today')

    # ---- the streak: days in a row, today counted once it is done; two devices' days add up
    pg.evaluate("""(() => { const D = Prog.d.days; D[dayKey(-1)] = ['a','b','c','d','e']; D[dayKey(-2)] = ['a','b','c','d','e','f']; D[dayKey(-4)] = 9; Prog.save(); })()""")
    pg.wait_for_timeout(300)
    assert pg.evaluate('[Daily.streak(), Daily.best()]') == [3, 3]
    bub = pg.inner_text('#coach .cbub'); print('streak medal:', bub.replace('\n', ' | ')); assert 'New badge: Three in a row' in bub
    m = pg.evaluate("""(() => { const k = dayKey(); const x = mergeProg({days: {[k]: ['a', 'b', 'c']}}, {days: {[k]: ['c', 'd', 'e'], '2026-01-01': 7}}); return [x.days[k].length, x.days['2026-01-01']]; })()""")
    assert m == [5, 7], m
    y = pg.evaluate("(() => { const keep = Prog.d.days; Prog.d.days = {[dayKey(-1)]: ['a','b','c','d','e'], [dayKey(-2)]: ['a','b','c','d','e']}; const r = [Daily.streak(), Daily.done(0)]; Prog.d.days = keep; return r; })()")
    assert y == [2, False], 'an open today keeps yesterday\'s streak alive'

    # ---- badges: earned quietly the first time, then the coach brings a medal; the profile shows them all
    got = pg.evaluate('Object.keys(Prog.d.badges || {})'); print('badges so far:', got); assert 'l1' in got and 's3' in got
    assert 'l10' not in got
    pg.evaluate("Badges.queue = []; Coach.hush()")
    pg.evaluate("for (let k = 0; k < 10; k++) Prog.d.lines['x' + k] = {box: 1, seen: 1, clean: 1, last: Date.now(), due: Date.now() + DAY}; useSide('w'); startDrillLine('setup')"); pg.wait_for_timeout(400)
    pg.evaluate('Prog.save()'); pg.wait_for_timeout(200)
    assert pg.evaluate('Badges.queue.map(B => B.id)') == ['l10'] and pg.evaluate("document.querySelector('#coach .cbub')") is None, 'held back while a line is played'
    play_line(pg); pg.wait_for_timeout(400)
    bub = pg.inner_text('#coach .cbub'); print('medal:', bub.replace('\n', ' | ')); assert 'New badge: Ten lines' in bub and pg.locator('#coach .cmedal svg').count() == 1
    pg.screenshot(path=out + 'd_medal.png')
    pg.click('#coach [data-cgo="me"]'); pg.wait_for_timeout(300)
    assert pg.evaluate('Acct.mode') == 'me'
    n_got, n_lock = pg.locator('#acctPanel .bdg.got').count(), pg.locator('#acctPanel .bdg.lock').count(); print('profile badges:', n_got, 'earned,', n_lock, 'locked')
    assert n_got >= 3 and n_lock >= 8 and n_got + n_lock == pg.evaluate('BADGES.length')
    assert pg.locator('#acctPanel .bdg.lock .bprog').count() == n_lock and 'days in a row' in pg.inner_text('#acctPanel .pstreak')
    pg.screenshot(path=out + 'd_profile.png')
    pg.keyboard.press('Escape'); pg.wait_for_timeout(200); assert pg.evaluate('Acct.mode') is None
    assert pg.evaluate("mergeProg({badges: {l1: 5}}, {badges: {l1: 3, l10: 9}}).badges") == {'l1': 3, 'l10': 9}

    # ---- settings from another device: the newer copy wins, the coach changes face
    pg.evaluate("Prog.d.set = {theme: 'light', size: 'm', board: 'plum', coords: true, coach: true, who: 'rook', t: Date.now() + 1000}; refresh()"); pg.wait_for_timeout(300)
    assert pg.evaluate("[SET.who, SET.board, document.documentElement.dataset.board, coachName()]") == ['rook', 'plum', 'plum', 'Rocco']
    pg.evaluate("Prog.d.set = {who: 'pawn', t: 1}; refresh()"); pg.wait_for_timeout(200)
    assert pg.evaluate("[SET.who, Prog.d.set.who]") == ['rook', 'rook'], 'an older copy gives way to this device'
    # (headless Chromium can lose a file:// page's storage written just before a scripted reload: give it a moment)
    pg.wait_for_timeout(1200); pg.reload(); pg.wait_for_timeout(800); assert pg.evaluate('SET.who') == 'rook', pg.evaluate("[SET.who, localStorage.getItem('playbook-settings')]")

    # ---- the engine board steps back to move one from where you came in
    pg.evaluate("useSide('w'); openLine('fried-liver')"); pg.wait_for_timeout(400); pg.keyboard.press('End'); pg.wait_for_timeout(300)
    n = pg.evaluate('LINES["fried-liver"].n.length - 1')
    pg.click('#exHere'); pg.wait_for_timeout(500)
    X = pg.evaluate('({start: S.ex.start, base: S.ex.base, i: S.ex.i, n: S.ex.moves.length})'); print('explore:', X)
    assert X['start'] == pg.evaluate('START_FEN') and X['base'] == n and X['i'] == n and X['n'] == n
    assert pg.locator('.timeline .trow').count() == n and pg.locator('.timeline .chip.came').count() == 1
    assert pg.evaluate("exChess().fen()") == pg.evaluate("nodeFen(LINES['fried-liver'].n[LINES['fried-liver'].n.length - 1])")
    pg.screenshot(path=out + 'd_explore.png')
    pg.click('#xFirst'); pg.wait_for_timeout(300); assert pg.evaluate('S.ex.i') == 0 and pg.evaluate('exChess().fen()') == pg.evaluate('START_FEN')
    pg.click('#xCame'); pg.wait_for_timeout(300); assert pg.evaluate('S.ex.i') == n
    pg.keyboard.press('ArrowLeft'); pg.keyboard.press('ArrowLeft'); pg.wait_for_timeout(300)
    u = pg.evaluate("exChess().moves({verbose: true}).map(m => m.from + m.to).find(x => x !== S.ex.moves[S.ex.i])")
    pg.evaluate(f"exTry('{u[:2]}', '{u[2:4]}')"); pg.wait_for_timeout(300)
    assert pg.evaluate('[S.ex.base, S.ex.moves.length]') == [0, n - 1] and pg.locator('#xCame').count() == 0, 'a new move before the entry point clears the mark'
    pg.wait_for_timeout(1000); pg.reload(); pg.wait_for_timeout(800); assert pg.evaluate('S.view') == 'explore' and pg.evaluate('S.ex.start') == pg.evaluate('START_FEN')

    # ---- phone: Drill and the profile fit
    ph = b.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True, color_scheme='dark'); q = ph.new_page(); hook(q)
    q.goto(URL + '#drill'); q.wait_for_timeout(900)
    w = q.evaluate('document.documentElement.scrollWidth'); print('phone drill', w); assert w <= 390
    q.screenshot(path=out + 'd_phone_today.png', full_page=True)
    q.click('#meBtn'); q.wait_for_timeout(300); assert q.evaluate('Acct.mode') == 'me'
    assert q.evaluate('document.documentElement.scrollWidth') <= 390 and q.evaluate('document.getElementById("acctPanel").scrollWidth <= document.getElementById("acctPanel").clientWidth + 1')
    q.screenshot(path=out + 'd_phone_profile.png')
    b.close()

print('ERRORS:', errors); assert not errors
print('daily checks passed')
