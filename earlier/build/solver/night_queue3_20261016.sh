#!/bin/zsh
cd "$(dirname "$0")"; PY=../../.venv/bin/python
( for n in nesths_300 nesths_600; do $PY -u solve.py configs/v2/$n.json > out_v2/_run_$n.log 2>&1 || echo "$n FAILED"; done ) &
echo "== nest3_k5 $(date +%T)"; $PY -u solve.py configs/v2/nest3_k5.json > out_v2/_run_nest3_k5.log 2>&1 || echo "nest3_k5 FAILED"
wait
echo "== nest3_425 $(date +%T)"; [ -f out_v2/nest3_k5.staging/scorecard.json ] && { $PY -u solve.py configs/v2/nest3_425.json > out_v2/_run_nest3_425.log 2>&1 || echo "nest3_425 FAILED"; }
[ -f out_v2/nest3_425.staging/scorecard.json ] && $PY smooth_v2.py nest3_425 --src staging 2>&1 | tail -3
echo "== DONE $(date +%T)"
