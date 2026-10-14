'use strict';

(() => {
  const menuButton = document.querySelector('.menu-toggle');
  const mobileNav = document.querySelector('#mobile-nav');

  const closeMenu = () => {
    if (!mobileNav || !menuButton) return;
    mobileNav.hidden = true;
    menuButton.setAttribute('aria-expanded', 'false');
    menuButton.setAttribute('aria-label', 'Открыть меню');
  };

  menuButton?.addEventListener('click', () => {
    const isOpen = menuButton.getAttribute('aria-expanded') === 'true';
    mobileNav.hidden = isOpen;
    menuButton.setAttribute('aria-expanded', String(!isOpen));
    menuButton.setAttribute('aria-label', isOpen ? 'Открыть меню' : 'Закрыть меню');
  });
  mobileNav?.querySelectorAll('a').forEach((link) => link.addEventListener('click', closeMenu));
  document.addEventListener('keydown', (event) => { if (event.key === 'Escape') closeMenu(); });
  window.matchMedia('(min-width: 851px)').addEventListener('change', (event) => { if (event.matches) closeMenu(); });

  const dialog = document.querySelector('#image-dialog');
  if (dialog) {
    const image = dialog.querySelector('#dialog-image');
    const caption = dialog.querySelector('#dialog-caption');
    const closeButton = dialog.querySelector('.dialog-close');
    let previousFocus;

    document.querySelectorAll('[data-zoom]').forEach((button) => {
      button.addEventListener('click', () => {
        previousFocus = button;
        image.src = button.dataset.zoom;
        image.alt = button.dataset.alt;
        caption.textContent = button.dataset.alt;
        if (typeof dialog.showModal === 'function') {
          dialog.showModal();
          document.body.style.overflow = 'hidden';
        } else {
          window.open(button.dataset.zoom, '_blank', 'noopener');
        }
      });
    });
    closeButton.addEventListener('click', () => dialog.close());
    dialog.addEventListener('click', (event) => {
      const bounds = dialog.getBoundingClientRect();
      const outside = event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom;
      if (outside) dialog.close();
    });
    dialog.addEventListener('close', () => {
      document.body.style.overflow = '';
      image.removeAttribute('src');
      previousFocus?.focus({ preventScroll: true });
    });
  }

  const form = document.querySelector('#request-form');
  if (form) {
    const result = document.querySelector('#request-result');
    const preview = document.querySelector('#request-preview');
    const copyButton = document.querySelector('#copy-request');
    const status = document.querySelector('#copy-status');
    const location = form.elements.location;

    const hideStaleResult = () => {
      result.hidden = true;
      copyButton.textContent = 'Скопировать текст';
    };
    form.addEventListener('input', hideStaleResult);
    form.addEventListener('change', hideStaleResult);
    location.addEventListener('input', () => location.setCustomValidity(''));

    form.addEventListener('submit', (event) => {
      event.preventDefault();
      location.setCustomValidity(location.value.trim() ? '' : 'Укажите город или населённый пункт');
      if (!form.reportValidity()) return;
      const lines = [
        'Здравствуйте! Хочу узнать стоимость.',
        `Услуга: ${form.elements.service.value}.`,
        `Место: ${location.value.trim()}.`,
      ];
      const details = form.elements.details.value.trim();
      if (details) lines.push(`Детали: ${details}`);
      lines.push('Подскажите стоимость и ближайшее удобное время. Фото приложу к сообщению.');
      preview.textContent = lines.join('\n');
      result.hidden = false;
      status.textContent = 'Скопируйте текст, откройте Viber и приложите фотографии.';
      copyButton.focus({ preventScroll: true });
      result.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
      document.dispatchEvent(new CustomEvent('vitcleaner:conversion', { detail: { action: 'request_prepared' } }));
    });

    copyButton.addEventListener('click', async () => {
      try {
        if (!navigator.clipboard?.writeText) throw new Error('Clipboard unavailable');
        await navigator.clipboard.writeText(preview.textContent);
        copyButton.textContent = 'Текст скопирован';
        status.textContent = 'Откройте Viber, вставьте сообщение и приложите фотографии.';
      } catch {
        const range = document.createRange();
        range.selectNodeContents(preview);
        const selection = window.getSelection();
        selection.removeAllRanges();
        selection.addRange(range);
        status.textContent = 'Текст выделен. Скопируйте его вручную и вставьте в Viber.';
      }
    });
  }

  document.querySelectorAll('a[href^="tel:"], a[href*="viber.click"]').forEach((link) => {
    link.addEventListener('click', () => {
      const action = link.href.startsWith('tel:') ? 'phone_click' : 'viber_click';
      document.dispatchEvent(new CustomEvent('vitcleaner:conversion', { detail: { action } }));
    });
  });
})();
