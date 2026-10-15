#!/bin/zsh
# Two-stage capstone (2026-10-13).  The one-stage capstone (every school optional, block level) ended an hour's search
# 100%+ from its bound and walked worse than option2.  Stage 1 picks schools and program hosts on ~700 tied pieces;
# stage 2 redraws block by block with that open set fixed, warm-started from stage 1.  No at-target bonus in either
# (with every open school required at target, the bonus only rewarded keeping more schools open).
set -u
cd "$(dirname "$0")"
PY=../../.venv/bin/python
LOCK=out_v2/.manifest.lock
lock() { until mkdir $LOCK 2>/dev/null; do sleep 2; done; }
unlock() { rmdir $LOCK 2>/dev/null; }
W=${WORKERS:-4}
lock
$PY - $W <<'PY'
import json, sys
w = int(sys.argv[1])
c = json.load(open('configs/v2/capstone.json'))
c['name'] = 'capstone_s1'
c['label'] = 'Capstone stage 1: schools and program hosts chosen on tied pieces (status-quo zone x block group x PPS A HS area)'
c['levels']['K-5']['coarse_ties'] = True
c['weights']['durable_school'] = 0.0
c['weights']['school_year_at_target'] = 0.0
c['solver'].update(time_first=2400, time_star=2400, max_rounds=1, time_round=600, workers=w, phase2_always=True)
json.dump(c, open('configs/v2/capstone_s1.json', 'w'), indent=1)
m = json.load(open('out_v2/MANIFEST.json'))
m['runs']['capstone_s1'] = {'status': 'running', 'notes': 'TEST capstone stage 1 (school choice on tied pieces). Feeds capstone_s2. Not for the site.'}
json.dump(m, open('out_v2/MANIFEST.json', 'w'), indent=1)
PY
unlock
caffeinate -i $PY solve.py configs/v2/capstone_s1.json > out_v2/_run_capstone_s1.log 2>&1 || { echo "s1 failed"; exit 1; }
echo "s1 done $(date)"
lock
$PY - $W <<'PY'
import json, sys, common as C
w = int(sys.argv[1])
c = json.load(open('configs/v2/capstone.json'))
sc = json.load(open('out_v2/capstone_s1.staging/scorecard.json'))
C.resolve_config(c, sc)                  # stage 1's open schools and program hosts, fixed
c['name'] = 'capstone_s2'
c['label'] = 'Capstone: schools and program hosts picked by the solver, lines redrawn for the shortest walks (stage 2)'
c['capstone_stage1'] = {'optional_schools': sc.get('optional_schools'), 'program_moves': sc.get('program_moves')}
c['weights']['durable_school'] = 0.0
c['weights']['school_year_at_target'] = 0.0
for lev in ('K-5', '6-8'):
    c['levels'][lev]['warm_start'] = {'run': 'capstone_s1', 'staging': True}
c['solver'].update(time_first=3600, time_star=3600, max_rounds=3, time_round=600, workers=w)
json.dump(c, open('configs/v2/capstone_s2.json', 'w'), indent=1)
m = json.load(open('out_v2/MANIFEST.json'))
m['runs']['capstone_s1']['status'] = 'done'
m['runs']['capstone_s2'] = {'status': 'running', 'notes': 'TEST capstone stage 2: block-level redraw on stage 1 open set. Not for the site until reviewed.'}
json.dump(m, open('out_v2/MANIFEST.json', 'w'), indent=1)
PY
unlock
caffeinate -i $PY solve.py configs/v2/capstone_s2.json > out_v2/_run_capstone_s2.log 2>&1 || { echo "s2 failed"; exit 1; }
echo "s2 done $(date)"
$PY smooth_v2.py capstone_s2 --src staging > out_v2/_smooth_capstone_s2.log 2>&1; tail -4 out_v2/_smooth_capstone_s2.log
$PY lines_qa.py scenario_A option2 --staging capstone_s2 2>&1 | tail -8
