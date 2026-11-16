from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union
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
def poly(s):
    # rings: outer rings and holes mixed; use even-odd via symmetric difference
    g = None
    for r in dec(s):
        if len(r) < 3: continue
        p = Polygon(r).buffer(0)
        g = p if g is None else g.symmetric_difference(p)
    return g
