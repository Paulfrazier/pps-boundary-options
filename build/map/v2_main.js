// ===== v2: compare, street names, zoom-gated toggles =====
const PLAN_LBL={T:"Today",PA:"PPS Scenario A (official map)",PB:"PPS Scenario B (official map)",A:"Walk redraw A",B:"Walk redraw B",DA:"Walk + diversity A"};
function pbars(s,n){const f=(RD[s].pfrom||{})[n]||"";const parts=f.split(", ").filter(Boolean).map(x=>{const i=x.lastIndexOf(" ");return[x.slice(0,i),+x.slice(i+1)]});const mx=Math.max(1,...parts.map(p=>p[1]));
 return parts.length?`<div class="from"><div class="tag">Students by today's area</div>${parts.map(([a,v])=>`<div class="bar"><span>${nm(a)}</span><em>${v}</em><s style="width:${(v/mx*100).toFixed(0)}%"></s></div>`).join("")}</div>`:`<p class="hint">All students here are in the citywide immersion program.</p>`}
const PROGTXT={"Cesar Chavez":["Focused K-5 regional Spanish DLI school; neighborhood (non-DLI) K-5 students move to Rosa Parks","PPS Family Guide, César Chávez, p.3"],
 "Lent":["Remains a focused K-5 Spanish DLI school; neighborhood boundary moves to Kelly","PPS Family Guide, Lent, p.3"],
 "Rigler":["Focused regional Spanish DLI K-5 school; non-DLI neighborhood boundary shifts to Scott","PPS Family Guide, Rigler, p.3"]};
function progList(plan){if(plan==="T")return[];const s=plan==="B"||plan==="PB"?"B":"A";const pol=polysOf(plan);
 const names=(plan==="PA"||plan==="PB")?Object.keys(RD[s].pps):Object.keys(RD[plan].stats);
 return names.filter(n=>!pol[n]&&SCH[n]&&n in PROG[s]).map(n=>({n,proj:PROG[s][n]}))}
const progInfo=p=>PROGTXT[p.n]||["Focused DLI school with no neighborhood area","PPS Family Guide"];
const progTxt=p=>`${nm(p.n)} (Spanish DLI focus) — ${progInfo(p)[0]}${p.proj!=null?` · PPS projection, 2031-32: ${fmt(p.proj)}`:""} · Source: ${progInfo(p)[1]}`;
function progMarkers(g,plan,skip){progList(plan).forEach(p=>{if(skip&&skip.has(p.n))return;const[x,y]=P(SCH[p.n]).split(",");const txt=progTxt(p);
  const c=mk("circle",{cx:x,cy:y,r:5,fill:"var(--cmp)",stroke:"var(--ink)","stroke-width":"1.8","vector-effect":"non-scaling-stroke","data-x":x,"data-y":y,"data-rm":"1.5",tabindex:"0",role:"img","aria-label":txt,class:"progm"});
  const ti=mk("title",{});ti.textContent=txt;c.append(ti);const sh=e=>showTip(e,txt);c.addEventListener("pointerenter",sh);c.addEventListener("pointermove",sh);c.addEventListener("pointerleave",hideTip);
  c.addEventListener("focus",()=>{const b=c.getBoundingClientRect();showTip({clientX:b.x+b.width/2,clientY:b.y},txt)});c.addEventListener("blur",hideTip);g.append(c);
  const t=mk("text",{x:+x+6,y:+y+4,class:"lbl","data-x":x,"data-y":y,"data-n":p.n,"data-rm":"1.5"});t.textContent=nm(p.n)+" (Spanish DLI focus)";g.append(t)})}
function progPanel(){const blk=pl=>{const L=progList(pl);return L.length?`<p class="hint" style="color:var(--ink)"><b>${PLAN_LBL[pl]}</b></p><ul class="proglist">${L.map(p=>`<li>${progTxt(p)}</li>`).join("")}</ul>`:""};
 if(!cmpOn()){const b=blk(scn);return b?`<div class="from progbox"><div class="tag">Program-only schools</div>${b}</div>`:""}
 const a=progList(p1),b=progList(p2),pol1=polysOf(p1),pol2=polysOf(p2);let h="";
 const lost=b.filter(p=>pol1[p.n]),gained=a.filter(p=>pol2[p.n]);
 if(lost.length)h+=`<p class="hint" style="color:var(--ink)">${lost.map(p=>nm(p.n)).join(", ")} ${lost.length>1?"go":"goes"} from having a neighborhood area in ${PLAN_LBL[p1]} to program-only in ${PLAN_LBL[p2]}.</p>`;
 if(gained.length)h+=`<p class="hint" style="color:var(--ink)">${gained.map(p=>nm(p.n)).join(", ")} ${gained.length>1?"go":"goes"} from program-only in ${PLAN_LBL[p1]} to having a neighborhood area in ${PLAN_LBL[p2]}.</p>`;
 const x=blk(p1)+(p1===p2?"":blk(p2));return(h||x)?`<div class="from progbox"><div class="tag">Program-only schools</div>${h}${x}</div>`:""}
