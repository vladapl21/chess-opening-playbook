"""The last three games, reviewed and drilled, with chess.com stubbed and the real engine (over local HTTP). The house
account's newest games: one where White leaves the Black book on move two, one where the player leaves the White book
(the knight grabs the e-pawn) and one where the queen is lost on move seven. The first check keeps the newest three,
each review says where the game left the book and what to play there (the book's move, or the engine's answer when the
book has none), the engine finds the first costly move, and Drill it plays each spot on the drill board: a wrong move
is answered with what punishes it, a clean run is kept with the review. Then: the reviews after a reload, a new game
pushing the oldest out, a game pasted in (and the question of which side the player was), the coach's word about a new
review, the Sandbox from the position where the player left the book, and a phone in dark mode."""
import json, re, datetime
import chess, chess.pgn  # python-chess: the fixtures are written move by move, so every game is legal
from io import StringIO
from playwright.sync_api import sync_playwright
from e2e_white import launch, out
from serve import Site

site = Site(docs=True); URL = site.start()
errors = []


def hook(pg):
    pg.on('pageerror', lambda e: errors.append(f'pageerror: {e}'))
    pg.on('console', lambda m: errors.append(f'console {m.type}: {m.text}') if m.type == 'error' and 'ERR_' not in m.text else None)


now = datetime.datetime.now(datetime.timezone.utc)
def pgn(sans, white, black, result, ago_h):
    b = chess.Board(); g = chess.pgn.Game()
    t = now - datetime.timedelta(hours=ago_h)
    g.headers.update({'Event': 'Live Chess', 'Site': 'Chess.com', 'White': white, 'Black': black, 'Result': result, 'WhiteElo': '1010', 'BlackElo': '1004',
                      'UTCDate': t.strftime('%Y.%m.%d'), 'UTCTime': t.strftime('%H:%M:%S'), 'Date': t.strftime('%Y.%m.%d'), 'TimeControl': '600',
                      'Link': f'https://www.chess.com/game/live/{abs(hash((white, black, ago_h))) % 10**9}'})
    node = g
    for s in sans.split():
        node = node.add_variation(b.parse_san(s)); b.push(node.move)
    return str(g)


ME = 'aqua_alpaca'
G_OPP = pgn('e4 e5 g3 Nf6 d3 d5 exd5 Nxd5 Bg2 Nc6 Nf3 Be7 O-O O-O Re1 Bg4', 'rook_lover', ME, '1/2-1/2', 1)      # White leaves the book on move 2
G_ME = pgn('e4 e5 Nf3 Nc6 Bc4 Nf6 Nxe5 Nxe5 d4 Nxc4 Qe2 d5 exd5 Qe7 Qxe7 Bxe7', ME, 'knightmare', '0-1', 3)      # the player grabs the e-pawn
G_MK = pgn('e4 e5 Nf3 Nc6 Bc4 a6 d3 Nf6 O-O Bc5 Qe2 d6 Qe3 Bxe3 Bxe3 O-O Nc3 Bg4 h3 Bh5', ME, 'queenside', '0-1', 5)  # the queen goes on move 7
G_OLD = [pgn('e4 c5 Nf3 d6 c3 Nf6 Be2 Nc6 O-O e5', ME, 'old_one', '1-0', 30), pgn('d4 d5 c4 c6 Nc3 Nf6 Nf3 dxc4', 'old_two', ME, '0-1', 40)]
G_NEW = pgn('e4 e5 Nf3 Nc6 Bc4 Bc5 c3 Nf6 d4 exd4 cxd4 Bb4+ Nc3 Nxe4 O-O Bxc3 d5', ME, 'latecomer', '1-0', 0.2)   # comes in later
G_PASTE = pgn('e4 e5 Nf3 Nc6 Bb5 a6 Ba4 Nf6 O-O Be7', 'strangerA', 'strangerB', '1-0', 50)                          # nobody we know: which side?
games = {'list': [G_OPP, G_ME, G_MK] + G_OLD}
hits = []


def chesscom(route):
    u = route.request.url; hits.append(u)
    m = re.search(r'/player/([^/]+)/games/(\d{4})/(\d\d)$', u)
    if m and m.group(1) == ME and (int(m.group(2)), int(m.group(3))) == (now.year, now.month):
        return route.fulfill(status=200, content_type='application/json', headers={'Access-Control-Allow-Origin': '*'}, body=json.dumps({'games': [{'rules': 'chess', 'time_class': 'blitz', 'pgn': g} for g in games['list']]}))
    route.fulfill(status=200, content_type='application/json', headers={'Access-Control-Allow-Origin': '*'}, body='{"games": []}')


def board_click(pg, a, b):
    box = pg.locator('#db svg').bounding_box(); flip = pg.evaluate('FLIP')
    def xy(sq):
        f, r = 'abcdefgh'.index(sq[0]), int(sq[1]) - 1
        if flip: f, r = 7 - f, 7 - r
        return box['x'] + (f + .5) * box['width'] / 8, box['y'] + (7 - r + .5) * box['height'] / 8
    pg.mouse.click(*xy(a)); pg.wait_for_timeout(120); pg.mouse.click(*xy(b))


