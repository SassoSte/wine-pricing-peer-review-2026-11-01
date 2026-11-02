# Wine valuation model audit and decision record

**Decision date: October 31, 2026. Status: locked reference; model search paused.**

V28 remains the reference/default model. Its explicit uncertainty reporting is retained,
but is not a calibrated confidence guarantee. The V37 premium correction remains an
experimental alternative. The later contextual premium head is rejected. No weights,
thresholds, or evidence labels were changed to establish this lock.

The project has produced a useful comparative-ranking system, a less reliable premium-size
classifier, and a durable elicitation record. It has not established a price estimator,
a universally reliable meaningful-premium classifier, or a general exact-equality predictor.
The pause is justified by repeated transfer failures and unsuccessful controlled experiments,
not by proof that the problem is mathematically exhausted.

## 1. What the system is trying to learn

An offering has four attributes: provenance, shade, vintage, and tare. The domain contains
10 provenances, five ordered shades, vintage values 20/25/30/35/40 years, and tare values
110/115/120/125/130 lb: 1,250 possible offerings. Younger vintage and lower tare generally
increase value in this elicited domain. This convention must not be replaced with assumptions
about commercial wine aging.

The expert's broad importance order is vintage, tare, provenance, then shade. This is not a
lexicographic rule: a large tare advantage can beat a smaller vintage advantage. Endpoints,
regional context, and the particular attribute combination matter. The exceptional
all-top profile was described as rare; no measured inventory distribution or scarcity
probability was supplied.

There are distinct prediction tasks:

1. **Direction:** A higher, B higher, or an explicitly supported equal-price relation.
2. **Premium size:** meaningful versus slight/practically similar.
3. **Uncertainty:** whether the system should withhold a premium classification.

A clear winner can still have a slight price advantage. Practical similarity without a
clear direction is not exact equality. Unresolved is not a tie. No dollar prices, percentage
premiums, consumer-choice probabilities, or market prices can be inferred from the internal
scores without additional calibration evidence.

## 2. Evidence and corrections

The current development snapshot is [evidence-v38.json](evidence-v38.json), with its
[scoring targets](benchmark-targets-v38.json):

| Quantity | Count |
|---|---:|
| Unique unordered pairs | 691 |
| Known strict directions | 509 |
| Known premium-size labels | 453 |
| Strict direction and size both known | 271 |
| Explicit exact-price equalities | 4 |
| Conservatively marked explicit size judgments | 285 |

Missing axes remain missing. Reversing A/B does not create a new observation. Repeated
clarifications supersede active labels once and preserve history; repetition does not
increase weight. Historical strength adjectives were not automatically translated into
precise monetary margins or reliability weights.

The two recent prospective sets were frozen and scored before entering development evidence.
Their original receipts remain separate. In the 16-question set, question 11 was revised
after results were shown: both original and corrected scores are retained. In the 20-question
set, question 14 was corrected at the user's request before predictions were revealed.
Its original response is preserved in the answer history.

Four early Northwest-versus-Western-Europe answers were explicitly revisited. Each was
corrected to Western Europe slightly higher, not meaningfully higher. Earlier regional
exact-equality interpretations were also clarified rather than silently resolved through
extra model complexity. These changes improve evidence consistency; they are not themselves
new predictive wins.

Sources: [regional clarifications](regional-clarifications-v35.json),
[16-question clarification history](prospective-reporting-v1-clarifications.json),
[20-question answer history](prospective-v37-progress.json).

## 3. Locked reference mathematics

### V28 pair score

[predictor_v27.py](predictor_v27.py) supplies the unchanged engine used by
[predictor_v28.py](predictor_v28.py). Its 20 coefficients are in
[model-config-v28.json](model-config-v28.json).

For offering x, phi(x) contains 18 terms:

- Nine provenance indicators; Eastern Europe is the reference.
- Four cumulative shade increments: copper, amber, golden, pale/straw.
- Four cumulative vintage increments: at most 35, 30, 25, and 20 years.
- Linear tare quality (130 - tare)/5.