const PLAN_SHORT={T:"Today",PA:"PPS A",PB:"PPS B",A:"Walk A",B:"Walk B",DA:"Walk+div A"};
const PLAN_ORD=["T","PA","PB","A","B","DA"];
const $=id=>document.getElementById(id);
let initLoad=false,mode="single",p1="PA",p2="A",swf=.5,showDiff=true,showHatch=false;
const cmpOn=()=>mode!=="single";
const gShare=(plan,n)=>(DIV.share[plan]||{})[n];
const cmpColKey=(a,b)=>a+"|"+b;
function cmpCols(a,b){const k=cmpColKey(a,b);if(colOf[k])return colOf[k];const pa=polysOf(a),pb=polysOf(b),m={};
 new Set([...Object.keys(pa),...Object.keys(pb)]).forEach(n=>{m[n]=[pa[n],pb[n]].filter(Boolean).join("|")});return colOf[k]=colorize(m)}
function pairInfo(a,b){const i=PLAN_ORD.indexOf(a),j=PLAN_ORD.indexOf(b);if(a===b)return null;const fwd=i<j;const D=CMPD.pairs[fwd?a+"|"+b:b+"|"+a];
 if(!D)return null;return{n:D.n,regs:D.regs.map(r=>fwd?r:[r[1],r[0],r[2],r[3]]),km2:D.area_km2,flows:D.flows.map(f=>fwd?f:[f[1],f[0],f[2]])}}
function fillStyle(plan,n,cols){return dvOn()?`fill:${dvFill(gShare(plan,n))}`:`fill:var(--c${cols[n]})`}
function drawPlan(g,plan,cols,tab){const polys=polysOf(plan);
 Object.entries(polys).forEach(([n,enc])=>{const p=mk("path",{d:dec(enc).map(r=>"M"+r.map(P).join("L")+"Z").join(""),class:"area"+(n===sel?" sel":""),"fill-rule":"evenodd","data-n":n,tabindex:tab?"0":"-1"});
  p.setAttribute("style",fillStyle(plan,n,cols));p.addEventListener("click",()=>select(n));if(tab)p.addEventListener("keydown",e=>{if(e.key==="Enter")select(n)});g.append(p)})}
function drawSchools(g,plan){Object.keys(polysOf(plan)).forEach(n=>{const s=SCH[n];if(!s)return;const[x,y]=P(s).split(",");
  g.append(mk("circle",{cx:x,cy:y,r:3.5,fill:"var(--plate)",stroke:"var(--ink)","stroke-width":"1.8","vector-effect":"non-scaling-stroke","data-x":x,"data-y":y}));
  const t=mk("text",{x:+x+6,y:+y+4,class:"lbl","data-x":x,"data-y":y,"data-n":n});t.textContent=nm(n);g.append(t)});progMarkers(g,plan)}
