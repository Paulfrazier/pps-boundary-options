"""Trade-offs matrix across plans (Paul 2026-10-14: "a trade offs table looking at each model ... green, yellow, red").

  python tradeoffs_matrix.py            -> out_v2/TRADEOFFS_MATRIX.json and .md

One row per plan, 2031-32 unless noted (our model v2 on PSU July 2026 Table 5.5; scorecards in out_v2/<plan>/).
Ratings: rule rows (at target every required year) are absolute (green all, yellow >= 80%, red less).  Comparison
rows place each plan that closes schools (everything but PPS Status Quo, shown uncolored) on the range from the best
to the worst of those plans: best third of the range green, middle third yellow, worst third red.  PPS A is rated like every other plan."""
import json, os
import numpy as np, pandas as pd
import common as C, metrics as MX

OUT = os.path.join(C.SOLVER, 'out_v2')
PLANS = [  # (run, folder, display name, status)
    ('status_quo', 'status_quo', 'PPS Status Quo', 'reference'),
    ('scenario_A', 'scenario_A', 'PPS A', 'reference'),
    ('scenario_B', 'scenario_B', 'PPS B', 'reference'),
    ('option2', 'option2', 'Boundary changes, same closures', 'pick'),
    ('option2_ms460', 'option2_ms460', 'Balanced middle schools', 'pick'),
    ('option2_ms460_sellwood_home', 'option2_ms460_sellwood_home', 'Balanced middle schools, Sellwood open', 'pick'),  # Paul 2026-10-20: promote
    ('option1_durable', 'option1_durable', 'Redrawn K-8 lines', 'pick'),
    ('frontier_k17', 'frontier_k17', 'Shortest walks', 'dropped'),
    ('option4', 'option4', 'Rebalanced PPS A', 'pick'),
    ('option3a', 'option3a', 'Close 2 focus options', 'what-if'),
    ('ppsrules_walk', 'ppsrules_walk.staging', 'PPS rules, walkable lines', 'test'),
    ('option2_sellwood_flex_long', 'option2_sellwood_flex_long.staging', 'Lead plan + Sellwood open', 'test'),
    ('capstone_s2', 'capstone_s2.staging', 'Solver picks schools', 'test'),
    ('option2_ms420', 'option2_ms420.staging', 'Same closures, middle 420-450', 'test'),
]
# local-only preview plans (build/export/preview_plans.json never ships): inserted after their 'after' plan
_PREV = os.path.join(C.SOLVER, '..', 'export', 'preview_plans.json')
if os.path.exists(_PREV):
    for _p in json.load(open(_PREV)).get('plans', []):
        _k = next((n for n, t in enumerate(PLANS) if t[0] == _p.get('after')), len(PLANS) - 1)
        PLANS.insert(_k + 1, (_p['name'], _p['sub'], _p['short'], 'preview'))



def friends(cfg, asg):
    """share of kids whose school's largest next-level destination is theirs (ES->MS by K-5 kids, MS->HS by 6-8 kids),
    and the number of schools that split (>=5% and >=5 kids to a second school)"""
    K = MX.level_kids(cfg, '2031')
    out = {}
    for a, b, w in (('K-5', '6-8', 'K-5'), ('6-8', '9-12', '6-8')):
        df = pd.DataFrame({'a': asg[a], 'b': asg[b], 'w': K[w]})
        df = df[df.w > 0]
        g = df.groupby(['a', 'b']).w.sum()
        top = g.groupby(level=0).max().sum()
        out[f'{a}->{b}_together_pct'] = round(100 * top / g.sum(), 1)
        n = 0
        for s, sub in g.groupby(level=0):
            sub = sub.sort_values(ascending=False)
            if len(sub) > 1 and sub.iloc[1] >= 5 and sub.iloc[1] / sub.sum() >= 0.05:
                n += 1
        out[f'{a}->{b}_splits'] = n
    return out


