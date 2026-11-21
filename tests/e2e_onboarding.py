"""A new visitor, start to finish: the welcome screen, locked sections, the sandbox, games in (by username against a
stubbed chess.com, and by PGN file), the reading screen, findings, the would-you-rather cards and the personal playbook.
The games are the ones in data/games, read as if they belonged to a new player."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
from e2e_white import launch, out
from serve import Site
# the website's own page, over local HTTP: headless Chromium sometimes drops a file:// page's storage across a scripted reload
site = Site(docs=True); URL = site.start()
ROOT = Path(__file__).resolve().parents[1]
errors = []


def hook(pg):
    pg.on('pageerror', lambda e: errors.append(f'pageerror: {e}'))
    pg.on('console', lambda m: errors.append(f'console {m.type}: {m.text}') if m.type == 'error' and 'ERR_' not in m.text and '404' not in m.text else None)


def games_of(name):
    """The PGN file split into games, as chess.com's API would return them."""
    text = (ROOT / 'data' / 'games' / name).read_text()
    return ['[Event ' + g for g in text.split('[Event ')[1:]]


with sync_playwright() as p:
    b = launch(p, house=False)
    ctx = b.new_context(viewport={'width': 1280, 'height': 900}); pg = ctx.new_page(); hook(pg)
    # a stand-in for chess.com's public API: two monthly archives for one player, 404 for anyone else
    v1, v2 = games_of('vladapl_1.pgn'), games_of('vladapl_2.pgn')
    as_json = lambda gs: json.dumps({'games': [{'rules': 'chess', 'time_class': 'blitz', 'pgn': g} for g in gs]})
    def api(route):
        u = route.request.url
        if '/player/vladapl/games/archives' in u: route.fulfill(status=200, content_type='application/json', body=json.dumps({'archives': ['https://api.chess.com/pub/player/vladapl/games/2026/09', 'https://api.chess.com/pub/player/vladapl/games/2026/10']}))
        elif u.endswith('/2026/09'): route.fulfill(status=200, content_type='application/json', body=as_json(v1))
        elif u.endswith('/2026/10'): route.fulfill(status=200, content_type='application/json', body=as_json(v2))
        else: route.fulfill(status=404, content_type='application/json', body='{}')
    ctx.route('https://api.chess.com/**', api)

    pg.goto(URL); pg.wait_for_timeout(1000)
    assert pg.evaluate('[PERSONA, S.view]') == ['new', 'start']
    assert pg.locator('.tabs button.lock').count() == 4 and 'lock' not in (pg.get_attribute('.tabs [data-view="sandbox"]', 'class') or '')
    w0 = pg.inner_text('.whero'); assert 'built from your own games' in w0 and not any(x in w0 for x in ('150', '200', '50 games', 'Get your playbook', "Hi, I'm")), w0
    assert pg.locator('.wbub, .lockcard').count() == 0 and pg.locator('.wcard .oname').count() == 1 and pg.locator('.wopens').count() == 1, 'the welcome shows the product, not a motto'
    assert pg.is_hidden('#meBtn') and pg.is_hidden('#drillDot'), 'no streak or drill mark before there is anything to drill'
    pg.screenshot(path=out + 'o_start.png', full_page=True)
    for v in ('course', 'drill', 'games', 'shop'):
        pg.click(f'.tabs [data-view="{v}"]'); pg.wait_for_timeout(250)
        assert pg.locator('.plocked').count() == 1 and pg.locator('#view .urow, #view .rtile, #view .mrow').count() == 0, v
    pg.screenshot(path=out + 'o_locked.png')
    assert pg.evaluate("(location.hash = '#line.setup', 1)") and True
    pg.reload(); pg.wait_for_timeout(800)
    assert pg.evaluate('S.view') == 'start' and pg.locator('#view .movecard, #view .lhead').count() == 0, 'a deep link into a lesson lands on the welcome screen'
    # the sandbox works without games
    pg.click('.tabs [data-view="sandbox"]'); pg.wait_for_timeout(500)
    assert pg.evaluate('S.view') == 'sandbox' and pg.locator('#sbpanel').count() == 1
    print('coach in the sandbox:', pg.inner_text('#coach .cbub').replace('\n', ' | ')[:120])
    pg.screenshot(path=out + 'o_sandbox.png')
    pg.click('.brand'); pg.wait_for_timeout(300); assert pg.evaluate('S.view') == 'start'

    # games in by username: unknown name, then a real one
    pg.click('[data-pgo="setup"]'); pg.wait_for_timeout(300)
    pg.screenshot(path=out + 'o_setup.png', full_page=True)
    pg.fill('#uname', 'nobody_here'); pg.click('#uform button[type=submit]'); pg.wait_for_timeout(600)
    print('unknown player:', pg.inner_text('.pmsg')); assert 'no player called' in pg.inner_text('.pmsg')
    assert not any(x in pg.inner_text('#view') for x in ('150', '200')), 'no game counts on the connect screen'
    # this player has fewer games than a repertoire needs (bullet left out): play more first
    pg.fill('#uname', 'VladAPL'); pg.click('#uform button[type=submit]'); pg.wait_for_timeout(900)
    assert pg.evaluate('S.view') == 'setup' and pg.locator('.pshort').count() == 1, pg.inner_text('#view')[:300]
    sh = pg.inner_text('.pshort'); print('not enough games:', sh.replace('\n', ' | ')[:200]); assert 'Not enough games yet' in sh and 'vladapl' in sh and not any(c.isdigit() for c in sh)
    assert pg.evaluate("Prog.d.me.short.user") == 'vladapl'
    pg.screenshot(path=out + 'o_short.png', full_page=True)
    pg.reload(); pg.wait_for_timeout(800)
    assert pg.locator('.pshort').count() == 1, 'still not enough after a reload'
    pg.evaluate("go('start')"); pg.wait_for_timeout(300)
    assert pg.locator('.whero [data-pgo="setup"]').inner_text() == 'Check my games again'
    pg.click('.whero [data-pgo="setup"]'); pg.wait_for_timeout(300); assert pg.locator('.pshort').count() == 1
    # (the made-up player gets a lower bar here, so the rest of the flow can run on the games in data/games)
    pg.evaluate("Product.need = 90"); pg.click('[data-recheck]'); pg.wait_for_timeout(900)
    assert pg.evaluate('S.view') == 'reading', pg.evaluate('S.view')
    pg.wait_for_timeout(1500); pg.screenshot(path=out + 'o_reading.png')
    pg.wait_for_function("S.view === 'findings'", timeout=60000); pg.wait_for_timeout(400)
    me = pg.evaluate("({state: Prog.d.me.state, n: Prog.d.me.P.n, user: Prog.d.me.P.user, src: Prog.d.me.src, rating: Prog.d.me.P.rating, leaks: Prog.d.me.P.leaks.length})")
    print('profile:', me); assert me['state'] == 'new' and me['n'] == 99 and me['user'] == 'vladapl' and me['src']['site'] == 'chess.com' and me['rating'] > 800   # the one bullet game is left out
    assert pg.evaluate("Prog.d.me.short") is None
    pg.screenshot(path=out + 'o_findings.png', full_page=True)
    assert pg.locator('.tiles .tile').count() == 4 and pg.locator('.brow').count() >= 3 and pg.locator('.leak').count() >= 1
    pg.reload(); pg.wait_for_timeout(800)   # the profile is kept: the welcome screen offers to carry on
    assert pg.evaluate('S.view') in ('findings', 'start')
    if pg.evaluate('S.view') == 'start': pg.click('[data-pgo="findings"]'); pg.wait_for_timeout(300)

    # would you rather
    pg.click('[data-pgo="choices"]'); pg.wait_for_timeout(500)
    n = pg.evaluate('Product.shown().length'); kinds = pg.evaluate('Product.shown().map(c => c.id)'); print('cards:', kinds)
    assert 'blackSic' not in kinds and 'blackSic' in pg.evaluate('Product.cards.map(c => c.id)'), 'which Sicilian? is asked only once the Sicilian is picked'
    assert 'blackD4' in kinds and kinds[-2:] == ['order', 'depth'], kinds   # this player met the d-pawn with something the library lacks
    assert kinds[:2] == ['white', 'blackE4'], kinds                          # the library has two first moves for White and two answers to the e-pawn, so both are asked too
    txt = pg.inner_text('.wyr'); assert 'Ready now' in txt and 'What you play now' in txt and 'Being written' not in txt
    for k in range(n):
        q = pg.evaluate('Product.shown()[Product.ci]')
        if q['id'] == 'blackE4':   # the second step: pick the Sicilian and the next card asks which one; Back, and another pick, take it away again
            sic = next(i for i, o in enumerate(q['opts']) if o['id'] == 'sicilian'); pg.click(f'.duo .wopt >> nth={sic}'); pg.wait_for_timeout(900)
            q2 = pg.evaluate('Product.shown()[Product.ci]'); txt = pg.inner_text('.wyr')
            assert q2['id'] == 'blackSic' and [o['id'] for o in q2['opts']] == ['kan', 'dragon'] and all(o['ready'] for o in q2['opts']), q2
            assert 'Which Sicilian' in txt and 'Dragon' in txt and 'Kan' in txt and f'of {n + 1}' in txt.lower(), txt[:200]
            pg.screenshot(path=out + 'o_choice_second.png', full_page=True)
            pg.click('[data-cback]'); pg.wait_for_timeout(500); assert pg.evaluate('Product.shown()[Product.ci].id') == 'blackE4'
        if q['id'] == 'blackE4':   # five systems on one card: a grid on a wide screen, none cut off or over another, and stacked on a phone
            assert [o['id'] for o in q['opts']] == ['e5', 'sicilian', 'caro', 'scandi', 'french'] and all(o['ready'] for o in q['opts']), q['opts']
            pg.wait_for_timeout(900)   # the cards pop in
            bx = [b_.bounding_box() for b_ in pg.locator('.duo .wopt').all()]; pg.screenshot(path=out + 'o_choice_four.png', full_page=True)
            assert len(bx) == 5 and max(b_['y'] for b_ in bx) - min(b_['y'] for b_ in bx) < 4 and all(bx[i]['x'] + bx[i]['width'] <= bx[i + 1]['x'] for i in range(4)) and bx[4]['x'] + bx[4]['width'] <= 1280, bx
            assert pg.locator('.duo.many .or').count() and not pg.locator('.duo.many .or').first.is_visible(), 'no "or" between five'
            pg.set_viewport_size({'width': 390, 'height': 844}); pg.wait_for_timeout(400)
            xs = [b_.bounding_box()['x'] for b_ in pg.locator('.duo .wopt').all()]
            assert pg.evaluate('document.documentElement.scrollWidth') <= 390 and max(xs) - min(xs) < 4, xs
            pg.screenshot(path=out + 'o_choice_four_phone.png', full_page=True); pg.set_viewport_size({'width': 1280, 'height': 900}); pg.wait_for_timeout(300)
        if q['id'] == 'blackD4':
            pg.screenshot(path=out + 'o_choice_system.png', full_page=True)
            txt = pg.inner_text('.wyr'); assert 'Being written' not in txt and 'Ready now' in txt and 'What you play now' in txt   # every system on the cards is written
            assert [o['id'] for o in q['opts']][0] == 'qgd' and len(q['opts']) == 3 and all(o['ready'] for o in q['opts']), q['opts']
        # take the system the books were first written for; first option for the style cards
        pick = next(i for i, o in enumerate(q['opts']) if o['id'] in ('e4', 'e5', 'slav')) if q['kind'] == 'system' else 0
        pg.click(f'.duo .wopt >> nth={pick}'); pg.wait_for_timeout(350)
        if k == n - 2: pg.screenshot(path=out + 'o_choice_style.png')
    assert pg.evaluate('[S.view, Prog.d.me.state, Prog.d.me.picks.white, Prog.d.me.picks.blackD4, Prog.d.me.picks.order, Prog.d.me.picks.depth]') == ['built', 'ready', 'e4', 'slav', 'leaks', 'core']
    pg.screenshot(path=out + 'o_built.png')
    pg.click('[data-open]'); pg.wait_for_timeout(1500)

    # the personal playbook
    st = pg.evaluate("({persona: PERSONA, view: S.view, units: COURSE.map(U => U.id), locks: document.querySelectorAll('.tabs button.lock').length, why: COURSE.find(U => U.kind !== 'skill').why, kick: COURSE[0].kicker})")
    print('course order:', st['units'][:6], '|', st['kick'], '|', st['why'][:90])
    assert st['persona'] == 'ready' and st['view'] == 'course' and st['locks'] == 0 and 'You met this in' in st['why'] and len(st['units']) == 17
    assert st['units'].index('threats') == 2 and st['units'] != ['w-italian', 'b-slav'] + st['units'][2:], 'the order comes from the games'
    pg.screenshot(path=out + 'o_course.png', full_page=True)
    foot = pg.inner_text('#foot'); print('footer:', foot.replace('\n', ' | '))
    assert '©' in foot and 'playbook,' not in foot and 'study' not in foot and 'Stockfish' not in foot   # the copyright only
    assert pg.is_visible('#meBtn') and pg.is_visible('#drillDot'), 'the streak chip and the drill mark come with a playbook'
    pg.evaluate("go('learn')"); pg.wait_for_timeout(400)
    assert pg.locator('.chnav [data-ch]').count() >= 5 and pg.locator('.changes').count() == 0 and pg.evaluate('tabOf(S.view)') == 'games'
    pg.click('.tabs [data-view="games"]'); pg.wait_for_timeout(500)
    # Your games opens on the openings, every one in the playbook for both colours; the rest is one click away
    n_open = pg.evaluate('BOOKS.w.chapters.length + BOOKS.b.chapters.length')
    assert pg.locator('.otile').count() == n_open and pg.locator('.leak, .gtable').count() == 0 and pg.locator('[data-gseg]').count() == 5
    assert pg.locator('[data-gseg]').nth(1).get_attribute('data-gseg') == 'last', 'the last three games come right after the openings'
    assert pg.locator('[data-gseg="recap"]').count() == 1 and pg.evaluate('Recap.aid()') == 'chess.com:vladapl', 'the monthly recap reads the account the playbook was built from'
    assert pg.locator('.otile:has-text("Not met yet")').count() == n_open - pg.evaluate("Object.keys(Product.me().P.white.systems).filter(id => BOOKS.w.chapters.some(c => c.id === id)).length + Object.keys(Product.me().P.black.systems).filter(id => BOOKS.b.chapters.some(c => c.id === id)).length")
    pg.screenshot(path=out + 'o_games.png', full_page=True)
    pg.click('[data-gseg="games"]'); pg.wait_for_timeout(300)
    assert pg.locator('.gtable tbody tr').count() == 40 and pg.locator('.factl li').count() >= 1
    pg.click('[data-gseg="leaks"]'); pg.wait_for_timeout(300)
    assert pg.locator('.leaks .leak').count() >= 4
    print('first leak:', pg.inner_text('.leaks .leak >> nth=0').replace('\n', ' | ')[:170])
    pg.screenshot(path=out + 'o_games_leaks.png', full_page=True)
    pg.click('.leaks [data-leak] >> nth=0'); pg.wait_for_timeout(500)
    assert pg.evaluate('S.view') == 'study', 'a leak opens its lesson'
    # no text about the house player's games is left anywhere in either book
    left = pg.evaluate("['w','b'].flatMap(s => BOOKS[s].nodes.filter(n => n.t && PERS.test(n.t)).map(n => n.t).concat(BOOKS[s].lessons.filter(l => PERS.test(l.why || '')).map(l => l.why)))")
    print('personal sentences left:', len(left), left[:2]); assert not left
    notation = pg.evaluate("(() => { let t = ''; for (const g of ['open', 'leaks', 'games']){ S.gseg = g; go('games'); t += document.getElementById('view').innerText; } return (t.match(/\\b[KQRBN]?x?[a-h][1-8]\\b/g) || []).filter(x => x !== 'f7' && x !== 'f2'); })()")
    print('notation on the games page:', notation); assert not notation
    pg.click('.tabs [data-view="drill"]'); pg.wait_for_timeout(300); assert pg.evaluate("S.dfilter.pri") == 'core'

    # phone: every step, no sideways scroll; and a PGN file instead of a username
    c2 = b.new_context(viewport={'width': 390, 'height': 844}); ph = c2.new_page(); hook(ph); ph.goto(URL); ph.wait_for_timeout(900)
    wide = lambda tag: (lambda w: (print('  phone', tag, w), w)[1])(ph.evaluate('document.documentElement.scrollWidth'))
    assert wide('start') <= 390; ph.screenshot(path=out + 'o_phone_start.png', full_page=True)
    ph.click('.tabs [data-view="drill"]'); ph.wait_for_timeout(300); assert wide('locked') <= 390
    ph.evaluate("go('setup'); Product.need = 40"); ph.wait_for_timeout(300); assert wide('setup') <= 390
    ph.set_input_files('#pgnFile', str(ROOT / 'data' / 'games' / 'aqua_alpaca.pgn')); ph.wait_for_timeout(600)
    assert ph.evaluate('S.view') == 'reading', ph.inner_text('#view')[:200]
    assert wide('reading') <= 390; ph.screenshot(path=out + 'o_phone_reading.png')
    ph.wait_for_function("S.view === 'findings'", timeout=60000); ph.wait_for_timeout(300)
    assert ph.evaluate("[Prog.d.me.P.user, Prog.d.me.P.n, Prog.d.me.src.site]") == ['aqua_alpaca', 43, 'pgn']   # seven bullet games left out
    assert wide('findings') <= 390; ph.screenshot(path=out + 'o_phone_findings.png', full_page=True)
    ph.click('[data-pgo="choices"]'); ph.wait_for_timeout(400); assert wide('choices') <= 390; ph.screenshot(path=out + 'o_phone_choice.png', full_page=True)
    # too few games in a file: the same 'play more first' screen, no counts, and another try is one tap away
    c3 = b.new_context(viewport={'width': 1280, 'height': 900}); q = c3.new_page(); hook(q); q.goto(URL + '#setup'); q.wait_for_timeout(800)
    small = ROOT / 'tests' / 'out' / 'few.pgn'; small.write_text(''.join(games_of('aqua_alpaca.pgn')[:20]))
    q.set_input_files('#pgnFile', str(small)); q.wait_for_timeout(500)
    sh = q.inner_text('.pshort'); print('too few:', sh.replace('\n', ' | ')[:160]); assert 'Not enough games yet' in sh and 'these files' in sh and q.evaluate('S.view') == 'setup'
    assert q.locator('[data-recheck]').count() == 0; q.click('[data-other]'); q.wait_for_timeout(300); assert q.locator('#uform').count() == 1
    b.close()
site.stop()
print('ERRORS:', errors); assert not errors
print('onboarding checks passed')
