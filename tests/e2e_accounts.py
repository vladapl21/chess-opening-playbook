"""End-to-end checks for accounts and synced progress on the site build.

The page is served from https://app.test/ with a fake Supabase (tests/fake_supabase.js) whose server lives in this
script, so two browser contexts act like two devices sharing one account."""
import json, secrets, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'pipeline'))
from assemble import site_html, SUPABASE_JS  # noqa: E402
from e2e_white import launch, out  # noqa: E402

APP = 'https://app.test/'
SITE = {'supabaseUrl': 'https://app.test/sb', 'supabaseKey': 'sb_publishable_test', 'home': APP}
BODY = (ROOT / 'data' / 'build' / 'playbook.html').read_text()
PAGE, PLAIN = site_html(BODY, SITE), site_html(BODY, None)
FAKE_JS = (ROOT / 'tests' / 'fake_supabase.js').read_text()
errors = []


class Server:
    """Just enough of Supabase: users, sessions, email links, and one progress row per user behind row-level security."""
    def __init__(self):
        self.users, self.tokens, self.codes, self.rows = {}, {}, {}, {}
        self.confirm = False; self.down = False; self.mail = []

    def session(self, u):
        t = secrets.token_hex(8); self.tokens[t] = u['id']
        return {'access_token': t, 'user': self.public(u)}

    def public(self, u):
        return {'id': u['id'], 'email': u['email'], 'user_metadata': u.get('meta', {}), 'app_metadata': u.get('app', {})}

    def handle(self, path, b):
        uid = self.tokens.get(b.get('token'))
        if path == 'signup':
            if b['email'] in self.users: return {'error': {'message': 'User already registered'}}
            u = self.users[b['email']] = {'id': 'u-' + secrets.token_hex(4), 'email': b['email'], 'password': b['password'], 'confirmed': not self.confirm, 'meta': b.get('data') or {}}
            if self.confirm:
                c = secrets.token_hex(6); self.codes[c] = u['email']; self.mail.append(('confirm', u['email'], c))
                return {'user': {'id': u['id'], 'email': u['email']}, 'session': None}
            return {'user': {'id': u['id'], 'email': u['email']}, 'session': self.session(u)}
        if path == 'signin':
            u = self.users.get(b['email'])
            if not u or u['password'] != b['password']: return {'error': {'message': 'Invalid login credentials'}}
            if not u['confirmed']: return {'error': {'message': 'Email not confirmed'}}
            return {'session': self.session(u)}
        if path == 'exchange':
            email = self.codes.pop(b['code'], None)
            if not email: return {'error': {'message': 'invalid flow state'}}
            u = self.users[email]; u['confirmed'] = True
            return {'session': self.session(u)}
        if path == 'reset':
            if b['email'] in self.users: c = secrets.token_hex(6); self.codes[c] = b['email']; self.mail.append(('reset', b['email'], c))
            return {}
        if path == 'update':
            if not uid: return {'error': {'message': 'Auth session missing!'}}
            next(u for u in self.users.values() if u['id'] == uid)['password'] = b['password']
            return {}
        if path == 'user':
            if not uid: return {'error': {'message': 'Auth session missing!'}}
            return {'user': self.public(next(u for u in self.users.values() if u['id'] == uid))}
        if self.down: return {'error': {'message': 'Failed to fetch'}}
        if path == 'select':
            if not uid or b['filters'].get('user_id') != uid: return {'row': None}
            row = self.rows.get(uid)
            return {'row': {'data': row['data']} if row else None}
        if path == 'upsert':
            if not uid or b['row'].get('user_id') != uid: return {'error': {'message': 'new row violates row-level security policy for table "progress"'}}
            self.rows[uid] = b['row']
            return {}
        return {'error': {'message': 'unknown call ' + path}}


S = Server()


def wire(ctx, page=PAGE):
    def app(route):
        url = route.request.url
        if '/sb/__fake/' in url:
            route.fulfill(status=200, content_type='application/json', body=json.dumps(S.handle(url.rsplit('/', 1)[1], json.loads(route.request.post_data or '{}'))))
        else:
            route.fulfill(status=200, content_type='text/html', body=page)
    ctx.route('https://app.test/**', app)
    ctx.route(SUPABASE_JS, lambda r: r.fulfill(status=200, content_type='application/javascript', body=FAKE_JS))
    ctx.route('https://fonts.googleapis.com/**', lambda r: r.abort())


def hook(pg, name):
    pg.on('pageerror', lambda e: errors.append(f'{name} pageerror: {e}'))
    pg.on('console', lambda m: errors.append(f'{name} console: {m.text}') if m.type == 'error' and 'ERR_' not in m.text and 'net::' not in m.text else None)


