"""Compare data: per-plan school sizes, per-pair student flows, per-pair 'differing area' polygons.
Reads: original page (plan polygons), cowork/model/final_asg.json (block assignment for A/B/DA),
build/data/blocks.csv (block centroids + modeled neighborhood K-5 students).  All read-only."""
import json, itertools, collections, math
import pandas as pd
from shapely.geometry import Polygon, MultiPolygon, Point
from shapely.ops import unary_union
from shapely.prepared import prep
from shapely import STRtree
from common import *

t = load_page()
RD = json.loads(grab(t, 'const RD=', ';\nconst SCH='))
PPSP = json.loads(grab(t, 'const PPSP=', ';\nconst STREETS'))
CUR = grab(t, 'const CUR=`', '`;\nconst RD')
CURP = {}
for l in CUR.strip().split('\n'):
    n, r = l.split('~'); CURP[n] = CURP[n] + '|' + r if n in CURP else r
PLANS = {'T': CURP, 'PA': PPSP['A'], 'PB': PPSP['B'], 'A': RD['A']['poly'], 'B': RD['B']['poly'], 'DA': RD['DA']['poly']}
# official PPS A/B: traced polygons (official.py) and block assignment (official_stats.py), replacing the page's old reconstruction
OFF = json.load(open(os.path.join(WORK, 'official_poly.json'))); OFFS = json.load(open(os.path.join(WORK, 'official.json')))
PLANS['PA'] = OFF['A']; PLANS['PB'] = OFF['B']
ORDER = ['T', 'PA', 'PB', 'A', 'B', 'DA']
KXc = KX

def to_m(ring): return [(x * KXc * LAT_M, y * LAT_M) for x, y in ring]
def from_m(g): return g

def school_geom(enc):
    """encoded multi-ring (even-odd) -> shapely geometry in metres"""
    g = None
    for ring in dec(enc):
        if len(ring) < 4: continue
        p = Polygon(to_m(ring))
        if not p.is_valid: p = p.buffer(0)
        g = p if g is None else g.symmetric_difference(p)
    return g

geoms = {k: {n: school_geom(e) for n, e in v.items()} for k, v in PLANS.items()}

# ---- blocks
b = pd.read_csv(os.path.join(KIT, 'build', 'data', 'blocks.csv'), usecols=['idx', 'x', 'y', 's_model'])
fa = json.load(open(os.path.join(KIT, 'cowork', 'model', 'final_asg.json')))
pts = [Point(x * KXc * LAT_M, y * LAT_M) for x, y in zip(b.x, b.y)]
w = b.s_model.values

def pip_assign(plan):
    names = list(geoms[plan]); gs = [geoms[plan][n] for n in names]
    tree = STRtree(gs); res = [None] * len(pts)
    for i, p in enumerate(pts):
        for j in tree.query(p, predicate='within'):
            res[i] = names[j]; break
    return res

ASG = {k: fa[k] for k in ('A', 'B', 'DA')}
ASG['T'] = pip_assign('T'); ASG['PA'] = OFFS['asg']['A']; ASG['PB'] = OFFS['asg']['B']
for k in ORDER:
    unas = sum(w[i] for i, a in enumerate(ASG[k]) if a is None)
    print(k, 'students', round(sum(w)), 'unassigned', round(unas, 1))

sizes = {k: {} for k in ORDER}
for k in ORDER:
    c = collections.Counter()
    for a, ww in zip(ASG[k], w):
        if a is not None: c[a] += ww
    sizes[k] = {n: round(v) for n, v in c.items() if round(v) > 0}

pairs = {}
OPEN = 14.0   # metres: morphological opening removes slivers where two plans trace the same street
MINA = 3000.0  # m^2
for a, c in itertools.combinations(ORDER, 2):
    flows = collections.Counter(); diff = 0.0
    for x, y, ww in zip(ASG[a], ASG[c], w):
        if x is not None and y is not None and x != y: flows[(x, y)] += ww; diff += ww
    # changed regions grouped by (school in plan a, school in plan c); each group dissolved, slivers dropped
    groups = collections.defaultdict(list)
    ga = geoms[a]; gc = geoms[c]
    tree = STRtree(list(gc.values())); cn = list(gc)
    for n, g in ga.items():
        for j in tree.query(g):
            m = cn[j]
            if m == n: continue
            ix = g.intersection(gc[m])
            if not ix.is_empty and ix.area > 1: groups[(n, m)].append(ix)
    regs = []; tot_area = 0.0
    for (n, m), parts in groups.items():
        if round(flows.get((n, m), 0)) < 1: continue   # area-only changes (no students) are not outlined
        U = unary_union(parts).buffer(-OPEN).buffer(OPEN).simplify(4.0)
        polys = [U] if U.geom_type == 'Polygon' else list(getattr(U, 'geoms', []))
        polys = [p for p in polys if p.area >= MINA]
        for p in polys:
            rings = []
            for r in [p.exterior] + list(p.interiors):
                ll = [(x / (KXc * LAT_M), y / LAT_M) for x, y in r.coords]
                e = enc_ring(ll)
                if e: rings.append(e)
            if rings:
                # n = students moving from->to across the whole group
                regs.append([n, m, round(flows.get((n, m), 0)), '|'.join(rings), p.area])
                tot_area += p.area
    fl = sorted(([x, y, round(v)] for (x, y), v in flows.items() if round(v) >= 3), key=lambda r: -r[2])[:100]
    pairs['%s|%s' % (a, c)] = {'n': round(diff), 'regs': [r[:4] for r in regs], 'flows': fl,
                               'area_km2': round(tot_area / 1e6, 2)}
    print(a, c, round(diff), len(regs), 0, pairs['%s|%s' % (a, c)]['area_km2'])

json.dump({'sizes': sizes, 'total': round(sum(w)), 'pairs': pairs}, open(os.path.join(WORK, 'compare.json'), 'w'), separators=(',', ':'))
print(os.path.getsize(os.path.join(WORK, 'compare.json')))
