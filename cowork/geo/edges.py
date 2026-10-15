import os as _os  # _PPS_MAP_HDR (added by export: repo-relative paths)
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_PPS_MAP = _os.environ.get('PPS_MAP_DIR') or _os.path.join(_HERE, '../../data/pps-map')
import json,numpy as np,math
from scipy.spatial import Voronoi
from shapely.geometry import Polygon,LineString
from shapely.ops import unary_union
D=json.load(open(_os.path.join(_PPS_MAP, 'pps-model.json')))
BL=D['BL'];kx=math.cos(math.radians(45.54))
def mp(c): return unary_union([Polygon(p[0],p[1:]).buffer(0) for p in c])
outl=mp(D['OUTLINE'])
pts=np.array([[b['x'],b['y']] for b in BL])+np.random.RandomState(1).normal(0,1e-7,(len(BL),2))
x0,y0,x1,y1=D['BB'];vor=Voronoi(np.vstack([pts,[[x0-1,y0-1],[x0-1,y1+1],[x1+1,y0-1],[x1+1,y1+1]]]))
E={}
for (p,q),rv in zip(vor.ridge_points,vor.ridge_vertices):
  if p>=len(BL) or q>=len(BL) or -1 in rv: continue
  seg=LineString(vor.vertices[rv]).intersection(outl)
  if seg.is_empty: continue
  L=seg.length*111.2  # approx km, scale x
  a,b=vor.vertices[rv[0]],vor.vertices[rv[1]];L=math.hypot((a[0]-b[0])*kx,a[1]-b[1])*111.2*(seg.length/max(LineString(vor.vertices[rv]).length,1e-12))
  if BL[p]['z']!=BL[q]['z']: L=0.0
  E[f"{min(p,q)},{max(p,q)}"]=round(L,4)
json.dump(E,open('../m/edges.json','w'));print(len(E),sum(E.values()))
# compare with NB
nb=sum(len(x) for x in D['NB'])//2;print('NB pairs',nb)
