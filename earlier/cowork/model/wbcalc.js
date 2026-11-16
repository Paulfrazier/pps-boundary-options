const M=require('./core.js');const {BL,wd,SC}=M;
function bands(s,asg,key){const o={};const all={n:0,c:[0,0,0,0]};BL.forEach((b,i)=>{const n=asg[i];const wt=key==='S'?b.s:(b.hu||0);const d=wd(b,n);const r=o[n]=o[n]||{n:0,c:[0,0,0,0]};[0.5,1,1.5,2].forEach((t,k)=>{if(d<=t){r.c[k]+=wt;all.c[k]+=wt}});r.n+=wt;all.n+=wt});
 const fmt=(r,extra)=>[Math.round(r.n+extra),...r.c.map(c=>Math.round(c/r.n*100))];const imm=SC[s].imm;
 const res={};for(const[n,r]of Object.entries(o))res[n]=fmt(r,0);res.__ALL=fmt(all,0);return res}
module.exports={bands};
if(require.main===module){const fs=require('fs');const wb=JSON.parse(fs.readFileSync('../work/wb.json'));for(const k of ['S','H']){const r=bands('A',M.D.FIXA,k);let bad=0;wb[k].forEach(row=>{const n=row[0];const x=r[n];const y=row.slice(11,16);if(!x&&y[0]==null)return;if(JSON.stringify(x)!==JSON.stringify(y)){bad++;if(bad<5)console.log(k,n,x,y)}});console.log(k,'mismatch',bad)}}
