#!/bin/zsh
# 2026-10-18 after hone_queue: capstone with the hard no-worse-than-PPS-A spacing rule + tiers (3 kid-miles). Staging only.
cd "$(dirname "$0")"
until grep -q "== DONE" out_v2/_hone_queue_20261018.log 2>/dev/null; do sleep 30; done
echo "== cap6_h3 $(date +%T)"; WORKERS=8 ./capstone6.sh cap6_h3 415 option2_ms460_long 1.25 3 || echo "cap6_h3 FAILED"
echo "== DONE $(date +%T)"
