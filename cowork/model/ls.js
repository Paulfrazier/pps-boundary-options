const M=require('./core.js');const A=require('./algo.js');const {BL,NB,SC,wd,ok,openOf,P}=M;
// diversity local search on contiguous map
function divLS(s,asg,{alpha=2,band=0.10,LB=330,UB=620,cap=2.0,maxWalkAdd=0.6,passes=40,rel=1}={}){const open=openOf(s);const {imm}=SC[s];
 const size={},st={},pc={};open.forEach(n=>{size[n]=imm[n]||0;st[n]=0;pc[n]=0});BL.forEach((b,i)=>{size[asg[i]]+=b.s;st[asg[i]]+=b.s;pc[asg[i]]+=b.s*b.p});
 const bw=BL.map(b=>{let m=1e9;for(const n of open)if(ok(b,n)){const v=wd(b,n);if(v<m)m=v}return m});
 const dv=n=>st[n]>0?st[n]*Math.max(0,Math.abs(pc[n]/st[n]-P)-band):0;
 const lb={},ub={};open.forEach(n=>{lb[n]=Math.min(LB,size[n]);ub[n]=Math.max(UB,size[n])});const sp=n=>size[n]>ub[n]?(size[n]-ub[n])*5:size[n]<lb[n]?(lb[n]-size[n])*5:0;
 let total=0;for(let p=0;p<passes;p++){let ch=0;
  for(let i=0;i<BL.length;i++){const b=BL[i];if(b.s<0.02)continue;const a=asg[i];const cnt={};let na=0;for(const j of NB[i]){if(asg[j]===a)na++;else cnt[asg[j]]=(cnt[asg[j]]||0)+1}
   for(const[t,nt]of Object.entries(cnt)){if(nt*rel<na||b.w[t]==null||!ok(b,t))continue;const w=wd(b,t);if(w>Math.max(cap,wd(b,a))||w>bw[i]+maxWalkAdd&&w>wd(b,a))continue;
    const before=alpha*(dv(a)+dv(t))+sp(a)+sp(t);size[a]-=b.s;st[a]-=b.s;pc[a]-=b.s*b.p;size[t]+=b.s;st[t]+=b.s;pc[t]+=b.s*b.p;
    const after=alpha*(dv(a)+dv(t))+sp(a)+sp(t);const dJ=after-before+b.s*(w-wd(b,a));
    if(dJ<-1e-4&&na>0){asg[i]=t;ch++;break}
    size[a]+=b.s;st[a]+=b.s;pc[a]+=b.s*b.p;size[t]-=b.s;st[t]-=b.s;pc[t]-=b.s*b.p}}
  total+=ch;if(!ch)break;if(p%5==4)A.contig(s,asg)}
 A.contig(s,asg);return total}
module.exports={divLS};
