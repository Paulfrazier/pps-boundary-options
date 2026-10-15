"""Maintain out_v2/MANIFEST.json (TRACKS.md contract).  Usage:
  python mk_manifest.py set <run> <status> [notes]     (status: queued|running|done|failed)
  python mk_manifest.py calibrated true|false
A run is only marked done after its folder holds every contract file (checked here)."""
import datetime as dt, json, os, sys
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out_v2')
P = os.path.join(OUT, 'MANIFEST.json')
NEED = ['assign_K-5.parquet', 'assign_6-8.parquet', 'assign_9-12.parquet', 'scorecard.json', 'schools.csv']
NEED_OPT = NEED + ['infeasibility.json', 'solve_log.txt']
CHANGES = [
    'fix 1: focus-lottery students (Sunnyside, Bridger, Buckman) are a separate population. A school with its own change follows PPS\'s stated rule: Buckman\'s enrolled students split 50/50 Abernethy/Sunnyside (Oct 6 memo p. 2); Sunnyside K-5 lottery students stay through grade 5 then return home (Sunnyside guide p. 3); Bridger 6-8 lottery students go to Harrison Park (Bridger guide p. 3); Sunnyside 6-8 lottery students return home. Returners live where Census residents live in the host\'s high-school cluster.',
    'fix 2: ~117 Lent-area non-DLI students (Marysville today; PPS capture report Oct 2025) are modeled. PPS baselines A/B keep them with Marysville at Arleta (PPS phase-in, Marysville guide p. 3); options assign them by where they live.',
    'fix 3: DLI arrival shares for moved strands IMPLIED by PPS Family Guide projections (not PPS-stated): Lent ~0.80, Rigler ~0.83, Woodstock 0.84-0.93, Chavez ~0.89, Beaumont->Roseway ~0.90; non-arrivals stay at the sending school if it still serves those grades, else go home.',
    'fix 4: capacities from PPS 2025-26 school profiles (captured second-hand via pps-dli-explorer snapshots; archived in build/pps-texts/school-profiles-2025-26/).',
    'fix 5: targets.md: 70-100% utilization is a PPS-stated aim (Family Guide glossary p. 2; PPS staff, Sept 15 2026 board meeting).',
    'fix 6: durability uses each school\'s own PSU July 2026 Table 5.5 forecast by year to 2035-36, extended to 2040-41 with the PSU medium district trend.',
    'Scenario A 9-12 lines kept in every option (Paul, 2026-10-12).',
    'scorecard.json durability.levels[*].schools[*].in_range_by_year added (aligned with durability.years).',
    'horizon "pps2031" (Paul 2026-10-12 ~15:15; configs key "horizon"): durability REQUIRES meet-or-beat Scenario A\'s count at target every year 2027-28 to 2031-32 at every level (PPS Family Guide p. 1, "Estimates cover 2027-28 through 2031-32"; per-school PSU Table 5.5 sizes); 2032-33 to 2035-36 REPORTED only; the 2036-41 district-trend extension is dropped. Applies to the baselines and to option1_durable, option2, option4 reruns; older runs keep horizon psu2041 (2031-32 to 2040-41). New scorecard keys: durability.horizon, required_years, reported_years, levels[*].at_target_all_required_years, at_target_all_years_to_2035_36, schools[*].in_range_all_required_years, durability.reference.',
    'middle->high feeders SOFT (Paul 2026-10-12 ~15:15): 200 kid-miles per extra high school a middle zone feeds, no floor; K-5 not hard-nested in A\'s high-school lines (0.1 kid-mile per kid across a line).',
]
def load():
    if os.path.exists(P):
        return json.load(open(P))
    return {'model_version': 'v2', 'calibrated': False, 'calibration_report': 'build/solver/out_v2/CALIBRATION.md',
            'changes_vs_v1': CHANGES, 'runs': {}}
def save(m):
    m['changes_vs_v1'] = CHANGES
    m['updated'] = dt.datetime.now().isoformat(timespec='seconds')
    tmp = P + '.tmp'
    json.dump(m, open(tmp, 'w'), indent=1); os.replace(tmp, P)
if __name__ == '__main__':
    m = load(); a = sys.argv[1:]
    if a[0] == 'calibrated':
        m['calibrated'] = a[1] == 'true'
    elif a[0] == 'set':
        run, st = a[1], a[2]
        note = a[3] if len(a) > 3 else m['runs'].get(run, {}).get('notes', '')
        if st == 'done':
            need = NEED if run in ('today', 'status_quo', 'scenario_A', 'scenario_B') else NEED_OPT
            miss = [f for f in need if not os.path.exists(os.path.join(OUT, run, f))]
            if miss:
                raise SystemExit(f'{run}: missing {miss}; not marking done')
        r = {'status': st, 'notes': note}
        if st in ('done', 'failed'):
            r['finished'] = dt.datetime.now().isoformat(timespec='seconds')
        m['runs'][run] = r
    save(m); print(json.dumps(m['runs'], indent=1)); print('calibrated', m['calibrated'])
