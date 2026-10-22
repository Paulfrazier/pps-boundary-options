"""Re-score a Plan D run's lines at PPS's bar (360 K-5 / 500 K-8 for every school but Astor/Skyline), with the
run's own zoned list (closed buildings excluded). Writes to a scratch folder; copy its scorecard.json to
out_v2/<run>/scorecard_scored360.json.  (2026-10-22: made the planD_redraw_ms 360 re-score; the earlier one, ad hoc,
used planD.json, whose K-5 list still held the six closed buildings: schools_open 54, past a closer school 1,434.)
    ../../.venv/bin/python rescore_planD360.py <run> <scratch outdir> run|planD"""
import os, sys, json, copy
import numpy as np, pandas as pd
sys.path.insert(0, 'build/solver')
import common as C, metrics as MX
run, out, base = sys.argv[1], sys.argv[2], sys.argv[3]   # base: 'run' (run cfg, exempt -> Astor/Skyline) or 'planD'
cfgdir = os.path.join(C.SOLVER, 'configs', 'v2')
if base == 'planD':
    cfg = C.load_config(os.path.join(cfgdir, 'planD.json'))
else:
    cfg = copy.deepcopy(C.load_config(os.path.join(cfgdir, run + '.json')))
    cfg['exempt_floor'] = ['Astor', 'Skyline']
    cfg['durability'] = {k: v for k, v in cfg['durability'].items() if k != 'note'}
cfg = copy.deepcopy(cfg)
cfg['name'] = run + '_scored360'
cfg['label'] = ("Plan D (a board member's alternative, per the Oregonian 2026-10-20), lines redrawn (" + run + "), re-scored at "
                "PPS's bar: every K-5 but Astor and Skyline counted against 360 (K-8 500); same lines as scorecard.json")
src = os.path.join(C.SOLVER, 'out_v2', run + '.staging')
if not os.path.isdir(src):
    src = os.path.join(C.SOLVER, 'out_v2', run)
plan = {lev: pd.read_parquet(os.path.join(src, f'assign_{lev}.parquet')).sort_values('idx')['school'].values.astype(object)
        for lev in C.LEVELS}
refs = MX.load_refs(cfgdir)
sc = MX.write_plan(out, cfg, plan, refs)
print(json.dumps({lev: {k: sc['levels'][lev].get(k) for k in ('schools_open', 'kids_past_closer_school', 'schools_in_range_non_exempt')} for lev in C.LEVELS}))
d = sc['durability']['levels']['K-5']; print({k: d[k] for k in d if k != 'schools'})
