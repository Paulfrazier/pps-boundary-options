#!/bin/zsh
# 2026-10-18 Paul: "a better plan that doesn't create a gap like that". Solver picks schools with a spacing cost
# (K-5 kids with no open school within 1.25 mi walking), moderate then strong. Middle minimum 415. Staging only.
cd "$(dirname "$0")"
echo "== cap5_w3 $(date +%T)"; WORKERS=8 ./capstone5.sh cap5_w3 415 option2_ms460_long 1.25 3 || echo "cap5_w3 FAILED"
echo "== cap5_w8 $(date +%T)"; WORKERS=8 ./capstone5.sh cap5_w8 415 option2_ms460_long 1.25 8 || echo "cap5_w8 FAILED"
echo "== DONE $(date +%T)"
