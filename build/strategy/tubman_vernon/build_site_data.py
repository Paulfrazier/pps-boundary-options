"""Data for the "Tubman in the Vernon building" sub-page of the Sabin options site. Run from build/solver:
    PYTHONPATH=. ../../.venv/bin/python ../strategy/tubman_vernon/build_site_data.py
Writes build/strategy/tubman_vernon/site_data/:
  blocks_ms_walk.csv  one row per Census block in today's Tubman, Vernon (K-8), Beaumont and Ockley Green middle-school
                      zones: middle-school kids (2031-32 PSU-forecast, model v2), walk miles to the Tubman building
                      (N Flint), the Vernon building, Beaumont and Ockley Green, today's middle school
  summary.json        headline numbers: today's Tubman zone (incl. Vernon's 6-8) walking to N Flint vs the Vernon building,
                      Vernon's K-5 size under each plan, buildings (LRFP 2021) with sources
Model figures are estimates (block kids scaled to PSU's per-school forecast; OSRM foot-network walks).
"""
import os, json
import numpy as np, pandas as pd
import common as C, metrics as MX

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'site_data')
os.makedirs(OUT, exist_ok=True)
b = C.blocks()
cfg = C.load_config(os.path.join(C.SOLVER, 'configs', 'v2', 'status_quo.json'))
K = MX.level_kids(cfg)['6-8']
asg = lambda run, lev: pd.read_parquet(os.path.join(C.SOLVER, 'out_v2', run, f'assign_{lev}.parquet')).sort_values('idx')['school'].values
ms0 = asg('status_quo', '6-8')
ZONES = ['Tubman', 'Vernon', 'Beaumont', 'Ockley Green']
SITES = ['Tubman', 'Vernon', 'Beaumont', 'Ockley Green']
W = C.dist('walk', SITES)
keep = np.isin(ms0, ZONES)
# PPS A's middle schools; B and Plan D draw Tubman's zone block for block the same (checked). Under all three,
# Irvington merges into Beverly Cleary and its middle schoolers leave Tubman for Beaumont, and Vernon's 6-8 joins Tubman
ms_abd = asg('scenario_A', '6-8')
for r in ('scenario_B', 'planD_updated'):
    assert ((asg(r, '6-8') == 'Tubman') == (ms_abd == 'Tubman')).all(), f'{r} Tubman zone differs from PPS A'
df = pd.DataFrame({'idx': np.arange(len(b))[keep], 'GEOID': b['GEOID'].values[keep], 'ms_today': ms0[keep],
                   'ms_abd': ms_abd[keep], 'es_today': b['sq_es'].values[keep], 'kids_6_8': K[keep].round(2)})
for j, s in enumerate(SITES):
    df[f'walk_{s.replace(" ", "_").lower()}'] = W[keep, j].round(3)
df.to_csv(os.path.join(OUT, 'blocks_ms_walk.csv'), index=False)

# Tubman's zone under PPS A, B and Plan D (today's zone minus Irvington, plus Vernon's own 6-8): N Flint vs the Vernon building
z = keep & (ms_abd == 'Tubman')
k = K[z]; wt, wv = W[z, 0], W[z, 1]
def stats(w):
    return {'avg_walk_mi': round(float((k * w).sum() / k.sum()), 2), 'kids_over_1_5mi': round(float(k[w > 1.5].sum())),
            'kids_within_1_5mi': round(float(k[w <= 1.5].sum()))}
vz = ms0[z] == 'Vernon'
es = b['sq_es'].values
# where today's Tubman and Vernon middle schoolers go under A/B/D, by today's elementary area
split = {}
for zt in ('Tubman', 'Vernon'):
    m = keep & (ms0 == zt)
    g = pd.DataFrame({'es': es[m], 'to': ms_abd[m], 'k': K[m]}).groupby(['es', 'to']).k.sum().round()
    split[zt] = {f'{e} -> {t}': int(v) for (e, t), v in g.items() if v > 0}
by_area = {}
for e in sorted(set(es[z])):
    m = z & (es == e)
    if K[m].sum() < 1:
        continue
    by_area[e] = {'kids': round(float(K[m].sum())), 'walk_flint_mi': round(float((K[m] * W[m, 0]).sum() / K[m].sum()), 2),
                  'walk_vernon_mi': round(float((K[m] * W[m, 1]).sum() / K[m].sum()), 2)}
summary = {
    'basis': '2031-32 PSU-forecast middle-school kids on 2020 Census blocks (model v2); OSRM walking miles. Estimates.',
    'zone': ("Tubman's middle-school zone under PPS A, B and Plan D (identical in all three): today's Tubman zone without "
             "Irvington (whose elementary merges into Beverly Cleary and whose middle schoolers go to Beaumont), plus "
             "Vernon's own 6-8 (Vernon becomes a K-5)"),
    'kids': round(float(k.sum())),
    'tubman_on_flint': stats(wt), 'tubman_at_vernon': stats(wv),
    'vernon_6_8_kids': round(float(k[vz].sum())),
    'vernon_6_8_walk_to_flint_mi': round(float((k[vz] * wt[vz]).sum() / k[vz].sum()), 2),
    'vernon_6_8_walk_to_vernon_mi': round(float((k[vz] * wv[vz]).sum() / k[vz].sum()), 2),
    'abd_zone_by_today_es_area': by_area,
    'today_to_abd_6_8': split,
}
sizes = {}
for run, lab in [('status_quo', 'Today (K-8)'), ('scenario_A', 'PPS A'), ('scenario_B', 'PPS B'), ('planD_updated', 'Plan D'),
                 ('irv_sabin_15th_grant', 'Irvington into Sabin')]:
    sc = pd.read_csv(os.path.join(C.SOLVER, 'out_v2', run, 'schools.csv')).drop_duplicates('school').set_index('school')
    sizes[lab] = {'vernon_total': round(float(sc.total['Vernon'])), 'floor': int(sc.floor['Vernon'])}
summary['vernon_size_2031'] = sizes
summary['buildings_lrfp_2021'] = {
    'source': 'PPS Long Range Facility Plan 2021 Vol 2 (build/pps-texts/lrfp-2021-vol2-ne-middle-sites.md)',
    'Vernon': {'site_acres': 3.74, 'building_sf': 70833, 'levels': 3, 'built': 1931, 'classrooms': 25, 'functional_capacity': 579, 'modulars': 4},
    'Tubman': {'site_acres': 3.05, 'building_sf': 87610, 'levels': 2, 'built': 1952, 'classrooms': 33, 'functional_capacity': 732, 'modulars': 0},
    'pps_program_sf_new_tubman': {'value': 120000, 'source': 'Tubman (re)siting due diligence v06 (build/pps-texts/tubman-siting-2022-23/htms-siting-due-diligence-v06.md)'}}
json.dump(summary, open(os.path.join(OUT, 'summary.json'), 'w'), indent=1)
print(json.dumps(summary, indent=1)[:1500])
print(len(df), 'blocks')
