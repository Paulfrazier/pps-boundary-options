#!/bin/zsh
# targeted high-school edits on the best plan (Paul: tweak some high school areas?). Staging only.
cd "$(dirname "$0")"; PY=../../.venv/bin/python
for n in hsfix_300 hsfix_600 hsfix_1000; do echo "== $n $(date +%T)"; $PY -u solve.py configs/v2/$n.json > out_v2/_run_$n.log 2>&1 || echo "$n FAILED"; done
echo "== DONE $(date +%T)"
