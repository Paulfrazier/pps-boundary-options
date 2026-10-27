#!/usr/bin/env python
"""Build pages/map.html: every plan on one map (Today, Status Quo 2027-28, PPS Scenario A and B, and our solver
options), at K-5 (default, embedded) and 6-8 / 9-12 (lazy-loaded from pages/map_data/level_<lv>.js, which also
works from file://).

REBUILD (one command, from the kit root):
    cd build/map && ../../.venv/bin/python build_site_map.py            # add --force to ignore caches

What it reads (all read only):
- pages/data/site_data.json (build/export/site_data.py): which plans to show, labels, version_label
  ("earlier model v1" / "model v2"), placeholder_note, and each plan's assign_<level>.parquet / scorecard.json /
  schools.csv paths. New options (2-5, v2 reruns) appear here on rebuild with no code change.
- Today / Status Quo / Scenario A / B: PPS's OFFICIAL lines (build/data/scenario_maps, build/data/boundaries;
  crisp/official_lv.py). Solver options: crisp street-following lines derived from their block assignments
  (crisp/geo.py + crisp/crisp.py, a port of cowork/crisp). Lines are cached per plan+level in
  work/site_cache/, keyed by a hash of the assignment file (and the traced source for official lines).
- Kids per block, walks and "past a closer school": scorebasis.py, which calls build/solver/metrics.py (read only) so
  every count equals each plan's scorecard (2031-32 kids, zoned schools, past_margin_miles, eligible = no new crossing).
  SITE_DATA=<path> overrides pages/data/site_data.json (testing only).
- build/data/blocks.parquet (homes), build/routing/walk_miles.parquet (walk miles),
  data/pps-map/pps-model.json + pps-race.csv (hard-edge zones, kids-of-color share), build/data/schools.csv
  (school locations), pages/pps-walk-redraw.html (streets, base layers, outline, today's K-5 lines),
  work/street_labels.txt + fonts/ (map v2 caches).
- build/safe_routes/ (read only): walk_crossings.parquet (hard crossings per block and school) and cache/artn.opl +
  sig.opl (busy streets, signals, marked crossings) for the Closer walk tooltips and the Busy streets to cross layer.

Writes: pages/map.html, pages/map_data/level_K-5.js (blocking script, cached, preloaded), pages/map_data/fonts/*.woff2, pages/map_data/level_6-8.js, pages/map_data/level_9-12.js, map_data/streets.js, map_data/street_names.js, map_data/crossings.js,
work/site_cache/qa_report.json (crisp quality checks). Never writes pages/pps-walk-redraw-v2.html.
"""
import collections, hashlib, itertools, json, os, sys, time
import numpy as np
import pandas as pd
import shapely
from shapely.geometry import Polygon
from shapely.ops import unary_union

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, 'crisp'))
from common import KIT, WORK, X0, Y0, grab, load_page, dec, enc_ring  # noqa: E402
from geo import MX, LAT_M, district, voronoi_cells, block_xy, to_ll    # noqa: E402
import crisp as CR                                                     # noqa: E402
import official_lv as OF                                               # noqa: E402
import stats as ST                                                     # noqa: E402
import scorebasis as SB                                                # noqa: E402

FORCE = '--force' in sys.argv
METHOD = 'site-map-5'          # bump to invalidate every cached plan/pair (2: scorecard kid basis + reconnect pass; 4: grid snap, reconnect lock, neck widening; 5: big empty faces split on reference lines)
PAIR_METHOD = 'pair-2'      # pair cache only (2: changed-area pieces carry their own kids, not the whole flow each)
CACHE = os.path.join(WORK, 'site_cache')
OUT = os.path.join(KIT, 'pages', 'map.html')
OUTD = os.path.join(KIT, 'pages', 'map_data')
LEVELS = ['K-5', '6-8', '9-12']
WCOL = {'K-5': 'k5', '6-8': 'm68', '9-12': 'h912'}
DEN_M = 400.0                # density grid cell, metres (map themes "Where kids live" / "Where kids move")
TYPES = {'K-5': ('K-5', 'K-8'), '6-8': ('6-8', 'K-8'), '9-12': ('9-12',)}
OFFICIAL = set(OF.COL)
os.makedirs(CACHE, exist_ok=True); os.makedirs(OUTD, exist_ok=True)
T0 = time.time()


def log(*a):
    print('[%5.1fs]' % (time.time() - T0), *a, flush=True)


def sha(*paths_or_bytes):
    h = hashlib.sha1()
    for p in paths_or_bytes:
        h.update(p if isinstance(p, bytes) else open(p, 'rb').read())
    return h.hexdigest()[:12]


def enc_geom(g):
    rings = []
    for p in ([g] if g.geom_type == 'Polygon' else [x for x in getattr(g, 'geoms', []) if x.geom_type == 'Polygon']):
        for r in [p.exterior] + list(p.interiors):
            e = enc_ring(list(to_ll(r).coords))
            if e:
                rings.append(e)
    return '|'.join(rings)


def dec_geom(enc):
    g = None
    for r in dec(enc):
        if len(r) < 4:
            continue
        p = Polygon([(x * MX, y * LAT_M) for x, y in r])
        if not p.is_valid:
            p = p.buffer(0)
        g = p if g is None else g.symmetric_difference(p)
    return g if g is not None else Polygon()


def rel(p):
    return os.path.relpath(p, KIT)


# ------------------------------------------------------------------ inputs
SD = json.load(open(os.environ.get('SITE_DATA') or os.path.join(KIT, 'pages', 'data', 'site_data.json')))   # SITE_DATA: test override
B = ST.blocks()
PTS = shapely.points(block_xy())
CELLS = np.array(voronoi_cells(), dtype=object)
POC = np.asarray(SB.solver()[1].poc_share(), dtype=float)   # as the scorecards (build/solver/common.poc_share)
HU = B['hu'].values.astype(float)
OPTS = [o for o in SD['options'] + SD.get('request_options', []) + SD.get('sabin_options', []) if o.get('assign')]   # requested and Sabin runs: own groups on the map
log('plans:', [o['name'] for o in OPTS])


def load_asg(o, lv):
    return pd.read_parquet(os.path.join(KIT, o['assign'][lv]))['school'].astype(object).values


