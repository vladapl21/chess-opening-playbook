"""Systems (packs): the library holds two answers to the e-pawn for Black, and a player has one of them.

- With nothing chosen, the playbook is what it always was: no Caro-Kann anywhere.
- Choosing the Caro-Kann in Settings swaps the chapters, the course units, the drills, the cheat sheet and the Sandbox.
- Progress in the other system is kept, and switching back brings everything back.
- A new player who already plays the Caro-Kann is offered it, and gets it."""
from playwright.sync_api import sync_playwright
from e2e_white import click_move, drag, launch, out
from serve import Site
# over local HTTP: headless Chromium sometimes drops a file:// page's storage across a scripted reload
site = Site(); URL = site.start()
errors = []
E5 = ['italian', 'ruy', 'scotch', 'vienna', 'attacks']


def hook(pg):
    pg.on('pageerror', lambda e: errors.append(f'pageerror: {e}'))
    pg.on('console', lambda m: errors.append(f'console {m.type}: {m.text}') if m.type == 'error' and 'ERR_' not in m.text else None)


def shape(pg):
    return pg.evaluate("""({chapters: BOOKS.b.chapters.map(c => c.id), all: BOOKS.b.full.chapters.length, units: COURSE.map(U => U.id),
        lines: BOOKS.b.lines.length, drill: BOOKS.b.drillable.length, cheat: BOOKS.b.cheat.length, white: BOOKS.w.chapters.length,
        first: (() => { useSide('b'); const e4 = N[0].k.find(k => N[k].u === 'e2e4'); return sbMyKids(e4).map(c => N[c].u); })()})""")


def drill_clean(pg):
    for _ in range(120):
        st = pg.evaluate("({state: S.drill.state, busy: S.drill.busy})")
        if st['state'] == 'done': break
        if st['busy']: pg.wait_for_timeout(200); continue
        u = pg.evaluate("N[LINES[S.drill.id].n[S.drill.i + 1]].u")
        if u in ('e8g8', 'e8c8'): drag(pg, 'e8', 'h8' if u[2] == 'g' else 'a8')
        else: click_move(pg, u[:2], u[2:4])
        pg.wait_for_timeout(750)
    return pg.evaluate("S.drill.state")


