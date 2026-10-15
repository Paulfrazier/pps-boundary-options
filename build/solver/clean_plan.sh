#!/bin/zsh
# Overnight line cleanup for one live plan (Paul 2026-10-12 ~23:00).  Usage: clean_plan.sh <target> <k5_weights_json> [k5_from_run]
#  1. candidate config <target>_tidy: the target's config, K-5 weights overridden, K-5 warm-started from the target,
#     6-8 kept block for block from the target (fixed_run), 9-12 as the target -> only K-5 is re-solved
#     (or, with k5_from_run, K-5 copied from that finished run's staging instead of solved)
#  2. smooth_v2.py: rule-preserving pocket swaps + one-block notch cleanup
#  3. promote_clean.py: swaps it in only if every check passes
set -u
T=$1; W=$2; FROM=${3:-}
cd "$(dirname "$0")"
PY=../../.venv/bin/python
C=${T}_tidy
LOCK=out_v2/.manifest.lock
lock() { until mkdir $LOCK 2>/dev/null; do sleep 2; done; }
unlock() { rmdir $LOCK 2>/dev/null; }
lock
$PY - "$T" "$C" "$W" "$FROM" <<'EOF'
import json, sys
t, c, w, frm = sys.argv[1:5]
cfg = json.load(open(f'configs/v2/{t}.json'))
cfg['name'] = c
cfg['label'] = cfg.get('label', t) + f' [line cleanup candidate: K-5 weights {w}]'
if frm:
    cfg['levels']['K-5']['fixed_run'] = frm
else:
    cfg['levels']['K-5']['weights'] = json.loads(w)
    cfg['levels']['K-5']['warm_start'] = {'run': t}
cfg['levels']['6-8']['fixed_run'] = t
cfg['solver']['phase2_warm'] = True
cfg['solver']['workers'] = 3
json.dump(cfg, open(f'configs/v2/{c}.json', 'w'), indent=1)
m = json.load(open('out_v2/MANIFEST.json'))
m['runs'][c] = {'status': 'running', 'notes': f'overnight line-cleanup candidate for {t} (K-5 {w}; 6-8 kept from {t}); '
                'swapped in via promote_clean.py only if every check passes. Not for the site.'}
json.dump(m, open('out_v2/MANIFEST.json', 'w'), indent=1)
EOF
unlock
$PY solve.py configs/v2/$C.json > out_v2/_run_$C.log 2>&1 || { echo "$C: solve failed"; exit 1; }
$PY smooth_v2.py $C --src staging 2>&1 | grep -o '"pockets_fixed": \[[^]]*\]\|K-5: walk.*\|6-8: walk.*\|at target all.*'
$PY lines_qa.py $T --staging $C 2>&1 | tail -4
lock
$PY promote_clean.py $C $T --teeth-ratio ${TR:-0.85} 2>&1 | tail -6
unlock
