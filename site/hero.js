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

  // The light cone and the beam into step 1 are aimed from where the forehead lens, the zoom circle and step 1 really are.
  // All three anchors are converted into the drawing's own user space (the SVG viewBox), so the result is independent of
  // CSS scaling. The HTML carries the same result for the phone layout as a no-JavaScript fallback.
  const fmt=n=>Math.round(n*10)/10;
  function aim(svg,eye,ring,pin,{cone,edge,beam,grad}){
    const ctm=svg.getScreenCTM(),rc=ring.getScreenCTM(),pc=pin.getScreenCTM();if(!ctm||!rc||!pc)return;
    const inv=ctm.inverse(),local=m=>inv.multiply(m),pt=(m,x,y)=>new DOMPoint(x,y).matrixTransform(local(m)),scale=m=>Math.hypot(local(m).a,local(m).b);
    const c=pt(rc,+ring.getAttribute('cx'),+ring.getAttribute('cy')),r=290*scale(rc);
    const p=pt(pc,+pin.getAttribute('cx'),+pin.getAttribute('cy')),pr=+pin.getAttribute('r')*scale(pc);
    const e=eye(inv);if(!e)return;
    const dx=c.x-e.x,dy=c.y-e.y,d=Math.hypot(dx,dy);if(d<=r)return;
    const base=Math.atan2(dy,dx),half=Math.asin(r/d),len=Math.sqrt(d*d-r*r);
    const t1=[e.x+len*Math.cos(base-half),e.y+len*Math.sin(base-half)],t2=[e.x+len*Math.cos(base+half),e.y+len*Math.sin(base+half)];
    const E=[fmt(e.x),fmt(e.y)].join(','),A=t1.map(fmt).join(','),B=t2.map(fmt).join(',');
    cone.setAttribute('d',`M${E} L${A} L${B} Z`);edge.setAttribute('d',`M${A} L${E} L${B}`);
    const bx=p.x-e.x,by=p.y-e.y,bl=Math.hypot(bx,by);
    beam.setAttribute('d',`M${fmt(e.x+bx/bl*e.r)},${fmt(e.y+by/bl*e.r)} L${fmt(p.x-bx/bl*pr)},${fmt(p.y-by/bl*pr)}`);
    [['x1',e.x],['y1',e.y],['x2',c.x],['y2',c.y]].forEach(([n,v])=>grad.setAttribute(n,fmt(v)));
  }
  const scene=document.querySelector('#hero-scene .d-lens')?.ownerSVGElement;
  const aimDesktop=()=>{const eye=document.querySelector('.d-eye');if(!scene||!eye||!frame?.clientWidth)return;
    // the eye is an absolutely positioned image in the 1440x900 scene, which is also the SVG's viewBox space
    aim(scene,()=>({x:eye.offsetLeft+eye.offsetWidth/2,y:eye.offsetTop+eye.offsetHeight/2,r:eye.offsetWidth/2}),scene.querySelector('.d-lens .okring'),scene.querySelector('.d-lens .pin0'),
      {cone:scene.querySelector('.d-cone'),edge:scene.querySelector('.d-cone-edge'),beam:document.querySelector('.d-beam'),grad:document.getElementById('cg')});};
  // Phones get the diagonal artwork from the HTML; two-column tablet and landscape layouts use a taller diagonal.
  const signal=document.querySelector('.mobileSignal');
  const art={"phone":{"v":"0 0 360 300","a":"translate(-61,-143.9) scale(0.49)","l":"translate(156.8 -2) scale(0.342)"},"stack":{"v":"0 0 360 430","a":"translate(-67.2,-68.3) scale(0.55)","l":"translate(127.6 -1.6) scale(0.39)"}};
  const twoColumn=matchMedia('(min-width:600px) and (max-width:1024px), (min-width:475px) and (max-height:550px) and (max-width:1024px)');
  const aimPhone=()=>{if(!signal)return;const q=c=>signal.querySelector(c),eye=q('.m-eye');
    const k=twoColumn.matches?'stack':'phone';if(signal.dataset.layout!==k){const v=art[k];
      signal.setAttribute('viewBox',v.v);q('.m-av').setAttribute('transform',v.a);q('.m-lens').setAttribute('transform',v.l);signal.dataset.layout=k;}
    aim(signal,inv=>{const m=eye.getScreenCTM();if(!m)return null;const loc=inv.multiply(m),c=new DOMPoint(+eye.getAttribute('x')+26,+eye.getAttribute('y')+26).matrixTransform(loc);c.r=26*Math.hypot(loc.a,loc.b);return c;},
      q('.m-lens .okring'),q('.m-lens .pin0'),{cone:q('.m-cone'),edge:q('.m-cone-edge'),beam:q('.m-beam'),grad:q('.m-cone-grad')});};
  // Recompute on any viewport or layout change, at most once per frame.
  let queued=0;
  const reaim=()=>{if(queued)return;queued=requestAnimationFrame(()=>{queued=0;aimDesktop();aimPhone();});};
  reaim();
  twoColumn.addEventListener('change',reaim);matchMedia('(max-width:1024px)').addEventListener('change',reaim);
  addEventListener('resize',reaim);addEventListener('orientationchange',reaim);window.visualViewport?.addEventListener('resize',reaim);
  document.fonts?.ready.then(reaim);
  if('ResizeObserver' in window){const ro=new ResizeObserver(reaim);[signal,frame,document.querySelector('#hero-scene')].forEach(n=>n&&ro.observe(n));}
  // Hero buttons: icon + label, with an explanation on hover or keyboard focus (and during a long press, without
  // blocking the browser's own link preview). Escape closes it; taps and native link actions are untouched.
  const heroButtons=[...document.querySelectorAll('a.hb')];
  heroButtons.forEach(b=>{
    let timer=0;
    b.addEventListener('pointerdown',e=>{if(e.pointerType==='mouse')return;clearTimeout(timer);
      timer=setTimeout(()=>{heroButtons.forEach(o=>o!==b&&o.removeAttribute('data-tip'));b.dataset.tip='open';},450);},{passive:true});
    for(const t of ['pointerup','pointercancel'])b.addEventListener(t,()=>clearTimeout(timer),{passive:true});
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
