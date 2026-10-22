"""Every plan scored on PPS's own dashboard measures (2026-10-21, Paul: "get me the pps table").

PPS's District Rightsizing & School Boundary Proposal Dashboard
(https://www.pps.net/about/portland-public-schools-information/rightsize/dashboard; v1.1, Oct 15 2026; our capture
build/pps-texts/pps-rightsizing-dashboard-2026-10-15.md) scores each scenario on: schools closed; % of schools sustainable
in 2031-32; % of students in sustainable schools 2031-32, overall and for Students Experiencing Poverty; % of K-8
students moved; % of students living within 1 and 1.5 miles (K-5, 6-8); % of buildings efficiently utilized 2031-32
(70%-100% of capacity). PPS's sustainable = at or above 360 (K-5), 500 (K-8, 6-8), 1,100 (9-12) in 2031-32, one year
only (our solver's "at target" is stricter: every year 2027-28..2031-32).

Our approximations: schools are the ones our model carries (neighborhood, immersion and focus hosts; alternative
programs like ACCESS are not modeled); utilization uses each building's Status Quo capacity (so a config's soft size
ceiling does not count as capacity); "within" uses our network walk, which runs a few points above PPS's
figure (build/pps-texts/pps-rightsizing-dashboard-2026-10-15.md); poverty shares are poverty_compare.py's block estimate.
Writes out_v2/PPS_SCORECARD.md (every plan, poverty columns; not published) and out_v2/PPS_SCORECARD_public.md (runs listed
done in MANIFEST_public.json, no poverty columns).   Run from build/solver:  ../../.venv/bin/python pps_scorecard.py
"""
import os, json, io, contextlib
import numpy as np, pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
# the poverty estimate and plan list are poverty_compare.py's (its setup section, before the PPS dashboard figures)
_src = open('poverty_compare.py').read().split("# ---- PPS's own figures")[0]
with contextlib.redirect_stdout(io.StringIO()):
    exec(_src)
PLANS = [('status_quo', 'Status Quo')] + PLANS

FLOOR = {'K-5': 360, 'K-8': 500, '6-8': 500, '9-12': 1100}
CAP = pd.read_csv(f'{SQ}/schools.csv').set_index('school')['capacity']
# PPS's own figures for its scenarios (dashboard p. 2-4), shown for checking
PPS = {'scenario_A': {'closed': 14, 'sust': 67, 'in_sust': 80, 'dc_sust': 81, 'moved': 27, 'dc_moved': 27, 'k5_1': 55, 'k5_15': 78},
       'scenario_B': {'closed': 11, 'sust': 59, 'in_sust': 74, 'dc_sust': 76, 'moved': 24, 'dc_moved': 25, 'k5_1': 58, 'k5_15': 79},
       'status_quo': {'closed': 0, 'sust': 26, 'in_sust': 48, 'dc_sust': 42, 'k5_1': 65, 'k5_15': 81}}


def score(d):
    s = pd.read_csv(f'{d}/schools.csv')
    s = s[s['total'] > 0].copy()
    s['floor_pps'] = s['type'].map(FLOOR).fillna(360)
    s['sust'] = s['total'] >= s['floor_pps'] - 0.5
    cap = s['school'].map(CAP).fillna(s['capacity'])
    u = s['total'] / cap
    sc = json.load(open(f'{d}/scorecard.json'))
    L = sc['levels']
    # Students Experiencing Poverty by school: neighborhood students only (block estimate), all levels
    good = set(s.loc[s['sust'], 'school'])
    pov = oth = pov_in = oth_in = 0.0; mv_p = mv_o = tot_p = tot_o = 0.0
    for lv in C.LEVELS:
        a = asg(d, lv); k = KSQ[lv]; p = P[lv]
        inn = np.isin(a, list(good))
        pov += (k * p).sum(); oth += (k * (1 - p)).sum()
        pov_in += (k * p)[inn].sum(); oth_in += (k * (1 - p))[inn].sum()
        if lv in ('K-5', '6-8'):
            m = a != asg(SQ, lv)
            mv_p += (k * p)[m].sum(); mv_o += (k * (1 - p))[m].sum(); tot_p += (k * p).sum(); tot_o += (k * (1 - p)).sum()
    return {'open': len(s), 'sust': 100 * s['sust'].mean(), 'in_sust': 100 * s.loc[s['sust'], 'total'].sum() / s['total'].sum(),
            'dc_sust': 100 * pov_in / pov, 'oth_sust': 100 * oth_in / oth,
            'moved': 100 * (mv_p + mv_o) / (tot_p + tot_o), 'dc_moved': 100 * mv_p / tot_p,
            'k5_1': L['K-5']['pct_within_1.0mi'], 'k5_15': L['K-5']['pct_within_1.5mi'],
            'ms_1': L['6-8']['pct_within_1.0mi'], 'ms_15': L['6-8']['pct_within_1.5mi'],
            'util': 100 * ((u >= 0.70) & (u <= 1.00)).mean()}


R = []
for n, lab in PLANS:
    d = folder(n)
    if d:
        R.append((n, lab, score(d)))
