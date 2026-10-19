// PPS boundary options: site map (build/map/site/map.js, assembled by build/map/build_site_map.py).
// Map engine (projection, base layers, pan/zoom, street names, swipe/overlay compare) carried over from map v2
// (pages/pps-walk-redraw-v2.html); plans, levels and per-school data come from META + MAPLV (built from pages/data/site_data.json).
const $=id=>document.getElementById(id);
// school names as on the options / landing / durability pages (numbers audit 2026-10-12: "MLK Jr", not "King"; "Lee", not
// "Sunrise (Lee)"); the map v2 LBL table only keeps its accents
["MLK Jr","Lee","Boise-Eliot/Humboldt"].forEach(n=>delete LBL[n]);
const nm=n=>LBL[n]||n;
const esc=s=>String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const fmt=n=>n==null?"—":Math.round(n).toLocaleString();
const sg=d=>d>0?"+"+fmt(d):d<0?"−"+fmt(-d):"0";
const pct=v=>v==null?"—":Math.round(v*100)+"%";
// d decimals, rounded half-up on the decimal value (0.975 → "0.98"), as the landing page; never toFixed on data
const fx=(v,d)=>v==null?"—":Number(v).toLocaleString("en-US",{minimumFractionDigits:d,maximumFractionDigits:d});
const src=(p,txt)=>p?`<a href="../${esc(p)}">${esc(txt||p.split("/").pop())}</a>`:"";
const dec=s=>s.split("|").map(rr=>{let X=0,Y=0;return rr.trim().split(" ").map((p,i)=>{const[a,b]=p.split(",").map(Number);if(i===0){X=a;Y=b}else{X+=a;Y+=b}return[(X-1229300)/1e4,(Y+454300)/1e4]})});
const lon0=-122.865,lon1=-122.545,lat0=45.428,lat1=45.66,kx=Math.cos(45.54*Math.PI/180),S=1000/((lon1-lon0)*kx);
const W=1000,H=Math.round((lat1-lat0)*S);
const P=([x,y])=>((x-lon0)*kx*S).toFixed(1)+","+((lat1-y)*S).toFixed(1);
const NS="http://www.w3.org/2000/svg";const mk=(t,a)=>{const e=document.createElementNS(NS,t);for(const k in a)e.setAttribute(k,a[k]);return e};
const svg=$("map");   // aspect ratio and viewBox: see "pan / zoom" (pickAR / fitVB)
const G=()=>mk("g");
const gA=G(),gA2=G(),gFade=G(),gPin=G(),gPast=G(),gSt=G(),gPri=G(),gRail=G(),gRiv=G(),gFwy=G(),gE1=G(),gE2=G(),gB=G(),gCur=G(),gOv=G(),gDiff=G(),gFoc=G(),gStN=G(),gS=G(),gTop=G();
{const defs=mk("defs");const c1=mk("clipPath",{id:"swc"});c1.append(mk("rect",{id:"swr",x:0,y:0,width:1,height:1}));const c2=mk("clipPath",{id:"swcL"});c2.append(mk("rect",{id:"swrL",x:0,y:0,width:1,height:1}));
 // rev7 (declutter): the change hatch is quiet: 8px apart, hairline, faint (it covered much of the map at 6px / 60%)
 const pt=mk("pattern",{id:"hatch",patternUnits:"userSpaceOnUse",width:8,height:8});pt.append(mk("path",{d:"M-1,1 L1,-1 M0,8 L8,0 M7,9 L9,7",class:"hatchl",style:"fill:none"}));
 // size colors: exempt schools (not counted in the target-range figure) = neutral fill + light dots
 const ex=mk("pattern",{id:"exh",patternUnits:"userSpaceOnUse",width:6,height:6});ex.append(mk("rect",{width:6,height:6,style:"fill:var(--sz-in)"}),mk("circle",{cx:3,cy:3,r:.9,style:"fill:var(--muted);opacity:.7"}));
 defs.append(c1,c2,pt,ex);svg.append(defs)}
[gFade,gPin,gSt,gPri,gRail,gRiv,gFwy,gCur,gOv,gFoc,gStN].forEach(g=>g.setAttribute("pointer-events","none"));gFwy.setAttribute("class","fwyg");
svg.append(gA,gA2,gFade,gPast,gSt,gPri,gRail,gRiv,gFwy,gE1,gE2,gB,gCur,gOv,gDiff,gFoc,gStN,gS,gTop,gPin);
const lines=s=>dec(s).filter(r=>r.length>1).map(r=>"M"+r.map(P).join("L")).join("");
const ringsD=enc=>dec(enc).map(r=>"M"+r.map(P).join("L")+"Z").join("");
const base={};BASE.split("\n").forEach(l=>{const i=l.indexOf("#");base[l.slice(0,i)]=l.slice(i+1)});
const fwyD=lines(base.motorway)+lines(base.trunk);
// collector + local streets and the street-name anchors are shared by every level and plan, so they live in their own
// cached files (map_data/streets.js, map_data/street_names.js): streets load once the page is up, names only when zoomed in
const lazyJS=(()=>{const st={};return(f,cb)=>{const s=st[f]||(st[f]={cbs:[],ok:false});if(s.ok)return cb();s.cbs.push(cb);if(s.el)return;
 s.el=document.createElement("script");s.el.src=`map_data/${f}?v=${SVER}`;s.el.onload=()=>{s.ok=true;s.cbs.splice(0).forEach(c=>c())};s.el.onerror=()=>{s.el=null;s.cbs.length=0};document.head.append(s.el)}})();
let stS=null,stR=null;
function streetsReady(){if(stS||!window.STREETS)return;const stD={};STREETS.split("\n").forEach(l=>{const i=l.indexOf("#");stD[l.slice(0,i)]=l.slice(i+1)});
 stS=mk("path",{d:lines(stD.s)+lines(stD.t),fill:"none",stroke:"var(--pri)","stroke-width":"1.1","stroke-opacity":"0.9","vector-effect":"non-scaling-stroke"});
 stR=mk("path",{d:lines(stD.r),fill:"none",stroke:"var(--pri)","stroke-width":"0.6","stroke-opacity":"0.6","vector-effect":"non-scaling-stroke"});
 gSt.append(stR,stS);updateLabels()}
gPri.append(mk("path",{d:lines(base.primary),fill:"none",stroke:"var(--pri)","stroke-width":"0.9","vector-effect":"non-scaling-stroke","stroke-opacity":"0.9"}));
gRail.append(mk("path",{d:lines(base.rail),fill:"none",stroke:"var(--rail)","stroke-width":"1.1","stroke-dasharray":"5 3","vector-effect":"non-scaling-stroke","stroke-opacity":"0.75"}));
gRiv.append(mk("path",{d:lines(base.river),fill:"none",stroke:"var(--water)","stroke-width":"7","stroke-linecap":"round","stroke-linejoin":"round","vector-effect":"non-scaling-stroke"}));
gFwy.append(mk("path",{d:fwyD,fill:"none",stroke:"var(--fwy-case)","stroke-width":"4.6","stroke-linejoin":"round","vector-effect":"non-scaling-stroke"}),mk("path",{d:fwyD,fill:"none",stroke:"var(--fwy)","stroke-width":"2.6","stroke-linejoin":"round","vector-effect":"non-scaling-stroke"}));
const outD=dec(OUTL).map(r=>"M"+r.map(P).join("L")+"Z").join("");
// district extent in map units: bbox of every K-5 plan's attendance areas (the outline path reaches well past them), 2% pad;
// the default view fits it and pan/zoom are clamped to it
const EXT=(()=>{let x0=1e9,y0=1e9,x1=-1e9,y1=-1e9;Object.values(MAPLV["K-5"].plans).forEach(pl=>Object.values(pl.poly||{}).forEach(enc=>dec(enc).forEach(r=>r.forEach(p=>{const[x,y]=P(p).split(",").map(Number);if(x<x0)x0=x;if(x>x1)x1=x;if(y<y0)y0=y;if(y>y1)y1=y}))));
 const m=Math.max(x1-x0,y1-y0)*.02;return[x0-m,y0-m,x1+m,y1+m]})();
gB.append(mk("path",{d:`M-3000,-3000H4000V4000H-3000Z`+outD,class:"beyond","fill-rule":"evenodd"}),mk("path",{d:outD,class:"outline","vector-effect":"non-scaling-stroke"}));
const near=(set,lon,lat,tol)=>{let best=null,bd=tol*tol;set.forEach(r=>r.forEach(p=>{const d=((p[0]-lon)*kx)**2+(p[1]-lat)**2;if(d<bd){bd=d;best=p}}));return best};
const fwyPts=[...dec(base.motorway),...dec(base.trunk)];
[["5",-122.684,45.585],["5",-122.694,45.474],["84",-122.615,45.533],["405",-122.687,45.524],["205",-122.566,45.535],["26",-122.735,45.508]].forEach(([n,lo,la])=>{const p=near(fwyPts,lo,la,0.012);if(!p)return;const[x,y]=P(p).split(",").map(Number);
 const g=mk("g",{class:"shield","data-x":x,"data-y":y});const w=n.length>2?29:n==="26"?42:21;g.append(mk("rect",{x:-w/2,y:-8.5,width:w,height:17,rx:4,"stroke-width":"1.5"}));const tx=mk("text",{x:0,y:0.5});tx.textContent=n==="26"?"US 26":n;g.append(tx);gTop.append(g)});
(()=>{const p=near(dec(base.river),-122.667,45.507,0.02);if(!p)return;const[x,y]=P(p).split(",").map(Number);const t=mk("text",{class:"wlbl","data-x":x+8,"data-y":y,x:x+8,y:y});t.textContent="Willamette";gTop.append(t)})();

// ---- plans, levels
const PM={};META.plans.forEach(p=>PM[p.k]=p);
const ORD=META.plans.map(p=>p.k);
const LVN={"K-5":"K–5","6-8":"6–8","9-12":"9–12"};
const BASELINE="status_quo";   // the one baseline: PPS Status Quo (2027-28, no closures) (Today archived)
let lv="K-5",mode="single",scn="scenario_A",p1=BASELINE,p2="scenario_A",sel=null,swf=.5,showHatch=true,wk="S",initLoad=false,pin=null;
const LD=()=>MAPLV[lv];
const PD=k=>LD().plans[k];
const polysOf=k=>(PD(k)||{}).poly||{};
const avail=()=>ORD.filter(k=>LD().plans[k]);
const isOpt=k=>PM[k]&&PM[k].kind==="option";
const lblShort=k=>PM[k]?PM[k].short:k;
const lblFull=k=>PM[k]?(PM[k].full||PM[k].short)+(isOpt(k)?` (${PM[k].ver})`:PM[k].lines==="official"&&k!==BASELINE?" (PPS lines)":""):k;
const LEAD=(META.plans.find(p=>p.rank===0)||{k:"option2_ms460"}).k;   // the best example we modeled (site_data brief_rank 0: option2_ms460, "Boundary changes, balanced middle schools")
const leadT=k=>k===LEAD?`<span class="lead" title="The best example we modeled">best we modeled</span>`:isWif(k)?`<span class="lead wif" title="A what-if, not one of the example plans">what-if</span>`:"";
const isWif=k=>!!(PM[k]&&PM[k].whatif);
const isReq=k=>!!(PM[k]&&PM[k].req);   // requested runs (pages/requests.html): their own group in the plan lists
const vtag=k=>(isOpt(k)?`<span class="vtag" title="The model version that produced this example plan">${esc(PM[k].ver)}</span>`:`<span class="vtag off" title="PPS's own lines, traced from its published maps">PPS's official lines</span>`)+leadT(k);
const SCH=()=>LD().sch;
// optional per-option caveat (site_data options[].caveat): side panel + plan menu tooltip; nothing when absent
const cavOf=k=>{const c=(PM[k]&&PM[k].caveat)||"",m=c.match(/\b(K-5|6-8|9-12)\b/g);return !m||m.includes(lv)?c:""};   // a caveat that names grade levels shows only at those levels (Lent: K-5)
const cav=(k,named)=>cavOf(k)?`<p class="caveat">${named?`<b>${esc(lblShort(k))}:</b> `:""}${esc(cavOf(k))}</p>`:"";
function cavTitles(){[["sel0",scn],["sel1",p1],["sel2",p2]].forEach(([id,k])=>{const s=$(id);if(!s)return;const c=cavOf(k);if(c)s.title=c;else s.removeAttribute("title")})}
const cmpOn=()=>mode!=="single";

// colors: greedy colouring over neighbours found by sampling along every edge (straight street edges have few vertices)
const PAL=8,colOf={};
function colorize(polys){const names=Object.keys(polys),pts={};const tol=0.0012;
 names.forEach(n=>{const out=[];dec(polys[n]).forEach(r=>{for(let i=0;i<r.length;i++){const a=r[i],b=r[(i+1)%r.length];const dx=(b[0]-a[0])*kx,dy=b[1]-a[1];const k=Math.max(1,Math.ceil(Math.hypot(dx,dy)/(tol*.8)));for(let j=0;j<k;j++)out.push([(a[0]+(b[0]-a[0])*j/k)*kx,a[1]+(b[1]-a[1])*j/k])}});pts[n]=out});
 const cell=k=>Math.floor(k/tol),grid=new Map();names.forEach(n=>pts[n].forEach(([x,y])=>{const k=cell(x)+":"+cell(y);if(!grid.has(k))grid.set(k,new Set());grid.get(k).add(n)}));
 const adj={};names.forEach(n=>adj[n]=new Set());names.forEach(n=>pts[n].forEach(([x,y])=>{for(let i=-1;i<=1;i++)for(let j=-1;j<=1;j++){const s=grid.get((cell(x)+i)+":"+(cell(y)+j));if(s)s.forEach(m=>{if(m!==n){adj[n].add(m);adj[m].add(n)}})}}));
 const used=Array(PAL).fill(0),out={};[...names].sort((a,b)=>adj[b].size-adj[a].size||a.localeCompare(b)).forEach(n=>{const bad=new Set([...adj[n]].map(m=>out[m]));let best=-1;for(let c=0;c<PAL;c++)if(!bad.has(c)&&(best<0||used[c]<used[best]))best=c;if(best<0)best=0;out[n]=best;used[best]++});return out}
function colsFor(a,b){const k=lv+"|"+a+"|"+(b||"");if(colOf[k])return colOf[k];if(!b)return colOf[k]=colorize(polysOf(a));
 const pa=polysOf(a),pb=polysOf(b),m={};new Set([...Object.keys(pa),...Object.keys(pb)]).forEach(n=>{m[n]=[pa[n],pb[n]].filter(Boolean).join("|")});return colOf[k]=colorize(m)}
