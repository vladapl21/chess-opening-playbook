"""Regenerate the README images in docs/img/ from docs/index.html.

    python3 tests/readme_shots.py

Needs Playwright and Pillow. The page loads its fonts from Google Fonts; on a machine without internet
access, point FONTS_DIR at the `ofl` folder of a google/fonts checkout (bodonimoda, instrumentsans and
jetbrainsmono are enough) and the fonts are served from disk instead.
"""
import io, os, sys
from pathlib import Path
from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright
sys.path.insert(0, str(Path(__file__).resolve().parent))
from e2e_white import ROOT, URL, launch  # noqa: E402
from serve import Site  # noqa: E402

IMG = ROOT / 'docs' / 'img'; IMG.mkdir(exist_ok=True)
FONTS_DIR = os.environ.get('FONTS_DIR')
FONT_FILES = {'Barlow-Regular.ttf': ('barlow', 'Barlow-Regular.ttf'), 'Barlow-Medium.ttf': ('barlow', 'Barlow-Medium.ttf'), 'Barlow-SemiBold.ttf': ('barlow', 'Barlow-SemiBold.ttf'), 'Barlow-Bold.ttf': ('barlow', 'Barlow-Bold.ttf'), 'Barlow-Italic.ttf': ('barlow', 'Barlow-Italic.ttf'), 'BarlowCondensed-Medium.ttf': ('barlowcondensed', 'BarlowCondensed-Medium.ttf'), 'BarlowCondensed-SemiBold.ttf': ('barlowcondensed', 'BarlowCondensed-SemiBold.ttf'), 'BarlowCondensed-Bold.ttf': ('barlowcondensed', 'BarlowCondensed-Bold.ttf'), 'BarlowCondensed-SemiBoldItalic.ttf': ('barlowcondensed', 'BarlowCondensed-SemiBoldItalic.ttf'), 'BarlowCondensed-BoldItalic.ttf': ('barlowcondensed', 'BarlowCondensed-BoldItalic.ttf'), 'jb.ttf': ('jetbrainsmono', 'JetBrainsMono[wght].ttf')}
FONT_CSS = '''@font-face{font-family:"Barlow";font-style:normal;font-weight:400;src:url(https://fonts.gstatic.com/local/Barlow-Regular.ttf) format("truetype")}
@font-face{font-family:"Barlow";font-style:normal;font-weight:500;src:url(https://fonts.gstatic.com/local/Barlow-Medium.ttf) format("truetype")}
@font-face{font-family:"Barlow";font-style:normal;font-weight:600;src:url(https://fonts.gstatic.com/local/Barlow-SemiBold.ttf) format("truetype")}
@font-face{font-family:"Barlow";font-style:normal;font-weight:700;src:url(https://fonts.gstatic.com/local/Barlow-Bold.ttf) format("truetype")}
@font-face{font-family:"Barlow";font-style:italic;font-weight:400;src:url(https://fonts.gstatic.com/local/Barlow-Italic.ttf) format("truetype")}
@font-face{font-family:"Barlow Condensed";font-style:normal;font-weight:500;src:url(https://fonts.gstatic.com/local/BarlowCondensed-Medium.ttf) format("truetype")}
@font-face{font-family:"Barlow Condensed";font-style:normal;font-weight:600;src:url(https://fonts.gstatic.com/local/BarlowCondensed-SemiBold.ttf) format("truetype")}
@font-face{font-family:"Barlow Condensed";font-style:normal;font-weight:700;src:url(https://fonts.gstatic.com/local/BarlowCondensed-Bold.ttf) format("truetype")}
@font-face{font-family:"Barlow Condensed";font-style:italic;font-weight:600;src:url(https://fonts.gstatic.com/local/BarlowCondensed-SemiBoldItalic.ttf) format("truetype")}
@font-face{font-family:"Barlow Condensed";font-style:italic;font-weight:700;src:url(https://fonts.gstatic.com/local/BarlowCondensed-BoldItalic.ttf) format("truetype")}
@font-face{font-family:"JetBrains Mono";font-style:normal;font-weight:100 800;src:url(https://fonts.gstatic.com/local/jb.ttf) format("truetype")}'''


def local_fonts(ctx):
    if not FONTS_DIR: return
    def font(route):
        folder, name = FONT_FILES[route.request.url.rsplit('/', 1)[1]]
        route.fulfill(status=200, content_type='font/ttf', body=(Path(FONTS_DIR) / folder / name).read_bytes())
    ctx.route('https://fonts.googleapis.com/**', lambda r: r.fulfill(status=200, content_type='text/css', body=FONT_CSS))
    ctx.route('https://fonts.gstatic.com/local/*', font)


