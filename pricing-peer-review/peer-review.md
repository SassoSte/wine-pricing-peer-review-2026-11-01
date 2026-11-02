# Wine pricing model peer review

**Prepared for:** an independent peer session, at Stefan Sassoon’s request  
**Prepared by:** Codex  
**Snapshot date:** 2026-10-27, America/Phoenix  
**Workspace:** `/Users/stefansassoon/projects/wine`

## Review request

Please independently review this preference-learning and pricing-model project. We have accumulated 401 unique labeled comparisons, tested progressively richer models, and reached a persistent tradeoff: models that recognize regional equalities tend to erase small real premiums; models that protect premiums invent differences where Stefan intends equal prices.

The current retained experimental baseline is the **v10 weighted hierarchy model**. Two convergence experiments remain separate and unpromoted. The latest refinement improves recognition of strict regional premiums but performs worse overall. The hand-coded `pricing.py` runtime remains revision E; “v10 baseline” means the experimental comparator, not a deployed replacement.

Your task is to challenge the evidence interpretation, representation, objective, constraints, and evaluation—not simply improve the reported percentage. Separate verified defects from plausible hypotheses. Recommend the smallest useful next experiments, including a simpler model if appropriate.

**Start read-only.** Preserve evidence, raw answers, frozen predictions, and all baselines. Do not silently turn uncertainty into equality, change labels, tune against outer-fold outcomes, or overwrite saved results. If an answer interpretation seems questionable, identify it for Stefan rather than correcting it yourself.

## Domain and intended output

Each stainless-steel offering is `[provenance, shade, vintage_years, tare_lb]`. Oak is outside this pricing loop.

| Attribute | Supported values |
|---|---|
| Domestic provenance | Northeast, Southwest, Southeast, Central, Northwest |
| Foreign provenance | Western Europe, Eastern Europe, West Central Asia, South/Eastern Asia, West Asia / Middle East |
| Shade, lighter to darker | Pale/straw, golden, amber, copper, brown |
| Vintage | 20, 25, 30, 35, 40 years |
| Empty vessel tare | 110, 115, 120, 125, 130 lb |

In this project, **younger vintage and lower tare generally increase preference**. Do not substitute external wine-market assumptions. The size/real-estate analogies used in conversation are explanatory; they do not reverse the established lower-tare preference.

The eventual goal is a pricing algorithm, but current learned scores are **normalized preference units, not dollars**. No monetary anchors have been elicited. Models assign offering scores and classify their difference as A higher, B higher, or equal. No learned abstention mechanism is implemented.

Stefan’s domestic hierarchy is soft: Northeast generally leads; Southwest and Southeast are close premium zones; Central and Northwest are slightly lower. Context can remove or reverse the effect of those regional advantages. Some young premium offerings converge; older offerings also often lose regional differentiation. These statements are not universal hard rules.

An important product question remains open: must the final system assign one globally consistent price to every offering, or can it return a comparison-specific judgment or uncertainty flag? That distinction matters for how exact equality and near-indifference should be represented.

## Evidence and answer semantics

The canonical current input is `evidence-v10.json`, not legacy `load_rows()` helpers in earlier scripts.

| Evidence item | Count or treatment |
|---|---|
| Unique labeled comparisons | 401 |
| A higher / B higher / exactly equal | 178 / 83 / 140 |
| Parent evidence v9 | 366 rows, preserved unchanged |
| Unique additions in v10 | 35 |
| Matched domestic regional ties | 56 |
| Matched domestic strict regional preferences | 14 |
| Matched domestic regional ties at age 30+ | 34 |
| Pure-tare exact ties / strict preferences | 27 / 41 |
| All domestic cross-zone comparisons | 118 |

“Matched regional” means only provenance differs; shade, vintage, and tare are identical. “Pure tare” means only tare differs. These are diagnostic subsets, not independent additional samples.

The 35 additions comprise 16 answered Round 27 pairs, one explicit supplemental provenance-swap comparison, 16 fresh isolation/component variants, and two resolved original pairs. One repeated comparison confirms an existing answer and adds no sample weight. Eight unresolved presentations/revisits are excluded; they concern the two unresolved original pairs below.

Current explicit options are:

1. Price A higher than B, including any tiny premium.
2. Price B higher than A, including any tiny premium.
3. Give them exactly the same price—no premium either way.
4. Leave unresolved / save for later.

