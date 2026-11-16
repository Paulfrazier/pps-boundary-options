#!/bin/zsh
# 2026-10-16: rerun option2_ms415 with phase2_always, after option3a_ms415 finishes. Lands in .staging.
cd "$(dirname "$0")"; PY=../../.venv/bin/python
until grep -q "== DONE\|FAILED" out_v2/_ms415b_queue_20261016.log 2>/dev/null; do sleep 30; done
echo "== option2_ms415 $(date +%T)"
$PY -u solve.py configs/v2/option2_ms415.json > out_v2/_run_option2_ms415.log 2>&1 || { echo "ms415 FAILED"; exit 1; }
$PY smooth_v2.py option2_ms415 --src staging 2>&1 | tail -3
echo "== DONE $(date +%T)"
