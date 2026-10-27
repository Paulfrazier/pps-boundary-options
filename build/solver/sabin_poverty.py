"""Sabin- and Irvington-area families under each plan, students experiencing poverty vs all other students (the data
behind the Sabin options page).

Area = today's K-5 attendance area (blocks.sq_es). Poverty = poverty_compare.py's block estimate (Census C17002 <185% of
poverty, block_poverty185.npy), so counts are estimates. 2031-32 kids. Walk = network walk to the assigned building.
"At target every year" = the assigned school is in range every year 2027-28..2031-32 in that plan's scorecard; "PPS
sustainable" = at or above 360 / 500 / 1,100 in 2031-32 (PPS's dashboard definition). Plans missing a folder are skipped.
Writes out_v2/SABIN_POVERTY.md and out_v2/SABIN_OPTIONS.json (data for the site's Sabin options page; render only plans whose
status is "done").   Run from build/solver:
    PYTHONPATH=. ../../.venv/bin/python sabin_poverty.py
"""
import os, io, json, contextlib
import numpy as np, pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
__file__ = os.path.join(HERE, 'poverty_compare.py')
_src = open('poverty_compare.py').read().split("# ---- PPS's own figures")[0]
with contextlib.redirect_stdout(io.StringIO()):
    exec(_src)

SPLANS = [('status_quo', 'Today (Status Quo)'), ('scenario_A', 'PPS Scenario A'), ('planD', 'Scenario D as written'),
          ('planD_redraw_ms', 'Scenario D re-drawn'), ('planD_sust', 'Scenario D buildings, every school at target'),
          ('equity_noswap_alameda_rig_hs', 'Current best: fewer DLI moves, sustainable schools'), ('sabin_all', 'Sabin into Irvington, all ideas'),
          ('sabin_all_keepbc', 'Sabin into Irvington, Beverly Cleary keeps its area'),
          ('irv_sabin', 'Irvington into Sabin'), ('irv_sabin_keep', 'Irvington into Sabin, all of Sabin stays, Vernon as today'), ('irv_sabin_whole', 'Irvington into Sabin, all of Sabin stays, then Tubman and Jefferson'), ('irv_sabin_noala', 'Sabin Stays - less moves'), ('irv_sabin_thompson21', 'Irvington line: Thompson / 21st / Knott'), ('irv_sabin_knott', 'Irvington line: NE Knott'), ('irv_sabin_15th', 'Irvington line: NE 15th + Knott'), ('irv_sabin_15th_grant', 'Irvington line: NE 15th + Knott, Irvington teens stay at Grant'), ('sabin_irv', 'Sabin into Irvington (small)'),
          ('sabin_irv_wide', 'Sabin into Irvington, wider receivers'), ('sabin_irv_both', 'Sabin and Irvington both open')]
AREAS = ['Sabin', 'Irvington']
NEIGH = ['Sabin', 'Irvington', 'MLK Jr', 'Alameda', 'Vernon', 'Beverly Cleary', 'Boise-Eliot/Humboldt', 'Rigler', 'Woodlawn']
BUS = {'K-5': 1.0, '6-8': 1.5}
FLOOR = {'K-5': 360, 'K-8': 500, '6-8': 500, '9-12': 1100}
b = C.blocks()
RUNS = json.load(open('out_v2/MANIFEST.json')).get('runs', {})


def plan_dir(n):
    return 'out_v2/status_quo' if n == 'status_quo' else folder(n)


def status(n):
    if n == 'status_quo':
        return 'done'
    v = RUNS.get(n) if isinstance(RUNS, dict) else next((x for x in RUNS if x.get('name') == n), None)
    return v.get('status') if isinstance(v, dict) else None


