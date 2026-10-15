# Build the street "face" partition of the district: every street / rail / freeway / river /
# today's PPS boundary line / zone edge is noded and polygonized; faces are clipped to the outline.
# Output: faces.pkl (list of shapely polygons, lon/lat)
import os as _os  # _PPS_MAP_HDR (added by export: repo-relative paths)
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_PPS_MAP = _os.environ.get('PPS_MAP_DIR') or _os.path.join(_HERE, '../../data/pps-map')
import json, pickle, re, sys
from shapely.geometry import Polygon, LineString, MultiLineString
from shapely.ops import unary_union, polygonize
from shapely import set_precision, STRtree
S = (_os.environ.get('CRISP_WORKDIR') or _os.path.join(_HERE, '..'))
D = json.load(open(_os.path.join(_PPS_MAP, 'pps-model.json')))

def dec(s):
    out = []
    for rr in s.split('|'):
        rr = rr.strip()
        if not rr: continue
        X = Y = 0; pts = []
        for i, p in enumerate(rr.split(' ')):
            a, b = map(int, p.split(','))
            if i == 0: X, Y = a, b
            else: X += a; Y += b
            pts.append(((X - 1229300) / 1e4, (Y + 454300) / 1e4))
        out.append(pts)
    return out

def mp(c): return unary_union([Polygon(p[0], p[1:]).buffer(0) for p in c])
outl = mp(D['OUTLINE'])
lines = []
def add(polys, kind):
    n = 0
    for r in polys:
        if len(r) > 1 and len(set(r)) > 1:
            lines.append(LineString(r)); n += 1
    print(kind, n)

st = {l.split('#', 1)[0]: l.split('#', 1)[1] for l in open(f'{S}/work/streets.txt').read().strip().split('\n')}
f = open(f'{S}/work/pps-walk-redraw.html').read()
i = f.index('const BASE=`') + 12
base = {l.split('#', 1)[0]: l.split('#', 1)[1] for l in f[i:f.index('`', i)].split('\n') if '#' in l}
for k in 's', 't', 'r': add(dec(st[k]), 'street ' + k)
for k in 'motorway', 'trunk', 'primary', 'rail': add(dec(base[k]), k)
# today's PPS boundaries (exact lines)
for l in open(f'{S}/work/enc.txt'):
    if '~' in l: lines.extend(LineString(r + [r[0]]) for r in dec(l.strip().split('~', 1)[1]) if len(r) > 2)
# district outline + zone polygons (river / I-84 hard edges used by the model)
add([list(outl.exterior.coords)] if outl.geom_type == 'Polygon' else [list(g.exterior.coords) for g in outl.geoms], 'outline')
for z, c in D['ZP'].items():
    g = mp(c)
    for gg in (g.geoms if g.geom_type == 'MultiPolygon' else [g]):
        add([list(gg.exterior.coords)] + [list(r.coords) for r in gg.interiors], 'zone ' + z)
clip = outl.buffer(0.002)
ml = unary_union([l.intersection(clip) for l in lines])  # nodes everything
print('noded', len(ml.geoms))
faces = []
for p in polygonize(ml.geoms):
    q = p.intersection(outl)
    if q.is_empty: continue
    for g in (q.geoms if hasattr(q, 'geoms') else [q]):
        if g.geom_type == 'Polygon' and g.area > 0: faces.append(g)
cov = unary_union(faces)
rest = outl.difference(cov)
for g in (rest.geoms if hasattr(rest, 'geoms') else [rest]):
    if g.geom_type == 'Polygon' and g.area > 1e-10: faces.append(g)
print('faces', len(faces), 'outline area', outl.area, 'sum', sum(g.area for g in faces))
pickle.dump(faces, open(f'{S}/crisp/faces.pkl', 'wb'))
