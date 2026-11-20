"""Marks on the moves, the names of the lines and your moves in order (over local HTTP, the website's page).

The other side's moves are marked by what they hand you (inaccuracy ?!, mistake ?, blunder ??), yours with one mark, the
key move (!): the answer that makes a mistake cost. Known positions first, then how many moves get a mark at all (a mark
on every other move would say nothing). In a lesson: the chip and its sentence on the move card, the badge on the board,
the icon in the list of moves and the legend under it, and no second chip that says the same in other words. The signs
are the ones players know, in colours close to the familiar ones but not the same, in both themes. In a drill and in a
Sandbox game the mark shows on the board with the move, with its word for a moment, and the sign beside the piece that
made the key move stays while the other side answers; a checkpoint shows none.

Names: the opening's name as a trail with the line's own name large, and in the lists of moves the name each move starts.

Your moves in order: the strip under a lesson's board, a picture for every move, the main line beside a line whose order
differs with the moves that changed places ringed in both rows, a tap on a move steps there, and the numbers on the
board. A drill names a move of the line that was played before its turn as an order slip. A phone in dark mode at the end."""
import re
from playwright.sync_api import sync_playwright
from e2e_white import launch, out, play_sandbox
from serve import Site

site = Site(docs=True); URL = site.start()
errors = []
AT = "(us => { let i = 0; for (const u of us.split(' ')){ i = (N[i].k || []).find(c => N[c].u === u); if (i === undefined) return null; } return i; })"
# colours a well-known review screen uses for its move marks: ours must be our own
THEIRS = {'#f7c631', '#ffa459', '#fa412d', '#ff7769', '#26c2a3', '#749bbf', '#81b64c', '#95b776', '#d5a47d', '#e58f2a', '#96bc4b', '#5c8bb0', '#1baca6', '#96af8b', '#f0c15c', '#e6912c', '#b33430', '#dbac16', '#56b4e9', '#e69f00', '#df5353', '#5b8bb0', '#ffa459'}


def hook(pg):
    pg.on('pageerror', lambda e: errors.append(f'pageerror: {e}'))
    pg.on('console', lambda m: errors.append(f'console {m.type}: {m.text}') if m.type == 'error' and 'ERR_' not in m.text else None)


def mark(pg, us):
    return pg.evaluate(f"(i => i == null ? 'not in the book' : markOf(i))({AT}('{us}'))")