def play_rv(pg, slip=False):
    """Play the review drill to its end: the player's moves from the line, one wrong move first if asked."""
    for _ in range(40):
        st = pg.evaluate("({s: S.drill.state, b: S.drill.busy, i: S.drill.i, n: S.drill.moves.length})")
        if st['s'] == 'done': return
        if st['b'] or st['i'] % 2: pg.wait_for_timeout(200); continue
        if slip:
            bad = pg.evaluate("(() => { const D = S.drill, exp = D.moves[D.i]; return Review.legal(D).find(u => u !== exp && !Review.punish(Review.fen(D), u, D.me)) || Review.legal(D).find(u => u !== exp); })()")
            board_click(pg, bad[:2], bad[2:4]); pg.wait_for_timeout(500)
            msg = pg.inner_text('#dpanel .feedback'); print('  a wrong move:', ' '.join(msg.split())[:140]); assert 'Not the move' in msg, msg
            board_click(pg, bad[:2], bad[2:4]); pg.wait_for_timeout(500)
            assert pg.evaluate("S.drill.hint === S.drill.moves[S.drill.i]"), 'two misses: the arrow shows the move'
            msg = pg.inner_text('#dpanel .feedback'); print('  twice:', ' '.join(msg.split())[:160]); assert 'The arrow shows the move' in msg
            slip = False; continue
        u = pg.evaluate("S.drill.moves[S.drill.i]"); board_click(pg, u[:2], u[2:4]); pg.wait_for_timeout(700)
    raise AssertionError('the drill did not end')


