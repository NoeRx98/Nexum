# Nexum ad concepts

One campaign for 2026: general ads that send people to the homepage. 14 concepts in Meta/Google sizes
1080x1080 (1x1), 1080x1350 (4x5) and 1080x1920 (9x16, story-safe).

| Concept | Landing page |
|---|---|
| G1 rate pill | `/` |
| G2 matched first, then sent (precision) | `/` |
| G3 machine lineup | `/` |
| G4 haul truck (Unsplash) | `/` |
| G5 semi (Unsplash) | `/` |
| G6 dozer, keep your cash (Unsplash) | `/` |
| G7 built for contractors | `/` |
| G8 turned down by your bank? | `/` |
| G9 trucks, trailers, lowboys | `/` |
| G10 financing in three steps | `/` |
| G11 stop renting, start owning | `/?ad=stop-renting` |
| G12 $0 down for qualified buyers | `/?ad=zero-down` |
| G13 won the bid? get the machine | `/?ad=won-the-bid` |
| G14 found it at auction? we can finance it | `/?ad=private-sale` |

G1 shows "Rates from 6.99%". Do not run it until a lender program in writing backs that rate for the
stated buyer profile. The disclosure on the ad must match that program.

Rebuild: `python3 src/build_ads.py`, then render with `src/render.mjs` (Playwright; serve the repo over
http and pass `ADS_URL` so Montserrat loads). Output lands in `out/`. This folder is excluded from the
public site by `.vercelignore`.

Unsplash photos (`src/u-*.jpg`) were picked by the owner from free-licence results. Brand badges,
licence plates and windshields are blurred. They came in as ~870 px screenshots and were upscaled 2x;
replace them with the full-size Unsplash downloads (same filenames) before running paid traffic.

No ad uses customer reviews or testimonials.

Wording rule: never quote a lender count ("40+ lenders") or say we "shop" a deal. Nexum matches the
deal first and sends the file only to lenders that fit.

The year-end campaign (Y1-Y10) is off for 2026 and its renders were removed; the code stays in
`src/build_ads.py` for next year, and its copy must be rewritten to the wording rule before reuse.

Situation ads (G11-G14) link to the homepage with `?ad=<key>`. The homepage swaps its headline to match
the ad before first paint; unknown or missing keys show the normal headline. Add the usual UTM tags
after it, e.g. `https://nexumcf.com/?ad=zero-down&utm_source=facebook&utm_campaign=general&utm_content=g12`.
The full URL reaches GHL in `landing_page`, so each lead shows which situation ad it came from.
