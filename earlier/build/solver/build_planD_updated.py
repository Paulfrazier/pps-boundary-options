"""Plan D, updated (a board member's draft framework, Google Doc revised after its 10/23 posting;
build/pps-texts/scenario-d-draft-framework-2026-10-25.md), as written.

Successor to build_planD.py (which followed the Oregonian 2026-10-20 account). What changed vs planD:
  - Sabin stays open (Sabin -> King/Vernon removed: Sabin's SES program does not fit).
  - The doc now names every receiver (Irvington -> Beverly Cleary, Peninsula + Chavez neighborhood -> Rosa Parks,
    Woodmere -> Whitman with ~76 to Lewis as in Scenario B, Buckman -> Abernethy / Sunnyside as in A/B).
  - Middle-school changes: Beverly Cleary, Laurelhurst, Sunnyside, Bridger, Faubion and Vernon become K-5;
    Beaumont Spanish DLI -> Roseway Heights; Creston area -> Kellogg, Maplewood -> Gray, Lewis -> Lane (Brentwood).
Status Quo everywhere else. Not solved: scored like the PPS baselines. Writes out_v2/planD_updated.staging/
(TRACKS.md write rule). Run from build/solver:
    ../../.venv/bin/python build_planD_updated.py
Not modeled (focus / program kids outside the block model, or too small to place): Odyssey into MLC and East Sylvan
closing, MLC 9-12 (~40) to Lincoln, Creston DHH and Woodmere CB classrooms, the Meadowlark Place and Bybee Lake
shelter slivers, Skyline 9-12 choice (Status Quo Lincoln kept), the phased Beaumont DLI move (modeled at its end
state; 2027-29 cohorts staying at Beaumont are not), lottery caps / start-grade changes.
"""
import os, json, copy
import numpy as np, pandas as pd
import common as C, metrics as MX

# closed K-5 area (sq_es) -> how its blocks are placed
CLOSE = {
    'Creston':   (['Arleta'], 'doc: Creston merges with Arleta (DHH program moves with it; not modeled)'),
    'Woodmere':  ('B_es', 'doc: Woodmere -> Whitman, ~76 to Lewis as in Scenario B (B_es: Woodmere area -> Whitman, '
                          'part of Whitman area -> Lewis)'),
    'Peninsula': (['Rosa Parks'], 'doc: Peninsula -> Rosa Parks (same as A/B)'),
    'Irvington': (['Beverly Cleary'], 'doc: Irvington merges with Beverly Cleary (same as A/B)'),
    'Buckman':   ('A_es', 'doc: some to Abernethy, rest to Sunnyside (variation on A/B; A_es lines used)'),
}
# Chavez's neighborhood program merges into Rosa Parks (same as A/B); Chavez stays a whole-school DLI K-8
CHAVEZ_AREA_TO = 'Rosa Parks'
TO_K5 = ['Beverly Cleary', 'Laurelhurst', 'Sunnyside', 'Bridger', 'Faubion', 'Vernon']   # K-8 -> K-5
MS_FROM_K8 = {'Beverly Cleary': 'Beaumont', 'Laurelhurst': 'Mt Tabor', 'Sunnyside': 'Hosford',
              'Bridger': 'Harrison Park', 'Faubion': 'Ockley Green', 'Vernon': 'Tubman'}
MS_BY_ES = {'Creston': 'Kellogg', 'Maplewood': 'Gray', 'Lewis': 'Lane',   # by Status Quo elementary area
            # Irvington merges into Beverly Cleary "same as A/B" (A_ms: Beaumont); the doc keeps only the current
            # Irvington 5th graders at Tubman ("Moving just current Beverly Cleary students into Beaumont in fall 2027",
            # DLI 6th/7th stay 2027-29), so the end state modeled here is Beaumont
            'Irvington': 'Beaumont',
            # Peninsula merges into Rosa Parks "same as A/B": Rosa Parks feeds George, and A_ms / B_ms send Peninsula
            # to George; keeping SQ Ockley Green would split Rosa Parks graduates between two middle schools
            'Peninsula': 'George'}
# (Kelly graduates stay at Lane/Brentwood: removed from the doc's list of moves)

cfg = C.load_config(os.path.join(C.SOLVER, 'configs', 'v2', 'status_quo.json'))
cfg = copy.deepcopy(cfg)
cfg['name'] = 'planD_updated'
cfg['kind'] = 'request'
cfg['label'] = ("Plan D, updated (a board member's draft framework, revised after 2026-10-23), as written: closes Creston, "
                "Woodmere, Peninsula, Irvington, Buckman (Sabin stays open); Beverly Cleary, Laurelhurst, Sunnyside, "
                "Bridger, Faubion, Vernon become K-5; Beaumont Spanish to Roseway Heights; Status Quo elsewhere")
