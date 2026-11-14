"""The shop: tokens from badges and days in a row, a wardrobe that opens after a week in a row, buying and wearing
looks for the coach, items that need a badge, the look on every coach and in the corner, and the record of it all."""
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

    # ---- a new tab, locked until a week in a row; tokens wait
    tabs = pg.locator('.tabs [role=tab]').all_inner_texts(); print('tabs:', tabs); assert tabs[-1] == 'Shop' and len(tabs) == 6
    pg.click('.tabs [data-view="shop"]'); pg.wait_for_timeout(400)
    assert pg.locator('.wlock').count() == 1 and pg.locator('[data-buy]').count() == 0, 'nothing to buy before a week in a row'
    assert pg.locator('.item.lock').count() == pg.evaluate('SHOP.length') - 1, 'every item but the classic look is locked'
    pg.screenshot(path=out + 's_locked.png', full_page=True)

    # ---- six days in a row, then today's five: the seventh day opens the wardrobe, with the week's badge
    pg.evaluate("""(() => { const D = Prog.d.days = {}; for (let k = 1; k <= 6; k++) D[dayKey(-k)] = ['a','b','c','d','e']; Prog.save(); Badges.queue = []; Coach.hush(); })()""")
    tok = pg.evaluate('[Shop.earned(), Shop.balance(), Shop.isOpen()]'); print('after six days:', tok)
    assert tok[0]['streak'] == 2 and tok[0]['week'] == 0 and not tok[2]
    pg.evaluate("for (const id of ['setup', 'center', 'grab', 'bxa1', 'moller-bf6']) Prog.record(id, true)"); pg.wait_for_timeout(400)
    tok = pg.evaluate('[Shop.earned(), Shop.balance(), Shop.isOpen(), Daily.streak()]'); print('after the seventh day:', tok)
    assert tok[2] and tok[3] == 7 and tok[0]['week'] == 1 and tok[1] == tok[0]['badges'] + tok[0]['streak'] + 1
    bub = pg.inner_text('#coach .cbub'); print('coach:', bub.replace('\n', ' | ')); assert 'wardrobe is open' in bub and pg.locator('#coach [data-cgo="shop"]').count() == 1
    pg.click('#coach [data-cgo="shop"]'); pg.wait_for_timeout(400)
    assert pg.evaluate('S.view') == 'shop' and pg.locator('.wlock').count() == 0

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
    tabs_w = q.evaluate("document.querySelector('.tabs').scrollWidth <= document.querySelector('.tabs').clientWidth + 1"); assert tabs_w, 'six tabs fit on a phone'
    q.screenshot(path=out + 's_phone.png', full_page=True)
    b.close()

print('ERRORS:', errors); assert not errors
print('shop checks passed')
