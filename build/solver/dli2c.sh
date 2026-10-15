#!/bin/zsh
cd "$(dirname "$0")"; PY=../../.venv/bin/python
$PY -u solve.py configs/v2/option2_dli2_crisp.json > out_v2/_run_option2_dli2_crisp.log 2>&1 || { echo FAILED; exit 1; }
$PY smooth_v2.py option2_dli2_crisp --src staging 2>&1 | tail -3
$PY lines_qa.py option2 --staging option2_dli2_crisp 2>&1 | tail -2
echo "== DONE $(date +%T)"
