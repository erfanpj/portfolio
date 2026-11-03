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

  // The light cone and the beam into step 1 are aimed from where the forehead lens and the zoom circle really are,
  // so they stay correct when the layout or the artwork scale changes. The HTML carries the same result as a fallback.
  const fmt=n=>Math.round(n*10)/10;
  function aim(svg,eye,ring,pin,{cone,edge,beam,grad}){
    const ctm=svg.getScreenCTM(),rc=ring.getScreenCTM(),pc=pin.getScreenCTM();if(!ctm||!rc||!pc)return;
    const inv=ctm.inverse(),pt=(m,x,y)=>new DOMPoint(x,y).matrixTransform(inv.multiply(m));
    const c=pt(rc,+ring.getAttribute('cx'),+ring.getAttribute('cy')),r=290*Math.hypot(inv.multiply(rc).a,inv.multiply(rc).b);
    const p=pt(pc,+pin.getAttribute('cx'),+pin.getAttribute('cy')),pr=+pin.getAttribute('r')*Math.hypot(inv.multiply(pc).a,inv.multiply(pc).b);
    const e=eye(inv);if(!e)return;
    const dx=c.x-e.x,dy=c.y-e.y,d=Math.hypot(dx,dy);if(d<=r)return;
    const base=Math.atan2(dy,dx),half=Math.asin(r/d),len=Math.sqrt(d*d-r*r);
    const t1=[e.x+len*Math.cos(base-half),e.y+len*Math.sin(base-half)],t2=[e.x+len*Math.cos(base+half),e.y+len*Math.sin(base+half)];
    const E=[fmt(e.x),fmt(e.y)].join(','),A=t1.map(fmt).join(','),B=t2.map(fmt).join(',');
    cone.setAttribute('d',`M${E} L${A} L${B} Z`);edge.setAttribute('d',`M${A} L${E} L${B}`);
    const bx=p.x-e.x,by=p.y-e.y,bl=Math.hypot(bx,by);beam.setAttribute('d',`M${E} L${fmt(p.x-bx/bl*pr)},${fmt(p.y-by/bl*pr)}`);
    [['x1',e.x],['y1',e.y],['x2',c.x],['y2',c.y]].forEach(([n,v])=>grad.setAttribute(n,fmt(v)));
  }
  const scene=document.querySelector('#hero-scene .d-lens')?.ownerSVGElement;
  const aimDesktop=()=>{const eye=document.querySelector('.d-eye');if(!scene||!eye||!frame?.clientWidth)return;
    aim(scene,()=>({x:eye.offsetLeft+eye.offsetWidth/2,y:eye.offsetTop+eye.offsetHeight/2}),scene.querySelector('.d-lens .okring'),scene.querySelector('.d-lens .pin0'),
      {cone:scene.querySelector('.d-cone'),edge:scene.querySelector('.d-cone-edge'),beam:scene.querySelector('.d-beam'),grad:document.getElementById('cg')});};
  aimDesktop();matchMedia('(min-width:1025px)').addEventListener('change',aimDesktop);
  // Phones get the diagonal illustration from the HTML; two-column tablet and landscape layouts use the stacked artwork.
  const signal=document.querySelector('.mobileSignal');
  if(signal){
    const art={"phone":{"v":"0 0 360 260","a":"translate(-54.9,-165.8) scale(0.47)","l":"translate(157.4 1) scale(0.34)"},"stack":{"v":"0 0 360 465","a":"translate(-43.8,-226) scale(0.46)","l":"translate(84 189) scale(0.46)"}};
    const twoColumn=matchMedia('(min-width:600px) and (max-width:1024px), (min-width:475px) and (max-height:550px) and (max-width:1024px)');
    const q=c=>signal.querySelector(c);
    const aimPhone=()=>{const eye=q('.m-eye');aim(signal,inv=>{const m=eye.getScreenCTM();return m&&new DOMPoint(+eye.getAttribute('x')+26,+eye.getAttribute('y')+26).matrixTransform(inv.multiply(m));},q('.m-lens .okring'),q('.m-lens .pin0'),
      {cone:q('.m-cone'),edge:q('.m-cone-edge'),beam:q('.m-beam'),grad:q('.m-cone-grad')});};
    const arrange=()=>{const k=twoColumn.matches?'stack':'phone';if(signal.dataset.layout!==k){const v=art[k];
      signal.setAttribute('viewBox',v.v);q('.m-av').setAttribute('transform',v.a);q('.m-lens').setAttribute('transform',v.l);signal.dataset.layout=k;}
      aimPhone();};
    twoColumn.addEventListener('change',arrange);matchMedia('(max-width:1024px)').addEventListener('change',arrange);arrange();
  }
  // Hero buttons: icon + label, with an explanation on hover, keyboard focus or a long press (a normal tap still follows the link).
  const heroButtons=[...document.querySelectorAll('a.hb')];
  heroButtons.forEach(b=>{
    let timer=0,held=false;
    b.addEventListener('pointerdown',e=>{if(e.pointerType==='mouse')return;held=false;clearTimeout(timer);
      timer=setTimeout(()=>{held=true;heroButtons.forEach(o=>o!==b&&o.removeAttribute('data-tip'));b.dataset.tip='open';},450);});
    for(const t of ['pointerup','pointercancel','pointerleave'])b.addEventListener(t,()=>clearTimeout(timer));
    b.addEventListener('click',e=>{if(held){e.preventDefault();held=false;}});
    b.addEventListener('contextmenu',e=>{if(held||b.dataset.tip==='open')e.preventDefault();});
    for(const t of ['focus','pointerenter'])b.addEventListener(t,()=>{if(b.dataset.tip==='closed')b.removeAttribute('data-tip');});
    b.addEventListener('blur',()=>b.removeAttribute('data-tip'));
  });
  document.addEventListener('pointerdown',e=>{if(!e.target.closest('a.hb'))heroButtons.forEach(b=>{if(b.dataset.tip==='open')b.removeAttribute('data-tip');});});
  document.addEventListener('keydown',e=>{if(e.key==='Escape')heroButtons.forEach(b=>{if(b.dataset.tip==='open'||b.matches(':hover,:focus-visible'))b.dataset.tip='closed';});});
  const phoneMotifs=[...document.querySelectorAll('.mobileChem button')];
  const desktopMotifs=[...document.querySelectorAll('.hor2,.mobileHormones .mh')];
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
  // Icon tooltips open on hover, tap or keyboard focus; Escape, blur or a second tap closes them.
  const openMotif=b=>{clearMotifs();b.dataset.open='true';delete b.dataset.dismissed;b.setAttribute('aria-expanded','true');};
  desktopMotifs.forEach(b=>{
    let focusedAt=0;
    b.addEventListener('focus',()=>{focusedAt=Date.now();openMotif(b);});
    b.addEventListener('click',()=>{
      if(b.dataset.open==='true'&&Date.now()-focusedAt>400)clearMotifs(); else openMotif(b);
    });
    b.addEventListener('pointerenter',()=>{delete b.dataset.dismissed;});
    b.addEventListener('blur', clearMotifs);
  });
  document.addEventListener('click',e=>{if(!e.target.closest('.hor2,.mobileHormones,.mobileChem,#mobile-motif-note'))clearMotifs();});
  document.addEventListener('keydown',e=>{if(e.key==='Escape')clearMotifs();});
})();
