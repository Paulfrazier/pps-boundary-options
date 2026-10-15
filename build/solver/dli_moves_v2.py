"""Option 2 recount: DLI students moved under Scenario A vs Option 2, gross and net of PPS-implied non-followers.
  python dli_moves_v2.py [out_dir]  -> <out_dir>/dli_moves.json, default out_v2/option2.staging (+ markdown on stdout)
2026-10-12 ~15:15 (Paul): Atkinson->Lent and Scott->Rigler are NECESSARY moves (Lent/Rigler below 360 otherwise);
the option2 config now makes them, so "avoided" = MLK Jr Mandarin + Beaumont Spanish 6-8."""
import json, os, sys
import common as C, v2 as V2
def moves(cfgname):
    cfg = C.load_config(os.path.join(C.SOLVER, 'configs', 'v2', f'{cfgname}.json'))
    th = V2.today_hosts()
    zoned = {lev: set(cfg['levels'][lev]['zoned']) for lev in C.LEVELS}
    out = []
    for lev in ('K-5', '6-8'):
        for host, keys in cfg['levels'][lev].get('programs', {}).items():
            for k in keys:
                src = th.get(k)
                if src is None or src == host:
                    continue
                s = V2.program_series(k)
                f = V2.follow_rate(k, 2031)
                src_open = src in zoned[lev] or src in cfg['levels'][lev].get('programs', {})
                out.append({'strand': k, 'level': lev, 'from': src, 'to': host, 'sending_building_stays_open_at_level': src_open,
                            'n_2025_26': round(s[2025]), 'n_2031_32': round(s[2031]), 'arrival_share_2031_implied': f,
                            'arrive_2031': round(f * s[2031]), 'non_followers_2031': round((1 - f) * s[2031]),
                            'per_grade_2031': round(s[2031] / (6 if lev == 'K-5' else 3), 1)})
    return out
A, O2 = moves('scenario_A'), moves('option2')
o2keys = {m['strand'] for m in O2}
def tot(ms, key):
    return sum(m[key] for m in ms)
NECESSARY = {'Atkinson|Spanish': 'Lent would be 274 (program-only, below 360) if the strand stayed home',
             'Scott|Spanish': 'Rigler would be 321 (program-only, below 360) if the strand stayed home'}
for m in O2:
    if m['strand'] in NECESSARY:
        m['necessary_because'] = NECESSARY[m['strand']]
res = {'scenario_A': A, 'option2': O2, 'necessary_moves_kept': [m for m in O2 if m['strand'] in NECESSARY],
       'avoided_by_option2': [m for m in A if m['strand'] not in o2keys],
       'summary': {}}
for nm, ms in (('scenario_A', A), ('option2', O2), ('avoided_by_option2', res['avoided_by_option2']),
               ('necessary_moves_kept', res['necessary_moves_kept'])):
    res['summary'][nm] = {k: tot(ms, k) for k in ('n_2025_26', 'n_2031_32', 'arrive_2031', 'non_followers_2031')}
recon = [m for m in A if m['strand'] in ('Sitton|Spanish', 'Atkinson|Spanish', 'Scott|Spanish', 'MLK Jr|Mandarin')]
res['reconstruction_731'] = {'strands': [m['strand'] for m in recon], 'n_2025_26': tot(recon, 'n_2025_26'),
                             'n_2031_32': tot(recon, 'n_2031_32'), 'arrive_2031': tot(recon, 'arrive_2031'),
                             'non_followers_2031': tot(recon, 'non_followers_2031'),
                             'note': 'our reconstruction: the four K-5 strands Scenario A moves out of buildings that stay open, other than Clark, sum to 731 in 2025-26 (PSU Table 5.5). The kit has no written source for "731".'}
od = sys.argv[1] if len(sys.argv) > 1 else os.path.join(C.SOLVER, 'out_v2', 'option2.staging')
os.makedirs(od, exist_ok=True)
json.dump(res, open(os.path.join(od, 'dli_moves.json'), 'w'), indent=1)
print('| Strand | Level | From → to (A) | 2025-26 | 2031-32 | per grade 2031-32 | Implied arrival share | Arrive 2031-32 | Stay/home 2031-32 | Option 2 |')
print('|---|---|---|---|---|---|---|---|---|---|')
for m in A:
    o = next((x for x in O2 if x['strand'] == m['strand']), None)
    print(f"| {m['strand']} | {m['level']} | {m['from']} → {m['to']}{'' if m['sending_building_stays_open_at_level'] else ' (building closes or changes grades)'} | {m['n_2025_26']} | {m['n_2031_32']} | {m['per_grade_2031']} | {m['arrival_share_2031_implied']:.2f} | {m['arrive_2031']} | {m['non_followers_2031']} | {'moves' if o else '**stays**'} |")
print(json.dumps(res['summary'], indent=1)); print(json.dumps(res['reconstruction_731'], indent=1))
