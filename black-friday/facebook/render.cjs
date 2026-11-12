// Randare PNG 1080x1350 pentru Facebook. Rulare: node render.cjs
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1350},deviceScaleFactor:1});
for(const f of fs.readdirSync(__dirname).filter(f=>/^\d\d-.*\.html$/.test(f))){
 await p.goto('file://'+path.join(__dirname,f),{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);
 const bad=await p.evaluate(()=>[...document.images].filter(i=>!i.naturalWidth).length);if(bad)throw Error(f+' broken images');
 await p.screenshot({path:path.join(__dirname,f.replace('.html','.png'))});console.log(f);}
await b.close();})();
