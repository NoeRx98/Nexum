// Page quality on / and /es/: errors, broken links/images, accessibility basics, layout on
// small phones, leftover English on the Spanish page, and speed budgets on a throttled phone.
import { test, before, after } from 'node:test';
import assert from 'node:assert/strict';
import { chromium } from 'playwright';
import { startSite } from './helpers/server.mjs';

const PAGES = ['/', '/es/'];
const BUDGET = { lcpMs: 2500, cls: 0.1, sameOriginKB: 500 };
let site, browser;
before(async () => { site = await startSite(); browser = await chromium.launch(); });
after(async () => { await browser?.close(); await site?.close(); });

for (const path of PAGES) {
  for (const width of [360, 390, 1440]) {
    test(`${path} at ${width}px: no errors, nothing broken, nothing off-screen`, async () => {
      const ctx = await browser.newContext({ viewport: { width, height: 800 }, isMobile: width < 500 });
      const page = await ctx.newPage();
      const problems = [];
      page.on('pageerror', e => problems.push('script error: ' + e.message));
      page.on('console', m => { if (m.type() === 'error') problems.push('console: ' + m.text()); });
      page.on('response', r => { if (r.status() >= 400 && r.url().startsWith(site.url)) problems.push(`${r.status()} ${r.url()}`); });
      await page.goto(site.url + path, { waitUntil: 'networkidle' });
      // scroll the whole page so lazy images load
      await page.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 500) { scrollTo(0, y); await new Promise(r => setTimeout(r, 40)); } scrollTo(0, 0); });
      await page.waitForTimeout(800);
      const r = await page.evaluate(() => {
        const ids = new Set([...document.querySelectorAll('[id]')].map(e => e.id));
        const vis = el => { const s = getComputedStyle(el); return s.display !== 'none' && s.visibility !== 'hidden'; };
        return {
          overflowX: document.documentElement.scrollWidth - innerWidth,
          deadAnchors: [...document.querySelectorAll('a[href^="#"]')].map(a => a.getAttribute('href')).filter(h => h.length > 1 && !ids.has(h.slice(1))),
          brokenImages: [...document.images].filter(i => i.complete && i.currentSrc && i.naturalWidth === 0).map(i => i.currentSrc),
          imagesWithoutAlt: [...document.images].filter(i => !i.hasAttribute('alt')).length,
          unlabeledFields: [...document.querySelectorAll('input:not([type=hidden]),select,textarea')]
            .filter(el => !el.closest('[aria-hidden=true]') && !(el.labels && el.labels.length) && !el.getAttribute('aria-label')).map(e => e.id || e.name),
          duplicateIds: [...document.querySelectorAll('[id]')].map(e => e.id).filter((v, i, a) => a.indexOf(v) !== i),
          h1: document.querySelectorAll('h1').length,
          badJsonLd: [...document.querySelectorAll('script[type="application/ld+json"]')].filter(s => { try { JSON.parse(s.textContent); return false; } catch { return true; } }).length,
          clippedText: [...document.querySelectorAll('body *')].filter(el => el.children.length === 0 && el.textContent.trim() && vis(el)
            && getComputedStyle(el).overflow !== 'visible' && el.scrollWidth > el.clientWidth + 1).map(el => el.textContent.trim().slice(0, 40))
        };
      });
      await ctx.close();
      assert.deepEqual(problems, []);
      assert.ok(r.overflowX <= 0, `page scrolls sideways by ${r.overflowX}px`);
      assert.deepEqual(r.deadAnchors, [], 'links to sections that do not exist');
      assert.deepEqual(r.brokenImages, []);
      assert.equal(r.imagesWithoutAlt, 0);
      assert.deepEqual(r.unlabeledFields, []);
      assert.deepEqual(r.duplicateIds, []);
      assert.equal(r.h1, 1, 'exactly one h1');
      assert.equal(r.badJsonLd, 0);
      assert.deepEqual(r.clippedText, [], 'text cut off inside its box');
    });
  }

  test(`${path}: speed on a throttled mid-range phone (LCP < ${BUDGET.lcpMs} ms, CLS < ${BUDGET.cls}, < ${BUDGET.sameOriginKB} KB)`, async () => {
    const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, deviceScaleFactor: 2 });
    const page = await ctx.newPage();
    const cdp = await ctx.newCDPSession(page);
    await cdp.send('Emulation.setCPUThrottlingRate', { rate: 4 });
    await cdp.send('Network.enable');
    await cdp.send('Network.emulateNetworkConditions', { offline: false, latency: 150, downloadThroughput: 1.6 * 1024 * 1024 / 8, uploadThroughput: 750 * 1024 / 8 });
    await page.addInitScript(() => {
      window.__lcp = 0; window.__cls = 0;
      new PerformanceObserver(l => { for (const e of l.getEntries()) window.__lcp = e.startTime; }).observe({ type: 'largest-contentful-paint', buffered: true });
      new PerformanceObserver(l => { for (const e of l.getEntries()) if (!e.hadRecentInput) window.__cls += e.value; }).observe({ type: 'layout-shift', buffered: true });
    });
    let bytes = 0;
    page.on('requestfinished', async rq => { if (rq.url().startsWith(site.url)) { try { const s = await rq.sizes(); bytes += s.responseBodySize; } catch {} } });
    await page.goto(site.url + path, { waitUntil: 'load' });
    await page.waitForTimeout(3000);
    const { lcp, cls } = await page.evaluate(() => ({ lcp: window.__lcp, cls: window.__cls }));
    await ctx.close();
    assert.ok(lcp > 0 && lcp < BUDGET.lcpMs, `LCP ${Math.round(lcp)} ms`);
    assert.ok(cls < BUDGET.cls, `CLS ${cls.toFixed(3)}`);
    assert.ok(bytes / 1024 < BUDGET.sameOriginKB, `downloaded ${Math.round(bytes / 1024)} KB from the site`);
  });
}

test('/es/: no English left in visible text, labels or messages', async () => {
  const page = await browser.newPage();
  await page.goto(site.url + '/es/');
  const leftovers = await page.evaluate(() => {
    const english = /\b(the|your|you|and|with|our|we|apply|see my|request|business line|equipment financing|step \d)\b/i;
    const ok = /Nexum Commercial Finance|Dallas-Fort Worth|STOP|HELP|English/g;
    const out = [];
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    while (walker.nextNode()) {
      const n = walker.currentNode, t = n.textContent.trim();
      if (!t || n.parentElement.closest('script,style,[hidden]')) continue;
      if (english.test(t.replace(ok, ''))) out.push(t.slice(0, 60));
    }
    for (const el of document.querySelectorAll('[aria-label],[alt],[placeholder],[data-name]'))
      for (const a of ['aria-label', 'alt', 'placeholder', 'data-name']) { const v = el.getAttribute(a); if (v && english.test(v.replace(ok, ''))) out.push(`${a}="${v}"`); }
    return out;
  });
  await page.close();
  assert.deepEqual(leftovers, []);
});

test('the old year-end page redirects home, and the language switch links both ways', async () => {
  const page = await browser.newPage();
  const res = await page.goto(site.url + '/section-179/');
  assert.equal(new URL(res.url()).pathname, '/');
  assert.equal(await page.getAttribute('a.lang', 'href'), '/es/');
  await page.goto(site.url + '/es/');
  assert.equal(await page.getAttribute('a.lang', 'href'), '/');
  assert.equal(await page.getAttribute('html', 'lang'), 'es');
  await page.close();
});
