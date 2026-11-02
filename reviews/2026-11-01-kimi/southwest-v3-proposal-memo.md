# Southwest Anchor Elicitation — v3 Proposal Memo (2026-11-01)

**Status: PROPOSAL ONLY.** V28 and Domestic Release Pricing v2 remain locked. The
locked wrapper continues to reject `southwest`. Nothing here modifies any packet
input, lock, model, workbook, or ZIP. This memo records an elicitation conducted
in chat after the peer review closed, and its analysis. It is not part of the
accepted review verdict and changes no finding in `reviews/2026-11-01-kimi.md`.

**Revision 2** (same commit date): the preregistered confirmation set in §5 has
been executed. Pin 2 is discarded per the frozen rule and replaced; findings and
the grid are updated. Revision 1 remains in git history.

**Revision 3** (same commit date): a five-question forced-choice consistency
pass ("partner refraction") ran against the confirmed knots — 5/5 agreement.
Because the answers were given by the original informant on his partner's
behalf, this is a consistency check across two framings, **not** independent
replication. The Q1 note upgrades the anchor to a floor (≥ $1,100). §5 and §6
updated.

## 1. Protocol

Two-pin elicitation preregistered in chat before answers were given; protocol
SHA-256 `a4caac25064138dacb8c6a5318df8b146318d4a4195921bdd0d5a80ac69bcc70`.
Frozen decision rule for shape transfer: SW amber 30/115 answer compared to
pin 1 × 0.563077 (the locked factor); deviation ≤10% supports transfer, >20%
questions it, between is inconclusive. A forced-choice refraction ladder
(eye-doctor style, ratio-first, no informant-named numbers) was preregistered
for re-eliciting pin 2 out of sequence, with a frozen scoring rule:

- Lens A (≥90%) or B (~70%) → pin 2 confirmed genuine flat mid-range.
- Lens C (~55%, the locked factor) → pin 2 discarded as sequence-anchored;
  locked transfer supported at this knot.
- Lens D (≤ ~35%) → cliff starts before 30 years.
- One bisection inside the chosen band; the chosen band replaces pin 2.

Single informant (the packet author). All answers: **"rough sense"** — the
lowest evidential tier. Ceilings recorded as bounds, not points. One
independent unit of observation throughout.

## 2. Pins (verbatim)

| # | Profile | Answer (verbatim) | Form | Status |
|---|---|---|---|---|
| 1 | SW pale/straw 20 yr 110 lb | "1100-1200" | range | active |
| 2 | SW amber 30 yr 115 lb | "950-1050" | range | **DISCARDED** — sequence-anchored; superseded by pin 5 per frozen rule |
| 3 | SW amber 35 yr 120 lb | "320 max" | ceiling (bound) | active |
| 4 | SW brown 40 yr 130 lb | "no more than 300" | ceiling (bound) | active |
| 5 | SW amber 30 yr 115 lb (fresh, out of sequence) | Lens "C", bisection "slightly above" | 55–60% of anchor → $605–$660 | active (replaces pin 2) |
| 6 | SW golden 30 yr 115 lb | "Same as amber, slightly above" | 55–60% of anchor → $605–$660 | active |
| 7 | SW copper 35 yr 120 lb | "Shade blind at 35/120" | ≤ $320 (same zone as pin 3) | active |

### 2.1 Second pass — "partner refraction" (consistency check, not replication)

Five forced-choice questions, answered by the informant on his partner's behalf
(one independent unit of observation, two framings). Frozen scoring: agreement
with confirmed knots strengthens internal consistency; any disagreement becomes
a reconciliation item with no averaging. Answers: **B, C, A, A, A — 5/5
agreement.** Notes verbatim:

