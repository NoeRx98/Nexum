// The lead relay (api/lead.js) against a fake GHL: delivery, retries, duplicates, spam and config errors.
import { test, before, after } from 'node:test';
import assert from 'node:assert/strict';
import path from 'node:path';
import { ROOT, startFakeGHL } from './helpers/server.mjs';

let ghl, handler, n = 0;
const lead = (extra = {}) => ({ funnel: 'Nexum Commercial Finance', first_name: 'Ana', last_name: 'Lopez', full_name: 'Ana Lopez',
  email: 'ana@example.com', phone: '2145550100', language: 'es', _gotcha: '', ...extra });
const post = (body, ip = `192.0.2.${++n}`) => handler(new Request('http://localhost/api/lead', {
  method: 'POST', headers: { 'content-type': 'application/json', 'x-forwarded-for': ip, host: 'localhost' },
  body: typeof body === 'string' ? body : JSON.stringify(body) }));

before(async () => {
  ghl = await startFakeGHL();
  process.env.GHL_WEBHOOK_URL = ghl.url;
  delete process.env.ALERT_WEBHOOK_URL;
  ({ default: handler } = await import(path.join(ROOT, 'api/lead.js')));
});
after(() => ghl.close());

test('GHL up: delivered once, with relay fields added and the honeypot stripped', async () => {
  ghl.reset('ok');
  const res = await post(lead());
  assert.equal(res.status, 200);
  assert.deepEqual(await res.json(), { ok: true });
  assert.equal(ghl.state.hits, 1);
  const got = ghl.state.bodies[0];
  assert.equal(got.email, 'ana@example.com');
  assert.equal(got.language, 'es');
  assert.ok(!('_gotcha' in got), '_gotcha must not reach GHL');
  assert.match(got.client_ip, /^192\.0\.2\./);
  assert.ok(!Number.isNaN(Date.parse(got.relayed_at)));
});

test('GHL down: three quick attempts, then 502 so the page asks the customer to retry', async () => {
  ghl.reset('down');
  const t = Date.now();
  const res = await post(lead());
  assert.equal(res.status, 502);
  assert.equal(ghl.state.hits, 3);
  assert.ok(Date.now() - t < 5000, 'failures should be reported fast');
});

test('GHL slow: sent once (no duplicates), customer sees success, finishes under the page\'s 20 s wait', async () => {
  ghl.reset('slow');
  const t = Date.now();
  const res = await post(lead());
  const ms = Date.now() - t;
  assert.equal(res.status, 200);
  assert.equal((await res.json()).unconfirmed, true);
  assert.equal(ghl.state.hits, 1, 'a timeout must not be retried');
  assert.ok(ms < 20000, `took ${ms} ms`);
});

test('spam is dropped quietly and never reaches GHL', async () => {
  ghl.reset('ok');
  for (const bad of [lead({ _gotcha: 'bot' }), lead({ email: 'not-an-email' }), lead({ phone: '12345' }), lead({ full_name: '', first_name: 'A' })]) {
    const res = await post(bad);
    assert.equal(res.status, 200);
    assert.equal((await res.json()).filtered, true);
  }
  assert.equal(ghl.state.hits, 0);
});

test('rate limit: the 6th submission in 10 minutes from one IP is dropped', async () => {
  ghl.reset('ok');
  const ip = '198.51.100.7';
  for (let i = 0; i < 5; i++) assert.equal((await post(lead(), ip)).status, 200);
  const sixth = await post(lead(), ip);
  assert.equal((await sixth.json()).filtered, true);
  assert.equal(ghl.state.hits, 5);
});

test('bad requests: GET is 405, broken JSON is 400', async () => {
  assert.equal((await handler(new Request('http://localhost/api/lead'))).status, 405);
  assert.equal((await post('{not json')).status, 400);
});

test('missing GHL_WEBHOOK_URL is a loud 500, not a silent success', async () => {
  const keep = process.env.GHL_WEBHOOK_URL;
  delete process.env.GHL_WEBHOOK_URL;
  try { assert.equal((await post(lead())).status, 500); }
  finally { process.env.GHL_WEBHOOK_URL = keep; }
});
