# Nexum Commercial Finance

Landing page for the Nexum Commercial Finance lead funnel. Plain static site, no build step. Leads are relayed through a serverless function so the GHL webhook URL is never exposed in the browser.

## Migrating to Vercel (in progress)

This site is moving from Netlify to Vercel. Both hosting configs exist side by side right now:

- `netlify/edge-functions/lead.mjs` + `netlify.toml` — the current **live** setup on Netlify, untouched.
- `api/lead.js` + `vercel.json` — the **new** Vercel equivalent, same logic and same env var names, ready to deploy but not yet live anywhere.

## Deploy to Vercel

1. Push these files to this repository.
2. vercel.com -> Add New Project -> import this repo.
3. Framework preset: **Other**. Leave build command empty, output directory empty (Vercel serves the static files from the repo root and auto-detects `api/lead.js` as a serverless function — no config needed beyond `vercel.json`, which is already in the repo).
4. Deploy. You get a permanent URL like `nexum-commercial-finance.vercel.app`.
5. Set the same three environment variables as below in Project Settings > Environment Variables.

Every future push to this repo redeploys automatically.

Once you've verified leads arrive correctly through the Vercel URL and pointed `nexumcf.com` at Vercel instead of Netlify, the old `netlify/edge-functions/lead.mjs`, `netlify.toml`, and the Netlify site itself can be retired.

## Deploy to Netlify (current live setup)

1. Push these files to this repository.
2. netlify.com -> Add new site -> Import an existing project -> pick this repo.
3. Leave build command empty. Publish directory: `.`
4. Deploy. You get a permanent URL like `nexum-commercial-finance.netlify.app`.

Every future push to this repo redeploys automatically.

## Required environment variables

Site configuration > Environment variables:

- `GHL_WEBHOOK_URL` (required) — Nexum's GHL inbound webhook
- `ALERT_WEBHOOK_URL` (optional) — your own GHL workflow, notified if delivery fails
- `CLIENT_NAME` (optional) — shows up in the alert email, e.g. "Nexum"

## Embedding in GHL

Add a Code element to a blank GHL funnel step:

```html
<iframe src="https://YOUR-SITE.netlify.app" style="width:100%;height:100vh;border:0" title="Nexum Commercial Finance"></iframe>
```

## Where the leads go

The form posts to `/api/lead` on this site. On Netlify that path is served by `netlify/edge-functions/lead.mjs`; on Vercel it's served by `api/lead.js` (Vercel's zero-config convention: anything in `/api` becomes a function at that path automatically). Either way, the function validates the submission, rate-limits spam, and forwards it as JSON to `GHL_WEBHOOK_URL`. If delivery fails, it retries twice and then alerts `ALERT_WEBHOOK_URL` if set.

## Files

- `index.html` — the page
- `support.js` — rendering runtime, do not edit
- `api/lead.js` — the lead relay, Vercel version (new)
- `vercel.json` — Vercel host config, allows the page to load inside GHL's iframe (new)
- `netlify/edge-functions/lead.mjs` — the lead relay, Netlify version (current live setup)
- `netlify.toml` — Netlify host config (current live setup)
- `config.js` — unused legacy file, safe to delete

## Known follow-ups

- Vehicle/equipment dropdowns are static lists — no external API calls to worry about here.
