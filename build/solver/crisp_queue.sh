#!/bin/zsh
# 2026-10-14 (Paul: "crisp that up ... and also crisp up close 2 ... keep sunnyside on one side of i84").
# Runs after nl_pipeline.sh. Everything lands in .staging; nothing is promoted without Paul.
cd "$(dirname "$0")"
PY=../../.venv/bin/python
while pgrep -f nl_pipeline.sh >/dev/null; do sleep 15; done
echo "== option2_crisp solve $(date +%T)"
$PY -u solve.py configs/v2/option2_crisp.json > out_v2/_run_option2_crisp.log 2>&1 || echo "option2_crisp FAILED"
$PY smooth_v2.py option2_crisp --src staging 2>&1 | tail -6
$PY lines_qa.py option2 --staging option2_crisp 2>&1 | tail -5
echo "== option3a smooth (max-extra 0.25) $(date +%T)"
$PY smooth_v2.py option3a --max-extra 0.25 2>&1 | tail -6
$PY lines_qa.py option3a --staging option3a 2>&1 | tail -5
echo "== DONE $(date +%T)"
