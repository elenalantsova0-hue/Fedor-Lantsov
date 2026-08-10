(() => {
  const requested = new URLSearchParams(location.search).get('id');
  if (!requested || !window.paintingsData) return;
  const painting = window.paintingsData.find(item => item.slug === requested || String(item.id) === requested);
  if (painting) location.replace(`artworks/${encodeURIComponent(painting.slug)}/`);
})();
