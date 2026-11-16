#!/bin/zsh
# 2026-10-19 Paul: Sellwood smaller on the live plan; 1-3 elementary-to-high splits at lower cost (softer nesting sweep);
# capstone (hard spacing rule) middle re-solved long. All with Skyline to Lincoln. One solver at a time. Staging only.
cd "$(dirname "$0")"; PY=../../.venv/bin/python
for n in option2_ms460_sellwood option2_hsn1 option2_hsn3 cap6_h3_ms; do
  echo "== $n $(date +%T)"
  caffeinate -i $PY -u solve.py configs/v2/$n.json > out_v2/_run_$n.log 2>&1 || echo "$n FAILED"
  [ -f out_v2/$n.staging/scorecard.json ] && $PY smooth_v2.py $n --src staging 2>&1 | tail -3
done
echo "== DONE $(date +%T)"
