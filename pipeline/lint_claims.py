"""Check what the built books say against the board, for both books.

  pins     a label or note that speaks of a pin needs a real one on the board, before or after the move:
           a piece attacked by a bishop, rook or queen with its king, or a more valuable piece, right behind it
  labels   a label that says the move guards a piece, or hits one, needs the board to agree: after the move the
           named piece has a new guard (or attacker), or the piece that moved guards (or attacks) it
  repeats  the same position reached by two move orders must get the same move from you

Exit code 1 if anything is found, so the build can stop on it."""
import sys, json, re, collections, itertools
import paths
from common import *

VAL = {chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3, chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 100}


def pins(b):
    """Every pin on the board: (pinned square, pinner square)."""
    out = []
    for sq, pc in b.piece_map().items():
        if pc.piece_type not in (chess.BISHOP, chess.ROOK, chess.QUEEN): continue
        for t in b.attacks(sq):
            tp = b.piece_at(t)
            if not tp or tp.color == pc.color or tp.piece_type == chess.KING: continue
            df = (chess.square_file(t) > chess.square_file(sq)) - (chess.square_file(t) < chess.square_file(sq))
            dr = (chess.square_rank(t) > chess.square_rank(sq)) - (chess.square_rank(t) < chess.square_rank(sq))
            f, r = chess.square_file(t) + df, chess.square_rank(t) + dr
            while 0 <= f < 8 and 0 <= r < 8:
                x = b.piece_at(chess.square(f, r))
                if x:
                    if x.color == tp.color and VAL[x.piece_type] > VAL[tp.piece_type] and (tp.piece_type != chess.PAWN or x.piece_type == chess.KING):
                        out.append((t, sq))
                    break
                f += df; r += dr
    return out


def book(side):
    D = json.load(open(paths.BUILD / f'data_{side}.json')); N = D['nodes']; boards = {}
    def board(i):
        if i not in boards:
            if N[i]['p'] is None: boards[i] = chess.Board()      # the book root, and the start of each game replay
            else:
                b = board(N[i]['p']).copy(); b.push(chess.Move.from_uci(N[i]['u'])); boards[i] = b
        return boards[i]
    def path(i):
        out = []
        while N[i]['p'] is not None: out.append(board(N[i]['p']).san(chess.Move.from_uci(N[i]['u']))); i = N[i]['p']
        return ' '.join(reversed(out))
    return D, N, board, path


# words that speak of a pin that is not on the board right now
HYPO = re.compile(r"can't be pinned|cannot be pinned|would be pinned|will be pinned|before the bishop can pin|to pin|no pin|not pinned|unpin|a pin\b"
                  r"|stop the pin|and pin your|from pinning|\bif\b[^.]*\bpins?\b", re.I)


def lint_pins(side):
    D, N, board, path = book(side); bad = []
    for i, n in enumerate(N):
        if n['p'] is None: continue
        txt = f"{n.get('l') or ''} | {n.get('t') or ''}"
        if not re.search(r'\bpin(s|ned)?\b', txt, re.I): continue
        if HYPO.search(txt) and not re.search(r'\bpins (the|your)\b', n.get('l') or '', re.I): continue
        if pins(board(i)) or pins(board(n['p'])): continue
        bad.append(f'{side}: no pin on the board | {txt[:110]} | {path(i)}')
    # line titles: a title that speaks of a pin needs one somewhere along its line
    lessons = {l['id'] for l in D['lessons']}
    for l in D['lines']:
        t = l.get('title') or ''
        if l['lesson'] not in lessons or not re.search(r'\bpin(s|ned)?\b', t, re.I) or HYPO.search(t): continue
        if not any(pins(board(i)) for i in l['n']): bad.append(f'{side}: no pin anywhere on the line | {t} | {l["id"]}')
    for l in D['lessons']:
        t = f"{l.get('title') or ''} | {l.get('sub') or ''}"
        if not re.search(r'\bpin(s|ned)?\b', t, re.I) or HYPO.search(t): continue
        mine = [x for x in D['lines'] if x['lesson'] == l['id']]
        if not any(pins(board(i)) for x in mine for i in x['n']): bad.append(f'{side}: no pin in any line of the lesson | {t} | {l["id"]}')
    return bad


