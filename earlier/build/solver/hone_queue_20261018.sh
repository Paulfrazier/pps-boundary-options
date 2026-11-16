#!/bin/zsh
# 2026-10-18 Paul: "use all you know to hone these plans" + "lets try not sending them over bridge". After the spacing runs:
# Skyline to Lincoln on the live and nested plans (no re-solve), then honed Rebalanced PPS A. One solver at a time. Staging only.
cd "$(dirname "$0")"; PY=../../.venv/bin/python
until grep -q "== DONE" out_v2/_spacing_queue3_20261018.log 2>/dev/null; do sleep 30; done
for n in option2_ms460_sky option2_nested_sky option4_h; do
  echo "== $n $(date +%T)"
  caffeinate -i $PY -u solve.py configs/v2/$n.json > out_v2/_run_$n.log 2>&1 || echo "$n FAILED"
  case $n in *_sky) ;; *) [ -f out_v2/$n.staging/scorecard.json ] && $PY smooth_v2.py $n --src staging 2>&1 | tail -3;; esac
done
echo "== DONE $(date +%T)"
