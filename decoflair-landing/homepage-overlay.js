/*!
 * Selecția Premium · Deco&Flair — afișare peste homepage
 * --------------------------------------------------------------
 * Se include O SINGURĂ DATĂ pe homepage, înainte de </body>:
 *
 *   <script defer src="/selectia-premium/homepage-overlay.js"></script>
 *
 * Opțiuni (atribute data-* pe tag, toate opționale):
 *   data-enabled="false"          dezactivează complet afișarea
 *   data-frequency="session"      session (implicit) = o dată pe sesiune de navigare
 *                                 day     = o dată la 24 de ore
 *                                 always  = la fiecare intrare pe homepage (pentru test)
 *   data-ends="AAAA-LL-ZZT00:00:00+02:00"  opțional: după această dată nu mai apare (implicit: fără dată de final)
 *   data-delay="400"              întârziere în ms înainte de afișare
 *
 * Pentru test pe site: adaugă ?df=1 la homepage (ex. https://www.decoflair.ro/?df=1)
 * ca să forțezi afișarea, indiferent de frecvență.
 * Pentru a redeschide din alt buton/banner: window.DecoFlairPremium.open()
 */
(function () {
  'use strict';
  var script = document.currentScript;
  if (!script || script.dataset.enabled === 'false' || window.top !== window || window.DecoFlairPremium) return;

  var d = document, params = new URLSearchParams(location.search);
  var force = params.get('df') === '1';

  // doar pe homepage: / , /index.php , /index.php?route=common/home (și variantele de limbă /ro/)
  var path = location.pathname.replace(/\/+$/, '/') || '/';
  var route = params.get('route');
  var isHome = /^\/([a-z]{2}\/)?(index\.php)?$/.test(path) && (!route || route === 'common/home');
  if (!isHome && !force) return;

  var ends = script.dataset.ends ? Date.parse(script.dataset.ends) : 0;
  if (!force && ends && Date.now() > ends) return;

  var src = new URL('index.html?overlay=1', script.src);
  if (src.origin !== location.origin) return; // landing-ul trebuie să fie pe același domeniu

  var freq = script.dataset.frequency || 'session';
  var KEY = 'decoflair:selectia-premium';
  function seen() {
    try {
      if (freq === 'always') return false;
      if (freq === 'day') { var t = +localStorage.getItem(KEY); return t && Date.now() - t < 864e5; }
      return sessionStorage.getItem(KEY) === '1';
    } catch (e) { return false; }
  }
  function remember() {
    try {
      if (freq === 'day') localStorage.setItem(KEY, String(Date.now()));
      else sessionStorage.setItem(KEY, '1');
    } catch (e) { /* storage blocat: overlay-ul se poate închide oricum */ }
  }

  var root, frame, prevFocus, prevOverflow;

  function css() {
    if (d.getElementById('df-overlay-css')) return;
    var s = d.createElement('style'); s.id = 'df-overlay-css';
    s.textContent =
      '#df-overlay{position:fixed;inset:0;z-index:2147483646;background:#F4EEE6;opacity:0;transition:opacity .45s ease}' +
      '#df-overlay.is-in{opacity:1}' +
      '#df-overlay iframe{display:block;width:100%;height:100%;border:0;background:#F4EEE6}' +
      '#df-overlay .df-x{position:absolute;z-index:2;right:max(14px,env(safe-area-inset-right));top:calc(54px + env(safe-area-inset-top));display:inline-flex;align-items:center;gap:10px;height:42px;padding:0 16px 0 18px;border-radius:999px;border:1px solid rgba(20,18,20,.18);background:rgba(251,248,243,.85);color:#141214;font:500 11.5px/1 Jost,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;letter-spacing:.16em;text-transform:uppercase;cursor:pointer;backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);box-shadow:0 10px 30px -14px rgba(20,18,20,.45);transition:background .25s,border-color .25s}' +
      '#df-overlay .df-x:hover,#df-overlay .df-x:focus-visible{background:#141214;color:#F4EEE6;border-color:#141214;outline:none}' +
      '#df-overlay .df-x b{font:300 20px/1 system-ui;letter-spacing:0;margin-top:-2px}' +
      '@media (max-width:520px){#df-overlay .df-x{top:calc(46px + env(safe-area-inset-top));height:38px;padding:0 12px 0 14px;font-size:10px;letter-spacing:.1em}#df-overlay .df-x span{display:none}}' +
      '@media (prefers-reduced-motion:reduce){#df-overlay{transition:none}}';
    d.head.appendChild(s);
  }

  function close() {
    remember();
    if (!root) return;
    root.classList.remove('is-in');
    var el = root; root = null; frame = null;
    d.documentElement.style.overflow = prevOverflow;
    d.removeEventListener('keydown', onKey, true);
    setTimeout(function () { el.remove(); }, 400);
    if (prevFocus && prevFocus.focus) try { prevFocus.focus(); } catch (e) {}
  }
  function onKey(ev) { if (ev.key === 'Escape') { ev.preventDefault(); close(); } }

  function open() {
    if (root) return;
    css();
    prevFocus = d.activeElement;
    root = d.createElement('div');
    root.id = 'df-overlay';
    root.setAttribute('role', 'dialog');
    root.setAttribute('aria-modal', 'true');
    root.setAttribute('aria-label', 'Selecția Premium · Deco&Flair');

    var btn = d.createElement('button');
    btn.type = 'button'; btn.className = 'df-x';
    btn.setAttribute('aria-label', 'Închide Selecția Premium și intră în magazin');
    btn.innerHTML = '<span>Intră în magazin</span><b aria-hidden="true">×</b>';
    btn.addEventListener('click', close);

    frame = d.createElement('iframe');
    frame.src = src.href;
    frame.title = 'Selecția Premium · Deco&Flair';
    frame.setAttribute('allow', 'clipboard-write');

    root.appendChild(frame); root.appendChild(btn);
    prevOverflow = d.documentElement.style.overflow;
    d.documentElement.style.overflow = 'hidden';
    d.body.appendChild(root);
    d.addEventListener('keydown', onKey, true);
    requestAnimationFrame(function () { root && root.classList.add('is-in'); });
    btn.focus({ preventScroll: true });
  }

  // mesaje din landing (df.js): închidere, navigare spre magazin, coș actualizat
  window.addEventListener('message', function (ev) {
    if (!frame || ev.source !== frame.contentWindow || ev.origin !== location.origin) return;
    var m = ev.data;
    if (m === 'df:lp:close') close();
    if (m === 'df:lp:navigate') remember();
    if (m === 'df:lp:cart') remember();
  });

  window.DecoFlairPremium = { open: open, close: close, dismiss: remember };

  function init() {
    if (!force && seen()) return;
    setTimeout(open, Math.max(0, +script.dataset.delay || 400));
  }
  if (d.readyState === 'loading') d.addEventListener('DOMContentLoaded', init, { once: true });
  else init();
})();
