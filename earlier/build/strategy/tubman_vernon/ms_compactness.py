"""How "Tetris-like" the NE middle-school zones are under each plan. Run from build/solver:
    PYTHONPATH=.:../map/crisp ../../.venv/bin/python ../strategy/tubman_vernon/ms_compactness.py [run ...]
For each NE middle school (zones made of the blocks' Voronoi cells, the same cells the site map's lines start from):
  polsby_popper   4*pi*area / perimeter^2 of the zone (1 = a circle; low = stretched or ragged)
  pieces          separate land pieces of the zone
  school_offset   distance from the building to the zone's kid-weighted centre, as a share of the zone's kid-weighted
                  average radius (0 = building at the centre of its kids; near 1 or more = building at the edge)
  past_closer     middle-school kids whose walk to another open NE middle school is >0.25 mi shorter than to their own
  avg_walk_mi     kid-weighted walk to the assigned middle school
Writes site_data/ms_compactness.json (appends/replaces the runs given) and site_data/ne_ms_totals.json: per run, all
middle-school kids assigned to the NE middle schools above, their kid-weighted average walk and how many live over
1.5 mi (the state no-bus distance for 6-8). Default runs: status_quo, scenario_A,
planD_updated, irv_sabin_15th_grant, plus any tubman_at_vernon* run that has finished (staging or promoted).
"""
import os, sys, json, glob
import numpy as np, pandas as pd, shapely
from shapely.ops import unary_union
import importlib.util
import common as C, metrics as MX
# build/map/crisp/geo.py imports build/map/common.py, which shares its module name with build/solver/common.py
_map = os.path.join(C.SOLVER, '..', 'map')
_spec = importlib.util.spec_from_file_location('common', os.path.join(_map, 'common.py'))
_mc = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_mc)
sys.modules['common'] = _mc
sys.path.insert(0, os.path.join(_map, 'crisp'))
import geo as G
sys.modules['common'] = C

HERE = os.path.dirname(os.path.abspath(__file__))
OUTF = os.path.join(HERE, 'site_data', 'ms_compactness.json')
NE_MS = ['Tubman', 'Vernon', 'Beaumont', 'Ockley Green', 'Roseway Heights', 'Faubion']
O2 = os.path.join(C.SOLVER, 'out_v2')


def run_dir(r):
    for d in (os.path.join(O2, r), os.path.join(O2, r + '.staging')):
        if os.path.exists(os.path.join(d, 'assign_6-8.parquet')):
            return d


runs = sys.argv[1:] or (['status_quo', 'scenario_A', 'planD_updated', 'irv_sabin_15th_grant']
                        + sorted({os.path.basename(p).replace('.staging', '')
                                  for p in glob.glob(os.path.join(O2, 'tubman_at_vernon*')) if run_dir(os.path.basename(p).replace('.staging', ''))}))
cells = np.array(G.voronoi_cells(), dtype=object)
xy = G.block_xy()
K = MX.level_kids(C.load_config(os.path.join(C.SOLVER, 'configs', 'v2', 'status_quo.json')))['6-8']
sb = C.school_block()
res = json.load(open(OUTF)) if os.path.exists(OUTF) else {}
TOTF = os.path.join(HERE, 'site_data', 'ne_ms_totals.json')
tot = json.load(open(TOTF)) if os.path.exists(TOTF) else {}
for r in runs:
    d = run_dir(r)
    if not d:
        print('skip', r); continue
    a = pd.read_parquet(os.path.join(d, 'assign_6-8.parquet')).sort_values('idx')['school'].astype(object).values
    open_ne = [s for s in NE_MS if (a == s).any()]
    W = C.dist('walk', open_ne)
    own = np.array([W[i, open_ne.index(a[i])] if a[i] in open_ne else np.nan for i in range(len(a))])
    out = {}
    for s in open_ne:
        m = a == s; k = K[m]
        z = unary_union(list(cells[m]))
        pp = 4 * np.pi * z.area / z.length ** 2
        npieces = len(getattr(z, 'geoms', [z]))
        c = (xy[m] * k[:, None]).sum(0) / k.sum()
        rad = (np.hypot(*(xy[m] - c).T) * k).sum() / k.sum()
        bi = sb[s] if isinstance(sb, dict) else sb.get(s)
        off = float(np.hypot(*(xy[bi] - c)) / rad) if bi is not None else None
        best = np.nanmin(W[m], 1)
        out[s] = {'kids': round(float(k.sum())), 'polsby_popper': round(float(pp), 3), 'pieces': npieces,
                  'school_offset': None if off is None else round(off, 2),
                  'past_closer': round(float(k[own[m] - best > 0.25].sum())),
                  'avg_walk_mi': round(float((k * own[m]).sum() / k.sum()), 2)}
    res[r] = out
    ne = np.isin(a, open_ne); kn = K[ne]; wn = own[ne]
    tot[r] = {'schools': open_ne, 'kids': round(float(kn.sum())), 'avg_walk_mi': round(float((kn * wn).sum() / kn.sum()), 2),
              'kids_over_1_5mi': round(float(kn[wn > 1.5].sum())),
              'past_closer': sum(v['past_closer'] for v in out.values())}
    print(r, {s: (v['polsby_popper'], v['school_offset'], v['past_closer'], v['avg_walk_mi']) for s, v in out.items()})
json.dump(res, open(OUTF, 'w'), indent=1)
json.dump(tot, open(TOTF, 'w'), indent=1)
