"""Shared imports for every pipeline script: python-chess and the Stockfish path."""
import paths  # noqa: F401  (sets up sys.path)
import chess, chess.pgn, chess.engine  # noqa: F401
SF = paths.STOCKFISH
