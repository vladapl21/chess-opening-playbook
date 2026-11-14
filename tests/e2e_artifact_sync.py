"""The claude.ai copy on two devices: the page keeps its progress in the artifact's database (window.claude.use('db')).
A stand-in for that database is shared by two browser contexts, so this is two devices on one claude.ai account.
Everything a player sets or earns must arrive on the other device: the coach, the look, the streak, badges, lines,
worn coach items; and a page that writes an older, smaller copy must not wipe what the other device added."""
import json, tempfile
from pathlib import Path
from playwright.sync_api import sync_playwright
from e2e_white import out

ROOT = Path(__file__).resolve().parents[1]
BODY = (ROOT / 'data' / 'build' / 'playbook.html').read_text()
HEAD = '<!doctype html><html><head><meta charset=utf8><meta name=viewport content="width=device-width,initial-scale=1"></head><body>\n'
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
    if (name === 'user') return {id: async () => 'viewer-1', isOwner: () => true};
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


def device(b, name):
    ctx = b.new_context(viewport={'width': 1280, 'height': 860})
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

    # ---- a page from an older version writes a smaller copy: the next save on either device puts everything back
    d = stored(); old = {k: v for k, v in d.items() if k not in ('days', 'prefs', 'set', 'badges', 'shop')}; old['someday'] = {'x': 1}
    DB['data/users/viewer-1/italian-progress'] = json.dumps(old); a.wait_for_timeout(700)
    a.evaluate("Prog.save()"); a.wait_for_timeout(900)
    d = stored(); print('after a smaller copy and one save:', sorted(d.keys()))
    assert all(k in d for k in ('days', 'prefs', 'badges', 'shop', 'someday')) and d['prefs']['who'][0] == 'pawn'
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