function curVis(){const t=cmpOn()?(p1==="T"||p2==="T"):scn==="T";gCur.style.display=(!t&&$("lcur").checked)?"":"none";$("lcurw").style.opacity=t?.4:1}
function drawAreas(){gA.replaceChildren();gA2.replaceChildren();gS.replaceChildren();gDiff.replaceChildren();gOv.replaceChildren();
 const c=cmpOn(),a=c?p1:scn;const polys=polysOf(a);
 const cols=c?cmpCols(p1,p2):(colOf[scn]||(colOf[scn]=colorize(polys)));
 curVis();
 drawPlan(gA,a,cols,true);drawSchools(gS,a);
 gS.removeAttribute("clip-path");gA2.removeAttribute("clip-path");
 if(c){const polys2=polysOf(p2);
  if(mode==="swipe"){drawPlan(gA2,p2,cols,false);gA2.setAttribute("clip-path","url(#swc)");
   const g1=mk("g"),g2=mk("g");gS.replaceChildren(g1,g2);drawSchools(g1,p1);drawSchools(g2,p2);g1.setAttribute("clip-path","url(#swcL)");g2.setAttribute("clip-path","url(#swc)")}
  else{const d=Object.values(polys2).map(enc=>dec(enc).map(r=>"M"+r.map(P).join("L")+"Z").join("")).join("");
   gOv.append(mk("path",{d,fill:"none",stroke:"var(--cmp-case)","stroke-width":"5","stroke-linejoin":"round","stroke-opacity":".9","vector-effect":"non-scaling-stroke"}),mk("path",{d,fill:"none",stroke:"var(--cmp)","stroke-width":"2.4","stroke-linejoin":"round","vector-effect":"non-scaling-stroke"}));
   const g2=mk("g");gS.append(g2);progMarkers(g2,p2,new Set(progList(p1).map(p=>p.n)));Object.keys(polys2).forEach(n=>{if(polys[n])return;const s=SCH[n];if(!s)return;const[x,y]=P(s).split(",");
    g2.append(mk("circle",{cx:x,cy:y,r:3.5,fill:"var(--plate)",stroke:"var(--cmp)","stroke-width":"1.8","vector-effect":"non-scaling-stroke","data-x":x,"data-y":y}));
    const t=mk("text",{x:+x+6,y:+y+4,class:"lbl","data-x":x,"data-y":y,"data-n":n});t.textContent=nm(n);g2.append(t)})}
  const I=pairInfo(p1,p2);if(I&&(showDiff||showHatch)){const pd=r=>r[3].split("|").map(rr=>dec(rr)[0]).map(q=>"M"+q.map(P).join("L")+"Z").join("");
   if(showHatch)gDiff.append(mk("path",{d:I.regs.map(pd).join(""),"fill-rule":"evenodd",fill:"url(#hatch)","pointer-events":"none"}));
   if(showDiff){const all=I.regs.map(pd).join("");
    gDiff.append(mk("path",{d:all,fill:"none",stroke:"var(--plate)","stroke-width":"6","stroke-linejoin":"round","stroke-opacity":".95","vector-effect":"non-scaling-stroke","pointer-events":"none"}),mk("path",{d:all,fill:"none",stroke:"var(--ink)","stroke-width":"2.6","stroke-linejoin":"round","vector-effect":"non-scaling-stroke","pointer-events":"none"}));
    I.regs.forEach(r=>{const p=mk("path",{d:pd(r),"fill-rule":"evenodd",fill:"#000","fill-opacity":"0",class:"chg",tabindex:"0",role:"img","aria-label":`${nm(r[0])} to ${nm(r[1])}, ${fmt(r[2])} students`});
     const show=e=>showTip(e,`${nm(r[0])} → ${nm(r[1])}, ${fmt(r[2])} students`);p.addEventListener("pointermove",show);p.addEventListener("pointerdown",show);p.addEventListener("pointerleave",hideTip);
     p.addEventListener("focus",()=>{const b=p.getBBox(),m=svg.getScreenCTM();showTip({clientX:m.e+(b.x+b.width/2)*m.a,clientY:m.f+(b.y+b.height/2)*m.d},`${nm(r[0])} → ${nm(r[1])}, ${fmt(r[2])} students`)});p.addEventListener("blur",hideTip);
     p.addEventListener("click",()=>select(r[0]));gDiff.append(p)})}}}
 viewHook();updateLabels();
 if(c){if(sel&&!polys[sel]&&!polysOf(p2)[sel])sel=null;select(sel)}
 else if(!sel||!polys[sel])select(scn==="T"?"Sabin":"MLK Jr");else select(sel)}
