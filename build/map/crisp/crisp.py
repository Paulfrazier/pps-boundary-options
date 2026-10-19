"""Crisp street-following school areas from a block-level assignment.

Port of the cowork/crisp method (faces.py -> assign.py -> mapshaper dissolve -> frag.py -> topology) to
work directly from solver block assignments (build/solver/out*/<option>/assign_<level>.parquet), with no
mapshaper: the atoms in geo.py already form an exact planar partition, so a coverage union per school gives
shared, gap-free, overlap-free edges by construction, and GEOS coverage_simplify keeps them shared.

Rules (same spirit as cowork/crisp/README.md):
- a street face holding populated block centres of one school only -> whole face to that school;
- a face holding populated centres of 2+ schools ("mixed") -> cut along the block Voronoi lines, so every
  populated block centre stays in its own school;
- an empty face -> school with the most Voronoi (reference) area in it; a thin or tiny empty face
  (sliver between parallel lines) -> the school it shares the most border with;
- cleanup: any piece of a school cut off from its main piece and holding no kids joins the neighbour it
  shares the most border with.
- reconnect pass (cowork/crisp/assign.py): a piece holding kids that is cut off from its school is joined back
  by the cheapest path: empty street faces between them flip to that school; if that is not enough, the
  populated faces on the path are cut along the reference (block Voronoi) line. Kids never change school.
  Pieces the block assignment itself detaches (its Voronoi area is a separate piece) are kept and reported
  as assignment exclaves.
"""
import os
import numpy as np
import shapely
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components, dijkstra

from geo import atoms, to_ll, to_m, block_xy

DEBUG = bool(os.environ.get('CRISP_DEBUG'))
SIMPLIFY_M = 2.0     # coverage simplification tolerance (metres); street geometry is already ~8 m resolution
NECK_M = 10.0       # neck widening reach (metres), about one encoding grid cell
NECK_MAX_M2 = 20000.0   # ...taking only kid-free atoms up to this size
GRID_DEG = 1e-4      # the page's polygon encoding grid (common.enc_ring rounds lon/lat to 1e-4 degree)
SPLIT_SHARE = 0.25   # a kid-free face whose minority reference share is at least this...
SPLIT_M2 = 20000.0   # ...and at least this many m2 is cut on the reference lines, not given whole to the majority


def _groups(keys, n):
    order = np.argsort(keys, kind='stable')
    ks = keys[order]
    starts = np.searchsorted(ks, np.arange(n))
    ends = np.searchsorted(ks, np.arange(n), side='right')
    return [order[s:e] for s, e in zip(starts, ends)]


_AT = None


def _at():
    global _AT
    if _AT is None:
        A = atoms()
        n = len(A['atoms'])
        pairs = np.array(list(A['adj'].keys()), dtype=int)
        lens = np.array(list(A['adj'].values()))
        A['pairs'] = pairs; A['lens'] = lens
        A['face_atoms'] = _groups(A['face_of'], A['n_faces'])
        A['n'] = n
        _AT = A
    return _AT


