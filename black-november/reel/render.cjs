// Reel Black November: randează reel.html cadru cu cadru (30 fps) → MP4 H.264 1080×1920 + copertă.
// Rulare: node black-november/reel/render.cjs   (necesită Playwright + ffmpeg)
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path'); const { execFileSync } = require('child_process');
const FPS = 30, dir = __dirname, frames = path.join(dir, 'frames');
const only = process.argv[2]; // opțional: secunde separate prin virgulă → doar previzualizări PNG
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.join(dir, 'reel.html'), { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await p.waitForFunction(() => [...document.images].every(i => i.complete));
  if (only) {
    for (const s of only.split(',')) { await p.evaluate(t => setT(t), +s); await p.screenshot({ path: path.join(dir, `preview-${s}.png`) }); }
    await b.close(); return;
  }
  fs.rmSync(frames, { recursive: true, force: true }); fs.mkdirSync(frames, { recursive: true });
  const total = await p.evaluate(() => window.TOTAL); const n = Math.round(total * FPS);
  for (let i = 0; i < n; i++) {
    await p.evaluate(t => setT(t), i / FPS);
    await p.screenshot({ path: path.join(frames, String(i).padStart(5, '0') + '.jpg'), type: 'jpeg', quality: 93 });
  }
  await p.evaluate(t => setT(t), 24.2);
  await p.screenshot({ path: path.join(dir, 'coperta-reel-black-november.jpg'), type: 'jpeg', quality: 92 });
  await b.close();
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-framerate', String(FPS), '-i', path.join(frames, '%05d.jpg'),
    '-c:v', 'libx264', '-profile:v', 'high', '-pix_fmt', 'yuv420p', '-preset', 'slow', '-crf', '18', '-movflags', '+faststart',
    path.join(dir, 'reel-black-november-nmc.mp4')]);
  fs.rmSync(frames, { recursive: true, force: true });
  console.log('cadre', n, 'secunde', total);
})();