// "Color areas by" = the map's ONE theme (one encoding at a time, each with its own key and panel list):
// "" school colors · "chg" changes only (plain fill; the lines and the hatch carry it) · "size" size vs target range (2031-32)
// · "past" past a closer school (plain fill + the past regions) · "race" racial mix
const colBy=()=>$("lcol").value,dvOn=()=>colBy()==="race",szOn=()=>colBy()==="size",pastOn=()=>colBy()==="past";
// schools at target, 2031-32, as on the options and landing pages (scorecard durability: zoned, non-exempt schools)
const durOf=k=>(PD(k)||{}).dur;
const szCls=(k,n)=>{const d=durOf(k);if(!d)return null;const x=d.s[n];return x?x[1]:"x"};   // -1 under floor, 0 at target, 1 over ceiling, "x" exempt
const SZF={"-1":"var(--sz-u)","0":"var(--sz-in)","1":"var(--sz-o)",x:"url(#exh)"};
const szCount=k=>{const d=durOf(k),c={"-1":0,"0":0,"1":0,x:0};if(!d)return c;Object.keys(polysOf(k)).forEach(n=>c[szCls(k,n)]++);return c};
const dvFill=q=>{if(q==null)return"var(--beyond)";const d=q-LD().kocd,a=Math.min(1,Math.abs(d)/25);return `color-mix(in srgb,var(${d<0?"--lo":"--hi"}) ${Math.round(8+a*82)}%,var(--plate))`};
const fillStyle=(plan,n,cols)=>{const t=colBy();return t==="race"?`fill:${dvFill((PD(plan).koc||{})[n])}`:t==="size"?`fill:${SZF[szCls(plan,n)]||"var(--beyond)"}`:t?"fill:var(--sz-in)":`fill:var(--c${cols[n]})`};
const EXT_T='title="Astor and Skyline: small K-8s PPS keeps below the floor in every scenario, so they are not counted"';
// size key with counts for the plan(s) whose fill is on screen (overlay: plan 1, with plan 2's count and a switch to swipe)
function szLegend(){const el=$("szl");el.hidden=!szOn();if(!szOn())return;const ks=!cmpOn()?[scn]:mode==="swipe"?[p1,p2]:[p1];
 const sw=c=>`<i class="szsw ${c}"></i>`,row=(k,i)=>{const d=durOf(k);if(!d)return `<span>${esc(lblShort(k))}: no size data</span>`;const c=szCount(k);
  return `<span class="szrow">${ks.length>1?`<b>${i?"Right":"Left"}, ${esc(lblShort(k))}:</b>`:`<b>${esc(lblShort(k))}:</b>`} <span>${sw("u")}Under floor ${c["-1"]}</span> <span>${sw("in")}At target ${c["0"]}</span> <span>${sw("o")}Over ceiling ${c["1"]}</span>${c.x?` <span ${EXT_T}>${sw("x")}Exempt, not counted ${c.x}</span>`:""}</span>`};
 const ov=cmpOn()&&mode==="overlay"&&p1!==p2,d2=durOf(p2);
 el.innerHTML=`<span class="szh">School size vs target range (floor to ceiling), ${LVN[lv]}, 2031-32 (model).</span>`+ks.map(row).join("")+
  (ov?`<span class="szh">Colors show plan 1 only. ${esc(lblShort(p2))} (plan 2): ${d2?`${d2.at} of ${d2.n}`:"—"} at target. <button type="button" class="lnk" id="toswipe">Swipe to see both</button></span>`:"")}

// ---- program-only schools
const PROGTXT={"Cesar Chavez":["Focused K-5 regional Spanish DLI school; neighborhood (non-DLI) K-5 students move to Rosa Parks","PPS Family Guide, César Chávez, p.3"],
 "Lent":["Remains a focused K-5 Spanish DLI school; neighborhood boundary moves to Kelly","PPS Family Guide, Lent, p.3"],
 "Rigler":["Focused regional Spanish DLI K-5 school; non-DLI neighborhood boundary shifts to Scott","PPS Family Guide, Rigler, p.3"]};
function progList(plan){const pd=PD(plan);if(!pd)return[];return pd.prog.filter(p=>SCH()[p[0]]&&!polysOf(plan)[p[0]]).map(p=>({n:p[0],kids:p[1]}))}
function progTxt(plan,p){const pps=(plan==="scenario_A"||plan==="scenario_B")&&PROGTXT[p.n]&&lv==="K-5";const proj=(META.ppsproj[plan]||{})[p.n];
 if(pps)return `${nm(p.n)} (Spanish DLI focus) — ${PROGTXT[p.n][0]}${proj!=null?` · PPS projection, 2031-32: ${fmt(proj)}`:""} · Source: ${PROGTXT[p.n][1]}`;
 return `${nm(p.n)} — no neighborhood area at ${LVN[lv]} in ${lblShort(plan)}; program students only${p.kids!=null?` (${fmt(p.kids)} modeled, 2031-32)`:""}`}
function progMarkers(g,plan,skip){progList(plan).forEach(p=>{if(skip&&skip.has(p.n))return;const[x,y]=P(SCH()[p.n]).split(",");const txt=progTxt(plan,p);
  const c=mk("circle",{cx:x,cy:y,r:5,fill:"var(--cmp)",stroke:"var(--ink)","stroke-width":"1.8","vector-effect":"non-scaling-stroke","data-x":x,"data-y":y,"data-rm":"1.5",role:"img","aria-label":txt,class:"progm","data-tip":txt});g.append(c);
  const t=mk("text",{x:+x+6,y:+y+4,class:"lbl","data-x":x,"data-y":y,"data-n":p.n,"data-rm":"1.5"});t.textContent=nm(p.n);g.append(t)})}
function progPanel(){const blk=pl=>{const L=progList(pl);return L.length?`<p class="hint" style="color:var(--ink)"><b>${esc(lblShort(pl))}</b></p><ul class="proglist">${L.map(p=>`<li>${esc(progTxt(pl,p))}</li>`).join("")}</ul>`:""};
 const cite=pl=>PM[pl]&&PM[pl].schools?`<p class="cite">Program counts: ${src(PM[pl].schools,"schools.csv")} (prog_${lv}).</p>`:"";
 if(!cmpOn()){const b=blk(scn);return b?`<div class="from progbox"><div class="tag">Program-only schools</div>${b}${cite(scn)}</div>`:""}
 const a=progList(p1),b=progList(p2),pol1=polysOf(p1),pol2=polysOf(p2);let h="";
 const lost=b.filter(p=>pol1[p.n]),gained=a.filter(p=>pol2[p.n]);
 if(lost.length)h+=`<p class="hint" style="color:var(--ink)">${lost.map(p=>nm(p.n)).join(", ")} ${lost.length>1?"go":"goes"} from having a neighborhood area in ${esc(lblShort(p1))} to program-only in ${esc(lblShort(p2))}.</p>`;
 if(gained.length)h+=`<p class="hint" style="color:var(--ink)">${gained.map(p=>nm(p.n)).join(", ")} ${gained.length>1?"go":"goes"} from program-only in ${esc(lblShort(p1))} to having a neighborhood area in ${esc(lblShort(p2))}.</p>`;
 const x=blk(p1)+(p1===p2?"":blk(p2));return(h||x)?`<div class="from progbox"><div class="tag">Program-only schools</div>${h}${x}${cite(p2)}</div>`:""}

// ---- drawing
// keyboard: the areas are ONE tab stop (roving tabindex: the selected area, else the first); arrow keys move focus to the
// nearest area in that direction, Enter/Space select it; focus pans the area into view and draws a ring above the lines
function drawPlan(g,ge,plan,cols,tab){const polys=polysOf(plan);let all="";
 Object.entries(polys).forEach(([n,enc])=>{const d=ringsD(enc);all+=d;const sw=szOn()?sizeWord(plan,n):"";
  // data-tip: the hover / tap name (one delegated handler, tipAt, reads every data-tip under the pointer)
  const p=mk("path",{d,class:"area"+(n===sel?" sel":""),"fill-rule":"evenodd","data-n":n,tabindex:"-1",role:tab?"button":"presentation","aria-label":nm(n)+sw,"data-tip":nm(n)+(cmpOn()?` (${lblShort(plan)})`:"")+sw});
  p.setAttribute("style",fillStyle(plan,n,cols));p.addEventListener("click",()=>select(n));
  if(tab){p.addEventListener("keydown",areaKey);p.addEventListener("focus",()=>areaFocus(p));p.addEventListener("blur",()=>{gFoc.replaceChildren();hideTip()})}g.append(p)});
 if(tab)rove();ge.append(mk("path",{d:all,class:"edge"}));selEdge(ge,polys[sel])}
const sizeWord=(k,n)=>({"-1":", under its target floor","0":", at target","1":", over its target ceiling",x:", exempt from the target"})[szCls(k,n)]||"";
function rove(){const L=[...gA.querySelectorAll(".area")];if(!L.length)return;const t=L.find(p=>p.dataset.n===sel)||L.find(p=>p.dataset.n===rove.last)||L[0];L.forEach(p=>p.setAttribute("tabindex",p===t?"0":"-1"))}
// keyboard focus: dashed ring above the lines, the area panned into view, the map scrolled into the window, and the name shown
function areaFocus(p){rove.last=p.dataset.n;gA.querySelectorAll(".area").forEach(x=>x.setAttribute("tabindex",x===p?"0":"-1"));
 if(!p.matches(":focus-visible"))return;   // mouse/touch clicks also focus the path: no ring or pan for those
 gFoc.replaceChildren(mk("path",{d:p.getAttribute("d"),class:"focc","fill-rule":"evenodd"}),mk("path",{d:p.getAttribute("d"),class:"focr","fill-rule":"evenodd"}));
 const b=p.getBBox();if(b.x<vb[0]||b.y<vb[1]||b.x+b.width>vb[0]+vb[2]||b.y+b.height>vb[1]+vb[3]){vb[0]=b.x+b.width/2-vb[2]/2;vb[1]=b.y+b.height/2-vb[3]/2;setVB()}
 document.querySelector(".mapbox").scrollIntoView({block:"nearest"});
 const r=svg.getBoundingClientRect(),cx=Math.max(vb[0],Math.min(vb[0]+vb[2],b.x+b.width/2)),cy=Math.max(vb[1],Math.min(vb[1]+vb[3],b.y+b.height/2));
 showTip({clientX:r.left+(cx-vb[0])/vb[2]*r.width,clientY:r.top+(cy-vb[1])/vb[3]*r.height},p.dataset.tip)}
function areaKey(e){const p=e.currentTarget;if(e.key==="Enter"||e.key===" "){e.preventDefault();select(p.dataset.n);return}
 const D={ArrowRight:[1,0],ArrowLeft:[-1,0],ArrowDown:[0,1],ArrowUp:[0,-1]}[e.key];if(!D)return;e.preventDefault();
 const c=q=>{const b=q.getBBox();return[b.x+b.width/2,b.y+b.height/2]},[x0,y0]=c(p);let best=null,bs=1e18;
 gA.querySelectorAll(".area").forEach(q=>{if(q===p)return;const[x,y]=c(q),dx=x-x0,dy=y-y0,along=dx*D[0]+dy*D[1];if(along<=0)return;const off=Math.abs(dx*D[1]-dy*D[0]),sc=along+2.5*off;if(sc<bs){bs=sc;best=q}});
 if(best)best.focus()}
function selEdge(g,enc){if(!sel||!enc)return;const d=ringsD(enc);g.append(mk("path",{d,class:"edge selc","data-sel":"1"}),mk("path",{d,class:"edge sel","data-sel":"1"}))}
function drawSchools(g,plan,color){Object.keys(polysOf(plan)).forEach(n=>{const s=SCH()[n];if(!s)return;const[x,y]=P(s).split(",");
  g.append(mk("circle",{cx:x,cy:y,r:3.5,fill:"var(--plate)",stroke:color||"var(--ink)","stroke-width":"1.8","vector-effect":"non-scaling-stroke","data-x":x,"data-y":y}));
  const t=mk("text",{x:+x+6,y:+y+4,class:"lbl","data-x":x,"data-y":y,"data-n":n});t.textContent=nm(n);g.append(t)});progMarkers(g,plan)}
function drawCur(){gCur.replaceChildren();const t=PD(BASELINE);if(!t)return;
 gCur.append(mk("path",{d:Object.values(t.poly).map(ringsD).join(""),fill:"none",stroke:"var(--cur)","stroke-width":"1","stroke-opacity":"0.6","stroke-linejoin":"round","vector-effect":"non-scaling-stroke"}));
 $("lgCurT").textContent=`PPS Status Quo ${LVN[lv]} lines`}
function curVis(){const t=cmpOn()?(p1===BASELINE||p2===BASELINE):scn===BASELINE;gCur.style.display=(!t&&$("lcur").checked)?"":"none";$("lcurw").hidden=t;$("lgCur").hidden=t||!$("lcur").checked}
// past a closer school, one plan (single, and each side of swipe): violet tint + dashed outline; hover / tap names the move
const pastTip=(plan,r,pre)=>`${pre?lblShort(plan)+": ":""}${nm(r[0])} · ${fmt(r[2])} kids · nearer: ${nm(r[1])}`;
function pastLayer(g,plan,pre){const pd=PD(plan);if(!pd)return;pd.past.regs.forEach(r=>{if(!r[3])return;const txt=`${lblShort(plan)}: about ${fmt(r[2])} ${LVN[lv]} kids assigned to ${nm(r[0])} live at least ${pd.past.margin} mi closer (on foot) to ${nm(r[1])}`;
  const p=mk("path",{d:ringsD(r[3]),"fill-rule":"evenodd",class:"pastm",role:"img","aria-label":txt,"data-tip":pastTip(plan,r,pre)});   // not a tab stop: the side panel lists the same counts
  p.addEventListener("click",()=>select(r[0]));g.append(p)})}
// overlay, past theme: the two plans' regions as a DIFFERENCE : fixed by plan 2 (plan 1 only) = blue fill,
// new under plan 2 (plan 2 only) = crimson fill of the same weight (round 5: the old teal fill vs sparse orange dots read as
// tilted toward plan 2, and the orange sat on the freeway hue), under both = violet dashed outline. Drawn with SVG masks / clips of the two
// plans' regions; the kid counts come per block from the build (pairs[...].px). Transparent per-region paths carry the tips.
function pastPair(){const R=k=>PD(k).past.regs.filter(r=>r[3]),r1=R(p1),r2=R(p2),defs=svg.querySelector("defs"),big={x:-3000,y:-3000,width:7000,height:7000};
 ["pmA","pmB","pcA","pcB"].forEach(id=>{const o=$(id);if(o)o.remove()});
 const paths=(L,a)=>L.map(r=>mk("path",Object.assign({d:ringsD(r[3]),"fill-rule":"evenodd","clip-rule":"evenodd"},a||{})));
 const mask=(id,L)=>{const m=mk("mask",Object.assign({id,maskUnits:"userSpaceOnUse"},big));m.append(mk("rect",Object.assign({fill:"#fff"},big)),...paths(L,{fill:"#000",stroke:"#000","stroke-width":".3"}));return m};
 const clip=(id,L)=>{const c=mk("clipPath",{id});c.append(...paths(L));return c};
 defs.append(mask("pmA",r2),mask("pmB",r1),clip("pcA",r1),clip("pcB",r2));
 const grp=(cls,L,a)=>{const g=mk("g",Object.assign({class:cls,"pointer-events":"none"},a));g.append(...paths(L));return g};
 gPast.append(grp("pfix",r1,{mask:"url(#pmA)"}),grp("pnew",r2,{mask:"url(#pmB)"}),grp("pboth",r1,{"clip-path":"url(#pcB)"}),grp("pboth l",r2,{"clip-path":"url(#pcA)"}));
 [[p1,r1],[p2,r2]].forEach(([k,L])=>L.forEach(r=>{const p=mk("path",{d:ringsD(r[3]),"fill-rule":"evenodd",class:"pasthit","data-pp":k===p1?"1":"2","data-tip":pastTip(k,r,true)});p.addEventListener("click",()=>select(r[0]));gPast.append(p)}))}