def row(run, folder):
    p = os.path.join(C.SOLVER, 'configs', 'v2', f'{run}.json')
    cfg = C.load_config(p)
    sc = json.load(open(os.path.join(OUT, folder, 'scorecard.json')))
    C.resolve_config(cfg, sc)
    asg = {l: pd.read_parquet(os.path.join(OUT, folder, f'assign_{l}.parquet'))['school'].values
           for l in ('K-5', '6-8', '9-12')}
    L, D = sc['levels'], sc['durability']['levels']
    r = {}
    for lev in ('K-5', '6-8'):
        r[f'{lev}_at_target_all_req'] = D[lev]['at_target_all_required_years']
        r[f'{lev}_zoned'] = D[lev]['n_zoned_non_exempt']
        r[f'{lev}_in_range_minus9'] = L[lev]['schools_in_range_at_minus9pct']
        r[f'{lev}_avg_walk'] = L[lev]['avg_walk_mi']
        r[f'{lev}_within_1mi_pct'] = L[lev]['pct_within_1.0mi']
        r[f'{lev}_past_closer'] = L[lev]['kids_past_closer_school']
        r[f'{lev}_over_bus'] = L[lev]['kids_over_bus_threshold']             # (2026-10-19, Paul) metrics.BUS
        r[f'{lev}_reassigned'] = L[lev]['kids_reassigned_vs_status_quo']      # vs PPS Status Quo (2027-28)
        r[f'{lev}_open'] = L[lev]['schools_open']
        r[f'{lev}_dissimilarity'] = L[lev]['dissimilarity_index']
    r['dli_moved'] = (sc.get('programs') or {}).get('dli_kids_moved_total')
    r['hs_reassigned'] = L['9-12']['kids_reassigned_vs_status_quo']
    r.update(friends(cfg, asg))
    # PPS's own plans: at-target counts from PPS's own Family Guide figures (Paul 2026-10-14: "use the official PPS
    # data to represent their models"); durability_vs_pps.py writes the file
    off = os.path.join(OUT, 'PPS_OFFICIAL_DURABILITY.json')
    if run in ('status_quo', 'scenario_A', 'scenario_B') and os.path.exists(off):
        OL = json.load(open(off))['plans'][run]['durability']['levels']
        for lev in ('K-5', '6-8'):
            r[f'{lev}_at_target_all_req'] = OL[lev]['at_target_all_required_years']
            r[f'{lev}_zoned'] = OL[lev]['n_zoned_non_exempt']
        r['at_target_source'] = 'PPS Family Guide figures'
    # a plan with a lower middle-school minimum (option2_ms460: 460) is counted at the common 500 minimum here, so
    # every plan in the table is held to the same rule; its own-minimum count is kept as 6-8_at_target_own_floor
    if cfg['floors'].get('6-8', 500) != 500:
        req = sc['durability']['required_years']
        S6 = D['6-8']['schools']
        r['6-8_at_target_own_floor'] = r['6-8_at_target_all_req']
        r['6-8_own_floor'] = cfg['floors']['6-8']
        r['6-8_at_target_all_req'] = sum(
            all(ok and v['sizes_by_year'][y] >= 500 for y, ok in zip(sc['durability']['years'], v['in_range_by_year'])
                if y in req) for v in S6.values() if not v['program_only'])
    # split counts: the scorecard's own (its feeder rule), so they match BRIEFS
    if L['6-8'].get('n_split_feeders_es_to_ms') is not None:
        r['K-5->6-8_splits'] = L['6-8']['n_split_feeders_es_to_ms']
    if L['9-12'].get('n_split_feeders_ms_to_hs') is not None:
        r['6-8->9-12_splits'] = L['9-12']['n_split_feeders_ms_to_hs']
    return r


# (key, label, better: 'high' | 'low' | 'rule', unit)
MEASURES = [
    ('K-5_at_target', 'K-5 schools at target every year 2027-32', 'rule'),
    ('6-8_at_target', '6-8 schools at target every year 2027-32', 'rule'),
    ('K-5_in_range_minus9', 'K-5 schools in range if enrollment is 9% lower', 'high'),
    ('moved', 'Students reassigned vs PPS Status Quo (K-5 + 6-8)', 'low'),
    ('dli_moved', 'Immersion students whose program moves', 'low'),
    ('K-5_past_closer', 'K-5 kids assigned to a farther school, past a closer one', 'low'),
    ('6-8_past_closer', '6-8 kids assigned to a farther school, past a closer one', 'low'),
    ('K-5_avg_walk', 'K-5 average walk (mi)', 'low'),
    ('6-8_avg_walk', '6-8 average walk (mi)', 'low'),
    ('K-5_over_bus', 'K-5 kids living past the 1-mile bus line', 'low'),
    ('6-8_over_bus', '6-8 kids living past the 1.5-mile bus line', 'low'),
    ('K-5->6-8_together_pct', 'Elementary class kept together into middle school (%)', 'high'),
    ('K-5->6-8_splits', 'Elementary schools split between middle schools', 'low'),
    ('6-8->9-12_together_pct', 'Middle-school class kept together into high school (%)', 'high'),
    ('6-8->9-12_splits', 'Middle schools split between high schools', 'low'),
    ('K-5_open', 'Elementary schools open', 'info'),
]


