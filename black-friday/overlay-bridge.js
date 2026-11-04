(() => {
  'use strict';
  if (window.parent === window) return;
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape') window.parent.postMessage('nmc:bf:close', location.origin);
  });
  document.querySelectorAll('a[href]').forEach(link => {
    const url = new URL(link.href);
    if (!['https:', 'http:'].includes(url.protocol) || (url.origin === location.origin && url.pathname === location.pathname && url.hash)) return;
    link.target = '_top';
    link.addEventListener('click', () => {
      // Persist dismissal synchronously before a top-level navigation unloads the frame.
      window.parent.NMCBlackFriday?.dismiss();
    });
  });
})();