def crisp(lab, w, verbose=False):
    """lab: array (n_blocks,) of school names; w: kids per block at this level.
    Returns (polys: {school: shapely geometry in metres}, qa: dict)."""
    A = _at()
    n = A['n']; face_of = A['face_of']; cell_of = A['cell_of']; area = A['area']
    lab = np.asarray(lab, dtype=object); w = np.asarray(w, dtype=float)
    names = sorted(set(lab))
    code = {s: k for k, s in enumerate(names)}
    labc = np.array([code[s] for s in lab])
    pop = w > 1e-6
    ca = A['centre_atom']
    # schools of populated centres per face
    fs = {}
    for i in np.where(pop)[0]:
        fs.setdefault(int(face_of[ca[i]]), set()).add(labc[i])
    sch = np.full(n, -1)
    deferred = []; nmixed = 0; nsplit = 0
    for f, at in enumerate(A['face_atoms']):
        if not len(at):
            continue
        s = fs.get(f)
        if s and len(s) == 1:
            sch[at] = next(iter(s))
        elif s:
            nmixed += 1
            sch[at] = labc[cell_of[at]]
        else:
            if A['face_thin'][f]:
                deferred.append(f); continue
            c = labc[cell_of[at]]
            tot = np.bincount(c, weights=area[at], minlength=len(names))
            mx = int(tot.argmax()); minor = tot.sum() - tot[mx]
            if minor >= SPLIT_SHARE * tot.sum() and minor >= SPLIT_M2:
                sch[at] = c; nsplit += 1      # big empty face split between schools (e.g. the Rosa Parks spike into Astor)
            else:
                sch[at] = mx
    # thin empty faces -> school sharing most border
    P = A['pairs']; L = A['lens']
    left = deferred
    for _ in range(50):
        if not left:
            break
        nxt = []; upd = []
        for f in left:
            at = A['face_atoms'][f]; inf = np.zeros(n, bool); inf[at] = True
            m0 = inf[P[:, 0]] & ~inf[P[:, 1]]; m1 = inf[P[:, 1]] & ~inf[P[:, 0]]
            other = np.r_[P[m0, 1], P[m1, 0]]; ll = np.r_[L[m0], L[m1]]
            s = sch[other]; ok = s >= 0
            if not ok.any():
                nxt.append(f); continue
            tot = np.bincount(s[ok], weights=ll[ok], minlength=len(names))
            upd.append((at, int(tot.argmax())))
        if not upd:
            break
        for at, s in upd:
            sch[at] = s
        left = nxt
    for f in left:   # isolated slivers: reference area
        at = A['face_atoms'][f]; c = labc[cell_of[at]]
        sch[at] = int(np.bincount(c, weights=area[at], minlength=len(names)).argmax())
    # kids per atom (populated centres)
    akids = np.bincount(ca[pop], weights=w[pop], minlength=n)
    rl = labc[cell_of]                          # reference (block Voronoi) school of every atom
    face_pop = np.zeros(A['n_faces'], bool); face_pop[list(fs)] = True
    moved = [0]
    log = []
    nrec = {'flipped_faces': 0, 'flipped_km2': 0.0, 'cut_faces': 0}
    rcomp = _comps(rl, P, n)[1]                 # reference pieces (connected same-school Voronoi atoms)
    locked = np.zeros(n, bool)                  # atoms a reconnect already flipped or cut: never flipped whole again
    nrec['rounds'] = 0
    stake = {}
    # 1) reconnect detached populated pieces in the atom graph; 2) draw (dissolve + simplify + snap to the page grid)
    # and widen any neck the snap pinched shut (_necks), one widened school at a time, most kids at stake first.
    # Where two schools' necks cross below the grid only one can be drawn connected: a widening that cuts another
    # school's populated piece off is kept only if that piece holds fewer kids than the widening joins back, and
    # the loser goes back through 1). Repeat (bounded; never re-widen the same atom). What stays pinched is
    # reported as grid_pinched.
    nrep = {'rounds': 0, 'atoms_flipped': 0}
    done = {}                                  # (atom, school) -> times widened (an atom a reconnect cut back may go again, twice)
    for outer in range(10):
        for rnd in range(30):
            _merge_empty(sch, akids, area, P, L, n, len(names), moved)
            nrec['rounds'] += 1
            if not _reconnect(sch, akids, area, rl, rcomp, face_of, face_pop, A, P, n, names, nrec, log, locked):
                break
        _merge_empty(sch, akids, area, P, L, n, len(names), moved)
        gnames, simp, snapq = _draw(sch, names, A)
        grow, stake = _necks(sch, akids, gnames, simp, names, A, P, n, np.where(pop)[0])
        grow = np.array([g for g in grow if done.get((int(g[0]), int(g[1])), 0) < 3], dtype=int).reshape(-1, 2)
        if not len(grow):
            break
        npc, lk = _npieces(sch, akids, P, n, len(names), True); kept = []
        for t in sorted(np.unique(grow[:, 1]), key=lambda t: -stake.get(int(t), 0.0)):
            gg = grow[grow[:, 1] == t]; before = sch[gg[:, 0]].copy()
            sch[gg[:, 0]] = t
            npc2, lk2 = _npieces(sch, akids, P, n, len(names), True)
            hurt = np.where((npc2 > npc) & (np.arange(len(names)) != t))[0]
            if len(hurt) and max(lk2[h] - lk[h] for h in hurt) >= stake.get(int(t), 0.0):
                if DEBUG:
                    print('neck', names[t], round(stake.get(int(t), 0), 1), len(gg), 'would cut', [(names[h], round(lk2[h] - lk[h], 1)) for h in hurt])
                sch[gg[:, 0]] = before
            else:
                if DEBUG:
                    print('neck', names[t], round(stake.get(int(t), 0), 1), len(gg), 'kept')
                npc, lk = npc2, lk2; kept.append(gg)
                for a_, b_ in gg:
                    done[(int(a_), int(b_))] = done.get((int(a_), int(b_)), 0) + 1
        if not kept:
            break
        grow = np.concatenate(kept); locked[grow[:, 0]] = True
        nrep['rounds'] += 1; nrep['atoms_flipped'] += len(grow)
    else:                                      # out of rounds right after a widening: reconnect once more, redraw
        for rnd in range(30):
            _merge_empty(sch, akids, area, P, L, n, len(names), moved)
            nrec['rounds'] += 1
            if not _reconnect(sch, akids, area, rl, rcomp, face_of, face_pop, A, P, n, names, nrec, log, locked):
                break
        _merge_empty(sch, akids, area, P, L, n, len(names), moved)
        gnames, simp, snapq = _draw(sch, names, A)
        stake = _necks(sch, akids, gnames, simp, names, A, P, n, np.where(pop)[0])[1]
    moved_frag = moved[0]
    polys = dict(zip(gnames, simp))
    # final components -> exclave report
    exclaves = []
    nc, comp = _comps(sch, P, n)
    ckids = np.bincount(comp, weights=akids, minlength=nc); carea = np.bincount(comp, weights=area, minlength=nc)
    csch = np.full(nc, -1); csch[comp] = sch
    best = {}
    for c in range(nc):
        s = csch[c]
        if s not in best or (ckids[c], carea[c]) > (ckids[best[s]], carea[best[s]]):
            best[s] = c
    mains = _mains(comp, nc, csch, ckids, carea, akids, rcomp, sch)
    for c in range(nc):
        if c != best[csch[c]]:
            at = np.where(comp == c)[0]
            ctr = to_ll(shapely.centroid(shapely.union_all(A['atoms'][at])))
            exclaves.append({'school': names[csch[c]], 'kids': round(float(ckids[c]), 1), 'km2': round(float(carea[c]) / 1e6, 4),
                             'blocks': int(np.isin(ca[pop], at).sum()), 'lonlat': [round(ctr.x, 5), round(ctr.y, 5)],
                             # true = the block assignment itself is detached here (its Voronoi area is a separate piece)
                             'assignment_exclave': bool(c in mains)})
    qa = {'split_empty_faces': nsplit, 'mixed_faces': nmixed, 'thin_empty_faces': len(deferred), 'empty_fragments_merged': moved_frag,
          'reconnect': dict(nrec, flipped_km2=round(nrec['flipped_km2'], 4), log=log),
          'n_assignment_exclaves_with_kids': sum(1 for e in exclaves if e['kids'] > 0 and e['assignment_exclave']),
          'exclaves_with_kids': [e for e in exclaves if e['kids'] > 0],
          'n_exclaves_with_kids': sum(1 for e in exclaves if e['kids'] > 0),
          'coverage_valid': bool(shapely.coverage_is_valid(simp)),
          'snap': dict(snapq, neck_repair=nrep),
          # kids whose block is joined to its school only through a contact narrower than the page grid that could
          # not be widened (another school's neck crosses it, or only populated cells border it): drawn detached
          'grid_pinched': {names[k]: round(v, 1) for k, v in sorted(stake.items()) if v > 0},
          'schools_missing': sorted(set(names) - set(gnames))}
    return polys, qa


