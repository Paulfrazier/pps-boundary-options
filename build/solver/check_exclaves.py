"""Exclave check (TRACKS.md write rule): every school's blocks must form one connected piece on the solver's block
adjacency (common.adjacency()[0]).  python check_exclaves.py <run_dir> [...]  -> prints JSON, exit 1 if any piece
with kids > 0.5 is cut off from the school's main piece (the piece holding its building block, else the largest)."""
import json, os, sys
from collections import deque
import numpy as np, pandas as pd
import common as C, metrics as MX

def check_pieces(asg, NB, roots, b, kids):
    seen = np.zeros(len(asg), bool)
    bys = {}
    for i in range(len(asg)):
        if seen[i]:
            continue
        s = asg[i]; q = deque([i]); seen[i] = True; comp = []
        while q:
            k = q.popleft(); comp.append(k)
            for j in NB[k]:
                if not seen[j] and asg[j] == s:
                    seen[j] = True; q.append(j)
        bys.setdefault(s, []).append(comp)
    bad = []
    for s, comps in bys.items():
        if len(comps) < 2:
            continue
        r = roots.get(s)
        main = next((ci for ci, cm in enumerate(comps) if r in cm), None)
        if main is None:
            main = max(range(len(comps)), key=lambda ci: kids[comps[ci]].sum())
        for ci, cm in enumerate(comps):
            if ci == main:
                continue
            kk = float(kids[cm].sum())
            bad.append({'school': s, 'blocks': len(cm), 'kids_2031': round(kk, 1),
                        'lon': round(float(b['x'].values[cm].mean()), 4), 'lat': round(float(b['y'].values[cm].mean()), 4)})
    return bad

def check(run_dir, cfg=None):
    NB = C.adjacency()[0]
    roots = C.school_block()
    b = C.blocks()
    out = {}
    if cfg is None:
        name = os.path.basename(run_dir.rstrip('/')).replace('.staging', '').replace('_msfeed_off', '')
        p = os.path.join(C.SOLVER, 'configs', 'v2', f'{name}.json')
        cfg = C.load_config(p) if os.path.exists(p) else None
    K = MX.level_kids(cfg, '2031') if cfg else None
    for lev in C.LEVELS:
        f = os.path.join(run_dir, f'assign_{lev}.parquet')
        if not os.path.exists(f):
            continue
        asg = pd.read_parquet(f)['school'].values
        fa = cfg['levels'][lev].get('fixed_assign') if cfg else None
        if fa:
            ref = b[fa].values.astype(object).copy()
            ras = cfg['levels'][lev].get('fixed_reassign', [])
            for ra in ras:                    # whole PPS areas moved to another school (solve.py fixed_reassign)
                # (2026-10-22) rules may key off the run's own K-5 lines ("by_plan") or another run ("by_run")
                if 'by_plan' in ra:
                    vals = pd.read_parquet(os.path.join(run_dir, f"assign_{ra['by_plan']}.parquet")).sort_values('idx')['school'].values
                elif 'by_run' in ra:
                    vals = pd.read_parquet(os.path.join(C.SOLVER, 'out_v2', ra['by_run']['run'], f"assign_{ra['by_run']['level']}.parquet")).sort_values('idx')['school'].values
                else:
                    vals = b[ra['by']].values
                ref[np.isin(vals, ra['area'] if isinstance(ra['area'], list) else [ra['area']])] = ra['to']
            if (ref == asg).all():
                if not ras:
                    out[lev] = 'fixed to PPS column %s (PPS traced lines; pieces there are PPS\'s, not checked)' % fa
                    continue
                pps = {(x['school'], x['blocks']) for x in check_pieces(b[fa].values, NB, roots, b, K[lev] if K is not None else np.ones(len(asg)))}
                out[lev] = [x for x in check_pieces(asg, NB, roots, b, K[lev] if K is not None else np.ones(len(asg)))
                            if (x['school'], x['blocks']) not in pps]   # only pieces the reassignment made
                continue
        out[lev] = check_pieces(asg, NB, roots, b, K[lev] if K is not None else np.ones(len(asg)))
    return out

if __name__ == '__main__':
    rc = 0
    for d in sys.argv[1:]:
        r = check(d)
        print(d, json.dumps(r))
        if any(x['kids_2031'] > 0.5 for v in r.values() if isinstance(v, list) for x in v):
            rc = 1
    sys.exit(rc)
