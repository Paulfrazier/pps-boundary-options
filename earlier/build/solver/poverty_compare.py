"""Plan comparison: impact on students experiencing poverty (2026-10-21, Paul). Uses PPS's own words and measure.

PPS's rightsizing dashboard reports, per scenario, the share of "Students Experiencing Poverty" (direct certification,
DC) who are moved, next to "All Students (K-8 Total)". We have no student records, so each block's DC share is estimated:
its Status Quo school's DC rate (PPS dashboard, Status Quo rows, "Free by DC", before change) spread within that school's
area by the block's ACS poverty rate (ACS C17002 under 185% of poverty, build/research/equity/block_poverty185.npy), so the area keeps PPS's school rate.
PPS A/B rows from the dashboard ("Seventy Percent" = A, "Fifty Percent" = B; DO-NOT-USE.md rules) are shown for checking.
Writes out_v2/POVERTY_COMPARE.md.   Run from build/solver:  ../../.venv/bin/python poverty_compare.py
"""
import os, json, re, unicodedata
import numpy as np, pandas as pd
import common as C, metrics as M, v2 as V

HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
DASH = '../pps-texts/pps-rightsizing-dashboard-model-2026-10-20/csv'
# (2026-10-21) within-area spread from ACS C17002 under 185% of poverty, smoothed (research/equity/build_block_poverty_v2.py);
# was ACS B17010 (block_poverty.npy), which read 0 in 338 of 1,240 block groups
POV = np.load('../research/equity/block_poverty185.npy')
PLANS = [('scenario_A', 'PPS Scenario A'), ('scenario_B', 'PPS Scenario B'), ('option2', 'Boundary changes, same closures (option2)'),
         ('option2_ms460', 'Balanced middle schools (best we modeled)'), ('planD', 'Plan D, as written'),
         ('equity_noswap', 'Equity: no program swaps'), ('equity_noswap_alameda', 'No swaps + big-school relief'), ('equity_noswap_alameda_rig', 'No swaps + big-school relief, Rigler-area kids corrected (before HS fix)'), ('dli_home3_rh', 'Current best: fewer DLI moves, sustainable schools'), ('equity_noswap_alameda_rig_hs', 'Previous best: no program swaps'), ('equity_noswap_bjj', 'No swaps + Beach and James John open'), ('equity_noswap_bjj_plus2', 'Beach + James John open, big-school relief, middle re-fit'), ('equity_noswap_bjj_rig', 'Beach + James John open, big-school relief, middle re-fit, Rigler-area kids corrected'), ('equity_nodli', 'Equity: immersion stays put + big-school relief'), ('equity_nodli_ms_hs', 'Immersion stays put: middle re-drawn from today'), ('equity2', 'Equity: no swaps + poverty weight (fixed data)'), ('equity_noswap_big', 'No swaps + big-school relief'), ('equity_noswap_bigpov', 'No swaps + big-school + low-poverty relief'), ('equity1', 'Equity: no swaps + poverty weight 0.5'),
         ('equity1_strong', 'Equity: no swaps + poverty weight 1.0'), ('planD_redraw', 'Scenario D, re-drawn'),
         ('beach_jj', 'Beach + James John open'), ('option2_fresh', 'option2, re-solved'),
         ('option2_mlkkeep', 'option2, MLK Jr only grows'), ('planD_redraw_mlkkeep', 'Scenario D re-drawn, MLK Jr only grows'),
         ('planD_sust', 'Scenario D buildings, every school at target'), ('planD_redraw_ms', 'Scenario D re-drawn, middle re-solved'),
         ('equity1_k5only', 'Equity: weight 0.5 at elementary only'),
         ('equity_noswap_hs', 'Equity: no swaps, high-school lines re-drawn'),
         ('equity_noswap_hs_eq', 'Equity: no swaps, high-school lines re-drawn with poverty weight')]
LV = ('K-5', '6-8')
REQ = [f'{y}-{str(y + 1)[2:]}' for y in range(2027, 2032)]


ALIAS = {'lane': 'brentwood', 'lee': 'sunrise', 'tubman': 'harriettubman', 'sunnyside': 'sunnysideenvironmental',
         'bridger': 'bridgercreativescience', 'idabwells': 'idabwellsbarnett'}


