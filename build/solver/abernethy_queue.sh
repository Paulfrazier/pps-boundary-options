#!/bin/zsh
# 2026-10-14 (Paul: "ya"): Sunnyside + Abernethy south of I-84 for Close 2 and the new-lines candidates. Staging only.
cd "$(dirname "$0")"; PY=../../.venv/bin/python
( $PY -u solve.py configs/v2/option3a_crisp.json > out_v2/_run_option3a_crisp.log 2>&1 && $PY smooth_v2.py option3a_crisp --src staging 2>&1 | tail -4 && $PY lines_qa.py option3a --staging option3a_crisp 2>&1 | tail -2 || echo "option3a_crisp FAILED" ) &
$PY -u solve.py configs/v2/nlA.json > out_v2/_run_nlA.log 2>&1 || { echo "nlA FAILED"; wait; exit 1; }
$PY smooth_v2.py nlA --src staging 2>&1 | tail -3
for n in nlA_460 nlA3_425 nlA5_460; do ( $PY -u solve.py configs/v2/$n.json > out_v2/_run_$n.log 2>&1 || echo "$n FAILED" ) & done
wait
for n in nlA_460 nlA3_425 nlA5_460; do echo "== $n"; $PY smooth_v2.py $n --src staging 2>&1 | tail -3; $PY lines_qa.py option2 --staging $n 2>&1 | tail -2; done
echo "== DONE $(date +%T)"
