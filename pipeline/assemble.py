"""Inject the piece symbols, both books and the course into app/template.html.

Writes data/build/playbook.html (the page body, as published to Claude artifacts; no accounts) and
docs/index.html (a complete standalone page for GitHub Pages; accounts through Supabase when
app/site.json has a project URL and publishable key)."""
import hashlib, json
import paths
from pieces import piece_svg_inner
from lint_claims import lint_labels, lint_pins, lint_repeats

VERSIONS = paths.DATA / 'line_versions.json'


def stamp_versions(books):
    """Give every line a version that goes up whenever its moves change.

    Progress is stored per line id. When a line's moves change, a record made on the old moves says nothing about
    the new ones, so the page treats it as due again. data/line_versions.json remembers {id: [version, hash of moves]}
    between builds; it is committed, and a rebuild that changes no moves leaves it untouched."""
    vers = json.load(open(VERSIONS)) if VERSIONS.exists() else {}
    for D in books:
        for l in D['lines']:
            h = hashlib.sha1(' '.join(D['nodes'][i].get('u', '') for i in l['n']).encode()).hexdigest()[:10]
            v = vers.get(l['id'])
            if v is None: vers[l['id']] = [1, h]
            elif v[1] != h: vers[l['id']] = [v[0] + 1, h]
            if vers[l['id']][0] > 1: l['v'] = vers[l['id']][0]
            else: l.pop('v', None)
    VERSIONS.write_text(json.dumps(vers, sort_keys=True, separators=(',', ':')).replace('],', '],\n') + '\n')
    return sum(1 for D in books for l in D['lines'] if l.get('v'))

SUPABASE_JS = 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.105.4'
HEAD = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
        '<meta name="description" content="A notation-free chess opening course built from 200 real games: one path through White and Black repertoires, drills, a sparring sandbox, threat-spotting from your own blunders and engine-checked game reviews.">'
        '<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top);padding-bottom:env(safe-area-inset-bottom)}'
        'body{margin:0;font:14px system-ui,sans-serif}img{max-width:100%}[hidden]{display:none!important}</style></head><body>')


def site_html(body, site=None):
    """The standalone page. With a configured site, load supabase-js before the app and hand it the config."""
    if site and site.get('supabaseUrl') and site.get('supabaseKey'):
        cfg = {k: site[k] for k in ('supabaseUrl', 'supabaseKey', 'home')}
        assert body.count('/*__SITE__*/null') == 1
        body = body.replace('/*__SITE__*/null', json.dumps(cfg))
        first = body.index('<script>')
        body = body[:first] + f'<script src="{SUPABASE_JS}"></script>\n' + body[first:]
    return HEAD + body + '</body></html>'


