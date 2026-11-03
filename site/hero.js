// Menu, notes and dialogs share the browser's focus model. The diagram never blocks reading.
(() => {
  const desktop = document.querySelector('#hero-scene'), phone = document.querySelector('#mobile-hero');
  const frame = document.querySelector('.heroFrame'), motion = matchMedia('(prefers-reduced-motion: reduce)');
  const preference = document.querySelector('#reduce-motion');
  let selected = false;
  try { selected = localStorage.getItem('epj-reduce-animation') === 'yes'; } catch {}
  function renderMotion() {
    for (const node of [desktop, phone]) node?.classList.toggle('still', selected || motion.matches);
    preference.checked = selected || motion.matches;
    preference.disabled = motion.matches;
    preference.title = motion.matches ? 'Your device requests reduced motion.' : '';
  }
  preference.addEventListener('change', () => { selected = preference.checked; try { localStorage.setItem('epj-reduce-animation', selected ? 'yes' : 'no'); } catch {} renderMotion(); });
  motion.addEventListener('change', renderMotion);
  renderMotion();
  const visible=new IntersectionObserver(items=>items.forEach(i=>i.target.classList.toggle('scene-away',!i.isIntersecting)));
  for(const node of [desktop,phone]) if(node)visible.observe(node);
  function fit() {
    if (!frame || !frame.clientWidth) return;
    frame.style.setProperty('--r', Math.min(frame.clientWidth / 1440, frame.clientHeight / 824, 1));
  }
  if (frame) { new ResizeObserver(fit).observe(frame); fit(); }

  const cases = [...document.querySelectorAll('a.case')];
  cases.forEach(link => {
    const dialog = document.querySelector(link.hash);
    if (!dialog || typeof dialog.showModal !== 'function') return;
    link.addEventListener('click', e => {
      e.preventDefault(); dialog.showModal();
      dialog.addEventListener('close', () => link.focus({preventScroll:true}), {once:true});
    });
    dialog.addEventListener('click', e => {
      if(e.target !== dialog) return;
      const b=dialog.getBoundingClientRect();
      if(e.clientX<b.left || e.clientX>b.right || e.clientY<b.top || e.clientY>b.bottom) dialog.close();
    });
    dialog.addEventListener('keydown',e=>{
      if(e.key!=='Tab')return;
      const list=[...dialog.querySelectorAll('button:not([disabled]),a[href]')];
      if(e.shiftKey&&document.activeElement===list[0]){e.preventDefault();list.at(-1)?.focus();}
      else if(!e.shiftKey&&document.activeElement===list.at(-1)){e.preventDefault();list[0]?.focus();}
    });
  });

  const menu = document.querySelector('#mobile-nav'), toggle = document.querySelector('#menu-toggle');
  if(menu && toggle) {
    const dismiss = () => { if(menu.open) menu.close(); toggle.setAttribute('aria-expanded','false');toggle.focus({preventScroll:true}); };
    toggle.addEventListener('click', () => {
      if(menu.open) return dismiss();
      menu.showModal(); toggle.setAttribute('aria-expanded','true'); document.querySelector('#menu-close')?.focus();
    });
    document.querySelector('#menu-close')?.addEventListener('click',dismiss);
    menu.addEventListener('cancel',e=>{e.preventDefault();dismiss();});
    menu.addEventListener('close',() => {toggle.setAttribute('aria-expanded','false');});
    menu.addEventListener('click',e=>{
      const a=e.target.closest('a');
      if(a) {
        const target=a.hash&&document.getElementById(a.hash.slice(1)); dismiss();
        if(target){ target.setAttribute('tabindex','-1'); target.focus({preventScroll:true}); }
        return;
      }
      const b=menu.getBoundingClientRect(); if(e.target===menu&&(e.clientX<b.left||e.clientX>b.right||e.clientY<b.top||e.clientY>b.bottom))dismiss();
    });
    menu.addEventListener('keydown',e=>{
      if(e.key!=='Tab')return;
      const active=[...menu.querySelectorAll('a[href],button:not([disabled])')];
      if(e.shiftKey && document.activeElement===active[0]) {e.preventDefault();active.at(-1).focus();}
      else if(!e.shiftKey && document.activeElement===active.at(-1)) {e.preventDefault();active[0].focus();}
    });
    matchMedia('(min-width:1025px)').addEventListener('change',e=>{if(e.matches)dismiss();});
  }

  // Phones get the wide side-by-side illustration from the HTML; two-column tablet and landscape layouts keep the stacked artwork.
  const signal=document.querySelector('.mobileSignal');
  if(signal){
    const art={phone:{v:"0 0 360 258",a:"translate(-58,-149.7) scale(0.45)",l:"translate(108.5 3) scale(0.42)",c:"M90.5,96.9 L151.31,40.04 L121.4,174.21 Z",e:"M151.31,40.04 L90.5,96.9 L121.4,174.21",g:["90.5","96.9","234.5","129"]},stack:{v:"0 0 360 465",a:"translate(-60,-247) scale(0.52)",l:"translate(58 167) scale(0.49)",c:"M111.6,37.96 L300.31,208.6 L65.28,288.13 Z",e:"M300.31,208.6 L111.6,37.96 L65.28,288.13",g:["111.6", "37.96", "205", "314"]}};
    const twoColumn=matchMedia('(min-width:600px) and (max-width:1024px), (min-width:475px) and (max-height:550px) and (max-width:1024px)');
    const q=c=>signal.querySelector(c);
    const arrange=()=>{const k=twoColumn.matches?'stack':'phone';if(signal.dataset.layout===k)return;const v=art[k],g=q('.m-cone-grad');
      signal.setAttribute('viewBox',v.v);q('.m-av').setAttribute('transform',v.a);q('.m-lens').setAttribute('transform',v.l);q('.m-cone').setAttribute('d',v.c);q('.m-cone-edge').setAttribute('d',v.e);
      ['x1','y1','x2','y2'].forEach((n,i)=>g.setAttribute(n,v.g[i]));signal.dataset.layout=k;};
    twoColumn.addEventListener('change',arrange);arrange();
  }
  const phoneMotifs=[...document.querySelectorAll('.mobileChem button')];
  const desktopMotifs=[...document.querySelectorAll('.hor2')];
  const note=document.querySelector('#mobile-motif-note');
  function clearMotifs(){
    for(const b of [...desktopMotifs,...phoneMotifs]) {
      b.removeAttribute('data-open');b.setAttribute('aria-expanded','false');
      if(b.matches(':hover,:focus-visible')) b.dataset.dismissed='true';
    }
    if(note){note.hidden=true; note.textContent='';}
  }
  phoneMotifs.forEach((b,i)=>b.addEventListener('click',()=>{
    const open=b.getAttribute('aria-expanded')==='true';clearMotifs();
    if(open||!note)return;
    const source=document.getElementById('desk-tip-'+i);
    const msg=source ? [...source.childNodes].filter(n=>n.nodeType===Node.TEXT_NODE).map(n=>n.textContent).join('').trim() : '';
    if(!msg)return;note.textContent=msg;note.hidden=false;b.setAttribute('aria-expanded','true');
  }));
  desktopMotifs.forEach(b=>{
    b.addEventListener('click',()=>{
      const open=b.dataset.open==='true';clearMotifs();
      if(!open){b.dataset.open='true';delete b.dataset.dismissed;b.setAttribute('aria-expanded','true');}
    });
    for(const type of ['pointerenter','focus']) b.addEventListener(type,()=>{delete b.dataset.dismissed;});
    b.addEventListener('blur', clearMotifs);
  });
  document.addEventListener('click',e=>{if(!e.target.closest('.hor2,.mobileChem,#mobile-motif-note'))clearMotifs();});
  document.addEventListener('keydown',e=>{if(e.key==='Escape')clearMotifs();});
})();