The pale/straw increment is suppressed at 130 lb, preserving the elicited zero golden-to-pale
premium there. This is an explicit domain rule, not a universal shade assumption.

For pair (A,B), let s = sign(vintage_B - vintage_A), positive when A is younger. The score is:

```text
g(A,B) = w · [phi(A) - phi(B)] + c1 h1(A,B) + c2 h2(A,B)

h1 = s when provenance matches, vintage differs by 5 years,
     and shades are golden versus pale/straw; otherwise 0.

h2 = s when provenance matches, vintage differs by 5 years,
     the younger offering is at most 30 years old,
     and the younger offering is 5 lb heavier; otherwise 0.
```

Positive g favors A; negative g favors B. The direction tolerance is 1e-7. The legacy
premium decision is meaningful when |g| > 1 + 1e-8. A zero or tiny score does not establish
an exact price equality in this pair comparator.

The context terms make this a pair model. We do not claim that every pair score is the
difference of globally consistent individual prices, or that rankings are universally
transitive across all possible offerings.

The V28 fitting family uses mixed-integer classification-error constraints with protected
training anchors and a small L1 tie-break. Solver time limits and feasible incumbents are
reported in saved receipts. Feasibility or a solver gap tolerance must not be described as
proof of an exact global optimum. See [tare_compensation_v27.py](tare_compensation_v27.py).

### Reporting layer

The retained reporting interface is [predictor_reporting_v2.py](predictor_reporting_v2.py),
with [reporting-config-v2.json](reporting-config-v2.json). Its default backend is V28.
For V28, the reporting score S is |g|:

```text
S < 1.0          small directional advantage, if a direction exists
1.0 <= S < 1.5   borderline premium; meaningfulness withheld
S >= 1.5         meaningful premium
```

Direction, premium classification, and uncertainty are separate output fields. Borderline
never means exactly equal. The raw legacy prediction remains available. Neither the
reporting score nor the boundary flag is a calibrated probability or winner-confidence
estimate. A small-directional label can still be wrong about the direction.

## 4. Experimental premium corrections

V35 adds a premium-only correction when a five-year vintage difference opposes a tare gap
greater than 10 lb and V28 already favors the lighter offering:

```text
L = max(0, (absolute_tare_gap - 10)/5) if eligible; otherwise 0
premium_decision_v35 = |g| - 1 + 0.7 L
```

V37 adds one context-dependent deduction. It applies only when the ranked loser is brown
and the winner is copper or amber. Let P+ and H+ be the positive winner-favoring provenance
and shade contributions, respectively:

```text
F = max(0, (winner_tare - 120)/10) * (P+ + H+) if eligible; otherwise 0
premium_decision_v37 = |g| - 1 + 0.7 L - 0.75 F
```

These adjustments do not change g or the ranked winner. V37's reporting score is
premium_decision_v37 + 1, not |g|. Its independently selected reporting band happened to
have the same endpoints as V28's; that does not make the scores interchangeable.

Both corrections are hypotheses about supplied preferences, not measured economic laws.
The contextual feature was motivated by reviewed errors. Its subsequent historical
cross-validation is not equivalent to a new prospective discovery.

Sources: [V35 implementation](predictor_premium_v35.py),
[V37 implementation](predictor_premium_v37.py), [V37 configuration](premium-config-v37.json).

## 5. Intrinsic ranking and exact equality

A separate experimental intrinsic model used 21 coefficients: nine provenance offsets,
four shade increments, four vintage increments, and four tare increments. Its pair score
is a true difference of per-offering utilities. It learned monotone curves and constrained
total attribute ranges to vintage > tare > provenance > shade, separated by a small
numerical margin. This is full-range ordering, not universal per-step dominance.

Its directional objective was squared hinge loss plus ridge regularization:

```text
min_w  mean_i max(0, 1 - d_i * delta_phi_i · w)^2 + lambda ||w||^2
```

Later versions imposed confirmed training equalities as delta_phi_i · w = 0 and required
small positive margins for explicit single-feature directional preferences. This corrected
five small-preference collapses caused by a shade increment being driven to zero. It did
not establish broad exact-equality generalization.