PEN = 150000.0     # m^2-equivalent cost of cutting a populated face on a reconnect path (cowork: 2e-5 deg^2)
EPS = 1e-6


def _comps(sch, P, n):
    same = sch[P[:, 0]] == sch[P[:, 1]]
    g = coo_matrix((np.ones(same.sum()), (P[same, 0], P[same, 1])), shape=(n, n))
    return connected_components(g, directed=False)


def _merge_empty(sch, akids, area, P, L, n, nn, moved):
    """any piece of a school cut off from its main piece and holding no kids joins the neighbour sharing the most border."""
    for rnd in range(8):
        nc, comp = _comps(sch, P, n)
        same = sch[P[:, 0]] == sch[P[:, 1]]
        ckids = np.bincount(comp, weights=akids, minlength=nc)
        carea = np.bincount(comp, weights=area, minlength=nc)
        csch = np.full(nc, -1); csch[comp] = sch
        main = {}
        for c in range(nc):
            s = csch[c]; key = (ckids[c], carea[c])
            if s not in main or key > main[s][0]:
                main[s] = (key, c)
        mains = {v[1] for v in main.values()}
        frag = [c for c in range(nc) if c not in mains and ckids[c] < 1e-6]
        if not frag:
            return
        frag.sort(key=lambda c: carea[c])
        cross = ~same
        pc0 = comp[P[:, 0]]; pc1 = comp[P[:, 1]]
        changed = 0
        for c in frag:
            m0 = cross & (pc0 == c); m1 = cross & (pc1 == c)
            other = np.r_[P[m0, 1], P[m1, 0]]; ll = np.r_[L[m0], L[m1]]
            if not len(other):
                continue
            tot = np.bincount(sch[other], weights=ll, minlength=nn)
            tot[csch[c]] = 0
            if tot.max() <= 0:
                continue
            sch[comp == c] = int(tot.argmax()); changed += 1; moved[0] += 1
        if not changed:
            return


