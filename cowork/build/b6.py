import json,re
t=open('walkmap4_tpl.html').read()
def R(old,new,cnt=1):
  global t
  assert t.count(old)>=1,old[:80]
  t=t.replace(old,new,cnt)
dv=json.load(open('div.json'))
# CSS
R(":root{\n  --paper","/* --lo / --hi: kids-of-color share below / above the district share */\n:root{\n  --lo:#3f8fb0; --hi:#b0562f;\n  --paper")
R("@media (prefers-color-scheme:dark){:root:not([data-theme=\"light\"]){\n","@media (prefers-color-scheme:dark){:root:not([data-theme=\"light\"]){\n  --lo:#6fb6d6; --hi:#e08a5c;\n")
R(":root[data-theme=\"dark\"]{\n",":root[data-theme=\"dark\"]{\n  --lo:#6fb6d6; --hi:#e08a5c;\n")
R(".lbl.off{display:none}",""".lbl.off{display:none}
.dvl{display:none;align-items:center;gap:8px}
.dvl.on{display:inline-flex}
.dvl b{display:block;width:120px;height:10px;border-radius:2px;background:linear-gradient(90deg,var(--lo),color-mix(in srgb,var(--lo) 12%,var(--plate)) 45%,color-mix(in srgb,var(--hi) 12%,var(--plate)) 55%,var(--hi))}
.dt td.pc{text-align:right;font-family:var(--mono);font-variant-numeric:tabular-nums}
.dt thead th[data-k]{cursor:pointer;white-space:nowrap}
.dt thead th[aria-sort]{color:var(--ink)}
.dt td.cl{color:var(--muted);text-align:right}""")
# buttons + checkbox
R('<button data-s="A" aria-pressed="true">Walk redraw · A</button>','<button data-s="A" aria-pressed="true">Walk redraw · A</button><button data-s="DA" aria-pressed="false">Walk + diversity · A</button>')
R('<label class="chk" id="lcurw">','<label class="chk"><input type="checkbox" id="ldiv"> Shade by kids of color</label>\n  <label class="chk" id="lcurw">')
R('<span><svg width="12" height="12"><circle','<span class="dvl" id="dvl">Kids of color: fewer than district<b></b>more <em style="font-style:normal">(district '+str(dv['P'])+'%)</em></span>\n<span><svg width="12" height="12"><circle')
# shading in drawAreas
R('p.setAttribute("style",`fill:var(--c${cols[n]})`);','p.setAttribute("style",dvOn()?`fill:${dvFill(DIV.share[shareKey()][n])}`:`fill:var(--c${cols[n]})`);')
R('let scn="A",sel=null;','''let scn="A",sel=null;
const DIV=__DIV__;
const shareKey=()=>scn;
const dvOn=()=>document.getElementById("ldiv").checked;
const dvFill=q=>{if(q==null)return"var(--beyond)";const d=q-DIV.P,a=Math.min(1,Math.abs(d)/25);return `color-mix(in srgb,var(${d<0?"--lo":"--hi"}) ${Math.round(8+a*82)}%,var(--plate))`};
const koc=(k,n)=>{const v=DIV.share[k]&&DIV.share[k][n];return v==null?"—":v+"%"};''')
R('document.getElementById("lrail").onchange=','document.getElementById("ldiv").onchange=()=>{document.getElementById("dvl").classList.toggle("on",dvOn());drawAreas()};\ndocument.getElementById("lrail").onchange=')
# side panels: kids of color rows
R('<span>Students, walk redraw</span><span>${st.size??"—"}</span></div>','<span>Students, walk redraw</span><span>${st.size??"—"}</span><span>Kids of color, PPS plan</span><span>${koc(scn,n)}</span><span>Kids of color, today</span><span>${koc("T",n)}</span></div>')
R('<div class="tag">Today\'s boundary</div><h3><i style="background:var(--c${c})"></i>${nm(n)}</h3>','<div class="tag">Today\'s boundary</div><h3><i style="background:var(--c${c})"></i>${nm(n)}</h3><div class="kv"><span>Kids of color, today</span><span>${koc("T",n)}</span><span>District share</span><span>${DIV.P}%</span></div>')
R('<div class="tag">Scenario ${scn} · walk-based redraw</div>','<div class="tag">${scn==="DA"?"Scenario A · walk + diversity redraw":"Scenario "+scn+" · walk-based redraw"}</div>')
R('<span>Immersion students</span><span>${st.imm||0}</span></div>','<span>Immersion students</span><span>${st.imm||0}</span><span>Kids of color</span><span>${koc(scn,n)}</span><span>Kids of color, today</span><span>${koc("T",n)}</span>${scn==="DA"?`<span>Kids of color, walk redraw A</span><span>${koc("A",n)}</span>`:""}</div>')
# T view goes(): only A and B; fine.
# diversity section after compare section
sec='''<section style="display:flex;flex-direction:column;gap:10px" id="diversity">
  <h2>How diverse each school would be</h2>
  <p class="note" style="color:var(--ink);font-size:.86rem">Share of each school's neighborhood K–5 students who are kids of color (any race or ethnicity other than non-Hispanic white), from 2020 Census under-18 counts by block. District-wide it is __P__%. The walk + diversity redraw keeps the same closures, the same I-84 and river rules and the same 360–600 size range as the walk redraw, but when two nearby schools are both a reasonable walk it leans toward the one that brings each school closer to the district mix.</p>
  <div class="panel tablebox"><table><thead><tr><th>Assignment</th><th class="num">Dissimilarity index</th><th class="num">Schools within 15 pts of district</th><th class="num">Lowest school</th><th class="num">Highest school</th><th class="num">Avg walk (mi)</th><th class="num">Walk over 1.5 miles</th></tr></thead><tbody id="dsum"></tbody></table></div>
  <p class="note">The dissimilarity index is the share of kids of color (or of white kids) who would have to switch schools for every school to match the district mix: 0 is perfectly even, higher is more separated. Lower is more integrated.</p>
  <div class="panel tablebox"><table class="dt"><thead><tr><th data-k="0">School</th><th class="num" data-k="1">Today</th><th class="num" data-k="2">PPS plan A</th><th class="num" data-k="3">Walk redraw A</th><th class="num" data-k="4">Walk + diversity A</th><th class="num" data-k="5">Change vs walk redraw</th></tr></thead><tbody id="dtb"></tbody></table></div>
  <p class="note">Tap a column heading to sort. Cells are shaded blue when a school has fewer kids of color than the district and orange when it has more; stronger shading means further from the district share. Immersion students are left out because they choose a program site.</p>
 </section>
 <section style="display:flex;flex-direction:column;gap:10px">
  <h2>Where freeways'''
