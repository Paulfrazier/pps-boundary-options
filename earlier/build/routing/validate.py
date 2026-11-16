import os as _os  # _PPS_MAP_HDR (added by export: repo-relative paths)
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_PPS_MAP = _os.environ.get('PPS_MAP_DIR') or _os.path.join(_HERE, '../../data/pps-map')
import json, numpy as np, pandas as pd
M=json.load(open(_os.path.join(_PPS_MAP, 'pps-model.json'))); BL=M['BL']; SCH=M['SCH']
S=pd.read_csv('school_points.csv',dtype={'ncessch':str})
W=pd.read_parquet('walk_miles.parquet'); B=pd.read_parquet('bike_miles.parquet')
nd=len(S)
wm=W.walk_miles.values.reshape(-1,nd); bm=B.bike_miles.values.reshape(-1,nd)
# map model name -> school idx by nearest coords
mp={}
for n,(x,y) in SCH.items():
    d=np.hypot((S.lon-x)*0.7,S.lat-y); j=d.idxmin()
    mp[n]=(j,float(d[j]*111000))
bad={n:v for n,v in mp.items() if v[1]>300}
rows=[]
for i,b in enumerate(BL):
    for n,v in b['w'].items():
        if n in mp and mp[n][1]<=300:
            rows.append((i,n,v,wm[i,mp[n][0]]))
d=pd.DataFrame(rows,columns=['i','school','old','new']); d['diff']=d.new-d.old; d['ad']=d['diff'].abs()
out=[]
out.append(f"pairs compared: {len(d)}  (schools mapped {len(mp)-len(bad)}/{len(mp)}; unmapped: {list(bad)})")
out.append(f"correlation r = {d.old.corr(d.new):.4f}")
out.append(f"median |diff| = {d.ad.median():.3f} mi, mean = {d.ad.mean():.3f}, p95 = {d.ad.quantile(.95):.3f}, p99 = {d.ad.quantile(.99):.3f}")
out.append(f"median signed diff (new-old) = {d['diff'].median():+.3f} mi; ratio median new/old = {(d.new/d.old).median():.3f}")
out.append(f"pairs with |diff|>0.25 mi: {(d.ad>.25).sum()} ({(d.ad>.25).mean()*100:.1f}%); >0.5 mi: {(d.ad>.5).sum()}")
big=d.sort_values('ad',ascending=False).head(25)
big=big.assign(geoid=[BL[i]['g'] for i in big.i],lon=[BL[i]['x'] for i in big.i],lat=[BL[i]['y'] for i in big.i])
d.to_csv('validation_pairs.csv',index=False)
open('_val_stats.txt','w').write('\n'.join(out)+'\n\n'+big.to_string(index=False))
print(open('_val_stats.txt').read())
# bike vs walk sanity
print('bike/walk median ratio',np.median(bm/np.maximum(wm,.01)))
# I-84 check
I84=M['I84']; print(type(I84), str(I84)[:300])
