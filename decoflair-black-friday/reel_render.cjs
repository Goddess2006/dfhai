// Randează reel/reel.html cadru cu cadru (30 fps) și îl codează MP4 H.264 1080x1920 cu ffmpeg.
// Rulare: node reel_render.cjs
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');const {execFileSync}=require('child_process');
const FPS=30, dir=path.join(__dirname,'reel'), frames=path.join(dir,'frames');
(async()=>{fs.rmSync(frames,{recursive:true,force:true});fs.mkdirSync(frames,{recursive:true});
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+path.join(dir,'reel.html'),{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);
const total=await p.evaluate(()=>window.TOTAL);const n=Math.round(total*FPS);
for(let i=0;i<n;i++){await p.evaluate(t=>setT(t),i/FPS);
 await p.screenshot({path:path.join(frames,String(i).padStart(5,'0')+'.jpg'),type:'jpeg',quality:94});}
await b.close();
execFileSync('ffmpeg',['-y','-loglevel','error','-framerate',String(FPS),'-i',path.join(frames,'%05d.jpg'),
 '-c:v','libx264','-pix_fmt','yuv420p','-preset','slow','-crf','18','-movflags','+faststart',path.join(dir,'decoflair-black-friday-reel.mp4')]);
fs.rmSync(frames,{recursive:true,force:true});
console.log('frames',n,'seconds',total.toFixed(1));})();
