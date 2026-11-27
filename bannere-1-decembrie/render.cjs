// Exportă out/*.html în JPEG la dimensiunea exactă (și @2x pentru ecrane retina).
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
(async()=>{const dir=path.join(__dirname,'out');const b=await chromium.launch();
for(const f of fs.readdirSync(dir).filter(x=>x.endsWith('.html'))){const m=f.match(/(\d+)x(\d+)/);const w=+m[1],h=+m[2];
 for(const sc of [1,2]){const p=await b.newPage({viewport:{width:w,height:h},deviceScaleFactor:sc});
  await p.goto('file://'+path.join(dir,f),{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);
  await p.screenshot({path:path.join(dir,f.replace('.html',sc==2?'@2x.jpg':'.jpg')),type:'jpeg',quality:sc==2?86:90});await p.close();}}
await b.close();})();
