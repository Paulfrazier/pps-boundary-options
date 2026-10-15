"""Reconnect a line-cleanup candidate's new real K-5 pockets by restoring the live plan's K-5/6-8 assignment for the
candidate's changed blocks within --radius miles of each pocket (overnight 2026-10-12/13; used where a pocket is
size-locked: its school and neighbours sit at their floors, so smooth_v2's swap finds nothing).
  python revert_pockets.py <candidate> <live> [--radius 0.8]"""
import argparse, json
import numpy as np, pandas as pd
import common as C, metrics as MX, lines_qa as Q

ap = argparse.ArgumentParser(); ap.add_argument('cand'); ap.add_argument('live'); ap.add_argument('--radius', type=float, default=0.8)
a = ap.parse_args()
b = C.blocks(); x, y = b['x'].values, b['y'].values
st = f'out_v2/{a.cand}.staging'
pk = Q.qa(a.cand, True)['K-5']['pockets']
cand = {lev: pd.read_parquet(f'{st}/assign_{lev}.parquet')['school'].values.astype(object) for lev in C.LEVELS}
live = {lev: pd.read_parquet(f'out_v2/{a.live}/assign_{lev}.parquet')['school'].values.astype(object) for lev in C.LEVELS}
n = 0
for p in pk:
    near = np.hypot((x - p['at'][0]) * 48.6, (y - p['at'][1]) * 69) < a.radius
    for i in np.where(near & (cand['K-5'] != live['K-5']))[0]:
        n += 1
        for lev in ('K-5', '6-8'):
            cand[lev][i] = live[lev][i]
cfg = C.load_config(f'configs/v2/{a.cand}.json')
old = json.load(open(f'{st}/scorecard.json'))
keep = {k: v for k, v in old.items() if k not in ('levels', 'durability', 'programs', 'name', 'label', 'basis')}
keep['pocket_fix'] = f'restored {n} K-5 blocks within {a.radius} mi of {len(pk)} new pocket(s) to the live {a.live} lines'
MX.write_plan(st, cfg, cand, MX.load_refs('configs/v2'), extra=keep)
print(a.cand, 'pockets', [(p['school'], p['blocks']) for p in pk], '-> restored', n, 'blocks; pockets now',
      [(p['school'], p['blocks']) for p in Q.qa(a.cand, True)['K-5']['pockets']])