def plan_polys(o, lv, w):
    """encoded polygons for one plan+level (cached by hash of assignment file + kid weights + method)."""
    f = os.path.join(KIT, o['assign'][lv])
    off = o['name'] in OFFICIAL
    parts = [f, METHOD.encode()]
    if not off:
        parts.append(np.round(np.asarray(w, dtype=float), 4).tobytes())   # crisp uses the kid weights
    if off:
        src = os.path.join(KIT, OF.SOURCE[o['name']][lv])
        parts.append(src)
        if o['name'] == 'today' and lv == 'K-5':
            parts.append(os.path.join(KIT, 'pages', 'pps-walk-redraw.html'))
    key = '%s_%s_%s' % (o['name'], lv, sha(*parts))
    cp = os.path.join(CACHE, 'poly_%s.json' % key)
    if os.path.exists(cp) and not FORCE:
        d = json.load(open(cp)); d['key'] = key; return d
    lab = load_asg(o, lv)
    if off:
        polys, gap = OF.build(o['name'], lv, lab)
        qa = {'method': 'official', 'gap_filled_km2': gap}
    else:
        polys, qa = CR.crisp(lab, w)
        qa['method'] = 'crisp'
    d = {'poly': {n: enc_geom(g) for n, g in sorted(polys.items())}, 'qa': qa}
    d['poly'] = {n: e for n, e in d['poly'].items() if e}
    json.dump(d, open(cp, 'w'), separators=(',', ':'))
    log('  built lines', key, qa.get('method'))
    d['key'] = key
    return d


def pip(geoms):
    names = list(geoms); tree = shapely.STRtree([geoms[n] for n in names])
    q = tree.query(PTS, predicate='within')
    got = np.full(len(PTS), None, dtype=object)
    for i, j in zip(*q):
        if got[i] is None:
            got[i] = names[j]
    return got


def school_rows(o):
    p = o.get('schools_source')
    if not p:
        return pd.DataFrame()
    return pd.read_csv(os.path.join(KIT, p))


def fnum(v, nd=3):
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return None
    if isinstance(v, (bool, np.bool_)):
        return bool(v)
    v = float(v)
    return int(round(v)) if nd == 0 else round(v, nd)


def lr_round(vals, total):
    """Largest-remainder rounding: integers per key that add up exactly to `total` (round 6, review4 #8: the per-school
    tables summed to 1,972 against the scorecard's 1,970). Ties go to the larger value, then the name, so it is stable."""
    fl = {n: int(np.floor(v)) for n, v in vals.items()}
    left = int(total) - sum(fl.values())
    order = sorted(vals, key=lambda n: (-(vals[n] - fl[n]), -vals[n], n))
    if left < 0:                      # only if `total` was rounded down past the floors (never for these counts)
        order = sorted(vals, key=lambda n: ((vals[n] - fl[n]), vals[n], n))
        for n in order[:-left]:
            fl[n] -= 1
    else:
        for n in order[:left]:
            fl[n] += 1
    return fl


