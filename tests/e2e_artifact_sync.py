"""The claude.ai copy on two devices: the page keeps its progress in the artifact's database (window.claude.use('db')).
A stand-in for that database is shared by two browser contexts, so this is two devices on one claude.ai account.
Everything a player sets or earns must arrive on the other device: the coach, the look, the streak, badges, lines,
worn coach items, the level; and a page that writes an older, smaller copy must not wipe what the other device added."""
import json, tempfile
from pathlib import Path
from playwright.sync_api import sync_playwright
from e2e_white import out

ROOT = Path(__file__).resolve().parents[1]
BODY = (ROOT / 'data' / 'build' / 'playbook.html').read_text()
# the skeleton claude.ai wraps the page in, with its small reset (hidden means hidden)
HEAD = ('<!doctype html><html><head><meta charset=utf8><meta name=viewport content="width=device-width,initial-scale=1,viewport-fit=cover"><style>:root{color-scheme:light;box-sizing:border-box;'
        'padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}html{scroll-padding-top:env(safe-area-inset-top,0px)}body{margin:0;padding:0;'
        'font:14px -apple-system,BlinkMacSystemFont,sans-serif;background:#fff;color:#000}img{max-width:100%}[hidden]:not([hidden=until-found i]){display:none!important}</style></head><body>\n')
page_file = Path(tempfile.mkdtemp()) / 'index.html'
page_file.write_text(HEAD + BODY + '\n</body></html>')
URL = page_file.as_uri()

DB = {}          # path -> JSON text: the artifact's database, shared by both devices
writes = []
# the platform's snapshots are frozen: the page must copy what it keeps
FAKE = """
(() => {
  const freeze = o => { if (o && typeof o === 'object'){ Object.freeze(o); for (const k in o) freeze(o[k]); } return o; };
  const snap = v => ({exists: v !== null, data: () => v === null ? undefined : freeze(JSON.parse(v))});
  window.claude = {use: async name => {
    if (name === 'user') return {id: async () => window.__viewer, isOwner: async () => window.__owner};
    if (name !== 'db') return null;
    return {doc: path => ({
      get: async () => snap(await window.__dbGet(path)),
      set: async data => { await window.__dbSet(path, JSON.stringify(data)); },
      onSnapshot: (next) => { let last; const tick = async () => { const v = await window.__dbGet(path); if (v !== last){ last = v; next(snap(v)); } };
        tick(); const h = setInterval(tick, 300); return () => clearInterval(h); }
    })};
  }};
})();
"""
errors = []


def device(b, name, viewer='viewer-1', owner=True):
    """A browser on the claude.ai copy: the artifact's owner by default, or someone it was shared with."""
    ctx = b.new_context(viewport={'width': 1280, 'height': 860})
    ctx.add_init_script(f"window.__viewer = {json.dumps(viewer)}; window.__owner = {'true' if owner else 'false'};")
    ctx.expose_binding('__dbGet', lambda src, path: DB.get(path))
    ctx.expose_binding('__dbSet', lambda src, path, text: (DB.__setitem__(path, text), writes.append((name, path))))
    ctx.add_init_script(FAKE)
    pg = ctx.new_page()
    pg.on('pageerror', lambda e: errors.append(f'{name} pageerror: {e}'))
    pg.on('console', lambda m: errors.append(f'{name} console: {m.text}') if m.type == 'error' and 'ERR_' not in m.text else None)
    pg.goto(URL); pg.wait_for_timeout(900)
    return pg


def finish_line(pg, lid):
    pg.evaluate(f"useSide('w'); startDrillLine('{lid}', '', null, {{from0: true}})"); pg.wait_for_timeout(300)
    for _ in range(80):
        st = pg.evaluate('({s: S.drill.state, busy: S.drill.busy})')
        if st['s'] == 'done': return
        if st['busy']: pg.wait_for_timeout(120); continue
        u = pg.evaluate('N[LINES[S.drill.id].n[S.drill.i + 1]].u'); pg.evaluate(f"tryMove('{u[:2]}', '{u[2:4]}')"); pg.wait_for_timeout(650)
    raise AssertionError('line did not finish')


def stored():
    return json.loads(DB['data/users/viewer-1/italian-progress'])


