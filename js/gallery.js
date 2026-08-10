(() => {
  const root = document.querySelector('[data-gallery]');
  if (!root) return;
  const staticCards = [...root.querySelectorAll('.painting-card')];
  const buttons = document.querySelectorAll('[data-filter]');
  const applyFilter = filter => {
    staticCards.forEach(card => {
      const show = filter === 'all' || card.dataset.category === filter || (filter === 'sold' && card.dataset.available === 'false');
      card.hidden = !show;
    });
  };
  buttons.forEach(button => button.addEventListener('click', () => {
    buttons.forEach(item => item.setAttribute('aria-pressed', 'false'));
    button.setAttribute('aria-pressed', 'true');
    applyFilter(button.dataset.filter);
  }));
  applyFilter('all');
})();