def plan_rows(d, m):
    """Per-level, per-group measures for the blocks in mask m, plus destinations and neighbor school sizes."""
    # a run that exempted schools from the floor (Plan D re-drawn) is judged on PPS's 360 bar for every school, as on the rest
    # of the site: use its re-score (scorecard_scored360.json, same lines) where there is one
    sc = json.load(open(f'{d}/scorecard_scored360.json' if os.path.exists(f'{d}/scorecard_scored360.json') else f'{d}/scorecard.json'))
    sch = pd.read_csv(f'{d}/schools.csv'); sch = sch[sch['total'] > 0]
    sust = sch['total'] >= sch['type'].map(FLOOR).fillna(360) - 0.5
    pps_good = set(sch.loc[sust, 'school'])
    r = {'d_n': len(sch), 'd_sust': 100 * sust.mean(), 'd_in_sust': 100 * sch.loc[sust, 'total'].sum() / sch['total'].sum()}
    dests = {}
    rr = np.where(m)[0]
    for lv in ('K-5', '6-8', '9-12'):
        k = KSQ[lv][m]; p = P[lv][m]; a = asg(d, lv)[m]; s = asg(SQ, lv)[m]
        names = sorted(set(a) | set(s)); W = C.dist('walk', names); ix = {q: j for j, q in enumerate(names)}
        da = W[rr, [ix[q] for q in a]]; ds = W[rr, [ix[q] for q in s]]
        ok = np.isfinite(da) & np.isfinite(ds)
        good = {q for q, v in sc['durability']['levels'][lv]['schools'].items() if v.get('in_range_all_required_years')}
        for g, wgt in (('pov', k * p), ('oth', k * (1 - p))):
            tot = wgt.sum()
            r[f'{lv}_{g}_n'] = tot
            r[f'{lv}_{g}_mv'] = 100 * wgt[a != s].sum() / tot
            r[f'{lv}_{g}_walk'] = np.average(np.where(ok, da, 0), weights=wgt)
            r[f'{lv}_{g}_dwalk'] = np.average(np.where(ok, da - ds, 0), weights=wgt)
            if lv in BUS:
                r[f'{lv}_{g}_in1'] = 100 * wgt[ok & (da <= 1.0)].sum() / tot
                r[f'{lv}_{g}_bus'] = 100 * wgt[ok & (da > BUS[lv])].sum() / tot
            r[f'{lv}_{g}_sust'] = 100 * wgt[np.isin(a, list(good))].sum() / tot
            r[f'{lv}_{g}_pps'] = 100 * wgt[np.isin(a, list(pps_good))].sum() / tot
        dk = pd.Series(k, index=a).groupby(level=0).sum(); dp = pd.Series(k * p, index=a).groupby(level=0).sum()
        dests[lv] = {q: {'kids': round(float(dk[q])), 'poverty': round(float(dp[q]))}
                     for q in dk.sort_values(ascending=False).index if dk[q] >= 1}
    bt = pd.read_csv(f'{d}/schools.csv').set_index('school')
    dur = sc['durability']['levels']['K-5']['schools']
    neigh = {q: {'total_2031': round(float(bt.total[q])) if q in bt.index and bt.total[q] > 0 else 0,
                 'at_target_every_year': bool(dur.get(q, {}).get('in_range_all_required_years'))} for q in NEIGH}
    return r, dests, neigh


f0 = lambda x: f'{x:.0f}%'
f2 = lambda x: f'{x:.2f}'
fd = lambda x: f'{x:+.2f}'
JS = {'note': 'Model v2 estimates, 2031-32 projected kids, by today\'s attendance area. pov = students experiencing poverty '
              '(Census <185% of poverty anchored to PPS school rates; rough for areas this small), oth = all other students. '
              'mv/in1/bus/sust/pps are percents; walk/dwalk are miles. Render only plans whose status is "done".',
      'source': 'build/solver/sabin_poverty.py', 'plans': []}
# (2026-10-22, site chat) how many schools this corner can fill: 2031-32 K-5 kids living in today's areas of these schools,
# plus the K-5 programs housed in them under the featured plan (King's Mandarin), against the 360 floor
CLUSTER = ['Sabin', 'Irvington', 'MLK Jr', 'Alameda', 'Vernon', 'Beverly Cleary', 'Boise-Eliot/Humboldt']
_cfg = json.load(open('configs/v2/equity_noswap_alameda_rig.json'))
_nb = float(KSQ['K-5'][np.isin(b['sq_es'].values, CLUSTER)].sum())
_pg = float(sum(v for q, v in M.program_totals(_cfg, 'K-5').items() if q in CLUSTER))
JS['capacity'] = {'schools': CLUSTER, 'year': '2031-32', 'neighborhood_k5_kids': round(_nb), 'program_k5_kids': round(_pg),
                  'total_k5_kids': round(_nb + _pg), 'floor': 360,
                  'kids_needed': {str(n): 360 * n for n in (5, 6, 7)},
                  'note': "K-5 kids living in these seven schools' current attendance areas plus the K-5 immersion program housed "
                          "there (King's Mandarin, as in the featured plan); compares with 360 per open school. Model v2, 2031-32."}
JS['note'] = JS['note'].replace('anchored to PPS school rates', "anchored to each school's direct-certification rate in PPS's Status Quo dashboard")
# (2026-10-22, site chat) by-year building totals for the Sabin page's size table, from the same building_table totals as
# durability.sizes_by_year, but for exempt schools too (Sabin, Vernon, Irvington); a closed school is left out
SY_SCHOOLS = ['Sabin', 'Irvington', 'Beverly Cleary', 'MLK Jr', 'Boise-Eliot/Humboldt', 'Vernon', 'Alameda',
              'Beaumont', 'Tubman', 'Jefferson', 'Grant']
_SY = {}


def school_years(n):
    if n not in _SY:
        d = plan_dir(n)
        cfg = C.load_config(f'configs/v2/{n}.json')
        plan = {lv: asg(d, lv).astype(object) for lv in C.LEVELS}
        yrs = json.load(open(f'{d}/scorecard.json'))['durability']['years']
        out = {}
        for y in yrs:
            bt = M.building_table(cfg, plan, year=y[:4]).set_index('school')
            for s in SY_SCHOOLS:
                if s in bt.index and bt.loc[s, 'total'] > 0:
                    out.setdefault(s, {'type': bt.loc[s, 'type'], 'years': {}})['years'][y] = round(float(bt.loc[s, 'total']), 1)
        _SY[n] = out
    return _SY[n]


