const {chromium}=require('playwright');const path=require('path');const fs=require('fs');
(async()=>{const ts=(process.argv[2]||'2,7,11,15,20,24,29,34,38,43,47,50,53,55').split(',').map(Number);const out=path.join(__dirname,'out','preview');fs.mkdirSync(out,{recursive:true});
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1080}});
await p.goto('file://'+path.join(__dirname,'out','film.html'),{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);
for(const t of ts){await p.evaluate(t=>setT(t),t);await p.screenshot({path:path.join(out,`f-${t}.jpg`),type:'jpeg',quality:80});}
await b.close();})();
