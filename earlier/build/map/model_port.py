"""Python port of cowork/model/core.js (wmetrics, bands, stats) so metrics can be recomputed for a new assignment.
Reads data/pps-map/pps-model.json and pps-race.csv (read only)."""
import os as _os  # _PPS_MAP_HDR (added by export: repo-relative paths)
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_PPS_MAP = _os.environ.get('PPS_MAP_DIR') or _os.path.join(_HERE, '../../data/pps-map')
import json, os
M = json.load(open(_os.path.join(_PPS_MAP, 'pps-model.json')))
BL, NB, NAMES, SC = M['BL'], M['NB'], M['NAMES'], M['SC']
R = {}
for l in open(_os.path.join(_PPS_MAP, 'pps-race.csv')).read().strip().split('\n'):
    c = l.split(','); R[c[0]] = [float(x) for x in c[1:]]
for b in BL:
    v = R.get(b['g'])
    if not v: b['kids'] = 0; b['p'] = None; continue
    kids = v[0] - v[5]; kw = v[2] - v[7]
    b['p'] = (1 - kw / kids) if kids > 0 else None
for _ in range(3):
    for i, b in enumerate(BL):
        if b['p'] is not None: continue
        xs = [BL[j]['p'] for j in NB[i] if BL[j]['p'] is not None]
        if xs: b['p'] = sum(xs) / len(xs)
for b in BL:
    if b['p'] is None: b['p'] = 0.35
Ptot = sum(b['s'] * b['p'] for b in BL) / sum(b['s'] for b in BL)
def wd(b, n): return b['w'][n] if n in b['w'] else b['st'][n] * 1.4
def open_of(s): return [n for n in NAMES if n not in SC[s]['rec']]
def best_walk(b, op):
    n = None; d = 1e9
    for o, v in b['w'].items():
        if o in op and v < d: d = v; n = o
    if n is None:
        for o in op:
            v = wd(b, o)
            if v < d: d = v; n = o
    return n, d
def pps_assign_old(s):
    rec = SC[s]['rec']; out = []
    for b in BL:
        if b['a'] in rec:
            out.append(min(rec[b['a']], key=lambda n: wd(b, n)))
        else: out.append(b['a'])
    return out
def wmetrics(s, asg, op=None):
    imm = SC[s]['imm']; op = op or open_of(s)
    size = {n: imm.get(n, 0) for n in op}; pc = {n: 0 for n in op}; st = {n: 0 for n in op}
    dist = stu = moved = past = o1 = o15 = 0
    for b, a in zip(BL, asg):
        if a not in size: size[a] = 0; pc[a] = 0; st[a] = 0
        d = wd(b, a); w = b['s']
        size[a] += w; st[a] += w; pc[a] += w * b['p']; dist += w * d; stu += w
        if a != b['a']: moved += w
        if d > 1: o1 += w
        if d > 1.5: o15 += w
        n, nd = best_walk(b, op)
        if a != n and d - nd >= 0.25: past += w
    share = {n: pc[n] / st[n] for n in op if st[n] > 0}
    POC = sum(pc[n] for n in share); WH = sum(st[n] - pc[n] for n in share)
    Dis = sum(abs(pc[n] / POC - (st[n] - pc[n]) / WH) for n in share) / 2
    sh = list(share.values()); within = sum(1 for x in sh if abs(x - Ptot) <= .15)
    v = list(size.values())
    return dict(size=size, share=share, avg=round(dist / stu, 3), moved=round(moved), past=round(past), o1=round(o1), o15=round(o15),
                full=sum(1 for x in v if x >= 360), n=len(v), D=round(Dis, 3), within=within, nsh=len(sh), min=min(sh), max=max(sh))
def bands(asg, key):
    o = {}; allr = {'n': 0, 'c': [0] * 4}
    for b, n in zip(BL, asg):
        wt = b['s'] if key == 'S' else (b.get('hu') or 0); d = wd(b, n)
        r = o.setdefault(n, {'n': 0, 'c': [0] * 4})
        for k, t in enumerate((.5, 1, 1.5, 2)):
            if d <= t: r['c'][k] += wt; allr['c'][k] += wt
        r['n'] += wt; allr['n'] += wt
    f = lambda r: [round(r['n'])] + [round(c / r['n'] * 100) for c in r['c']]
    res = {n: f(r) for n, r in o.items()}; res['__ALL'] = f(allr); return res
