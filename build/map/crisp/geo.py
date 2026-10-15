"""Shared geometry for the site map build: metric projection, district outline, block centres,
block Voronoi cells, and the "atom" partition used by the crisp street-following lines.

Atoms = the district cut by every line a boundary may follow (secondary/tertiary/residential streets,
freeways, primary streets, rail, today's PPS lines at all three levels, the district outline and the
hard-edge zone lines from pps-model.json) AND by the Voronoi cell edges of the 9,295 Census-block centres.
Every atom knows its street face and its Voronoi cell (block), so any block-level assignment can be turned
into street-following polygons by table lookups plus an exact coverage union (crisp/crisp.py).

Built once and cached in build/map/work/site_cache/atoms.pkl (inputs are fixed Phase 1 files).
All inputs are read only: pages/pps-walk-redraw.html (streets, base layers, today's K-5 lines, outline),
build/data/boundaries/current_{6-8,9-12}.geojson, build/data/blocks.parquet, data/pps-map/pps-model.json.
"""
import os as _os  # _PPS_MAP_HDR (added by export: repo-relative paths)
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_PPS_MAP = _os.environ.get('PPS_MAP_DIR') or _os.path.join(_HERE, '../../../data/pps-map')
import json, math, os, pickle, sys, time
import numpy as np
import pandas as pd
import shapely
from shapely.geometry import Polygon, LineString, MultiPoint, Point, shape
from shapely.ops import unary_union, polygonize

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from common import KIT, WORK, KX, LAT_M, grab, load_page, dec  # noqa: E402

CACHE = os.path.join(WORK, 'site_cache')
os.makedirs(CACHE, exist_ok=True)
MX = KX * LAT_M          # metres per degree longitude (local equirectangular, as official.py)


def to_m(g):
    return shapely.transform(g, lambda c: c * np.array([MX, LAT_M]))


def to_ll(g):
    return shapely.transform(g, lambda c: c / np.array([MX, LAT_M]))


_page = None


def page():
    global _page
    if _page is None:
        _page = load_page()
    return _page


def district():
    """District outline polygon in metres (even-odd rings of the page's OUTL)."""
    p = os.path.join(CACHE, 'district.pkl')
    if os.path.exists(p):
        return pickle.load(open(p, 'rb'))
    outl = json.loads(grab(page(), 'const OUTL=', ';\nconst CLOSE_A'))
    d = None
    for r in dec(outl):
        q = Polygon([(x * MX, y * LAT_M) for x, y in r]).buffer(0)
        d = q if d is None else d.symmetric_difference(q)
    pickle.dump(d, open(p, 'wb'))
    return d


def blocks():
    return pd.read_parquet(os.path.join(KIT, 'build', 'data', 'blocks.parquet'))


def block_xy():
    b = blocks()
    return np.c_[b.x.values * MX, b.y.values * LAT_M]


def voronoi_cells():
    """list (block order) of Voronoi cells clipped to the district, metres."""
    p = os.path.join(CACHE, 'cells.pkl')
    if os.path.exists(p):
        return pickle.load(open(p, 'rb'))
    xy = block_xy(); dist = district()
    pts = shapely.points(xy)
    vor = shapely.voronoi_polygons(MultiPoint(list(pts)), extend_to=dist.buffer(5000))
    cells = list(vor.geoms)
    tree = shapely.STRtree(cells)
    idx = tree.query(pts, predicate='within')       # (2, n): [point i, cell j]
    out = [None] * len(xy)
    for i, j in zip(*idx):
        if out[i] is None:
            out[i] = cells[j]
    out = [shapely.intersection(c, dist) if c is not None else Polygon() for c in out]
    pickle.dump(out, open(p, 'wb'))
    return out


def _line_sets():
    t = page()
    base = {}
    i = t.index('const BASE=`') + len('const BASE=`')
    for l in t[i:t.index('`', i)].split('\n'):
        if '#' in l:
            k, v = l.split('#', 1); base[k] = v
    st = {}
    i = t.index('const STREETS=`') + len('const STREETS=`')
    for l in t[i:t.index('`', i)].split('\n'):
        if '#' in l:
            k, v = l.split('#', 1); st[k] = v
    cur = grab(t, 'const CUR=`', '`;\nconst RD')
    lines = []
    def add(rings, closed=False):
        for r in rings:
            q = [(x * MX, y * LAT_M) for x, y in r]
            if closed and q[0] != q[-1]:
                q = q + [q[0]]
            if len(q) > 1 and len(set(q)) > 1:
                lines.append(LineString(q))
    for k in ('s', 't', 'r'):
        add(dec(st[k]))
    for k in ('motorway', 'trunk', 'primary', 'rail'):
        add(dec(base[k]))
    for l in cur.strip().split('\n'):
        add(dec(l.split('~', 1)[1]), closed=True)
    for lv in ('6-8', '9-12'):
        g = json.load(open(os.path.join(KIT, 'build', 'data', 'boundaries', 'current_%s.geojson' % lv)))
        for f in g['features']:
            geom = to_m(shape(f['geometry']))
            lines.append(geom.boundary)
    M = json.load(open(_os.path.join(_PPS_MAP, 'pps-model.json')))
    for z, c in M['ZP'].items():
        for poly in c:
            for r in poly:
                add([[tuple(p) for p in r]], closed=True)
    return lines


