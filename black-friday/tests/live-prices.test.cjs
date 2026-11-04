const { test } = require('node:test');
const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
const path = require('node:path');
const { parseHTML, DOMParser } = require('linkedom');
const script = fs.readFileSync(path.join(__dirname, '../live-prices.js'), 'utf8');
const html = (price, old = '') => `<div id="product-product"><div class="product-info"><div class="product-price-group"><div class="${old ? 'product-price-new' : 'product-price'}">${price} lei</div>${old ? `<div class="product-price-old">${old} lei</div>` : ''}</div></div><div class="related"><div class="product-price">1 lei</div></div></div>`;
const settle = async () => { for (let i = 0; i < 12; i++) await new Promise(resolve => setImmediate(resolve)); };
function setup() {
  const { document } = parseHTML(`<html><body>
    <script id="nmc-products" type="application/json">{"products":[{"id":"a","cat":"ext","url":"https://www.nmcromania.ro/a"},{"id":"b","cat":"ext","url":"https://www.nmcromania.ro/b"}]}</script>
    <div data-live-price="a"></div><div data-live-price="a"></div><div data-live-price="b"></div>
    <div data-category-price="ext"></div><p id="priceStatus"></p></body></html>`);
  const intervals = new Map();
  const events = new Map();
  const responses = { '/a': html('100.00', '150.00'), '/b': html('250.00') };
  let now = 1000;
  class Clock extends Date { static now() { return now; } }
  const requests = [];
  const context = { document, DOMParser, URL, Date: Clock, Intl, Map, AbortController,
    location: new URL('https://www.nmcromania.ro/black-friday/'),
    window: { addEventListener: (event, handler) => { events.set(event, handler); } },
    setTimeout, clearTimeout, setInterval: (fn, ms) => intervals.set(ms, fn),
    fetch: async (url, options) => {
      requests.push({ url, options });
      if (responses[url] instanceof Error) throw responses[url];
      return { ok: true, url: 'https://www.nmcromania.ro' + url, headers: new Headers({ 'content-type': 'text/html' }), text: async () => responses[url] };
    }
  };
  vm.runInNewContext(script, context);
  return { document, responses, intervals, requests, setNow: value => { now = value; } };
}

test('prices refresh across duplicate cards; expired promotion and old price disappear', async () => {
  const app = setup(); await settle();
  assert.equal(app.document.querySelectorAll('[data-live-price="a"] .price').length, 2);
  assert.equal(app.document.querySelector('[data-live-price="a"] .price-old').textContent.replace(/\s/g, ''), '150,00RON');
  assert.match(app.document.querySelector('[data-category-price]').textContent, /100,00/);
  app.responses['/a'] = html('80.00');
  await app.intervals.get(120000)();
  assert.ok([...app.document.querySelectorAll('[data-live-price="a"] .price')].every(node => node.textContent.includes('80,00')));
  assert.equal(app.document.querySelector('[data-live-price="a"] .price-old'), null);
  assert.ok(app.requests.every(request => request.options.credentials === 'same-origin' && request.options.cache === 'no-store'));
});

test('network failure hides old prices and incomplete category minima', async () => {
  const app = setup(); await settle();
  app.responses['/a'] = new Error('offline');
  await app.intervals.get(120000)();
  assert.equal(app.document.querySelector('[data-live-price="a"] .price'), null);
  assert.match(app.document.querySelector('[data-live-price="a"]').textContent, /Vezi prețul/);
  assert.equal(app.document.querySelector('[data-category-price]').textContent, 'Descoperă colecția');
  assert.ok(app.document.querySelector('[data-live-price="b"] .price'));
});

test('malformed, unrelated-product and non-RON prices cannot replace a main product price', async () => {
  const app = setup(); await settle();
  app.responses['/a'] = '<div class="related"><div class="product-price">1 lei</div></div>';
  app.responses['/b'] = html('NaN');
  await app.intervals.get(120000)();
  assert.equal(app.document.querySelector('.price'), null);
  app.responses['/a'] = html('100').replace('lei', 'EUR');
  await app.intervals.get(120000)();
  assert.equal(app.document.querySelector('.price'), null);
});

test('prices expire without another successful network response', async () => {
  const app = setup(); await settle();
  app.setNow(181001); app.intervals.get(15000)();
  assert.equal(app.document.querySelector('.price'), null);
});

test('Romanian decimal and thousands separators are preserved', async () => {
  const app = setup(); await settle();
  app.responses['/a'] = html('1.234,56');
  await app.intervals.get(120000)();
  assert.match(app.document.querySelector('[data-live-price="a"] .price').textContent, /1\.234,56/);
});


test('store format with comma thousands and decimal point is supported', async () => {
  const app = setup(); await settle();
  app.responses['/a'] = html('1,064.80');
  await app.intervals.get(120000)();
  assert.match(app.document.querySelector('[data-live-price="a"] .price').textContent, /1\.064,80/);
});