// past kids by assigned school, one plan (from the drawn and undrawn regions: every block counted)
// (round 6: the build's per-school counts, largest-remainder rounded so the rows add up to the scorecard total exactly)
const pastBy=k=>{const p=(PD(k)||{past:{regs:[]}}).past;if(p.by)return Object.assign({},p.by);const o={};p.regs.forEach(r=>o[r[0]]=(o[r[0]]||0)+r[2]);return o};
const pastN=k=>fmt((PD(k)||{past:{}}).past.n);
// plan 2's line, in words (rev7: one dashed magenta stroke at every width)
const W2='magenta dashed lines',W2s='magenta dashed lines';
// the theme key (top of the side panel): what the fill, lines and marks mean right now
function themeKey(){const c=cmpOn(),sw=c2=>`<i class="pastsw${c2}"></i>`,I=c?pairInfo(p1,p2):null;
 $("lgP").innerHTML=!pastOn()?"":!c?`<span>${sw("")}Sent to a farther school, ${esc(lblShort(scn))}: ${pastN(scn)} kids</span>`:mode==="swipe"||!I?`<span>${sw("")}Sent to a farther school (left: ${esc(lblShort(p1))} ${pastN(p1)} kids; right: ${esc(lblShort(p2))} ${pastN(p2)})</span>`:
  `<span class="pxh">Sent to a farther school: ${esc(lblShort(p1))} ${pastN(p1)} kids → ${esc(lblShort(p2))} ${pastN(p2)}</span><span>${sw(" fix")}Fixed by ${esc(lblShort(p2))}: ${fmt(I.px[0])}</span> <span>${sw(" new")}New under ${esc(lblShort(p2))}: ${fmt(I.px[1])}</span> <span>${sw(" both")}Under both: ${I.px[2]===I.px[3]?`${fmt(I.px[3])} kids in either plan`:`${fmt(I.px[2])} kids in ${esc(lblShort(p1))}, ${fmt(I.px[3])} in ${esc(lblShort(p2))}`}</span>`+
  `<span class="pxn">Fixed + both = ${pastN(p1)} (${esc(lblShort(p1))} total); new + both = ${pastN(p2)} (${esc(lblShort(p2))} total).${I.px[2]!==I.px[3]?" Each plan counts its own neighborhood kids (program kids differ), so “both” differs a little.":""}</span>`;
 const n=$("cnote");n.hidden=!c;if($("lgO1T"))$("lgO1T").parentNode.hidden=sameLn();
 if(c)n.innerHTML=(mode==="swipe"?`Left of the handle: ${esc(lblShort(p1))} (plan 1); right: ${esc(lblShort(p2))} (plan 2). Drag it, or use the arrow keys.`:sameLn()?`Same lines: no kid changes school between ${esc(lblShort(p1))} and ${esc(lblShort(p2))}, so the ${W2} show both plans' boundaries; fill: ${esc(lblShort(p1))}. (Plan 1's own line is hidden: the two tracings differ slightly along the river and the district edge, where no kids live.)`:`Fill and thin solid lines: ${esc(lblShort(p1))} (plan 1). ${W2.replace("magenta","Magenta")}: ${esc(lblShort(p2))} (plan 2).`)+" Tap any spot to see its school under every plan."}
// overlay of two plans with the same lines (no kid changes school, e.g. most 9-12 pairs): plan 1's dark line is hidden
const sameLn=()=>{if(!cmpOn()||mode!=="overlay"||p1===p2)return false;const I=pairInfo(p1,p2);return !!I&&!I.n};
function pairInfo(a,b){if(a===b)return null;const i=ORD.indexOf(a),j=ORD.indexOf(b);const fwd=i<j;const D=LD().pairs[fwd?a+"|"+b:b+"|"+a];
 if(!D)return null;const x=D.px||[0,0,0,0];return{n:D.n,tot:D.tot,regs:D.regs.map(r=>fwd?r:[r[1],r[0],r[2],r[3]]),km2:D.km2,flows:D.flows.map(f=>fwd?f:[f[1],f[0],f[2]]),px:fwd?x:[x[1],x[0],x[3],x[2]]}}
// schools whose names show even zoomed out: the ones the current theme is about (changed most, off target, most past)
let IMP=new Map(),IMPS={};
// swipe: each side gets its own plan's list (round 6, review4 #9: plan 1's flagged schools were named on plan 2's side too)
function impSet(){const sw=mode==="swipe"&&p1!==p2;IMPS=sw?{L:impFor([p1],true),R:impFor([p2],true)}:{};IMP=sw?new Map([...IMPS.L,...IMPS.R]):impFor(null,false)}
function impFor(side,sw){const m=new Map(),add=L=>L.slice(0,12).forEach((n,i)=>{if(!m.has(n))m.set(n,i)}),top=(o,min)=>Object.keys(o).filter(n=>Math.abs(o[n])>=min).sort((x,y)=>Math.abs(o[y])-Math.abs(o[x]));
 const dif=(a,b)=>{const o={};new Set([...Object.keys(a),...Object.keys(b)]).forEach(n=>o[n]=(b[n]||0)-(a[n]||0));return o},two=cmpOn()&&p1!==p2;
 if(szOn())add((side||(cmpOn()?[p1]:[scn])).flatMap(k=>{const d=durOf(k);return d?Object.keys(d.s).filter(n=>d.s[n][1]):[]}));
 else if(pastOn())add(sw?top(pastBy(side[0]),40):two?top(dif(pastBy(p1),pastBy(p2)),40):top(pastBy(cmpOn()?p1:scn),40));
 else if(two)add(top(dif(PD(p1).size,PD(p2).size),100));
 return m}
// the change hatch belongs to the School colors and Changes only themes (round 5: it cluttered past, size and racial mix)
const hatchTheme=()=>colBy()===""||colBy()==="chg",hatchOn=()=>showHatch&&hatchTheme();
function drawAreas(){hideTip();[gA,gA2,gFade,gS,gDiff,gOv,gPast,gE1,gE2,gFoc].forEach(g=>g.replaceChildren());cavTitles();
 const c=cmpOn(),a=c?p1:scn;const polys=polysOf(a);const cols=c?colsFor(p1,p2):colsFor(scn);
 curVis();
 drawPlan(gA,gE1,a,cols,true);drawSchools(gS,a);
 if(c&&mode==="overlay")gE1.querySelectorAll(".edge:not([data-sel])").forEach(e=>{e.classList.add("p1");if(sameLn())e.style.display="none"});
 [gS,gA2,gE1,gE2,gPast].forEach(g=>g.removeAttribute("clip-path"));
 $("lgP").hidden=!pastOn();
 if(pastOn()){if(mode==="swipe"){const L=G(),R=G();pastLayer(L,p1,true);pastLayer(R,p2,true);L.setAttribute("clip-path","url(#swcL)");R.setAttribute("clip-path","url(#swc)");gPast.append(L,R)}
  else if(c&&p1!==p2&&pairInfo(p1,p2))pastPair();else pastLayer(gPast,a)}
 themeKey();szLegend();
 let I=null;
 if(c){const polys2=polysOf(p2);
  if(mode==="swipe"){drawPlan(gA2,gE2,p2,cols,false);gA2.setAttribute("clip-path","url(#swc)");gE2.setAttribute("clip-path","url(#swc)");gE1.setAttribute("clip-path","url(#swcL)");
   const g1=G(),g2=G();g1.dataset.side="L";g2.dataset.side="R";gS.replaceChildren(g1,g2);drawSchools(g1,p1);drawSchools(g2,p2);g1.setAttribute("clip-path","url(#swcL)");g2.setAttribute("clip-path","url(#swc)")}
  else{const d=Object.values(polys2).map(ringsD).join("");
   // rev7 (declutter): plan 2 = ONE magenta dashed stroke over plan 1's thin solid line (was a cased double line that read
   // as chaos). Hue and dash both differ (colorblind-safe); where the two plans share a line the dashes sit on the solid line.
   gOv.append(mk("path",{d,class:"ov2m",fill:"none",stroke:"var(--cmp)","stroke-width":"2.4","stroke-dasharray":"7 4","stroke-linejoin":"round","vector-effect":"non-scaling-stroke"}));
   const g2=G();gS.append(g2);progMarkers(g2,p2,new Set(progList(p1).map(p=>p.n)));Object.keys(polys2).forEach(n=>{if(polys[n])return;const s=SCH()[n];if(!s)return;const[x,y]=P(s).split(",");
    g2.append(mk("circle",{cx:x,cy:y,r:3.5,fill:"var(--plate)",stroke:"var(--cmp)","stroke-width":"1.8","vector-effect":"non-scaling-stroke","data-x":x,"data-y":y}));
    const t=mk("text",{x:+x+6,y:+y+4,class:"lbl","data-x":x,"data-y":y,"data-n":n});t.textContent=nm(n);g2.append(t)})}
  I=pairInfo(p1,p2);if(I){const pd=r=>ringsD(r[3]);
   if(hatchOn()&&I.regs.length)gDiff.append(mk("path",{d:I.regs.map(pd).join(""),"fill-rule":"evenodd",fill:"url(#hatch)","pointer-events":"none"}));
   // changed areas: invisible hover/tap targets (no fade/highlight; the two plans' lines carry the comparison)
   I.regs.forEach(r=>{const p=mk("path",{d:pd(r),"fill-rule":"evenodd",fill:"#000","fill-opacity":"0",class:"chg",role:"img","aria-label":`${nm(r[0])} to ${nm(r[1])}, ${r[2]?"about "+fmt(r[2])+" kids in this area":"no kids live in this area"}`,"data-tip":r[2]?`${nm(r[0])} → ${nm(r[1])}: about ${fmt(r[2])} kids in this area move`:`${nm(r[0])} → ${nm(r[1])}: the line moves here, but no kids live in this area (model)`});
    p.addEventListener("click",()=>select(r[0]));gDiff.append(p)})}}
 $("lgH").hidden=!(I&&I.n&&hatchOn());$("lhfw").hidden=!c||!hatchTheme();
 impSet();viewHook();updateLabels();drawPin();
 if(sel&&!polys[sel]&&!(c&&polysOf(p2)[sel]))sel=null;select(sel);
 tables();optInd();hashWrite()}

// ---- side panel (#sidec; the theme key #tkey above it stays put)
function kvs(rows){return `<div class="kv">${rows.filter(Boolean).map(([k,v])=>`<span>${k}</span><span>${v}</span>`).join("")}</div>`}
function bars(list,tag){if(!list||!list.length)return"";const mx=Math.max(1,...list.map(p=>p[1]));return `<div class="from"><div class="tag">${tag}</div>${list.slice(0,8).map(([a,v])=>`<div class="bar"><span>${esc(nm(a))}</span><em>${fmt(v)}</em><s style="width:${Math.round(v/mx*100)}%"></s></div>`).join("")}</div>`}
// district-wide scorecard for one or two plans (each plan's scorecard, PD(k).sum; schools at target from its durability
// block, PD(k).dur, the same figure as the options and landing pages); with two, ✓ marks the better value
const atTxt=k=>{const d=durOf(k);return d?`${d.at} of ${d.n}`+(d.src==="pps"?' <span class="pf">(PPS figures)</span>':""):"—"};   // PPS plans: PPS's own Family Guide figures ; HTML (.pf drops to its own line in the side-panel table, round 8)
function scoreTbl(ks){const bus=(META.levels[lv]||{}).bus_threshold_mi,S=ks.map(k=>Object.assign({_k:k,_d:durOf(k)},PD(k).sum||{})),two=ks.length===2;
 const R=[["Average walk",s=>s.avg_walk_mi,x=>fx(x,2)+" mi",-1],["Kids sent to a farther school",s=>s.kids_past_closer_school,fmt,-1],[lv==="9-12"?`Kids living over ${bus} mi (most ride TriMet)`:`Kids walking over ${bus} mi (bus line)`,s=>s.kids_over_bus_threshold,fmt,-1],
  ["Schools at target, 2031-32",s=>s._d&&s._d.n?s._d.at/s._d.n:null,(x,s)=>atTxt(s._k),1],
  // Status Quo is the baseline for reassignments: its cell reads "–" and the row gets no ✓ when it is one of the pair
  ["Kids moved from their Status Quo school",s=>s._k===BASELINE?null:s.kids_reassigned_vs_status_quo,fmt,ks.includes(BASELINE)?0:-1,s=>s._k===BASELINE?'<span title="the baseline">–</span>':null]];
 return `<table class="dtab score${two||ks.length>1?"":" one"}"><thead><tr><th><span class="sr">Measure</span></th>${ks.map((k,i)=>`<th class="num${i?" p2":""}">${esc(lblShort(k))}${leadT(k)}</th>`).join("")}</tr></thead><tbody>${R.map(([l,g,f,dir,alt])=>{const v=S.map(g);
  const w=two&&dir&&v[0]!=null&&v[1]!=null&&Math.abs(v[0]-v[1])>1e-9?((v[1]-v[0])*dir>0?1:0):-1;
  return `<tr><th scope="row">${l}</th>${v.map((x,i)=>`<td class="num${i===w?" win":""}">${alt&&alt(S[i])||(x==null?"—":f(x,S[i]))}${i===w?'<b aria-hidden="true"> ✓</b><span class="sr"> (better)</span>':""}</td>`).join("")}</tr>`}).join("")}</tbody></table>
 <p class="cite">${two?"✓ = better of the two (fewer kids, shorter walk, or a larger share of schools at target). ":""}From each plan's scorecard: ${ks.map(k=>src(PM[k].src,lblShort(k))).join(" · ")}. Schools at target: zoned schools inside their target size range in 2031-32, <span ${EXT_T}>exempt schools</span> left out (as on the options page).</p>`}
// zoned schools NOT at target in 2031-32 under a plan (same definition and count as "Schools at target"); names with an area
// select it; open under the size theme on wide screens (on phones they made the panel ~5,000px tall)
function oorHtml(ks){return ks.map(k=>{const d=durOf(k),st=PD(k).st||{},pol=polysOf(k);if(!d)return"";const L=Object.keys(d.s).filter(n=>d.s[n][1]!==0).sort((a,b)=>nm(a).localeCompare(nm(b)));
 if(!L.length)return `<p class="hint oor">${esc(lblShort(k))}: all ${d.n} zoned schools at target in 2031-32.</p>`;
 return `<details class="oor"${szOn()&&innerWidth>900?" open":""}><summary>Not at target in ${esc(lblShort(k))}: ${L.length} of ${d.n} zoned schools</summary><ul>${L.map(n=>{const s=st[n]||{},[sz,c]=d.s[n],lab=esc(nm(n)),rng=s.floor!=null?`${fmt(s.floor)}–${s.ceil!=null?fmt(s.ceil):"no cap"}`:"";
  const off=c<0&&s.floor!=null?`${fmt(s.floor-sz)} under`:c>0&&s.ceil!=null?`${fmt(sz-s.ceil)} over`:c<0?"under":"over";
  return `<li>${pol[n]?`<button type="button" data-sel="${esc(n)}">${lab}</button>`:lab}<span>${fmt(sz)} · ${off}${rng?` <small>(${rng})</small>`:""}</span></li>`}).join("")}</ul><p class="cite">Whole-school sizes, 2031-32 (neighborhood and program kids), from the plan's scorecard (durability), so they run higher than the area counts in this panel; <span ${EXT_T}>exempt schools</span> are not counted. Range = floor (PPS's minimum size) to ceiling (building capacity).</p></details>`}).join("")}