def _mains(comp, nc, csch, ckids, carea, akids, rcomp, sch):
    """crisp components that are the main piece of some reference piece: for every (school, reference piece) the
    crisp component holding most of that reference piece's kids (ties: area)."""
    pop = np.where(akids > 0)[0]
    best = {}
    acc = {}
    for a in pop:
        if sch[a] < 0:
            continue
        k = (int(rcomp[a]), int(comp[a]))
        acc[k] = acc.get(k, 0.0) + akids[a]
    for (r, c), v in acc.items():
        key = (v, carea[c])
        if r not in best or key > best[r][0]:
            best[r] = (key, c)
    return {v[1] for v in best.values()}


def _reconnect(sch, akids, area, rl, rcomp, face_of, face_pop, A, P, n, names, nrec, log, locked):
    """cowork/crisp reconnect pass. A populated piece cut off from its school (not the main piece of any of the
    school's reference pieces) is joined to the main piece of the reference piece holding most of its kids, along
    the cheapest path: free through the school's own atoms; through an empty street face at that face's area
    (cheaper where it is the school's reference area), and the whole empty face flips; through a populated face
    only along the school's own reference (Voronoi) atoms, with a penalty, and that face is cut along the
    reference line. Kids never change school: populated centres keep their reference label.

    Faces a reconnect already flipped or cut are locked: they are never flipped whole again, only cut along the
    reference line. Without the lock two schools whose detached pieces need the same empty face (an X crossing:
    e.g. v2 option2 K-5 Rosa Parks/Arleta, Chief Joseph/MLK Jr, Markham/Hayhurst) flip it back and forth every
    round and both end up detached. With it, the second school goes along its own reference (Voronoi) atoms
    (the reference partition connects every reference piece), so the pass converges (v2: <= ~18 rounds)."""
    nc, comp = _comps(sch, P, n)
    ckids = np.bincount(comp, weights=akids, minlength=nc)
    carea = np.bincount(comp, weights=area, minlength=nc)
    csch = np.full(nc, -1); csch[comp] = sch
    mains = _mains(comp, nc, csch, ckids, carea, akids, rcomp, sch)
    todo = [c for c in range(nc) if ckids[c] > 1e-6 and c not in mains]
    if not todo:
        return False
    fa = np.bincount(face_of, weights=area, minlength=A['n_faces'])
    src = np.r_[P[:, 0], P[:, 1]]; dst = np.r_[P[:, 1], P[:, 0]]
    changed = False
    for c in sorted(todo, key=lambda c: -ckids[c]):
        s = csch[c]
        at = np.where(comp == c)[0]
        if (sch[at] != s).any():          # changed by an earlier reconnect this round
            continue
        # target: main crisp piece of the reference piece holding most of this piece's kids
        pk = at[akids[at] > 0]
        rr = np.bincount(rcomp[pk], weights=akids[pk])
        r = int(rr.argmax())
        tgt = [m for m in mains if csch[m] == s and akids[(comp == m) & (rcomp == r)].sum() > 0]
        if not tgt:
            continue
        tmask = np.isin(comp, tgt) & (sch == s)
        # node costs (cost of entering v)
        fv = face_of
        sh = np.bincount(fv, weights=area * (rl == s), minlength=A['n_faces']) / np.maximum(fa, 1e-9)
        cost = np.full(n, np.inf)
        own = sch == s
        emp = ~face_pop[fv]
        cost[own] = EPS
        free = emp & ~locked
        m = ~own & free
        cost[m] = fa[fv[m]] * (1.05 - sh[fv[m]])
        m = ~own & ~free & (rl == s)
        cost[m] = area[m] * 0.05 + PEN
        wgt = cost[dst].copy()
        same_face = (fv[src] == fv[dst]) & ~own[dst] & free[dst]
        wgt[same_face] = EPS           # an empty face is paid once, on entry
        ok = np.isfinite(wgt)
        G = coo_matrix((wgt[ok], (src[ok], dst[ok])), shape=(n, n)).tocsr()
        dist, pred, _ = dijkstra(G, directed=True, indices=at, min_only=True, return_predecessors=True)
        tt = np.where(tmask & np.isfinite(dist))[0]
        if not len(tt):
            log.append('cannot reconnect %s piece (%.1f kids)' % (names[s], ckids[c]))
            continue
        u = int(tt[dist[tt].argmin()])
        path = []
        while u >= 0 and comp[u] != c:
            path.append(u); u = int(pred[u])
        flips = set(); cuts = set()
        for v in path:
            if sch[v] == s:
                continue
            (flips if free[v] else cuts).add(int(fv[v]))
        fk = 0.0
        for f in flips:
            fat = A['face_atoms'][f]; sch[fat] = s; fk += area[fat].sum(); locked[fat] = True
        for f in cuts:
            fat = A['face_atoms'][f]; sch[fat] = rl[fat]; locked[fat] = True
        nrec['flipped_faces'] += len(flips); nrec['cut_faces'] += len(cuts); nrec['flipped_km2'] += fk / 1e6
        log.append('reconnect %s (%.1f kids): flipped %d empty faces (%.4f km2), cut %d populated faces' % (
            names[s], ckids[c], len(flips), fk / 1e6, len(cuts)))
        changed = True
    return changed


