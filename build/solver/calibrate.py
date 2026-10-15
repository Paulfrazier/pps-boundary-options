"""Calibration gate: our building totals vs PPS Family Guide projections ("How many students are expected?", p. 4),
per school, 2027-28 and 2031-32.  PPS "No changes" <-> our Status Quo; "Options A and B"/"Option A"/"Option B" <-> A/B.

  python calibrate.py            -> out_v2/calibration_table.csv (+ prints summary)
v1 has only a 2031-32 basis, so v1 is compared for 2031-32 only.
"""
import json
import os

import numpy as np
import pandas as pd

import common as C
import metrics as MX

PPS = json.load(open(os.path.join(C.DATA, 'scenarios.json')))['pps_projections_2027_28_to_2031_32']
ALIAS = {'Lee': 'Sunrise', 'Lane': 'Brentwood', 'MLK Jr': 'Dr  Martin Luther King Jr ', 'Tubman': 'Harriet Tubman',
         'Bridger': 'Bridger Creative Science', 'Mt Tabor': 'Mt  Tabor', 'Ida B. Wells': 'Ida B Wells',
         'Boise-Eliot/Humboldt': 'Boise-Eliot Humboldt', 'MLC': 'Metropolitan Learning Center'}
PLANS = [('status_quo', 'no_change'), ('scenario_A', 'A'), ('scenario_B', 'B')]


def pps(n, key, k):
    p = PPS.get(ALIAS.get(n, n)) or PPS.get(n)
    if p is None or not isinstance(p.get(key), list):
        return np.nan
    return float(p[key][k])


def table():
    rows = []
    for plan, key in PLANS:
        c1 = C.load_config(os.path.join(C.SOLVER, 'configs', f'{plan}.json'))
        c2 = C.load_config(os.path.join(C.SOLVER, 'configs', 'v2', f'{plan}.json'))
        bt1 = MX.building_table(c1, MX.plan_from_columns(c1)).set_index('school')
        p2 = MX.plan_from_columns(c2)
        bt2_31 = MX.building_table(c2, p2, year='2031').set_index('school')
        bt2_27 = MX.building_table(c2, p2, year='2027').set_index('school')
        focus = set(c2.get('focus', []))
        for n in sorted(set(bt2_31.index) | set(bt1.index)):
            r = bt2_31.loc[n] if n in bt2_31.index else None
            rows.append({
                'plan': plan, 'school': n,
                'type': r['type'] if r is not None else bt1.loc[n, 'type'],
                'focus_or_alt': n in focus,
                'program_only': bool(r['program_only']) if r is not None else None,
                'ours_v1_2031': round(float(bt1.loc[n, 'total']), 0) if n in bt1.index else np.nan,
                'ours_v2_2031': round(float(r['total']), 0) if r is not None else np.nan,
                'pps_2031': pps(n, key, 4),
                'ours_v2_2027': round(float(bt2_27.loc[n, 'total']), 0) if n in bt2_27.index else np.nan,
                'pps_2027': pps(n, key, 0),
            })
    df = pd.DataFrame(rows)
    for a, b_ in (('v1_2031', '2031'), ('v2_2031', '2031'), ('v2_2027', '2027')):
        df[f'pct_{a}'] = (100 * (df[f'ours_{a}'] / df[f'pps_{b_}'] - 1)).round(1)
    return df


def summary(df, col):
    d = df.dropna(subset=[col])
    d = d[~d['focus_or_alt']]
    a = d[col].abs()
    return {'n': int(len(d)), 'within_10pct': int((a <= 10).sum()), 'within_5pct': int((a <= 5).sum()),
            'median_abs_pct': round(float(a.median()), 1), 'mean_abs_pct': round(float(a.mean()), 1),
            'over_10': d.loc[a > 10, ['school', col]].sort_values(col).values.tolist()}


if __name__ == '__main__':
    df = table()
    os.makedirs(os.path.join(C.SOLVER, 'out_v2'), exist_ok=True)
    df.to_csv(os.path.join(C.SOLVER, 'out_v2', 'calibration_table.csv'), index=False)
    for plan, _ in PLANS:
        d = df[df.plan == plan]
        for col in ('pct_v1_2031', 'pct_v2_2031', 'pct_v2_2027'):
            print(plan, col, summary(d, col))