with sync_playwright() as p:
    b = launch(p)
    pg = b.new_context(viewport={'width': 1280, 'height': 1000}).new_page(); hook(pg)
    pg.goto(URL + '#course'); pg.wait_for_timeout(900)

    # ---- known positions, White's book: what Black hands you, and your answer to it
    pg.evaluate("useSide('w')")
    FL = 'e2e4 e7e5 g1f3 b8c6 f1c4 g8f6 f3g5 d7d5 e4d5 f6d5'
    known_w = {'e2e4 g7g5': 'mistake', 'e2e4 e7e5 g1f3 f7f6': 'mistake', 'e2e4 e7e5 g1f3 f7f6 f3e5': 'key', FL: 'slip', FL + ' g5f7': 'key',
               'e2e4 e7e5 g1f3 d7d6': None, 'e2e4 c7c5': None, 'e2e4': None, 'e2e4 e7e5 g1f3': None}
    got = {us: mark(pg, us) for us in known_w}; print('white book:', got)
    assert got == known_w, got
    # a move of your own the book shows as one to avoid reads as a mistake, and a move the notes call a blunder is one
    # even where the game was won already (the share of the point barely moves there)
    own = pg.evaluate("(() => { const i = N.findIndex((n, k) => k && isMine(n) && (n.g || []).includes('warn') && (linesByNode.get(k) || []).length); return [markOf(i), markWords(i, markOf(i))]; })()")
    assert own == ['mistake', 'A move to avoid: it is here so you know why'], own
    told = pg.evaluate("N.map((n, k) => k && !isMine(n) && (n.g || []).includes('blunder') && (linesByNode.get(k) || []).length ? markOf(k) : 0).filter(Boolean)")
    assert told and set(told) == {'blunder'}, told
    mated = pg.evaluate("""(() => { const sg = ME === 1 ? 1 : -1, m = e => typeof e === 'string' && cpOf(e) * sg >= 2000;
        return N.map((n, k) => k && !isMine(n) && (linesByNode.get(k) || []).length && m(n.e) && N[n.p].e !== undefined && !m(N[n.p].e) ? markOf(k) : 0).filter(Boolean); })()""")
    print('moves that walk into a forced mate:', len(mated)); assert mated and set(mated) == {'blunder'}, mated

    # ---- Black's book: White's odd first moves are judged by the engine alone (the notes there carry no tags)
    pg.evaluate("useSide('b')")
    known_b = {'g2g4': 'mistake', 'f2f4': None, 'b2b4': None, 'e2e4 e7e5 e1e2': 'mistake', 'e2e4 e7e5 e1e2 g8f6': 'key', 'e2e4 e7e5 d1h5': 'slip',
               'e2e4 e7e5 d1h5 b8c6': None, 'e2e4 e7e5 g1f3 b8c6 f1c4 f8c5 c4f7': 'blunder', 'e2e4 e7e5': None}
    got = {us: mark(pg, us) for us in known_b}; print('black book:', got)
    assert got == known_b, got

    # ---- a mark is the exception in both books, every key move answers a marked move, and nothing is marked twice
    for side in ('w', 'b'):
        pg.evaluate(f"useSide('{side}')")
        c = pg.evaluate("""(() => { const used = new Set(); DATA.lines.forEach(l => LESSONS[l.lesson] && l.n.forEach(i => used.add(i))); const c = {me: 0, opp: 0, key: 0, opm: 0, orphan: 0, bad: 0};
            for (const i of used){ if (!i) continue; const k = markOf(i);
              if (isMine(N[i])){ c.me++; if (k === 'key'){ c.key++; if (!markOf(N[i].p)) c.orphan++; } else if (k && !(N[i].g || []).some(t => ['warn', 'blunder', 'mistake'].includes(t))) c.bad++; }
              else { c.opp++; if (k){ c.opm++; if (k === 'key') c.bad++; } } }
            return c; })()""")
        print(side, 'marks:', c)
        assert c['orphan'] == 0 and c['bad'] == 0, c
        assert .05 < c['opm'] / c['opp'] < .25 and .02 < c['key'] / c['me'] < .12, 'a mark has to stay the exception'

    # ---- in a lesson: Black's mistake, then your key move
    pg.evaluate("useSide('w')")
    lid, k = pg.evaluate(f"(i => {{ const id = (linesByNode.get(i) || []).find(x => LESSONS[LINES[x].lesson] && LINES[x].main) || linesByNode.get(i)[0]; return [id, LINES[id].n.indexOf(i)]; }})({AT}('e2e4 e7e5 g1f3 f7f6'))")
    pg.evaluate(f"openLine('{lid}', {k})"); pg.wait_for_timeout(500); pg.evaluate("Coach.hush()")
    card = ' '.join(pg.inner_text('.mcard').split()); print('the move card:', card[:200])
    chip = lambda page=pg: page.evaluate("(document.querySelector('.mcard .mkc') || {lastChild: {textContent: ''}}).lastChild.textContent.trim()")
    assert chip() == 'Mistake' and pg.text_content('.mcard .mkc svg text') == '?' and 'It hands you the better game' in pg.inner_text('.mcard .mkw')
    assert pg.locator('.mcard .chips .chip.mistake, .mcard .chips .chip.blunder, .mcard .chips .chip.key').count() == 0, 'the mark is said once'
    badge = pg.evaluate("(() => { const g = document.querySelector('#sb svg g.mkb'); return g && [g.getAttribute('class'), getComputedStyle(g.querySelector('circle')).fill]; })()")
    print('on the board:', badge); assert badge and 'mk-mistake' in badge[0]
    assert pg.locator('.thumb g.mkb').count() == 0, 'small boards carry no badge'
    icons = pg.evaluate("[document.querySelectorAll('.timeline .mki').length, LINES[S.line].n.filter((x, q) => q && markOf(x)).length, [...document.querySelectorAll('.mklegend span')].map(s => s.lastChild.textContent.trim()), [...document.querySelectorAll('.mklegend .mki text')].map(t => t.textContent)]")
    print('in the list of moves:', icons); assert icons[0] == icons[1] > 0 and icons[2] == ['Key move', 'Inaccuracy', 'Mistake', 'Blunder'] and icons[3] == ['!', '?!', '?', '??'], icons
    assert pg.evaluate("document.querySelector('.timeline .trow.cur .mki').getAttribute('aria-label')") == 'Mistake'
    pg.screenshot(path=out + 'mk_mistake.png')
    pg.keyboard.press('ArrowRight'); pg.wait_for_timeout(400)
    assert chip() == 'Key move' and pg.text_content('.mcard .mkc svg text') == '!' and pg.inner_text('.mcard .mkw').strip() == 'It makes the mistake cost'
    assert pg.evaluate("document.querySelector('#sb svg g.mkb').getAttribute('class')").endswith('mk-key')
    assert pg.locator('.mcard .chip.key').count() == 0 and 'key' in (pg.evaluate('N[LINES[S.line].n[S.i]].g') or []), 'the old Key move chip is gone: it sat on half the moves'
    pg.screenshot(path=out + 'mk_key.png')
    words = ' '.join(pg.inner_text('#view').split())
    assert not re.search(r'\b[a-h][1-8]\b', words.replace('f7', '').replace('f2', '')), 'no squares in the words'
    # a line with nothing to mark has no legend
    calm = pg.evaluate("DATA.lines.find(l => LESSONS[l.lesson] && !l.n.some((x, q) => q && markOf(x))).id")
    pg.evaluate(f"openLine('{calm}', 3)"); pg.wait_for_timeout(400)
    assert pg.locator('.mklegend').count() == 0 and pg.locator('.timeline .mki').count() == 0 and pg.locator('#sb svg g.mkb').count() == 0

    # ---- our own colours and shapes, in both themes
    def colours(page):
        return page.evaluate("['key', 'slip', 'mis', 'blun'].map(k => getComputedStyle(document.documentElement).getPropertyValue('--mk-' + k).trim().toLowerCase())")
    light = colours(pg); print('mark colours, light:', light)
    assert len(set(light)) == 4 and not set(light) & THEIRS, light
    assert pg.evaluate("MARK_SIGN") == {'key': '!', 'slip': '?!', 'mistake': '?', 'blunder': '??'}, 'the signs players know'
    # close to the familiar colours: a blue, a yellow, an orange and a red, in that order
    hue = pg.evaluate("""['key', 'slip', 'mis', 'blun'].map(k => { const c = getComputedStyle(document.documentElement).getPropertyValue('--mk-' + k).trim(), r = parseInt(c.slice(1, 3), 16) / 255, g = parseInt(c.slice(3, 5), 16) / 255, b = parseInt(c.slice(5, 7), 16) / 255, mx = Math.max(r, g, b), mn = Math.min(r, g, b), d = mx - mn;
        return Math.round(((mx === r ? ((g - b) / d) % 6 : mx === g ? (b - r) / d + 2 : (r - g) / d + 4) * 60 + 360) % 360); })""")
    print('hues:', hue); assert 195 <= hue[0] <= 225 and 38 <= hue[1] <= 55 and 15 <= hue[2] <= 35 and (hue[3] <= 10 or hue[3] >= 350), hue

    # ---- a drill: the mark comes onto the board with the move. Black's mistake carries its sign and, for a moment, its
    #      word; your key move gets the ! beside the piece, and it stays there while Black answers
    pg.evaluate(f"startDrillLine('{lid}', '', null, {{from0: true}})"); pg.wait_for_timeout(600)
    seen = {'opp': None, 'key': None, 'kept': [], 'pending': None}
    for _ in range(80):
        st = pg.evaluate("""({s: S.drill.state, b: S.drill.busy, at: S.drill.i, mk: markOf(LINES[S.drill.id].n[S.drill.i]),
            board: [...document.querySelectorAll('#db g.mkb')].map(g => g.getAttribute('class').split(' ').pop()), word: [...document.querySelectorAll('#db g.mkl text')].map(t => t.textContent),
            chips: [...document.querySelectorAll('#dpanel .mkc')].map(c => c.lastChild.textContent.trim())})""")
        if st['s'] == 'done': break
        if st['b']: pg.wait_for_timeout(120); continue
        if st['mk'] == 'mistake' and not seen['opp']: seen['opp'] = st
        if seen['pending'] is not None:                              # Black has answered a key move: is its sign still up?
            n = pg.evaluate("LINES[S.drill.id].n"); mine, reply = pg.evaluate(f"[N[{n[seen['pending']]}].u.slice(2, 4), N[{n[st['at']]}].u.slice(2, 4)]")
            seen['kept'].append([mine != reply, 'mk-key' in st['board']]); seen['pending'] = None
        nxt = pg.evaluate("markOf(LINES[S.drill.id].n[S.drill.i + 1])")
        pg.evaluate("(u => tryMove(u.slice(0, 2), u.slice(2, 4)))(expectedMove()[0])")
        if nxt == 'key': seen['pending'] = st['at'] + 1
        if nxt == 'key' and not seen['key']:
            seen['key'] = pg.evaluate("""({board: [...document.querySelectorAll('#db g.mkb')].map(g => g.getAttribute('class').split(' ').pop()), word: [...document.querySelectorAll('#db g.mkl text')].map(t => t.textContent),
                chips: [...document.querySelectorAll('#dpanel .mfeed .mkc')].map(c => c.lastChild.textContent.trim())})""")
        pg.wait_for_timeout(250)
    print('Black\'s mistake on the board:', seen['opp'] and [seen['opp']['board'], seen['opp']['word'], seen['opp']['chips']])
    assert seen['opp'] and seen['opp']['board'][-1] == 'mk-mistake' and seen['opp']['word'][-1] == 'Mistake' and 'Mistake' in seen['opp']['chips']
    print('your key move:', seen['key'], '| after Black\'s answers [piece still there, sign still up]:', seen['kept'])
    assert seen['key'] and seen['key']['board'][-1] == 'mk-key' and seen['key']['word'][-1] == 'Key move' and seen['key']['chips'] == ['Key move']
    assert seen['kept'] and all(a == b for a, b in seen['kept']) and any(a for a, b in seen['kept']), 'the sign beside the piece that made the key move stays while the other side answers, unless that piece was just taken'
    # a piece picked up draws the board again: the signs stay, the word has gone
    pg.evaluate(f"startDrillLine('{lid}', '', null, {{from0: true}})"); pg.wait_for_timeout(400)
    for _ in range(40):
        st = pg.evaluate("({b: S.drill.busy, mk: markOf(LINES[S.drill.id].n[S.drill.i])})")
        if not st['b'] and st['mk'] == 'mistake': break
        if not st['b']: pg.evaluate("(u => tryMove(u.slice(0, 2), u.slice(2, 4)))(expectedMove()[0])")
        pg.wait_for_timeout(150)
    assert pg.locator('#db g.mkl').count() == 1
    pg.evaluate("renderDrillBoard()"); assert pg.locator('#db g.mkl').count() == 0 and pg.locator('#db g.mkb').count() >= 1
    # a checkpoint shows no marks: there the position is the question
    pg.evaluate("S.drill = S.drillState = null; startQuiz(COURSE.find(U => U.side === 'w' && U.quiz && U.quiz.length).id)"); pg.wait_for_timeout(700)
    assert pg.evaluate("S.view") == 'quiz' and pg.locator('#db g.mkb, #db g.mkl').count() == 0, 'no marks in a checkpoint'

    # ---- a Sandbox game: the same on the board, the other side's card says it, and the list is marked as the game goes
    pg.evaluate("S.quizState = null; useSide('w'); go('sandbox')"); pg.wait_for_timeout(400)
    pick = pg.evaluate("""(() => { for (const l of Object.values(LINES)){ if (!LESSONS[l.lesson] || !DRILLABLE.includes(l.id)) continue;
        const q = l.n.findIndex((x, i) => i > 2 && !isMine(N[x]) && ['mistake', 'blunder'].includes(markOf(x))); if (q < 0) continue;
        let k = l.n.length - 1; while (k > 2 && sbBookKids(l.n[k - 1]).length === 1) k--;
        if (k < q && k < l.n.length - 3 && sbCanFrom(l.n[k])) return {line: l.id, at: l.n[k], marks: l.n.filter((x, i) => i > k && markOf(x)).length}; } return null; })()""")
    print('a Sandbox game with a mistake in it:', pick); assert pick and pick['marks'] >= 2
    pg.evaluate(f"sbSetFrom('w', {pick['at']}); sbStart()"); pg.wait_for_timeout(1500)
    live = {'board': 0, 'list': 0, 'card': 0, 'keyword': 0}
    for _ in range(80):
        st = pg.evaluate("""({s: S.drill.state, busy: S.drill.busy, mine: myTurnAt(S.drill.node), board: document.querySelectorAll('#db g.mkb').length, list: document.querySelectorAll('#sbfeed .mki').length,
            card: document.querySelectorAll('#sbpanel .mcard .mkc').length, kw: [...document.querySelectorAll('#db g.mkl text')].some(t => t.textContent === 'Key move')})""")
        if st['s'] == 'done': break
        for kk, v in (('board', st['board']), ('list', st['list']), ('card', st['card']), ('keyword', int(st['kw']))): live[kk] = max(live[kk], v)
        if st['busy'] or not st['mine']: pg.wait_for_timeout(120); continue
        pg.evaluate("(u => tryMove(u.slice(0, 2), u.slice(2, 4)))(expectedMove()[0])"); pg.wait_for_timeout(120)
    print('while the game was on:', live)
    assert pg.evaluate("S.drill.state") == 'done' and live['board'] >= 1 and live['list'] >= 1 and live['card'] >= 1 and live['keyword'] == 1, live
    after = pg.evaluate("[document.querySelectorAll('#sbpanel .mki').length, [...document.querySelectorAll('#sbfeed .mki')].map(e => e.getAttribute('aria-label'))]")
    print('once it is over:', after); assert len(after[1]) >= pick['marks'] and 'Key move' in after[1], after
    assert pg.locator('#sbpanel .mklegend').count() == 1, 'with the legend under the list'
    pg.screenshot(path=out + 'mk_sandbox.png')

    # ---- the names: the family and the variations as a trail, the line's own name large, and the list of moves says
    #      where each name starts
    nm = pg.evaluate("[Openings.ofNode(S.drill.node), [...document.querySelectorAll('#sbpanel .opn .otrail')].map(e => e.innerText), document.querySelector('#sbpanel .opn .oname').innerText, parseFloat(getComputedStyle(document.querySelector('#sbpanel .opn .oname')).fontSize)]")
    print('the name on the panel:', nm)
    parts = pg.evaluate(f"nameParts({nm[0]!r})"); assert nm[2] == parts[-1] and nm[3] >= 22 and (len(parts) == 1 or parts[0].upper() in nm[1][0].upper()), nm
    tags = pg.evaluate("[document.querySelectorAll('#sbfeed .ntag').length, document.querySelectorAll('#sbfeed .named').length]"); print('names in the list of moves:', tags); assert sum(tags) >= 2
    assert pg.evaluate("nameParts('Italian Game: Two Knights Defense, Fried Liver Attack')") == ['Italian Game', 'Two Knights Defense', 'Fried Liver Attack'] and pg.evaluate("nameParts('Queen\\'s Pawn Game')") == ["Queen's Pawn Game"]

    # ---- your moves in order
    pg.evaluate("sbSetFrom(null); S.drill = S.sbState = null; useSide('b')")
    main = pg.evaluate("DATA.lines.find(l => l.lesson === CHAPTERS.slav.first && l.main).id")
    pg.evaluate(f"openLine('{main}', 4)"); pg.wait_for_timeout(500); pg.evaluate("Coach.hush()")
    strip = ' '.join(pg.inner_text('.ostrip').split()); print('the main line:', strip[:140])
    assert 'This is the order to know for this opening' in strip and pg.locator('.otoks.ref').count() == 0
    n_mine = pg.evaluate("myMoves(LINES[S.line]).length")
    assert pg.locator('.otoks button.otok').count() == n_mine and pg.locator('.otoks .omap').count() == n_mine, 'a picture for every move of yours'
    assert pg.locator('.otok.cur').count() == 1 and pg.locator('.otok.done').count() == 1, 'two of your moves made, the second one current'
    pg.locator('.otoks button.otok').nth(4).click(); pg.wait_for_timeout(300)
    assert pg.evaluate("[S.i, isMine(N[LINES[S.line].n[S.i]]), myMoves(LINES[S.line])[4].k]") == [pg.evaluate('S.i'), True, pg.evaluate('S.i')], 'a tap on a move steps there'
    # the numbers on the board: every piece of yours that has moved carries the number of its last move
    assert pg.locator('#sb g.onum').count() == 0
    pg.click('#cNums'); pg.wait_for_timeout(300)
    nums = pg.evaluate("[[...document.querySelectorAll('#sb g.onum text')].map(t => +t.textContent).sort((a, b) => a - b), orderNums(LINES[S.line], S.i).map(x => x[1]).sort((a, b) => a - b), document.getElementById('cNums').getAttribute('aria-pressed')]")
    print('numbers on the board:', nums); assert nums[0] == nums[1] and len(nums[0]) >= 4 and max(nums[0]) == 5 and nums[2] == 'true', nums
    # a line whose order differs: the main line beside it, the move that changed places ringed in both rows
    swap = pg.evaluate("DATA.lines.find(l => LESSONS[l.lesson] && chapterOf(LESSONS[l.lesson]).id === 'slav' && orderOf(l).diff.length === 1 && orderOf(l).diff[0].odd === 'swap').id")
    pg.evaluate(f"openLine('{swap}', LINES['{swap}'].n.length - 1)"); pg.wait_for_timeout(500); pg.evaluate("Coach.hush()")
    strip = ' '.join(pg.inner_text('.ostrip').split()); print('a line in another order:', strip[:200])
    assert 'THE MAIN LINE' in strip.upper() and 'THIS LINE' in strip.upper() and re.search(r'comes (later|earlier) than in the main line', strip), strip
    odd = pg.evaluate("[[...document.querySelectorAll('.otoks.ref .otok.odd')].map(e => e.title), [...document.querySelectorAll('.otoks:not(.ref) .otok.odd')].map(e => e.title), orderOf(LINES[S.line]).diff.map(m => m.nd.l)]")
    print('ringed in both rows:', odd); assert len(odd[1]) == 1 and odd[1] == odd[2] and len(odd[0]) == 1, odd
    assert pg.evaluate("(() => { const a = document.querySelector('.otoks.ref .otok.odd .omap').innerHTML, b = document.querySelector('.otoks:not(.ref) .otok.odd .omap').innerHTML; return a === b; })()"), 'the same move, the same picture'
    assert pg.locator('.otoks.ref button').count() == 0, 'the main line is there to look at, not to tap'
    pg.locator('.ostrip').screenshot(path=out + 'mk_order.png'); pg.screenshot(path=out + 'mk_lesson.png', full_page=True)
    # a game review has no strip (it isn't a line to learn in order), and the numbers stay off there
    g = pg.evaluate("DATA.games[0].id"); pg.evaluate(f"openLine('{g}', 6)"); pg.wait_for_timeout(400)
    assert pg.locator('.ostrip').count() == 0 and pg.locator('#sb g.onum').count() == 0

    # ---- a drill: a move of the line played before its turn is named as that (the order slipped, not the move), without
    #      saying which move is due; the second miss shows the arrow as always, and the coach's note says it again
    pg.evaluate(f"useSide('b'); startDrillLine('{main}', '', null, {{from0: true}})"); pg.wait_for_timeout(1500)
    for _ in range(30):
        if not pg.evaluate('S.drill.busy'): break
        pg.wait_for_timeout(150)
    early = pg.evaluate("""(() => { const D = S.drill, n = LINES[D.id].n, legal = legalFor(), exp = expectedMove()[0]; let c = 0;
        for (let k = D.i + 2; k < n.length; k++){ if (!isMine(N[n[k]])) continue; c++; if (N[n[k]].u !== exp && legal.includes(N[n[k]].u)) return [N[n[k]].u, c, exp]; } return null; })()""")
    print('a later move of the line that is legal now:', early); assert early
    pg.evaluate(f"tryMove('{early[0][:2]}', '{early[0][2:4]}')"); pg.wait_for_timeout(300)
    msg = ' '.join(pg.inner_text('#dpanel .feedback').split()); print('  played early:', msg[:150])
    words = ['', 'one move', 'two moves', 'three moves', 'four moves', 'five moves', 'six moves']
    assert 'The right move at the wrong moment' in msg and f'it comes {words[early[1]]} later' in msg and pg.evaluate('S.drill.hint') is None, msg
    assert pg.evaluate("S.drill.slipOrd && Object.values(S.drill.slipOrd)[0]") == early[1]
    other = pg.evaluate(f"legalFor().find(u => u !== '{early[2]}' && !laterInLine(S.drill, u))")
    pg.evaluate(f"tryMove('{other[:2]}', '{other[2:4]}')"); pg.wait_for_timeout(300)
    msg = ' '.join(pg.inner_text('#dpanel .feedback').split())
    assert 'The arrow shows the move' in msg and 'The right move at the wrong moment' not in msg and pg.evaluate('S.drill.hint') == early[2], msg
    for _ in range(80):
        st = pg.evaluate("({s: S.drill.state, b: S.drill.busy})")
        if st['s'] == 'done': break
        if st['b']: pg.wait_for_timeout(200); continue
        pg.evaluate("(u => tryMove(u.slice(0, 2), u.slice(2, 4)))(expectedMove()[0])"); pg.wait_for_timeout(300)
    note = ' '.join(pg.inner_text('.coachnote').split()); print('  the coach afterwards:', note[:220])
    assert 'the order slipped, not the move' in note and 'See the order' in note, note
    pg.click('.coachnote [data-line]'); pg.wait_for_timeout(500)
    assert pg.evaluate("[S.view, S.line]") == ['study', main] and pg.locator('.ostrip').count() == 1 and pg.evaluate("N[LINES[S.line].n[S.i]].u") == early[2], 'See the order opens the lesson at the move that was due'
    assert pg.locator('.ccol .opn .oname').count() == 1 and pg.locator('.timeline .ntag, .timeline .named').count() >= 1, 'the lesson names its line too'

    # ---- a phone in dark mode
    ph = b.new_context(viewport={'width': 390, 'height': 844}, color_scheme='dark'); q = ph.new_page(); hook(q)
    q.goto(URL + '#course'); q.wait_for_timeout(800)
    q.evaluate(f"useSide('b'); S.onums = true; openLine('{swap}', LINES['{swap}'].n.length - 1)"); q.wait_for_timeout(600); q.evaluate("Coach.hush()")
    assert q.evaluate('document.documentElement.scrollWidth') <= 390, 'no sideways scroll on a phone'
    assert q.evaluate("document.querySelector('.ostrip').getBoundingClientRect().right") <= 390
    dark = colours(q); print('mark colours, dark:', dark)
    assert len(set(dark)) == 4 and not set(dark) & THEIRS and not set(dark) & set(light), 'the dark theme has its own'
    q.screenshot(path=out + 'mk_phone.png', full_page=True)
    q.evaluate(f"useSide('w'); openLine('{lid}', {k})"); q.wait_for_timeout(500)
    assert q.evaluate('document.documentElement.scrollWidth') <= 390 and q.locator('.mcard .mkc').count() == 1
    ph.close(); b.close()
site.stop()
print('ERRORS:', errors)
assert not errors, errors
print('marks checks passed')
