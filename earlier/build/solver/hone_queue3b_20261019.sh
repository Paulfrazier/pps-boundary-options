#!/bin/zsh
# 2026-10-19 replaces hone_queue3 (Paul: "bump capstone to the end"): finishes the running Sellwood solve, then the
# softer-nesting pair; cap6_h3_ms moved to hone_queue7. Writes "== DONE" to hone_queue3's log so hone_queue4 starts.
cd "$(dirname "$0")"; PY=../../.venv/bin/python; L3=out_v2/_hone_queue3_20261019.log
while pgrep -f "solve.py configs/v2/option2_ms460_sellwood.json" >/dev/null; do sleep 30; done
[ -f out_v2/option2_ms460_sellwood.staging/scorecard.json ] && $PY smooth_v2.py option2_ms460_sellwood --src staging 2>&1 | tail -3 >> $L3
for n in option2_hsn1 option2_hsn3; do
  echo "== $n $(date +%T)" >> $L3
  caffeinate -i $PY -u solve.py configs/v2/$n.json > out_v2/_run_$n.log 2>&1 || echo "$n FAILED" >> $L3
  [ -f out_v2/$n.staging/scorecard.json ] && $PY smooth_v2.py $n --src staging 2>&1 | tail -3 >> $L3
done
echo "== DONE $(date +%T) (via hone_queue3b; cap6_h3_ms moved to hone_queue7)" >> $L3
