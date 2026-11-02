(() => {
  'use strict';
  const id = document.currentScript?.dataset.measurementId;
  const hosts = ['erfanpj.com', 'www.erfanpj.com'];
  if (!/^G-[A-Z0-9]+$/.test(id || '') || location.protocol !== 'https:' || !hosts.includes(location.hostname)) return;

  const panel = document.getElementById('analytics-privacy');
  const settings = document.getElementById('analytics-settings');
  const status = document.getElementById('analytics-status');
  const buttons = panel.querySelectorAll('[data-analytics-choice]');
  const key = 'epj-analytics-choice-v1';
  const lifetime = 180 * 24 * 60 * 60;
  const disableKey = 'ga-disable-' + id;
  const denied = {analytics_storage: 'denied', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied'};
  const projects = new Map([
    ['https://erfanpj.github.io/brain-signals-lab/viewer/', 'brain-signals-lab'],
    ['https://erfanpj.github.io/opsdesk-ai/', 'opsdesk-ai'],
    ['https://erfanpj.github.io/reachboard-showcase/', 'reachboard'],
    ['https://erfanpj.github.io/recall-studio/', 'recall-studio'],
    ['https://erfanpj.github.io/commonnest-showcase/', 'commonnest'],
    ['#case-0', 'brain-signals-lab'], ['#case-1', 'opsdesk-ai'], ['#case-2', 'reachboard']
  ]);
  let choice = null;
  let tag = null;
  let ready = false;
  let configured = false;

  function savedChoice() {
    try {
      const saved = JSON.parse(localStorage.getItem(key));
      if (saved && ['allow','decline'].includes(saved.value) && saved.until > Date.now()) return saved.value;
    } catch { /* Preferences may be unavailable in a private browser. */ }
    return null;
  }

  function forgetCookies() {
    for (const name of ['_ga', '_ga_' + id.slice(2)]) {
      for (const domain of ['', '; Domain=erfanpj.com']) {
        document.cookie = name + '=; Path=/; Max-Age=0; Secure; SameSite=Lax' + domain;
      }
    }
  }

  function referrerOrigin() {
    try {
      const source = new URL(document.referrer);
      if (['http:', 'https:'].includes(source.protocol) && !hosts.includes(source.hostname)) return source.origin;
    } catch { /* Direct visits have no referrer. */ }
    return '';
  }

  function configure() {
    if (!ready || choice !== 'allow' || configured) return;
    configured = true;
    window.gtag('config', id, {
      send_page_view: false,
      page_location: 'https://erfanpj.com/',
      page_title: document.title,
      page_referrer: referrerOrigin(),
      allow_google_signals: false,
      allow_ad_personalization_signals: false,
      cookie_domain: 'erfanpj.com',
      cookie_expires: lifetime,
      cookie_update: false,
      cookie_flags: 'SameSite=Lax;Secure'
    });
    window.gtag('event', 'page_view', {send_to: id});
  }

  function enable() {
    window[disableKey] = false;
    if (!tag) {
      window.dataLayer = window.dataLayer || [];
      window.gtag = function () { window.dataLayer.push(arguments); };
      window.gtag('consent', 'default', denied);
      window.gtag('js', new Date());
      tag = document.createElement('script');
      tag.async = true;
      tag.referrerPolicy = 'no-referrer';
      tag.src = 'https://www.googletagmanager.com/gtag/js?id=' + id;
      tag.addEventListener('load', () => { ready = true; configure(); });
      document.head.append(tag);
    }
    window.gtag('consent', 'update', {...denied, analytics_storage: 'granted'});
    configure();
  }

  function apply(value) {
    choice = value;
    if (choice === 'allow') enable();
    else {
      window[disableKey] = true;
      if (tag) window.gtag('consent', 'update', denied);
      forgetCookies();
    }
    for (const button of buttons) button.setAttribute('aria-pressed', String(button.dataset.analyticsChoice === choice));
    status.textContent = choice === 'allow' ? 'Analytics is on.' : choice === 'decline' ? 'Analytics is off.' : '';
  }

  for (const button of buttons) {
    button.addEventListener('click', () => {
      const value = button.dataset.analyticsChoice;
      let remembered = true;
      try { localStorage.setItem(key, JSON.stringify({value, until: Date.now() + lifetime * 1000})); }
      catch { remembered = false; }
      apply(value);
      if (!remembered) status.textContent += ' This choice applies to this visit.';
    });
  }

  settings.hidden = false;
  settings.addEventListener('click', () => {
    panel.hidden = false;
    panel.scrollIntoView({block:'start'});
    document.getElementById('analytics-title').focus({preventScroll:true});
  });
  function sync() {
    const saved = savedChoice();
    if (saved !== choice) apply(saved);
    if (!saved) panel.hidden = false;
  }
  window.addEventListener('storage', event => { if (event.key === key || event.key === null) sync(); });
  window.addEventListener('pageshow', event => { if (event.persisted) sync(); });

  function trackLink(event) {
    if (choice !== 'allow' || !configured || event.button > 1) return;
    const link = event.target.closest?.('a[href]');
    if (!link) return;
    const href = link.getAttribute('href');
    if (href === 'Erfan-Pirjahandideh-CV.pdf') {
      window.gtag('event', 'file_download', {send_to:id, file_name:'Erfan-Pirjahandideh-CV.pdf', file_extension:'pdf'});
    } else if (projects.has(href)) {
      window.gtag('event', 'select_content', {
        send_to: id, content_type: href.startsWith('#') ? 'case_study' : 'project_demo', content_id: projects.get(href)
      });
    }
  }
  document.addEventListener('click', trackLink, true);
  document.addEventListener('auxclick', trackLink, true);

  apply(savedChoice());
  panel.hidden = choice !== null && location.hash !== '#analytics-privacy';
})();