def snap_coverage(geoms, grid=GRID_DEG):
    """Snap a coverage (metres) to the page's encoding grid AS ONE PARTITION, so that encoding cannot make it
    overlap. Rounding each school's rings to 1e-4 degree independently (common.enc_ring) keeps shared edges
    shared, but a piece or hole narrower than the grid (~8 x 11 m) collapses or turns inside out and the decoded
    rings overlap their neighbour (v2 option2 K-5: a 2 m wide Rosa Parks sliver -> 909 m2 Rosa Parks/Sitton
    overlap). Here all boundaries are noded together with snap-rounding on the grid, polygonized into faces, and
    each face goes to the school covering most of it. Returns (geoms in metres, qa dict)."""
    geoms = list(geoms)
    ll = [to_ll(g) for g in geoms]
    lines = shapely.union_all(shapely.get_parts(shapely.boundary(np.array(ll, dtype=object))), grid_size=grid)
    faces = shapely.get_parts(shapely.polygonize(shapely.get_parts(lines)))
    faces = faces[shapely.area(faces) > 0]
    tree = shapely.STRtree(ll)
    owner = np.full(len(faces), -1)
    best = np.zeros(len(faces))
    fi, gi = tree.query(faces)
    ia = shapely.area(shapely.intersection(faces[fi], np.array(ll, dtype=object)[gi]))
    for f, g, a in zip(fi, gi, ia):
        if a > best[f]:
            best[f] = a; owner[f] = g
    orphan = owner < 0                        # (no area overlap: a sliver; take the nearest school)
    for f in np.where(orphan)[0]:
        owner[f] = int(tree.query_nearest(shapely.point_on_surface(faces[f]))[0])
    out = []
    for k in range(len(geoms)):
        sel = faces[owner == k]
        out.append(to_m(shapely.coverage_union_all(sel)) if len(sel) else shapely.Polygon())
    lost = sum(abs(to_m(ll[k]).area - out[k].area) for k in range(len(geoms)))
    return np.array(out, dtype=object), {'faces': int(len(faces)), 'orphan_faces': int(orphan.sum()),
                                          'area_changed_m2': round(lost)}


