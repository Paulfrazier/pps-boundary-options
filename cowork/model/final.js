const M=require('./core.js');const {shapeLS,perim}=require('./shape.js');const {bands}=require('./wbcalc.js');const fs=require('fs');const {BL,ZS,D,SC,wd,ppsAssign}=M;
const lockOf=a=>BL.map((b,i)=>ZS[a[i]]!==b.z);
const run=(s,base,o)=>{const a=base.slice();const lock=lockOf(base);for(let r=0;r<4;r++)shapeLS(s,a,{...o,lock});return a};
const DA0=JSON.parse(fs.readFileSync('ls_final.json'))['a100w0.5'];
const F={A:JSON.parse(fs.readFileSync('region_runs.json')).G8,B:run('B',D.BASE_B,{beta:80,gamma:3,maxAdd:0.4}),DA:run('A',DA0,{beta:80,gamma:3,alpha:30,maxAdd:0.4})};
fs.writeFileSync('final_asg.json',JSON.stringify(F));
const sc={A:'A',B:'B',DA:'A'};
const stats=(s,asg)=>{const {imm}=SC[s];const st={};BL.forEach((b,i)=>{const n=asg[i];const d=wd(b,n);const o=st[n]=st[n]||{s:0,d:0,max:0,from:{}};o.s+=b.s;o.d+=b.s*d;if(b.s>0.05&&d>o.max)o.max=d;o.from[b.a]=(o.from[b.a]||0)+b.s});
 const out={};for(const n of M.openOf(s)){const o=st[n];const im=imm[n]||0;if(!o){out[n]={size:im,imm:im,avg:null,max:null,from:''};continue}
 out[n]={size:Math.round(o.s+im),imm:im,avg:+(o.d/o.s).toFixed(2),max:+o.max.toFixed(2),from:Object.entries(o.from).filter(([k,v])=>v>=15).sort((a,b)=>b[1]-a[1]).map(([k,v])=>`${k==='MLK Jr'?'King':k} ${Math.round(v)}`).join(', ')}}return out};
const runs={T:['Q',BL.map(b=>b.a)],PA:['A',ppsAssign('A')],PB:['B',ppsAssign('B')],A:['A',F.A],B:['B',F.B],DA:['A',F.DA]};
const out={P:+(M.P*100).toFixed(1),share:{},summ:{},stats:{},perim:{}};
for(const[k,[s,a]]of Object.entries(runs)){const m=M.wmetrics(s,a);out.share[k]=Object.fromEntries(Object.entries(m.share).map(([n,q])=>[n,Math.round(q*100)]));out.summ[k]={D:m.D,within:m.within,n:m.nsh,min:Math.round(m.min*100),max:Math.round(m.max*100),avg:m.avg,o1:m.o1,o15:m.o15,past:m.past,full:m.full,nn:m.n,moved:m.moved};out.perim[k]=+perim(a).toFixed(0)}
for(const k of ['A','B','DA'])out.stats[k]=stats(sc[k],F[k]);
// walk bands: replace redraw-A columns
const wb=JSON.parse(fs.readFileSync('../work/wb.json'));for(const key of ['S','H']){const r=bands('A',F.A,key);wb[key].forEach(row=>{const x=r[row[0]];if(x)for(let k=0;k<5;k++)row[11+k]=x[k]})}
fs.writeFileSync('../work/wb2.json',JSON.stringify(wb));
fs.writeFileSync('../work/div2.json',JSON.stringify(out));
console.log(JSON.stringify(out.summ));console.log(out.perim);
const sab={};BL.forEach((b,i)=>{if(b.a==='Sabin'){sab[F.A[i]]=(sab[F.A[i]]||0)+b.s}});console.log('sabin A',JSON.stringify(sab));
console.log('all',wb.S.find(r=>r[0]==='__ALL'),wb.H.find(r=>r[0]==='__ALL'));
