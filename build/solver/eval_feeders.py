"""Feeder + line comparison across runs (2026-10-15 night work on split feeders).

  python eval_feeders.py run [run ...]        (a run name, or name.staging)

Per run, our model, 2031-32 kids unless noted:
  at target every required year (K-5, 6-8 at the run's own floor; 6-8 also at 500),
  K-5 / 6-8 kids past a closer school and average walk, kids reassigned vs PPS Status Quo,
  ES->MS splits (scorecard rule), ES->HS splits (elementary areas whose kids go to 2+ high schools,
  >=5 kids and >=5% on a second one), MS->HS splits (scorecard), middle sizes (low/high, 2027-28..2031-32),
  line teeth / fingers (lines_qa)."""
import json, os, sys
import pandas as pd
import common as C, metrics as MX
import lines_qa as Q

OUT = os.path.join(C.SOLVER, 'out_v2')


def folder(r):
    return r if os.path.exists(os.path.join(OUT, r, 'scorecard.json')) else r + '.staging'


def splits(a, b, w):
    df = pd.DataFrame({'a': a, 'b': b, 'w': w})
    df = df[df.w > 0]
    g = df.groupby(['a', 'b']).w.sum()
    n = 0
    for _, gg in g.groupby(level=0):
        t = gg.sum()
        n += sum(1 for v in gg.values if v >= 5 and v / t >= 0.05) > 1
    return n


def row(r):
    f = folder(r)
    name = f.replace('.staging', '')
    sc = json.load(open(os.path.join(OUT, f, 'scorecard.json')))
    cp = os.path.join(C.SOLVER, 'configs', 'v2', f'{name}.json')
    cfg = C.load_config(cp if os.path.exists(cp) else os.path.join(C.SOLVER, 'configs', 'v2', 'option2.json'))
    C.resolve_config(cfg, sc)
    K = MX.level_kids(cfg, '2031')
    asg = {l: pd.read_parquet(os.path.join(OUT, f, f'assign_{l}.parquet'))['school'].values for l in C.LEVELS}
    L, D = sc['levels'], sc['durability']['levels']
    req = sc['durability']['required_years']
    S6 = {n: v for n, v in D['6-8']['schools'].items() if not v['program_only']}
    sz = [x for v in S6.values() for y, x in v['sizes_by_year'].items() if y in req]
    at500 = sum(all(ok and v['sizes_by_year'][y] >= 500 for y, ok in zip(sc['durability']['years'], v['in_range_by_year'])
                    if y in req) for v in S6.values())
    lq = {}
    for lev in ('K-5', '6-8'):
        try:
            q = Q.line_stats(asg[lev], lev) if hasattr(Q, 'line_stats') else None
        except Exception:
            q = None
        lq[lev] = q
    return {
        'run': r, 'floor68': cfg['floors']['6-8'],
        'K5_at': D['K-5']['at_target_all_required_years'], '68_at': D['6-8']['at_target_all_required_years'], '68_at500': at500,
        'K5_past': L['K-5']['kids_past_closer_school'], 'K5_walk': L['K-5']['avg_walk_mi'],
        '68_past': L['6-8']['kids_past_closer_school'], '68_walk': L['6-8']['avg_walk_mi'],
        'moved': L['K-5']['kids_reassigned_vs_status_quo'] + L['6-8']['kids_reassigned_vs_status_quo'],
        'ES_MS': L['6-8'].get('n_split_feeders_es_to_ms'),
        'ES_HS': splits(asg['K-5'], asg['9-12'], K['9-12']),
        'MS_HS': L['9-12'].get('n_split_feeders_ms_to_hs'), 'MS_one_HS_pct': L['9-12'].get('pct_ms_feeders_to_one_hs'),
        'ms_low': round(min(sz)), 'ms_high': round(max(sz)), 'K5_minus9': L['K-5']['schools_in_range_at_minus9pct'],
    }


if __name__ == '__main__':
    rows = [row(r) for r in sys.argv[1:]]
    cols = list(rows[0])
    print('| ' + ' | '.join(cols) + ' |')
    print('|' + '---|' * len(cols))
    for r in rows:
        print('| ' + ' | '.join(str(r[c]) for c in cols) + ' |')