def norm(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z]', '', s.lower().replace('elementary', '').replace('middle', '').replace('school', ''))


def folder(n):
    for d in (f'out_v2/{n}', f'out_v2/{n}.staging'):
        if os.path.exists(f'{d}/scorecard.json'):
            return d


def asg(d, lv): return pd.read_parquet(f'{d}/assign_{lv}.parquet').sort_values('idx')['school'].values


# ---- PPS DC rate per Status Quo school -> per-block DC share
dp = pd.read_csv(f'{DASH}/demographic_pct.csv').dropna(how='all')
dp = dp[(dp['Scenario'] == 'Status Quo') & (dp['Demographic Component'] == 'Free by DC')]
dc = {norm(r['School Name']): float(r['Before Change %']) for _, r in dp.iterrows()}
SQ = folder('status_quo'); KSQ = M.level_kids(json.load(open('configs/v2/status_quo.json')))
P = {}; unmatched = set()
KSQ['9-12'] = KSQ['9-12']
for lv in LV + ('9-12',):
    s = asg(SQ, lv); k = KSQ[lv]; p = np.zeros(len(s))
    for sch in set(s):
        m = s == sch; r = dc.get(norm(sch), dc.get(ALIAS.get(norm(sch), '-')))
        if r is None:
            unmatched.add(sch); r = np.average(list(dc.values()))
        a = POV[m]; am = np.average(a, weights=k[m]) if k[m].sum() > 0 else a.mean()
        p[m] = np.clip(r * (a / am if am > 0 else 1.0), 0, 1)
    P[lv] = p

# ---- PPS's own figures for A / B (dashboard)
dm = pd.read_csv(f'{DASH}/demographic_moves.csv').dropna(how='all')
dm = dm[dm['Metric Category'] == 'Direct Certification']
pps = {}
for sc, lab in (('Seventy Percent', 'scenario_A'), ('Fifty Percent', 'scenario_B')):
    x = dm[dm['Scenario'] == sc].set_index('Demographic / Grade Band Segment')
    pps[lab] = {'pov': x.loc['Students Experiencing Poverty', '% Moved'], 'not': x.loc['Not DC', '% Moved'],
                'all': x.loc['All Students (K-8 Total)', '% Moved']}

# ---- immersion (DLI) students: PSU 2031-32 strand sizes; homes = data/focus_dli_homes.parquet (where DLI students live
# is not published: spread over the host's 2025-26 HS cluster, per PPS's lottery priority); DC share = the estimate
# above on those home blocks. Every strand student is assumed to follow the strand (follow rates ignored here).
# (2026-10-21) homes = data/focus_dli_homes.parquet, now the OBSERVED Oct 2025 home mix (PPS enrollment by school and HS
# area; data/scripts/06_focus_dli.py). Out-of-district students are not on blocks (column sums = in-district count).
HOMES = pd.read_parquet(os.path.join(C.DATA, 'focus_dli_homes.parquet'))
STRANDS = []
for key, (n25, n31, band) in C.PROGRAMS.items():
    lv = 'K-5' if band in ('K-5',) else ('6-8' if band == '6-8' else None)
    if lv is None or '|' not in key:
        continue
    try:
        col = V._home_col(key)
    except KeyError:
        continue
    h = HOMES[col].values.astype(float); h = h / max(h.sum(), 1e-9)
    STRANDS.append((key, lv, float(n31), h))


def hosts(cfg, lv):
    out = {}
    for host, keys in (cfg['levels'][lv].get('programs') or {}).items():
        for k_ in keys:
            out[k_] = host
    return out


SQCFG = json.load(open('configs/v2/status_quo.json'))
SQSC = json.load(open(f'{SQ}/scorecard.json'))


def sustainable(sc, lv):
    return {q for q, v in sc['durability']['levels'][lv]['schools'].items() if v.get('in_range_all_required_years')}


