import sys,os,json  # usage: python blocks_b.py blocks_b.json
SOL=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..'))  # build/solver
sys.path.insert(0,SOL); os.chdir(SOL)
import numpy as np, pandas as pd
import common as C, metrics as M
cfgdir=os.path.join(SOL,'configs','v2')
refs=M.load_refs(cfgdir)
lev='K-5'
blk=C.blocks(); mod=C.model()
out={'n':len(blk)}
runs={'B':('scenario_B','out_v2/scenario_B'),'R':('bscale_B_ref','out_v2/bscale_B_ref.staging')}
for key,(cn,od) in runs.items():
    cfg=C.load_config(os.path.join(cfgdir,cn+'.json'))
    ap=os.path.join(od,'assign_K-5.parquet')
    if not os.path.exists(ap): ap=os.path.join(os.path.dirname(os.path.abspath(__file__)),cn+'_assign_K-5.parquet')  # shipped copy
    asg=pd.read_parquet(ap)['school'].values.astype(object)
    K=np.asarray(M.level_kids(cfg,'2031')[lev],float)
    names=sorted(set(cfg['levels'][lev]['zoned']))
    col={n:k for k,n in enumerate(names)}
    W=C.dist('walk',names)
    ai=np.array([col.get(s,-1) for s in asg])
    rows=np.arange(len(asg))
    d=np.where(ai>=0, W[rows,np.maximum(ai,0)], np.nan).astype(float)
    E=M.eligible_mask(lev,names,[refs[r][lev] for r in ('today','status_quo')])
    Wm=np.where(E,W,np.inf); dmin=Wm.min(1); nn=np.array(names,dtype=object)[Wm.argmin(1)]
    past=(d-dmin)>=cfg.get('past_margin_miles',0.25)
    print(key,'kids',K.sum().round(),'past',K[past].sum().round(),'unzoned',(ai<0).sum(),'walk',(np.nansum(K*d)/K[ai>=0].sum()).round(3))
    out[key]={'asg':list(asg),'d':np.round(d,3).tolist(),'dmin':np.round(dmin,3).tolist(),'nn':list(nn),'K':np.round(K,3).tolist()}
out['x']=[b['x'] for b in mod['BL']]; out['y']=[b['y'] for b in mod['BL']]; out['today']=[b['a'] for b in mod['BL']]
out['closed']=sorted(set(mod['NAMES'])-set(json.load(open(os.path.join(cfgdir,'scenario_B.json')))['levels'][lev]['zoned']))
json.dump(out,open(sys.argv[1],'w'))
print(out['closed'])
