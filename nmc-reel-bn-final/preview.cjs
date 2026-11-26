// Previzualizare: capturi la momente cheie -> reel/preview/*.jpg
const {chromium}=require('playwright');const path=require('path');const fs=require('fs');
(async()=>{const v=process.argv[2]||'organic';const ts=(process.argv[3]||'1,3.5,5.2,7.8,9.5,10.9,12.7,14.5,16.3,19.5,21.5,24').split(',').map(Number);
const out=path.join(__dirname,'reel','preview');fs.mkdirSync(out,{recursive:true});
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+path.join(__dirname,'reel',`nmc-bn-${v}.html`),{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);
for(const t of ts){await p.evaluate(t=>setT(t),t);await p.screenshot({path:path.join(out,`${v}-${t}.jpg`),type:'jpeg',quality:80});}
await b.close();})();
