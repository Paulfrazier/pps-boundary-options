"""Plan D (a board member's alternative, per the Oregonian 2026-10-20; build/pps-texts/oregonian-2026-10-20-splitt-scenario-d.md), as written.

Status Quo 2027-28 lines and programs, with six K-5 closures sent to receivers. Not solved: scored like the PPS
baselines. Writes out_v2/planD.staging/ (TRACKS.md write rule).  Run from build/solver:
    ../../.venv/bin/python build_planD.py
Receivers: from the article where it names them; otherwise PPS A's (data/scenarios.json), flagged ASSUMED.
"Some to X, the rest to Y" is split by shortest walk per block (the PPS-plan rule in CLAUDE.md).
"""
import os, json, copy
import numpy as np, pandas as pd
import common as C, metrics as MX

CLOSE = {   # closed K-5 area (sq_es) -> receivers; 'A_es' = take PPS A's block column
    'Creston':   (['Arleta'], 'article: merges with Arleta; DHH program moves with it (DHH not modeled)'),
    'Sabin':     (['MLK Jr', 'Vernon'], 'article: some to Vernon, rest to King; split by shortest walk'),
    'Woodmere':  (['Whitman', 'Lewis'], 'article: some to Lewis; rest ASSUMED Whitman (PPS A); split by shortest walk'),
    'Buckman':   ('A_es', 'ASSUMED PPS A: Abernethy south of Burnside, Sunnyside north (article gives no receiver)'),
    'Irvington': (['Beverly Cleary'], 'ASSUMED PPS A: Beverly Cleary (article gives no receiver)'),
    'Peninsula': (['Rosa Parks'], 'ASSUMED PPS A: Rosa Parks (article gives no receiver)'),
}

cfg = C.load_config(os.path.join(C.SOLVER, 'configs', 'v2', 'status_quo.json'))
cfg = copy.deepcopy(cfg)
cfg['name'] = 'planD'
cfg['kind'] = 'request'
cfg['label'] = ("Plan D (a board member's alternative, per the Oregonian 2026-10-20), as written: Status Quo lines, grade setups and "
                "immersion programs; closes Creston, Buckman, Woodmere, Sabin, Irvington, Peninsula")
# Buckman's arts focus closes with its building (as PPS A); its lottery kids split like its neighborhood area
cfg['v2']['focus_lottery']['Buckman']['placement'] = {'K-5': {'Abernethy': 0.5, 'Sunnyside': 0.5}}
cfg['planD_receivers'] = {k: {'to': v[0], 'how': v[1]} for k, v in CLOSE.items()}
# (2026-10-22 fix) closed buildings are not zoned: status_quo.json's K-5 list still had all six, so they were scored
# as open (schools_open 54), non-exempt and empty (n_zoned_non_exempt 50), and counted as 'a closer school' in
# kids_past_closer_school. Drop them so the scorecard sees Plan D's 48 K-5 buildings (46 zoned + 2 program-only).
cfg['levels']['K-5']['zoned'] = [s for s in cfg['levels']['K-5']['zoned'] if s not in CLOSE]
for lev_ in ('6-8', '9-12'):
    assert not set(CLOSE) & set(cfg['levels'][lev_]['zoned']), lev_
json.dump(cfg, open(os.path.join(C.SOLVER, 'configs', 'v2', 'planD.json'), 'w'), indent=1)

b = C.blocks()
plan = MX.plan_from_columns(cfg)                 # SQ lines (Lent area -> Marysville as in Status Quo)
k5 = plan['K-5'].copy()
sq = b['sq_es'].values
log = []
for area, (to, how) in CLOSE.items():
    m = sq == area
    if to == 'A_es':
        k5[m] = b['A_es'].values[m]
    elif len(to) == 1:
        k5[m] = to[0]
    else:
        W = C.dist('walk', to)
        k5[m] = np.array(to, dtype=object)[np.nanargmin(np.where(np.isfinite(W[m]), W[m], 1e9), axis=1)]
    log.append((area, how, pd.Series(k5[m]).value_counts().to_dict()))
plan['K-5'] = k5
assert not set(CLOSE) & set(k5), 'a closed school still has blocks'

refs = MX.load_refs(os.path.join(C.SOLVER, 'configs', 'v2'))
sc = MX.write_plan(os.path.join(C.SOLVER, 'out_v2', 'planD.staging'), cfg, plan, refs)
K = MX.level_kids(cfg)['K-5']
for area, how, cnt in log:
    kids = {s: round(float(K[(sq == area) & (k5 == s)].sum())) for s in cnt}
    print(f'{area}: {how}; 2031-32 K-5 kids by receiver {kids}')
d = sc['durability']
print({lev: list(d['levels'][lev]['at_target_zoned'].values()) for lev in C.LEVELS})
