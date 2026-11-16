"""Marginal cost of the next middle->high feeder fix (Paul 2026-10-12 ~15:15: "report the marginal cost of fixing
the next crossing; rough is fine").  Penalty sensitivity: re-solve ONLY 6-8 from <run>'s K-5 (staging or final)
with ms_split raised, and compare one-HS count and 6-8 walk.
  python feeder_margin.py setup <run> <ms_split> [--src staging|final]   -> configs/v2/_diag_fm<ms>_<run>.json + staging seed
  python feeder_margin.py straddle <run> [--src ...]                       -> K-5 zones crossing A's HS lines (kids)
Run the diag with:  python solve.py configs/v2/_diag_fm<ms>_<run>.json --from 6-8   (writes its own .staging; scratch)"""
import json, os, shutil, sys
import numpy as np, pandas as pd
import common as C, metrics as MX

OUT = os.path.join(C.SOLVER, 'out_v2')


def src_dir(run, src):
    return os.path.join(OUT, run + ('.staging' if src == 'staging' else ''))


def setup(run, ms, src):
    c = json.load(open(os.path.join(C.SOLVER, 'configs', 'v2', f'{run}.json')))
    name = f'_diag_fm{int(ms)}_{run}'
    c['name'] = name
    c['weights']['ms_split'] = float(ms)
    json.dump(c, open(os.path.join(C.SOLVER, 'configs', 'v2', f'{name}.json'), 'w'), indent=1)
    st = os.path.join(OUT, name + '.staging')
    os.makedirs(st, exist_ok=True)
    for f in ('checkpoint.json', 'assign_K-5.parquet'):
        shutil.copy2(os.path.join(src_dir(run, src), f), os.path.join(st, f))
    print(name)


def straddle(run, src):
    cfg = C.load_config(os.path.join(C.SOLVER, 'configs', 'v2', f'{run}.json'))
    k5 = pd.read_parquet(os.path.join(src_dir(run, src), 'assign_K-5.parquet'))['school'].values
    hs = C.blocks()['A_hs'].values
    K = MX.level_kids(cfg, '2031')['9-12']
    df = pd.DataFrame({'es': k5, 'hs': hs, 'k': K}).groupby(['es', 'hs'])['k'].sum().reset_index()
    out = {}
    for es, g in df.groupby('es'):
        g = g[g['k'] >= 5].sort_values('k', ascending=False)
        if len(g) > 1:
            out[es] = {r.hs: round(float(r.k), 1) for r in g.itertuples()}
    print(json.dumps(out, indent=1))
    print('K-5 zones crossing an A high-school line (>=5 high-school-age kids on the minority side):', len(out),
          '; minority-side high-school-age kids:', round(sum(sum(list(v.values())[1:]) for v in out.values())))
    return out


if __name__ == '__main__':
    a = sys.argv[1:]
    src = 'final'
    if '--src' in a:
        i = a.index('--src'); src = a[i + 1]; del a[i:i + 2]
    if a[0] == 'setup':
        setup(a[1], float(a[2]), src)
    else:
        straddle(a[1], src)
