const M=require('./core.js');const A=require('./algo.js');const {shapeLS,perim}=require('./shape.js');const fs=require('fs');const {BL,NB,ZS,SC,wd,ok}=M;
const F=JSON.parse(fs.readFileSync('final_asg.json'));const base=F.A;
const core=process.argv[2].split(',');
// region: core + their neighbors
const adj=new Set(core);BL.forEach((b,i)=>{if(core.includes(base[i]))NB[i].forEach(j=>adj.add(base[j]))});const R=[...adj];
const lock=BL.map((b,i)=>ZS[base[i]]!==b.z);
const idx=BL.map((b,i)=>i).filter(i=>R.includes(base[i])&&!lock[i]);
const tgt={};R.forEach(n=>tgt[n]=0);idx.forEach(i=>tgt[base[i]]+=BL[i].s);
const st=(b,n)=>b.st[n]!=null?b.st[n]:wd(b,n)/1.4;
function solve(G,tol=15){const lam={};R.forEach(n=>lam[n]=0);let asg;for(let it=0;it<1500;it++){asg={};const sz={};R.forEach(n=>sz[n]=0);
  for(const i of idx){const b=BL[i];let bn=null,bc=1e9;for(const n of R){if(!ok(b,n))continue;const w=wd(b,n);if(w>Math.max(2.0,wd(b,base[i])))continue;const c=w+G*st(b,n)**2+lam[n];if(c<bc){bc=c;bn=n}}asg[i]=bn||base[i];sz[asg[i]]+=b.s}
  let worst=0;const eta=0.02*Math.pow(0.997,it);R.forEach(n=>{const d=sz[n]-tgt[n];if(Math.abs(d)>tol)lam[n]+=eta*Math.sign(d)*Math.min(1,Math.abs(d)/100);worst=Math.max(worst,Math.abs(d))});if(worst<=tol)break}
 const a=base.slice();for(const i of idx)a[i]=asg[i];A.contig('A',a);return a}
const f=(v,a)=>`perim ${perim(a).toFixed(0)} avg ${v.avg} o1 ${v.o1} o15 ${v.o15} past ${v.past} full ${v.full}/${v.n} | D ${v.D} within ${v.within}`;
const m0=M.wmetrics('A',base);console.log('base',f(m0,base),'R',R.join(','));
const S0=m0.size;const LB={},UB={};for(const[n,v]of Object.entries(S0)){LB[n]=Math.min(360,v);UB[n]=Math.max(600,v)}
const out={};for(const G of (process.argv[3]||'4,8,15,30').split(',').map(Number)){const a=solve(G,8);for(let r=0;r<3;r++){A.rebalance('A',a,LB,UB);A.contig('A',a)}const lockAll=lock;for(let r=0;r<2;r++)shapeLS('A',a,{beta:80,gamma:3,maxAdd:0.4,lock:lockAll});const m=M.wmetrics('A',a);
 console.log('G'+G,f(m,a),'| sizes',R.map(n=>n.slice(0,6)+':'+Math.round(m.size[n])).join(' '));out['G'+G]=a}
fs.writeFileSync('region_runs.json',JSON.stringify(out));