# ------------------------------------------------------------------ per level
QA = {}
LVDATA = {}
for lv in LEVELS:
    log('level', lv)
    plans = {}; labs = {}; geoms = {}; keys = {}; KW = {}; SBP = {}
    ref = {}
    for o in OPTS:
        if lv not in o['assign']:
            continue
        labs[o['name']] = load_asg(o, lv)
        # scorecard basis (build/solver/metrics.py): 2031-32 kids per block + past-a-closer-school rule
        SBP[o['name']] = SB.past(o, lv, labs[o['name']]); KW[o['name']] = SBP[o['name']]['K']
    for r in ('today', 'status_quo'):
        if r in labs:
            ref[r] = labs[r]
    for o in OPTS:
        if lv not in o['assign']:
            continue
        k = o['name']; lab = labs[k]; w = KW[k]; sp = SBP[k]
        pp = plan_polys(o, lv, w); keys[k] = pp['key']
        geoms[k] = {n: dec_geom(e) for n, e in pp['poly'].items()}
        # ---- QA: block centres vs drawn polygons (after encoding at the page's 1e-4 degree precision)
        got = pip(geoms[k])
        sz_a = collections.Counter(); sz_p = collections.Counter()
        for a, b, ww in zip(lab, got, w):
            sz_a[a] += ww
            if b is not None:
                sz_p[b] += ww
        mism = {n: round(sz_p[n] - sz_a[n], 1) for n in set(sz_a) | set(sz_p) if abs(sz_p[n] - sz_a[n]) >= 0.05}
        wrong = (got != lab) & (w > 0)
        q = dict(pp['qa'])
        q.update({'populated_blocks_off': int(wrong.sum()), 'kids_off': round(float(w[wrong].sum()), 1),
                  'max_school_mismatch_kids': max([abs(v) for v in mism.values()], default=0.0),
                  'school_mismatch': dict(sorted(mism.items(), key=lambda x: -abs(x[1]))[:6])})
        if q['method'] == 'crisp':
            U = shapely.union_all(list(geoms[k].values()))
            q['gap_m2'] = round(district().difference(U).area)
            q['overlap_m2'] = round(sum(g.area for g in geoms[k].values()) - U.area)
            # pieces holding kids AS DRAWN (decoded page polygons) apart from the school's biggest piece: 'drawn' =
            # visibly separate; 'corner' = touching the rest of the school only at a point (looks joined on the map)
            dx = []
            for n, g in geoms[k].items():
                ps = [g] if g.geom_type == 'Polygon' else [p for p in getattr(g, 'geoms', []) if p.geom_type == 'Polygon']
                if len(ps) < 2:
                    continue
                sel = np.where((lab == n) & (w > 0))[0]
                pk = [float(w[sel[shapely.contains_xy(p, shapely.get_x(PTS[sel]), shapely.get_y(PTS[sel]))]].sum()) for p in ps]
                order_ = np.argsort(pk)[::-1]
                for j in order_[1:]:
                    if pk[j] <= 0:
                        continue
                    rest = shapely.union_all([ps[i] for i in range(len(ps)) if i != j])
                    c = to_ll(ps[j].centroid)
                    dx.append({'school': n, 'kids': round(pk[j], 1), 'lonlat': [round(c.x, 5), round(c.y, 5)],
                               'corner': bool(ps[j].distance(rest) < 0.5)})
            q['drawn_exclaves'] = dx
            q['drawn_exclaves_with_kids'] = sum(1 for e in dx if not e['corner'])
            q['drawn_corner_touch_with_kids'] = sum(1 for e in dx if e['corner'])
        QA['%s %s' % (k, lv)] = q
        # ---- stats from block assignment (scorecard 2031-32 basis kids, walks as metrics.py)
        size = collections.Counter(); pc = collections.Counter()
        for a, ww, p in zip(lab, w, POC):
            size[a] += ww; pc[a] += ww * p
        koc = {n: round(100 * pc[n] / size[n]) for n in size if size[n] > 0}
        names = sorted(set(lab))
        col = {n: i for i, n in enumerate(names)}
        ai = np.array([col[a] for a in lab]); d = sp['d']
        bands = {}
        for key_, wt in (('S', w), ('H', HU)):
            res = {}
            allr = np.zeros(5)
            for n in names:
                m = (ai == col[n]); tot = wt[m].sum()
                c = [wt[m & (d <= t)].sum() for t in (.5, 1, 1.5, 2)]
                res[n] = [round(tot)] + [round(x / tot * 100) if tot > 0 else 0 for x in c]
                allr += np.array([tot] + c)
            res['__ALL'] = [round(allr[0])] + [round(x / allr[0] * 100) for x in allr[1:]]
            bands[key_] = res
        # students by the baseline's area (status_quo = PPS 2027-28, no closures; Today archived by)
        frm = {}
        if 'status_quo' in labs:
            c2 = collections.defaultdict(collections.Counter)
            for a, t, ww in zip(lab, labs['status_quo'], w):
                c2[a][t] += ww
            frm = {n: [[t, round(v)] for t, v in c.most_common() if v >= 15] for n, c in c2.items()}
        # past a closer school: exactly the scorecard rule and kids (scorebasis.py <- build/solver/metrics.py)
        lvsum = o.get('levels', {}).get(lv, {})
        margin = sp['margin']; dmin = sp['dmin']; amin = sp['amin']; znames = sp['names']
        past = sp['past']
        regs = []
        grp = collections.defaultdict(list)
        for i in np.where(past & (w > 0))[0]:
            grp[(lab[i], znames[amin[i]])].append(i)
        for (a, nn), ids in grp.items():
            kids = float(w[ids].sum())
            if kids < 0.05:
                continue
            e = ''
            U = unary_union(list(CELLS[ids]))
            if a in geoms[k]:
                U = U.intersection(geoms[k][a])
            U = U.buffer(-8).buffer(8).simplify(4.0)
            ps = [U] if U.geom_type == 'Polygon' else [g for g in getattr(U, 'geoms', []) if g.geom_type == 'Polygon']
            ps = [p for p in ps if p.area >= 1500]
            if ps:
                e = enc_geom(unary_union(ps))
            regs.append([a, nn, round(kids, 1), e])     # e = '' when too small to draw; still counted
        regs.sort(key=lambda r: -r[2])
        pb = collections.Counter()
        for i in np.where(past & (w > 0))[0]:
            pb[lab[i]] += float(w[i])
        pn = round(float(w[past].sum()))
        pastd = {'n': pn, 'margin': margin, 'regs': regs, 'by': {n: v for n, v in lr_round(pb, pn).items() if v > 0},
                 'extra_mi': round(float((w[past] * (d[past] - dmin[past])).sum() / max(w[past].sum(), 1e-9)), 2)}
        # per-school stats from the option's schools.csv
        S = school_rows(o); st = {}; prog = []
        if len(S):
            for r in S.to_dict('records'):
                if r['type'] not in TYPES[lv]:
                    continue
                L = lv
                st[r['school']] = {
                    'type': r['type'], 'total': fnum(r.get('total'), 0), 'cap': fnum(r.get('capacity'), 0),
                    'util': fnum(r.get('utilization'), 3), 'floor': fnum(r.get('floor'), 0), 'ceil': fnum(r.get('ceiling'), 0),
                    'in_range': fnum(r.get('in_range')), 'nbhd': fnum(r.get('nbhd_' + L), 0), 'prog': fnum(r.get('prog_' + L), 0),
                    'walk': fnum(r.get('avg_walk_' + L), 2), 'bus': fnum(r.get('kids_over_bus_' + L), 0),
                    'poc': fnum(r.get('poc_share_' + L), 3), 'exempt': fnum(r.get('floor_exempt')), 'po': bool(r.get('program_only'))}
                zoned = r.get('zoned_' + L)
                if r.get('program_only') and r['school'] not in geoms[k] and ST.coords(r['school']):
                    prog.append([r['school'], fnum(r.get('prog_' + L), 0) or fnum(r.get('total'), 0)])
        # a plan solved with a lower floor (site_data PPS_FLOOR_RECOUNT) is shown at PPS's floor, like every other plan
        pfl = (o.get('pps_floor') or {}).get(lv)
        if pfl:
            for x in st.values():
                if x['floor'] is not None and x['floor'] < pfl:
                    x['floor'] = pfl
                    if x['in_range'] and (x['total'] or 0) < pfl:
                        x['in_range'] = False
        summ = {x: lvsum.get(x) for x in ('kids', 'avg_walk_mi', 'pct_within_0.5mi', 'pct_within_1.0mi', 'pct_within_1.5mi',
                                          'kids_over_bus_threshold', 'bus_threshold_mi', 'kids_past_closer_school', 'past_margin_mi',
                                          'kids_reassigned_vs_today', 'kids_reassigned_vs_status_quo', 'dissimilarity_index',
                                          'schools_open', 'schools_in_range', 'schools_evaluated_non_exempt',
                                          'schools_in_range_non_exempt', 'min_size', 'max_size')}
        # schools at target, 2031-32: the site's definition (scorecard durability: zoned, non-exempt schools; options /
        # landing "Schools at target, 2031-32"). s = {school: [zoned size 2031-32, -1 under floor | 0 at target | 1 over ceiling]};
        # zoned schools with an area but missing from s are exempt (not counted)
        dl = ((o.get('durability') or {}).get('levels') or {}).get(lv)
        dur = None
        if dl:
            yi = o['durability']['years'].index('2031-32')
            ds = {}
            for n, x in dl['schools'].items():
                if x.get('program_only'):
                    continue
                sz = x['sizes_by_year']['2031-32']; f = (st.get(n) or {}).get('floor')
                ds[n] = [round(sz), 0 if x['in_range_by_year'][yi] else (-1 if f is not None and sz < f else 1)]
            dur = {'at': dl['at_target_zoned']['2031-32'], 'n': dl['n_zoned_non_exempt'], 'yr': '2031-32', 's': ds}
            assert dur['at'] == sum(1 for v in ds.values() if v[1] == 0) and dur['n'] == len(ds), (k, lv)
        # PPS's own Family Guide figures represent PPS's plans (school sizes, at-target counts)
        pf = (((SD.get('pps_figures') or {}).get('plans') or {}).get(o['name']) or {})
        pl = (pf.get('levels') or {}).get(lv)
        if pl:
            yi = pf['years'].index('2031-32')
            ds = {}
            for n, x in pl['schools'].items():
                if x.get('po') or x['s'][yi] is None:
                    continue
                v, f, c = x['s'][yi], x.get('f'), x.get('c')
                ds[n] = [round(v), 0 if (f is None or v >= f) and (c is None or v <= c) else (-1 if f is not None and v < f else 1)]
            dur = {'at': pl['at_target_zoned']['2031-32'], 'n': pl['n_zoned_non_exempt'], 'yr': '2031-32', 's': ds, 'src': 'pps'}
            if dur['at'] != sum(1 for v in ds.values() if v[1] == 0) or dur['n'] != len(ds):
                print(f'  note: PPS figures for {k} {lv}: at {dur["at"]} / n {dur["n"]} vs schools {len(ds)}', file=sys.stderr)
        plans[k] = {'tot': round(float(w.sum())), 'poly': pp['poly'], 'dur': dur, 'size': {n: v for n, v in lr_round(size, round(float(w.sum()))).items() if v > 0}, 'koc': koc,
                    'bands': bands, 'from': frm, 'past': pastd, 'st': st, 'prog': prog, 'sum': summ,
                    'avgw': {n: round(float((w[ai == col[n]] * d[ai == col[n]]).sum() / max(w[ai == col[n]].sum(), 1e-9)), 2) for n in names}}
    # ---- pairs: changed areas + flows (cached by both plans' keys)
    pairs = {}
    order = [o['name'] for o in OPTS if o['name'] in plans]
    for a, c in itertools.combinations(order, 2):
        ck = os.path.join(CACHE, 'pair_%s.json' % sha(('%s|%s|%s|%s' % (keys[a], keys[c], METHOD, PAIR_METHOD)).encode(),
                                                     np.round(KW[c], 4).tobytes()))   # flows use plan c's kids
        if os.path.exists(ck) and not FORCE:
            pairs['%s|%s' % (a, c)] = json.load(open(ck)); continue
        flows = collections.Counter(); diff = 0.0
        for x, y, ww in zip(labs[a], labs[c], KW[c]):   # kids of the later plan (as its scorecard's kids_reassigned_vs_*)
            if x != y:
                flows[(x, y)] += ww; diff += ww
        ga, gc = geoms[a], geoms[c]
        cn = list(gc); tree = shapely.STRtree([gc[m] for m in cn])
        groups = collections.defaultdict(list)
        for n, g in ga.items():
            for j in tree.query(g):
                m = cn[j]
                if m == n:
                    continue
                ix = g.intersection(gc[m])
                if not ix.is_empty and ix.area > 1:
                    groups[(n, m)].append(ix)
        moved = collections.defaultdict(list)          # (school under a, school under c) -> moved blocks
        for i, (x, y) in enumerate(zip(labs[a], labs[c])):
            if x != y and KW[c][i] > 0:
                moved[(x, y)].append(i)
        regs = []; tot_area = 0.0
        for (n, m), ps in groups.items():
            fk = flows.get((n, m), 0)
            if round(fk) < 1:
                continue
            U = unary_union(ps).buffer(-14).buffer(14).simplify(4.0)
            polys = [U] if U.geom_type == 'Polygon' else [p for p in getattr(U, 'geoms', []) if p.geom_type == 'Polygon']
            polys = [(p, e) for p in polys if p.area >= 3000 for e in [enc_geom(p)] if e]
            if not polys:
                continue
            # each piece carries the kids of the moved blocks inside it (a block outside every drawn piece goes to the
            # nearest one), rounded so a move's pieces add up to its flow; before, every piece repeated the whole flow
            share = np.zeros(len(polys)); tr = shapely.STRtree([p for p, _ in polys])
            for i in moved.get((n, m), []):
                hit = [j for j in tr.query(PTS[i]) if polys[j][0].covers(PTS[i])]
                j = hit[0] if hit else int(np.argmin([p.distance(PTS[i]) for p, _ in polys]))
                share[j] += KW[c][i]
            cnt = lr_round({j: share[j] / max(share.sum(), 1e-9) * fk for j in range(len(polys))}, round(fk))
            for j, (p, e) in enumerate(polys):
                regs.append([n, m, cnt[j], e]); tot_area += p.area
        fl = sorted(([x, y, round(v)] for (x, y), v in flows.items() if round(v) >= 3), key=lambda r: -r[2])[:100]
        pairs['%s|%s' % (a, c)] = P = {'n': round(diff), 'tot': round(float(KW[c].sum())), 'regs': regs, 'flows': fl, 'km2': round(tot_area / 1e6, 2)}
        json.dump(P, open(ck, 'w'), separators=(',', ':'))
    # past a closer school, block by block (not cached: cheap): px = [kids past under a only ("fixed by c"), under c only
    # ("new under c"), under both (a's kids), under both (c's kids)]; the map draws the same split from the two plans' regions
    for pk, P in pairs.items():
        a, c = pk.split('|'); pa, pc_ = SBP[a]['past'], SBP[c]['past']; wa, wc = KW[a], KW[c]
        # rounded so the legend adds up exactly: fixed + both = plan a's past.n, new + both = plan c's (the "both" parts are
        # rounded on their own and the one-plan parts take the remainder; each total is the scorecard figure)
        b1, b2 = round(float(wa[pa & pc_].sum())), round(float(wc[pa & pc_].sum()))
        P['px'] = [plans[a]['past']['n'] - b1, plans[c]['past']['n'] - b2, b1, b2]
        assert P['px'][0] >= 0 and P['px'][1] >= 0 and abs(P['px'][0] - float(wa[pa & ~pc_].sum())) <= 2 and abs(P['px'][1] - float(wc[~pa & pc_].sum())) <= 2, (pk, P['px'])
    log('  pairs', len(pairs))
    sch = {}
    for k in plans:
        for n in list(plans[k]['poly']) + [p[0] for p in plans[k]['prog']]:
            if n not in sch:
                c = ST.coords(n)
                if c:
                    sch[n] = c
    w0 = KW[order[0]]          # district kid total / kids-of-color share: first plan (the baseline) on the scorecard basis
    kocd = round(100 * float((w0 * POC).sum() / w0.sum()), 1)
    # where kids live: the baseline's kids summed on a 400 m grid (cells with under half a kid left out); the map's
    # "Where kids live" and "Where kids move" themes shade by kids per km2 in steps (den.b, rounded cell quantiles)
    XY = block_xy(); ix = np.floor(XY[:, 0] / DEN_M).astype(int); iy = np.floor(XY[:, 1] / DEN_M).astype(int)
    cell = collections.Counter()
    for i, j, ww in zip(ix, iy, w0):
        cell[(int(i), int(j))] += float(ww)
    cells = sorted([i, j, round(v, 1)] for (i, j), v in cell.items() if v >= 0.5)
    dk = np.array([c[2] for c in cells]) / (DEN_M * DEN_M / 1e6)
    nice = lambda v: float('%.2g' % v) if v < 100 else float(round(v, -1))
    br = sorted({nice(np.quantile(dk, q)) for q in (0.2, 0.4, 0.6, 0.8)})
    den = {'dx': DEN_M / MX, 'dy': DEN_M / LAT_M, 'm': DEN_M, 'b': br, 'cells': cells}
    # "Walk to assigned school" theme: per plan, each density cell's kid-weighted average walk to the school that plan
    # assigns (scorebasis d = metrics.py walk miles, the plan's own scorecard kids), in hundredths of a mile, in den.cells
    # order; -1 = under 0.05 of the plan's kids in the cell
    cidx = {(c[0], c[1]): n for n, c in enumerate(cells)}
    bc = np.array([cidx.get((int(i), int(j)), -1) for i, j in zip(ix, iy)])
    for k in plans:
        w, d = KW[k], SBP[k]['d']
        ok = (bc >= 0) & np.isfinite(d) & (w > 0)
        sw = np.bincount(bc[ok], weights=w[ok], minlength=len(cells))
        swd = np.bincount(bc[ok], weights=(w * d)[ok], minlength=len(cells))
        plans[k]['wk'] = [int(round(100 * a / b)) if b >= 0.05 else -1 for a, b in zip(swd, sw)]
    LVDATA[lv] = {'plans': plans, 'pairs': pairs, 'total': round(float(w0.sum())), 'sch': sch, 'kocd': kocd, 'den': den}

