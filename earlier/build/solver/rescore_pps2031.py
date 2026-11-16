"""Re-score an existing v2 result on the pps2031 horizon without re-solving (Paul 2026-10-12 ~15:15).
Writes out_v2/<run>.staging/ (TRACKS.md write rule); promote with promote_v2.py.

  python rescore_pps2031.py today status_quo scenario_A scenario_B        (baselines: lines from PPS columns)
  python rescore_pps2031.py option1_durable_msfeed_off --config option1_durable
        (a solved run: its own assign_*.parquet, scored with configs/v2/<config>.json, which must carry the same
         schools/programs; the scorecard's other keys, e.g. 'solve', are kept)
"""
import argparse, json, os, shutil
import numpy as np, pandas as pd
import common as C, metrics as MX

OUT = os.path.join(C.SOLVER, 'out_v2')
BASE = ('today', 'status_quo', 'scenario_A', 'scenario_B')


def rescore(run, cfgname=None):
    cfg = C.load_config(os.path.join(C.SOLVER, 'configs', 'v2', f'{cfgname or run}.json'))
    assert C.horizon(cfg)[0] == 'pps2031', 'config must carry "horizon": "pps2031"'
    cfg['name'] = run
    src, st = os.path.join(OUT, run), os.path.join(OUT, run + '.staging')
    os.makedirs(st, exist_ok=True)
    refs = MX.load_refs(os.path.join(C.SOLVER, 'configs', 'v2'))
    if run in BASE:
        plan = MX.plan_from_columns(cfg)
        sc = MX.write_plan(st, cfg, plan, refs)
    else:
        plan = {lev: pd.read_parquet(os.path.join(src, f'assign_{lev}.parquet'))['school'].values.astype(object)
                for lev in C.LEVELS}
        old = json.load(open(os.path.join(src, 'scorecard.json')))
        for f in os.listdir(src):       # solve_log, infeasibility, checkpoint, dli_moves ... (not the outputs we rewrite)
            if f not in ('scorecard.json', 'schools.csv', 'TRADEOFFS.md') and not f.startswith('assign_'):
                shutil.copy2(os.path.join(src, f), os.path.join(st, f))
        keep = {k: v for k, v in old.items() if k not in ('levels', 'durability', 'programs', 'name', 'label', 'basis')}
        keep['rescored'] = (f'2026-10-12: re-scored on horizon pps2031 with configs/v2/{cfgname or run}.json; '
                            'lines unchanged from the original solve (solved under horizon psu2041)')
        sc = MX.write_plan(st, cfg, plan, refs, extra=keep)
    d = sc['durability']
    print(run, {lev: (list(d['levels'][lev]['at_target_zoned'].values()), d['levels'][lev]['at_target_all_required_years'])
                for lev in C.LEVELS})
    return sc


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('runs', nargs='+')
    ap.add_argument('--config')
    a = ap.parse_args()
    for r in a.runs:
        rescore(r, a.config)
