"""(2026-10-27) Irvington line runs with the middle and high school feeds fixed: take a promoted Irvington-line run (its K-5
lines as they are) and set, for every block in today's Irvington area, 9-12 back to today's school (Grant), and 6-8 either
as the base run has it (Sabin side Tubman, Beverly Cleary side Beaumont: ms=model) or all at Tubman as today (ms=tubman).
Nothing else moves. Re-scored with metrics.write_plan (no solver).
    usage: irvline_feed.py <base run> <new run> <model|tubman> "<label>" """
import json, os, sys
import numpy as np, pandas as pd
import common as C, metrics as MX
base, run, ms, label = sys.argv[1:5]
assert ms in ('model', 'tubman')
CFG_DIR = os.path.join(C.SOLVER, 'configs', 'v2')
cfg_js = json.load(open(os.path.join(CFG_DIR, f'{base}.json')))
cfg_js['name'] = run
cfg_js['label'] = label
cfg_js['label_detail'] = cfg_js.get('label_detail', '') + (
    " Middle and high school for today's Irvington area: " +
    ('all of it stays at Tubman for 6-8, as today' if ms == 'tubman' else "6-8 as the base run (Sabin side Tubman, Beverly Cleary side Beaumont)") +
    ", and all of it stays at Grant for 9-12, as today.")
cfg_js['feed_note'] = f'built by irvline_feed.py from {base} (ms={ms}, Irvington-area 9-12 as today); not solved'
json.dump(cfg_js, open(os.path.join(CFG_DIR, f'{run}.json'), 'w'), indent=1)
cfg = C.load_config(os.path.join(CFG_DIR, f'{run}.json'))
rd = lambda d, lev: pd.read_parquet(os.path.join(C.SOLVER, 'out_v2', d, f'assign_{lev}.parquet')).sort_values('idx')['school'].values.copy()
plan = {lev: rd(base, lev) for lev in C.LEVELS}
sq9 = rd('status_quo', '9-12')
irv = np.where(C.blocks()['sq_es'].values == 'Irvington')[0]
ch = {'9-12': int((plan['9-12'][irv] != sq9[irv]).sum())}
plan['9-12'][irv] = sq9[irv]
if ms == 'tubman':
    ch['6-8'] = int((plan['6-8'][irv] != 'Tubman').sum())
    plan['6-8'][irv] = 'Tubman'
print(run, 'blocks changed', ch)
# blocks left cut off from their 6-8 / 9-12 building by the change (a pocket of another area that reached Beaumont or
# Jefferson through Irvington) join the neighbours' majority school
from collections import deque, Counter
NB = C.adjacency()[0]; roots = C.school_block(); orphans = []
for lev, schs in (('6-8', ('Beaumont', 'Tubman')), ('9-12', ('Grant', 'Jefferson'))):
    for sch in schs:
        idx = set(map(int, (plan[lev] == sch).nonzero()[0])); seen = {roots[sch]} & idx or {roots[sch]}; q = deque(seen)
        while q:
            i = q.popleft()
            for j in NB[i]:
                if j in idx and j not in seen:
                    seen.add(j); q.append(j)
        cut = sorted(idx - seen)
        while cut:
            left = []
            for i in cut:
                nb = Counter(plan[lev][j] for j in NB[i] if plan[lev][j] != sch)
                if nb: plan[lev][i] = nb.most_common(1)[0][0]; orphans.append((lev, i, sch, plan[lev][i]))
                else: left.append(i)
            if len(left) == len(cut): break
            cut = left
print('orphans fixed', len(orphans), Counter((o[0], o[2], o[3]) for o in orphans))
ch['orphans'] = len(orphans)
refs = MX.load_refs(CFG_DIR)
out = os.path.join(C.SOLVER, 'out_v2', f'{run}.staging')
MX.write_plan(out, cfg, plan, refs, extra={'note_feed': cfg_js['feed_note']})
with open(os.path.join(out, 'solve_log.txt'), 'w') as f:
    f.write(f'{run}: {cfg_js["feed_note"]}; blocks changed {ch}\n')
