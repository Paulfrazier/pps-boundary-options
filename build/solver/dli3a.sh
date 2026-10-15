#!/bin/zsh
cd "$(dirname "$0")"; PY=../../.venv/bin/python
$PY -u solve.py configs/v2/option3a_dli.json > out_v2/_run_option3a_dli.log 2>&1 || { echo "FAILED"; exit 1; }
$PY smooth_v2.py option3a_dli --src staging 2>&1 | tail -3
$PY lines_qa.py option3a --staging option3a_dli 2>&1 | tail -2
echo "== DONE $(date +%T)"