For a compatible intrinsic model, confirmed identity vectors form a matrix E. If E w = 0
and a new feature difference delta lies in row-span(E), then delta · w = 0. This is a
model-relative linear implication. The certificate in [equality_span.py](equality_span.py)
also checks the reference gap numerically and rejects incompatible weights.

It is not applied to V28's pair-context score. We do not infer equality by chaining
approximately close pairs. The prior certificate audit checked the then-current identities
and strict labels; it does not certify every subsequently elicited equality. In particular,
the new equality in the 20-pair test was not recognized by either frozen reporting model.

The older Western Europe equality was representable alongside its nearby strict preference,
but could not be independently identified when the family containing that relationship was
withheld. Small valid tare-step changes moved the predicted balance while preserving training
winner counts and other constraints. That is an identification limitation in the tested
representation, not proof that exact equality is intrinsically unknowable.

Sources: [positive-margin ranking results](positive-summary-v33.json),
[local balance audit](local-balance-audit-v34.json).

## 6. How validation was performed

The recurring family key is the unordered provenance pair combined with the unordered
shade pair. Age/tare variants stay together. Five outer folds are repeated using five
seeds; appropriate tuning occurs inside training partitions. Repeats are correlated:
five results for one comparison are not five independent observations.

For a known size label y in {0,1}, binary size accuracy is mean(1[predicted_y = y]).
Joint accuracy additionally requires the supplied direction or exact relation to match;
unknown axes are never guessed. Tables explicitly identify the applicable denominator.

With an abstention band, let K be the retained observations:

```text
coverage = |K| / number_of_size_labels
retained_size_accuracy = correct_retained_size_calls / |K|
```

Abstention is not scored as a correct prediction. We separately count false meaningful
premiums, missed meaningful premiums, and true premiums withheld in the band.

Three evaluation regimes must remain distinct:

- **Full-data fit/rescore:** describes known data, not generalization.
- **Historical family validation:** exploratory after many rounds of model selection.
  Frozen V28-based corrections have historical training exposure in their base model;
  only the new correction or reporting calibration is withheld.
- **Frozen prospective elicitation:** predictions and rules are sealed before responses.
  The sets are small, targeted stress tests, not representative population samples.

Repeated tuning, targeted question selection, and revisiting labels limit inference.
Neither a stable training fit nor high retained accuracy proves calibrated confidence.

## 7. Results that control the decision

### Fresh 12-pair combined-model pilot

| Measure | V28 | Combined intrinsic-rank candidate |
|---|---:|---:|
| Direction correct | 11/12 | 10/12 |
| Size correct | 9/12 | 9/12 |
| Both correct | 8/12 | 7/12 |

The combined model did not justify replacement. Incorrect spoken descriptions were corrected
with verified tables before recorded answers; this delivery issue is retained in the receipt.
Source: [pilot results](combined-pilot-v34-results.json).

### Fresh 16-pair reporting test

V28 direction was 14/16. Original size accuracy was 11/16 and joint accuracy 9/16.
One answer was corrected after prediction disclosure, producing 12/16 size and 10/16
joint accuracy; those revised counts are not a new independent prospective result.
The band withheld one call. Three false premiums remained outside it.

Sources: [original results](prospective-reporting-v1-results.json),
[post-disclosure correction results](prospective-reporting-v1-corrected-results.json).

### Fresh 20-pair V28 versus V37 test

| Measure | V28 | V37 |
|---|---:|---:|
| Direction correct on strict labels | 18/19 | 18/19 |
| Explicit equalities recognized | 0/1 | 0/1 |
| Binary size correct | 14/20 | 14/20 |
| Value relation and size correct | 13/20 | 13/20 |
| Calls retained after boundary filtering | 18/20 | 17/20 |
| Size correct among retained calls | 14/18 | 14/17 |
| False meaningful premiums retained | 4 | 3 |

The only category change was question 3: V37 withheld a premium that V28 called meaningful;
the expert judged exact equality. This was useful abstention, not equality recognition.
No genuine premium was withheld or missed in this set. V37 did not improve binary size or
joint accuracy and therefore did not earn default promotion.
Source: [sealed test results](prospective-v37-results.json).

