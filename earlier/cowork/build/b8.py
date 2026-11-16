import json,re
t=open('walkmap5_tpl.html').read()
f=open('src_prev.html').read()
def grab(pre,post):
  i=f.index(pre)+len(pre); return f[i:f.index(post,i)]
sm=json.load(open('../geo/smooth.json'))
rd=json.load(open('pj5.json'))
smf=json.load(open('../geo/smoothF.json'))
for s in 'AB': rd[s]['poly']=smf['F'+s]['poly']
dv=json.load(open('div2.json'))
fix=lambda st:{k:{**v,'from':', '.join(('King'+x[6:]) if x.startswith('MLK Jr ') else x for x in v['from'].split(', ')) if v['from'] else ''} for k,v in st.items()}
rd['DA']={'order':rd['A']['order'],'poly':smf['FDA']['poly'],'stats':dv['stats']['DA'],'pps':rd['A']['pps']}
for s in 'AB': rd[s]['stats']=dv['stats'][s]
cmp=json.loads(grab('const CMP=',';\nconst DET='))
R_=lambda s_:[f"{s_['avg']:.3f}",f"{s_['o1']:,}",f"{s_['o15']:,}",f"{s_['past']:,}",f"{s_['full']} of {s_['nn']}",f"{s_['moved']:,}"]
new={"A · walk redraw":R_(dv["summ"]["A"]),"B · walk redraw":R_(dv["summ"]["B"]),"No closures · walk redraw":["0.780","3,116","1,043","480","18 of 53","3,652"]}
for r in cmp:
  if r[0] in new: r[1:]=new[r[0]]
s_=dv['summ']['DA'];i=[r[0] for r in cmp].index('A · walk redraw')
cmp.insert(i+1,['A · walk + diversity redraw',f"{s_['avg']:.3f}",f"{s_['o1']:,}",f"{s_['o15']:,}",f"{s_['past']:,}",f"{s_['full']} of {s_['nn']}",f"{s_['moved']:,}"])
vals={'__BASE__':grab('const BASE=`','`;\nconst CUR'),'__CUR__':grab('const CUR=`','`;\nconst RD='),'__RD__':json.dumps(rd,separators=(',',':')),
 '__SCH__':grab('const SCH=',';\nconst CMP='),'__CMP__':json.dumps(cmp,ensure_ascii=False),'__DET__':grab('const DET=',';\nconst PPSP=') if 'const PPSP=' in f else grab('const DET=',';\nconst OUTL'),'__OUTL__':json.dumps(smf['FA']['outline']),'__PPSP__':open('../geo/ppspoly.json').read(),'__WB__':open('wb2.json').read(),'__DIV__':json.dumps({'P':dv['P'],'share':dv['share'],'summ':dv['summ']},separators=(',',':')),'__STREETS__':open('streets.txt').read().strip()}
# static html sections from current page
for pat in [r'<table><thead><tr><th>Closing area</th>.*?</thead>',r'<p class="note">Averages are.*?</p>']:
  pass
t=t.replace("<h2>Where freeways and rail make PPS's plan a long walk</h2>","<h2>Walking from each closing school's area under PPS plan A</h2>")
t=re.sub(r'<table><thead><tr><th>Today\'s area</th>.*?</thead>',lambda m:re.search(r'<table><thead><tr><th>Closing area</th>.*?</thead>',f).group(0),t,count=1,flags=re.S)
t=re.sub(r'<p class="note">Groups of blocks.*?</p>',lambda m:re.search(r'<p class="note">Averages are.*?</p>',f).group(0),t,count=1,flags=re.S)
t=t.replace('<td class="num">${r[4]}</td><td>${nm(r[5])}</td></tr>','<td class="num">${r[4]}</td><td class="num">${r[5]}</td><td>${nm(r[6])} (${r[7]}%)</td></tr>')
old="Boundary shapes are drawn from the blocks each school receives, so edges follow block centers rather than exact street lines."
assert old in t
t=t.replace(old,"I-84 and the Willamette are treated as hard edges: a block can only be assigned to a school on its own side of both, with one exception that matches PPS: about 117 students live in blocks that today's Buckman, Laurelhurst and Beverly Cleary areas already reach across I-84, and those blocks may stay with a school on the far side. In Scenario A there is one added crossing, by request: about 87 Rose City Park students in the Hollywood blocks just north of I-84 go to Laurelhurst (about a 1.1-mile walk) instead of Beverly Cleary (about 1.3 miles). After that first pass, every school's area is made one connected piece: blocks are switched to the school most of their neighbors use when that adds no more than 0.2 mi to the walk, any piece cut off from its school joins the neighbor with the shortest walk, and border blocks are traded back so school sizes stay where the first pass put them. That cleanup adds about 0.01 mi to the average walk. Boundary shapes are drawn from the blocks each school receives, then smoothed, so redraw edges are accurate to about a block; today's boundaries are PPS's exact lines.")
t=t.replace("so freeways, rail lines and the river only count as crossable at real bridges and overpasses.","so freeways, rail lines and the river only count as crossable at real bridges and overpasses. Beyond the few I-84 crossings today's boundaries already have, the redraw adds only one: Hollywood blocks north of I-84 go to Laurelhurst in Scenario A.")
assert "adds only one" in t
for k,v in vals.items(): t=t.replace(k,v)
assert not re.search(r'__[A-Z]+__',t)
open('pps-walk-redraw-v6.html','w').write(t)
open('chk.js','w').write(re.search(r'<script>(.*)</script>',t,re.S).group(1))
print(len(t))
