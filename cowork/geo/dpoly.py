import os as _os  # _PPS_MAP_HDR (added by export: repo-relative paths)
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_PPS_MAP = _os.environ.get('PPS_MAP_DIR') or _os.path.join(_HERE, '../../data/pps-map')
import json,sys,numpy as np
from scipy.spatial import Voronoi
from shapely.geometry import Polygon,MultiPolygon,shape,mapping
from shapely.ops import unary_union
D=json.load(open(_os.path.join(_PPS_MAP, 'pps-model.json')))
asg=json.load(open(sys.argv[2] if len(sys.argv)>2 else '../m/ls_final.json'))[sys.argv[1]]
BL=D['BL']
def mp(c): return unary_union([Polygon(p[0],p[1:]).buffer(0) for p in c])
outl=mp(D['OUTLINE']);Z={k:mp(v).intersection(outl) for k,v in D['ZP'].items()}
pts=np.array([[b['x'],b['y']] for b in BL])
x0,y0,x1,y1=D['BB'];far=[[x0-1,y0-1],[x0-1,y1+1],[x1+1,y0-1],[x1+1,y1+1]]
# jitter duplicates
pts=pts+np.random.RandomState(1).normal(0,1e-7,pts.shape)
vor=Voronoi(np.vstack([pts,far]))
from shapely import set_precision
def rnd(g): return set_precision(g,1e-4).buffer(0)
cells={}
for i,b in enumerate(BL):
  r=vor.regions[vor.point_region[i]]
  if -1 in r or not r: continue
  c=Polygon(vor.vertices[r]).buffer(0).intersection(Z[b['z']])
  if not c.is_empty: cells.setdefault(asg[i],[]).append(c)
feats=[{"type":"Feature","properties":{"name":n},"geometry":mapping(rnd(unary_union(cs).buffer(0)))} for n,cs in sorted(cells.items())]
json.dump({"type":"FeatureCollection","features":feats},open(sys.argv[3] if len(sys.argv)>3 else 'DA.json','w'))
print(len(feats))
