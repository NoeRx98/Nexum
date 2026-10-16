// The lead form, end to end in a real browser: page -> /api/lead relay -> fake GHL.
// Checks exactly what GHL receives from the English and Spanish pages.
import { test, before, after } from 'node:test';
import assert from 'node:assert/strict';
import { chromium } from 'playwright';
import { startSite, startFakeGHL } from './helpers/server.mjs';

let site, ghl, browser;
before(async () => {
  ghl = await startFakeGHL();
  process.env.GHL_WEBHOOK_URL = ghl.url;
  site = await startSite();
  browser = await chromium.launch();
});
after(async () => { await browser?.close(); await site?.close(); await ghl?.close(); });

// The exact values GHL workflows are built on. Changing any of these breaks the client's automations.
const NEEDS = ['Commercial equipment financing', 'Business line of credit'];
const ALLOWED_KEYS = new Set(['funnel', 'lead_page', 'language', 'first_name', 'last_name', 'full_name', 'email', 'phone',
  'years_in_business', 'monthly_revenue', 'credit_score', 'equipment_needed', 'sms_consent', 'sms_consent_text',
  'submitted_at', 'source_url', 'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content',
  'gclid', 'gbraid', 'wbraid', 'fbclid', 'msclkid', 'landing_page', 'referrer', 'client_ip', 'relayed_at']);

async function fillForm(page, { need, sms = true, email = 'ana@example.com' }) {
  await page.locator(`label.nc:has(input[value="${need}"])`).click();
  for (const [name, value] of [['years', '3 years+'], ['revenue', '$20K+ / month'], ['credit', '650+']]) {
    await page.locator(`label:has(input[name="${name}"][value="${value}"])`).click();
  }
  // answering all three on step 2 moves on by itself; press Continue only if it did not
  const step3 = page.locator('.step[data-step="3"]');
  try { await step3.waitFor({ state: 'visible', timeout: 2000 }); }
  catch { await page.locator('.step[data-step="2"] [data-next]').click(); await step3.waitFor({ state: 'visible' }); }
  await page.fill('#first', 'Ana'); await page.fill('#last', 'Lopez');
  await page.fill('#email', email); await page.fill('#phone', '(214) 555-0100');
  if (sms) await page.locator('label.consent').click();
}

for (const [path, lang, doneText] of [['/', 'en', 'Request received, Ana.'], ['/es/', 'es', 'Solicitud recibida, Ana.']]) {
  for (const need of NEEDS) {
    test(`${lang}: "${need}" reaches GHL with the exact values`, async () => {
      ghl.reset('ok');
      const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
      await page.goto(`${site.url}${path}?utm_source=facebook&utm_campaign=general&utm_content=g12-zero-down&fbclid=TEST123`);
      await fillForm(page, { need });
      const consentShown = (await page.locator('#smsText').textContent()).trim();
      await page.click('#submit');
      await page.locator('#doneH').waitFor({ state: 'visible' });
      assert.equal((await page.locator('#doneH').textContent()).trim(), doneText);

      assert.equal(ghl.state.hits, 1, 'exactly one delivery');
      const got = ghl.state.bodies[0];
      assert.deepEqual(
        { funnel: got.funnel, lead_page: got.lead_page, language: got.language, equipment_needed: got.equipment_needed,
          years_in_business: got.years_in_business, monthly_revenue: got.monthly_revenue, credit_score: got.credit_score,
          first_name: got.first_name, last_name: got.last_name, full_name: got.full_name, email: got.email, sms_consent: got.sms_consent },
        { funnel: 'Nexum Commercial Finance', lead_page: 'main', language: lang, equipment_needed: need,
          years_in_business: '3 years+', monthly_revenue: '$20K+ / month', credit_score: '650+',
          first_name: 'Ana', last_name: 'Lopez', full_name: 'Ana Lopez', email: 'ana@example.com', sms_consent: 'yes' });
      assert.equal(got.phone.replace(/\D/g, ''), '2145550100');
      assert.equal(got.sms_consent_text, consentShown, 'the consent record must match the words shown on screen');
      assert.equal(got.utm_source, 'facebook'); assert.equal(got.utm_content, 'g12-zero-down'); assert.equal(got.fbclid, 'TEST123');
      assert.match(got.source_url, new RegExp(`${path.replace(/\//g, '\\/')}\\?`));
      assert.match(got.submitted_at, /CT$/);
      const unknown = Object.keys(got).filter(k => !ALLOWED_KEYS.has(k));
      assert.deepEqual(unknown, [], `unexpected keys sent to GHL: ${unknown}`);
      await page.close();
    });
  }
}

test('texting box left unchecked: consent is "no" and no consent text is recorded', async () => {
  ghl.reset('ok');
  const page = await browser.newPage();
  await page.goto(site.url + '/');
  assert.equal(await page.locator('#sms').isChecked(), false, 'consent must be unchecked by default');
  await fillForm(page, { need: NEEDS[0], sms: false });
  await page.click('#submit');
  await page.locator('#doneH').waitFor({ state: 'visible' });
  assert.equal(ghl.state.bodies[0].sms_consent, 'no');
  assert.equal(ghl.state.bodies[0].sms_consent_text, '');
  await page.close();
});

test('a bad email is caught on the page and nothing is sent', async () => {
  ghl.reset('ok');
  const page = await browser.newPage();
  await page.goto(site.url + '/');
  await fillForm(page, { need: NEEDS[0], email: 'ana@nowhere' });
  await page.click('#submit');
  await page.locator('#err3').waitFor({ state: 'visible' });
  await page.waitForTimeout(300);
  assert.equal(ghl.state.hits, 0);
  await page.close();
});

for (const [path, word] of [['/', 'try again'], ['/es/', 'intente otra vez']]) {
  test(`${path}: when GHL is down the customer is told to retry and keeps their answers`, async () => {
    ghl.reset('down');
    const page = await browser.newPage();
    await page.goto(site.url + path);
    await fillForm(page, { need: NEEDS[1] });
    await page.click('#submit');
    await page.locator('#err3').waitFor({ state: 'visible', timeout: 15000 });
    assert.match((await page.locator('#err3').textContent()), new RegExp(word));
    assert.equal(await page.locator('#submit').isEnabled(), true);
    assert.equal(await page.inputValue('#email'), 'ana@example.com');
    await page.close();
  });
}

test('English and Spanish forms offer the identical set of values', async () => {
  const values = async path => {
    const page = await browser.newPage();
    await page.goto(site.url + path);
    const v = await page.$$eval('#form input[type=radio]', els => els.map(e => `${e.name}=${e.value}`).sort());
    await page.close();
    return v;
  };
  assert.deepEqual(await values('/es/'), await values('/'));
});
