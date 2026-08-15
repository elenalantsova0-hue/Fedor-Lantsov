(() => {
  const page = document.documentElement.dataset.page;
  document.querySelectorAll('.nav-link').forEach(link => {
    if (link.dataset.page === page) link.setAttribute('aria-current', 'page');
  });
  document.querySelectorAll('[data-current-year]').forEach(element => {
    element.textContent = new Date().getFullYear();
  });

  const form = document.querySelector('[data-inquiry-form]');
  if (!form) return;

  const status = form.querySelector('.form-status');
  const submitButton = form.querySelector('[data-submit-button]');
  const artworkField = form.elements.artworkTitle;
  const sourcePageField = form.elements.sourcePage;
  const artwork = new URLSearchParams(location.search).get('artwork');
  const painting = (window.paintingsData || []).find(item => item.slug === artwork);

  sourcePageField.value = location.href;
  if (painting) {
    artworkField.value = painting.title;
    form.querySelector('#message').value = `I would like more information about “${painting.title}”.`;
  }

  const setStatus = (message, state) => {
    status.textContent = message;
    status.dataset.state = state;
  };

  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (!form.reportValidity()) return;

    const defaultLabel = submitButton.textContent;
    submitButton.disabled = true;
    submitButton.textContent = 'Sending…';
    setStatus('Sending your inquiry…', 'pending');

    try {
      const response = await fetch(form.action, {
        method: form.method.toUpperCase(),
        body: new FormData(form),
        headers: { Accept: 'application/json' },
      });

      if (!response.ok) {
        const result = await response.json().catch(() => null);
        const details = result?.errors?.map(error => error.message).join(' ');
        throw new Error(details || 'The inquiry could not be sent. Please try again.');
      }

      form.reset();
      sourcePageField.value = location.href;
      setStatus('Thank you. Your private inquiry has been sent.', 'success');
    } catch (error) {
      setStatus(error.message || 'The inquiry could not be sent. Please try again.', 'error');
    } finally {
      submitButton.disabled = false;
      submitButton.textContent = defaultLabel;
    }
  });
})();