cfg['planD_receivers'] = {k: {'to': v[0], 'how': v[1]} for k, v in CLOSE.items()}
cfg['planD_receivers']['Cesar Chavez'] = {'to': [CHAVEZ_AREA_TO], 'how': 'doc: neighborhood program -> Rosa Parks; '
                                                                         'Chavez stays whole-school DLI K-8'}
cfg['planD_ms'] = {'k8_to_k5': MS_FROM_K8, 'by_es_area': MS_BY_ES, 'Beaumont|Spanish': 'Roseway Heights'}

K5, MS = cfg['levels']['K-5'], cfg['levels']['6-8']
K5['zoned'] = [s for s in K5['zoned'] if s not in CLOSE and s != 'Cesar Chavez']
MS['zoned'] = [s for s in MS['zoned'] if s not in TO_K5 and s != 'Cesar Chavez']
for L in (K5, MS):
    L['k8'] = [s for s in L['k8'] if s not in TO_K5]
assert 'Cesar Chavez' in K5['programs'] and 'Cesar Chavez' in MS['programs']   # program-only host, both bands
MS['programs']['Beaumont'] = [k for k in MS['programs']['Beaumont'] if k != 'Beaumont|Spanish']
MS['programs']['Roseway Heights'] = MS['programs']['Roseway Heights'] + ['Beaumont|Spanish']
fl = cfg['v2']['focus_lottery']
fl['Buckman']['placement'] = {'K-5': {'Abernethy': 0.5, 'Sunnyside': 0.5}}   # as planD / PPS A
fl['Sunnyside']['placement'] = {'K-5': 'host', '6-8': {'Hosford': 1.0}}      # doc: all Sunnyside kids can go to Hosford
fl['Bridger']['placement'] = {'K-5': 'host', '6-8': {'Harrison Park': 1.0}}  # doc: lottery Bridger 6-8 -> Harrison Park
json.dump(cfg, open(os.path.join(C.SOLVER, 'configs', 'v2', 'planD_updated.json'), 'w'), indent=1)

b = C.blocks()
plan = MX.plan_from_columns(cfg)                 # SQ lines (Lent area -> Marysville as in Status Quo)
sq_es, sq_ms = b['sq_es'].values, b['sq_ms'].values
k5, ms = plan['K-5'].copy(), plan['6-8'].copy()
log = []
for area, (to, how) in CLOSE.items():
    m = sq_es == area
    if isinstance(to, str):
        k5[m] = b[to].values[m]
    else:
        k5[m] = to[0]
    log.append((area, how, m))
# Scenario B's Woodmere piece: B_es moves part of Whitman's area to Lewis
mw = (sq_es == 'Whitman') & (b['B_es'].values == 'Lewis')
k5[mw] = 'Lewis'
log.append(('Whitman (part)', 'Scenario B: part of Whitman area -> Lewis to make room for Woodmere', mw))
mc = sq_es == 'Cesar Chavez'
k5[mc] = CHAVEZ_AREA_TO
log.append(('Cesar Chavez', 'neighborhood program -> Rosa Parks', mc))
for k8, to in MS_FROM_K8.items():
    ms[sq_ms == k8] = to
for es, to in MS_BY_ES.items():
    ms[sq_es == es] = to
mcm = sq_ms == 'Cesar Chavez'
ms[mcm] = b['A_ms'].values[mcm]                  # Chavez neighborhood 6-8 as in A/B (George)
plan['K-5'], plan['6-8'] = k5, ms
for lev, arr in (('K-5', k5), ('6-8', ms)):
    bad = set(arr) - set(cfg['levels'][lev]['zoned'])
    assert not bad, (lev, bad)

refs = MX.load_refs(os.path.join(C.SOLVER, 'configs', 'v2'))
sc = MX.write_plan(os.path.join(C.SOLVER, 'out_v2', 'planD_updated.staging'), cfg, plan, refs)
K = MX.level_kids(cfg)
for area, how, m in log:
    kids = {s: round(float(K['K-5'][m & (k5 == s)].sum())) for s in pd.unique(k5[m])}
    print(f'{area}: {how}; 2031-32 K-5 kids by receiver {kids}')
d = sc['durability']
print({lev: list(d['levels'][lev]['at_target_zoned'].values()) for lev in C.LEVELS})
