// Randează tiktok/tiktok-{ads,organic}.html cadru cu cadru (30 fps) → MP4 H.264 + previzualizare cu zonele TikTok.
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');const {execFileSync}=require('child_process');
const FPS=30, dir=path.join(__dirname,'tiktok');
(async()=>{const b=await chromium.launch();
for(const v of ['ads','organic']){const frames=path.join(dir,'frames-'+v);fs.rmSync(frames,{recursive:true,force:true});fs.mkdirSync(frames,{recursive:true});
 const p=await b.newPage({viewport:{width:1080,height:1920}});
 await p.goto('file://'+path.join(dir,`tiktok-${v}.html`),{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);
 const total=await p.evaluate(()=>window.TOTAL);const n=Math.round(total*FPS);
 for(let i=0;i<n;i++){await p.evaluate(t=>setT(t),i/FPS);await p.screenshot({path:path.join(frames,String(i).padStart(5,'0')+'.jpg'),type:'jpeg',quality:94});}
 await p.close();
 execFileSync('ffmpeg',['-y','-loglevel','error','-framerate',String(FPS),'-i',path.join(frames,'%05d.jpg'),'-c:v','libx264','-pix_fmt','yuv420p','-preset','slow','-crf','18','-movflags','+faststart',path.join(dir,`nmc-wow-30-tiktok-${v}.mp4`)]);
 fs.rmSync(frames,{recursive:true,force:true});console.log(v,n,total.toFixed(1));}
await b.close();})();
