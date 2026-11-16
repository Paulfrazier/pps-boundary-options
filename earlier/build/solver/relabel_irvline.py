"""(2026-10-26) Irvington line runs as relabels of irv_sabin_15th: same plan everywhere, except the Irvington-area
blocks follow the given line file (configs/v2/areas/<file>.csv, labels irv_to_sabin / irv_to_bc). Moved blocks take the
6-8 and 9-12 school irv_sabin_15th gives the Irvington-area blocks of their new K-5 school, so the two runs differ only
by the line. Re-scored with metrics.write_plan (no solver).  usage: relabel_irvline.py <run> <areas csv>"""
import json, os, sys
import pandas as pd
import common as C, metrics as MX
run, area = sys.argv[1], sys.argv[2]
base = 'irv_sabin_15th'
cfg = C.load_config(os.path.join(C.SOLVER, 'configs', 'v2', f'{run}.json'))
plan = {lev: pd.read_parquet(os.path.join(C.SOLVER, 'out_v2', base, f'assign_{lev}.parquet')).sort_values('idx')['school'].values.copy()
        for lev in C.LEVELS}
lab = pd.read_csv(os.path.join(C.SOLVER, area)).set_index('idx')['label']
to = {'irv_to_sabin': 'Sabin', 'irv_to_bc': 'Beverly Cleary'}
irv = lab.index.values
follow = {}
for lev in ('6-8', '9-12'):
    d = pd.DataFrame({'k5': plan['K-5'][irv], 's': plan[lev][irv]})
    follow[lev] = d.groupby('k5')['s'].agg(lambda x: x.mode().iloc[0]).to_dict()
moved = 0
for i, l in lab.items():
    k = to[l]
    if plan['K-5'][i] != k:
        moved += 1
        plan['K-5'][i] = k
        for lev in ('6-8', '9-12'):
            plan[lev][i] = follow[lev][k]
print(run, 'blocks relabeled', moved, 'follow', follow)
# blocks of Sabin or Beverly Cleary left cut off from their school by the new line (e.g. Buckman-area corner blocks
# that irv_sabin_15th sent to Sabin through its southwest corner) join the neighbours' majority school
from collections import deque, Counter
NB = C.adjacency()[0]; roots = C.school_block(); orphans = []
for sch in ('Sabin', 'Beverly Cleary'):
    idx = set(map(int, (plan['K-5'] == sch).nonzero()[0])); seen = {roots[sch]}; q = deque(seen)
    while q:
        i = q.popleft()
        for j in NB[i]:
            if j in idx and j not in seen:
                seen.add(j); q.append(j)
    for i in sorted(idx - seen):
        k = Counter(plan['K-5'][j] for j in NB[i] if plan['K-5'][j] != sch).most_common(1)[0][0]
        plan['K-5'][i] = k
        for lev in ('6-8', '9-12'):
            plan[lev][i] = follow[lev].get(k, plan[lev][i])
        orphans.append((i, sch, k))
print('orphans fixed', orphans)
refs = MX.load_refs(os.path.join(C.SOLVER, 'configs', 'v2'))
out = os.path.join(C.SOLVER, 'out_v2', f'{run}.staging')
MX.write_plan(out, cfg, plan, refs, extra={'note_relabel': f'relabel of {base}: Irvington-area line from {area}; not solved'})
with open(os.path.join(out, 'solve_log.txt'), 'w') as f:
    f.write(f'{run}: relabel of {base} (not solved); Irvington-area blocks by {area}; {moved} blocks moved; '
            f'6-8/9-12 follow {base}\'s Irvington-area pattern {follow}; cut-off blocks joined neighbours: {orphans}\n')
