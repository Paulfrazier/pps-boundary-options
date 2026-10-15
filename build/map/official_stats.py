"""Metrics for official PPS A/B (and the old approximation, for the before/after report). Writes work/official.json."""
import json, collections, sys
import pandas as pd
from common import *
from model_port import *

DLI_FOLLOW = '--literal' not in sys.argv   # default: whole-school DLI areas (Lent, Rigler) stay with their program; --literal = PPS's drawn areas as-is
blocks = pd.read_csv(os.path.join(KIT, 'build', 'data', 'blocks.csv'), usecols=['idx', 'A_es', 'B_es'])
def official(s):
    a = list(blocks[s + '_es'])
    if DLI_FOLLOW: a = [BL[i]['a'] if BL[i]['a'] in ('Lent', 'Rigler') else x for i, x in enumerate(a)]
    return a

def det(s, asg, minn=50):
    rec = SC[s]['rec']; op = open_of(s); G = collections.defaultdict(lambda: dict(s=0, st=0, d=0, o1=0, best=collections.Counter()))
    for b, a in zip(BL, asg):
        if b['a'] not in rec: continue
        g = G[(b['a'], a)]; w = b['s']; d = wd(b, a)
        g['s'] += w; g['st'] += w * b['st'][a]; g['d'] += w * d
        if d > 1: g['o1'] += w
        g['best'][best_walk(b, op)[0]] += w
    rows = []
    for (area, a), g in G.items():
        if g['s'] < minn: continue
        bn, bw = g['best'].most_common(1)[0]
        rows.append([area, a, round(g['s']), '%.2f' % (g['st'] / g['s']), '%.2f' % (g['d'] / g['s']), round(g['o1']), bn, round(bw / g['s'] * 100)])
    rows.sort(key=lambda r: -r[2]); return rows

if __name__ == '__main__':
    t = load_page()
    DET = json.loads(grab(t, 'const DET=', ';\nconst PPSP='))
    old = det('A', pps_assign_old('A'))
    print('DET old reproduces:', [r[:3] for r in old] == [r[:3] for r in DET], old[:2] == DET[:2])
    for r, q in zip(old, DET):
        if r != q: print(' diff', r, q); break
    res = {'asg': {}, 'metrics': {}, 'det': {}, 'bands': {}, 'before': {}, 'pfrom': {}}
    for s in 'AB':
        asg = official(s); ob = pps_assign_old(s)
        for tag, a in (('new', asg), ('old', ob)):
            m = wmetrics(s, a)
            res['metrics'][s + tag] = {k: (v if not isinstance(v, dict) else None) for k, v in m.items()}
            if tag == 'new':
                res['sizes_' + s] = {n: round(v) for n, v in m['size'].items()}
                res['share_' + s] = {n: round(q * 100) for n, q in m['share'].items()}
        res['asg'][s] = asg
        res['bands'][s] = {k: bands(asg, k) for k in 'SH'}
        if s == 'A': res['det'] = det('A', asg)
        # students by today's area for each school
        fr = collections.defaultdict(lambda: collections.Counter())
        for b, a in zip(BL, asg): fr[a][b['a']] += b['s']
        res['pfrom'][s] = {n: ', '.join('%s %d' % ('King' if k == 'MLK Jr' else k, round(v)) for k, v in c.most_common() if v >= 15) for n, c in fr.items()}
    json.dump(res, open(os.path.join(WORK, 'official%s.json' % ('' if DLI_FOLLOW else '_literal')), 'w'), separators=(',', ':'))
    for k, v in res['metrics'].items(): print(k, {x: v[x] for x in ('avg', 'o1', 'o15', 'past', 'full', 'n', 'moved', 'D', 'within')})