with sync_playwright() as p:
    b = launch(p)
    ctx = b.new_context(viewport={'width': 1280, 'height': 900}, device_scale_factor=2); ctx.route('https://api.chess.com/**', chesscom)
    pg = ctx.new_page(); hook(pg)
    pg.goto(URL + '#course'); pg.wait_for_timeout(800)
    assert pg.evaluate("[Review.on(), Review.can()]") == [True, True], 'the house playbook reads its own account'

    # ---- the first check: the newest three games, the oldest two left out
    pg.wait_for_function("(Prog.d.rg || {}).chk > 0", timeout=20000)
    ids = pg.evaluate("Review.list().map(R => [R.opp, R.me, R.by, R.at])"); print('kept:', ids)
    assert [x[0] for x in ids] == ['rook_lover', 'knightmare', 'queenside'], ids
    assert ids[0][1:] == ['b', 'opp', 2] and ids[1][1:] == ['w', 'me', 6] and ids[2][1:] == ['w', 'opp', 5], ids
    coach = pg.evaluate("(document.querySelector('#coach .cbub') || {}).innerText || ''"); print('coach:', ' '.join(coach.split())[:120])
    assert 'White left your book at move 2' in coach, coach
    pg.click('#coach [data-cgo="last"]'); pg.wait_for_timeout(600)
    assert pg.evaluate("[S.view, S.gseg]") == ['games', 'last'], 'the coach opens the reviews'
    # the engine's part: the answer to the new move, then the first costly move in each game
    pg.wait_for_function("Review.list().every(R => R.mk !== undefined && (R.by !== 'opp' || R.ln))", timeout=240000)
    revs = pg.evaluate("Review.list().map(R => ({opp: R.opp, ln: R.ln, mk: R.mk && [R.mk.k, R.mk.best, R.mk.loss]}))"); print('engine part:', revs)
    assert len(revs[0]['ln']) >= 3 and revs[2]['mk'] and revs[2]['mk'][0] == 12, revs
    pg.screenshot(path=out + 'rv_list.png', full_page=True)

    cards = pg.locator('.rvcard')
    t0 = ' '.join(cards.nth(0).inner_text().split()); print('card 1:', t0[:300])
    assert 'Move 2: White left your book' in t0 and "The engine's answer:" in t0 and 'Your book has:' in t0, t0
    t1 = ' '.join(cards.nth(1).inner_text().split()); print('card 2:', t1[:300])
    assert 'Move 4: you left your book' in t1 and 'Your book:' in t1 and 'Drill your line' in t1, t1
    t2 = ' '.join(cards.nth(2).inner_text().split()); print('card 3:', t2[:400])
    assert 'Move 7: the first costly move' in t2 and 'Better:' in t2, t2
    assert not re.search(r'\b[a-h][1-8]\b', ' '.join([t0, t1, t2]).replace('f7', '').replace('f2', '')), 'no squares in the words'

    # ---- Drill it: White's new move, the engine's answer from the position in the game
    cards.nth(0).locator('[data-rvd$=":o"]').click(); pg.wait_for_timeout(900)
    assert pg.evaluate("[S.view, S.drill.kind, S.drill.part, SIDE, FLIP]") == ['drill', 'rv', 'o', 'b', True]
    assert pg.evaluate("document.querySelector('.today').closest('[hidden]') !== null"), 'the rest of the drill page stays out of the way'
    pg.screenshot(path=out + 'rv_drill.png')
    play_rv(pg, slip=True)
    done = ' '.join(pg.inner_text('#dpanel').split()); print('done:', done[:160]); assert '1 slip' in done
    pg.click('#rvAgain'); pg.wait_for_timeout(700); play_rv(pg)
    assert 'Clean run' in pg.inner_text('#dpanel')
    assert pg.evaluate("Review.list()[0].d.o.slice(0, 2)") == [2, 1], 'the runs are kept with the review'
    pg.click('#rvBack'); pg.wait_for_timeout(600)
    assert pg.evaluate("[S.view, S.gseg]") == ['games', 'last']

    # ---- the player left the book: the book's own line from move one, and the Sandbox from that position
    pg.locator('.rvcard').nth(1).locator('[data-rvb]').click(); pg.wait_for_timeout(900)
    st = pg.evaluate("[S.view, S.drill.kind, SIDE, S.drill.s0, LINES[S.drill.id].n.slice(1, 8).map(i => N[i].u).join(' ')]"); print('book line:', st)
    assert st[:4] == ['drill', 'line', 'w', 0] and st[4].startswith('e2e4 e7e5 g1f3 b8c6 f1c4 g8f6 f3g5'), st
    pg.evaluate("S.drill = S.drillState = null; S.gseg = 'last'; go('games')"); pg.wait_for_timeout(600)
    pg.locator('.rvcard').nth(1).locator('[data-rvs]').click(); pg.wait_for_timeout(1400)
    st = pg.evaluate("[S.view, S.drill.kind, N[S.drill.from].u, ply(S.drill.from)]"); print('sandbox from the position:', st)
    assert st == ['sandbox', 'sb', 'g8f6', 6], st

    # ---- the first costly move: drill the better move
    pg.evaluate("S.drill = S.sbState = null; S.gseg = 'last'; go('games')"); pg.wait_for_timeout(600)
    pg.locator('.rvcard').nth(2).locator('[data-rvd$=":m"]').click(); pg.wait_for_timeout(900)
    assert pg.evaluate("[S.drill.kind, S.drill.part, S.drill.no]") == ['rv', 'm', 7]
    play_rv(pg); assert 'Clean run' in pg.inner_text('#dpanel')

    # ---- after a reload: everything kept, nothing to work out again
    pg.reload(); pg.wait_for_timeout(1200)
    keep = pg.evaluate("Review.list().map(R => [R.opp, !!R.ln, R.mk === undefined ? 'none' : !!R.mk, R.d ? Object.keys(R.d).sort().join() : ''])"); print('after a reload:', keep)
    assert keep == [['rook_lover', True, keep[0][2], 'o'], ['knightmare', False, keep[1][2], ''], ['queenside', True, True, 'm']], keep

    # ---- a new game comes in, the oldest goes
    games['list'] = [G_NEW] + games['list']
    pg.evaluate("S.gseg = 'last'; go('games')"); pg.wait_for_timeout(500)
    pg.click('#rvGo'); pg.wait_for_function("Review.list()[0].opp === 'latecomer'", timeout=20000)
    print('after the next check:', pg.evaluate("Review.list().map(R => R.opp)"))
    assert pg.evaluate("Review.list().map(R => R.opp)") == ['latecomer', 'rook_lover', 'knightmare'] and pg.evaluate("Prog.d.rg.g.length") == 3

    # ---- a game pasted in, by someone else: which side?
    pg.click('.rvpaste summary') if not pg.evaluate("document.querySelector('.rvpaste').open") else None
    pg.fill('#rvPgn', G_PASTE); pg.click('#rvAdd'); pg.wait_for_timeout(400)
    assert pg.locator('[data-rvside]').count() == 2, 'neither player is the account: the page asks'
    pg.click('[data-rvside="b"]'); pg.wait_for_timeout(500)
    top = pg.evaluate("[Review.list()[0].opp, Review.list()[0].me, Review.list()[0].src, Review.list().length]"); print('pasted:', top)
    assert top == ['strangerA', 'b', 'paste', 3], top
    pg.evaluate("document.querySelector('.rvpaste').open = true")
    pg.fill('#rvPgn', 'not a game'); pg.click('#rvAdd'); pg.wait_for_timeout(300)
    assert "doesn't look like a game" in pg.inner_text('.rvpaste')

    # ---- a phone in dark mode
    ph = b.new_context(viewport={'width': 390, 'height': 844}, color_scheme='dark'); ph.route('https://api.chess.com/**', chesscom)
    q = ph.new_page(); hook(q); q.goto(URL + '#games'); q.wait_for_timeout(800)
    q.evaluate(f"Prog.d.rg = {json.dumps(pg.evaluate('Prog.d.rg'))}; Prog.d.rg.chk = Date.now(); S.gseg = 'last'; go('games')"); q.wait_for_timeout(700)
    assert q.evaluate('document.documentElement.scrollWidth') <= 390, 'no sideways scroll on a phone'
    q.screenshot(path=out + 'rv_phone.png', full_page=True)
    ph.close()
    b.close()
site.stop()
print('ERRORS:', errors)
assert not errors, errors
print('review checks passed')
