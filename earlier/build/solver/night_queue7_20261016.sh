#!/bin/zsh
cd "$(dirname "$0")"; PY=../../.venv/bin/python
echo "== nest3_dur35b $(date +%T)"; $PY -u solve.py configs/v2/nest3_dur35b.json > out_v2/_run_nest3_dur35b.log 2>&1 || { echo "dur35b FAILED"; exit 1; }
echo "== nest3_dur35m $(date +%T)"; $PY -u solve.py configs/v2/nest3_dur35m.json > out_v2/_run_nest3_dur35m.log 2>&1 || echo "dur35m FAILED"
[ -f out_v2/nest3_dur35m.staging/scorecard.json ] && $PY smooth_v2.py nest3_dur35m --src staging 2>&1 | tail -3
echo "== DONE $(date +%T)"
