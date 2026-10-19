#!/bin/zsh
# 2026-10-16 (Paul: "try a model run, of the 500 middle school, if we lower the floor to 415"). Lands in .staging; nothing promoted without Paul.
cd "$(dirname "$0")"; PY=../../.venv/bin/python
echo "== option2_ms415 $(date +%T)"
$PY -u solve.py configs/v2/option2_ms415.json > out_v2/_run_option2_ms415.log 2>&1 || { echo "ms415 FAILED"; exit 1; }
$PY smooth_v2.py option2_ms415 --src staging 2>&1 | tail -3
echo "== DONE $(date +%T)"
