'use strict';
(() => {
  const menuButton = document.querySelector('.menu-toggle');
  const mobileNav = document.querySelector('#mobile-nav');
  function closeMenu() { if (!mobileNav || !menuButton) return; mobileNav.hidden = true; menuButton.setAttribute('aria-expanded', 'false'); menuButton.setAttribute('aria-label', 'Открыть меню'); }
  menuButton?.addEventListener('click', () => {
    const expanded = menuButton.getAttribute('aria-expanded') === 'true';
    mobileNav.hidden = expanded;
    menuButton.setAttribute('aria-expanded', String(!expanded));
    menuButton.setAttribute('aria-label', expanded ? 'Открыть меню' : 'Закрыть меню');
  });
  mobileNav?.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
  document.addEventListener('keydown', event => { if (event.key === 'Escape') closeMenu(); });
  window.matchMedia('(min-width: 851px)').addEventListener('change', event => { if (event.matches) closeMenu(); });

  const track = document.querySelector('#gallery');
  if (track) {
    const cards = [...track.querySelectorAll('.work-card')];
    const prev = document.querySelector('#gallery-prev');
    const next = document.querySelector('#gallery-next');
    const counter = document.querySelector('#gallery-count');
    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
    let activeCards = [...cards];
    let current = 0;
    let frame = 0;
    function update() {
      const left = track.getBoundingClientRect().left;
      let nearest = Infinity;
      activeCards.forEach((card, index) => { const distance = Math.abs(card.getBoundingClientRect().left - left); if (distance < nearest) { nearest = distance; current = index; } });
      track.style.height = `${activeCards[current].offsetHeight}px`;
      counter.textContent = `${String(current + 1).padStart(2, '0')} / ${String(activeCards.length).padStart(2, '0')}`;
      prev.disabled = current === 0;
      next.disabled = current === activeCards.length - 1;
    }
    function go(index) {
      const card = activeCards[Math.max(0, Math.min(index, activeCards.length - 1))];
      const delta = card.getBoundingClientRect().left - track.getBoundingClientRect().left;
      track.scrollTo({ left: track.scrollLeft + delta, behavior: reduced.matches ? 'instant' : 'smooth' });
    }
    prev.addEventListener('click', () => go(current - 1));
    next.addEventListener('click', () => go(current + 1));
    track.addEventListener('scroll', () => { cancelAnimationFrame(frame); frame = requestAnimationFrame(update); }, { passive: true });
    track.addEventListener('keydown', event => { if (event.target !== track) return; if (event.key === 'ArrowRight') { event.preventDefault(); go(current + 1); } if (event.key === 'ArrowLeft') { event.preventDefault(); go(current - 1); } if (event.key === 'Home') { event.preventDefault(); go(0); } if (event.key === 'End') { event.preventDefault(); go(activeCards.length - 1); } });
    document.querySelectorAll('[data-filter]').forEach(button => button.addEventListener('click', () => {
      document.querySelectorAll('[data-filter]').forEach(other => other.setAttribute('aria-pressed', String(other === button)));
      cards.forEach(card => { card.hidden = button.dataset.filter !== 'all' && card.dataset.category !== button.dataset.filter; });
      activeCards = cards.filter(card => !card.hidden);
      current = 0;
      track.scrollTo({ left: 0, behavior: 'instant' });
      update();
    }));
    window.addEventListener('resize', update);
    update();
  }
  const dialog = document.querySelector('#image-dialog');
  if (dialog) {
    const picture = document.querySelector('#dialog-image');
    const caption = document.querySelector('#dialog-caption');
    let previousFocus;
    function openImage(source) {
      previousFocus = source;
      picture.src = source.src;
      picture.alt = source.alt;
      caption.textContent = source.alt;
      if (typeof dialog.showModal === 'function') { dialog.showModal(); document.body.style.overflow = 'hidden'; }
      else window.open(source.src, '_blank', 'noopener');
    }
    document.querySelectorAll('[data-zoom]').forEach(img => {
      img.addEventListener('click', () => openImage(img));
      img.addEventListener('keydown', event => { if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); openImage(img); } });
    });
    dialog.querySelector('.dialog-close').addEventListener('click', () => dialog.close());
    dialog.addEventListener('click', event => { const rect = dialog.getBoundingClientRect(); if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close(); });
    dialog.addEventListener('close', () => { document.body.style.overflow = ''; previousFocus?.focus({ preventScroll: true }); });
  }
  const form = document.querySelector('#request-form');
  if (form) {
    const result = document.querySelector('#request-result');
    const preview = document.querySelector('#request-preview');
    const copyButton = document.querySelector('#copy-request');
    const status = document.querySelector('#copy-status');
    const location = form.elements.location;
    location.addEventListener('input', () => location.setCustomValidity(''));
    function hideStaleResult() { result.hidden = true; copyButton.textContent = 'Скопировать текст'; }
    form.addEventListener('input', hideStaleResult);
    form.addEventListener('change', hideStaleResult);
    form.addEventListener('submit', event => {
      event.preventDefault();
      location.setCustomValidity(location.value.trim() ? '' : 'Укажите город или населённый пункт');
      if (!form.reportValidity()) return;
      const lines = ['Здравствуйте! Хочу узнать стоимость.', `Услуга: ${form.elements.service.value}.`, `Место: ${location.value.trim()}.`];
      const detail = form.elements.details.value.trim();
      if (detail) lines.push(`Детали: ${detail}`);
      lines.push('Подскажите стоимость и ближайшее удобное время.');
      preview.textContent = lines.join('\n');
      result.hidden = false;
      status.textContent = 'Скопируйте текст, откройте Viber и вставьте сообщение в чат. Затем приложите фотографии.';
      copyButton.focus({ preventScroll: true });
      result.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
      document.dispatchEvent(new CustomEvent('vitcleaner:conversion', { detail: { action: 'request_prepared' } }));
    });
    copyButton.addEventListener('click', async () => {
      try {
        if (!navigator.clipboard?.writeText) throw new Error('Clipboard unavailable');
        await navigator.clipboard.writeText(preview.textContent);
        copyButton.textContent = 'Текст скопирован';
        status.textContent = 'Теперь откройте Viber, вставьте сообщение и отправьте его вместе с фотографиями.';
      } catch {
        const range = document.createRange(); range.selectNodeContents(preview);
        const selection = window.getSelection(); selection.removeAllRanges(); selection.addRange(range);
        status.textContent = 'Текст выделен. Скопируйте его вручную через меню устройства, затем вставьте в Viber.';
      }
    });
  }
  document.querySelectorAll('a[href^="tel:"], a[href*="viber.click"]').forEach(link => link.addEventListener('click', () => document.dispatchEvent(new CustomEvent('vitcleaner:conversion', { detail: { action: link.href.startsWith('tel:') ? 'phone_click' : 'viber_click' } }))));
  if ('IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const observer = new IntersectionObserver(entries => entries.forEach(entry => { if (entry.isIntersecting) { entry.target.classList.add('in-view'); observer.unobserve(entry.target); } }), { threshold: 0.12 });
    document.querySelectorAll('.section-head, .process-copy, .price-panel').forEach(element => observer.observe(element));
  }
})();
