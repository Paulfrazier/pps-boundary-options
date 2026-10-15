#!/bin/zsh
# Bonus-time follow-up (Paul 2026-10-13: "could i tell it, it gets bonus time?" -> "lets do both").
# Usage: bonus_run.sh <run>
#  Waits for <run>'s solve to finish, then solves <run>_bonus: same config, middle lines started from <run>'s
#  result (warm start + split-phase hint), so the search continues instead of starting over.  Keeps the Mac awake
#  while it runs.  The solve log records wall seconds and work units per round (det=...), used to calibrate
#  solver.work_per_sec (time limits that a laptop sleep does not use up).
set -u
R=$1; B=${R}_bonus
cd "$(dirname "$0")"
PY=../../.venv/bin/python
LOCK=out_v2/.manifest.lock
while pgrep -f "[s]olve.py configs/v2/$R.json" >/dev/null; do sleep 20; done
[ -f out_v2/$R.staging/assign_6-8.parquet ] || { echo "$R: no staging result"; exit 1; }
cp out_v2/$R.staging/assign_6-8.parquet out_v2/_hints/${R}_6-8.parquet
until mkdir $LOCK 2>/dev/null; do sleep 2; done
$PY - "$R" "$B" <<'EOF'
import json, sys
r, b = sys.argv[1:3]
c = json.load(open(f'configs/v2/{r}.json'))
c['name'] = b
c['label'] = c['label'] + f' [bonus time: continues from {r}]'
c['levels']['6-8']['warm_start'] = {'run': r, 'staging': True}
c['solver']['phase2_hint_file'] = f'out_v2/_hints/{r}_6-8.parquet'
c['solver']['hint_mode'] = 'repair'            # use the parent's plan as a real starting point
c['solver'].setdefault('work_per_sec', 0.4)     # sleep-proof time limits (work units; rough calibration 2026-10-13)
json.dump(c, open(f'configs/v2/{b}.json', 'w'), indent=1)
m = json.load(open('out_v2/MANIFEST.json'))
m['runs'][b] = {'status': 'running', 'notes': f'TEST bonus-time follow-up of {r}: same rules, middle lines continue from its result. '
                'Keep whichever of the two walks less. Not for the site until reviewed.'}
json.dump(m, open('out_v2/MANIFEST.json', 'w'), indent=1)
EOF
rmdir $LOCK
caffeinate -i $PY solve.py configs/v2/$B.json > out_v2/_run_$B.log 2>&1
echo "$B exit $?"
grep -n "det=\|at target in every" out_v2/_run_$B.log | tail -6