“Very slightly” is a strict direction, not a tie. Its wording is retained, but no numerical premium is inferred. “Too close to call” is unresolved, not exact equality. Explanations and workflow feedback are metadata, not extra training samples. Older rounds used less explicit comparative language; corrections and reconciliations are versioned.

**Original Questions 7 and 11 remain unresolved and excluded from fitting/scoring.** Their answered variants are separate observations. Do not infer equality by interpolating between them.

| Original unresolved pair | Nearby observations |
|---|---|
| Q7: Central golden25/110 vs. Northeast golden20/125 | B at 120 favors B slightly; B at130 favors A slightly. Giving only A pale/straw favors A slightly; giving only B pale/straw favors B slightly. Original golden/golden pair remains too close to call. |
| Q11: West Central Asia pale/straw30/120 vs. brown20/120 | A at 25 favors A slightly; A at35 favors B slightly. Reducing only A tare to110 favors A slightly; reducing only B tare to110 favors B slightly. Original equal-tare pair remains too close to call. |

Two other original pairs were resolved:

- **Q15:** Southeast copper20/120 versus golden25/120 → A slightly higher. A separate same-age probe established copper20 = golden20 in this context, and younger vintage decided the full pair.
- **Q20:** Northeast versus Western Europe, both golden25/120 → recorded equal. **Interpretation detail:** the final wording was “we’d need shade difference to make a decision.” Immediately before this, Stefan explicitly clarified identical wording for the 20-year matched pair as option 3, exactly equal. Codex applied that clarified meaning at 25. The raw wording and label basis are retained. This is an appropriate evidence-provenance audit target; do not present it as a fresh explicit “3” at 25.

The supplemental Round27 Q2 provenance swap is also explicit user evidence, not an algorithmically generated label. Its endpoints and raw explanation are retained under `round27-2-provenance-swap`.

## Modeling history and current mechanics

The broad progression was hand-coded revision E → additive/near-tie models → direct ranking-and-tie fitting → contextual nonlinear tare curves → provenance-scoped tare equalities → weighted domestic hierarchy → regional convergence experiments. Historical percentages from different evidence versions are not directly comparable.

### Shared objective and offering model

For score difference `m = score(A) - score(B)` and strict label `y ∈ {-1,+1}`, the basic fitting loss is:

- Strict preference: `max(0, 1 - y*m)^2`.
- Exact tie: `m^2`.
- Plus regularization and structural constraints.

The unit strict margin is an arbitrary learning convention. A “very slight” preference and a strong preference have the same target direction/margin in this objective. Prediction uses a symmetric tie band: A if `m > threshold`, B if `m < -threshold`, otherwise tie, with small numerical tolerance.

**A predicted tie is generally not exact score equality.** Some exact equalities are enforced structurally; others merely fall inside the decision band.

The shared offering model has provenance offsets, shade/vintage increments, shared shade-by-vintage tare step curves, and partially pooled provenance-local tare curves. Local curves are activated from pure-tare comparison inputs in the training partition. Exact pure-tare ties fix the relevant local steps to zero. Weak younger-vintage, lighter-shade, and lower-tare monotonicity is enforced across the supported grid. Strict rankings remain soft losses.

The full v10 offering fit has 293 coefficients and 44 local contexts. Parameter counts are not effective degrees of freedom: regularization and constraints matter. They nevertheless deserve scrutiny against 401 dependent, adaptively elicited pairs.

A necessary scope regression is preserved:

- Western Europe, copper35, tare 120 versus125 → exact equality.
- Southeast, copper35, tare 120 versus125 → lower tare strictly higher.

Earlier shared tare curves could not represent both. Provenance-local constraints fixed that representational conflict. A feature-design conflict should not be called a contradiction in Stefan’s judgments without checking the underlying offerings.

### The three models under review

| Model | Structure and training changes |
|---|---|
| **v10 weighted hierarchy** | Shared offering fit plus a 33-parameter domestic layer: 5 persistent regional residuals, 25 shade/age hierarchy gains, 3 positive shade/vintage/tare scales. Soft average hierarchy and young premium-region guidance. Persistent residuals can retain regional differences even when a hierarchy gain goes to zero. |
| **First convergence candidate** | Replace that layer with a common domestic intercept, 100 centered shade/age regional parameters, and 3 learned offering scales. Penalize absolute pairwise domestic total-score gaps at reference tare 120 to allow zero gaps. Stronger age-dependent fusion and adjacent-context smoothing.104 predictive parameters; 250 auxiliary optimization variables. |
| **Selective convergence refinement** | Same contextual representation, but anchor regional gaps and adjacent-context changes to a training-only v10 pilot. Fix its 3 offering scales. Reduce fusion where matched regional training examples show premiums; increase the influence of those rare strict examples. Change inner selection to balance equality and premium recognition.101 regional parameters fitted, 3 scales fixed. |

