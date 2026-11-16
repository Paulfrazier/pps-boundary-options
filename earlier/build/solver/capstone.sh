#!/bin/zsh
# Capstone pipeline (Paul 2026-10-13: "prep a capstone run ... you get to pick the schools ... best overall outcome").
# Waits for every other solve (and bonus watcher) to finish so it gets all cores, then:
#  1. solve configs/v2/capstone.json (solver picks open schools; long searches; Mac kept awake)
#  2. smooth_v2.py: rule-preserving pocket + notch cleanup on the result
#  3. lines_qa.py vs PPS A and the lead plan
#  4. bonus_run.sh: a follow-up solve continuing from the result
set -u
cd "$(dirname "$0")"
PY=../../.venv/bin/python
LOCK=out_v2/.manifest.lock
while pgrep -f "[s]olve.py configs/v2/" >/dev/null || pgrep -f "[b]onus_run.sh" >/dev/null; do sleep 30; done
until mkdir $LOCK 2>/dev/null; do sleep 2; done
"$PY" - capstone <<'PYEOF'
import json
m = json.load(open('out_v2/MANIFEST.json'))
m['runs']['capstone'] = {'status': 'running', 'notes': 'CAPSTONE (Paul 2026-10-13): solver picks open K-5 and middle schools; every lesson so far. Not for the site until reviewed.'}
json.dump(m, open('out_v2/MANIFEST.json', 'w'), indent=1)
PYEOF
rmdir $LOCK
caffeinate -i $PY solve.py configs/v2/capstone.json > out_v2/_run_capstone.log 2>&1 || { echo "capstone: solve failed"; tail -20 out_v2/_run_capstone.log; exit 1; }
$PY smooth_v2.py capstone --src staging > out_v2/_smooth_capstone.log 2>&1; tail -5 out_v2/_smooth_capstone.log
$PY lines_qa.py scenario_A option2 --staging capstone 2>&1 | tail -6
grep -n "optional\|kept_open\|at target in every" out_v2/_run_capstone.log | tail -8
./bonus_run.sh capstone