# ------------------------------------------------------------------ "Closer walk" theme (map color=closer)
# For a fixed set of two or three schools: which is the shortest walk, on a fine grid (CLOSER_M) over the PPS Status Quo
# areas listed. Several sets per level (the map's picker; the first is the level's default). Same walk matrix as the "walk"
# theme and the scorecards (solver common.dist('walk'), via scorebasis), PPS Status Quo's 2031-32 kids. focus (optional) =
# the closing school whose kids the legend headline counts (its Status Quo area at focus_lv); without one the headline
# counts every covered block. A block goes to its closest school (a two-way exact tie to the second, as irvington_walks.py).
# A level with no set shows a short key instead.
CLOSER = [   # key = URL cpair=; picking one zooms the map to its areas
    {'key': 'sabin-bc', 'lv': 'K-5', 'schools': ['Sabin', 'Beverly Cleary'], 'areas': ['Irvington', 'Sabin', 'Beverly Cleary'], 'focus': 'Irvington', 'focus_lv': 'K-5'},
    {'key': 'sabin-bc-king', 'lv': 'K-5', 'schools': ['Sabin', 'Beverly Cleary', 'MLK Jr'], 'areas': ['Irvington', 'Sabin', 'MLK Jr']},
    {'key': 'bc-buckman', 'lv': 'K-5', 'schools': ['Beverly Cleary', 'Buckman'], 'areas': ['Beverly Cleary', 'Buckman', 'Sunnyside']},
    {'key': 'beach-be', 'lv': 'K-5', 'schools': ['Beach', 'Boise-Eliot/Humboldt'], 'areas': ['Beach', 'Boise-Eliot/Humboldt']},
    {'key': 'beaumont-tubman', 'lv': '6-8', 'schools': ['Beaumont', 'Tubman'], 'areas': ['Beaumont', 'Tubman'], 'focus': 'Irvington', 'focus_lv': 'K-5'},
]
CLOSER_M = 150.0
CL_TIE = 0.10                      # "about the same" band, miles (as the walk overlay's middle step)
_sq = next(o for o in OPTS if o['name'] == 'status_quo')
_XY = block_xy()
# hard crossings (build/safe_routes, read only): per block and school, the busy streets the shortest walk crosses with no
# signal within 25 m (walk_crossings.parquet; routed only within 1.5 walk miles). Same files as the models chat's crossing page.
SAFE = os.path.join(KIT, 'build', 'safe_routes')
_HX = pd.read_parquet(os.path.join(SAFE, 'walk_crossings.parquet'), columns=['block_idx', 'school_idx', 'hard_x', 'hard_streets'])
_RIX = SB.solver()[1].school_routing_index()
_DIR = {'Northeast': 'NE', 'Northwest': 'NW', 'Southeast': 'SE', 'Southwest': 'SW', 'North': 'N', 'South': 'S', 'East': 'E', 'West': 'W'}
_SUF = {'Street': 'St', 'Avenue': 'Ave', 'Boulevard': 'Blvd', 'Highway': 'Hwy', 'Road': 'Rd', 'Drive': 'Dr', 'Parkway': 'Pkwy'}


