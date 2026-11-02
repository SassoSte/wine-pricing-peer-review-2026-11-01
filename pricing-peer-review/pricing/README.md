# Locked domestic pricing reference — November 1, 2026

**Domestic Release Pricing v2 is now locked as a provisional reference schedule.**
Its scope is Northeast, Southeast, Central and Northwest seat-origin/reference offerings,
whole filled casks, matching volume, mint condition and comparable initial-release
 distributor/insider terms. Prices are USD and exclude fees, taxes and delivery.

- Reference: [domestic-release-reference-v2.md](domestic-release-reference-v2.md).
- Entry point: `pricing/domestic_release_pricing.py`.
- Scope and configuration: `pricing/domestic-release-policy-v2.json` and
  `pricing/consistent-price-config-v2.json`.
- Pricing lock: `pricing/pricing-lock-v2.json` — 33 artifact hashes.
- Workbook: [consistent-prices-v2.xlsx](consistent-prices-v2.xlsx).

The approved entry point rejects Southwest and foreign regions; their earlier inferred
values are not promoted into this reference. The pricing curve itself is unchanged.
All500supported domestic profile outputs match the existing v2 engine. Four supplied
anchors match exactly. The expert checks and later endorsements are preserved separately
from initial estimates and are not described as transaction validation.

Verification completed:33pricing hashes,500domestic outputs,4anchors and scope rejection;
14pricing unit tests; all46original V28 lock hashes. V28 remains independently locked and
unchanged as the comparative reference. Existing premium-reporting caveats still apply.

Next evidence should be observed offered/accepted/completed-sale outcomes with clear dates,
terms and units. No tuning, new questionnaire, or background task is pending. Futurechanges
require explicit scope and a new version; do not overwrite these artifacts. A lock documents
reproducibility, not operating-system write protection or guaranteed market accuracy.

