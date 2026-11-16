# Assign street faces to schools.  Usage: python3 assign.py FA [FB FDA]
# Reference partition = S/geo/<X>_fix.json (unsmoothed block-Voronoi polygons after sliver cleanup).
# Each block centroid is labelled with the reference school containing it.
#  - face holding centroids of one school only           -> whole face to that school
#  - face holding no centroid                             -> school with most reference area in it
#  - face holding centroids of 2+ schools ("mixed")       -> split along the reference polygons
# Then per school: union, merge stray unpopulated fragments into the neighbour sharing the most edge.
# Output: <X>_crisp_parts.json (GeoJSON, one feature per school)
import os as _os  # _PPS_MAP_HDR (added by export: repo-relative paths)
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_PPS_MAP = _os.environ.get('PPS_MAP_DIR') or _os.path.join(_HERE, '../../data/pps-map')
import json, pickle, sys, math
import numpy as np
from shapely.geometry import shape, mapping, Point, Polygon, MultiPolygon
from shapely.ops import unary_union
from shapely import STRtree, set_precision
S = (_os.environ.get('CRISP_WORKDIR') or _os.path.join(_HERE, '..'))
D = json.load(open(_os.path.join(_PPS_MAP, 'pps-model.json')))
BL = D['BL']
kx = math.cos(math.radians(45.54))
km2 = lambda g: g.area * kx * 111.2 * 111.2
faces = pickle.load(open(f'{S}/crisp/faces.pkl', 'rb'))
ftree = STRtree(faces)
pts = [Point(b['x'], b['y']) for b in BL]

def polys(g): return [x for x in (g.geoms if hasattr(g, 'geoms') else [g]) if x.geom_type == 'Polygon' and not x.is_empty]

def thin(g):
    # Polsby-Popper compactness in metric-ish coords; < 0.12 = long sliver, or tiny (< 1500 m2)
    a = km2(g) * 1e6; p = g.length * 111200 * 0.85
    return a < 1500 or 4 * math.pi * a / (p * p) < 0.12
