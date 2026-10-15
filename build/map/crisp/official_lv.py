"""Official (PPS-drawn) lines for Today, Status Quo 2027-28, PPS Scenario A and B at every level.
Generalizes build/map/official.py (K-5 A/B) to all plans x levels:
- traced polygons: build/data/scenario_maps/<plan>_<level>.geojson (PPS 2027-28 map PDFs, BoardBook);
  Today: K-5 = today's lines carried by the map page (CUR), 6-8 / 9-12 = build/data/boundaries/current_*.geojson
  (9-12 dissolved by 2025-26 cluster, which is how the solver counts the Jefferson dual-assignment zones);
- nested/overlapping traced polygons: smallest wins; gaps the traces leave (K-8 dashed areas, Skyline inset,
  slivers) are filled with block Voronoi cells labelled by the official block assignment (blocks.parquet).
"""
import collections, json, os
import numpy as np
import shapely
from shapely.geometry import Polygon, shape
from shapely.ops import unary_union

from geo import KIT, MX, LAT_M, to_m, district, voronoi_cells, page, grab, dec

COL = {'today': {'K-5': 'es_cur', '6-8': 'ms_cur', '9-12': 'hs_cluster_cur'},
       'status_quo': {'K-5': 'sq_es', '6-8': 'sq_ms', '9-12': 'sq_hs'},
       'scenario_A': {'K-5': 'A_es', '6-8': 'A_ms', '9-12': 'A_hs'},
       'scenario_B': {'K-5': 'B_es', '6-8': 'B_ms', '9-12': 'B_hs'}}
SOURCE = {'today': {'K-5': 'build/data/boundaries/current_K-5_K-8.geojson',
                    '6-8': 'build/data/boundaries/current_6-8.geojson',
                    '9-12': 'build/data/boundaries/current_9-12.geojson'}}
for p in ('status_quo', 'scenario_A', 'scenario_B'):
    SOURCE[p] = {lv: 'build/data/scenario_maps/%s_%s.geojson' % (p, lv) for lv in ('K-5', '6-8', '9-12')}


def traced(plan, lv):
    if plan == 'today' and lv == 'K-5':
        cur = grab(page(), 'const CUR=`', '`;\nconst RD')
        by = collections.defaultdict(list)
        for l in cur.strip().split('\n'):
            n, r = l.split('~')
            by[n].extend(dec(r))
        out = []
        for n, rings in by.items():
            g = None
            for r in rings:
                if len(r) < 4:
                    continue
                q = Polygon([(x * MX, y * LAT_M) for x, y in r]).buffer(0)
                g = q if g is None else g.symmetric_difference(q)
            out.append((n, g))
        return out
    gj = json.load(open(os.path.join(KIT, SOURCE[plan][lv])))
    out = collections.defaultdict(list)
    for f in gj['features']:
        p = f['properties']
        n = p.get('label') or p.get('cluster_2025_26') or p.get('school')
        if plan == 'today' and lv == '9-12':
            n = p['cluster_2025_26']
        out[n].append(to_m(shape(f['geometry'])).buffer(0))
    return [(n, unary_union(v)) for n, v in out.items()]


def build(plan, lv, asg):
    """asg: official block assignment (list of names, block order). Returns {school: geometry (m)}."""
    dist = district(); cells = voronoi_cells()
    tr = [(n, g) for n, g in traced(plan, lv) if g is not None and not g.is_empty]
    # unlabeled traced polygons (e.g. one in status_quo 9-12): name by the majority official school of its blocks
    if any(n is None for n, g in tr):
        from geo import block_xy
        pts = shapely.points(block_xy()); asg_a = np.asarray(asg, dtype=object)
        fixed = []
        for n, g in tr:
            if n is None:
                inside = shapely.contains(g, pts)
                c = collections.Counter(asg_a[inside])
                if not c:
                    continue
                n = c.most_common(1)[0][0]
            fixed.append((n, g))
        tr = fixed
    tr.sort(key=lambda x: x[1].area)
    taken = Polygon(); parts = collections.defaultdict(list)
    for n, g in tr:
        g2 = g.difference(taken)
        if not g2.is_empty:
            parts[n].append(g2)
        taken = taken.union(g)
    gap = dist.difference(taken.buffer(1))
    gap = gap.buffer(-20).buffer(20) if not gap.is_empty else gap
    if not gap.is_empty:
        cl = np.array(cells, dtype=object)
        hit = shapely.intersects(cl, gap)
        gp = collections.defaultdict(list)
        for i in np.where(hit)[0]:
            ix = cl[i].intersection(gap)
            if not ix.is_empty and ix.area > 400:
                gp[asg[i]].append(ix)
        for n, ps in gp.items():
            parts[n].append(unary_union(ps))
    polys = {}
    for n, ps in parts.items():
        U = unary_union(ps).intersection(dist).buffer(0)
        U = U.buffer(6).buffer(-6).simplify(3.0)
        if U.is_empty:
            continue
        gs = [U] if U.geom_type == 'Polygon' else [g for g in getattr(U, 'geoms', []) if g.geom_type == 'Polygon']
        gs = [g for g in gs if g.area > 800]
        if gs:
            polys[n] = unary_union(gs)
    return polys, round(gap.area / 1e6, 2) if not gap.is_empty else 0.0
