#!/usr/bin/env python3
"""Walk bands for the NE area, for pages/tubman.html: every middle schooler (and elementary kid) living in today's six NE
middle-school zones, by walk to the school each plan assigns them. Prints JSON; tubman_data.py runs it in its own process
(the solver's `common` module shares a name with build/map's).

Usage: tubman_bands.py RUN [RUN ...]
"""
import json, os, sys
import numpy as np
import pandas as pd

KIT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(KIT, 'build', 'solver'))
import common as C, metrics as MX  # noqa: E402

NE_MS = ['Tubman', 'Vernon', 'Beaumont', 'Ockley Green', 'Roseway Heights', 'Faubion']
CUTS = {'6-8': [1.0, 1.5, 2.0], 'K-5': [0.5, 1.0, 1.5]}   # 1.5 mi = middle-school bus line, 1 mi = elementary

cfg = C.load_config(os.path.join(C.SOLVER, 'configs', 'v2', 'status_quo.json'))
K = MX.level_kids(cfg)
M = C.dist_matrix('walk')
idx = C.school_routing_index()


def asg(run, lev):
    return pd.read_parquet(os.path.join(C.SOLVER, 'out_v2', run, f'assign_{lev}.parquet')).sort_values('idx')['school'].values


area = np.isin(asg('status_quo', '6-8'), NE_MS)
out = {}
for run in sys.argv[1:]:
    out[run] = {}
    for lev, cuts in CUTS.items():
        a = asg(run, lev)
        w = np.array([M[i, idx[s]] if s in idx else np.nan for i, s in enumerate(a)])
        m = area & ~np.isnan(w) & (K[lev] > 0)
        k, ww = K[lev][m], w[m]
        edges = [0.0] + cuts + [np.inf]
        out[run][lev] = {'cuts': cuts, 'kids': round(float(k.sum())), 'avg_walk_mi': round(float((k * ww).sum() / k.sum()), 2),
                         'pct': [round(float(k[(ww > edges[j]) & (ww <= edges[j + 1])].sum() / k.sum() * 100), 1) for j in range(len(edges) - 1)]}
print(json.dumps(out))
