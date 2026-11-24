// Randează reel/reel-<variantă>.html cadru cu cadru (30 fps) → MP4 H.264 1080x1920.
// Rulare: node reel_render.cjs organic   |   node reel_render.cjs ads
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');const {execFileSync}=require('child_process');
const V=process.argv[2]||'organic', FPS=30, dir=path.join(__dirname,'reel'), frames=path.join(dir,'frames-'+V);
(async()=>{fs.rmSync(frames,{recursive:true,force:true});fs.mkdirSync(frames,{recursive:true});
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+path.join(dir,'reel-'+V+'.html'),{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);
const total=await p.evaluate(()=>window.TOTAL);const n=Math.round(total*FPS);
for(let i=0;i<n;i++){await p.evaluate(t=>setT(t),i/FPS);
 await p.screenshot({path:path.join(frames,String(i).padStart(5,'0')+'.jpg'),type:'jpeg',quality:94});}
await b.close();
execFileSync('ffmpeg',['-y','-loglevel','error','-framerate',String(FPS),'-i',path.join(frames,'%05d.jpg'),
 '-c:v','libx264','-pix_fmt','yuv420p','-preset','slow','-crf','23','-maxrate','9M','-bufsize','18M','-movflags','+faststart',path.join(dir,'decoflair-reel-interior-'+V+'.mp4')]);
fs.rmSync(frames,{recursive:true,force:true});
console.log('frames',n,'seconds',total.toFixed(1));})();
