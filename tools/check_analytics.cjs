// Serve the local site at its production origin in an isolated browser.
// Even with --real-tag, analytics collections are captured locally.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
let playwright;
try { playwright = require(process.env.PLAYWRIGHT_MODULE || 'playwright'); }
catch { playwright = require('C:/Users/user/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright'); }

const site = path.resolve(__dirname, '../site');
const realTag = process.argv.includes('--real-tag');
const origin = 'https://erfanpj.com';
const id = 'G-WHZYD0QJF8';
const marker = 'private-test-483';
const mime = {'.html':'text/html','.js':'application/javascript','.css':'text/css','.svg':'image/svg+xml','.png':'image/png','.woff2':'font/woff2','.ttf':'font/ttf'};
const gaHosts = /(^|\.)(google-analytics\.com|googletagmanager\.com|doubleclick\.net|analytics\.google\.com)$/;
const commands = (page, name) => page.evaluate(n=>(window.dataLayer || []).filter(c=>c[0]===n).map(c=>Array.from(c)),name);

(async () => {
  const executablePath = process.env.CHROME_BIN || (process.platform==='win32' ? 'C:/Program Files/Google/Chrome/Application/chrome.exe' : undefined);
  const browser = await playwright.chromium.launch({executablePath});
  const context = await browser.newContext({viewport:{width:375,height:667}});
  const traffic = [];
  const errors = [];
  context.on('page', p=>p.on('pageerror', e=>errors.push(e.message)));
  try {
    await context.route('**/*', async route => {
      const request=route.request(), url=new URL(request.url());
      if (url.origin===origin) {
        if (url.pathname==='/contact-config.js') return route.fulfill({contentType:mime['.js'],body:'window.EPJ_CONTACT_ENDPOINT="https://erfanpj.com/test-contact";'});
        if (url.pathname==='/test-contact') return route.fulfill({contentType:mime['.js'],body:'EPJ_contact('+JSON.stringify({tag:url.searchParams.get('tag'),result:{question:'Test challenge',id:'a'.repeat(32),receipt:'b'.repeat(32)}})+');'});
        const file=path.resolve(site,'.'+(url.pathname==='/'?'/index.html':url.pathname));
        if (!file.startsWith(site+path.sep) || !fs.existsSync(file)) return route.fulfill({status:404,body:''});
        return route.fulfill({path:file,contentType:mime[path.extname(file)]||'application/octet-stream'});
      }
      if (gaHosts.test(url.hostname)) {
        traffic.push([request.url(),request.postData()||'',request.headers().referer||'']);
        if (url.hostname==='www.googletagmanager.com' && ['/gtag/js','/gtag/destination'].includes(url.pathname))
          return realTag ? route.continue() : route.fulfill({contentType:mime['.js'],body:'/* offline tag load fixture */'});
        return route.fulfill({status:204});
      }
      return route.abort();
    });
    const page=await context.newPage();
    const url=origin+'/?email='+marker+'%40example.invalid#'+marker;
    await page.goto(url,{referer:'https://referrer.example/private?name='+marker});
    await page.locator('#analytics-privacy').waitFor();
    assert.equal(traffic.length,0);
    assert(!(await context.cookies()).some(c=>c.name.startsWith('_ga')));
    await page.getByRole('button',{name:'Decline analytics'}).click();
    await page.reload();
    assert.equal(traffic.length,0);
    assert(!(await page.locator('#analytics-privacy').isVisible()));
    await page.getByRole('button',{name:'Privacy & analytics'}).click();
    assert.equal(await page.locator('#analytics-status').innerText(),'Analytics is off.');
    await page.getByRole('button',{name:'Allow analytics'}).click();
    await page.waitForFunction(()=>(window.dataLayer||[]).some(c=>c[0]==='event'&&c[1]==='page_view'));
    assert(traffic.some(([u])=>new URL(u).searchParams.get('id')===id));
    const config=(await commands(page,'config'))[0][2];
    assert.equal(config.page_location,origin+'/');
    assert.equal(config.send_page_view,false);
    assert.equal(config.allow_google_signals,false);
    assert.equal(config.allow_ad_personalization_signals,false);
    assert(!config.page_referrer.includes(marker));

    await page.locator('#contact-form [name=email]').fill(marker+'@example.invalid');
    await page.locator('#contact-form [name=message]').fill(marker+' contact text');
    await page.evaluate(()=>document.addEventListener('click',e=>{if(e.target.closest('a.cvbtn, a.project-thumb'))e.preventDefault();}));
    await page.locator('a.cvbtn').click();
    await page.locator('a.case').first().click();
    await page.keyboard.press('Escape');
    const events=await commands(page,'event');
    assert.deepEqual(events.map(c=>c[1]),['page_view','file_download','select_content']);
    assert.equal(events[2][2].item_id,'brain-signals-lab');
    assert(!JSON.stringify(events).includes(marker));
    if (realTag) {
      const timeout=Date.now()+24000;
      while (Date.now()<timeout && !traffic.some(r=>r.join('&').includes('en=select_content')))
        await new Promise(resolve=>setTimeout(resolve,250));
      for (const name of ['page_view','file_download','select_content'])
        assert(traffic.some(r=>r.join('&').includes('en='+name)),'Missing outbound event '+name);
      assert((await context.cookies()).some(c=>c.name==='_ga'),'The actual tag did not set the consented cookie');
    } else {
      await context.addCookies(['_ga','_ga_'+id.slice(2)].map(name=>({name,value:'fixture',domain:'erfanpj.com',path:'/'})));
    }

    const other=await context.newPage();
    await other.goto(origin);
    await other.waitForFunction(()=>(window.dataLayer||[]).some(c=>c[0]==='event'&&c[1]==='page_view'));
    await page.getByRole('button',{name:'Privacy & analytics'}).click();
    await page.getByRole('button',{name:'Decline analytics'}).click();
    await other.waitForFunction(tag=>window['ga-disable-'+tag]===true,id);
    assert(!(await context.cookies()).some(c=>c.name==='_ga'||c.name==='_ga_'+id.slice(2)));
    assert.equal(await page.locator('#contact-form [name=message]').inputValue(),marker+' contact text');
    const before=(await commands(page,'event')).length;
    await page.locator('a.cvbtn').click();
    assert.equal((await commands(page,'event')).length,before);
    const afterDecline=traffic.length;
    await page.reload();
    assert.equal(traffic.length,afterDecline,'Reloading after decline contacted Analytics');
    assert(!JSON.stringify(traffic).includes(marker),'A private URL or form value escaped into an Analytics request');
    assert.equal(errors.length,0,errors.join('\n'));
    console.log('PASS: opt-in, decline, remembered choice, stripped URLs, three allowed events, form privacy, cookie cleanup and cross-tab withdrawal. '+(realTag?'Google tag requests intercepted; no test data submitted.':'Offline fixture.'));
  } finally { await browser.close(); }
})().catch(e=>{console.error(e);process.exitCode=1;});
