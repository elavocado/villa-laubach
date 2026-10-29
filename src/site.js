(() => {
  'use strict';
  const de = document.documentElement.lang === 'de';
  const menu = document.querySelector('.menu-toggle');
  const mobile = document.getElementById('mobile-nav');
  if (menu && mobile) {
    menu.addEventListener('click', () => {
      const expanded = menu.getAttribute('aria-expanded') === 'true';
      menu.setAttribute('aria-expanded', String(!expanded));
      mobile.hidden = expanded;
    });
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape' && !mobile.hidden) { mobile.hidden = true; menu.setAttribute('aria-expanded','false'); menu.focus(); }
    });
  }
  const gallery = [...document.querySelectorAll('.gallery-item')];
  const dialog = document.querySelector('.lightbox');
  let current = 0;
  let opener;
  const visibleGallery = () => gallery.filter(x => !x.hidden);
  function showPhoto(index) {
    const items = visibleGallery();
    if (!items.length) return;
    current = (index + items.length) % items.length;
    const source = items[current].querySelector('img');
    const target = dialog.querySelector('figure img');
    target.src = source.src; target.alt = source.alt;
    dialog.querySelector('figcaption').textContent = `${source.alt} · ${current + 1} / ${items.length}`;
  }
  document.querySelectorAll('[data-filter]').forEach(button => button.addEventListener('click', () => {
    document.querySelectorAll('[data-filter]').forEach(b => b.setAttribute('aria-pressed', String(b === button)));
    gallery.forEach(item => { item.hidden = button.dataset.filter !== 'all' && item.dataset.category !== button.dataset.filter; });
  }));
  if (dialog) {
    gallery.forEach(item => item.addEventListener('click', () => {
      opener = item; showPhoto(visibleGallery().indexOf(item)); dialog.showModal(); document.body.classList.add('no-scroll');
    }));
    dialog.querySelector('.lightbox-close').addEventListener('click', () => dialog.close());
    dialog.querySelector('.lightbox-prev').addEventListener('click', () => showPhoto(current - 1));
    dialog.querySelector('.lightbox-next').addEventListener('click', () => showPhoto(current + 1));
    dialog.addEventListener('click', e => { if (e.target === dialog) dialog.close(); });
    dialog.addEventListener('keydown', e => { if (e.key === 'ArrowRight') showPhoto(current + 1); if (e.key === 'ArrowLeft') showPhoto(current - 1); });
    dialog.addEventListener('close', () => { document.body.classList.remove('no-scroll'); opener?.focus(); });
  }
  const form = document.getElementById('stay-form');
  if (form) {
    const arrival = form.elements.arrival;
    const departure = form.elements.departure;
    const today = new Date();
    const dateISO = d => `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
    arrival.min = dateISO(today);
    departure.min = dateISO(today);
    arrival.addEventListener('change', () => {
      if (!arrival.value) return;
      const next = new Date(arrival.value + 'T12:00:00'); next.setDate(next.getDate() + 1);
      departure.min = dateISO(next);
    });
    form.addEventListener('submit', e => {
      e.preventDefault();
      const error = document.getElementById('form-error');
      error.textContent = '';
      document.getElementById('enquiry-result').hidden = true;
      const adults = Number(form.elements.adults.value), children = Number(form.elements.children.value);
      if (!arrival.value || !departure.value || arrival.value < dateISO(today) || departure.value <= arrival.value) {
        error.textContent = de ? 'Bitte wählen Sie eine gültige Anreise und eine spätere Abreise.' : 'Please choose a valid arrival date and a later departure date.'; return;
      }
      if (adults + children > 8) { error.textContent = de ? 'Die Unterkunft wird für maximal 8 Gäste angeboten. Bitte passen Sie die Gästezahl an.' : 'The accommodation is listed for up to 8 guests. Please adjust your guest numbers.'; return; }
      const format = value => new Intl.DateTimeFormat(de ? 'de-DE' : 'en-GB', {day:'numeric',month:'long',year:'numeric'}).format(new Date(value+'T12:00:00'));
      const custom = form.elements.message.value.trim();
      document.getElementById('enquiry-text').value = de
        ? `Hallo,\n\nwir interessieren uns für einen Aufenthalt in der Villa Laubach.\nAnreise: ${format(arrival.value)}\nAbreise: ${format(departure.value)}\nErwachsene: ${adults}\nKinder: ${children}\n\n${custom ? custom + '\n\n' : ''}Ist die Unterkunft für diesen Zeitraum verfügbar? Bitte teilen Sie uns die passenden Bedingungen mit.\n\nVielen Dank!`
        : `Hello,\n\nwe are interested in staying at Villa Laubach.\nArrival: ${format(arrival.value)}\nDeparture: ${format(departure.value)}\nAdults: ${adults}\nChildren: ${children}\n\n${custom ? custom + '\n\n' : ''}Is the accommodation available for these dates? Please let us know the applicable terms.\n\nThank you!`;
      const result = document.getElementById('enquiry-result'); result.hidden = false;
      document.getElementById('copy-status').textContent = '';
      result.scrollIntoView({behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth',block:'center'});
    });
    document.getElementById('copy-enquiry').addEventListener('click', async () => {
      const text = document.getElementById('enquiry-text');
      const status = document.getElementById('copy-status');
      try { await navigator.clipboard.writeText(text.value); status.textContent = de ? 'Kopiert. Fügen Sie Ihren Text in Ihre Nachricht auf Airbnb ein.' : 'Copied. Paste the text into your message on Airbnb.'; }
      catch { text.focus(); text.select(); status.textContent = de ? 'Bitte kopieren Sie den ausgewählten Text manuell.' : 'Please copy the selected text manually.'; }
    });
  }
})();