DOM = float(__import__("os").environ.get("DOM", "0"))  # an empty face goes whole to a school holding this share of it
for X in sys.argv[1:]:
    ref = {f['properties']['name']: shape(f['geometry']).buffer(0) for f in json.load(open(f'{S}/geo/{X}_fix.json'))['features']}
    # _fix may hold several features per school (exploded parts) -> merge
    R = {}
    for f in json.load(open(f'{S}/geo/{X}_fix.json'))['features']:
        R.setdefault(f['properties']['name'], []).append(shape(f['geometry']).buffer(0))
    ref = {n: unary_union(v) for n, v in R.items()}
    names = sorted(ref); rtree = STRtree([ref[n] for n in names])
    lab = []
    for p in pts:
        c = [names[j] for j in rtree.query(p) if ref[names[j]].covers(p)]
        lab.append(c[0] if c else None)
    print(X, 'unlabelled blocks', sum(l is None for l in lab))
    fsch = [dict() for _ in faces]  # face -> {school: students+eps}
    for i, p in enumerate(pts):
        if lab[i] is None: continue
        for j in ftree.query(p):
            if faces[j].covers(p):
                d = fsch[j]; d[lab[i]] = d.get(lab[i], 0) + BL[i]['s'] + 1e-3; break
    pieces = {n: [] for n in names}
    nmixed = 0; mixed_area = 0; nsplit = 0; deferred = []
    for j, fc in enumerate(faces):
        d = fsch[j]
        if len(d) == 1:
            pieces[next(iter(d))].append(fc); continue
        ov = {names[k]: fc.intersection(ref[names[k]]) for k in rtree.query(fc)}
        ov = {n: g for n, g in ov.items() if not g.is_empty and g.area > 0}
        if not d:
            if not ov: continue
            if thin(fc): deferred.append(j); continue
            top = max(ov, key=lambda n: ov[n].area)
            if ov[top].area >= DOM * fc.area: pieces[top].append(fc)
            else:
                nsplit += 1
                for n, g in ov.items(): pieces[n].append(g)
            continue
        nmixed += 1; mixed_area += km2(fc)
        # split exactly along the reference polygons
        for n, g in ov.items(): pieces[n].append(g)
    # thin empty faces (slivers between parallel streets/rail/today's lines, road strips) join the
    # school they share the most border with, so they don't poke spikes into a neighbour
    owner = {}
    for n, v in pieces.items():
        for g in v: owner.setdefault(id(g), n)
    asg_t = STRtree([g for v in pieces.values() for g in v]); asg_n = [n for n, v in pieces.items() for g in v]
    asg_g = [g for v in pieces.values() for g in v]
    left = deferred[:]
    while left:
        nxt = []; done = []
        for j in left:
            fc = faces[j]; fb = fc.boundary; L = {}
            for k in asg_t.query(fc.buffer(1e-6)):
                l = fb.intersection(asg_g[k].buffer(1e-6)).length
                if l > 0: L[asg_n[k]] = L.get(asg_n[k], 0) + l
            for (jj, m) in done:
                pass
            if L: done.append((j, max(L, key=L.get)))
            else: nxt.append(j)
        if not done: break
        for j, m in done:
            pieces[m].append(faces[j]); asg_g.append(faces[j]); asg_n.append(m)
        asg_t = STRtree(asg_g)
        left = nxt
    print(X, 'thin empty faces', len(deferred), 'unresolved', len(left))
    print(X, 'empty faces split', nsplit, 'mixed faces', nmixed, f'{mixed_area:.2f} km2')
    # ---- atoms + reconnect pass -------------------------------------------------------------
    A = [[n, h] for n, v in pieces.items() for g in v for h in polys(g)]
    import heapq
    PEN = 2e-5   # extra cost (deg^2, ~0.1 km2) for routing a corridor through a populated atom
    for rnd in range(4):
        atree = STRtree([a[1] for a in A])
        apop = [dict() for _ in A]          # atom -> {ref school: students} of centres inside
        for i, p in enumerate(pts):
            if lab[i] is None: continue
            for k in atree.query(p):
                if A[k][1].covers(p): apop[k][lab[i]] = apop[k].get(lab[i], 0) + BL[i]['s'] + 1e-3; break
        nbr = [set() for _ in A]
        for k, (n, g) in enumerate(A):
            gb = g.boundary.buffer(2e-7)
            for j in atree.query(g, predicate='intersects'):
                if j > k and gb.intersection(A[j][1].boundary).length > 2e-6:
                    nbr[k].add(int(j)); nbr[int(j)].add(k)
        def comps(n):
            seen, out = set(), []
            for k in range(len(A)):
                if A[k][0] != n or k in seen: continue
                st, c = [k], []
                seen.add(k)
                while st:
                    u = st.pop(); c.append(u)
                    for v in nbr[u]:
                        if v not in seen and A[v][0] == n: seen.add(v); st.append(v)
                out.append(c)
            return out
        split = set()
        for n in names:
            refc = polys(ref[n])
            cs = comps(n)
            if len(cs) <= len(refc): continue
            main = set()
            for r in refc:
                main.add(max(range(len(cs)), key=lambda c: sum(A[k][1].intersection(r).area for k in cs[c])))
            target = set(k for c in main for k in cs[c])
            for ci, c in enumerate(cs):
                if ci in main: continue
                if sum(sum(apop[k].values()) for k in c) < 0.01: continue   # empty: frag.py merges it
                # Dijkstra to the main piece: free through n's own atoms, cheap through empty atoms
                # (preferring n's reference area), expensive through atoms holding other schools' blocks
                dist = {k: 0.0 for k in c}; prev = {}; h = [(0.0, k) for k in c]; hit = None
                while h:
                    dd, u = heapq.heappop(h)
                    if dd > dist.get(u, 1e18): continue
                    if u in target: hit = u; break
                    for v in nbr[u]:
                        if v in split: continue
                        g = A[v][1]
                        if A[v][0] == n: w = 0.0
                        else:
                            sh = g.intersection(ref[n]).area / g.area
                            if any(m != n for m in apop[v]):
                                if sh < 1e-3: continue
                                w = g.area * (1.05 - sh) + PEN
                            else: w = g.area * (1.05 - sh)
                        if dd + w < dist.get(v, 1e18): dist[v] = dd + w; prev[v] = u; heapq.heappush(h, (dd + w, v))
                if hit is None:
                    print(X, f'cannot reconnect {n} piece ({sum(sum(apop[k].values()) for k in c):.1f} students)'); continue
                u = hit; path = []
                while u in prev: u = prev[u]; path.append(u)
                flips = [k for k in path if A[k][0] != n and not any(m != n for m in apop[k])]
                cuts = [k for k in path if A[k][0] != n and any(m != n for m in apop[k])]
                for k in flips: A[k][0] = n
                split.update(cuts)
                print(X, f'reconnect {n}: flipped {len(flips)} empty atoms ({sum(km2(A[k][1]) for k in flips):.4f} km2), reference-split {len(cuts)} populated atoms')
        if not split: break
        B2 = []
        for k, (n, g) in enumerate(A):
            if k not in split: B2.append([n, g]); continue
            rest = g
            for j in rtree.query(g):
                m = names[j]; q = g.intersection(ref[m])
                for hh in polys(q): B2.append([m, hh])
        A = B2
    feats = [{"type": "Feature", "properties": {"name": n}, "geometry": mapping(h)} for n, h in A]
    json.dump({"type": "FeatureCollection", "features": feats}, open(f'{S}/crisp/{X}_atoms.json', 'w'))
    json.dump(lab, open(f'{S}/crisp/{X}_reflab.json', 'w'))
    print(X, 'atoms', len(feats))
