"""End-to-end checks for the engine and the explore board.

The page is served over HTTP with engine/ beside it, the way GitHub Pages serves it: a web worker can't start from a
file:// page. The file:// build is checked too, for its fallback note."""
import re, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
sys.path.insert(0, str(Path(__file__).resolve().parent))
from e2e_white import launch, out, URL as FILE_URL  # noqa: E402
from serve import Site  # noqa: E402
errors = []


def hook(pg, name=''):
    pg.on('pageerror', lambda e: errors.append(f'{name} pageerror: {e}'))
    pg.on('console', lambda m: errors.append(f'{name} console: {m.text}') if m.type == 'error' and 'ERR_' not in m.text else None)


def notation(text):
    """Squares, piece-letter moves or castling symbols in text the user reads (f7 and f2 are allowed)."""
    bad = [m for m in re.findall(r'\b[a-h][1-8]\b', text) if m not in ('f7', 'f2')]
    bad += re.findall(r'\b[KQRBN]x?[a-h][1-8]\b|\bO-O\b', text)
    return bad


def wait_depth(pg, d=12, secs=20):
    for _ in range(int(secs * 5)):
        if (pg.evaluate('EngineUI.r ? EngineUI.r.d : 0') or 0) >= d: return True
        pg.wait_for_timeout(200)
    return False


def ex_xy(pg, sq):
    box = pg.locator('#xb svg').bounding_box()
    f = 'abcdefgh'.index(sq[0]); r = int(sq[1]) - 1
    if pg.evaluate('S.ex.flip'): f, r = 7 - f, 7 - r
    return box['x'] + (f + .5) * box['width'] / 8, box['y'] + (7 - r + .5) * box['height'] / 8


def ex_move(pg, u, drag=False):
    (x1, y1), (x2, y2) = ex_xy(pg, u[:2]), ex_xy(pg, u[2:4])
    if drag: pg.mouse.move(x1, y1); pg.mouse.down(); pg.mouse.move(x2, y2, steps=6); pg.mouse.up()
    else: pg.mouse.click(x1, y1); pg.wait_for_timeout(80); pg.mouse.click(x2, y2)
    pg.wait_for_timeout(350)


site = Site(); APP = site.start()

