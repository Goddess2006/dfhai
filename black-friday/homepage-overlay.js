(() => {
  'use strict';
  const script = document.currentScript;
  if (script?.dataset.enabled === 'false' || window.top !== window || window.NMCBlackFriday) return;
  const home = location.pathname === '/' || location.pathname === '/index.php';
  const route = new URLSearchParams(location.search).get('route');
  if (!home || (route && route !== 'common/home')) return;
  const campaign = script?.dataset.campaign || 'black-friday-2026';
  const storageKey = 'nmc:closed:' + campaign;
  const source = new URL(script?.dataset.variant === '2' ? './varianta-2/index.html?overlay=1' : './index.html?overlay=1', script.src);
  if (source.origin !== location.origin) return;
  let dialog, frame, previousFocus, previousOverflow;
  const wasClosed = () => { try { return sessionStorage.getItem(storageKey) === '1'; } catch { return false; } };
  const remember = () => { try { sessionStorage.setItem(storageKey, '1'); } catch { /* Session storage may be blocked. */ } };
  function close() {
    remember();
    if (dialog?.open) dialog.close();
    if (dialog) document.documentElement.style.overflow = previousOverflow;
    dialog?.remove(); dialog = null; frame = null;
    previousFocus?.focus?.();
  }
  function open() {
    if (dialog || !('HTMLDialogElement' in window)) return;
    previousFocus = document.activeElement;
    dialog = document.createElement('dialog');
    dialog.setAttribute('aria-label', 'Black Friday NMC România');
    dialog.style.cssText = 'position:fixed;inset:0;margin:0;border:0;padding:0;width:100vw;max-width:none;height:100dvh;max-height:none;background:#09090a;color:white;overflow:hidden;z-index:2147483647;';
    const shell = document.createElement('div');
    shell.style.cssText = 'display:flex;flex-direction:column;height:100%;';
    const bar = document.createElement('div');
    bar.style.cssText = 'display:flex;justify-content:space-between;align-items:center;gap:12px;padding:10px 16px;padding-top:max(10px,env(safe-area-inset-top));background:#141417;font:600 14px system-ui;flex-shrink:0;border-bottom:1px solid #333;';
    const label = document.createElement('span');
    label.textContent = 'NMC România · Black Friday';
    const button = document.createElement('button');
    button.type = 'button';
    button.textContent = 'Continuă în magazin ×';
    button.setAttribute('aria-label', 'Închide Black Friday și revino la magazin');
    button.style.cssText = 'border:1px solid #555;border-radius:24px;padding:10px 14px;color:white;background:#232328;cursor:pointer;font:inherit;';
    button.addEventListener('click', close);
    frame = document.createElement('iframe');
    frame.src = source.href;
    frame.title = 'Colecțiile Black Friday NMC România';
    frame.style.cssText = 'display:block;border:0;width:100%;flex:1;min-height:0;background:#09090a;';
    bar.append(label, button); shell.append(bar, frame); dialog.append(shell);
    dialog.addEventListener('cancel', event => { event.preventDefault(); close(); });
    previousOverflow = document.documentElement.style.overflow;
    document.documentElement.style.overflow = 'hidden';
    document.body.append(dialog);
    try { dialog.showModal(); button.focus(); } catch { document.documentElement.style.overflow = previousOverflow; dialog.remove(); dialog = null; frame = null; }
  }
  window.addEventListener('message', event => {
    if (!frame || event.source !== frame.contentWindow || event.origin !== location.origin) return;
    if (event.data === 'nmc:bf:close') close();
    if (event.data === 'nmc:bf:navigate') remember();
  });
  window.NMCBlackFriday = { open, close, dismiss: remember };
  const init = () => { if (!wasClosed()) open(); };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, { once: true });
  else init();
})();
