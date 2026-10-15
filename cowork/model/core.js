const fs=require('fs');
const D=JSON.parse(fs.readFileSync(require('path').join(process.env.PPS_MAP_DIR||require('path').join(__dirname,'../../data/pps-map'),'pps-model.json'),'utf8'));
const {NAMES,ZS,SC}=D;const NB=D.NB;
const BL=D.BL.map(b=>({...b,az:new Set(b.az)}));
// race
const R={};fs.readFileSync(require('path').join(process.env.PPS_MAP_DIR||require('path').join(__dirname,'../../data/pps-map'),'pps-race.csv'),'utf8').trim().split('\n').forEach(l=>{const c=l.split(',');const v=c.slice(1).map(Number);R[c[0]]=v});
let miss=0;BL.forEach(b=>{const v=R[b.g];if(!v){miss++;b.kids=0;b.p=null;return}const kids=v[0]-v[5],kw=v[2]-v[7],kh=v[1]-v[6],kb=v[3]-v[8],ka=v[4]-v[9];b.kids=kids;b.kw=kw;b.p=kids>0?1-kw/kids:null});
// fill null p with neighbor avg
for(let pass=0;pass<3;pass++)BL.forEach((b,i)=>{if(b.p!=null)return;let s=0,n=0;NB[i].forEach(j=>{if(BL[j].p!=null){s+=BL[j].p;n++}});if(n)b.p=s/n});
BL.forEach(b=>{if(b.p==null)b.p=0.35});
const wd=(b,n)=>b.w[n]!=null?b.w[n]:b.st[n]*1.4;const ok=(b,n)=>b.az.has(ZS[n]);
const openOf=s=>NAMES.filter(n=>!SC[s].rec[n]);
const ppsAssign=s=>{const {rec}=SC[s];return BL.map(b=>rec[b.a]?rec[b.a].reduce((p,n)=>wd(b,n)<wd(b,p)?n:p):b.a)};
const bestWalk=(b,open)=>{let n=null,d=1e9;for(const o of Object.keys(b.w)){if(!open.includes(o))continue;if(b.w[o]<d){d=b.w[o];n=o}}if(!n){for(const o of open){const v=wd(b,o);if(v<d){d=v;n=o}}}return [n,d]};
const P=BL.reduce((a,b)=>a+b.s*b.p,0)/BL.reduce((a,b)=>a+b.s,0);
function wmetrics(s,asg){const {imm}=SC[s];const open=openOf(s);const size={},pc={},st={};open.forEach(n=>{size[n]=imm[n]||0;pc[n]=0;st[n]=0});let dist=0,stu=0,moved=0,past=0,o1=0,o15=0;
 BL.forEach((b,i)=>{const a=asg[i];const d=wd(b,a);size[a]+=b.s;st[a]+=b.s;pc[a]+=b.s*b.p;dist+=b.s*d;stu+=b.s;if(a!==b.a)moved+=b.s;if(d>1)o1+=b.s;if(d>1.5)o15+=b.s;const[n,nd]=bestWalk(b,open);if(a!==n&&d-nd>=0.25)past+=b.s});
 const v=Object.values(size);const share={};let POC=0,WH=0;open.forEach(n=>{if(st[n]>0){share[n]=pc[n]/st[n];POC+=pc[n];WH+=st[n]-pc[n]}});
 let Dis=0;open.forEach(n=>{if(st[n]>0)Dis+=Math.abs(pc[n]/POC-(st[n]-pc[n])/WH)});Dis/=2;
 const sh=Object.values(share);const within=sh.filter(x=>Math.abs(x-P)<=0.15).length;
 return {size,share,avg:+(dist/stu).toFixed(3),moved:Math.round(moved),past:Math.round(past),o1:Math.round(o1),o15:Math.round(o15),full:v.filter(x=>x>=360).length,n:v.length,D:+Dis.toFixed(3),within,nsh:sh.length,min:Math.min(...sh),max:Math.max(...sh)}}
module.exports={D,BL,NB,NAMES,ZS,SC,wd,ok,openOf,ppsAssign,bestWalk,wmetrics,P};
