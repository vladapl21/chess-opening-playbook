"""Print Maia human-move odds for paths: python3 pipeline/human_odds.py "e4 e5" "d4 Nf6" ..."""
import sys
import paths
import expand as X
for p in sys.argv[1:]:
    p = '' if p == '-' else p
    hs = X.human(p)
    print(f"--- [{p or 'start'}]  " + '  '.join(f"{s} {v*100:.0f}" for s, v in hs[:10]))
X.save()
