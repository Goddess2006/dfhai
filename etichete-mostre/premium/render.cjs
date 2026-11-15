// npm ci; npx playwright install --with-deps chromium; npm run build; npm run render
const {chromium}=require('playwright');
const {PDFDocument}=require('pdf-lib');
const fs=require('node:fs/promises');
const path=require('node:path');
(async()=>{
 const browser=await chromium.launch({headless:true});
 const page=await browser.newPage({viewport:{width:1000,height:1300},deviceScaleFactor:3});
 for(const theme of ['mono','color']){
  const stem=path.join(__dirname,`etichete-${theme}-A4`);
  await page.goto('file://'+stem+'.html');
  await page.emulateMedia({media:'print'});
  await page.evaluate(()=>document.fonts.ready);
  const checks=await page.evaluate(()=>({labels:document.querySelectorAll('.label').length,fonts:document.fonts.check('600 16px "Cormorant Garamond"')&&document.fonts.check('400 16px Montserrat'),overflow:[...document.querySelectorAll('.label')].filter(e=>e.scrollHeight>e.clientHeight+1).length,contentOverflow:[...document.querySelectorAll('.frame')].filter(e=>e.scrollHeight>e.clientHeight+1).length,brokenImages:[...document.images].filter(e=>!e.complete||e.naturalWidth===0).length}));
  if(checks.labels!==4||!checks.fonts||checks.overflow||checks.contentOverflow||checks.brokenImages)throw Error(JSON.stringify(checks));
  await page.pdf({path:stem+'.pdf',format:'A4',printBackground:true,preferCSSPageSize:true,margin:{top:0,bottom:0,left:0,right:0}});
  const pdf=await PDFDocument.load(await fs.readFile(stem+'.pdf'));
  if(pdf.getPageCount()!==1)throw Error('PDF must contain exactly one A4 sheet');
  await page.locator('.label').first().screenshot({path:path.join(__dirname,`apercu-${theme}.png`)});
  const {PNG}=require('pngjs'),jsQR=require('jsqr');
  const png=PNG.sync.read(await fs.readFile(path.join(__dirname,`apercu-${theme}.png`)));
  const decoded=jsQR(new Uint8ClampedArray(png.data),png.width,png.height);
  if(decoded?.data!=='https://decoflair.ro/bagheta-polistiren')throw Error('QR decode failed');
  if(theme==='mono'){for(let i=0;i<png.data.length;i+=4){if(Math.max(...png.data.subarray(i,i+3))-Math.min(...png.data.subarray(i,i+3))>1)throw Error('Color found in monochrome label');}}
  await page.locator('.sheet').screenshot({path:path.join(__dirname,`coala-${theme}.png`)});
  console.log(theme,JSON.stringify(checks),'PDF pages:',pdf.getPageCount(),'size:',pdf.getPage(0).getSize());
 }
 // Comparison is another browser rendering of the actual labels.
 await page.emulateMedia({media:'screen'});
 await page.setViewportSize({width:900,height:680});
 await page.setContent(`<style>body{margin:0;background:#e9e7e2;padding:28px;display:flex;gap:24px;font:12px sans-serif}figure{margin:0;flex:1}img{width:100%;display:block}figcaption{text-align:center;padding:12px;color:#343b36;letter-spacing:2px}</style><figure><img src="file://${__dirname}/apercu-mono.png"><figcaption>ALB-NEGRU</figcaption></figure><figure><img src="file://${__dirname}/apercu-color.png"><figcaption>COLOR PREMIUM</figcaption></figure>`);
 await page.evaluate(()=>Promise.all([...document.images].map(i=>i.decode())));
 await page.screenshot({path:path.join(__dirname,'comparatie.png'),fullPage:true});
 await browser.close();
})();
