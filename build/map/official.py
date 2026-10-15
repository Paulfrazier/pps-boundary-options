"""Official PPS Scenario A/B (traced from PPS's 2027-28 BoardBook K-5 maps) -> page polygons + metrics.
Inputs (read only): build/data/scenario_maps/scenario_{A,B}_K-5.geojson, build/data/blocks.csv (A_es/B_es official block
assignment, incl. K-8/inset fallback rules), the original page (district outline, old PPS polygons), data/pps-map model."""
import json, collections
import pandas as pd
from shapely.geometry import shape, Polygon, Point, MultiPolygon
from shapely.ops import unary_union, voronoi_diagram
from shapely import STRtree
from common import *
from model_port import *

t = load_page()
OUTL = json.loads(grab(t, 'const OUTL=', ';\nconst CLOSE_A'))
def m(x, y): return (x * KX * LAT_M, y * LAT_M)
from shapely.ops import transform as shp_transform
def to_m(g): return shp_transform(lambda x, y, z=None: (x * KX * LAT_M, y * LAT_M), g)
def to_ll(g): return shp_transform(lambda x, y, z=None: (x / (KX * LAT_M), y / LAT_M), g)

dist = None
for r in dec(OUTL):
    p = Polygon([m(*q) for q in r]).buffer(0)
    dist = p if dist is None else dist.symmetric_difference(p)

blocks = pd.read_csv(os.path.join(KIT, 'build', 'data', 'blocks.csv'), usecols=['idx', 'x', 'y', 'A_es', 'B_es', 'A_es_how', 'B_es_how'])
pts = [Point(*m(x, y)) for x, y in zip(blocks.x, blocks.y)]

def build(sc):
    col = sc + '_es'; asg = list(blocks[col])
    gj = json.load(open(os.path.join(KIT, 'build', 'data', 'scenario_maps', 'scenario_%s_K-5.geojson' % sc)))
    traced = [(f['properties']['label'], to_m(shape(f['geometry'])).buffer(0)) for f in gj['features']]
    # nested/overlapping polygons: smallest wins (matches how the block assignment was made)
    traced.sort(key=lambda x: x[1].area)
    taken = Polygon(); parts = collections.defaultdict(list)
    for n, g in traced:
        g2 = g.difference(taken)
        if not g2.is_empty: parts[n].append(g2)
        taken = taken.union(g)
    covered = taken
    # gaps (K-8 dashed areas, Skyline inset, slivers): nearest-block voronoi cell, school from official block assignment
    gap = dist.difference(covered.buffer(1))
    gap = gap.buffer(-20).buffer(20) if not gap.is_empty else gap
    from shapely import MultiPoint
    vor = voronoi_diagram(MultiPoint(pts), envelope=dist.buffer(5000))
    cells = list(vor.geoms); tree = STRtree(cells)
    gaparea = collections.Counter()
    for i, p in enumerate(pts):
        pass
    cellof = {}
    for j in tree.query(MultiPoint(pts).envelope.buffer(0)):
        pass
    for i, p in enumerate(pts):
        for j in tree.query(p, predicate='within'):
            cellof[j] = asg[i]; break
    gp = collections.defaultdict(list)
    for j, n in cellof.items():
        ix = cells[j].intersection(gap)
        if not ix.is_empty and ix.area > 400: gp[n].append(ix)
    for n, ps in gp.items(): parts[n].append(unary_union(ps))
    polys = {}
    for n, ps in parts.items():
        U = unary_union(ps).intersection(dist).buffer(0)
        U = U.buffer(6).buffer(-6).simplify(3.0)
        if U.is_empty: continue
        gs = [U] if U.geom_type == 'Polygon' else list(U.geoms)
        gs = [g for g in gs if g.area > 800]
        if gs: polys[n] = unary_union(gs)
    # cross-check: official block assignment vs final polygons
    names = list(polys); tr = STRtree([polys[n] for n in names]); bad = 0; badw = 0.0; none = 0
    for i, p in enumerate(pts):
        hit = [names[j] for j in tr.query(p, predicate='within')]
        if not hit: none += 1; continue
        if hit[0] != asg[i]: bad += 1; badw += BL[i]['s']
    print(sc, 'schools', len(polys), 'blocks outside polygons', none, 'blocks in other school polygon', bad, 'students', round(badw), 'gap km2', round(gap.area / 1e6, 2))
    return polys

def enc_poly(g):
    rings = []
    for p in ([g] if g.geom_type == 'Polygon' else g.geoms):
        for r in [p.exterior] + list(p.interiors):
            e = enc_ring(list(to_ll(r).coords))
            if e: rings.append(e)
    return '|'.join(rings)

if __name__ == '__main__':
    out = {}
    for sc in 'AB':
        P = build(sc); out[sc] = {n: enc_poly(g) for n, g in P.items()}
    json.dump(out, open(os.path.join(WORK, 'official_poly.json'), 'w'), separators=(',', ':'))
    print({k: len(json.dumps(v)) for k, v in out.items()})