const fmt=n=>Math.round(n).toLocaleString();
const sg=d=>d>0?"+"+fmt(d):d<0?"−"+fmt(-d):"0";
function cmpSide(n){const I=pairInfo(p1,p2),s1=CMPD.sizes[p1],s2=CMPD.sizes[p2],in1=polysOf(p1),in2=polysOf(p2);
 const names=[...new Set([...Object.keys(in1),...Object.keys(in2)])];
 const rows=names.map(k=>{const v1=in1[k]?(s1[k]||0):null,v2=in2[k]?(s2[k]||0):null;return[k,v1,v2,(v2||0)-(v1||0)]});
 rows.sort((x,y)=>Math.abs(y[3])-Math.abs(x[3])||nm(x[0]).localeCompare(nm(y[0])));
 const chg=rows.filter(r=>r[3]!==0);
 const po1=new Set(progList(p1).map(p=>p.n)),po2=new Set(progList(p2).map(p=>p.n));
 const cell=(v,k,po)=>v==null?(po.has(k)?'<span title="immersion program only, no neighborhood area">program only</span>':'<span title="not open in this plan">closed</span>'):fmt(v);
 let h=`<div class="cside"><div class="tag">Comparing</div><h3 style="font-size:1.1rem;flex-wrap:wrap">${PLAN_LBL[p1]}<span style="font-weight:600;color:var(--muted)">vs</span><span style="color:var(--cmp)">${PLAN_LBL[p2]}</span></h3>`;
 if(!I){h+=`<p class="hint">Pick two different plans to see what changes.</p>`}
 else{const pct=(I.n/CMPD.total*100).toFixed(1);
  h+=`<div class="big">${fmt(I.n)}</div><p class="hint" style="color:var(--ink);font-size:.9rem;margin-top:-4px"><b>students (${pct}%)</b> are assigned to a different school.</p><p class="hint">Out of ${fmt(CMPD.total)} modeled neighborhood K–5 students. ${showDiff?`The outlined areas on the map (${I.km2} km²) are where the two plans assign a different school. Hover or tap one to see the move.`:"Turn on “Outline changed schools” to see where on the map."}</p>`}
 if(n){const r=rows.find(x=>x[0]===n);
  if(r){const fl=(I?I.flows:[]);const out=fl.filter(f=>f[0]===n).slice(0,4),inn=fl.filter(f=>f[1]===n).slice(0,4);
   h+=`<div class="kv"><span>${nm(n)}, ${PLAN_LBL[p1]}</span><span>${r[1]==null?"closed":fmt(r[1])}</span><span>${nm(n)}, ${PLAN_LBL[p2]}</span><span>${r[2]==null?"closed":fmt(r[2])}</span><span>Change</span><span class="${r[3]>0?"pos":r[3]<0?"neg":""}">${sg(r[3])}</span></div>`;
   if(out.length||inn.length)h+=`<div class="from">${out.length?`<div class="tag">Leaving ${nm(n)} for</div>`+out.map(f=>`<div class="bar"><span>${nm(f[1])}</span><em>${fmt(f[2])}</em></div>`).join(""):""}${inn.length?`<div class="tag">Arriving at ${nm(n)} from</div>`+inn.map(f=>`<div class="bar"><span>${nm(f[0])}</span><em>${fmt(f[2])}</em></div>`).join(""):""}</div>`}}
 if(I){h+=`<div class="tag">Change in school size (neighborhood students)</div><div class="dscroll" tabindex="0" role="region" aria-label="School size change table, scrollable"><table class="dtab"><thead><tr><th>School</th><th class="num">${PLAN_SHORT[p1]}</th><th class="num">${PLAN_SHORT[p2]}</th><th class="num">Change</th></tr></thead><tbody>${chg.map(r=>`<tr${r[0]===n?' class="hl"':""}><th scope="row"><button type="button" data-sel="${r[0].replace(/"/g,"&quot;")}">${nm(r[0])}</button></th><td class="num">${cell(r[1],r[0],po1)}</td><td class="num">${cell(r[2],r[0],po2)}</td><td class="num ${r[3]>0?"pos":"neg"}">${sg(r[3])}</td></tr>`).join("")}</tbody></table></div>`;
  const top=I.flows.slice(0,6);if(top.length)h+=`<div class="from"><div class="tag">Biggest moves</div>${top.map(f=>`<div class="bar"><span>${nm(f[0])} → ${nm(f[1])}</span><em>${fmt(f[2])}</em></div>`).join("")}</div>`;
  h+=`<p class="hint">${rows.length-chg.length} school${rows.length-chg.length===1?"":"s"} unchanged. Counts are modeled K–5 neighborhood students from 2020 Census blocks; immersion and program seats are left out, so they run lower than total enrollment.${n?"":" Tap an area for one school."}</p>`}
 $("side").innerHTML=h+"</div>"+progPanel();
 $("side").querySelectorAll("[data-sel]").forEach(b=>b.onclick=()=>select(b.dataset.sel))}
