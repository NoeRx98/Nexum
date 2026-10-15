# GHL field mapping for Nexum lead forms

The homepage form posts JSON to `/api/lead`, which relays it to the GHL inbound webhook (`GHL_WEBHOOK_URL`).
GHL keeps only the fields the workflow maps; anything unmapped is dropped without an error.

Create each new field under **Settings → Custom Fields** as single-line text, then map it in the
workflow's **Create/Update Contact** action as `{{inboundWebhookRequest.<field>}}`. New keys appear
in the trigger only after GHL receives a request containing them: submit one test lead, then use
**Fetch sample request** on the Inbound Webhook trigger.

## Sent by the form

The form shows shorter chip labels (for example `$20K+`), but the value sent is the full original
text (`$20K+ / month`). The year-end page (`/section-179/`) was taken down for 2026 and redirects to
the homepage; it can be restored from git history next year.

| Field | Values / example | Notes |
|---|---|---|
| `funnel` | `Nexum Commercial Finance` | Unchanged on every form, so existing triggers and filters keep working |
| `lead_page` | `main` | Which page sent the lead (only `main` while the year-end page is off) |
| `language` | `en`, `es` | **New.** `es` = came from the Spanish page (`/es/`). Route these to the Spanish-speaking advisor and send Spanish texts |
| `first_name`, `last_name`, `full_name`, `email`, `phone` | | Standard contact fields |
| `years_in_business` | `1 year+` … `10 years+` | |
| `monthly_revenue` | `$5K+ / month` … `$20K+ / month` | |
| `credit_score` | `Under 600` … `750+` | |
| `equipment_needed` | `Commercial equipment financing`, `Business line of credit` | Unchanged from the original form |
| `sms_consent` | `yes` / `no` | **Only text contacts where this is `yes`** |
| `sms_consent_text` | exact opt-in wording, empty when `no` | Proof of what the person agreed to |
| `submitted_at` | `10/14/26, 4:01:47 PM CT` | Central time |
| `source_url` | full URL of the page | |
| `utm_source`, `utm_medium`, `utm_campaign`, `utm_term`, `utm_content` | from the ad link | First touch for the visit |
| `gclid`, `gbraid`, `wbraid` | Google Ads click IDs | Needed for offline conversion import |
| `fbclid` | Meta click ID | |
| `msclkid` | Microsoft Ads click ID | |
| `landing_page`, `referrer` | URLs | |
| `client_ip`, `relayed_at` | added by the relay | |

## Texting rules

1. After Create/Update Contact, add **If/Else: `sms_consent` equals `yes`**. Only the yes branch may send SMS.
   For no or empty, use email and a call task, and set SMS DND on the contact.
2. Do not send any SMS until A2P 10DLC registration is approved (Settings → Phone Numbers → Trust Center).
   Registration needs the privacy policy URL (with a section saying phone numbers and SMS consent are not
   shared or sold for marketing), the opt-in wording above, and the page URLs where it appears.
3. The Spanish page (`/es/`) shows a Spanish opt-in, and `sms_consent_text` carries that Spanish text.
   Add the Spanish wording and the `/es/` URL to the A2P registration before texting Spanish leads.
4. If the opt-in wording changes, change it in `index.html` (`#smsText`) and in the Spanish build and update the A2P registration to match.