const selBtn=n=>`<button type="button" data-sel="${esc(n)}">${esc(nm(n))}</button>`;
// size theme, two plans: which schools change size status (from each plan's durability block)
function szMoves(){const a=durOf(p1),b=durOf(p2);if(!a||!b||p1===p2)return"";const on=(d,n)=>d.s[n]&&d.s[n][1]===0,off=(d,n)=>d.s[n]&&d.s[n][1]!==0;
 const fix=Object.keys(a.s).filter(n=>off(a,n)&&on(b,n)),brk=Object.keys(b.s).filter(n=>off(b,n)&&on(a,n)),L=x=>x.sort((p,q)=>nm(p).localeCompare(nm(q))).map(selBtn).join(", ");
 return `<div class="from szmv"><div class="tag">Size status, ${esc(lblShort(p1))} → ${esc(lblShort(p2))}</div>${fix.length?`<p class="hint" style="color:var(--ink)">Off target → at target (${fix.length}): ${L(fix)}</p>`:""}${brk.length?`<p class="hint" style="color:var(--ink)">At target → off target (${brk.length}): ${L(brk)}</p>`:""}${!fix.length&&!brk.length?`<p class="hint">No school changes size status.</p>`:""}</div>`}
// long side-panel tables show 12 rows (plus the selected school's) and a "Show all" button (round 5: the panel ran ~3,800px)
const CAP=12,capRows=L=>L.map((t,i)=>i<CAP||t.startsWith('<tr class="hl"')?t:'<tr class="xr"'+t.slice(3)).join(""),
 moreBtn=n=>n>CAP?`<button type="button" class="lnk morer" data-more="${n}">Show all ${n} rows</button>`:"";
// past theme: kids past a closer school by assigned school (one plan), or plan 1 vs plan 2 sorted by the change
function pastTbl(){const two=cmpOn()&&p1!==p2;
 if(!two){const k=cmpOn()?p1:scn,o=pastBy(k),L=Object.keys(o).sort((x,y)=>o[y]-o[x]).filter(n=>Math.round(o[n])>0);if(!L.length)return"";
  return `<div class="tag">Sent to a farther school, by assigned school (${esc(lblShort(k))})</div><div class="dscroll" tabindex="0" role="region" aria-label="Sent to a farther school by school, scrollable"><table class="dtab"><thead><tr><th>School</th><th class="num">Kids</th></tr></thead><tbody>${capRows(L.map(n=>`<tr${n===sel?' class="hl"':""}><th scope="row">${polysOf(k)[n]?selBtn(n):esc(nm(n))}</th><td class="num">${fmt(o[n])}</td></tr>`))}</tbody></table></div>${moreBtn(L.length)}`}
 const a=pastBy(p1),b=pastBy(p2),L=[...new Set([...Object.keys(a),...Object.keys(b)])].map(n=>[n,a[n]||0,b[n]||0,Math.round(b[n]||0)-Math.round(a[n]||0)]).filter(r=>r[3]!==0).sort((x,y)=>x[3]-y[3]||nm(x[0]).localeCompare(nm(y[0])));
 if(!L.length)return"";const has=n=>polysOf(p1)[n]||polysOf(p2)[n];
 return `<div class="tag">Sent to a farther school, by assigned school</div><div class="dscroll" tabindex="0" role="region" aria-label="Sent to a farther school by school, plan 1 vs plan 2, scrollable"><table class="dtab"><thead><tr><th>School</th><th class="num">${esc(lblShort(p1))}</th><th class="num">${esc(lblShort(p2))}</th><th class="num">Change</th></tr></thead><tbody>${capRows(L.map(r=>`<tr${r[0]===sel?' class="hl"':""}><th scope="row">${has(r[0])?selBtn(r[0]):esc(nm(r[0]))}</th><td class="num">${fmt(r[1])}</td><td class="num">${fmt(r[2])}</td><td class="num ${r[3]<0?"pos":"neg"}">${sg(r[3])}</td></tr>`))}</tbody></table></div>${moreBtn(L.length)}<p class="cite">Kids assigned to each school who live at least ${PD(p1).past.margin} mi closer on foot to another open school (each plan's scorecard rule). Negative = fewer under ${esc(lblShort(p2))}.</p>`}
function selectOne(n){sel=n;markSel();const pd=PD(scn),pm=PM[scn];
 const head=`<div class="tag">${esc(pm.short)} · ${LVN[lv]}, whole district</div><div class="vline">${vtag(scn)}</div>`+spotHtml()+scoreTbl([scn])+cav(scn)+(pastOn()?pastTbl()+oorHtml([scn]):oorHtml([scn]));
 if(!n||!polysOf(scn)[n]){$("sidec").innerHTML=head+`<p class="hint">Tap an area for one school's numbers (hover shows its name).</p>`+progPanel();sideWire();return}
 const c=(colsFor(scn)||{})[n],st=(pd.st||{})[n];
 const past=pd.past.regs.filter(r=>r[0]===n);const pastK=pastBy(scn)[n]||0;
 const rows=[["Kids living in this area (model)",fmt(pd.size[n])],["Kids of color in this area",pd.koc[n]!=null?pd.koc[n]+"%":"—"],["Average walk, kids in this area",pd.avgw[n]!=null?fx(pd.avgw[n],2)+" mi":"—"]];
 if(pastK)rows.push([`Sent to a farther school (≥ ${pd.past.margin} mi)`,fmt(pastK)]);
 let h=`<div class="tag sch">School area</div><h3><i style="background:var(--c${c})"></i>${esc(nm(n))}</h3>`+kvs(rows)+
  `<p class="cite">Area counts: modeled ${LVN[lv]} neighborhood kids, 2031-32, by 2020 Census block, the same kids as the plan's ${src(pm.src,"scorecard")} (${src("build/solver/metrics.py","metrics.py")}), assigned per ${src(pm.assign[lv],"assign_"+lv+".parquet")}; walks from ${src("build/routing/walk_miles.parquet","walk_miles.parquet")}.</p>`;
 if(st){const rng=st.floor!=null?`${fmt(st.floor)}–${st.ceil!=null?fmt(st.ceil):"no cap"}`:"";
  h+=`<div class="tag">School, ${esc(pm.basis?pm.basis.split(" ")[0]:"2031-32")} (model)</div>`+kvs([["Students, whole school",fmt(st.total)],["Neighborhood "+LVN[lv],fmt(st.nbhd)],st.prog?["Program students "+LVN[lv],fmt(st.prog)]:null,["Capacity",fmt(st.cap)],["Use of capacity",pct(st.util)],
   ["At target, 2031-32"+(rng?` (${rng})`:""),{"-1":"no, under floor","0":"yes","1":"no, over ceiling",x:`<span ${EXT_T}>exempt, not counted</span>`}[szCls(scn,n)]||(st.in_range==null?"—":st.in_range?"yes":"no")],st.walk!=null?["Average walk (school)",fx(st.walk,2)+" mi"]:null,st.bus!=null?[`Kids over ${(META.levels[lv]||{}).bus_threshold_mi||""} mi`,fmt(st.bus)]:null,st.poc!=null?["Kids of color (school)",pct(st.poc)]:null])+
   `<p class="cite">Source: ${src(pm.schools,"schools.csv")} (${esc(pm.ver)}).${META.note?" Preliminary.":""}</p>`}
 if(scn!==BASELINE)h+=bars((pd.from||{})[n],`Kids by PPS Status Quo ${LVN[lv]} school`);
 if(past.length)h+=bars(past.map(r=>[r[1],r[2]]),"Sent to a farther school: the nearer school");
 if(pm.lines==="official")h+=`<p class="hint">PPS's lines, traced from its published 2027-28 map and may be off by about 70 feet. ${src(pm.linesrc[lv],"Traced source")}.</p>`;
 else h+=`<p class="hint">Lines follow streets and are derived from the option's block assignment (crisp method).</p>`;
 $("sidec").innerHTML=head+h+progPanel();sideWire()}
function markSel(){[gA,gA2].forEach(g=>g.querySelectorAll(".area").forEach(p=>{p.classList.toggle("sel",p.dataset.n===sel)}));rove();
 [[gE1,cmpOn()?p1:scn],[gE2,p2]].forEach(([g,pl])=>{g.querySelectorAll("[data-sel]").forEach(o=>o.remove());if(!g.childNodes.length)return;selEdge(g,polysOf(pl)[sel])});
 updateLabels()}   // updateLabels un-hides the selected school's name
function cmpSide(n){const I=pairInfo(p1,p2),s1=PD(p1).size,s2=PD(p2).size,in1=polysOf(p1),in2=polysOf(p2),L=LVN[lv];
 const names=[...new Set([...Object.keys(in1),...Object.keys(in2)])];
 const rows=names.map(k=>{const v1=in1[k]?(s1[k]||0):null,v2=in2[k]?(s2[k]||0):null;return[k,v1,v2,(v2||0)-(v1||0)]});
 rows.sort((x,y)=>Math.abs(y[3])-Math.abs(x[3])||nm(x[0]).localeCompare(nm(y[0])));
 const chg=rows.filter(r=>r[3]!==0);const po1=new Set(progList(p1).map(p=>p.n)),po2=new Set(progList(p2).map(p=>p.n));
 const cell=(v,k,po)=>v==null?(po.has(k)?'<span title="program only, no neighborhood area">program</span>':'<span title="no area in this plan">none</span>'):fmt(v);
 let h=`<div class="cside"><div class="tag">Comparing · ${L}</div><div class="cmpn"><h3>${esc(lblShort(p1))}</h3><span class="vline">${vtag(p1)}</span></div>${p1!==p2?`<div class="cmpvs">vs</div><div class="cmpn"><h3 style="color:var(--cmp)">${esc(lblShort(p2))}</h3><span class="vline">${vtag(p2)}</span></div>`:""}`;
 const oo=oorHtml(p1!==p2?[p1,p2]:[p1]),notes=cav(p1,true)+(p1!==p2?cav(p2,true):"")+(pastOn()?pastTbl()+oo:oo+(szOn()?szMoves():""));   // the active theme's table leads
 // a tapped spot's answer goes right under the headline (round 5: it used to render ~2,000px down on desktop)
 if(!I){h+=`<p class="hint">Pick two different plans to see what changes.</p>`+spotHtml()+scoreTbl(p1!==p2?[p1,p2]:[p1])+notes}
 else{const tot=I.tot||LD().total,pc=fx(I.n/tot*100,1),basis=`Out of ${fmt(tot)} modeled ${L} neighborhood kids (2031-32, ${(k=>`the ${esc(lblShort(k))}`)(ORD.indexOf(p1)<ORD.indexOf(p2)?p2:p1)} scorecard basis).`;
  // headline = plan 1 vs plan 2 directly; the scorecard row counts each plan against Status Quo instead
  h+=I.n?`<div class="big">${fmt(I.n)}</div><p class="hint" style="color:var(--ink);font-size:.9rem;margin-top:-4px"><b>kids (${pc}%)</b> would go to a different ${L} school under ${esc(lblShort(p2))} than under ${esc(lblShort(p1))}.</p>`:
   `<p class="hint" style="color:var(--ink);font-size:.95rem"><b>Same ${L} lines.</b> ${esc(lblShort(p2))} keeps the same ${L} boundaries as ${esc(lblShort(p1))}, so no kid changes school between them.</p>`;
  h+=spotHtml();
  h+=`<div class="tag" style="margin-top:10px">Whole district, ${L}</div>`+scoreTbl([p1,p2])+
  (I.n?`<p class="hint">${basis} The headline compares the two plans directly; “Kids moved from their Status Quo school” counts each plan against PPS Status Quo. ${mode==="swipe"?"Drag the handle across: where the lines change, kids change school":`Where the thin solid and ${W2s} differ, kids change school`} (about ${(m=>fx(m,m>=10?0:1))(I.km2*0.386102)} sq mi in all). ${hatchOn()?"Hatched areas change school; hover or tap one to see the move.":hatchTheme()?"Hover or tap there to see the move, or turn on “Hatch changed areas” to mark them.":"Hover or tap there to see the move (the hatch shows under School colors or Changes only)."}</p>`:"")+notes}
 const hd=h;h="";
 if(n){const r=rows.find(x=>x[0]===n);
  if(r){const fl=(I?I.flows:[]);const out=fl.filter(f=>f[0]===n).slice(0,4),inn=fl.filter(f=>f[1]===n).slice(0,4);
   h+=`<div class="kv"><span>${esc(nm(n))}, ${esc(lblShort(p1))}</span><span>${r[1]==null?"no area":fmt(r[1])}</span><span>${esc(nm(n))}, ${esc(lblShort(p2))}</span><span>${r[2]==null?"no area":fmt(r[2])}</span><span>Change</span><span class="${r[3]>0?"pos":r[3]<0?"neg":""}">${sg(r[3])}</span></div>`;
   if(out.length||inn.length)h+=`<div class="from">${out.length?`<div class="tag">Leaving ${esc(nm(n))} for</div>`+out.map(f=>`<div class="bar"><span>${esc(nm(f[1]))}</span><em>${fmt(f[2])}</em></div>`).join(""):""}${inn.length?`<div class="tag">Arriving at ${esc(nm(n))} from</div>`+inn.map(f=>`<div class="bar"><span>${esc(nm(f[0]))}</span><em>${fmt(f[2])}</em></div>`).join(""):""}</div>`;
   const st1=(PD(p1).st||{})[n],st2=(PD(p2).st||{})[n];
   const at=k=>({"-1":"no, under floor","0":"yes","1":"no, over ceiling",x:`<span ${EXT_T}>exempt</span>`})[szCls(k,n)]||"—";
   if(st1||st2)h+=`<div class="tag">Whole school, 2031-32 (model)</div>`+kvs([["Students: "+esc(lblShort(p1)),fmt(st1&&st1.total)],["Students: "+esc(lblShort(p2)),fmt(st2&&st2.total)],["At target: "+esc(lblShort(p1)),polysOf(p1)[n]?at(p1):"no area"],["At target: "+esc(lblShort(p2)),polysOf(p2)[n]?at(p2):"no area"]])+`<p class="cite">Sources: ${src(PM[p1].schools,lblShort(p1)+" schools.csv")} · ${src(PM[p2].schools,lblShort(p2)+" schools.csv")}</p>`}}
 if(I&&I.n){h+=`<div class="tag">Change in kids living in each area</div><div class="dscroll" tabindex="0" role="region" aria-label="School size change table, scrollable"><table class="dtab"><thead><tr><th>School</th><th class="num">${esc(lblShort(p1))}</th><th class="num">${esc(lblShort(p2))}</th><th class="num">Change</th></tr></thead><tbody>${capRows(chg.map(r=>`<tr${r[0]===n?' class="hl"':""}><th scope="row">${selBtn(r[0])}</th><td class="num">${cell(r[1],r[0],po1)}</td><td class="num">${cell(r[2],r[0],po2)}</td><td class="num ${r[3]>0?"pos":"neg"}">${sg(r[3])}</td></tr>`))}</tbody></table></div>${moreBtn(chg.length)}`;
  const top=I.flows.slice(0,6);if(top.length)h+=`<div class="from"><div class="tag">Biggest moves</div>${top.map(f=>`<div class="bar"><span>${esc(nm(f[0]))} → ${esc(nm(f[1]))}</span><em>${fmt(f[2])}</em></div>`).join("")}</div>`;
  const un=rows.length-chg.length;h+=`<p class="hint">${un?`${un} school${un===1?"'s area is":"s' areas are"} unchanged.`:"Every school's area changes."} Moves (and the headline) count the modeled kids of ${(k=>esc(lblShort(k)))(ORD.indexOf(p1)<ORD.indexOf(p2)?p2:p1)}, as its scorecard does; each column above counts its own plan's kids (each plan leaves out its own program kids, such as DLI), so a school's moves and its column can differ by a few kids. Counts are modeled ${L} neighborhood kids by 2020 Census block (${src("build/data/blocks.parquet","blocks.parquet")}); program seats are left out, so they run lower than enrollment.${n?"":" Tap an area for one school."}</p>`}
 $("sidec").innerHTML=hd+h+"</div>"+progPanel();sideWire()}