R(''' <section style="display:flex;flex-direction:column;gap:10px">
  <h2>Where freeways''',' '+sec)
t=t.replace('__P__',str(dv['P']))
js='''
// diversity tables
(()=>{const S=DIV.summ;const rows=[["Today","T"],["A · PPS plan","PA"],["A · walk redraw","A"],["A · walk + diversity redraw","DA"],["B · PPS plan","PB"],["B · walk redraw","B"]];
 document.getElementById("dsum").innerHTML=rows.map(([l,k])=>{const s=S[k];return `<tr${k==="DA"?' class="hl"':""}><th scope="row">${l}</th><td class="num">${s.D.toFixed(3)}</td><td class="num">${s.within} of ${s.n}</td><td class="num">${s.min}%</td><td class="num">${s.max}%</td><td class="num">${s.avg.toFixed(3)}</td><td class="num">${s.o15.toLocaleString()}</td></tr>`}).join("");
 const ks=["T","PA","A","DA"];const names=Object.keys(DIV.share.T).concat(Object.keys(DIV.share.DA)).filter((n,i,a)=>a.indexOf(n)===i);
 const data=names.map(n=>{const r=[n,...ks.map(k=>DIV.share[k][n]??null)];r.push(r[3]!=null&&r[4]!=null?r[4]-r[3]:null);return r});
 const dist=v=>v==null?null:Math.abs(v-DIV.P);
 let r0="";const cell=(v,k)=>{if(v==null)return `<td class="cl">${k===1?"—":DIV.share.T[r0]!=null&&r0==="Cesar Chavez"?"immersion only":"closes"}</td>`;if(k===5)return `<td class="pc">${v>0?"+":v<0?"−":""}${Math.abs(v)} pts</td>`;return `<td class="pc" style="background:${dvFill(v)}">${v}%</td>`};
 let sk=1,dir=1;const draw=()=>{const rs=data.slice().sort((a,b)=>{const x=a[sk],y=b[sk];if(sk===0)return dir*nm(x).localeCompare(nm(y));if(x==null&&y==null)return 0;if(x==null)return 1;if(y==null)return -1;return dir*(x-y)});
  document.getElementById("dtb").innerHTML=rs.map(r=>`<tr${r[0]==="Sabin"||r[0]==="MLK Jr"||r[0]==="Alameda"?' class="hl"':""}><th scope="row">${nm(r0=r[0])}</th>${r.slice(1).map((v,i)=>cell(v,i+1)).join("")}</tr>`).join("")};
 document.querySelectorAll(".dt thead th[data-k]").forEach(th=>{th.onclick=()=>{const k=+th.dataset.k;if(sk===k)dir=-dir;else{sk=k;dir=k===0?1:1}document.querySelectorAll(".dt thead th").forEach(x=>x.removeAttribute("aria-sort"));th.setAttribute("aria-sort",dir>0?"ascending":"descending");draw()}});
 draw()})();
'''
R('\n// walk-band table',js+'\n// walk-band table')
# method
R('Building capacity, safe-route features like crossing guards, and hills aren\'t modeled.</p>','Building capacity, safe-route features like crossing guards, and hills aren\'t modeled.</p>\n  <p><b>Walk + diversity redraw.</b> Starts from the Scenario A walk redraw and trades border blocks between neighboring schools when the trade brings both schools\' kids-of-color shares closer to the district share (within 8 points counts as on target). A block can only move to a school whose area it already touches, the walk can\'t grow by more than half a mile beyond the closest allowed school or past 2 miles, and school sizes stay within the same 360–600 range. Areas are then made one connected piece again.</p>\n  <p><b>Smoothing.</b> All three redraws then get a final pass that trades border blocks to shorten and straighten boundaries: a block can switch to a neighboring school when that makes the shared boundary shorter or pulls the area closer around its school, as long as it adds no more than 0.4 mi to anyone’s walk, keeps every school in its size range, keeps each area in one piece and, for the diversity version, doesn’t undo its diversity gains. The I-84 crossings described above are left as they are. In the Scenario A walk redraw, the area around Rigler, Scott, Bridger and Abernethy was also redrawn as a group, favoring rounder areas centered on each school while holding every school’s size. Together these passes cut the total length of school boundaries by about 10% in the walk redraw and 16% in the diversity version without changing average walks. Race and ethnicity come from 2020 Census tables P2 and P4 (total minus 18-and-over) by block; they describe who lives in each block, not who enrolls.</p>')
open('walkmap5_tpl.html','w').write(t)
print('tpl ok')