def save(png, name, width=1600, crop=None):
    im = Image.open(io.BytesIO(png)).convert('RGB')
    if crop: im = im.crop(crop)
    if width and im.width > width: im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    im.save(IMG / name, optimize=True)
    print(f'{name:16s} {im.size[0]}x{im.size[1]}  {os.path.getsize(IMG / name) // 1024} KB')


def settle(pg, ms=300):
    pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(ms)
    pg.evaluate('document.activeElement && document.activeElement.blur()')
    vp = pg.viewport_size; pg.mouse.move(vp['width'] - 1, vp['height'] - 1); pg.wait_for_timeout(150)


def xy(pg, sq):
    box = pg.locator('#db svg').bounding_box(); f = 'abcdefgh'.index(sq[0]); r = int(sq[1]) - 1
    if pg.evaluate('FLIP'): f, r = 7 - f, 7 - r
    return box['x'] + (f + .5) * box['width'] / 8, box['y'] + (7 - r + .5) * box['height'] / 8


def tap(pg, uci):
    x, y = xy(pg, uci[:2]); pg.mouse.click(x, y); pg.wait_for_timeout(100)
    x, y = xy(pg, uci[2:4]); pg.mouse.click(x, y)


def months_of_games():
    """The house account's games (data/games) re-dated into this month and the two before, as chess.com serves them."""
    import re, random, datetime
    G = ['[Event ' + g for g in (ROOT / 'data/games/aqua_alpaca.pgn').read_text().split('[Event ')[1:]]
    t = datetime.datetime.now(datetime.timezone.utc); rnd = random.Random(4)
    ym = [((t.year * 12 + t.month - 1 - n) // 12, (t.year * 12 + t.month - 1 - n) % 12 + 1) for n in range(3)]
    def redate(g, y, m, d, elo):
        side = 'White' if '[White "aqua_alpaca"]' in g else 'Black'
        return re.sub(rf'\[{side}Elo "\d+"\]', f'[{side}Elo "{elo}"]', re.sub(r'\[Date "[^"]*"\]', f'[Date "{y}.{m:02d}.{d:02d}"]', g))
    days = max(1, t.day - 1)
    return {f'{ym[2][0]}/{ym[2][1]:02d}': [redate(g, *ym[2], 1 + i % 28, 900 + i * 2 + rnd.randint(-6, 6)) for i, g in enumerate(G[:30])],
            f'{ym[1][0]}/{ym[1][1]:02d}': [redate(g, *ym[1], 1 + i % 28, 935 + i * 2 + rnd.randint(-8, 8)) for i, g in enumerate(G[5:50])],
            f'{ym[0][0]}/{ym[0][1]:02d}': [redate(g, *ym[0], 1 + i % days, 1010 + i * 2 + rnd.randint(-5, 5)) for i, g in enumerate(G[10:40])]}


def chesscom(months):
    import json
    def route(r):
        k = '/'.join(r.request.url.split('/')[-2:])
        if '/player/aqua_alpaca/games/' in r.request.url and k in months:
            return r.fulfill(status=200, content_type='application/json', body=json.dumps({'games': [{'rules': 'chess', 'time_class': 'blitz', 'pgn': g} for g in months[k]]}))
        r.fulfill(status=404, content_type='application/json', body='{}')
    return route


def play_drill(pg, bad=None):
    """Play the drill line to its end; at index bad[0] play the move bad[1] once instead of the book's."""
    for _ in range(200):
        st = pg.evaluate('({state: S.drill.state, busy: S.drill.busy, i: S.drill.i})')
        if st['state'] == 'done': return
        if st['busy']: pg.wait_for_timeout(120); continue
        u = pg.evaluate('N[LINES[S.drill.id].n[S.drill.i + 1]].u')
        if bad and st['i'] + 1 == bad[0]: u, bad = bad[1], None
        pg.evaluate(f"tryMove('{u[:2]}', '{u[2:4]}')"); pg.wait_for_timeout(650)


def idle(pg):
    for _ in range(40):
        if not pg.evaluate('S.drill && S.drill.busy'): return
        pg.wait_for_timeout(200)


with sync_playwright() as p:
    b = launch(p)
    ctx = b.new_context(viewport={'width': 1280, 'height': 860}, device_scale_factor=2); local_fonts(ctx); ctx.route('https://api.chess.com/**', chesscom(months_of_games()))
    pg = ctx.new_page(); errors = []; pg.on('pageerror', lambda e: errors.append(str(e)))

    # Course: unit 1 passed, unit 2 under way
    pg.goto(URL + '#course'); pg.wait_for_timeout(900)
    pg.evaluate("""(() => { const now = Date.now(), W = UNIT['w-italian'], B = UNIT['b-slav'];
      Prog.d.course = {u: {'w-italian': {idea: now, pass: now, cp: 6, spar: 3, sparGames: 4}, 'b-slav': {idea: now, spar: 1, sparGames: 1}}, seen: {}};
      W.lessons.concat(B.lessons.slice(0, 2)).forEach(l => Prog.d.course.seen[l] = now);
      W.lines.forEach(id => Prog.d.lines[id] = {box: 2, seen: 2, clean: 2, last: now, due: now + 2 * DAY});
      render(); })()"""); pg.wait_for_timeout(400); settle(pg)
    save(pg.screenshot(), 'course.png')
    # Play along: the Italian unit's first lesson two moves in, the arrow on the next move and the coach's word on it
    pg.evaluate("useSide('w'); startGuided(LIDX.w[UNIT['w-italian'].lessons[0]].lines[0], 'w-italian')"); pg.wait_for_timeout(900)
    for _ in range(2):
        idle(pg); tap(pg, pg.evaluate('N[LINES[S.drill.id].n[S.drill.i + 1]].u')); pg.wait_for_timeout(1600)
    idle(pg); pg.wait_for_timeout(300); pg.evaluate("Coach.hush(); window.scrollTo(0, 0)"); settle(pg)
    save(pg.screenshot(), 'play.png'); pg.evaluate("S.drill = S.drillState = null")
    pg.evaluate("localStorage.clear()"); pg.goto(URL + '#learn'); pg.reload(); pg.wait_for_timeout(900); settle(pg)
    save(pg.screenshot(), 'learn-white.png')
    pg.click('.sidesw [data-side="b"]'); pg.wait_for_timeout(700); pg.evaluate("go('learn')"); pg.wait_for_timeout(500); settle(pg)
    save(pg.screenshot(), 'learn-black.png')

    # Study: the Scotch lesson, a few moves in
    pg.evaluate("openLine('bs-classical')"); pg.wait_for_timeout(400)
    for _ in range(9): pg.keyboard.press('ArrowRight'); pg.wait_for_timeout(120)
    settle(pg, 500); save(pg.screenshot(), 'study.png')

    # Drill: three moves into the Berlin, next piece picked up
    pg.evaluate("startDrillLine('br-oo')"); pg.wait_for_timeout(1800)
    for _ in range(3):
        idle(pg); tap(pg, pg.evaluate('N[LINES[S.drill.id].n[S.drill.i + 1]].u')); pg.wait_for_timeout(1300)
    idle(pg); u = pg.evaluate('N[LINES[S.drill.id].n[S.drill.i + 1]].u')
    x, y = xy(pg, u[:2]); pg.mouse.click(x, y); pg.wait_for_timeout(400); settle(pg)
    save(pg.screenshot(), 'drill.png')

    # Sandbox: play until a game of 11+ plies with one slip, then shoot the report
    pg.evaluate("go('sandbox')"); pg.wait_for_timeout(300)
    pg.evaluate("SBS.scope = 'all'; SBS.odds = 'real'; sbStart()"); pg.wait_for_timeout(600)
    for game in range(20):
        slips = 0
        for _ in range(150):
            st = pg.evaluate("({state: S.drill.state, busy: S.drill.busy, mine: myTurnAt(S.drill.node)})")
            if st['state'] == 'done': break
            if st['busy'] or not st['mine']: pg.wait_for_timeout(250); continue
            exp = pg.evaluate("sbMyKids(S.drill.node).map(c => N[c].u)")
            if not slips and pg.evaluate('S.drill.hist.length') > 4:
                wrong = [m for m in pg.evaluate("DATA.legal[String(S.drill.node)] || []") if m not in exp and len(m) == 4]
                if wrong: tap(pg, wrong[0]); slips += 1; pg.wait_for_timeout(800); continue
            tap(pg, exp[0]); pg.wait_for_timeout(700)
        if pg.evaluate('S.drill.hist.length') >= 11 and slips: break
        pg.evaluate('sbStart()'); pg.wait_for_timeout(700)
    pg.evaluate('window.scrollTo(0, 0)'); settle(pg, 500)
    bottom = pg.evaluate("Math.max(document.getElementById('sbfeed').getBoundingClientRect().bottom, document.getElementById('db').parentElement.getBoundingClientRect().bottom) + scrollY + 28")
    full = pg.screenshot(full_page=True); w, h = Image.open(io.BytesIO(full)).size
    save(full, 'sandbox.png', crop=(0, 0, w, min(h, round(bottom * 2))))

    # level 5: the chip in the corner and the card that opens the shop (a few lines known, a week of days)
    pg.evaluate("""(() => { const now = Date.now(), D = Prog.d.days = Prog.d.days || {}; for (let k = 1; k <= 8; k++) D[dayKey(-k)] = ['a','b','c','d','e'];
      for (const id of BOOKS.b.drillable){ if (Level.n() >= 5) break; Prog.d.lines[id] = {box: 2, seen: 2, clean: 2, last: now, due: now + 2 * DAY, v: VER[id] || 1}; }
      S.drill = S.drillState = S.sbState = null; Prog.d.lvl = 4; Badges.queue = []; Coach.hush(); go('course'); Prog.save(); Badges.queue = []; Coach.hush(); })()""")
    pg.wait_for_timeout(1400); pg.evaluate("Coach.hush()"); settle(pg, 200)
    box = pg.evaluate("(() => { const c = document.getElementById('lvup').getBoundingClientRect(), b = document.getElementById('lvBtn').getBoundingClientRect(); return [Math.min(c.left, b.left) - 24, 0, innerWidth, c.bottom + 24]; })()")
    save(pg.screenshot(), 'levels.png', crop=tuple(round(v * 2) for v in box))
    pg.evaluate("const el = document.getElementById('lvup'); if (el) el.remove()")
    # Your games: some of every opening's lines known (a different share in each), the openings first
    pg.evaluate("""(() => { const now = Date.now(), share = [.6, .35, .5, .25, .45, .15, .3, .55];
      useSide('w'); DATA.chapters.forEach((C, k) => { const ls = chLines('w', C); ls.slice(0, Math.round(ls.length * share[k % share.length])).forEach(id => Prog.d.lines[id] = {box: 1, seen: 1, clean: 1, last: now, due: now + DAY, v: VER[id] || 1}); });
      Prog.d.lvl = Level.n(); Prog.save(); Badges.queue = []; Coach.hush(); S.gseg = 'open'; go('games'); })()"""); pg.wait_for_timeout(500); pg.evaluate("Coach.hush()"); settle(pg)
    bottom = pg.evaluate("document.querySelector('.otiles').getBoundingClientRect().bottom + scrollY + 24")
    full = pg.screenshot(full_page=True); w, h = Image.open(io.BytesIO(full)).size
    save(full, 'games.png', crop=(0, 0, w, min(h, round(bottom * 2)))); pg.evaluate("useSide('b')")
    # Today's five, three lines in, on a four-day streak; then the profile with a few badges
    pg.evaluate("""(() => { const D = Prog.d.days = {}; for (let k = 1; k <= 3; k++) D[dayKey(-k)] = ['a','b','c','d','e']; D[dayKey(-5)] = ['a','b','c','d','e'];
      D[dayKey()] = ['setup', 'center', 'grab']; S.drill = S.drillState = null; Coach.hush(); Badges.queue = []; Prog.save(); Badges.queue = []; go('drill'); })()"""); pg.wait_for_timeout(500); settle(pg)
    pg.evaluate("Coach.hush()"); pg.wait_for_timeout(200)
    shot = pg.screenshot(); save(shot, 'today.png', crop=(0, 0, 2560, 1500))
    pg.evaluate("Acct.open('me')"); pg.wait_for_timeout(400); settle(pg)
    box = pg.evaluate("(() => { const r = document.getElementById('acctPanel').getBoundingClientRect(); return [r.left, r.top, r.right, Math.min(r.bottom, innerHeight)]; })()")
    save(pg.screenshot(), 'badges.png', crop=tuple(round(v * 2) for v in box)); pg.evaluate("Acct.close()")
    # the shop: a top hat and the midnight colour on the coach
    pg.evaluate("""(() => { const el = document.getElementById('lvup'); if (el) el.remove(); const D = Prog.d.days; for (let k = 1; k <= 8; k++) D[dayKey(-k)] = ['a','b','c','d','e'];
      Prog.d.lvl = Level.n(); Prog.d.shop = {own: {'h-tophat': 1, 'c-midnight': 1}, wear: {head: ['h-tophat', 2], skin: ['c-midnight', 2]}}; Prog.save(); Badges.queue = []; Coach.hush(); go('shop'); })()""")
    pg.wait_for_timeout(500); pg.evaluate("Coach.hush(); const el = document.getElementById('lvup'); if (el) el.remove()"); settle(pg)
    save(pg.screenshot(), 'shop.png', crop=(0, 0, 2560, 1700))
    # the monthly recap: the month that has just ended, beside the one before it, with the lines drilled
    pg.evaluate("""(() => { const ids = BOOKS.w.drillable.slice(0, 60).concat(BOOKS.b.drillable.slice(0, 60)), D = Prog.d.days;
      for (let k = 18; k <= 46; k++) if (!D[dayKey(-k)]) D[dayKey(-k)] = ids.slice((k * 7) % 110, (k * 7) % 110 + 5); Prog.save(); Badges.queue = []; })()"""); pg.wait_for_timeout(300)
    pg.evaluate("document.querySelectorAll('#lvup').forEach(e => e.remove()); Coach.hush(); S.gseg = 'recap'; Recap.sel = null; go('games')"); pg.wait_for_function('!Recap.busy && !!(Prog.d.recap || {}).chk', timeout=60000)
    pg.evaluate("Coach.hush(); renderGames(); window.scrollTo(0, document.querySelector('.gseg').getBoundingClientRect().top + scrollY - 16)"); settle(pg)
    bottom = pg.evaluate("document.querySelector('.rcprac').getBoundingClientRect().bottom + 24")
    save(pg.screenshot(full_page=False), 'recap.png', crop=(0, 0, 2560, min(1720, round(bottom * 2))))
    # the coach after a slip in a drill: the same move has caught you twice, what the book says about it, and why
    for k in range(2):
        pg.evaluate("useSide('w'); startDrillLine('traxler', '', null, {from0: true})"); pg.wait_for_timeout(600); play_drill(pg, (9, 'g5f7')); pg.wait_for_timeout(500)
    pg.evaluate("Coach.hush(); window.scrollTo(0, 0)"); settle(pg)
    box = pg.evaluate("(() => { const b = document.querySelector('#db').getBoundingClientRect(), d = document.querySelector('.donebox').getBoundingClientRect(); return [b.left - 16, b.top - 16, d.right + 16, Math.max(b.bottom, d.bottom) + 16]; })()")
    save(pg.screenshot(), 'slip.png', crop=tuple(round(v * 2) for v in box))
    # the course finished: the big moment, then the library (a few slips on the Vienna unit's lines)
    pg.evaluate("""(() => { const t = Date.now() - 24 * DAY, c = Prog.d.course || (Prog.d.course = {u: {}, seen: {}}); c.u = c.u || {};
      for (const U of COURSE.filter(U => !U.soon)) c.u[U.id] = Object.assign({idea: t, spar: 3, sparGames: 3 + U.k % 3}, c.u[U.id] || {}, {pass: t + DAY * U.k, cp: U.id === 'w-sicilian' ? 5 : 6});
      for (const id of unitAllLines(UNIT['b-vienna']).slice(0, 10)) Prog.d.lines[id] = {box: 0, seen: 3, clean: 1, last: t, due: Date.now() + DAY, v: VER[id] || 1};
      stampGrad(); Prog.save(); Badges.queue = []; Coach.hush(); go('grad'); })()""")
    pg.wait_for_timeout(1300); settle(pg, 200)
    bottom = pg.evaluate("document.querySelector('.gradv').getBoundingClientRect().bottom + scrollY + 24")
    full = pg.screenshot(full_page=True); w, h = Image.open(io.BytesIO(full)).size
    save(full, 'grad.png', crop=(0, 0, w, min(h, round(bottom * 2))))
    pg.evaluate("openLibrary()"); pg.wait_for_timeout(500); settle(pg)
    bottom = pg.evaluate("document.querySelector('.libshelf').getBoundingClientRect().bottom + scrollY + 24")
    full = pg.screenshot(full_page=True); w, h = Image.open(io.BytesIO(full)).size
    save(full, 'library.png', crop=(0, 0, w, min(h, round(bottom * 2))))
    pg.evaluate("useSide('w'); S.chapter = 'italian'; S.lview = 'glance'; go('learn')"); pg.wait_for_timeout(500)
    pg.evaluate("window.scrollTo(0, document.querySelector('#chapter > .gseg').getBoundingClientRect().top + scrollY - 16)"); settle(pg)
    save(pg.screenshot(), 'glance.png'); pg.evaluate("S.lview = 'lessons'; useSide('b')")
    pg.evaluate("go('drill')"); pg.wait_for_timeout(300)
    pg.evaluate("startPuzzle(DATA.puzzles.findIndex(p => p.id === 'gb-charizard-47'))"); pg.wait_for_timeout(500); settle(pg)
    save(pg.screenshot(), 'puzzle.png')
    ctx.close()

    # Three phones: Learn (light), a lesson (dark), the openings in Your games (light)
    phones = []
    for scheme, hash_ in [('light', '#b.learn'), ('dark', '#b.line.bsl-slow'), ('light', '#b.games')]:
        c = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2, color_scheme=scheme, is_mobile=True, has_touch=True)
        local_fonts(c); q = c.new_page(); q.goto(URL + hash_); q.wait_for_timeout(900); settle(q)
        if '.line.' in hash_:
            for _ in range(12): q.keyboard.press('ArrowRight'); q.wait_for_timeout(90)
            q.evaluate("window.scrollTo(0, document.querySelector('.lhead').getBoundingClientRect().top + scrollY - 14)")
        if hash_.endswith('games'):
            q.evaluate("window.scrollTo(0, document.querySelector('.gseg').getBoundingClientRect().top + scrollY - 16)")
        q.wait_for_timeout(300); phones.append(Image.open(io.BytesIO(q.screenshot())).convert('RGB')); c.close()
    pw, ph = phones[0].size; pad, gap = 60, 56
    canvas = Image.new('RGB', (pad * 2 + pw * 3 + gap * 2, pad * 2 + ph), (206, 217, 208))
    for i, s in enumerate(phones):
        x = pad + i * (pw + gap)
        mask = Image.new('L', s.size, 0); ImageDraw.Draw(mask).rounded_rectangle([0, 0, pw - 1, ph - 1], radius=56, fill=255)
        canvas.paste(Image.new('RGB', s.size, (178, 192, 181)), (x + 8, pad + 12), mask); canvas.paste(s, (x, pad), mask)
    buf = io.BytesIO(); canvas.save(buf, 'PNG'); save(buf.getvalue(), 'phones.png')

    # Animated walk through one lesson
    c = b.new_context(viewport={'width': 1280, 'height': 760}); local_fonts(c)
    q = c.new_page(); q.goto(URL + '#b.line.bs-classical'); q.wait_for_timeout(900); settle(q)
    q.evaluate("openLine('bs-classical', 0)"); q.wait_for_timeout(300)
    frames = []
    for _ in range(q.evaluate("LINES['bs-classical'].n.length")):
        q.wait_for_timeout(350)
        shot = q.screenshot(clip={'x': 0, 'y': 90, 'width': 1280, 'height': 640})
        frames.append(Image.open(io.BytesIO(shot)).convert('RGB').resize((960, 480), Image.LANCZOS).convert('P', palette=Image.ADAPTIVE, colors=128))
        q.keyboard.press('ArrowRight')
    c.close()
    frames[0].save(IMG / 'demo.gif', save_all=True, append_images=frames[1:], duration=[1200] + [1300] * (len(frames) - 2) + [3000], loop=0, optimize=True)
    print(f"{'demo.gif':16s} {len(frames)} frames  {os.path.getsize(IMG / 'demo.gif') // 1024} KB")

    # The engine and the explore board: the end of a Black lesson, played on. The engine runs in a web worker, which
    # needs the page served over HTTP.
    site = Site(); app = site.start()
    try:
        c = b.new_context(viewport={'width': 1280, 'height': 1120}, device_scale_factor=2); local_fonts(c)
        q = c.new_page(); q.on('pageerror', lambda e: errors.append(str(e)))
        q.goto(app + '#b.line.bs-classical'); q.wait_for_timeout(900)
        q.keyboard.press('End'); q.wait_for_timeout(300)
        q.click('#exHere'); q.wait_for_timeout(400)
        for _ in range(100):
            if q.evaluate('!!(EngineUI.r && EngineUI.r.done)'): break
            q.wait_for_timeout(250)
        settle(q, 400); save(q.screenshot(), 'engine.png')
        c.close()
    finally:
        site.stop()
    b.close()
    if errors: sys.exit('page errors: ' + '; '.join(errors))
