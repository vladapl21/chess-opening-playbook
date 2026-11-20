"""Systems (packs): the library holds four answers to the e-pawn and two to the d-pawn for Black and three first moves for
White, and a player has one of each.

- With nothing chosen, the playbook is what it always was: no Caro-Kann and no London anywhere.
- Choosing the Caro-Kann in Settings swaps the chapters, the course units, the drills, the cards at a glance and the Sandbox.
- Progress in the other system is kept, and switching back brings everything back.
- A new player who already plays the Caro-Kann is offered it, and gets it.
- The same for White: the London swaps the White book, and the Sandbox opens with the d-pawn.
- The Scandinavian, the King's Indian (two chapters in place of the Slav's three) and the English switch the same way:
  chapters, units, a main line drilled clean, the plan at its end, the Sandbox's first move, and back again."""
from playwright.sync_api import sync_playwright
from e2e_white import click_move, drag, launch, out
from serve import Site
# over local HTTP: headless Chromium sometimes drops a file:// page's storage across a scripted reload
site = Site(); URL = site.start()
errors = []
E5 = ['italian', 'ruy', 'scotch', 'vienna', 'attacks']
WE4 = ['italian', 'e5x', 'caro', 'sic', 'scandi', 'pirc', 'french', 'rare']
WE4_UNITS = {'w-italian', 'w-sicilian', 'w-caro', 'w-2knights', 'w-philidor', 'w-defences', 'w-rare'}
LONDON_UNITS = {'w-london', 'w-lindian', 'w-lrare'}


def hook(pg):
    pg.on('pageerror', lambda e: errors.append(f'pageerror: {e}'))
    pg.on('console', lambda m: errors.append(f'console {m.type}: {m.text}') if m.type == 'error' and 'ERR_' not in m.text else None)


def shape(pg):
    return pg.evaluate("""({chapters: BOOKS.b.chapters.map(c => c.id), all: BOOKS.b.full.chapters.length, units: COURSE.map(U => U.id),
        lines: BOOKS.b.lines.length, drill: BOOKS.b.drillable.length, cheat: BOOKS.b.cheat.length, white: BOOKS.w.chapters.length,
        first: (() => { useSide('b'); const e4 = N[0].k.find(k => N[k].u === 'e2e4'); return sbMyKids(e4).map(c => N[c].u); })()})""")


def wshape(pg):
    return pg.evaluate("""(() => { useSide('w'); return {chapters: BOOKS.w.chapters.map(c => c.id), all: BOOKS.w.full.chapters.length,
        units: COURSE.map(U => U.id), lines: BOOKS.w.lines.length, cheat: BOOKS.w.cheat.length, black: BOOKS.b.chapters.length,
        first: N[BOOKS.w.e4].u, roots: N[0].k.filter(k => BOOKS.w.lines.some(l => l.n[1] === k)).map(k => N[k].u)}; })()""")


def switch(pg, ask, name='aqua_alpaca'):
    pg.click('#setBtn'); pg.wait_for_timeout(300)
    pg.click('#setPanel .repdet > summary'); pg.wait_for_timeout(200)
    pg.click(f'#setPanel [data-packask="{ask}"]'); pg.wait_for_timeout(200); pg.fill('#repName', name)
    pg.evaluate("window.__before = 1"); pg.click('.repask [type=submit]')
    pg.wait_for_function("typeof __before === 'undefined' && typeof COURSE !== 'undefined' && typeof PERSONA !== 'undefined'"); pg.wait_for_timeout(900)


def drill_clean(pg):
    for _ in range(120):
        st = pg.evaluate("({state: S.drill.state, busy: S.drill.busy})")
        if st['state'] == 'done': break
        if st['busy']: pg.wait_for_timeout(200); continue
        u = pg.evaluate("N[LINES[S.drill.id].n[S.drill.i + 1]].u")
        if u in ('e8g8', 'e8c8', 'e1g1', 'e1c1'): drag(pg, u[:2], u[0].replace('e', 'h' if u[2] == 'g' else 'a') + u[1])
        else: click_move(pg, u[:2], u[2:4])
        pg.wait_for_timeout(750)
    return pg.evaluate("S.drill.state")


