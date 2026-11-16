const M=require('./core.js');const fs=require('fs');const {BL,wd,ppsAssign,NAMES,SC}=M;
const F=JSON.parse(fs.readFileSync('final_asg.json'));
const plans=[['T','Today','Q',BL.map(b=>b.a)],['PA','PPS plan A','A',ppsAssign('A')],['A','Walk redraw A','A',F.A],['DA','Walk + diversity A','A',F.DA],['PB','PPS plan B','B',ppsAssign('B')],['B','Walk redraw B','B',F.B]];
const out={plans:plans.map(p=>[p[0],p[1]]),names:NAMES,data:{},imm:{}};
for(const[k,l,s,a]of plans){const o={};BL.forEach((b,i)=>{const n=a[i];const d=wd(b,n);const r=o[n]=o[n]||{S:[0,0,0,0,0],H:[0,0,0,0,0],ws:0};for(const[key,w]of[['S',b.s],['H',b.hu||0]]){r[key][0]+=w;[0.5,1,1.5,2].forEach((t,j)=>{if(d<=t)r[key][j+1]+=w})}r.ws+=b.s*d});
 const res={};for(const n of NAMES){const r=o[n];if(!r){res[n]=null;continue}res[n]={S:r.S.map(Math.round),H:r.H.map(Math.round),avg:+(r.ws/Math.max(r.S[0],1e-9)).toFixed(2)}}
 const tot={S:[0,0,0,0,0],H:[0,0,0,0,0],ws:0};Object.values(o).forEach(r=>{for(let j=0;j<5;j++){tot.S[j]+=r.S[j];tot.H[j]+=r.H[j]}tot.ws+=r.ws});res.__ALL={S:tot.S.map(Math.round),H:tot.H.map(Math.round),avg:+(tot.ws/tot.S[0]).toFixed(3)};
 out.data[k]=res;out.imm[k]=SC[s].imm}
fs.writeFileSync('../work/tables.json',JSON.stringify(out));
for(const k of Object.keys(out.data))console.log(k,JSON.stringify(out.data[k].__ALL));console.log(JSON.stringify(out.data.A.Alameda),JSON.stringify(out.data.T.Sabin),out.data.A.Sabin);
