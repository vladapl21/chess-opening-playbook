"""Classify the Black games into Black-book chapters (None = not covered by the book)."""
def chapter_of(sans):
    s = list(sans) + [''] * 8
    # 1.Nf3 Nc6 2.e4 e5 is a 1.e4 e5 2.Nf3 Nc6 position: reorder
    if s[0] == 'Nf3' and s[2] == 'e4' and s[3] == 'e5' and s[1] == 'Nc6':
        s = ['e4', 'e5', 'Nf3', 'Nc6'] + s[4:]
    if s[0] == 'e4':
        if s[1] != 'e5': return None
        w2 = s[2]
        if w2 == 'Nf3':
            w3 = s[4]
            return {'Bc4': 'italian', 'Bb5': 'ruy', 'd4': 'scotch', 'Nc3': 'vienna'}.get(w3, 'vienna')
        if w2 == 'd4': return 'scotch'
        if w2 == 'Nc3': return 'vienna'
        if w2 == 'Bc4': return 'italian' if s[4] == 'Nf3' else 'vienna' if s[4] == 'Nc3' else 'attacks'
        if w2 in ('Qh5', 'Qf3', 'f4'): return 'attacks'
        return 'vienna'
    if s[0] == 'd4':
        if s[2] == 'c4': return 'qgd'
        if s[2] == 'Bf4' or (s[2] == 'Nf3' and s[4] == 'Bf4'): return 'london'
        return 'd4x'
    return 'other'
if __name__ == '__main__':
    import json, collections, paths
    G = json.load(open(paths.DATA / 'black_games.json'))
    c = collections.defaultdict(lambda: [0, 0, 0, 0])
    for g in G:
        ch = chapter_of(g['sans']); c[ch][0] += 1; c[ch][{'W': 1, 'L': 2, 'D': 3}[g['res']]] += 1
    for k, v in sorted(c.items(), key=lambda kv: -kv[1][0]): print(k, v)
    print(sum(v[0] for v in c.values()))
