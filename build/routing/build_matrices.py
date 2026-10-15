import os as _os  # _PPS_MAP_HDR (added by export: repo-relative paths)
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_PPS_MAP = _os.environ.get('PPS_MAP_DIR') or _os.path.join(_HERE, '../../data/pps-map')
import json, requests, numpy as np, pandas as pd
M=json.load(open(_os.path.join(_PPS_MAP, 'pps-model.json'))); BL=M['BL']
S=pd.read_csv('school_points.csv',dtype={'ncessch':str})
blk=pd.DataFrame({'block_idx':range(len(BL)),'geoid':[b['g'] for b in BL],'lon':[b['x'] for b in BL],'lat':[b['y'] for b in BL]})
def nearest(port,prof,lon,lat):
    r=requests.get(f'http://localhost:{port}/nearest/v1/{prof}/{lon},{lat}').json()
    return r['waypoints'][0]['distance'] if r.get('code')=='Ok' else np.nan
for name,port,prof in [('walk',5001,'foot'),('bike',5002,'bicycle')]:
    dst=';'.join(f'{x},{y}' for x,y in zip(S.lon,S.lat)); nd=len(S)
    rows=[]; CH=400
    snapb=[]
    for a in range(0,len(blk),CH):
        b=blk.iloc[a:a+CH]
        src=';'.join(f'{x},{y}' for x,y in zip(b.lon,b.lat))
        url=f'http://localhost:{port}/table/v1/{prof}/{src};{dst}'
        r=requests.post(url.split('/table')[0]+'/table/v1/'+prof+'/'+src+';'+dst if False else url,
            params={'sources':';'.join(map(str,range(len(b)))),'destinations':';'.join(str(len(b)+j) for j in range(nd)),'annotations':'duration,distance'}).json()
        assert r['code']=='Ok',r
        D=np.array(r['distances'],dtype=float); T=np.array(r['durations'],dtype=float)
        df=pd.DataFrame({'block_idx':np.repeat(b.block_idx.values,nd),'geoid':np.repeat(b.geoid.values,nd),
            'school_idx':np.tile(np.arange(nd),len(b)),'ncessch':np.tile(S.ncessch.values,len(b)),
            f'{name}_miles':(D/1609.344).ravel(),f'{name}_seconds':T.ravel()})
        rows.append(df); print(name,a,flush=True)
    out=pd.concat(rows,ignore_index=True)
    out.to_parquet(f'{name}_miles.parquet',index=False)
    print(name,'null pairs',out[f'{name}_miles'].isna().sum(),'of',len(out))
    # snap diagnostics
    sn=[nearest(port,prof,x,y) for x,y in zip(S.lon,S.lat)]
    S[f'{name}_snap_m']=sn
S.to_csv('school_points.csv',index=False)
