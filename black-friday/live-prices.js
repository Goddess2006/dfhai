(() => {
  'use strict';
  const config = JSON.parse(document.getElementById('nmc-products').textContent);
  const products = config.products;
  const refreshMs = 120000;
  const maxAgeMs = 180000;
  const money = new Intl.NumberFormat('ro-RO', { style: 'currency', currency: 'RON' });
  const prices = new Map();
  let running = false;
  let stopped = false;

  // Read only the main product's price group, never related-product prices.
  function parseAmount(text) {
    if (!text || !/\blei\b|\bRON\b/i.test(text)) return null;
    let value = text.replace(/\s|lei|RON/gi, '');
    if (value.includes(',') && value.includes('.')) {
      value = value.lastIndexOf(',') > value.lastIndexOf('.')
        ? value.replace(/\./g, '').replace(',', '.')
        : value.replace(/,/g, '');
    } else if (value.includes(',')) value = value.replace(',', '.');
    if (!/^\d+(?:\.\d{1,2})?$/.test(value)) return null;
    const number = Number(value);
    return Number.isFinite(number) && number > 0 ? number : null;
  }

  function readPrice(html) {
    const page = new DOMParser().parseFromString(html, 'text/html');
    const group = page.querySelector('#product-product .product-info .product-price-group');
    if (!group) throw new Error('Product price group missing');
    const price = parseAmount(group.querySelector('.product-price-new, .product-price')?.textContent);
    if (price === null) throw new Error('Invalid product price');
    const old = parseAmount(group.querySelector('.product-price-old')?.textContent);
    return { price, old: old !== null && old > price ? old : null, at: Date.now() };
  }

  function render() {
    let ready = 0;
    for (const product of products) {
      const item = prices.get(product.id);
      const fresh = item && Date.now() - item.at < maxAgeMs;
      if (fresh) ready++;
      document.querySelectorAll(`[data-live-price="${product.id}"]`).forEach(slot => {
        slot.replaceChildren();
        if (!fresh) {
          const label = document.createElement('span');
          label.className = 'price-unavailable';
          label.textContent = 'Vezi prețul în magazin';
          slot.append(label);
          return;
        }
        if (item.old) {
          const old = document.createElement('s');
          old.className = 'price-old';
          old.textContent = money.format(item.old);
          slot.append(old);
        }
        const price = document.createElement('div');
        price.className = 'price';
        price.textContent = money.format(item.price);
        slot.append(price);
      });
    }
    for (const category of ['ext', 'int', 'tapet', 'adeziv']) {
      const items = products.filter(product => product.cat === category).map(product => prices.get(product.id));
      const fresh = items.length && items.every(item => item && Date.now() - item.at < maxAgeMs);
      document.querySelectorAll(`[data-category-price="${category}"]`).forEach(slot => {
        slot.textContent = fresh ? 'de la ' + money.format(Math.min(...items.map(item => item.price))) : 'Descoperă colecția';
      });
    }
    const status = document.getElementById('priceStatus');
    status.textContent = ready === products.length
      ? 'Prețuri actualizate din magazin · TVA inclus'
      : ready ? 'Unele prețuri se confirmă în magazin · TVA inclus'
        : 'Consultă prețurile actuale în paginile produselor';
  }

  async function fetchPrice(product) {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 10000);
    try {
      // Same origin retains the shopper's session, tax and customer pricing.
      const path = new URL(product.url).pathname;
      const response = await fetch(path, {
        credentials: 'same-origin', cache: 'no-store', signal: controller.signal,
        headers: { Accept: 'text/html' }
      });
      if (!response.ok || !response.headers.get('content-type')?.includes('text/html')) throw new Error('Product unavailable');
      if (new URL(response.url, location.href).origin !== location.origin) throw new Error('Unexpected origin');
      prices.set(product.id, readPrice(await response.text()));
    } catch {
      // Never retain a previous price after an unsuccessful refresh.
      prices.delete(product.id);
    } finally {
      clearTimeout(timeout);
      if (!stopped) render();
    }
  }

  async function refresh() {
    if (running || stopped || document.hidden) return;
    running = true;
    const queue = [...products];
    try {
      await Promise.all(Array.from({ length: 3 }, async () => {
        while (queue.length && !stopped) await fetchPrice(queue.shift());
      }));
    } finally { running = false; }
  }
  render();
  refresh();
  setInterval(refresh, refreshMs);
  setInterval(render, 15000);
  document.addEventListener('visibilitychange', () => { if (!document.hidden) { render(); refresh(); } });
  window.addEventListener('pageshow', () => { render(); refresh(); });
  window.addEventListener('pagehide', () => { stopped = true; });
  window.addEventListener('pageshow', () => { stopped = false; refresh(); });
})();
