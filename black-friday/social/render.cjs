// Randează imaginile Facebook din facebook.html. Rulare: node black-friday/social/render.cjs
const path = require('path');
const { chromium } = require('playwright');
const formats = { portrait: [1080, 1350], square: [1080, 1080], link: [1200, 630] };
(async () => {
  const browser = await chromium.launch();
  for (const [name, [width, height]] of Object.entries(formats)) {
    const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: 1 });
    await page.goto('file://' + path.join(__dirname, 'facebook.html') + '?f=' + name, { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    const out = path.join(__dirname, `facebook-black-friday-${name}-${width}x${height}.png`);
    await page.screenshot({ path: out, clip: { x: 0, y: 0, width, height } });
    console.log(out);
  }
  await browser.close();
})();
