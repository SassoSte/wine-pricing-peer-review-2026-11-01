# Independent peer review — v35 preference-learning and premium system

Reviewer: Claude (Fable 5.1), 2026-10-29. Code-level review against the artifacts in
`/Users/stefansassoon/projects/wine`. Nothing in the project was modified; all diagnostics ran from
the session scratchpad and only read project files. Section F lists exactly what was executed.

---

## A. Independent verdict

**The pause on incremental local tuning is justified, but the brief's reason for it is incomplete.**
The recent "fix one, break another" pattern is not a sign that the evidence is exhausted. It is the
predictable behaviour of a premium boundary that was fitted with zero margin. Specifically:

1. V28 was fitted by a mixed-integer program that minimises a weighted 0-1 error count with the
   decision radius fixed at 1.0 and constraint targets of 1.00001 / 0.99999. The optimiser therefore
   places labelled rows directly on the threshold. On v35, 20 size-labelled rows sit at |score| = 1 ± 0.00001
   and 32 rows sit within [0.99, 1.10), split exactly 16 meaningful / 16 not. In V28's own
   family-held-out runs, rows with |score| in [0.9, 1.5) are 14% of size judgments but 49% of size errors
   (27–33% error rate inside the band, 0.5–4% above 1.5). Questions 4 (1.308) and 6 (1.077) are band
   cases. Any one-coefficient correction will trade band cases against each other, which is what you observed.
2. A single monotone threshold on V28's score is already at its full-data ceiling: the best possible
   threshold gives 388/413, identical to the current radius. The ceiling for *any* function of the scalar
   is 405/413. So no recalibration of the radius can help; only a different score or a richer output can.
3. The 94% family-held-out ranking figure does not describe performance on new comparisons written to probe
   weaknesses. V28 scored 17/22 directions and 17/23 sizes on the non-pilot pairs added after its training
   evidence (rounds 55–56 and the voice isolations). The stratified pilot (11/12, 9/12) is the fairer number
   for random new pairs; the 17/22 is the fairer number for adversarial ones.

**What is working.** Label bookkeeping is clean: every headline count reproduces (655 / 474 / 413 / 232 /
3 exact / 245 explicit), no size label contradicts its direction, exact equality and practical similarity
are kept apart, and clarifications supersede rather than duplicate. The additive intrinsic ranking
transfers at 94.1% held-out and at 96.7% on rows without a "slight"-type adjective. V28's held-out score
magnitude is a well-calibrated confidence signal (Section B.21). The accordion the expert described is
already in the model; it is simply not being reported.

**What is not working.** The V28 fitting objective (no margin, three protected rows, a hard constraint that
two later labels contradict); the validation design (the family definition makes provenance×shade
interactions untestable by construction, and the three largest families land in the same folds in every
seed); a handful of early-round labels that are irreconcilable with later ones under any additive model;
and the latest candidate coefficient, which is an exception expressed as a number.

**Recommendation.** Consolidate V28 and the intrinsic ranking as they are. Change the *output*, not the
weights: report premium calls in three zones using the existing score. Put the four contradictory
northwest/Western-Europe rows to the expert as one clarification. Do not promote the 0.7 large-tare
coefficient. *(Update after execution: the three experiments in Section C were run read-only or in the
scratchpad, Sections G–J. E1 step 1 is half confirmed and worth adopting; E2 arm A and E3 are falsified
and should not be pursued further.)*

---

## B. Ranked findings

### B1. Verified mathematical or implementation defects