### Historical uncertainty-band calibration

On evidence v37, the 25-fold mean conditional results were:

| Measure | V28 | V37 |
|---|---:|---:|
| Coverage | 90.02% | 90.81% |
| Retained size accuracy | 95.23% | 96.85% |
| False premiums | 3.6 | 0.4 |
| Missed premiums | 15.0 | 12.0 |
| True premiums withheld | 32.8 | 30.2 |

These historically favorable results did not establish an error-free clear zone on fresh
questions. Source: [band calibration](reporting-calibration-v37.json).

## 8. Why the attempted repairs were not adopted

Several failures provided useful constraints on future reasoning:

- A shared shade–tare interaction improved ranking only marginally and did not reliably
  transfer the motivating cases. Those cases were later clarified as exact ties, illustrating
  the danger of optimizing against an interpretation the expert does not endorse.
- Broad older-brown attenuation reduced historical ranking accuracy: unchanged structure
  93.98%, 25% attenuation 93.20%, 50% attenuation 90.61%. It pushed the unresolved balance
  toward the wrong outcome rather than learning equality.
- Generic opposition discounts selected zero in all 25 folds for both tested formulations.
  Forcing a penalty to fix two false premiums reduced full-data size correctness from
  391/413 to 366/413: false premiums fell 10 to 6, but missed premiums rose 12 to 41.
- The later one-coefficient heavy-tare/near-shade correction improved conditional calibration
  and preserved controls, but its fresh 20-pair test produced no binary-size improvement.
- The final independently specified contextual premium head also failed its acceptance gate.

The last head used 22 coefficients: 13 generic pair/context features and nine regularized
regional shade deviations. It optimized equal-per-case logistic loss with ridge regularization,
train-only scaling, three-fold inner selection, and a fixed 0.5 classification threshold.
Ranking remained frozen. Its protocol was recorded before fitting; features were not revised
after seeing the results.

On development evidence v38:

| Measure | Frozen V28 | Frozen V37 | New head, withheld-family mean |
|---|---:|---:|---:|
| Size correct | 418/453 | 425/453 | 397.8/453 |
| False premiums | 20 | 16 | 25.0 |
| Missed premiums | 15 | 12 | 30.2 |
| Direction and size correct | 235/271 | 242/271 | 216.0/271 |

The new head's full-data size score was 411/453. It preserved tested controls but performed
worse broadly. This comparison is an operational gate, not a perfectly independent whole-model
contest: frozen references had historical exposure, whereas the new head was family-withheld.

Sources: [brown experiment](brown-summary-v34.json),
[opposition experiment](premium-opposition-decision-v35.json),
[V37 correction](premium-context-selection-v37.json),
[final head protocol](context-head-protocol-v38.json),
[final head decision](context-head-decision-v38.json).

## 9. Independent peer review

Fable's E1 reporting analysis was independently reproduced, including the selected band
and its coverage costs. E2/E3 receipt source hashes and summary arithmetic were verified;
the scratch refits were not rerun in this project session.

The reported E3 margin-target experiment scored 93.63% baseline directional accuracy,
91.86% with targets 0.25/1.0/1.5, and 93.46% with 0.5/1.0/1.25. Later “slight” clarifications
could lose influence to earlier, less precise unqualified judgments. Magnitude adjectives
are not evidence-reliability weights.

These experiments reject specific formulations. They do not prove that every alternative
loss fails or that residual error is necessarily irreducible noise. The peer's equality-span
recommendation is restricted to a compatible intrinsic representation and audited for strict
preference conflicts; it is not a universal pair-comparator theorem.

Sources: [peer review](peer-review-v35.md), [E1](peer-review-e1-step1-v35.json),
[E2](peer-review-e2-v35.json), [E3](peer-review-e3-v35.json).

## 10. What the remaining errors mean

The model commonly gets the winner right while overstating the size of the advantage.
The expert distinguishes being better than a poor alternative from commanding a substantial
premium. The current additive score-to-size mapping does not consistently express that.

