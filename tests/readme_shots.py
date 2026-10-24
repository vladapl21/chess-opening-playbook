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

IMG = ROOT / 'docs' / 'img'; IMG.mkdir(exist_ok=True)
FONTS_DIR = os.environ.get('FONTS_DIR')
FONT_FILES = {
    'bm.ttf': ('bodonimoda', 'BodoniModa[opsz,wght].ttf'),
    'bmi.ttf': ('bodonimoda', 'BodoniModa-Italic[opsz,wght].ttf'),
    'is.ttf': ('instrumentsans', 'InstrumentSans[wdth,wght].ttf'),
    'jb.ttf': ('jetbrainsmono', 'JetBrainsMono[wght].ttf'),
}
FONT_CSS = '''@font-face{font-family:"Bodoni Moda";font-style:normal;font-weight:400 900;src:url(https://fonts.gstatic.com/local/bm.ttf) format("truetype")}
@font-face{font-family:"Bodoni Moda";font-style:italic;font-weight:400 900;src:url(https://fonts.gstatic.com/local/bmi.ttf) format("truetype")}
@font-face{font-family:"Instrument Sans";font-style:normal;font-weight:400 700;src:url(https://fonts.gstatic.com/local/is.ttf) format("truetype")}
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


def idle(pg):
    for _ in range(40):
        if not pg.evaluate('S.drill && S.drill.busy'): return
        pg.wait_for_timeout(200)


with sync_playwright() as p:
    b = launch(p)
    ctx = b.new_context(viewport={'width': 1280, 'height': 860}, device_scale_factor=2); local_fonts(ctx)
    pg = ctx.new_page(); errors = []; pg.on('pageerror', lambda e: errors.append(str(e)))

    pg.goto(URL + '#learn'); pg.wait_for_timeout(900); settle(pg)
    save(pg.screenshot(), 'learn-white.png')
    pg.click('.sidesw [data-side="b"]'); pg.wait_for_timeout(700); settle(pg)
    save(pg.screenshot(), 'learn-black.png')

    # Study: the Scotch lesson, a few moves in
    pg.evaluate("openLine('bs-mieses')"); pg.wait_for_timeout(400)
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

    pg.evaluate("go('games')"); pg.wait_for_timeout(500); settle(pg)
    full = pg.screenshot(full_page=True); w, h = Image.open(io.BytesIO(full)).size
    save(full, 'games.png', crop=(0, 0, w, min(h, 3000)))
    pg.evaluate("go('cheat')"); pg.wait_for_timeout(400); settle(pg); save(pg.screenshot(), 'cheat.png')
    pg.evaluate("go('drill')"); pg.wait_for_timeout(300)
    pg.evaluate("startPuzzle(DATA.puzzles.findIndex(p => p.id === 'gb-charizard-47'))"); pg.wait_for_timeout(500); settle(pg)
    save(pg.screenshot(), 'puzzle.png')
    ctx.close()

    # Three phones: Learn (light), a lesson (dark), Your games (light)
    phones = []
    for scheme, hash_ in [('light', '#b.learn'), ('dark', '#b.line.bq-ortho'), ('light', '#b.games')]:
        c = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2, color_scheme=scheme, is_mobile=True, has_touch=True)
        local_fonts(c); q = c.new_page(); q.goto(URL + hash_); q.wait_for_timeout(900); settle(q)
        if '.line.' in hash_:
            for _ in range(12): q.keyboard.press('ArrowRight'); q.wait_for_timeout(90)
            q.evaluate("window.scrollTo(0, document.querySelector('.lhead').getBoundingClientRect().top + scrollY - 14)")
        if hash_.endswith('games'):
            q.evaluate("window.scrollTo(0, document.querySelector('.insight').getBoundingClientRect().top + scrollY - 16)")
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
    q = c.new_page(); q.goto(URL + '#b.line.bs-mieses'); q.wait_for_timeout(900); settle(q)
    q.evaluate("openLine('bs-mieses', 0)"); q.wait_for_timeout(300)
    frames = []
    for _ in range(q.evaluate("LINES['bs-mieses'].n.length")):
        q.wait_for_timeout(350)
        shot = q.screenshot(clip={'x': 0, 'y': 90, 'width': 1280, 'height': 640})
        frames.append(Image.open(io.BytesIO(shot)).convert('RGB').resize((960, 480), Image.LANCZOS).convert('P', palette=Image.ADAPTIVE, colors=128))
        q.keyboard.press('ArrowRight')
    c.close()
    frames[0].save(IMG / 'demo.gif', save_all=True, append_images=frames[1:], duration=[1200] + [1300] * (len(frames) - 2) + [3000], loop=0, optimize=True)
    print(f"{'demo.gif':16s} {len(frames)} frames  {os.path.getsize(IMG / 'demo.gif') // 1024} KB")
    b.close()
    if errors: sys.exit('page errors: ' + '; '.join(errors))
