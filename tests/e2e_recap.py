"""The monthly recap in Your games, with chess.com stubbed: the first check reads this month and the two before it, the
months before this one are final, the part shows the month beside the one before, the coach says when a finished
month's recap is new, Check now reads again, a failed check saves nothing, and the claude.ai copy (which can't reach
chess.com) points to the website instead. The fixture is the house account's own games, re-dated into three months."""
import json, re, random, datetime
from pathlib import Path
from playwright.sync_api import sync_playwright
from e2e_white import launch, URL, out, ROOT
errors = []
ART = (ROOT / 'data' / 'build' / 'playbook.html').as_uri()


def hook(pg):
    pg.on('pageerror', lambda e: errors.append(f'pageerror: {e}'))
    pg.on('console', lambda m: errors.append(f'console {m.type}: {m.text}') if m.type == 'error' and 'ERR_' not in m.text and '503' not in m.text else None)   # 503: the failed check below


# three calendar months (UTC, as chess.com files them): this one and the two before
today = datetime.datetime.now(datetime.timezone.utc)
def shift(y, m, n):
    k = y * 12 + m - 1 + n; return k // 12, k % 12 + 1
KEYS = [shift(today.year, today.month, -n) for n in range(3)]           # [(y, m) this month, last month, the one before]
G = ['[Event ' + g for g in (ROOT / 'data/games/aqua_alpaca.pgn').read_text().split('[Event ')[1:]]
random.seed(4)
def redate(g, y, m, d, elo):
    g = re.sub(r'\[Date "[^"]*"\]', f'[Date "{y}.{m:02d}.{d:02d}"]', g)
    side = 'White' if '[White "aqua_alpaca"]' in g else 'Black'
    return re.sub(rf'\[{side}Elo "\d+"\]', f'[{side}Elo "{elo}"]', g)
days_now = max(1, today.day - 1)
MONTHS = {KEYS[2]: [redate(g, *KEYS[2], 1 + i % 28, 900 + i * 2 + random.randint(-6, 6)) for i, g in enumerate(G[:30])],
          KEYS[1]: [redate(g, *KEYS[1], 1 + i % 28, 955 + i + random.randint(-8, 8)) for i, g in enumerate(G[5:50])],
          KEYS[0]: [redate(g, *KEYS[0], 1 + i % days_now, 990 + i * 2 + random.randint(-5, 5)) for i, g in enumerate(G[10:40])]}
key = lambda ym: f'{ym[0]}-{ym[1]:02d}'
hits, fail = [], {'on': False}


def chesscom(route):
    u = route.request.url; m = re.search(r'/player/([^/]+)/games/(\d{4})/(\d\d)$', u); hits.append(u)
    if fail['on']: return route.fulfill(status=503, body='busy')
    if m and m.group(1) == 'aqua_alpaca' and (int(m.group(2)), int(m.group(3))) in MONTHS:
        ym = (int(m.group(2)), int(m.group(3)))
        return route.fulfill(status=200, content_type='application/json', body=json.dumps({'games': [{'rules': 'chess', 'time_class': 'blitz', 'pgn': g} for g in MONTHS[ym]]
            + [{'rules': 'chess', 'time_class': 'bullet', 'pgn': MONTHS[ym][0]}, {'rules': 'chess960', 'time_class': 'blitz', 'pgn': MONTHS[ym][1]}]}))
    route.fulfill(status=404, content_type='application/json', body='{}')


