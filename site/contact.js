// Public endpoint only; no account credential is used by this page.
(() => {
  const form=document.getElementById('contact-form'), endpoint=window.EPJ_CONTACT_ENDPOINT;
  if (!form || !endpoint) return;
  const hint=form.querySelector('#human-prompt'), picture=form.querySelector('#human-picture'),
    ans=form.elements.answer, send=form.querySelector('[type=submit]'), status=form.querySelector('#contact-status'),
    refresh=form.querySelector('#new-challenge'), change=form.querySelector('#challenge-mode');
  const pending=new Map(), allowedStates={verification:'The answer was incorrect or expired. Try the new challenge.',invalid:'Please check the email, phone, subject and message.',limited:'The message limit has been reached. Please email Erfan directly or try later.',unavailable:'The mail service is unavailable. Please use the direct email link.'};
  let current=null, generation=0, mode='image', sending=false, seen=false;
  const random=()=>[...crypto.getRandomValues(new Uint8Array(8))].map(b=>b.toString(16).padStart(2,'0')).join('');
  window.EPJ_contact=({tag,result})=>{if(pending.has(tag))pending.get(tag)(result);};
  function query(params){
    return new Promise((resolve,reject)=>{
      const tag=random(), s=document.createElement('script'), u=new URL(endpoint);
      for (const [k,v] of Object.entries({...params,tag})) u.searchParams.set(k,v);
      const finish=(cb,v)=>{clearTimeout(timer);pending.delete(tag);s.remove();cb(v);};
      const timer=setTimeout(()=>finish(reject,Error('Contact service timed out')),12000);
      pending.set(tag,r=>finish(resolve,r));s.onerror=()=>finish(reject,Error('Contact service unavailable'));s.src=u.href;s.referrerPolicy='no-referrer';
      document.head.append(s);
    });
  }
  async function loadChallenge(){
    if(sending)return;
    const local=++generation;current=null;send.disabled=true;ans.value='';ans.setCustomValidity('');picture.hidden=true;
    hint.textContent='Loading the verification…';change.textContent=mode==='image'?'Use a text question':'Use an image';
    try {const next=await query({op:'challenge',mode});if(local!==generation)return;
      if(!next.id||!next.receipt||!next.question)throw Error('No challenge');
      current=next;hint.textContent=next.question;
      if(next.image){picture.src=next.image;picture.hidden=false;}send.disabled=false;
    } catch {if(local===generation)hint.textContent='Verification could not load. Try a new challenge or email Erfan directly.';}
  }
  const start=()=>{if(!seen){seen=true;loadChallenge();}};
  form.hidden=false;
  const observer=new IntersectionObserver(rows=>{if(rows.some(r=>r.isIntersecting)){start();observer.disconnect();}},{rootMargin:'160px'});observer.observe(form);
  form.addEventListener('focusin',start,{once:true});
  refresh.onclick=()=>{status.textContent='';loadChallenge();};change.onclick=()=>{status.textContent='';mode=mode==='image'?'text':'image';loadChallenge();};
  let outstanding=null;
  const again=document.createElement('button');again.type='button';again.className='retry-attempt';again.hidden=true;again.textContent='Edit and start a new attempt';status.after(again);
  const freeze=on=>{for(const k of ['email','phone','title','message','answer'])form.elements[k].readOnly=on;refresh.disabled=on;change.disabled=on;};
  again.onclick=async()=>{outstanding=null;again.hidden=true;freeze(false);send.textContent='Send message ↗';status.textContent='Your text was kept. The earlier delivery is unconfirmed; a new send may duplicate it.';await loadChallenge();ans.focus();};
  async function poll(receipt){
    for(let i=0;i<8;i++){
      if(i)await new Promise(r=>setTimeout(r,Math.min(700+i*220,1700)));
      const {state}=await query({op:'status',receipt});
      if(state&&state!=='pending')return state;
    }
    return 'unknown';
  }
  form.addEventListener('submit',async e=>{
    e.preventDefault();if(sending||!current||!form.reportValidity())return;
    const token=current;const d=new FormData(form);
    for(const n of ['email','title','message']){if(!String(d.get(n)||'').trim()){form.elements[n].setCustomValidity('Please complete this field.');form.elements[n].reportValidity();return;}}
    if(d.get('phone')&&!/^[+() .0-9x#-]+$/i.test(d.get('phone'))){form.elements.phone.setCustomValidity('Use a phone number with digits and an optional country code.');form.elements.phone.reportValidity();return;}
    sending=true;send.disabled=true;freeze(true);again.hidden=true;status.textContent=outstanding?'Checking delivery…':'Sending your message…';
    let state;
    try{
      if(!outstanding){
        const body=new URLSearchParams(); for(const n of ['email','phone','title','message','answer','_gotcha'])body.set(n,String(d.get(n)||'').trim());
        body.set('id',token.id);body.set('receipt',token.receipt);outstanding=token.receipt;
        await fetch(endpoint,{method:'POST',mode:'no-cors',credentials:'omit',referrerPolicy:'no-referrer',body,signal:AbortSignal.timeout(14000)});
      }
      state=await poll(outstanding);
    }catch{state='unknown';}
    finally{sending=false;}
    if(state==='unknown'){status.textContent='Delivery could not be confirmed. Your text is preserved. Check the delivery status, or explicitly start a new attempt.';send.textContent='Check delivery status';send.disabled=false;again.hidden=false;return;}
    outstanding=null;freeze(false);send.textContent='Send message ↗';
    if(state==='sent'){form.reset();status.textContent='Message sent to Erfan. Thank you for getting in touch.';await loadChallenge();}
    else if(state==='expired'){status.textContent='This receipt expired, so delivery cannot be confirmed. Your text is preserved. Only send again if you are prepared for a possible duplicate.';await loadChallenge();ans.focus();}
    else{status.textContent=allowedStates[state]||allowedStates.unavailable;await loadChallenge();ans.focus();}
  });
  form.addEventListener('input',e=>e.target.setCustomValidity?.(''));
})();
