#!/bin/zsh
# 2026-10-17 restart after the 2026-10-16 22:49 reboot killed req_jj_queue/main_queue. req_jj_sitton resumes at 6-8
# (its K-5 is saved in staging), then the rest of both queues in the same order. One solver at a time. Staging only.
cd "$(dirname "$0")"; PY=../../.venv/bin/python
echo "== req_jj_sitton (from 6-8) $(date +%T)"
$PY -u solve.py configs/v2/req_jj_sitton.json --from 6-8 >> out_v2/_run_req_jj_sitton.log 2>&1 || echo "req_jj_sitton FAILED"
[ -f out_v2/req_jj_sitton.staging/scorecard.json ] && $PY smooth_v2.py req_jj_sitton --src staging 2>&1 | tail -3
for n in req_jj_sitton_chz option2_ms415 option3a_ms415 req_irv_open req_sabin_open req_irv_for_bc; do
  echo "== $n $(date +%T)"
  $PY -u solve.py configs/v2/$n.json > out_v2/_run_$n.log 2>&1 || echo "$n FAILED"
  [ -f out_v2/$n.staging/scorecard.json ] && $PY smooth_v2.py $n --src staging 2>&1 | tail -3
done
echo "== cap4_415 $(date +%T)"
WORKERS=8 ./capstone4.sh cap4_415 415 option2_ms460_long || echo "cap4_415 FAILED"
echo "== DONE $(date +%T)"
