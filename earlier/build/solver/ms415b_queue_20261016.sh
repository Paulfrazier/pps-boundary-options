#!/bin/zsh
# 2026-10-16 (Paul: "do a focus option removed with floor of 415"): runs after option2_ms415. Lands in .staging.
cd "$(dirname "$0")"; PY=../../.venv/bin/python
until grep -q "== DONE\|FAILED" out_v2/_ms415_queue_20261016.log 2>/dev/null; do sleep 30; done
echo "== option3a_ms415 $(date +%T)"
$PY -u solve.py configs/v2/option3a_ms415.json > out_v2/_run_option3a_ms415.log 2>&1 || { echo "3a_ms415 FAILED"; exit 1; }
$PY smooth_v2.py option3a_ms415 --src staging 2>&1 | tail -3
echo "== DONE $(date +%T)"
