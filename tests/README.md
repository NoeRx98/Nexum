# Site tests

Run before every merge (GitHub runs them on every push; a red check means do not merge):

    cd tests && npm ci && npx playwright install chromium && npm test

| File | What it proves |
|---|---|
| `form.test.mjs` | A real browser fills the English and Spanish forms; the lead goes through the real `/api/lead` relay to a fake GHL, and the test checks every value GHL receives (exact option values, `language`, consent text matches the screen, UTM and click IDs, no unexpected keys). Also: unchecked consent, bad email, GHL down. |
| `relay.test.mjs` | `api/lead.js`: delivers once, retries only real failures, never duplicates on a slow GHL, drops spam and over-limit submissions, fails loudly when `GHL_WEBHOOK_URL` is missing. |
| `pages.test.mjs` | `/` and `/es/` at 360, 390 and 1440 px: no script errors, broken links, broken images, missing labels, sideways scrolling or cut-off text; no English left on `/es/`; speed on a throttled phone (LCP < 2.5 s, CLS < 0.1, < 500 KB). |
| `config.test.mjs` | Every file the pages reference exists; the pages match `tools/site-build`; security headers, the temporary year-end redirect, the deploy ignore list, sitemap and hreflang. |
| `live/smoke.mjs` | Runs daily and after each deploy against nexumcf.com (`.github/workflows/live-check.yml`). Confirms the webhook is configured with a bot-flagged probe that the relay drops before GHL, so no lead is ever sent. |

When a test fails, read its message first: each one says what broke in plain words.