def value(r, k):
    if k == 'K-5_at_target':
        return r['K-5_at_target_all_req'], f"{r['K-5_at_target_all_req']}/{r['K-5_zoned']}"
    if k == '6-8_at_target':
        return r['6-8_at_target_all_req'], f"{r['6-8_at_target_all_req']}/{r['6-8_zoned']}"
    if k == 'K-5_in_range_minus9':
        return r[k], f"{r[k]}/{r['K-5_open']}"
    if k == 'moved':
        v = r['K-5_reassigned'] + r['6-8_reassigned']
        return v, f'{v:,.0f}'
    v = r[k]
    if v is None:
        return None, 'n/a'
    return v, (f'{v:.2f}' if 'walk' in k else f'{v:.1f}' if 'pct' in k else f'{v:,.0f}')


def rate(k, kind, v, ref, r):
    if kind == 'info' or v is None or ref is None:
        return ''
    if kind == 'rule':
        n = r[k.replace('at_target', 'zoned')]
        return 'green' if v >= n else 'yellow' if v >= 0.8 * n else 'red'
    return ''          # comparison rows are rated in __main__ (thirds of the range across the closure plans)


if __name__ == '__main__':
    rows = {}
    for run, folder, name, status in PLANS:
        if os.path.exists(os.path.join(OUT, folder, 'scorecard.json')):
            rows[run] = row(run, folder)
    ref = rows['scenario_A']
    table = []
    for run, folder, name, status in PLANS:
        if run not in rows:
            continue
        cells = {}
        for k, label, kind in MEASURES:
            v, txt = value(rows[run], k)
            rv, _ = value(ref, k)
            cells[k] = {'value': v, 'text': txt, 'rating': rate(k, kind, v, rv, rows[run]) if kind == 'rule' else ''}
        table.append({'run': run, 'name': name, 'status': status, 'cells': cells, 'raw': rows[run]})
    for k, label, kind in MEASURES:          # rank tertiles among the closure plans
        if kind not in ('high', 'low'):
            continue
        pool = [t for t in table if t['run'] != 'status_quo' and t['cells'][k]['value'] is not None]
        vs = [t['cells'][k]['value'] for t in pool]
        lo, hi = min(vs), max(vs)
        for t in pool:
            f = (t['cells'][k]['value'] - lo) / (hi - lo) if hi > lo else 0.0
            f = 1 - f if kind == 'high' else f          # 0 = best, 1 = worst
            t['cells'][k]['rating'] = 'green' if f <= 1 / 3 else 'yellow' if f <= 2 / 3 else 'red'
    json.dump({'basis': __doc__, 'measures': MEASURES, 'plans': table},
              open(os.path.join(OUT, 'TRADEOFFS_MATRIX.json'), 'w'), indent=1, default=float)
    dot = {'green': '🟢', 'yellow': '🟡', 'red': '🔴', '': ''}
    # preview plans (local-only) stay out of the .md unless the site builds a preview
    table = [t for t in table if t['status'] != 'preview' or os.environ.get('PPS_SITE_PREVIEW') == '1']
    md = ['| Measure | ' + ' | '.join(t['name'] for t in table) + ' |', '|---' * (len(table) + 1) + '|']
    for k, label, kind in MEASURES:
        md.append(f'| {label} | ' + ' | '.join(f"{dot[t['cells'][k]['rating']]} {t['cells'][k]['text']}".strip()
                                               for t in table) + ' |')
    md += ['', 'At-target rows for PPS Status Quo, PPS A and PPS B use PPS\'s own Family Guide enrollment figures (p. 4, '
           'guides dated 2026-10-08); every other number is our model (v2) on PSU July 2026 Table 5.5. '
           '"Balanced middle schools" and "Balanced middle schools, Sellwood open" use a 460 middle-school minimum; '
           'their middle-school at-target counts here use the 500 minimum like every other plan (13/13 at their own 460 '
           'minimum). Sellwood is exempt from the minimum in "Balanced middle schools, Sellwood open", so its count is '
           'out of 13.']
    open(os.path.join(OUT, 'TRADEOFFS_MATRIX.md'), 'w').write('\n'.join(md) + '\n')
    print('\n'.join(md))
