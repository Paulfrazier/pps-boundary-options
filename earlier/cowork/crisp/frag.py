# Keep each school in as many pieces as the reference (today's published) polygons have; give
# every extra fragment to the neighbour it shares the most border with.  Reports students moved.
# Usage: python3 frag.py FA   (reads FA_cparts.json, writes FA_cfix.json + FA_frag.json)
import os as _os  # _PPS_MAP_HDR (added by export: repo-relative paths)
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_PPS_MAP = _os.environ.get('PPS_MAP_DIR') or _os.path.join(_HERE, '../../data/pps-map')
import json, sys, math
from shapely.geometry import shape, mapping, Point
from shapely import STRtree
S = (_os.environ.get('CRISP_WORKDIR') or _os.path.join(_HERE, '..'))
D = json.load(open(_os.path.join(_PPS_MAP, 'pps-model.json'))); BL = D['BL']
kx = math.cos(math.radians(45.54)); km2 = lambda g: g.area * kx * 111.2 * 111.2
for X in sys.argv[1:]:
    parts = [[f['properties']['name'], shape(f['geometry']).buffer(0)] for f in json.load(open(f'{S}/crisp/{X}_cparts.json'))['features']]
    ref = [(f['properties']['name'], shape(f['geometry'])) for f in json.load(open(f'{S}/geo/{X}_fix.json'))['features']]
    keep = set()
    for n, r in ref:
        c = [(p[1].intersection(r).area, k) for k, p in enumerate(parts) if p[0] == n]
        if c: keep.add(max(c)[1])
    pts = [Point(b['x'], b['y']) for b in BL]; tree = STRtree(pts)
    moved = []
    frag = [k for k in range(len(parts)) if k not in keep]
    frag.sort(key=lambda k: parts[k][1].area)
    for k in frag:
        n, g = parts[k]
        best, bl = None, 0
        for j, (m, h) in enumerate(parts):
            if m == n or j == k: continue
            L = g.boundary.intersection(h.buffer(2e-6)).length
            if L > bl: best, bl = m, L
        blocks = [int(i) for i in tree.query(g) if g.contains(pts[i])]
        st = sum(BL[i]['s'] for i in blocks)
        print(X, f'fragment {n} -> {best}: {km2(g):.4f} km2, {len(blocks)} block centres, {st:.1f} students')
        moved.append({'from': n, 'to': best, 'km2': km2(g), 'blocks': blocks, 'students': st})
        parts[k][0] = best
    json.dump({"type": "FeatureCollection", "features": [{"type": "Feature", "properties": {"name": n}, "geometry": mapping(g)} for n, g in parts]}, open(f'{S}/crisp/{X}_cfix.json', 'w'))
    json.dump(moved, open(f'{S}/crisp/{X}_frag.json', 'w'))