function sideWire(){const sd=$("sidec");sd.querySelectorAll("[data-sel]").forEach(b=>b.onclick=()=>select(b.dataset.sel));
 const x=sd.querySelector("#spotx");if(x)x.onclick=()=>{pin=null;drawPin();select(sel)};
 sd.querySelectorAll("[data-plan]").forEach(b=>b.onclick=()=>{showPlan(b.dataset.plan);if(innerWidth<=900)toMap()});
 sd.querySelectorAll("[data-more]").forEach(b=>b.onclick=()=>{const t=b.previousElementSibling,all=t.classList.toggle("all");b.textContent=all?"Show fewer":`Show all ${b.dataset.more} rows`})}
// a short status line for screen readers (the panel itself is not a live region: it re-renders on every selection)
function selMsg(n){const m=$("selmsg");if(!m)return;if(!n){m.textContent="";return}const ks=cmpOn()?(p1===p2?[p1]:[p1,p2]):[scn];
 m.textContent=`${nm(n)} selected: `+ks.map(k=>`${polysOf(k)[n]?fmt(PD(k).size[n]||0)+" kids":"no area"} in ${lblShort(k)}`).join(", ")}
function select(n){if(!cmpOn())selectOne(n);else{sel=n;markSel();cmpSide(n)}selMsg(sel);spotPill();hashWrite()}

// ---- "this spot under every plan": tap anywhere; point-in-polygon on the drawn lines of every plan at this level
const ringCache={};
function ringsOf(k){const key=lv+"|"+k;if(ringCache[key])return ringCache[key];const out=[];
 Object.entries(polysOf(k)).forEach(([n,enc])=>{const rs=dec(enc).filter(r=>r.length>2);let x0=1e9,y0=1e9,x1=-1e9,y1=-1e9;
  rs.forEach(r=>r.forEach(([x,y])=>{if(x<x0)x0=x;if(x>x1)x1=x;if(y<y0)y0=y;if(y>y1)y1=y}));out.push({n,rs,bb:[x0,y0,x1,y1]})});return ringCache[key]=out}
// round 6 (review4 #4): a tap in a sliver between two traced areas (a fingertip is about a block wide) takes the nearest
// area within NEAR_M metres; schoolAt.edge says the last answer came from that fallback (the spot card says so)
const NEAR_M=40,MPD=111320;
function schoolAt(k,lon,lat){schoolAt.edge=false;const R=ringsOf(k);for(const o of R){const b=o.bb;if(lon<b[0]||lon>b[2]||lat<b[1]||lat>b[3])continue;let inside=false;
  for(const r of o.rs)for(let i=0,j=r.length-1;i<r.length;j=i++){const[xi,yi]=r[i],[xj,yj]=r[j];if((yi>lat)!==(yj>lat)&&lon<(xj-xi)*(lat-yi)/(yj-yi)+xi)inside=!inside}
  if(inside)return o.n}
 const tl=NEAR_M/MPD,tx=tl/kx,px=lon*kx*MPD,py=lat*MPD;let best=null,bd=NEAR_M*NEAR_M;
 for(const o of R){const b=o.bb;if(lon<b[0]-tx||lon>b[2]+tx||lat<b[1]-tl||lat>b[3]+tl)continue;
  for(const r of o.rs)for(let i=0,j=r.length-1;i<r.length;j=i++){const ax=r[j][0]*kx*MPD,ay=r[j][1]*MPD,bx=r[i][0]*kx*MPD,by=r[i][1]*MPD,dx=bx-ax,dy=by-ay,l=dx*dx+dy*dy;
   const t=l?Math.max(0,Math.min(1,((px-ax)*dx+(py-ay)*dy)/l)):0,ex=ax+t*dx-px,ey=ay+t*dy-py,d=ex*ex+ey*ey;if(d<bd){bd=d;best=o.n}}}
 schoolAt.edge=!!best;return best}
const toLL=([x,y])=>[x/(kx*S)+lon0,lat1-y/S];
function drawPin(){gPin.replaceChildren();if(!pin)return;const[x,y]=P(pin).split(",").map(Number);const k=mk1();
 const g=mk("g",{class:"pin",transform:`translate(${x},${y}) scale(${k})`,"data-x":x,"data-y":y});
 g.append(mk("circle",{r:9,class:"pin-halo"}),mk("circle",{r:4.5,class:"pin-dot"}));gPin.append(g)}
function spotHtml(){if(!pin)return"";const A=avail(),cur=new Set(cmpOn()?[p1,p2]:[scn]);const t=A.includes(BASELINE)?schoolAt(BASELINE,pin[0],pin[1]):null;
 let edge=false;const rows=A.map(k=>{const n=schoolAt(k,pin[0],pin[1]);edge=edge||schoolAt.edge;const moved=k!==BASELINE&&t&&n&&n!==t;
  return `<tr${cur.has(k)?' class="hl"':""}><th scope="row"><button type="button" data-plan="${esc(k)}" title="Show ${esc(lblFull(k))} on the map">${esc(lblShort(k))}</button></th><td>${n?esc(nm(n)):'<span class="muted">no area</span>'}</td><td class="mv">${moved?"moves":""}</td></tr>`}).join("");
 return `<div class="spot"><div class="spothd"><div class="tag">This spot, ${LVN[lv]}</div><button type="button" id="spotx" aria-label="Clear this spot">Clear</button></div>
 <table class="dtab spott"><thead><tr><th>Plan</th><th>School</th><th><span class="sr">Change from PPS Status Quo</span></th></tr></thead><tbody>${rows}</tbody></table>
 ${edge?`<p class="cite edgen"><b>This spot is on a boundary line</b> in at least one plan: zoom in and tap again to be sure.</p>`:""}<p class="cite">From each plan's drawn lines (PPS lines are traced, about 70 feet off at worst), so check a spot right on a boundary on PPS's own map. “Moves” = a different school than PPS Status Quo. Tap a plan to show it.</p></div>`}
function showPlan(k){if(cmpOn()){if(k===p1||k===p2)return;p2=k;fillSelects();chips();quick();drawAreas()}else{scn=k;$("sel0").value=k;drawAreas()}}
// in-map answer for a tapped spot (every width since round 5): the spot's school under the plan(s) on screen, one line, with
// "details ↓" (the only thing that scrolls: a tap never moves the page by itself) and × to clear the pin
function spotPill(){const el=$("spotpill");if(!el)return;document.querySelector(".mapbox").classList.toggle("haspin",!!pin);if(!pin){el.hidden=true;return}const at=k=>schoolAt(k,pin[0],pin[1]);
 let t;if(cmpOn()&&p1!==p2){const a=at(p1),b=at(p2);t=a===b?`${esc(a?nm(a):"no area")} under both`:`${esc(a?nm(a):"no area")} → ${esc(b?nm(b):"no area")}`}else{const a=at(cmpOn()?p1:scn);t=`${esc(a?nm(a):"no area")} (${esc(lblShort(cmpOn()?p1:scn))})`}
 el.innerHTML=`<span class="spt" title="This spot: ${t}">This spot: <b>${t}</b></span><button type="button" id="spotgo">details ↓</button><button type="button" class="spotx" id="spotpx" aria-label="Clear this spot" title="Clear this spot">×</button>`;el.hidden=false;
 $("spotgo").onclick=()=>{const s=$("sidec").querySelector(".spot");if(s)s.scrollIntoView({behavior:"smooth",block:innerWidth>900?"nearest":"start"})};
 $("spotpx").onclick=()=>{pin=null;drawPin();select(sel)}}

// ---- tables
const coarse=matchMedia("(pointer:coarse)");
// a requested run joins the comparison table only while it is on the map
function tables(){const hl=new Set(cmpOn()?[p1,p2]:[scn]),A=avail().filter(k=>!isReq(k)||hl.has(k));const L=LVN[lv],bus=(META.levels[lv]||{}).bus_threshold_mi;
 $("cmpH").textContent=`How the plans compare, ${L}`;
 // trade-off columns first (past a closer school, at target, reassigned); Lines and Source hide on phones (map.css), where the
 // short header (.hs) replaces the long one (.hl)
 const hd=(l,s)=>s?`<span class="tlong">${l}</span><span class="tshort">${s}</span>`:l;
 $("ctabh").innerHTML=`<tr><th>Plan</th><th class="num">${hd("Sent to a farther school","Farther school")}</th><th class="num">${hd("Schools at target, 2031-32","At target")}</th><th class="num">${hd("Moved from Status Quo school","Moved")}</th><th class="num">${hd("Avg walk (mi)","Walk mi")}</th><th class="num">${hd("Within 1 mi","≤1 mi")}</th><th class="num">${hd(`Over ${bus} mi`)}</th><th class="num">${hd("Dissimilarity","Dissim.")}</th><th class="c-lines">Lines</th><th class="c-src">Source</th></tr>`;
 // bold = best value in a column among PPS A, PPS B and the example plans (Status Quo is the baseline), as on the landing page
 const C=[[s=>s.kids_past_closer_school,-1,v=>fmt(v)],[(s,k)=>{const d=durOf(k);return d&&d.n?d.at/d.n:null},1,(v,k)=>atTxt(k)],[(s,k)=>k===BASELINE?null:s.kids_reassigned_vs_status_quo,-1,(v,k)=>k===BASELINE?"–":fmt(v)],
  [s=>s.avg_walk_mi,-1,v=>fx(v,2)],[s=>s["pct_within_1.0mi"],1,v=>fx(v,1)+"%"],[s=>s.kids_over_bus_threshold,-1,v=>fmt(v)],[s=>s.dissimilarity_index,-1,v=>fx(v,3)]];
 const V=A.map(k=>C.map(c=>{const v=c[0](PD(k).sum||{},k);return v==null||isNaN(v)?null:+v}));
 const best=C.map((c,j)=>{const x=A.map((k,i)=>PM[k].kind==="reference"||isReq(k)?null:V[i][j]).filter(v=>v!=null);return x.length>1?(c[1]>0?Math.max(...x):Math.min(...x)):null});
 $("ctab").innerHTML=A.map((k,i)=>{const pm=PM[k];
  // the plan name is a button: it puts that plan on the map (as plan 2 when comparing) and scrolls up to it
  return `<tr class="pick${hl.has(k)?" hl":""}" data-row="${esc(k)}"><th scope="row"><button type="button" data-plan="${esc(k)}" title="Show ${esc(lblFull(k))} on the map">${esc(pm.short)}</button>${leadT(k)}<small>${isOpt(k)?esc(pm.ver):k===BASELINE?"baseline":"PPS plan"}</small></th>${C.map((c,j)=>{const v=V[i][j],b=v!=null&&best[j]!=null&&pm.kind!=="reference"&&!isReq(k)&&Math.abs(v-best[j])<1e-9;
   return `<td class="num${b?" best":""}">${v==null&&!(j===2&&k===BASELINE)?"—":c[2](v,k)}</td>`}).join("")}<td class="c-lines">${pm.lines==="official"?"PPS official":"street-following, derived"}</td><td class="c-src">${src(pm.src,"scorecard")}</td></tr>`}).join("");
 $("ctabn").innerHTML=`Figures are each plan's model scorecard at ${L} (2031-32 basis; ${esc(PM[A[0]].ver)} unless labeled)<span class="tlong">, linked in the last column</span><span class="tshort">; scorecards are linked on the options page</span>. <b>Bold</b> = best in the column among PPS A, PPS B and the example plans (Status Quo is the baseline). Tap a plan's name to show it on the map. “Sent to a farther school” counts kids whose assigned school is at least 0.25 mi farther on foot than another open school reachable without a new I-84 or Willamette crossing. Schools at target: zoned schools inside their target size range in 2031-32, exempt schools left out (the options page's figure). “Moved” = kids assigned to a different school than under PPS Status Quo. Dissimilarity: 0 = every school matches the district mix of kids of color.${META.note?" "+esc(META.note):""}`;
 // a row click loads that plan; on touch only the plan-name cell does (reading a number must not jump the page)
 $("ctab").querySelectorAll("tr.pick").forEach(tr=>tr.onclick=e=>{if(e.target.closest("a"))return;if(coarse.matches&&!e.target.closest("th"))return;const k=tr.dataset.row;if(cmpOn()&&(k===p1||k===p2)){toMap();return}showPlan(k);toMap()});
 bandsTable()}
const toMap=()=>{const m=document.querySelector(".mapbox");if(m.getBoundingClientRect().top<0||m.getBoundingClientRect().top>innerHeight*.5)m.scrollIntoView({behavior:"smooth",block:"start"})};
let bsk=0,bdir=1;
function bandsTable(){const L=LVN[lv];const pl=cmpOn()?(p1===p2?[p1]:[p1,p2]):[scn];$("bwS").textContent=`${L} kids`;
 $("bandsH").textContent=`Share of each school's area within walking distance, ${L}`;
 $("bandsN").innerHTML=`Percent of each school's modeled ${L} neighborhood kids (or of its homes, 2020 Census housing units) within ½, 1, 1½ and 2 miles on foot, under ${pl.map(k=>esc(lblFull(k))).join(" and ")}. Tap a column heading to sort. Walks: ${src("build/routing/walk_miles.parquet","walk_miles.parquet")} (OpenStreetMap foot routes); kids and homes: ${src("build/data/blocks.parquet","blocks.parquet")}.`;
 const lab=["Count","½ mi","1 mi","1½ mi","2 mi"];$("bgrp").innerHTML=`<th rowspan="1"></th>`+pl.map(k=>`<th colspan="5" class="grp">${esc(lblShort(k))}</th>`).join("");
 $("bth").innerHTML=`<th data-k="0">School</th>`+pl.map((k,g)=>lab.map((l,i)=>`<th class="num${i?"":" g0"}" data-k="${1+g*5+i}">${l}</th>`).join("")).join("");
 const names=[...new Set(pl.flatMap(k=>Object.keys(PD(k).bands[wk]).filter(n=>n!=="__ALL")))];
 const rowOf=n=>[n,...pl.flatMap(k=>{const b=PD(k).bands[wk][n];return b?b:[null,null,null,null,null]})];
 const D=names.map(rowOf);D.sort((a,b)=>{const x=a[bsk],y=b[bsk];if(bsk===0)return bdir*nm(x).localeCompare(nm(y));if(x==null&&y==null)return 0;if(x==null)return 1;if(y==null)return -1;return bdir*(x-y)});
 const cell=(v,i)=>{if(v==null)return i===0?`<td class="g0 cl" colspan="5">no area</td>`:"";if(i===0)return `<td class="g0 pc">${fmt(v)}</td>`;const a=Math.max(0,Math.min(1,v/100));return `<td class="pc" style="background:color-mix(in srgb,var(--accent) ${Math.round(a*a*38)}%,transparent)">${v}%</td>`};
 const row=r=>`<tr${r[0]===sel?' class="hl"':""}><th scope="row">${esc(r[0]==="__ALL"?"District":nm(r[0]))}</th>${pl.map((k,g)=>r.slice(1+g*5,6+g*5).map((v,i)=>cell(v,i)).join("")).join("")}</tr>`;
 $("btb").innerHTML=D.map(row).join("");$("btf").innerHTML=row(rowOf("__ALL"));
 // folded: the summary line carries the district row
 $("bandsSum").innerHTML=`District, share of ${wk==="S"?L+" kids":"homes"} within ½ / 1 / 1½ / 2 mi: `+pl.map(k=>{const b=PD(k).bands[wk].__ALL;return `<b>${esc(lblShort(k))}</b> ${b.slice(1).map(x=>x+"%").join(" / ")}`}).join(" · ");
 document.querySelectorAll("#bth th[data-k]").forEach(th=>{if(+th.dataset.k===bsk)th.setAttribute("aria-sort",bdir>0?"ascending":"descending");th.onclick=()=>{const k=+th.dataset.k;if(bsk===k)bdir=-bdir;else{bsk=k;bdir=k===0?1:-1}bandsTable()}})}
