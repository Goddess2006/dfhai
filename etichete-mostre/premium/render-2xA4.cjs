// 2 etichete A5 pe A4 orizontal. Rulare: node render-2xA4.cjs (după python3 build.py)
const {chromium}=require('playwright');const path=require('node:path');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1300,height:900},deviceScaleFactor:2});
for(const t of ['mono','color']){const stem=path.join(__dirname,`etichete-${t}-2xA4`);
 await p.goto('file://'+stem+'.html');await p.emulateMedia({media:'print'});await p.evaluate(()=>document.fonts.ready);
 const c=await p.evaluate(()=>({labels:document.querySelectorAll('.label').length,overflow:[...document.querySelectorAll('.frame')].filter(e=>e.scrollHeight>e.clientHeight+1).length,broken:[...document.images].filter(i=>!i.naturalWidth).length}));
 if(c.labels!==2||c.overflow||c.broken)throw Error(JSON.stringify(c));
 await p.pdf({path:stem+'.pdf',preferCSSPageSize:true,printBackground:true});
 await p.locator('.sheet').screenshot({path:path.join(__dirname,`coala-${t}-2xA4.png`)});console.log(t,c);}
await b.close();})();
