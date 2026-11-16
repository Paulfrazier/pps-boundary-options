#!/bin/zsh
# capstone5.sh = capstone3.sh plus a spacing cost (2026-10-18, Paul: "a better plan that doesn't create a gap like that"):
# usage capstone5.sh <name> <ms_floor> <ws68_run> <miles> <kid_miles_per_kid> (tiers: that cost within <miles>, 2x more beyond 2 mi, 4x more beyond 3 mi). Original header:
# Capstone re-run (2026-10-14, Paul: "with our updated constraints ... re run or tune the capstone"). Usage: capstone3.sh <name> <ms_floor> <ws68_run>
# Changes vs capstone_s1/s2: program hosts fixed at the lead plan's (no program_choice -> immersion moves = option2's 1,226,
# never more than PPS A's 1,567; Paul's DLI rule), Sunnyside kept south of I-84 (same_side), K-5 warm start from the new
# elementary lines (hsK_460, tidied), middle minimum <ms_floor>.  Two stages as capstone2.sh.  Staging only.
set -u
cd "$(dirname "$0")"
PY=../../.venv/bin/python
N=$1; FL=$2; WS=$3; CM=$4; CW=$5; W=${WORKERS:-4}
LOCK=out_v2/.manifest.lock
lock() { until mkdir $LOCK 2>/dev/null; do sleep 2; done; }
unlock() { rmdir $LOCK 2>/dev/null; }
lock
$PY - $N $FL $WS $W $CM $CW <<'PY'
import json, sys
n, fl, ws, w = sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4])
cm, cw = float(sys.argv[5]), float(sys.argv[6])
c = json.load(open('configs/v2/capstone.json'))
c.pop('program_choice', None)
c['floors']['6-8'] = fl
c['levels']['K-5']['same_side'] = ['Sunnyside']
c['levels']['K-5']['warm_start'] = {'run': 'hsK_460', 'staging': True}
c['levels']['6-8']['warm_start'] = {'run': ws, 'staging': ws != 'option2'}
c['levels']['K-5']['coverage'] = {'tiers': [[cm, cw], [2.0, 2 * cw], [3.0, 4 * cw]], 'mode': 'walk'}  # tiers: farther gaps cost more
c['name'] = n + '_s1'
c['label'] = (f'Capstone with spacing stage 1 (2026-10-18): cost per K-5 kid with no open school within {cm} mi ({cw} kid-miles); solver picks schools on tied pieces; program hosts fixed as the lead '
              f'plan (DLI rule); Sunnyside south of I-84; middle minimum {fl}')
c['levels']['K-5']['coarse_ties'] = True
c['weights']['durable_school'] = 0.0
c['weights']['school_year_at_target'] = 0.0
c['solver'].update(time_first=1800, time_star=1800, max_rounds=1, time_round=600, workers=w, phase2_always=True)
json.dump(c, open(f'configs/v2/{n}_s1.json', 'w'), indent=1)
m = json.load(open('out_v2/MANIFEST.json'))
m['runs'][n + '_s1'] = {'status': 'running', 'notes': f'TEST capstone5 spacing stage 1 (Paul 2026-10-18: no big gaps), {cm} mi / {cw}, middle min {fl}. Feeds {n}_s2. Not for the site.'}
json.dump(m, open('out_v2/MANIFEST.json', 'w'), indent=1)
PY
unlock
caffeinate -i $PY -u solve.py configs/v2/${N}_s1.json > out_v2/_run_${N}_s1.log 2>&1 || { echo "$N s1 failed"; exit 1; }
echo "$N s1 done $(date +%T)"
lock
$PY - $N $W <<'PY'
import json, sys, common as C
n, w = sys.argv[1], int(sys.argv[2])
c = json.load(open(f'configs/v2/{n}_s1.json'))
sc = json.load(open(f'out_v2/{n}_s1.staging/scorecard.json'))
C.resolve_config(c, sc)
c['name'] = n + '_s2'
c['label'] = c['label'].replace('stage 1', 'stage 2').replace('solver picks schools on tied pieces', 'stage 1 open set fixed, lines redrawn block by block')
c['capstone_stage1'] = {'optional_schools': sc.get('optional_schools')}
c['levels']['K-5'].pop('coarse_ties', None)
for lev in ('K-5', '6-8'):
    c['levels'][lev]['warm_start'] = {'run': n + '_s1', 'staging': True}
c['solver'].update(time_first=2400, time_star=1200, max_rounds=1, time_round=600, workers=w)
c['solver'].pop('phase2_always', None)
json.dump(c, open(f'configs/v2/{n}_s2.json', 'w'), indent=1)
m = json.load(open('out_v2/MANIFEST.json'))
m['runs'][n + '_s1']['status'] = 'done'
m['runs'][n + '_s2'] = {'status': 'running', 'notes': f'TEST capstone re-run stage 2 (Paul 2026-10-14). Not for the site.'}
json.dump(m, open('out_v2/MANIFEST.json', 'w'), indent=1)
PY
unlock
caffeinate -i $PY -u solve.py configs/v2/${N}_s2.json > out_v2/_run_${N}_s2.log 2>&1 || { echo "$N s2 failed"; exit 1; }
echo "$N s2 done $(date +%T)"
$PY smooth_v2.py ${N}_s2 --src staging 2>&1 | tail -4
$PY lines_qa.py option2 --staging ${N}_s2 2>&1 | tail -2
echo "$N DONE $(date +%T)"