function select(n){if(!cmpOn()){selectOne(n);const pp=progPanel();if(pp)$("side").insertAdjacentHTML("beforeend",pp);return}sel=n;[gA,gA2].forEach(g=>g.querySelectorAll(".area").forEach(p=>p.classList.toggle("sel",p.dataset.n===n)));cmpSide(n)}
// ---- mode + controls
function setMode(m){const was=mode;mode=m;document.querySelectorAll("[data-m]").forEach(b=>b.setAttribute("aria-pressed",b.dataset.m===m));
 const c=m!=="single";$("cmpbar").hidden=!c;$("segS").hidden=c;$("swipe").hidden=m!=="swipe";$("chipL").hidden=$("chipR").hidden=!c;$("lg2").hidden=!c;
 $("lgS").hidden=m!=="swipe";$("lgO").hidden=m!=="overlay";
 if(c&&was==="single"&&!initLoad){p1=scn;p2=scn==="PA"?"A":"PA";$("sel1").value=p1;$("sel2").value=p2}
 if(c&&was==="single"){showDiff=true;$("ldf").checked=true}
 if(c)$("cnote").textContent=m==="swipe"?"Drag the handle (or use the left and right arrow keys) to reveal the second plan on the right.":"Fill shows plan 1. The magenta line is plan 2's boundary.";
 if(!c){sel=null}
 chips();drawAreas()}
function chips(){$("chipL").textContent=PLAN_LBL[p1];$("chipR").innerHTML=mode==="overlay"?`<i></i>${PLAN_LBL[p2]}`:PLAN_LBL[p2];
 $("swipe").querySelector("button").setAttribute("aria-label",`Swipe divider: left shows ${PLAN_LBL[p1]}, right shows ${PLAN_LBL[p2]}`)}
document.querySelectorAll("[data-m]").forEach(b=>b.onclick=()=>setMode(b.dataset.m));
["sel1","sel2"].forEach(id=>{const s=$(id);PLAN_ORD.forEach(k=>s.append(new Option(PLAN_LBL[k],k)));s.onchange=()=>{p1=$("sel1").value;p2=$("sel2").value;chips();drawAreas()}});
$("sel1").value=p1;$("sel2").value=p2;
$("swapb").onclick=()=>{[p1,p2]=[p2,p1];$("sel1").value=p1;$("sel2").value=p2;chips();drawAreas()};
$("ldf").onchange=e=>{showDiff=e.target.checked;drawAreas()};$("lhf").onchange=e=>{showHatch=e.target.checked;drawAreas()};
const tip=$("tip");function showTip(e,txt){const r=$("map").getBoundingClientRect();tip.textContent=txt;tip.hidden=false;const w=tip.offsetWidth;tip.style.left=Math.max(4,Math.min(r.width-w-4,e.clientX-r.left+12))+"px";tip.style.top=Math.max(4,e.clientY-r.top-34)+"px"}
function hideTip(){tip.hidden=true}
$("lcur").onchange=curVis;
// ---- swipe handle
const swb=$("swipe").querySelector("button");
function setSwipe(f){swf=Math.max(0,Math.min(1,f));$("swipe").style.left=(swf*100)+"%";swb.setAttribute("aria-valuenow",Math.round(swf*100));swb.setAttribute("aria-valuetext",Math.round(swf*100)+"% from the left");viewHook()}
swb.addEventListener("pointerdown",e=>{e.preventDefault();swb.setPointerCapture(e.pointerId);swb.dataset.drag=1;swb.focus()});
swb.addEventListener("pointermove",e=>{if(!swb.dataset.drag)return;const r=svg.getBoundingClientRect();setSwipe((e.clientX-r.left)/r.width)});
const swEnd=e=>{delete swb.dataset.drag};swb.addEventListener("pointerup",swEnd);swb.addEventListener("pointercancel",swEnd);
swb.addEventListener("keydown",e=>{const st=e.shiftKey?.1:.02;if(e.key==="ArrowLeft"||e.key==="ArrowDown"){setSwipe(swf-st)}else if(e.key==="ArrowRight"||e.key==="ArrowUp"){setSwipe(swf+st)}else if(e.key==="Home"){setSwipe(0)}else if(e.key==="End"){setSwipe(1)}else return;e.preventDefault()});
function viewHook(){const r=svg.getBoundingClientRect(),ppu=(r.width||W)/vb[2];
 if(mode==="swipe"){const x=vb[0]+swf*vb[2];const a=$("swr"),b=$("swrL");a.setAttribute("x",x);a.setAttribute("y",vb[1]-50);a.setAttribute("width",vb[2]*2);a.setAttribute("height",vb[3]+100);
  b.setAttribute("x",vb[0]-vb[2]);b.setAttribute("y",vb[1]-50);b.setAttribute("width",x-vb[0]+vb[2]);b.setAttribute("height",vb[3]+100)}
 $("hatch").setAttribute("patternTransform",`scale(${1/ppu})`)}
