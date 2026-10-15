const M=require('./core.js');const A=require('./algo.js');const {BL,NB,SC,wd,ok,openOf,P}=M;
const EL=JSON.parse(require('fs').readFileSync(__dirname+'/edges.json'));const el=(i,j)=>{const v=EL[i<j?i+','+j:j+','+i];return v==null?0.03:v};
function perim(asg){let c=0;BL.forEach((b,i)=>NB[i].forEach(j=>{if(j>i&&asg[j]!==asg[i])c+=el(i,j)}));return c}
function cut(asg){let c=0;BL.forEach((b,i)=>NB[i].forEach(j=>{if(j>i&&asg[j]!==asg[i])c++}));return c}
function connectedWithout(asg,i,a){const nbs=NB[i].filter(j=>asg[j]===a);if(nbs.length<=1)return nbs.length===1;const target=new Set(nbs.slice(1));const seen=new Set([i,nbs[0]]);const q=[nbs[0]];let steps=0;
 while(q.length&&target.size&&steps<400){const k=q.shift();steps++;for(const j of NB[k]){if(seen.has(j)||asg[j]!==a)continue;seen.add(j);target.delete(j);q.push(j)}}return target.size===0}
function shapeLS(s,asg,{beta=0.3,alpha=0,band=0.08,maxAdd=0.25,cap=2.0,LB=360,UB=600,passes=60,gamma=0,c0=0.5,lock=null}={}){const open=openOf(s);const {imm}=SC[s];
 const size={},st={},pc={};open.forEach(n=>{size[n]=imm[n]||0;st[n]=0;pc[n]=0});BL.forEach((b,i)=>{size[asg[i]]+=b.s;st[asg[i]]+=b.s;pc[asg[i]]+=b.s*b.p});
 const lb={},ub={};open.forEach(n=>{lb[n]=Math.min(LB,size[n]);ub[n]=Math.max(UB,size[n])});
 const dv=n=>st[n]>0?st[n]*Math.max(0,Math.abs(pc[n]/st[n]-P)-band):0;const sp=n=>size[n]>ub[n]?(size[n]-ub[n])*5:size[n]<lb[n]?(lb[n]-size[n])*5:0;
 const school={};for(const n of open)school[n]=1;
 for(let p=0;p<passes;p++){let ch=0;for(let i=0;i<BL.length;i++){if(lock&&lock[i])continue;const b=BL[i];const a=asg[i];const cnt={};let na=0;for(const j of NB[i]){const L=el(i,j);if(asg[j]===a)na+=L;else cnt[asg[j]]=(cnt[asg[j]]||0)+L}
   let best=null,bd=-1e-4;
   for(const[t,nt]of Object.entries(cnt)){if(!ok(b,t))continue;if(b.s>0&&(size[a]-b.s<lb[a]-0.01||size[t]+b.s>ub[t]+0.01))continue;const wa=wd(b,a),wt=wd(b,t);if(b.s>0.01&&(wt>wa+maxAdd||wt>Math.max(cap,wa)))continue;
    const before=alpha*(dv(a)+dv(t))+sp(a)+sp(t);size[a]-=b.s;st[a]-=b.s;pc[a]-=b.s*b.p;size[t]+=b.s;st[t]+=b.s;pc[t]+=b.s*b.p;const after=alpha*(dv(a)+dv(t))+sp(a)+sp(t);
    size[a]+=b.s;st[a]+=b.s;pc[a]+=b.s*b.p;size[t]-=b.s;st[t]-=b.s;pc[t]-=b.s*b.p;
    const sa=b.st[a]!=null?b.st[a]:wa/1.4,stt=b.st[t]!=null?b.st[t]:wt/1.4;const dJ=after-before+b.s*(wt-wa)+beta*(na-nt)+gamma*(b.s+c0)*(stt*stt-sa*sa);if(dJ<bd){bd=dJ;best=t}}
   if(best&&connectedWithout(asg,i,a)){const t=best;size[a]-=b.s;st[a]-=b.s;pc[a]-=b.s*b.p;size[t]+=b.s;st[t]+=b.s;pc[t]+=b.s*b.p;asg[i]=t;ch++}}
  if(!ch)break}
 A.contig(s,asg);return asg}
module.exports={shapeLS,cut,perim};
