"""(2026-10-28) The Tubman-at-Vernon northeast package on another plan, spliced (no solver). Paul: "do a run of vernon
thats more like b, and more like d", and the lead plan with Rose City Park kept open (PPS B and Plan D keep it, 391-370).
Northeast package = tubman_at_vernon_beh (Tubman's middle school in the Vernon building; Vernon's elementary families to
Sabin or King; Irvington to Beverly Cleary, its west part to Boise-Eliot/Humboldt; Sabin, King and Vernon on to Tubman at
Vernon and Jefferson; Boise-Eliot to Ockley Green; Faubion's main neighborhood to Vernon).
  K-5:  blocks in today's Sabin, Irvington, Vernon, King, Alameda, Beverly Cleary and Boise-Eliot/Humboldt areas take
        the package's school; every other block keeps the base plan's (so the base's own closures, receivers and
        programs stand outside those seven areas)
  6-8:  blocks whose base middle school is in the NE (Tubman, Beaumont, Ockley Green, Roseway Heights, or the Vernon /
        Faubion K-8s) take the package's middle school where the package sends them to an NE middle school; the base's
        Tubman becomes the Tubman middle school in the Vernon building
  9-12: the base's, with the package's reassignments in the seven areas (Sabin and Vernon areas to Jefferson,
        Irvington to Grant)
  --rcp-open: Rose City Park stays open as today (its area and its Vietnamese program back in its building)
Cut-off K-5 / 6-8 pieces join their neighbours' majority school; scored with metrics.write_plan.
    usage: build_tubvern_on.py <base run> <new run> "<label>" [--rcp-open]
"""
import json, os, sys, copy
from collections import deque, Counter
import numpy as np, pandas as pd
import common as C, metrics as MX

base, run, label = sys.argv[1:4]
RCP = '--rcp-open' in sys.argv
MAND = '--king-mandarin-home' in sys.argv   # King's Mandarin program stays at King (PPS B moves it to Boise-Eliot/Humboldt)
PKG = 'tubman_at_vernon_beh'
AREAS = ['Sabin', 'Irvington', 'Vernon', 'MLK Jr', 'Alameda', 'Beverly Cleary', 'Boise-Eliot/Humboldt']
NE_MS = ['Vernon', 'Beaumont', 'Ockley Green', 'Roseway Heights']
CFG_DIR = os.path.join(C.SOLVER, 'configs', 'v2'); O2 = os.path.join(C.SOLVER, 'out_v2')
rd = lambda r, lev: pd.read_parquet(os.path.join(O2, r if os.path.isdir(os.path.join(O2, r)) else r + '.staging', f'assign_{lev}.parquet')).sort_values('idx')['school'].values.astype(object).copy()
bj = json.load(open(os.path.join(CFG_DIR, f'{base}.json')))
pj = json.load(open(os.path.join(CFG_DIR, f'{PKG}.json')))
es = C.blocks()['sq_es'].values
sq68 = rd('status_quo', '6-8')

c = copy.deepcopy(bj)
c['name'] = run; c['kind'] = 'request'; c['label'] = label
c['label_detail'] = (f"{bj.get('label', base)} everywhere, with the Tubman-at-Vernon northeast package in today's Sabin, "
                     "Irvington, Vernon, King, Alameda, Beverly Cleary and Boise-Eliot/Humboldt areas and the NE middle "
                     "schools: Tubman's middle school in the Vernon building, Vernon's families to Sabin or King, Irvington to "
                     "Beverly Cleary (west part to Boise-Eliot/Humboldt)." + (" Rose City Park stays open." if RCP else ""))
c['feed_note'] = f'spliced by build_tubvern_on.py: {base} with the NE package from {PKG}' + (', Rose City Park open' if RCP else '') + '; not solved'
k5c, m8c = c['levels']['K-5'], c['levels']['6-8']
for lev in ('K-5', '6-8', '9-12'):
    for key in ('start', 'fixed_run', 'warm_start', 'hint_run'):
        c['levels'][lev].pop(key, None)
k5c['zoned'] = sorted((set(k5c['zoned']) | {'Sabin', 'MLK Jr', 'Alameda', 'Beverly Cleary', 'Boise-Eliot/Humboldt'}) - {'Vernon', 'Irvington'})
k5c['k8'] = [s for s in k5c.get('k8', []) if s in k5c['zoned']]
m8c['zoned'] = sorted({('Vernon' if s == 'Tubman' else s) for s in m8c['zoned']} | {'Vernon'})
m8c['programs'] = {('Vernon' if k == 'Tubman' else k): v for k, v in m8c.get('programs', {}).items()}
m8c['k8'] = [s for s in m8c.get('k8', []) if s in m8c['zoned'] and s != 'Vernon']
c['capacity_overrides'] = dict(c.get('capacity_overrides', {}), Vernon=pj['capacity_overrides']['Vernon'])
c['capacity_note'] = pj.get('capacity_note', '')
if '--no-relief-cap' in sys.argv:   # big-school relief caps from the base don't apply in the package's areas, which hold their own lines
    for s_ in AREAS:
        if s_ not in pj['capacity_overrides']:
            c['capacity_overrides'].pop(s_, None)