MD = []
for AREA in AREAS:
    m = b['sq_es'].values == AREA
    rows = []
    for n, lab in SPLANS:
        d = plan_dir(n)
        if not d or not os.path.exists(f'{d}/scorecard.json'):
            continue
        r, dests, neigh = plan_rows(d, m)
        r['lab'] = lab; r['dests'] = dests
        rows.append(r)
        JS['plans'].append({'area': AREA, 'run': n, 'label': lab, 'status': status(n),
                            'groups': {lv: {g: {k_.split('_', 2)[2]: round(float(v), 4) for k_, v in r.items()
                                                if k_.startswith(f'{lv}_{g}_')}
                                            for g in ('pov', 'oth')} for lv in ('K-5', '6-8', '9-12')},
                            'destinations': dests,
                            'district': {'schools_open': int(r['d_n']), 'pct_sustainable_schools': round(r['d_sust'], 1),
                                         'pct_students_in_sustainable': round(r['d_in_sust'], 1)},
                            'neighbor_schools': neigh, 'school_years': school_years(n)})
    q = lambda r, lv, k_, f: f"{f(r[f'{lv}_pov_{k_}'])} / {f(r[f'{lv}_oth_{k_}'])}"
    out = [f'# {AREA}-area families: students experiencing poverty vs all others', '',
           f'Today\'s {AREA} attendance area, 2031-32 projected kids. Estimated {rows[0]["K-5_pov_n"]:.0f} of '
           f'{rows[0]["K-5_pov_n"] + rows[0]["K-5_oth_n"]:.0f} K-5 kids live in poverty (Census <185% of poverty, anchored to PPS '
           'school direct-certification rates; small numbers, so read the shares as rough). Each cell: students experiencing poverty / all other students.', '',
           '## Elementary (K-5)', '',
           '| Plan | Moved from today\'s school | Avg walk (mi) | Walk change vs today (mi) | Within 1 mi | Past the 1-mile bus line | In a school at target every year |',
           '|---|---|---|---|---|---|---|']
    out += [f"| {r['lab']} | {q(r, 'K-5', 'mv', f0)} | {q(r, 'K-5', 'walk', f2)} | {q(r, 'K-5', 'dwalk', fd)} | {q(r, 'K-5', 'in1', f0)} | "
            f"{q(r, 'K-5', 'bus', f0)} | {q(r, 'K-5', 'sust', f0)} |" for r in rows]
    out += ['', '## Middle school (6-8)', '',
            '| Plan | Moved | Avg walk (mi) | Walk change (mi) | Past the 1.5-mile bus line | In a school at target every year |', '|---|---|---|---|---|---|']
    out += [f"| {r['lab']} | {q(r, '6-8', 'mv', f0)} | {q(r, '6-8', 'walk', f2)} | {q(r, '6-8', 'dwalk', fd)} | {q(r, '6-8', 'bus', f0)} | "
            f"{q(r, '6-8', 'sust', f0)} |" for r in rows]
    out += ['', '## High school (9-12)', '', '| Plan | Moved | Walk change (mi) | In a school at target every year |', '|---|---|---|---|']
    out += [f"| {r['lab']} | {q(r, '9-12', 'mv', f0)} | {q(r, '9-12', 'dwalk', fd)} | {q(r, '9-12', 'sust', f0)} |" for r in rows]
    out += ['', f'## {AREA}-area kids in a sustainable school (PPS definition: at or above 360 / 500 / 1,100 in 2031-32)', '',
            '| Plan | K-5 | 6-8 | 9-12 |', '|---|---|---|---|']
    out += ['| ' + r['lab'] + ' | ' + ' | '.join(q(r, lv, 'pps', f0) for lv in ('K-5', '6-8', '9-12')) + ' |' for r in rows]
    if AREA == AREAS[0]:
        out += ['', '## District: PPS dashboard sustainability (all levels, 2031-32)', '',
                '| Plan | Schools open | % sustainable schools | % of students in sustainable schools |', '|---|---|---|---|']
        out += [f"| {r['lab']} | {r['d_n']} | {r['d_sust']:.0f}% | {r['d_in_sust']:.0f}% |" for r in rows]
    out += ['', f'## Where {AREA}-area kids go', '', '| Plan | Level | Schools (kids, of whom in poverty) |', '|---|---|---|']
    out += [f"| {r['lab']} | {lv} | " + ', '.join(f"{s} {v['kids']} ({v['poverty']} in poverty)" for s, v in r['dests'][lv].items()) + ' |'
            for r in rows for lv in ('K-5', '6-8', '9-12')]
    MD.append('\n'.join(out))
open('out_v2/SABIN_POVERTY.md', 'w').write('\n\n'.join(MD) + '\n')
json.dump(JS, open('out_v2/SABIN_OPTIONS.json', 'w'), indent=1)
print('\n\n'.join(MD))
