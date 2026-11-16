"""Line-quality QA for v2 runs (Paul 2026-10-12 ~23:00: "look for weird lines, weird pockets and fix them").

  python lines_qa.py [run ...] [--staging run ...] [--md out_v2/LINES_QA.md]

Per run and level (K-5, 6-8), on the block adjacency with real shared edges (common.edges, length > 0; the Voronoi
bridges common.adjacency adds across gaps are NOT used, so a piece joined only by a bridge counts as detached):
  teeth    blocks whose shared boundary is mostly (> 50%) with other schools' areas (one-block sawtooth notches)
  fingers  runs of >= 3 connected thin blocks (same-school share < 60%): long one-block-wide extensions
  pockets  pieces of a school's area cut off from the piece holding its building that touch another school's area
           (Washington County blocks, GEOID 41067..., are listed separately: a detached part of the district; pieces
           with no real shared edge at all, rural West Hills Voronoi fragments, are data gaps and not counted; pieces joined
           to their school only across the I-84 line are listed as across_i84, as PPS's Buckman/Sunnyside areas)
  far      runs of >= 3 connected blocks whose kids walk >= 0.5 mi past a closer open school (eligible, no new
           I-84/river crossing)
Kids are the run's 2031-32 band kids.  Coordinates are block centroids (lon, lat) so pieces can be found on the map."""
import argparse, json, os, sys
from collections import defaultdict, deque
import numpy as np, pandas as pd
import common as C, metrics as MX

OUT = os.path.join(C.SOLVER, 'out_v2')


def _cfg(run, src=None):
    p = os.path.join(C.SOLVER, 'configs', 'v2', f'{run}.json')
    if not os.path.exists(p):
        p = os.path.join(C.SOLVER, 'configs', 'v2', 'option1_durable.json')
    cfg = C.load_config(p)
    sc = os.path.join(src or os.path.join(OUT, run), 'scorecard.json')
    if os.path.exists(sc):
        C.resolve_config(cfg, json.load(open(sc)))    # the run's own closures / program moves (capstone)
    return cfg


def _runs(sel, adj):
    """connected components of the boolean mask sel on adjacency adj"""
    seen, out = set(), []
    for i in np.nonzero(sel)[0]:
        if i in seen:
            continue
        comp, q = [], deque([i])
        seen.add(i)
        while q:
            k = q.popleft()
            comp.append(k)
            for j in adj[k]:
                if sel[j] and j not in seen:
                    seen.add(j)
                    q.append(j)
        out.append(comp)
    return out


