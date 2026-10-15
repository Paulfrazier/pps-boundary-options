#!/bin/zsh
cd "$(dirname "$0")"; PY=../../.venv/bin/python
$PY -u solve.py configs/v2/nlC.json > out_v2/_run_nlC.log 2>&1 || { echo "nlC FAILED"; exit 1; }
$PY smooth_v2.py nlC --src staging 2>&1 | tail -3
for n in nlC_460 nlC3_425 nlC5_460; do ( $PY -u solve.py configs/v2/$n.json > out_v2/_run_$n.log 2>&1 || echo "$n FAILED" ) & done
wait
for n in nlC_460 nlC3_425 nlC5_460; do echo "== $n"; $PY smooth_v2.py $n --src staging 2>&1 | tail -3; $PY lines_qa.py option2 --staging $n 2>&1 | tail -2; done
echo "== DONE $(date +%T)"
