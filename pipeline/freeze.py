"""Keep a copy of the site as it stands today at docs/<name>/: python3 pipeline/freeze.py v1 "22 November 2026"

The copy is today's build (data/build/playbook.html, made by assemble.py) as a page of its own, with the engine files
beside it. It has no accounts, and it keeps its own things in the browser: the live site has the same address, so
every key the copy writes in localStorage or sessionStorage gets '<name>:' in front, and a key it has never written
reads the live site's value. The copy opens with the progress the live site had, and the two never touch each other's
saved progress again. Nothing in the copy is built again later: it is a snapshot, not part of `make build`.
"""
import json, shutil, sys
import paths
from assemble import HEAD

SHIM = """<script>
// This copy keeps its own things in the browser, apart from the live site at the same address: every key it writes
// gets '%(p)s:' in front, and a key it has never written reads the live site's value, so the copy opens with the progress
// the live site had. It never writes to the live site's keys.
(function(){
  try {
    var P = '%(p)s:', GONE = '\\u0000', S = Storage.prototype, get = S.getItem, set = S.setItem;
    var ours = function(o){ try { return o === window.localStorage || o === window.sessionStorage; } catch(e){ return false; } };
    S.getItem = function(k){ if (!ours(this)) return get.call(this, k); var v = get.call(this, P + k); return v === GONE ? null : v !== null ? v : get.call(this, k); };
    S.setItem = function(k, v){ return set.call(this, ours(this) ? P + k : k, v); };
    var del = S.removeItem;
    S.removeItem = function(k){ return ours(this) ? set.call(this, P + k, GONE) : del.call(this, k); };
  } catch(e){}
})();
</script>"""


def main():
    name, day = sys.argv[1], sys.argv[2]
    site = json.load(open(paths.APP / 'site.json'))
    live = site.get('home', '')
    home = live.rstrip('/') + f'/{name}/'
    body = (paths.BUILD / 'playbook.html').read_text()
    assert body.count(json.dumps(live)) == 1, 'the home address appears once in the build'
    body = body.replace(json.dumps(live), json.dumps(home))
    assert body.startswith('<title>Opening Playbook</title>')
    body = body.replace('<title>Opening Playbook</title>', f'<title>Opening Playbook ({day})</title>', 1)
    out = paths.DOCS / name
    out.mkdir(exist_ok=True)
    (out / 'index.html').write_text(HEAD + SHIM % {'p': name} + body + '</body></html>')
    shutil.copytree(paths.DOCS / 'engine', out / 'engine', dirs_exist_ok=True)
    print('wrote', out / 'index.html', '| home', home)


if __name__ == '__main__':
    main()