NAME = {'pawn': chess.PAWN, 'knight': chess.KNIGHT, 'bishop': chess.BISHOP, 'rook': chess.ROOK, 'queen': chess.QUEEN}
OBJ = (r"(?:the |your |its |white's |black's |their )?(?:(?:loose|pinned|other|extra|weak|lone|second|king's|queen's|dark|light|center|central|middle|far|same|big|trapped) )*"
       r"((?:[a-h]-|edge |rook |)pawn|knight|bishop|rook|queen)\b")
NOT = re.compile(r"\b(no longer|can't|cannot|nothing|nobody|not|doesn't|don't|never|only|left|lost|needs?|must|has to|should|if)\b", re.I)


def lint_labels(side):
    """'X guards the knight' and 'X hits your bishop' are claims about the board. Only the label's first clause is read."""
    D, N, board, path = book(side); bad = []
    for i, n in enumerate(N):
        if n['p'] is None or not n.get('l'): continue
        head = re.split(r'[:;,]', n['l'])[0]
        if NOT.search(head): continue
        b, pb, mv = board(i), board(n['p']), chess.Move.from_uci(n['u']); col = not b.turn
        for verb, own in ((r'guards?', True), (r'(?:hits|attacks|threatens|forks)', False)):
            m = re.search(r'\b' + verb + ' ' + OBJ, head, re.I)
            if not m: continue
            w = m.group(1); pt = chess.PAWN if w.endswith('pawn') else NAME[w]
            f = 'abcdefgh'.index(w[0]) if re.match(r'[a-h]-', w) else None
            tg = [s for s, p in b.piece_map().items() if p.piece_type == pt and (p.color == col) == own and (f is None or chess.square_file(s) == f)]
            if not any(mv.to_square in b.attackers(col, s) or len(b.attackers(col, s)) > len(pb.attackers(col, s)) for s in tg):
                bad.append(f"{side}: the move does not {'guard' if own else 'hit'} that piece | {n['l']} | {path(i)}")
    return bad


def combos(D):
    """Every repertoire a player can hold: one pack per slot (see PACKS in the content). Returns sets of chapter ids left out."""
    slots = list((D.get('packs') or {}).values())
    if not slots: return [frozenset()]
    out = []
    for pick in itertools.product(*[list(s['packs']) for s in slots]):
        out.append(frozenset(c for s, p in zip(slots, pick) for q, chs in s['packs'].items() if q != p for c in chs))
    return out


def lint_repeats(side):
    D, N, board, path = book(side); me = chess.WHITE if side == 'white' else chess.BLACK
    part_ch = {p: c['id'] for c in D['chapters'] for p in c['parts']}; les_ch = {l['id']: part_ch[l['part']] for l in D['lessons']}
    bad = []
    for off in combos(D):
        on = set()
        for l in D['lines']:
            if l['lesson'] in les_ch and les_ch[l['lesson']] not in off: on.update(l['n'])
        pos = collections.defaultdict(dict)
        for i in on:
            if board(i).turn != me: continue
            for k in N[i]['k']:
                if k in on and 'warn' not in (N[k].get('g') or []): pos[board(i).epd()].setdefault(N[k]['u'], k)
        for key, mv in pos.items():
            if len(mv) > 1:
                msg = f'{side}: same position, different moves | ' + ' || '.join(path(k) for k in mv.values())
                if msg not in bad: bad.append(msg)
    return bad


if __name__ == '__main__':
    out = []
    for side in ('white', 'black'): out += lint_repeats(side) + lint_pins(side) + lint_labels(side)
    print('\n'.join(out)); print(len(out), 'problems')
    sys.exit(1 if out else 0)
