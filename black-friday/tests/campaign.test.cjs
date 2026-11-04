const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const { parseHTML, Event } = require('linkedom');
const root = path.join(__dirname, '..');
function setup() {
  const { document } = parseHTML(fs.readFileSync(path.join(root, 'index.html'), 'utf8'));
  document.querySelectorAll('.products').forEach(shelf => {
    Object.defineProperty(shelf, 'clientWidth', { value: 1000 });
    Object.defineProperty(shelf, 'scrollWidth', { value: 3000 });
    shelf.scrollLeft = 0;
    shelf.scrollBy = ({ left }) => {
      shelf.scrollLeft = Math.max(0, Math.min(2000, shelf.scrollLeft + left));
      shelf.dispatchEvent(new Event('scroll'));
    };
  });
  const window = { addEventListener: () => {}, matchMedia: () => ({ matches: true }) };
  vm.runInNewContext(fs.readFileSync(path.join(root, 'campaign.js'), 'utf8'), { document, window });
  return document;
}
test('campaign discounts respect category, model and adhesive exceptions', () => {
  const document = setup();
  const badge = id => document.querySelector(`[data-product-id="${id}"] .product__discount`);
  assert.equal(document.querySelectorAll('.product__discount').length, 34);
  for (const id of ['ext0', 'ext1', 'ext2', 'ext3']) assert.match(badge(id).textContent, /−20%/);
  for (const model of ['z21', 'z11', 'wo2', 'wt25', 'fd3', 'fo1', 'l2', 'l5']) assert.match(badge('int-' + model).textContent, /până la −40%/);
  document.querySelectorAll('#tapet .product').forEach(product => {
    assert.match(product.querySelector('h3').textContent, /Carrara Best/);
    assert.match(product.querySelector('.product__discount').textContent, /−30%/);
    assert.match(product.querySelector('.product__note').textContent, /stocului/);
  });
  assert.match(badge('adeziv12').textContent, /−30%/);
  assert.equal(badge('adeziv13'), null);
  assert.match(document.querySelector('[data-product-id="adeziv13"] .product__note').textContent, /preț întreg/);
});
test('gallery arrows move the shelf and disable at both boundaries', () => {
  const document = setup(); const section = document.querySelector('.collection');
  const previous = section.querySelector('[data-carousel="-1"]');
  const next = section.querySelector('[data-carousel="1"]');
  assert.equal(previous.disabled, true); assert.equal(next.disabled, false);
  next.click(); assert.equal(section.querySelector('.products').scrollLeft, 1000);
  assert.equal(previous.disabled, false); next.click(); assert.equal(next.disabled, true);
  previous.click(); previous.click(); assert.equal(previous.disabled, true);
});
test('search filters all shelves and resets their scroll position', () => {
  const document = setup(); const input = document.getElementById('q');
  document.querySelector('.products').scrollLeft = 1000;
  input.value = 'Z11'; input.dispatchEvent(new Event('input'));
  const visible = [...document.querySelectorAll('.product')].filter(p => !p.hidden);
  assert.equal(visible.length, 2); assert.ok(visible.every(product => product.dataset.productId === 'int-z11'));
  assert.equal(document.querySelector('.products').scrollLeft, 0);
  assert.match(document.getElementById('searchStatus').textContent, /1 produs/);
  input.value = ''; input.dispatchEvent(new Event('input'));
  assert.equal([...document.querySelectorAll('.product')].filter(p => !p.hidden).length, 35);
});

test('exterior, interior and wallpaper lead the campaign; adhesives are the final product section', () => {
  const document = setup();
  const featured = [...document.querySelectorAll('#vedete [data-product-id]')].map(p => p.dataset.productId);
  assert.deepEqual(featured, ['ext0', 'int-z11', 'tapet-82671']);
  assert.equal(document.querySelector('#oferta [href*="adeziv"]'), null);
  assert.equal([...document.querySelectorAll('.collection')].at(-1).id, 'adeziv');
  assert.equal(document.querySelectorAll('.ambience-card img').length, 3);
  assert.match(document.querySelector('#exterior .collection__head').textContent, /Adezivii sunt excluși/);
  const catalog = JSON.parse(fs.readFileSync(path.join(root, 'catalog.json'), 'utf8'));
  assert.ok(catalog.products.every(product => product.inStock === true));
  assert.equal(catalog.products.filter(product => product.cat === 'int').length, 8);
  assert.equal(catalog.products.filter(product => product.cat === 'tapet').length, 18);
});
