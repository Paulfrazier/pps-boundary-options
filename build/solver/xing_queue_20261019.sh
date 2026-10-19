#!/bin/zsh
# 2026-10-19 Paul: busy-street crossing cost (build/safe_routes/FOR_MODELS.md) on "Balanced middle schools".
# 0.25 first (matches the quarter-mile closer-school margin), then 0.5 and 0.1. Staging only, no promote.
# No smoothing: smooth_v2 doesn't know the crossing cost and could undo it.
cd "$(dirname "$0")"; PY=../../.venv/bin/python
until ! pgrep -f "solve.py" >/dev/null; do sleep 30; done
for n in option2_ms460_x25 option2_ms460_x50 option2_ms460_x10; do
  echo "== $n $(date +%T)"
  caffeinate -i $PY -u solve.py configs/v2/$n.json > out_v2/_run_$n.log 2>&1 || echo "$n FAILED"
  [ -f out_v2/$n.staging/scorecard.json ] && $PY hard_walks.py option2_ms460 $n.staging 2>&1 | grep -v Warn | tail -1
done
echo "== DONE $(date +%T)"
