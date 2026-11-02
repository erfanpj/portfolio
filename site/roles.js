// Fit check tabs and project filter. Without JavaScript every panel and project stays visible.
(() => {
  const list = [...document.querySelectorAll('.project-entry')];
  const chips = [...document.querySelectorAll('.project-filter button')];
  const status = document.querySelector('#filter-status');
  const names = {all:'all projects', ai:'applied AI & automation', ml:'ML & computer vision', neuro:'brain & health data', software:'software'};
  function filter(key, announce = true) {
    const keys = key.split(' ');
    let shown = 0;
    for (const item of list) {
      const tags = (item.dataset.tags || '').split(' ');
      const show = key === 'all' || keys.some(k => tags.includes(k));
      item.hidden = !show; if (show) shown++;
    }
    for (const c of chips) c.setAttribute('aria-pressed', String(c.dataset.filter === keys[0] || (key === 'all' && c.dataset.filter === 'all')));
    if (status && announce) status.textContent = key === 'all' ? '' : `Showing ${shown} of ${list.length} projects for ${names[keys[0]] || keys[0]}.`;
  }
  if (chips.length) {
    document.querySelector('.project-filter').hidden = false;
    chips.forEach(c => c.addEventListener('click', () => filter(c.dataset.filter)));
  }
  const tabs = [...document.querySelectorAll('.fit-tabs [role=tab]')];
  const panels = document.querySelector('.fit-panels');
  if (tabs.length && panels) {
    document.querySelector('.fit-tabs').hidden = false; panels.classList.add('js');
    const select = (tab, focus) => {
      for (const t of tabs) {
        const on = t === tab; t.setAttribute('aria-selected', String(on)); t.tabIndex = on ? 0 : -1;
        document.getElementById(t.getAttribute('aria-controls')).hidden = !on;
      }
      if (focus) tab.focus();
    };
    tabs.forEach((t, i) => {
      t.addEventListener('click', () => select(t));
      t.addEventListener('keydown', e => {
        const k = {ArrowRight: 1, ArrowLeft: -1}[e.key];
        if (k) { e.preventDefault(); select(tabs[(i + k + tabs.length) % tabs.length], true); }
        else if (e.key === 'Home') { e.preventDefault(); select(tabs[0], true); }
        else if (e.key === 'End') { e.preventDefault(); select(tabs.at(-1), true); }
      });
    });
    select(tabs[0]);
  }
  document.querySelectorAll('.fit-link[data-show]').forEach(a => a.addEventListener('click', () => filter(a.dataset.show)));
})();