First-convergence constants: age 20/25/30/35/40 weights `2/1/2/3/4`; fusion coefficient 0.3; gap ridge 0.1; adjacent-context smoothing 0.5. These are modeling choices, not elicited monetary quantities or guaranteed age laws. Soft average hierarchy permits zero gaps. The existing weak young premium-region prior remains; its synthetic scenarios are regularization, not observations.

Selective fusion uses matched regional training examples **within the same provenance pair**, weighted by `1/(1 + age_distance/5 + shade_index_distance)`. Its multiplier is `(1 + tie_support)/(2 + tie_support + 4*premium_support)`. Strict matched-regional losses receive the training tie/premium count ratio, clipped to `[1,4]`. Anchoring and fusion act on complete regional score differences at 120 lb, including the local tare contribution at that reference point.

This refinement changed several mechanisms together. Its result cannot by itself identify the contribution of adaptive fusion, pilot anchoring, fixed offering scales, sample weighting, or the selection criterion.

## Validation and results

All three current models use **the same401 evidence rows and the same outer withheld-family assignments**: five folds repeated with seeds 11, 29, 47, 71, 103. A family is the unordered provenance pair plus the unordered shade pair; all age/tare variants of that family stay together. Earlier family assignments were preserved as evidence expanded; new families were assigned by size without labels.

The v10 comparator uses its saved training-selected offering settings. Candidate fusion strength is selected from 0.1/1/10 inside three grouped training folds. The selective refinement additionally selects its v10 pilot’s prior strength in grouped subfolds inside each inner training partition. Fusion support, weights, local contexts, and constraints are derived from training only. Every current experiment reproduces all saved v10 held-out baseline predictions exactly.

**Threshold documentation correction:** some earlier result prose refers to a 0.2 validation threshold. Actual `fold_audits` and code use inherited fold-specific thresholds **0.15, 0.2, 0.3, 0.4, 0.5**, with inherited alpha/pooling settings also varying. The full-data snapshot uses alpha 0.1, pooling 1, threshold 0.2. All compared models use the same settings within each outer fold. Treat code, audits, and predictions as authoritative over that shorthand. The suitability of inherited thresholds for changed score distributions is an open review question.

v10 and first convergence select by overall A/B/tie balanced accuracy. The selective refinement instead averages overall class-balanced accuracy with matched-regional equality-versus-correct-premium balanced accuracy; ties favor smaller fusion strength. The changed selection objective is explicit, not an apples-to-apples architecture-only ablation.

### Same-evidence withheld-family results

Values are means across the five repeats, each covering all 401 rows once. Repeats are not five independent datasets.

| Metric | v10 | First convergence | Selective refinement |
|---|---:|---:|---:|
| Overall accuracy |76.36%|76.46%|75.11%|
| Balanced A/B/tie accuracy |75.15%|75.34%|73.72%|
| All exact-tie recall |70.71%|75.43%|66.29%|
| Domestic cross-zone accuracy,118 pairs |78.98%|76.78%|75.59%|
| Matched regional equality accuracy,56 pairs |90.71%|96.07%|82.86%|
| Older matched regional equality accuracy,34 pairs |87.65%|95.88%|83.53%|
| Strict matched-regional accuracy,14 pairs |38.57%|1.43%|52.86%|
| Pure-tare equality accuracy,27 pairs |54.81%|67.41%|54.81%|
| Pure-tare strict accuracy,41 pairs |96.10%|95.12%|96.10%|
| Opposite-winner errors per401 |11.4|12.8|14.4|

The first candidate predicts ties for 13.8 of 14 strict regional pairs on average. The selective model reduces that to 6.6, but loses legitimate ties elsewhere. All tare-only predictions in the selective model exactly match v10 in every repeat.

Raw correct counts by seed provide a compact paired check:

| Seed | v10 | First convergence | Selective refinement |
|---|---:|---:|---:|
|11|306|306|299|
|29|315|315|307|
|47|296|291|293|
|71|307|318|310|
|103|307|303|297|

Neither candidate is promoted. Do not treat small percentage differences or split ranges as statistical confidence intervals. These outer results have repeatedly informed model design; they are exploratory despite training-only fitting within each run.

