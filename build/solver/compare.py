"""Side-by-side scorecards and a check of our Scenario-A sizes against PPS's own projections.

  python compare.py option1 [more plans...]   -> out/compare.md
"""
import json
import os
import sys

import pandas as pd

import common as C

KEYS = ['avg_walk_mi', 'avg_bike_mi', 'pct_within_0.5mi', 'pct_within_1.0mi', 'pct_within_1.5mi',
        'pct_within_2.0mi', 'kids_over_bus_threshold', 'kids_past_closer_school', 'schools_open',
        'schools_in_range', 'schools_in_range_non_exempt', 'schools_evaluated_non_exempt', 'min_size',
        'max_size', 'avg_utilization', 'schools_in_range_2025_26_basis', 'schools_in_range_at_minus9pct',
        'kids_reassigned_vs_status_quo', 'kids_reassigned_vs_today', 'poc_share_of_movers_vs_status_quo',
        'dissimilarity_index', 'n_split_feeders_es_to_ms', 'n_split_feeders_ms_to_hs',
        'pct_ms_feeders_to_one_hs', 'hs_range']


def md(df):
    cols = list(df.columns)
    fmt = lambda v: '' if v is None or (isinstance(v, float) and v != v) else (f'{v:g}' if isinstance(v, float) else str(v))
    lines = ['| ' + ' | '.join(map(str, cols)) + ' |', '|' + '---|' * len(cols)]
    for r in df.itertuples(index=False):
        lines.append('| ' + ' | '.join(fmt(v) for v in r) + ' |')
    return '\n'.join(lines)


def load(name):
    for sub in (os.path.join('out', name), os.path.join('out', 'baselines', name)):
        p = os.path.join(C.SOLVER, sub, 'scorecard.json')
        if os.path.exists(p):
            return json.load(open(p))
    raise FileNotFoundError(name)


def table(names):
    scs = {n: load(n) for n in names}
    out = []
    for lev in C.LEVELS:
        rows = []
        for k in KEYS:
            vals = [scs[n]['levels'][lev].get(k) for n in names]
            if all(v is None for v in vals):
                continue
            rows.append([k] + vals)
        df = pd.DataFrame(rows, columns=['metric'] + names)
        out.append(f'### {lev}\n\n' + md(df))
    prog = pd.DataFrame([[n, scs[n]['programs']['dli_kids_moved_total'],
                          scs[n]['programs']['because_building_closes'],
                          scs[n]['programs']['because_program_moves']] for n in names],
                        columns=['plan', 'DLI kids moved', 'building closes', 'program moves'])
    out.append('### DLI / program moves vs today (2031-32 counts)\n\n' + md(prog))
    return '\n\n'.join(out)


def durability_table(names):
    scs = {n: load(n) for n in names}
    out = []
    for lev in C.LEVELS:
        rows = []
        for n in names:
            d = scs[n].get('durability', {}).get('levels', {}).get(lev)
            if not d:
                continue
            rows.append([n, d['n_zoned_non_exempt']] + [d['at_target_zoned'][y] for y in C.YEARS]
                        + [d['durable_through_2040_41']])
        df = pd.DataFrame(rows, columns=['plan', 'zoned'] + C.YEARS + ['all 10 yrs'])
        out.append(f'### {lev}: zoned non-exempt schools at target each year (PSU medium)\n\n' + md(df))
    return '\n\n'.join(out)


def validate_A():
    """Our Scenario-A building totals vs PPS family-guide 2031-32 'A' projections."""
    sch = C.schools_table()
    ours = pd.read_csv(os.path.join(C.SOLVER, 'out', 'baselines', 'scenario_A', 'schools.csv')).set_index('school')
    rows = []
    for n, r in ours.iterrows():
        if n not in sch.index:
            continue
        v = sch.loc[n, 'pps_proj_2031_32_A']
        try:
            v = float(v)
        except (TypeError, ValueError):
            continue
        rows.append({'school': n, 'type': r['type'], 'ours_2031': round(r['total']), 'pps_A_2031': round(v),
                     'diff_pct': round(100 * (r['total'] - v) / v, 1)})
    df = pd.DataFrame(rows).sort_values('diff_pct')
    mape = df['diff_pct'].abs().mean()
    return df, mape


if __name__ == '__main__':
    names = ['today', 'status_quo', 'scenario_A', 'scenario_B'] + sys.argv[1:]
    doc = ['# Scorecards side by side', '', 'Neighborhood kids, 2031-32 basis. See METHOD.md for definitions.', '',
          table(names), '', '## Durability 2031-32 to 2040-41', '', durability_table(names)]
    df, mape = validate_A()
    doc += ['', '## Check: our Scenario A building sizes vs PPS family-guide 2031-32 A projections', '',
           f'Mean absolute difference {mape:.1f}% over {len(df)} buildings.', '', md(df)]
    with open(os.path.join(C.SOLVER, 'out', 'compare.md'), 'w') as f:
        f.write('\n'.join(doc))
    print('\n'.join(doc))
