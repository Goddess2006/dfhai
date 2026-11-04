const { test } = require('node:test');
const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
const path = require('node:path');
const { parseHTML, Event } = require('linkedom');

test('embedded category links remain internal; product links navigate the main window and remember dismissal', () => {
  const { document } = parseHTML('<html><body><a id="cat" href="https://www.nmcromania.ro/black-friday/index.html?overlay=1#tapet">Tapet</a><a id="product" href="https://www.nmcromania.ro/a">Product</a></body></html>');
  let dismissed = false;
  const messages = [];
  const parent = { postMessage: (...args) => messages.push(args), NMCBlackFriday: { dismiss: () => { dismissed = true; } } };
  const window = { parent };
  vm.runInNewContext(fs.readFileSync(path.join(__dirname, '../overlay-bridge.js'), 'utf8'), {
    window, document, URL, location: new URL('https://www.nmcromania.ro/black-friday/index.html?overlay=1')
  });
  assert.notEqual(document.getElementById('cat').target, '_top');
  assert.equal(document.getElementById('product').target, '_top');
  document.getElementById('product').click();
  assert.equal(dismissed, true);
  const event = new Event('keydown'); event.key = 'Escape'; document.dispatchEvent(event);
  assert.equal(messages[0][0], 'nmc:bf:close');
  assert.equal(messages[0][1], 'https://www.nmcromania.ro');
});
