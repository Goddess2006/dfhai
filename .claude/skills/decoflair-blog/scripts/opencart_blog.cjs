#!/usr/bin/env node
/*
 Blog decoflair.ro (OpenCart + Journal3) din linia de comandă, printr-un browser Playwright logat în admin.

 Variabile de mediu (setate în environment, NICIODATĂ în repo sau în chat):
   DECOFLAIR_ADMIN_URL   ex. https://decoflair.ro/<folder-admin>/   (adresa paginii de login admin)
   DECOFLAIR_ADMIN_USER  utilizator admin dedicat (recomandat: grup cu drepturi doar pe Journal3 blog + Image Manager)
   DECOFLAIR_ADMIN_PASS

 Comenzi:
   login-test                         verifică logarea (nu afișează tokenul)
   capture [--out capture.json]       deschide editorul de blog Journal3 și înregistrează cererile AJAX ->
                                      confirmă rutele și formatul datelor la prima rulare (fără modificări)
   list                               lista articolelor (id, titlu, status)
   get --id N [--out post.json]       articol existent ca JSON (șablonul pentru articole noi)
   upload --dir blog/<slug> f1.jpg …  urcă imagini în Image Manager -> catalog/blog/<slug>/
   create --json post.json            creează articolul (pune status 0 = nepublicat în JSON)
   set-status --id N --status 1|0     publică / ascunde (folosit de sesiunea programată la ora publicării)
   screenshot --url <url> --out f.png captură a paginii publice

 Rutele Journal3 implicite se pot suprascrie în endpoints.json (lângă script) după `capture`.
*/
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const cmd = args[0];
const opt = (k, d) => { const i = args.indexOf('--' + k); return i > -1 ? args[i + 1] : d; };
const files = args.slice(1).filter((a, i, all) => !a.startsWith('--') && !(all[i - 1] || '').startsWith('--'));

const EP_FILE = path.join(__dirname, 'endpoints.json');
const EP = Object.assign({
  list: 'journal3/blog_post/all',
  get: 'journal3/blog_post/get',
  add: 'journal3/blog_post/add',
  edit: 'journal3/blog_post/edit',
  bodyMode: 'form-data-json', // 'form-data-json' = câmpul POST "data" cu JSON; 'json' = corp JSON
  editor: 'journal3/journal3',
  upload: 'common/filemanager/upload',
}, fs.existsSync(EP_FILE) ? JSON.parse(fs.readFileSync(EP_FILE, 'utf8')) : {});

function env(k) { const v = process.env[k]; if (!v) { console.error(`Lipsește ${k} în mediul sesiunii.`); process.exit(2); } return v; }

