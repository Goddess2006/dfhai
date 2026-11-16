// Randare: desktop 1920x970 @2x (3840x1940) + 1920x970; mobil 1080x1350. Rulare: node render.cjs
const {chromium}=require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch();
for(const [f,w,h,scales] of [['homepage-black-november-desktop',1920,970,[2,1]],['homepage-black-november-mobil',1080,1350,[1]]]){
 for(const s of scales){const p=await b.newPage({viewport:{width:w,height:h},deviceScaleFactor:s});
  await p.goto('file://'+path.join(__dirname,f+'.html'),{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);
  const bad=await p.evaluate(()=>[...document.images].filter(i=>!i.naturalWidth).length);if(bad)throw Error('img');
  const out=f+(f.includes('desktop')?`-${w*s}x${h*s}`:`-${w}x${h}`)+'.jpg';
  await p.screenshot({path:path.join(__dirname,out),type:'jpeg',quality:92});console.log(out);await p.close();}}
await b.close();})();
