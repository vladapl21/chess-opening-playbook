"""Repository paths and external tools. Importing this module puts pipeline/, content/ and app/ on sys.path.

Environment variables (all optional when the committed caches cover every position):
  STOCKFISH        path to a Stockfish binary (default: "stockfish" on PATH)
  MAIA_WEIGHTS     folder with maia-1300.pb.gz and maia-1500.pb.gz (CSSLab/maia-chess)
  LCZERO_TRAINING  checkout of LeelaChessZero/lczero-training (for the policy index)
"""
import os, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PIPE = ROOT / 'pipeline'
APP = ROOT / 'app'
CONTENT_WHITE = ROOT / 'content' / 'white'
CONTENT_BLACK = ROOT / 'content' / 'black'
DATA = ROOT / 'data'
GAMES = DATA / 'games'
CACHE = DATA / 'cache'
BUILD = DATA / 'build'
DOCS = ROOT / 'docs'

for p in (PIPE, CONTENT_WHITE, CONTENT_BLACK, APP):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

STOCKFISH = os.environ.get('STOCKFISH', 'stockfish')
MAIA_WEIGHTS = Path(os.environ.get('MAIA_WEIGHTS', ROOT / 'vendor' / 'maia'))
LCZERO_TF = Path(os.environ.get('LCZERO_TRAINING', ROOT / 'vendor' / 'lczero-training')) / 'tf'
