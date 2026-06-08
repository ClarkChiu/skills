// social-card QA rules — piped into `agent-browser eval --stdin`.
// Runs in the rendered page DOM; returns a findings array. Empty = pass.
(() => {
  const FLOOR = 28;                       // min readable body px on a 1080-wide canvas
  const TITLE_MAX_LINES = 4;              // display-title hard cap
  const SAFE = { 'ig-916': { top: 250, bottom: 340 } };  // Stories/Reels UI bands
  const out = [];
  for (const card of document.querySelectorAll('.card')) {
    const id = card.id || '(no-id)';
    // R1 overflow
    if (card.scrollHeight > card.clientHeight + 1)
      out.push({ card: id, rule: 'R1-overflow', fix: 'split the card or cut copy — never shrink the font' });
    // R3 min font floor on body/lead/caption
    for (const el of card.querySelectorAll('.body,.lead,.caption,.meta,.label')) {
      const px = parseFloat(getComputedStyle(el).fontSize);
      if (px && px < FLOOR)
        out.push({ card: id, rule: 'R3-font-floor', detail: `${el.className} ${px}px < ${FLOOR}px` });
    }
    // Title line cap
    for (const t of card.querySelectorAll('.title,.h-hero,.h-xl')) {
      const lh = parseFloat(getComputedStyle(t).lineHeight) || 1.1 * parseFloat(getComputedStyle(t).fontSize);
      const lines = Math.round(t.scrollHeight / lh);
      if (lines > TITLE_MAX_LINES)
        out.push({ card: id, rule: 'title-cap', detail: `${lines} lines > ${TITLE_MAX_LINES}`, fix: 'shorten the title' });
    }
    // Safe-area for Stories/Reels
    for (const [cls, band] of Object.entries(SAFE)) {
      if (!card.classList.contains(cls)) continue;
      const cr = card.getBoundingClientRect();
      for (const el of card.querySelectorAll('.title,.body,.lead,.cta')) {
        const r = el.getBoundingClientRect();
        if (r.top - cr.top < band.top || cr.bottom - r.bottom < band.bottom)
          out.push({ card: id, rule: 'safe-area', detail: `${el.className} enters the UI band`, fix: 'pull content into the central safe band' });
      }
    }
  }
  return out;
})();