with sync_playwright() as p:
    b = launch(p)
    ctx = b.new_context(viewport={'width': 1280, 'height': 900}); pg = ctx.new_page(); hook(pg)
    pg.goto(URL); pg.wait_for_timeout(1000)
    a = shape(pg); print('default:', {k: (v if k != 'units' else len(v)) for k, v in a.items()})
    assert 'caro' not in a['chapters'] and a['chapters'][:5] == E5 and a['all'] == len(a['chapters']) + 5
    assert 'b-caro' not in a['units'] and len(a['units']) == 17 and a['first'] == ['e7e5']
    assert pg.evaluate("Object.keys(LIDX.b).some(l => l.startsWith('bck-'))") is False

    # some progress in the first system, then switch
    pg.evaluate("useSide('b'); startDrillLine('bi-main')"); pg.wait_for_timeout(600); assert drill_clean(pg) == 'done'
    pg.click('#setBtn'); pg.wait_for_timeout(300)
    assert not pg.locator('#setPanel [data-packask="blackE4:caro"]').is_visible(), 'the repertoire is folded away'
    pg.click('#setPanel .repdet > summary'); pg.wait_for_timeout(200)
    rows = pg.locator('#setPanel [data-packask]').all_inner_texts(); print('settings:', rows); assert len(rows) == 9
    pg.click('#setPanel [data-packask="blackE4:caro"]'); pg.wait_for_timeout(200)
    assert pg.evaluate("PICKS.blackE4 || null") is None and pg.locator('#repName').count() == 1, 'a tap alone switches nothing'
    pg.fill('#repName', 'somebody'); assert pg.is_disabled('.repask [type=submit]')
    pg.screenshot(path=out + 'p_confirm.png')
    pg.fill('#repName', 'vladapl'); assert pg.is_disabled('.repask [type=submit]'), 'only the house account confirms'
    pg.fill('#repName', 'Aqua_Alpaca'); assert not pg.is_disabled('.repask [type=submit]')
    pg.evaluate("window.__before = 1"); pg.click('.repask [type=submit]')
    pg.wait_for_function("typeof __before === 'undefined' && typeof COURSE !== 'undefined' && typeof PERSONA !== 'undefined'"); pg.wait_for_timeout(900)
    print('after the switch:', pg.evaluate("[localStorage.getItem('playbook-packs'), JSON.stringify(Prog.d.packs), JSON.stringify(PICKS), PERSONA, performance.getEntriesByType('navigation')[0].type]"))
    c = shape(pg); print('caro:', {k: (v if k != 'units' else len(v)) for k, v in c.items()})
    assert c['chapters'][0] != 'italian' and 'caro' in c['chapters'] and not set(E5) & set(c['chapters']) and {'slav', 'london', 'd4x', 'other'} <= set(c['chapters'])
    assert 'b-caro' in c['units'] and not {'b-italian', 'b-scotch', 'b-ruy', 'b-vienna'} & set(c['units']) and 'b-slav' in c['units'] and 'w-italian' in c['units']
    assert c['first'] == ['c7c6'] and c['white'] == a['white']
    assert pg.evaluate("Prog.rec('bi-main').clean") == 1, 'progress in the other system is kept'
    assert pg.evaluate("[PICKS.blackE4, Prog.d.packs.blackE4]") == ['caro', 'caro']

    # the Caro-Kann is a full part of the book: chapter page, lesson with a plan, drill, cards at a glance, course unit, Sandbox
    pg.evaluate("useSide('b'); S.chapter = 'caro'; go('learn')"); pg.wait_for_timeout(500)
    txt = pg.inner_text('#view'); assert 'against the e-pawn' in txt and 'The Advance Variation' in txt and 'The Classical: take, then the bishop out' in txt
    pg.screenshot(path=out + 'p_chapter.png', full_page=True)
    pg.evaluate("openLine('bck-main')"); pg.wait_for_timeout(500); pg.keyboard.press('End'); pg.wait_for_timeout(500)
    assert 'Dark bishop, castle, then the c-pawn' in pg.inner_text('#view'); pg.screenshot(path=out + 'p_lesson.png')
    pg.evaluate("startDrillLine('bck-main-bd3')"); pg.wait_for_timeout(600); assert drill_clean(pg) == 'done'
    assert pg.evaluate("Prog.rec('bck-main-bd3').clean") == 1
    pg.evaluate("S.lview = 'glance'; S.chapter = 'caro'; go('learn')"); pg.wait_for_timeout(400); ch = pg.inner_text('#view')
    assert pg.locator('#view .ccard').count() == pg.evaluate("glanceCards(CHAPTERS.caro).length") > 0 and 'Mirror the bishop' not in ch
    glance = pg.evaluate("DATA.chapters.flatMap(C => glanceCards(C)).map(c => c.rule)"); assert 'Bishop out before the e-pawn' in glance and 'Mirror the bishop' not in glance
    pg.evaluate("S.lview = 'lessons'")
    pg.evaluate("go('course')"); pg.wait_for_timeout(400); pg.evaluate("S.unit = 'b-caro'; S.slide = 0; go('unit')"); pg.wait_for_timeout(500)
    assert 'Two pawn moves, every game' in pg.inner_text('#view'); pg.screenshot(path=out + 'p_unit.png')
    seen = set()
    pg.evaluate("useSide('b'); SBS.scope = 'caro'; SBS.odds = 'even'; go('sandbox')"); pg.wait_for_timeout(300)
    for k in range(4):
        pg.evaluate("sbStart()"); pg.wait_for_timeout(500)
        for _ in range(80):
            st = pg.evaluate("({state: S.drill.state, busy: S.drill.busy})")
            if st['state'] == 'done': break
            if st['busy']: pg.wait_for_timeout(250); continue
            u = pg.evaluate("(() => { const ks = sbMyKids(S.drill.node); return ks.length ? N[ks[0]].u : null; })()")
            if not u: break
            if u in ('e8g8', 'e8c8'): drag(pg, 'e8', 'h8' if u[2] == 'g' else 'a8')
            else: click_move(pg, u[:2], u[2:4])
            pg.wait_for_timeout(800)
        seen.add(pg.evaluate("chapterOf(lessonOf(S.drill.line || sbLinesThrough(S.drill.node)[0])).id"))
    print('sandbox games stayed in:', seen); assert seen == {'caro'}
    assert pg.evaluate('document.documentElement.scrollWidth') <= 1280

    # and back
    pg.evaluate("go('course')"); pg.click('#setBtn'); pg.wait_for_timeout(300)
    pg.click('#setPanel .repdet > summary'); pg.wait_for_timeout(200)
    assert pg.get_attribute('#setPanel [data-packask="blackE4:caro"]', 'aria-pressed') == 'true'
    pg.click('#setPanel [data-packask="blackE4:e5"]'); pg.wait_for_timeout(200); pg.fill('#repName', 'aqua_alpaca')
    pg.evaluate("window.__before = 1"); pg.click('.repask [type=submit]')
    pg.wait_for_function("typeof __before === 'undefined' && typeof COURSE !== 'undefined' && typeof PERSONA !== 'undefined'"); pg.wait_for_timeout(900)
    d = shape(pg); assert d['chapters'] == a['chapters'] and d['units'] == a['units'] and d['first'] == ['e7e5'] and d['lines'] == a['lines']
    assert pg.evaluate("[Prog.rec('bck-main-bd3').clean, Prog.rec('bi-main').clean]") == [1, 1]
    print('switched back: the same', len(d['chapters']), 'chapters and', len(d['units']), 'units')

    # a new player who already plays the Caro-Kann is offered it first, as ready
    cards = pg.evaluate("""makeChoices({slots: {blackE4: {n: 20, opts: {caro: {n: 15, w: 8, l: 6, d: 1}, e5: {n: 5, w: 2, l: 3, d: 0}}},
        blackD4: {n: 12, opts: {slav: {n: 12, w: 6, l: 5, d: 1}}}}}).map(c => [c.id, (c.opts || []).map(o => [o.id, !!o.ready])])""")
    print('cards for a Caro-Kann player:', cards[:2]); assert cards[0] == ['blackE4', [['caro', True], ['e5', True], ['sicilian', True], ['scandi', True]]], cards[0]
    assert cards[1] == ['blackD4', [['slav', True], ['kid', True]]] and cards[2][0] == 'order', 'the d-pawn has a second system now, so it gets a card'
    three = pg.evaluate("""makeChoices({slots: {blackE4: {n: 20, opts: {sicilian: {n: 16, w: 8, l: 7, d: 1}, e5: {n: 4, w: 2, l: 2, d: 0}}}}})[0].opts.map(o => o.id)""")
    assert three == ['sicilian', 'e5', 'caro', 'scandi'], three

    # the Sicilian is a pack too
    pg.evaluate("Prog.d.packs = {blackE4: 'sicilian', updated: Date.now()}; Prog.save(); window.__before = 1; syncPacks()")
    pg.wait_for_function("typeof __before === 'undefined' && typeof COURSE !== 'undefined' && typeof PERSONA !== 'undefined'"); pg.wait_for_timeout(900)
    s3 = shape(pg); print('sicilian:', s3['chapters'], s3['first'])
    assert 'sicilian' in s3['chapters'] and 'caro' not in s3['chapters'] and not set(E5) & set(s3['chapters']) and s3['first'] == ['c7c5'] and 'b-sicilian' in s3['units']
    pg.evaluate("useSide('b'); startDrillLine('bsi-open')"); pg.wait_for_timeout(600); assert drill_clean(pg) == 'done'
    pg.evaluate("openLine('bsi-open')"); pg.wait_for_timeout(400); pg.keyboard.press('End'); pg.wait_for_timeout(400); pg.screenshot(path=out + 'p_sicilian.png')
    pg.evaluate("Prog.d.packs = {blackE4: 'e5', updated: Date.now()}; Prog.save(); window.__before = 1; syncPacks()")
    pg.wait_for_function("typeof __before === 'undefined' && typeof COURSE !== 'undefined' && typeof PERSONA !== 'undefined'"); pg.wait_for_timeout(900)
    assert shape(pg)['chapters'] == a['chapters']

    # the London is a pack for White, beside the e-pawn
    w0 = wshape(pg); print('white default:', {k: (v if k != 'units' else len(v)) for k, v in w0.items()})
    assert w0['chapters'] == WE4 and w0['all'] == len(WE4) + 6 and w0['first'] == 'e2e4' and w0['roots'] == ['e2e4']
    assert not LONDON_UNITS & set(w0['units']) and WE4_UNITS <= set(w0['units'])
    assert pg.evaluate("Object.keys(LIDX.w).some(l => l.startsWith('ld-'))") is False
    pg.evaluate("useSide('w'); startDrillLine('setup')"); pg.wait_for_timeout(600); assert drill_clean(pg) == 'done'
    pg.evaluate("go('course')"); switch(pg, 'white:d4')
    w1 = wshape(pg); print('london:', {k: (v if k != 'units' else len(v)) for k, v in w1.items()})
    assert w1['chapters'] == ['london', 'lindian', 'lrare'] and w1['first'] == 'd2d4' and w1['roots'] == ['d2d4'] and w1['black'] == len(a['chapters'])
    assert LONDON_UNITS <= set(w1['units']) and not WE4_UNITS & set(w1['units']) and 'b-slav' in w1['units']
    assert pg.evaluate("[PICKS.white, Prog.d.packs.white, Prog.rec('setup').clean]") == ['d4', 'd4', 1]
    pg.evaluate("useSide('w'); S.chapter = 'london'; go('learn')"); pg.wait_for_timeout(500)
    txt = pg.inner_text('#view'); assert 'one order' in txt and 'The setup' in txt, txt[:400]
    pg.screenshot(path=out + 'p_london_chapter.png', full_page=True)
    pg.evaluate("openLine('ld-setup')"); pg.wait_for_timeout(500); pg.keyboard.press('End'); pg.wait_for_timeout(500)
    assert 'Castle, then the knight into the hole' in pg.inner_text('#view'); pg.screenshot(path=out + 'p_london_lesson.png')
    for lid in ('ld-setup', 'ld-trick', 'lr-englund'):
        pg.evaluate(f"useSide('w'); startDrillLine('{lid}')"); pg.wait_for_timeout(600); assert drill_clean(pg) == 'done', lid
    assert pg.evaluate("Prog.rec('ld-trick').clean") == 1
    assert pg.evaluate("DRILLSET.has('lr-englund-trap')") is False, 'the line that shows the trap is never drilled'
    glance = pg.evaluate("DATA.chapters.flatMap(C => glanceCards(C)).map(c => c.rule)")
    assert 'Bishop out before the e-pawn' in glance and 'Get the bishop out first' not in glance, glance[:6]
    pg.evaluate("go('course')"); pg.wait_for_timeout(400); pg.evaluate("S.unit = 'w-london'; S.slide = 0; go('unit')"); pg.wait_for_timeout(500)
    assert 'Bishop out first' in pg.inner_text('#view'); pg.screenshot(path=out + 'p_london_unit.png')
    seen = set()
    pg.evaluate("useSide('w'); SBS.scope = 'london'; SBS.odds = 'even'; go('sandbox')"); pg.wait_for_timeout(300)
    for k in range(3):
        pg.evaluate("sbStart()"); pg.wait_for_timeout(900)
        assert pg.evaluate("N[S.drill.hist[1]].u") == 'd2d4', 'the Sandbox opens with the d-pawn'
        for _ in range(80):
            st = pg.evaluate("({state: S.drill.state, busy: S.drill.busy})")
            if st['state'] == 'done': break
            if st['busy']: pg.wait_for_timeout(250); continue
            u = pg.evaluate("(() => { const ks = sbMyKids(S.drill.node); return ks.length ? N[ks[0]].u : null; })()")
            if not u: break
            if u in ('e1g1', 'e1c1'): drag(pg, 'e1', 'h1' if u[2] == 'g' else 'a1')
            else: click_move(pg, u[:2], u[2:4])
            pg.wait_for_timeout(800)
        seen.add(pg.evaluate("chapterOf(lessonOf(S.drill.line || sbLinesThrough(S.drill.node)[0])).id"))
    print('London sandbox games stayed in:', seen); assert seen <= {'london', 'lindian', 'lrare'} and seen
    assert pg.evaluate('document.documentElement.scrollWidth') <= 1280
    # the records as they stand before switching back (a London practice game can end on the same line and add to it)
    kept = pg.evaluate("[Prog.rec('setup').clean, Prog.rec('ld-trick').clean]"); assert kept[0] == 1 and kept[1] >= 1, kept
    pg.evaluate("go('course')"); switch(pg, 'white:e4')
    w2 = wshape(pg); assert w2['chapters'] == WE4 and w2['units'] == w0['units'] and w2['lines'] == w0['lines'] and w2['first'] == 'e2e4'
    assert pg.evaluate("[Prog.rec('setup').clean, Prog.rec('ld-trick').clean]") == kept, 'switching back keeps both systems\' records'
    print('White switched back: the same', len(w2['chapters']), 'chapters and', len(w2['units']), 'units')
    wc = pg.evaluate("""makeChoices({slots: {white: {n: 30, opts: {d4: {n: 24, w: 12, l: 10, d: 2}, e4: {n: 6, w: 3, l: 3, d: 0}}}}}).map(c => [c.id, (c.opts || []).map(o => [o.id, !!o.ready])])""")
    print('cards for a d-pawn player:', wc[:1]); assert wc[0] == ['white', [['d4', True], ['e4', True], ['flank', True]]], wc[0]

    # the three newer systems: each swaps its chapters and units, its main line drills clean and ends with a plan, and it switches back
    base_b, base_w = shape(pg), wshape(pg)
    pg.evaluate("go('course')"); switch(pg, 'blackE4:scandi')
    n1 = shape(pg); print('scandinavian:', n1['chapters'], n1['first'])
    assert n1['chapters'][0] == 'scandi' and not set(E5) & set(n1['chapters']) and n1['first'] == ['d7d5'] and 'b-scandi' in n1['units'] and {'slav', 'other'} <= set(n1['chapters'])
    pg.evaluate("useSide('b'); startDrillLine('bsc-main')"); pg.wait_for_timeout(600); assert drill_clean(pg) == 'done'
    assert pg.evaluate("!!planOf('bsc-main')") and pg.evaluate("planOf('bsc-main').h") in pg.inner_text('#view'), 'a clean drill ends with the plan'
    pg.evaluate("go('course')"); switch(pg, 'blackD4:kid')
    n2 = shape(pg); print('king\'s indian:', n2['chapters'])
    assert {'kid', 'kidx', 'scandi', 'other'} <= set(n2['chapters']) and not {'slav', 'london', 'd4x'} & set(n2['chapters']) and {'b-kid', 'b-kidx'} <= set(n2['units']) and 'b-slav' not in n2['units']
    assert pg.evaluate("(() => { useSide('b'); const d4 = N[0].k.find(k => N[k].u === 'd2d4'); return sbMyKids(d4).map(c => N[c].u); })()") == ['g8f6']
    for lid in ('bki-main', 'bkx-london'):
        pg.evaluate(f"useSide('b'); startDrillLine('{lid}')"); pg.wait_for_timeout(600); assert drill_clean(pg) == 'done', lid
    pg.evaluate("useSide('b'); S.chapter = 'kid'; go('learn')"); pg.wait_for_timeout(500)
    txt = pg.inner_text('#view'); assert 'then strike' in txt and 'The Four Pawns Attack' in txt and 'The Classical: castle, then the e-pawn' in txt; pg.screenshot(path=out + 'p_kid.png')
    pg.evaluate("go('course')"); switch(pg, 'white:flank')
    n3 = wshape(pg); print('english:', n3['chapters'], n3['first'])
    assert n3['chapters'] == ['english', 'engsym', 'engrare'] and n3['first'] == 'c2c4' and n3['roots'] == ['c2c4'] and {'w-english', 'w-engsym', 'w-engrare'} <= set(n3['units']) and not WE4_UNITS & set(n3['units'])
    pg.evaluate("useSide('w'); startDrillLine('en-main')"); pg.wait_for_timeout(600); assert drill_clean(pg) == 'done'
    pg.evaluate("useSide('w'); S.chapter = 'english'; go('learn')"); pg.wait_for_timeout(500)
    txt = pg.inner_text('#view'); assert 'one square' in txt and 'Black opens the middle' in txt; pg.screenshot(path=out + 'p_english.png')
    pg.evaluate("useSide('w'); SBS.scope = 'all'; SBS.odds = 'even'; go('sandbox')"); pg.wait_for_timeout(300); pg.evaluate("sbStart()"); pg.wait_for_timeout(1200)
    assert pg.evaluate("N[S.drill.hist[1]].u") == 'c2c4', 'the Sandbox opens with the c-pawn'
    assert pg.evaluate('document.documentElement.scrollWidth') <= 1280
    for ask in ('white:e4', 'blackD4:slav', 'blackE4:e5'):
        pg.evaluate("go('course')"); switch(pg, ask)
    e_b, e_w = shape(pg), wshape(pg)
    assert e_b['chapters'] == base_b['chapters'] and e_b['units'] == base_b['units'] and e_b['lines'] == base_b['lines'] and e_w['chapters'] == base_w['chapters'] and e_w['lines'] == base_w['lines']
    assert pg.evaluate("['bsc-main', 'bki-main', 'bkx-london', 'en-main'].map(l => Prog.rec(l).clean)") == [1, 1, 1, 1], 'records in the other systems are kept'
    print('the Scandinavian, the King\'s Indian and the English switch in and out')

    # phone width with the Caro-Kann on
    ph = b.new_context(viewport={'width': 390, 'height': 844}); ph.add_init_script("localStorage.setItem('playbook-packs', JSON.stringify({blackE4: 'caro'}))")
    q = ph.new_page(); hook(q); q.goto(URL); q.wait_for_function("typeof Prog !== 'undefined' && typeof COURSE !== 'undefined'"); q.wait_for_timeout(900)
    q.evaluate("Prog.d.packs = {blackE4: 'caro', updated: Date.now()}; Prog.save(); useSide('b'); S.chapter = 'caro'; go('learn')"); q.wait_for_timeout(500)
    w = q.evaluate('document.documentElement.scrollWidth'); print('phone scrollWidth', w); assert w <= 390
    # and with the London on
    ph2 = b.new_context(viewport={'width': 390, 'height': 844}); ph2.add_init_script("localStorage.setItem('playbook-packs', JSON.stringify({white: 'd4'}))")
    q2 = ph2.new_page(); hook(q2); q2.goto(URL); q2.wait_for_function("typeof Prog !== 'undefined' && typeof COURSE !== 'undefined'"); q2.wait_for_timeout(900)
    q2.evaluate("Prog.d.packs = {white: 'd4', updated: Date.now()}; Prog.save(); useSide('w'); S.chapter = 'london'; go('learn')"); q2.wait_for_timeout(500)
    for view in ("go('learn')", "openLine('lr-englund')", "S.unit = 'w-london'; S.slide = 0; go('unit')"):
        q2.evaluate(view); q2.wait_for_timeout(500)
        w = q2.evaluate('document.documentElement.scrollWidth'); assert w <= 390, (view, w)
    q2.screenshot(path=out + 'p_london_phone.png', full_page=True)
    b.close()
site.stop()

print('ERRORS:', errors); assert not errors
print('pack checks passed')
