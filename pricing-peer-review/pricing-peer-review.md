# Independent peer review of Domestic Release Pricing v2

## Review request

Please independently review the locked monetary-pricing layer in this packet. Determine
whether its mathematics, implementation, calibration, scope and stated limitations are
sound, and whether it is suitable as a **provisional domestic initial-release price guide**.

This is separate from the already locked V28 comparative-preference model. Do not assume
that good ranking implies good prices, that reference consistency proves price accuracy,
or that expert agreement after seeing a proposed price is independent validation.

Challenge our conclusions. Identify errors, hidden assumptions, unsupported extrapolations,
and small principled improvements if justified. Recommend retention, narrower use, or a
bounded follow-up test. Do not recommend a new model search simply because alternatives exist.

## Read first and preserve the lock

Paths are relative to the extracted packet root:

1. `pricing/domestic-release-reference-v2.md`
2. `pricing/domestic-release-policy-v2.json`
3. `pricing/pricing-lock-v2.json`
4. `pricing/consistent-price-config-v2.json`
5. `pricing/consistent-price-verification-v2.json`
6. `pricing/README.md` — current checkpoint first; older sections are historical.

The packet preserves the original directory layout. Absolute Mac paths in older documents
are historical references; use your own extraction directory.

Review inputs are read-only. Do not change models, evidence, labels, price anchors, weights,
curve knots, thresholds, workbooks or lock manifests. Do not run calibration/export scripts
that overwrite their outputs. Read their implementations instead. Bounded read-only checks
are welcome. Refits or changed assumptions require a proposed experiment, not an unannounced
modification of the packet.

An isolated environment for verification is appropriate. The original virtual environment
is not included. See `requirements-review.txt`. Use bytecode suppression when checking:

```sh
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 python pricing/verify_pricing_lock.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 python verify_model_lock.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 python pricing/test_consistent_pricing_v2.py -v
```

The pricing test file executes eight v2 tests plus six inherited v1 tests: 14 total.
The lock verifiers should confirm33 pricing artifact hashes and46 comparative artifact hashes.

## 1. Intended use

Prices are in US dollars for entire filled casks, assuming:

- Northeast, Southeast, Central or Northwest domestic provenance.
- Comparable regional seat-origin/reference batch status.
- Matching contents volume; the absolute volume has not been supplied.
- Mint condition.
- Comparable initial-release distributor/insider terms.
- Fees, taxes and delivery excluded.

These are not verified transaction, retail, resale, delivered-cost or market-clearing prices.
Inventory, distributor decisions and collector demand may move actual prices.

The input lattice is five shades (brown,copper,amber,golden,pale/straw), five vintages
(20, 25, 30, 35, 40 years) and five tare levels(110, 115, 120, 125, 130 lb). Younger vintage and lower
tare generally improve value in this elicited domain. Do not substitute real-world wine-aging
assumptions. Tare is not a substitute for contents volume.

The approved wrapper covers500 profiles acrossfour regions. The underlying experimental
engine can generate1,250 profiles across10 regions, but Southwest andforeignregions lack actual
anchors and are explicitly excluded from the approved wrapper. Verify that scope boundary.

## 2. Evidence hierarchy and actual anchors

`pricing/anchors-v1.json` contains four user-reported initial-release offer prices:

| Region / batch | Pale/straw,20years,110lb | Reported share of its regional production |
|---|---:|---:|
| Northeast / Manhattan Hudson | $1,100 | 2% |
| Southeast / Miami Vicecory | $1,075 | 3% |
| Central / Fort Brent | $1,050 | 4% |
| Northwest / Pearl Cliff | $1,000 | 5% |

All four were confirmed as comparable release-period prices for mint filled casks of equal volume.
They were offered to distributors/insiders; completed sales were not confirmed. Calendar dates,
absolute volume, production counts, underlying costs and margin percentages remain unspecified.

These seat-origin batches have commemorative seals/designs. Ordinary regional offerings come
from the same region but not its seat. The user gave a5–10% discount for otherwise matching
regular counterparts: NE990–1045,SE967.50–1021.25,Central945–997.50,NW900–950USD. These ranges
come from one shared expert rule; they are not eight independent observed prices. The locked
wrapper does not apply this discount to the full grid.

Region, seat/batch identity, design and reported rarity vary together in the four anchors.
Their independent effects cannot be isolated from these observations. Shares ofdifferent
regional populations are not comparable absolute scarcity measures without production counts.

## 3. Why a separate price layer was necessary

The first exploratory mapping used V28's pair score directly:

`P(x) = anchor_price + dollar_scale * g(x, reference)`.

NE/NW established a scale ofapproximately 130 USD per preference-score unit. This matched nearby
expert plausibility checks but failed the exhaustive grid:

- 15 nonpositive linearprices.
- 50 single-attribute shade-order violations.
- 190 profiles whose prices changed bymorethan$1 through anintermediate reference, up to$140.
- 580 within-region pair/list direction reversals witha listedgap above$1;540also had a
 pair-implied dollar gap above$1.