def qa(run, staging=False):
    src = os.path.join(OUT, run + ('.staging' if staging else ''))
    cfg = _cfg(run, src)
    b = C.blocks()
    x, y, geo = b['x'].values, b['y'].values, b['GEOID'].astype(str).values
    EL = defaultdict(dict)
    for i, j, L in C.edges():
        if L > 0:
            EL[i][j] = L
            EL[j][i] = L
    adj = {i: list(EL[i]) for i in range(len(b))}
    # zero-length NB edges across the I-84 zone line (N|S): a piece joined to its school only there sits across the
    # freeway from it, as PPS's own Buckman/Sunnyside areas do; it is listed as across_i84, not as a pocket
    zone = C.block_zones()[1]
    I84 = defaultdict(set)
    for i, j, L in C.edges():
        if L <= 0 and {zone[i], zone[j]} == {'N', 'S'}:
            I84[i].add(j)
            I84[j].add(i)
    roots = C.school_block()
    K = MX.level_kids(cfg, '2031')
    res = {}
    for lev in ('K-5', '6-8'):
        a = pd.read_parquet(os.path.join(src, f'assign_{lev}.parquet'))['school'].values
        k = K[lev]
        share = np.ones(len(a))
        for i, nb in EL.items():
            tl = sum(nb.values())
            if tl > 0:
                share[i] = sum(L for j, L in nb.items() if a[j] == a[i]) / tl
        teeth = share < 0.5 - 1e-9
        thin = share < 0.6 - 1e-9
        fingers = []
        for comp in _runs(thin, {i: [j for j in adj[i] if a[j] == a[i]] for i in range(len(a))}):
            if len(comp) >= 3:
                fingers.append({'school': a[comp[0]], 'blocks': len(comp), 'kids': round(float(k[comp].sum()), 1),
                                'at': [round(float(x[comp].mean()), 4), round(float(y[comp].mean()), 4)]})
        pockets, detached, across = [], [], []
        for s in sorted(set(a)):
            m = a == s
            comps = _runs(m, {i: [j for j in adj[i] if a[j] == s] for i in np.nonzero(m)[0]})
            r = roots.get(s)
            main = next((c for c in comps if r in c), max(comps, key=len))
            for c in comps:
                if c is main:
                    continue
                rec = {'school': s, 'blocks': len(c), 'kids': round(float(k[c].sum()), 1),
                       'at': [round(float(x[c].mean()), 4), round(float(y[c].mean()), 4)]}
                if all(geo[i].startswith('41067') for i in c):
                    detached.append(rec)
                elif any(a[j] == s and j in set(main) for i in c for j in I84[i]):
                    across.append(rec)
                elif any(a[j] != s for i in c for j in adj[i]):
                    pockets.append(rec)       # enclosed by / touching another school's area: a real pocket
                # else: a piece with no real shared edge to any block (rural West Hills / Forest Park Voronoi
                # fragments): a data gap, joined to its school by the solver's bridges; not a pocket
        names = sorted(cfg['levels'][lev]['zoned'])
        W = C.dist('walk', names)
        refs = MX.load_refs(os.path.join(C.SOLVER, 'configs', 'v2'))
        E = MX.eligible_mask(lev, names, [refs['today'][lev], refs['status_quo'][lev]])
        Wm = np.where(E, W, np.inf)
        idx = {n: q for q, n in enumerate(names)}
        dmin = np.nanmin(np.where(np.isnan(Wm), np.inf, Wm), axis=1)
        dasg = np.array([W[i, idx[s]] if s in idx else np.nan for i, s in enumerate(a)])
        farm = (dasg - dmin >= 0.5) & (k > 0)
        far = []
        for comp in _runs(farm, {i: [j for j in adj[i] if a[j] == a[i]] for i in range(len(a))}):
            if len(comp) >= 3:
                far.append({'school': a[comp[0]], 'blocks': len(comp), 'kids': round(float(k[comp].sum()), 1),
                            'extra_mi': round(float(np.nanmean(dasg[comp] - dmin[comp])), 2),
                            'at': [round(float(x[comp].mean()), 4), round(float(y[comp].mean()), 4)]})
        res[lev] = {'teeth': int(teeth.sum()), 'teeth_kids': round(float(k[teeth].sum()), 1),
                    'fingers': sorted(fingers, key=lambda r: -r['blocks']),
                    'pockets': sorted(pockets, key=lambda r: -r['kids']), 'detached_wash_co': detached,
                    'across_i84': across,
                    'far': sorted(far, key=lambda r: -r['kids'])}
    return res


def summary(run, r):
    out = []
    for lev in ('K-5', '6-8'):
        q = r[lev]
        out.append(f"| {run} | {lev} | {q['teeth']} ({q['teeth_kids']:.0f} kids) | {len(q['fingers'])} "
                   f"({sum(f['blocks'] for f in q['fingers'])} blocks) | {len(q['pockets'])} "
                   f"({sum(p['kids'] for p in q['pockets']):.0f} kids) | {len(q['far'])} "
                   f"({sum(p['kids'] for p in q['far']):.0f} kids) |")
    return out


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('runs', nargs='*', default=['scenario_A', 'option1_durable', 'option2', 'option2_ms460', 'option4'])
    ap.add_argument('--staging', nargs='*', default=[])
    ap.add_argument('--md')
    ap.add_argument('--json')
    a = ap.parse_args()
    allr = {}
    rows = ['| Plan | Level | Teeth | Fingers (>=3 thin blocks) | Pockets | Far pockets (>=0.5 mi past closer) |',
            '|---|---|---|---|---|---|']
    for run in a.runs:
        allr[run] = qa(run)
        rows += summary(run, allr[run])
    for run in a.staging:
        allr[run + '.staging'] = qa(run, True)
        rows += summary(run + ' (staging)', allr[run + '.staging'])
    print('\n'.join(rows))
    if a.json:
        json.dump(allr, open(a.json, 'w'), indent=1)
    if a.md:
        open(a.md, 'w').write('\n'.join(rows) + '\n')