document.querySelectorAll("[data-w]").forEach(b=>b.onclick=()=>{wk=b.dataset.w;document.querySelectorAll("[data-w]").forEach(x=>x.setAttribute("aria-pressed",x===b));bandsTable()});

// ---- controls
function fillSelects(){const A=avail(),lt=innerWidth<=430?" (best)":" (best we modeled)";[["sel0",scn],["sel1",p1],["sel2",p2]].forEach(([id,v])=>{const s=$(id);s.replaceChildren();
  // short names keep the one-row selects narrow (full name + version in the tooltip); the best example we modeled is tagged
  const grp=(t,ks)=>{if(!ks.length)return;const g=document.createElement("optgroup");g.label=t;ks.forEach(k=>{const o=new Option(lblShort(k)+(k===LEAD?lt:isWif(k)?" (what-if)":""),k);o.title=lblFull(k)+(cavOf(k)?" — "+cavOf(k):"");g.append(o)});s.append(g)};
  grp("PPS plans",A.filter(k=>!isOpt(k)));grp("Example plans",A.filter(k=>isOpt(k)&&!isWif(k)&&!isReq(k)));grp("What-if",A.filter(k=>isWif(k)&&!isReq(k)));grp("Requested runs",A.filter(isReq));s.value=v})}
// round 8 ("only do pre filled compare on a few"): three presets with short labels; any other pair is in
// the two plan selects. [plan 1 (left), plan 2 (right), label, tooltip]
const QUICK=()=>[[BASELINE,"scenario_A","PPS A vs no closures"],[BASELINE,"scenario_B","PPS B vs no closures"],[LEAD,"scenario_A","PPS A vs best we modeled"]];
// the chip row scrolls sideways on phones: a right-edge fade shows while more chips are hidden
const quickFade=()=>{const q=$("quick");q.classList.toggle("more",q.scrollLeft+q.clientWidth<q.scrollWidth-2)};
$("quick").addEventListener("scroll",quickFade,{passive:true});
function quick(){const q=$("quick");q.querySelectorAll("button").forEach(b=>b.remove());const A=avail();
 QUICK().filter(([a,b])=>a!==b&&A.includes(a)&&A.includes(b)).forEach(([a,b,t])=>{const bt=document.createElement("button");bt.type="button";bt.textContent=t;bt.title=`${lblFull(a)} (left) vs ${lblFull(b)} (right)`;
  bt.setAttribute("aria-pressed",cmpOn()&&p1===a&&p2===b);bt.onclick=()=>{p1=a;p2=b;if(!cmpOn()){initLoad=true;setMode("swipe");initLoad=false}else{fillSelects();chips();drawAreas()}quick();hashWrite()};q.append(bt)});quickFade()}
// "Map options" (round 8): a dot on the button while anything in it differs from the default, so a hidden setting is never a surprise
function optInd(){const off=[];if(colBy())off.push("colors: "+$("lcol").selectedOptions[0].text);if(cmpOn()&&hatchTheme()&&!showHatch)off.push("hatch off");
 if($("lcur").checked&&!$("lcurw").hidden)off.push("Status Quo lines on top");[["lpri","major streets"],["lst","collector streets"],["lloc","local streets"],["lnm","street names"],["lrail","rail"]].forEach(([id,t])=>{if(!$(id).checked)off.push(t+" off")});
 $("mdot").hidden=!off.length;$("mdotT").textContent=off.length?" (changed: "+off.join(", ")+")":"";$("mopt").querySelector("summary").title=off.length?"Changed: "+off.join(", "):"Colors, hatching, streets and rail"}
function modeUI(){const m=mode,c=m!=="single";document.querySelectorAll("[data-m]").forEach(b=>b.setAttribute("aria-pressed",b.dataset.m===m));
 $("cmpbar").hidden=!c;$("segS").hidden=c;$("swipe").hidden=m!=="swipe";$("chipL").hidden=$("chipR").hidden=!c;$("lg2").hidden=!c;
 $("lgS").hidden=m!=="swipe";$("lgO").hidden=m!=="overlay";document.querySelector(".mapbox").classList.toggle("sw",m==="swipe");
 $("lhfw").hidden=!c||!hatchTheme();themeKey();
 fillSelects();chips();quick()}
function setMode(m){const was=mode;mode=m;const c=m!=="single";
 if(c&&was==="single"&&!initLoad){const A=avail();p1=scn;p2=scn==="scenario_A"?(A.includes("option1_durable")?"option1_durable":BASELINE):"scenario_A";if(!A.includes(p2))p2=A.find(k=>k!==p1)||p1}
 if(!c&&was!=="single")scn=p2;
 if(!c){sel=null}
 modeUI();drawAreas()}
// map chips: the "best we modeled" tag ("best attempt" on phones) goes first so a truncated name never hides it
// "X lines", unless the plan name already ends with "lines"; names with a comma get "(lines)" ("Boundary changes, same closures (lines)")
const lnT=k=>{const s=lblShort(k);return /\blines$/i.test(s)?s:/,/.test(s)?s+" (lines)":s+" lines"};
// a plan named in running text where a possessive would follow: "the best example we modeled" for the best example we modeled, else its name
const pRef=k=>esc(lblShort(k));
function chips(){const lt=k=>k===LEAD?`<span class="lead">${innerWidth<=430?"best attempt":"best we modeled"}</span> `:isWif(k)?'<span class="lead wif">what-if</span> ':"";$("chipL").innerHTML=(mode==="overlay"?`<i class="p1"></i>`:"")+lt(p1)+esc(lblShort(p1));if($("lgO1T")){$("lgO1T").textContent=lnT(p1)+" (plan 1)";$("lgO2T").textContent=lnT(p2)+" (plan 2)"}$("chipR").innerHTML=(mode==="overlay"?`<i class="p2"></i>`:"")+lt(p2)+esc(lblShort(p2));
 $("chipL").title=lblFull(p1);$("chipR").title=lblFull(p2);
 $("swipe").querySelector("button").setAttribute("aria-label",`Swipe divider: left shows ${lblShort(p1)}, right shows ${lblShort(p2)}`)}
document.querySelectorAll("[data-m]").forEach(b=>b.onclick=()=>setMode(b.dataset.m));
$("sel0").onchange=()=>{scn=$("sel0").value;sel=null;drawAreas()};
["sel1","sel2"].forEach(id=>$(id).onchange=()=>{p1=$("sel1").value;p2=$("sel2").value;chips();quick();drawAreas()});
$("swapb").onclick=()=>{[p1,p2]=[p2,p1];$("sel1").value=p1;$("sel2").value=p2;chips();quick();drawAreas()};
$("lhf").onchange=e=>{showHatch=e.target.checked;drawAreas()};
$("lcur").onchange=curVis;
$("lpri").onchange=e=>gPri.style.display=e.target.checked?"":"none";
$("lrail").onchange=e=>gRail.style.display=e.target.checked?"":"none";
$("lcol").onchange=()=>{$("dvl").classList.toggle("on",dvOn());drawAreas()};
$("tkey").addEventListener("click",e=>{if(e.target.id==="toswipe")setMode("swipe")});
// level switch (6-8 / 9-12 data load on demand from map_data/, which works from file:// too)
function loadLevel(l,cb){if(MAPLV[l])return cb();$("loading").hidden=false;const s=document.createElement("script");s.src=`map_data/level_${l}.js?v=${LVVER}`;
 s.onload=()=>{$("loading").hidden=true;cb()};s.onerror=()=>{$("loading").hidden=true;$("loading").textContent="Could not load map_data/level_"+l+".js";$("loading").hidden=false};document.head.append(s)}
function levelUI(){const l=lv;document.querySelectorAll("[data-l]").forEach(b=>b.setAttribute("aria-pressed",b.dataset.l===l));$("dvlP").textContent=`district ${LD().kocd}%`;
 svg.setAttribute("aria-label",`Map of ${LVN[l]} attendance areas over freeways, rail and the river`);drawCur();linesNote()}
function setLevel(l){loadLevel(l,()=>{lv=l;const A=avail();
 [scn,p1,p2]=[scn,p1,p2].map(k=>A.includes(k)?k:A[0]);sel=null;levelUI();fillSelects();chips();quick();drawAreas()})}
// ---- URL hash state (format documented at the top of build/map/MAP_UX_AUDIT.md):
//   #level=K-5&view=overlay&a=status_quo&b=scenario_A[&school=Sabin][&at=-122.6501,45.5502]   (view = swipe | overlay)
//   #level=6-8&view=single&plan=scenario_A[&school=...][&at=lon,lat]
//   [&color=chg|size|past|race]  the "Color areas by" theme (no key = school colors)
//   [&layers=none]  hatch changed areas off (on by default; written only in a compare view under School colors / Changes only;
//                   layers=hatch is still read).
//   Legacy: layers=past (old checkbox) = color=past, layers=race = color=race (an explicit color key wins); #6-8 / #9-12.
//   Every read starts from the defaults (also on hashchange), so a missing or unknown key never keeps the last view's value.
const VIEWS=["single","swipe","overlay"],THEMES=["chg","size","past","race"];let lastHash="";
const henc=v=>encodeURIComponent(v).replace(/%2C/g,",").replace(/%20/g,"+");
// round 8: the default view (K-5, swipe, PPS Status Quo | PPS A) writes no hash; any key that differs from its default is written
const DEF={level:"K-5",view:"swipe",a:BASELINE,b:"scenario_A",plan:"scenario_A"};
const defPick=(k,i)=>{const A=avail();return A.includes(k)?k:A[Math.min(i,A.length-1)]};
function hashWrite(){if(initLoad)return;const q=[];if(lv!==DEF.level)q.push(["level",lv]);if(mode!==DEF.view)q.push(["view",mode]);
 if(cmpOn()){if(p1!==defPick(DEF.a,0))q.push(["a",p1]);if(p2!==defPick(DEF.b,1))q.push(["b",p2])}else if(scn!==defPick(DEF.plan,0))q.push(["plan",scn]);
 if(colBy())q.push(["color",colBy()]);if(cmpOn()&&hatchTheme()&&!showHatch)q.push(["layers","none"]);   // round 6: off-only, and only where the hatch is drawn
 if(sel)q.push(["school",sel]);if(pin)q.push(["at",pin[0].toFixed(5)+","+pin[1].toFixed(5)]);
 const h=q.length?"#"+q.map(([k,v])=>k+"="+henc(v)).join("&"):"";if(h===location.hash)return;lastHash=h;try{history.replaceState(null,"",h||location.pathname+location.search)}catch(_){}}
function hashRead(){const h=(location.hash||"").slice(1);if(!h)return{};if(LVN[h])return{level:h};const o={};
 h.split("&").forEach(kv=>{const i=kv.indexOf("=");if(i>0)try{o[kv.slice(0,i)]=decodeURIComponent(kv.slice(i+1).replace(/\+/g," "))}catch(_){}});return o}
// defaults (DEF, round 8): K-5, swipe, PPS Status Quo (left) | PPS A (right), school colors, hatch on, no school, no spot
function restore(st,done){const L=LVN[st.level]?st.level:"K-5";loadLevel(L,()=>{lv=L;const A=avail(),ok=k=>A.includes(k),pick=(k,i)=>ok(k)?k:A[Math.min(i,A.length-1)];
 scn=ok(st.plan)?st.plan:pick(DEF.plan,0);p1=ok(st.a)?st.a:pick(DEF.a,0);p2=ok(st.b)?st.b:pick(DEF.b,1);   // default pair: PPS Status Quo | PPS A (was PPS A vs the best example we modeled)
 mode=VIEWS.includes(st.view)?st.view:(st.plan&&!st.a?"single":DEF.view);
 sel=st.school&&(polysOf(cmpOn()?p1:scn)[st.school]||(cmpOn()&&polysOf(p2)[st.school]))?st.school:null;
 const at=(st.at||"").split(",").map(Number);pin=at.length===2&&at.every(isFinite)&&at[0]>lon0&&at[0]<lon1&&at[1]>lat0&&at[1]<lat1?at:null;
 const ly=st.layers!=null?st.layers.split(","):null;$("lhf").checked=showHatch=ly?ly.includes("hatch"):true;
 $("lcol").value=st.color!=null?(THEMES.includes(st.color)?st.color:""):ly&&ly.includes("past")?"past":ly&&ly.includes("race")?"race":"";
 $("dvl").classList.toggle("on",dvOn());
 initLoad=true;levelUI();modeUI();drawAreas();initLoad=false;hashWrite();if(done)requestAnimationFrame(done)})}
// copy a link to this view (the hash holds level, view, plans, school, spot and layers)
$("copyl").onclick=()=>{hashWrite();const u=location.href,b=$("copyl"),t=$("copylT"),done=ok=>{t.textContent=ok?"Link copied":"Copy failed";b.classList.add("msg");setTimeout(()=>{t.textContent="Copy link";b.classList.remove("msg")},1800)};
 const fb=()=>{const t=document.createElement("textarea");t.value=u;t.setAttribute("readonly","");t.style.position="fixed";t.style.opacity="0";document.body.append(t);t.select();let ok=false;try{ok=document.execCommand("copy")}catch(_){}t.remove();done(ok)};
 if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(u).then(()=>done(true),fb);else fb()};
window.addEventListener("hashchange",()=>{if(location.hash!==lastHash)restore(hashRead())});
document.querySelectorAll("[data-l]").forEach(b=>b.onclick=()=>setLevel(b.dataset.l));
const tip=$("tip");let tipT=0;
function showTip(e,txt){const r=$("map").getBoundingClientRect(),touch=e.pointerType==="touch";tip.textContent=txt;tip.hidden=false;const w=tip.offsetWidth;
 tip.style.left=Math.max(4,Math.min(r.width-w-4,e.clientX-r.left+(touch?-w/2:12)))+"px";tip.style.top=Math.max(4,e.clientY-r.top-(touch?64+tip.offsetHeight-28:34))+"px";
 clearTimeout(tipT);if(touch)tipT=setTimeout(hideTip,4000)}   // touch: centred well above the finger, stays ~4 s
function hideTip(){clearTimeout(tipT);tip.hidden=true}
// one delegated hover / tap tooltip: every data-tip under the pointer (area name, then moves, past regions, program schools)
function tipAt(e){if(moved||ptrs.size>1)return;const L=document.elementsFromPoint(e.clientX,e.clientY).filter(x=>x.dataset&&x.dataset.tip&&svg.contains(x));
 if(!L.length){if(e.pointerType!=="touch")hideTip();return}
 const ar=L.filter(x=>x.classList.contains("area")).slice(0,1),rest=L.filter(x=>!x.classList.contains("area"));
 // past difference (overlay): say which part the pointer is in (fixed / new / both) before the regions' own lines
 const ph=rest.filter(x=>x.dataset.pp),h1=ph.some(x=>x.dataset.pp==="1"),h2=ph.some(x=>x.dataset.pp==="2");
 const st=!ph.length?"":h1&&h2?`Under both plans: sent to a farther school in ${lblShort(p1)} and in ${lblShort(p2)}`:h1?`Fixed by ${lblShort(p2)}: sent to a farther school in ${lblShort(p1)} only`:`New under ${lblShort(p2)}: sent to a farther school in ${lblShort(p2)} only`;
 showTip(e,[...new Set([...ar.map(x=>x.dataset.tip),st,...rest.map(x=>x.dataset.tip)])].filter(Boolean).join("\n"))}
