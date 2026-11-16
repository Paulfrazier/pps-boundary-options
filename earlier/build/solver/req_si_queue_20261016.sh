#!/bin/zsh
# 2026-10-16 parent request: Sabin/Irvington (design: build/research/request_sabin_irvington.md). Runs after the James John queue. Lands in .staging.
cd "$(dirname "$0")"; PY=../../.venv/bin/python
until grep -q "== DONE" out_v2/_req_jj_queue_20261016.log 2>/dev/null; do sleep 30; done
for n in req_irv_open req_sabin_open req_irv_for_bc; do
  echo "== $n $(date +%T)"
  $PY -u solve.py configs/v2/$n.json > out_v2/_run_$n.log 2>&1 || echo "$n FAILED"
  [ -f out_v2/$n.staging/scorecard.json ] && $PY smooth_v2.py $n --src staging 2>&1 | tail -3
done
echo "== DONE $(date +%T)"
