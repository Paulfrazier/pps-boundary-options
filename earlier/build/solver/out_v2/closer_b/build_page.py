import json,os
H=os.path.dirname(os.path.abspath(__file__)); O=os.path.dirname(H)
def m(run):
  s=json.load(open(os.path.join(O,run,'scorecard.json')));l=s['levels']['K-5']
  return {'past':l['kids_past_closer_school'],'bus':l['kids_over_bus_threshold'],'w1':l['pct_within_1.0mi'],'walk':l['avg_walk_mi'],
          'moved':l['kids_reassigned_vs_status_quo'],'dis':l['dissimilarity_index'],'kids':l['kids'],
          'dur':s['durability']['levels']['K-5']['at_target_all_required_years']}
M={'B':m('scenario_B'),'R':m('bscale_B_ref.staging')}
t=open(os.path.join(H,'template.html')).read()
t=t.replace('__DATA__',open(os.path.join(H,'vizdata.json')).read()).replace('__METRICS__',json.dumps(M))
open(os.path.join(H,'closer_schools_b.html'),'w').write(t); print(M)
