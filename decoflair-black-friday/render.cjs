// Randare PNG: feed 1080x1350 (./NN-*.html) si story 1080x1920 (./story/*.html). Rulare: node render.cjs
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const files=[...fs.readdirSync(__dirname).filter(f=>/^\d\d-.*\.html$/.test(f)),
  ...fs.readdirSync(path.join(__dirname,'story')).filter(f=>f.endsWith('.html')).map(f=>'story/'+f)];
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1350}});
for(const f of files){
 await p.setViewportSize({width:1080,height:f.startsWith('story/')?1920:1350});
 await p.goto('file://'+path.join(__dirname,f),{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);
 const bad=await p.evaluate(()=>[...document.images].filter(i=>!i.naturalWidth).length);if(bad)throw Error(f+' broken images');
 await p.screenshot({path:path.join(__dirname,f.replace('.html','.png'))});console.log(f);}
await b.close();})();
