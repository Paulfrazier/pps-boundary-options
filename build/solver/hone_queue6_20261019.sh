#!/bin/zsh
# 2026-10-19 Paul: James John B, smaller North Portland schools for better lines. After hone_queue5. Staging only.
cd "$(dirname "$0")"; PY=../../.venv/bin/python
until grep -q "== DONE" out_v2/_hone_queue5_20261019.log 2>/dev/null; do sleep 30; done
for n in req_jj_b_small; do
  echo "== $n $(date +%T)"
  caffeinate -i $PY -u solve.py configs/v2/$n.json > out_v2/_run_$n.log 2>&1 || echo "$n FAILED"
  [ -f out_v2/$n.staging/scorecard.json ] && $PY smooth_v2.py $n --src staging 2>&1 | tail -3
done
echo "== DONE $(date +%T)"
