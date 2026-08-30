# Nexum Commercial Finance

Landing page for the Nexum Commercial Finance lead funnel. Plain static site, no build step. Leads are relayed through a serverless function so the GHL webhook URL is never exposed in the browser.

## Deploy to Netlify

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

The form posts to `/api/lead` on this site, which runs `netlify/edge-functions/lead.mjs`. That function validates the submission, rate-limits spam, and forwards it as JSON to `GHL_WEBHOOK_URL`. If delivery fails, it retries twice and then alerts `ALERT_WEBHOOK_URL` if set.

## Files

- `index.html` — the page
- `support.js` — rendering runtime, do not edit
- `netlify/edge-functions/lead.mjs` — the lead relay
- `netlify.toml` — host config, allows the page to load inside GHL's iframe
- `config.js` — unused legacy file, safe to delete

## Known follow-ups

- Vehicle/equipment dropdowns are static lists — no external API calls to worry about here.
