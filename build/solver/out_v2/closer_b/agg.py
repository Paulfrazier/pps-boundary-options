import json,math,sys,os,collections  # usage: python agg.py blocks_b.json vizdata.json
sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..')))
import common as C
D=json.load(open(sys.argv[1])); m=C.model()
n=D['n']; X=D['x'];Y=D['y']; T=D['today']
CL=['Beach','Buckman','Creston','Irvington','James John','Maplewood','Marysville','Peninsula','Sabin','Woodmere']
LAT0=45.53; kx=math.cos(math.radians(LAT0))*69.17; ky=69.05  # miles per degree
CELL=0.25 # miles (~400 m)
def cell(i): return (int(math.floor((X[i]+122.7)*kx/CELL)), int(math.floor((Y[i]-45.5)*ky/CELL)))
out={'cell':CELL,'kx':kx,'ky':ky}
grids={}; area=collections.defaultdict(lambda:{'kids':0,'B':0,'R':0}); pairs=collections.defaultdict(lambda:[0,0,0,0])
tot={}
for key in ('B','R'):
  P=D[key]; g=collections.defaultdict(lambda:[0,0,0])  # kids total, kids past, kid-miles extra
  pk=0; extra=0
  for i in range(n):
    K=P['K'][i]; d=P['d'][i]; dm=P['dmin'][i]
    c=cell(i); g[c][0]+=K
    if d-dm>=0.25:
      g[c][1]+=K; g[c][2]+=K*(d-dm); pk+=K; extra+=K*(d-dm)
      area[T[i]][key]+=K
      if key=='B':
        p=pairs[(T[i],P['asg'][i],P['nn'][i])]; p[0]+=K; p[1]+=K*d; p[2]+=K*dm
        if D['R']['asg'][i]==P['nn'][i] or D['R']['d'][i]-D['R']['dmin'][i]<0.25: p[3]+=K
    if key=='B': area[T[i]]['kids']+=K
  grids[key]=g; tot[key]={'past':round(pk),'extra_mi':round(extra,1),'avg_extra':round(extra/pk,2)}
cells=sorted(set(grids['B'])|set(grids['R']))
out['cells']=[[c[0],c[1],round(grids['B'][c][0],1),round(grids['B'][c][1],1),round(grids['R'][c][1],1),round(grids['B'][c][2]/grids['B'][c][1],2) if grids['B'][c][1] else 0] for c in cells if grids['B'][c][0]>0.5 or grids['R'][c][0]>0.5]
out['tot']=tot
out['area']=sorted([[a,round(v['kids']),round(v['B']),round(v['R']),a in CL] for a,v in area.items() if v['B']>=1 or v['R']>=1],key=lambda r:-r[2])
out['pairs']=sorted([[a,s,nn,round(v[0]),round(v[1]/v[0],2),round(v[2]/v[0],2),round(v[3])] for (a,s,nn),v in pairs.items() if v[0]>=15],key=lambda r:-r[3])
def pj(lon,lat): return [round((lon+122.7)*kx/CELL,2), round((lat-45.5)*ky/CELL,2)]
def simp(pts,step):
  r=pts[::step]; 
  if r[-1]!=pts[-1]: r.append(pts[-1])
  return [pj(*p) for p in r]
out['outline']=[simp(ring,6) for poly in m['OUTLINE'] for ring in poly[:1]]
out['river']=simp(m['RV'],1); out['i84']=simp(m['I84'],1)
openB=set(a for a in D['B']['asg'])
out['schools']=[[nm]+pj(*xy)+[nm in CL, nm in openB] for nm,xy in m['SCH'].items()]
json.dump(out,open(sys.argv[2],'w'),separators=(',',':'))
print(tot, len(out['cells']), 'outline pts',sum(len(r) for r in out['outline']))
for r in out['area'][:16]: print(r)
print()
for r in out['pairs'][:22]: print(r)