Verify from the project root:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv-regional/bin/python pricing/verify_pricing_lock.py
PYTHONDONTWRITEBYTECODE=1 .venv-regional/bin/python verify_model_lock.py
```

Older candidate statuses and next-step instructions below are historical; this checkpoint
and the two lock manifests take precedence.

---

## Middle-range pricing reconsidered — current curve endorsed

After seeing the6results and consultingpartner, user stated the model isright and its
predictions strong. Round-level expertendorsement saved in pricing/middle-range-checks-v1.json;
initialestimates, Q2correctionhistory andcalculateddifferences retained. Do nottreat these
initialdifferences asconfirmed marketpricingerrors, or rewrite them aszero-errorblindvalidation.
Partneragreement isreportedbyuser; no separateblindestimate ortransaction supplied.
Retainconsistentpricingv2 unchanged; no corrective refit based onwithdrawnfirstguesses.
This supports expertplausibility ofthecurrentcurve, notverifiedtransactions orconfidencebounds.
Earlier notes below describing middle-rangeobjections asunresolved are superseded.
V28locked; no pendingquestion, refit, orbackgroundjob.

## Middle-range pricing checks complete — v2 curve unchanged

pricing/middle-range-checks-v1.json records6frozenexpertchecks; summary in
pricing/middle-range-summary-v1.json. Five pointjudgments:MAE105.05USD,mean signederror-97.30,
meanabsolutepercentdifference14.68%;4underestimates/1overestimate. Q2isrange550–600corrected
from450–500afterforecastdisclosure; originalpreserved, model618 ($18above revisedupperbound).
Q3NEpale30/125:model521vs800;Q4NWamber30/115:model563vs700 arelargest discrepancies.
Q6NWgolden35/110:model493vs525. No retuningornewaccuracyclaim; expertchecksnottransactions.
Currentconsistentcurve structuralguarantees remain, butmidrangevalidationdoesnotsupport
consolidatingasreliableacrossinventory. ExamineQ3/Q4 andrepresentation beforeglobalcurveuplift.
All6answered; no pendingquestion orbackgroundjob. V28locked; pricingv2unchanged.

## Regional low-end transfer check complete — curve unchanged

Six frozenexpertchecks complete in pricing/regional-low-end-transfer-v1.json; summary in
pricing/regional-low-end-transfer-summary-v1.json. Amber35/120: NWmodel409vs400estimate,
SE440vs425,Central430vs400; meanabsolute deviation17.80USD/4.38%, allmodelestimateshigher.
Brown40/130: NW273,SE293,Central286, eachsatisfiesuserceiling300. Ceilingcomplianceisnot
accuracyagainst300pointprices; no lowerbounds oractualcosts provided. No refit. Smallexpert
transfercheck, notmarketvalidation orfullyblindstudy (earlierNE/regionalscenarios visible).
Currentconsistentpricingv2 retained; V28locked. No pendingquestion orbackgroundjob.

# Current pricing candidate — consistent low-end refinement v2

Entry: `consistent_price_v2.py`, configuration `consistent-price-config-v2.json`.
The original v1 layer and V28 remain unchanged. Read `consistent-price-verification-v2.json`
and the formula-driven `consistent-prices-v2.xlsx` for the current grid and checks.

Two new Northeast constraints extend the monotone log-discount curve:
- Amber,35years,120lb:450USD as the center of the expert's approximatevaluation.
- Brown,40years,130lb:300USD as a ceiling-active endpoint, consistent with “near,butnotabove300.”
  This is not a verified costfloor, exact transactionprice, orinventedlowerbound.

All five original curve knots and all regionalanchors are unchanged. The four supplied
initial-releaseprices still match exactly; all ten previouslyfitted estimate prices and
230previouslyin-span grid prices remain identical to v1. Their original calibrationresiduals
relative to acceptedhypotheticalprices have not been hidden or rewritten.

14tests pass (8refined-layer tests plus6prior-layer tests); all1250pricespositive,3000adjacent
orderingchecks and3750referencechecks pass. Workbook6294formulas recalculated withnoerrors;
all1250prices matchruntime. Newcurve spans the current modeled attribute-loss range.

Coverage of the scalar lossrange is notvalidation of everyoffering. Low-end shape comesfrom
twoNortheast judgments. Applying it to918non-Northeast low-endprofiles isexplicitly flagged
as regionaltransfer; sixregions still lack independentpriceanchors. No priceconfidenceinterval
or general economicfloor has been established. Trade/batchterms remain asstated inconfig.

Run:
```sh
PYTHONDONTWRITEBYTECODE=1 .venv-regional/bin/python pricing/consistent_price_v2.py --offering '["northeast","amber",35,120]'
PYTHONDONTWRITEBYTECODE=1 .venv-regional/bin/python pricing/test_consistent_pricing_v2.py -v
```

Older pricing notes below describe preserved prior stages, not the current curve.

---

## Low-end curve findings and consolidation decision

The analysis in `low-end-curve-analysis-v1.json` preserves the current configuration.
Three tails meet the calibrated curve at the same value and first derivative:

- Current continuation: `P = P_boundary * exp(-s*t)`.
- Slower continuation: `P = P_boundary / (1+s*t)`.
- A second slower continuation: `P = P_boundary / sqrt(1+2*s*t)`.

Here `t` is attribute loss beyond1.8462276923 and `s=0.2961953723`. These are sensitivity
scenarios, not an exhaustive range of possible curves or a confidence interval. All three
leave the230in-span modeledprices unchanged, remain positive over1,250profiles, and pass
9,000combined adjacent-order checks. Withno observations beyondtheboundary, currentcalibration
cannotchoose amongthese shapes. They do not establish a nonzero economicfloor.

For Northeast brown/40years/130lb, the three scenarios produce approximately$120,$271,$357;
Northwest approximately$109,$246,$324. Differences are assumptions, not measurederror bars.
The lower copper/35year/125lb profiles show similar uncertainty. Existing anchors andnear-top
acceptances alone do not establish consolidation ofthetail.

Consolidate the canonical per-offering engine, unit/source tracking, and explicit scopeflags.
Keep tail extrapolation provisional and unanchored regions marked. Do not average scenarios
into a falselyprecisequote. The next requested expert check is Northeast amber/35years/120lb,
with prices frozen in low-end-checks-v1.json and not disclosed for that profile yet. A genuinely
established comparable price is stronger evidence than acceptance of a disclosed scenario.
One additional point constrains localtail behavior; it doesnot establish a floor orentirecurve.

## Pricing insights and consolidation scope

The successful consistency fix is a separate monetary layer, not evidence that V28 became
more accurate. Its canonical value function assigns one price to each modeled offering
under fixed batch, volume, condition and commercial terms. Comparisons subtract those prices;
references no longer supply independent pair adjustments.

### What we learned

1. A useful pair-ranking model need not define consistent monetary prices. Direct conversion
   of V28's pair-context adjustments caused reference-path differences and shade-order reversals.
   Removing those terms from the monetary representation fixes the structural defect without
   changing V28's comparative engine or stored weights.
2. The new price function is `regional anchor × exp(-f(base attribute loss))`. A monotone
   log-discount curve ensures positive prices and nondecreasing prices when an attribute improves.
   Mathematical consistency is established; market accuracy is not.
3. Four established initial-release prices reproduce exactly by construction. Ten accepted
   hypothetical estimates reduce to only four distinct non-top attribute profiles, and were
   accepted after seeing proposals. They support local plausibility, not ten independent sales.
4. Fit residuals are small (mean$5.97,max$16.07), but holding out an entire profile produces
   meanerror$39.73; the combined profile's errors are$65–88. Preserve these distinctions.
5. The shared response curve assumes the same proportional discount at the same base attribute
   loss across regions. Actual regional anchors differ, but regional depreciation shapes have
   not been independently identified. Six regions still lack supplied monetary anchors.
6. Current curve support ends at loss1.8462276923. Most profiles (1,020/1,250) lie beyond it.
   Their positive values arise from continuing the last log-discount slope, not from observed
   low-end prices. There is no supplied economic floor or residual contents/vessel cost.
7. Regular-batch discounts, fees, taxes and delivery remain separate. Do not extrapolate the
   supplied5–10%regular-top-profile discount into every profile or treat baseprice as deliveredcost.

### Next analysis before consolidation

Keep the current configuration intact. Compare monotone positive low-end tails that reproduce
all current calibration points and meet at the same boundary. Differences beyond that boundary
measure assumption sensitivity, not a confidence interval. Check all-domain ordering and
reference independence. Identify a minimal low-end anchor that would discriminate the curves;
request a price/range before revealing scenarios if further elicitation is authorized.
Do not select a tail or invent a price floor merely because its numbers look plausible.

Sources: consistent-price-config-v1.json, consistent-price-validation-v1.json,
consistent-price-verification-v1.json, anchors-v1.json and the original valuation-check files
(all under pricing/). Current reference V28 remains locked and no historical evidence is rewritten.

# Separate consistent pricing layer

The current candidate is `consistent_price_layer.py`, configured by
`consistent-price-config-v1.json`. V28 remains locked and untouched.

For a fixed version and comparable trade/batch terms:

`P(region, offering) = regional_anchor × exp(-f(attribute_loss))`

Attribute loss uses V28's nonnegative base shade, vintage and tare contributions only.
The pair-specific comparison adjustments are not converted into money. The shared log-discount
curve is monotone, piecewise linear, and anchored at zero loss. Regional anchors are the four
supplied initial-release prices plus six explicitly inferred top-profile values.

Every offering has one canonical price. Comparison differences are `P(A)-P(B)` and ratios
are `P(A)/P(B)`. Reference translation uses this same configuration's canonical reference price;
an arbitrary new external price requires a new calibration version, not an on-the-fly override.

## What is verified

- Four supplied anchors reproduced exactly.
- All1,250domainprices positive and finite;3,000adjacentimprovementchecks pass.
-3,750referencechecks agree withinfloating-pointtolerance; differencestelescope.
- Golden/pale equivalence at130lb preserved.
- Ten accepted hypotheticalpricechecks: calibrationMAE$5.97, maximumdifference$16.07.
- Holdingout eachentire attributeprofile (allregionalcopies): MAE$39.73; thecombinedprofile
  heldout isoverestimated by$65–88. This isnot a market-accuracy estimate.

## Limitations

Only four distinct non-top attribute profiles informed the curve. Those prices were accepted
AFTER model disclosure; they are plausibility targets, not independent transactions. Of the
1,250gridprofiles,1,020extend beyond the calibrated loss span. Their positive prices depend on
last-slope extrapolation, not a verified low-end floor. Six regions lack actualpriceanchors.
Even inside the scalarspan, unobserved attribute combinations are not independently validated.

Assumes wholefilledcasks with comparable seat/reference-status, volume, mintcondition and
initial-release distributor terms; excludes fees,taxes,delivery. Do not apply the regularbatch
discount acrossallprofiles. Canonicalprices may disagree withV28's paircontext ranking; consistency
cannot be achieved by claiming every original pair-specific comparison has become a price gap.

## Artifacts and reproduction

- `consistent-prices-v1.xlsx`: formula-driven fullpricegrid,curve,anchors,acceptedchecks,
  profile-heldoutresults andregionalmodeledbounds. These bounds are not marketconfidenceintervals.
- `consistent-price-validation-v1.json`: complete checks,calibrationresiduals andgrid.
- `consistent-price-verification-v1.json`: testreceipt.
- `consistent-price-protocol-v1.json`: procedure fixedbeforecalibration.
- `all-region-price-grid-v1.xlsx`: previousstress-test grid,retained as a historical diagnostic,
  not the current candidatepricefunction.

Run checks fromtheprojectroot:

```sh
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 .venv-regional/bin/python pricing/test_consistent_pricing.py -v
PYTHONDONTWRITEBYTECODE=1 .venv-regional/bin/python verify_model_lock.py
```

No marketvalidation, questionnaire, deployment, or defaultV28change was performed.
