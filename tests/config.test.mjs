// Static checks: every file the pages point to exists, generated pages match their build scripts,
// and the deploy config (headers, redirects, ignore list, sitemap) is what launch depends on.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { ROOT } from './helpers/server.mjs';

const read = f => fs.readFileSync(path.join(ROOT, f), 'utf8');
const PAGES = ['index.html', 'es/index.html'];

test('every local file referenced by the pages exists (including lazy and fallback images)', () => {
  const missing = [];
  for (const p of PAGES) {
    const html = read(p);
    const refs = new Set();
    for (const m of html.matchAll(/\b(?:src|href|data-src|poster)="(\/[^"#?]*)"/g)) refs.add(m[1]);
    for (const m of html.matchAll(/\b(?:srcset|data-srcset|imagesrcset)="([^"]+)"/g))
      for (const part of m[1].split(',')) { const u = part.trim().split(/\s+/)[0]; if (u.startsWith('/')) refs.add(u); }
    for (const m of html.matchAll(/url\((?:'|")?(\/[^)'"]+)/g)) refs.add(m[1]);
    for (const r of refs) {
      if (r === '/' || r.startsWith('/api/') || r.startsWith('//')) continue;
      const f = path.join(ROOT, r.endsWith('/') ? r + 'index.html' : r);
      if (!fs.existsSync(f)) missing.push(`${p}: ${r}`);
    }
  }
  assert.deepEqual(missing, []);
});

test('index.html and es/index.html match their build scripts (nobody hand-edited a generated page)', () => {
  const before = PAGES.map(read);
  try {
    execFileSync('python3', ['tools/site-build/build.py'], { cwd: ROOT, stdio: 'pipe' });
    const es = execFileSync('python3', ['tools/site-build/build_es.py'], { cwd: ROOT, stdio: 'pipe' }).toString();
    assert.match(es, /missing: \[\]/, 'Spanish build could not find some English strings to translate:\n' + es);
    PAGES.forEach((p, i) => assert.ok(read(p) === before[i], `${p} differs from what tools/site-build produces; edit the scripts, then rebuild`));
  } finally {
    PAGES.forEach((p, i) => fs.writeFileSync(path.join(ROOT, p), before[i]));
  }
});

test('vercel.json: security headers, cache rules and the temporary year-end redirect', () => {
  const v = JSON.parse(read('vercel.json'));
  const all = v.headers.find(h => h.source === '/(.*)').headers;
  const h = Object.fromEntries(all.map(x => [x.key.toLowerCase(), x.value]));
  assert.equal(h['x-frame-options'], 'SAMEORIGIN');
  assert.match(h['content-security-policy'], /frame-ancestors 'self'/);
  assert.equal(h['x-content-type-options'], 'nosniff');
  assert.ok(h['referrer-policy']);
  assert.ok(v.headers.some(x => x.source === '/uploads/(.*)'));
  const r = v.redirects.find(x => x.source === '/section-179');
  assert.ok(r && r.destination === '/' && r.permanent === false, 'year-end redirect must stay temporary');
});

test('.vercelignore keeps private folders off the public site', () => {
  const ignored = read('.vercelignore').split('\n').map(s => s.trim());
  for (const f of ['tools', 'tests', 'marketing', 'docs', '.github']) assert.ok(ignored.includes(f), `${f} is not in .vercelignore`);
});

test('sitemap, canonical and hreflang agree for both languages', () => {
  const sm = read('sitemap.xml');
  for (const u of ['https://nexumcf.com/', 'https://nexumcf.com/es/']) assert.ok(sm.includes(`<loc>${u}</loc>`), `${u} missing from sitemap`);
  const en = read('index.html'), es = read('es/index.html');
  assert.match(en, /<link rel="canonical" href="https:\/\/nexumcf\.com\/">/);
  assert.match(es, /<link rel="canonical" href="https:\/\/nexumcf\.com\/es\/">/);
  for (const page of [en, es]) {
    assert.match(page, /hreflang="en" href="https:\/\/nexumcf\.com\/"/);
    assert.match(page, /hreflang="es" href="https:\/\/nexumcf\.com\/es\/"/);
  }
});

test('the relay copies for Vercel and Netlify keep the same timing rules', () => {
  const v = read('api/lead.js'), n = read('netlify/edge-functions/lead.mjs');
  for (const src of [v, n]) {
    assert.match(src, /ms = 8000/);
    assert.match(src, /\[400, 1200\]/);
    assert.match(src, /"timeout"/);
  }
  for (const page of PAGES) assert.match(read(page), /ctrl\.abort\(\)\},20000\)/, `${page}: browser must wait 20 s for the relay`);
});
