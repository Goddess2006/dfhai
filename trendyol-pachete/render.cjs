// Randare build/<pachet>/*.html -> out/<pachet>/*.jpg (1200x1800). Rulare: node render.cjs
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const B=path.join(__dirname,'build'),O=path.join(__dirname,'out');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1200,height:1800}});
for(const d of fs.readdirSync(B).sort()){for(const f of fs.readdirSync(path.join(B,d)).filter(f=>f.endsWith('.html')).sort()){
 await p.goto('file://'+path.join(B,d,f),{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);
 const bad=await p.evaluate(()=>[...document.images].filter(i=>!i.naturalWidth).map(i=>i.src));if(bad.length)throw Error(d+'/'+f+' imagini lipsă '+bad);
 fs.mkdirSync(path.join(O,d),{recursive:true});
 await p.screenshot({path:path.join(O,d,f.replace('.html','.jpg')),type:'jpeg',quality:90});console.log(d+'/'+f);}}
await b.close();})();