### Fitted examples and failures

Full-data training consistency is 364/401 for v10, 343/401 for first convergence, and 357/401 for selective refinement. This is not held-out accuracy.

| Evidence ID | Pair, in original A/B order | User | v10 fit | First fit | Selective fit |
|---|---|---|---|---|---|
|round27-3|NE vs Central; golden35/125|Equal|A|Equal|Equal|
|round27-9|Central vs SW; brown35/115|Equal|B|Equal|Equal|
|round27-14|NE vs Central; amber35/110|Equal|A|Equal|Equal|
|round27-19|SW amber25/130 vs NW amber30/110|B|B|Equal|B|
|round27-15|SE copper20/120 vs SE golden25/120|A|A|Equal|A|
|round27-20|NE vs Western Europe; golden25/120|Equal|Equal|B|A|

The first convergence fit gives the three targeted regional equalities zero score gaps within 1e-7; the selective fit classifies them equal through the tie band, with nonzero gaps. Both retain all 27 enforced pure-tare equalities. First convergence has 45/56 matched regional ties at numerical zero; selective has 8/56. Exact equality at the reference weight does not automatically extend to other tare values.

### Prospective evidence and its limits

Round27 froze weighted-v9 and weighted-v8 models and 20 question/prediction pairs before elicitation. Sixteen were resolved initially; both models scored 9/16. Four were deferred. Later resolutions and isolation variants entered v10, so that round is **not** a fresh holdout for any model trained on v10. Its original score remains unchanged. No new frozen prospective comparison of the two convergence candidates has been run.

Question selection was purposeful and adaptive, not random population sampling. Adjacent probes can be correlated, and one person supplied all judgments. The A/B labels are imbalanced. No independent temporal test-retest study or population-level accuracy claim is established by these experiments.

## Questions for the reviewer

Please rank your concerns; the following are hypotheses to investigate, not conclusions you must accept.

1. **Target and decision rule.** Are we mixing exact price equality, uncertain preference, and practical indifference in a representation that cannot support all three? Is a single offering utility plus a global tie band appropriate? If abstention is introduced, how should it differ from predicting equal prices and how should its coverage be scored?
2. **Loss and threshold calibration.** Does treating every strict answer as a unit-margin target distort tiny premiums? Can direction-only evidence support a better equality/ranking objective without inventing magnitudes? Should thresholds be recalibrated inside training folds for each architecture rather than inherited? How would calibration avoid rewarding indiscriminate ties?
3. **Consistency and identifiability.** Audit exact-tie equivalence classes and strict-preference cycles on complete offering tuples, separately from conflicts caused by restricted feature designs. Is there any demonstrated data-level incompatibility, or only model mismatch? Are multiple score decompositions effectively indistinguishable with these comparisons?
4. **Representation and two-stage fitting.** Do persistent offsets, context gates, local tare curves, and later regional overlays confound one another? Would a joint fit or a smaller representation transfer better? Does fusion of total scores at 120 lb conflate regional premiums with tare effects?
5. **Learning where equality holds.** Can equality be selective without memorizing pairs or forcing a universal age cutoff? Should the strength/direction model and equality decision be separate, or must they remain consistent with one global price function? Identify the tradeoffs, not just a preferred model family.
6. **Rare premiums and selection bias.** Fourteen strict matched-regional examples are a small diagnostic subset. Did upweighting them and changing the selection objective overcorrect? Which single-change ablations would distinguish useful premium protection from added variance?
7. **Validation independence.** Is the current family grouping the right generalization target? It blocks age/tare variants of a region/shade pair but may allow shared endpoints or nearby related comparisons across folds. What alternative holdout would answer the intended product question? Does A/B/tie balanced accuracy depend too much on arbitrary presentation orientation? Propose appropriate paired, group-level uncertainty reporting.
8. **Elicitation and interpretation.** Which apparent equalities should be rechecked neutrally? In particular, review Q20’s contextual wording interpretation and any older ambiguous labels. Does repeated boundary probing induce anchoring or consistency pressure? Avoid proposing another large questionnaire without an information-gain rationale.
9. **Implementation audit.** Verify objective gradients/QP equivalence, row orientation, deduplication, inherited fold/config lineage, train-only constraints/support, pilot nesting, and serialization. Tests pass, but they do not prove the modeling assumptions or absence of a shared implementation mistake.

Please consider a simple comparator and an ablation plan before proposing more architecture. Do not assume that additional complexity, more questions, or larger premiums in the loss will solve the problem.