open0 = R[0][2]['open']
f = lambda x: f'{x:.0f}%'
out = ['# Plans on PPS\'s own dashboard measures', '',
       'Measures and wording from PPS\'s rightsizing dashboard (https://www.pps.net/about/portland-public-schools-information/rightsize/dashboard, '
       'v1.1 Oct 15 2026). 2031-32 basis; "sustainable" = at or above 360 (K-5), 500 (K-8, 6-8), 1,100 (9-12) that year. '
       'Our model\'s figures, so Status Quo and PPS A/B rows show how close we get to PPS\'s own (in brackets). Staging runs; not for the site.', '',
       '| Plan | Schools closed | % Sustainable Schools 31-32 | % of Students in Sustainable Schools 31-32 | % Students Experiencing Poverty in Sustainable Schools | '
       '% all other students in Sustainable Schools | K-8 students moved | Students Experiencing Poverty moved | K-5 within 1 mi / 1.5 mi | '
       '6-8 within 1 mi / 1.5 mi | % Efficiently Utilized 31-32 |',
       '|---' * 11 + '|']
for n, lab, r in R:
    pp = PPS.get(n, {})
    g = lambda k, txt: txt + (f' [{pp[k]}%]' if k in pp else '')
    out.append(f"| {lab} | {open0 - r['open']}" + (f" [{pp['closed']}]" if 'closed' in pp else '') +
               f" | {g('sust', f(r['sust']))} | {g('in_sust', f(r['in_sust']))} | {g('dc_sust', f(r['dc_sust']))} | {f(r['oth_sust'])} | "
               f"{g('moved', f(r['moved'])) if n != 'status_quo' else '-'} | {g('dc_moved', f(r['dc_moved'])) if n != 'status_quo' else '-'} | "
               f"{r['k5_1']:.0f}% / {r['k5_15']:.0f}%" + (f" [{pp['k5_1']}% / {pp['k5_15']}%]" if 'k5_1' in pp else '') +
               f" | {r['ms_1']:.0f}% / {r['ms_15']:.0f}% | {f(r['util'])} |")
out += ['', 'How these are computed: schools closed = buildings open in our Status Quo minus open in the plan (our model carries '
        f'{open0} Status Quo buildings; PPS counts closures of its own list). Sustainable and students-in-sustainable use all students '
        '(neighborhood + immersion + focus) in 2031-32. The poverty columns use neighborhood students only (block estimate, '
        'poverty_compare.py). Moved = K-5 and 6-8 neighborhood students zoned to a different school than Status Quo (PPS\'s '
        'K-8 measure). Within 1 / 1.5 mi = our network walk to the assigned school; PPS does not publish its method and its '
        'shares run a few points lower. Efficiently utilized = 2031-32 total between 70% and 100% of the building\'s Status Quo capacity.']
open('out_v2/PPS_SCORECARD.md', 'w').write('\n'.join(out) + '\n')

# public version: only runs MANIFEST_public.json lists as done (their final folders, never staging), no poverty columns
PUB = {k for k, v in json.load(open('out_v2/MANIFEST_public.json'))['runs'].items() if v.get('status') == 'done'}
pub = ['# Plans on PPS\'s own dashboard measures', '',
       'Measures and wording from PPS\'s rightsizing dashboard (https://www.pps.net/about/portland-public-schools-information/rightsize/dashboard, '
       'v1.1 Oct 15 2026). 2031-32 basis; "sustainable" = at or above 360 (K-5), 500 (K-8, 6-8), 1,100 (9-12) that year. '
       'Our model\'s figures (model v2 on PSU July 2026 Table 5.5), so Status Quo and PPS A/B rows show how close we get to PPS\'s own (in brackets).', '',
       '| Plan | Schools closed | % Sustainable Schools 31-32 | % of Students in Sustainable Schools 31-32 | K-8 students moved | '
       'K-5 within 1 mi / 1.5 mi | 6-8 within 1 mi / 1.5 mi | % Efficiently Utilized 31-32 |',
       '|---' * 8 + '|']
for n, lab, r in R:
    if n not in PUB or not os.path.exists(f'out_v2/{n}/scorecard.json'):
        continue
    pp = PPS.get(n, {})
    g = lambda k, txt: txt + (f' [{pp[k]}%]' if k in pp else '')
    pub.append(f"| {json.load(open(f'out_v2/{n}/scorecard.json')).get('label', lab)} | {open0 - r['open']}" + (f" [{pp['closed']}]" if 'closed' in pp else '') +
               f" | {g('sust', f(r['sust']))} | {g('in_sust', f(r['in_sust']))} | {g('moved', f(r['moved'])) if n != 'status_quo' else '-'} | "
               f"{r['k5_1']:.0f}% / {r['k5_15']:.0f}%" + (f" [{pp['k5_1']}% / {pp['k5_15']}%]" if 'k5_1' in pp else '') +
               f" | {r['ms_1']:.0f}% / {r['ms_15']:.0f}% | {f(r['util'])} |")
pub += ['', 'How these are computed: schools closed = buildings open in our Status Quo minus open in the plan (our model carries '
        f'{open0} Status Quo buildings; PPS counts closures of its own list). Sustainable and students-in-sustainable use all students '
        '(neighborhood + immersion + focus) in 2031-32, from each run\'s schools.csv. Moved = K-5 and 6-8 neighborhood students zoned to a '
        'different school than Status Quo (PPS\'s K-8 measure). Within 1 / 1.5 mi = our network walk to the assigned school (scorecard.json '
        'pct_within_1.0mi / pct_within_1.5mi); PPS does not publish its method and its shares run a few points lower. Efficiently utilized = '
        '2031-32 total between 70% and 100% of the building\'s Status Quo capacity. Computed by build/solver/pps_scorecard.py.']
open('out_v2/PPS_SCORECARD_public.md', 'w').write('\n'.join(pub) + '\n')

print('\n'.join(out))
