import json,math,sys
from shapely.geometry import shape
kx=math.cos(math.radians(45.54))
from shapely.affinity import scale
def pp_of(fc):
  out={}
  for f in json.load(open(fc))['features']:
    g=scale(shape(f['geometry']),xfact=kx,yfact=1,origin=(0,0))
    out[f['properties']['name']]=4*math.pi*g.area/g.length**2
  return out
r={k:pp_of(v) for k,v in [a.split('=') for a in sys.argv[1:]]}
ks=list(r);names=sorted(r[ks[0]],key=lambda n:r[ks[0]][n])
print('mean',' '.join(f"{k} {sum(r[k].values())/len(r[k]):.3f}" for k in ks))
for n in (names if len(sys.argv)<0 else names): print(n,' '.join(f"{r[k].get(n,0):.2f}" for k in ks))
