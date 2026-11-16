#!/bin/zsh
cd "$(dirname "$0")"; PY=../../.venv/bin/python
echo "== nest2_k5 $(date +%T)"; $PY -u solve.py configs/v2/nest2_k5.json > out_v2/_run_nest2_k5.log 2>&1 || { echo "nest2_k5 FAILED"; exit 1; }
echo "== nest2_425 $(date +%T)"; $PY -u solve.py configs/v2/nest2_425.json > out_v2/_run_nest2_425.log 2>&1 || echo "nest2_425 FAILED"
echo "== smooth $(date +%T)"; $PY smooth_v2.py nest2_425 --src staging 2>&1 | tail -3
echo "== smooth nest_425"; $PY smooth_v2.py nest_425 --src staging 2>&1 | tail -3
echo "== DONE $(date +%T)"