def main():

    syms = ''.join(f'<symbol id="p-{c}{k}" viewBox="0 0 45 45">{piece_svg_inner(c, k)}</symbol>' for c in 'wb' for k in 'kqrbnp')
    W = json.load(open(paths.BUILD / 'data_white.json'))
    B = json.load(open(paths.BUILD / 'data_black.json'))
    C = json.load(open(paths.BUILD / 'data_course.json'))
    # White book extras (the White data was built before the Black book existed)
    W['side'] = 'w'; W['oddsRoot'] = W['e4']
    first_puz = lambda gid: next(k for k, p in enumerate(W['puzzles']) if p['game'] == gid)
    W['insights'] = [
      dict(puz=first_puz('g-joedbm'), big='6', unit='times', h='Bishop takes f7, missed', p='Four times in one Italian, once more in the Italian on Oct 14, and once in the Philidor the same day. Each time the bishop sacrifice on f7 won material.'),
      dict(puz=first_puz('g-bacha'), big='6', unit='chances', h='Push the d-pawn at the knight', p='In three Sicilians, after the pawn trade Black\'s knight sat where your d-pawn could hit it. Pushing the pawn at it was the best move six times, and it was skipped every time.'),
      dict(puz=first_puz('g-malik'), big='3', unit='in one game', h='The e-pawn push, skipped', p='In the bishop-retreat line of the Italian, kicking the knight with your e-pawn was the best move three turns running.'),
      dict(puz=first_puz('g-gilmar'), big='6', unit='moves', h='Guard the e-pawn first', p='Against the bishop on the long diagonal your e-pawn was attacked twice and guarded once. It fell on move four, and two moves later the same bishop took another pawn with your corner rook next.'),
    ]
    # plans for the end of each lesson's main line (content/plans.py), checked for notation like every other text
    import re
    from plans import W as PLAN_W, B as PLAN_B
    for D, P in ((W, PLAN_W), (B, PLAN_B)):
        ids = {l['id'] for l in D['lessons']}
        assert set(P) <= ids, sorted(set(P) - ids)
        for L in D['lessons']:
            if L['id'] in P: L['plan'] = P[L['id']]
    for k, pl in list(PLAN_W.items()) + list(PLAN_B.items()):
        for t in [pl['h']] + [x[1] for x in pl['b']]:
            bad = [m for m in re.findall(r'\b[a-h][1-8]\b', t) if m not in ('f7', 'f2')] + re.findall(r'\b[KQRBN]x?[a-h][1-8]\b|O-O', t)
            assert not bad, (k, t, bad)
        assert all(x[0] in ('king', 'pawns', 'pieces', 'target', 'them', 'watch') for x in pl['b']), k
    # the same position must get the same move whatever the move order; a pin, a guard or an attack that a label
    # speaks of must be on the board
    problems = [x for side in ('white', 'black') for x in lint_repeats(side) + lint_pins(side) + lint_labels(side)]
    assert not problems, '\n' + '\n'.join(problems)
    changed = stamp_versions((W, B))
    # progress records are shared between the books, so ids must never collide
    wl, bl = {l['id'] for l in W['lines']}, {l['id'] for l in B['lines']}
    assert not (wl & bl), sorted(wl & bl)[:10]
    assert not ({p['id'] for p in W['puzzles']} & {p['id'] for p in B['puzzles']})

    dump = lambda d: json.dumps(d, separators=(',', ':')).replace('</', '<\\/')
    tpl = (paths.APP / 'template.html').read_text()
    site = json.load(open(paths.APP / 'site.json'))
    # chess.js (BSD-2) is inlined: free exploration needs legal moves, checks and full positions for the engine
    chessjs = (paths.APP / 'vendor' / 'chess.js').read_text()
    assert '</script' not in chessjs
    body = tpl.replace('<!--__PIECES__-->', syms).replace('/*__DATA_W__*/', dump(W)).replace('/*__DATA_B__*/', dump(B)).replace('/*__DATA_C__*/', dump(C))
    body = body.replace('/*__CHESSJS__*/', chessjs).replace("/*__HOME__*/''", json.dumps(site.get('home', '')))
    # the game analysis and the product shell (welcome, games in, choices, the coach) live in their own files
    for mark, name in (('/*__ANALYZE__*/', 'analyze.js'), ('/*__PRODUCT_JS__*/', 'product.js'), ('/*__PRODUCT_CSS__*/', 'product.css')):
        assert body.count(mark) == 1, mark
        body = body.replace(mark, (paths.APP / name).read_text().replace("if (typeof module !== 'undefined') module.exports = Analyze;", '').replace('</', '<\\/'))
    assert '/*__DATA' not in body and '/*__CHESSJS__*/' not in body and '/*__HOME__*/' not in body
    (paths.BUILD / 'playbook.html').write_text(body)
    page = site_html(body, site)
    (paths.DOCS / 'index.html').write_text(page)
    print('playbook.html', len(body), '| docs/index.html', len(page), '| lines changed since first release', changed, '| accounts', 'on' if site.get('supabaseUrl') and site.get('supabaseKey') else 'off (app/site.json has no project yet)')


if __name__ == '__main__':
    main()