def st_short(n):
    """'Northeast Fremont Street' -> 'NE Fremont St' (OSM names, as on street signs)."""
    w = n.replace('Martin Luther King Junior', 'MLK Jr').split(' ')
    if len(w) > 1 and w[0] in _DIR:
        w[0] = _DIR[w[0]]
    if len(w) > 1 and w[-1] in _SUF:
        w[-1] = _SUF[w[-1]]
    return ' '.join(w)


def hard_of(school):
    """block -> list of unsignalized busy streets on the shortest walk to school ([] none; None not routed)."""
    g = _HX[_HX.school_idx == _RIX[school]]
    out = [None] * len(B)
    for bi, hx, hs in zip(g.block_idx.values, g.hard_x.values, g.hard_streets.values):
        out[int(bi)] = [st_short(x) for x in hs.split('; ')] if hx > 0 and hs else []
    return out
_BL = {}


def bus_line(school, lv):
    """The bus line (metrics.BUS: 1 mi K-5, 1.5 mi 6-8): outline of every block in the district, kids or not, whose shortest
    walk to the school is within the no-bus distance (blocks' Voronoi cells, merged). Plan-independent, so one per school."""
    if (school, lv) not in _BL:
        w = SB.solver()[1].dist('walk', [school]).astype(float)[:, 0]
        u = unary_union(list(CELLS[np.isfinite(w) & (w <= SB.solver()[0].BUS[lv])])).buffer(2).buffer(-2).simplify(12)
        _BL[school, lv] = enc_geom(u)
    return _BL[school, lv]
for lv in LEVELS:
    LVDATA[lv]['closer'] = []
