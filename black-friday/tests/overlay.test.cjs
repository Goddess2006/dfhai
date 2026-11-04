const { test } = require('node:test');
const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
const path = require('node:path');
const { parseHTML } = require('linkedom');
const script = fs.readFileSync(path.join(__dirname, '../homepage-overlay.js'), 'utf8');
function setup(url = 'https://www.nmcromania.ro/', storage = new Map(), enabled = true) {
  const { document } = parseHTML('<html><body><button id="previous">Original homepage</button></body></html>');
  document.documentElement.style.overflow = 'auto';
  const previous = document.getElementById('previous');
  let focused = false; previous.focus = () => { focused = true; };
  Object.defineProperty(document, 'activeElement', { value: previous });
  Object.defineProperty(document, 'readyState', { value: 'complete' });
  Object.defineProperty(document, 'currentScript', { value: { src: 'https://www.nmcromania.ro/black-friday/homepage-overlay.js', dataset: { enabled: String(enabled) } } });
  const create = document.createElement.bind(document);
  document.createElement = tag => {
    const el = create(tag); el.focus = () => {};
    if (tag === 'dialog') { el.showModal = () => { el.open = true; }; el.close = () => { el.open = false; }; }
    return el;
  };
  const handlers = {};
  const window = { HTMLDialogElement: function () {}, addEventListener: (name, callback) => { handlers[name] = callback; } };
  window.top = window;
  vm.runInNewContext(script, { document, window, location: new URL(url), URL, URLSearchParams,
    sessionStorage: { getItem: key => storage.get(key), setItem: (key, value) => storage.set(key, value) } });
  return { document, window, handlers, storage, focusRestored: () => focused };
}

test('home overlay closes, restores scroll/focus and stays closed for the session', () => {
  const app = setup();
  assert.ok(app.document.querySelector('dialog').open);
  assert.equal(app.document.documentElement.style.overflow, 'hidden');
  assert.match(app.document.querySelector('iframe').src, /black-friday\/index.html\?overlay=1/);
  app.document.querySelector('dialog button').click();
  assert.equal(app.document.querySelector('dialog'), null);
  assert.equal(app.document.documentElement.style.overflow, 'auto');
  assert.equal(app.focusRestored(), true);
  assert.equal(setup(undefined, app.storage).document.querySelector('dialog'), null);
  app.window.NMCBlackFriday.open();
  assert.ok(app.document.querySelector('dialog'));
});

test('product pages, non-home OpenCart routes and disabled campaigns remain untouched', () => {
  for (const url of ['https://www.nmcromania.ro/product', 'https://www.nmcromania.ro/index.php?route=checkout/cart', 'https://www.nmcromania.ro/?route=product/product']) {
    assert.equal(setup(url).document.querySelector('dialog'), null);
  }
  assert.equal(setup(undefined, undefined, false).document.querySelector('dialog'), null);
  assert.ok(setup('https://www.nmcromania.ro/index.php?route=common/home').document.querySelector('dialog'));
});

test('messages from an unrelated window cannot close the overlay', () => {
  const app = setup();
  app.handlers.message({ source: {}, origin: 'https://example.org', data: 'nmc:bf:close' });
  assert.ok(app.document.querySelector('dialog'));
});

test('Escape cancellation restores the homepage and dismisses the campaign', () => {
  const app = setup();
  const dialog = app.document.querySelector('dialog');
  const event = new (require('linkedom').Event)('cancel', { cancelable: true });
  dialog.dispatchEvent(event);
  assert.equal(event.defaultPrevented, true);
  assert.equal(app.document.querySelector('dialog'), null);
  assert.equal(app.document.documentElement.style.overflow, 'auto');
});
