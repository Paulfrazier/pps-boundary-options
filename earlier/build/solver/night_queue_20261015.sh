#!/bin/zsh
# overnight (Paul: "try and do better with middle to high splits and elem to high ... go all night"). Staging only.
cd "$(dirname "$0")"; PY=../../.venv/bin/python
while pgrep -f cores_queue5_20261015.sh >/dev/null; do sleep 20; done
echo "== nest_k5 $(date +%T)"; $PY -u solve.py configs/v2/nest_k5.json > out_v2/_run_nest_k5.log 2>&1 || { echo "nest_k5 FAILED"; exit 1; }
for n in nest_460 nest_425; do ( $PY -u solve.py configs/v2/$n.json > out_v2/_run_$n.log 2>&1 || echo "$n FAILED" ) & done; wait
echo "== DONE $(date +%T)"
