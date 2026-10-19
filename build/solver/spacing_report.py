"""(2026-10-18) Spacing report: K-5 kids far from the nearest open neighbourhood K-5 school (walking), per run,
and the areas of today's schools that PPS A closes.  usage: python spacing_report.py run [run ...]"""
import sys, pandas as pd, numpy as np, metrics as MX, common as C

def load(r):
    import os
    return r if os.path.exists(f'out_v2/{r}/schools.csv') else r + '.staging'

def main(runs):
    cfg = C.load_config('configs/v2/option2.json'); k = np.asarray(MX.level_kids(cfg)['K-5'], float)
    area = pd.read_parquet('out_v2/status_quo/assign_K-5.parquet')['school'].values
    opens = {r: set(pd.read_csv(f'out_v2/{load(r)}/schools.csv').query('`zoned_K-5`==True').school) for r in runs}
    names = sorted(set().union(*opens.values())); D = np.nan_to_num(C.dist('walk', names), nan=99.0)
    near = {r: D[:, [names.index(s) for s in o]].min(1) for r, o in opens.items()}
    print('| run | open K-5 | avg to nearest | >1 mi | >1.25 mi | >1.5 mi |\n|---|---:|---:|---:|---:|---:|')
    for r in runs:
        d = near[r]
        print(f'| {r} | {len(opens[r])} | {(k*d).sum()/k.sum():.2f} | {k[d>1].sum():.0f} | {k[d>1.25].sum():.0f} | {k[d>1.5].sum():.0f} |')
    closedA = sorted(opens.get('status_quo', set()) - opens.get('scenario_A', set()))
    print('\nAreas PPS A closes: average miles to the nearest open school (share over 1 mi); * = school open in that run')
    print('| area | kids | ' + ' | '.join(runs) + ' |\n|---|---:|' + '---:|' * len(runs))
    for a in closedA:
        m = area == a; w = k[m]
        cells = [f"{(w*near[r][m]).sum()/w.sum():.2f} ({w[near[r][m]>1].sum()/w.sum()*100:.0f}%){'*' if a in opens[r] else ''}" for r in runs]
        print(f'| {a} | {w.sum():.0f} | ' + ' | '.join(cells) + ' |')
    for r in runs:
        if r in ('status_quo', 'scenario_A'): continue
        A = opens.get('scenario_A', set())
        print(f'{r} vs PPS A: keeps open {sorted(opens[r]-A)}; closes {sorted(A-opens[r])}')

if __name__ == '__main__':
    main(sys.argv[1:])
