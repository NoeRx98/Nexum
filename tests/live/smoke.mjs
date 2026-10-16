// Daily check of the LIVE site. Never sends a real lead to GHL.
// Usage: node live/smoke.mjs [https://nexumcf.com]
const BASE = (process.argv[2] || process.env.SITE_URL || 'https://nexumcf.com').replace(/\/$/, '');
const fails = [], notes = [];
const check = (ok, msg) => { (ok ? notes : fails).push((ok ? 'ok   ' : 'FAIL ') + msg); };

async function page(path, lang) {
  const t = Date.now();
  const res = await fetch(BASE + path, { redirect: 'follow' });
  const ms = Date.now() - t, html = await res.text();
  check(res.status === 200, `${path} returns 200 (got ${res.status}) in ${ms} ms`);
  check(ms < 3000, `${path} responds in under 3 s`);
  check(html.includes(`<html lang="${lang}"`), `${path} is the ${lang} page`);
  check(html.includes('id="form"') && html.includes('fetch("/api/lead"'), `${path} has the lead form wired to /api/lead`);
  check(html.includes('ctrl.abort()},20000)'), `${path} is the current build (20 s form wait)`);
  const h = res.headers;
  check(h.get('x-frame-options') === 'SAMEORIGIN' && (h.get('content-security-policy') || '').includes("frame-ancestors 'self'"), `${path} sends anti-framing headers`);
  check(!(h.get('x-robots-tag') || '').includes('noindex'), `${path} can be indexed by Google`);
}

await page('/', 'en');
await page('/es/', 'es');

const redir = await fetch(BASE + '/section-179/', { redirect: 'follow' });
check(new URL(redir.url).pathname === '/', `/section-179/ redirects home (ended at ${new URL(redir.url).pathname})`);

const get = await fetch(BASE + '/api/lead');
check(get.status === 405, `lead relay is up (GET returns 405, got ${get.status})`);

// A bot-flagged submission: the relay checks GHL_WEBHOOK_URL first (500 if missing), then drops
// the lead as spam before contacting GHL. So 200 + filtered proves the webhook is configured.
const probe = await fetch(BASE + '/api/lead', { method: 'POST', headers: { 'content-type': 'application/json' },
  body: JSON.stringify({ _gotcha: 'uptime-check', full_name: 'Uptime Check', email: 'uptime@example.com', phone: '0000000000' }) });
const pj = await probe.json().catch(() => ({}));
check(probe.status === 200 && pj.filtered === true, `GHL webhook is configured on the live site (status ${probe.status}${pj.reason ? ', ' + pj.reason : ''})`);

const sm = await fetch(BASE + '/sitemap.xml');
check(sm.status === 200 && (await sm.text()).includes('/es/'), 'sitemap lists the Spanish page');

for (const p of ['/tools/site-build/build.py', '/marketing/ads/README.md', '/tests/package.json'])
  check((await fetch(BASE + p)).status === 404, `${p} is not public`);

console.log(`Live check of ${BASE}\n` + [...fails, ...notes].join('\n'));
if (fails.length) { console.error(`\n${fails.length} problem(s) on the live site.`); process.exit(1); }
