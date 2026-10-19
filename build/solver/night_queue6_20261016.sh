#!/bin/zsh
cd "$(dirname "$0")"; PY=../../.venv/bin/python
$PY -u solve.py configs/v2/nest3_tidy12.json > out_v2/_run_nest3_tidy12.log 2>&1 || echo "FAILED"
[ -f out_v2/nest3_tidy12.staging/scorecard.json ] && $PY smooth_v2.py nest3_tidy12 --src staging 2>&1 | tail -3
echo "== DONE $(date +%T)"
