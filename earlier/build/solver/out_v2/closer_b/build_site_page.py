"""Site version of the Scenario B closer-schools page -> pages/closer-b.html (kit root relative).
Reuses template.html (the standalone page) and swaps in the site chrome. Run build_page.py first's inputs: vizdata.json + scorecards."""
import json,os,re
H=os.path.dirname(os.path.abspath(__file__)); O=os.path.dirname(H); KIT=os.path.abspath(os.path.join(H,'..','..','..','..'))
def m(run):
  s=json.load(open(os.path.join(H,run+'_scorecard.json'))) if os.path.exists(os.path.join(H,run+'_scorecard.json')) else json.load(open(os.path.join(O,run,'scorecard.json')))
  l=s['levels']['K-5']
  return {'past':l['kids_past_closer_school'],'bus':l['kids_over_bus_threshold'],'w1':l['pct_within_1.0mi'],'walk':l['avg_walk_mi'],
          'moved':l['kids_reassigned_vs_status_quo'],'dis':l['dissimilarity_index'],'kids':l['kids'],
          'dur':s['durability']['levels']['K-5']['at_target_all_required_years']}
M={'B':m('scenario_B'),'R':m('bscale_B_ref')}
t=open(os.path.join(H,'template.html')).read()
style=t[t.index('<style>')+7:t.index('</style>')]
# drop the standalone token/base rules; site.css supplies paper/ink/pps/ours etc.
keep_tokens=lambda blk:';'.join(x for x in blk.split(';') if re.match(r'\s*(--h\d|--empty|--line|color-scheme)',x))
def toks(sel_rx,s):
  mm=re.search(sel_rx,s,re.S); return mm
light=re.search(r':root\{(.*?)\}',style,re.S).group(1)
dark=re.search(r':root\[data-theme="dark"\]\{(.*?)\}',style,re.S).group(1)
tok=(':root{'+keep_tokens(light)+'}\n@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){'+keep_tokens(dark)+'}}\n:root[data-theme="dark"]{'+keep_tokens(dark)+'}\n')
rest=style[style.index('*{box-sizing'):]
for r in [r'\*\{box-sizing:border-box\}\n',r'body\{[^}]*\}\n',r'main\{[^}]*\}\n',r'\.ai\{[^}]*\}\n',r'h1\{[^}]*\}\n',r'h2\{[^}]*\}\n',r'p\{max-width:68ch\}\n',r'a\{color:var\(--accent\)\}\n']:
  rest=re.sub(r,'',rest,count=1)
rest=rest.replace('var(--sans)','system-ui,-apple-system,"Segoe UI",Roboto,sans-serif')
rest+='#pps-disclaimer+.eyebrow{margin-top:18px}\n.claim{margin-top:14px}\nh2{margin-top:40px}\n'
body=t[t.index('<p class="eyebrow">'):t.index('</main>')]
body=body.replace('<h1>Same ten closures. Shorter walks.</h1>','<h1>Same ten closures. Shorter walks.</h1>\n<p class="notreal">These are best effort boundaries. NOT REAL PLANS, yet.</p>')
script=t[t.index('<script>'):t.rindex('</script>')+9].replace('__DATA__',open(os.path.join(H,'vizdata.json')).read()).replace('__METRICS__',json.dumps(M))
script=script.replace('<code>out_v2/scenario_B/scorecard.json</code>','')
body=body.replace('Sources: <code>out_v2/scenario_B/scorecard.json</code>, <code>out_v2/bscale_B_ref.staging/scorecard.json</code>.',
 'Sources: <a href="../build/solver/out_v2/scenario_B/scorecard.json">PPS B scorecard</a>, <a href="../build/solver/out_v2/closer_b/bscale_B_ref_scorecard.json">walk-first scorecard</a>, <a href="../build/solver/out_v2/closer_b/">scripts and data</a>.')
FAV=open(os.path.join(KIT,'pages','sabin.html')).read()
fav=re.search(r'<link rel="icon"[^>]*>',FAV).group(0)
nav=re.search(r'<nav class="site-nav">.*?</nav>',FAV,re.S).group(0).replace(' aria-current="page"','').replace('<a href="closer-b.html">','<a href="closer-b.html" aria-current="page">')
disc=re.search(r'<div class="warn" id="pps-disclaimer">.*?</div>',FAV,re.S).group(0)
foot=FAV[FAV.rindex('<footer>'):FAV.index('</footer>')+9]
foot=re.sub(r'<footer><p>.*?</p>','<footer><p><a href="options.html">Every plan side by side</a> &middot; <a href="map.html">Every option on one map</a> &middot; <a href="method.html">How the model works</a></p>',foot,count=1,flags=re.S)
html=f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Closer schools in Scenario B | PPS boundary options</title>
<meta name="description" content="Scenario B's ten closures with K-5 lines drawn by walking distance: far fewer kids sent past a closer open school, with more schools at PPS's size target.">
{fav}
<link rel="stylesheet" href="site.css">
<style>
{tok}{rest}</style>
</head>
<body>
{nav}
<main>
{disc}
{body}{foot}
</main>
{script}
</body>
</html>
'''
open(os.path.join(KIT,'pages','closer-b.html'),'w').write(html)
print('wrote pages/closer-b.html',len(html),M['R']['past'])