def _draw(sch, names, A):
    """atoms -> per-school geometry: exact coverage union, coverage simplify, snap to the page grid."""
    geoms = []; gnames = []
    for k, s in enumerate(names):
        sel = np.where(sch == k)[0]
        if not len(sel):
            continue
        geoms.append(shapely.coverage_union_all(A['atoms'][sel])); gnames.append(s)
    geoms = np.array(geoms, dtype=object)
    simp = shapely.coverage_simplify(geoms, SIMPLIFY_M, simplify_boundary=False)
    simp = shapely.make_valid(simp)
    simp, snapq = snap_coverage(simp)
    return gnames, simp, snapq


def _necks(sch, akids, gnames, simp, names, A, P, n, pblk):
    """A connected piece of a school (atom graph) whose kids land in 2+ separate DRAWN parts after the grid snap:
    a neck narrower than the ~8 x 11 m grid collapsed (v2 option2 K-5 Glencoe, 19 kids). Widen it by one atom
    layer: atoms of the piece that the drawing lost take their neighbours, never an atom holding another school's
    populated block centre (kids never move). Returns array of (atom, school code) to flip; empty when none."""
    if 'rep' not in A:
        A['rep'] = shapely.point_on_surface(A['atoms'])
    rep = A['rep']
    nc, comp = _comps(sch, P, n)
    part = np.full(n, -1)                      # drawn part id holding each atom's representative point
    parts = []; powner = []
    for g, nm_ in zip(simp, gnames):
        for q in ([g] if g.geom_type == 'Polygon' else [x for x in getattr(g, 'geoms', []) if x.geom_type == 'Polygon']):
            parts.append(q); powner.append(names.index(nm_))
    if not parts:
        return np.zeros((0, 2), int), {}
    tree = shapely.STRtree(np.array(parts, dtype=object))
    ai, pi = tree.query(rep, predicate='within')
    powner = np.array(powner)
    ok = powner[pi] == sch[ai]
    part[ai[ok]] = pi[ok]
    if 'cpt' not in A:
        A['cpt'] = shapely.points(block_xy())
    bi, bp = tree.query(A['cpt'][pblk], predicate='within')     # drawn part holding each populated block centre
    ca = A['centre_atom'][pblk]
    split = set()
    seen = {}
    for i, q in zip(bi, bp):
        a = ca[i]
        if powner[q] == sch[a]:
            d = seen.setdefault(comp[a], {}); d[int(q)] = d.get(int(q), 0.0) + akids[a]
    stake = {}                                 # per school: kids the snap cut off from their piece
    for c, ps in seen.items():
        if len(ps) > 1:
            split.add(c)
            v = sorted(ps.values())
            k = int(sch[np.argmax(comp == c)]); stake[k] = stake.get(k, 0.0) + sum(v[:-1])
    if not split:
        return np.zeros((0, 2), int), stake
    lost = np.isin(comp, list(split)) & (part < 0)
    # only the necks: clusters of lost atoms whose same-school neighbours sit in 2+ different drawn parts
    li = np.where(lost)[0]
    both = lost[P[:, 0]] & lost[P[:, 1]]
    g = coo_matrix((np.ones(both.sum()), (P[both, 0], P[both, 1])), shape=(n, n))
    lc = connected_components(g, directed=False)[1]
    touch = {}
    for x, y in ((P[:, 0], P[:, 1]), (P[:, 1], P[:, 0])):
        m = lost[x] & ~lost[y] & (sch[y] == sch[x]) & (part[y] >= 0)
        for u, v in zip(lc[x[m]], part[y[m]]):
            touch.setdefault(int(u), set()).add(int(v))
    neck = {c for c, ps in touch.items() if len(ps) > 1}
    lost = np.zeros(n, bool); lost[li[np.isin(lc[li], list(neck))]] = True
    # and pinch points between two kept atoms of the same piece that landed in different drawn parts
    insp = np.isin(comp, list(split))
    m = (sch[P[:, 0]] == sch[P[:, 1]]) & insp[P[:, 0]] & (part[P[:, 0]] >= 0) & (part[P[:, 1]] >= 0) & (part[P[:, 0]] != part[P[:, 1]])
    lost[P[m, 0]] = True; lost[P[m, 1]] = True
    out = {}
    for x, y in ((P[:, 0], P[:, 1]), (P[:, 1], P[:, 0])):
        m = lost[x] & (sch[y] != sch[x]) & (akids[y] <= 0)
        for u, v in zip(x[m], y[m]):
            out.setdefault(int(v), int(sch[u]))
    # and any kid-free atom of another school within NECK_M of the neck (one grid cell), so one round makes the
    # neck wide enough to survive the snap even where its own neighbours are slivers or hold kids
    if 'tree' not in A:
        A['tree'] = shapely.STRtree(A['atoms'])
    nk = np.where(lost)[0]
    for u in nk:
        for v in A['tree'].query(A['atoms'][u], predicate='dwithin', distance=NECK_M):
            if sch[v] != sch[u] and akids[v] <= 0 and A['area'][v] <= NECK_MAX_M2:
                out.setdefault(int(v), int(sch[u]))
    return np.array(sorted(out.items()), dtype=int).reshape(-1, 2), stake


def _npieces(sch, akids, P, n, nn, detached=False):
    """populated pieces per school in the atom graph (and, with detached, kids outside each school's biggest piece)."""
    nc, comp = _comps(sch, P, n)
    ck = np.bincount(comp, weights=akids, minlength=nc)
    cs = np.full(nc, -1); cs[comp] = sch
    m = (ck > 0) & (cs >= 0)
    cnt = np.bincount(cs[m], minlength=nn)
    if not detached:
        return cnt
    tot = np.bincount(cs[m], weights=ck[m], minlength=nn)
    big = np.zeros(nn)
    np.maximum.at(big, cs[m], ck[m])
    return cnt, tot - big
