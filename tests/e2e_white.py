"""End-to-end checks for the White book: chapters, study, sandbox, drill, Your games, the openings at a glance (desktop, phone, dark)."""
import os, sys, random
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT = Path(__file__).resolve().parents[1]
URL = (ROOT / 'docs' / 'index.html').as_uri()
OUT = ROOT / 'tests' / 'out'; OUT.mkdir(exist_ok=True)
out = str(OUT) + '/'
CH = os.environ.get('CHROMIUM')  # optional path to a Chromium binary; default: Playwright's own
# The site build starts a visitor without games on the welcome screen. These suites test the hand-built playbook, so every
# context they open is marked as that player; tests/e2e_onboarding.py uses launch(p, house=False) to start as a new visitor.
HOUSE = """(() => { const K = 'italian-playbook-progress-v1'; if (!localStorage.getItem(K)) localStorage.setItem(K, JSON.stringify({lines: {}, puz: {}, updated: 0, me: {state: 'house'}})); })()"""


def launch(p, house=True):
    b = p.chromium.launch(executable_path=CH, args=['--no-sandbox']) if CH else p.chromium.launch()
    if house:
        new_context, new_page = b.new_context, b.new_page
        def ctx(**kw):
            c = new_context(**kw); c.add_init_script(HOUSE); return c
        def page(**kw):
            pg = new_page(**kw); pg.add_init_script(HOUSE); return pg
        b.new_context, b.new_page = ctx, page
    return b
errors = []

def sq_xy(pg, sq):
    box = pg.locator('#db svg').bounding_box()
    f = 'abcdefgh'.index(sq[0]); r = int(sq[1]) - 1
    if pg.evaluate('FLIP'): f, r = 7 - f, 7 - r
    return box['x'] + (f + .5) * box['width'] / 8, box['y'] + (7 - r + .5) * box['height'] / 8

def drag(pg, a, b):
    x1, y1 = sq_xy(pg, a); x2, y2 = sq_xy(pg, b)
    pg.mouse.move(x1, y1); pg.mouse.down(); pg.mouse.move(x2, y2, steps=5); pg.mouse.up()

def click_move(pg, a, b):
    x1, y1 = sq_xy(pg, a); pg.mouse.click(x1, y1); pg.wait_for_timeout(80)
    x2, y2 = sq_xy(pg, b); pg.mouse.click(x2, y2)

def play_sandbox(pg, slip_chance=0.25, label=''):
    pg.wait_for_timeout(500)
    moves = 0; slips_made = 0
    for _ in range(200):
        st = pg.evaluate("S.drill ? ({state:S.drill.state, busy:S.drill.busy, node:S.drill.node, wtm: myTurnAt(S.drill.node)}) : null")
        if not st: pg.wait_for_timeout(200); continue
        if st['state'] == 'done': break
        if st['busy'] or not st['wtm']: pg.wait_for_timeout(250); continue
        exp = pg.evaluate("sbMyKids(S.drill.node).map(c => N[c].u)")
        legal = pg.evaluate("DATA.legal[String(S.drill.node)] || []")
        if random.random() < slip_chance:
            wrong = [m for m in legal if m not in exp and len(m) == 4]
            if wrong:
                m = random.choice(wrong); drag(pg, m[:2], m[2:4]); slips_made += 1
                pg.wait_for_timeout(700)
                continue
        u = exp[0]
        if u in ('e1g1', 'e1c1', 'e8g8', 'e8c8') and random.random() < .5:
            drag(pg, u[:2], ('h' if u[2] == 'g' else 'a') + u[1])
        elif moves % 2: click_move(pg, u[:2], u[2:4])
        else: drag(pg, u[:2], u[2:4])
        moves += 1
        pg.wait_for_timeout(450)
    res = pg.evaluate("({state:S.drill.state, slips:S.drill.slips.length, line:S.drill.line, choices:S.drill.choices.length, hist:S.drill.hist.length})")
    print(f'  sandbox {label}: {res} white moves {moves} wrong tries {slips_made}')
    return res