## Reproduction and source map

The accompanying ZIP preserves project-relative file names and includes a SHA-256 manifest. It excludes virtual environments, caches, media, and unrelated personal files. Extract into a new directory; use the supplied snapshots for inspection. If using the live workspace, do not overwrite baselines.

### Minimal reading order

1. `peer-review.md` — this brief.
2. `evidence-v10.json` — rows, unresolved pairs, reconciliation audit, explanation metadata, source hashes.
3. `weighted-hierarchy-comparison-v10.json` — retained comparator, `candidate_fit_all_401` and `nested_cv`.
4. `regional-convergence-comparison-v10.json` and `selective-convergence-comparison-v10.json` — candidates, per-seed predictions, subgroup metrics, fold audits.
5. `compare_models.py` — classification, metrics, family-fold helper. **Do not use its legacy `load_rows()` for current evidence.**
6. `compare_objectives.py`, `provenance_tare_model.py`, `weighted_domestic_model.py` — common loss, offering fit/constraints, v10 layer.
7. `regional_convergence_model.py`, `selective_convergence_model.py` — candidate parameterizations, penalties, QP/reference solvers, nested selection.
8. `refit_weighted_v10.py`, `compare_regional_convergence.py`, `compare_selective_convergence.py` — reconciliation and current evaluation drivers.
9. `round27-fixed.json` through `round32-isolation.json` — raw recent answers, frozen predictions, clarifications and adaptive probes. Earlier rounds are included for lineage.
10. `README.md` and `HANDOFF.md` — latest status first, followed by substantial historical context. Some older prose is superseded; the fold-threshold correction above is important.

### Commands

The live workspace has `.venv-regional` with OSQP 1.1.3 and access to installed NumPy/SciPy. For a fresh extracted packet, create an isolated environment. `review-environment.json` records the package versions used for this snapshot; `requirements-regional.txt` pins the additional OSQP dependency. Python-version or numerical-library differences can change tiny floating-point gaps.

```sh
python3 -m venv .venv-review
.venv-review/bin/python -m pip install -r review-requirements.txt
OPENBLAS_NUM_THREADS=1 .venv-review/bin/python -m unittest -v test_weighted_v10.py test_regional_convergence.py test_selective_convergence.py
```

`review-requirements.txt` pins the direct numerical dependencies to the snapshot versions; `review-environment.json` also records Python and platform information. The current verification suites contain 6, 8, and 9 tests respectively. They cover reported metrics, baseline reproduction, training-only contexts/support, unresolved exclusion, numerical checks, monotonicity, symmetry and equality preservation.

Full experiment entry points are:

```sh
OPENBLAS_NUM_THREADS=1 .venv-review/bin/python refit_weighted_v10.py
OPENBLAS_NUM_THREADS=1 .venv-review/bin/python compare_regional_convergence.py
OPENBLAS_NUM_THREADS=1 .venv-review/bin/python compare_selective_convergence.py
```

**Inspect before rerunning.** These drivers reproduce complete experiments and use immutable-output guards: a result file may be written only if absent or byte-identical. A different numerical environment can cause an overwrite refusal even when behavior is equivalent. Do not delete historical snapshots to bypass it; conduct reruns in a scratch copy and adapt the output destination with a clearly recorded source change. Full nested fitting uses more CPU than reading snapshots or running the tests. Use one BLAS thread.

Saved numerical-equality diagnostics use tolerance 1e-7; monotonicity tests allow numerical tolerance. Read the exact test and solver tolerances before treating a tiny residual as a substantive premium.

## Requested review output

Please return:

1. **Your independent diagnosis**, separating verified issues, supported interpretations, and untested hypotheses. Cite file/function names and evidence IDs.
2. **Any evidence corrections requiring Stefan’s confirmation**, with the original wording and reason. Do not apply them automatically.
3. **A ranked plan of at most three experiments**, each with the specific hypothesis, smallest implementation change, train-only tuning procedure, evaluation target, and a result that would falsify the hypothesis.
4. **A proposed success criterion** that protects exact equalities and genuine small premiums without hiding reversals, abstentions, or coverage loss in one overall percentage.
5. **A recommendation on the next elicitation step**, if needed: a few high-information neutral questions, a delayed repeat, a new frozen holdout, or no additional questions yet.

If files are unavailable, distinguish conceptual advice from verified code/data findings. It is acceptable to recommend keeping v10, simplifying, or changing the target definition rather than producing another higher-capacity model.