For example, Northeast golden25/115 wasaround790directly but860through a25-year pale reference.
These were conversion defects, not grounds for modifying V28's locked comparative weights.
See `pricing/all-region-price-grid-v1.json` and `pricing/price-grid-findings-v1.json`.

## 4. Current mathematics

Files: `pricing/consistent_price_layer.py`, `pricing/consistent_price_v2.py`,
`pricing/domestic_release_pricing.py` and the associated configurations.

Let A_r be the regional initial-release anchor. Let phi(x) contain cumulative shade andvintage
quality indicators and tare quality `(130-tare)/5`. Retain only V28's nonnegative base
shade/vintage/tare coefficients, indexed9through17. Exclude its provenance offsets and both
pair-context coefficients from monetary adjustments.

```text
L(x) = w_base · [phi(pale20/110) - phi(x)]
P_r(x) = A_r * exp(-f(L(x)))
```

L is a nonnegative attribute-loss coordinate. At130lb, the paleincrement is suppressed,
preserving the elicited golden/pale equivalence. The log-discount function f is monotone,
continuous and piecewise linear. It is not claimed differentiable at its knots.

The current knots, to displayed precision, are:

| Attribute loss L | Log discount f(L) |
|---:|---:|
| 0 | 0 |
| 0.076906153846 | 0.009591409708 |
| 0.538493076923 | 0.069161035199 |
| 1.230828461539 | 0.165769485334 |
| 1.846227692309 | 0.348047889601 |
| 5.000199996207 | 0.893817876022 |
| 8.154152303901 | 1.299282984130 |

The JSON configuration contains authoritative full precision. The final upper-bound knot
uses a one-ULP conservative rounding adjustment to avoid floating-point overshoot above300USD.

Comparisons subtract canonical prices: `P(A)-P(B)`. Relative prices are `P(A)/P(B)`.
A reference translation uses the reference's canonical price from the same configuration,
not an arbitrary external quotation. Thus differences telescope and closed-loop ratios
multiply toone. A new inconsistent external anchor requires recalibration/versioning rather
than changing the comparison reference at runtime.

Because the regional multiplier is the only region-dependent component, two regions retain
a constant price ratio for the same attribute profile. Assess whether that structural
assumption is acceptable or too strong for the available evidence.

## 5. Calibration procedure and what was actually learned

The original five knots preserved the four top anchors and fit ten expert-accepted
hypothetical prices at only four distinct non-top attribute profiles. Those proposedprices
were shown before acceptance. They are plausibility targets, not independent sales.

For each distinct profile, calibration averages `log(anchor/accepted_price)` across its
regional examples. Profiles receive equal weight. Monotonic pooling is available if means
violate ordering. The fitted curve has anorigin knot atzero and interpolates those profile
means. Its single-log-slope comparator was also evaluated.

Original fitted-price deviations from the accepted targets:

- Mean absolute difference: **$5.97**.
- Maximum absolute difference: **$16.07**.
- Single-log-slope comparator mean difference: **$23.06**.
- Leave-entire-profile-out mean error: **$39.73**.
- Holding out the combined-change profile produced errors ofabout **$65–88**.

The profile-heldout procedure removes all regional copies together. It still evaluates
expert judgments rather than market prices. See `pricing/consistent-price-validation-v1.json`.

The low end was initially extrapolated. Three positive monotone tails could match all known
calibration points and theboundary slope yet differ greatly at the bottom. Two additional
Northeast expert judgments were then used to addknots:

- Amber35/120: **around$450**, treated as anapproximate-center target.
- Brown40/130: **near, but not above $300**, treated as aceiling-active endpoint.

The second judgment didnot supply anexact price, lower bound, cost amount, ormargin. Choosing
the upper endpoint is a modeling decision consistent with the qualitativeguidance, not a
verified economicfloor. Both newpoints were usedfor calibration, not retained asindependenttests.
All previous fiveknots, regionalanchors,10fittedprices and230previouslyin-span prices were
preserved exactly. The currentknots cover the supportedlossrange, but range coverage isnot
independentvalidation ofeverycombination. Most profiles remain unobserved.

## 6. Checks after low-end refinement

### Regional transfer

The curve and six forecasts were frozen before responses, asking one offering at a time.
Earlier Northeast prices and sequential regional results were visible.

| Offering | Region | Expert judgment | Frozen estimate |
|---|---|---:|---:|
| Amber35/120 | Northwest | Around$400 | $409.09 |
| Amber35/120 | Southeast | Around$425 | $439.77 |
| Amber35/120 | Central | Around$400 | $429.55 |
| Brown40/130 | Northwest | Atmost$300 | $272.73 |
| Brown40/130 | Southeast | Atmost$300 | $293.18 |
| Brown40/130 | Central | Atmost$300 | $286.36 |

The three approximatevaluations have meanabsolute difference$17.80 and meanabsolutepercentage
difference4.38%; allthree predictions were high. The three upperbounds were satisfied, but
that isnot three exact-price successes. No curve was refitted duringthesechecks.

Sources: `pricing/regional-low-end-transfer-v1.json` and its summary.

