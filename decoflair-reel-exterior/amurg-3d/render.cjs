const { createHash } = require('node:crypto');
const fs = require('node:fs/promises');
const { tmpdir } = require('node:os');
const { join, dirname, resolve } = require('node:path');
const { pathToFileURL } = require('node:url');
const { once } = require('node:events');
const { spawn } = require('node:child_process');
const { parseArgs } = require('node:util');
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');

const FPS = 24;
const FRAMES = FPS * 15;
const { values: args } = parseArgs({ options: {
  three: { type: 'string' },
  chromium: { type: 'string' },
  ffmpeg: { type: 'string', default: 'ffmpeg' },
  output: { type: 'string' },
  preview: { type: 'boolean' },
}});

async function main() {
  if (!args.three || !args.output) throw new Error('Pass --three and --output.');
  const three = await fs.readFile(args.three);
  const digest = createHash('sha256').update(three).digest('hex');
  if (digest !== '170c6789f43217c96b3170f4b42fafe135de7f7cd48497a4218f9757ee1d49fa') throw new Error('Use the pinned Three.js build documented in README.md.');

  const site = await fs.mkdtemp(join(tmpdir(), 'ncl107-3d-'));
  let browser;
  try {
    for (const name of ['index.html', 'scene.js']) {
      await fs.copyFile(join(__dirname, name), join(site, name));
    }
    await fs.writeFile(join(site, 'three.min.js'), three);
    const [width, height] = args.preview ? [405, 720] : [1080, 1920];
    browser = await chromium.launch({
      executablePath: args.chromium,
      args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'],
    });
    const page = await browser.newPage({ viewport: { width, height } });
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    page.on('console', message => {
      if (message.type() === 'error') errors.push(message.text());
    });
    const url = pathToFileURL(join(site, 'index.html'));
    url.search = new URLSearchParams({ width, height });
    await page.goto(url.href);
    async function capture(frame) {
      const data = await page.evaluate(
        ([index, fps]) => window.renderFrame(index, fps).toDataURL('image/jpeg', .96).split(',')[1],
        [frame, FPS],
      );
      if (errors.length) throw new Error(errors.join('\n'));
      return Buffer.from(data, 'base64');
    }

    if (args.preview) {
      await fs.mkdir(args.output, { recursive: true });
      for (const frame of [0, 36, 80, 144, 224, 320, 359]) {
        await fs.writeFile(join(args.output, String(frame).padStart(3, '0') + '.jpg'), await capture(frame));
      }
      return;
    }

    const output = resolve(args.output);
    await fs.mkdir(dirname(output), { recursive: true });
    const partial = output + '.partial.mp4';
    const ffmpeg = spawn(args.ffmpeg, [
      '-hide_banner', '-loglevel', 'error', '-y', '-f', 'image2pipe', '-framerate', String(FPS),
      '-c:v', 'mjpeg', '-threads', '1', '-i', '-', '-an',
      '-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p',
      '-colorspace', 'bt709', '-color_trc', 'bt709', '-color_primaries', 'bt709',
      '-c:v', 'libx264', '-threads', '2', '-preset', 'veryfast', '-crf', '15',
      '-movflags', '+faststart', partial,
    ], { stdio: ['pipe', 'inherit', 'inherit'] });
    ffmpeg.stdin.on('error', error => { errors.push(error.message); });
    const done = once(ffmpeg, 'close').catch(error => { errors.push(error.message); return [1]; });
    try {
      for (let frame = 0; frame < FRAMES; frame++) {
        if (!ffmpeg.stdin.write(await capture(frame))) await once(ffmpeg.stdin, 'drain');
        if (frame % FPS === 0) process.stdout.write('Randat ' + (frame + 1) + '/' + FRAMES + '\n');
      }
      ffmpeg.stdin.end();
      const [code] = await done;
      if (code !== 0) throw new Error('FFmpeg exited with code ' + code);
      await fs.rename(partial, output);
    } finally {
      ffmpeg.stdin.destroy();
      if (ffmpeg.exitCode === null) ffmpeg.kill();
      await done;
      await fs.rm(partial, { force: true });
    }
  } finally {
    if (browser) await browser.close();
    await fs.rm(site, { recursive: true, force: true });
  }
}

main().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
