/* Black November · NMC România
   - countdown, filtre pe subcategorii, căutare fără diacritice, navigare activă;
   - pe nmcromania.ro (același domeniu): preț + stoc live din pagina produsului și „Adaugă în coș”.
   Pagina rămâne complet funcțională fără acest script. */
(function () {
  'use strict';
  var d = document, root = d.documentElement;
  root.classList.add('js');
  var $$ = function (s, r) { return Array.prototype.slice.call((r || d).querySelectorAll(s)); };
  var norm = function (t) { return (t || '').normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[șş]/g, 's').replace(/[țţ]/g, 't').toLowerCase(); };

  /* ---------- countdown ---------- */
  var cd = d.querySelector('[data-cd]');
  var end = cd ? Date.parse(cd.getAttribute('data-cd')) : 0;
  var pad = function (n) { return String(n).padStart(2, '0'); };
  function tick() {
    var ms = Math.max(0, end - Date.now());
    var D = Math.floor(ms / 864e5), H = Math.floor(ms / 36e5) % 24, M = Math.floor(ms / 6e4) % 60, S = Math.floor(ms / 1e3) % 60;
    if (cd) { cd.querySelector('[data-d]').textContent = pad(D); cd.querySelector('[data-h]').textContent = pad(H); cd.querySelector('[data-m]').textContent = pad(M); cd.querySelector('[data-s]').textContent = pad(S); }
    $$('[data-cd-mini]').forEach(function (el) { el.textContent = (D ? D + 'z ' : '') + pad(H) + ':' + pad(M) + ':' + pad(S); });
  }
  if (end) { tick(); setInterval(tick, 1000); }

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
  var q = d.getElementById('bn-q'), status = d.getElementById('bn-status'), terms = [];
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
    var n = $$('.grid .card:not([hidden]), .wp:not([hidden])').length;
    status.textContent = terms.length ? n + (n === 1 ? ' produs găsit' : ' produse găsite') + ' pentru „' + q.value.trim() + '”' : '';
    if (terms.length && n) { var first = d.querySelector('.grid .card:not([hidden]), .wp:not([hidden])'); if (first && ev_scroll) first.scrollIntoView({ behavior: 'smooth', block: 'center' }); }
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
    $$('.card, .star, .banner, .post, .wp, .spot').forEach(function (el) { el.classList.add('rv'); rv.observe(el); });
  }

  /* ---------- preț + stoc live (doar pe același domeniu cu magazinul) ---------- */
  var LIVE = /(^|\.)nmcromania\.ro$/.test(location.hostname);
  if (!LIVE) return;
  var fmt = function (n) { return n.toLocaleString('ro-RO', { minimumFractionDigits: 2, maximumFractionDigits: 2 }); };
  var parseLei = function (t) { var m = (t || '').replace(/\s/g, '').match(/\d[\d.,]*/); if (!m) return 0; var v = m[0].replace(/[.,]$/, ''); var i = Math.max(v.lastIndexOf('.'), v.lastIndexOf(',')); if (i > -1 && v.length - i - 1 === 2) v = v.slice(0, i).replace(/[.,]/g, '') + '.' + v.slice(i + 1); else v = v.replace(/[.,]/g, ''); return parseFloat(v) || 0; };
  var cache = {};
  function info(url) {
    if (!cache[url]) cache[url] = fetch(url, { credentials: 'same-origin' }).then(function (r) { return r.ok ? r.text() : Promise.reject(r.status); }).then(function (html) {
      var doc = new DOMParser().parseFromString(html, 'text/html'), price = 0;
      $$('script[type="application/ld+json"]', doc).forEach(function (s) { try { var j = JSON.parse(s.textContent); if (j['@type'] === 'Product' && j.offers) price = parseFloat(j.offers.price) || 0; } catch (e) {} });
      var oldEl = doc.querySelector('.product-price-old'), newEl = doc.querySelector('.product-price-new');
      var stockEl = doc.querySelector('.product-stock'), pid = doc.querySelector('input[name="product_id"]');
      var hasOptions = !!doc.querySelector('#product .product-options .form-group, #product [name^="option["]');
      return { price: newEl ? parseLei(newEl.textContent) || price : price, old: oldEl ? parseLei(oldEl.textContent) : 0,
        inStock: stockEl ? stockEl.classList.contains('in-stock') : null, pid: pid ? pid.value : '', options: hasOptions };
    });
    return cache[url];
  }
  function render(el, x) {
    var box = el.querySelector('[data-price]');
    if (box && x.price > 0) {
      var p = x.price.toFixed(2).split('.');
      box.innerHTML = (x.old > x.price ? '<span class="price__old">' + fmt(x.old) + ' lei</span>' : '') +
        '<span class="price__now">' + Number(p[0]).toLocaleString('ro-RO') + '<sup>' + p[1] + '</sup><small>lei</small></span>';
      if (x.old > x.price) { var b = el.querySelector('.badge'); if (b) { b.textContent = '−' + Math.round((1 - x.price / x.old) * 100) + '%'; b.classList.add('is-pct'); } }
    } else if (box && x.price === 0) { box.innerHTML = '<span class="price__ph">Preț la cerere</span>'; }
    var st = el.querySelector('[data-stock]');
    if (st && x.inStock === false) { st.classList.add('is-out'); st.innerHTML = '<i></i>Disponibil la comandă'; }
    var acts = el.querySelector('.card__actions');
    if (acts && x.pid && !x.options && x.inStock !== false && !acts.querySelector('.btn--cart')) {
      var btn = d.createElement('button'); btn.type = 'button'; btn.className = 'btn btn--cart'; btn.textContent = 'Adaugă în coș';
      btn.addEventListener('click', function () { addToCart(x.pid, el.getAttribute('data-url'), btn); });
      acts.insertBefore(btn, acts.firstChild);
      var cta = acts.querySelector('[data-cta]'); if (cta) { cta.innerHTML = 'Vezi detalii'; cta.classList.add('btn--ghostdark'); }
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

  var toast = d.getElementById('bn-toast'), tT;
  function say(html) { toast.innerHTML = html; toast.classList.add('show'); clearTimeout(tT); tT = setTimeout(function () { toast.classList.remove('show'); }, 4000); }
  function addToCart(pid, url, btn) {
    btn.disabled = true; btn.textContent = 'Se adaugă…';
    var body = new URLSearchParams({ product_id: pid, quantity: '1' });
    fetch('index.php?route=checkout/cart/add', { method: 'POST', credentials: 'same-origin', headers: { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Requested-With': 'XMLHttpRequest' }, body: body })
      .then(function (r) { return r.json(); })
      .then(function (j) {
        if (j && j.success) {
          say('✓ Produs adăugat în coș <a href="/cos-cumparaturi">Vezi coșul →</a>');
          var c = d.getElementById('bn-cart'); if (c) { c.hidden = false; c.textContent = String((parseInt(c.textContent, 10) || 0) + 1); }
          btn.textContent = '✓ Adăugat';
        } else { location.href = url; } // produs cu opțiuni / minim de comandă: alegerea se face pe pagina produsului
      })
      .catch(function () { location.href = url; })
      .then(function () { setTimeout(function () { btn.disabled = false; btn.textContent = 'Adaugă în coș'; }, 1800); });
  }
})();
