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
test('only ADRO-FIX exterior 1.5 kg carries a product discount', () => {
  const document = setup();
  const badges = document.querySelectorAll('.product__discount');
  assert.equal(badges.length, 1);
  assert.equal(badges[0].closest('[data-product-id]').dataset.productId, 'adeziv12');
  assert.match(badges[0].textContent, /−30%/);
  assert.ok([...document.querySelectorAll('.product:not([data-product-id="adeziv12"])')].every(p => !p.querySelector('.product__discount')));
  assert.equal(document.querySelectorAll('[data-product-id="adeziv13"] .product__discount').length, 0);
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
  assert.equal(visible.length, 1); assert.equal(visible[0].dataset.productId, 'int-z11');
  assert.equal(document.querySelector('.products').scrollLeft, 0);
  assert.match(document.getElementById('searchStatus').textContent, /1 produs/);
  input.value = ''; input.dispatchEvent(new Event('input'));
  assert.equal([...document.querySelectorAll('.product')].filter(p => !p.hidden).length, 32);
});
