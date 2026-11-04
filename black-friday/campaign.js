(() => {
  'use strict';
  const normalize = text => text.normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[șş]/g, 's').replace(/[țţ]/g, 't').toLowerCase();
  function updateControls(section) {
    const shelf = section.querySelector('.products');
    section.querySelector('[data-carousel="-1"]').disabled = shelf.scrollLeft <= 1;
    section.querySelector('[data-carousel="1"]').disabled = shelf.scrollLeft >= shelf.scrollWidth - shelf.clientWidth - 1;
  }
  document.querySelectorAll('.collection').forEach(section => {
    const shelf = section.querySelector('.products');
    section.querySelectorAll('[data-carousel]').forEach(button => button.addEventListener('click', () => {
      shelf.scrollBy({ left: Number(button.dataset.carousel) * shelf.clientWidth,
        behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth' });
    }));
    shelf.addEventListener('scroll', () => updateControls(section), { passive: true });
    updateControls(section);
  });
  window.addEventListener('resize', () => document.querySelectorAll('.collection').forEach(updateControls));
  document.getElementById('q').addEventListener('input', event => {
    const terms = normalize(event.target.value).trim().split(/\s+/).filter(Boolean);
    document.querySelectorAll('[data-search]').forEach(card => {
      card.hidden = !terms.every(term => normalize(card.dataset.search).includes(term));
    });
    document.querySelectorAll('.collection').forEach(section => {
      section.querySelector('.empty').hidden = !!section.querySelector('.product:not([hidden])');
      section.querySelector('.products').scrollLeft = 0;
      updateControls(section);
    });
    document.getElementById('searchStatus').textContent = terms.length ? `${document.querySelectorAll('.product:not([hidden])').length} ${document.querySelectorAll('.product:not([hidden])').length === 1 ? 'produs găsit' : 'produse găsite'}` : '';
  });
  if ('IntersectionObserver' in window) {
    const chips = [...document.querySelectorAll('.chip')];
    const observer = new IntersectionObserver(entries => entries.forEach(entry => {
      if (entry.isIntersecting) chips.forEach(chip => chip.classList.toggle('is-active', chip.hash === '#' + entry.target.id));
    }), { rootMargin: '-20% 0px -60% 0px' });
    document.querySelectorAll('.collection').forEach(section => observer.observe(section));
  }
})();