BUS = {'K-5': 1.0, '6-8': 1.5}
G = ('pov', 'oth', 'dli_pov', 'dli_oth')
rows = []
for n, lab in PLANS:
    d = folder(n)
    if not d:
        continue
    cfg = json.load(open(f'configs/v2/{n}.json')); K = M.level_kids(cfg)
    # a run that exempted schools from the floor (planD_redraw) is judged on PPS's bar for every school: use its
    # re-score (scorecard_scored360.json, same lines) for who is in a sustainable school
    sc = json.load(open(f'{d}/scorecard_scored360.json' if os.path.exists(f'{d}/scorecard_scored360.json') else f'{d}/scorecard.json'))
    t = {f'{g}_{m}': 0.0 for g in G for m in ('n', 'mv', 'far', 'bus', 'w0', 'w1', 'ok0', 'ok1')}
    for lv in LV:
        ok1s, ok0s = sustainable(sc, lv), sustainable(SQSC, lv)
        k = K[lv]; p = P[lv]; a = asg(d, lv); s = asg(SQ, lv); mv = a != s
        names = sorted(set(a) | set(s) | set(hosts(cfg, lv).values()) | set(hosts(SQCFG, lv).values()))
        W = C.dist('walk', names); ix = {q: j for j, q in enumerate(names)}
        r_ = np.arange(len(a)); da = W[r_, [ix[q] for q in a]]; ds = W[r_, [ix[q] for q in s]]
        ok = np.isfinite(da) & np.isfinite(ds)
        far = mv & ok & (da > ds + 0.1); bus = ok & (da > BUS[lv]) & (ds <= BUS[lv])
        for g, wgt in (('pov', k * p), ('oth', k * (1 - p))):
            t[g + '_n'] += wgt.sum(); t[g + '_mv'] += wgt[mv].sum(); t[g + '_far'] += wgt[far].sum(); t[g + '_bus'] += wgt[bus].sum()
            t[g + '_w0'] += (wgt * np.where(ok, ds, 0)).sum(); t[g + '_w1'] += (wgt * np.where(ok, da, 0)).sum()
            t[g + '_ok0'] += wgt[np.isin(s, list(ok0s))].sum(); t[g + '_ok1'] += wgt[np.isin(a, list(ok1s))].sum()
        h1, h0 = hosts(cfg, lv), hosts(SQCFG, lv)
        for key, slv, size, hv in STRANDS:
            if slv != lv or key not in h0:
                continue
            b0 = h0[key]; b1 = h1.get(key, b0)
            if b0 not in ix or b1 not in ix:
                continue
            d0 = np.nansum(hv * np.nan_to_num(W[:, ix[b0]])); d1 = np.nansum(hv * np.nan_to_num(W[:, ix[b1]]))
            sp = float(np.sum(hv * p))
            for g, wgt in (('dli_pov', size * sp), ('dli_oth', size * (1 - sp))):
                t[g + '_n'] += wgt; t[g + '_mv'] += wgt * (b1 != b0); t[g + '_far'] += wgt * (d1 > d0 + 0.1)
                t[g + '_w0'] += wgt * d0; t[g + '_w1'] += wgt * d1
                t[g + '_ok0'] += wgt * (b0 in ok0s); t[g + '_ok1'] += wgt * (b1 in ok1s)
    rows.append(dict(n=n, lab=lab, **t))


def grp(r, gs, m): return sum(r[f'{g}_{m}'] for g in gs)


L = []; w = L.append
w('# Impact on students experiencing poverty: plan comparison\n')
w('Models track, 2026-10-21. PPS\'s words and group from its rightsizing dashboard: **students experiencing poverty** '
  '(direct certification), K-8. Includes students in immersion (DLI) programs. Our runs are staging and not for the site '
  'until Paul reviews.\n')
w('## Outcome: in a sustainable school\n')
w('Share of each group whose school is in PPS\'s size range every year 2027-28 to 2031-32 (K-5 360, K-8 and middle 500, up '
  'to capacity), today\'s lines (Status Quo) vs the plan.\n')
w('| plan | students experiencing poverty | all other students | immersion students experiencing poverty | other immersion students |')
w('|---|---|---|---|---|')
for r in rows:
    c = []
    for gs in (('pov', 'dli_pov'), ('oth', 'dli_oth'), ('dli_pov',), ('dli_oth',)):
        c.append(f"{grp(r, gs, 'ok0') / grp(r, gs, 'n'):.0%} -> {grp(r, gs, 'ok1') / grp(r, gs, 'n'):.0%}")
    w(f"| {r['lab']} | " + ' | '.join(c) + ' |')