The latest questions 13, 14, and 16 were all slight preferences for 30-year offerings, but
their mechanisms differ: shade alone; shade plus tare; and vintage/tare offset by provenance.
A universal brown penalty, age penalty, or opposition discount is not supported.

A concrete limit on threshold tuning is visible within Southeast: the model scores a
30-year copper/110 versus brown/120 advantage more highly than a 20-year copper/115 versus
brown/120 advantage, while the expert judges the former slight and the latter meaningful.
No monotone cutoff on that fixed score can classify both correctly.

This establishes a limitation of that score ordering, not an impossibility theorem about
all models. Sparse context support, historical label interpretations, experimental selection,
and representation choices remain plausible contributors. See
[the final prospective diagnosis](prospective-v37-premium-diagnosis.json).

## 11. Operational expectations and boundaries

Use the reference to propose a comparative ranking and a premium category, with the raw
score and uncertainty status available for inspection. Treat subtle or economically consequential
comparisons as requiring judgment beyond this model. Do not present score units as currency.

Known limitations:

- Meaningful-premium errors occur both inside and outside the reporting band.
- Directional confidence has not been probability-calibrated.
- Exact equality is not generally predicted by V28; no tie band is substituted for it.
- Small targeted prospective sets cannot establish population accuracy.
- The model's constrained input lattice does not validate interpolation to arbitrary weights,
  vintages, new regions, or additional hidden attributes.
- There is no measured scarcity model, objective market-price truth, or inventory-demand model.
- V28 pair-context adjustments do not guarantee intrinsic monetary-price consistency.
- Strong performance on obvious extremes does not demonstrate a learned rarity mechanism.

## 12. Lock and reopening policy

The lock is a reproducible reference-state agreement backed by hashes, not operating-system
write protection. [model-lock-2026-10-31.json](model-lock-2026-10-31.json) identifies the locked
runtime/configuration, evidence, test receipts, and this audit. Run:

```sh
.venv-regional/bin/python verify_model_lock.py
```

V28 is the default. V37 and the contextual head retain their experimental/rejected statuses.
No automatic training, background search, or questionnaire is scheduled. Future changes require
an explicit new scope, a new version rather than overwriting baselines, an independently stated
hypothesis, training-only selection, preserved label semantics, and a genuinely untouched test.
A gain on already examined comparisons alone is insufficient for promotion.

Reopening is justified by new independent evidence, a verified implementation defect, or a
materially different mathematical hypothesis with a bounded test. Merely moving a band until
known errors disappear is not sufficient. Current observed limits remain documented even if
future versions improve them.

## Appendix A Exact retained coefficients

The following table is generated directly from the retained V28 configuration. Runtime
configuration and its SHA-256 in the lock manifest are authoritative.

| Feature | Coefficient |
|---|---:|
| `provenance:Western Europe` | 0.307804615385313 |
| `provenance:West Central Asia` | -0.6921753846154 |
| `provenance:South/Eastern Asia` | -0.692185384614687 |
| `provenance:West Asia / Middle East` | -0.99999 |
| `provenance:central` | 0.0770061538469424 |
| `provenance:northeast` | 0.538553076923578 |
| `provenance:northwest` | -0.230678461538158 |
| `provenance:southwest` | 0.153952307692724 |
| `provenance:southeast` | 0.0770561538470478 |
| `shade_increment:copper` | 1.30772461538521 |
| `shade_increment:amber` | 0.230738461538265 |
| `shade_increment:golden` | 0 |
| `shade_increment:pale/straw` | 0.0769061538457811 |
| `vintage_increment:35` | 0.538503076923471 |
| `vintage_increment:30` | 1.30776461158989 |
| `vintage_increment:25` | 1.30771461538521 |
| `vintage_increment:20` | 1.23082846153943 |
| `lower_tare_per5lb` | 0.538493076923471 |
| `matched_provenance_five_year_golden_pale` | 0.53841307692231 |
| `younger_five_lb_heavier_compensation` | 0.538493076923471 |
