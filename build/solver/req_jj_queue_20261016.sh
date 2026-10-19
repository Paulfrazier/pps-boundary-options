#!/bin/zsh
# 2026-10-16 parent request: James John open, James John + Sitton Spanish stay. Runs after the 415 queue. Lands in .staging.
cd "$(dirname "$0")"; PY=../../.venv/bin/python
until grep -q "== DONE\|FAILED" out_v2/_ms415c_queue_20261016.log 2>/dev/null; do sleep 30; done
for n in req_jj_sitton req_jj_sitton_chz; do
  echo "== $n $(date +%T)"
  $PY -u solve.py configs/v2/$n.json > out_v2/_run_$n.log 2>&1 || echo "$n FAILED"
  [ -f out_v2/$n.staging/scorecard.json ] && $PY smooth_v2.py $n --src staging 2>&1 | tail -3
done
echo "== DONE $(date +%T)"
