'use strict';
const en = document.documentElement.lang === 'en';
const say = (es, english) => en ? english : es;
const emit = (name, service) => window.dispatchEvent(new CustomEvent('readytoprod:conversion', {
  detail: { event: name, service: service || null, language: document.documentElement.lang }
}));
// No analytics requests, identifiers or personal data are sent by this event hook.
for (const button of document.querySelectorAll('[data-copy]')) {
  button.addEventListener('click', async () => {
    const status = document.getElementById('copy-status');
    try {
      if (!navigator.clipboard?.writeText) throw new Error('unavailable');
      await navigator.clipboard.writeText(button.dataset.copy);
      status.textContent = say('Correo copiado: ', 'Email copied: ') + button.dataset.copy;
      emit('email_copied');
    } catch {
      status.textContent = say('Selecciona y copia este correo: ', 'Select and copy this email: ') + button.dataset.copy;
    }
  });
}
const menu = document.getElementById('main-nav');
const toggle = document.getElementById('menu-toggle');
if (menu && toggle) {
  const mobile = matchMedia('(max-width: 800px)');
  const setOpen = open => { menu.hidden = !open; toggle.setAttribute('aria-expanded', String(open)); };
  const reset = () => { toggle.hidden = !mobile.matches; setOpen(!mobile.matches); };
  toggle.addEventListener('click', () => setOpen(menu.hidden));
  menu.addEventListener('click', e => { if (mobile.matches && e.target.closest('a')) setOpen(false); });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && mobile.matches && !menu.hidden) { setOpen(false); toggle.focus(); }
  });
  mobile.addEventListener('change', reset);
  reset();
}
function languageLinks() {
  for (const link of document.querySelectorAll('[data-language]')) {
    const target = new URL(link.href);
    target.hash = location.hash;
    link.href = target.href;
  }
}
languageLinks();
addEventListener('hashchange', languageLinks);

const form = document.getElementById('contact-form');
if (form) form.addEventListener('submit', async event => {
  event.preventDefault();
  if (!form.reportValidity()) return;
  const status = document.getElementById('contact-status');
  const button = form.querySelector('[type=submit]');
  const data = new FormData(form);
  const service = data.get('service');
  const selected = form.querySelector('select').selectedOptions[0].textContent;
  const message = String(data.get('message') || '').trim();
  if (message.length < 15) {
    status.textContent = say('Describe tu consulta con al menos 15 caracteres.', 'Describe your inquiry using at least 15 characters.');
    form.querySelector('textarea').focus();
    return;
  }
  if (form.dataset.mode !== 'live') {
    const subject = say('Proyecto para readytoprod: ', 'Project for readytoprod: ') + selected;
    const body = say('Servicio: ', 'Service: ') + selected + '\n\n' + message;
    const url = 'mailto:dariosc235@gmail.com?cc=fsegui16%40gmail.com&subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
    const retry = document.createElement('a');
    retry.href = url;
    retry.className = 'text-link';
    retry.textContent = say('Abrir borrador de correo', 'Open email draft');
    status.replaceChildren(document.createTextNode(say('El borrador está listo. Revisa el mensaje y envíalo desde tu correo. ', 'Your draft is ready. Review it and send it from your email app. ')), retry);
    emit('email_draft_prepared', service); // This is not an inquiry-sent event.
    return;
  }
  button.disabled = true;
  form.setAttribute('aria-busy', 'true');
  status.textContent = say('Enviando…', 'Sending…');
  // Reuse the key on retry, then clear it only after a successful request.
  form.dataset.requestId ||= crypto.randomUUID();
  try {
    const response = await fetch('/api/contact', {
      method: 'POST',
      signal: AbortSignal.timeout(30000),
      headers: { 'Content-Type': 'application/json', 'Idempotency-Key': form.dataset.requestId },
      body: JSON.stringify({
        service, message, email: data.get('email'), name: data.get('name') || '',
        website: data.get('website') || '', language: en ? 'en' : 'es',
        turnstileToken: data.get('cf-turnstile-response') || ''
      })
    });
    if (!response.ok) throw new Error('not accepted');
    status.textContent = say('Tu consulta ha sido aceptada para su envío al equipo.', 'Your inquiry has been accepted for delivery to the team.');
    emit('inquiry_accepted', service);
    form.reset();
    delete form.dataset.requestId;
  } catch {
    status.textContent = say('No se pudo enviar la consulta. Inténtalo de nuevo o utiliza los correos de contacto.', 'Your inquiry could not be sent. Try again or use the contact email addresses.');
  } finally {
    button.disabled = false;
    form.removeAttribute('aria-busy');
    if (window.turnstile) window.turnstile.reset();
  }
});

const demo = document.getElementById('demo-form');
if (demo) {
  const status = document.getElementById('demo-status');
  const result = document.getElementById('demo-result');
  const download = document.getElementById('demo-download');
  let rows = [];
  demo.addEventListener('submit', event => {
    event.preventDefault();
    if (!demo.reportValidity()) return;
    const data = new FormData(demo);
    const volume = Number(data.get('volume'));
    const urgent = data.get('urgency') === 'urgent';
    const service = data.get('service');
    const type = demo.querySelector('[name=service]').selectedOptions[0].textContent;
    const next = urgent ? say('Revisión prioritaria por el equipo', 'Priority review by the team')
      : volume >= 25 ? say('Revisión del volumen y agrupación de solicitudes', 'Review volume and group requests')
      : say('Diagnóstico del proceso y definición del alcance', 'Process discovery and scope definition');
    rows = [
      [say('Servicio', 'Service'), type],
      [say('Solicitudes al día', 'Requests per day'), String(volume)],
      [say('Prioridad declarada', 'Requested priority'), urgent ? say('Urgente', 'Urgent') : 'Normal'],
      [say('Siguiente paso', 'Next step'), next]
    ];
    result.replaceChildren();
    for (const [key, value] of rows) {
      const dt = document.createElement('dt'); dt.textContent = key;
      const dd = document.createElement('dd'); dd.textContent = value;
      result.append(dt, dd);
    }
    status.textContent = say('Solicitud organizada con los datos seleccionados. Puedes descargar el resumen.', 'Request organized using your selected data. You can download the summary.');
    download.hidden = false;
    emit('demo_completed', service);
  });
  download.addEventListener('click', () => {
    if (!rows.length) return;
    const cell = v => '"' + String(v).replace(/"/g, '""') + '"';
    const blob = new Blob(['\uFEFF' + rows.map(row => row.map(cell).join(',')).join('\r\n')], { type: 'text/csv;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a'); a.href = url; a.download = 'readytoprod-summary.csv'; a.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
    emit('demo_downloaded');
  });
  document.getElementById('demo-reset').addEventListener('click', () => {
    demo.reset(); rows = []; result.replaceChildren(); download.hidden = true;
    status.textContent = say('Muestra restablecida. Organiza otra solicitud para ver el resultado.', 'Sample reset. Organize another request to see the result.');
    demo.querySelector('select').focus();
  });
}
