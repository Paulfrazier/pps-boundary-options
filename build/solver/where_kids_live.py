"""Where PPS students live, per block and level (2031-32 basis): build/data/v2/where_kids_live_2031.parquet.

For maps only. The scorecard basis (metrics.level_kids) is right for scoring but is not a residence surface: it
holds neighborhood-program kids only, and Rigler-area K-5 blocks keep 2% of their kids because whole-school DLI
students are counted at the program. Shading it shows holes where immersion students live.

residence = neighborhood kids on blocks (status_quo basis, with the Rigler-area Scott students put back on Rigler
blocks, as the plan configs do) + every DLI/focus/alt program's students at their estimated homes
(focus_dli_homes_lentobs.parquet: observed PPS home mix), each split by its grade mix and scaled to 2031-32 by its own PSU series if it has one,
else by the level's district factor. Solver results and scorecards do not read this file.
Run from the kit root: .venv/bin/python build/solver/where_kids_live.py
"""
import copy, json, os, re, sys
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import common as C, v2 as V, metrics as M

KIT = os.path.abspath(os.path.join(HERE, '..', '..'))
OUT = os.path.join(KIT, 'build', 'data', 'v2', 'where_kids_live_2031.parquet')
GR = {'K-5': ['K', 1, 2, 3, 4, 5], '6-8': [6, 7, 8], '9-12': [9, 10, 11, 12]}
COL = {'K-5': 'k5', '6-8': 'm68', '9-12': 'h912'}


def series_scale(prog, lev, district):
    """2031/2025 for a focus_dli.csv program at a level, from v2.program_series; district factor if no series."""
    m = re.match(r'DLI (\w+) @ ([^(]+?)(?: \(.*\))?$', prog)
    if m:
        lang, host = m.group(1), m.group(2).split(' (')[0]
        for key in (f'{host}|{lang}', f'{host}|{lang} {lev}', f'{host}|{lang} K-5' if lev == 'K-5' else ''):
            if key in C.PROGRAMS:
                try:
                    s = V.program_series(key)
                    if s[2025] > 0:
                        return s[2031] / s[2025], key
                except Exception:
                    pass
    return district[lev], None


def build():
    cfg = C.load_config(os.path.join(HERE, 'configs', 'v2', 'status_quo.json'))
    cfg_l = copy.deepcopy(cfg)
    rn = json.load(open(os.path.join(HERE, 'configs', 'v2', 'dli_home3_rh.json')))['v2']['rigler_nondli']
    cfg_l['v2']['rigler_nondli'] = {**rn, 'baseline_hold': False}
    nb = {k: np.asarray(v, float) for k, v in M.level_kids(cfg_l, '2031').items()}
    b = C.blocks()
    homes = pd.read_parquet(os.path.join(C.DATA, 'focus_dli_homes_lentobs.parquet'))   # Lent, Rigler from PPS's observed home mix
    fd = pd.read_csv(os.path.join(C.DATA, 'focus_dli.csv')).set_index('program')
    k31 = C.kids('2031'); district = {}
    for lev in GR:
        a = {'K-5': b.k5, '6-8': b.m68, '9-12': b.h912}[lev].values.astype(float)
        keep = ~b.es_cur.isin(C.LR_AREAS).values if lev == 'K-5' else np.ones(len(b), bool)
        district[lev] = k31[lev][keep].sum() / a[keep].sum()
    prog = {lev: np.zeros(len(b)) for lev in GR}; log = []
    for p, row in fd.iterrows():
        h = homes[p].values.astype(float)
        total = sum(row[f'est_g_{g}'] for gs in GR.values() for g in gs)
        for lev, gs in GR.items():
            sh = sum(row[f'est_g_{g}'] for g in gs) / max(total, 1e-9)
            if sh <= 0:
                continue
            sc, key = series_scale(p, lev, district)
            prog[lev] += h * sh * sc
            log.append((p, lev, round(h.sum() * sh), round(sc, 3), key or 'district factor'))
    out = pd.DataFrame({'idx': b['idx'], 'GEOID': b['GEOID']})
    for lev, c in COL.items():
        out[c + '_nbhd'] = nb[lev].round(4); out[c + '_program'] = prog[lev].round(4)
        out[c] = (nb[lev] + prog[lev]).round(4)
    return out, pd.DataFrame(log, columns=['program', 'level', 'kids_2025_26', 'scale_2031', 'scale_from'])


if __name__ == '__main__':
    out, log = build()
    out.to_parquet(OUT, index=False)
    print(log.to_string()); print({c: round(out[c].sum()) for c in out.columns if c not in ('idx', 'GEOID')})
