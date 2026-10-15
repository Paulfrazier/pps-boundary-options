"""PPS's own durability numbers for PPS's own plans (Paul 2026-10-14: "use the official PPS data to represent their models").

  python durability_vs_pps.py      -> out_v2/PPS_OFFICIAL_DURABILITY.json (+ a check table on stdout)

For PPS Status Quo, PPS A and PPS B: each school's enrollment by year 2027-28 to 2031-32 is PPS's own Family Guide figure
("How many students are expected?", p. 4; guides dated 2026-10-08; digitized in build/data/scenarios.json ->
pps_projections_2027_28_to_2031_32, re-checked here against the archived text in build/pps-texts/family-guide-*.md).
"No changes" = PSU PRC July 24, 2026 forecast, Table 5.5.  At target = the same rule as every plan on the site (floor
360 K-5, 500 K-8 and 6-8, 1,100 9-12; ceiling = building capacity, PPS School Profiles 2025-26, captured second-hand),
over the same schools as our scorecards (zoned, not exempt, not focus, not program-only).  PPS publishes no figures
past 2031-32, so later years are absent.  The JSON mirrors scorecard['durability'] so the site can swap it in."""
import glob, json, os, re
import pandas as pd
import common as C, metrics as MX
from calibrate import ALIAS

OUT = os.path.join(C.SOLVER, 'out_v2')
TEXTS = os.path.join(C.SOLVER, '..', 'pps-texts')
YR = ['2027-28', '2028-29', '2029-30', '2030-31', '2031-32']
PLANS = {'status_quo': 'no_change', 'scenario_A': 'A', 'scenario_B': 'B'}
SRC = ('PPS Family Guides, "How many students are expected?" table, p. 4 (guides dated 2026-10-08; '
       'https://www.pps.net/about/portland-public-schools-information/rightsize/how-could-your-school-be-impacted), '
       'archived as build/pps-texts/family-guide-*.md. "No changes" row = PSU PRC July 24, 2026 forecast, Table 5.5.')


def guide_rows():
    """{guide file stem: {row label: [5 ints]}} from the archived row-wise text"""
    out = {}
    for f in glob.glob(os.path.join(TEXTS, 'family-guide-*.md')):
        rows, on = {}, False
        for ln in open(f):
            ln = ln.strip()
            if ln.startswith('School year 2027-28 2028-29'):
                on = True
                continue
            if on and (ln.startswith('Programs') or ln.startswith('Measure')):
                break
            m = re.match(r'^(No changes|Options A and B|Options A & B|Option A|Option B)\s+([\d,\s]+)$', ln) if on else None
            if m:
                nums = [int(x.replace(',', '')) for x in m.group(2).split()]
                if len(nums) == 5:
                    rows[m.group(1)] = nums
        out[os.path.basename(f)[13:-3]] = rows
    return out


def check_digitized(P0, G):
    """every guide row found in the text must equal the digitized figure; returns (checked, mismatches)"""
    norm = lambda s: re.sub(r'[^a-z]', '', s.lower())
    gi = {norm(k): v for k, v in G.items()}
    n, bad = 0, []
    for s, d in P0.items():
        rows = gi.get(norm(s))
        if not rows:
            continue
        for lab, keys in (('No changes', ['no_change']), ('Options A and B', ['A', 'B']), ('Options A & B', ['A', 'B']),
                          ('Option A', ['A']), ('Option B', ['B'])):
            if lab in rows:
                for k in keys:
                    n += 1
                    if list(d.get(k) or []) != rows[lab]:
                        bad.append((s, k, d.get(k), rows[lab]))
    return n, bad


if __name__ == '__main__':
    P0 = json.load(open(os.path.join(C.SOLVER, '..', 'data', 'scenarios.json')))['pps_projections_2027_28_to_2031_32']
    n, bad = check_digitized(P0, guide_rows())
    print(f'digitized figures checked against guide text: {n} rows, {len(bad)} mismatches')
    for b in bad:
        print('   MISMATCH', b)
    res = {'basis': __doc__.split('\n\n', 1)[1].strip(), 'source': SRC, 'years': YR, 'required_years': YR,
           'reported_years': [], 'plans': {}}
    for run, key in PLANS.items():
        cfg = C.load_config(os.path.join(C.SOLVER, 'configs', 'v2', f'{run}.json'))
        sc = json.load(open(os.path.join(OUT, run, 'scorecard.json')))
        C.resolve_config(cfg, sc)
        plan = {l: pd.read_parquet(os.path.join(OUT, run, f'assign_{l}.parquet'))['school'].values for l in C.LEVELS}
        bt = MX.building_table(cfg, plan).set_index('school')
        levels = {}
        for lev, L in sc['durability']['levels'].items():
            schools, counts = {}, {y: 0 for y in YR}
            for s, v in L['schools'].items():
                if v['program_only']:
                    continue
                fig = P0.get(ALIAS.get(s, s), {}).get(key)
                if not fig or len(fig) != 5:
                    raise SystemExit(f'no PPS figure for {run} {s}')
                fl, ce = float(bt.loc[s, 'floor']), bt.loc[s, 'ceiling']
                inr = [bool(x >= fl and (pd.isna(ce) or x <= ce)) for x in fig]
                first = next(((y, x - (fl if x < fl else float(ce))) for y, x, ok in zip(YR, fig, inr) if not ok), None)
                for y, ok in zip(YR, inr):
                    counts[y] += ok
                schools[s] = {'sizes_by_year': dict(zip(YR, fig)), 'in_range_by_year': inr,
                              'in_range_all_required_years': all(inr), 'in_range_all_years': all(inr),
                              'first_year_out': first[0] if first else None, 'by': first[1] if first else None,
                              'size_2031': fig[-1], 'floor': fl, 'capacity': None if pd.isna(ce) else float(ce),
                              'program_only': False, 'pps_name': ALIAS.get(s, s)}
            levels[lev] = {'n_zoned_non_exempt': len(schools), 'at_target_zoned': counts,
                           'at_target_all_required_years': sum(v['in_range_all_required_years'] for v in schools.values()),
                           'schools': schools,
                           'model_at_target_all_required_years': L['at_target_all_required_years']}
        res['plans'][run] = {'durability': {'years': YR, 'required_years': YR, 'reported_years': [], 'horizon': 'pps2031',
                                            'basis': 'PPS Family Guide figures', 'levels': levels}}
    json.dump(res, open(os.path.join(OUT, 'PPS_OFFICIAL_DURABILITY.json'), 'w'), indent=1)
    print('\n| Plan | Level | PPS figures: at target every year | Our model | By year (PPS figures) |\n|---|---|---:|---:|---|')
    for run, d in res['plans'].items():
        for lev, L in d['durability']['levels'].items():
            print(f"| {run} | {lev} | {L['at_target_all_required_years']}/{L['n_zoned_non_exempt']} | "
                  f"{L['model_at_target_all_required_years']} | {list(L['at_target_zoned'].values())} |")
