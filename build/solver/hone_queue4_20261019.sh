#!/bin/zsh
# 2026-10-19 Paul: fold the Skyline fix into the featured plan (option2_ms460) and find the best James John plan for its
# own page. After hone_queue3. One solver at a time. The James John runs stay in staging.
cd "$(dirname "$0")"; PY=../../.venv/bin/python; LOCK=out_v2/.manifest.lock
until grep -q "== DONE" out_v2/_hone_queue3_20261019.log 2>/dev/null; do sleep 30; done
echo "== option2_ms460 (Skyline fold-in) $(date +%T)"
caffeinate -i $PY -u solve.py configs/v2/option2_ms460.json > out_v2/_run_option2_ms460_skyfold.log 2>&1 || echo "option2_ms460 FAILED"
$PY report_v2.py tradeoffs option2_ms460 --staging 2>&1 | tail -2
until mkdir $LOCK 2>/dev/null; do sleep 2; done
$PY promote_v2.py option2_ms460 --note "2026-10-19 Skyline area to Lincoln (Paul); K-5/6-8 unchanged" 2>&1 | tail -4
rmdir $LOCK
$PY tradeoffs_matrix.py 2>&1 | tail -2; $PY public_manifest.py 2>&1 | tail -2; $PY public_tradeoffs.py 2>&1 | tail -3
for n in req_jj_chz_sky req_jj_chz_long req_jj_chz_nest415; do
  echo "== $n $(date +%T)"
  caffeinate -i $PY -u solve.py configs/v2/$n.json > out_v2/_run_$n.log 2>&1 || echo "$n FAILED"
  case $n in *_sky) ;; *) [ -f out_v2/$n.staging/scorecard.json ] && $PY smooth_v2.py $n --src staging 2>&1 | tail -3;; esac
done
echo "== DONE $(date +%T)"
