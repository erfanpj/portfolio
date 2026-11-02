// Exercise the deployed Apps Script handlers without a live mailbox.
const fs=require('node:fs'),vm=require('node:vm'),crypto=require('node:crypto'),assert=require('node:assert/strict'),path=require('node:path');
const entries=new Map(),props=new Map(),mail=[];let now=Date.now(),quota=99;
const cache={put:(k,v,t)=>entries.set(k,{v,end:now+t*1000}),get:k=>{let item=entries.get(k);return item&&item.end>=now?item.v:null;},remove:k=>entries.delete(k)};
const U={getUuid:()=>crypto.randomUUID(),base64Encode:s=>Buffer.from(s).toString('base64'),base64EncodeWebSafe:b=>Buffer.from(b).toString('base64url'),computeDigest:(_,s)=>crypto.createHash('sha256').update(s).digest(),DigestAlgorithm:{SHA_256:1},Charset:{UTF_8:1},formatDate:()=>new Date(now).toISOString().slice(0,13).replace(/[-T]/g,'')};
class Clock extends Date{constructor(...a){super(...(a.length?a:[now]));}static now(){return now;}}
const ctx=vm.createContext({Utilities:U,CacheService:{getScriptCache:()=>cache},PropertiesService:{getScriptProperties:()=>({getProperty:k=>props.get(k),setProperty:(k,v)=>props.set(k,v)})},LockService:{getScriptLock:()=>({tryLock:()=>true,releaseLock(){}})},MailApp:{getRemainingDailyQuota:()=>quota,sendEmail:v=>mail.push(v)},ContentService:{createTextOutput:s=>({body:s,setMimeType(){return this;}}),MimeType:{JAVASCRIPT:1}},Date:Clock});
vm.runInContext(fs.readFileSync(path.resolve(__dirname,'../contact/Code.gs'),'utf8'),ctx);
const get=(op,more={})=>JSON.parse(ctx.doGet({parameter:{op,tag:'a'.repeat(16),...more}}).body.replace(/^EPJ_contact\(/,'').replace(/\);$/,'')).result;
const init=()=>{const c=get('challenge',{mode:'text'});const n=c.question.match(/\d+/g).map(Number);return {id:c.id,receipt:c.receipt,answer:String(c.question.includes('plus')?n[0]+n[1]:n[0]-n[1]),email:'sender@example.org',phone:'+49 555 0100',title:'Testing',message:'Synthetic local test.'};};
const send=p=>ctx.doPost({contentLength:450,parameter:p});const state=p=>get('status',{receipt:p.receipt}).state;const ready=()=>{const p=init();now+=2500;return p;};
const im=get('challenge',{mode:'image'});assert.match(im.image,/^data:image\/svg\+xml;base64,/);assert.equal(im.id.length,32);assert(!im.question.match(/\d{5}/));assert(!('answer'in im));
let p=ready();send(p);assert.equal(state(p),'sent');assert.equal(mail.length,1);assert.equal(mail[0].to,'erfanpj@gmail.com');assert.equal(mail[0].replyTo,'sender@example.org');assert(mail[0].body.includes(p.phone));
send(p);assert.equal(mail.length,1); // replay
p=ready();p.answer='incorrect';send(p);assert.equal(state(p),'verification');
p=init();send(p);assert.equal(state(p),'verification'); // too fast
p=ready();p._gotcha='robot';send(p);assert.equal(state(p),'verification');
p=ready();p.email='x@example.com\nBcc:wrong@example.com';send(p);assert.equal(state(p),'invalid');
p=ready();p.phone='';p.title='';send(p);assert.equal(state(p),'invalid');
p=ready();p.phone='';send(p);assert.equal(state(p),'sent'); // optional phone
p=ready();send(p);assert.equal(state(p),'sent');p=ready();send(p);assert.equal(state(p),'limited');
p=ready();p.email='other@example.org';quota=0;send(p);assert.equal(state(p),'limited');quota=99;
p=ready();now+=610000;send(p);assert.equal(state(p),'expired');
assert.equal(ctx.doGet({parameter:{tag:'alert(1)'}}).body,'Portfolio contact service.');
assert.equal(mail.length,3);console.log('PASS: fixed recipient, valid receipt, optional phone, validation, visual/text challenges, one-time use, expiry, bot check, per-address limit, quota and no callback injection.');
