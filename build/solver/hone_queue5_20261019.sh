#!/bin/zsh
# 2026-10-19 Paul: "can anything be done about the walks?" (James John plan). Beach Spanish to Sitton instead of Chavez.
cd "$(dirname "$0")"; PY=../../.venv/bin/python
until grep -q "== DONE" out_v2/_hone_queue4_20261019.log 2>/dev/null; do sleep 30; done
for n in req_jj_beach_sitton; do
  echo "== $n $(date +%T)"
  caffeinate -i $PY -u solve.py configs/v2/$n.json > out_v2/_run_$n.log 2>&1 || echo "$n FAILED"
  [ -f out_v2/$n.staging/scorecard.json ] && $PY smooth_v2.py $n --src staging 2>&1 | tail -3
done
echo "== DONE $(date +%T)"
