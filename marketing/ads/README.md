# Nexum ad concepts

Two campaigns, three concepts each, in Meta/Google sizes 1080x1080 (1x1), 1080x1350 (4x5) and 1080x1920 (9x16, story-safe).

| Concept | Campaign | Landing page |
|---|---|---|
| G1 rate pill | General | `/` |
| G2 1 lender vs 40+ | General | `/` |
| G3 machine lineup | General | `/` |
| Y1 December calendar | Year-end | `/section-179/` |
| Y2 path to Dec 31 | Year-end | `/section-179/` |
| Y3 Section 179 hook | Year-end | `/section-179/` |

G1 shows "Rates from 6.99%". Do not run it until a lender program in writing backs that rate for the
stated buyer profile. The disclosure on the ad must match that program.

Rebuild: `python3 src/build_ads.py`, then render with `src/render.mjs` (Playwright; serve the repo over
http and pass `ADS_URL` so Montserrat loads). Output lands in `out/`. This folder is excluded from the
public site by `.vercelignore`.