if __name__ == '__main__':
    with sync_playwright() as p:
        b = launch(p)
        ctx = b.new_context(viewport={'width': 1280, 'height': 900})
        pg = ctx.new_page()
        pg.on('pageerror', lambda e: errors.append(f'pageerror: {e}'))
        pg.on('console', lambda m: errors.append(f'console {m.type}: {m.text}') if m.type == 'error' else None)
        pg.goto(URL + '#learn'); pg.wait_for_timeout(1200)
        pg.screenshot(path=out + 'v2_learn_italian.png')
        for ch in ['e5x', 'caro', 'sic', 'scandi', 'pirc', 'french', 'rare']:
            pg.click(f'.chnav [data-ch="{ch}"]'); pg.wait_for_timeout(350)
            assert pg.evaluate(f"S.chapter") == ch
            if ch in ('caro', 'sic'):
                pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(150)
                pg.screenshot(path=out + f'v2_learn_{ch}.png', full_page=True)
        print('hash', pg.evaluate('location.hash'))
        # open a lesson and look at options with odds
        pg.click('.chnav [data-ch="caro"]'); pg.wait_for_timeout(300)
        pg.click('[data-lesson="ck-march"]'); pg.wait_for_timeout(300)
        for _ in range(4): pg.keyboard.press('ArrowRight'); pg.wait_for_timeout(120)
        pg.screenshot(path=out + 'v2_study_caro.png')
        print('study where:', pg.inner_text('.crumbs .where'))
        # sandbox
        pg.click('.tabs button[data-view="sandbox"]'); pg.wait_for_timeout(300)
        pg.screenshot(path=out + 'v2_sb_intro.png')
        pg.click('#sbGo'); pg.wait_for_timeout(300)
        random.seed(4)
        play_sandbox(pg, 0.3, 'all/real')
        pg.screenshot(path=out + 'v2_sb_report.png', full_page=True)
        for scope, odds in [('sic', 'real'), ('caro', 'even'), ('e5x', 'weak'), ('italian', 'real'), ('pirc', 'even'), ('rare', 'even'), ('scandi', 'real'), ('french', 'real')]:
            pg.click('[data-sbf="scope:all"]'); pg.click(f'[data-sbf="pick:{scope}"]'); pg.click(f'[data-sbf="odds:{odds}"]'); pg.wait_for_timeout(100)
            pg.click('#sbAgain'); pg.wait_for_timeout(200)
            r = play_sandbox(pg, 0.15, f'{scope}/{odds}')
            assert r['state'] == 'done'
            if r['line']:
                les = pg.evaluate(f"chapterOf(lessonOf('{r['line']}')).id")
                assert les == scope, (les, scope)
        pg.screenshot(path=out + 'v2_sb_report2.png', full_page=True)
        print('sb stats', pg.evaluate("JSON.stringify(Prog.d.sb)")[:200])
        # mid-game screenshot
        pg.click('[data-sbf="scope:all"]'); pg.click('#sbAgain'); pg.wait_for_timeout(2600)
        pg.screenshot(path=out + 'v2_sb_mid.png')
        # drill by chapter
        pg.click('.tabs button[data-view="drill"]'); pg.wait_for_timeout(300)
        pg.click('.dmore > summary'); pg.wait_for_timeout(200)   # picking lines yourself is folded under today's five
        pg.click('[data-f="ch:sic"]'); pg.wait_for_timeout(200)
        pg.click('#smart'); pg.wait_for_timeout(900)
        print('drill line:', pg.evaluate('S.drill.id'))
        for _ in range(40):
            st = pg.evaluate('({state:S.drill.state,busy:S.drill.busy})')
            if st['state'] != 'play': break
            if st['busy']: pg.wait_for_timeout(300); continue
            u = pg.evaluate('N[LINES[S.drill.id].n[S.drill.i+1]].u'); drag(pg, u[:2], u[2:4]); pg.wait_for_timeout(800)
        print('drill final', pg.evaluate('S.drill.state'), pg.evaluate('S.drill.mistakes'))
        pg.screenshot(path=out + 'v2_drill.png')
        # switch away mid-sandbox and back
        pg.click('.tabs button[data-view="sandbox"]'); pg.wait_for_timeout(300)
        print('sandbox kept state:', pg.evaluate("S.drill && S.drill.kind"))
        pg.click('.tabs button[data-view="games"]'); pg.wait_for_timeout(400)
        # Your games: the openings first, as tiles; shots and game reviews behind a switch
        assert pg.locator('.otile').count() == pg.evaluate('DATA.chapters.length') and pg.locator('.mshot, .grev').count() == 0
        known, total = pg.evaluate("[chLines('w', CHAPTERS.sic).filter(lineClean).length, chLines('w', CHAPTERS.sic).length]"); print('sicilian lines known:', known, 'of', total)
        assert f'{known} of {total} lines' in pg.inner_text('.otile[data-ch="sic"]')
        pg.screenshot(path=out + 'v2_games.png', full_page=True)
        pg.click('[data-gseg="shots"]'); pg.wait_for_timeout(300); assert pg.locator('.mshot').count() == 4
        pg.click('[data-gseg="games"]'); pg.wait_for_timeout(300); assert pg.locator('.grev').count() == pg.evaluate('DATA.games.length')
        pg.screenshot(path=out + 'v2_games_reviews.png', full_page=True)
        pg.locator('.grev').nth(2).click(); pg.wait_for_timeout(300); assert pg.evaluate('[S.view, S.studyFrom]') == ['study', 'games']
        pg.click('.crumbs [data-go="games"]'); pg.wait_for_timeout(300); assert pg.locator('.grev').count() > 0, 'back on the same part of the page'
        pg.click('[data-gseg="open"]'); pg.wait_for_timeout(300)
        pg.click('.otile[data-ch="italian"]'); pg.wait_for_timeout(400)
        assert pg.evaluate('[S.view, S.chapter]') == ['learn', 'italian'] and pg.locator('[data-lview]').count() == 2
        pg.click('[data-lview="glance"]'); pg.wait_for_timeout(300)
        n_glance = pg.locator('#view .ccard').count(); print('italian at a glance:', n_glance); assert n_glance == pg.evaluate('glanceCards(CHAPTERS.italian).length') >= 20
        assert pg.locator('#view .lcard').count() == 0
        pg.screenshot(path=out + 'v2_glance.png')
        pg.locator('#view .ccard').nth(6).click(); pg.wait_for_timeout(300); assert pg.evaluate('[S.view, S.studyFrom]') == ['study', 'learn']
        pg.click('.crumbs [data-go="learn"]'); pg.wait_for_timeout(300); assert pg.locator('#view .ccard').count() == n_glance
        pg.click('[data-lview="lessons"]'); pg.wait_for_timeout(300); assert pg.locator('#view .lcard').count() > 0
        # every opening has its cards, and together they are the old cheat sheet
        assert pg.evaluate('DATA.chapters.reduce((a, C) => a + glanceCards(C).length, 0)') == pg.evaluate('DATA.cheat.length')
        # puzzles all solvable
        pg.click('.tabs button[data-view="drill"]'); pg.wait_for_timeout(300)
        n = pg.evaluate('DATA.puzzles.length'); solved = 0
        for k in range(n):
            pg.evaluate(f'startPuzzle({k})'); pg.wait_for_timeout(250)
            u = pg.evaluate(f'DATA.puzzles[{k}].ok[0]'); drag(pg, u[:2], u[2:4]); pg.wait_for_timeout(350)
            solved += pg.evaluate('S.drill.state') == 'done'
        print('puzzles solved', solved, '/', n)
        ctx.close()
        # phone
        ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
        pg = ctx.new_page(); pg.on('pageerror', lambda e: errors.append(f'pageerror(m): {e}'))
        pg.goto(URL + '#learn'); pg.wait_for_timeout(1200)
        print('m learn scrollWidth', pg.evaluate('document.documentElement.scrollWidth'))
        pg.screenshot(path=out + 'v2_m_learn.png')
        pg.evaluate("document.querySelector('.chnav [data-ch=\"sic\"]').click()"); pg.wait_for_timeout(500)
        pg.screenshot(path=out + 'v2_m_learn_sic.png', full_page=True)
        print('m sic scrollWidth', pg.evaluate('document.documentElement.scrollWidth'))
        pg.evaluate("document.querySelector('.tabs button[data-view=\"sandbox\"]').click()"); pg.wait_for_timeout(300)
        pg.evaluate("document.getElementById('sbGo').click()")
        random.seed(9)
        play_sandbox(pg, 0.3, 'phone')
        print('m sandbox scrollWidth', pg.evaluate('document.documentElement.scrollWidth'))
        pg.screenshot(path=out + 'v2_m_sb_report.png', full_page=True)
        for v in ['games', 'drill']:
            pg.evaluate(f"document.querySelector('.tabs button[data-view=\"{v}\"]').click()"); pg.wait_for_timeout(400)
            print(f'm {v} scrollWidth', pg.evaluate('document.documentElement.scrollWidth'))
        for g in ['shots', 'games', 'open']:
            pg.evaluate(f"S.gseg = '{g}'; go('games')"); pg.wait_for_timeout(300)
            w = pg.evaluate('document.documentElement.scrollWidth'); print(f'm games/{g} scrollWidth', w); assert w <= 390
        pg.evaluate("S.lview = 'glance'; S.chapter = 'italian'; go('learn')"); pg.wait_for_timeout(400)
        w = pg.evaluate('document.documentElement.scrollWidth'); print('m glance scrollWidth', w); assert w <= 390
        pg.screenshot(path=out + 'v2_m_glance.png', full_page=True); pg.evaluate("S.lview = 'lessons'")
        pg.screenshot(path=out + 'v2_m_drill.png')
        pg.evaluate("document.querySelector('.tabs button[data-view=\"games\"]').click()"); pg.wait_for_timeout(400)
        pg.screenshot(path=out + 'v2_m_games.png', full_page=True)
        ctx.close()
        # dark
        ctx = b.new_context(viewport={'width': 1280, 'height': 900}, color_scheme='dark')
        pg = ctx.new_page(); pg.on('pageerror', lambda e: errors.append(f'pageerror(d): {e}'))
        pg.goto(URL + '#learn.scandi'); pg.wait_for_timeout(1200)
        pg.screenshot(path=out + 'v2_dark_scandi.png')
        pg.goto(URL + '#sandbox'); pg.reload(); pg.wait_for_timeout(900)
        pg.evaluate("document.getElementById('sbGo').click()"); pg.wait_for_timeout(2500)
        pg.screenshot(path=out + 'v2_dark_sb.png')
        print('errors', errors[:10])
        assert not [e for e in errors if 'ERR_' not in e], 'page errors'
        b.close()
