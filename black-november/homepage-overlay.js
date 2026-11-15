/*!
 * Black November · NMC România — afișare peste homepage
 * --------------------------------------------------------------
 * Se include O SINGURĂ DATĂ pe homepage, înainte de </body>:
 *
 *   <script defer src="/black-november/homepage-overlay.js"></script>
 *
 * Opțiuni (atribute data-* pe tag, toate opționale):
 *   data-enabled="false"          dezactivează complet afișarea
 *   data-frequency="session"      session (implicit) = o dată pe sesiune de navigare
 *                                 day     = o dată la 24 de ore
 *                                 always  = la fiecare intrare pe homepage (pentru test)
 *   data-ends="2026-12-01T00:00:00+02:00"  după această dată nu mai apare (implicit 1 dec. 2026)
 *   data-delay="400"              întârziere în ms înainte de afișare
 *
 * Pentru test pe site: adaugă ?bn=1 la homepage (ex. https://www.nmcromania.ro/?bn=1)
 * ca să forțezi afișarea, indiferent de frecvență.
 * Pentru a redeschide din alt buton/banner: window.NMCBlackNovember.open()
 */
(function () {
  'use strict';
  var script = document.currentScript;
  if (!script || script.dataset.enabled === 'false' || window.top !== window || window.NMCBlackNovember) return;

  var d = document, params = new URLSearchParams(location.search);
  var force = params.get('bn') === '1';

  // doar pe homepage: / , /index.php , /index.php?route=common/home (și variantele de limbă /ro/)
  var path = location.pathname.replace(/\/+$/, '/') || '/';
  var route = params.get('route');
  var isHome = /^\/([a-z]{2}\/)?(index\.php)?$/.test(path) && (!route || route === 'common/home');
  if (!isHome && !force) return;

  var ends = Date.parse(script.dataset.ends || '2026-12-01T00:00:00+02:00');
  if (!force && ends && Date.now() > ends) return;

  var src = new URL('index.html?overlay=1', script.src);
  if (src.origin !== location.origin) return; // landing-ul trebuie să fie pe același domeniu

  var freq = script.dataset.frequency || 'session';
  var KEY = 'nmc:black-november:2026';
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
    if (d.getElementById('bn-overlay-css')) return;
    var s = d.createElement('style'); s.id = 'bn-overlay-css';
    s.textContent =
      '#bn-overlay{position:fixed;inset:0;z-index:2147483646;background:#070A09;opacity:0;transition:opacity .45s ease}' +
      '#bn-overlay.is-in{opacity:1}' +
      '#bn-overlay iframe{display:block;width:100%;height:100%;border:0;background:#070A09}' +
      '#bn-overlay .bn-x{position:absolute;z-index:2;right:max(14px,env(safe-area-inset-right));top:calc(50px + env(safe-area-inset-top));display:inline-flex;align-items:center;gap:10px;height:42px;padding:0 16px 0 18px;border-radius:999px;border:1px solid rgba(255,255,255,.22);background:rgba(7,10,9,.78);color:#F2ECE3;font:500 11.5px/1 Inter,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;letter-spacing:.16em;text-transform:uppercase;cursor:pointer;backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);box-shadow:0 10px 30px -12px #000;transition:background .25s,border-color .25s}' +
      '#bn-overlay .bn-x:hover,#bn-overlay .bn-x:focus-visible{background:#2A0B23;border-color:#E3A6C6;outline:none}' +
      '#bn-overlay .bn-x b{font:300 20px/1 system-ui;letter-spacing:0;margin-top:-2px}' +
      '@media (max-width:520px){#bn-overlay .bn-x{top:calc(47px + env(safe-area-inset-top));height:38px;padding:0 12px 0 14px;font-size:10px;letter-spacing:.1em}#bn-overlay .bn-x span{display:none}}' +
      '@media (prefers-reduced-motion:reduce){#bn-overlay{transition:none}}';
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
    root.id = 'bn-overlay';
    root.setAttribute('role', 'dialog');
    root.setAttribute('aria-modal', 'true');
    root.setAttribute('aria-label', 'Black November · NMC România');

    var btn = d.createElement('button');
    btn.type = 'button'; btn.className = 'bn-x';
    btn.setAttribute('aria-label', 'Închide Black November și intră în magazin');
    btn.innerHTML = '<span>Intră în magazin</span><b aria-hidden="true">×</b>';
    btn.addEventListener('click', close);

    frame = d.createElement('iframe');
    frame.src = src.href;
    frame.title = 'Black November · NMC România';
    frame.setAttribute('allow', 'clipboard-write');

    root.appendChild(frame); root.appendChild(btn);
    prevOverflow = d.documentElement.style.overflow;
    d.documentElement.style.overflow = 'hidden';
    d.body.appendChild(root);
    d.addEventListener('keydown', onKey, true);
    requestAnimationFrame(function () { root && root.classList.add('is-in'); });
    btn.focus({ preventScroll: true });
  }

  // mesaje din landing (bn.js): închidere, navigare spre magazin, coș actualizat
  window.addEventListener('message', function (ev) {
    if (!frame || ev.source !== frame.contentWindow || ev.origin !== location.origin) return;
    var m = ev.data;
    if (m === 'nmc:bn:close') close();
    if (m === 'nmc:bn:navigate') remember();
    if (m === 'nmc:bn:cart') remember();
  });

  window.NMCBlackNovember = { open: open, close: close, dismiss: remember };

  function init() {
    if (!force && seen()) return;
    setTimeout(open, Math.max(0, +script.dataset.delay || 400));
  }
  if (d.readyState === 'loading') d.addEventListener('DOMContentLoaded', init, { once: true });
  else init();
})();
