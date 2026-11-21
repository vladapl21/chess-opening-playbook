"""Systems: which chapters a repertoire holds.

PACKS (content/white/content2_meta.py, content/black/bmeta.py) is slot -> dict(default, packs={pack: [chapters]}).
A slot is one decision ("what do I play against the e-pawn?") and a pack is one answer to it. A slot can carry
`within=[slot, pack]`: it is a second step that exists only while that pack of the other slot is in play ("which
Sicilian?" once the Sicilian is the answer to the e-pawn). Its chapters are held only then.

picks is {slot: pack}; a slot that isn't named is at its default. The page has the same rule (packOf, slotOn and
applyPacks in app/template.html, inPlay in app/analyze.js)."""


def pick(P, picks, slot):
    p = (picks or {}).get(slot)
    return p if p in P[slot]['packs'] else P[slot]['default']


def on(P, picks, slot):
    """Is the slot in play with these picks?"""
    w = P[slot].get('within')
    return not w or (on(P, picks, w[0]) and pick(P, picks, w[0]) == w[1])


def off(P, picks=None):
    """The chapters a player with these picks does not hold (no picks: the house playbook)."""
    return {c for s, v in (P or {}).items() for pk, chs in v['packs'].items() if not on(P, picks, s) or pk != pick(P, picks, s) for c in chs}


def need(P, slot, pack):
    """What has to be picked for this pack to be in play: {slot: pack}, up the chain."""
    out = {slot: pack}; w = P[slot].get('within')
    if w: out.update(need(P, w[0], w[1]))
    return out


def together(a, b):
    """Can one player hold both? a and b are need() results, or None for a chapter outside the slots."""
    return a is None or b is None or all(b.get(s, p) == p for s, p in a.items())


def depth(P, slot):
    w = P[slot].get('within')
    return 1 + depth(P, w[0]) if w else 0


def combos(P):
    """Every repertoire a player can hold, as picks."""
    slots = sorted(P or {}, key=lambda s: depth(P, s)); out = []

    def go(i, picks):
        if i == len(slots): out.append(dict(picks)); return
        s = slots[i]
        if not on(P, picks, s): go(i + 1, picks); return
        for pk in P[s]['packs']: go(i + 1, {**picks, s: pk})
    go(0, {})
    return out


def in_house(P, slot, pack):
    """Is this pack part of the house playbook (every slot at its default)?"""
    return on(P, None, slot) and P[slot]['default'] == pack
