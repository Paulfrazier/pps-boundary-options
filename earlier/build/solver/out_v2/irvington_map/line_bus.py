"""Kids who can walk (no yellow bus) in today's Sabin and Irvington areas under Today, PPS A/B, Plan D and three Irvington
split lines (Knott only, 15th + Knott, Thompson / 21st / Knott). Bus line: over 1 mi K-5, over 1.5 mi 6-8/9-12 (ORS 327.043 /
PPS), on the solver's OSRM walk matrix. Line options: Irvington blocks by build/map/line_options/work/options_blocks.csv;
middle school as modeled (Sabin side Tubman, Beverly Cleary side Beaumont) and with all of Irvington at Tubman; high school as
today. 2031-32 kids. Writes out_v2/irvington_map/line_bus.json. Run from build/solver:
    PYTHONPATH=. ../../.venv/bin/python out_v2/irvington_map/line_bus.py
"""
import sys, os, json
_HERE = os.path.dirname(os.path.abspath(__file__)); _SOLVER = os.path.abspath(os.path.join(_HERE, '..', '..'))
os.chdir(_SOLVER)
_src = open('sabin_poverty.py').read().split('MD = []')[0].replace("HERE = os.path.dirname(os.path.abspath(__file__))", f"HERE = {_SOLVER!r}")
exec(_src)
lo=pd.read_csv('../map/line_options/work/options_blocks.csv').set_index('idx')
area=b['sq_es'].values; m=np.isin(area,['Sabin','Irvington']); ix=np.where(m)[0]
assert (b.index.values[ix]==ix).all() if hasattr(b,'index') else True
BUS={'K-5':1.0,'6-8':1.5,'9-12':1.5}
plans={}
for run,lab in [('status_quo','Today'),('scenario_A','PPS A'),('scenario_B','PPS B'),('planD_updated','Plan D')]:
  d='out_v2/'+run if run!='status_quo' else SQ
  plans[lab]={lv:asg(d,lv)[ix].astype(object) for lv in BUS}
sq9=asg(SQ,'9-12')[ix].astype(object)
# the two promoted 15th + Knott runs exactly as built (all three levels from the run)
for run,lab in [('irv_sabin_15th','15th + Knott, Sabin side to Jefferson (run)'),('irv_sabin_15th_grant','15th + Knott, Irvington teens stay at Grant (run)')]:
  plans[lab]={lv:asg('out_v2/'+run,lv)[ix].astype(object) for lv in BUS}
for key,lab in [('knott','Knott only'),('15th_knott','15th + Knott'),('thompson21_knott','Thompson / 21st / Knott')]:
  toS=np.array([area[i]=='Sabin' or lo.loc[i,key]=='Sabin' for i in ix])
  plans[lab]={'K-5':np.where(toS,'Sabin','Beverly Cleary').astype(object),'6-8':np.where(toS,'Tubman','Beaumont').astype(object),'9-12':sq9}
  plans[lab+' (Irvington stays at Tubman)']={'K-5':plans[lab]['K-5'],'6-8':np.full(len(ix),'Tubman',object),'9-12':sq9}
out={}
for lab,P_ in plans.items():
  r={}
  for lv,th in BUS.items():
    a=P_[lv]; names=sorted(set(a)); W=C.dist('walk',names); j={q:k for k,q in enumerate(names)}
    w=W[ix,[j[q] for q in a]]; w=np.where(np.isfinite(w),w,9)
    k=KSQ[lv][ix]; pk=k*P[lv][ix]
    for ar in ['Sabin','Irvington','both']:
      mm=np.ones(len(ix),bool) if ar=='both' else area[ix]==ar
      r[f'{lv}|{ar}']={'kids':round(float(k[mm].sum()),1),'walk_ok':round(float(k[mm&(w<=th)].sum()),1),'bus':round(float(k[mm&(w>th)].sum()),1),'pov_walk_ok':round(float(pk[mm&(w<=th)].sum()),1),'pov':round(float(pk[mm].sum()),1),'avg_walk':round(float(np.average(w[mm],weights=k[mm])),3)}
  out[lab]=r
json.dump(out, open(os.path.join(_HERE, 'line_bus.json'), 'w'), indent=1)
for lab,r in out.items():
  print(f"{lab:48s}",' | '.join(f"{lv} {r[lv+'|both']['walk_ok']:.0f}/{r[lv+'|both']['kids']:.0f} (Irv {r[lv+'|Irvington']['walk_ok']:.0f} Sab {r[lv+'|Sabin']['walk_ok']:.0f})" for lv in BUS))