svg.addEventListener("pointermove",e=>{if(e.pointerType!=="touch")tipAt(e)});
svg.addEventListener("pointerdown",e=>{if(e.pointerType==="touch"){moved=false;tipAt(e)}});
svg.addEventListener("pointerleave",e=>{if(e.pointerType!=="touch")hideTip()});

// ---- pan / zoom
// The aspect ratio adapts to the screen (pickAR): as tall as the whole district where there is room, but never taller than
// ~62% of a phone's height, ~70% of a short landscape screen or ~80% of a desktop's (a taller map traps scrolling on touch).
// The default view (VB0) fits the whole district; full zoom-out is VB0's width, and the view is clamped to the district.
// vb always equals the SVG's real viewBox (screen-to-map math in toSvg depends on it).
let AR=0.78,VB0=[0,0,W,W*AR],WMAX=W,vb=[...VB0],arW=0,arH=0;
// Desktop and tablet: the window height less the controls (#ctl) and a margin, at least 520px, so the controls and the map
// fit one screen once the page header has scrolled away (round 5: sizing against the map's offset from the page top
// counted the nav, disclaimer and title too, and shrank the district to a third of the map). Re-picked when the width,
// the window height (not on touch, where the URL bar moves it) or the controls' height changes (ResizeObserver, init).
// Round 6 (review4 #7): a plain visit on desktop (no hash, e.g. the nav's "Map" link) keeps the page top (disclaimer and title)
// in view and sizes the map to the window space below it (at least 440px), so the whole district shows without scrolling;
// a deep link scrolls the controls to the top instead (init) and gets the taller map. Decided once per page load.
const fitTop=false;   // "map should be big as reasonable": every visit gets the tall map (plain visits still don't scroll)
function pickAR(){const w=svg.parentNode.clientWidth||1000,sm=innerWidth<=600||innerHeight<=560,ch=($("ctl")||{}).offsetHeight||0;
 const h=sm?innerHeight*(innerWidth<=600?0.62:0.7):fitTop&&innerWidth>900?Math.max(440,innerHeight-(svg.getBoundingClientRect().top+scrollY)-12):Math.max(520,innerHeight-ch-40);return Math.max(0.3,Math.min((EXT[3]-EXT[1])/(EXT[2]-EXT[0]),h/w))}
function fitVB(){const w=Math.max(EXT[2]-EXT[0],(EXT[3]-EXT[1])/AR);return[(EXT[0]+EXT[2]-w)/2,(EXT[1]+EXT[3]-w*AR)/2,w,w*AR]}
function setAR(reset){const a=pickAR();arW=innerWidth;arH=innerHeight;if(!reset&&Math.abs(a-AR)<.004)return;const home=Math.abs(vb[2]-VB0[2])<1,cy=vb[1]+vb[3]/2;
 AR=a;svg.style.aspectRatio=`1000/${Math.round(1000*AR)}`;VB0=fitVB();WMAX=VB0[2];
 if(reset||home||vb[2]>=WMAX)vb=[...VB0];else{vb[3]=vb[2]*AR;vb[1]=cy-vb[3]/2}}
function clampVB(){vb[2]=Math.min(vb[2],WMAX);vb[3]=vb[2]*AR;[0,1].forEach(i=>{const a=EXT[i],b=EXT[i+2],s=vb[i+2];vb[i]=s>=b-a?(a+b-s)/2:Math.max(a-s*.3,Math.min(b-s*.7,vb[i]))})}
setAR(true);svg.setAttribute("viewBox",vb.map(v=>v.toFixed(1)).join(" "));
// pan/zoom: vb is clamped at once (all screen-to-map math reads it), but the viewBox write and the label/marker pass run
// at most once per animation frame, however many pointer or wheel events arrive
let vbRaf=0;
const setVB=re=>{if(re===true||innerWidth!==arW||(Math.abs(innerHeight-arH)>40&&!matchMedia("(pointer:coarse)").matches))setAR();clampVB();if(!vbRaf)vbRaf=requestAnimationFrame(()=>{vbRaf=0;svg.setAttribute("viewBox",vb.map(v=>v.toFixed(1)).join(" "));updateLabels()})};
// markers and labels are sized in screen pixels (PX = the old desktop scale, ~0.93 px per map unit), not in map units,
// so they stay readable on a 356px-wide phone map; school names show once the map is zoomed in far enough (px per unit)
const PX=0.93,mk1=()=>PX*vb[2]/(svg.getBoundingClientRect().width||W);
// school names: all of them once zoomed in; zoomed out, only the selected school and the ones the theme is about (IMP);
// then collision culling in screen pixels (selected first, then IMP by rank), with the river label placed last
// text widths in screen px at 12px (canvas, cached): labels are semibold title-case Overpass, no tracking (.lbl, rev7), the river
// label italic 600 with .04em (.wlbl)
const twC=new Map(),twX=document.createElement("canvas").getContext("2d");
const tw=(s,f,ls)=>{const key=f+"|"+s;if(!twC.has(key)){twX.font=f;twC.set(key,twX.measureText(s).width+s.length*ls)}return twC.get(key)};
const LFS=12;   // school labels, shields and the river label: 12px on screen at every zoom (round 6, review4 #9)
function updateLabels(){const r=svg.getBoundingClientRect(),pxPer=(r.width||W)/vb[2],k=PX/pxPer,u=1/pxPer;streetState(pxPer);viewHook();
 // phone-sized overlay at district zoom: plan 2 as one thin line (map.css .thin2), double again once zoomed in (review4 #2)
 const thin=cmpOn()&&mode==="overlay"&&innerWidth<=900&&(r.width||W)<=700&&pxPer<1;if(document.documentElement.classList.contains("thin2")!==thin)document.documentElement.classList.toggle("thin2",thin);
 // names zoomed out: K-5 (~50 schools) from 0.3 px/unit, i.e. at the default zoom on desktop (0.4 on a phone-sized map,
 // about 1.4x zoom there), collision
 // culling keeps it clean (round 6; was 1.4); 6-8 (~15) from 0.25; 9-12 (8) always (N5: they were all hidden)
 const ns=Object.keys(polysOf(cmpOn()?p1:scn)).length,hide=ns>20?pxPer<((r.width||W)<=600?0.4:0.3):ns>10?pxPer<0.25:false;
 const box=[],hit=(x,y,w,h)=>box.some(b=>x<b[0]+b[2]&&x+w>b[0]&&y<b[1]+b[3]&&y+h>b[1]),fit=(x,y,w,h)=>{if(hit(x,y,w,h))return false;box.push([x,y,w,h]);return true},swx=vb[0]+swf*vb[2];
 // round 5: labels also yield to the school markers, the freeway shields and the map's own chips, zoom buttons, scale and pill;
 // round 6: and to the swipe handle (line + knob), so no name is cut in half at the divider
 const scr=(X,Y)=>[(X-vb[0])*pxPer,(Y-vb[1])*pxPer];
 gS.querySelectorAll("circle").forEach(c=>{if(c.closest('[data-side]')&&mode==="swipe"&&((c.closest('[data-side]').dataset.side==="L")!==(+c.dataset.x<swx)))return;const[x,y]=scr(+c.dataset.x,+c.dataset.y),q=4.2*(+c.dataset.rm||1);box.push([x-q,y-q,2*q,2*q])});
 // freeway shields: skipped where they would sit on a school marker (round 6)
 const nm0=box.length;gTop.querySelectorAll(".shield").forEach(g=>{const[x,y]=scr(+g.dataset.x,+g.dataset.y),w=+g.querySelector("rect").getAttribute("width")*PX,b=[x-w/2-1,y-8.5,w+2,17];
  const on=!box.slice(0,nm0).some(q=>b[0]<q[0]+q[2]&&b[0]+b[2]>q[0]&&b[1]<q[1]+q[3]&&b[1]+b[3]>q[1]);g.style.display=on?"":"none";if(on)box.push(b)});
 ["chipL","chipR","spotpill"].forEach(id=>{const e=$(id);if(e&&!e.hidden){const b=e.getBoundingClientRect();if(b.width)box.push([b.left-r.left,b.top-r.top,b.width,b.height])}});
 document.querySelectorAll(".mapbox .zoom,.mapbox .scale").forEach(e=>{const b=e.getBoundingClientRect();if(b.width)box.push([b.left-r.left,b.top-r.top,b.width,b.height])});
 if(mode==="swipe"){const hx=swf*(r.width||W);box.push([hx-3,0,6,r.height],[hx-24,r.height/2-24,48,48])}
 const T=[...gS.querySelectorAll("text")].map((t,i)=>{t.style.fontSize=(LFS*u)+"px";t.style.strokeWidth=(3.4*u)+"px";t.setAttribute("y",+t.dataset.y+4.3*u);
  const n=t.dataset.n,sd=t.parentNode.dataset.side,clip=mode==="swipe"&&sd&&((sd==="L")!==(+t.dataset.x<swx)),im=sd&&IMPS[sd]?IMPS[sd]:IMP;
  return{t,p:clip?null:n===sel?-1:im.has(n)?im.get(n):hide?null:100+i}});
 T.filter(o=>o.p==null).forEach(o=>o.t.classList.add("off"));
 // right of the marker, else left of it (text-anchor end); never past the map's edges; boxes are the 13px text height
 T.filter(o=>o.p!=null).sort((a,b)=>a.p-b.p).forEach(o=>{const[cx,cy]=scr(+o.t.dataset.x,+o.t.dataset.y),w=tw(o.t.textContent,`600 ${LFS}px Overpass, system-ui, sans-serif`,0)+4,y=cy-7.5,rm=+o.t.dataset.rm||1;
  const R=[cx+5.6*rm,"start",6],L=[cx-5.6*rm-w,"end",-6],ok=([x])=>x>=2&&x+w<=r.width-2&&y>=2&&y+13<=r.height-2&&fit(x,y,w,13);
  const inb=([x])=>x>=2&&x+w<=r.width-2,c=ok(R)?R:ok(L)?L:o.p===-1?(F=>(box.push([F[0],y,w,13]),F))(inb(R)||!inb(L)?R:L):null;/* the selected name always shows, on the side that stays inside the map */o.t.classList.toggle("off",!c);if(c){o.t.setAttribute("x",+o.t.dataset.x+c[2]*rm*k);o.t.style.textAnchor=c[1]}});
 gS.querySelectorAll("circle").forEach(c=>c.setAttribute("r",((+c.dataset.rm||1)*3.6*k).toFixed(2)));
 gPin.querySelectorAll(".pin").forEach(g=>g.setAttribute("transform",`translate(${g.dataset.x},${g.dataset.y}) scale(${k})`));
 gTop.querySelectorAll(".shield").forEach(g=>g.setAttribute("transform",`translate(${g.dataset.x},${g.dataset.y}) scale(${k})`));
 gTop.querySelectorAll(".wlbl").forEach(t=>{t.style.fontSize=(LFS*u)+"px";t.style.strokeWidth=(3*u)+"px";t.style.display=fit((+t.dataset.x-vb[0])*pxPer,(+t.dataset.y-vb[1])*pxPer-11,tw(t.textContent,`italic 600 ${LFS}px Overpass, system-ui, sans-serif`,LFS*.04),14)?"":"none"});
 const mi=S/69.05*pxPer,sm=innerWidth<=600;let m=1;if(mi>260)m=0.5;if(mi>520)m=0.25;if(mi>1300)m=0.1;if(mi<60)m=2;if(mi<30)m=5;$("scbar").style.width=(mi*m).toFixed(0)+"px";$("sclab").textContent=m<0.5?(m===0.25?"¼ mile":"0.1 mile"):m===0.5?"½ mile"+(sm?"":" · about 10 min walk"):m===1?"1 mile"+(sm?"":" · about 20 min walk"):m+" miles"}
function zoomAt(f,cx,cy){const nw=Math.min(WMAX,Math.max(W/16,vb[2]/f)),nh=nw*AR;vb=[cx-(cx-vb[0])*nw/vb[2],cy-(cy-vb[1])*nh/vb[3],nw,nh];setVB()}
const toSvg=ev=>{const r=svg.getBoundingClientRect();return[vb[0]+(ev.clientX-r.left)/r.width*vb[2],vb[1]+(ev.clientY-r.top)/r.height*vb[3]]};
svg.addEventListener("wheel",e=>{e.preventDefault();const[x,y]=toSvg(e);zoomAt(e.deltaY<0?1.25:0.8,x,y)},{passive:false});
// pointers: one finger/mouse pans (after 3px, or 10px for touch, so finger jitter still counts as a tap); two fingers pinch-zoom
// around their midpoint and pan with it; when one finger of a pinch lifts, the other re-anchors (it used to jump the map)
const ptrs=new Map();let last=null,down=null,pinch=null,moved=false;
const pinchOf=()=>{const[a,b]=[...ptrs.values()];return{d:Math.hypot(a.clientX-b.clientX,a.clientY-b.clientY),x:(a.clientX+b.clientX)/2,y:(a.clientY+b.clientY)/2}};
svg.addEventListener("pointerdown",e=>{ptrs.set(e.pointerId,e);if(ptrs.size===1){moved=false;down=[e.clientX,e.clientY]}last=[e.clientX,e.clientY];if(ptrs.size===2)pinch=pinchOf()});
// touch screens (coarse pointer): one finger scrolls the page (CSS touch-action:pan-y) and two fingers move/zoom the map; a one-finger
// drag on the map shows a brief "Use two fingers" hint. Mouse, pen and fine-pointer touch keep one-pointer panning.
const coarseMQ=matchMedia("(pointer:coarse)"),oneFinger=e=>e.pointerType==="touch"&&coarseMQ.matches;
const mbox=svg.parentNode,mhint=document.createElement("div");mhint.className="mhint";mhint.setAttribute("role","status");mhint.textContent="Use two fingers to move the map";mbox.appendChild(mhint);
let mhT=0;const showMH=()=>{mhint.classList.add("on");clearTimeout(mhT);mhT=setTimeout(()=>mhint.classList.remove("on"),1500)};
mbox.addEventListener("touchstart",e=>{if(e.touches.length>=2&&e.cancelable)e.preventDefault()},{passive:false});
mbox.addEventListener("touchmove",e=>{if(e.touches.length>=2&&e.cancelable)e.preventDefault()},{passive:false});
svg.addEventListener("pointermove",e=>{if(!ptrs.has(e.pointerId))return;ptrs.set(e.pointerId,e);const r=svg.getBoundingClientRect();
 if(ptrs.size===1&&oneFinger(e)){if(!moved&&down&&Math.hypot(e.clientX-down[0],e.clientY-down[1])>10)showMH();return}
 if(ptrs.size===2&&pinch){const q=pinchOf();vb[0]-=(q.x-pinch.x)/r.width*vb[2];vb[1]-=(q.y-pinch.y)/r.height*vb[3];const[x,y]=toSvg({clientX:q.x,clientY:q.y});zoomAt(pinch.d>0?q.d/pinch.d:1,x,y);pinch=q;moved=true;hideTip();return}
 if(ptrs.size===1&&last){if(!moved&&down&&Math.hypot(e.clientX-down[0],e.clientY-down[1])>(e.pointerType==="touch"?10:3)){moved=true;svg.classList.add("drag");hideTip();try{svg.setPointerCapture(e.pointerId)}catch(_){}}
  if(moved){vb[0]-=(e.clientX-last[0])/r.width*vb[2];vb[1]-=(e.clientY-last[1])/r.height*vb[3];setVB()}last=[e.clientX,e.clientY]}});