for cf in CLOSER:
    lv = cf['lv']; ns = cf['schools']; fo = cf.get('focus')
    lab = load_asg(_sq, lv); flab = load_asg(_sq, cf.get('focus_lv', lv)); K = SB.kids(_sq, lv)
    Wp = SB.solver()[1].dist('walk', ns).astype(float)
    m = (np.isin(lab, cf['areas']) | (flab == fo)) & (K > 0) & np.isfinite(Wp).all(axis=1)
    ix = np.floor(_XY[:, 0] / CLOSER_M).astype(int); iy = np.floor(_XY[:, 1] / CLOSER_M).astype(int)
    acc = collections.defaultdict(lambda: np.zeros(1 + len(ns)))
    for i in np.where(m)[0]:
        acc[(int(ix[i]), int(iy[i]))] += np.r_[K[i], K[i] * Wp[i]]
    cells = sorted([i, j, round(float(v[0]), 1)] + [int(round(100 * x / v[0])) for x in v[1:]]
                   for (i, j), v in acc.items() if v[0] >= 0.05)
    # hx (parallel to cells): 0 = no unsignalized busy crossing on any school's walk for most kids here; else per school
    # -1 not routed (over 1.5 mi), 0 none, k = the main street (1-based in hn) for the kids whose walk has one, if over half
    HL = [hard_of(x) for x in ns]; hn = []; hx = []; ckey = [(c[0], c[1]) for c in cells]
    cblk = collections.defaultdict(list)
    for i in np.where(m)[0]:
        cblk[(int(ix[i]), int(iy[i]))].append(i)
    for key in ckey:
        ids = cblk[key]; kt = float(K[ids].sum()); row = []
        for q in range(len(ns)):
            rt = [i for i in ids if HL[q][i] is not None]
            if float(K[rt].sum()) < kt / 2:
                row.append(-1); continue
            hk = [i for i in rt if HL[q][i]]
            if float(K[hk].sum()) <= float(K[rt].sum()) / 2:
                row.append(0); continue
            c = collections.Counter()
            for i in hk:
                for x in dict.fromkeys(HL[q][i]):
                    c[x] += float(K[i])
            nmx = c.most_common(1)[0][0]
            if nmx not in hn:
                hn.append(nmx)
            row.append(hn.index(nmx) + 1)
        hx.append(row if any(v > 0 for v in row) else 0)
    best = len(ns) - 1 - np.argmin(Wp[:, ::-1], axis=1)       # closest school; an exact tie goes to the later school
    srt = np.sort(Wp, axis=1); near = (srt[:, 1] - srt[:, 0]) < CL_TIE

    def cnt(sel):      # kids in sel: total, then closest to each school, then top two within the tie band
        tot = round(float(K[sel].sum())); c = lr_round({k: float(K[sel & (best == k)].sum()) for k in range(len(ns))}, tot)
        return [tot] + [c[k] for k in range(len(ns))] + [round(float(K[sel & near].sum()))]
    hd = cnt(m & (flab == fo) if fo else m)
    head = {'focus': fo, 'flv': cf.get('focus_lv'), 'n': hd[0], 'c': hd[1:-1], 'tie': hd[-1]}
    by = [[n] + cnt(m & (lab == n)) for n in cf['areas']]
    # hard walks (build/safe_routes README): kids inside the no-bus distance (metrics.BUS) whose shortest walk to the school
    # crosses a busy street with no signal; per covered area (and the focus area), per school
    bus = SB.solver()[0].BUS[lv]; hard = np.array([[bool(HL[q][i]) for q in range(len(ns))] for i in range(len(B))])
    hw = [[n, [round(float(K[sel & hard[:, q] & (Wp[:, q] <= bus)].sum())) for q in range(len(ns))]]
          for n, sel in [(x, m & (lab == x)) for x in cf['areas']] + ([(fo, m & (flab == fo))] if fo and fo not in cf['areas'] else [])]
    bl = [bus_line(x, lv) for x in ns]
    LVDATA[lv]['closer'].append({'key': cf['key'], 's': ns, 'areas': cf['areas'], 'dx': CLOSER_M / MX, 'dy': CLOSER_M / LAT_M,
                                 'm': CLOSER_M, 'tie': CL_TIE, 'head': head, 'by': by, 'cells': cells, 'hx': hx, 'hn': hn, 'hw': hw, 'bus': bus, 'bl': bl})
    log('  closer', lv, cf['key'], 'cells', len(cells), 'bytes', len(json.dumps(LVDATA[lv]['closer'][-1], separators=(',', ':'))), head, by, 'hard walks', hw)
    if cf['key'] == 'sabin-bc':      # for the Sabin options page's note: Sabin takes only the Irvington blocks it is closer to
        a_, b_ = ns; dlt = Wp[:, 0] - Wp[:, 1]; own = {x: float(K[lab == x].sum()) for x in ns}; fm = m & (flab == fo)
        for t in (0.0, CL_TIE):
            tk = fm & (dlt < t)
            log('    %s takes %s blocks with walk diff < %.2f: %s %.1f, %s %.1f' % (a_, fo, t, a_, own[a_] + K[tk].sum(), b_, own[b_] + K[fm & ~tk].sum()))

# bus line for the single-plan view (map bus=1): one outline per school with an area in any plan, K-5 and 6-8 only (9-12 rides
# TriMet); the map draws those zoned in the plan shown
for lv in ['K-5', '6-8']:
    LVDATA[lv]['bl'] = {n: bus_line(n, lv) for n in sorted({n for pl in LVDATA[lv]['plans'].values() for n in pl['poly']})}
    log('  bus lines', lv, len(LVDATA[lv]['bl']), 'bytes', len(json.dumps(LVDATA[lv]['bl'], separators=(',', ':'))))

# ------------------------------------------------------------------ "Busy streets to cross" layer (map xing=1)
# pages/map_data/crossings.js, shared by every level: busy streets and their signal / marked crossings from
# build/safe_routes/cache/artn.opl + sig.opl (OSM, the routing's own extract; read only), with routes.py's rules: busy =
# trunk/primary/secondary (and links) or any arterial with 4+ lanes or a 35+ mph limit; signal = highway=traffic_signals,
# crossing=traffic_signals or crossing:signals=yes; marked = crossing=marked/zebra/uncontrolled with no signal within 25 m.
# Points within 15 m of a busy street inside the district, one per 30 m. Freeways are drawn as barriers already.
BUSY_HW = {'trunk', 'trunk_link', 'primary', 'primary_link', 'secondary', 'secondary_link'}