w('\n## Who has a worse trip to school\n')
w('Trip = walking-route distance from home to school. "Longer trip" = more than 0.1 mi longer than under today\'s lines. '
  '"Newly past the bus line" = within the bus distance today (K-5 1.0 mi, middle 1.5 mi), beyond it in the plan '
  '(neighborhood students; immersion students are mostly bused already).\n')
w('| plan | longer trip: students experiencing poverty / others | average trip change (mi): poverty / others | newly past the bus line: poverty / others | immersion students with a longer trip: poverty / others |')
w('|---|---|---|---|---|')
for r in rows:
    P_, O_ = ('pov', 'dli_pov'), ('oth', 'dli_oth')
    lt = f"{grp(r, P_, 'far') / grp(r, P_, 'n'):.1%} / {grp(r, O_, 'far') / grp(r, O_, 'n'):.1%}"
    tc = (f"{(grp(r, P_, 'w1') - grp(r, P_, 'w0')) / grp(r, P_, 'n'):+.2f} / "
          f"{(grp(r, O_, 'w1') - grp(r, O_, 'w0')) / grp(r, O_, 'n'):+.2f}")
    bu = f"{r['pov_bus'] / r['pov_n']:.1%} / {r['oth_bus'] / r['oth_n']:.1%}"
    dl = f"{r['dli_pov_far'] / r['dli_pov_n']:.1%} / {r['dli_oth_far'] / r['dli_oth_n']:.1%}"
    w(f"| {r['lab']} | {lt} | {tc} | {bu} | {dl} |")
w('\n## Moved to a different school than today\'s lines (PPS\'s dashboard measure)\n')
w('| plan | students experiencing poverty | all other students | immersion students moved |')
w('|---|---|---|---|')
for r in rows:
    w(f"| {r['lab']} | {grp(r, ('pov', 'dli_pov'), 'mv') / grp(r, ('pov', 'dli_pov'), 'n'):.1%} | "
      f"{grp(r, ('oth', 'dli_oth'), 'mv') / grp(r, ('oth', 'dli_oth'), 'n'):.1%} | {grp(r, ('dli_pov', 'dli_oth'), 'mv'):,.0f} |")
w('\nPPS\'s own figures (dashboard, student records): ' + '; '.join(
    f"{'A' if k_ == 'scenario_A' else 'B'}: students experiencing poverty {v['pov']:.1%} moved, other students "
    f"{v['not']:.1%}, all K-8 {v['all']:.1%}" for k_, v in pps.items()) + '.\n')
w('## How we estimate it\n')
w('- **Who is experiencing poverty.** We have no student records. Each home block\'s share is its Status Quo school\'s '
  'direct certification rate (PPS dashboard, Status Quo rows) spread within the school\'s area by neighborhood poverty '
  '(Census ACS 2019-2023, B17010), so each area keeps PPS\'s school rate. Our moved shares for PPS A and B land within '
  'about half a point of PPS\'s own.'
  + (f' No PPS rate found for: {", ".join(sorted(unmatched))} (district average used).' if unmatched else ''))
w('- **Immersion students.** Strand sizes are PSU\'s 2031-32 forecasts (Table 5.5). PPS publishes where immersion students live by high-school area (Oct 2025), so their homes follow PPS\'s observed October 2025 mix (Enrollment Summary by school and high-school '
  'area): each program\'s own-boundary students on the host\'s area, the rest on the high-school areas they live in; their poverty share is the estimate above on those blocks. When a '
  'strand moves, all its students are assumed to follow (PPS\'s own projections imply 80-90% do). Treat immersion rows as '
  'rough.')
