"""The shop and the levels: points from lines played and days kept, a level chip in the corner with a card for each new
level, a shop that opens at level 5, tokens from badges, days in a row and levels. The whole shop is a daily shop: six
pieces set by the date (two hats, two colours, one pair of glasses, one for the neck), the same all day on every device
and different the next day, with only the time left beside it. What is bought goes in the locker, where it is put on;
pieces that need a badge wait there until the badge is earned and then join the rotation. Also: the fit of every piece
on every coach, the look in the corner, and the record of it all."""
from playwright.sync_api import sync_playwright
from e2e_white import launch, URL, out
errors = []


def hook(pg):
    pg.on('pageerror', lambda e: errors.append(f'pageerror: {e}'))
    pg.on('console', lambda m: errors.append(f'console {m.type}: {m.text}') if m.type == 'error' and 'ERR_' not in m.text else None)


with sync_playwright() as p:
    b = launch(p)
    ctx = b.new_context(viewport={'width': 1366, 'height': 900}); pg = ctx.new_page(); hook(pg)
    pg.goto(URL); pg.wait_for_timeout(900)

    # ---- the points and the steps between levels: each level asks a little more than the last
    assert pg.evaluate('[Level.step(1), Level.step(2), Level.step(4)]') == [45, 60, 90]
    assert pg.evaluate('[Level.of(0).n, Level.of(44).n, Level.of(45).n, Level.of(269).n, Level.of(270).n, Level.of(270).into]') == [1, 1, 2, 4, 5, 0]
    assert pg.evaluate("mergeProg({lines: {}, lvl: 3}, {lines: {}, lvl: 5}).lvl") == 5
    lv = pg.evaluate("[Level.n(), document.getElementById('lvN').textContent, document.getElementById('lvBtn').hidden]"); print('level on opening:', lv)
    assert lv == [1, '1', False], 'the chip is in the corner from the start'

    # ---- a tab of its own, locked until level 5; tokens wait
    tabs = pg.locator('.tabs [role=tab]').all_inner_texts(); print('tabs:', tabs); assert tabs[-1] == 'Shop' and len(tabs) == 5
    pg.click('.tabs [data-view="shop"]'); pg.wait_for_timeout(400)
    assert pg.locator('.wlock').count() == 1 and pg.locator('[data-buy]').count() == 0, 'nothing to buy before level 5'
    assert 'level 5' in pg.inner_text('.wlock') and pg.locator('.wlock .wlv i').count() == 5
    assert pg.locator('.items.daily .item.lock').count() == pg.evaluate('Shop.today().length') == 6, 'today\'s shelf is there to look at, with nothing to tap'
    head = ' '.join(pg.inner_text('.shophd').split()); print('the header:', head)
    assert head.startswith('Daily shop Locker') and head.endswith(' left') and pg.locator('#dropT').count() == 1
    page = pg.inner_text('#view').lower()
    for gone in ('two drops', 'today only', 'gone at midnight', 'tomorrow', 'wardrobe', 'days only', 'fridays', 'saturdays'): assert gone not in page, gone
    pg.screenshot(path=out + 's_locked.png', full_page=True)

    # ---- six days in a row, then today's five: a week in a row, but points, not days, open the wardrobe
    pg.evaluate("""(() => { const D = Prog.d.days = {}; for (let k = 1; k <= 6; k++) D[dayKey(-k)] = ['a','b','c','d','e']; Prog.save(); Badges.queue = []; Coach.hush(); })()""")
    tok = pg.evaluate('[Shop.earned(), Shop.balance(), Shop.isOpen(), Level.xp(), Level.n()]'); print('after six days:', tok)
    assert tok[0]['streak'] == 2 and 'week' not in tok[0] and not tok[2] and tok[3] == 6 * 15 and tok[4] == 2, 'a day with today\'s five is worth 15 points'
    pg.wait_for_timeout(1700)   # the points from those days have floated away
    ids = pg.evaluate('DRILLABLE.slice(0, 26)')
    for k, lid in enumerate(ids[:5]):
        pg.evaluate(f"Prog.record('{lid}', true)"); pg.wait_for_timeout(120)
        if k == 0: assert pg.locator('#lvBtn .xpf').count() == 1 and pg.inner_text('#lvBtn .xpf') == '+10', 'points float up from the chip'
        if k == 4: assert pg.locator('#lvBtn .xpf').last.inner_text() == '+25', 'the fifth line also finishes the day'
    pg.wait_for_timeout(300)
    tok = pg.evaluate('[Shop.earned(), Shop.balance(), Shop.isOpen(), Daily.streak(), Level.xp(), Level.n()]'); print('after the seventh day:', tok)
    assert tok[3] == 7 and tok[4] == 7 * 15 + 5 * 10 and tok[5] == 3 and not tok[2]
    card = pg.inner_text('#lvup'); print('level card:', card.replace('\n', ' | ')); assert 'Level 3' in card and 'level 5' in card and pg.locator('#lvup [data-go]').count() == 0
    bub = pg.inner_text('#coach .cbub'); print('coach:', bub.replace('\n', ' | ')); assert ('A week in a row' in bub or 'New badge' in bub) and 'first full week' not in bub and pg.locator('#coach [data-cgo="shop"]').count() == 0, 'no way into a shop that is still shut'
    pg.screenshot(path=out + 's_level3.png')
    # ---- twenty-one more lines: level 5, and that card waits with the way in
    for lid in ids[5:]: pg.evaluate(f"Prog.record('{lid}', true)")
    pg.wait_for_timeout(500)
    tok = pg.evaluate('[Shop.earned(), Shop.balance(), Shop.isOpen(), Level.xp(), Level.n(), Prog.d.lvl]'); print('after 26 lines:', tok)
    assert tok[2] and tok[3] == 7 * 15 + 26 * 10 and tok[4] == 5 and tok[5] == 5 and tok[0]['level'] == 1
    assert tok[1] == tok[0]['badges'] + tok[0]['streak'] + tok[0]['level']
    card = pg.inner_text('#lvup'); print('level card:', card.replace('\n', ' | ')); assert 'Level 5' in card and 'shop is open' in card
    pg.screenshot(path=out + 's_level5.png')
    pg.wait_for_timeout(5600); assert pg.locator('#lvup').count() == 1, 'the card that opens the shop stays until it is used or closed'
    pg.click('#lvup [data-go="shop"]'); pg.wait_for_timeout(400)
    assert pg.evaluate('S.view') == 'shop' and pg.locator('.wlock').count() == 0 and pg.locator('#lvup').count() == 0
    # a level reached while a line is being played waits for the line to end
    pg.evaluate("Prog.d.lvl = 5; startDrillLine(DRILLABLE[40])"); pg.wait_for_timeout(500)
    pg.evaluate("Prog.d.xpb = (Prog.d.xpb || 0) + Level.of().need - Level.of().into; Prog.save()"); pg.wait_for_timeout(300)
    assert pg.evaluate('[Level.n(), Lv.pending, S.drill.state]') == [6, 6, 'play'] and pg.locator('#lvup').count() == 0
    pg.evaluate("delete Prog.d.xpb; S.drillState = S.drill = null; Prog.d.lvl = 5; Lv.pending = 0; Prog.save(); go('shop')"); pg.wait_for_timeout(300)

    # ---- buy and wear: the coach in the corner wears it at once, and says nothing about it; what costs too much can't be bought
    bal = pg.evaluate('Shop.balance()')
    shelf = pg.evaluate('Shop.today().map(I => [I.id, I.slot, I.price, I.name])'); print('today:', [x[0] for x in shelf], '| tokens:', bal)
    assert [x[1] for x in shelf] == ['head', 'head', 'skin', 'skin', 'face', 'neck'] and pg.locator('.items.daily .item').count() == 6
    hat = min((x for x in shelf if x[1] == 'head'), key=lambda x: x[2]); assert hat[2] <= bal, (hat, bal)
    poor = [x[0] for x in shelf if x[2] > bal]
    for i in poor: assert pg.is_disabled(f'[data-buy="{i}"]'), i
    pg.click(f'[data-buy="{hat[0]}"]'); pg.wait_for_timeout(300)
    assert pg.evaluate('Shop.balance()') == bal - hat[2] and pg.evaluate('Shop.worn().head') == hat[0]
    assert pg.locator('#coach .cbub').count() == 0, 'no speech for a purchase'
    vb = pg.get_attribute('#coach .cav svg', 'viewBox'); print('room for the hat:', vb)
    assert vb == pg.evaluate(f"hatBox('knight', '{hat[0]}')") and pg.locator(f'#coach .cav svg [data-g="{hat[0]}"]').count() == 1, 'the corner coach wears the hat'
    assert pg.evaluate('Shop.today().map(I => I.id)') == [x[0] for x in shelf], 'the shelf stays as it was for the day'
    assert pg.locator(f'.items.daily [data-buy="{hat[0]}"]').count() == 0 and pg.locator('.items.daily .item').count() == 5, 'what is bought leaves the shelf for the locker'
    # ---- the fit. Every hat on every coach is inside its picture with a shadow under its rim, the picture makes room
    #      for the hat and little more, and what goes round the knight's neck is cut to the neck (each picture its own cut)
    fit = pg.evaluate("""(() => { const host = document.createElement('div'); host.style.cssText = 'position:absolute;left:0;top:0;width:200px;visibility:hidden'; document.body.appendChild(host); const bad = [];
      for (const c of COACHES) for (const I of SHOP.filter(x => x.slot === 'head')){
        host.innerHTML = `<div style="width:200px;height:200px">${knightSVG('', c.id, {head: I.id}).replace('<svg ', '<svg width="200" height="200" style="overflow:visible" ')}</div>`; const svg = host.querySelector('svg'), r = svg.getBoundingClientRect(), hat = svg.lastElementChild.getBoundingClientRect();
        const vb = svg.getAttribute('viewBox').split(' ').map(Number), top = (hat.top - r.top) / r.height * vb[3];
        if (hat.top < r.top - .5 || hat.left < r.left - .5 || hat.right > r.right + .5) bad.push([c.id, I.id, 'outside']);
        if (vb[1] < 0 && top > 6.5) bad.push([c.id, I.id, 'too much room: ' + top.toFixed(1)]);
        if (!HAT_LOOSE[I.id] && !svg.querySelector('.g-seat')) bad.push([c.id, I.id, 'no shadow']);
      }
      host.remove(); return bad; })()""")
    assert not fit, fit
    neck = pg.evaluate("""(() => { const host = document.createElement('div'); host.style.cssText = 'position:absolute;left:0;top:0;width:200px;visibility:hidden'; document.body.appendChild(host); const out = {};
      for (const I of SHOP.filter(x => x.slot === 'neck')){ host.innerHTML = knightSVG('', 'knight', {neck: I.id}) + knightSVG('', 'knight', {neck: I.id}) + knightSVG('', 'rook', {neck: I.id});
        const [a, b, r] = host.querySelectorAll('svg'), ca = a.querySelector('clipPath'), cb = b.querySelector('clipPath'), g = a.querySelector('[clip-path]');
        out[I.id] = [!!ca && !!g && g.getAttribute('clip-path') === `url(#${ca.id})`, ca && cb && ca.id !== cb.id, !r.querySelector('clipPath'), g ? g.children.length : 0]; }
      host.remove(); return out; })()""")
    print('round the knight\'s neck:', neck)
    assert all(v[0] and v[1] and v[2] and v[3] >= 1 for v in neck.values()) and len(neck) == 7, neck
    # a card shows the piece by itself: the hat just put on is on the mannequin, not on the cards for glasses or scarves
    alone = [pg.locator(f'.mannequin svg [data-g="{hat[0]}"]').count() == 1, pg.locator('.items.daily .ipv.z-face svg [data-g], .items.daily .ipv.z-neck svg [data-g], .items.daily .ipv.z-skin svg [data-g]').count() > 0, pg.locator('.items.daily .ipv.z-head svg').count()]
    assert alone == [True, False, 1], alone
    row = pg.evaluate("[...document.querySelectorAll('.items.daily .item > :last-child')].slice(0, 3).map(e => Math.round(e.getBoundingClientRect().bottom))")
    assert len(row) == 3 and max(row) - min(row) <= 2, ('what a card does sits on one line across a row', row)
    pg.click('[data-shoptab="locker"]'); pg.wait_for_timeout(200)
    pg.click('[data-off="head"]'); pg.wait_for_timeout(200); assert pg.evaluate('Shop.worn().head') is None
    pg.click(f'[data-wear="{hat[0]}"]'); pg.wait_for_timeout(200); assert pg.evaluate('Shop.worn().head') == hat[0]
    # the locker: what is owned, by kind, and under it the pieces a badge still has to earn
    lock = pg.inner_text('.shopmain'); assert hat[3] in lock and 'Earned with a badge' in lock and 'Badge: ' in lock
    need = pg.evaluate("SHOP.filter(I => I.needs && !(Prog.d.badges || {})[I.needs]).map(I => I.id)"); print('waiting for a badge:', need)
    assert need and pg.locator('.shopmain .slot:last-child .item.lock').count() == len(need) and pg.locator('.shopmain .slot:last-child [data-buy]').count() == 0
    assert not set(need) & set(pg.evaluate("Array.from({length: 30}, (_, k) => Shop.on(new Date(2026, 10, 1 + k, 12)).map(I => I.id)).flat()")), 'never on the shelf before the badge'
    pg.click('[data-shoptab="shop"]'); pg.wait_for_timeout(200)
    # a colour, then the same look on another coach
    sk = next((x for x in shelf if x[1] == 'skin' and x[2] <= pg.evaluate('Shop.balance()')), None)
    if sk: pg.click(f'[data-buy="{sk[0]}"]'); pg.wait_for_timeout(200); assert pg.get_attribute('#coach .cav svg', 'class') == 'sk-' + pg.evaluate(f"SKINS['{sk[0]}']")
    pg.click('.shopside [data-coachwho="rook"]'); pg.wait_for_timeout(300)
    assert pg.evaluate('SET.who') == 'rook' and pg.locator(f'.mannequin svg [data-g="{hat[0]}"]').count() == 1
    pg.evaluate('Coach.hush()'); pg.screenshot(path=out + 's_open.png', full_page=True)
    assert 'Spent' not in pg.inner_text('.shopside') and 'week' not in pg.inner_text('.earn').lower(), 'no spent row and no week token'

    # ---- the daily shop's rules: one shelf all day and the same on every device, another the next day, every piece
    #      taking its turn, nothing else for sale, and a piece that is owned or still needs its badge staying out
    on = lambda y, m, d, h=12: pg.evaluate(f"Shop.on(new Date({y}, {m}, {d}, {h})).map(I => I.id)")
    assert on(2026, 10, 16, 1) == on(2026, 10, 16, 23), 'one shelf all day'
    assert on(2026, 10, 16) != on(2026, 10, 17) and not set(on(2026, 10, 16)) & set(on(2026, 10, 17)), 'a new shelf the next day'
    month = set(sum((on(2026, 10, d) for d in range(1, 29)), []))
    forsale = set(pg.evaluate("SHOP.filter(I => I.price && !Shop.owns(I.id) && (!I.needs || (Prog.d.badges || {})[I.needs])).map(I => I.id)"))
    print('pieces for sale:', len(forsale), '| on a shelf within four weeks:', len(month & forsale)); assert forsale <= month, forsale - month
    off = pg.evaluate("SHOP.filter(I => I.price && !Shop.owns(I.id) && !Shop.today().includes(I)).map(I => [I.id, Shop.lockOf(I), Shop.buy(I.id)])")
    assert off and all(x[1] in ('gone', 'badge') and x[2] is False for x in off), 'what is not on today\'s shelf can\'t be bought'
    # a badge earned: its piece joins the rotation
    b0 = pg.evaluate("SHOP.find(I => I.needs && !(Prog.d.badges || {})[I.needs])"); print('a badge piece:', b0['id'], 'needs', b0['needs'])
    pg.evaluate(f"(Prog.d.badges = Prog.d.badges || {{}})['{b0['needs']}'] = Date.now()")
    assert b0['id'] in set(sum((on(2026, 10, d) for d in range(1, 29)), [])), 'with the badge it comes up like any other piece'
    pg.evaluate(f"delete Prog.d.badges['{b0['needs']}']")
    # bought on an earlier day, a piece is out of the rotation for good
    pg.evaluate(f"Prog.d.shop.own['{hat[0]}'] = Date.now() - 3 * DAY; Prog.save()")
    later = pg.evaluate("Array.from({length: 28}, (_, k) => Shop.on(new Date(Date.now() + (k + 1) * DAY)).map(I => I.id)).flat()")
    assert hat[0] not in pg.evaluate('Shop.today().map(I => I.id)') and hat[0] not in later
    pg.evaluate("renderShop()"); pg.wait_for_timeout(200)
    assert pg.locator('.items.daily .item').count() == 6 - (1 if sk else 0), 'the next piece of its kind takes the empty place'
    assert pg.evaluate("/^\\d+ (h \\d+ )?min left$/.test(document.getElementById('dropT').textContent)"), pg.inner_text('#dropT')
    pg.click('[data-shoptab="locker"]'); pg.wait_for_timeout(200)
    names = pg.locator('.shopmain .slot .item b').all_inner_texts(); print('locker:', names[:6]); assert hat[3] in names and (not sk or sk[3] in names)
    pg.screenshot(path=out + 's_locker.png', full_page=True)
    pg.click('[data-shoptab="shop"]'); pg.wait_for_timeout(200)

    # ---- the record: bought items stay bought, the newer choice of what to wear wins, tokens are the same everywhere
    m = pg.evaluate("mergeProg({shop: {own: {'h-cap': 5}, wear: {head: ['h-cap', 10]}}}, {shop: {own: {'h-cap': 3, 'n-bowtie': 4}, wear: {head: ['h-tophat', 20], neck: ['n-bowtie', 4]}}}).shop")
    assert m == {'own': {'h-cap': 3, 'n-bowtie': 4}, 'wear': {'head': ['h-tophat', 20], 'neck': ['n-bowtie', 4]}}, m
    assert pg.evaluate("Shop.spent()") == pg.evaluate("Object.keys(Prog.d.shop.own).reduce((a, id) => a + SHOP.find(x => x.id === id).price, 0)")

    # ---- dark and phone
    ph = b.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True, color_scheme='dark'); q = ph.new_page(); hook(q)
    q.goto(URL + '#shop'); q.wait_for_timeout(900)
    w = q.evaluate('document.documentElement.scrollWidth'); print('phone shop', w); assert w <= 390
    tabs_w = q.evaluate("document.querySelector('.tabs').scrollWidth <= document.querySelector('.tabs').clientWidth + 1"); assert tabs_w, 'the tabs fit on a phone'
    q.screenshot(path=out + 's_phone.png', full_page=True)
    b.close()

print('ERRORS:', errors); assert not errors
print('shop checks passed')