def atoms():
    """dict with atom geometries + lookups (cached)."""
    p = os.path.join(CACHE, 'atoms.pkl')
    if os.path.exists(p):
        return pickle.load(open(p, 'rb'))
    t0 = time.time()
    dist = district(); cells = voronoi_cells(); xy = block_xy()
    clip = dist.buffer(50)
    lines = [shapely.intersection(l, clip) for l in _line_sets()]
    lines.append(dist.boundary)
    face_lines = unary_union([l for l in lines if not l.is_empty])
    print('face lines noded', round(time.time() - t0, 1), 's')
    faces = []
    for g in polygonize(face_lines.geoms if hasattr(face_lines, 'geoms') else [face_lines]):
        q = g.intersection(dist)
        for h in (q.geoms if hasattr(q, 'geoms') else [q]):
            if h.geom_type == 'Polygon' and h.area > 0.5:
                faces.append(h)
    rest = dist.difference(unary_union(faces))
    for h in (rest.geoms if hasattr(rest, 'geoms') else [rest]):
        if h.geom_type == 'Polygon' and h.area > 0.5:
            faces.append(h)
    print('faces', len(faces), round(time.time() - t0, 1), 's; area check', round(sum(f.area for f in faces) / dist.area, 6))
    # atoms: node face lines + Voronoi cell edges together
    cell_edges = unary_union([c.boundary for c in cells if not c.is_empty])
    allm = unary_union([face_lines, cell_edges])
    edges = list(allm.geoms)
    print('all lines noded', len(edges), round(time.time() - t0, 1), 's')
    A = []
    for g in polygonize(edges):
        if g.area < 1e-3:
            continue
        A.append(g)
    A = np.array(A, dtype=object)
    rp = shapely.point_on_surface(A)
    inside = shapely.contains(dist, rp)
    A = A[inside]; rp = rp[inside]
    print('atoms', len(A), round(time.time() - t0, 1), 's; area check', round(shapely.area(A).sum() / dist.area, 6))
    ftree = shapely.STRtree(faces)
    q = ftree.query(rp, predicate='within')
    face_of = np.full(len(A), -1); face_of[q[0]] = q[1]
    ctree = shapely.STRtree(cells)
    q = ctree.query(rp, predicate='within')
    cell_of = np.full(len(A), -1); cell_of[q[0]] = q[1]
    # fallbacks (rep point on a cell edge etc.): nearest
    for arr, tree in ((face_of, ftree), (cell_of, ctree)):
        bad = np.where(arr < 0)[0]
        if len(bad):
            arr[bad] = tree.query_nearest(rp[bad], return_distance=False)[1]
    # block centre -> atom
    atree = shapely.STRtree(A)
    pts = shapely.points(xy)
    q = atree.query(pts, predicate='within')
    centre_atom = np.full(len(xy), -1); centre_atom[q[0]] = q[1]
    bad = np.where(centre_atom < 0)[0]
    if len(bad):
        centre_atom[bad] = atree.query_nearest(pts[bad], return_distance=False)[1]
    print('block centres not strictly inside an atom (nearest used):', len(bad))
    # atom adjacency with shared edge length: probe both sides of every noded edge
    mids = shapely.line_interpolate_point(np.array(edges, dtype=object), 0.5, normalized=True)
    a0 = shapely.line_interpolate_point(np.array(edges, dtype=object), 0.49, normalized=True)
    a1 = shapely.line_interpolate_point(np.array(edges, dtype=object), 0.51, normalized=True)
    mx, my = shapely.get_x(mids), shapely.get_y(mids)
    dx = shapely.get_x(a1) - shapely.get_x(a0); dy = shapely.get_y(a1) - shapely.get_y(a0)
    nn = np.hypot(dx, dy); nn[nn == 0] = 1
    ox, oy = -dy / nn * 0.02, dx / nn * 0.02
    L = shapely.length(np.array(edges, dtype=object))
    side = []
    for sgn in (1, -1):
        pp = shapely.points(np.c_[mx + sgn * ox, my + sgn * oy])
        q = atree.query(pp, predicate='within')
        s = np.full(len(edges), -1); s[q[0]] = q[1]; side.append(s)
    ok = (side[0] >= 0) & (side[1] >= 0) & (side[0] != side[1])
    adj = {}
    for a, b, l in zip(side[0][ok], side[1][ok], L[ok]):
        k = (min(a, b), max(a, b)); adj[k] = adj.get(k, 0.0) + float(l)
    print('adjacent atom pairs', len(adj), round(time.time() - t0, 1), 's')
    # thin faces (slivers between parallel lines / road strips)
    fa = np.array([f.area for f in faces]); fl = np.array([f.length for f in faces])
    thin = (fa < 1500) | (4 * math.pi * fa / np.maximum(fl * fl, 1e-9) < 0.12)
    res = dict(atoms=A, area=shapely.area(A), face_of=face_of, cell_of=cell_of, centre_atom=centre_atom,
               adj=adj, n_faces=len(faces), face_thin=thin, faces=faces)
    pickle.dump(res, open(p, 'wb'))
    print('atoms cached', round(time.time() - t0, 1), 's')
    return res


if __name__ == '__main__':
    a = atoms()
    print(len(a['atoms']), a['n_faces'])
