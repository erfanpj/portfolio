// ErfanPJ contact-only web app. Client GETs carry only opaque random IDs; never visitor data.
// Deploy as the owner, accessible to anyone. The only mail destination is fixed below.
const DESTINATION = 'erfanpj@gmail.com';
const DIGITS = {2:['111','001','111','100','111'],3:['111','001','111','001','111'],4:['101','101','111','001','001'],5:['111','100','111','001','111'],6:['111','100','111','101','111'],7:['111','001','001','010','010'],8:['111','101','111','101','111'],9:['111','101','111','001','111']};
const MINUTE=60, TTL=10*MINUTE;
const random=(low,high)=>low+Math.floor(Math.random()*(high-low+1));
const key=()=>Utilities.getUuid().replace(/-/g,'');
const validKey=v=>typeof v==='string'&&/^[a-f0-9]{32}$/.test(v);
const fingerprint=value=>Utilities.base64EncodeWebSafe(Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256,value,Utilities.Charset.UTF_8)).slice(0,36);
function art(answer) {
  let marks='';
  [...answer].forEach((n,i)=>{let dot=4,dy=random(6,13),dx=12+i*26+random(-2,2);
    DIGITS[n].forEach((row,y)=>[...row].forEach((v,x)=>{if(v==='1')marks+='M'+(dx+x*dot)+' '+(dy+y*dot)+'h4v4h-4z';}));});
  let svg='<svg xmlns="http://www.w3.org/2000/svg" width="154" height="43" viewBox="0 0 154 43"><rect width="154" height="43" fill="#f5f1ea"/><path d="M0 30Q49 4 94 28T154 16 M4 13Q65 37 151 9" stroke="#c8bab2" fill="none"/><path fill="#242026" d="'+marks+'"/></svg>';
  return 'data:image/svg+xml;base64,'+Utilities.base64Encode(svg);
}
function issue(mode) {
  const c=CacheService.getScriptCache(), uuid=key(), receipt=key();
  const text=mode==='text'; let answer, question, image;
  if(text){const a=random(3,14), b=random(2,12), op=random(0,1);
    answer=String(op ? a+b : Math.max(a,b)-Math.min(a,b));
    question=op?'What is '+a+' plus '+b+'?':'What is '+Math.max(a,b)+' minus '+Math.min(a,b)+'?';
  }else{answer=Array.from({length:5},()=>String(random(2,9))).join(''); image=art(answer); question='Enter the five digits in the image.';}
  c.put('challenge:'+uuid,JSON.stringify({answer:fingerprint(uuid+':'+answer),issued:Date.now(),receipt}),TTL);
  c.put('receipt:'+receipt,'pending',TTL);
  return {id:uuid,receipt,question,image:image||null};
}
function doGet(e) {
  const p=(e&&e.parameter)||{}, tag=String(p.tag||'');
  if(!/^[a-f0-9]{16}$/.test(tag)) return ContentService.createTextOutput('Portfolio contact service.');
  let response={error:'Unsupported request.'};
  if(p.op==='challenge') response=issue(p.mode);
  if(p.op==='status'&&validKey(p.receipt)) response={state:CacheService.getScriptCache().get('receipt:'+p.receipt)||'expired'};
  const json=JSON.stringify({tag,result:response}).replace(/</g,'\\u003c');
  return ContentService.createTextOutput('EPJ_contact('+json+');').setMimeType(ContentService.MimeType.JAVASCRIPT);
}
function checkFields(p) {
  const email=String(p.email||'').trim(),phone=String(p.phone||'').trim(),title=String(p.title||'').trim(),message=String(p.message||'').trim();
  if(!/^[^\s@<>]+@[^\s@<>]+\.[^\s@<>]+$/.test(email)||email.length>254||/[\r\n]/.test(email))return null;
  if(phone.length>40||(phone&&!/^[+()\- .0-9x#]+$/i.test(phone)))return null;
  if(title.length<1||title.length>120||/[\r\n]/.test(title)||message.length<1||message.length>4000)return null;
  return {email,phone,title,message};
}
function submit(p) {
  if(!validKey(p.id)||!validKey(p.receipt))return;
  const cache=CacheService.getScriptCache(), lock=LockService.getScriptLock();
  if(!lock.tryLock(7000))return;
  try{
    const json=cache.get('challenge:'+p.id);if(!json)return;
    const ch=JSON.parse(json); if(ch.receipt!==p.receipt)return;
    const receiptKey='receipt:'+ch.receipt, done=s=>cache.put(receiptKey,s,TTL);
    cache.remove('challenge:'+p.id); // consumed even if the answer was incorrect
    if(p._gotcha||Date.now()-ch.issued<1500||Date.now()-ch.issued>TTL*1000||ch.answer!==fingerprint(p.id+':'+String(p.answer||'').trim())){done('verification');return;}
    const f=checkFields(p);if(!f){done('invalid');return;}
    const stamp=Utilities.formatDate(new Date(),'UTC','yyyyMMddHH');
    const day=stamp.slice(0,8), sender='sender:'+fingerprint(f.email.toLowerCase())+':'+stamp;
    const props=PropertiesService.getScriptProperties(), budget=JSON.parse(props.getProperty('dailyBudget')||'{}');
    const dayCount=budget.day===day?Number(budget.count)||0:0;
    if(Number(cache.get(sender)||0)>=3||dayCount>=30||MailApp.getRemainingDailyQuota()<2){done('limited');return;}
    try {MailApp.sendEmail({to:DESTINATION,replyTo:f.email,name:'ErfanPJ portfolio',
      subject:'Portfolio contact: '+f.title,body:'Reply email: '+f.email+'\nPhone: '+(f.phone||'Not supplied')+'\n\n'+f.message});}
    catch(_){done('unavailable');return;}
    done('sent');
    cache.put(sender,String(Number(cache.get(sender)||0)+1),3600);
    props.setProperty('dailyBudget',JSON.stringify({day,count:dayCount+1}));
  }finally{lock.releaseLock();}
}
function doPost(e) {
  if(e&&Number(e.contentLength||0)<24000) submit(e.parameter||{});
  return ContentService.createTextOutput('Submitted for processing. Check the receipt on the portfolio.');
}