const up=e=>{if(e.type==="pointercancel"&&ptrs.size===1&&oneFinger(e)&&!pinch)showMH();ptrs.delete(e.pointerId);if(ptrs.size<2)pinch=null;if(ptrs.size===1){const p=[...ptrs.values()][0];last=[p.clientX,p.clientY]}if(!ptrs.size){last=null;svg.classList.remove("drag")}};
svg.addEventListener("pointerup",up);svg.addEventListener("pointercancel",up);
svg.addEventListener("click",e=>{if(moved){e.stopPropagation();e.preventDefault();moved=false}},true);
let lastPT="mouse";svg.addEventListener("pointerdown",e=>{lastPT=e.pointerType},true);
// a tap on a changed or past area pins that spot too (round 5: skipping it left the last spot's pin and pill on screen)
svg.addEventListener("click",e=>{if(e.target.closest&&e.target.closest(".swipe"))return;
 const ll=toLL(toSvg(e));if(!avail().some(k=>schoolAt(k,ll[0],ll[1])))return;pin=ll;drawPin();select(sel)});   // no auto-scroll: the in-map pill has "details ↓"
$("zin").onclick=()=>zoomAt(1.5,vb[0]+vb[2]/2,vb[1]+vb[3]/2);
$("zout").onclick=()=>zoomAt(1/1.5,vb[0]+vb[2]/2,vb[1]+vb[3]/2);
$("zres").onclick=()=>{vb=[...VB0];setVB()};
// ---- swipe handle
const swb=$("swipe").querySelector("button");
function setSwipe(f){swf=Math.max(0,Math.min(1,f));$("swipe").style.left=(swf*100)+"%";swb.setAttribute("aria-valuenow",Math.round(swf*100));swb.setAttribute("aria-valuetext",Math.round(swf*100)+"% from the left");updateLabels()}
swb.addEventListener("pointerdown",e=>{e.preventDefault();e.stopPropagation();swb.setPointerCapture(e.pointerId);swb.dataset.drag=1;swb.focus()});
swb.addEventListener("pointermove",e=>{if(!swb.dataset.drag)return;const r=svg.getBoundingClientRect();setSwipe((e.clientX-r.left)/r.width)});
const swEnd=()=>{delete swb.dataset.drag};swb.addEventListener("pointerup",swEnd);swb.addEventListener("pointercancel",swEnd);
swb.addEventListener("keydown",e=>{const st=e.shiftKey?.1:.02;if(e.key==="ArrowLeft"||e.key==="ArrowDown"){setSwipe(swf-st)}else if(e.key==="ArrowRight"||e.key==="ArrowUp"){setSwipe(swf+st)}else if(e.key==="Home"){setSwipe(0)}else if(e.key==="End"){setSwipe(1)}else return;e.preventDefault()});
function viewHook(){const r=svg.getBoundingClientRect(),ppu=(r.width||W)/vb[2];
 if(mode==="swipe"){const x=vb[0]+swf*vb[2];const a=$("swr"),b=$("swrL");a.setAttribute("x",x);a.setAttribute("y",vb[1]-50);a.setAttribute("width",vb[2]*2);a.setAttribute("height",vb[3]+100);
  b.setAttribute("x",vb[0]-vb[2]);b.setAttribute("y",vb[1]-50);b.setAttribute("width",x-vb[0]+vb[2]);b.setAttribute("height",vb[3]+100)}
 const pt=`scale(${1/ppu})`;$("hatch").setAttribute("patternTransform",pt);$("exh").setAttribute("patternTransform",pt)}
// ---- zoom-gated street toggles
// gated by on-screen pixels per map unit (ppu), not by zoom factor: a phone map is ~2.6x narrower than a desktop one, so the
// same zoom shows the same ground in far fewer pixels (desktop ppu ≈ 0.93 x zoom). The "zoom in" buttons use the same gates.
const GATES=[["lst",1.5],["lloc",2.8],["lnm",2.6]];
function streetState(ppu){GATES.forEach(([id,th])=>{const i=$(id),lab=i.closest("label"),on=ppu>=th;i.disabled=!on;lab.classList.toggle("dim",!on);lab.querySelector(".zh").hidden=on;i.title=on?"":"Zoom in to use this"});
 if(stS){stS.style.display=$("lst").checked&&ppu>=1.5?"":"none";stR.style.display=$("lloc").checked&&ppu>=2.8?"":"none"}else if(ppu>=1.3)lazyJS("streets.js",streetsReady);
 if(ppu>=2&&$("lnm").checked)lazyJS("street_names.js",namesReady);scheduleNames(ppu>=2.6&&$("lnm").checked)}
const ppuNow=()=>(svg.getBoundingClientRect().width||W)/vb[2];
document.querySelectorAll(".zh").forEach(b=>{const g=GATES.find(x=>x[0]===b.closest("label").querySelector("input").id);b.onclick=()=>{const p=ppuNow();if(p<g[1])zoomAt(g[1]*1.02/p,vb[0]+vb[2]/2,vb[1]+vb[3]/2)}});
["lst","lloc","lnm"].forEach(id=>$(id).onchange=updateLabels);
// ---- street names (anchors precomputed from OSM; laid out in screen space with collision culling)
// anchors come from map_data/street_names.js, fetched the first time the map is zoomed to 3x (names show from 4x)
const SL=[];
function namesReady(){if(SL.length||!window.SLBL)return;SLBL.split("\n").forEach(l=>{const c=l[0],i=l.indexOf("~"),name=l.slice(1,i);l.slice(i+1).split(" ").forEach(a=>{const[x,y,ang,r]=a.split(",").map(Number);SL.push({c,name,x:((x-1229300)/1e4-lon0)*kx*S,y:(lat1-(y+454300)/1e4)*S,a:ang,r:r*10})})});
 SL.sort((p,q)=>"str".indexOf(p.c)-"str".indexOf(q.c)||q.r-p.r);nmReg=null;if(nmOn)scheduleNames(true)}
let nmOn=false,nmReg=null,nmRaf=0;
function scheduleNames(on){nmOn=on;if(!on){gStN.replaceChildren();nmReg=null;return}if(!nmRaf)nmRaf=requestAnimationFrame(()=>{nmRaf=0;layoutNames()})}
function layoutNames(){if(!nmOn||!SL.length)return;const r=svg.getBoundingClientRect();if(!r.width)return;const ppu=r.width/vb[2];
 if(nmReg&&Math.abs(ppu/nmReg.ppu-1)<.005&&vb[0]>=nmReg.x0&&vb[1]>=nmReg.y0&&vb[0]+vb[2]<=nmReg.x1&&vb[1]+vb[3]<=nmReg.y1)return;
 const mx=vb[2]*.35,my=vb[3]*.35,R={ppu,x0:vb[0]-mx,y0:vb[1]-my,x1:vb[0]+vb[2]+mx,y1:vb[1]+vb[3]+my};nmReg=R;
 const ppm=ppu*S/111320,placed=[],frag=document.createDocumentFragment();let cnt=0;
 for(const a of SL){if(a.x<R.x0||a.x>R.x1||a.y<R.y0||a.y>R.y1)continue;if(a.c==="r"&&ppu<4.6)continue;
  const fs=12,w=a.name.length*fs*.58;if(w>a.r*ppm*.9)continue;
  const cx=(a.x-R.x0)*ppu,cy=(a.y-R.y0)*ppu,rad=a.a*Math.PI/180,co=Math.abs(Math.cos(rad)),si=Math.abs(Math.sin(rad)),hw=(w/2+4)*co+(fs/2+3)*si,hh=(w/2+4)*si+(fs/2+3)*co;
  let bad=false;for(const b of placed){if(Math.abs(b[0]-cx)<b[2]+hw&&Math.abs(b[1]-cy)<b[3]+hh){bad=true;break}}if(bad)continue;placed.push([cx,cy,hw,hh]);
  const t=mk("text",{class:"stn"+(a.c==="r"?"":" m"),transform:`translate(${a.x.toFixed(1)} ${a.y.toFixed(1)}) rotate(${-a.a}) scale(${(1/ppu).toFixed(5)})`,dy:".35em","font-size":fs});t.textContent=a.name;frag.append(t);if(++cnt>=350)break}
 gStN.replaceChildren(frag)}
window.addEventListener("resize",()=>{nmReg=null;setVB()});   // setVB re-picks the aspect ratio when the width changes

// ---- notes
function linesNote(){const off=avail().filter(k=>PM[k].lines==="official"),cr=avail().filter(k=>PM[k].lines==="crisp");
 $("lines-note").innerHTML=`<h2>Where the ${LVN[lv]} lines come from</h2><p><b>PPS Status Quo, PPS A and PPS B</b> use the district's own lines: PPS's 2027-28 ${LVN[lv]} scenario maps, traced from the PDFs PPS posted to BoardBook (${off.map(k=>src(PM[k].linesrc[lv],PM[k].short)).join(", ")}; median trace error about 70 feet). Areas PPS draws dashed or as insets (K-8 areas, Skyline) follow the official block assignment. </p>`+
 (cr.length?`<p><b>Example plans</b> (${cr.map(k=>esc(lblFull(k))).join(", ")}) are drawn from each option's block assignment (${cr.map(k=>src(PM[k].assign[lv],lblShort(k)+" assign_"+lv+".parquet")).join(", ")}): each street face goes whole to the school its kids are assigned to, and only faces shared by two schools are cut, along the line halfway between Census block centers. So the lines follow streets, freeways, rail and today's boundaries, and every populated block lands in its assigned school.</p>`:"")}
function method(){const a=META.plans.filter(p=>p.kind==="option");
 $("method").innerHTML=`<p><b>What the map counts.</b> Every count on this map uses the same kids as the plan's scorecard: modeled neighborhood kids at each grade level in 2031-32, by 2020 Census block (${src("build/data/blocks.parquet","blocks.parquet")}, scaled to the PSU forecast as in ${src("build/solver/metrics.py","metrics.py")}; ${src("build/data/README.md","method")}). Area counts in the side panel, the changed-area totals and the walking-distance table add up blocks; the school figures (total, capacity, target range) are from each plan's schools.csv and the table above from its scorecard. Area counts leave out program students (DLI, focus options), which the school totals include.</p>
 <p><b>Sent to a farther school.</b> Shaded areas are populated Census blocks where another open school at the same level is at least ${(PD(scn)||PD(BASELINE)).past.margin} mi shorter to walk to than the assigned school, counting only schools reachable without a new I-84 or Willamette crossing (same rule as the scorecards; walks from OpenStreetMap foot routes, ${src("build/routing/walk_miles.parquet","walk_miles.parquet")}). Counts use the scorecard's kids and rule, so the shaded areas add up to the “Sent to a farther school” figure in the table (a few blocks too small to shade are still counted).</p>
 <p><b>Crisp lines for the example plans.</b> Street faces come from OpenStreetMap secondary, tertiary and residential streets, freeways, primary streets, rail, today's (2025-26) lines at all three levels, the district outline and the I-84 / Willamette zone lines. The method is a port of the street-following redraw lines first built for the earlier walk redraws. Shared edges are exact (no gaps or overlaps); where a populated piece ends up cut off from its school, the empty street faces between them join that school, or if needed the populated faces on the way are cut along the halfway line, so kids stay where the assignment puts them. A piece stays apart from its main area only where the assigned blocks themselves are detached.</p>
 <p><b>Model version.</b> Example plans are labeled with their model version (${[...new Set(a.map(p=>esc(p.ver)))].join(", ")}).${META.note?" "+esc(META.note):""} Method: ${src(META.method_source,"solver METHOD.md")}; targets: ${src(META.targets_source,"targets.md")}. Map data © OpenStreetMap contributors (ODbL).</p>`}

// ---- init
(function init(){fillSelects();
 if(META.note){$("prelim").hidden=false;$("prelim").innerHTML=`<b>Preliminary numbers.</b> ${esc(META.note)}`}
 $("dvlP").textContent=`district ${LD().kocd}%`;drawCur();linesNote();method();setSwipe(.5);
 {const A=avail(),pick=(k,i)=>A.includes(k)?k:A[Math.min(i,A.length-1)];scn=pick(scn,0);p1=pick(BASELINE,0);p2=pick("scenario_A",1)}
 const deep=!!(location.hash||"").slice(1);mode=DEF.view;
 // phones: the legend folds into a disclosure (map.css); the "Terms" glossary is folded at every width (round 5)
 const mq=matchMedia("(max-width:600px)");["legd"].forEach(id=>{const d=$(id);if(d){d.open=!mq.matches;mq.addEventListener("change",e=>{if(!e.matches)d.open=true})}});
 // the map's height follows the controls' height (mode, plan rows, wrapping): re-pick the aspect ratio when it changes (N8)
 if(window.ResizeObserver){let ch=0;new ResizeObserver(()=>{const h=$("ctl").offsetHeight;if(h!==ch){ch=h;setVB(true)}}).observe($("ctl"))}
 // a deep link (landing-page cards, copied links): scroll the controls to the top so controls + map fit the window; on phones
 // too (round 6, review4 #3), or the map's top when controls + map are taller than the screen (landscape phones). A plain
 // visit never scrolls: the disclaimer and title stay in view.
 restore(hashRead(),deep?()=>{const m=svg.getBoundingClientRect();if(m.bottom<=innerHeight)return;const c=$("ctl").getBoundingClientRect();
  scrollTo(0,(innerWidth>900||m.bottom-c.top+8<=innerHeight?c.top:document.querySelector(".mapbox").getBoundingClientRect().top)+scrollY-8)}:null);   // after the level (6-8 / 9-12 load on demand) is drawn
 // "Map options" popover (round 8): closes on an outside tap or Escape (focus back to its button); opens under its button,
 // right-aligned (map.css); every change inside updates the button's "changed" dot
 const mo=$("mopt");
 document.addEventListener("click",e=>{if(mo.open&&!mo.contains(e.target))mo.open=false});mo.addEventListener("keydown",e=>{if(e.key==="Escape"&&mo.open){mo.open=false;mo.querySelector("summary").focus()}});
 mo.addEventListener("change",optInd);
 // skip link: focus the map's one tab stop (the selected or first school area)
 $("skipmap").onclick=e=>{const a=gA.querySelector('.area[tabindex="0"]');if(a){e.preventDefault();document.querySelector(".mapbox").scrollIntoView({block:"nearest"});a.focus()}};
 // collector/local streets: fetch once the page has settled (cached file; needed from 1.6x zoom)
 // not on phones, Save-Data or slow links: there streets load only when zoomed in (streetState)
 const cn=navigator.connection||{},slow=cn.saveData||["slow-2g","2g","3g"].includes(cn.effectiveType)||innerWidth<=600;
 const pre=()=>lazyJS("streets.js",streetsReady);if(!slow){if(window.requestIdleCallback)requestIdleCallback(pre,{timeout:3000});else setTimeout(pre,1500)}})();
