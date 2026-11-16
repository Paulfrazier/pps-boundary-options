#!/bin/zsh
cd "$(dirname "$0")"; PY=../../.venv/bin/python
for n in nlC_500 nlC_500s6; do ( $PY -u solve.py configs/v2/$n.json > out_v2/_run_$n.log 2>&1 || echo "$n FAILED" ) & done
wait
for n in nlC_500 nlC_500s6; do echo "== $n"; $PY smooth_v2.py $n --src staging 2>&1 | tail -3; done
echo "== DONE $(date +%T)"
