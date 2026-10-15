# Motion Plan: Nexum /section-179/

```
MOTION PLAN — Nexum Commercial Finance, year-end page
Tier: 2 (industry default 1 for finance; +1 because the owner asked for creative motion
      and the page sells a visual, physical product; paid mobile traffic keeps it CSS-only)
Signature moment: the hero "night shift" scene. The photo slowly pushes in, the excavator
      cab lights breathe, a work-light pool sweeps the ground, dust drifts in the light, and
      the crane's red warning lights blink. It says "we work while you work" without a word.
Per section:
  hero      signature scene (CSS only, behind the overlay, out of the headline's path);
            pointer parallax on desktop only; countdown digits roll once on load
  form      tier 1: the equipment card plays through the five machines ONCE, the line-of-credit
            card plays draw / repay / draw again ONCE, then both sit still (replay on hover,
            desktop). Step changes slide 300 ms. Chips pop on tap. Nothing loops in the form.
  proof, broker, timeline, FAQ, final   static
Libraries: CSS + ~2 KB inline JS. No animation library.
Budgets: eager motion JS 0 KB; LCP ≤ 2.5 s; CLS ≤ 0.1; TBT ≤ 200 ms (390×844, 4× CPU, slow 4G)
Reduced motion: no push-in, parallax, sweep, dust or blinking (lights stay lit, still);
      form cards show their first frame; steps swap instantly.
Battery: hero animations pause when the hero is off screen.
Waivers: none
```

## Homepage (`/`)

Same plan as the year-end page, plus the year-end panel in the hero: the countdown digits roll
into place once on load, the tax-year bar fills to today's position once, and the minutes update
in place every 15 seconds (no looping motion). The panel hides itself after December 31.
Reduced motion: digits and bar render at their final values with no movement.
