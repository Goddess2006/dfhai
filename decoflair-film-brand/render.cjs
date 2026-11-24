// Randează out/film.html cadru cu cadru (30 fps, 1920x1080) și combină cu out/muzica.wav → out/decoflair-film-prezentare.mp4
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');const {execFileSync}=require('child_process');
const FPS=30, dir=path.join(__dirname,'out'), frames=path.join(dir,'frames');
(async()=>{fs.rmSync(frames,{recursive:true,force:true});fs.mkdirSync(frames,{recursive:true});
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1080}});
await p.goto('file://'+path.join(dir,'film.html'),{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);
const total=await p.evaluate(()=>window.TOTAL);const n=Math.round(total*FPS);
for(let i=0;i<n;i++){await p.evaluate(t=>setT(t),i/FPS);await p.screenshot({path:path.join(frames,String(i).padStart(5,'0')+'.jpg'),type:'jpeg',quality:93});}
await b.close();
execFileSync('ffmpeg',['-y','-loglevel','error','-framerate',String(FPS),'-i',path.join(frames,'%05d.jpg'),'-i',path.join(dir,'muzica.wav'),
 '-c:v','libx264','-pix_fmt','yuv420p','-preset','slow','-crf','19','-maxrate','16M','-bufsize','32M','-c:a','aac','-b:a','256k','-shortest','-movflags','+faststart',path.join(dir,'decoflair-film-prezentare.mp4')]);
fs.rmSync(frames,{recursive:true,force:true});console.log('frames',n,'seconds',total.toFixed(1));})();
