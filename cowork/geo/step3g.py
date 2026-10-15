import json,math,sys
from shapely.geometry import Polygon,MultiPolygon
from shapely.ops import unary_union
kx=math.cos(math.radians(45.54));M=111200
def vis(pts,thr):
  pts=[list(p) for p in pts]
  if len(pts)<=3: return pts
  def area(a,b,c): return abs((b[0]-a[0])*(c[1]-a[1])-(c[0]-a[0])*(b[1]-a[1]))*kx*M*M/2
  while len(pts)>3:
    areas=[area(pts[i-1],pts[i],pts[i+1]) for i in range(1,len(pts)-1)]
    i=min(range(len(areas)),key=areas.__getitem__)
    if areas[i]>thr: break
    del pts[i+1]
  return pts
def chaikin(pts,it=3):
  for _ in range(it):
    if len(pts)<3: return pts
    out=[pts[0]]
    for a,b in zip(pts,pts[1:]):
      out.append([.75*a[0]+.25*b[0],.75*a[1]+.25*b[1]]);out.append([.25*a[0]+.75*b[0],.25*a[1]+.75*b[1]])
    out.append(pts[-1]);pts=out
  return pts
def rdp(pts,tol):
  if len(pts)<3: return pts
  a,b=pts[0],pts[-1];dx,dy=(b[0]-a[0])*kx,b[1]-a[1];L=math.hypot(dx,dy) or 1e-12
  dmax,idx=0,0
  for i in range(1,len(pts)-1):
    px,py=(pts[i][0]-a[0])*kx,pts[i][1]-a[1]
    d=abs(px*dy-py*dx)/L if L>1e-12 else math.hypot(px,py)
    if d>dmax: dmax,idx=d,i
  if dmax<=tol: return [a,b]
  return rdp(pts[:idx+1],tol)[:-1]+rdp(pts[idx:],tol)
def enc(ring):
  pts=[(round(x*1e4)+1229300,round(y*1e4)-454300) for x,y in ring]
  ded=[pts[0]]
  for p in pts[1:]:
    if p!=ded[-1]: ded.append(p)
  if len(ded)>1 and ded[0]==ded[-1]: ded=ded[:-1]
  s=[f"{ded[0][0]},{ded[0][1]}"]+[f"{b[0]-a[0]},{b[1]-a[1]}" for a,b in zip(ded,ded[1:])]
  return " ".join(s)
res={}
for sc in sys.argv[2:]:
  t=json.load(open(f'{sc}_topo.json'));geoms=list(t['objects'].values())[0]['geometries']
  use=[0]*len(t['arcs'])
  def walk(o):
    for x in o:
      if isinstance(x,list): walk(x)
      else: use[x if x>=0 else ~x]+=1
  for g in geoms: walk(g['arcs'])
  arcs=[]
  for i,a in enumerate(t['arcs']):
    if use[i]>=2: arcs.append(rdp(chaikin(vis(a,6000),3),0.00004))
    else: arcs.append(vis(a,800))
  def ring(ids):
    out=[]
    for k in ids:
      a=arcs[k] if k>=0 else arcs[~k][::-1]
      out.extend(a if not out else a[1:])
    return out
  poly={};outl=[]
  for g in geoms:
    n=g['properties']['name'];polys=g['arcs'] if g['type']=='MultiPolygon' else [g['arcs']]
    rings=[ring(r) for p in polys for r in p]
    rings=[r for r in rings if len(r)>=4]
    poly[n]="|".join(enc(r) for r in rings)
    for p in polys:
      rr=[ring(r) for r in p];
      if len(rr[0])>=4: outl.append(Polygon(rr[0],[r for r in rr[1:] if len(r)>=4]).buffer(0))
  u=unary_union([o.buffer(0.0002) for o in outl]).buffer(-0.0002)
  gs=u.geoms if isinstance(u,MultiPolygon) else [u]
  res[sc]={"poly":poly,"outline":"|".join(enc(list(g.exterior.coords)) for g in gs if g.area>1e-6)}
  print(sc,len(poly),sum(len(v) for v in poly.values()),len(gs))
json.dump(res,open(sys.argv[1],'w'))
