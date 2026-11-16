#!/bin/zsh
# 2026-10-14 (Paul: "try 3 and 5. and do new lines + 460"): clean the new K-5 lines once, then build the three middle
# variants on them, then line cleanup + QA.  All output in .staging; not for the site until Paul says.
cd "$(dirname "$0")"
PY=../../.venv/bin/python
echo "== nl_tidy solve $(date +%T)"
$PY -u solve.py configs/v2/nl_tidy.json > out_v2/_run_nl_tidy.log 2>&1 || { echo "nl_tidy FAILED"; exit 1; }
echo "== nl_tidy smooth $(date +%T)"
$PY smooth_v2.py nl_tidy --src staging 2>&1 | tail -6
for n in nl_460 nl3_425 nl5_460; do
  sed -i '' 's/"workers": 8/"workers": 2/' configs/v2/$n.json
  ( $PY -u solve.py configs/v2/$n.json > out_v2/_run_$n.log 2>&1 || echo "$n FAILED" ) &
done
wait
for n in nl_460 nl3_425 nl5_460; do
  echo "== $n smooth $(date +%T)"
  $PY smooth_v2.py $n --src staging 2>&1 | tail -6
  echo "== $n lines_qa"
  $PY lines_qa.py option2 --staging $n 2>&1 | tail -5
done
echo "== DONE $(date +%T)"