1. **Zero-margin premium boundary (V28 objective).** `tare_compensation_v27.fit` solves a MILP whose
   premium constraints are `d·x·w ≥ 1.00001` (meaningful) and `|x·w| ≤ 0.99999` (not meaningful), with a
   1e-8 L1 tie-break and no margin term. Consequence on v35 (full data, 413 size rows):

   | V28 \|score\| | n | meaningful | not | notes |
   |---|---:|---:|---:|---|
   | [0, 0.9) | 267 | 15 | 252 | all 15 missed premiums live here |
   | [0.9, 0.99) | 5 | 0 | 5 | |
   | [0.99, 1.01) | 20 | 10 | 10 | separated by 0.00002 |
   | [1.01, 1.1) | 12 | 6 | 6 | Q6 at 1.077 |
   | [1.1, 1.5) | 17 | 14 | 3 | Q4 at 1.308; all 10 false premiums are in (1, 1.5] |
   | [1.5, ∞) | 92 | 92 | 0 | |

   Held-out (V28's own 5-seed runs in `tare-refit-validation-v28.json`, 620 rows): error rate 27% in
   [0.9, 1.0), 33% in [1.0, 1.1), 28% in [1.1, 1.3), 13% in [1.3, 1.5), 4% in [1.5, 2), 0.5% above 2.

2. **The 0.7 large-tare coefficient is an exception, not a calibration.** It is active on 9 of 655 pairs;
   3 have a meaningful label it fixes (round53-2, round56-6, pilot Q9), 2 were already meaningful, 3 are
   unlabelled, 1 has zero score. Q9 and round53-2 clear the threshold by 0.0078 (score 0.3078 − 1 + 0.7).
   The grid (0, .1, .2, .35, .5, .7, 1) selects 0.7 because it is the smallest value above 0.6923; 2 of 25
   folds select 0.5, which fails both. Same zero-margin signature as finding 1. Keep it archived as a
   diagnostic; do not promote.

3. **A hard constraint in the V28 fit contradicts two explicit labels.** The fit imposes
   `w[pale] + w[tare_step] ≤ 0.99999` and `w[tare_step] ≤ 0.9999999`. Hence no single 5-lb step can ever be
   meaningful. round55-2 and round55-9 (20-year pale/straw, 110 vs 115 lb, explicit meaningful) are
   unlearnable by construction; they are 2 of the 15 missed premiums. The brief's "all-top-profile outputs
   preserved" refers to a separate mechanism; the V28 constraint still stands.

4. **Three protected rows inside the baseline.** `domestic_vintage_context_v27.ANCHORS =
   ('round49-2','round50-4','round49-17')` have their error binaries forced to zero in the V28 MILP
   (`protected_training_ids` in `tare-refit-validation-v28.json`). This is a per-pair exception in the
   retained default and should be disclosed wherever V28 is described as having "no pair lookups".

5. **Label drift explains 4 of V28's 10 false premiums.** 14 pairs changed label between evidence v28
   (V28's training set) and v35. round6-8, round6-9, round6-10 and round7-1 (central vs Middle East, brown,
   120 lb) were *meaningful* when V28 was trained and became *slight* in round57. V28 reproduces its
   training labels on them (score 1.077). These are not model errors. With the 4 coarsened early-round
   ties (r2-4, revision-8, revision-14, round9-18), only Q4 and Q6 remain as false premiums on labels that
   were stable and explicit.

6. **Fold generator is nearly deterministic for the largest families.** `compare_models.folds` assigns
   families greedily, largest first; the seed only shuffles tie order. The three largest families
   (EE, WCA, WE golden/pale; 27+22+21 rows) land in folds 0, 1, 2 in *every* seed. For 11% of the data the
   "25 repeats" are 5 identical repeats. Fold sizes are 131/131/131/131/131 in all seeds.

7. **The hierarchy constraint is active, and it binds on shade.** In the full `global-positive-v33` fit the
   learned ranges are vintage 6.433, tare 3.484, provenance 2.86107, shade 2.86106: the shade ≤ provenance
   constraint is tight to its 1e-5 separation; the same holds in the fold fits (3.06561 vs 3.06560). The
   data want a larger shade range than the hierarchy permits. Vintage ≥ tare and tare ≥ provenance are slack.

### B2. Plausible modelling limitations

8. **Missed premiums are a ranking problem, not a size problem.** All 15 missed-meaningful rows have
   |score| ≤ 0.70; none is near the threshold. Five are sign reversals (round47-15, 51-13, 56-2, 56-5,
   56-12): same-provenance golden↔pale/straw pairs where the older, lighter offering wins meaningfully.
   Across all provenances, in matched golden/pale 5-year pairs the younger wins at equal tare (37/38) and
   whenever the older is lighter by only 5–10 lb (15/15), and the older wins when lighter by 15 lb (5/5). That is one
   exchange rate (10 lb < 5 years < 15 lb), not a context effect. V28's
   `matched_provenance_five_year_golden_pale` term (+0.538 toward the younger) pushes the wrong way on the
   15-lb rows and is the reason the large-tare correction cannot reach them (it requires V28 to already rank
   the lighter offering higher).

9. **Brown is a provenance-dependent defect.** Eastern Europe: copper beats brown plus 10 years (r5-7,
   revision-4) and plus 10 lb (round13-11); copper loses to brown plus 15 years (revision-5). West Central
   Asia: the full brown→pale range is worth between 5 and 10 years (round11-14/15/16). Western Europe:
   brown→amber equals 5 years + 5 lb at the old end (round50-9, exact). Northeast: brown→amber is more than
   5 lb but less than 5 years + 5 lb (round54-17/18). A single global brown step cannot fit these, which is
   why the EE rows are missed 0/5 held-out, and why finding 7 binds. A provenance-specific brown term is the
   kind of "provenance-dependent effect" the brief says hurt held-out performance. See finding 19 for why
   the validation scheme could not have rewarded it even if it is real.

10. **The intrinsic value gap alone is a poor premium separator.** Best single threshold on the
    `global-positive-v33` |gap| gives 357/413 full-data and 331–357/400 held-out, versus V28's 388 (in-sample).
    Size judgments need their own calibration; a stronger ranking does not imply a stronger premium call,
    exactly as the brief states.

11. **Scalar at ceiling.** Best threshold on V28 |score| = 388 = current. Any-function ceiling = 405.
    The 8 irreducible overlaps are at 0.538 (pure 5-lb steps: 62 not / 3 meaningful) and 1.077 / 1.308.

12. **Two mechanisms tested and not supported.** (a) "Contested top": 16 size rows where the loser holds
    the best vintage or tare that the winner lacks; errors go both ways (4 missed, 1 false), so "competing
    strengths ⇒ slight" is not a rule. (b) "Weak bracket": 109 rows with both offerings ≥ 35 years; V28 size
    accuracy there is 98.2% with 2 false premiums, so bracket-level compression is not a systematic pattern.
    Both of the brief's Q4 narratives are pair stories, not mechanisms. Stop pursuing them.

### B3. Evidence and identifiability limitations

13. **Exact equality is a span property.** The 3 confirmed ties encode 2 independent identities:
    copper→amber = vintage(30→25) + tare(125→115) (round42-12 WE, round54-11 SE, same difference vector) and
    brown→amber = vintage(40→35) + tare(120→115) (round50-9 WE). In a continuous additive model an unseen
    exact tie has probability zero unless its attribute-difference vector lies in the span of confirmed
    identity vectors. So: predict "exactly equal" only when the pair's difference vector is a linear
    combination of confirmed identities and the model gap is ≈ 0; otherwise report "practically similar".
    This needs no fitting, is transitive by construction, and cannot erase strict preferences. The withheld
    older-WE tie is unidentifiable for the same reason: its vector is not in the span of the other two.
    Incidentally V28's lattice arithmetic returns |score| = 1e-5 on two of the three ties.

14. **213 strength adjectives are unused.** 39% of direction rows carry a slight-type adjective. Held-out
    direction accuracy is 90.0% on those versus 96.7% on the rest; the hinge demands the same unit margin
    from "slimmest possible margin" and "overwhelmingly". The residual ranking error is concentrated where
    the expert said the comparison is close.

15. **Quasi-prospective slice.** 35 pairs post-date V28's training evidence. V28: direction 28/34, size
    26/35, both 22/34. Excluding the 12 stratified pilot pairs: 17/22, 17/23, 14/22. These rounds were
    targeted (12 of 23 are WCA golden/pale), so this is a lower bound, not a population estimate. It is
    nonetheless the only number in the project that is not conditioned on a fit that saw the rows.

16. **A genuine contradiction under additivity.** r3-2, r4-7, r4-8, r5-5 (rounds 3–5, no adjectives, no
    size) say northwest > Western Europe at identical shade/vintage/130 lb. round36-1..4, r2-2, r5-6,
    revision-18, round14-4 say Western Europe > northwest (slightly) at 115–130 lb. No additive provenance
    offset satisfies both; the four early rows are 0/5 held-out and are 4 of the 21 full-fit intrinsic
    misses. Either they are historical imprecision or the expert holds a tare-conditional provenance effect.
    This is the single largest resolvable block of residual ranking error and it is a one-question decision
    for the expert, not a modelling task.

17. **Ridge grid floor.** α = 0.001 (the smallest grid value) is selected in 13/25 outer fits, 0.01 in the
    other 12. Regularisation is effectively inactive. Harmless given the margin constraints, but extend the
    grid downward or drop ridge and say so.

### B4. Validation limitations

18. **Family-held-out accuracy is flat in family size** (singleton 93.4%, size 2 95.7%, 3–5 94.2%, 6–9
    93.3%, ≥10 94.7%). The scheme is not measuring transfer difficulty; it is measuring near-tie noise
    (finding 14) and the structural misses (findings 8, 9, 16).

19. **The family definition makes provenance×shade interactions untestable.** A family is one unordered
    provenance pair × one unordered shade pair. Every row that could identify an interaction between a given
    provenance and a given shade is in the same family, so withholding the family removes all its support.
    "Improved full fit, worse held-out" for contextual terms is therefore partly an artefact of the split,
    not evidence against the terms. Interpolation (within-family, held-out vintage/tare variants) and
    transfer (across families) must be reported separately.

20. **Twelve fresh questions cannot select between models.** 10/12 vs 11/12 is one question. Use fresh
    sets only to falsify a frozen model's *band* claims (e.g. "fewer than 10% errors above 1.5"), not to rank
    two models.

21. **Held-out score magnitude is a calibrated confidence signal** (V28, 5 seeds, 620 rows):

    | held-out \|score\| | direction error | size error |
    |---|---:|---:|
    | [0, 0.1) | 16.8% | — |
    | [0.1, 0.3) | 23.6% | 3–7% (all missed premiums) |
    | [0.3, 0.6) | 13.1% | |
    | [0.6, 1.0) | 4.5% | 27% in [0.9, 1.0) |
    | [1.0, 1.5) | 1.6% (≥1) | 33% / 28% / 13% |
    | [1.5, ∞) | | 4% / 0.5% |

    This *is* the accordion. The product should say so.

---

## C. Ranked experiments

### E1 — Three-zone premium output, then a margin-aware refit of the same MILP (highest priority)

- **Hypothesis.** Premium errors are concentrated in a narrow score band that is predictable from the score
  itself; reporting that band as "borderline premium" and refitting with a margin removes most false
  premiums without touching rankings.
- **Minimal change.** Step 1 (no fitting): classify |score| ∈ [0.9, 1.5) as `borderline_premium`; keep
  `meaningful` above and `slight` below. Step 2: in `tare_compensation_v27.fit` replace the targets
  1.00001 / 0.99999 by 1+δ / 1−δ and replace the 1e-8 L1 tie-break with maximisation of δ subject to the
  error-count optimum (or a fixed δ grid {0.1, 0.2, 0.3} selected in training folds). Everything else,
  including protected anchors, unchanged for comparability; then rerun once without anchors.
- **Why the evidence supports it.** Findings 1, 5, 21. Held-out: 49% of size errors in 14% of rows.
- **Baseline.** V28 with the three-zone output (Step 1) so that the refit is judged on the same scale.
- **Procedure / leakage.** Same 25 family folds; δ chosen on training rows only; score on the 245 explicit
  rows and the 413 rows separately; also score the 35-pair quasi-prospective slice with the full fit.
- **Success.** Outside-band size accuracy ≥ 97% with ≤ 15% of rows in the band; held-out direction not
  worse than V28 (93.4%); pure 5-lb controls and the 3 exact ties unchanged.
- **Falsified if** errors do not concentrate in the band after the refit, or the band needed to reach 97%
  exceeds 25% of rows, or direction accuracy drops by more than 1 point.
- **Elicitation.** None. Q4 and Q6 become "borderline"; Q9 stays a miss (it is a ranking-side case).

### E2 — Release the brown defect from the shade-range hierarchy (intrinsic model)

- **Hypothesis.** The expert's hierarchy applies to the copper→pale/straw gradient; brown is a defect whose
  size the hierarchy is currently clipping (finding 7), and that clipping causes the EE brown misses.
- **Minimal change.** In `global_positive_v33.fit`, the ordering constraint
  `provenance_range − Σ w[9:13] ≥ 1e-5` becomes `provenance_range − Σ w[10:13] ≥ 1e-5`; `w[9]` (brown→copper)
  stays ≥ 0 and unbounded by the hierarchy. Optional arm B: `w[9]` becomes provenance-specific with
  shrinkage to a shared value (10 extra coefficients, one ridge weight).
- **Why the evidence supports it.** Findings 7, 9; the expert's own statement that brown is a defect.
- **Baseline.** `global-positive-v33` on the same 25 folds (94.10%).
- **Procedure / leakage.** Arm A: same family folds. Arm B additionally needs a within-family row-held-out
  tier (hold out vintage/tare variants inside each family) because family folds cannot score it (finding 19).
- **Success.** Shade range increases and the constraint goes slack; r5-7, revision-4, round13-11 move to
  ≥ 4/5 correct; overall held-out ≥ 94.1%; no new misses in the 92 rows with V28 |score| ≥ 1.5.
- **Falsified if** the brown step does not grow when freed, or held-out accuracy drops, or arm B wins only
  on the within-family tier and loses on the family tier (then it is memorisation).
- **Elicitation.** None.

### E3 — Strength-graded margins in the intrinsic hinge (ordinal targets)

- **Hypothesis.** Treating "very slightly" and "overwhelmingly" as the same unit-margin constraint distorts
  coefficients to satisfy near-ties; graded margins improve ranking on clear rows without losing slight rows.
- **Minimal change.** In `fit`, the lower bound for direction row i becomes m_i instead of 1:
  m_i = 0.25 for slight-type adjectives (`slightly`, `very slightly`, `slight`, `ever so slightly`,
  `very very slightly`, `slimmest possible margin`, `very close call`, `leaning`, `lean B`), 1.0 otherwise,
  1.5 where the row also carries a meaningful size label. Slack and ridge unchanged.
- **Why the evidence supports it.** Finding 14 (90.0% vs 96.7%); 213 adjectives currently unused.
- **Baseline.** `global-positive-v33`, same folds, same inner α selection.
- **Procedure / leakage.** Margin targets come from the training rows' own adjectives; validation rows are
  scored on direction only, exactly as now. Report accuracy separately for slight and non-slight rows.
- **Success.** Non-slight held-out accuracy ≥ 96.7% and slight ≥ 90.0%, with overall ≥ 94.1%; secondary:
  the fitted |gap| becomes a better size separator than 357/413.
- **Falsified if** non-slight accuracy drops, or the gain is confined to rows whose adjective was in training
  (then it is label leakage through the margin, and the experiment should be rerun with adjectives masked
  for the validation family).
- **Elicitation.** None.

---

## D. What to retain and what to stop

**Retain**
- V28 as the default, with the three-zone output added (E1 step 1) before anything else changes.
- The intrinsic `global-positive-v33` model as the ranking reference, including hard training equalities
  and the 1e-4 single-feature sign floor. Both are correct mechanisms.
- The five-category label semantics and the benchmark's refusal to infer size from adjectives or direction
  from ties. The bookkeeping reproduces exactly; keep the `clarification_history` discipline.
- Family-held-out validation as *one* tier, with the fold-placement caveat (finding 6) stated.
- The quasi-prospective slice (pairs post-dating a model's training evidence) as a standing report line for
  every frozen model.

**Stop**
- Any further generic scalar discounts or per-context premium coefficients on V28, including promotion of
  the 0.7 large-tare correction. Archive it as a diagnostic.
- Closeness-band and context-classifier equality detectors. Replace with the span rule (finding 13).
- Brown attenuation and bracket-level compression terms; the data do not show bracket compression.
- Using 12-question pilots to choose between models. Use them to falsify band claims of a frozen model.
- Adding pair-context terms to the V28 feature set. The two existing ones already fight the WCA evidence
  (finding 8).

**Resolve once, with the expert**
- The four rounds-3–5 northwest/Western-Europe rows (finding 16): confirm, retract, or state a
  tare-conditional provenance rule. Do not fit a term to accommodate four early rows.

---

## E. Confidence and unknowns

**Verified by execution (read-only):** all headline counts; sign consistency of size vs direction; V28 and
candidate scores on all 655 pairs; the lattice and band tables; the quasi-prospective slice; the 14 label
changes since v28; per-row held-out margins from `positive-validation-v33.json` and
`tare-refit-validation-v28.json`; family size and fold placement; active hierarchy constraint; the
opposition-test γ = 0 in all 25 folds; the 0.7/0.5 fold selections; the MILP constraints and protected
anchors in the fitting code.

**Inferred, not executed:** the three experiments (no refits were run); the claim that a provenance-specific
brown term would transfer (finding 9 shows the pattern in labels, not a fitted result); that the four
NW/WE rows are historical rather than a real tare-conditional effect.

**Not checked:** runtime-equivalence proofs (`tare-predictor-equivalence-v28.json`), the narrative in
`HANDOFF.md`/`README.md`, whether the 109 "coarsened recorded ties" from early rounds were individually
audited (their `basis` says so; I did not re-audit), and the v22 alternative objectives the brief mentions
(I confirmed only that the selected V28 came from the MILP).

**Main uncertainty about my own verdict:** the band analysis uses V28's held-out margins from the v28
evidence (620 rows, labels at that time). If the 14 later label changes fall disproportionately inside the
band, the in-band error rates are slightly overstated; the full-data table in finding 1 (v35 labels) shows
the same shape, so the conclusion stands.

---

## F. Exactly what was run

Scripts (scratchpad, not in the project): `diag1.py` (V28 scores, lattice, band, misses, candidate
activation, ties), `diag2.py` (quasi-prospective slice and label changes vs v28), `diag3.py` (intrinsic
full-fit and held-out per-row analysis, family-size and adjective splits), plus inline one-offs for family
structure, fold placement, hierarchy ranges, opposition and winning-gap fold parameters, and the V28
held-out band table. Interpreter: `.venv-regional/bin/python -B` (no bytecode written). No project file was
created, modified, or refitted; this review file is the only addition.

---

## G. E1 step 1 executed (2026-10-29, read-only)

Receipt: `peer-review-e1-step1-v35.json` (source hashes inside). Script: scratchpad `diag4.py`. No weights
fitted; direction outputs unchanged by construction; all 53 pure 5-lb rows stay "slight"; the 3 exact ties
stay "slight" (the span rule in finding 13 is a separate step).

**Band selected on training folds.** Over the 25 saved v35 family folds, choosing (lo, hi) on training rows
to maximise outside-band accuracy under a band-share cap picks **[1.0, 1.5)** in 25/25 folds at a 15% cap.
Validation rows: band share 9.7%, outside-band accuracy **96.0%**, false premiums **0.0** per seed,
missed premiums 15.0. On the 245 explicit rows: 12.7% band, 93.9% outside.

**V28's own nested-CV held-out margins** (620 rows, fixed band [0.9, 1.5)): with v35 labels, band share
13.8%, outside accuracy **96.9%**, false premiums 1.8 per seed (two-zone: 18.0 in the same runs), missed
premiums 8.2. With v28-era labels: 95.8% outside, 2.0 false premiums.

**Quasi-prospective slice.** 23 non-pilot post-training pairs: 5 in band, outside accuracy 12/18 (66.7%),
0 false premiums, 6 missed. Pilot 12: 2 in band (Q4, Q6), 9/10 outside, Q9 still missed.

**Reading.** The hypothesis is half confirmed and half falsified. False premiums are entirely a band
phenomenon: every one of them disappears at roughly 10% abstention, and the band edges barely matter
(sweep in the receipt: any hi ≥ 1.5 gives 0 false premiums). But the ≥ 97% outside-band target is **not
met**, because all 15 missed premiums sit at |score| ≤ 0.70, far below any sensible lower edge; no band
reaches them. They are the ranking-side cases of finding 8 (WCA golden/pale sign reversals, the two all-top
5-lb rows forbidden by the V28 constraint, and the large-tare trio). Conclusion: adopt the three-zone output
as a reporting change now (it costs ~10% abstention and removes the false-premium class), do not expect the
E1 step 2 refit to recover the missed premiums, and treat E2 and finding 8 as the route to those.

---

## H. E2 arm A executed (2026-10-29, scratchpad refit) — falsified

Receipt: `peer-review-e2-v35.json` (per-fold audits, held-out margins, full-fit coefficients, hashes).
Script: scratchpad `e2.py`. The only code change is the ordering constraint
`provenance_range − Σ w[10:13] ≥ 1e-5` (brown→copper excluded from the shade range) plus the matching
post-solve sanity check; hard equalities, the sign floor, nonnegativity and inner α selection are the
v33 code verbatim. Both arms were rerun on v35 with identical regenerated folds (seeds 11/29/47/71/103),
so the baseline here is the v33 structure on v35, not the saved v33 number.

| | baseline (v33 structure on v35) | brown released |
|---|---:|---:|
| held-out direction, 5 seeds | 93.67 / 93.25 / 93.25 / 93.46 / 94.51 | 92.62 / 92.41 / 93.25 / 93.04 / 93.25 |
| mean | **93.63%** | **92.91%** |
| held-out exact ties (of 3) per seed | 2/2/0/2/2 | 2/2/0/2/2 |
| full-fit direction | 449/474 | 452/474 |
| full-fit brown step ÷ vintage range | 0.235 | 0.261 |
| shade−provenance slack in fold fits | 0 (active) | +0.18 to +0.73 |

Target rows r5-7, revision-4 and round13-11 (Eastern Europe copper vs brown) stay **0/5** in both arms.
Twenty-one rows changed outcome: 6 improved (+7 row-repeats), 15 worsened (−24), the largest losses being
the central vs Middle-East brown rows round6-11 and round9-7 (5/5 → 1/5).

**Reading.** Both falsification conditions in E2 fired: held-out accuracy dropped 0.7 points and the brown
step barely grew relative to vintage when freed. The constraint does go slack once released, so finding 7
was right that it binds, but wrong about what it was clipping: the extra shade range is absorbed by the
copper→pale steps and by provenance offsets (top provenance changes from northeast to southeast), not by
brown, and it does not transfer. The Eastern Europe brown rows cannot be fitted by *any* global brown step
because other provenances bound it from above (round54-17 northeast, round10-10 WCA). That leaves a
provenance-specific brown term (E2 arm B) as the only candidate, and arm B can only be scored on a
within-family held-out tier (finding 19). Retain the v33 hierarchy as is. Finding 7 should be read as
"the constraint is active but releasing it does not help", and the brown-defect pattern in finding 9 as
evidence of provenance dependence rather than of a clipped global step.

Side observation: the v33 structure scores 93.63% on v35 versus the saved 94.10% on v33; the 13 pairs added
since (pilot and voice isolations) lowered held-out accuracy by about half a point, consistent with the
post-training slice being harder than the historical average.

---

## I. E3 executed (2026-10-29, scratchpad refit) — falsified

Receipt: `peer-review-e3-v35.json`. Script: scratchpad `e3.py`. One line changed in the v33 fit: the
squared-hinge lower bound per direction row is a per-row target instead of 1. Targets come only from the
rows being fitted (training rows at every level); validation rows are scored on direction alone. Same
regenerated v35 folds as E2; baseline identical to E2's.

| | baseline | primary 0.25 / 1.0 / 1.5 | sensitivity 0.5 / 1.0 / 1.25 |
|---|---:|---:|---:|
| held-out direction, mean of 5 seeds | **93.63%** | **91.86%** | 93.46% |
| held-out, 187 slight-adjective rows | 89.2% | 84.6% | 88.2% |
| held-out, 287 other rows | 96.5% | 96.6% | 96.9% |
| held-out exact ties per seed | 2/2/0/2/2 | same | same |
| full-fit direction | 449/474 | 441/474 | 448/474 |
| best size threshold on fitted \|gap\|, held-out | 346–358 / 400 | 341–363 | 350–357 |
| rows changed (improved / worsened, net row-repeats) | | 60 (23 / 37, −42) | 42 (20 / 22, −4) |

**Reading.** The hypothesis was that unit margins on near-tie rows distort the coefficients and cost
accuracy on clear rows. It is falsified: relaxing the near-tie margins leaves the clear rows essentially
unchanged (+0.1 to +0.4 points) and makes the near-tie rows worse (−1 to −4.6 points). The slight-row
residual is therefore not a loss-shaping artefact; it is genuine near-tie noise and label inconsistency.
The fitted gap does not become a better size separator either.

The primary arm also exposes a hazard specific to this evidence history: the rows that lose most are the
round36 Western-Europe/northwest clarifications, all labelled "slightly", which under a 0.25 target lose
to the unadorned rounds-3–5 rows (finding 16) that still carry a 1.0 target. Any strength-weighted
objective would privilege the earliest, least precise labels over the later clarifications. Do not pursue
ordinal margins on this evidence set; if strength is ever used, it must be in reporting, not in the loss.

## J. Position after the three experiments

- E1: half confirmed. Every false premium is a band case and disappears at ~10% abstention; the missed
  premiums are ranking cases no band can reach. Adopt the three-zone output as a reporting change.
- E2 arm A: falsified. The hierarchy constraint is active but releasing brown does not help and costs 0.7
  points; the brown defect is provenance-specific and only a within-family tier could ever score it.
- E3: falsified in both arms. Near-tie error is noise and label history, not loss shaping.

The pause is therefore better justified now than in the brief, and for reasons that point at consolidation:
the remaining error is (a) a boundary band that should be reported rather than fitted, (b) near-tie
comparisons the expert called close, and (c) four early-round labels that contradict later ones. None of
these is a model-structure problem that a small principled change fixes. The constructive next steps are
the three-zone output, the span rule for exact equality, the one-question resolution of the
northwest/Western-Europe rows, and a sealed prospective slice for any future frozen model.
