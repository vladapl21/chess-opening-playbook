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
        return {'access_token': t, 'user': {'id': u['id'], 'email': u['email']}}

    def handle(self, path, b):
        uid = self.tokens.get(b.get('token'))
        if path == 'signup':
            if b['email'] in self.users: return {'error': {'message': 'User already registered'}}
            u = self.users[b['email']] = {'id': 'u-' + secrets.token_hex(4), 'email': b['email'], 'password': b['password'], 'confirmed': not self.confirm}
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
    for _ in range(40):
        if pg.evaluate("!!Cloud.user && Cloud.state === 'ok' && !Cloud.writing && !Cloud.pulling"): return True
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
    bp.click('#acctPanel [data-act="close"]')

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

    # ---- the claude.ai build and an unconfigured site have no account features at all
    D = b.new_context(viewport={'width': 1280, 'height': 860}); wire(D, PLAIN)
    d = D.new_page(); hook(d, 'D'); d.goto(APP); d.wait_for_timeout(800)
    assert d.locator('#acctBtn').is_hidden() and d.locator('#nudge').is_hidden() and not d.evaluate('Cloud.on()')
    print('unconfigured build: no account button, no nudge')
    # ---- a visitor without games: the account comes first, then the games. An account that already holds the hand-built
    # playbook keeps it when it is opened on a new device.
    nb = launch(p, house=False); S.confirm = False
    N1 = nb.new_context(viewport={'width': 1280, 'height': 860}); wire(N1); n1 = N1.new_page(); hook(n1, 'N1')
    n1.goto(APP); n1.wait_for_timeout(900)
    assert n1.evaluate('[PERSONA, S.view]') == ['new', 'start'] and n1.locator('.whero [data-acct="signup"]').count() == 1 and n1.locator('[data-pgo="setup"]').count() == 0
    n1.evaluate("go('setup')"); n1.wait_for_timeout(200); assert n1.locator('#uform').count() == 0 and 'First, an account' in n1.inner_text('#view')
    n1.evaluate("go('start')"); n1.wait_for_timeout(200)
    n1.click('.whero [data-acct="signup"]'); n1.wait_for_timeout(200); assert n1.evaluate('Acct.mode') == 'signup'
    sheet(n1, 'signup', 'player@example.com', 'a long password'); assert synced(n1), n1.evaluate('[!!Cloud.user, Cloud.state, Cloud.err, Cloud.writing, Cloud.pulling, Acct.mode, Acct.msg]')
    if n1.evaluate('!!Acct.mode'): n1.evaluate('Acct.close()')
    n1.wait_for_timeout(300)
    assert n1.locator('.whero [data-pgo="setup"]').count() == 1 and n1.locator('.steps3 li.done').count() == 1, 'signed in: the next step is the games'
    row = S.rows[S.users['player@example.com']['id']]['data']; assert row['me']['state'] == 'new', row.get('me')
    n1.click('.whero [data-pgo="setup"]'); n1.wait_for_timeout(200); assert n1.locator('#uform').count() == 1
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
    nb.close()
    print('ERRORS:', errors[:8])
    assert not errors
    b.close()