### Middle-range checks and later endorsement

All six forecasts were frozen. First statedjudgments versus forecasts:

| Offering | Initial expert estimate | Frozen price |
|---|---:|---:|
| NE golden30/115 | $600 | $619.39 |
| NW copper25/120 | $550–600 aftertypo correction | $618.07 |
| NE pale30/125 | $800 | $520.96 |
| NW amber30/115 | $700 | $563.08 |
| NE copper30/120 | $600 | $542.19 |
| NW golden35/110 | $525 | $492.90 |

The range was originally450–500 andcorrected after the forecast was revealed; both records remain.
For thefive pointestimates, MAEwas$105.05, meansignederror−$97.30 andmeanabsolutepercentage
difference14.68%. Do not replace therange witha midpoint to inflate thepoint count.

After seeingthe results andconsulting a partner, theuser endorsed the model prices and
reconsidered the initial estimates. That isuseful expert plausibility support, not independent
blind validation or proof ofzeroerror. The partner's agreement wasreported bytheuser, not
separately elicited. The curve wasnot adjusted to the initial guesses or the later endorsement.

Sources: `pricing/middle-range-checks-v1.json`, `pricing/middle-range-summary-v1.json`.

## 7. What the integrity tests establish

The currentverification reports:

- Allfour supplied anchors reproduced exactly.
- All 1,250 experimental engineprices positive andfinite.
- 3,000 adjacent attribute-order checks passed.
- 3,750 reference-independence checks passed.
- Originalten fittedcheckprices unchanged.
- 14 pricing unit tests passed.
- 6,294 spreadsheet formulas recalculated withoutformulaerrors; all 1,250 spreadsheet prices matchruntime.
- Approveddomestic wrapper reproduces500 engine prices and rejectsunsupportedregions.

These establish implementation properties, not marketaccuracy. Thepricefunction can disagree
withV28's original pair-context preferences; we do not claim to preserve everyranking while
also imposing a consistent intrinsicprice. OriginalV28 remains unchanged andindependently locked.

## 8. Questions for the reviewer

1. Are theunits, featureencoding, signs, interpolation, boundaryhandling andreference translation correct?
2. Is the useof V28's baseattribute weights as aone-dimensional loss coordinate defensible?
   Which materiallydifferent offerings collapse tothesame L, anddoes availableevidence challenge that?
3. Does shared f acrossregions unduly impose constantregional ratios? Is a moreflexible model
   identifiable fromcurrent data, orwould it simply memorize expert acceptances?
4. Are profile averaging, equal profile weights andmonotonic pooling appropriate? What is identified
   byten acceptances atfour profiles versus imposedbythe functionalform?
5. Does treating near-but-not-above300 as anactiveendpoint overstate precision? Howshould a
   censored/interval judgment be represented without inventing a lower bound orcost floor?
6. Are positivity, monotonicity andreferenceindependence sufficient for internaluse? What other
   economically meaningful consistency checks should be run?
7. Is it legitimate to retain this as a provisional price guide given thefirst-estimate discrepancies
   and post-disclosure endorsement? Distinguish operational usefulness fromvalidated accuracy.
8. Are seat-origin rarity, design, provenance andmarketterms confounded inways that materially
   limit transfer? Avoid inventing scarcitymultipliers fromregionalproduction percentages.
9. Are observed asking, accepted andcompleted-sale prices needed next? Specify the smallest useful
   validation design, including offers that didnot sell and comparability ofterms/volume/condition.
10. Is thecurrent lock appropriate? Recommend narrower deployment scope, better reporting, or a
    concrete model change onlywhere supported. We do not seek an open-ended refinementcycle.

## 9. Required response

Return:

- **Verdict:** retain theprovisionalreference, narrowitsuse, orreopen a specific bounded issue.
- **Ranked findings:** verified defects, unsupported assumptions, evidence/identification limits,
  and documentation issues keptdistinct; citeexactfiles and calculations.
- **Up tothree rankedexperiments, onlyif warranted:** hypothesis, minimalmathchange, baseline,
  leakage controls, acceptance/failurecriteria, requireddata, and explicitstoppingrule.
- **Preserve/stop list:** distinguish comparativeV28, monetarycurve, regionalanchors, batch/terms,
  uncertaintyreporting andevidenceinterpretation.
- **Execution receipt:** files examined, checks actuallyexecuted, exactconfig/manifest identities,
  and what remains inferred. Do notclaim checks youdidnotrun.

Read-only inputscope doesnot prohibit writing yourreview to a separateoutputdirectory.
Return the review as Markdown plus small calculation receipts. If this packet is later
hosted in a repository with an explicitly writable `reviews/` location, usea branch/pullrequest
when authorized; otherwise return downloadablefiles or completeMarkdown. Never modify the
locked inputpacket or claim upload withouta receipt.

Please be skeptical without being dismissive. A coherent pricefunction is real progress;
it is not proof of correctprices. Conversely, sparse evidence doesnot automatically make
an internal reference useless. We want an independent, evidence-grounded judgment about
what this pricing layer can responsibly support and what would most efficiently improve it.