// ---- zoom-gated toggles
const GATES=[["lst",1.6],["lloc",3],["lnm",4]];
function streetState(z){GATES.forEach(([id,th])=>{const i=$(id),lab=i.closest("label"),on=z>=th;i.disabled=!on;lab.classList.toggle("dim",!on);lab.querySelector(".zh").hidden=on;i.title=on?"":"Zoom in to use this"});
 stS.style.display=$("lst").checked&&z>=1.6?"":"none";stR.style.display=$("lloc").checked&&z>=3?"":"none";scheduleNames(z>=4&&$("lnm").checked)}
document.querySelectorAll(".zh").forEach(b=>b.onclick=()=>{const th=+b.dataset.z;const z=W/vb[2];if(z<th)zoomAt(th*1.02/z,vb[0]+vb[2]/2,vb[1]+vb[3]/2)});
["lloc","lnm"].forEach(id=>$(id).onchange=updateLabels);
// ---- street names (anchors precomputed from OSM; laid out in screen space with collision culling)
const SL=[];SLBL.split("\n").forEach(l=>{const c=l[0],i=l.indexOf("~"),name=l.slice(1,i);l.slice(i+1).split(" ").forEach(a=>{const[x,y,ang,r]=a.split(",").map(Number);SL.push({c,name,x:((x-1229300)/1e4-lon0)*kx*S,y:(lat1-(y+454300)/1e4)*S,a:ang,r:r*10})})});
SL.sort((p,q)=>"str".indexOf(p.c)-"str".indexOf(q.c)||q.r-p.r);
let nmOn=false,nmReg=null,nmRaf=0;
function scheduleNames(on){nmOn=on;if(!on){gStN.replaceChildren();nmReg=null;return}if(!nmRaf)nmRaf=requestAnimationFrame(()=>{nmRaf=0;layoutNames()})}
function layoutNames(){if(!nmOn)return;const r=svg.getBoundingClientRect();if(!r.width)return;const ppu=r.width/vb[2],z=W/vb[2];
 if(nmReg&&Math.abs(ppu/nmReg.ppu-1)<.005&&vb[0]>=nmReg.x0&&vb[1]>=nmReg.y0&&vb[0]+vb[2]<=nmReg.x1&&vb[1]+vb[3]<=nmReg.y1)return;
 const mx=vb[2]*.35,my=vb[3]*.35,R={ppu,x0:vb[0]-mx,y0:vb[1]-my,x1:vb[0]+vb[2]+mx,y1:vb[1]+vb[3]+my};nmReg=R;
 const ppm=ppu*S/111320,placed=[],frag=document.createDocumentFragment();let cnt=0;
 for(const a of SL){if(a.x<R.x0||a.x>R.x1||a.y<R.y0||a.y>R.y1)continue;if(a.c==="r"&&z<5)continue;
  const fs=a.c==="r"?9.5:10.5,w=a.name.length*fs*.58;if(w>a.r*ppm*.9)continue;
  const cx=(a.x-R.x0)*ppu,cy=(a.y-R.y0)*ppu,rad=a.a*Math.PI/180,co=Math.abs(Math.cos(rad)),si=Math.abs(Math.sin(rad)),hw=(w/2+4)*co+(fs/2+3)*si,hh=(w/2+4)*si+(fs/2+3)*co;
  let bad=false;for(const b of placed){if(Math.abs(b[0]-cx)<b[2]+hw&&Math.abs(b[1]-cy)<b[3]+hh){bad=true;break}}if(bad)continue;placed.push([cx,cy,hw,hh]);
  const t=mk("text",{class:"stn"+(a.c==="r"?"":" m"),transform:`translate(${a.x.toFixed(1)} ${a.y.toFixed(1)}) rotate(${-a.a}) scale(${(1/ppu).toFixed(5)})`,dy:".35em","font-size":fs});t.textContent=a.name;frag.append(t);if(++cnt>=350)break}
 gStN.replaceChildren(frag)}
setSwipe(.5);

function initCompare(){p1="T";p2="PA";$("sel1").value=p1;$("sel2").value=p2;initLoad=true;setMode("overlay");initLoad=false}
