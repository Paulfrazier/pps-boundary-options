#!/bin/zsh
# 2026-10-18 relaunch of spacing_queue2 after the 2026-10-18 20:06 reboot. Tiered spacing cost: per K-5 kid with no open school
# within 1.25 mi (w), 2 mi (2w), 3 mi (4w). Middle minimum 415. Staging only.
cd "$(dirname "$0")"
echo "== cap5_t3 $(date +%T)"; WORKERS=8 ./capstone5.sh cap5_t3 415 option2_ms460_long 1.25 3 || echo "cap5_t3 FAILED"
echo "== cap5_t6 $(date +%T)"; WORKERS=8 ./capstone5.sh cap5_t6 415 option2_ms460_long 1.25 6 || echo "cap5_t6 FAILED"
echo "== DONE $(date +%T)"
