// node shot.js page.html prefix  -> prefix_full_A.png, prefix_ne_A.png (and DA/B full)
const {chromium}=require('playwright');(async()=>{const f=process.argv[2],pre=process.argv[3];const b=await chromium.launch();const p=await b.newPage({viewport:{width:1500,height:1300}});
const e=[];p.on('pageerror',x=>e.push(x.message));await p.goto('file://'+process.cwd()+'/'+f);await p.waitForTimeout(800);
await p.evaluate(()=>{document.getElementById('lcur').click()}); // hide today's lines so redraw edges are visible
const m=await p.$('.mapbox');
for(const s of (process.argv[4]||'A').split(',')){await p.click(`[data-s="${s}"]`);await p.waitForTimeout(200);
 await p.click('#zres');await p.waitForTimeout(300);await m.screenshot({path:`${pre}_full_${s}.png`});
 await p.evaluate(()=>{const a=P([-122.66,45.57]).split(',').map(Number),c=P([-122.58,45.53]).split(',').map(Number);const w=c[0]-a[0];vb=[a[0],a[1]-(w*AR-(c[1]-a[1]))/2,w,w*AR];setVB()});
 await p.waitForTimeout(300);await m.screenshot({path:`${pre}_ne_${s}.png`});}
console.log('errors',e);await b.close()})();
