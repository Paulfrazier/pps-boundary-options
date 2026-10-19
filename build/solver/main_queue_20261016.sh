#!/bin/zsh
# 2026-10-16 combined queue (replaces req_si_queue / capstone4_queue): after the James John runs ->
# 415 reruns (phase-2 keep fix) -> Sabin/Irvington -> capstone4. One solver at a time. Staging only.
cd "$(dirname "$0")"; PY=../../.venv/bin/python
until grep -q "== DONE" out_v2/_req_jj_queue_20261016.log 2>/dev/null; do sleep 30; done
for n in option2_ms415 option3a_ms415 req_irv_open req_sabin_open req_irv_for_bc; do
  echo "== $n $(date +%T)"
  $PY -u solve.py configs/v2/$n.json > out_v2/_run_$n.log 2>&1 || echo "$n FAILED"
  [ -f out_v2/$n.staging/scorecard.json ] && $PY smooth_v2.py $n --src staging 2>&1 | tail -3
done
echo "== cap4_415 $(date +%T)"
WORKERS=8 ./capstone4.sh cap4_415 415 option2_ms460_long || echo "cap4_415 FAILED"
echo "== DONE $(date +%T)"