try:
    with sync_playwright() as p:
        b = launch(p)
        ctx = b.new_context(viewport={'width': 1280, 'height': 900})
        pg = ctx.new_page(); hook(pg, 'desktop')

        # ---- study: the switch under the board turns the engine on; it remembers
        pg.goto(APP + '#line.fried-liver'); pg.wait_for_timeout(900)
        pg.keyboard.press('End'); pg.wait_for_timeout(200)
        assert pg.locator('#engcard').count() == 0 and pg.evaluate('Engine.state') == 'off', 'engine starts only when asked'
        pg.click('#cEng')
        assert wait_depth(pg, 14), pg.evaluate('[Engine.state, Engine.why]')
        card = pg.inner_text('#engcard')
        rows = pg.locator('#engcard .erow').count()
        print('study card:', card.replace('\n', ' | ')[:260])
        assert rows == 3, rows
        assert pg.locator('#sb svg g.eng .arr.e').count() == 3, 'three engine arrows'
        # three different moves, and no two of them read the same
        assert pg.evaluate('new Set(EngineUI.r.lines.map(l => l.pv[0])).size') == 3, pg.evaluate('EngineUI.r.lines.map(l => l.pv[0])')
        labels = pg.locator('#engcard .erow .el').all_inner_texts()
        assert len(set(labels)) == 3, labels
        # the end of a main line also says what to aim for from here; earlier positions don't
        plan = pg.inner_text('.plan'); print('plan:', plan.replace('\n', ' | ')[:160])
        assert plan.upper().startswith('PLAN FROM HERE') and pg.locator('.plan li').count() >= 2 and not notation(plan), plan
        assert 'depth' in pg.inner_text('#stext') and not notation(card), notation(card)
        pg.screenshot(path=out + 'engine_study.png')
        # hovering a move singles out its arrow
        pg.hover('#engcard [data-ek="1"]'); pg.wait_for_timeout(120)
        assert pg.locator('#sb svg g.eng .arr.e2.on').count() == 1 and pg.locator('#sb svg g.eng .arr.e.dim').count() == 2
        pg.mouse.move(5, 5)
        # stepping back re-analyses; stepping forward again shows what was found at once (kept for the session)
        fen_end, d_end = pg.evaluate('EngineUI.host.fen'), pg.evaluate('EngineUI.r.d')
        pg.keyboard.press('ArrowLeft'); pg.wait_for_timeout(300)
        assert pg.evaluate('EngineUI.host.fen') != fen_end and pg.locator('.plan').count() == 0
        assert wait_depth(pg, 10)
        pg.keyboard.press('ArrowRight'); pg.wait_for_timeout(60)
        assert pg.evaluate('EngineUI.r.d') >= d_end and pg.locator('#engcard .erow').count() == 3
        pg.reload(); pg.wait_for_timeout(900)
        pg.goto(APP + '#line.fried-liver'); pg.wait_for_timeout(600)
        assert pg.locator('#engcard').count() == 1 and pg.get_attribute('#cEng', 'aria-pressed') == 'true', 'switch remembered'

        # ---- a move from the card opens the explore board with that move played
        pg.keyboard.press('End'); pg.wait_for_timeout(200)
        assert wait_depth(pg, 12)
        best = pg.evaluate('EngineUI.r.lines[0].pv[0]')
        pg.click('#engcard [data-ek="0"]'); pg.wait_for_timeout(700)
        X = pg.evaluate('({view: S.view, moves: S.ex.moves, i: S.ex.i, base: S.ex.base, title: S.ex.title})')
        B = X['base']; print('explore:', {k: v for k, v in X.items() if k != 'moves'}, X['moves'][B:])
        assert X['view'] == 'explore' and B > 0 and X['moves'][B:] == [best] and X['i'] == B + 1, 'the moves from the start come along'
        assert pg.evaluate('location.hash') == '#explore'
        assert wait_depth(pg, 12)
        assert not notation(pg.inner_text('#view')), notation(pg.inner_text('#view'))
        pg.screenshot(path=out + 'engine_explore.png')

        # step back, then play other moves for both sides (tap-tap and drag)
        pg.keyboard.press('ArrowLeft'); pg.wait_for_timeout(250)
        assert pg.evaluate('S.ex.i') == B
        legal = pg.evaluate("exChess().moves({verbose: true}).map(m => m.from + m.to)")
        other = next(u for u in legal if u != best[:4])
        ex_move(pg, other)
        assert pg.evaluate('S.ex.moves.slice(S.ex.base)') == [other] and pg.evaluate('S.ex.i') == B + 1, pg.evaluate('S.ex.moves')
        reply = pg.evaluate("exChess().moves({verbose: true}).map(m => m.from + m.to)")[0]
        ex_move(pg, reply, drag=True)
        assert pg.evaluate('S.ex.i') == B + 2, pg.evaluate('[S.ex.moves, S.ex.i]')
        # an illegal try changes nothing
        ex_move(pg, 'a1a8')
        assert pg.evaluate('S.ex.i') == B + 2
        # the board turns around and still takes moves the right way up
        pg.click('#xFlip'); pg.wait_for_timeout(200)
        assert pg.evaluate('S.ex.flip') != pg.evaluate('FLIP')
        u3 = pg.evaluate("exChess().moves({verbose: true}).map(m => m.from + m.to)")[0]
        ex_move(pg, u3)
        assert pg.evaluate('S.ex.i') == B + 3 and pg.evaluate(f'S.ex.moves[{B + 2}]') == u3
        assert pg.locator('.timeline .trow').count() == B + 3

        # the engine answers your moves when asked
        pg.check('#exAns'); pg.wait_for_timeout(200)
        before = pg.evaluate('S.ex.i')
        if pg.evaluate('S.ex.busy'):  # it was the engine's turn: it moves first
            for _ in range(40):
                if not pg.evaluate('S.ex.busy'): break
                pg.wait_for_timeout(150)
            before = pg.evaluate('S.ex.i')
        mine = pg.evaluate("exChess().moves({verbose: true}).map(m => m.from + m.to)")[0]
        ex_move(pg, mine)
        for _ in range(40):
            if pg.evaluate('S.ex.i') == before + 2 and not pg.evaluate('S.ex.busy'): break
            pg.wait_for_timeout(150)
        print('engine answered:', pg.evaluate('S.ex.moves.slice(-2)'))
        assert pg.evaluate('S.ex.i') == before + 2
        pg.uncheck('#exAns')

        # play the engine's line on the board, then stop it
        assert wait_depth(pg, 10)
        i0 = pg.evaluate('S.ex.i')
        pg.click('#eLine'); pg.wait_for_timeout(2600)
        assert pg.evaluate('!!S.ex.auto') and pg.evaluate('S.ex.i') >= i0 + 2, pg.evaluate('[S.ex.i, i0]')
        pg.click('#xPlay'); pg.wait_for_timeout(200)
        assert not pg.evaluate('!!S.ex.auto')

        # a reload keeps the explored position; Back returns to the lesson where you left it
        moves = pg.evaluate('S.ex.moves')
        pg.reload(); pg.wait_for_timeout(900)
        assert pg.evaluate('S.view') == 'explore' and pg.evaluate('S.ex.moves') == moves
        pg.click('#exBack'); pg.wait_for_timeout(400)
        assert pg.evaluate('[S.view, S.line]') == ['study', 'fried-liver'], pg.evaluate('[S.view, S.line]')
        assert pg.evaluate('S.i') == pg.evaluate('LINES[S.line].n.length - 1')

        # ---- drill: the engine stays away while you play, and opens on the final position afterwards
        pg.evaluate("startDrillLine('setup')"); pg.wait_for_timeout(500)
        assert pg.evaluate('EngineUI.host') is None and pg.locator('#engcard').count() == 0
        for _ in range(80):
            st = pg.evaluate('({state: S.drill.state, busy: S.drill.busy})')
            if st['state'] == 'done': break
            if st['busy']: pg.wait_for_timeout(200); continue
            u = pg.evaluate('N[LINES[S.drill.id].n[S.drill.i + 1]].u'); pg.evaluate(f"tryMove('{u[:2]}', '{u[2:4]}')"); pg.wait_for_timeout(800)
        assert pg.evaluate('Engine.state') != 'busy' or pg.evaluate('EngineUI.host') is None
        assert pg.locator('.plan').count() == 1, 'a finished main line shows its plan'
        pg.click('#dExplore'); pg.wait_for_timeout(500)
        last = pg.evaluate("nodeFen(LINES['setup'].n[LINES['setup'].n.length - 1])")
        assert pg.evaluate('S.view') == 'explore' and pg.evaluate('S.ex.start') == pg.evaluate('START_FEN') and pg.evaluate('S.ex.i') == pg.evaluate('S.ex.base') > 0 and pg.evaluate('exChess().fen()') == last
        assert 'PLAN FROM THE END' in pg.inner_text('.plan').upper(), 'the plan comes along to the explore board'
        pg.click('#exBack'); pg.wait_for_timeout(300)
        assert pg.evaluate('S.view') == 'drill' and pg.evaluate('S.drill.state') == 'done'

        # ---- Black book, phone width, dark: the board faces Black and nothing scrolls sideways
        ph = b.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True, color_scheme='dark')
        q = ph.new_page(); hook(q, 'phone')
        q.goto(APP + '#b.line.bsl-slow'); q.wait_for_timeout(900)
        q.keyboard.press('End'); q.wait_for_timeout(200)
        q.click('#cEng'); assert wait_depth(q, 10)
        assert q.evaluate('document.documentElement.scrollWidth') <= 390
        q.screenshot(path=out + 'engine_phone_study_dark.png', full_page=True)
        q.click('#exHere'); q.wait_for_timeout(500)
        assert q.evaluate('S.ex.flip') is True and q.evaluate('ME') == 0
        assert wait_depth(q, 10)
        assert q.evaluate('document.documentElement.scrollWidth') <= 390
        q.screenshot(path=out + 'engine_phone_explore_dark.png', full_page=True)

        # ---- opened as a file, the engine can't start: the card says so, nothing breaks
        f = b.new_context(viewport={'width': 1280, 'height': 900}).new_page(); hook(f, 'file')
        f.goto(FILE_URL + '#line.fried-liver'); f.wait_for_timeout(900)
        if f.get_attribute('#cEng', 'aria-pressed') != 'true': f.click('#cEng')
        f.wait_for_timeout(300)
        print('file:// note:', f.inner_text('#engcard').replace('\n', ' | '))
        assert f.evaluate('Engine.state') == 'failed' and 'website' in f.inner_text('#engcard')
        b.close()
finally:
    site.stop()
print('ERRORS:', errors[:8])
assert not errors
print('engine checks passed')
