(() => {
  'use strict';
  const normalize = text => text.normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[șş]/g, 's').replace(/[țţ]/g, 't').toLowerCase();
  document.getElementById('q').addEventListener('input', event => {
    const terms = normalize(event.target.value).trim().split(/\s+/).filter(Boolean);
    document.querySelectorAll('[data-search]').forEach(card => {
      card.hidden = !terms.every(term => normalize(card.dataset.search).includes(term));
    });
    document.querySelectorAll('.collection').forEach(section => {
      section.querySelector('.empty').hidden = !!section.querySelector('.product:not([hidden])');
    });
    document.getElementById('searchStatus').textContent = terms.length ? `${document.querySelectorAll('.product:not([hidden])').length} produse găsite` : '';
  });
  if ('IntersectionObserver' in window) {
    const chips = [...document.querySelectorAll('.chip')];
    const observer = new IntersectionObserver(entries => entries.forEach(entry => {
      if (entry.isIntersecting) chips.forEach(chip => chip.classList.toggle('is-active', chip.hash === '#' + entry.target.id));
    }), { rootMargin: '-20% 0px -60% 0px' });
    document.querySelectorAll('.collection').forEach(section => observer.observe(section));
  }
})();
