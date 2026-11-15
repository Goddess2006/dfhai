/* Selecția Premium 2027 · Deco&Flair — df.js
   - countdown campanie (dispare automat după dată), căutare fără diacritice, navigare activă, animații la derulare;
   - pe decoflair.ro (același domeniu): stoc live din pagina produsului + „Adaugă în coș” (fără prețuri pe landing);
   - când rulează în iframe peste homepage (homepage-overlay.js): Escape închide, linkurile spre magazin deschid fereastra principală.
   Pagina rămâne complet funcțională fără acest script. */
(function () {
  'use strict';
  var d = document, root = d.documentElement;
  root.classList.add('js');

  /* ---------- afișare peste homepage (iframe pe același domeniu, vezi homepage-overlay.js) ---------- */
  var inOverlay = false;
  try { inOverlay = window.parent !== window && window.parent.location.origin === location.origin; } catch (e) { inOverlay = false; }
  var tell = function (m) { if (inOverlay) try { window.parent.postMessage(m, location.origin); } catch (e) {} };
  if (inOverlay) {
    root.classList.add('in-overlay');
    d.addEventListener('keydown', function (ev) { if (ev.key === 'Escape') tell('df:lp:close'); });
    // orice link spre magazin se deschide în fereastra principală; ancorele #secțiune rămân în landing
    d.addEventListener('click', function (ev) {
      var a = ev.target.closest && ev.target.closest('a[href]'); if (!a) return;
      var u = new URL(a.href, location.href);
      if (u.origin === location.origin && u.pathname === location.pathname && u.hash) return;
      if (!/^https?:$/.test(u.protocol)) return; // tel:, mailto:
      ev.preventDefault(); tell('df:lp:navigate');
      window.top.location.href = u.href;
    });
  }
  var $$ = function (s, r) { return Array.prototype.slice.call((r || d).querySelectorAll(s)); };
  var norm = function (t) { return (t || '').normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[șş]/g, 's').replace(/[țţ]/g, 't').toLowerCase(); };

  /* ---------- countdown ---------- */
  var cd = d.querySelector('[data-cd]');
  var end = cd ? Date.parse(cd.getAttribute('data-cd')) : 0;
  var pad = function (n) { return String(n).padStart(2, '0'); };
  function tick() {
    var ms = Math.max(0, end - Date.now());
    var D = Math.floor(ms / 864e5), H = Math.floor(ms / 36e5) % 24, M = Math.floor(ms / 6e4) % 60, S = Math.floor(ms / 1e3) % 60;
    if (cd) { cd.querySelector('[data-d]').textContent = pad(D); cd.querySelector('[data-h]').textContent = pad(H); cd.querySelector('[data-m]').textContent = pad(M); var sEl = cd.querySelector('[data-s]'); if (sEl) sEl.textContent = pad(S); }
    $$('[data-cd-mini]').forEach(function (el) { el.textContent = (D ? D + 'z ' : '') + pad(H) + ':' + pad(M) + ':' + pad(S); });
  }
  if (end && Date.now() > end) root.classList.add('camp-off');
  else if (end) { tick(); setInterval(tick, 1000); }

  /* ---------- filtre ---------- */
  $$('.filters').forEach(function (bar) {
    var grid = d.querySelector('[data-grid="' + bar.getAttribute('data-for') + '"]');
    bar.addEventListener('click', function (ev) {
      var b = ev.target.closest('.fchip'); if (!b) return;
      $$('.fchip', bar).forEach(function (x) { var on = x === b; x.classList.toggle('is-on', on); x.setAttribute('aria-pressed', on); });
      var f = b.getAttribute('data-filter');
      $$('.card', grid).forEach(function (c) { c.dataset.f = (f === '*' || c.getAttribute('data-sub') === f) ? '' : 'off'; apply(c); });
    });
  });
  // cercurile de categorie activează filtrul potrivit
  $$('.circ[data-jump]').forEach(function (a) {
    a.addEventListener('click', function () {
      var f = a.getAttribute('data-jump'); if (!f) return;
      var sec = d.querySelector(a.getAttribute('href'));
      var chip = sec && sec.querySelector('.fchip[data-filter="' + f + '"]');
      if (chip) chip.click();
    });
  });

  /* ---------- căutare ---------- */
  var q = d.getElementById('df-q'), status = d.getElementById('df-status'), terms = [];
  function apply(c) {
    var s = norm(c.getAttribute('data-search'));
    var okSearch = terms.every(function (t) { return s.indexOf(t) > -1; });
    c.hidden = c.dataset.f === 'off' || !okSearch;
  }
  if (q) q.addEventListener('input', function () {
    terms = norm(q.value).trim().split(/\s+/).filter(Boolean);
    $$('[data-search]').forEach(apply);
    $$('.sec').forEach(function (sec) {
      var g = sec.querySelector('.grid'), nr = sec.querySelector('.noresults');
      if (g && nr) nr.hidden = !!g.querySelector('.card:not([hidden])') || !terms.length;
    });
    var n = $$('.pc:not([hidden])').length;
    status.textContent = terms.length ? n + (n === 1 ? ' produs găsit' : ' produse găsite') + ' pentru „' + q.value.trim() + '”' : '';
    if (terms.length && n) { var first = d.querySelector('.pc:not([hidden])'); if (first && ev_scroll) first.scrollIntoView({ behavior: 'smooth', block: 'center' }); }
  });
  var ev_scroll = false;
  if (q) q.addEventListener('keydown', function (e) { ev_scroll = e.key === 'Enter'; if (ev_scroll) q.dispatchEvent(new Event('input')); ev_scroll = false; });

  /* ---------- nav activ + reveal ---------- */
  if ('IntersectionObserver' in window) {
    var links = $$('.nav a');
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) links.forEach(function (l) { l.classList.toggle('is-on', l.hash === '#' + e.target.id); }); });
    }, { rootMargin: '-40% 0px -55% 0px' });
    $$('main section[id]').forEach(function (s) { io.observe(s); });
    var rv = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); rv.unobserve(e.target); } }); }, { rootMargin: '0px 0px -8% 0px' });
    $$('.pc, .chapter__head, .pillar, .svc, .post, .manifesto').forEach(function (el) { el.classList.add('rv'); rv.observe(el); });
  }

  /* ---------- stoc live + „Adaugă în coș” (doar pe același domeniu cu magazinul) ----------
     Regulă de campanie: pe produse NU se afișează prețuri sau procente. */
  var LIVE = /(^|\.)decoflair\.ro$/.test(location.hostname);
  if (!LIVE) return;
  var cache = {};
  function info(url) {
    if (!cache[url]) cache[url] = fetch(url, { credentials: 'same-origin' }).then(function (r) { return r.ok ? r.text() : Promise.reject(r.status); }).then(function (html) {
      var doc = new DOMParser().parseFromString(html, 'text/html');
      var stockEl = doc.querySelector('.product-info .product-stock') || doc.querySelector('.product-stock');
      var pid = doc.querySelector('input[name="product_id"]');
      var hasOptions = !!doc.querySelector('#product [name^="option["]');
      return { inStock: stockEl ? stockEl.classList.contains('in-stock') : null, pid: pid ? pid.value : '', options: hasOptions };
    });
    return cache[url];
  }
  function render(el, x) {
    var st = el.querySelector('[data-stock]');
    if (st && x.inStock === false) { st.classList.add('is-out'); st.innerHTML = '<i></i>Disponibil la comandă'; }
    if (st && x.inStock === true) { st.classList.remove('is-out'); st.innerHTML = '<i></i>În stoc · livrare rapidă'; }
    var acts = el.querySelector('.card__actions');
    if (acts && x.pid && !x.options && x.inStock === true && !acts.querySelector('.btn--cart')) {
      var btn = d.createElement('button'); btn.type = 'button'; btn.className = 'btn btn--cart'; btn.textContent = 'Adaugă în coș';
      btn.addEventListener('click', function () { addToCart(x.pid, el.getAttribute('data-url'), btn); });
      acts.insertBefore(btn, acts.firstChild);
    }
  }
  var queue = $$('[data-url]'), running = 0;
  function next() {
    while (running < 4 && queue.length) {
      (function (el) {
        running++;
        info(el.getAttribute('data-url')).then(function (x) { render(el, x); }).catch(function () {}).then(function () { running--; next(); });
      })(queue.shift());
    }
  }
  next();

  var toast = d.getElementById('df-toast'), tT;
  function say(html) { toast.innerHTML = html; toast.classList.add('show'); clearTimeout(tT); tT = setTimeout(function () { toast.classList.remove('show'); }, 4000); }
  function addToCart(pid, url, btn) {
    btn.disabled = true; btn.textContent = 'Se adaugă…';
    var body = new URLSearchParams({ product_id: pid, quantity: '1' });
    fetch('index.php?route=checkout/cart/add', { method: 'POST', credentials: 'same-origin', headers: { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Requested-With': 'XMLHttpRequest' }, body: body })
      .then(function (r) { return r.json(); })
      .then(function (j) {
        if (j && j.success) {
          say('✓ Produs adăugat în coș <a href="/cos-cumparaturi" target="_top">Vezi coșul →</a>'); tell('df:lp:cart');
          var c = d.getElementById('df-cart'); if (c) { c.hidden = false; c.textContent = String((parseInt(c.textContent, 10) || 0) + 1); }
          btn.textContent = '✓ Adăugat';
        } else { location.href = url; } // produs cu opțiuni / minim de comandă: alegerea se face pe pagina produsului
      })
      .catch(function () { location.href = url; })
      .then(function () { setTimeout(function () { btn.disabled = false; btn.textContent = 'Adaugă în coș'; }, 1800); });
  }
})();
