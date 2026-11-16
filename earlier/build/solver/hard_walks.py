"""Hard walks per run (2026-10-19, Paul: lines that follow busy streets): 2031-32 kids inside the bus line whose
shortest walk crosses a busy street with no signal (build/safe_routes/FOR_MODELS.md).  Reads staging folders too.
  python hard_walks.py run [run ...]        (a run name, or name.staging)"""
import json, os, sys
import numpy as np
import pandas as pd
import common as C
import metrics as MX
sys.path.insert(0, os.path.join(C.SOLVER, '..', 'safe_routes'))
import crossings as X

OUT = os.path.join(C.SOLVER, 'out_v2')


def score(run):
    base = run.replace('.staging', '')
    cfg = json.load(open(os.path.join(C.SOLVER, 'configs', 'v2', base + '.json')))
    K = MX.level_kids(cfg, '2031')
    r = {'run': run}
    for lev in ('K-5', '6-8'):
        a = pd.read_parquet(os.path.join(OUT, run, f'assign_{lev}.parquet'))['school'].values
        names = sorted(set(a) - {None})
        ix = {n: k for k, n in enumerate(names)}
        col = np.array([ix.get(s, -1) for s in a])
        ok = col >= 0
        W, H = C.dist('walk', names), X.hard(names)
        rows = np.arange(len(a))[ok]
        d, h = W[rows, col[ok]], np.nan_to_num(H[rows, col[ok]], nan=0.0)
        k = K[lev][ok]
        walk = d <= MX.BUS[lev]
        r[f'{lev} walkers'] = round(float(k[walk].sum()))
        r[f'{lev} hard'] = round(float(k[walk & (h > 0)].sum()))
        r[f'{lev} over bus'] = round(float(k[~walk].sum()))
        r[f'{lev} walk mi'] = round(float((k * d).sum() / k.sum()), 3)
    return r


if __name__ == '__main__':
    print(pd.DataFrame([score(x) for x in sys.argv[1:]]).to_string(index=False))