| Q | Lens | Confirmed knot | Note (verbatim) |
|---|---|---|---|
| 1 anchor | B (about the same as NE $1,100) | A_SW = $1,100 | "could even be more, but no less than its northeast counterpart" |
| 2 amber 30/115 | C (about half) | $605–$660 | "the 30-year vintage is no picnic, but certainly must be substantially lower than the SW 20/110 blend" |
| 3 amber 35/120 | A (at most a third) | ≤ $320 | "the 35 vintage is forgetful redeemable only by its weight" |
| 4 golden vs amber 30/115 | A (same money) | shade-blind | "golden/amber in this vintage is negligeable, ultimately a function of preference/mood/taste (this is where re-sellers can pad or trim margins)" |
| 5 brown 40/130 | A (under $300) | ≤ $300 | "No higher than 300$ - on a good day" |

Interpretation of notes: Q1 upgrades the anchor to a **floor** (A_SW ≥ $1,100;
$1,100 retained as the conservative point, also where pin 4 pins it). Q4 frames
shade-blindness at 30 yr as a property of the *market* (reseller margin noise),
not only of the informant's perception. Q5 reads as an enthusiastic ceiling,
not a midpoint.

Informant's stated rationale (verbatim): "Southwest, because it consists of the
beach cities, commands a high premium, and the 20/110 harvest are among the most
sought after in the entire domestic area."

## 3. Findings

### 3.1 Level — resolved to a floor: A_SW = $1,100 (conservative point)

