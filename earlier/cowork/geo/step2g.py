import json,math,sys
from shapely.geometry import shape,mapping
kx=math.cos(math.radians(45.54))
def km2(g): return g.area*kx*111.2*111.2
for sc in sys.argv[1:]:
  fs=json.load(open(f'{sc}_parts.json'))['features']
  parts=[[f['properties']['name'],shape(f['geometry'])] for f in fs]
  big={}
  for n,g in parts: big[n]=max(big.get(n,0),g.area)
  small=[p for p in parts if p[1].area<big[p[0]] and km2(p[1])<0.25]
  sids={id(p) for p in small}
  for p in small:
    n,g=p
    best=None;bl=0
    for q in parts:
      if q[0]==n or id(q) in sids: continue
      L=g.boundary.intersection(q[1].buffer(0.00008)).length
      if L>bl: bl=L;best=q[0]
    if best:
      print(sc,'reassign',n,'->',best,round(km2(g),3)); p[0]=best
  json.dump({"type":"FeatureCollection","features":[{"type":"Feature","properties":{"name":n},"geometry":mapping(g)} for n,g in parts]},open(f'{sc}_fix.json','w'))
