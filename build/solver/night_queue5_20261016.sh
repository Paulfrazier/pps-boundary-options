#!/bin/zsh
cd "$(dirname "$0")"; PY=../../.venv/bin/python
for n in nest3t_425 nest3t_460w; do ( $PY -u solve.py configs/v2/$n.json > out_v2/_run_$n.log 2>&1 || echo "$n FAILED"; [ -f out_v2/$n.staging/scorecard.json ] && $PY smooth_v2.py $n --src staging > out_v2/_smooth_$n.log 2>&1 ) & done; wait
echo "== DONE $(date +%T)"