with sync_playwright() as p:
    b = p.chromium.launch()
    a = device(b, 'A')
    assert a.evaluate('PERSONA') == 'house' and a.evaluate('!!Prog.ref'), 'the claude.ai copy talks to its database'

    # ---- device A: a coach, a board colour, one line played to its end
    a.evaluate("setSetting('who', 'rook'); setSetting('board', 'wood')")
    finish_line(a, 'setup'); a.wait_for_timeout(600)
    d = stored(); print('stored after A:', {k: d.get(k) for k in ('prefs',)}, '| days', d.get('days'))
    assert d['prefs']['who'][0] == 'rook' and d['prefs']['board'][0] == 'wood' and d['lines']['setup']['seen'] == 1 and list(d['days'].values()) == [['setup']]

    # ---- device B opens: everything is there
    bp = device(b, 'B'); bp.wait_for_timeout(500)
    got = bp.evaluate("[SET.who, SET.board, document.documentElement.dataset.board, coachName(), Daily.count(), (Prog.rec('setup') || {}).seen]")
    print('device B on opening:', got); assert got == ['rook', 'wood', 'wood', 'Rocco', 1, 1], got

    # ---- B, already open, keeps hearing A; a change on each side never undoes the other
    bp.evaluate("setSetting('theme', 'dark')"); bp.wait_for_timeout(900)
    assert a.evaluate("[SET.theme, SET.who]") == ['dark', 'rook'], a.evaluate("[SET.theme, SET.who, JSON.stringify(Prog.d.prefs)]")
    a.evaluate("setSetting('who', 'pawn')"); bp.evaluate("setSetting('board', 'plum')"); a.wait_for_timeout(1200)
    a.evaluate("Prog.save()"); bp.evaluate("Prog.save()"); a.wait_for_timeout(1200)
    for pg in (a, bp):
        assert pg.evaluate("[SET.who, SET.board, SET.theme]") == ['pawn', 'plum', 'dark'], pg.evaluate("[SET.who, SET.board, SET.theme]")
    print('both devices: coach Dot, plum board, dark theme')

    # ---- B's lines and badges reach A; a frozen snapshot is copied, so B's own records still update
    finish_line(bp, 'center'); bp.wait_for_timeout(900)
    assert bp.evaluate("Prog.rec('center').seen") == 1 and a.evaluate("Daily.count()") == 2 and a.evaluate("(Prog.rec('center') || {}).seen") == 1
    finish_line(bp, 'setup'); bp.wait_for_timeout(900)
    assert bp.evaluate("Prog.rec('setup').seen") == 2 and a.evaluate("Prog.rec('setup').seen") == 2, 'records merged in from the database stay writable'
    assert stored()['badges'].get('l1'), 'badges are stored'
    a.evaluate("Prog.d.shop = {own: {}, wear: {head: ['crown', Date.now()]}}; Prog.save()"); a.wait_for_timeout(1200)
    assert bp.evaluate("Prog.d.shop && Prog.d.shop.wear.head[0]") == 'crown'
    # ---- finishing the course is stamped once (the earliest stamp wins); deep dive parts travel like any unit
    bp.evaluate("const c = Prog.d.course || (Prog.d.course = {u: {}, seen: {}}); c.u = c.u || {}; c.grad = 1700000000000; c.u['x-w-italian-1'] = {o: Date.now(), cp: 4}; Prog.save()"); bp.wait_for_timeout(1200)
    assert a.evaluate("[Prog.d.course.grad, Prog.d.course.u['x-w-italian-1'].cp]") == [1700000000000, 4]
    a.evaluate("Prog.d.course.grad = 1800000000000; Prog.save()"); a.wait_for_timeout(1200)
    assert stored()['course']['grad'] == 1700000000000 and a.evaluate("Prog.d.course.grad") == 1700000000000 and bp.evaluate("Prog.d.course.grad") == 1700000000000
    # ---- the level last celebrated: the highest wins
    bp.evaluate("Prog.d.lvl = 9; Prog.save()"); bp.wait_for_timeout(1200)
    assert a.evaluate('Prog.d.lvl') == 9
    a.evaluate("Prog.d.lvl = 2; Prog.save()"); a.wait_for_timeout(1200)
    assert stored()['lvl'] == 9 and a.evaluate('Prog.d.lvl') == 9
    # ---- monthly recaps (made on the website, kept with the progress): each month's newest summary wins
    bp.evaluate("Prog.d.recap = {m: {'2026-10': {a: 'chess.com:aqua_alpaca', at: 5, fin: true, all: [40, 24, 15, 1]}}, chk: 5, seen: '2026-09'}; Prog.save()"); bp.wait_for_timeout(1200)
    assert a.evaluate("[Prog.d.recap.m['2026-10'].all[0], Prog.d.recap.seen]") == [40, '2026-09']
    a.evaluate("Prog.d.recap.m['2026-10'] = {a: 'chess.com:aqua_alpaca', at: 2, fin: true, all: [1, 0, 1, 0]}; Prog.d.recap.seen = '2026-10'; Prog.save()"); a.wait_for_timeout(1200)
    assert stored()['recap']['m']['2026-10']['all'][0] == 40 and stored()['recap']['seen'] == '2026-10' and bp.evaluate("Prog.d.recap.seen") == '2026-10'

    # ---- the artifact's owner has a switch nobody else has: it works on a copy that is never written to the database,
    # while what other devices write keeps arriving underneath and is there when the switch goes off
    a.wait_for_function('Owner.can === true', timeout=5000)
    n0 = len([w for w in writes if w[0] == 'A']); before = DB['data/users/viewer-1/italian-progress']
    a.click('h1'); a.keyboard.type('admin'); a.wait_for_timeout(300)
    assert a.evaluate('Owner.on') and a.locator('#opill').is_visible()
    a.evaluate("OwnerUI.act('badges'); OwnerUI.act('course'); Prog.record('grab', true)"); a.wait_for_timeout(1200)
    assert len([w for w in writes if w[0] == 'A']) == n0 and DB['data/users/viewer-1/italian-progress'] == before, 'admin mode writes nothing'
    assert not bp.evaluate("Prog.rec('grab')") and bp.evaluate("Object.keys(Prog.d.badges).length") < a.evaluate("Object.keys(Prog.d.badges).length")
    bp.evaluate("Prog.record('moller-bf6', true)"); bp.wait_for_timeout(1200)
    assert not a.evaluate("Prog.rec('moller-bf6')"), 'the copy is not touched by the other device'
    a.click('h1'); a.keyboard.type('admin'); a.wait_for_timeout(600)
    assert not a.evaluate('Owner.on') and a.evaluate("(Prog.rec('moller-bf6') || {}).seen") == 1 and not a.evaluate("Prog.rec('grab')") and a.locator('#opill').count() == 0
    # someone the copy was shared with: no switch, no sign of one
    c = device(b, 'C', viewer='viewer-2', owner=False); c.wait_for_timeout(600)
    c.click('h1'); c.keyboard.type('admin'); c.wait_for_timeout(300); c.click('#setBtn'); c.wait_for_timeout(200)
    assert not c.evaluate('Owner.can || Owner.on') and c.locator('[data-own], #opill').count() == 0 and 'admin' not in c.inner_text('body').lower()
    c.context.close()

    # ---- a page from an older version writes a smaller copy: the next save on either device puts everything back
    d = stored(); old = {k: v for k, v in d.items() if k not in ('days', 'prefs', 'set', 'badges', 'shop', 'lvl', 'recap')}; old['someday'] = {'x': 1}
    DB['data/users/viewer-1/italian-progress'] = json.dumps(old); a.wait_for_timeout(700)
    a.evaluate("Prog.save()"); a.wait_for_timeout(900)
    d = stored(); print('after a smaller copy and one save:', sorted(d.keys()))
    assert all(k in d for k in ('days', 'prefs', 'badges', 'shop', 'lvl', 'recap', 'someday')) and d['prefs']['who'][0] == 'pawn'
    assert a.evaluate("Prog.d.someday && Prog.d.someday.x") == 1, 'a field this version does not know is kept'

    # ---- the explore screen is not disturbed by another device: no re-render while a line is being played
    a.evaluate("useSide('w'); startDrillLine('grab', '', null, {from0: true})"); a.wait_for_timeout(300)
    i0 = a.evaluate('S.drill.i'); bp.evaluate("setSetting('size', 'l')"); a.wait_for_timeout(900)
    assert a.evaluate('S.drill.state') == 'play' and a.evaluate('S.drill.i') == i0 and a.evaluate('SET.size') == 'l'
    a.screenshot(path=out + 'sync_artifact.png')
    b.close()

print('ERRORS:', errors); assert not errors
print('writes:', len(writes))
print('artifact sync checks passed')