with sync_playwright() as p:
    b = launch(p)
    ctx = b.new_context(viewport={'width': 1280, 'height': 900}); pg = ctx.new_page(); hook(pg)
    pg.goto(URL); pg.wait_for_timeout(1000)
    a = shape(pg); print('default:', {k: (v if k != 'units' else len(v)) for k, v in a.items()})
    assert 'caro' not in a['chapters'] and a['chapters'][:5] == E5 and a['all'] == len(a['chapters']) + 2
    assert 'b-caro' not in a['units'] and len(a['units']) == 17 and a['first'] == ['e7e5']
    assert pg.evaluate("Object.keys(LIDX.b).some(l => l.startsWith('bck-'))") is False

    # some progress in the first system, then switch
    pg.evaluate("useSide('b'); startDrillLine('bi-main')"); pg.wait_for_timeout(600); assert drill_clean(pg) == 'done'
    pg.click('#setBtn'); pg.wait_for_timeout(300)
    rows = pg.locator('#setPanel [data-pack]').all_inner_texts(); print('settings:', rows); assert len(rows) == 3
    pg.evaluate("window.__before = 1"); pg.click('#setPanel [data-pack="blackE4:caro"]')
    pg.wait_for_function("typeof __before === 'undefined' && typeof COURSE !== 'undefined' && typeof PERSONA !== 'undefined'"); pg.wait_for_timeout(900)
    print('after the switch:', pg.evaluate("[localStorage.getItem('playbook-packs'), JSON.stringify(Prog.d.packs), JSON.stringify(PICKS), PERSONA, performance.getEntriesByType('navigation')[0].type]"))
    c = shape(pg); print('caro:', {k: (v if k != 'units' else len(v)) for k, v in c.items()})
    assert c['chapters'][0] != 'italian' and 'caro' in c['chapters'] and not set(E5) & set(c['chapters']) and {'slav', 'london', 'd4x', 'other'} <= set(c['chapters'])
    assert 'b-caro' in c['units'] and not {'b-italian', 'b-scotch', 'b-ruy', 'b-vienna'} & set(c['units']) and 'b-slav' in c['units'] and 'w-italian' in c['units']
    assert c['first'] == ['c7c6'] and c['white'] == a['white']
    assert pg.evaluate("Prog.rec('bi-main').clean") == 1, 'progress in the other system is kept'
    assert pg.evaluate("[PICKS.blackE4, Prog.d.packs.blackE4]") == ['caro', 'caro']

    # the Caro-Kann is a full part of the book: chapter page, lesson with a plan, drill, cheat sheet, course unit, Sandbox
    pg.evaluate("useSide('b'); S.chapter = 'caro'; go('learn')"); pg.wait_for_timeout(500)
    txt = pg.inner_text('#view'); assert 'against the e-pawn' in txt and 'The e-pawn pushes past' in txt and 'Take, then the bishop out' in txt
    pg.screenshot(path=out + 'p_chapter.png', full_page=True)
    pg.evaluate("openLine('bck-main')"); pg.wait_for_timeout(500); pg.keyboard.press('End'); pg.wait_for_timeout(500)
    assert 'Dark bishop, castle, then the c-pawn' in pg.inner_text('#view'); pg.screenshot(path=out + 'p_lesson.png')
    pg.evaluate("startDrillLine('bck-main-bd3')"); pg.wait_for_timeout(600); assert drill_clean(pg) == 'done'
    assert pg.evaluate("Prog.rec('bck-main-bd3').clean") == 1
    pg.evaluate("go('cheat')"); pg.wait_for_timeout(400); ch = pg.inner_text('#view'); assert 'Bishop out before the e-pawn' in ch and 'Mirror the bishop' not in ch
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
    assert pg.get_attribute('#setPanel [data-pack="blackE4:caro"]', 'aria-pressed') == 'true'
    pg.evaluate("window.__before = 1"); pg.click('#setPanel [data-pack="blackE4:e5"]')
    pg.wait_for_function("typeof __before === 'undefined' && typeof COURSE !== 'undefined' && typeof PERSONA !== 'undefined'"); pg.wait_for_timeout(900)
    d = shape(pg); assert d['chapters'] == a['chapters'] and d['units'] == a['units'] and d['first'] == ['e7e5'] and d['lines'] == a['lines']
    assert pg.evaluate("[Prog.rec('bck-main-bd3').clean, Prog.rec('bi-main').clean]") == [1, 1]
    print('switched back: the same', len(d['chapters']), 'chapters and', len(d['units']), 'units')

    # a new player who already plays the Caro-Kann is offered it first, as ready
    cards = pg.evaluate("""makeChoices({slots: {blackE4: {n: 20, opts: {caro: {n: 15, w: 8, l: 6, d: 1}, e5: {n: 5, w: 2, l: 3, d: 0}}},
        blackD4: {n: 12, opts: {slav: {n: 12, w: 6, l: 5, d: 1}}}}}).map(c => [c.id, (c.opts || []).map(o => [o.id, !!o.ready])])""")
    print('cards for a Caro-Kann player:', cards[:2]); assert cards[0] == ['blackE4', [['caro', True], ['e5', True], ['sicilian', True]]] and cards[1][0] == 'order'
    three = pg.evaluate("""makeChoices({slots: {blackE4: {n: 20, opts: {sicilian: {n: 16, w: 8, l: 7, d: 1}, e5: {n: 4, w: 2, l: 2, d: 0}}}}})[0].opts.map(o => o.id)""")
    assert three == ['sicilian', 'e5', 'caro'], three

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

    # phone width with the Caro-Kann on
    ph = b.new_context(viewport={'width': 390, 'height': 844}); ph.add_init_script("localStorage.setItem('playbook-packs', JSON.stringify({blackE4: 'caro'}))")
    q = ph.new_page(); hook(q); q.goto(URL); q.wait_for_timeout(900)
    q.evaluate("Prog.d.packs = {blackE4: 'caro', updated: Date.now()}; Prog.save(); useSide('b'); S.chapter = 'caro'; go('learn')"); q.wait_for_timeout(500)
    w = q.evaluate('document.documentElement.scrollWidth'); print('phone scrollWidth', w); assert w <= 390
    b.close()
site.stop()

print('ERRORS:', errors); assert not errors
print('pack checks passed')