def sheet(pg, mode, email=None, password=None):
    """Fill and submit the account sheet in the given mode."""
    if pg.locator('#acctSheet').is_hidden(): pg.click('#acctBtn'); pg.wait_for_timeout(150)
    if mode == 'forgot' and pg.evaluate('Acct.mode') == 'signup': pg.click('#acctPanel [data-mode="signin"]'); pg.wait_for_timeout(100)
    if mode != pg.evaluate('Acct.mode'): pg.click(f'#acctPanel [data-mode="{mode}"]'); pg.wait_for_timeout(100)
    if email is not None: pg.fill('#acctPanel input[name=email]', email)
    if password is not None: pg.fill('#acctPanel input[name=password]', password)
    pg.click('#acctPanel button[type=submit]'); pg.wait_for_timeout(500)


def synced(pg):
    for _ in range(60):
        try:
            if pg.evaluate("!!Cloud.user && Cloud.state === 'ok' && !Cloud.writing && !Cloud.pulling"): return True
        except Exception as e:                      # the page is loading again (a new account opens on its own playbook)
            if 'navigation' not in str(e) and 'context' not in str(e) and 'is not defined' not in str(e): raise
        pg.wait_for_timeout(150)
    return False


with sync_playwright() as p:
    b = launch(p)
    A = b.new_context(viewport={'width': 1280, 'height': 860}); wire(A)
    a = A.new_page(); hook(a, 'A')
    a.goto(APP + '#course'); a.wait_for_timeout(900)
    assert a.locator('#acctBtn').is_visible() and a.inner_text('#acctBtn') == 'Sign in'
    assert a.locator('#nudge').is_visible(), 'nudge'

    # ---- progress made before there is an account comes along into the new account
    a.evaluate("openUnit('w-italian')"); a.wait_for_timeout(300)
    for _ in range(3): a.keyboard.press('ArrowRight'); a.wait_for_timeout(80)
    assert a.evaluate("!!up('w-italian').idea")
    a.click('.tabs button[data-view="course"]'); a.wait_for_timeout(300)
    assert a.locator('#nudge [data-nudge="signin"]').is_visible(), 'a new device can also sign in from the banner'
    a.click('#nudge [data-nudge="signup"]'); a.wait_for_timeout(200)
    assert a.evaluate('Acct.mode') == 'signup'
    a.screenshot(path=out + 'acct_signup.png')
    sheet(a, 'signup', 'vlad@example.com', 'short')
    assert a.evaluate('Acct.mode') == 'signup', 'browser should refuse a short password'
    sheet(a, 'signup', 'vlad@example.com', 'correct horse')
    assert synced(a), a.evaluate('[Cloud.state, Cloud.err]')
    uid = a.evaluate('Cloud.user.id'); row = S.rows[uid]['data']
    print('signed up:', uid, '| button:', a.inner_text('#acctBtn').replace('\n', ' '), '| toast:', a.inner_text('#toast'))
    assert row['course']['u']['w-italian']['idea'] and row['owner'] == uid
    assert a.locator('#nudge').is_hidden()

    # ---- a second device signs in and gets it; its own progress flows back
    B = b.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True); wire(B)
    bp = B.new_page(); hook(bp, 'B')
    bp.goto(APP); bp.wait_for_timeout(900)
    assert not bp.evaluate("!!up('w-italian').idea")
    assert bp.evaluate('document.documentElement.scrollWidth') <= 390
    bp.screenshot(path=out + 'acct_phone_nudge_new.png')
    sheet(bp, 'signin', 'vlad@example.com', 'wrong password')
    print('wrong password ->', bp.inner_text('#acctPanel .formmsg'))
    assert 'Invalid login' in bp.inner_text('#acctPanel .formmsg')
    sheet(bp, 'signin', 'vlad@example.com', 'correct horse')
    assert synced(bp) and bp.evaluate("!!up('w-italian').idea"), 'pulled progress on device B'
    bp.evaluate("markSeen('center')"); bp.wait_for_timeout(1800)
    assert S.rows[uid]['data']['course']['seen'].get('center'), 'device B pushed'
    a.evaluate("document.dispatchEvent(new Event('visibilitychange'))"); a.wait_for_timeout(800)
    assert a.evaluate("lessonSeen('w', 'center')"), 'device A picked up device B progress on return'
    bp.click('#acctBtn'); bp.wait_for_timeout(200)
    bp.screenshot(path=out + 'acct_phone_account.png')
    assert bp.locator('#acctPanel .bdg').count() > 10 and bp.locator('#acctPanel [data-mail]').count() == 1, 'the profile: badges and the reminder switch'
    assert bp.evaluate('document.getElementById("acctPanel").scrollWidth <= document.getElementById("acctPanel").clientWidth + 1')
    bp.click('#acctPanel [data-act="close"]')

    # ---- the coach, the look and the reminder choice follow the account to the other device
    a.evaluate("setSetting('who', 'rook'); setSetting('board', 'wood'); setSetting('nums', false); setSetting('animk', 'arcade'); setSetting('snd', false)"); a.click('#acctBtn'); a.wait_for_timeout(200)
    assert a.get_attribute('#acctPanel [data-mail]', 'aria-checked') == 'false'
    a.click('#acctPanel [data-mail]'); a.wait_for_timeout(200); assert a.get_attribute('#acctPanel [data-mail]', 'aria-checked') == 'true'
    a.click('#acctPanel [data-act="close"]'); a.wait_for_timeout(1800)
    row = S.rows[uid]['data']; assert row['set']['who'] == 'rook' and row['set']['board'] == 'wood' and row['mail']['on'] is True, (row.get('set'), row.get('mail'))
    bp.evaluate("document.dispatchEvent(new Event('visibilitychange'))"); bp.wait_for_timeout(900)
    got = bp.evaluate("[SET.who, SET.board, document.documentElement.dataset.board, coachName(), !!(Prog.d.mail && Prog.d.mail.on), SET.nums, SET.animk, SET.snd]"); print('device B after a pull:', got)
    assert got == ['rook', 'wood', 'wood', 'Rocco', True, False, 'arcade', False], (got, 'the move numbers, the animation and the sounds are settings like the others')
    bp.evaluate("setSetting('who', 'pawn')"); bp.wait_for_timeout(1800)
    a.evaluate("document.dispatchEvent(new Event('visibilitychange'))"); a.wait_for_timeout(900)
    assert a.evaluate("[SET.who, SET.board]") == ['pawn', 'wood'], 'the newer change wins, the rest stays'
    assert a.evaluate("mergeProg({set: {who: 'rook', t: 5}}, {set: {who: 'pawn', t: 3}}).set.who") == 'rook'

    # ---- setting by setting: a board changed on B never undoes a coach picked on A, even with both pages open
    # (the two saves can cross on the way to the account; the next pull on each side puts both changes together)
    a.evaluate("setSetting('who', 'rook')"); bp.evaluate("setSetting('board', 'plum')"); a.wait_for_timeout(1800)
    for pg in (a, bp): pg.evaluate("document.dispatchEvent(new Event('visibilitychange'))"); pg.wait_for_timeout(300)
    for pg in (a, bp):
        pg.evaluate("document.dispatchEvent(new Event('visibilitychange'))")
        pg.wait_for_function("SET.who === 'rook' && SET.board === 'plum'", timeout=8000)
    # the streak, badges, worn coach items and the level last celebrated travel too
    bp.evaluate("Prog.d.days = Object.assign(Prog.d.days || {}, {[dayKey(-1)]: ['a', 'b', 'c', 'd', 'e']}); Prog.d.shop = {own: {cap: Date.now()}, wear: {head: ['cap', Date.now()]}}; Prog.d.lvl = 7; Prog.save()"); bp.wait_for_timeout(1800)
    a.evaluate("document.dispatchEvent(new Event('visibilitychange'))"); a.wait_for_timeout(900)
    assert a.evaluate("[Daily.n(dayKey(-1)), Prog.d.shop.wear.head[0], !!Prog.d.shop.own.cap, Prog.d.lvl]") == [5, 'cap', True, 7]
    a.evaluate("Prog.d.lvl = 3; Prog.save()"); a.wait_for_timeout(1800)
    assert S.rows[uid]['data']['lvl'] == 7 and a.evaluate('Prog.d.lvl') == 7, 'the highest level celebrated wins'
    # monthly recaps: each month's newest summary, the last check and the last month opened
    bp.evaluate("Prog.d.recap = {m: {'2026-10': {a: 'chess.com:aqua_alpaca', at: 5, fin: true, all: [40, 24, 15, 1]}, '2026-09': {a: 'chess.com:aqua_alpaca', at: 9, fin: true, all: [30, 17, 13, 0]}}, chk: 9, seen: '2026-09'}; Prog.save()"); bp.wait_for_timeout(1800)
    a.evaluate("document.dispatchEvent(new Event('visibilitychange'))"); a.wait_for_timeout(900)
    assert a.evaluate("[Prog.d.recap.m['2026-10'].all[0], Prog.d.recap.chk, Prog.d.recap.seen]") == [40, 9, '2026-09']
    a.evaluate("Prog.d.recap.m['2026-10'] = {a: 'chess.com:aqua_alpaca', at: 7, fin: true, all: [41, 25, 15, 1]}; Prog.d.recap.m['2026-09'].at = 1; Prog.d.recap.m['2026-09'].all = [1, 0, 1, 0]; Prog.d.recap.seen = '2026-10'; Prog.save()"); a.wait_for_timeout(1800)
    r = S.rows[uid]['data']['recap']; print('recap after both:', {k: v['all'][0] for k, v in r['m'].items()}, r['seen'])
    assert r['m']['2026-10']['all'][0] == 41 and r['m']['2026-09']['all'][0] == 30 and r['seen'] == '2026-10' and r['chk'] == 9, 'the newer copy of each month wins'
    # finishing the course is stamped once (the earliest stamp wins); deep dive parts travel like any unit
    bp.evaluate("const c = Prog.d.course || (Prog.d.course = {u: {}, seen: {}}); c.u = c.u || {}; c.grad = 1700000000000; c.u['x-w-italian-1'] = {o: Date.now(), cp: 4}; Prog.save()"); bp.wait_for_timeout(1800)
    a.evaluate("document.dispatchEvent(new Event('visibilitychange'))"); a.wait_for_timeout(900)
    assert a.evaluate("[Prog.d.course.grad, Prog.d.course.u['x-w-italian-1'].cp]") == [1700000000000, 4]
    a.evaluate("Prog.d.course.grad = 1800000000000; Prog.save()"); a.wait_for_timeout(1800)
    assert S.rows[uid]['data']['course']['grad'] == 1700000000000 and a.evaluate("Prog.d.course.grad") == 1700000000000
    # the tour, taken on one device, is taken on every device (the earliest time wins)
    bp.evaluate("Prog.d.tour = {done: 1750000000000}; Prog.save()"); bp.wait_for_timeout(1800)
    a.evaluate("document.dispatchEvent(new Event('visibilitychange'))"); a.wait_for_timeout(900)
    assert a.evaluate("Prog.d.tour && Prog.d.tour.done") == 1750000000000
    a.evaluate("Prog.d.tour = {done: 1760000000000}; Prog.save()"); a.wait_for_timeout(1800)
    assert S.rows[uid]['data']['tour']['done'] == 1750000000000 and a.evaluate("Prog.d.tour.done") == 1750000000000
    # the last three games' reviews: per game, the newest three kept, what each device worked out and drilled kept too
    bp.evaluate("Prog.d.rg = {g: [{id: 'g1', t: 1700000001000, added: 1700000001000, src: 'acct', me: 'w', opp: 'one', oe: 900, r: 0, url: '', u: ['e2e4', 'e7e5', 'g1f3', 'b8c6', 'f1c4', 'g8f6', 'f3e5'], at: 6, by: 'me', w: 0}, {id: 'g2', t: 1700000002000, added: 1700000002000, src: 'acct', me: 'w', opp: 'two', oe: 900, r: 0, url: '', u: ['e2e4', 'e7e5', 'g1f3', 'b8c6', 'f1c4', 'g8f6', 'f3e5'], at: 6, by: 'me', w: 0}], chk: 5}; Prog.save()"); bp.wait_for_timeout(1800)
    a.evaluate("document.dispatchEvent(new Event('visibilitychange'))"); a.wait_for_timeout(900)
    assert a.evaluate("Review.list().map(R => R.opp)") == ['two', 'one']
    a.evaluate("Review.get('g1').mk = 0; Review.get('g2').d = {o: [1, 1, 9]}; Prog.d.rg.g.push({id: 'g3', t: 1700000003000, added: 1700000003000, src: 'acct', me: 'w', opp: 'three', oe: 900, r: 0, url: '', u: ['e2e4', 'e7e5', 'g1f3', 'b8c6', 'f1c4', 'g8f6', 'f3e5'], at: 6, by: 'me', w: 0}, {id: 'g4', t: 1700000004000, added: 1700000004000, src: 'acct', me: 'w', opp: 'four', oe: 900, r: 0, url: '', u: ['e2e4', 'e7e5', 'g1f3', 'b8c6', 'f1c4', 'g8f6', 'f3e5'], at: 6, by: 'me', w: 0}); Prog.save()"); a.wait_for_timeout(1800)
    bp.evaluate("document.dispatchEvent(new Event('visibilitychange'))"); bp.wait_for_timeout(900)
    got = bp.evaluate("Review.list().map(R => [R.opp, R.mk, R.d ? R.d.o : null])"); print('reviews on the other device:', got)
    assert got == [['four', None, None], ['three', None, None], ['two', None, [1, 1, 9]]] and len(S.rows[uid]['data']['rg']['g']) == 3, got
    # a page from an older version writes a smaller copy: the next save on any device writes everything back
    row = S.rows[uid]['data']; S.rows[uid]['data'] = {k: v for k, v in row.items() if k not in ('days', 'prefs', 'set', 'shop', 'badges', 'lvl', 'recap', 'tour', 'rg')}
    a.evaluate("Prog.save()"); a.wait_for_timeout(1800)
    row = S.rows[uid]['data']; print('after an older copy and one save:', sorted(row.keys()))
    assert all(k in row for k in ('days', 'prefs', 'shop', 'badges', 'lvl', 'recap', 'tour', 'rg')) and row['prefs']['who'][0] == 'rook' and row['prefs']['board'][0] == 'plum'

    # ---- the account copy can't be reached: the app says so, keeps working, and catches up later
    S.down = True
    a.evaluate("markSeen('grab')"); a.wait_for_timeout(1800)
    assert a.evaluate('Cloud.state') == 'err' and 'Not saved' in a.inner_text('#acctBtn')
    a.click('#acctBtn'); a.wait_for_timeout(200)
    print('offline line:', a.inner_text('#acctPanel .syncline'))
    S.down = False
    a.click('#acctPanel [data-act="sync"]'); a.wait_for_timeout(700)
    assert a.evaluate('Cloud.state') == 'ok' and S.rows[uid]['data']['course']['seen'].get('grab')

    # ---- signing out keeps the device's progress; another account on the same device starts from its own
    a.click('#acctPanel [data-act="signout"]'); a.wait_for_timeout(300)
    assert a.inner_text('#acctBtn') == 'Sign in' and a.evaluate("lessonSeen('w', 'grab')")
    # the first-try bug: after signing out, the button opened "make an account" and signing in was hard to find
    assert a.locator('#nudge').is_visible() and 'signed out' in a.inner_text('#nudge'), a.inner_text('#nudge')
    assert a.locator('#nudge [data-nudge="signup"]').count() == 0
    a.screenshot(path=out + 'acct_nudge_signed_out.png')
    a.click('#nudge [data-nudge="signin"]'); a.wait_for_timeout(200)
    assert a.evaluate('Acct.mode') == 'signin'
    a.click('#acctPanel [data-act="close"]'); a.wait_for_timeout(100)
    a.click('#acctBtn'); a.wait_for_timeout(200)
    assert a.evaluate('Acct.mode') == 'signin', a.evaluate('Acct.mode')
    assert a.input_value('#acctPanel input[name=email]') == 'vlad@example.com', 'last email remembered'
    assert a.evaluate('document.activeElement.name') == 'password', 'cursor waits in the password box'
    assert a.locator('#acctPanel .atabs button').count() == 2
    a.screenshot(path=out + 'acct_signin_after_signout.png')
    a.click('#acctPanel .atabs [data-mode="signup"]'); a.wait_for_timeout(100)
    assert a.evaluate('Acct.mode') == 'signup' and a.evaluate("document.activeElement.dataset.mode") == 'signup'
    a.click('#acctPanel [data-act="close"]'); a.wait_for_timeout(100)
    sheet(a, 'signup', 'friend@example.com', 'another one')
    assert synced(a)
    assert not a.evaluate("lessonSeen('w', 'grab') || !!up('w-italian').idea"), "someone else's progress leaked into a new account"
    fid = a.evaluate('Cloud.user.id'); assert 'course' not in S.rows[fid]['data'] or not S.rows[fid]['data']['course'].get('seen', {}).get('grab')
    a.click('#acctBtn'); a.click('#acctPanel [data-act="signout"]'); a.wait_for_timeout(200)
    sheet(a, 'signin', 'vlad@example.com', 'correct horse')
    assert synced(a) and a.evaluate("lessonSeen('w', 'grab')"), 'back to the first account'

    # ---- email confirmation and password reset links
    S.confirm = True
    C = b.new_context(viewport={'width': 1280, 'height': 860}, color_scheme='dark'); wire(C)
    c = C.new_page(); hook(c, 'C')
    c.goto(APP); c.wait_for_timeout(800)
    sheet(c, 'signup', 'new@example.com', 'brand new pass')
    assert c.evaluate('Acct.mode') == 'check', c.evaluate('Acct.mode')
    c.screenshot(path=out + 'acct_check_dark.png')
    kind, email, code = S.mail[-1]; assert kind == 'confirm'
    c.goto(f'{APP}?code={code}'); c.wait_for_timeout(1000)
    print('after confirm link:', c.evaluate('[location.search, Cloud.user && Cloud.user.email]'), '| toast:', c.inner_text('#toast'))
    assert c.evaluate("location.search === '' && Cloud.user.email === 'new@example.com'")
    c.click('#acctBtn'); c.click('#acctPanel [data-act="signout"]'); c.wait_for_timeout(200)
    sheet(c, 'forgot', 'new@example.com')
    print('reset request:', c.inner_text('#acctPanel .formmsg'))
    kind, email, code = S.mail[-1]; assert kind == 'reset'
    c.goto(f'{APP}?reset=1&code={code}'); c.wait_for_timeout(1000)
    assert c.evaluate('Acct.mode') == 'newpass', c.evaluate('Acct.mode')
    c.fill('#acctPanel input[name=password]', 'changed it now'); c.click('#acctPanel button[type=submit]'); c.wait_for_timeout(400)
    assert c.evaluate('Acct.mode') is None and S.users['new@example.com']['password'] == 'changed it now'
    c.goto(f'{APP}?error=access_denied&error_code=otp_expired&error_description=Email+link+is+invalid+or+has+expired'); c.wait_for_timeout(900)
    print('expired link:', c.inner_text('#acctPanel .formmsg'))
    assert c.evaluate('Acct.mode') == 'signin' and c.evaluate('location.search') == ''
    c.screenshot(path=out + 'acct_expired_dark.png')
    # phone, light: the sheet sits at the bottom and nothing scrolls sideways
    bp.click('#acctBtn'); bp.click('#acctPanel [data-act="signout"]'); bp.wait_for_timeout(200)
    bp.click('#acctBtn'); bp.wait_for_timeout(200)
    assert bp.evaluate('Acct.mode') == 'signin'
    assert bp.evaluate('document.documentElement.scrollWidth') <= 390
    bp.screenshot(path=out + 'acct_phone_signin.png')

    # ---- a switch only the server can hand out (app_metadata, which no page can write): anyone else sees nothing,
    # metadata a user can set does not count, and the switched-on page works on a copy that never reaches the account
    S.confirm = False
    O = b.new_context(viewport={'width': 1280, 'height': 860}); wire(O); o = O.new_page(); hook(o, 'O')
    o.goto(APP + '#course'); o.wait_for_timeout(900)
    sheet(o, 'signup', 'someone@example.com', 'just a player'); assert synced(o)
    oid = o.evaluate('Cloud.user.id'); S.users['someone@example.com']['meta']['playbook_owner'] = True   # set by the user: worth nothing
    o.reload(); o.wait_for_timeout(1200); assert synced(o)
    o.click('h1'); o.keyboard.type('admin'); o.wait_for_timeout(300)
    o.click('#setBtn'); o.wait_for_timeout(200)
    assert not o.evaluate('Owner.can || Owner.on') and o.locator('[data-own], #opill').count() == 0 and 'admin' not in o.inner_text('body').lower()
    o.keyboard.press('Escape'); o.wait_for_timeout(100)
    o.evaluate("markSeen('setup')"); o.wait_for_timeout(1500); assert S.rows[oid]['data']['course']['seen'].get('setup')
    S.users['someone@example.com']['app'] = {'playbook_owner': True}                                    # set on the server
    o.reload(); o.wait_for_timeout(1200); assert synced(o)
    o.wait_for_function('Owner.can === true', timeout=5000)
    o.click('#setBtn'); o.wait_for_timeout(200); assert o.locator('#setPanel [data-own]').count() == 1
    o.keyboard.press('Escape'); o.wait_for_timeout(100)
    before = json.dumps(S.rows[oid]['data'], sort_keys=True)
    o.click('h1'); o.keyboard.type('admin'); o.wait_for_timeout(300)
    assert o.evaluate('Owner.on') and o.locator('#opill').is_visible() and o.evaluate('Shop.balance()') == float('inf')
    o.evaluate("OwnerUI.act('course')"); o.wait_for_timeout(500)
    assert o.evaluate('!!gradAt()') and o.evaluate("COURSE.filter(U => !U.soon).every(unitPassed)")
    o.evaluate("Prog.record('center', true)"); o.wait_for_timeout(1800)
    assert json.dumps(S.rows[oid]['data'], sort_keys=True) == before, 'nothing done in admin mode reaches the account'
    o.reload(); o.wait_for_timeout(1500); o.wait_for_function('Owner.on === true', timeout=5000)   # the switch stays on across a reload
    assert o.evaluate('!!gradAt()'), 'the copy is kept on this device'
    o.click('h1'); o.keyboard.type('admin'); o.wait_for_timeout(800)
    assert not o.evaluate('Owner.on') and not o.evaluate('gradAt()') and o.evaluate("lessonSeen('w', 'setup')") and not o.evaluate("Prog.rec('center')"), 'back to the real progress'
    o.evaluate("markSeen('grab')"); o.wait_for_timeout(1500); assert S.rows[oid]['data']['course']['seen'].get('grab') and not S.rows[oid]['data']['course'].get('grad')
    o.click('h1'); o.keyboard.type('admin'); o.wait_for_timeout(300); assert o.evaluate('Owner.on')
    o.click('#acctBtn'); o.click('#acctPanel [data-act="signout"]'); o.wait_for_timeout(400)
    assert not o.evaluate('Owner.on || Owner.can') and o.locator('#opill').count() == 0, 'signing out ends it'
    print('owner switch: server-marked account only, never written to the account')

    # ---- the claude.ai build and an unconfigured site have no account features at all
    D = b.new_context(viewport={'width': 1280, 'height': 860}); wire(D, PLAIN)
    d = D.new_page(); hook(d, 'D'); d.goto(APP); d.wait_for_timeout(800)
    assert d.locator('#acctBtn').is_hidden() and d.locator('#nudge').is_hidden() and not d.evaluate('Cloud.on()')
    print('unconfigured build: no account button, no nudge')
    # ---- a visitor without games: the account comes first, then the games. An account that already holds the hand-built
    # playbook keeps it when it is opened on a new device.
    nb = launch(p, house=False); S.confirm = False
    N1 = nb.new_context(viewport={'width': 1280, 'height': 860}); wire(N1); n1 = N1.new_page(); hook(n1, 'N1')
    ROOTP = Path(__file__).resolve().parents[1]
    games = lambda f: ['[Event ' + g for g in (ROOTP / 'data' / 'games' / f).read_text().split('[Event ')[1:]]
    arch = {'09': games('vladapl_1.pgn'), '10': games('vladapl_2.pgn')}
    def chesscom(route):
        u = route.request.url
        if u.endswith('/player/vladapl/games/archives'): route.fulfill(status=200, content_type='application/json', body=json.dumps({'archives': [f'https://api.chess.com/pub/player/vladapl/games/2026/{m}' for m in arch]}))
        elif u[-2:] in arch: route.fulfill(status=200, content_type='application/json', body=json.dumps({'games': [{'rules': 'chess', 'time_class': 'blitz', 'pgn': g} for g in arch[u[-2:]]]}))
        else: route.fulfill(status=404, content_type='application/json', body='{}')
    N1.route('https://api.chess.com/**', chesscom)
    n1.goto(APP); n1.wait_for_timeout(900)
    assert n1.evaluate('[PERSONA, S.view]') == ['new', 'start'] and n1.locator('.whero [data-acct="signup"]').count() == 1 and n1.locator('[data-pgo="setup"]').count() == 0
    n1.evaluate("go('setup')"); n1.wait_for_timeout(200); assert n1.locator('#uform').count() == 0 and 'Start with an account' in n1.inner_text('#view')
    n1.evaluate("go('start')"); n1.wait_for_timeout(200)
    n1.click('.whero [data-acct="signup"]'); n1.wait_for_timeout(200); assert n1.evaluate('Acct.mode') == 'signup'
    assert n1.locator('#acctPanel input[name=chess]').count() == 1 and n1.is_checked('#acctPanel input[name=mail]'), 'the chess account and reminders are part of the sign-up'
    n1.click('#acctPanel [data-csite="lichess"]'); n1.wait_for_timeout(100); assert 'Lichess' in n1.get_attribute('#acctPanel input[name=chess]', 'placeholder')
    n1.click('#acctPanel [data-csite="chess.com"]'); n1.wait_for_timeout(100)
    n1.fill('#acctPanel input[name=chess]', 'VladAPL'); n1.screenshot(path=out + 'acct_signup_connect.png')
    sheet(n1, 'signup', 'player@example.com', 'a long password'); assert synced(n1), n1.evaluate('[!!Cloud.user, Cloud.state, Cloud.err, Cloud.writing, Cloud.pulling, Acct.mode, Acct.msg]')
    if n1.evaluate('!!Acct.mode'): n1.evaluate('Acct.close()')
    # straight to the games: this made-up player has too few of them, so the playbook waits for more
    n1.wait_for_function("S.view === 'setup' && !!document.querySelector('.pshort')", timeout=20000); n1.wait_for_timeout(1800)
    assert S.users['player@example.com']['meta'] == {'chess_site': 'chess.com', 'chess_user': 'VladAPL'}
    row = S.rows[S.users['player@example.com']['id']]['data']; print('after sign-up:', row['me'], '| reminders', row.get('mail'))
    assert row['me']['state'] == 'new' and row['me']['short']['user'] == 'vladapl' and row['me']['auto'] == 1 and row['mail']['on'] is True, row.get('me')
    n1.reload(); n1.wait_for_timeout(1200); assert n1.evaluate('Product.busy') is False and n1.locator('.pshort').count() == 1, 'the games are read once, not on every visit'
    n1.evaluate("go('start')"); n1.wait_for_timeout(300)
    assert n1.locator('.whero [data-pgo="setup"]').inner_text() == 'Check my games again' and n1.locator('.steps3 li.done').count() == 1
    n1.click('.whero [data-pgo="setup"]'); n1.wait_for_timeout(200); n1.click('[data-other]'); n1.wait_for_timeout(200); assert n1.locator('#uform').count() == 1
    print('new player: account first, then', n1.inner_text('.chead h2'))
    N2 = nb.new_context(viewport={'width': 1280, 'height': 860}); wire(N2); n2 = N2.new_page(); hook(n2, 'N2')
    n2.goto(APP); n2.wait_for_timeout(900); assert n2.evaluate('PERSONA') == 'new'
    n2.click('.whero [data-acct="signin"]'); n2.wait_for_timeout(200)
    sheet(n2, 'signin', 'vlad@example.com', 'correct horse'); n2.wait_for_timeout(1500)
    assert n2.evaluate('PERSONA') == 'house' and n2.locator('.tabs button.lock').count() == 0, n2.evaluate('[PERSONA, JSON.stringify(Prog.d.me)]')
    print('the hand-built playbook follows its account to a new device:', n2.evaluate('[PERSONA, S.view]'))
    m = n2.evaluate("""[mergeProg({lines: {}, me: {state: 'new'}}, {lines: {x: {box: 1}}}).me.state, mergeProg({lines: {}, me: {state: 'new', updated: 9}}, {lines: {}, me: {state: 'ready', updated: 1}}).me.state,
        mergeProg({lines: {}}, {lines: {}}).me === undefined]""")
    assert m == ['house', 'ready', True], m
    # ---- Reset account, in Advanced settings. The username confirms it; everything earned goes, on this device and in
    #      the account; the page opens on the welcome screen with the same chess account or another to choose from.
    vid = S.users['vlad@example.com']['id']
    n2.evaluate("Prog.record('setup', true); setSetting('board', 'blue'); Prog.save()"); n2.wait_for_timeout(1900)
    assert S.rows[vid]['data']['lines'].get('setup'), 'progress in the account before the reset'
    n2.click('#setBtn'); n2.wait_for_timeout(300); assert 'Advanced settings' in n2.inner_text('#setPanel .repdet > summary')
    n2.click('#setPanel .repdet > summary'); n2.wait_for_timeout(200); n2.click('#setPanel [data-resetask]'); n2.wait_for_timeout(200)
    sub = n2.locator('#setPanel .resetask [type=submit]'); assert sub.is_disabled()
    n2.fill('#resetName', 'somebody'); assert sub.is_disabled(), 'another name does not confirm it'
    n2.screenshot(path=out + 'acct_reset_ask.png')
    n2.fill('#resetName', 'Aqua_Alpaca'); assert not sub.is_disabled(); sub.click()
    n2.wait_for_function("typeof PERSONA !== 'undefined' && PERSONA === 'new' && S.view === 'start' && !!document.querySelector('.whero [data-again]')", timeout=20000); n2.wait_for_timeout(600)
    row = S.rows[vid]['data']; print('after the reset:', {k: row.get(k) for k in ('me', 'lines')}, '| board kept:', row['set']['board'])
    assert row['me']['state'] == 'new' and row['me']['was'] == {'site': 'chess.com', 'user': 'aqua_alpaca', 'house': True} and row['lines'] == {} and row['reset'] and row['set']['board'] == 'blue'
    left = n2.evaluate("[Object.keys(Prog.d.lines).length, !!Prog.d.badges, !!Prog.d.days, !!Prog.d.tour, SET.board]"); print('on this device:', left)
    assert left == [0, False, False, False, 'blue'], left
    btns = n2.locator('.whero .cta button').all_inner_texts(); print('the welcome screen after it:', btns); assert btns[:2] == ['Use aqua_alpaca again', 'Link another account'], btns
    n2.screenshot(path=out + 'acct_reset_welcome.png')
    # an older copy on another device can't bring the progress back, whichever way the two meet
    mr = n2.evaluate("""(() => { const oldc = {lines: {x: {box: 3, seen: 4}}, days: {a: [1]}, badges: {s3: 1}, updated: 5}, fresh = {lines: {}, puz: {}, reset: 9, me: {state: 'new'}};
        return [mergeProg(oldc, fresh), mergeProg(fresh, oldc)].map(m => [Object.keys(m.lines).length, !!m.days, !!m.badges, m.me.state, m.reset]); })()""")
    assert mr == [[0, False, False, 'new', 9]] * 2, mr
    # the same account again: the hand-built playbook, from nothing
    n2.click('.whero [data-again]'); n2.wait_for_function("typeof PERSONA !== 'undefined' && PERSONA === 'house' && S.view !== 'start'", timeout=20000); n2.wait_for_timeout(1500)
    back = n2.evaluate("[PERSONA, Object.keys(Prog.d.lines).length, document.querySelectorAll('.tabs button.lock').length]"); print('the same account again:', back, S.rows[vid]['data']['me']['state'])
    assert back == ['house', 0, 0] and S.rows[vid]['data']['me']['state'] == 'house'
    nb.close()
    print('ERRORS:', errors[:8])
    assert not errors
    b.close()