if RCP:
    k5c['zoned'] = sorted(set(k5c['zoned']) | {'Rose City Park'})
    pr = {h: [p for p in ps if p != 'Rose City Park|Vietnamese'] for h, ps in k5c.get('programs', {}).items()}
    pr = {h: ps for h, ps in pr.items() if ps}
    pr['Rose City Park'] = pr.get('Rose City Park', []) + ['Rose City Park|Vietnamese']
    k5c['programs'] = pr
if MAND:
    pr = {h: [p for p in ps if p != 'MLK Jr|Mandarin'] for h, ps in k5c.get('programs', {}).items()}
    pr = {h: ps for h, ps in pr.items() if ps}
    pr['MLK Jr'] = pr.get('MLK Jr', []) + ['MLK Jr|Mandarin']
    k5c['programs'] = pr
    c['label_detail'] += " King's Mandarin program stays at King."
    c['feed_note'] += "; King's Mandarin stays at King"
json.dump(c, open(os.path.join(CFG_DIR, f'{run}.json'), 'w'), indent=1)
cfg = C.load_config(os.path.join(CFG_DIR, f'{run}.json'))

bp = {lev: rd(base, lev) for lev in C.LEVELS}
pk = {lev: rd(PKG, lev) for lev in C.LEVELS}
plan = {lev: bp[lev].copy() for lev in C.LEVELS}
inA = np.isin(es, AREAS)
plan['K-5'][inA] = pk['K-5'][inA]
if RCP:
    plan['K-5'][es == 'Rose City Park'] = 'Rose City Park'
# any base school no longer zoned (e.g. the base's Vernon K-5 or a closed school outside the areas): package's school
zon = set(k5c['zoned'])
bad = ~np.isin(plan['K-5'], list(zon))
plan['K-5'][bad] = pk['K-5'][bad]
# still unzoned (the package's school is closed in this base, e.g. Rigler as immersion-only): nearest open school by walk
still = ~np.isin(plan['K-5'], list(zon))
if still.any():
    zl = sorted(zon); Wz = C.dist('walk', zl)
    plan['K-5'][still] = np.array(zl, dtype=object)[np.nanargmin(np.where(np.isnan(Wz[still]), np.inf, Wz[still]), axis=1)]
    print('K-5 blocks to nearest open school:', int(still.sum()))
plan['6-8'][plan['6-8'] == 'Tubman'] = 'Vernon'
neMS = np.isin(sq68, ['Tubman', 'Vernon', 'Beaumont', 'Ockley Green', 'Roseway Heights', 'Faubion']) & np.isin(pk['6-8'], NE_MS)
plan['6-8'][neMS] = pk['6-8'][neMS]
bad8 = ~np.isin(plan['6-8'], list(m8c['zoned']))
plan['6-8'][bad8] = pk['6-8'][bad8]
plan['9-12'][inA] = pk['9-12'][inA]
ch = {lev: int((plan[lev] != bp[lev]).sum()) for lev in C.LEVELS}
print(run, 'blocks changed from', base, ch, '| K-5 fallbacks', int(bad.sum()), '| 6-8 fallbacks', int(bad8.sum()))

NB = C.adjacency()[0]; roots = C.school_block(); orphans = []
for lev in ('K-5', '6-8'):
    a = plan[lev]
    for sch in sorted(set(a)):
        if sch not in roots:
            continue
        idx = set(map(int, (a == sch).nonzero()[0])); st = {roots[sch]} & idx or {next(iter(idx))}; q = deque(st)
        while q:
            i = q.popleft()
            for j in NB[i]:
                if j in idx and j not in st:
                    st.add(j); q.append(j)
        # only pieces the splice made: the base plan's own detached pieces (PPS's lines) are left as they are
        cut = sorted(i for i in idx - st if bp[lev][i] != sch or (lev == 'K-5' and inA[i]))
        while cut:
            lft = []
            for i in cut:
                nb = Counter(a[j] for j in NB[i] if a[j] != sch)
                if nb: a[i] = nb.most_common(1)[0][0]; orphans.append((lev, sch, a[i]))
                else: lft.append(i)
            if len(lft) == len(cut):
                break
            cut = lft
print('orphans fixed', len(orphans), Counter(orphans).most_common(10))
refs = MX.load_refs(CFG_DIR)
out = os.path.join(O2, f'{run}.staging')
MX.write_plan(out, cfg, plan, refs, extra={'note_feed': c['feed_note']})
with open(os.path.join(out, 'solve_log.txt'), 'w') as f:
    f.write(f'{run}: {c["feed_note"]}; blocks changed {ch}; orphans {len(orphans)}\n')
json.dump({'schools_out_of_range_2031_32': [], 'solver_slack': f'not solved: {c["feed_note"]}',
           'feeder_splits_used': 'as the two source plans'}, open(os.path.join(out, 'infeasibility.json'), 'w'), indent=1)
