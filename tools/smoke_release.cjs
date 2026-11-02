// Exercise the website a visitor receives at a domain root and a Pages subpath.
const fs = require('node:fs'), path = require('node:path'), http = require('node:http');
const crypto = require('node:crypto');
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const chrome=process.env.CHROME_BIN || (process.platform==='win32'&&fs.existsSync('C:/Program Files/Google/Chrome/Application/chrome.exe')?'C:/Program Files/Google/Chrome/Application/chrome.exe':undefined);
const root = path.resolve(__dirname,'..'), site = path.resolve(process.argv[2] || path.join(root,'site'));
const out = path.resolve(process.argv[3] || path.join(require('node:os').tmpdir(),'erfanpj-portfolio-smoke'));
fs.mkdirSync(out,{recursive:true});
const types = {'.html':'text/html','.css':'text/css','.js':'text/javascript','.pdf':'application/pdf','.svg':'image/svg+xml','.png':'image/png','.jpg':'image/jpeg','.webp':'image/webp','.woff2':'font/woff2','.ttf':'font/ttf','.txt':'text/plain','.xml':'text/xml'};
const server = http.createServer((req,res)=>{
  const u = new URL(req.url,'http://127.0.0.1'); let n = decodeURIComponent(u.pathname).replace(/^\/portfolio(?=\/)/,'').replace(/^\//,'');
  if(!n||n.endsWith('/')) n+='index.html'; const file=path.resolve(site,n);
  if(!file.startsWith(site+path.sep)||!fs.existsSync(file)||!fs.statSync(file).isFile()){res.writeHead(404);res.end();return;}
  res.writeHead(200,{'content-type':types[path.extname(file)]||'application/octet-stream'});fs.createReadStream(file).pipe(res);
});
const checks=[], errors=[], observations=[];
const check=(scenario,name,passed,detail='')=>{checks.push({scenario,name,passed:!!passed,detail});};
const demos = ['brain-signals-lab/viewer/','opsdesk-ai/','reachboard-showcase/','recall-studio/','commonnest-showcase/'];
let browser;
(async()=>{
 await new Promise(r=>server.listen(0,'127.0.0.1',r)); const origin='http://127.0.0.1:'+server.address().port;
 browser=await chromium.launch({headless:true,executablePath:chrome,args:['--disable-extensions','--no-first-run']});
 for(const base of ['/portfolio/','/']) for(const width of [320,375,768,1024,1100,1440]) {
   const scenario=base+' @ '+width, phone=width<=1024; const page=await browser.newPage({viewport:{width,height:width<500?844:900},locale:'en-US',reducedMotion:'no-preference'});
   page.setDefaultTimeout(5000); page.setDefaultNavigationTimeout(25000); page.on('pageerror',e=>errors.push(scenario+' '+e)); page.on('response',r=>{if(r.url().startsWith(origin)&&r.status()>=400)errors.push(scenario+' '+r.status()+' '+r.url())});
   const response=await page.goto(origin+base,{waitUntil:'load'});await page.evaluate(()=>document.fonts.ready);
   const obs=await page.evaluate(()=>{
     const box=e=>e.getBoundingClientRect(), seen=e=>box(e).width>0&&box(e).height>0;
     const anchors=[...document.querySelectorAll('a[href^="#"]')];
     return {width:innerWidth,scrollWidth:document.documentElement.scrollWidth,visibleH1:[...document.querySelectorAll('h1')].filter(seen).map(h=>h.textContent),
       missingImages:[...document.images].filter(e=>!e.complete||!e.naturalWidth).map(e=>e.getAttribute('src')),
       missingAnchors:anchors.filter(e=>!document.getElementById(decodeURIComponent(e.hash.slice(1)))).map(e=>e.hash),
       links:[...document.links].map(a=>a.href), externalRequests:performance.getEntriesByType('resource').map(e=>e.name).filter(s=>/^https?:/.test(s)&&!s.startsWith(location.origin)),
       body:document.body.innerText, dt:document.title,desc:document.querySelector('meta[name=description]')?.content,
       fontStatus:document.fonts.check('16px "Familjen Grotesk"')&&document.fonts.check('16px "DM Sans"')};
   });
   check(scenario,'page and metadata',response.status()===200&&obs.dt.includes('Erfan')&&!!obs.desc);
   check(scenario,'reflow and one visible primary heading',obs.width===obs.scrollWidth&&obs.visibleH1.length===1,JSON.stringify([obs.width,obs.scrollWidth,obs.visibleH1]));
   check(scenario,'real local images, fonts and anchors',!obs.missingImages.length&&!obs.missingAnchors.length&&obs.fontStatus,JSON.stringify([obs.missingImages,obs.missingAnchors]));
   check(scenario,'no third-party runtime requests',!obs.externalRequests.length,obs.externalRequests.join(','));
   check(scenario,'five demos + contact',demos.every(x=>obs.links.includes('https://erfanpj.github.io/'+x))&&obs.links.includes('mailto:erfanpj@gmail.com')&&obs.links.includes('https://www.linkedin.com/in/erfan-pirjahandideh'));
   check(scenario,'measured results and dated log',['61.8%','50.4%','57.8%','Recall Studio','Commonnest','Fraunhofer'].every(x=>obs.body.includes(x))&&!/\[date\]|\{\{/.test(obs.body));
   const href=obs.links.find(x=>x.endsWith('/Erfan-Pirjahandideh-CV.pdf'));const pdf=href&&await page.request.get(href);
   const digest=pdf&&crypto.createHash('sha256').update(await pdf.body()).digest('hex');
   check(scenario,'verified original PDF served at deployment base',href===origin+base+'Erfan-Pirjahandideh-CV.pdf'&&pdf?.status()===200&&pdf.headers()['content-type']==='application/pdf'&&digest==='37a3a324b1b7cf1d545e28cc161d64aa242a71b31548afc44b438d50539cf814',digest);
   const play=page.locator('#hero-play:visible,#mobile-hero-play:visible').first();
   const motionCount=await page.evaluate(()=>document.getAnimations().filter(a=>a.playState==='running'&&a.effect?.target?.getBoundingClientRect().width>0).length);
   check(scenario,'scene animates before pause',motionCount>0,String(motionCount));
   if(await play.count()) {await play.focus();await page.keyboard.press('Enter');check(scenario,'motion keyboard toggle',/play|resume|replay/i.test(await play.innerText()));}
   else check(scenario,'motion keyboard toggle',false,'no control');
   if(base==='/portfolio/') {await page.evaluate(()=>window.scrollTo(0,0));await page.screenshot({path:path.join(out,'hero-'+width+'.png')});if(width===375||width===1440)await page.screenshot({path:path.join(out,'page-'+width+'.png'),fullPage:true});}
   const cases=page.locator('a.case,button.case');check(scenario,'three case studies',await cases.count()===3);
   for(let i=0;i<await cases.count();i++){
     const trigger=cases.nth(i);await trigger.focus();await page.keyboard.press('Enter');const dialog=page.locator('dialog[open]');
     if(!await dialog.count()){check(scenario,'open case '+i,false);continue;}
     const links=await dialog.locator('a').evaluateAll(a=>a.map(x=>x.href)); const copy=await dialog.innerText();
     check(scenario,'case '+i+' evidence, source, demo and limit',/limit|boundary|what this shows/i.test(copy)&&links.some(x=>x.startsWith('https://github.com/erfanpj/'))&&links.some(x=>x.startsWith('https://erfanpj.github.io/')));
     if(base==='/portfolio/'&&width===375&&i===0)await page.screenshot({path:path.join(out,'case-phone.png')});
     let stays=true;for(let k=0;k<5;k++){await page.keyboard.press('Tab');if(!await dialog.evaluate(e=>e.contains(document.activeElement)))stays=false;}
     check(scenario,'case '+i+' keyboard stays in dialog',stays);
     await page.keyboard.press('Escape');check(scenario,'case '+i+' Escape and focus restoration',!(await dialog.count())&&await trigger.evaluate(e=>e===document.activeElement));
   }
   if(phone){
     const menu=page.locator('#menu-toggle');await menu.focus();await page.keyboard.press('Enter');const sheet=page.locator('#mobile-nav');
     let escapeTab=false;for(let q=0;q<13;q++){await page.keyboard.press('Tab');if(!await sheet.evaluate(e=>e.contains(document.activeElement))){escapeTab=true;break;}}
     check(scenario,'menu opens and contains keyboard focus',await menu.getAttribute('aria-expanded')==='true'&&!escapeTab);
     await page.keyboard.press('Escape');check(scenario,'menu Escape restores focus',await menu.getAttribute('aria-expanded')==='false'&&await menu.evaluate(e=>e===document.activeElement));
     await menu.click();await sheet.locator('a[href="#contact"]').click();check(scenario,'menu Contact resolves',page.url().endsWith('#contact')&&await menu.getAttribute('aria-expanded')==='false');
     const steps=await page.locator('.mobileStepGrid li').all();check(scenario,'six accessible mobile stages',steps.length===6);
     const motifs=page.locator('.mobileChem button');check(scenario,'four phone illustration controls',await motifs.count()===4);
     if(await motifs.count()){const first=motifs.first();await first.focus();await page.keyboard.press('Space');check(scenario,'Space operates motif',await first.getAttribute('aria-expanded')==='true'||await first.getAttribute('aria-pressed')==='true');await page.keyboard.press('Escape');check(scenario,'Escape closes motif',await first.getAttribute('aria-expanded')!=='true'&&await first.getAttribute('aria-pressed')!=='true');}
     const crops=await page.locator('#mobile-hero [src*="portrait-scene"],#mobile-hero [src*="neuron-scene"]').count();
     check(scenario,'phone illustration drawn as one shared scene',crops===0,String(crops)+' prototype screenshot layers');
   }else{
     await page.evaluate(()=>scrollTo({top:0,behavior:'instant'}));
     const eyebrow=await page.locator('#hero-scene div.top p').first().evaluate(e=>e.getBoundingClientRect().top);
     const mast=await page.locator('.masthead').evaluate(e=>e.getBoundingClientRect().bottom);
     check(scenario,'masthead clears hero copy',eyebrow>=mast,JSON.stringify([eyebrow,mast]));
     const motif=page.locator('.hor2:visible').first();await motif.focus();await page.keyboard.press('Space');check(scenario,'desktop motif keyboard disclosure',await motif.getAttribute('aria-expanded')==='true');await page.keyboard.press('Escape');check(scenario,'desktop motif Escape',await motif.getAttribute('aria-expanded')==='false');
     const navContact=page.locator('a[href="#contact"]:visible').first();if(await navContact.count()){await navContact.scrollIntoViewIfNeeded();const hit=await navContact.evaluate(e=>{const b=e.getBoundingClientRect(),h=document.elementFromPoint(b.x+b.width/2,b.y+b.height/2);return [e.contains(h),h?.textContent?.slice(0,48)]});check(scenario,'desktop Contact target unobstructed',hit[0],String(hit[1]));}
   }
   await page.emulateMedia({reducedMotion:'reduce'});await page.reload(); await page.evaluate(()=>document.fonts.ready);
   const moving=await page.evaluate(()=>document.getAnimations().filter(a=>a.playState==='running'&&Number(a.effect?.getComputedTiming().activeDuration)>100).length);
   check(scenario,'reduced motion produces a static scene',moving===0,String(moving));
   observations.push({scenario,base,width,images:obs.missingImages,externalRequests:obs.externalRequests});await page.close();
 }
})().catch(e=>{errors.push(String(e.stack||e));}).finally(async()=>{
 await browser?.close();server.close();fs.writeFileSync(path.join(out,'results.json'),JSON.stringify({checks,errors,observations},null,2));
 const fails=checks.filter(c=>!c.passed);console.log(JSON.stringify({total:checks.length,failed:fails.length,failures:[...new Set(fails.map(x=>x.name+': '+x.detail))],errors},null,2));if(fails.length||errors.length)process.exitCode=1;
});
