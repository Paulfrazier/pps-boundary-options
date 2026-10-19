#!/bin/zsh
cd "$(dirname "$0")"; PY=../../.venv/bin/python
echo "== nest3_tidy $(date +%T)"; $PY -u solve.py configs/v2/nest3_tidy.json > out_v2/_run_nest3_tidy.log 2>&1 || echo "nest3_tidy FAILED"
[ -f out_v2/nest3_tidy.staging/scorecard.json ] && $PY smooth_v2.py nest3_tidy --src staging 2>&1 | tail -3
echo "== DONE $(date +%T)"
