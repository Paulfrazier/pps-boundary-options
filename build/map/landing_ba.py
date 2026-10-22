#!/usr/bin/env python3
"""Landing-page before/after map: the current best example we modeled vs PPS A, elementary areas.

    python3 build/map/landing_ba.py      (build_site.py runs it after the map build)

Reads pages/map_data/level_K-5.js (the map page's own K-5 data: plan polygons and the plan-pair
changed areas) and writes pages/map_data/landing_ba.js, which sets window.LANDING_BA = {left, right, n, ar}:
two SVGs (same school = same color on both sides) with the changed areas outlined, the kids in them
(the pair's n, as on the map page), and the drawing's aspect ratio. Sides match the map page's
"PPS A vs current best" preset: the current best (site_data brief_rank 0) on the left, PPS A on the right.
"""
import json
import math
import os

KIT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(KIT, 'pages', 'map_data', 'level_K-5.js')
OUT = os.path.join(KIT, 'pages', 'map_data', 'landing_ba.js')
SITE = os.path.join(KIT, 'pages', 'data', 'site_data.json')


def current_best():
    """The plan site_data ranks first (BRIEFS.md order), as the map page's LEAD does."""
    try:
        opts = json.load(open(SITE)).get('options', [])
    except (OSError, ValueError):
        opts = []
    return next((o['name'] for o in opts if o.get('brief_rank') == 0), 'equity_noswap_alameda_rig_hs')


LEFT, RIGHT = current_best(), 'scenario_A'   # current best | PPS A
KX = math.cos(45.54 * math.pi / 180)          # same projection as the map page
PAL = ['#c9d9ec', '#f3d9b1', '#cfe5c8', '#ead0e4', '#f6e7a6', '#cde8e6', '#e8cfc6', '#d9d4ee']


def rings(enc):
    """Delta-encoded rings ('|'-separated; first pair absolute) -> lists of (x, y) in encoded units."""
    out = []
    for rr in enc.split('|'):
        t = rr.strip().split(' ')
        x, y = map(int, t[0].split(','))
        pts = [(x, y)]
        for q in t[1:]:
            if q:
                a, b = map(int, q.split(','))
                x += a; y += b
                pts.append((x, y))
        out.append(pts)
    return out


def path(enc):
    out = []
    for r in rings(enc):   # relative moves, rounded on the running total so error doesn't build up
        px, py = round(r[0][0] * KX), -r[0][1]
        seg = [f'M{px},{py}l']
        for x, y in r[1:]:
            nx, ny = round(x * KX), -y
            if (nx, ny) != (px, py):
                seg.append(f'{nx - px},{ny - py} ')
                px, py = nx, ny
        out.append(''.join(seg).rstrip() + 'z')
    return ''.join(out)


def main():
    s = open(SRC).read()
    i = s.index('MAPLV["K-5"]=') + len('MAPLV["K-5"]=')
    d = json.loads(s[i:].rstrip().rstrip(';'))
    pl = d['plans']
    pair = d['pairs'].get(f'{LEFT}|{RIGHT}') or d['pairs'][f'{RIGHT}|{LEFT}']
    # colors: greedy, north to south, avoiding the six nearest already-colored schools
    names = sorted(set(pl[LEFT]['poly']) | set(pl[RIGHT]['poly']))
    pt = d['sch']
    col = {}
    for n in sorted(names, key=lambda n: -pt.get(n, [0, 0])[1]):
        near = sorted((m for m in col if m in pt and n in pt),
                      key=lambda m: (pt[m][0] - pt[n][0]) ** 2 + (pt[m][1] - pt[n][1]) ** 2)[:6]
        used = {col[m] for m in near}
        col[n] = next((c for c in PAL if c not in used), PAL[0])
    xs, ys = [], []
    for k in (LEFT, RIGHT):
        for e in pl[k]['poly'].values():
            for r in rings(e):
                xs += [x * KX for x, _ in r]; ys += [-y for _, y in r]
    pad = 20
    x0, y0, w, h = min(xs) - pad, min(ys) - pad, max(xs) - min(xs) + 2 * pad, max(ys) - min(ys) + 2 * pad
    chg = ''.join(f'<path d="{path(r[3])}"/>' for r in pair['regs'])

    def svg(k, cls, label):
        areas = ''.join(f'<path d="{path(e)}" fill="{col[n]}"><title>{n}</title></path>' for n, e in pl[k]['poly'].items())
        return (f'<svg class="{cls}" viewBox="{x0:.0f} {y0:.0f} {w:.0f} {h:.0f}" role="img" aria-label="Elementary attendance areas, {label}">'
                f'<g stroke="#fff" stroke-width="5" stroke-linejoin="round">{areas}</g>'
                f'<g class="chg" fill="none" stroke="#1b2a3a" stroke-width="5" stroke-dasharray="14 8" stroke-linejoin="round">{chg}</g></svg>')

    data = {'left': svg(LEFT, 'ba-l', 'current best example we modeled'), 'right': svg(RIGHT, 'ba-r', 'PPS A'),
            'n': pair['n'], 'ar': round(w / h, 3)}
    with open(OUT, 'w') as f:
        f.write('window.LANDING_BA=' + json.dumps(data, separators=(',', ':')) + ';\n')
    print(f'landing_ba: {OUT} ({os.path.getsize(OUT) // 1024} KB), {pair["n"]:,} kids in changed areas')


if __name__ == '__main__':
    main()
