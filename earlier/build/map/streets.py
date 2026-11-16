"""Street-name label anchors for the zoomed-in 'Street names' toggle.
Source: build/routing/osm/portland.osm.pbf (read-only) via `osmium` CLI -> work/st.geojsonseq.
Geometry of the street lines themselves is NOT re-extracted: the page already carries secondary/tertiary/
residential lines (cowork/build/streets.txt, 545 KB); this adds only names, one anchor every ~250-400 m."""
import json, math, subprocess, os, re, collections
from shapely.geometry import LineString, Polygon, Point
from shapely.ops import linemerge, unary_union
from shapely.prepared import prep
from common import *

PBF = os.path.join(KIT, 'build', 'routing', 'osm', 'portland.osm.pbf')
box = os.path.join(WORK, 'box.pbf'); st = os.path.join(WORK, 'st.pbf'); gj = os.path.join(WORK, 'st.geojsonseq')
if not os.path.exists(gj):
    subprocess.check_call(['osmium', 'extract', '-b', '-122.87,45.42,-122.54,45.665', PBF, '-o', box, '--overwrite'])
    subprocess.check_call(['osmium', 'tags-filter', box, 'w/highway=residential,tertiary,secondary', '-o', st, '--overwrite'])
    subprocess.check_call(['osmium', 'export', st, '-f', 'geojsonseq', '-o', gj, '--overwrite', '-x', 'print_record_separator=false'])

t = load_page()
OUTL = grab(t, 'const OUTL=', ';\nconst CLOSE_A') if 'const OUTL=' in t else None
outl = json.loads(OUTL)
KXc = KX
def m(lon, lat): return (lon * KXc * LAT_M, lat * LAT_M)
dist = None
for r in dec(outl):
    p = Polygon([m(*q) for q in r]).buffer(0)
    dist = p if dist is None else dist.symmetric_difference(p)
pd_ = prep(dist)

ABBR = [('Northeast', 'NE'), ('Northwest', 'NW'), ('Southeast', 'SE'), ('Southwest', 'SW'), ('North', 'N'), ('South', 'S'), ('East', 'E'), ('West', 'W'),
        ('Street', 'St'), ('Avenue', 'Ave'), ('Boulevard', 'Blvd'), ('Drive', 'Dr'), ('Court', 'Ct'), ('Place', 'Pl'), ('Road', 'Rd'),
        ('Terrace', 'Ter'), ('Lane', 'Ln'), ('Highway', 'Hwy'), ('Parkway', 'Pkwy'), ('Circle', 'Cir'), ('Way', 'Way'), ('Mount', 'Mt'), ('Saint', 'St')]
def short(n):
    ws = n.split(' ')
    return ' '.join(dict(ABBR).get(x, x) for x in ws)

lines = collections.defaultdict(list)   # (cls,name) -> [LineString m]
for l in open(gj):
    f = json.loads(l)
    if f['geometry']['type'] != 'LineString': continue
    p = f['properties']; h = p.get('highway'); n = p.get('name')
    if not n or h not in ('residential', 'tertiary', 'secondary'): continue
    if '~' in n or '|' in n: continue
    cls = {'residential': 'r', 'tertiary': 't', 'secondary': 's'}[h]
    lines[(cls, short(n))].append(LineString([m(*c) for c in f['geometry']['coordinates']]))

def heading(a, b): return math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
def angdiff(a, b): return abs((a - b + 180) % 360 - 180)

out = collections.defaultdict(list); nanch = collections.Counter()
for (cls, name), ls in lines.items():
    mg = linemerge(ls)
    gs = [mg] if mg.geom_type == 'LineString' else list(mg.geoms)
    step = 250 if cls == 'r' else 400
    for g in gs:
        L = g.length
        if L < 70: continue
        k = max(1, int(L // step)); 
        for i in range(k):
            d = (i + 0.5) * L / k
            p0 = g.interpolate(max(0, d - 25)); p1 = g.interpolate(min(L, d + 25))
            h = heading((p0.x, p0.y), (p1.x, p1.y))
            # straight run in each direction (heading within 18 deg of anchor heading over 20 m chords)
            def run(sign):
                s = 0.0
                while s < 300:
                    a = g.interpolate(min(L, max(0, d + sign * s))); b = g.interpolate(min(L, max(0, d + sign * (s + 20))))
                    if (a.x, a.y) == (b.x, b.y) or angdiff(heading((a.x, a.y), (b.x, b.y)) if sign > 0 else heading((b.x, b.y), (a.x, a.y)), h) > 18: break
                    s += 20
                return s
            r = min(run(1), run(-1)) * 2
            if r < 40: continue
            c = g.interpolate(d)
            if not pd_.contains(Point(c.x, c.y)): continue
            ang = h
            if ang > 90: ang -= 180
            if ang <= -90: ang += 180
            lon, lat = c.x / (KXc * LAT_M), c.y / LAT_M
            out[(cls, name)].append((round(lon * 1e4 + X0), round(lat * 1e4 - Y0), round(ang), min(60, int(r // 10))))
            nanch[cls] += 1
txt = []
for (cls, name), an in sorted(out.items()):
    txt.append(cls + name + '~' + ' '.join('%d,%d,%d,%d' % a for a in an))
s = '\n'.join(txt)
open(os.path.join(WORK, 'street_labels.txt'), 'w').write(s)
print(nanch, len(out), len(s))
