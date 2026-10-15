# Nexum ad concepts

Two campaigns, 10 concepts each, in Meta/Google sizes 1080x1080 (1x1), 1080x1350 (4x5) and 1080x1920 (9x16, story-safe).

| Concept | Campaign | Landing page |
|---|---|---|
| G1 rate pill | General | `/` |
| G2 1 lender vs 40+ | General | `/` |
| G3 machine lineup | General | `/` |
| Y1 December calendar | Year-end | `/section-179/` |
| Y2 path to Dec 31 | Year-end | `/section-179/` |
| Y3 Section 179 hook | Year-end | `/section-179/` |
| G4 haul truck (Unsplash) | General | `/` |
| G5 semi (Unsplash) | General | `/` |
| G6 dozer, keep your cash (Unsplash) | General | `/` |
| Y4 cranes at dusk (Unsplash) | Year-end | `/section-179/` |
| Y5 fleet trucks (Unsplash) | Year-end | `/section-179/` |
| G7 built for contractors | General | `/` |
| G8 turned down by your bank? | General | `/` |
| G9 trucks, trailers, lowboys | General | `/` |
| G10 financing in three steps | General | `/` |
| Y6 buy it in 2026, put it to work in 2026 | Year-end | `/section-179/` |
| Y7 hauling more next year (Unsplash) | Year-end | `/section-179/` |
| Y8 Section 179 has a deadline (Unsplash) | Year-end | `/section-179/` |
| Y9 year-end checklist (Unsplash) | Year-end | `/section-179/` |
| Y10 lineup, fund it before Dec 31 | Year-end | `/section-179/` |

G1 shows "Rates from 6.99%". Do not run it until a lender program in writing backs that rate for the
stated buyer profile. The disclosure on the ad must match that program.

Rebuild: `python3 src/build_ads.py`, then render with `src/render.mjs` (Playwright; serve the repo over
http and pass `ADS_URL` so Montserrat loads). Output lands in `out/`. This folder is excluded from the
public site by `.vercelignore`.

Unsplash photos (`src/u-*.jpg`) were picked by the owner from free-licence results. Brand badges,
licence plates and windshields are blurred. They came in as ~870 px screenshots and were upscaled 2x;
replace them with the full-size Unsplash downloads (same filenames) before running paid traffic.

No ad uses customer reviews or testimonials.
