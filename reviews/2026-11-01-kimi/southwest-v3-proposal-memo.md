# Southwest Anchor Elicitation — v3 Proposal Memo (2026-11-01)

**Status: PROPOSAL ONLY.** V28 and Domestic Release Pricing v2 remain locked. The
locked wrapper continues to reject `southwest`. Nothing here modifies any packet
input, lock, model, workbook, or ZIP. This memo records an elicitation conducted
in chat after the peer review closed, and its analysis. It is not part of the
accepted review verdict and changes no finding in `reviews/2026-11-01-kimi.md`.

## 1. Protocol

Two-pin elicitation preregistered in chat before answers were given; protocol
SHA-256 `a4caac25064138dacb8c6a5318df8b146318d4a4195921bdd0d5a80ac69bcc70`.
Frozen decision rule for shape transfer: SW amber 30/115 answer compared to
pin 1 × 0.563077 (the locked factor); deviation ≤10% supports transfer, >20%
questions it, between is inconclusive. Two further tail pins were then requested
and given. Basis word ("established offering" vs "rough sense") was requested
for every pin.

Single informant (the packet author). All answers: **"rough sense"** — the
lowest evidential tier. Two answers were given as ceilings and are recorded as
bounds, not points. One independent unit of observation throughout.

## 2. Pins (verbatim)

| # | Profile | Answer (verbatim) | Form | Basis |
|---|---|---|---|---|
| 1 | SW pale/straw 20 yr 110 lb | "1100-1200" | range | rough sense |
| 2 | SW amber 30 yr 115 lb | "950-1050" | range | rough sense |
| 3 | SW amber 35 yr 120 lb | "320 max" | ceiling (bound) | rough sense |
| 4 | SW brown 40 yr 130 lb | "no more than 300" | ceiling (bound) | rough sense |

Informant's stated rationale (verbatim): "Southwest, because it consists of the
beach cities, commands a high premium, and the 20/110 harvest are among the most
sought after in the entire domestic area."

## 3. Findings

### 3.1 Level — resolved to a point: A_SW = $1,100

Pin 1 gives A_SW ∈ [$1,100, $1,200]. Pin 4 (brown 40/130 ≤ $300) coincides with
the locked curve's prediction at A_SW = $1,100 **to the dollar** (locked range at
A ∈ [1100, 1200]: $300.00–$327.27). Intersection pins the anchor at exactly
**$1,100 — NE-equal**, consistent with the informant's beach-premium rationale.
This replaces (as a proposal) the retired v1 `model_inferred` value 1050.002,
which the review already bars from use.

### 3.2 Shape — locked transfer falsified twice, in opposite directions

| Stretch | Informant-implied ratio | Locked ratio | Verdict |
|---|---|---|---|
| 20/110 → amber 30/115 | 0.79–0.95 | 0.5631 | much flatter |
| amber 30/115 → amber 35/120 | ≤ 0.30–0.34 | 0.7265 | much steeper |
| → brown 40/130 (cumulative) | ≤ 0.273 | 0.2727 | on the curve |

Per the frozen rule, pin 2 alone questioned transfer (+41% to +70% deviation,
>20% threshold). Pin 3 falsifies it again the other way: locked prediction
$450–$491 vs bound ≤$320 (29–35% below); under locked shape it would force
A_SW ≤ $782, contradicting pin 1. The implied SW curve is **flat, then a cliff
between 30 and 35 years, then rejoining the locked tail**.

Regional specificity check: the four pre-disclosure regional judgments at
amber 35/120 (NE 450, SE 425, Central 400, NW 400; ratios 0.38–0.41) sit
essentially on the locked curve (0.4091). The locked shape is therefore the
informant's *generic* domestic curve at that profile; the SW ≤320 bound is a
genuine regional departure — SW mid-tail would be the cheapest in the domestic
set in absolute dollars despite the joint-highest anchor, matching the stated
demand-concentration rationale.

### 3.3 Pin 2 is an outlier — flagged, not smoothed over

Pins 1, 3, 4 draw a coherent flat–cliff–tail curve. Pin 2 ($950–$1,050 for
amber 30/115) contradicts both the locked curve and that pattern (≈5–21% decay
over 10 years followed by ≈70% over the next 5 is not a smooth schedule). Most
plausible cause: anchoring on the top-profile figure quoted moments earlier in
sequence. It is retained in the grid as given and flagged; see §5 for the
preregistered re-elicitation.

## 4. Expanded SW grid (A_SW = $1,100; informant-interpolated)

Interpolation is piecewise-linear in loss L between the pins: (L=0, $1,100);
(L=3.154, $950–$1,050 band); (L=5.000, ≤$320 bound); (L=8.154, ≤$300 bound).
Coverage of the 125-profile domain: 44 profiles two-sided (L ≤ 3.154), 44 in the
cliff zone (semi-bounded), 37 deep-tail (ceiling-only, because pins 3–4 are
bounds). Locked-shape prices shown for contrast as contradicted scenario S1.

| Profile | Locked S1 (contradicted) | Informant band |
|---|---|---|
| pale/straw 20/110 | $1,100 | $1,100 (pin 1) |
| pale/straw 20/115 | $1,026 | $1,073–$1,091 |
| golden 20/110 | $1,089 | $1,096–$1,099 |
| pale/straw 25/110 | $932 | $1,039–$1,080 |
| golden 25/115 | $777 | $1,010–$1,070 |
| golden 30/115 | $619 | ≤ $1,050 (same L as pin 2) |
| amber 30/115 | $619 | ≤ $1,050 (pin 2, **flagged outlier**) |
| copper 30/115 | $595 | ≤ $905 |
| amber 30/120 | $564 | ≤ $742 |
| amber 35/115 | $494 | ≤ $453 |
| amber 35/120 | $450 | ≤ $320 (pin 3) |
| copper 35/120 | $437 | ≤ $318 |
| brown 35/120 | $369 | ≤ $310 |
| brown 40/110 | $396 | ≤ $314 |
| copper 40/130 | $355 | ≤ $308 |
| pale/straw 40/130 | $366 | ≤ $310 |
| brown 40/130 | $300 | ≤ $300 (pin 4) |

Representative rows shown; the full 125-profile grid can be generated from the
pinned interpolation above if this proposal advances.

## 5. Preregistered confirmation (required before any v3 lock)

This design is a **proposal requiring preregistration** before execution:

1. **Re-elicit amber 30/115 fresh, out of sequence** (the flagged outlier).
   Frozen rule: if the fresh answer falls below $800, pin 2 is discarded as
   sequence-anchored; if it repeats $950+, the flat mid-range is accepted as
   genuine and the cliff moves to the 30–35 stretch as drawn.
2. **Elicit golden 30/115** — identical loss L = 3.154 to amber 30/115 in the
   locked curve (factor 0.563078 both). Tests whether shade itself moves price
   at fixed age/tare, i.e., whether the loss axis is sufficient for SW at all.
3. **One copper pin in the cliff zone** (e.g., copper 35/120) to locate the
   cliff's position and steepness with a second shade.
4. Basis word required for every answer; ceilings recorded as bounds; ideally a
   second independent informant to break the single-unit dependence.

## 6. Limitations

- One informant, rough-sense basis throughout; zero independent replication.
- Two of four pins are one-sided bounds; the deep tail is ceiling-only.
- Pin 2 unresolved (§3.3); the mid-range premium is the least reliable part.
- Interpolation in loss space assumes the locked loss *ordering* transfers to SW
  even though the locked discount *magnitudes* do not; confirmation pin 2 tests
  a slice of this assumption only.
- No transaction data; nothing here is independently validated market pricing.
