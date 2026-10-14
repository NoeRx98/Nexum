# GHL field mapping for Nexum lead forms

Both forms post JSON to `/api/lead`, which relays it to the GHL inbound webhook (`GHL_WEBHOOK_URL`).
GHL keeps only the fields the workflow maps; anything unmapped is dropped without an error.

Create each new field under **Settings → Custom Fields** as single-line text, then map it in the
workflow's **Create/Update Contact** action as `{{inboundWebhookRequest.<field>}}`. New keys appear
in the trigger only after GHL receives a request containing them: submit one test lead, then use
**Fetch sample request** on the Inbound Webhook trigger.

## Sent by both forms

| Field | Values / example | Notes |
|---|---|---|
| `funnel` | `Nexum Commercial Finance` (main page), `Nexum Year-End Equipment (Section 179 page)` | Which page sent the lead; use it to tag or route |
| `first_name`, `last_name`, `full_name`, `email`, `phone` | | Standard contact fields |
| `years_in_business` | `1 year+` … `10 years+` | |
| `monthly_revenue` | `$5K+ / month` … `$20K+ / month` | |
| `credit_score` | `Under 600` … `750+` | |
| `equipment_needed` | `Commercial equipment financing`, `Business line of credit` | Year-end page always sends equipment financing |
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

## Sent by the year-end page only (`/section-179/`)

| Field | Values |
|---|---|
| `equipment_type` | `Excavator`, `Dozer`, `Wheel loader`, `Dump truck`, `Truck & trailer`, `Other equipment` |
| `equipment_condition` | `New`, `Used` |
| `equipment_price_range` | `Under $50,000`, `$50,000 – $150,000`, `$150,000 – $500,000`, `$500,000 – $1M`, `Over $1M` |

## Texting rules

1. After Create/Update Contact, add **If/Else: `sms_consent` equals `yes`**. Only the yes branch may send SMS.
   For no or empty, use email and a call task, and set SMS DND on the contact.
2. Do not send any SMS until A2P 10DLC registration is approved (Settings → Phone Numbers → Trust Center).
   Registration needs the privacy policy URL (with a section saying phone numbers and SMS consent are not
   shared or sold for marketing), the opt-in wording above, and the page URLs where it appears.
3. If the opt-in wording changes, change it in both `index.html` (`SMS_TEXT`) and `section-179/index.html`
   (`#smsText`) and update the A2P registration to match.
