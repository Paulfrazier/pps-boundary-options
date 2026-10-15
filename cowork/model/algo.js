const M=require('./core.js');const {BL,NB,NAMES,ZS,SC,wd:wd0,ok,openOf,wmetrics,P}=M;
let MU={};const wd=wd0;const cst=(b,n)=>wd0(b,n)+(MU[n]||0)*(b.p-P);
function redraw(s,{G=0,L=360,U=600,iters=900,div=0,band=0.08,slack=0.5,cap=2.0}={}){const {imm}=SC[s];const open=openOf(s);
 const cands=BL.map(b=>{let c=Object.keys(b.w).filter(n=>open.includes(n)&&ok(b,n));if(!c.length)c=open.filter(n=>ok(b,n)).sort((p,q)=>b.st[p]-b.st[q]).slice(0,4);if(!c.length)c=open.slice().sort((p,q)=>b.st[p]-b.st[q]).slice(0,2);
   const best=Math.min(...c.map(n=>wd(b,n)));if(div>0)c=c.filter(n=>wd(b,n)<=Math.max(best+slack,Math.min(cap,best+1))&&(wd(b,n)<=cap||wd(b,n)===best));return c});
 const lam={},mu={};open.forEach(n=>{lam[n]=0;mu[n]=0});let best=null;
 for(let it=0;it<iters;it++){const size={},st={},pc={};open.forEach(n=>{size[n]=imm[n]||0;st[n]=0;pc[n]=0});const asg=new Array(BL.length);
  BL.forEach((b,i)=>{let bn=null,bc=1e9;for(const n of cands[i]){const c=wd(b,n)+lam[n]+mu[n]*(b.p-P)+G*(b.st[n]||0);if(c<bc){bc=c;bn=n}}asg[i]=bn;size[bn]+=b.s;st[bn]+=b.s;pc[bn]+=b.s*b.p});
  let viol=0,dist=0,dv=0;open.forEach(n=>{if(size[n]>U)viol+=size[n]-U;else if(size[n]<L)viol+=L-size[n];if(st[n]>0){const q=pc[n]/st[n];dv+=st[n]*Math.max(0,Math.abs(q-P)-band)}});BL.forEach((b,i)=>dist+=b.s*wd(b,asg[i]));
  const score=viol*0.01+dist/1000+div*dv/100;if(!best||score<best.score)best={score,asg:asg.slice(),mu:{...mu}};
  const eta=0.08*Math.pow(0.995,it);open.forEach(n=>{if(size[n]>U)lam[n]+=eta*Math.min(1,(size[n]-U)/U*3);else if(size[n]<L)lam[n]-=eta*Math.min(1,(L-size[n])/L*3);else lam[n]*=0.999;lam[n]=Math.max(-0.7,Math.min(1.5,lam[n]));
   if(div>0&&st[n]>0){const q=pc[n]/st[n];const e=q-P;if(Math.abs(e)>band)mu[n]+=div*eta*2*(e-Math.sign(e)*band)*4;else mu[n]*=0.995;mu[n]=Math.max(-3,Math.min(3,mu[n]))}})}
 MU=div>0?best.mu:{};return best.asg}
function contig(s,asg){const open=openOf(s);let tot=0;for(let it=0;it<12;it++){let changed=0;const seen=new Int32Array(BL.length).fill(-1);const comps=[];
  for(let i=0;i<BL.length;i++){if(seen[i]>=0)continue;const id=comps.length;const q=[i];seen[i]=id;const mem=[];while(q.length){const k=q.pop();mem.push(k);for(const j of NB[k])if(seen[j]<0&&asg[j]===asg[i]){seen[j]=id;q.push(j)}}comps.push({n:asg[i],mem,stu:mem.reduce((a,k)=>a+BL[k].s,0)})}
  const main={};open.forEach(n=>{let bi=-1,bd=1e9;BL.forEach((b,i)=>{if(asg[i]!==n)return;if(b.st[n]<bd){bd=b.st[n];bi=i}});if(bi>=0)main[n]=seen[bi]});
  comps.forEach((c,id)=>{if(main[c.n]===id)return;const nb={};c.mem.forEach(k=>NB[k].forEach(j=>{if(seen[j]!==id&&asg[j]!==c.n)nb[asg[j]]=1}));const o=Object.keys(nb).filter(n=>c.mem.every(k=>ok(BL[k],n)));if(!o.length)return;
   let best=null,bc=1e9;for(const n of o){const cost=c.mem.reduce((a,k)=>a+BL[k].s*cst(BL[k],n),0)/Math.max(c.stu,1e-6);if(cost<bc){bc=cost;best=n}}c.mem.forEach(k=>asg[k]=best);changed++;tot+=c.stu});if(!changed)break}return tot}
function cleanup(s,asg0,{maxAdd=0.2,cAdd=null}={}){const asg=asg0.slice();for(let pass=0;pass<10;pass++){let ch=0;for(let i=0;i<BL.length;i++){const t={};let tot=0;for(const j of NB[i]){const w=BL[j].s+0.2;t[asg[j]]=(t[asg[j]]||0)+w;tot+=w}
   if(!tot)continue;let bx=null,bv=0;for(const[k,v]of Object.entries(t))if(v>bv){bv=v;bx=k}const b=BL[i];
   if(bx!==asg[i]&&bv/tot>=0.5&&b.w[bx]!=null&&ok(b,bx)&&wd(b,bx)<=wd(b,asg[i])+maxAdd&&cst(b,bx)<=cst(b,asg[i])+(cAdd==null?maxAdd:cAdd)){asg[i]=bx;ch++}}if(!ch)break}contig(s,asg);return asg}
function rebalance(s,asg,LB,UB,maxMoves=4000){const open=openOf(s);const {imm}=SC[s];const size={};open.forEach(n=>size[n]=imm[n]||0);BL.forEach((b,i)=>size[asg[i]]+=b.s);let moves=0;
 const pen=n=>size[n]>UB[n]?size[n]-UB[n]:size[n]<LB[n]?LB[n]-size[n]:0;
 for(;moves<maxMoves;moves++){let best=null,bs=1e9;for(let i=0;i<BL.length;i++){const a=asg[i];const b=BL[i];if(b.s<0.05)continue;const cnt={};let na=0;for(const j of NB[i]){if(asg[j]===a)na++;else cnt[asg[j]]=(cnt[asg[j]]||0)+1}
   for(const[t,nt]of Object.entries(cnt)){if(b.w[t]==null||!ok(b,t))continue;const before=pen(a)+pen(t);size[a]-=b.s;size[t]+=b.s;const after=pen(a)+pen(t);size[a]+=b.s;size[t]-=b.s;const gain=before-after;if(gain<=0.01)continue;
    const dw=cst(b,t)-cst(b,a);const sc=dw/Math.min(gain,b.s)-0.03*(nt-na);if(sc<bs){bs=sc;best=[i,t]}}}
  if(!best)break;const[i,t]=best;size[asg[i]]-=BL[i].s;size[t]+=BL[i].s;asg[i]=t}return moves}
function full(s,opts){const RW=redraw(s,opts);const R0=wmetrics(s,RW).size;const LB={},UB={};for(const[n,v]of Object.entries(R0)){LB[n]=Math.min(360,v);UB[n]=Math.max(600,v)}
 const a=cleanup(s,RW,opts);for(let r=0;r<5;r++){rebalance(s,a,LB,UB);contig(s,a)}return a}
module.exports={redraw,contig,cleanup,rebalance,full};
