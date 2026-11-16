#!/bin/zsh
# Same closures, better lines 2.0 sweep (Paul 2026-10-14): three middle-school split caps in parallel, 2 workers each.
cd "$(dirname "$0")"
PY=../../.venv/bin/python
for n in 0 3 6; do
  caffeinate -i $PY solve.py configs/v2/lead2_s$n.json > out_v2/_run_lead2_s$n.log 2>&1 &
done
wait
for n in 0 3 6; do echo "lead2_s$n"; grep -n "at target in every\|splits=" out_v2/_run_lead2_s$n.log | tail -3; done
