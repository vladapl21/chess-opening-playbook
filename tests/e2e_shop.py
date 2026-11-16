"""The shop and the levels: points from lines played and days kept, a level chip in the corner with a card for each new
level, a wardrobe that opens at level 5, tokens from badges, days in a row and levels, buying and wearing looks for the
coach, items that need a badge, the look on every coach and in the corner, and the record of it all."""
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
    assert pg.locator('.item.lock').count() == pg.evaluate('SHOP.length') - 1, 'every item but the classic look is locked'
    pg.screenshot(path=out + 's_locked.png', full_page=True)

    # ---- six days in a row, then today's five: a week in a row, but points, not days, open the wardrobe
    pg.evaluate("""(() => { const D = Prog.d.days = {}; for (let k = 1; k <= 6; k++) D[dayKey(-k)] = ['a','b','c','d','e']; Prog.save(); Badges.queue = []; Coach.hush(); })()""")
    tok = pg.evaluate('[Shop.earned(), Shop.balance(), Shop.isOpen(), Level.xp(), Level.n()]'); print('after six days:', tok)
    assert tok[0]['streak'] == 2 and tok[0]['week'] == 0 and not tok[2] and tok[3] == 6 * 15 and tok[4] == 2, 'a day with today\'s five is worth 15 points'
    pg.wait_for_timeout(1700)   # the points from those days have floated away
    ids = pg.evaluate('DRILLABLE.slice(0, 26)')
    for k, lid in enumerate(ids[:5]):
        pg.evaluate(f"Prog.record('{lid}', true)"); pg.wait_for_timeout(120)
        if k == 0: assert pg.locator('#lvBtn .xpf').count() == 1 and pg.inner_text('#lvBtn .xpf') == '+10', 'points float up from the chip'
        if k == 4: assert pg.locator('#lvBtn .xpf').last.inner_text() == '+25', 'the fifth line also finishes the day'
    pg.wait_for_timeout(300)
    tok = pg.evaluate('[Shop.earned(), Shop.balance(), Shop.isOpen(), Daily.streak(), Level.xp(), Level.n()]'); print('after the seventh day:', tok)
    assert tok[3] == 7 and tok[0]['week'] == 1 and tok[4] == 7 * 15 + 5 * 10 and tok[5] == 3 and not tok[2]
    card = pg.inner_text('#lvup'); print('level card:', card.replace('\n', ' | ')); assert 'Level 3' in card and 'level 5' in card and pg.locator('#lvup [data-go]').count() == 0
    bub = pg.inner_text('#coach .cbub'); print('coach:', bub.replace('\n', ' | ')); assert 'A full week' in bub and pg.locator('#coach [data-cgo="shop"]').count() == 0, 'no way into a shop that is still shut'
    pg.screenshot(path=out + 's_level3.png')
    # ---- twenty-one more lines: level 5, and that card waits with the way in
    for lid in ids[5:]: pg.evaluate(f"Prog.record('{lid}', true)")
    pg.wait_for_timeout(500)
    tok = pg.evaluate('[Shop.earned(), Shop.balance(), Shop.isOpen(), Level.xp(), Level.n(), Prog.d.lvl]'); print('after 26 lines:', tok)
    assert tok[2] and tok[3] == 7 * 15 + 26 * 10 and tok[4] == 5 and tok[5] == 5 and tok[0]['level'] == 1
    assert tok[1] == tok[0]['badges'] + tok[0]['streak'] + tok[0]['week'] + tok[0]['level']
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

    # ---- buy and wear: the coach in the corner wears it; what costs too much can't be bought; some items need a badge
    bal = pg.evaluate('Shop.balance()')
    pg.click('[data-buy="h-tophat"]'); pg.wait_for_timeout(300)
    assert pg.evaluate('Shop.balance()') == bal - 3 and pg.evaluate('Shop.worn().head') == 'h-tophat'
    assert pg.get_attribute('#coach .cav svg', 'viewBox') == '-6 -12 76 76' and pg.locator('#coach .cav svg .g-ros').count() == 1, 'the corner coach wears the hat'
    assert 'Needs the badge' in pg.inner_text('.item:has([data-buy="h-crown"]), .item:has-text("Crown")')
    assert pg.locator('[data-buy="h-crown"]').count() == 0
    poor = pg.evaluate("SHOP.filter(I => I.price > Shop.balance() && !Shop.owns(I.id) && !Shop.lockOf(I)).map(I => I.id)")
    for i in poor: assert pg.is_disabled(f'[data-buy="{i}"]'), i
    pg.click('[data-off="head"]'); pg.wait_for_timeout(200); assert pg.evaluate('Shop.worn().head') is None
    pg.click('[data-wear="h-tophat"]'); pg.wait_for_timeout(200); assert pg.evaluate('Shop.worn().head') == 'h-tophat'
    # a colour, then the same look on another coach
    if pg.evaluate('Shop.balance()') >= 2: pg.click('[data-buy="c-ruby"]'); pg.wait_for_timeout(200); assert pg.get_attribute('#coach .cav svg', 'class') == 'sk-ruby'
    pg.click('.shopside [data-coachwho="rook"]'); pg.wait_for_timeout(300)
    assert pg.evaluate('SET.who') == 'rook' and pg.locator('.mannequin svg .g-ros').count() == 1
    pg.evaluate('Coach.hush()'); pg.screenshot(path=out + 's_open.png', full_page=True)

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
