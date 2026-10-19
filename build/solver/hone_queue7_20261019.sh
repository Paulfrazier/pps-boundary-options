#!/bin/zsh
# 2026-10-19 Paul: capstone last. cap6_h3_ms (capstone with the hard spacing rule, middle re-solved long). Staging only.
cd "$(dirname "$0")"; PY=../../.venv/bin/python
until grep -q "== DONE" out_v2/_hone_queue6_20261019.log 2>/dev/null; do sleep 30; done
for n in cap6_h3_ms; do
  echo "== $n $(date +%T)"
  caffeinate -i $PY -u solve.py configs/v2/$n.json > out_v2/_run_$n.log 2>&1 || echo "$n FAILED"
  [ -f out_v2/$n.staging/scorecard.json ] && $PY smooth_v2.py $n --src staging 2>&1 | tail -3
done
echo "== DONE $(date +%T)"