with sync_playwright() as p:
    b = launch(p)
    ctx = b.new_context(viewport={'width': 1280, 'height': 900}); ctx.route('https://api.chess.com/**', chesscom); ctx.route('https://lichess.org/**', lambda r: r.fulfill(status=200, content_type='application/x-chess-pgn', body=MONTHS[KEYS[1]][0]))
    pg = ctx.new_page(); hook(pg)
    pg.goto(URL); pg.wait_for_timeout(900)
    assert pg.evaluate("[Recap.on(), Recap.can(), JSON.stringify(Recap.acct())]") == [True, True, '{"site":"chess.com","user":"aqua_alpaca"}'], 'the house playbook reads its own account'
    assert pg.evaluate("(() => { const keep = [PERSONA, Prog.d.me]; PERSONA = 'ready'; Prog.d.me = {state: 'ready', src: {site: 'lichess', user: 'Someone'}}; const a = Recap.aid(); Prog.d.me = {state: 'ready', src: {site: 'pgn', user: 'x'}}; const b = Recap.on(); [PERSONA, Prog.d.me] = keep; return [a, b]; })()") == ['lichess:someone', False], 'a personal playbook reads the account it was built from; files alone have none'
    assert pg.evaluate("Recap.read({site: 'lichess', user: 'Someone'}, '%s').then(t => t.includes('[Event'))" % key(KEYS[1])), 'Lichess games are read by date'
    hits.clear()

    # ---- the first check: this month, the month before (final once it is over) and the one before that
    pg.evaluate("Coach.hush(); S.gseg = 'recap'; go('games')"); pg.wait_for_timeout(300)
    assert pg.locator('.gseg [data-gseg="recap"][aria-selected="true"]').count() == 1
    pg.wait_for_function('!Recap.busy && !!(Prog.d.recap || {}).chk', timeout=60000); pg.wait_for_timeout(300)
    got = sorted(h.split('/games/')[1] for h in hits); print('read:', got)
    assert got == sorted(f'{y}/{m:02d}' for y, m in KEYS)
    st = pg.evaluate("Object.fromEntries(Object.entries(Prog.d.recap.m).map(([k, M]) => [k, [M.all[0], M.fin, M.tc, M.rs.length > 1, Object.keys(M.ch).length > 3, !!M.best]]))"); print('months:', st)
    assert st[key(KEYS[0])][:2] == [30, False] and st[key(KEYS[1])][:2] == [45, True] and st[key(KEYS[2])][:2] == [30, True], 'bullet and other variants are left out; past months are final'
    assert all(v[2] == 'blitz' and v[3] and v[4] and v[5] for v in st.values())
    size = pg.evaluate('JSON.stringify(Prog.d.recap).length'); print('stored:', size, 'characters'); assert size < 6000, 'a month is a small summary'
    txt = pg.inner_text('#view'); print('status:', pg.inner_text('.rcstat').replace('\n', ' | '))
    assert 'chess.com · aqua_alpaca' in txt and 'Checked just now' in txt and 'Next check after' in txt
    # first the month that has just ended (opening it marks it seen), then this month so far, then the one before
    assert pg.locator('.rctiles li').count() == 4 and pg.inner_text('.rctiles li:first-child b') == '45' and 'So far' not in pg.inner_text('.rcnav h3')
    assert pg.evaluate('Prog.d.recap.seen') == key(KEYS[1]) and pg.locator('.gseg .sgdot').count() == 0
    assert 'since ' in pg.inner_text('.rcchg').lower() and pg.locator('.rcprac .rcrow').count() >= 4 and pg.locator('.rchist tbody tr').count() == 3
    assert not re.search(r'\b[KQRBN]?[a-h]x?[a-h]?[1-8]\b', re.sub(r'\b(f7|f2)\b', '', pg.inner_text('.gbody'))), 'no chess notation'
    pg.screenshot(path=out + 'r_month.png', full_page=True)
    pg.click('.rcnav [aria-label="Month after"]'); pg.wait_for_timeout(300)
    assert pg.inner_text('.rctiles li:first-child b') == '30' and 'So far' in pg.inner_text('.rcnav h3') and pg.locator('.rcnav [aria-label="Month after"][disabled]').count() == 1
    pg.click('.rchist [data-rcm="%s"]' % key(KEYS[2])); pg.wait_for_timeout(300)
    assert pg.evaluate('Prog.d.recap.seen') == key(KEYS[1]), 'seen is the latest month opened' 
    pg.locator('.rcchart').scroll_into_view_if_needed(); box = pg.locator('.rcchart .rch').nth(2).bounding_box(); pg.mouse.move(box['x'] + box['width'] / 2, box['y'] + box['height'] / 2); pg.wait_for_timeout(200)
    tip = pg.inner_text('.rctip'); print('tip:', tip); assert pg.is_visible('.rctip') and re.match(r'^\w{3} \d+: \d{3,4}$', tip)

    # ---- when it checks: not again for six hours, then once more; Check now reads at once, and only what can change
    assert pg.evaluate('Recap.due()') is False
    hits.clear(); pg.click('#rcGo'); pg.wait_for_timeout(200); pg.wait_for_function('!Recap.busy', timeout=30000); pg.wait_for_timeout(200)
    print('check now read:', [h.split('/games/')[1] for h in hits]); assert [h.split('/games/')[1] for h in hits] == [f'{KEYS[0][0]}/{KEYS[0][1]:02d}'], 'a final month is not read again'
    assert pg.evaluate("Prog.d.recap.chk = Date.now() - 7 * 36e5; Recap.tried = 0; Recap.due()") is True
    # a failed check: said on the page, nothing saved, the next try waits
    fail['on'] = True; chk = pg.evaluate('Prog.d.recap.chk'); pg.click('#rcGo'); pg.wait_for_timeout(200); pg.wait_for_function('!Recap.busy', timeout=30000); pg.wait_for_timeout(200)
    print('after a failure:', pg.inner_text('.rcstat').replace('\n', ' | ')); assert "didn't answer" in pg.inner_text('.rcstat') and pg.evaluate('Prog.d.recap.chk') == chk and pg.evaluate('Recap.due()') is False
    fail['on'] = False

    # ---- the coach: a finished month that hasn't been opened is news on any tab, once; the switch shows a dot
    # (seen only moves forward in a merge, so it is set back on this device alone, in memory and on disk, and the coach
    # forgets what it has said; a save as the page unloads then writes the same)
    pg.evaluate("Prog.d.recap.seen = '%s'; Prog.saveLocal(); Coach.seen = {}; try { localStorage.removeItem('playbook-coach'); } catch(e){}" % key(KEYS[2])); pg.reload(); pg.wait_for_timeout(1500)
    bub = pg.inner_text('#coach .cbub'); print('coach:', bub.replace('\n', ' | ')); assert 'recap is ready' in bub and pg.locator('#coach [data-cgo="recap"]').count() == 1
    pg.evaluate("S.gseg = 'open'; go('games')"); pg.wait_for_timeout(300); assert pg.locator('.gseg .sgdot').count() == 1, 'the switch marks the new recap'
    pg.evaluate("Coach.hush(); go('course')"); pg.wait_for_timeout(300); assert 'recap is ready' not in pg.inner_text('#coach'), 'said once'
    pg.evaluate("Coach.say('x', {cta: ['recap', 'See the recap']})"); pg.click('#coach [data-cgo="recap"]'); pg.wait_for_timeout(400)
    assert pg.evaluate('[S.view, S.gseg]') == ['games', 'recap'] and key(KEYS[1]) in pg.evaluate("Recap.cur()") and pg.evaluate('Prog.d.recap.seen') == key(KEYS[1])
    assert pg.locator('.gseg .sgdot').count() == 0 and 'So far' not in pg.inner_text('.rcnav h3'), 'the way in opens the finished month'
    # no dates and no account names in the rest of Your games
    for seg in ('open', 'shots', 'games'):
        pg.evaluate(f"S.gseg = '{seg}'; renderGames()"); pg.wait_for_timeout(150); t = pg.inner_text('#view')
        assert 'both accounts' not in t and 'vladapl' not in t and not re.search(r'\b(January|February|March|April|May|June|July|August|September|October|November|December|Jul|Oct|Nov) \d', t), seg

    # ---- phone and dark
    ph = b.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True, color_scheme='dark'); ph.route('https://api.chess.com/**', chesscom)
    q = ph.new_page(); hook(q); q.goto(URL); q.wait_for_timeout(900); q.evaluate("Coach.hush(); S.gseg = 'recap'; go('games')")
    q.wait_for_function('!Recap.busy && !!(Prog.d.recap || {}).chk', timeout=60000); q.wait_for_timeout(300); q.evaluate('Coach.hush()')
    w = q.evaluate('document.documentElement.scrollWidth'); print('phone recap', w); assert w <= 390
    q.screenshot(path=out + 'r_phone.png', full_page=True); ph.close()

    # ---- the claude.ai copy can't reach chess.com: it says where recaps are made, and asks nothing of chess.com
    hits.clear(); art = ctx.new_page(); hook(art); art.goto(ART); art.wait_for_timeout(900)
    art.evaluate("Coach.hush(); S.gseg = 'recap'; go('games')"); art.wait_for_timeout(600)
    print('claude.ai copy:', art.inner_text('.rcstat').replace('\n', ' | ')); assert 'made on the website' in art.inner_text('.rcstat') and not hits and not art.evaluate('Recap.can()')
    b.close()

print('ERRORS:', errors); assert not errors
print('recap checks passed')