async function login() {
  const adminUrl = env('DECOFLAIR_ADMIN_URL').replace(/\/?$/, '/');
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ locale: 'ro-RO' });
  const page = await ctx.newPage();
  await page.goto(adminUrl, { waitUntil: 'domcontentloaded' });
  await page.fill('input[name="username"]', env('DECOFLAIR_ADMIN_USER'));
  await page.fill('input[name="password"]', env('DECOFLAIR_ADMIN_PASS'));
  await Promise.all([page.waitForLoadState('networkidle').catch(() => {}), page.click('button[type="submit"], input[type="submit"]')]);
  await page.waitForTimeout(1500);
  const m = page.url().match(/[?&](user_token|token)=([^&#]+)/);
  if (!m) { await browser.close(); throw new Error('Logare eșuată (fără token în URL). Verifică adresa, utilizatorul, parola sau 2FA.'); }
  const tk = { name: m[1], value: m[2] };
  const u = (route, extra = '') => `${adminUrl}index.php?route=${route}&${tk.name}=${tk.value}${extra}`;
  return { browser, ctx, page, u, adminUrl };
}

async function call(s, route, { method = 'GET', data, extra = '' } = {}) {
  const url = s.u(route, extra);
  let res;
  if (method === 'GET') res = await s.page.request.get(url);
  else if (EP.bodyMode === 'json') res = await s.page.request.post(url, { data });
  else res = await s.page.request.post(url, { form: { data: JSON.stringify(data) } });
  const txt = await res.text();
  try { return JSON.parse(txt); } catch { throw new Error(`Răspuns ne-JSON (${res.status()}) de la ${route}: ${txt.slice(0, 300)}`); }
}

(async () => {
  if (!cmd) { console.log(fs.readFileSync(__filename, 'utf8').split('*/')[0]); return; }
  if (cmd === 'screenshot') {
    const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 900 } });
    await p.goto(opt('url'), { waitUntil: 'networkidle' }); await p.screenshot({ path: opt('out', 'preview.png'), fullPage: true });
    await b.close(); return;
  }
  const s = await login();
  try {
    if (cmd === 'login-test') {
      console.log('Logare reușită. Titlu pagină:', await s.page.title());
    } else if (cmd === 'capture') {
      const log = [];
      s.page.on('response', async (r) => {
        const url = r.url();
        if (!/route=journal3\//.test(url)) return;
        let body = ''; try { body = (await r.text()).slice(0, 4000); } catch {}
        log.push({ url: url.replace(/(user_token|token)=[^&]+/, '$1=***'), method: r.request().method(),
                   post: (r.request().postData() || '').slice(0, 2000), status: r.status(), body });
      });
      await s.page.goto(s.u(EP.editor) + '#/blog_post', { waitUntil: 'networkidle' });
      await s.page.waitForTimeout(4000);
      const first = s.page.locator('a[href*="blog_post/edit"], a[href*="#/blog_post/edit"]').first();
      if (await first.count()) { await first.click(); await s.page.waitForTimeout(4000); }
      fs.writeFileSync(opt('out', 'capture.json'), JSON.stringify(log, null, 1));
      await s.page.screenshot({ path: 'capture.png', fullPage: true });
      console.log(`${log.length} cereri Journal3 salvate în ${opt('out', 'capture.json')} (+ capture.png). Nimic nu a fost modificat.`);
    } else if (cmd === 'list') {
      const r = await call(s, EP.list);
      const items = (r.response && (r.response.items || r.response)) || r.items || r;
      for (const p of [].concat(items)) console.log(p.id ?? p.blog_post_id, p.status ?? '', p.name ?? p.title ?? JSON.stringify(p).slice(0, 80));
    } else if (cmd === 'get') {
      const r = await call(s, EP.get, { extra: `&id=${opt('id')}` });
      const out = opt('out'); const js = JSON.stringify(r, null, 1);
      if (out) { fs.writeFileSync(out, js); console.log('Salvat', out); } else console.log(js);
    } else if (cmd === 'upload') {
      const dir = opt('dir'); if (!dir || !files.length) throw new Error('upload --dir blog/<slug> fisier1 fisier2 …');
      // creează folderul (ignoră eroarea dacă există), apoi urcă fiecare fișier
      const parent = path.posix.dirname(dir) === '.' ? '' : path.posix.dirname(dir);
      await s.page.request.post(s.u('common/filemanager/folder', `&directory=${encodeURIComponent(parent)}`), { multipart: { folder: path.posix.basename(dir) } }).catch(() => {});
      for (const f of files) {
        const r = await s.page.request.post(s.u(EP.upload, `&directory=${encodeURIComponent(dir)}`), {
          multipart: { 'file[]': { name: path.basename(f), mimeType: f.endsWith('.png') ? 'image/png' : f.endsWith('.webp') ? 'image/webp' : 'image/jpeg', buffer: fs.readFileSync(f) } } });
        const t = await r.text();
        console.log(path.basename(f), '->', /error/i.test(t) ? t.slice(0, 200) : `image/catalog/${dir}/${path.basename(f)}`);
      }
    } else if (cmd === 'create') {
      const data = JSON.parse(fs.readFileSync(opt('json'), 'utf8'));
      const r = await call(s, EP.add, { method: 'POST', data });
      console.log(JSON.stringify(r).slice(0, 500));
    } else if (cmd === 'set-status') {
      const id = opt('id'); const r = await call(s, EP.get, { extra: `&id=${id}` });
      const data = r.response || r; data.status = String(opt('status')) === '1' ? '1' : '0';
      const w = await call(s, EP.edit, { method: 'POST', data, extra: `&id=${id}` });
      console.log(`Articol ${id}: status=${data.status}`, JSON.stringify(w).slice(0, 200));
    } else throw new Error('Comandă necunoscută: ' + cmd);
  } finally { await s.browser.close(); }
})().catch((e) => { console.error(e.message); process.exit(1); });