def _opl_tags(tok):
    out = {}
    for kv in tok[1:].split(','):
        if '=' in kv:
            k, v = kv.split('=', 1)
            out[k] = v.replace('%20%', ' ').replace('%2c%', ',')
    return out


def _num(v):
    try:
        return float(str(v).split()[0].split(';')[0])
    except (ValueError, IndexError):
        return None


def _enc_pt(x, y):
    return [round(x / MX * 1e4 + X0), round(y / LAT_M * 1e4 - Y0)]


def _enc_line(c):
    q = []
    for x, y in c:
        p = tuple(_enc_pt(x, y))
        if not q or p != q[-1]:
            q.append(p)
    return '%d,%d' % q[0] + ''.join(' %d,%d' % (b[0] - a[0], b[1] - a[1]) for a, b in zip(q, q[1:])) if len(q) >= 2 else None


def crossings_data():
    srcs = [os.path.join(SAFE, 'cache', f) for f in ('artn.opl', 'sig.opl')]
    cp = os.path.join(CACHE, 'xing_%s.json' % sha(*srcs, b'xing-2'))
    if os.path.exists(cp) and not FORCE:
        return json.load(open(cp))
    nxy = {}; byname = collections.defaultdict(list)
    for line in open(srcs[0]):
        f = line.split(' ')
        if line[0] == 'n':
            x = next(t for t in f if t[0] == 'x'); y = next(t for t in f if t[0] == 'y')
            nxy[int(f[0][1:])] = (float(x[1:]) * MX, float(y[1:]) * LAT_M)
        elif line[0] == 'w':
            T = _opl_tags(next(t for t in f if t[0] == 'T')); hw = T.get('highway', '')
            if hw in BUSY_HW or (_num(T.get('lanes')) or 0) >= 4 or (_num(T.get('maxspeed')) or 0) >= 35:
                pts = [nxy[int(n[1:])] for n in next(t for t in f if t[0] == 'N').strip()[1:].split(',') if n and int(n[1:]) in nxy]
                if len(pts) >= 2:
                    byname[st_short(T.get('name') or T.get('ref') or hw)].append(shapely.LineString(pts))
    D = district().buffer(50); lines = []; parts_all = []
    for n, ls in sorted(byname.items()):
        g = shapely.line_merge(shapely.union_all(ls)).intersection(D).simplify(6)
        ps = [g] if g.geom_type == 'LineString' else [x for x in getattr(g, 'geoms', []) if x.geom_type == 'LineString']
        ps = [x for x in ps if x.length >= 20]
        e = [x for x in (_enc_line(list(x.coords)) for x in ps) if x]
        if e:
            lines.append('|'.join(e)); parts_all += ps      # no names: drawing only (names show on the street layer)
    tree = shapely.STRtree(parts_all); sig = []; mkd = []
    for line in open(srcs[1]):
        f = line.split(' '); T = _opl_tags(next((t for t in f if t[0] == 'T'), 'T'))
        x = next(t for t in f if t[0] == 'x'); y = next(t for t in f if t[0] == 'y'); p = (float(x[1:]) * MX, float(y[1:]) * LAT_M)
        if T.get('highway') == 'traffic_signals' or T.get('crossing') == 'traffic_signals' or T.get('crossing:signals') == 'yes':
            sig.append(p)
        elif T.get('crossing') in ('marked', 'zebra', 'uncontrolled') or T.get('crossing_ref') == 'zebra':
            mkd.append(p)

    def keep(P, avoid=None):
        P = np.array(P); g = shapely.points(P)
        ok = (np.array([len(tree.query(x, predicate='dwithin', distance=15)) > 0 for x in g]) & shapely.contains_xy(D, P[:, 0], P[:, 1]))
        if avoid is not None:
            ok &= np.array([len(avoid.query(x, predicate='dwithin', distance=25)) == 0 for x in g])
        out = []; grid = {}
        for x, y in P[ok]:       # one point per 30 m
            k = (int(x // 30), int(y // 30))
            if any((x - a) ** 2 + (y - b) ** 2 < 900 for i in (-1, 0, 1) for j in (-1, 0, 1) for a, b in grid.get((k[0] + i, k[1] + j), [])):
                continue
            grid.setdefault(k, []).append((x, y)); out.append((x, y))
        return out
    S = keep(sig); M_ = keep(mkd, shapely.STRtree(shapely.points(np.array(S))))
    d = {'lines': lines, 'sig': [_enc_pt(*p) for p in S], 'mk': [_enc_pt(*p) for p in M_]}
    json.dump(d, open(cp, 'w'), separators=(',', ':'))
    return d


XING = crossings_data()
open(os.path.join(OUTD, 'crossings.js'), 'w', encoding='utf-8').write('window.XING=' + json.dumps(XING, separators=(',', ':'), ensure_ascii=False) + ';\n')
log('  crossings.js', len(XING['lines']), 'streets', len(XING['sig']), 'signals', len(XING['mk']), 'marked',
    '%.1f KB' % (os.path.getsize(os.path.join(OUTD, 'crossings.js')) / 1e3))

json.dump(QA, open(os.path.join(CACHE, 'qa_report.json'), 'w'), indent=1)

# ------------------------------------------------------------------ PROG (PPS projections + Family Guide wording for PPS scenarios)
sc = ST.schools_table()
PPSPROJ = {}
for s, k in (('A', 'scenario_A'), ('B', 'scenario_B')):
    col = 'pps_proj_2031_32_' + s
    PPSPROJ[k] = {n: int(sc.loc[n, col]) for n in sc.index if col in sc.columns and pd.notna(sc.loc[n, col]) and str(sc.loc[n, col]).replace('.', '', 1).isdigit()}

# ------------------------------------------------------------------ plan metadata
PLANS = []
for o in OPTS:
    PLANS.append({'k': o['name'], 'short': o['short'], 'full': o.get('full') or o['short'], 'label': o.get('label'), 'kind': o['kind'], 'ver': o['version_label'],
                  'lines': 'official' if o['name'] in OFFICIAL else 'crisp', 'src': o['source'], 'schools': o.get('schools_source'),
                  'assign': o['assign'], 'trade': o.get('tradeoffs'), 'basis': o.get('basis'), 'caveat': o.get('caveat') or None,
                  'linesrc': {lv: OF.SOURCE[o['name']][lv] for lv in LEVELS} if o['name'] in OFFICIAL else None,
                  'rank': o.get('brief_rank'), 'whatif': bool(o.get('what_if')), 'req': bool(o.get('request') or o.get('sabin')), 'sab': bool(o.get('sabin'))})   # brief_rank 0 = the lead plan (tagged "lead plan" on the map)
META = {'plans': PLANS, 'note': SD.get('placeholder_note'), 'model_version': SD.get('model_version'),
        'calibrated': SD.get('calibrated'), 'generated': SD.get('generated'), 'levels': SD.get('levels'),
        'ppsproj': PPSPROJ, 'method_source': SD.get('method_source'), 'targets_source': SD.get('targets_source')}

# ------------------------------------------------------------------ page
t = load_page()
def const(name, end):
    return grab(t, 'const %s=' % name, end)
BASE = grab(t, 'const BASE=`', '`;')
STREETS = grab(t, 'const STREETS=`', '`;')
OUTL = const('OUTL', ';\nconst CLOSE_A')
LBL = const('LBL', ';\nconst nm=')
SLBL = open(os.path.join(WORK, 'street_labels.txt')).read()

def js(v):
    return json.dumps(v, separators=(',', ':'), ensure_ascii=False).replace('</', '<\\/')

# every level's data is its own cached file; K-5 (the default) loads with a plain blocking <script src> right after the
# inline META, so the page text paints first and repeat visits take the ~1 MB of K-5 data from the browser cache
for lv in LEVELS:
    body = 'window.MAPLV=window.MAPLV||{};MAPLV[%s]=%s;\n' % (js(lv), js(LVDATA[lv]))
    open(os.path.join(OUTD, 'level_%s.js' % lv), 'w', encoding='utf-8').write(body)
VER = sha(*(os.path.join(OUTD, 'level_%s.js' % lv) for lv in LEVELS))
# shared street layers, the same at every level and for every plan: own files so the browser caches them across
# rebuilds that change only plan data. streets.js (collector + local streets) loads after the page; street_names.js
# (label anchors) only once the map is zoomed in far enough to show names.
open(os.path.join(OUTD, 'streets.js'), 'w', encoding='utf-8').write('window.STREETS=`' + STREETS + '`;\n')
open(os.path.join(OUTD, 'street_names.js'), 'w', encoding='utf-8').write('window.SLBL=' + js(SLBL) + ';\n')
SVER = sha(os.path.join(OUTD, 'streets.js'), os.path.join(OUTD, 'street_names.js'), os.path.join(OUTD, 'crossings.js'))

# fonts: Overpass + Overpass Mono (latin subset, variable woff2; Google Fonts, OFL) as their own cached files in
# map_data/fonts/ (were ~106 KB of base64 in <head>, re-sent with every page load); the regular face is preloaded
os.makedirs(os.path.join(OUTD, 'fonts'), exist_ok=True)
FV = {}
for f in ('ov.woff2', 'ovi.woff2', 'ovm.woff2'):
    b = open(os.path.join(HERE, 'fonts', f), 'rb').read()
    open(os.path.join(OUTD, 'fonts', f), 'wb').write(b)
    FV[f] = 'map_data/fonts/%s?v=%s' % (f, hashlib.sha1(b).hexdigest()[:10])
fonts = f"""<link rel="preload" href="{FV['ov.woff2']}" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="map_data/level_K-5.js?v=/*K5VER*/" as="script">
<style>
/* Overpass + Overpass Mono, latin subset, variable woff2 (Google Fonts, OFL), cached files in map_data/fonts/ */
@font-face{{font-family:"Overpass";font-style:normal;font-weight:400 800;font-display:swap;src:url({FV['ov.woff2']}) format("woff2")}}
@font-face{{font-family:"Overpass";font-style:italic;font-weight:400 800;font-display:swap;src:url({FV['ovi.woff2']}) format("woff2")}}
@font-face{{font-family:"Overpass Mono";font-style:normal;font-weight:400 700;font-display:swap;src:url({FV['ovm.woff2']}) format("woff2")}}
</style>""".replace('/*K5VER*/', VER)
i = t.index('<style>'); j = t.index('</style>', i)
css = t[i + 7:j]
css = css.replace('--sans:"Overpass",system-ui,-apple-system,"Segoe UI",sans-serif; --mono:"Overpass Mono",ui-monospace,Menlo,monospace;',
                  '--sans:"Overpass",system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI","Helvetica Neue",Roboto,Arial,sans-serif; --mono:"Overpass Mono",ui-monospace,"SF Mono",SFMono-Regular,Menlo,Consolas,"Liberation Mono",monospace;')
css += open(os.path.join(HERE, 'v2_head.css')).read() + open(os.path.join(HERE, 'site', 'map.css')).read()
data = ('const META=' + js(META) + ';\nwindow.MAPLV=window.MAPLV||{};\nconst LVVER=' + js(VER) + ';\nconst SVER=' + js(SVER) + ';\n'
        'const BASE=`' + BASE + '`;\nconst OUTL=' + OUTL + ';\nconst LBL=' + LBL + ';\n')
tpl = open(os.path.join(HERE, 'site', 'map.tpl.html'), encoding='utf-8').read()
page = (tpl.replace('/*GENDATE*/', SD.get('generated_label') or SD.get('generated') or '').replace('/*FONTS*/', fonts).replace('/*CSS*/', css).replace('/*DATA*/', data)
        .replace('/*K5*/', '<script src="map_data/level_K-5.js?v=%s"></script>' % VER).replace('/*JS*/', open(os.path.join(HERE, 'site', 'map.js'), encoding='utf-8').read()))
open(OUT, 'w', encoding='utf-8').write(page)

sizes = {rel(OUT): os.path.getsize(OUT)}
for f in ('level_K-5.js', 'level_6-8.js', 'level_9-12.js', 'streets.js', 'street_names.js'):
    p = os.path.join(OUTD, f); sizes[rel(p)] = os.path.getsize(p)
log('wrote', {k: '%.2f MB' % (v / 1e6) for k, v in sizes.items()})
for k, q in QA.items():
    extra = ''
    if q['method'] == 'crisp':
        extra = ' gap_m2=%s overlap_m2=%s coverage_valid=%s exclaves_with_kids=%s (assignment %s, drawn %s) mixed_faces=%s' % (
            q['gap_m2'], q['overlap_m2'], q['coverage_valid'], q['n_exclaves_with_kids'], q['n_assignment_exclaves_with_kids'],
            '%s+%s corner' % (q['drawn_exclaves_with_kids'], q['drawn_corner_touch_with_kids']), q['mixed_faces'])
    print('QA %-28s %-8s populated blocks off=%-3d kids off=%-6s max school mismatch=%s%s' % (
        k, q['method'], q['populated_blocks_off'], q['kids_off'], q['max_school_mismatch_kids'], extra))
