// node metrics.js IMPLIED.json  -> compare final_asg vs implied: per-school size, walk, diversity
const M=require('../m/core.js');const fs=require('fs');const {BL,wd}=M;
const F=JSON.parse(fs.readFileSync('../m/final_asg.json'));const I=JSON.parse(fs.readFileSync(process.argv[2]));
const sc={A:'A',B:'B',DA:'A'};const EXEMPT=['Skyline','Forest Park','Sitton','Cesar Chavez'];
for(const k of ['A','B','DA']){const a=M.wmetrics(sc[k],F[k]),b=M.wmetrics(sc[k],I[k]);
 const mv={};BL.forEach((bl,i)=>{if(F[k][i]!==I[k][i]){const key=`${F[k][i]} -> ${I[k][i]}`;mv[key]=mv[key]||{blocks:0,s:0,dw:0};mv[key].blocks++;mv[key].s+=bl.s;mv[key].dw+=bl.s*(wd(bl,I[k][i])-wd(bl,F[k][i]))}});
 console.log(`== ${k}: avg walk ${a.avg} -> ${b.avg}; over 1.5 mi ${a.o15} -> ${b.o15}; over 1 mi ${a.o1} -> ${b.o1}; past-closer ${a.past} -> ${b.past}; dissimilarity ${a.D} -> ${b.D}; within15 ${a.within} -> ${b.within}`);
 for(const[key,v]of Object.entries(mv))console.log(`   ${key}: ${v.blocks} blocks, ${v.s.toFixed(1)} students, walk change ${(v.dw/Math.max(v.s,1e-9)).toFixed(2)} mi each`);
 const ch=Object.keys(a.size).filter(n=>Math.round(a.size[n])!==Math.round(b.size[n])).map(n=>`${n} ${Math.round(a.size[n])}->${Math.round(b.size[n])} (KoC ${(a.share[n]*100).toFixed(1)}->${(b.share[n]*100).toFixed(1)}%)`);console.log('   sizes:',ch.join('; '));
 const out=Object.keys(b.size).filter(n=>!EXEMPT.includes(n)&&(b.size[n]<360||b.size[n]>600)&&!(a.size[n]<360||a.size[n]>600));console.log('   newly outside 360-600:',out.join(',')||'none')}
