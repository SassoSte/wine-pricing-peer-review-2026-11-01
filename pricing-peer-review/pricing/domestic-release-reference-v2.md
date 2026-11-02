# Domestic Release Pricing v2

**Locked on November 1, 2026 as a provisional reference schedule.**

The separate pricing layer is retained without changing its curve. V28 remains independently
locked as the comparative model. Pricing is based on each offering's canonical value, not
on a chain of pair-specific score adjustments.

## Scope

Northeast, Southeast, Central and Northwest only. Whole filled casks with comparable
seat-origin/reference status, the same volume as supplied anchors, mint condition, and
initial-release distributor/insider terms. Currency is US dollars. Fees, taxes and delivery
are excluded. No inflation adjustment, delivered-cost estimate or resale-price claim is made.

Supported domain: pale/straw, golden, amber, copper and brown; vintage20/25/30/35/40years;
tare110/115/120/125/130lb. No extrapolation outside these input values. Southwest andforeign
regions are outside this locked reference; their prior grid values remain hypothetical.
Regular-batch discounts are not automatically applied across the entire domain.

## Method

`Price = regional anchor × exp(-monotone log-discount(base attribute loss))`.

The four supplied anchors are1100USD(NE),1075USD(SE),1050USD(Central),1000USD(NW), all at
pale/straw20years110lb. The underlying base shade/vintage/tare coefficients come from V28;
pair-context adjustments are excluded from money. The curve is stored in
`consistent-price-config-v2.json`. It was calibrated to accepted hypothetical prices and
two low-end Northeast judgments: approximately450USD foramber35/120 and near,butnotabove,
300USD forbrown40/130. The300value is a ceiling-active modeling target, not a verified costfloor.

All prior calibrated knots and fitted estimate values were retained during the low-end
refinement. Every offering has one price for this configuration; comparison differences
telescope, prices remain positive, and improvements do not lower prices.

## Evidence and verification

- Four user-reported initial-release offer anchors; completed transactions not established.
- Ten accepted disclosed hypothetical estimates across four distinct non-top profiles.
  Original fitMAE5.97USD, maximum16.07USD; profile-heldoutMAE39.73USD. These are calibration
  statistics against plausibility targets, not transaction accuracy.
- Regional low-end check: three approximate amber valuations differed by17.80USD/4.38% on
  average; three brown forecasts complied with300USD ceilings. Ceiling compliance isnot
  agreement with300USD point prices. Curve stayed frozen.
- Six middle-range checks: initial estimates differed, including a post-disclosure range
  correction. User later endorsed the model prices after consulting partner. Preserve that
  endorsement as expert support, not a retroactive zero-error blind test.
-14pricing tests pass (8v2+6v1); all1250gridpricespositive,3000orderingchecks and3750reference
  checks passed. Approved domestic reference is the500profile subset of that grid.
- The pricing workbook's6294formulas were recalculated and all1250prices matched runtime.

## Interpretation

This is a consistent, expert-calibrated reference, not a guaranteed market-clearing price.
Reported regional ranges span different offerings; they are not uncertainty intervals.
Shared curve shape is an assumption supported by limited expert checks, not independently
identified in every region or attribute combination. Inventory, distributor decisions,
collector demand, fees and condition differences can alter actual prices.

The next evidence should be actual offered, accepted and completed-sale outcomes, retaining
price basis, date, quantity and terms. Do not silently replace initial judgments with later
endorsements or count repeated discussion as independent observations.

## Use and verify

From the project root:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv-regional/bin/python pricing/domestic_release_pricing.py --offering '["northeast","pale/straw",20,110]'
PYTHONDONTWRITEBYTECODE=1 .venv-regional/bin/python pricing/verify_pricing_lock.py
PYTHONDONTWRITEBYTECODE=1 .venv-regional/bin/python verify_model_lock.py
```

`domestic-release-policy-v2.json` defines the approved scope. `pricing-lock-v2.json` records
artifact hashes. The lock is a reproducibility agreement, not filesystem write protection.
Future changes require an explicit new scope and new version. No tuning or questionnaire is
scheduled; previous configurations and validation records remain preserved.