w('- Neighborhood students are 2031-32 projections by where they live. Grades K-8.')
# ---- (2026-10-21, Paul: "need middle and hs feeders") high school, and feeders by group
HS = []; FD = []
for n, lab in PLANS:
    d = folder(n)
    if not d:
        continue
    cfg = json.load(open(f'configs/v2/{n}.json')); K = M.level_kids(cfg)
    sc = json.load(open(f'{d}/scorecard_scored360.json' if os.path.exists(f'{d}/scorecard_scored360.json') else f'{d}/scorecard.json'))
    A = {lv: asg(d, lv) for lv in C.LEVELS}; S = {lv: asg(SQ, lv) for lv in C.LEVELS}
    # high school: neighborhood students by home block
    k = K['9-12']; p = P['9-12']; a = A['9-12']; s_ = S['9-12']; mv = a != s_
    names = sorted(set(a) | set(s_)); W = C.dist('walk', names); ix = {q: j for j, q in enumerate(names)}
    r_ = np.arange(len(a)); da = W[r_, [ix[q] for q in a]]; ds = W[r_, [ix[q] for q in s_]]
    ok = np.isfinite(da) & np.isfinite(ds); far = mv & ok & (da > ds + 0.1)
    good = sustainable(sc, '9-12'); good0 = sustainable(SQSC, '9-12')
    h = {}
    for g, wgt in (('pov', k * p), ('oth', k * (1 - p))):
        h[g] = dict(mv=wgt[mv].sum() / wgt.sum(), far=wgt[far].sum() / wgt.sum(),
                    dw=(wgt * np.where(ok, da - ds, 0)).sum() / wgt.sum(),
                    ok0=wgt[np.isin(s_, list(good0))].sum() / wgt.sum(), ok1=wgt[np.isin(a, list(good))].sum() / wgt.sum())
    HS.append((lab, h))
    # feeders: a student "stays with classmates" when their school's largest next-level destination is theirs
    f = {}
    for (lo, hi), plan_ in (((('K-5', '6-8')), A), ((('K-5', '6-8')), S), ((('6-8', '9-12')), A), ((('6-8', '9-12')), S)):
        pass
    for tag, plan_ in (('plan', A), ('sq', S)):
        for lo, hi in (('K-5', '6-8'), ('6-8', '9-12')):
            k = K[lo]; p = P[lo]
            df = pd.DataFrame({'a': plan_[lo], 'b': plan_[hi], 'k': k})
            top = df[df.k > 0].groupby(['a', 'b']).k.sum().reset_index().sort_values('k').drop_duplicates('a', keep='last')
            topm = dict(zip(top.a, top.b))
            tog = np.array([topm.get(x) == y for x, y in zip(plan_[lo], plan_[hi])])
            for g, wgt in (('pov', k * p), ('oth', k * (1 - p))):
                f[(tag, lo, g)] = wgt[tog].sum() / wgt.sum()
    FD.append((lab, f))

w('\n## High school (grades 9-12, neighborhood students)\n')
w('In-district high-school lines: PPS A\'s in PPS A, option2 and the equity runs; Status Quo in Scenario D. Immersion '
  'high-school programs stay put in every plan here.\n')
w('| plan | moved: poverty / others | longer trip: poverty / others | average trip change (mi): poverty / others | in a sustainable high school (today -> plan): poverty / others |')
w('|---|---|---|---|---|')
for lab, h in HS:
    w(f"| {lab} | {h['pov']['mv']:.1%} / {h['oth']['mv']:.1%} | {h['pov']['far']:.1%} / {h['oth']['far']:.1%} | "
      f"{h['pov']['dw']:+.2f} / {h['oth']['dw']:+.2f} | {h['pov']['ok0']:.0%} -> {h['pov']['ok1']:.0%} / {h['oth']['ok0']:.0%} -> {h['oth']['ok1']:.0%} |")
w('\n## Feeders: staying with classmates\n')
w('Share of each group whose school sends most of its students to the same next school they go to (elementary -> middle, '
  'middle -> high), today\'s lines -> the plan. Lower means more students split from most of their class.\n')
w('| plan | elementary -> middle: poverty | others | middle -> high: poverty | others |')
w('|---|---|---|---|---|')
for lab, f in FD:
    w(f"| {lab} | {f[('sq','K-5','pov')]:.0%} -> {f[('plan','K-5','pov')]:.0%} | {f[('sq','K-5','oth')]:.0%} -> {f[('plan','K-5','oth')]:.0%} | "
      f"{f[('sq','6-8','pov')]:.0%} -> {f[('plan','6-8','pov')]:.0%} | {f[('sq','6-8','oth')]:.0%} -> {f[('plan','6-8','oth')]:.0%} |")
open('out_v2/POVERTY_COMPARE.md', 'w').write('\n'.join(L) + '\n')
print('\n'.join(L))