Pin 1 gives A_SW ∈ [$1,100, $1,200]. Pin 4 (brown 40/130 ≤ $300) coincides with
the locked curve's prediction at A_SW = $1,100 **to the dollar** (locked range at
A ∈ [1100, 1200]: $300.00–$327.27). The second-pass Q1 note ("could even be
more, but no less than its northeast counterpart") upgrades the anchor to a
**floor: A_SW ≥ $1,100**. The schedule below keeps $1,100 as the conservative
point estimate — NE-equal at minimum, consistent with the informant's
beach-premium rationale. This replaces (as a proposal) the retired v1
`model_inferred` value 1050.002, which the review already bars from use.

### 3.2 Shape — locked transfer SUPPORTED through 30 years; a single cliff is the only departure

| Stretch | Informant evidence | Locked | Verdict |
|---|---|---|---|
| pale/straw 20/110 (L=0) | $1,100 | $1,100 | anchor, pinned |
| amber 30/115 (L=3.154) | $605–$660 (pin 5) | $619 | **on the curve** — transfer supported |
| golden 30/115 (L=3.154) | $605–$660 (pin 6) | $619 | **on the curve**; shade-blind at fixed loss |
| amber 35/120 (L=5.000) | ≤ $320 (pin 3) | $450 | **cliff** — 29% below curve |
| copper 35/120 (L=5.231) | ≤ $320 (pin 7) | $437 | **cliff is shade-blind** at 35/120 |
| brown 40/130 (L=8.154) | ≤ $300 (pin 4) | $300 | rejoins the curve at the corner |

The revision-1 "flat mid-range" finding is reversed: it was a sequence-anchoring
artifact (pin 2 given immediately after the top-profile figure) and is discarded
per the frozen rule. The confirmed picture: SW rides the standard domestic curve
from the anchor down to 30 years, falls off a **shade-blind cliff between 30 and
35 years**, and lands back on the locked curve at the deep corner — matching the
informant's demand-concentration rationale with no leftover anomalies.

Loss-axis sufficiency check (preregistered): golden and amber 30/115 sit at
identical loss in the locked curve (L = 3.154, factor 0.563 both); the informant
independently placed them in the same band. At 35/120 the informant again made
the cliff shade-blind (copper joins amber ≤ $320). Two slices, both consistent
with the loss axis transferring to SW even where discount magnitudes do not.

Backward-interpolation sanity check: golden 25/115 falls at $775–$816 under the
confirmed knots; locked curve says $777 — inside the band.

Regional specificity: the four pre-disclosure regional judgments at amber 35/120
(NE 450, SE 425, Central 400, NW 400; ratios 0.38–0.41) sit essentially on the
locked curve (0.4091), so the cliff is SW-specific, not curve-generic. SW
mid-tail would be the cheapest in the domestic set in absolute dollars despite
the joint-highest anchor.

## 4. Expanded SW grid (A_SW = $1,100; confirmed knots)

Interpolation is piecewise-linear in loss L between: (L=0, $1,100);
(L=3.154, $605–$660 band); (L=5.000, ≤$320 bound); (L=8.154, ≤$300 bound).
Coverage of the 125-profile domain: 44 profiles two-sided (L ≤ 3.154), 44 in the
cliff zone (ceiling-only), 37 deep-tail (ceiling-only). Locked-shape prices shown
for contrast.

| Profile | Locked | Confirmed SW band |
|---|---|---|
| pale/straw 20/110 | $1,100 | $1,100 (pin 1) |
| pale/straw 20/115 | $1,026 | $993–$1,008 |
| golden 20/110 | $1,089 | $1,084–$1,086 |
| pale/straw 25/110 | $932 | $871–$901 |
| golden 25/115 | $777 | $775–$816 |
| amber 30/115 | $619 | $605–$660 (pin 5) |
| golden 30/115 | $619 | $605–$660 (pin 6) |
| copper 30/115 | $595 | ≤ $603 |
| amber 30/120 | $564 | ≤ $534 |
| amber 35/115 | $494 | ≤ $395 |
| amber 35/120 | $450 | ≤ $320 (pin 3) |
| copper 35/120 | $437 | ≤ $320 (pin 7) |
| brown 35/120 | $369 | ≤ $310 |
| brown 40/110 | $396 | ≤ $314 |
| copper 40/130 | $355 | ≤ $308 |
| pale/straw 40/130 | $366 | ≤ $310 |
| brown 40/130 | $300 | ≤ $300 (pin 4) |

Representative rows shown; the full 125-profile grid can be generated from the
pinned interpolation above if this proposal advances.

## 5. Preregistered confirmation — EXECUTED

All four preregistered elements ran:

1. **Amber 30/115 re-elicited fresh, out of sequence** (refraction ladder):
   Lens C, bisected slightly above → $605–$660. Per the frozen rule, pin 2 is
   discarded as sequence-anchored and locked transfer is supported at this knot.
2. **Golden 30/115 elicited**: same band → shade does not move SW price at
   fixed age/tare (slice 1).
3. **Copper 35/120 elicited** (cliff zone, second shade): "shade blind" →
   ≤$320, joining amber (slice 2).
4. Basis word captured for all pins ("rough sense"); ceilings recorded as
   bounds.
5. **Second-pass consistency check (revision 3)**: five-question forced-choice
   refraction against the confirmed knots — 5/5 agreement (B, C, A, A, A), zero
   reconciliation items. Q1 note upgrades the anchor to a floor (§3.1). Recorded
   as one independent unit of observation across two framings, **not**
   independent replication (answers given by the informant on his partner's
   behalf; the partner's own cold answers, if ever offered, supersede these).

Remaining before any v3 lock: independent replication (a second informant
answering directly, or transaction evidence).

## 6. Limitations

- One independent unit of observation throughout (one informant; the second
  pass was given on the partner's behalf and counts as a consistency framing,
  not replication). Rough-sense basis throughout.
- The anchor is a floor (≥ $1,100); $1,100 is the conservative point, not a
  measured central tendency.
- Three of five active pins are one-sided bounds; the cliff zone and deep tail
  are ceiling-only.
- The cliff's exact position and steepness between L=3.154 and L=5.000 is
  interpolated, not observed; no pin exists inside the cliff.
- Interpolation in loss space assumes the locked loss *ordering* transfers to
  SW; two shade-at-fixed-loss slices support this, but it is not exhaustively
  tested.
- No transaction data; nothing here is independently validated market pricing.
