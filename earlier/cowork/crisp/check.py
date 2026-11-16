# Which block centres fall inside which school's drawn polygon?  Usage: python3 check.py POLYFILE OUT.json
# Writes {A,B,DA: implied assignment} where a block keeps its final_asg school unless its centre lies
# strictly inside another school's polygon.  Prints wrong-side counts.
import os as _os  # _PPS_MAP_HDR (added by export: repo-relative paths)
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_PPS_MAP = _os.environ.get('PPS_MAP_DIR') or _os.path.join(_HERE, '../../data/pps-map')
import json, sys
from shapely.geometry import Point
from shapely import STRtree
from dec import poly
S = (_os.environ.get('CRISP_WORKDIR') or _os.path.join(_HERE, '..'))
D = json.load(open(_os.path.join(_PPS_MAP, 'pps-model.json'))); BL = D['BL']
F = json.load(open(f'{S}/m/final_asg.json'))
P = json.load(open(sys.argv[1]))
out = {}
for k in 'A', 'B', 'DA':
    G = {n: poly(s) for n, s in P['F' + k]['poly'].items()}
    names = list(G); tr = STRtree([G[n] for n in names])
    imp = []; bad = []; nowhere = 0
    for i, b in enumerate(BL):
        p = Point(b['x'], b['y']); a = F[k][i]
        inside = [names[j] for j in tr.query(p) if G[names[j]].contains(p)]
        if not inside: nowhere += 1
        if inside and a not in inside:
            imp.append(inside[0]); bad.append(i)
        else: imp.append(a)
    out[k] = imp
    st = sum(BL[i]['s'] for i in bad); stp = [i for i in bad if BL[i]['s'] > 0.05]
    print(f'{sys.argv[1]} {k}: {len(bad)} block centres on the wrong side ({len(stp)} populated, {st:.1f} students); {nowhere} centres in no polygon')
json.dump(out, open(sys.argv[2], 'w'))
