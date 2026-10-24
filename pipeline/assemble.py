"""Inject the piece symbols and both books into app/template.html.

Writes data/build/playbook.html (the page body, as published to Claude artifacts) and
docs/index.html (a complete standalone page for GitHub Pages or any static host)."""
import json
import paths
from pieces import piece_svg_inner

syms = ''.join(f'<symbol id="p-{c}{k}" viewBox="0 0 45 45">{piece_svg_inner(c, k)}</symbol>' for c in 'wb' for k in 'kqrbnp')
W = json.load(open(paths.BUILD / 'data_white.json'))
B = json.load(open(paths.BUILD / 'data_black.json'))
# White book extras (the White data was built before the Black book existed)
W['side'] = 'w'; W['oddsRoot'] = W['e4']
first_puz = lambda gid: next(k for k, p in enumerate(W['puzzles']) if p['game'] == gid)
W['insights'] = [
  dict(puz=first_puz('g-joedbm'), big='6', unit='times', h='Bishop takes f7, missed', p='Four times in one Italian, once more in the Italian on Oct 14, and once in the Philidor the same day. Each time the bishop sacrifice on f7 won material.'),
  dict(puz=first_puz('g-bacha'), big='6', unit='chances', h='Push the d-pawn at the knight', p='In three Sicilians, after the pawn trade Black\'s knight sat where your d-pawn could hit it. Pushing the pawn at it was the best move six times, and it was skipped every time.'),
  dict(puz=first_puz('g-malik'), big='3', unit='in one game', h='The e-pawn push, skipped', p='In the bishop-retreat line of the Italian, kicking the knight with your e-pawn was the best move three turns running.'),
  dict(puz=first_puz('g-gilmar'), big='6', unit='moves', h='Guard the e-pawn first', p='Against the bishop on the long diagonal your e-pawn was attacked twice and guarded once. It fell on move four, and two moves later the same bishop took another pawn with your corner rook next.'),
]
# progress records are shared between the books, so ids must never collide
wl, bl = {l['id'] for l in W['lines']}, {l['id'] for l in B['lines']}
assert not (wl & bl), sorted(wl & bl)[:10]
assert not ({p['id'] for p in W['puzzles']} & {p['id'] for p in B['puzzles']})

dump = lambda d: json.dumps(d, separators=(',', ':')).replace('</', '<\\/')
tpl = (paths.APP / 'template.html').read_text()
body = tpl.replace('<!--__PIECES__-->', syms).replace('/*__DATA_W__*/', dump(W)).replace('/*__DATA_B__*/', dump(B))
assert '/*__DATA' not in body
(paths.BUILD / 'playbook.html').write_text(body)
head = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
        '<meta name="description" content="A notation-free chess opening trainer built from 149 real games: White and Black repertoires, drills, a sparring sandbox and engine-checked game reviews.">'
        '<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top);padding-bottom:env(safe-area-inset-bottom)}'
        'body{margin:0;font:14px system-ui,sans-serif}img{max-width:100%}[hidden]{display:none!important}</style></head><body>')
(paths.DOCS / 'index.html').write_text(head + body + '</body></html>')
print('playbook.html', len(body), '| docs/index.html', len(head) + len(body) + 14)
