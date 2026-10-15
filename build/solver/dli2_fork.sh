#!/bin/zsh
cd "$(dirname "$0")"; PY=../../.venv/bin/python
while pgrep -f nlC_queue.sh >/dev/null; do sleep 20; done
$PY -u solve.py configs/v2/option2_dli3.json > out_v2/_run_option2_dli3.log 2>&1 || { echo "FAILED"; exit 1; }
$PY smooth_v2.py option2_dli3 --src staging 2>&1 | tail -3
$PY lines_qa.py option2 --staging option2_dli3 2>&1 | tail -2
echo "== DONE $(date +%T)"
