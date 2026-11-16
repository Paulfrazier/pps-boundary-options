#!/bin/zsh
# 2026-10-16 (Paul: "queue up a capstone rerun with trying to keep HS as close to today as possible, and the new middle school floors").
# After the Sabin/Irvington queue. 8 workers. Staging only.
cd "$(dirname "$0")"
until grep -q "== DONE" out_v2/_req_si_queue_20261016.log 2>/dev/null; do sleep 30; done
echo "== cap4_415 $(date +%T)"
WORKERS=8 ./capstone4.sh cap4_415 415 option2_ms460_long || echo "cap4_415 FAILED"
echo "== DONE $(date +%T)"
