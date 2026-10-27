"""(2026-10-27) Boise-Eliot / Faubion swap on a Tubman-at-Vernon run, middle school only (no solver): take a finished
Tubman-at-Vernon run (its K-5 and 9-12 lines as they are) and re-set 6-8 for two elementary zones:
  - Boise-Eliot/Humboldt's zone -> Ockley Green (about 1.66 mi vs 1.95 to the Vernon building)
  - Faubion's zone: its main neighborhood (the piece holding the Faubion building) -> the Tubman middle school in the
    Vernon building (about 1.0 mi vs 2.7 to Ockley Green); the Bybee Lake shelter piece -> Astor, as Plan D says
    ("The Bybee Lake Shelter school area would move from Faubion to Astor"); any other detached piece -> Ockley Green
Re-scored with metrics.write_plan.
    usage: build_tubvern_swap.py <base run> <new run> "<label>" """
import json, os, sys
from collections import deque, Counter
import numpy as np, pandas as pd
import common as C, metrics as MX

base, run, label = sys.argv[1:4]
CFG_DIR = os.path.join(C.SOLVER, 'configs', 'v2')
O2 = os.path.join(C.SOLVER, 'out_v2')
bdir = next(d for d in (os.path.join(O2, base), os.path.join(O2, base + '.staging')) if os.path.exists(os.path.join(d, 'assign_6-8.parquet')))
cfg_js = json.load(open(os.path.join(CFG_DIR, f'{base}.json')))
cfg_js['name'] = run
cfg_js['label'] = label
cfg_js['label_detail'] = cfg_js.get('label_detail', '') + (
    " Middle school swap: Boise-Eliot/Humboldt goes to Ockley Green; Faubion's main neighborhood goes to the Tubman "
    "middle school in the Vernon building, and the Bybee Lake shelter area goes to Astor, as Plan D says.")
cfg_js['feed_note'] = f'built by build_tubvern_swap.py from {os.path.basename(bdir)}; 6-8 re-set for Boise-Eliot/Humboldt and Faubion; not solved'
json.dump(cfg_js, open(os.path.join(CFG_DIR, f'{run}.json'), 'w'), indent=1)
cfg = C.load_config(os.path.join(CFG_DIR, f'{run}.json'))
plan = {lev: pd.read_parquet(os.path.join(bdir, f'assign_{lev}.parquet')).sort_values('idx')['school'].values.astype(object).copy()
        for lev in C.LEVELS}
b = C.blocks(); NB = C.adjacency()[0]; roots = C.school_block()
k5, ms = plan['K-5'], plan['6-8']
assert 'Vernon' in set(ms) and 'Tubman' not in set(ms), 'base is not a Tubman-at-Vernon run'
before = ms.copy()

ms[k5 == 'Boise-Eliot/Humboldt'] = 'Ockley Green'
# Faubion's zone, block by block: the Bybee Lake shelter area -> Astor (Plan D); the rest to whichever of the Vernon
# building and Ockley Green is the shorter walk (its main neighborhood is ~1.0 mi from Vernon vs ~2.7 to Ockley Green;
# the far north blocks are nearer Ockley Green). The zone is one connected piece on the block adjacency, so the split
# is by walk, not by piece.
fzi = np.where(k5 == 'Faubion')[0]
W = C.dist('walk', ['Vernon', 'Ockley Green'])
lon = b['x'].values
bybee = fzi[lon[fzi] < -122.73]          # Smith and Bybee Lakes, the shelter's area
rest = fzi[lon[fzi] >= -122.73]
ms[bybee] = 'Astor'
ms[rest] = np.where(W[rest, 0] <= W[rest, 1], 'Vernon', 'Ockley Green')
K68 = MX.level_kids(cfg)['6-8']
pieces = {t: {'blocks': int((ms[fzi] == t).sum()), 'kids_2031': round(float(K68[fzi][ms[fzi] == t].sum()), 1)}
          for t in ('Vernon', 'Ockley Green', 'Astor')}
print('Faubion pieces:', pieces)

# cut-off 6-8 pieces join their neighbours' majority school (as irvline_feed.py)
orphans = []
for sch in ('Vernon', 'Ockley Green', 'Astor', 'Beaumont'):
    idx = set(map(int, (ms == sch).nonzero()[0])); st = {roots[sch]} & idx or {roots[sch]}; q = deque(st)
    while q:
        i = q.popleft()
        for j in NB[i]:
            if j in idx and j not in st:
                st.add(j); q.append(j)
    cut = sorted(idx - st)
    if sch == 'Astor':
        cut = [i for i in cut if not (k5[i] == 'Faubion' and lon[i] < -122.73)]   # Plan D's own detached piece
    while cut:
        left = []
        for i in cut:
            nb = Counter(ms[j] for j in NB[i] if ms[j] != sch)
            if nb: ms[i] = nb.most_common(1)[0][0]; orphans.append((i, sch, ms[i]))
            else: left.append(i)
        if len(left) == len(cut):
            break
        cut = left
ch = int((ms != before).sum())
print(run, '6-8 blocks changed', ch, '; orphans fixed', len(orphans), Counter((o[1], o[2]) for o in orphans))
refs = MX.load_refs(CFG_DIR)
out = os.path.join(O2, f'{run}.staging')
MX.write_plan(out, cfg, plan, refs, extra={'note_feed': cfg_js['feed_note']})
with open(os.path.join(out, 'solve_log.txt'), 'w') as f:
    f.write(f'{run}: {cfg_js["feed_note"]}; 6-8 blocks changed {ch}; Faubion pieces {pieces}; orphans {len(orphans)}\n')
json.dump({'schools_out_of_range_2031_32': [], 'solver_slack': f'not solved: {cfg_js["feed_note"]}',
           'feeder_splits_used': "as the base, except Faubion's zone splits by piece (main to Vernon, Bybee Lake to Astor)"},
          open(os.path.join(out, 'infeasibility.json'), 'w'), indent=1)
sc = pd.read_csv(os.path.join(out, 'schools.csv')).drop_duplicates('school').set_index('school')
print(sc.loc[[s for s in ('Vernon', 'Ockley Green', 'Beaumont', 'Roseway Heights', 'Astor') if s in sc.index], ['total', 'capacity', 'floor']])
