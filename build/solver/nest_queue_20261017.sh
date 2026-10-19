#!/bin/zsh
# 2026-10-17 Paul: fewer elementary->high splits for the James John request. Hard nesting on PPS A high-school lines. Staging only.
cd "$(dirname "$0")"; PY=../../.venv/bin/python
for n in req_jj_sitton_nest; do
  echo "== $n $(date +%T)"
  $PY -u solve.py configs/v2/$n.json > out_v2/_run_$n.log 2>&1 || echo "$n FAILED"
  [ -f out_v2/$n.staging/scorecard.json ] && $PY smooth_v2.py $n --src staging 2>&1 | tail -3
done
echo "== DONE $(date +%T)"
