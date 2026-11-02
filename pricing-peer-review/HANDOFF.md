# Locked domestic pricing reference — November 1, 2026

**Domestic Release Pricing v2 is now locked as a provisional reference schedule.**
Its scope is Northeast, Southeast, Central and Northwest seat-origin/reference offerings,
whole filled casks, matching volume, mint condition and comparable initial-release
 distributor/insider terms. Prices are USD and exclude fees, taxes and delivery.

- Reference: [pricing/domestic-release-reference-v2.md](pricing/domestic-release-reference-v2.md).
- Entry point: `pricing/domestic_release_pricing.py`.
- Scope and configuration: `pricing/domestic-release-policy-v2.json` and
  `pricing/consistent-price-config-v2.json`.
- Pricing lock: `pricing/pricing-lock-v2.json` — 33 artifact hashes.
- Workbook: [pricing/consistent-prices-v2.xlsx](pricing/consistent-prices-v2.xlsx).

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

## Pricing low-end refined — separate v2 layer, V28 still locked

Currentpricingentry pricing/consistent_price_v2.py withconsistent-price-config-v2.json.
TwoNortheast expertknots:amber35/120=450center;brown40/130=300ceiling-activeendpoint.
Prior5knots,allregionalanchors,10previouslyfittedchecks and230in-spanprices unchanged.
14tests pass;1250positiveprices,3000monotonicchecks,3750referencechecks. Workbook
pricing/consistent-prices-v2.xlsx recalculated6294formulas,allpricesverified.
No globalcostfloor/marketvalidation claimed. Sharedlow-endcurve transfers tootherregions
assumptively; sixregions stillunanchored. Currentgrid no longerextrapolates in scalar loss,
but mostofferingcombinations remainunvalidated. Fullreceipt pricing/consistent-price-verification-v2.json.
Previouspricingconfigsv1 andall46lockedV28artifacts unchanged. Noquestionnaire/job pending.

## Low-end pricing analysis completed — curve not consolidated yet

Internalreasoning updated first in pricing/README.md. low-end-curve-analysis-v1.json compares
3positive monotone tails thatmatchcalibration andboundaryslope. Same230in-spanprices;1020profiles
remainextrapolations. LowestNEprofile scenarios~120/271/357USD;NW~109/246/324. No preferredtail,
marketconfidenceinterval,or costfloor established.9,000adjacentchecks pass across3scenarios.
Consolidate canonicalpricingstructure andscopeflags, notunidentifiedtail. V28 unchanged.
Next pricingquestion: NEseat-origin amber35years120lb; expectedexpertprice/range requested
before its frozen scenarios are disclosed. State in pricing/low-end-checks-v1.json.
No questionnairebeyondthispricingcheck started; no refit orbackgroundjob.

## Current next phase — low-end pricing curve assessment

The canonical pricing layer fixes reference dependence,negativeprices and attribute-order
violations, while leavingV28 unchanged. Read pricing/README.md for insightsandreasoning.
Localplausibilityfit isnotmarketvalidation:10acceptedvalues,4non-topprofiles,4actualtopanchors;
1,020/1,250profiles extendpast supportedloss. Current exponentialtail is anassumption.
Next comparepositive monotone tails withidentical calibratedregion andboundaryslope;
retaincurrentconfig anddo notinventfloors. Consolidation mustseparate validatedarithmetic,
localcalibration,unsupportedtail andunanchoredregions. Noexistingmodel/default change.

## Latest pricing layer — reference consistency fixed separately from V28

Read pricing/README.md andpricing/consistent-price-verification-v1.json.
Newcanonicalpricing: regionalanchor × exp(-monotone logdiscount(baseattribute loss)).
Pair-context terms excludedfrommoney; V28weights andcomparativeengineunchanged.
Fouractualanchorprices exact;10acceptedhypotheticalprices fitMAE$5.97,max$16.07.
Only4unique non-topprofiles; leaveprofileoutMAE$39.73 andcombinedprofileheldout errors$65–88.
All1250pricespositive;3000adjacentorderingchecks,3750referencechecks,6unittests pass.
Workbook pricing/consistent-prices-v1.xlsx recalculated,5060formulas verified,noerrors.
Oneprice peroffering nowindependent ofreference; price differences telescope.
Still1020profiles extrapolated;6regions lackrealanchors. Nopriceconfidenceguarantee or
actualmarketvalidation. Oldinconsistentgridretained asdiagnostic,notactivepricefunction.
No questionnaire orbackgroundjob. Original46artifactlock verifiedintact.

## Latest pricing stress test — complete grid, structural issues identified

pricing/all-region-price-grid-v1.xlsx contains formula-driven1250offering grid over10regions,
plusinputs,regionalbounds,issues andconsistencyexamples. JSON/CSV counterpartsand
pricing/price-grid-findings-v1.json preserve reproducibility. FrozenV28weightsunchanged.
4providedseatanchorprices;6regionalanchors inferredfromNW andNOT independentlypriced.
Linear andlog mappings both anchored atNE/NW endpoints,known4regionsuseownanchorprices.
Their min/max isassumptionsensitivity,notmarket/confidenceinterval. No genericregular-batch
discountapplied outsideoriginalmatchingtopprofiles.

Findings:15nonpositive linearprices;50shade-order violations (golden25yr about70USD belowamber);
190profiles haveintermediate-anchor path differences upto140USD;580same-region pair-order
reversals againstprice-list (540withbothimpliedandlistedgaps above1USD);529profileslinear/log
differby>25%oflargerabsoluteestimate. E.gNEgolden25/115direct790versusvia25yrpaleanchor860.
NegativeNWbrown40/130about-60USD;logalternative364USD isnotvalidatedreplacement.
Nextfocus: coherent per-offering pricing representation andanchorconsistency beforelow-end
curve/floorselection; realpriceanchorsneededforunanchoredregions. Do notsilentlyclipprices.

Workbook7594formulas recalculatedbyheadlessLOconversion;nocachedformulaerrors,all1250linear/log
values matchPython. Interactivecanvas at/Users/stefansassoon/.cursor/projects/Users-stefansassoon-projects-wine/canvases/cask-price-grid.canvas.tsx. No weightingchangeornewpricegroundtruth.
Original46artifactlock verified. No processespending fromrecalculation.

# Current handoff — v39 reconciled; pricing is the next phase

Start with the current section at the top of README.md.

**Keep V28 locked.** No new winner-withholding rule was adopted. V39 contains666activepairs
plus25separatelydeferred historicalpairs,691unique total. The60reviewedpairs supersededexisting
records once:28labelchanges,32reaffirmations. Active labels494directions/442sizes/5exactties.
Read evidence-v39-change-summary.json andfixed-model-rescore-v39.json; predictionsunchanged,
scorechangesreflectlabels,notrefitting. Original46artifactlockstillrefers toitsv38snapshot.

Reporting-only test:44reviewednondirections,494strictpreferences,123confirmedslights. Scorecutoff
recovered0inallrepeats;context recovered0,2,2,0,0 while incorrectlywithholding0,0,2,1,0otherstrict
judgments. No slightpreferences lost, butcoverage too limited; fullfitwithheldnothing. Decision:
retainexistingranking/premiumreporting. See direction-reporting-decision-v39.json. No further
preference-model search or A/Bquestionnaire pending.

**Next phase: determine whether established prices for known cask offerings can support
monetary pricing estimates.** Begin with available priced-offering records and target units:
wholecask/contents/vessel/perunit, currency/date/source, transaction versusasking/expertvalue,
volume/condition and includedfees/taxes/delivery. Tare isnotcontentsvolume. Preserve rawrecords.
Do notinventanchors or turncomparisonscores directly into dollars. V28pair-contextscores need
not be globallyconsistentindividualvalues; establish comparability andidentification first.

If data permit, benchmark a separate versionedpricinglayer againstsimplecomparables onheldout
casks/offerings (andtimewherepossible), avoidrelated-transaction leakage, reportmonetaryerrors
andrange coverage, andstateunsupportedextrapolation. KeepV28weights unchanged. Existingpremium
bands are not dollarconfidenceintervals. No pricingfit ordata collection performed yet.

Modelaudit/manifest remainintact. Externalreview closed andpublicrepodeleted; localarchive
retained. No backgroundjobs. Earlier instructions below are historical; do notresume oldtests.

---

## Latest reporting-only test — no new direction gate adopted

See direction-reporting-decision-v39.json. FrozenV28;44reviewednondirectionspositive,
494strictnegative(including123confirmedslights).5exacttiesand123othernondirections excluded;
25deferredpairs separate. Scorecutoff recovers0/44eachrepeat. Contextclassifierrecovers
0,2,2,0,0; strictfalsewithholding0,0,2,1,0. Confirmedslightloss0allrepeats. Fullfitwithholds0.
Meanrecovery0.8/44notuseful;noadoption, nointegrationorfurthertuning. TrainingonlyinnerOOF
ridge/thresholdselection andouterfamilyexclusions verified. Model/premiumband unchanged;
46lockedhashesverified. Conditionalreportingtest,notfreshmodelvalidation. Noquestionnaire/job.

## Latest evidence update — v39 reconciled, fixed models rescored

Userrequested incorporation of60reviewedcomparisons withoutrefit. Read evidence-v39-change-summary.json
and fixed-model-rescore-v39.json. 60existingpairs supersededonce:28scoringlabelchanges,32reaffirmations.
25unasked matched-domesticpairs areseparate in deferred-pairs-v39.json and evidence-v39.deferred_pairs;
no inferredanswers.666active+25deferred=691unique;no newpairs. Reviewedstates14strictslight,
44practical/unspecifiedties,2explicitexactequalities. Allpriorrecords andrawreviewhistoriesretained.
V39active labels:494directions,442sizes,5exactties. Allsixfixedruntime predictions matchedsaved
ensembleoutputs on691pairs. Same666cohort before/after: V28size393/428→412/442,joint235/275→235/275;
V37size400/428→419/442,joint242/275→242/275. Label/maskchanges,notlearning; jointmembershipchanges
despiteequaldenominator. No defaultpromotion/refit; V28lockedreference remainsunchanged(v38snapshot
stillinsideoriginalmanifest). Sourcehashesverified. Reviewguidance retainedbutnotexpanded aslabels.
Noactivequestionnaire orbackgroundjob. Nextaction requiresuserscope.

## A/B disagreement review — all six saved items resolved

The60individuallyreviewed pairs in direction-disagreement-review.json nowhavefinalanswers;
noexplicitunresolved item remains. Saveditems34,42,43,53,58,60revisited withhistoriesretained.
25repetitive matched-domestic comparisons remain unasked/deferred, notsyntheticallyanswered.
Modelsfixed; no refit or evidence reconciliation. Nextstep onlywhenrequested: reconcile
reviewedpairs once into a newevidenceversion, retaining distinctions andrule-scopelimits.

## A/B disagreement review checkpoint — nonredundant pass finished

Question60savedforlater/unresolved. direction-disagreement-review.json contains60reviewed
pairs including6explicitunresolved:34,42,43,53,58,60. Remaining25unaskedpairsarethe matched
domestic comparisons deliberatelydeferredafterusergeneral guidance; no syntheticlabels.
Nextquestionnull, statusreviewed_nonredundant_pairs. Do notresume repetitivequestions or
markall85individuallyanswered. No evidence reconciliation or refit authorized/performed.
Modelsremainfixed. Rawanswers, exact/practical distinctions, andconditionalguidance preserved.

## A/B disagreement review paused after question50

Userrequestedbreak. Answers1–50saved in direction-disagreement-review.json; resumeat51
usingitscurrentorder. Questions34,42,43remainexplicitlysavedforlater/unresolved. Repetitive
matched domestic pairs remain deferred; no syntheticanswersadded. Modelslockedandfixed;
reviewclarificationsnotyetreconciledintotrainingevidence. Noquestionsuntiluserresumes.

## Active review paused at user request

A/B disagreement review saved in direction-disagreement-review.json. Questions1–38
recorded; question34 explicitly savedforlater/unresolved. Resume withquestion39 using
savedorder, notoriginalsourceorder: repetitive matched domestic comparisons were deferred
followinguserguidance. Keepmodelsfixed. Bare/preference ties are not automaticallyhard
exactequalities; onlyexplicitexactjudgments have exactflag. No evidence reconciliation or
refit performed. Userrequestedbreak; do notcontinuequestionsuntilresumed.

# Final closeout — V28 remains locked

The user confirmed the final decision after the bounded ensemble test: **retain V28 as
the locked reference/default and close this development cycle.** No model search,
questionnaire, background experiment, or follow-up is pending.

## Ensemble result and decision

Six frozen configurations were evaluated with a shallow, context-based whole-answer
selector. Depth0/1/2 was selected within training families; each leaf required at least
20 complete-label training pairs. Five family folds were repeated with five seeds.
No question IDs, answer lookups, or expert coefficient changes were used.

| Measure | V28 | Training-selected single model | Ensemble | Strongest individual, V37 |
|---|---:|---:|---:|---:|
| Relation and size correct, out of275 | 235 | 238.8 | 237.2 | 242 |
| Size correct, out of453 | 418 | 422 | 420.8 | 425 |
| False meaningful premiums | 20 | 18.6 | 18.8 | 16 |

Fractional counts average five repeats. The joint denominator includes four explicit
equalities. The strongest individual is a descriptive comparison, not a prospective
promotion result. V37 remains experimental because earlier fresh tests did not establish
a replacement advantage.

The selector achieved247/275 on the full data but only237.2/275 on withheld families.
Inner validation selected depth0 in15/25outerfolds. The hindsight best-expert upper bound
was264/275; that is not deployable accuracy. The ensemble did not beat the training-selected
single model or V37, and is **not adopted**. Only the selector was family-heldout; frozen
experts have historical evidence exposure. Do not present this as fresh whole-model testing.

Sources: [protocol](ensemble-protocol-v38.json), [validation](ensemble-validation-v38.json),
[decision](ensemble-decision-v38.json), [locked audit](model-audit-2026-10-31.md).
The ensemble is a separately authorized post-lock experiment; the original locked audit,
manifest, model weights, configurations, and evidence snapshots were not rewritten.

## Reference and verification

- Default: V28 via `predictor_reporting_v2.py` and `reporting-config-v2.json`.
- V37: experimental, not promoted. Contextual premium head and bounded ensemble: rejected.
- Latest development evidence: `evidence-v38.json` / `benchmark-targets-v38.json`.
- Lock: `model-lock-2026-10-31.json` (46 artifact hashes).
- Verify: `PYTHONDONTWRITEBYTECODE=1 .venv-regional/bin/python verify_model_lock.py`.
- Peer review is merged and archived locally; the temporary GitHub repository is deleted.
  Closure receipt: `external-reviews/2026-10-31-hermes/closure/closure-receipt.json`.

Any future investigation requires explicit new scope, a separately recorded hypothesis,
new versioned artifacts, and an untouched evaluation plan. Do not automatically restart
ensemble searches, revisit expert answers, or retune the uncertainty band. Earlier active
or pending instructions below are historical and superseded by this closeout.

---

## Latest authorized bounded ensemble test — not promoted

See ensemble-decision-v38.json and ensemble-validation-v38.json. Predeclared6frozenexperts;
shallowwhole-answerselector depths0/1/2,20completepairs minimumleaf,trainingonlyinnerselection,
25outerfamilyfolds. Jointmean237.2/275 vsV28 235,trainingselectedsingle238.8,strongestindividual
V37 242. Size421-ishmean versusV37 425. Fullfit247notgeneralization. Oracle264/275 ishindsight
upperbound only. Depth0selected15/25folds. Rejectpromotion; no feature/depthsearchafterresults.
Original46artifactlockverified; V28defaultunchanged. Conditionalgatevalidation,not independent
wholemodeltest (frozenexperts historicalexposure). Noquestionnaire/backgroundjob. Reviewlock
andoriginalauditpreserved; thisseparatelyauthorizedexperiment storedoutside lockmanifest.

# Peer review fully closed — model remains locked

GitHub authorization refresh completed. Temporary repository
SassoSte/wine-model-peer-review-2026-10-31 was deleted successfully; an authenticated
owner API request now returns404. The review PR had already been merged.

Review, diagnostic, our assessment, PR discussion/metadata, and full Git history are
preserved in external-reviews/2026-10-31-hermes/closure/. Every archived file checksum
was reverified and review-repository.bundle passed Git verification after deletion.
See closure-receipt.json there for the final receipt. The local repository checkout and
original ZIP are retained. No remaining deletion blocker or remote cleanup is pending.

V28 remains locked/default; V37 experimental; contextual head rejected. No models,
thresholds, evidence, locked audit, or manifest changed. Earlier statements below about
pending authorization or a private repository are superseded by this closeout.

---

# Peer review closeout — model remains locked

The review PR was merged at commit4129ff04c13cbfcb081c1e65fe8cac84a5422e86.
Review,diagnostic,ourassessment,PRcomments/reviews/commits,repositorymetadata,andfullGit
history are preserved under external-reviews/2026-10-31-hermes/closure/.
review-repository.bundle passedGitverification;closure-receipt.json recordschecksums.

**Public access removed; permanent deletion pending.** GitHub rejecteddeletion withHTTP403
becausecurrentCLIauthentication lacksdelete_repo scope. Repositorywasmadeprivate instead;
authenticatedAPIconfirmsprivate andanonymousAPIreturns404. Do notclaimitwasdeleted.
Temporaryrepo: SassoSte/wine-model-peer-review-2026-10-31.
Tofinishdeletion, obtainappropriateGitHubauthentication (gh auth refresh -h github.com -s
 delete_repo requiresuserauthorization) orownerdelete throughGitHubsettings, thenverify.
Do notrepublish,rewritemodels,orstartnewexperiments. All46model-lockartifacthashesremain
unchanged. V28default,V37experimental,contextualheadrejected. Noactivequestionnaire or
backgroundmonitor. Originalreviewandourqualifiedassessmentremainseparate.

---

## Final peer review received — lock retained

Hermesreview PR: https://github.com/SassoSte/wine-model-peer-review-2026-10-31/pull/1
Open/unmerged atinspection;head0dae9a4999cbe8e39f607f84bb31d0c2d32ba3b4. Originalreviewand
diagnostic preserved underexternal-reviews/2026-10-31-hermes/. Diagnostic independently
reproduced. assessment.json recordsacceptanceofpauseandqualifications: correctedlabeldoesnot
proveunstablepreference; approximate1/13gridisnotexact,norlegacycutoff1.5; onefailedheadnot
universalimpossibility. No newtests/refits/questionnaire scheduled. Packet/modelremainlocked;
publicrepo notdeleted andPRnotmerged. Awaituserdirection beforeclosingreview workflow.

## Public peer-review repository — awaiting external review

Published and verified public: https://github.com/SassoSte/wine-model-peer-review-2026-10-31
Remote main matches local commit; receipt in peer-review-public-repo.json.
Reviewer starts at repository README and submits in reviews/ through a fork/PR unless
explicit collaborator access is granted. Public visibility alone doesnotpermit directcommits.
Original model lock remains intact. No monitoring or deletion job scheduled. Once user says
review is complete, preserve review submissions/receipts/discussion locally before removing
the public repository. Do not infer completion or delete it automatically.

# Awaiting final peer review — model remains locked

The final review packet is ready for the external reviewing agent. Review completion or
submission is not implied by packet creation. Resume here when the user supplies the review.

## Packet and verification

- ZIP: [peer-review-final.zip](peer-review-final.zip) (11,235,624 bytes; approximately 11 MB).
- Entry inside ZIP: `peer-review-final/start-here.md`, then `peer-review-final.md`.
- Review prompt: [peer-review-final.md](peer-review-final.md).
- Audit: [model-audit-2026-10-31.md](model-audit-2026-10-31.md).
- Packaging receipt: [peer-review-final-package-receipt.json](peer-review-final-package-receipt.json).
- ZIP SHA-256: `900c0246c5a4ddfb13df1a490648de9cd42ae05b1177abdec067752cb35a9ed2`.
- Contents: 547 project files plus start instructions, numerical dependency
  versions, and package manifest (550 files total). Includes code, weights,
  evidence, prospective results, peer receipts, and supporting local dependencies.
- Verification completed: ZIP integrity; every payload checksum; all 46 locked artifact
  hashes; extracted-copy lock verification; all nine reporting tests. Original project
  source files remained unchanged. No virtual environment is included.

## Resume when the review returns

1. Read the complete returned review and any calculation receipts. Establish which packet,
   model, evidence version, and files were reviewed. Distinguish verified findings from
   recommendations, hypotheses, and claims based only on the prompt.
2. Compare the findings with the locked audit and prior rejected experiments. Identify
   genuinely new mathematical mechanisms, implementation defects, or validation concerns.
   Do not restart an earlier failed approach merely because it has a different name.
3. Report a concise disposition for each material finding: verified/actionable,
   needs verification, already covered, or unsupported. Reproduce bounded read-only checks
   where useful; do not describe unreproduced calculations as independently confirmed.
4. Recommend whether to retain the lock or propose one separately scoped experiment with
   explicit success/failure criteria, preservation checks, and untouched validation.
   Receiving a review alone does not authorize refitting, relabeling, changing thresholds,
   replacing defaults, or launching another questionnaire.
5. Any authorized future model change must use a new version and preserve this reference,
   its evidence history, and the original prospective test results.

## Locked state

V28 remains the default/reference through `predictor_reporting_v2.py` and
`reporting-config-v2.json`. V37 remains experimental; the v38 contextual premium head is
rejected. The latest development evidence is v38. The lock manifest remains
`model-lock-2026-10-31.json`; verify with:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv-regional/bin/python verify_model_lock.py
```

Only documentation was updated for this checkpoint. No model, configuration, threshold,
evidence, locked audit, ZIP payload, or lock manifest was changed. No background work,
review monitoring, or questionnaire is scheduled.

---

# Locked reference and completed audit — 2026-10-31

**V28 is locked as the reference/default. Model search is paused.** V37 remains
experimental; the separate v38 contextual premium head was rejected. No automatic
questionnaire, training, or background job is pending.

Start with [the model audit](model-audit-2026-10-31.md). It records the objective, evidence
history, exact mathematics and coefficients, validation methods, prospective outcomes,
failed experiments, operational expectations, known limitations, and reopening criteria.
The audit supersedes older “next step,” “active,” and “pending” statements below.

- Runtime: `predictor_reporting_v2.py`, default `v28` in `reporting-config-v2.json`.
- Evidence snapshot: `evidence-v38.json` / `benchmark-targets-v38.json`.
- Reproducibility manifest: `model-lock-2026-10-31.json` (46 artifact hashes).
- Verify: `.venv-regional/bin/python verify_model_lock.py`.
- Reporting tests: `.venv-regional/bin/python -m unittest test_reporting test_reporting_v2 -q`.

Latest checks: all46hashes verified,691unique pairs andlabelcounts verified,9tests passed.
Lock means an explicit reproducible reference, not filesystem write protection. Premium
uncertainty isnot calibrated probability; exact equality isnot inferred from theboundaryband.
Fresh tests didnotjustify promotingV37. Historical94%ranking isnot jointpremiumaccuracy.
Futurework needs explicitnewscope/version anduntouchedvalidation; donotreopen casepatching
or reinterpret confirmedanswers tofit predictions.

---

## Latest completed experiment — separate contextual premium head rejected

Read context-head-decision-v38.json. Userauthorized newphase; protocol frozenbeforefit in
context-head-protocol-v38.json. Evidencev38adds20prospectivepairs once=691pairs;453sizelabels,
285direct,271strictdirection+size.22coefficientlogistichead (13genericcontext +9regionalshade
terms),ridge .001/.01/.1/1 selectedtrain-onlyinner3familyfolds,25outerfamilyfolds. Rankingsfixed.
Mean size397.8/453 versusfrozenV28 418 andv37 425; false25vs20/16; missed30.2vs15/12;
joint216/271vs235/242. Failsdeclaredgate. Reject; no defaultchange orpostresulttuning.
Baselineshistoricallytrained so comparisonconditional, notfreshwholemodelcontest. Swapsymmetry
691cases verified. Fullfit/controlresults inreceipt. Noquestionnaire/backgroundjob.
Do notinterpret failure asproof allcontextualmethods impossible oruserjudgmentsnoise.

## Latest read-only diagnosis — stop local tuning

prospective-v37-premium-diagnosis.json analyzesQ13/Q14/Q16. Allwinners30yr, but mechanisms
differ:Q13purebrown→amber withregionalcounterexample(round45-14);Q14shade+tarewithsameSE
20yrQ18meaningful counterexample;Q16vintage+tare/provenance,noshadecontrast. ScoreQ14>Q18
butlabelslight<meaningful rulesoutone monotonecutoff. Q13/Q16justaboveband1.5;Q14not.
Do notblanketsuppress30yr/lowshade/110lb:earliermeaningfulcounterexamples exist.
Recommendationstoplocalcoefficient/bandpatching,keepV28defaultandv37experimental; anyfuture
contextualpremium redesign requiresseparatescope anduntouchedvalidation. No fit/evidence
change/questionnaire/job. No claimthat residualsproveirreduciblenoise.

## Latest completed prospective test — v37 vs V28, 20 pairs

Read prospective-v37-results.json. Frozenhashes verified, no refit. Q14corrected toAslight
beforepredictiondisclosure, original preserved. Both direction18/19strict; exactQ3missed.
Both binarysize14/20 and relation+size13/20. V28retains18calls,size14/18;v37retains17,
size14/17. OnlychangedclassificationQ3:V28meaningful→v37borderline,actualequal.
V37retainedfalsepremiumsQ13,Q14,Q16;V28alsoQ3. No genuinepremiums withheld/missed.
Q9,Q20borderlineboth;Q2directionreversalboth. No evidenceof improvedbinarysize accuracy;
keepV28default, v37experimental. NewcontrolanswersQ13/Q14slight showlower-tarecontrols
arenotautomaticallymeaningful; do not silently widen gate or reinterpretanswers.
No questionnairepending; sealedsetcomplete, answersnotincorporatedintrainingyet.

## Latest completed calibration — v37 reporting and fresh frozen set

Read reporting-v37-readiness.json andreporting-calibration-v37.json. Newentry
predictor_reporting_v2.py/config reporting-config-v2.json supports explicitv28/v37;
defaultremainsv28. Bothfullcalibrations select[1.0,1.5),butv37uses correctedpremium
score+1,notrawgap. Same25familyfolds,15%trainingabstentioncap: V28mean90.02%coverage,
95.23%retainedsizeaccuracy,3.6falsepremiums,15missed,32.8truepremiumswithheld;
v37mean90.81%coverage,96.85%retainedaccuracy,0.4false,12missed,30.2truewithheld.
Theseareconditionalbandcalibrationonhistoricallytrainedmodels,notfreshvalidation.
Fullv37bandwithholds42/433including32genuinepremiums;retained379/391,0false,12missed.
9tests pass,sourcehashesverified. Alloldpredictors/configs/evidenceunchanged.
prospective-v37-sealed.json has20freshshuffledattribute-stratifiedpairsandbothforecasts,
notshown/notanswered/notusedforcalibration. Fivegroups4each:heavybrowncomparison,
lightertare shadecontrols,coretradeoffs,mixedprovenance,alignedadvantages. Preserve
hashes/noretuning;starttablesoneatatime onlyonuserrequest. No backgroundjob.

## Latest completed test — v37 contextual premium candidate

Read premium-context-selection-v37.json and premium-context-verification-v37.json.
Evidencev37:671unique pairs,prospective16incorporatedonce withQ11correctionhistory.
DefaultV28 unchanged. Candidate predictor_premium_v37.py / premium-config-v37.json adds
onecoefficient0.75 on topoffrozenlarge-tare candidate: reducepositiveprovenance/shade
premium contributions whenloserbrown,winnercopper/amber,winnertareabove120lb(ramp).
Conditionalfamilyholdoutsize404/433V28,407/433large-tare,410.6/433newmean;falsepremiums
14→10.4versuslarge-tare,missed12unchanged. FullfitfixesQ5/Q12/Q14andpriorpilotQ4,
nootheroutputschange. Targetcorrectrepeats5/5,4/5,4/5;Q15preserved5/5. No knownmeaningful
premiumloss anyrepeat.671rank/swapchecks and1000pure5lbcontrols pass. Keep as experimental
candidate, notdefault; bandnotrecalibrated. Prospective examplesnowdevelopmentmaterial,
notfreshvalidation. Models/baselines preserved; noquestionnaire orbackgroundjob.

## Latest post-result correction

Question11 corrected byuser toAslight aftermodelresults revealed; Q5,Q12,Q14 reaffirmedBslight (Q14explicitlyclarified). See prospective-reporting-v1-clarifications.json andprospective-reporting-v1-corrected-results.json. Revised direction14/16,size12/16,both10/16;retainedsize12/15,both10/15,oneabstentionQ4. ThreefalsepremiumsQ5/Q12/Q14remain,nomissedpremiums. Originalprospectiveanswers/results preserved; revisedscoreispost-disclosure,notnewindependentvalidation. Models unchanged.

## Latest completed prospective validation — 16 answers

Read prospective-reporting-v1-results.json. Sealed forecasts/source hashes verified;
no refit or band changes. V28 direction14/16, size11/16, both9/16. Reporting abstains
onlyQ4 (actualAslight); retained size11/15, both9/15, coverage15/16. Threefalsepremiums
remainoutsideband(Q5,Q12,Q14); one missedpremiumQ11. DirectionreversalsQ9,Q10.
Therefore historicalzero-false-premium result doesnottransfer tothis freshslice.
Do notwidenband retrospectively orclaim uncertaintycalibrated. Smallstratified sample,
notpopulation estimate; exactequalityuntested. Answersstoredseparately fromsealedfile;
notincorporatedintotraining evidence. Roundcomplete, no pendingquestion orbackgroundjob.

## Current update — regional reconciliation and frozen validation

Evidence v36 supersedes four existing Northwest/Western Europe rows with explicit Bslight answers;655pairs retained,no addedweights. History preserved. Baseline models andreporting bands unchanged. Sealed16question prospective validation nowinprogress,question1presented. Read prospective-reporting-v1-progress.json for answers/nextquestion and prospective-reporting-v1-sealed.json forimmutablequestions/forecasts; neverexposeforecasts duringelicitation. Userprefers tablesonly,oneatatime. No refit untilroundcomplete.

# Current handoff — 2026-10-31

Consolidation and uncertainty reporting completed. Start at README's topsection.
Entry: predictor_reporting.py / reporting-config-v1.json; defaultV28 preserved.
All655pairs reproduce legacyoutputs forbothbackends. V28band[1.0,1.5) independently
reproduces peerE1:40/413withheld,including30truepremiums;retained358/373;15missedremain.
Candidateband uncalibrated andnot silentlyborrowed. Intrinsicspan helpertestedseparately,
notappliedtoV28. Peer sourcehashes andE2/E3arithmetic verified; E2/E3refits notrerun.
Five tests pass.16fresh prospectivequestions sealed/unasked, noactivequestionnaire.
Regionalfourlabels mapped but unchanged. See reporting-verification-v1.json.
Next: use reportinginterface; onlythen boundedregionalresolution orsealedprospective
elicitation ifrequested. No modelsearch,defaultchange,orbackgroundjob pending.

---

# Resume checkpoint — 2026-10-29

**Start with the current-state section at the top of README.md.** User requested that
we resume with consolidation and explicit uncertainty reporting, pausing model search.
Default remains V28; the one-coefficient large-tare premium correction is experimental.
Evidence v35 has 655 pairs. No new questionnaire, fit, default switch, or reporting-layer
implementation was performed by this checkpoint.

Next: inspect full Fable review/receipts, verify its band and span-rule definitions,
then consolidate explicit configuration and separate direction, premium size, boundary
uncertainty, exact equality, and unresolved input. Calibrate reporting on training data;
report coverage and true premiums withheld alongside errors. Reconcile the peer's four
regional-label concerns only after source mapping. Prepare a sealed prospective slice
without silently starting another questionnaire. Preserve all baseline artifacts.

Peer E1–E3 claims are user-reported, not independently reproduced here. E3 rejects two
specific margin schemes; it does not prove an irreducible noise floor. Clear preference
confidence is not meaningful premium size. Do not resume abandoned penalty searches.

No background job is running on behalf of this task. Older content below is historical,
including old instructions to fit, ask questions, or reconcile already completed rounds.

---

# Calculator handoff

## Latest voice-agreed test — global priority model

User agreed to globalfirst preference learning with Vintage>Tare>Provenance>Shade,
then narrowly scoped regional specialists only if they improve heldout predictions.
Ran the first GLOBAL RANKING test; no specialist ornewquestionnaire. Read
 global-priority-summary-v31.json and global-priority-validation-v31.json.
Learnednonnegative attribute curves; totalnormalizedranges strictlyordered withtiny
numerical separation,not literal5/4/3/2dollars. Regionalextremes selected bytraining-only
pilot. Existing130lb gold/pale rule retained. Exactties are softzero targets inthis
simpleglobalmodel; it doesnot claim to solve contextualequalities.
Winner-only results andclear-case count are in the summary. Do not compare this
percentage directly with earlier85%complete-judgment accuracy. Same reusedfamily
splits,not prospectivevalidation. Baselines/defaultunchanged. Next:inspect residual
clusters andendpoints before fitting anyspecialist; avoid routing isolated mistakes.

## Voice checkpoint — spectrum-first objective, 2026-10-28

User described an accordion: most offerings occupy a broad middle; the model should
recognize very poor and exceptional profiles, and be most reliable on obvious
comparisons. Moving inward should expose progressively closer, taste-sensitive choices.
User asked where the model succeeds/fails under this framing, then deferred to Codex
about preparing for compaction. This is NOT authorization for another questionnaire,
new model fitting, or an assumption that compaction has been triggered.

Next action: READ-ONLY spectrum audit of existing evidence and frozen predictions.
Separate three things: absolute profile position (low/middle/top), comparative advantage
(clear versus close), and all-top completion/distinctiveness. Two top-end offerings can
still be close, while a small attribute step can complete the exceptional profile.
Do not impose a mechanically smooth confidence curve or label all middle cases hard.
Actual inventory frequencies are unavailable; concentration in the middle and rarity
are qualitative user guidance, not measured scarcity statistics.

Live checks just made on the saved v31 validation rescore:
- All-top WE and Northeast pale20/110 versus115: v28 gets fulljudgment0/5 each;
  frozen v30 experimental candidate4/5 each. These are top-versus-near-top examples,
  not opposite ends of inventory. Do not generalize these counts to all extremes.
- Four nearby ordinary5lb controls: both models correct5/5 each.
- Three newlyconfirmed exact-price ties: neither frozenmodel predicts exactequality
  in withheld-family runs. This does not imply each falsely calls a meaningfulpremium;
  failure can be a residual nonzero value ranking despite correct practical similarity.
- Two close WCA tradeoffs (round56-7 andround56-8) remain weak.

The user's request is exploratory understanding and a checkpoint; do not change
weights/evidence or manufacture a fresh accuracy claim. No spectrum-wide measurement
has been completed yet. Give the grounded answer before proposing another fit.

## Current evidence — v31; Round57 reconciled and refit validated

Start with model-selection-v31.json. Evidence-v31.json / benchmark-targets-v31.json
contain640unique pairs:18existing pairs superseded,0newpairs. Rawexplanations, answer
histories,inventoryqualification andcase9interpretationbasis retained. Strictdirections460,
knownsizes396 (130meaningful,266nonmeaningful),3explicitexactties. Maincomparison has
219knownvalue-relation+size judgments,includingexactties; do not compare directly with
older220-case strict-direction percentages.

Exactties:round50-9 (reviewcase1),round6-8(case15),round8-4(case18). Case11/source51-7
remainspracticalsimilarity withunspecifieddirection,notexactequality or unresolved.
Case7/source37-9 keepsnominaltinyB plusinventory-dependenttie qualification. Other small
positive judgments retainstrictdirections. Historicalcoarsenedties not upgradedautomatically.

Refit:32intrinsicvalue coefficients,addingone commonmaturity/darkness interaction across
9regional effects. Current23basis cannot express35-year regional equality together with
strictyounger regionaldifferences; seev31-representation-check.json. Exactconstraints
andlatestreview direction/size guards usedonly intraining. Existinggold/pale equality
at130lb preserved throughoutnewfeatures. Testedcoupled/refittedpremiumencoder andfrozen
v30referenceencoder withrefittedv31head; latterbetter. Conservativeanchoring ofnewvalue
weights to matchingv30trainingfits wasbestrefit. No answerlookups atprediction.

Meanheld-family value-relation+size accuracy,allscored onv31:
- frozenv28:186.4/219 =85.11%
- frozenv30soft-order/frozen-premium candidate:192.6/219 =87.95%
- bestv31anchoredrefit:186.8/219 =85.30%
Allmodels recover0/3exactties when thosefamilies arewithheld. Fullv31refit matchesall18
reviewjudgments onprovidedaxes,including3/3exactties. This isconstraint satisfaction,
not generalization. Frozenv30 scoregain reflectsclarified targets,notnewtraining.

Default remains predictor_v28.py; do not call it thebestv31benchmark (thefrozenv30
candidate scoresbetter). Newrefit isexperimental:predictor_v31.py / model-config-v31.json.
No refitpromoted. Numericalvalue equality uses1e-7solver tolerance,not a broadpractical
band. Predictions expose equal/A_higher/B_higher; prices are not calibrateddollars.

Twoolder preferences conflict withnewties underown-attribute monotonicity:
- round9-7 versus exactround6-8 (Central/MiddleEast,brown35).
- round8-5 versus exactround8-4 (EasternEurope/WCA,copper30).
They remainrecorded andscored assofttargets; newexactties areprioritized. No silent
relabelling. Seev31-equality-conflicts.json. No newquestionnaire authorized or active.

59tests passed. All1250offering features and1640pair outputs checked; exactnumerical
clusters consistent. Provisionalruns thatmissedzero-shade propagation were rejected;
onlyrebuilt zero-shade caches/results apply. Baselines andevidencev30 unchanged.
Round57sourcefile's reconciliation_pending flag ishistorical; round57-reconciled-v31.json
andpricing-reset-progress.json recordcompletion. No backgroundfit remains.

## Round57 review complete — reconcile before the next fit

All18 existing comparisons reviewed; read round57-findings.json and the verbatim
answers in round57-consistent-misses-review.json. Models and evidencev30 stayed fixed.
Cases1,15,18 are explicit exact-price equalities. Case11 is practical similarity with
no clear direction, not exact equality. Case7 is B/very slight with an inventory-dependent
tie qualification. Case9 describes a premium from top20-year vintage+pale shade at125lb;
its meaningful label and interpretation basis are retained with the original wording.
Reconcile existing pairs once, retaining correction histories and exact-equality semantics.
No new unique pairs, active question or new fit. Do not call this a fresh validation round.

## Active review — 18 consistent misses

User authorized Round57: one at a time, starting with case1/source round50-9.
See round57-consistent-misses-review.json for fixed order and model hashes.
Record detailed explanations; keep models fixed. This revisits existing pairs,
not fresh validation. Reconcile later without duplicate weighting. All18cases recorded. Round57 complete; corrections awaiting reconciliation, models fixed.

## Latest ranking experiment — soft domestic prior, frozen premium assessor

Read regional-rank-fix-selection-v30.json. V28 remains the default. Leading experiment:
predictor_rank_soft_order_v30.py / rank-soft-order-frozen-premium-config-v30.json.
Evidence remains v30. No questionnaire or background fitting job is active.

Ranking audit: 464 known directions over 551 offerings contain no directed cycles.
This excludes strict-ranking cycles as a forced source of error; it does not prove
that current feature/size constraints can fit everything. Several near-boundary
regional/tare and top-vintage comparisons remain misranked. Some mixed-provenance
misses instead have the right winner but understated premium (notably round51-11).

Tested without new value features: centered regional regularization; a soft domestic
order penalty; and both together. Domestic ordering follows user's earlier hierarchy,
allows violations, and imposes no numeric price gap. Penalty strength is an engineering
choice (4x existing ridge), not an elicited economic weight. Inner ridge selection and
all fitting use training families only. Centered penalty alone did not improve ranking;
soft order improved it slightly. Combining penalties was not a clear improvement.

Refitting the premium head perturbed its gains, so the selected experiment freezes the
ENTIRE previous premium assessor, including its reference value encoder. Updated
intrinsic ranking is separate. All premium scores and size judgments are unchanged.
Runtime stores an additional frozen reference coefficient vector; do not claim total
stored parameter count is unchanged. No pair routing or answer lookup affects rankings.
Output exposes premium_reference_direction; it may differ from updated ranking.

Same five repeated family validations:
                               ranking   both axes correct
v28                            92.93%    84.55%
previous shared-context model   92.37%    84.91%
soft order + frozen premium     92.63%    85.36%
New paired complete deltas versus v28: [-1,-1,+2,+3,+6]. Balanced joint accuracy is
89.01% versus v28 89.05%; these are small exploratory differences, not a decisive win.
Ranking gains versus previous candidate:9 corrected and3 regressed repeat-events,
net6 overfive repeats (1.2/repeat). Much of the gain comes from one partition.

Premium precision/recall remains exactly 89.4%/88.9% on all size labels and91.9%/92.7%
on directly stated sizes. False premiums14.4, missed15.0/repeat; no new wrong-winner
premium observed. Protected all-top and small-positive cases pass. No previously
correct full-fit direction is lost. FullRound56 remains10/12, in sample.

A separate domestic-tier-context diagnostic fixes round51-11 in allfive repeats,
but that is ONE comparison repeated, not five independent successes. The tier
extension is not included in the selected runtime; support is too narrow to assert
that the substitution generalizes. See domestic-tier-context-validation-v30.json.

53 tests passed. Runtime preserves the frozen premium outputs; intrinsic value rankings
remain transitive. Baseline/evidence hashes verified. Same reused/adaptively explored
family splits, not prospective accuracy. Next work, if requested, should target the
remaining ranking structure and mixed-provenance justification with this distinction
between error types intact.

Artifacts: regional-rank-fix-validation-v30.json, regional-rank-combined-validation-v30.json,
regional-rank-frozen-premium-validation-v30.json, regional-rank-fix-selection-v30.json,
v30-ranking-consistency-audit.json, domestic-tier-context-validation-v30.json.

## Latest completed test — extend the shared-context feature

Read premium-context-extension-selection-v30.json. V28 remains active. The new
experimental predictor is predictor_premium_context_extended_v30.py, configured by
premium-context-extended-config-v30.json. Evidence remains v30.

Diagnosis: paired losses to v28 included repeated missed premiums in matching amber
and adjacent copper/amber comparisons excluded by the previous light-shade feature.
Ranking errors were the largest paired-loss category and remain unchanged in this test.

Smallest fix tested: widen the existing feature, without adding coefficients. It now
allows matching or adjacent non-light shades when the younger vintage is at most 30.
The same-provenance, five-year gap, at-most-5-lb tare gap, and younger-winner conditions
remain. Preserve the 35-versus-40/heavier-younger guard, the older non-light vintage
boundary, and the matching-shade 30-versus-35 low-tare counterexample (revision-8).
These are feature boundaries, not forced output labels or pair-ID lookups.

Same five family repeats on v30:
                          Both correct   False premiums   Missed premiums
v28                       84.55%         15.0             18.8
previous shared context   83.00%         17.0             17.8
same-shade extension      84.18%         15.8             16.0
adjacent-shade extension   84.91%         14.4             15.0

Extended premium precision/recall: 89.4%/88.9% on all size labels, versus v28
87.9%/85.3%; directly stated judgments 91.9%/92.7%, versus 90.3%/87.5%.
However, complete-judgment deltas versus v28 are [-2,-1,-2,+3,+6], only two wins.
Balanced joint accuracy is 88.74% versus 89.05%, and frozen ranking accuracy is
92.37% versus 92.93%. The premium head improves, but no overall active replacement.

Value weights, rankings, head parameter count, loss, ridge, cutoff and family splits
are unchanged. Protected all-top/small-premium cases and older/low-tare guards pass.
Every previously correct non-premium full-fit classification is retained. Full Round56
now matches 10/12 in sample: Q7 still overstates size; Q8 still reverses direction.
This is not a new prospective result. Active feature scope has 57 meaningful labels,
24 size-unspecified rows and no non-premium labels after guards; unseen negatives
remain a limitation. Feature boundaries were informed by existing v30 evidence.

48 tests passed, including 1,250 offering values and 1,640 runtime comparisons.
Baseline/evidence hashes checked. No active questionnaire or background fit.
If asked to continue, inspect the remaining ranking errors and mixed-provenance
premium misses rather than another broad loss-weight sweep.

Artifacts: premium-context-extension-validation-v30.json,
premium-context-extension-selection-v30.json, predictor_premium_context_extended_v30.py,
premium-context-extended-config-v30.json, test_premium_context_extension_v30.py.

## Latest completed fix — shared-context vintage distinction

Read premium-distinction-selection-v30.json. V28 remains active. Newexperimental
foundationhead: predictor_premium_context_v30.py / premium-shared-context-config-v30.json.
Evidencev30 andallvalue/ranking weights unchanged.

Compared15persistent falsepremiums with19genuine premiums suppressed bybothstricter
losses in>=3/5priorrepeats. Of19genuine cases,18sharedprovenance,13matchedtare,17matched
shade orweregolden/pale. Falsecases moreoftencontained actualprovenance/shade conflicts
orlarge coretradeoffs. Cohorts are diagnostic selections,not independenttestsets.

Oneadded feature:five-year youngerintrinsicwinner,sameprovenance,bothgolden/pale,
taregap<=5. Exclude35-vs40 whenyoungerheavier, respecting round51-17/round52-3.
All25fold coefficients positive,range0.77..1.13. Matchingprovenancealone didnothelp
(80.36%joint). Counterfactualattribution andgenericnetlead ratio also failed(79.64%).
They remain saved as rejected experiments; attributionalgebra checked,not assumedbadcode.

Samefamily-repeat means:
                          joint    precision recall  false missed
v28                       84.55%   87.9%    85.3%   15.0  18.8
oldfoundationhead         80.73%   81.0%    87.9%   27.8  16.4
newguardedcontexthead     83.00%   87.5%    86.8%   17.0  17.8
previous2xloss            63.73%   81.6%    56.0%   17.0  59.4
New direct-sizeprecision90.1%,recall89.5%;v28 90.3%,87.5%. Newhead improvesoldfoundation
inall5repeats butbeatsv28 only1/5. Noactivepromotion. It avoidsfalsecalls withfarless
recallloss thanreweighting. Rankings stay92.37%;v28 92.93%.

Protectedalltop/smallpremium cases andround51-17 boundary pass. FullRound56 now9/12
in-sample:Q7andQ10size overcalled,Q8directionwrong. No12/12orprospectiveclaim. Activefeature
scope contains50knownmeaningful andno knownnonpremium labels afterguard; guard andfeature
were developedfromv30,so unseennegativecases remain unverified.44tests passed;1250values,
1640runtimepairs,swap symmetry,training-only headfits,baselinehashes andguardchecks.

Artifacts:premium-contrast-analysis-v30.json,premium-distinction-validation-v30.json,
premium-isolated-vintage-validation-v30.json,premium-isolated-guarded-validation-v30.json,
premium-same-provenance-validation-v30.json,premium-distinction-selection-v30.json.
No activequestionnaire orbackgroundfit. If asked tocontinue, focus on remainingcompeting
coreprofiles andfixedranking errors rather than another blindloss sweep.

## Latest completed experiment — premium-loss weighting, value heads frozen

Read premium-loss-selection-v30.json. V28 remains active. On evidencev30, tested equal
per-case loss and2x per-case nonpremium penalty against thefoundation premiumhead's
class-balanced loss. Allvalueweights,rankings,headfeatures,normalization,ridge.03,
protectedtrainingconstraints,0.5cutoff and25outerfolds unchanged. No thresholdretuning.
Newlosses normalized tosum1,so no incidentalregularization-scale change.

Means over5repeats,all396size-labeled pairs:
                           precision   correctpremiumrecall   false   missed
v28                        87.9%       85.3%                  15.0    18.8
foundationclassbalanced    81.0%       87.9%                  27.8    16.4
equalpercase               82.3%       71.0%                  20.6    39.2
falsepremium2x             81.6%       56.0%                  17.0    59.4
Precision includeswinnercorrectness;v28alsohas1.0wrongwinnerpremium/repeat,others0.
On261direct-size labels:precision/recall v28 90.3/87.5%;classbalanced83.9/89.7%;
equal84.9/71.0%;2x83.2/54.9%. V28dominatesbothnewarms onbothmetrics inbothviews.
Complete-label accuracy:v28 84.55%,classbalanced80.73%,equal72.36%,2x63.73%.
Threshold-free ROCAUC also declines:all-labelv28 .9466,classbalanced .9240,equal .9143,
2x .8946;direct .9444,.9260,.9124,.8880. Notmerely a bad fixedcutoff.

Conclusion:reweighting reducesfalsecalls bysuppressing toomany realpremiums. It doesnot
fix thishead's discrimination. Theearlier1.93xpositive-weight audit identified a real
objective choice,not a demonstratedrootcause or a guaranteedfix. No newcandidate promoted.
Next diagnostic:inspectpersistentfalsecalls andsuppressedtruepremiums together before
another featureorweight change. No questionnaire currentlyauthorized.

Artifacts:premium-loss-validation-v30.json,premium-loss-discrimination-v30.json,
premium-loss-selection-v30.json,premium-losses-full-v30.json. Experimentalruntime
predictor_foundation_amplifiers_v30.py accepts --config premium-loss-equal_case-config-v30.json
or premium-loss-false_premium_2x-config-v30.json. Originaldefault remainsunchanged.
39tests passed;all1250offeringvalues and1140pairoutputs checkedpernewarm,rankings unchanged;
protectedalltop/smallpremium cases pass. Reusedfamilyvalidation,notnewprospectiveaccuracy.
No evidencechange orbackgroundjob remains. Twofoldpenalty is a testscenario,not usercost.

## Resumed — premium-objective audit completed

User asked to resume with the lowest-resistance item. Audited frozen predictions and
training/evaluation weighting; no model refit or evidence change. Read
premium-objective-audit-v30.json next. V28 remains active.

Finding1: the new binary class-balanced premium head assigns each positive case
1.93x the training weight of each non-premium case (135 versus261 labels). Equal total
class weight is not equal per-error cost; it favors premium recall. This is not a code
bug, but may mismatch the user's obvious/defensible-premium objective. No numerical
false-premium cost was elicited; tested ratios1..3 are audit sensitivities only.

Finding2: complete-label accuracy excludes176knownnonpremium rows lacking a direction
label. Macrogroup weighting also gives different per-case costs depending on direction
availability. Track premium claim precision, recall and wrong-winner premiums separately.

Mean precision of claimed premiums, requiring correct winner AND meaningfulness:
v28 87.9%;guarded intrinsic86.4%;newfoundation balancedhead81.0% onall size labels.
On directly supported size labels:v28 90.3%,guarded90.1%,foundation83.9%. Guardedmodel
recognizes100correctdirect premiums/repeat versusv28 95.4 at nearlyequal precision.
Thus evaluation provenance matters. Do not delete or relabel older proxy/coarsened rows.

Next smallest test: freeze value/ranking head and compare current class-balanced premium
loss with equal per-case loss and a modest false-premium-weighted alternative, using
training-only family calibration. Report precision/recall/falseclaims onboth all-size
anddirect-size views; preserve protectedalltop/small-premium cases. Reject improvements
that merely suppress meaningful-premium recognition. No new valuefeatures or questionnaire
needed for that experiment. The audit itself does not prove a new loss will win.

## Latest architecture test — foundation, contextual amplifiers, separate premium head

User semantic clarification in premium-semantics-clarification.json was applied to a
new model on unchangedv30. Active model remainsv28. Bestexperimental within thisnew
architecture: predictor_foundation_amplifiers_v30.py / foundation-amplifiers-selected-config-v30.json.
Earlier experimentalpredictors andtheir receipts remain available; this is not a claim
that the new architecture beats them. Decision:foundation-amplifiers-selection-v30.json.

Value head:23coefficients. Nonlinear vintage/tare increments plus their interaction
form thefoundation. Nineprovenance andfourshade coefficients contribute through
C(v,t)=0.5+0.25*(normalizedvintage+normalizedtare),not universalconstant bonuses. An
all-top profile term is available. Monotonic own-attribute values andaggregatefoundation
range>=combinedmodifier range are enforced. Thiscontext function/range prior are
engineeringhypotheses implementing user guidance,not elicitednumericprices or universal
pairwise dominance. Inference returns value-components peroffering andan intrinsicrank.

Premiumhead:separate regularizedclassifier trained onknownmeaningfulness labels,using
cross-fitted value contributions,opposingattributes,coreprofile andall-top distinction.
It is not a fixedcutoff onthevalue index. Alternativeclassweights,opposition constraint,
rawprofilefeatures anddirectionaltradeoffproducts were tested andsaved; bestwas the
13-feature contributionhead withbalancedsize weighting. Coefficient signs amongcorrelated
features are not causal explanations. Score is not calibratedconsumerchoice probability
or measuredmarket scarcity. A buyer mayprefer thelessvaluable offering; nochoice dataused.

Same25outerfamily folds; threefoldtraining-only groupedridge selection forvaluehead;
head learns frominnerout-of-fold value features. Missing direction/size remainmissing;
no new label,row orquestionnaire added. Frozenv28 comparison andsame-valuegap-cutoff
ablation scored directly onindependent direction/meaningfulness outputs:
- v28:joint84.55%,direction92.93%,falsepremiums15.0,missedmeaningful18.8/repeat.
- newvalue +singlegapcutoff:joint68.27%,direction92.37%.
- newtwo-head model:joint80.73%,direction92.37%,falsepremiums27.8,missedmeaningful16.4.
V28wins completejudgments inall5repeats. Separatingoutputs helps withinthenewarchitecture,
but thepremiumclassifier overstates close cases; nooverallpromotion.

Full-fit protectedalltop andoldsmall-positive controls pass. FullRound56:11/12directions,
7/12size judgments,6/12both; do NOT carryforward previousmodels'12/12claim. Theseare
in-sample results. Valueindex units areordinal,notmoney; additionalall-top valuecoefficient
may beunidentified byranklabels even whenpremiumheadrecognizes thatprofile.

35tests passed,1250offering values/components and2140pair outputs verified. Runtime is
NumPy+JSON anduses noanswerlookup. API has premium_justification_score andexplicit
predicted_meaningfulness; there is NO decision_radius for thetwo-head model. Evaluate
its explicitlabels,not abs(valuegap)>1. Reused/adaptivevalidation is exploratory,notfresh
prospective accuracy. No backgroundprocess oractive questionnaire remains.

Artifacts:foundation-amplifiers-validation-v30.json,foundation-robust-head-validation-v30.json,
foundation-profile-head-validation-v30.json,foundation-tradeoff-head-validation-v30.json,
foundation-amplifiers-selection-v30.json,foundation-amplifiers-verification-v30.json.

## New valuation semantics — user clarification, 2026-10-28

Read premium-semantics-clarification.json before the next modeling step. A meaningful
premium is an obvious/defensible value advantage from rarity,scarcity ordistinctiveness;
personal preference can still cause someone to choose the less valuable alternative.
Do not equate this with universal purchasing agreement or a fixed dollar/percentage gap.
Vintage and tare are primary;provenance andshade frame/amplify that underlying profile.
Conditional interactions are a modeling hypothesis to test,not a numerical formula
elicited here. Preserve all priorpairanswers,including pure-shade/provenance comparisons.
This is semantic guidance,not a synthetic training row or a new evidenceversion.

## Latest experiment — guarded vintage/tare meaningfulness boundary

Evidence remainsv30. Decision receipt:vintage-tare-selection-v30.json. V28 remains
active; bestintrinsic experimental option is now predictor_vintage_tare_v30.py with
vintage-tare-guarded-config-v30.json. All25intrinsic coefficients unchanged.

Verified assumption conflict (vintage-tare-assumption-conflict-v30.json): WCAgold30/115
meaningfully exceedsWCAgold25/130, which meaningfully exceedsWCApale30/125. A common
meaningfulnessradius1 impliesfirst-last>2, while twoordinary5lb caps plus shade
monotonicity implyfirst-last<2. This holds for arbitraryintrinsic utilities. The two
intermediate5lb caps are extrapolatedrules,not elicited pair labels; rankings themselves
are consistent. Additional sharedweights alone cannot repair this assumption conflict.

Smallesttested fix:one learned meaningfulness radius for sameprovenance,exact5-year
vintagegap,younger<=30,younger5lbheavier,atmostone adjacent shade step,withtheyounger
offering already rankedhigher. Fullscale0.2; foldscalestraining-only. Guard keepsnormal
radius for same-shade30vs35 whenolderlightertare<=115. This protects recordedrevision-8.
The guard followed an initial unguarded test that added0.8falsepremiums/repeat. It is
attribute-based,not ananswerlookup, but adaptiveguard selection requiresqualification.

Held-family meancomplete judgments: intrinsicparent173.4/220(78.82%),guarded187/220
(85.00%),v28 186/220(84.55%). Directionunchanged92.63%,v28 92.93%. Missedmeaningful
28.8->15.2,v28 18.8. Falsepremiums19.0->19.0,v28 15.0. JointdeltasvsV28 byrepeat
[-2,-1,+10,+3,-5]; only2/5wins. Balancedjoint88.00%versusv28 89.05%; nooverallpromotion.
Scope afterguard has20size-labeledpositive pairs and9size-unspecified pairs; theknown
negative is explicitlyguarded. No extraobservedfalsecalls doesnot establish safety on
unseennegativecases. This is reused/adaptive validation,not a fresh prospective result.

Allintrinsic values/rankings andpure5lb behavior unchanged. Allrecorded nonmeaningful
predictions unchanged versusintrinsicparent. All-topWE/NE premiums,oldWCA anchor and
all12Round56 full-fit answers retained,including7smallpositivepremiums. Round56 remains
in-sample,not a newfrozen test.29tests passed;1250offeringvalues and1500randompairscope
checks passed. No evidencechange,activequestionnaire orrunningfit remains.

Artifacts:vintage-tare-assumption-conflict-v30.json,vintage-tare-threshold-validation-v30.json,
vintage-tare-guarded-validation-v30.json,vintage-tare-selection-v30.json,
predictor_vintage_tare_v30.py,vintage-tare-guarded-config-v30.json.

## Latest audit — regional model stability and one-coefficient repair

Evidence remainsv30,640pairs. Active predictor remainsv28. Latest decision receipt:
regional-stability-selection-v30.json, superseding earlier experimental rankings.

Isolated solver test:20/25originalregional fold fits already met0.1%MIPgap. Reran5
remaining folds at90sec versus12sec, selected incumbents by training objective only.
All25then met tolerance; joint complete correct162.4->162.8/220 (73.82%->74.00%).
Solver time alone does not explain the gap. Full45sec regional fit already converged.

Minimum-L2 postfit keeps every correct training judgment plus structural rules and
selects smaller coefficients. No features/thresholds changed. Mean fold coefficient
variance0.4845->0.0553; completion-coefficient range0..8->0..0.2684; accuracy only
74.00%->74.09%. OSQP with equivalent SLSQP fallback on iteration limit, preserving
previously successful checked fits. Not a global lexicographic search over error sets.

Verified structural limitation: round45-5 requires V35-P>1 (P>=0); round50-12 requires
0<V35<1. Both are individually feasible but jointly impossible for the24-term family.
This is model misspecification,not contradictory user evidence. New single feature
allows the40->35 vintage increment to differ for golden/pale versus darker shades;
its value persists at younger vintages as a cumulative increment. It does not directly
change same-profile5lb steps or golden/pale equality at130lb.

Five-family-repeat complete-label scores/220:
- v28:186.0 (84.55%)
- originalregional24:162.4 (73.82%)
- longer solver:162.8 (74.00%)
- longer + minimum norm:163.0 (74.09%)
- new25-term feature:172.6 (78.45%)
- new feature + minimum norm:173.4 (78.82%); wins against oldregional all5repeats.
Newfeature fits30sec/fold,90sec/full; all25folds reached requested solver tolerance.
Direction improved91.16%->92.63%,v28 92.93%. Falsepremiums20.8->19.0,v28 15.0;
missedmeaningful33.2->28.8,v28 18.8. Underlying regional training accuracy~89.1%
versus74.0%heldout; afterfeature/minnorm90.5%training versus78.82%heldout. Missing
context and sparse-family transfer remain; cannot attribute all loss solely to overfit.

New full model retains12/12Round56 answers including all7smallpositive premiums,
WE/NE all-top completion,oldWCA15lb anchor and ordinary5lb/130lbshade controls.
Those12are in-sample; heldout Round56 average9/12,priorregional8.4/12. No leakage or
answer lookup in prediction. Experimental NumPy+JSON runtime:
predictor_regional_mature_v30.py / regional-mature-selected-config-v30.json.
1250offering values and1640pair outputs match reference exactly;25tests passed.
V28 remains active because its overall held-family accuracy is better.

Artifacts:regional-solver-audit-v30.json,regional-minnorm-validation-v30.json,
regional-mature-shade-validation-v30.json,regional-representation-conflict-v30.json,
regional-stability-selection-v30.json,regional-stability-verification-v30.json.
Reused/adaptively explored family validation,not new prospective accuracy. No active
questionnaire or pending evidence reconciliation; no background fit remains.

## Current state — evidence v30; v28 retained after intrinsic interaction tests

Round56 incorporated once:640 unique pairs,464 directions,396 size labels,220both-axis
judgments. Seven new small premiums retain strictA/B direction plus practical size.
Evidence-v30.json / benchmark-targets-v30.json; no unresolved answers inferred as ties.

Compared frozenv28/original intrinsic23 with refitted23control,24mature-tare interaction,
25mature-tare×shade, and an adaptive24regional-vintage alternative on the same25family
folds. Current-label both-axis accuracy: v28 84.55%;original intrinsic78.82%;refitcontrol
72.64%;maturetare73.09%;maturetare×shade73.36%;regionalvintage73.82%.
These currentv30 denominators differ from priorv29 results; baseline weights unchanged.

Verified representation conflict: round49-2,round50-4,round56-4,round56-12 cannot all
fit the proposed25-term intrinsic family with structural rules, even without upper
coefficient bounds. Removing any one makes the subset feasible. The110lb middle
profile cancels from the comparison chain; merely adding low-tare interactions cannot
fix shared foreign top-vintage effects. One signedSEA20-year offering term removes
this specific conflict, but does not establish generalization or solve all evidence.
Proof: interaction-conflict-v30.json; reproducible LP scripts saved.

Full-data fit: tare×vintage×shade matches11/12Round56 (Q4wrongdirection);regionalvintage
matches12/12, including all7smallpositive premiums. All tested full models preserve
protectedWE/NE all-top110lb cases and small-positive controls; all-domain ordinary5lb
cap and130lb golden/pale equality verified. These are in-sample checks,not retests.

Active predictor remains predictor_v28.py / model-config-v28.json. Experimental best
refitted candidate: intrinsic_regional_v30.py with interaction-config-regional_vintage-v30.json.
The activev28 still does not implement the all-top intrinsic exception. No promotion
because every refit trails frozenv28 on withheld-family complete judgments.21tests
passed. Several MILP fits time-limited; do not claim globally optimal weights. Reused
exploratory validation,not new prospective accuracy.

Primary receipt:model-selection-v30.json. Details:interaction-validation-v30.json,
regional-interaction-validation-v30.json,interaction-selection-v30.json (ranks only
initialthree refits),interaction-feasibility-v30.json andinteraction-conflict-v30.json.
No active questionnaire. Round56 evidence reconciliation complete.

## Round56 complete — frozen WCA threshold versusv28

All12 fresh targeted comparisons answered and all24 frozen predictions rechecked.
Candidate: direction9/12,meaningfulness6/12,both5/12,4falsepremiums,2missedmeaningful.
V28: direction7/12,meaningfulness8/12,both6/12,0falsepremiums,4missedmeaningful.
Candidate direction missesQ7/Q8/Q9; size missesQ1/Q5/Q7/Q8/Q11/Q12.
V28 direction missesQ2/Q5/Q7/Q8/Q12; size missesQ2/Q5/Q6/Q12.
No ties or unresolved answers:7practicallysimilar with direction;5meaningful.

Post-round threshold-only counterfactual: original intrinsic would get3/12both;
threshold gets5/12. It fixes sizeQ2/Q6 but adds falsepremiumQ7 (already wrong sign).
FalsepremiumsQ1/Q8/Q11 come from intrinsic weights even at radius1, not threshold alone.
Matched controlsQ1/Q11 andQ2/Q12 get the same user judgments across provenances.
Do not claim WCA threshold alone caused every error or fixes reversed directions.

Round56 is a targeted challenge set, not general population accuracy. Results do not
justify promoting the candidate overv28. Answers/explanations remain inround56-fixed.json;
analysis inround56-findings.json. Evidencev29 and model weights remain frozen. Round56
awaits later evidence reconciliation; no active question.


## Intrinsic refinement follow-up — completed

Evidence remainsv29. Tested zero-extra-coefficient protected refit, oneWCA tare
coefficient, and two alternatives adding a second light-shade vintage orWCA20-year
coefficient. Full fits satisfy WCA15lb meaningful and WE/NE all-top requirements,
but none recovers the WCA meaningful premium in any of5 withheld-family repeats.
Complete-judgment accuracy: protected77.69%,WCA tare78.17%,tare+light-vintage80.10%,
tare+WCA20year76.73%,versus original intrinsic82.21% andv28 87.31%.

One threshold-only diagnostic improves original intrinsic to83.27%, with unchanged
93.27%direction and no additional observed falsepremiums (14/repeat). It leaves all
23 intrinsic utility coefficients untouched, changing the meaningfulness radius from1
to a training-selected scalar for matchedWCA with>=15lb tare gap. Full-data scalar.25;
WCA target correct4/5 withheld repeats versus0/5 for both original models. Existing
all-top utility premium and ordinary5lb controls preserved. This is a classification
fix, NOT an increase in intrinsic tare value. Scope has5unique pairs,only3size labels,
all positive; no within-scope negative controls. Treat as exploratory,not confirmed.

Active runtime remains predictor_v28.py. Experimental option:
predictor_intrinsic_threshold_v29.py / intrinsic-threshold-config-v29.json.
See intrinsic-refinement-summary-v29.json for overall disposition and limitations;
intrinsic-refinement-selection-v29.json ranks only the protectedweight-refit subset.
All22tests passed: baseline integrity, train-family separation, training-only anchors,
intrinsic utility invariance/antisymmetry, all-domain structural rules, required cases.

## Current selection — evidence v29, v28 retained

Round55 is incorporated into evidence-v29.json and benchmark-targets-v29.json:
628 unique pairs,452 known directions,384 meaningfulness labels,208 complete judgments.
Eight new pairs; two clarifications supersede active labels with history retained.
Source round47-18 now has no clear direction/practical similarity, not exact equality.

The23-coefficient intrinsic candidate assigns utility to each offering independently.
It adds domestic top-vintage, foreign young-pale, nonlinear premium-tare hinge,
young-vintage/tare interaction, and the confirmed WE/NE pale20/110 completion term.
Monotonic shade/age/tare constraints cover the supported domain. Ordinary pure5lb
steps remain nonmeaningful except the two confirmed completion profiles. Golden/pale
utility is identical at130lb. These are utility scores, not calibrated prices.

Same five repeated family partitions, training-only fits/anchors, frozen v28 fold
weights rescored against current labels. Short3sec/12sec fit repeated at12sec/fold
and45sec full fit to check optimization budget sensitivity. Longer-fit comparison:
- Both axes correct: v28 181.6/208 (87.31%); intrinsic 171.0/208 (82.21%).
- Direction: v28 93.76%; intrinsic 93.27%.
- Meaningfulness balanced accuracy: v28 91.44%; intrinsic 88.47%.
- False premiums/repeat: v28 13.0; intrinsic 14.0.
- Missed meaningful/repeat: v28 15.6; intrinsic 22.8.

Selected delivery remains predictor_v28.py / model-config-v28.json. It is a pair
comparator, not an intrinsic price function, and does not implement the new all-top
exception. The candidate remains available in intrinsic_v29.py with
intrinsic-long-config-v29.json. No answer lookup is counted as prediction.

Selection is based on observed held-family performance; solver incumbents remain
time-limited, not certified optimal. These reused partitions are exploratory and
feature design used Round55, so this is not fresh prospective accuracy or proof that
intrinsic valuation cannot work. See model-selection-v29.json,
intrinsic-diagnostics-v29.json, intrinsic-long-validation-v29.json, and
intrinsic-validation-v29.json for full fit/predictions, regressions and solver gaps.

## Round55 complete — intrinsic tare context and all-top-tier exception

Ten active judgments saved in round55-tare-context-isolation.json. WCAgold30/115 vs
gold25/130 reaffirmed A/moderate:15lb gap andposition drive value. WE andNE pale20
110vs115 explicitly meaningful; scoped exceptions invalidate blanket all5lb-nonmeaningful
constraint. Controls WEpale20 115vs120,WEpale25 110vs115,WEgold20 110vs115,NWpale20
110vs115 all A/slight/practical. Cross WEgold/NWpale20 at110 A/slight/practical;at115
no clear direction/practical. Relative home-geography tier guidance retained, not
converted into arbitrary numerical weights or empirical rarity claims.

User explicitly wants offering-intrinsic value: comparisons reveal value difference,
not create premium. Current pair-dependent predictor does not guarantee this, so future
math must address it explicitly. Source47-18 SWgold30/125 vsNWgold25/130 clarified to
no clear cost-based direction/practical,not exacttie; earlierA target pending supersession
withhistory, old frozen test unchanged. All10 predictions/source hashes verified.
No active question or refit. Evidence staysv28 pending deduplicated incorporation.
Receipt round55-findings.json.

## Active Round55 — tare gap and premium-profile context

User reaffirms round53-2 WCAgold30/115 >gold25/130 moderately. Explanation: gap size
and position matter; high tare quality completing premium provenance/shade/vintage
profile can carry extra value. Preserve as qualitative preference, not empirical rarity
or numeric interaction weights. Q2 tests WEpale20 at110vs115lb;110 is supported-domain
minimum, user top-tier cutoff not assumed. Q2 explicitly confirms meaningful A premium atWEpale20/110 vs115 due all-topprofile.
This is a scoped exception to blanket5lb cap, not an empirical rarity claim. Q3 115vs120 now A/slightly/practical/not tie. Intrinsic offering-value guidance retained.
Q4 WEpale25/110vs115 A/slightly/practical confirmed. Q5 golden boundary A/slightly/practical confirmed,perceptual caveat retained. Q6 NW boundary A/slightly/practical confirmed. User proposes cross-profile isolation: Q7 WEgolden20/110 >NWpale20/110 slightly/practically,one-step shade gap guidance retained. Q8 no clear direction/practical approximate pricing confirmed; relativehome-geography ladder guidance retained. Q9 NEpale20/110vs115 meaningful confirmed, second all-top-profile positive; scoped5lb exceptions established. Q10 middle-tier explanation: no meaningful premium justified,explicitlynot exacttie; A/B directional clarification pending. Models fixed. Separate SW/NW original mismatch remains queued after tare isolation.
Record round55-tare-context-isolation.json.

## Current model — v28 joint refit on reconciled evidence

Use predictor_v28.py / model-config-v28.json. The entry point delegates to the unchanged
standalone20-coefficient engine in predictor_v27.py; new weights, no extra features.
Evidencev28 has620 unique pairs,446 known directions,376 sizes,202 both-axis labels.
Rounds51-54 reconciled by unordered pair; original IDs/orientation and answer histories
preserved. All original unresolved pairs now resolved and unresolved registry empty.
Final probe round54-17 retains A/slightly with binary size unspecified; never inferred.

Same5 paired withheld-family repeats on current labels:
                                 previous tare     selectedv28
Both-axis correct/202            170.0             176.6
Both-axis accuracy               84.16%            87.43%
Direction/446                    91.43%            93.45%
Balanced meaningfulness          91.44%            92.07%
False premiums/repeat            19.6              13.0
Missed meaningful/repeat         11.8              13.6
Correct meaningful direction     114.2             114.0
Complete counts improve+7,+7,+3,+12,+4; direction andfalse premiums improve every
repeat. Selected overall joint improvement despite missed-meaningful tradeoff. Same
model structure/objective/solver budgets, training-only anchors/fits, old587 baseline
margins reproduce. Reused-family validation is exploratory, not fresh-test accuracy.

Full-fit limitations: WCA golden30/115 vs golden25/130 still understated (A practical,
user meaningful); Southwest golden30/125 vs Northwest golden25/130 still wrong direction
(B practical versus user A practical). Other9/10 original resolved anchors fit supplied
axes. Do not claim total reconciliation success from evidence bookkeeping alone.

Runtime equivalence: all1,562,500 supported ordered pairs match refitted candidate,
plus historical/random scalar checks.12 tests passed: dedup/history, missing labels,
train-family separation, protected anchors, score reproduction, old margins,1000 pure
5lb,50 zero-shade130,3000 no-heavier-reward checks and no answer lookup. One negligible
floating-boundary difference in baseline occurred only on a size-unspecified row and
did not change scored outcomes. No new inference logic added after fitting.

Artifacts evidence-v28.json,benchmark-targets-v28.json,tare-refit-validation-v28.json,
model-selection-v28.json,model-config-v28.json,predictor_v28.py,
tare-predictor-equivalence-v28.json,test_tare_refit_v28.py. All pending reconciliation
fromRounds51-54 is incorporated; no active elicitation round.

## Round54 post-completion clarification — last probe direction resolved

User now chooses A slightly for matchedNortheast brown25/115 vsamber30/120, citing
younger vintage and lower tare. Prior too-close response retained in answer_history.
No unresolved winner remains in this deconstruction. Probe17 binary meaningfulness
was not explicitly supplied; retain slightly without inferring a category. All10
original resolutions remain strict direction/practical similarity. Evidence incorporation
pending; model unchanged.

## Round54 complete — all10 original unresolved comparisons resolved

21 total anchor/probe judgments saved. All10 original anchors explicitly resolved
with strict A/B direction and practical similarity, not ties: round27-11 B,round42-3 B,
round42-10 A,round42-12 B,round45-12 B,round47-1 A,round47-12 A,round47-18 A,
round49-9 A,round49-10 A. Preserve original histories on next reconciliation;
no duplicate weighting. Separate matchedNortheast brown25/115 vsamber30/120 probe
round54-17 remains unresolved on both axes; originalNE/SE resolution does not label
that probe. Models and evidencev27 unchanged; all42 predictions/source hashes verified.
No active question. Receipts round54-unresolved-isolation.json/round54-findings.json.

## Active Round54 — deconstruct10 remaining unresolved comparisons

Round53 complete:WCA golden30/115 beats golden25/130 meaningfully;15lb tare alone
sufficient, pale only adds smaller benefit. Pending reconciliation, no refit.
User requests remaining unresolved items one at a time with isolation. Ten original
pairs reconciled afterRound52 clarifications. Start source27-11(WCA pale30/120 vs
brown20/120); prior request for provenance/tare differentiator honored. Q1 changes
only A tare120to115. Original pair remains unresolved until explicit net judgment;
probe label does not resolve anchor automatically. Models fixed, no invented total
probe count. Record round54-unresolved-isolation.json;Q1 B/slightly/practical confirmed. Q2 originalround27-11 resolved B/slightly/practical. Q3 matchedSouthwest probe A/slightly/practical confirmed. Q4 originalround42-3 resolved B/slightly/practical. Q5 matchedNortheast probe B/meaningful confirmed. Q6 originalround42-10 resolved A/slightly/practical. Q7 matchedcopper probe A/slightly/practical confirmed. Q8 originalround42-12 resolved B/slightly/practical. Q9 matchedNorthwest probe A/slightly/practical confirmed. Q10 originalround45-12 resolved B/slightly/practical. Q11 matchedSoutheast probe B/slightly/practical confirmed. Q12 originalround47-1 resolved A/slightly/practical. Q13 matchedEasternEurope probe A/meaningful confirmed. Q14 originalround47-12 resolved A/slightly/practical. Q15 matchedSouthwest probe B/meaningful confirmed. Q16 originalround47-18 resolved A/slightly/practical. Q17 matchedNortheast probe unresolved/too close. Q18 B/slightly/practical confirmed at equal30years. Q19 originalround49-9 resolved A/slightly/practical. Q20 matchedgolden probe A/slightly/practical confirmed. Q21 restores B pale, originalround49-10 awaiting judgment. Probe17 remains unresolved separately.

## Active Round53 — Round51 Q13 tare-led miss

User explains A moderately more expensive:15lb tare advantage main driver,pale adds
a little, five-year younger B cannot offset both. Source answer reaffirmed, no label
change or duplicate weighting. Saved round53-isolation.json. Q2 changes only A shade
from pale to golden; shade now matched, isolates age/tare tradeoff. Models fixed.

## Round52 complete — Round51 Q2/Q15/Q17 clarified

All3 now explicit small positive premiums, not ties: sourceQ2 A/practical,sourceQ15
A/practical,sourceQ17 B/practical. Full explanations and exchange-rate closeness joke
retained; no FX feature inferred. Saved round52-clarifications.json/round52-findings.json.
All6 model predictions/source hashes verified unchanged. No model/evidence update;
reconcile original pair IDs with history in next evidence version, no duplicate weights.
Original Round51 score receipt remains historical; revisits not fresh prediction accuracy.
No active clarification.

## Active Round52 — clarify Round51 Q2/Q15/Q17

User requests meaningfulness clarification, one pair at a time. Pairs and model
predictions saved in round52-clarifications.json; sources hashed. Direction and
meaningfulness separate, unresolved remains allowed. Q1/sourceRound51-2 resolved A/slightly/practical, nottie. Q2/sourceRound51-15 A/slight/practical confirmed, nottie. Q3/sourceRound51-17 awaiting meaningfulness. Prior round/evidence preserved; repeated clarification not fresh accuracy.

## Round51 complete — compensation/v26 tie on scored answers

Both direction15/16,size13/17,both11/15,zero-shade2/2. Q2/Q15 unresolved/not ties;
Q17 B/slightly size unspecified. Q18 answered on requested revisit B/practical.
Shared misses:Q7/Q18 false meaningful premiums in dark-shade mixed trades;Q11 correct
youngerDomesticCentral direction but size understated;Q13 WCA pale30/115 vs golden25/130
wrong direction+size (userA meaningful,modelsB practical). Active compensation contexts
Q1/3/6/10 correct for both. No incremental gain demonstrated here. All40 predictions
recomputed and source hashes verified. Evidence remainsv27; no active round/refit.
Broader selected fresh pairs, not population accuracy. Receipts round51-fixed.json
and round51-findings.json.

## Active Round51 — tare-compensation model versusv26

20 fresh varied pairs across all10 provenances; includes4 active compensation-context
comparisons and older/zero-shade/pure-tare/out-of-scope controls. Reverse duplicates
checked against saved rounds/evidence/isolation. Attribute selection precedes predictions.
All40 predictions and model/config hashes frozen in round51-fixed.json. Present5 at
a time; hide predictions/interim scores; separate axes, unresolved available. Awaiting
Q1 A/meaningful,Q2 unresolved/not tie,Q3 A/meaningful,Q4 A/practical,Q5 A/meaningful. Q6 A/meaningful,Q7 B/practical,Q8 A/practical,Q9 zero-shade tie,Q10 A/meaningful. Q11 B/meaningful,Q12 B/meaningful,Q13 A/meaningful,Q14 A/practical,Q15 unresolved/not tie. Q16 A/meaningful,Q17 B/slightly size unspecified,Q18 revisit requested,Q19 zero-shade tie,Q20 B/meaningful. Reposing Q18 now; no interim scoring. No mathematical changes during this round.

## Current predictor — selected tare-compensation model (v27)

Canonical runtime: predictor_v27.py with model-config-v27.json. NumPy plus one JSON
configuration; no training/historical-model/evidence imports. Exact saved20-coefficient
candidate selected after requested direction-regression/stability review. No refit or
mathematical change during delivery. Earlier predictor.py/model-config.json remain
v26 reference snapshots; do not confuse them with current runtime.

```python
from predictor_v27 import Model
result = Model().compare(
    ["Western Europe", "golden", 30, 125],
    ["Western Europe", "pale/straw", 35, 120],
)
```

Paired run changes versusv26 in complete judgments: +10,0,+7,+3,+2; direction:
+1,-3,+7,-5,-7. Balanced joint score improves4/5, complete counts improve4/5 and tie1.
Means: complete146.2/163(89.69%) vs141.8(86.99%); direction92.76% vs93.10%;false
premiums14.6 each; missed meaningful8.8 vs9.4;correct meaningful104.2 vs103.4.
57 direction losses offset by50 gains.46 losses lack a supplied size label,11 have
one; missing sizes do not make those preferences unimportant. Some slight provenance/
tare orderings regress repeatedly (notably round10-13). Clarified round49-2 loses in
one held-out fold even though full-fit training anchors all hold. One extreme wrong-
direction fold margin on round47-15 is not calibrated confidence. Coefficients vary
substantially between folds; do not interpret them as monetary percentages.

Decision: gain in complete judgments is consistent enough to justify small aggregate
direction loss under requested joint objective. Original strict-gate result preserved;
this explicit user-requested review supersedes it. Overlapping repeats are exploratory,
not independent significance or fresh prospective evidence. Evidence remainsv27.

Verification: tare-predictor-equivalence.json covers all1,562,500 ordered pairs,616
unique historical scalar pairs and2000 random scalar pairs; exact features/scores and
classifications match saved candidate. Only output model tag changes.12 tests pass;
1000 pure5lb cases,50 zero-shade130 cases and3000 checks that5lb heavier never earns
an advantage in active compensation context. Runtime/model config and audit receipts
are self-contained; no lookup of answers during prediction. No new uncertainty policy.

Files: predictor_v27.py,model-config-v27.json,tare-compensation-selection-audit.json,
tare-predictor-equivalence.json,test_predictor_v27.py. Candidate model is pair-dependent,
not a transitive standalone price/dollar estimate.

## Remaining-premium refinement tested — one bounded tare-context coefficient

Audit remaining-premium-audit-v27.json decomposes WesternEurope round44-8: correct
signed margins0.667-0.750 but boundary1, per5lb penalty0.833-0.875 in most folds.
Related WCAamber/copper round44-9 andEEamber round37-2 share younger-but5lb-heavier
structure. Pure-provenance missed premiums are separate, not targeted by this change.

Added one coefficient to19-weight matched-vintage model (20total): attenuate5lb tare
penalty when provenance matches, vintage gap5years, younger<=30 and younger5lb heavier.
Cap attenuation<=tare weight, so heavier never earns a reward. Older35vs40 bracket
excluded. Sameevidencev27/objective/folds and train-only3-anchor protection.
                                v26       parent19     candidate20
Both-axis correct/163           141.8     142.8        146.2
Both-axis accuracy              86.99%    87.61%       89.69%
Direction                       93.10%    93.00%       92.76%
False premiums/repeat           14.6      13.8         14.6
Missed meaningful/repeat         9.4      12.0          8.8
WesternEurope target recovered5/5 from0/5 parent, WCA4/5 from0/5, EE5/5 from1/5.
Three clarified anchors preserved fullfit; target misses not hardcoded constraints.
Direction slight decline vs v26 fails prespecified nonregression gate: predictor.py/
model-config.json stayv26. Candidate saved tare-compensation-candidate-v27.json.
Do not claim this is uniformly better; direction losses listed in findings (mostly
but not entirely direction-only older records). Full fit attenuation nearly cancels
contextual5lb penalty; scores are not money and no causal identification claimed.

12 tests pass including1000 pure5lb cases,50 zero-shade130 checks and3000 active-context
monotonicity checks. Evidence unchanged; no new elicitation. Reused-family/adaptive
validation exploratory. Files tare_compensation_v27.py,tare-compensation-protocol-v27.json,
tare-compensation-validation-v27.json,tare-compensation-findings-v27.json,
test_tare_compensation_v27.py.

## Refined one-context model tested — same19 coefficients, v26 retained

Loss audit of anchored domestic20 candidate: top3 full-judgment losses are foreign
same-provenance5-year golden/pale trades (round41-6,round42-2,round44-8), eachv26 5/5
versus candidate0/5. All3 original anchors plus foreignround41-6 infeasible under
that domestic-only mechanism. Replacing its extra feature with matched-provenance
5-year golden/pale bonus makes them feasible, using the SAME19 coefficient count.

Same evidencev27/objective/folds/solver budget, train-only protection of3 anchors:
                              v26      domestic20    matched-vintage
Both-axis correct/163         141.8    140.4         142.8
Both-axis accuracy            86.99%   86.13%        87.61%
Direction                     93.10%   93.40%        93.00%
False premiums/repeat         14.6     17.2          13.8
Missed meaningful/repeat       9.4     13.4          12.0
Round41-6/42-2 recovered5/5 each;round44-8 stays0/5 joint. Original3 clarified anchors
preserved in full fit. Slight direction drop and more missed meaningful versusv26
fail prespecified promotion checks; current predictor.py/model-config.json stayv26.
Refinement saved as matched-vintage-candidate-v27.json, promoted:false.

Cost of refinement: feature is comparison-dependent, not offering-level; no global
transitive standalone price claim. Per-case lookup absent. Zero130 and pure5lb rules
preserved. Hypothesis follows error inspection; validation exploratory, no prospective
claim. Candidate improvement is real within this validation but not dominance on all
axes. Evidence untouched. Files domestic-vintage-loss-audit-v27.json,
matched-vintage-protocol-v27.json,matched-vintage-context-validation-v27.json,
matched-vintage-context-findings-v27.json,matched_vintage_context_v27.py,
test_matched_vintage_context_v27.py.

## Smallest context test — domestic20-year bonus, v26 retained

Evidencev27 unchanged. Added exactly1 coefficient to simple18-weight additive utility:
domestic AND20years bonus. This distinguishes domestic20vs25 vintage contribution from
foreign without lookup/pair exceptions.19 coefficients total. Feasibility:18 fails the
three-anchor check,19 succeeds. Full fits, with and without training-anchor protection,
classify allthree correctly. No proof this is the unique/true economic mechanism.

Same25 withheld-family fits and joint objective:
                              v26    additive18   domestic20   protected domestic20
Both-axis correct/163         141.8  137.0        137.8        140.4
Direction                    93.10% 93.35%       92.91%       93.40%
False premiums/repeat        14.6   18.6         18.6         17.2
Missed meaningful/repeat      9.4   16.8         15.6         13.4
Protected anchors enforced ONLY when present in training, never held-out. Unforced
full fit also reconciles all3; anchoring is a controlled additional requirement, not
hidden label leakage. MILP single-thread bounds/time/gaps recorded; numerical tolerance
not exact mathematical optimality. Reused-family/hypothesis-informed evaluation exploratory.

v26 stays canonical predictor.py/model-config.json. Both candidate configs saved:
domestic20-candidate-v27.json/domestic20-anchored-candidate-v27.json, promoted:false.
Near-boundary fitted margins mean categorical reconciliation, not dollar calibration.
Allpure5lb andzero-shade130 checks pass. Sources and evidence unchanged, no elicitation.
Artifacts domestic_vintage_context_v27.py,domestic-vintage-context-protocol-v27.json,
domestic-vintage-context-validation-v27.json,domestic-vintage-context-findings-v27.json,
test_domestic_vintage_context_v27.py.

## Evidence v27 reconciled — consolidatedv26 remains best tested predictor

Round49 and14 final Round50 judgments incorporated by unordered pair.587 unique
pairs;406 supplied directions,335 size targets,163 both-axis labels;252 missing sizes.
Three Round49 labels corrected in-place (2/6/16), full history retained. Round50-Q4
retracted meaningful response is history only. Ten unresolved registry pairs remain
separate from practical similarity; nine unlabelled rows excluded from objective.
No duplicate weights. Raw explanations/context retained in evidence-v27.json.

Compared frozenv26, fresh18-coefficient additive,19-coefficient additive with domestic
pale increment, and refitted19-coefficient v26 context structure, using same joint
objective/family splits. Additive utility uses only provenance,shade,age-step,tare and
mandatory pale=golden at130lb per-offering rule. Tare+pale cap preserves every5lb step.
No pair gates,correction offsets or variable thresholds in simple models. A separate
MILP optimizer check also tested18-weight additive; all25 fits met0.1% relative gap
criterion, not an exact optimality claim. All experiments retained.

                           v26      additive18   additive19   context refit
Both-axis correct/163      141.8    140.4        139.6        140.0
Direction                  93.10%  94.33%       94.78%       93.40%
Balanced meaningfulness    92.57%  89.79%       89.18%       91.72%
False premiums/repeat      14.6    17.2         17.6         11.0
Missed meaningful/repeat    9.4    14.4         15.6         13.2
MILP additive both137.0/163, false18.6, missed16.8. Thus selected working runtime
remains predictor.py/model-config.json (v26). Evidencev27 is current; no new math
promoted just to create a version. See model-selection-v27.json for complete receipt.

Concrete additive incompatibility: round49-2 corrected A preference requires P+T>V+S;
round50-4 practical provenance requires P<M;round49-17 meaningful domestic younger
golden with5lb tare disadvantage requires V-T-D>M. Nonnegative shade premiums imply
P>M, contradiction. Each2-row subset is feasible. Thus globalcommon additive weights
and common meaningfulness threshold cannot fit all3 even with separate domestic shade.
This does NOT mean user judgments contradict each other; their contexts differ. No
extra explanation needed to establish this limitation. Local14-judgment feasibility
still holds; it was never proof of global adequacy. See additive-conflict-v27.json.

Reused-family evidence exploratory. Safeguards tested on1000 pure5lb and50 zero-shade
pairs per fitted model. New code:joint_models_v27.py,additive_milp_v27.py;results
joint-models-validation-v27.json/additive-milp-validation-v27.json;tests
 test_joint_models_v27.py. No active elicitation round.

## Round50 complete — explanation-led isolation of three recurring cases

14 active judgments, raw explanations and retractedQ4 meaningful answer preserved.
Three source clarifications pending next evidence version: round49-2 -> A/slight/practical
(Q50-1);round49-16 -> A/slight/practical(Q50-8);round49-6 -> A/slight/practical(Q50-13).
Q50-14 NW/WE golden25/120 approximately same price, no cost-based direction, not an
exact-equality instruction. Positive small premiums kept separate from ties.

All14 active judgments are feasible under a local monotone19-feature additive utility
with normalized meaningfulness boundary. This does NOT prove global additivity or
unique weights, and explanatory context alone does not require additional interaction
terms. Important correction to earlier inference: do not assume new complexity is
necessary before testing corrected labels. Feasibility witness not fitted/deployed.
All14 prediction snapshots/source hashes verified; no refit/evidence version change.
No active questionnaire. Next incorporation must reconcile original IDs and avoid
duplicate weights for repeated isolation pairs. Receipts round50-isolation.json,
round50-findings.json,round50-consistency-check.json.

## Active explanation-led isolation — Round50

User requests recurring weakness one comparison at a time with full explanations.
First exact pair is round49-2, saved in round50-isolation.json. No invented total;
subsequent isolation adapts to explanation. Record raw reasoning and separate facts
from model inference. Current model/config frozen for elicitation. Q1 contextual explanation saved:20-25 vintage sensitivity reduced,copper/pale premium small,WE provenance and lower tare more important. Overall now A/slightly/practical, correcting round49-2; explanation retained and reconciliation pending. Q2 B/slightly/practical confirmed. Q3 A/slightly/practical confirmed; provenance outweighs shade at25years125lb. Q4 corrected to A/slightly/nonmeaningful, nottie; initial meaningful answer retracted. Q5 B/slightly/practical, positive shade premium explicitly nottie. Q6 B/meaningful for vintage alone confirmed. Q7 A/slightly/practical confirmed, positive tare premium. Seven active judgments locally algebraically consistent (round50-first-family-check.json), no weights inferred. Q8 A/slightly/practical confirmed, nottie; corrects round49-16 size. Q9 B/slightly/practical, nottie. Q10 B/slightly/practical confirmed, nottie. Q11 B/meaningful pure brown-to-amber premium confirmed. Q12 A/slight/practical confirmed; brown/amber family mathematically feasible (round50-second-family-check.json). Q13 A/slight/practical corrected,115lb lightness narrowly beats WE provenance. Q14 changesonly A tare115to120; pure provenance comparison awaiting answer.

## Round49 complete — broader consolidatedv26/v25 comparison

V26 direction13/16,size15/17,both12/15 vs v25 direction14/16,size14/17,both11/15.
Mixed result, not dominance. Q1 slightly is direction-only;Q9/Q10 unresolved/not
ties;Q18 practical provenance tie, not zero latent provenance. Both zero-shade1/1,
no false meaningful calls. Q2 is v26 direction regression on fresh WE copper25/120
vs SEA pale20/125 (userB meaningful,v26 A practical,v25 B practical); known
cross-provenance copper/pale weakness recurs. SharedQ6 provenance/tare slight
direction miss andQ16 WEbrown/NWamber mixed direction+size miss. Q17 v26 sizegain.
All40 predictions/source hashes verified. No refit or evidence incorporation;
evidencev26/runtime predictor.py remain. No active round. Receipts round49-fixed.json
and round49-findings.json. Fresh selected pairs, not random population accuracy.

## Active Round49 — consolidatedv26 versusv25

20 fresh unordered comparisons, reverse duplicates checked against all saved rounds/
evidence. Broader variety across all10 provenances,shade/vintage/tare and mixed
tradeoffs/controls. Design precedes model calls. All40 predictions and source hashes
frozen in round49-fixed.json. Present5 at a time; hide predictions/interim scores,
separate direction/meaningfulness, unresolved allowed. Q1 A/slightly size unspecified;Q2 B/meaningful,Q3 A/meaningful,Q4 A/practical,Q5 A/meaningful. Q6 B/practical,Q7 B/meaningful,Q8 zero-shade tie,Q9/Q10 unresolved/not ties. Q11 A/practical,Q12 A/meaningful,Q13 B/meaningful,Q14 A/meaningful,Q15 A/practical. Awaiting batch Q16-20.

## Current predictor — selected v26, consolidated without mathematical changes

Use `predictor.py` with `model-config.json`. This is the canonical runtime/config;
NumPy is its only non-standard runtime dependency. It imports no historical model,
fitting, solver or evidence modules. Historical scripts remain reference snapshots.

```python
from predictor import Model
model = Model()
result = model.compare(
    ["Western Europe", "golden", 25, 120],
    ["Western Europe", "pale/straw", 30, 120],
)
```

CLI: `.venv-regional/bin/python predictor.py --a '["central","golden",25,120]' --b '["central","golden",30,120]'`

Configuration explicitly separates fitted weights, offset reference weights, shade
context, five-year multiplier, older/microshade offsets, provenance-boundary references
and classification tolerances. The reference-offset arithmetic and separate boundary
additions are deliberately preserved for numeric parity. `model_id` retains the legacy
v26 candidate string solely for exact output compatibility; selection_status is selected.
No new confidence/abstention or dollar-price behaviour has been added.

Selection audit: v26 wins joint balanced accuracy and direction in5/5 repeats, both-axis
count in4/5; paired both-axis changes +7,+5,-1,+3,+3. False premiums improve3/5,one equal,
one worse. Mean both-axis124.2/138 versus120.8; direction93.26% versus91.05%;false premiums
8.8 versus12.4. The old one-decision meaningful regression was NET11 losses/10 gains,
not one isolated loss. One loss reverses direction (round45-11), and that case also
remains wrong in the full-data v26 fit. Selected for stronger overall results with that
explicit limitation; original gate outcome remains untouched. Repeats overlap: no
claim of statistical independence/significance or a fresh prospective result.

Equivalence receipt: predictor-equivalence.json checks all1,562,500 ordered pairs in
the supported1250-offering domain, plus exact scalar historical and random calls.
No direction/meaningfulness changes versus savedv26. Numeric differences reported in
receipt rather than hidden. Test suite: test_predictor.py. Model-selection-audit.json
retains every loss/gain event and per-repeat results. Evidence remainsv26.

## Evidence v26 reconciled — joint refit saved as candidate

Latest Rounds46/47 appended and Round48 reconciled into original source IDs with
history retained.556 main-table records,380 supplied directions,307 size labels,
138 both-axis labels. Eight unresolved pairs remain separate from ties: round27-11,
round42-3/10/12,round45-12,round47-1/12/18. Seven are completely unlabelled main rows;
round27-11 registry-only. They contribute no training/scoring labels. round27-7 now
Blean with size unspecified, added once; round38-3 now practical/no clear direction.

All19 underlying weights refitted with joint correctness, v25 context/boundary and
older/microshade residual offsets frozen. Same25 family splits extended label-free.
                                  v25       refit candidate
Both-axis correct (138)           120.8     124.2
Both-axis accuracy                87.54%    90.00%
Direction (380)                   91.05%    93.26%
Balanced meaningfulness           92.59%    93.38%
False premiums/repeat             12.4       8.8
Missed meaningful/repeat           9.0       9.2
Correct meaningful direction      92.8      92.6
One lost correct meaningful decision across5 repeats triggers predeclared no-loss
gate; candidate NOT silently promoted. Current working runtime remains pricing_v25.py
and older-dark-scoped-delivery-v25.json. New candidate runnable via pricing_v26.py
loading joint-refit-candidate-v26.json. joint-refit-delivery-v26.json records fallback
v25. No claim that every metric improved. Evidencev26 is current for next work.

Tests: family separation, refit replay, scores, old523 margins, source hashes,
unlabelled-row deletion invariance, no lookup/orientation,1000 pure5lb,50 zero-shade130
and250 matched amber/copper cases. Reused-family validation exploratory, no prospective
claim. No active questionnaire and baselines unchanged. Reconciliation complete; no
pending corrections fromRound48. Artifacts evidence-v26.json,benchmark-targets-v26.json,
joint-refit-validation-v26.json,joint-refit-candidate-v26.json,joint-refit-findings-v26.json,
joint_refit_v26.py,pricing_v26.py,test_joint_refit_v26.py.

## Round48 complete — unresolved-pair audit

All10 neutral revisits saved. Eight remain explicitly unresolved/not ties: revisit
Q2/4/5/6/7/8/9/10 (source round27-11,round42-3/10/12,round45-12,round47-1/12/18).
RevisitQ1/source round27-7 now Blean, direction resolved but size unspecified.
RevisitQ3/source round38-3 now explicit practical similarity/no clear direction.
No labels inferred from very close. Models/predictions unchanged;all20 predictions
recomputed/source hashes verified. Evidence remainsv25; reconciliation pending, not
duplicate weighting. No active questionnaire. These repeated pairs are not fresh
accuracy. Receipts round48-fixed.json/round48-findings.json.

## Active Round48 — all10 remaining unresolved pairs

Neutral one-at-a-time revisits frozen in round48-fixed.json; no prior answers or
predictions displayed. Registry/active evidence and historical deferred rounds audited;
already-resolved deferred pairs excluded. Includes missing-axis round38-3. Source IDs
round27-7/11,round38-3,round42-3/10/12,round45-12,round47-1/12/18. Q1 direction resolved B/lean; meaningfulness unspecified. Q2 still unresolved/not tie; provenance or tare differentiator needed. Q3 resolved no clear direction/practically similar; taste-dependent provenance comparison. Q4 still unresolved/not tie; younger vintage versus10lb tare between premium provenances. Q5 still unresolved/not tie; Northeast provenance and5lb tare versus five-year younger vintage. Q6 still unresolved/not tie; younger vintage versus lighter amber and10lb tare. Q7 still unresolved/not tie; younger vintage versus Northeast provenance and10lb tare. Q8 still unresolved/not tie; Southeast vintage/provenance versus lighter amber and10lb tare. Q9 still unresolved/not tie; younger vintage versus Northwest provenance,amber and5lb tare. Q10 awaiting answer.
Both models fixed, direction/meaningfulness separate; unresolved remains available.
Repeated pairs, not fresh predictive accuracy. No evidence changes during revisit.

Round47 finished: v25 direction14/15,size15/17,both13/15;v24 12/15,14/17,10/15.
Both zero-shade1/1. Q1/12/18 unresolved/not ties. All40 predictions rechecked.
Receipts round47-fixed.json/round47-findings.json.

## Active Round47 — v25 versus v24

20 fresh unordered comparisons checked against all saved rounds/evidence, including
reversed orientation. Older-vintage,microshade,brown,regional and mixed-attribute
challenges plus zero-shade/pure5lb controls. Selection precedes prediction calls.
All questions and40 predictions frozen in round47-fixed.json. Present five at a time;
hide predictions/interim scores; direction/meaningfulness separate; unresolved
available. Explicit tie/zero-premium checks separate. Q1 unresolved/not tie;Q2 A/meaningful,Q3 A/meaningful,Q4 B/practical,Q5 A/meaningful. Q6/7/8/10 A meaningful;Q9 tie/zero-shade130. Q11/13 B meaningful;Q12 unresolved/not tie;Q14 no meaningful provenance premium;Q15 A meaningful. Awaiting batch Q16-20. No refits.

## Round46 complete — v25 matched all supplied judgments

V25 direction11/11,size11/11,both10/10,zero-shade1/1 versusv24 8/11,10/11,7/10,1/1.
Q6 slightly remains direction-only, size excluded. V25 fixes Q1 older35vs40 golden/pale
direction+size andQ2/Q7 small amber/copper direction. Other supplied controls/tradeoffs
pass for both. All24 predictions recomputed and source hashes verified; evidence
staysv25, no refit/active questionnaire. Small varied fresh-pair test, not universal
accuracy or resolution of earlier brown/amberQ45-8 and unresolved mixed tradeoffs.
Receipts round46-fixed.json/round46-findings.json.

## Active Round46 — v25 versus v24

12 fresh unordered comparisons checked against all saved rounds/evidence, including
reversed orientation. Older-vintage,microshade,brown,regional and mixed-attribute
challenges plus zero-shade/pure5lb controls. Selection precedes prediction calls.
All questions and24 predictions frozen in round46-fixed.json. Present one at a time;
hide predictions/interim scores; direction/meaningfulness separate; unresolved
available. Explicit tie/zero-premium checks separate. Q1 recorded A/meaningful; younger golden35 beats pale40 at West Central Asia110lb. Q2 recorded A/practically similar; amber-copper shade advantage slight at Domestic Southeast25years115lb. Q3 recorded A/meaningful; younger vintage,10lb lower tare and Western Europe provenance outweigh lighter amber. Q4 recorded B/meaningful; younger golden20 beats pale25 at Eastern Europe120lb. Q5 recorded B/meaningful; pure15lb lower tare gives clear advantage. Q6 recorded A/slightly; meaningfulness unspecified, vintage outweighs provenance and5lb. Q7 recorded B/practically similar; amber shade advantage slight at Western Europe20years125lb. Q8 recorded tie/no adjacent shade premium at130lb. Q9 recorded B/meaningful; younger vintage and lighter shade outweigh A5lb tare advantage. Q10 recorded A/practically similar; pure5lb tare advantage slight, not meaningful. Q11 recorded A/meaningful;10-year younger vintage outweighs B10lb tare advantage. Q12 awaiting answer. No refits.

## Evidence v25 — older-vintage and small shade fixes delivered

Rounds44/45 appended:523 records,353 supplied directions,278 size targets,245 missing
sizes. All491 parent rows unchanged. Q45-12 remains explicitly unresolved on both
axes; Q45-1/2 slightly remain direction-only. Previous unresolved registry/history intact.
No questionnaire. New runtime pricing_v25.py uses older-dark-scoped-delivery-v25.json.

Initial additive changes fixed examples but added false premiums (revision-7 and
round10-19); preserved in older-dark-validation-v25.json. Follow-up narrows35vs40
adjustment to matched-provenance golden/pale, microshade to amber/copper with other
attributes identical. Combined selected, full parameters[1.4,0,0.1] in documented
feature units. Only older-age and microshade changes active; brown increment0.
Q45-5/20 andQ45-3 fixed in full fit. Q45-8 brown/amber mixed comparison remains wrong;
do not claim all dark-shade tradeoffs solved or full fit as prospective accuracy.

Matched5-repeat family validation on523 rows:
                                frozenv24    selectedv25
Both-axis correct (113)         97.6         99.4
Both-axis accuracy              86.37%       87.96%
Direction (353)                 91.10%       91.39%
Balanced meaningfulness         91.74%       92.81%
False premiums/repeat           10.8         10.8
Missed meaningful/repeat         9.2          7.4
Original491 v24 margins/radii reproduce. All fitting training-only; repeated/adaptive
hypothesis testing exploratory, not independent random accuracy. Pure5lb and zero-
shade130 rules retained;1,000 pure5lb and50 zero-shade combinations tested at max
adjustments too. Models/evidence baselines unchanged.

Artifacts evidence-v25.json,benchmark-targets-v25.json,older_dark_scoped_v25.py,
older-dark-scoped-validation-v25.json,older-dark-scoped-delivery-v25.json,
older-dark-findings-v25.json,pricing_v25.py,test_older_dark_v25.py.

## Round45 complete — broader frozen test

V24 direction13/17,size13/17,both10/15 vs joint-refit13/17,size12/17,both9/15.
No false premiums;v24 missed meaningful4,baseline5. Q1/Q2 slightly retain direction
only; Q12 explicitly unresolved on both axes, not tie. Q7 practical/no-clear direction,
not zero provenance; Q16 zero-shade separate1/1 both. Shared missesQ3 microshade
direction (amber/copper),Q5/Q20 older35vs40 low-tare shade/vintage direction+size,
Q8 domestic brown/amber mixed tradeoff direction+size,Q15 cross-provenance size.
V24 fixes Q13 size. Pure5lb,20lb,10year andzero-shade controls pass. Broader fresh
attribute-stratified batch, small/not population accuracy; prior narrow12/12 not
universal. All40 predictions recomputed and source hashes intact. No refit/evidence
incorporation; evidence remainsv24, no active questionnaire. Receipts:
round45-fixed.json and round45-findings.json.

## Active Round45 — joint weight refit versus v24

20 fresh unordered comparisons checked against all saved rounds/evidence, including
reversed orientation. Broader domestic/foreign/provenance/shade/vintage/tare tradeoffs and controls. Selection precedes prediction calls.
All questions and40 predictions frozen in round45-fixed.json. Present one at a time;
hide predictions/interim scores; direction/meaningfulness separate; unresolved
available. Explicit tie/zero-premium checks separate. Q1 recorded A/slightly; meaningfulness unspecified, vintage weighting explanation retained. Q2 recorded B/slightly and close; meaningfulness unspecified. Q3 recorded A/practically similar; amber-copper shade advantage slight at Domestic Central30years120lb. Q4 recorded B/meaningful; younger vintage and5lb lower tare outweigh Western Europe provenance. Q5 recorded A/meaningful; younger golden35 beats pale40 at Eastern Europe115lb. Q6 recorded A/meaningful; pure20lb tare advantage clear with other attributes matching. Q7 recorded no clear direction/practically similar; provenance lacks meaningful premium at this35-year context. Q8 recorded B/meaningful; amber shade and5lb lower tare outweigh younger vintage and Southwest provenance. Q9 recorded B/meaningful;10-year younger vintage outweighs shade and10lb tare advantages. Q10 recorded A/practically similar; pure5lb tare advantage slight, not meaningful. Q11 recorded B/meaningful; younger vintage and lighter shade outweigh Western Europe provenance and5lb tare advantages. Q12 unresolved on both axes, explicitly not a tie; younger vintage versus Northeast provenance and10lb tare. Q13 recorded B/meaningful; younger vintage outweighs adjacent shade and5lb tare advantages. Q14 recorded B/meaningful; amber shade clearly favored over brown with other attributes matching. Q15 recorded B/meaningful; younger vintage and5lb lower tare outweigh Central provenance and lighter shade. Q16 recorded tie/no adjacent shade premium at130lb. Q17 recorded B/meaningful; pure10-year younger vintage advantage clear. Q18 recorded A/meaningful; younger vintage and15lb lower tare outweigh lighter copper shade. Q19 recorded A/practically similar; Southeast provenance advantage slight with other attributes matching. Q20 awaiting answer. No refits.

## Round44 complete — v24 matched all supplied judgments

Frozen prospective targeted test: v24 direction10/10,size12/12,both axes10/10,
zero-shade2/2. Joint refit direction8/10,size8/12,both6/10,zero2/2. Baseline misses
Q1/4 direction andQ1/2/4/6 size. V24 fixes those while preserving pure5lb,zero-shade,
same-age shade and other-shade controls in this batch. All24 predictions recomputed
and source hashes verified.12 fresh exact pairs but familiar targeted families;
do NOT generalize to100%population accuracy. Models and evidence remain unchanged
(v24); no active questionnaire. EarlierQ42-3/10/12 still unresolved. Receipts:
round44-fixed.json and round44-findings.json.

## Active Round44 — joint weight refit versus v24

12 fresh unordered comparisons checked against all saved rounds/evidence, including
reversed orientation. Five-year golden/pale,domestic,mixed-tare and other-shade
challenges plus zero-shade/pure5lb controls. Selection precedes prediction calls.
All questions and24 predictions frozen in round44-fixed.json. Present one at a time;
hide predictions/interim scores; direction/meaningfulness separate; unresolved
available. Explicit tie/zero-premium checks separate. Q1 recorded A/meaningful; younger golden25 beats pale30 at Western Europe110lb. Q2 recorded B/meaningful; younger golden30 beats pale35 at Eastern Europe110lb. Q3 recorded A/practically similar; pure5lb tare advantage slight, not meaningful. Q4 recorded A/meaningful; younger golden25 beats pale30 at West Central Asia115lb. Q5 recorded tie/no adjacent shade premium at130lb. Q6 recorded B/meaningful; younger golden20 beats pale25 at Domestic Northwest120lb. Q7 recorded B/practically similar; adjacent shade alone slight at Eastern Europe30years125lb. Q8 recorded A/meaningful; younger vintage outweighs B adjacent shade and5lb tare advantages. Q9 recorded A/meaningful; younger vintage and lighter amber shade outweigh B5lb tare advantage. Q10 recorded B/meaningful; younger vintage outweighs A adjacent shade and5lb tare advantages. Q11 recorded tie/no adjacent shade premium at130lb. Q12 awaiting answer. No refits.

## Evidence v24 — clarifications reconciled, five-year fix selected

491 rows, no duplicate weighting. round36-9/12 active labels superseded by explicit
neutral115lb revisits, both younger golden25 meaningfully beats pale30; prior records
retained in clarification_history. Other489 rows unchanged. Q42-3/10/12 decomposed
using existing evidence and remain unresolved on BOTH axes, not ties/practical labels.
Crux:Q3 vintage vs10lb+cross-provenance;Q10 vintage vsprovenance+5lb;Q12 vintage vs10lb+
copper/amber shade. Existing pure5lb control alone does not establish net tradeoff.
No additional questionnaire or guessed preferences. See unresolved-isolation-v24.json.

Selected runtime pricing_v24.py / five-year-premium-delivery-v24.json. Same five-year
experiment asv23, now corrected labels. One coefficient0.5 boosts existing age-step
score50% for matched provenance/exact5year/golden-pale contrasts; NOT a dollar premium.
Broader all-shade scope adds false premiums and is rejected. Underlying joint-refit
weights/boundaries and all baseline artifacts unchanged.

Same5 repeated family validations on491 rows:
                               frozen joint refit   selected adjustment
Both-axis correct (88)         72.0                 77.8
Both-axis accuracy             81.82%               88.41%
Direction (326)                90.61%               91.35%
Balanced meaningfulness        88.66%               93.12%
False premiums/repeat          10.6                 10.6
Missed meaningful/repeat       11.0                  5.2
Full fit now selects nonzero0.5 (v23 selected0); both115lb clarified pairs andQ42-1/6/8
fit correctly. Those are training checks, not prospective accuracy. Samefold reuse
exploratory, frozen baseline rescored on samev24 targets. Zero130 and1000 pure5lb
comparisons preserved; unresolved3/10/12 outside selected scope/predictions unchanged.

Artifacts evidence-v24.json, benchmark-targets-v24.json, unresolved-isolation-v24.json,
five-year-premium-validation-v24.json, five-year-premium-delivery-v24.json,
five-year-premium-findings-v24.json, pricing_v24.py,test_five_year_premium_v24.py.

## Round43 complete —115lb clarifications saved

Both neutral revisits explicitly prefer golden25 over pale30 meaningfully at115lb:
EasternEurope Q1=B,WesternEurope Q2=A. Saved in round43-fixed.json; do not display
prior answers during revisits. Source IDs round36-9/round36-12 await reconciliation
in next evidence version, retaining original history and avoiding duplicate weighting.
Models/source hashes and predictions verified unchanged. Evidence remainsv23, no
refit or active questionnaire. Repeated pairs, not fresh prediction accuracy.

## Active Round43 — neutral115lb revisits

Two earlier115lb comparisons revisited one at a time, no earlier answers/predictions
displayed. round43-fixed.json freezes pair order/predictions and model source hashes.
Separate direction/meaningfulness; unresolved allowed. Repeated pairs, not fresh
accuracy. Q1 recorded B/meaningful; Q2 awaiting answer. No model or evidence changes during elicitation.

## Evidence v23 — five-year premium tested, runtime unchanged

Round42 appended without changing479 parent records.491 rows;326 supplied directions,
249 size targets,242 unspecified sizes. Q42-3/10/12 remain explicitly unresolved on
BOTH axes and are listed in unresolved registry, not ties/practical labels. Prior
EasternEurope correction and older unresolved pairs preserved. No questionnaire.

One-coefficient fractional boost of existing5-year vintage step tested under two
scopes: same-provenance golden/pale only, and all same-provenance exact5-year contrasts.
Same frozen joint-refit weights/thresholds, original25 family partitions extended.
Coefficients fit from training labels only with joint objective.
                                     frozen refit   broader5-year fit
Both-axis correct (88)               72.0           73.4
Both-axis accuracy                   81.82%         83.41%
Direction (326)                      90.61%         90.61%
Balanced meaningfulness              88.95%         90.22%
False premiums/repeat                11.6           11.6
Missed meaningful/repeat             10.0            8.4
Targeted adjacent-only also73.4/88 but slight direction/false-premium regressions.
Broader scope passes validation gates BUT full-data fitted coefficient0. Both scopes
select0 on full evidence. Thus NO runtime behavior change/promotion claimed. Current
pricing_joint_weights_v22.py remains working model. five-year-premium-delivery-v23
contains selected procedure with zero fraction, not a newly changed prediction model.

Diagnostic fraction.5 fixes recent examples but disturbs earlier practical and pale-
favoring tradeoffs. Full macro joint95.43% falls93.91%;both-axis count stays83/88.
Examples round36-9/12 (EE/WE115 pale30 vs golden25), revision-7 and broader brown/pale
comparisons. Evidence unchanged, no forced weighting or inferred labels. Old479
baseline margins reproduce. Reused-family results exploratory, not fresh accuracy.
Tests cover1000 pure5lb and50 zero-shade130 cases even at maximum adjustment.

Artifacts evidence-v23.json, benchmark-targets-v23.json, five_year_premium_v23.py,
five-year-premium-validation-v23.json, five-year-premium-delivery-v23.json,
five-year-premium-findings-v23.json, test_five_year_premium_v23.py.

## Round42 complete — frozen joint weight comparison

Joint refit direction6/7,size6/9,both axes4/7 versus v21 direction5/7,size5/9,both3/7.
Q3/Q10/Q12 unresolved on BOTH axes and excluded, never ties/practical labels. Q10/Q12
explicitly not ties. Explanations preserved. Refit missesQ1 direction+size (EE110lb
golden25 vs pale30),Q6 size (WE115lb golden30 vs pale35),Q8 size (domesticCentral125lb
pale25 vs golden20). Q2 meaningfulness fixed. Zero-shadeQ4/Q9 and pure5lbQ5/Q11 allpass
for both. All24 frozen predictions recomputed and source hashes intact. No active
questionnaire/refit/evidence change; evidence staysv22. Small targeted fresh-pair
sample, not population accuracy. Receipts round42-fixed.json/round42-findings.json.

## Active Round42 — joint weight refit versus v21

12 fresh unordered comparisons checked against all saved rounds/evidence, including
reversed orientation. Low-tare,young-vintage,mixed-tare,regional and other-shade
challenges plus zero-shade/pure5lb controls. Selection precedes prediction calls.
All questions and24 predictions frozen in round42-fixed.json. Present one at a time;
hide predictions/interim scores; direction/meaningfulness separate; unresolved
available. Explicit tie/zero-premium checks separate. Q1 recorded A/meaningful; younger golden25 beats pale30 at Eastern Europe110lb. Q2 recorded B/meaningful; younger vintage outweighs adjacent shade and5lb tare advantages. Q3 very close premium-vintage/10lb tradeoff; both axes unresolved, explanation retained. Q4 recorded tie/no adjacent shade premium at130lb. Q5 recorded A/practically similar; pure5lb tare advantage slight, not meaningful. Q6 recorded A/meaningful; younger golden30 beats pale35 at Western Europe115lb. Q7 recorded A/meaningful; younger vintage outweighs B adjacent shade and5lb tare advantages. Q8 recorded B/meaningful; younger golden20 beats pale25 at Domestic Central125lb. Q9 recorded tie/no adjacent shade premium at130lb. Q10 unresolved on both axes; explicitly not a tie, provenance/tare versus vintage tradeoff. Q11 recorded A/practically similar; pure5lb tare advantage slight, not meaningful. Q12 awaiting answer. No refits.

## All-weight joint refit — direct objective selected

Full-fit target check:Q41-6 now B meaningful;Q41-7 now correct B direction but still
understates meaningfulness. All19 weights free;12 materially changed.

Evidencev22 unchanged. New working comparator pricing_joint_weights_v22.py loads
 direct-joint-weights-delivery-v22.json. All19 underlying weights refitted under
monotone increments/pure5lb cap/domestic adjacent-shade cap. V21 context functions
and boundary/proximity reference mapping frozen; not just two residual adjustments.
Golden/pale shade cancels at both130 by feature transformation. This remains a pair
comparator, not a transitive dollar-price model. All baseline artifacts preserved.

Same5 repeated family splits on479 rows:
                                  v21       direct joint refit
Both-axis correct (81)            62.2      67.2
Both-axis accuracy                76.79%    82.96%
Direction (319)                   90.03%    90.53%
Balanced meaningfulness (240)     87.25%    90.09%
False meaningful/repeat           14.4      11.6
Missed meaningful/repeat           10.2       7.8
Correct meaningful direction      44.6      49.4

Primary joint-hinge QP and ridge sensitivities were weaker and preserved in
joint-weight-refit-validation-v22.json / joint-weight-ridge-check-v22.json.
Final direct correctness search adjusts all19 weights from2 TRAINING-only starts
(reference and weak-ridge). Deterministic coordinate optimizer, no global optimum
claim. Direct selection avoids smooth-loss solutions just across decision boundaries.
All outer families excluded from fitting. Multiple successive trials mean exploratory
reused-validation evidence, not fresh accuracy or independence. No new questionnaire.

Structural tests cover1000 pure5lb comparisons and50 zero-shade130 pairs for all5
refit variants. Baseline feature prediction equivalence and score reproduction pass.
Final artifacts direct-joint-weights-validation-v22.json,
direct-joint-weights-delivery-v22.json, joint-weight-refit-findings-v22.json,
pricing_joint_weights_v22.py, test_joint_weight_refit_v22.py. Earlier joint-weight-refit
DELIVERY file retains its failed primary experiment fallback; use direct-joint delivery.

## Joint-objective experiment on v22 — selected correction

Evidencev22 unchanged. New runtime pricing_joint_v22.py uses joint-objective-delivery-v22.json.
V21 and all prior baselines remain unchanged. Same two residual parameters/grid/bounds,
base coefficients and thresholds as previous controlled experiment. Only fitting objective
changed: require correct direction AND meaningfulness on fully labelled pairs; use only
supplied axes for partial labels. Four-group balance; signed joint hinge tie-break. A
signed-loss objective is a separate control. All fitting excludes held-out families.

                                v21       old separate     joint objective
Both axes correct (81)          62.2      63.0             63.2
Both-axis accuracy              76.79%    77.78%           78.02%
Joint balanced partial-label    83.93%    84.81%           85.07%
Direction accuracy (319)         90.03%    90.72%           90.97%
Magnitude-only balanced size    87.25%    86.22%           85.70%
False premiums                  14.4      14.4             14.4
Correct meaningful direction    44.6      44.8             44.8
Mean counts per5 repeated family validations.478 records have at least one supplied
axis; only81 have both. Do not call partial-label score complete pricing accuracy.
Full-fit parameters0.65 vintage/0.55 shade equal the previously tested combined
candidate. Objective-only gain is0.2 fully correct pairs/repeat, not the entire1.0
pair gain overv21. Magnitude-only size declines; new joint selection gates intentionally
focus on correct complete judgments and no false-premium/direction regression.

Diagnosis: wrong-way meaningful predictions previously received magnitude credit.
But objective is not the only obstacle: bounded residual cannot reach correct meaningful
Q41-6 in4/5 heldoutfits; Q40-9/Q41-12 in5/5. These are diagnostic attainable bounds,
never fitting/selection inputs. Old heldout weights can differ sharply from full fit;
missing family support and frozen base geometry limit repairs. Reused validation is
exploratory, not a new prospective result. No questionnaire or new evidence version.
Zero shade at130 and all1000 pure5lb comparisons retained.

Artifacts joint_objective_v22.py, joint-objective-validation-v22.json,
joint-objective-delivery-v22.json, joint-objective-findings-v22.json,
pricing_joint_v22.py, test_joint_objective_v22.py.

## Evidence v22 incorporated — v21 remains selected

Round41 appended; revision-13 explicitly corrected toB (EE120 golden25 beats pale30).
OldA/slightly record retained in correction_history; new size/strength unspecified.
Other466 prior rows unchanged.479 total;319 supplied directions,240 sizes,239 missing.
Round41 taste-dependent tie and explicit zero-shade statements preserved distinctly.
Correction incorporation receipt is this evidence/progress, not mutation of frozen
revision-13-correction.json (its historical pending status remains as originally saved).

Tested one vintage residual (fraction of20vs25 increment), one low-tare/mature-foreign
shade residual, and combination against frozen v21 on same extended family folds.
                               v21     vintage    shade      combined
Direction                      90.03%  90.72%     90.03%     90.72%
Balanced meaningfulness         87.25%  86.22%     87.25%     86.22%
False premiums/repeat           14.4    14.4       14.4       14.4
Missed meaningful/repeat        10.2    11.4       10.2       11.4
Correct meaningful direction    44.6    44.8       44.6       44.8
Direct size accuracy            87.43%  86.29%     87.43%     86.29%

Full-fit parameters0.65 vintage /0.55 shade fixQ41-6 andQ41-7 but do not establish
held-out generalization. Q7-family-held-out shade parameter0 all5 repeats. More
missing meaningful includes shrinking previously WRONG-direction confident premiums
in round40-9/round41-3/round41-12; do not portray those prior calls as joint successes.
Gates reject promotion, v21 remains default pricing_v21.py. Residual-fixes-delivery-v22
explicitly selects unchangedv21; evidencev22 is current for next work. No pricing_v22
runtime promoted, no questionnaire. Same1,000 pure5lb cases and50 zero-shade130lb cases
checked across arms. All old baseline predictions/source hashes intact; original467
baseline margins reproduce, scores reflect corrected target/new12rows. Reused-family
validation exploratory, not fresh prospective accuracy.

Artifacts: evidence-v22.json, benchmark-targets-v22.json, residual_fixes_v22.py,
residual-fixes-validation-v22.json, residual-fixes-delivery-v22.json,
residual-fixes-findings-v22.json, test_residual_fixes_v22.py.

## Round41 complete — frozen v21/v20 verified

V21 direction8/9,size10/12 versus v20 direction3/9,size9/12. Size magnitude alone
is not joint correctness: v20 meaningful predictions sometimes favor wrong offering.
V21 tie/no-direction checks3/3;v20 0/3. Q1/Q8 explicit zero-shade statements and
Q4 taste-dependent tie preserved distinctly. V21 missesQ6 size (WCA pale25/125
vs golden20/130, B direction correct but too small) andQ7 direction/size (EE
pale35/115 vs golden30/115, user B meaningful, both models A practical). Pure5lb
Q10 and domestic Q11 controls correct for both. All24 predictions rechecked, hashes
intact. No refit/evidence update; evidence staysv21. revision-13-correction.json
remains pending next evidence version. No active questionnaire. Targeted fresh
pairs, not random population accuracy. Receipts round41-fixed.json/round41-findings.json.

## Active Round41 — frozen v21 versus v20

12 fresh unordered pairs and predictions frozen in round41-fixed.json before answers.
Show one at a time, hide predictions/interim scores, separate direction/meaningfulness,
unresolved allowed. Explicit zero-shade claims checked separately. Q1 recorded tie/no adjacent shade premium at130lb. Q2 recorded B/meaningful; younger vintage outweighs adjacent shade and5lb tare advantages. Q3 recorded A/meaningful; younger vintage outweighs adjacent shade at West Central Asia115lb. Q4 recorded tie/no meaningful difference; taste/preference decides at Western Europe20years130lb. Q5 recorded A/meaningful; younger golden30 beats pale35 at Eastern Europe120lb. Q6 recorded B/meaningful; younger vintage outweighs adjacent shade and5lb tare advantages. Q7 recorded B/meaningful; younger golden30 beats pale35 at Eastern Europe115lb. Q8 recorded tie/no adjacent shade premium at130lb. Q9 recorded B/meaningful; younger vintage and lighter shade both favor B. Q10 recorded A/practically similar; pure5lb tare advantage slight, not meaningful. Q11 recorded A/meaningful; younger vintage outweighs adjacent shade at Domestic Northeast125lb. Q12 awaiting answer.
User correction saved in revision-13-correction.json: EE120 golden25 beats pale30;
meaningfulness unspecified. Earlier disagreement is superseded by clarification,
but frozen evidence/model artifacts remain intact until next evidence incorporation.
No refits during this round.

## Evidence v21 — broader shade/vintage correction delivered

Round40 appended without changing455 parent rows.467 total,310 supplied directions,
228 size targets,239 unspecified sizes. Three explicit zero adjacent shade premium
statements stored separately; not discarded as merely practical similarity. No new
questionnaire. Baseline models/code/evidence/predictions remain unchanged.

Default pricing_v21.py / shade-vintage-shared-delivery-v21.json (pooled).
Retains frozen utility weights and boundary; replaces v20 narrow gate with2 learned
shared-context shade parameters:90% foreign adjacent-shade reduction when BOTH tares
>=120; complete reduction when younger vintage20. Both130 enforces zero adjacent
shade premium for all regions as user-required structural rule. Uses minimum tare,
not max, so one heavy vessel does not impose its context on a lighter one. Domestic
shade contribution below130 otherwise unchanged. Same-shade/pure5lb comparisons
exactly preserve v20. Pairwise context does NOT imply a transitive standalone price.

Matched5-repeat withheld-family validation on467 rows:
                              v20      selectedv21
Direction accuracy            90.13%   90.19%
Balanced meaningfulness       85.44%   88.96%
False premiums/repeat         14.8     14.4
Missed meaningful/repeat       10.4      7.0
Direct size accuracy          85.16%   89.25%
Original455-row v20 predictions/radii reproduce. New parameters fit only training
families. Zero130 rule is a mandated prior from current instruction, NOT independent
held-out evidence of discovery. Reused families/hypothesis refinement are exploratory.

Initial max-tare experiment rejected (extra mixed-tare false premiums), retained in
shade-vintage-validation-v21.json. Shared minimum-tare follow-up passes all gates;
separate120/125 coefficients did worse. Selected full fit matches Round36/39/40
supplied axes and all3 zero-shade checks, but that is training consistency, not fresh
accuracy. Older revision-13 EE120 pale30>gold25 is now reversed by model; its evidence
is intact. Do not claim universal preservation or total resolution of prior judgments.

Artifacts: evidence-v21.json, benchmark-targets-v21.json, shade_vintage_shared_v21.py,
shade-vintage-shared-validation-v21.json, shade-vintage-shared-delivery-v21.json,
shade-vintage-findings-v21.json, pricing_v21.py, test_shade_vintage_v21.py.

## Round40 complete — frozen comparison verified

V20 direction6/9, meaningfulness7/12; v19 direction3/9,meaningfulness4/12.
Magnitude-only size scoring is separate from direction: Q9 is wrong direction
despite correct meaningful magnitude. V20 false meaningful0, missed meaningful5;
v19 false meaningful3, missed meaningful5. Q1/6/8 explicitly no golden/pale premium
at130lb: BOTH models fail zero-premium checks0/3; v20 practical classification
does not satisfy zero preference. Preserve these statements, do not hide misses.
Both pure5lb controls Q4/Q11 correct. Remaining v20: lower-tare Q3/Q9 direction,
age-step Q5/Q10 size, unequal-tare mixed Q7/Q12. All24 predictions recomputed and
hashes intact. Evidence staysv20; no refit/no active questionnaire. Targeted fresh
pairs, not random accuracy. Receipts: round40-fixed.json, round40-findings.json.

## Active Round40 — frozen v20 versus v19

12 fresh unordered pairs verified against saved rounds/evidence, including reversed
orientation.6 eligible shade targets+6 below-boundary/tare controls. Attribute design
precedes model calls. All questions/predictions saved in round40-fixed.json, frozen
before answers. Familiar families, not random population sample. Present one at a
time, hide predictions/interim scores, record direction and meaningfulness separately.
Unresolved/save for later allowed on either axis. Q1 recorded tie/no shade premium; user golden-to-pale no-premium rule at>=130lb preserved separately. Q2 recorded B/meaningful; younger vintage decides, no adjacent shade premium at130lb. Q3 recorded A/meaningful; younger vintage outweighs adjacent shade at Western Europe120lb. Q4 recorded B/practically similar; pure5lb tare advantage slight, not meaningful. Q5 recorded A/meaningful; five-year younger vintage outweighs adjacent shade at Eastern Europe125lb. Q6 recorded tie/no shade premium at130lb with other attributes matching. Q7 recorded A/meaningful; younger vintage and5lb lower tare jointly outweigh adjacent shade. Q8 recorded tie/no adjacent shade premium at130lb in West Central Asia. Q9 recorded B/meaningful; younger golden20 beats pale25 at Eastern Europe115lb. Q10 recorded B/meaningful; younger golden35 beats pale40 at Western Europe125lb. Q11 recorded A/practically similar; pure5lb tare advantage slight, not meaningful. Q12 awaiting answer. No refits.

## Evidence v20 — contextual shade premium delivered

Round39 incorporated append-only:455 rows,301 supplied directions,216 size targets,
239 unspecified sizes;81 directly supported size labels. All449 prior rows and
unresolved pairs preserved. Q38-8 strongly remains qualifier-derived, not explicit.

Default: pricing_v20.py / contextual-shade-delivery-v20.json. Selected heavy_only:
one scalar0.55 reduces the existing foreign golden-to-pale increment by55% only
when provenance matches, tare is equal and>=125lb, and shades are golden/pale.
Unlike rejected narrow model, equal vintages are included. All19 v19 utility
coefficients and v19 boundary stay fixed. New correction is exactly zero for every
unequal-tare pair: it cannot add a5lb premium. Same-shade and domestic comparisons
also remain unchanged. This is a pair-context comparison score, not a transitive
per-offering price model or dollar-price estimate.

Matched5-repeat withheld-family validation on455 rows:
                              v19      v20 one-scalar
Direction accuracy            89.50%   90.63%
Balanced meaningfulness       85.37%   89.97%
False premiums/repeat         15.2     14.6
Missed meaningful/repeat       8.8      5.0
Direct size accuracy          85.43%   89.88%
Old449-row v19 margins/radii reproduce exactly. Training families only fit new
parameters. Cached baseline fits exclude held-out families. Reused/hypothesis-informed
validation is exploratory; new Round39 is now training evidence, not prospective test.

Two-context alternative adds WesternEurope120lb scalar0.50. It fits all6 isolation
answers versus5/6 for selected simpler model, but has identical held-out metrics;
simpler model wins tie-break. WE120lb Q39-1 remains known limitation. AllRound36
full-fit answers preserved, plus earlier EE120lb and WE115lb tradeoffs. Do not call
full-fit5/6 or6/6 predictive accuracy. No more questionnaire, all baselines unchanged.

Artifacts: evidence-v20.json, benchmark-targets-v20.json, contextual_shade_v20.py,
contextual-shade-validation-v20.json, contextual-shade-delivery-v20.json,
contextual-shade-findings-v20.json, pricing_v20.py, test_contextual_shade_v20.py.

## Round39 isolation complete — no refit

All6 explicit directions and sizes saved. Frozen v19: direction2/6,size1/6.
Frozen rejected narrow-shade candidate: direction6/6,size4/6; size missesQ1(120lb)
andQ5(equal-age shade-only). Diagnostic targeted set, not population accuracy.
Five-year younger golden meaningfully beats older pale at WE120/130lb (anchor125),
and EE/WCA125lb. Shade-only WE25years125lb pale advantage is slight/practical.
Ten-year younger golden also meaningful. Tradeoff-only gate misses the isolated
shade problem; adjacent shade magnitude needs contextual examination. Earlier115lb
and EE120lb answers remain intact; no universal tare independence inferred.
All12 predictions recomputed, hashes intact. Evidence remainsv19, models unchanged,
no active questionnaire. Receipts: round39-fixed.json and round39-findings.json.

## Active Round39 — Question8 one-factor isolation

Six questions frozen in round39-fixed.json. Each varies only provenance, vintage
or tare relative to round38-8. Diagnostic isolation, not fresh accuracy. V19 and
rejected narrow-shade candidate snapshots/predictions frozen; evidence unchanged.
One question at a time, hide predictions and earlier answers, record direction and
meaningfulness separately. Unresolved/save for later allowed. Q1 recorded A/meaningful at Western Europe120lb. Q2 recorded A/meaningful at Eastern Europe125lb. Q3 recorded A/meaningful at Western Europe130lb. Q4 recorded A/meaningful at West Central Asia125lb. Q5 recorded B/practically similar; adjacent shade alone slight at Western Europe25years125lb. Q6 awaiting answer.

## Narrow shade correction tested — v19 retained

Analyzed broad tare-dependent shade side effects against delivered v19. The broad
combined fix increased false premiums in revision-14 (EE pale30/125 vs golden30/115,
1 to2 of5 repeats) and round21-15 (WCA pale20/120 vs pale20/125,0 to4). Offering-level
shade discount inadvertently creates an extra tare effect even at matching shade.

Narrowed to foreign matched-provenance/equal-tare golden/pale tradeoffs with golden
younger, still one bounded scalar. Both collateral cases now exactly match v19.
But same withheld-family validation yields direction90.24% vs v19 90.51%, balanced
size89.24% unchanged, false premiums14.4 unchanged, missed meaningful5.0 unchanged.
Only3 evidence rows have nonzero feature. Full fit coefficient0.5 fixes Q38-8 but
reverses revision-13 at120lb. With Q38-8 family withheld, coefficient0 in all5 repeats.
This is not evidence of generalization. Do not promote or disguise as a price rule.
Pair-dependent experimental score does not establish a transitive global price.

Baseline/default remains pricing_v19.py and contextual-fixes-delivery-v19.json.
Evidence v19 unchanged; no questionnaire. New rejected experiment/receipts:
narrow_shade_v19.py, validate_narrow_shade_v19.py, narrow-shade-validation-v19.json,
narrow-shade-candidate-v19.json, narrow-shade-analysis-v19.json,
test_narrow_shade_v19.py. Do not confuse candidate with promoted delivery.

## Evidence v19 — smallest validated fix delivered

Round38 incorporated append-only:449 rows,295 supplied directions,210 size labels,
239 missing sizes. Q3 remains missing on both scoring axes. Q8 strongly remains
qualifier-derived meaningfulness, not explicit direct-size evidence. Earlier answers
and unresolved Round27 pairs preserved. No active questionnaire.

Use pricing_v19.py with contextual-fixes-delivery-v19.json. Delivered boundary-only
fix leaves all19 v18 ranking coefficients unchanged and raises its full-data mature
context coefficient from0.75 to1.10 (additional0.35). It fixes Round38 Q5 false premium.
The model still misses Q8; this is explicit, not hidden by an answer lookup.

Same5 repeated withheld-family splits extended to449 rows; cached v18 base fits and
predictions on prior437 rows reproduce. Corrections fit only training labels; same
attributes/family cannot appear on both sides of a fold. Frozen baseline uses old
training evidence, candidate residuals use v19 training evidence. Exploratory reuse,
not fresh prospective accuracy. Direction/meaningfulness evaluated separately.

                         v18     boundary    shade-only    combined
Direction accuracy       90.51%  90.51%      90.78%        90.78%
Balanced size accuracy   89.12%  89.24%      89.35%        89.53%
False premiums/repeat    14.8    14.4        15.8          15.2
Missed premiums/repeat    5.0     5.0         4.6           4.6
Direct size accuracy     89.87%  90.40%      88.80%        89.33%

The shade hypothesis reduces foreign pale shade advantage above115lb using one
bounded coefficient. Full fit fixes Q8 at125lb while preserving round36-12 B/practical
at115lb, but worsens held-out false premiums/direct size accuracy. It and combined
remain rejected experiments in contextual-fixes-validation-v19.json, not defaults.
Choosing only training fit would overstate progress. Boundary-only benefit is small.

Sources/receipts: evidence-v19.json, benchmark-targets-v19.json, miss-analysis-v19.json,
contextual-fixes-validation-v19.json, contextual-fixes-delivery-v19.json,
contextual_fixes_v19.py, pricing_v19.py, test_contextual_fixes_v19.py.
All earlier baselines, model code, predictions and evidence unchanged.

## Round38 complete — frozen prospective comparison

Both v18 and improved v17 scored6/7 supplied directions and9/11 meaningfulness
judgments. Only model disagreement is Q3 meaningfulness, which user did not
explicitly supply: v18 practical, v17 meaningful. No demonstrated v18 advantage.
No-clear directions excluded. Q8 strongly counted as meaningful with qualifier
preserved; explicit-size-only score9/10 each. Shared misses: Q5 false premium
(Southwest golden40/115 vs Northwest golden40/120); Q8 direction and size error
(Western Europe golden25/125 vs pale30/125: user A strongly, models tiny B/practical).
All24 predictions recomputed and source hashes intact. No refit or incorporation;
evidence stays v18. No active questionnaire. Receipts: round38-fixed.json and
round38-findings.json.

## Active frozen comparison — Round38

12 fresh unordered pairs compare v18 against improved precision v17. All pairs and
predictions frozen in round38-fixed.json before answers. Attribute design preceded
model calls; historical pairs including reversed pairs excluded. Some families recur.
Present one at a time; hide predictions and interim results. Record direction and
meaningfulness separately, allow unresolved/save for later, infer neither missing
axis nor exact equality. Models/evidence stay fixed throughout. Q1 recorded no clear direction/practically similar; Western Europe cachet caveat preserved. Q2 recorded A/meaningful, younger vintage outweighs negligible domestic golden/pale shade difference. Q3 recorded no clear direction; taste-dependent, meaningfulness unspecified. Q4 recorded A/practically similar; combined provenance and5lb advantage not meaningful here. Q5 recorded A/practically similar; slight Southwest provenance and5lb advantage not meaningful at40. Q6 recorded A/meaningful;10-year younger vintage and10lb lower tare outweigh Northeast provenance. Q7 recorded B/meaningful; Western Europe provenance and lower tare favor B. Q8 recorded A/meaningful from strongly; vintage outweighs adjacent shade at Western Europe125lb. Q9 recorded no clear direction/practically similar; Southeast provenance and Central5lb tare advantages offset here. Q10 recorded no clear direction/practically similar; matched premium domestic zones need another differentiator. Q11 recorded B/meaningful;20lb lower tare and lighter shade outweigh A vintage/provenance advantages. Q12 awaiting answer.

## Evidence v18 — contextual meaningfulness correction delivered

Evidence v18 appends the 12 clarified Round37 pairs to the unchanged 425 v17 rows.
437 rows; 288 supplied directions; 199 size labels (166 practical/coarsened-negative,
33 meaningful including 25 historical proxies); 238 sizes remain unspecified.
Direct size support: 65 judgments, 8 meaningful and 57 nonmeaningful. Six new missing
directions remain missing. Round27-7/11 remain unresolved. No new questionnaire.

Use pricing_v18.py and contextual-boundary-fit-delivery-v18.json. The improved-v17
19 utility coefficients remain byte-for-byte numerically identical. One scalar (0.75)
widens the meaningfulness boundary in matched regional comparisons at age >=35, or
brown age >=30, with <=5 lb tare separation. A smooth provenance-score proximity
factor limits widening. Directions, domestic shade/vintage behavior and small
provenance ordering are unchanged. Practical similarity is not exact price equality.

Five repeated withheld-family validations on the same 437 rows:
- v16: direction 89.03%; balanced size 87.18%; false meaningful 13.4; missed 5.8.
- improved v17: direction 90.56%; balanced size 89.72%; false 15.0; missed 3.8.
- v18 selected context procedure: direction 90.56%; balanced size 90.21%; false 13.4; missed 3.8.
Counts are means per repeat, not independent observations. The context kind is chosen
inside training partitions; scalar fitting also excludes held-out families. The final
full-data kind is mature_shade. These are exploratory reused-family results, not a
new prospective test. Existing baseline fits/caches and all frozen rounds preserved.

Full-data model now separates Round37 Q6 (brown Central/EE practical) from Q9
(amber Central/EE meaningful), also fixes Q4/Q10, and matches 11/12 Round37 sizes.
Q3 (Western Europe vs Central, pale30, 5 lb) remains a false premium. Round36 stays
12/12 on size. These are training-fit checks after incorporation, NOT fresh accuracy.
Shade and common tare both changed in Q6/Q9; causal attribution is not established.

Artifacts: evidence-v18.json, benchmark-targets-v18.json,
contextual-boundary-fit-validation-v18.json, contextual-boundary-fit-delivery-v18.json,
pricing_v18.py, test_contextual_meaningfulness_v18.py. The initial OOF-calibrated
experiment contextual-meaningfulness-validation-v18.json is preserved: its light-tare
candidate reduced validation errors but failed the full-data Q6 correction. The later
training-fitted scalar experiment is separately recorded, not an overwritten result.
A matched-context widening control scores higher balanced size (90.63%) but cannot
represent the Q6/Q9 distinction; it is retained as a diagnostic, not the context fix.
All metrics and inference come from attributes/coefficients, never answer lookup.

## Round37 finalized after user-authorized size clarifications

round37-fixed.json final scores retain initial incomplete-axis receipt separately.
All12 sizes explicit:5 meaningful,7 practical.6 A/B directions supplied; other6
no clear direction excluded, not exact-equality labels. Q2/Q9 clarified B meaningful.
V16 direction6/6,size8/12,3 false premiums(Q6/Q7/Q10),1 missed meaningful(Q2).
Improved v17 direction6/6,size8/12,4 false premiums(Q3/Q4/Q6/Q10),0 missed meaningful.
Both wider controls correct on both axes; targeted10 cases both6/10 size. This small
purposeful batch does not establish reduced false-premium frequency or population
accuracy. All24 predictions independently recomputed; frozen model/source hashes
unchanged. No model fit or evidence-version incorporation performed in this round.

round37-findings.json records a concrete feature limitation: Q6 Central vs Eastern
Europe at brown30/110 is practical; Q9 same regional contrast at amber30/125 is
meaningful. After aligning orientation both models produce IDENTICAL feature
differences, so no global threshold/weight adjustment can separate these sizes.
Shade and shared tare level both vary: do not claim this proves shade alone causes
it. Other misses cluster in older brown domestic and domestic/foreign+5lb contexts.
Next correction should address conditional materiality of regional differences;
no new questionnaire active, no need to re-ask the clarified questions.


## Round37 clarification in progress

User authorized re-posing Q2/Q9 for incomplete or mistaken feedback. Revisit one
at a time, both direction and size allowed to change. Clarification1 (Q2) answered B/meaningful; clarification2 (Q9) awaits
answer. Models and original prediction plan remain frozen. Initial scoring receipt
preserved separately; do not reveal predictions or refit during clarification.


## Active frozen comparison — Round37 remaining false premiums

round37-fixed.json:12 fresh questions versus18-coefficient v16 and improved precision
v17 (19 coefficients, weight4 full fit). Full snapshots and all predictions frozen.
10 remaining-error-family neighbors plus2 wider controls; selected before model calls.
All unordered pairs checked against earlier rounds/evidence. These are targeted nearby
contexts, not independent random samples. Q1 answered A/meaningful difference
(tare outweighs provenance here); Q2 answered B, size unspecified
(vintage outweighs5 lb tare here); Q3 answered A/practically similar;
Q4 answered practically similar/no clear direction; older-vintage conditional
guidance preserved. Q5 answered no clear direction/practically similar.
Q6 answered no clear direction/practically similar; Q7 answered no clear direction/
practically similar; Q8 answered no clear direction/practically similar; Q9 answered B, size unspecified
(Central provenance advantage); Q10 answered no clear direction/practically similar;
Q11 answered A/meaningful difference; Q12 awaiting answer.
One at a time; hide
prior answers/predictions. Record direction and meaningfulness separately; A/B alone
is direction only. Practical similarity can retain a lean; deliberate identical prices
and unresolved stay distinct. Missing axes excluded from scoring with coverage shown.
No model/threshold updates or evidence incorporation during this round. No replay of
old pair endpoints; matched-attribute shifts intentionally test transfer of false calls.


## Precision-improved v17 candidate delivered

Use pricing_v17_precision.py -> precision-shade-candidate-v17.json. Same19 features
and user-behavior constraints; no evidence changes or questionnaire. Existing v16,
v17, frozen scores and previous delivery snapshots unchanged. Six tests passed.

Audit: original v17 made72 false-premium events across5 repeats versus51 v16.
41 new errors and20 removed (net21 extra);58/72 mixed/other attributes,25/72
cross domestic/foreign. None inside zero-loss0.25 band: not a dead-zone bug.
false-premium-audit-v17.json lists every affected row, source wording and repeat count.

Repair: only unprotected legacy no-meaningful loss gets weight1/2/4. Direct constraints,
directional/proxy losses, ridge grid and19 features unchanged. Precision selector uses
v16 INNER out-of-fold predictions on shared old training rows as a false-call budget
and direction reference. Requires no new errors on direct cases original v17 inner
predictions got right. All selection training-only; outer scores not used for tuning.
If no setting qualifies, retain original v17 config and explicitly record fallback.
Weighted procedure budget feasible14/25 folds;11 fall back. Weight choices20 folds1,
4 folds2,1 fold4. Full-data choice weight4,alpha0.01,radius0.3000001.

Mean paired validation v16 / original v17 / improved v17:
- Direction88.79% /90.35% /90.35%; reversals31.6 /27.2 /27.2.
- Balanced materiality88.58% /90.47% /91.31%.
- False meaningful10.2 /14.4 /10.6; missed meaningful4.6 /2.8 /3.0.
- Raw materiality accuracy92.09% /90.80% /92.73%.
- Direct53 materiality95.09% /97.74% /97.74%; direct meaningful recall73.33% /100% /100%.
- Corrected Round36 provenance and shade-vintage held-out panels identical to original
  v17. All12 new cases still fit both axes correctly; this is training consistency,
  not new prospective accuracy. Inference reads coefficients only, no answer lookup.
Selection-only replay reduced false calls to12.6; weighted extension to10.6.

Improvement removes3.8/14.4 false calls (26.4%) and most net excess over v16, but
remains0.4 above v16. Strict v16 no-regression delivery gate therefore still fails;
precision-shade-delivery-v17.json records that conservative outcome. Improved model
is separately exported as requested behavior-preserving candidate, not misrepresented
as an unqualified replacement. Scores are exploratory repeated-data estimates, no
currency calibration; sparse direct positive sizes and coarsened legacy labels remain.

Artifacts: precision_shade_model.py; validate_precision_shade_v17.py;
precision-shade-protocol-v17.json; precision-shade-validation-v17.json;
precision-shade-candidate-v17.json; precision-shade-cache-v17/;
test_precision_shade_v17.py. Tests verify source/baseline hashes, train-only budgets,
selector replay, QP/reference/gradients, preserved constraints and full-grid ordering,
reported metrics, residual-gap disclosure and model-only runtime. All jobs exited.


## Evidence v17 and focused domestic-shade correction delivered

Evidence-v17.json:413 unchanged parent rows +12 unique Round36 answers =425 pairs.
190 A/92 B/109 retained equalities/34 practical-only labels;10 new slight directions
also explicitly practical,2 new directions meaningful. Targets in benchmark-targets-v17:
159 no-meaningful,28 meaningful direct/proxy,238 unspecified. Direct subset53 comprises
3 meaningful and50 no-meaningful;25 other positives remain qualifier proxies.
Original Q7/Q11 unresolved. Round36 frozen scores remain6/12 versus5/12 direction,
10/12 size each; their new fitted consistency must not be presented as fresh accuracy.

Corrected candidate: pricing_v17.py -> domestic-shade-candidate-v17.json.
19 coefficients: same18 additive features plus domestic x pale/straw. No NW-amber,
domestic-age or WCA-light-shade extras in this candidate; earlier models unchanged.
This separates foreign pale-step from domestic pale-step, which the shared model
could not do. Full candidate domestic golden/pale score difference0.3 within its
0.3000001 band, versus foreign0.7758054; global25-to30 vintage increment0.7757054.
Foreign pale30 narrowly beats golden25; domestic golden25 beats pale30 meaningfully.
Small WE>NW and WCA>South/Eastern Asia orderings remain positive and within band.
Numerical strict margin1e-4 is a fitting convention, NOT a measured premium amount.

High-confidence paired answers generate constraints only from TRAINING rows:
practical abs(gap)<=fit radius; known direction signed gap>=1e-4; explicit meaningful
signed gap>=radius+1e-4. Unknown directions never invented.25 adjective proxies,
109 coarsened legacy ties and238 unspecified sizes are not hard protected. Existing
user5lb and domestic golden/pale rules constrain feature contributions within radius,
not to zero. All monotonicity constraints retained. No lookup or per-pair override.

Compared matched v16 (trained on old413 only), data-updated18, soft19 and protected19
using preserved family splits extended to425,5x5 outer and3 inner grouped tuning.
Protected19 vs v16: direction90.35% vs88.79%; balanced materiality90.47% vs88.58%;
wrong-way27.2 vs31.6 per282 directional comparisons. Direct materiality97.74% vs95.09%
on53 cases. But all-target false meaningful14.4 vs10.2; raw size accuracy90.80% vs92.09%.
This regression is mostly older coarsened targets, which remain unchanged and counted.
Conservative delivery safeguard rejects unqualified replacement; v16 retained as
baseline. Corrected candidate exported for the requested behavior, not called a clean
across-the-board winner. Data-only18:89.36% direction/91.60% balanced size but misses
more direct meaningful cases; soft19:87.02%/92.91% with more reversals. Full protected
fit matches all12 new directions and sizes; that is training consistency only.

Artifacts: build_evidence_v17.py; domestic_shade_model.py;
validate_domestic_shade_v17.py; domestic-shade-protocol-v17.json;
domestic-shade-validation-v17.json; domestic-shade-candidate-v17.json;
domestic-shade-cache-v17/. Six tests passed: append-only data, hashes, frozen baseline
reproduction, train-only protected rows, QP/reference parity, grid/rule constraints,
metrics and model-only API. Exact global prices and monetary premiums not inferred.
No new questionnaire started; no prior labels, model snapshots or frozen scores changed.


## Round36 complete — fresh comparison does not support replacing additive baseline

round36-fixed.json records all12 independent direction/size answers and frozen scores.
Additive v16: direction6/12, meaningfulness10/12, both6/12. Context21: direction5/12,
meaningfulness10/12, both5/12. All12 predictions independently reconstructed after
completion; source/plan hashes intact. No model refit or prior evidence alteration.
10 practical similarities,2 meaningful differences. Both models detect2/2 meaningful
but falsely call2/10 practical cases meaningful (precision2/4); do not overstate
10/12 accuracy on this small targeted set. Tiny directions scored separately.

New findings in round36-findings.json:
- At115 lb, WE slight advantage over Northwest across amber25/30/35 and copper30;
  all practical. Additive4/4 directions, context3/4. No reversal in tested settings.
- At25 years/110 lb, WCA slight advantage over South/Eastern Asia across4 shades;
  all practical. Both models0/4 directions, but4/4 materiality.
- At115 lb, pale30 vs golden25: foreign EE/WE favor pale slightly/practically;
  domestic Central/Southwest favor younger golden meaningfully. User explicitly
  says domestic golden-to-pale shade difference negligible. Both models get the
  domestic cases right, reverse and overstate the foreign cases.
Q10 final within-answer clarification is meaningful A, superseding its opening
practically-similar wording; full raw response preserved. No numeric premium or
hard zero shade coefficient inferred. Old comparisons at other ages/tares remain
unchanged; this does not establish universal regional order or erase old evidence.

Working reference returns to simpler v16 (pricing_simple.py) after the targeted
prospective result; context snapshot/entrypoint remain intact for comparison.
Do not ask these questions again. Next correction should use these clean explicit
patterns, not another broad architecture sweep. No questionnaire active.


## Active frozen comparison — Round36 context effects

round36-fixed.json freezes12 fresh paired questions and predictions for selected
21-coefficient context+5lb-rule model versus18-coefficient v16 additive baseline.
Three four-question blocks: Northwest/Western Europe shade and age; West Central
Asia/South-Eastern Asia shade; domestic versus foreign shade-age tradeoffs. All
unordered endpoint pairs checked against all earlier rounds/evidence. Shared tare
within each block; preselected without model outcomes. Targeted neighboring contexts,
not an independent population sample. Full model snapshots and file/plan hashes saved.
Q1 answered B/practically similar; Q2 answered A/practically similar; Q3 answered B/practically similar; Q4 answered A/practically similar; Q5 answered A/practically similar; Q6 answered B/practically similar; Q7 answered A/practically similar; Q8 answered B/practically similar; Q9 answered A/practically similar; Q10 answered A/meaningful difference per final
within-answer clarification (domestic golden-to-pale negligible, vintage decides).
Q11 answered B/meaningful difference; Q12 awaiting answer. Ask one at a time.
Hide predictions and earlier answers.
Direction and meaningfulness must remain independent. A/B alone records direction
only; missing meaningfulness remains missing. Practical similarity can retain a lean;
deliberate equal prices separate. Unresolved dimensions excluded from their metric,
with coverage reported. No fits, threshold changes or evidence incorporation until
all12 answered. Never use recorded-answer retrieval for model predictions.


## Delivered minimal-context correction on evidence v16

Use pricing_context.py with minimal-context-rule-delivery-v16.json (21 coefficients).
Existing v16 simple, earlier models, evidence and frozen scores unchanged. No new
questionnaire. Direction/materiality outputs are coefficient-only estimates, never
recorded-answer retrieval. Nine tests passed across structural and rule variants.

Four feature collisions analyzed: (1) Northwest/Western Europe rank depends on
shade and vintage; (2) Southeast/Northwest tare tradeoff changes with shade;
(3) West Central Asia/South-Eastern Asia rank changes amber versus golden;
(4) pale30 versus golden25 tradeoff differs Eastern Europe versus Central.
3 added terms: Northwest x amber; domestic x(30-vintage)/10; West Central Asia x
 golden-or-pale. All four conflict sets feasible with this pool; all smaller subsets
fail. This is minimal within the declared interpretable pool, not over arbitrary
composite features.15 records involved, only4 verbatim;11 structured history only.
No label changed. Full-grid monotonicity preserved with free interaction coefficients.

Unmodified v16 loss/regularization grid/joint selector; same25 outer family folds,
inner training-only tuning. Verified v16 cached predictions preserved exactly.
First candidate improved balanced materiality91.39% vs89.87%, but threshold in one
fold(11/3) was0.32592085, slightly below its5lb coefficient0.32658651. All11 direct
false materiality cases in that repeat were otherwise-matched5lb differences.
Enforce existing user rule: radius=max(calibrated radius,abs(beta_tare5lb)+1e-8).
No new fitted parameter; no coefficient/label change; rule depends only on training
fit and prior user instruction. Applied to both baseline/candidate. Baseline unchanged;
one candidate fold changes. Identified after error inspection: exploratory, not a
fresh holdout. Original uncorrected experiment/result also retained unchanged.

Mean v16 / delivered21-coefficient+rule, same held-out comparisons:
- Direction270:90.67% /90.74%; reversals25.2 /25.0 (essentially flat).
- Meaningfulness175 balanced89.87% /92.13%; ordinary accuracy93.03% /94.17%.
- Meaningful recall85.38% /89.23%; no-meaningful recall94.36% /95.03%.
- False meaningful8.4 /7.4; missed meaningful3.8 /2.8.
- Direct41 materiality subset both100%, but only1 positive;25 other positives
  remain qualifier proxies,109 negatives coarsened ties.238 sizes unconfirmed/excluded.
All delivery safeguards pass against both native and rule-applied v16.

On the15 conflict cases, mean held-out direction correct7.2 /8.0; representational
capacity is not a claim that every reversal was learned. Full learned NW-amber term
is effectively0; domestic-age0.07706; WCA-light-shade-0.03430. Full calibration radius
0.32462662 already exceeds5lb contribution0.30611809, so rule does not alter final
fitted scores. Known round35-3/4/6 tiny direction discrepancies remain exposed.
No forced same-price outputs or monetary calibration asserted.

Artifacts: minimal-context-conflict-audit-v16.json; minimal_context_model.py;
validate_minimal_context_v16.py; minimal-context-validation-v16.json;
validate_minimal_context_rule_v16.py; minimal-context-rule-validation-v16.json;
minimal-context-rule-delivery-v16.json; minimal-context-cache-v16/.
Tests: test_minimal_context_v16.py and test_minimal_context_rule_v16.py verify
source hashes, subset feasibility, nested isolation, gradient, monotonicity, cached
metrics, no-lookup runtime and5lb invariant over the full grid. No process left running.


## Delivered model-only simple v16 benchmark

Use pricing_simple.py and simple-benchmark-v16-delivery.json. Selected v16_blended
under preregistered direction/materiality co-primary rules. Same18 monotone additive
coefficients; no lookups, overlays or new contextual features. Prior models/evidence
unchanged. refit_simple_benchmark_v16.py reproduces the comparison; six tests passed.

Validation: same preserved family assignments for first401 rows, extended to413
without labels,5 folds x5 seeds; inner3 folds select settings. Matched v15 recipe
control refitted inside training, not tested using its full-data coefficients.
Compared v16 same-loss recalibration and same-feature direction-only logistic fit.
Direction and meaningfulness scored separately; wrong winner does not itself count
as wrong detection of whether a difference is meaningful. Combined diagnostic
reported separately. Unknown238 meaningfulness targets excluded from size metrics.

v15 control / selected v16:
- Direction accuracy on270 known directions89.11% /90.67%; sign reversals29.4 /25.2.
- Meaningfulness balanced accuracy89.56% /89.87% on175 targets.
- Meaningful recall81.54% /85.38%; no-meaningful recall97.58% /94.36%.
- False meaningful declarations3.6 /8.4; missed meaningful4.8 /3.8.
- Ordinary size accuracy95.20% /93.03%; disclose this tradeoff alongside balance.
Meaningfulness data include25 positive qualifier proxies, only1 clear direct positive,
40 direct no-meaningful cases and109 coarsened older ties. Direct41 subset matches
in every repeat, but one positive cannot validate general meaningful-premium detection.
Repeated adaptive data, not independent prospective confirmation. No dollar prices.
Direction-only fit89.33% direction /86.97% balanced materiality failed joint criteria.

Full selected alpha0.1,radius0.320940715979069. pricing_simple.Model.compare(a,b)
returns model-only estimated direction and meaningfulness, explicitly no exact-price
assertion. Tests forbid runtime evidence reads and reconstruct every outer margin
from validation feature vectors and training coefficients. No recorded-answer accuracy.
Current full fit still leans B on round35-3/4/6 (inside practical band); recorded A
judgments remain intact. round35-9 predicts A inside band. These errors are exposed,
not patched by lookup. Do not claim all three familiar cases fixed by this refit.

simple-direction-feasibility-v16.json identifies four opposite-direction groups
with identical additive feature differences. Example: Northwest versus Western
Europe ranking changes with shade/vintage, which cancels from this18-feature
same-attribute regional contrast. Another: West Central Asia versus South/Eastern
Asia amber30/120 versus golden30/120 has opposite stored directions. These are
representation conflicts on different offerings, not user-answer contradictions.
A linear feasibility check cannot satisfy all270 directions with this feature set.
This is concrete context-assumption evidence to inspect before any future questions.
No new questionnaire created; any later set must distinguish a specified hypothesis
and have a predeclared effect on model/data decisions.


## Three mixed misses resolved at the evidence and output layer

mixed-miss-analysis-v16.json traces round35-4/6/9. Frozen v13 gaps:-0.421/-0.381/
+0.076; current v15 gaps:+0.170/+0.171/+0.344. Current weights already favor A for
all three; two earlier sign errors were fixed by prior refits. Remaining apparent
miss is unconfirmed magnitude: raw answers are a, **A.**, A. Meaningful-A was inferred
from prompt wording, not independently stated. Do not declare these practically
similar or definitely meaningful from that shorthand. User direction remains A.

Applied uniform whole-Round35 provenance rule, not a targeted outcome rewrite:
evidence-v16.json retains all413 raw answers/winners/directions and all unresolved
cases, qualifying9 size assertions as prompt-inferred/unconfirmed. Old interpretation
preserved. Strong long-shot and explicit similarity/close clarification retained.
benchmark-targets-v16.json masks those9 sizes (238 unspecified,149 no-meaningful,
26 direct/proxy meaningful), keeping known directions. No model weights changed.

pricing_resolved.py delivers recorded judgments separately from provisional model
estimates. Known target pairs return A with size unconfirmed. Known round35-3 keeps
recorded A/practical similarity while exposing disagreeing model B estimate. Original
Q7/Q11 stay unresolved. For validation use estimate(), never retrieved answers;
this is an interpretation/output correction, not learned accuracy improvement.
resolved-mixed-comparisons.json demonstrates the three responses.5 tests passed.

Do not lower threshold just to force the three labels: .15 would mark67/149 existing
no-meaningful targets significant instead of1 at.5, including all32 otherwise matched
5lb pairs. Current5lb score contribution0.321 exceeds Q4/Q6 net gaps; no single threshold
can call both meaningful while keeping5lb alone not meaningful with these weights.
Their true sizes remain unknown; changing weights to assert them is unjustified.
No new questions, no baseline changes, no rewritten frozen test score. The original
8/12 receipt used prompt-inferred sizes and is not clean verified materiality accuracy.


## Simple benchmark refreshed on v15

meaningful-benchmark-v15.json refits the unchanged18-coefficient model using the
corrected materiality view. round35-3 now classifies no meaningful difference;
its raw model margin is-0.05049 within radius0.5. The model's tiny B lean does NOT
match the elicited A lean. Preserve A as recorded evidence; do not promote an
unvalidated subthreshold sign into a claimed preference. Prior model snapshots,
evidence and frozen test receipt unchanged. No dollar anchor or new prospective
accuracy available. Current stage: qualitative direction/materiality separation,
not renewed architecture search or repetitive questions.


## Qualitative anchor clarified — evidence v15, direction retained

User answered anchor-1 "very very close." Record practical similarity for original
round35-3, retaining the earlier A direction. No value, percentage, or deliberate
exact price equality inferred. Evidence-v15.json preserves all413 rows and all
other answers; only explicit_materiality for round35-3 is corrected. A remains the
directional label. benchmark-targets-v15.json reflects149 no-meaningful,35 meaningful
direct/proxy and229 unspecified cases. All earlier models/evidence unchanged.
price-anchors.json preserves qualitative response with numeric value null. Do not
force a number or re-ask the same preference. Treat bare A/B as insufficient size
measurement by itself; this correction is scoped, not a blanket recoding of others.
Original8/12 frozen receipt stays historical; do not claim retrospective9/12 as
new prospective performance. No new model fit or dollar calibration performed.


## Reset checkpoint — Round35 scored; direct labels saved; first anchor pending

Frozen18-coefficient v13 benchmark scored8/12 on fresh Round35. All3 wide controls
and the sole practical-similarity answer correct. Four misses Q3/Q4/Q6/Q9 were
predicted practically similar but user chose meaningful A. Q3/Q4/Q6 had underlying
B lean; Q9 had A lean. Threshold adjustment alone cannot fix the three wrong signs.
No meaningful-B reversals were emitted, but three secondary directions were wrong.
Only one no-meaningful case; do not claim robust similarity discrimination or
population accuracy. Original frozen receipt preserved in round35-fixed.json.

Evidence-v14.json preserves401 parent rows and adds12 unique direct materiality
answers:8 meaningful A,3 meaningful B,1 practical similarity.413 total; original
Q7/Q11 unresolved. benchmark-targets-v14.json retains229 unspecified meaningfulness
cases;25 older positive proxies plus11 direct positives and148 no-meaningful labels.
Same18-parameter architecture refitted only, saved as meaningful-benchmark-v14.json.
It matches7/12 recent rows in training after calibration (not an improvement or new
validation result); not promoted. No new architecture sweep or historical edits.

Next: quantify a settled preference using reference-value anchors. price-anchors.json
anchor-1 awaits user value for Northwest golden20/130, with Northwest golden30/110
fixed at100 reference units. This asks magnitude, not the already answered winner;
no dollar/percentage calibration or numeric premium invented. Preserve all baseline
models and frozen scores. Current progress: pricing-reset-progress.json.


## Reset implemented — v13 tare semantics; fresh benchmark round35 active

User clarified matched5lb tare differences as practical similarity: a tiny lower-
tare premium may exist but is not meaningful on its own. Evidence-v13.json changes
27 prior hard tare equalities to practical similarity; preserves5 existing tiny
strict directions with separate no-meaningful-difference qualification. Counts:
176 A/83 B/109 retained equality labels/33 practical similarities,401 unique pairs.
All old evidence/models/deliveries remain unchanged; Q7/Q11 remain unresolved.

benchmark-targets-v13.json is a derived partial target view, not rewritten truth:
147 no-meaningful-preference labels (coarsening exact/practical judgments, plus
matched5lb rule),25 moderate/strong qualifier-derived positive PROXIES,229 cases
with direction but unspecified meaningfulness. Do not convert every A/B into a
meaningful premium or slight adjective into numerical prices. Original equality
semantics and wording audit remain available separately.

meaningful-benchmark-v13.json: one18-coefficient monotone additive benchmark, no
regional overlays, fusion, context-specific tare curves or hard zero-price steps.
Direction-only and meaningfulness targets distinguished; training bands/margins
are declared model conventions, not dollar/percentage anchors.3 grouped folds used
only for calibration; no claimed new generalization accuracy.4 tests passed.
Reproducer build_meaningful_benchmark.py; tests test_meaningful_benchmark.py.

round35-fixed.json freezes12 fresh pairs, their order and benchmark predictions;
question1 answered meaningful A ("by a long shot", typo interpretation retained);
question2 answered meaningful A (tare/vintage); question3 answered meaningful A;
question4 answered meaningful A; question5 answered meaningful B; question6 answered meaningful A; question7 answered meaningful A; question8 answered practical similarity with no lean;
question9 answered meaningful A; question10 answered meaningful A; question11 answered meaningful B; question12 awaits answer.
One at a time. Primary choices:1 meaningful A premium,
2 meaningful B premium,3 practical similarity (optional tiny direction),4 deliberate
identical prices,5 unresolved. Hide predictions and do not update model during batch.
No pure5lb repeats or previously asked pair/reversal in the new batch. Current
workflow state pricing-reset-progress.json supersedes earlier pending plan snapshot.
After this fresh test, consider a few monetary anchors; stop architecture churn.


## Pricing reset — wording audit complete; no further architecture search

User agreed to reset the target/evidence before more model tuning. Current audit:
equality-wording-audit-v12.json, reproducible with audit_equality_semantics.py.
All136 retained equality labels reviewed by recorded answer/source:80 explicit
same-price wordings,14 numbered selections mapped to exact-price option,22 bare
ties (4 under explicit-price prompts),18 without verbatim answer,2 differentiator-
language cases.100 have recorded prompts offering exact equality but no practical-
similarity choice. These are wording/provenance categories, NOT relabeled truth.
Existing six practical-similarity cases and unresolved Q7/Q11 not reopened.

All27 hard local tare equalities concern5 lb steps, same provenance/shade/vintage.
One group-level clarification is the highest-impact next question; stored in
pricing-reset-plan.json. Do not replay27 pairs or silently generalize provenance
semantics to tare. Ask whether a5 lb tare difference judged not meaningful calls
for deliberate identical prices, practical similarity with possible tiny premium,
or context-specific interpretation. Keep all originals/models unchanged meanwhile.

Reset target: meaningful preference primary; known tiny direction secondary;
exact equality deliberate; unresolved distinct. Most existing directional answers
do not independently label economic meaningfulness, so do not relabel every A/B
as meaningful or every small adjective as not meaningful. After scoped semantic
clarification, build ONE simple benchmark, freeze fresh practical evaluation, then
obtain a few price anchors. Audit first; no further convergence variants.


## Delivered simpler exact-zero comparison against v12

Run complete: exact-zero-comparison-v12.json. Use pricing_current.py with
current-pricing-model.json; retained model is v12 because the exact-zero candidate
loses genuine premiums and increases reversals. Earlier baselines and deliveries
are unchanged. Evidence v12 and unresolved Q7/Q11 unchanged.

Candidate:16 raw regional coefficients (common intercept plus centered region,
age-slope and shade-slope vectors;13 free regional degrees). Underlying offering
and component scales frozen within each training partition. Uniform L1 fusion
across1250 domestic pair/shade/age/tare gaps, no adaptive weights/context gates/
pilot anchoring. Only fusion strength selected from0.1/1/10/100 inside grouped
training folds. Same25 outer partitions; baseline margins reproduced. Equality
means identical canonical scalar scores at1e-7 numerical resolution; globally
transitive, no economic decision band. Practical similarity separately diagnosed.

Common literal equality/sign scoring, v12 / exact-zero candidate:
- Determinate395 accuracy59.09% /62.18% (NOT comparable to native band76.61%).
- Literal equality recall0% /15.15%; regional literal ties0/55 /20.4/55.
- All strict direction90.12% /86.87%; regional strict13/14 /5.4/14.
- Small premiums104.2/118 /97.4/118; reversals13.4 /14.6.
- Overall strict reversals25.2 /27.0; practical coverage56.67% /83.33% (6 pairs).
Thus headline exact-semantic accuracy improves by adding equalities, but the
premium-retention/reversal safeguards fail. Keep v12 as the balanced delivery.
Full-data strength100, all27 known tare equalities retained. Full training data
has28 exact equalities total, including only1/55 matched regional exact ties.

Files: exact_zero_model.py; run_exact_zero_v12.py; exact-zero-protocol-v12.json;
exact-zero-cache-v12/; test_exact_zero_v12.py. Six tests passed: hashes/baseline
reproduction, nested training scope/frozen scales, all-tare fusion and gradients,
QP/reference parity, grid constraints/canonical transitivity, metrics/delivery API.
Initial1e-7 monotonic slack hit5.7e-8 inherited numerical feasibility residual;
rerun used2e-7 slack (inside existing2e-6 verification tolerance), unchanged model
structure/centering. All25 outer constrained designs independently LP-feasible.
Source hashes verified; batch and tests exited. No repeated elicitation needed.


## Delivered selection and threshold ablations against v12

Use pricing_best.py with best-pricing-model.json. Both requested experiments are
complete on unchanged evidence-v12.json and the same25 outer family folds.
The retained deployable fit is v12: no alternative passed all prespecified safeguards.
Threshold-only has the highest determinate band accuracy76.96% versus76.61%, with
11.0 reversals unchanged, but small-premium recognition85.2/118 versus85.6/118.
Its full-data calibrated radius is0.2, identical to v12; full coefficients are also
identical. Thus even that procedure produces the same deployable comparator here.

Selection-only was replayed on identical per-strength caches for both v12 weighted
and original convergence architectures. Weighted selection-only:76.61%,12.8 reversals;
strict regional recognition24.29%->70.00%, but regional band ties91.64%->86.55%.
Convergence original selector:76.86%,13.0 reversals; changed selector:75.29%,14.4.
No adaptive fusion, pilot anchoring, or sample weighting was added to convergence.
Only the existing v12 practical-similarity loss adaptation is shared by both arms.

Threshold-only keeps EVERY v12 fit/margin and training-loss radius unchanged;
only the operational decision radius is selected using grouped inner predictions.
Inner reversal count may not exceed inherited setting; maximize minimum regional
equality-label band recall/strict band accuracy. Best outer scores never set an
inner threshold. Full-data radius unchanged. Literal zero equality and similarity
are separately reported; band recognition is not proof of exact price equality.

Artifacts: pricing-ablations-v12.json; pricing_ablation_protocol.json (prespecified);
ablation-cache-v12/ (all inner/outer margins for every strength, selector replay,
training partitions and hashes); run_pricing_ablations_v12.py; convergence_v12_ablation.py.
Current small-premium subset118 rows, not frozen-v10's119. No evidence edits,
re-elicitation or peer-session messaging. Existing baseline hashes unchanged.
Six tests pass: hashes/training isolation/selector replay, baseline and threshold
fit identity, metrics/delivery guard, semantic QP-reference parity, full-grid
constraints and callable inference. Model remains experimental, no dollar prices.

Run comparisons via existing .venv-regional/bin/python pricing_best.py --a '[...]'
--b '[...]', or Model().compare(a,b). All401 pairs/reversals supported by tests.
Batch exited. Do not ask for approval to carry out already authorized routine work.


## Current delivery — evidence and weighted model v12

Evidence-v12.json incorporates Round34 into the same401 unique pairs:176 A/83 B,
136 retained equality labels,6 practical similarities. Only round8-1 and round27-20
changed from v11; both now practical similarity with no assigned winner. Earlier
records preserved per row. Original Q7/Q11 remain unresolved and excluded.

weighted-hierarchy-comparison-v12.json contains the refitted model and matched
v11-control validation; refit_weighted_v12.py reproduces it. Same semantic loss,
architecture, priors, family splits and inherited per-fold settings. V11 control
margins/radii reproduced within1e-10; all existing baselines unchanged. No peer
session contacted. Neither ambiguous pair should be re-asked.

Both clarified pairs now fit within the practical-similarity band in full-data fit:
round8-1 margin0.084265; round27-20 margin0.174708; radius0.2 is a model convention,
not a price tolerance. Their small modeled A direction is not a user-assigned label.
Matched held-out legacy band diagnostic on395 determinate pairs: v11 76.46%, v12
76.61%; small change, no material improvement claim. Strict sign recall90.04% /
90.12%; similarity coverage56.67% /56.67% on6 pairs; literal equality recall0% /0%.
Score-band ties remain distinct from numerical equality. All27 known pure-tare
equalities remain enforced in training. Observed strict/equality graph has no cycles.

pricing_v12.py is a usable loader/comparison API and CLI for the saved v12 model;
pricing.py revision E remains unchanged. It returns direction, practical band and
exact-score-equality flags separately, normalized scores only, no monetary calibration
or abstention claim. Example: Model().compare(a,b), with offering arrays as usual.
Four v12 tests passed, including scoped reconciliation, hashes, baseline reproduction,
metrics and full-grid constraints. Loader checked on all401 pairs and reversals.
Workflow: carry authorized routine follow-through to completion; do not require
repeated approvals or re-ask settled comparisons. Keep progress communication brief.


## Round 34 complete — both pairs practically similar

round34-reconciliation.json records round8-1 and round27-20 as practical similarity,
with no assigned direction or numeric premium. For NE versus Western Europe at
 golden25/120, user reiterates both are top-tier in their respective domestic/foreign
contexts and needs shade/tare differentiation. Apply previously explicit practical-
similarity semantics; do not ask repetitive confirmation or re-present this pair
unless user requests reconsideration or introduces materially different context.
Raw wording and label basis retained. Model/evidence/source hashes and question
plan verified unchanged. Responses stored separately; evidence v11 and models not
updated. Any future reconciliation must preserve practical similarity distinctly
from exact equality and unresolved. Original Q7/Q11 remain unresolved.


## Current evidence — v11 semantic clarification and weighted refit completed

Canonical evidence-v11.json: same401 unique pairs, with177 A/83 B/137 retained
exact-equality labels/4 practical_similarity judgments. Two originals round27-7
and round27-11 remain unresolved in unresolved_pairs, never fitted/scored.
Candidate/results weighted-hierarchy-comparison-v11.json; reproducer
refit_weighted_v11.py; semantics/loss semantic_weighted_model.py; tests
 test_weighted_v11.py (nine passed). All prior evidence, models, frozen results,
peer-review packet and documents remain unchanged. No promotion; other peer-review
session not contacted or modified during this task.

Only the five Round33 revisited pairs changed in v11: round7-14 retains A (latest
slight wording); round7-13, round7-16, round7-17, round31-2 become practical similarity
with no assigned direction. Prior raw records and clarification preserved per row.
All rows explicitly carry judgment_type and direction; winner retains A/B/tie for
legacy determinate labels and uses practical_similarity for the new type. Legacy
loaders must not silently coerce it to tie. Other137 equality labels are retained,
not freshly reverified. Historical explanatory entries remain chronology; current
semantic_reconciliation and judgment_type govern the five clarified rows.

Observed strict/equality graph audit:496 offering nodes; v10 strict cycle edges
round7-14/round7-16; v11 none. Similarity adds no equality graph edges. This removes
the identified recorded exact-price conflict without inventing a strict ordering
for similar pairs. Not proof of identifiability or fit by a restricted architecture.

Unchanged model architecture and priors: provenance-scoped offering plus33-parameter
weighted domestic hierarchy. Both stages retain strict squared-hinge and exact
squared-zero losses. Practical similarity uses max(0,abs(margin)-radius)^2: no
pressure toward zero inside band, either sign allowed, no hard equality constraint.
Radius is inherited fold threshold0.15–0.5; full fit0.2, a MODEL convention, not a
user-supplied numeric price tolerance. Four similar pairs cannot calibrate a general
band. Round33-1 remains strict with a practical qualification in metadata; no extra
numeric upper bound inferred from that qualification.

Outputs distinguish score direction, exact numerical equality(abs(m)<=1e-7), and
within-similarity-band status. Tiny direction and similarity can coexist. Unresolved
is an evidence state; abstention predictor not added. Exact equality requires zero
within numerical tolerance; similarity may include zero. Similar rows with zero
score are not assumed confirmed literal equalities. This is set-valued semantic
compatibility, not conventional four-class accuracy.

Validation: same401 row order/family folds as v10,5 folds x5 seeds. V10 control
trained on prior labels; v11 candidate trained on clarified labels. Same inherited
base alpha/pooling/radius settings. Inner3 training-family folds select prior strength
by mean strict-direction/exact-equality/practical-similarity recall, then overall
compatibility and reversals. The metric/selection semantics changed alongside loss
and evidence; this is not a pure architecture or data-only ablation. All original
v10 held-out band predictions reproduce exactly. Report denominators: only4 similar
pairs make macro compatibility especially sensitive; repeats are not independent.

Matched v10 control / v11 candidate on clarified targets:
- Correct score direction,260 strict pairs:89.69% /89.77% (including tiny signed gaps).
- Literal zero-score equality recall,137 retained equality labels:0% /0% held out.
- Practical band coverage,4 pairs:45% /50% (1.8/4 vs2/4 average per repeat).
- Combined semantic compatibility58.60% /58.70%; macro44.90% /46.59%.
- Opposite SIGN errors26.4 /26.2, counting tiny negative gaps inside the band too.
Separately, legacy three-way band diagnostic on397 determinate labels:76.52% /76.17%
accuracy, balanced75.28% /74.87%, band-masked reversals11.4 /11.4. Its tie recall
71.09% /71.39% means near-band classification, NOT literal price equality. Do not
compare new semantic percentages directly with old published401-row accuracy.
No overall improvement established. No fresh prospective holdout was collected.

Full-data strength10; domestic score scales shade1.000/vintage1.039/tare0.951,
not monetary percentage changes. All27 enforced pure-tare equalities remain zero
in training; literal equality recall27/137 (19.71%) there, versus0% held out. This
highlights failure to transfer exact equality, not failure of stored constraints.
Four practical pairs: Southeast/Northeast and Northwest/Western Europe fit inside
0.2 band; Southeast/Western Europe and Northeast/Western Europe remain outside.
Known Northeast>Northwest direction retained. No directions inferred as user labels
for practical pairs. Legacy full-data band consistency357/397, not held-out accuracy.

Nine checks passed: scoped reconciliation/input preservation; source/evidence hash
immutability; distinct practical loss and no hard equality; explicit metrics;
analytic gradients and old-objective equivalence when similarity absent; graph
semantics; family preservation/baseline reproduction/training scope; full-grid
monotonicity and27 hard tare equalities; reported metric reconstruction.
Run: PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 .venv-regional/bin/python refit_weighted_v11.py
Tests: PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 .venv-regional/bin/python -m unittest test_weighted_v11.py
Versioned outputs refuse changed overwrite. Batch exited; no server started.


## Round 33 completed — practical similarity clarified; no model changes

round33-reconciliation.json preserves all five raw pricing responses and a later
explicit semantic clarification: practical similarity, not necessarily identical
prices, when close provenances alone do not provide meaningful differentiation.
A tiny premium may exist; a significant provenance difference can still decide.
Scope is the current golden20/120 close-provenance comparisons and related wording;
never blanket relabel every historic tie. No numerical tolerance elicited.
Original option3 responses preserved for provenance, with clarification stored
separately; not ready to ingest as hard equalities. Round33-1 retains explicit
slight A direction plus qualification. Other similar pairs have no newly assigned
premium direction. Prior equality-cycle audit is conditional on exact semantics;
clarification removes justification for hard equality links, not proof of a new
consistent global ranking. Future evidence reconciliation must distinguish exact
equality, practical similarity and unresolved without inventing numeric margins.
Evidence v10, all models, frozen scores, and original Q7/Q11 unresolved status
remain unchanged. No refit or new evidence version authorized by this clarification.


## Independent peer review handoff

peer-review.md is the self-contained review brief dated2026-10-27. The portable
peer-review-packet.zip contains evidence/model history, current tests and a SHA-256
manifest; review-environment.json and review-requirements.txt record numerical
versions. No models or evidence changed during document preparation.
Documentation correction: full-fit threshold is0.2; actual inherited outer-fold
thresholds vary0.15/0.2/0.3/0.4/0.5, with alpha/pooling also fold-specific. Current
comparisons share identical per-fold settings. Saved result method prose that says
0.2 throughout validation is shorthand/inaccurate; code and fold_audits govern.
See peer-review.md for the independent review questions and read-only instructions.


## Selective convergence refinement — tested; retain v10 baseline

Candidate: selective_convergence_model.py; runner: compare_selective_convergence.py.
Snapshot/results: selective-convergence-comparison-v10.json (candidate_fit_all_401).
Tests: test_selective_convergence.py; nine passed. Evidence-v10.json remains
unchanged (401 labeled pairs); original round27-7/11 remain unresolved/excluded.
All earlier model sources/results, evidence and frozen round scores unchanged.
No promotion: strict regional premiums improve, but overall accuracy and regional
and general tie recognition regress against v10.

Refinement keeps the first convergence layer's contextual regional representation,
but anchors complete regional score gaps and adjacent-context changes to a v10
pilot fitted only on training data. Domestic shade/vintage/tare scales FIXED to
that pilot, not jointly shrunk by the fusion objective. Fusion strength varies
with matched-regional training support in the same provenance pair: reciprocal
age/shade-distance kernel; multiplier(1+ties)/(2+ties+4*premiums). Age weights remain
20/25/30/35/40 =2/1/2/3/4, modeling conventions rather than universal cutoffs.
Strict matched-regional losses weighted by training tie/premium ratio clipped[1,4].
No conversion of 'slightly' to numeric prices; no hard regional equalities or
pair-lookup predictions. 101 regional parameters fitted +3 fixed offering scales.

Selection averages overall class-balanced accuracy and matched-regional equality
versus correct-premium balanced accuracy, from inner3 grouped folds; strength
0.1/1/10, ties favor smaller strength. Pilot prior selection uses additional3
subfolds inside each inner training partition, never its validation labels.
Outer pilot uses saved v10 training-selected settings; full pilot is saved v10
all-data fit. Same v10 five outer family folds xfive seeds. Every v10 held-out
prediction reproduced exactly. All fold local contexts/fusion support restricted
to training. Repeated adaptive evidence and exploratory refinement, not fresh
prospective validation or an unbiased claim after model search.

Mean withheld-family v10 / selective candidate:
- Overall76.36% /75.11%; balanced75.15% /73.72%.
- All exact-tie recall70.71% /66.29%; opposite-winner errors11.4 /14.4 per401.
- Domestic cross-zone78.98% /75.59% (118 cases).
- Matched domestic regional ties90.71% /82.86% (56 cases).
- Older (age>=30) matched regional ties87.65% /83.53% (34 cases).
- Younger matched regional ties95.45% /81.82% (22 cases).
- Strict matched-regional premiums38.57% /52.86% (14 cases), versus1.43% for first
  convergence candidate. Selective candidate calls6.6/14 ties on average; no
  wrong-way strict regional predictions in this subset.
- Pure-tare tie54.81% /54.81%; strict96.10% /96.10%. ALL tare-only predictions
  match baseline in every outer repeat, as intended by fixing offering scales.
Accuracy ranges73.82–78.55% /73.07–77.31% describe split sensitivity, not confidence.

Full-data selected strength0.1 (outer21/25 folds choose0.1,3 choose1,1 chooses10).
Domestic scales identical to v10 within solver tolerance:1.041/1.060/0.983.
Full-fit consistency357/401 (89.03%), below v10's364/401; not validation accuracy.
All27 pure-tare equalities exact;8/56 matched regional equalities exact (all8 older).
All seven original Round27 misses classify correctly in full fit, including the
three regional ties Q3/Q9/Q14, which are decision-band ties, NOT zero score gaps.
Resolved Q15 remains A correctly; resolved Q20 incorrectly predicts A rather than
tie. Original Q7/Q11 remain unlabeled. More premium retention trades away equality
recognition; do not claim combined success or replace baseline.

Checks passed: baseline/evidence/source hashes, unresolved exclusion, outer/inner/
pilot-subfold separation and training-only support, adaptive strict-support
protection, exact v10 embedding and locked component scales, every tare-only
held-out prediction unchanged, analytic gradient and QP/SLSQP parity, full-grid
monotonicity/foreign invariance, symmetry, exact tare constraints and metrics.
Run with existing isolated .venv-regional and requirements-regional.txt:
OPENBLAS_NUM_THREADS=1 .venv-regional/bin/python compare_selective_convergence.py
OPENBLAS_NUM_THREADS=1 .venv-regional/bin/python -m unittest test_selective_convergence.py
Versioned result refuses changed overwrite. Batch exited; no server/watcher started.


## Regional convergence experiment — tested; retain v10 baseline

New candidate: regional_convergence_model.py. Reproducer: compare_regional_convergence.py.
Results/snapshot: regional-convergence-comparison-v10.json, candidate_fit_all_401.
Evidence-v10.json remains unchanged:401 labeled pairs; original Q7/Q11 excluded.
All existing models, source evidence, elicitation rounds and frozen scores unchanged.
This experiment is NOT promoted: convergence improves regional ties but erases
strict regional premiums, with essentially unchanged overall held-out accuracy.

Architecture: replace persistent domestic region offsets + tier gates (33 layer
parameters) with a common domestic intercept,100 centered shade/age regional
parameters and3 positive offering scales (104 predictive parameters total).
L1 fusion of pairwise complete domestic scores at reference tare120 permits
numerically zero regional gaps. Region-specific tare curves remain distinct, so
reference equality need not hold at other weights. No hard regional tie labels.
Prespecified fusion weights by age20/25/30/35/40 =2/1/2/3/4; fusion coefficient0.3,
gap ridge0.1, adjacent-age/shade gap smoothing0.5. These are modeling conventions,
not elicited prices or universal cutoffs. Soft hierarchy has zero minimum margin,
allowing equality. Same weak young premium-region guidance as baseline retained.
Full-grid age/shade/tare monotonicity preserved; foreign-only scores unchanged.

Same v10 outer family folds:5 folds x5 seeds; same training-selected offering
settings/decision threshold. Inner3 family folds refit offering+new layer, select
strength0.1/1/10 without outer outcomes. Every saved v10 held-out prediction
reproduces exactly. Full-data offering snapshot identical to v10. No label leakage
from withheld families; same repeatedly used adaptive data, not fresh validation.

Mean withheld-family results, v10 baseline / convergence candidate:
- Overall accuracy76.36% /76.46%; balanced75.15% /75.34%.
- All exact-tie recall70.71% /75.43%; opposite-winner errors11.4 /12.8 per401.
- Domestic cross-zone accuracy78.98% /76.78% (118 cases).
- Matched domestic regional ties90.71% /96.07% (56 cases).
- Older matched domestic regional ties (age>=30)87.65% /95.88% (34 cases).
- Matched domestic strict regional premiums38.57% /1.43% (14 cases): new model
  calls13.8 of14 ties per split on average. This is the central failure mode.
- Pure-tare exact ties54.81% /67.41%; pure-tare strict96.10% /95.12%.
Overall ranges73.82–78.55% /72.57–79.30% are split sensitivity, not confidence intervals.

Full-data strength10; domestic shade/vintage/tare scales1.210/0.985/0.581. These
are score scales, not price percentages. Training consistency343/401 (85.54%)
versus v10's364/401; not validation accuracy. All27 hard pure-tare ties remain
exact;45 of56 matched regional ties have zero score gap within1e-7 (28/34 older).
Round27 Q3/Q9/Q14 now score equal within1e-7, resolving the targeted training
misses. But Q19 and resolved Q15 become predicted ties (answers B and A), and
resolved Q20 is predicted B (answer tie). Known Western-Europe-versus-southeast
copper35 tare-scope regression remains correct. Original Q7/Q11 still unlabeled.
Conclusion: indiscriminate convergence sacrifices meaningful small premiums;
keep v10 baseline. Any follow-up structural experiment must be separately saved
and validated; do not tune against these outer results and call it fresh evidence.

Solver/runtime: OSQP1.1.3 installed only in .venv-regional (system-site-packages),
pinned in requirements-regional.txt. Objective unchanged from SLSQP reference;
full-data parity checked at strengths0.1/1/10 with identical classifications and
objective differences below0.0001. Initial slow SLSQP validation stopped before
completion; restarted full run with equivalent QP solver. Eight tests passed:
source/evidence immutability, unresolved exclusion, folds/baseline reproduction,
training-only local contexts, numerical gradient, QP/reference parity, full-grid
monotonicity/foreign invariance, exact tare equalities, symmetry, and all metrics.
Run: OPENBLAS_NUM_THREADS=1 .venv-regional/bin/python compare_regional_convergence.py
Tests: OPENBLAS_NUM_THREADS=1 .venv-regional/bin/python -m unittest test_regional_convergence.py
New outputs refuse nonidentical overwrites. Completed batch processes exited;
no server/watcher launched. Existing baseline runtime still unchanged.


## Current analytical evidence — version 10; weighted hierarchy refit completed

Current input: evidence-v10.json (401 unique labeled pairs:178 A/83 B/140 ties).
Candidate/results: weighted-hierarchy-comparison-v10.json, candidate_fit_all_401.
Reproducer: refit_weighted_v10.py. Verification: test_weighted_v10.py (six passed).
366 parent rows preserved exactly +35 unique additions:16 answered Round27 pairs,
one explicit provenance-swap supplemental pair,16 fresh component/variant pairs,
and two resolved originals (Round27 Q15=A slightly; Q20=exact tie). One repeated
pair (round32-1 versus round25-17, reversed orientation) confirms existing evidence
and adds no sample weight. Eight unresolved presentations are excluded; originals
round27-7 and round27-11 retained separately as unresolved_pairs, never training ties.
Q20 label basis preserves user's explicit clarification of identical wording in
previous matched-age probe. Raw answers, resolution sources,44 explanatory/workflow
metadata entries and confirmation audit retained. No quantitative strength targets
or universal rules inferred. Original frozen round files/scores remain unchanged.

Same architecture and priors: provenance-scoped offering model plus weighted
contextual domestic hierarchy. Base alpha0.1,pooling1,threshold0.2 inherited;
prior strength selected by inner grouped training folds. Full-data strength1;
domestic shade/vintage/tare scales1.041/1.060/0.983 (score contributions, not prices).
No uncertainty/abstention mechanism added; unresolved pairs do not receive labels.
No promotion or modifications to existing models, pricing.py, or prior evidence.

Validation: five outer family folds x five seeds. Preserve original v9 family
assignments, assign new families without labels. Matched control uses only v9
training rows/settings; candidate adds eligible v10 rows and reselects hierarchy
prior strength in inner training-only folds, refitting offering model inside each.
All366 original v9 held-out control predictions reproduce exactly for every seed.
Local contexts derived only from each fold's training data; no family leakage.

Matched control / v10 candidate, same401 held-out comparisons:
- Accuracy76.66% /76.36%; balanced accuracy75.13% /75.15%.
- Exact-tie recall70.29% /70.71%; opposite-winner errors11.6 /11.4 per401.
- Domestic cross-zone accuracy78.98% /78.98% (118 cases).
- Pure-tare exact ties59.26% /54.81% (27 cases).
- Pure-tare strict preferences95.61% /96.10% (41 cases).
- New35 comparisons66.86% /69.14%; their tie recall35.0% /43.33%.
No overall improvement established. Accuracy ranges75.06–78.05% /73.82–78.55%
are split sensitivity, not confidence intervals. Adaptive nonrandom evidence reused;
this is grouped validation, not a fresh prospective model test.

Full-data training consistency364/401 (90.77%), not validation accuracy. All27
observed pure-tare equalities have exactly zero fitted score difference. Scope
regression intact: Western Europe copper35 120=125; southeast120>125.
Of seven original Round27 misses, full fit now matches Q4/Q13/Q18 tare ties and
Q19 tradeoff. Q3/Q9/Q14 regional equalities remain misclassified even in training.
Resolved Q15 and Q20 classify correctly; Q20 tie is within decision threshold,
not exact score equality (margin0.111668). Original Q7/Q11 remain unresolved.
Next structural work should focus on regional equalities/contextual convergence;
this run supplies evidence, not authorization to alter the baseline or add rules.

Checks: reconciliation/deduplication and unresolved guards; immutable source and
question/prediction hashes; preserved family folds/control reproduction; training-
only local contexts; full-grid weak age/shade/tare monotonicity, foreign regional-
overlay invariance, symmetry and all27 hard tare equalities; reported metrics.


## Completed isolation — Round 32: Superbowl Questions 7 and 11

round32-isolation.json records six answered variants and two unresolved original
revisits. Original Q7 and Q11 remain unresolved, not exact ties. For Q7, B130 favors
A slightly, while prior B120 favored B slightly; improving either offering alone
to pale/straw favors that offering slightly. For Q11, pale/straw35 versus brown20
favors B slightly, while prior pale/straw25 favored A slightly; reducing either
original offering alone from120 to110 lb favors that offering slightly. Original
same-shade Q7 and equal-tare Q11 remain too close to call. No exact crossover or
numeric premium inferred. Provenance variant for Q11 has not been tested.
Both model snapshots and all original/adaptive prediction hashes verified unchanged.
Round27 receipt/score unchanged. Retain scoped explanations, deduplicate repeated
pairs in future evidence; never turn unresolved originals into training ties.


## Completed isolation — Round 31: Superbowl Question 20

Original unresolved pair: Northeast versus Western Europe, golden25/120 matched.
round31-isolation.json retains unchanged v9/v8 weighted models and source hashes.
Q1 exact tie at golden35/120; Q2 explicitly clarified exact tie at golden20/120. Q3 resolves original golden25/120 pair as exact tie, applying the user’s immediately preceding clarification of identical wording (shade difference needed). Raw wording and label basis preserved; no age interpolation.
Original25-year pair resolved; Round27 receipt/score unchanged. Original freeze applies to questions[:1];
Q2 and Q3 each have separate adaptive_question_freezes hashes. Adapt subsequent probes to user answers, widen contrasts if useful;
freeze each added prediction before presenting. One question at a time, explicit
A higher / B higher / exactly equal / unresolved. Predictions hidden; no refits.
Only a direct revisit resolves original. Prior Q15 resolved A slightly; Q7/Q11
remain unresolved with their separate adaptive variants answered. Round27 unchanged.


## Completed isolation — Round 30: Superbowl Question 15

round30-isolation.json uses unchanged v9 and previous v8 weighted hierarchy
snapshots from Round27. Three fixed questions: copper versus golden at20 years;
golden20 versus golden25; then original copper20 versus golden25. All Southeast,
120 lb. Q1 exact tie; Q2 A slightly; Q3 directly resolves original round27-15 as A slightly. Shades equally valued in this context; vintage decides. Preserve Round27 unresolved receipt and frozen score; reconcile resolution once under original ID in future evidence. Both models unchanged. Present one at a time with explicit A/B higher,
exactly equal, and unresolved options. Preserve explanations separately; component
answers cannot resolve the original. Repeats marked for deduplication. All three
predictions frozen and hidden; no refit. Original Round27 receipt unchanged.
Prior Superbowl Q7 and Q11 remain unresolved; adaptive variants recorded separately.


## Active isolation — Round 29: Superbowl Question 11

round29-isolation.json uses unchanged v9 and previous v8 weighted hierarchy
snapshots from Round27. Three fixed questions: pale/straw versus brown at30 years;
brown30 versus brown20; then original pale/straw30 versus brown20. All West Central
Asia,120 lb. Q1 answered A; Q2 answered B; Q3 original full pair remains unresolved (too close to call). Adaptive Q4 answered A slightly: only A vintage reduced to25; pale/straw outweighs the five-year vintage difference. Original full pair remains unresolved. Both models unchanged. Original freeze applies to questions[:3]; Q4 has a separate adaptive_question_freezes hash. Present one at a time with explicit A/B
higher, exactly equal, and unresolved options. Preserve explanations separately;
component answers cannot resolve the original pair. Repeats marked for deduplication.
All three predictions frozen and hidden; no refit. Round27 receipt unchanged.
Round28 Q7 remains unresolved at B125; adaptive B120 variant favors B slightly.


## Active isolation — Round 28: Superbowl Question 7

Adaptive Q5 answered B slightly: Central golden25/110 versus Northeast golden20/120,
reducing only original B tare from125 to120 at user request. Original four-question
plan hash preserved over questions[:4] (initial_frozen_question_count); new Q5 has
its own adaptive_question_freezes hash. Both model snapshots unchanged; predictions
hidden. Original full pair remains unresolved; this probe cannot resolve it directly.

round28-isolation.json freezes the same v9 and previous v8 weighted hierarchy
snapshots from Round27. Four planned questions: provenance only at golden25/110;
vintage25 versus20 at Northeast golden/110; tare110 versus125 at Northeast golden20;
then original Central golden25/110 versus Northeast golden20/125.
Questions 1–2 answered B slightly; question 3 answered A; question 4 remains unresolved: "Very very close. Too close to call." Initial four-question isolation complete. Do not convert uncertainty into exact equality. Both models unchanged. Present one at a time with explicit pricing options,
including exactly equal and unresolved. Preserve explanations separately. Component
answers do not resolve the original or imply additive strength arithmetic. Original
Round27 receipt/score stays unchanged; direct resolution recorded here. Repeats are
marked for later deduplication. Both models and all four predictions fixed/hidden.


## Completed frozen comparison — Round 27

round27-fixed.json compares v9 weighted hierarchy (candidate_fit_all_366) against
previous v8 weighted hierarchy (candidate_fit_all_341). All 20 questions presented;
16 resolved; Q7, Q11, Q15 and Q20 unresolved and tagged superbowl for later discussion.
Both models: 9/16 correct (56.25%), identical predictions on resolved pairs.
Strict preferences: 7/8 correct; exact ties: 2/8 correct. Shared misses:
Q3/Q9/Q14 (regional equalities at 35 years), Q4/Q13/Q18 (110–115 lb local
pure-tare equalities), Q19 (predicted A, user B: 20 lb outweighs five years + region).
Q2 supplied a separate provenance-swap counterfactual, retained outside frozen score.
User explanations remain scoped metadata. Q14 suggests shade for later isolation;
no specific counterfactual winner was elicited there. Superbowl items remain unlabeled.
All source hashes and frozen plan hash verified; all predictions independently
recomputed from saved snapshots. No refit, baseline modification or promotion.
Small purposeful test, not a population accuracy estimate. Next review can address
Superbowl questions 7/11/15/20 one at a time, preserving originals and distinguishing
component probes from direct resolutions.


## Current analytical evidence — version 8; provenance-scoped refit completed

Current input: evidence-v8.json. Candidate/results: provenance-comparison-v8.json.
Reproducer: refit_provenance_v8.py. Verification: test_provenance_v8.py.

341 distinct comparisons = 310 parent v7 + 17 answered Round23 + 11 fresh Round24
components + 3 resolved formerly unanswered pairs. Round24-2 corrects round23-10
from A to exact tie IN PLACE; it is not an additional sample. Round23 Q15's in-round
correction stays intact. Resolution rows keep original round23 IDs with explicit
round24 provenance. Counts: 156 A / 66 B / 119 ties. The difficulty explanation is
saved as workflow_feedback, never a pricing label or extra sample. Parent evidence
and every historical model/score are unchanged.

Unchanged provenance-scoped architecture: local curves enabled from training
pure-tare inputs, pooled toward shared shade/vintage curves; exact constraints only
on their own provenance. All-data model has 41 local contexts / 281 parameters.
Alpha 0.1, pooling 1.0, threshold 0.2 remain fixed from the prior full-data candidate.
No new hyperparameter tuning or model promotion.

Validation extends the ORIGINAL v7 family folds: old families retain their exact
folds; three new families are assigned by size without labels. Original training-
selected per-fold settings are reused. Matched control uses only v7 training rows;
v8 candidate adds eligible new rows. Local contexts and hard constraints are derived
inside each training fold only. Control predictions on the original 310 held-out
rows exactly reproduce the original scope comparison, verified by assertion/tests.
This is a fixed-settings data-update experiment, not a newly tuned contender.

Mean matched control / candidate results on the same 341 held-out pairs:
- Accuracy: 76.4% / 76.4%.
- Balanced accuracy: 74.6% / 74.5%.
- All exact-tie recall: 70.4% / 71.3%.
- Tare-only tie recognition (23 cases): 54.8% / 65.2%.
- Strict tare preference accuracy (37 cases): 96.8% / 95.7%.
- Opposite-winner errors: 10.6 / 10.4 per 341.
Overall performance is flat despite better targeted tare ties. The same adaptive
nonrandom evidence is reused; no claim of new population accuracy or significant
improvement. Split ranges are sensitivity, not confidence intervals.

Full-data fit: 312/341 classifications correct (training consistency only).
All 23 observed pure-tare ties have exact score equality within tolerance, including
the five recent targets round23-1/7/10/13/19. The original scope regression still
passes: Western Europe copper35 120=125; southeast copper35 120>125. No strict
preference is forced to zero solely by the fixed local equality bounds. This does
not imply all historical comparisons fit or all unseen contexts transfer correctly.

Six tests passed: reconciliation/accounting/no mutation; resolution/override guards;
historical hashes; original-family fold preservation and exact control prediction
reproduction; training-only local contexts; provenance scope and known regression;
full-grid monotonicity/symmetry/metrics. Versioned outputs refuse silent replacement.
No existing model, evidence version, or frozen score changed. New modeling should
use v8; old loaders are for baseline reproduction. Once incorporated, these answers
are training data rather than fresh validation. A prospective test needs new frozen
unseen pairs. User feedback: isolate provenance/tare and exact equality/tiny premiums
when questions are difficult, without inferring subjective reasons from outcomes.

## Current analytical evidence — version 9; weighted hierarchy refit completed

Current input evidence-v9.json; candidate/results weighted-hierarchy-comparison-v9.json;
reproducer refit_weighted_v9.py; verification test_weighted_v9.py.
366 distinct pairs = 341 parent v8 + 20 Round25 answers + 5 fresh Round26 components.
Counts: 167 A / 71 B / 128 exact ties. No corrections or repeated samples in this
update. Twenty-five scoped explanations are retained separately as metadata, not
additional observations, numeric margins, or universal hard age/tare thresholds.
Historical models, input evidence and original frozen scores remain unchanged.

Unchanged weighted-hierarchy architecture/priors: base provenance-scoped offering
pipeline refit on training rows, regional context gates and domestic component
scales fitted afterward. No new universal >=30 equality or >=10 dominance rule was
inserted. Recorded labels supply those contexts; explanations preserve scope for
future design. Selected all-data prior strength 1.0; component scales relative to
refitted offering: shade1.068, vintage1.104, tare0.948 (preference contributions,
NOT percentage price changes). Base settings and decision threshold remain as in
the old recipe; threshold0.2. Exact tare equalities retain provenance-local scope.

Validation preserves original v8 family assignments; only new families assigned
without labels. Matched control fits v8 training rows with its saved training-
selected prior strength; candidate adds eligible v9 rows and reselects prior
strength within inner training-only three-family folds, including refitting the
base offering on inner training only. Five outer folds x five seeds. Original
control predictions reproduce prior results exactly on all 341 parent rows.

Mean matched weighted control / v9 candidate:
- Overall accuracy:76.5% /77.6%.
- Balanced accuracy:74.6% /75.7%.
- Exact-tie recall:72.5% /73.6%.
- Domestic cross-zone accuracy (104 pairs):77.5% /80.2%.
- Opposite-winner errors:10.0 /10.4 per366 predictions.
This is modest exploratory improvement with a small reversal trade-off, not proof
of fresh population accuracy. Split ranges overlap; repeated adaptive evidence is
not new independent samples. Do not compare directly to different-size earlier tests.

All-data fit337/366 (training consistency only). All three original misses now
classify correctly: round25-11 tie, round25-13 tie, round25-18 B. Age boundaries
also classify correctly: NE>central amber25, NE=central amber30; southwest>central
brown25, southwest=central brown30. The regional tie scores are nonzero gaps within
the classifier band, NOT exact underlying utility equality. All24 confirmed pure-
tare ties have equal fitted scores within tolerance. The Western Europe copper35
equality and southeast copper35 strict preference scope regression still passes.

Six tests passed: accounting/metadata separation/no duplicates or mutation; source
guards; historical hashes; family isolation and original control reproduction;
foreign scores unchanged by the regional overlay relative to the newly refitted
base offering; exact tare equalities/full-grid weak monotonicity/symmetry/metrics.
The refitted base offering can differ from old versions; foreign invariance applies
to the overlay, not an assertion all foreign scores stayed fixed across refits.
No model promoted. Future experiments should use v9 evidence; prior loaders remain
for historical reproduction. Round25/26 now training data, not fresh validation of
v9; a prospective comparison needs new frozen unseen questions.

## Round 26 — three Round25 misses isolated; models unchanged

Completed in round26-isolation.json: five fresh diagnostic comparisons, no repeats,
corrections or unresolved answers. Explanations saved alongside labels; no extra
synthetic observations or numerical strength targets added.

- Original Q11 (NE=SE amber25/120) stays unchanged. Wider tier contrast NE versus
  central is A very slightly at amber25/120, exactly equal at amber30/120. User
  states otherwise-identical >=30 would tie; directly tested boundary is30.
- Original Q13 (northwest copper40 120=125 lb) stays unchanged. New 120>130 lb
  is very slight; user attributes it to tare with all other attributes equal.
- Original Q18 (southwest > central brown20/120 very slightly) stays unchanged.
  New brown25/120 still favors southwest very slightly; brown30/120 ties exactly.

These findings distinguish within-premium-tier comparability from an age-dependent
premium between tiers. They do not imply every 20-year offering converges or every
provenance premium disappears at30 regardless of shade/tare. Fixed global age/gap
rules and numeric exchange rates have not been established.

Both weighted-hierarchy and provenance-v8 source/model hashes verified unchanged.
Evidence-v8 and original Round25 frozen scores (17/20 weighted,18/20 baseline)
unchanged. No refit or promotion. Future authorized integration may add Round25's
20 answers and these five fresh comparisons once; explanations are metadata, not
independent samples. This diagnostic is not new predictive-validation accuracy.

## Round 25 — weighted hierarchy versus current provenance v8 COMPLETE

All 20 answered, no unresolved pairs. Q20=A very slightly with explanation. Both
models, coefficients, priors, thresholds, question order and pre-answer predictions
verified unchanged throughout. Record, explanations and rule_statements are in
round25-fixed.json. Explanations are not extra training samples or numeric weights.

Frozen result: weighted hierarchy 17/20 (85%); current provenance-scoped v8 18/20
(90%). No opposite-winner errors for either. Weighted gets 12/13 strict preferences
and 5/7 exact ties; current gets 13/13 strict preferences and 5/7 exact ties.
Both get all three young-premium-versus-tare cases and both five-year/20-lb trade-offs
right. They also both get the two foreign controls right. Small purposeful sample,
not a population accuracy estimate or a decisive global model ranking.

Shared misses:
- Q11 NE vs SE, amber/25-year/120 lb: user exactly equal, both predict A.
- Q13 northwest copper/40-year 120 vs125 lb: user exactly equal, both predict A.
Additional weighted-model miss:
- Q18 central vs southwest, brown/20-year/120 lb: user B very slightly, weighted
  predicts tie; current v8 predicts B correctly.
This suggests distinguishing convergence WITHIN a similarly valued tier from
flattening the premium BETWEEN tiers. The current soft template uses one context
gain; a future experiment may separate these effects, but no change is authorized
by this result alone and no refit has been performed.

User explanations to retain with scope:
- Comparable premium zones can tie with shade/vintage/tare equal; a >5 lb tare
  difference can decide when other attributes match. Do not impose globally.
- >=10-year youth advantage usually compensates for extra tare, particularly in
  premium regions; the three tested combinations support this. Usually is not always.
- Five-year youth plus a premium region can lose to 20 lb lighter tare (Q14/Q17).
- Brown at >=30 years has reduced zone sensitivity, especially comparable zones.
- Brown at 20 years can still carry a small premium-zone advantage (Q18).
- Youth plus lower tare can outweigh a higher region (Q12/Q19); do not infer either
  component alone is sufficient without an isolated comparison.
No monetary exchange rates or universal thresholds were elicited. This round's
qualitative guidance was saved without updating either frozen model mid-test.

README and handoff updated. Evidence-v8, all prior models, and historical frozen
scores unchanged. No promotion. Future authorized incorporation should add the 20
pairs once and keep explanatory statements separate from observed labels. Once used
for fitting/tuning, this round ceases to be fresh validation for that new candidate.

## Latest experiment — soft domestic hierarchy with contextual premiums

User supplied the Monopoly/property analogy: northeast highest, southwest and
southeast close behind, central/northwest slightly lower; some 20-year offerings
can be similarly valued. Comparable zones shift importance to offering attributes.
Young vintage in a premium region should almost always outweigh size, with observed
exceptions respected. This is recorded as a SOFT prior, not new pair labels or
permission to overwrite earlier explicit answers.

Built two separate candidates, leaving all baselines/evidence-v8 unchanged:
1. domestic_hierarchy_model.py -> domestic-hierarchy-comparison.json: regional
   overlay with 5 domestic residual levels and 25 shade/vintage hierarchy gains.
   Existing offering calculation fixed within each training fold; foreign-only
   comparisons and all pure-tare score differences remain unchanged.
2. weighted_domestic_model.py -> weighted-domestic-comparison.json: joint domestic
   regional layer and three positive offering-component scales (shade/vintage/tare),
   plus a soft average hierarchy-order penalty. Foreign scores unchanged. Positive
   tare scaling preserves exact pure-tare ties and score direction, though decision
   thresholds may classify a small strict score differently.

Prior conventions (not measured prices): centered tier template [2,1,1,0,0] in
NE/SW/SE/central/NW order; residuals allow within-tier variation and exceptions.
Context gains are nonnegative, partially pooled, with extra soft shrinkage toward
zero at 20 years. Average gain target 0.1; weighted model's average order margin
0.03. These are preference-unit regularization conventions, not dollar weights.
The weak dominance prior uses 30 synthetic scenarios: premium domestic region at
20 years versus central/northwest at 30 years, same shade, 130 versus110 lb.
Margin convention 0.05. They are penalty scenarios ONLY, never evidence rows or
validation successes; no hard 20-versus25 dominance assumption was added. Only
TWO recorded pairs directly match young-premium/heavier versus older/lighter
domestic offerings, both supporting younger; neither identifies a general rate.

Validation: same current-v8 withheld-family partitions, seeds and offering settings.
Inner three-family folds refit offering on inner training only, then regional layer;
select prior strength from 0.1/1/10 by balanced accuracy. Outer test outcomes excluded
from fitting/selection. Baseline outer predictions reconstructed exactly. The weighted
variant was explored after seeing regional-only results; all results remain exploratory,
not pristine prospective tests. No prior strength chosen from outer test scores.

Mean held-out accuracy / balanced accuracy:
- Current v8 provenance-scoped baseline: 76.4% / 74.5%.
- Regional hierarchy overlay: 75.6% / 74.1%.
- Weighted hierarchy: 75.7% / 74.0%.
Domestic cross-zone accuracy (84 pairs): 79.3% baseline, 76.4% overlay, 75.2% weighted.
Same-attribute domestic 20-year comparisons (16 pairs): 92.5%, 73.8%, 77.5%.
Small slice; do not generalize as population rates. No demonstrated predictive upgrade.

The weighted full-data candidate expresses the stated baseline better: average
regional scores NE .877, SW .802, SE .853, central .547, NW .486 (preference units,
NOT prices). NE leads in 21/25 shade/age regional-premium contexts; SE leads in four
20-year contexts. Thus the hierarchy is soft and young offerings can converge.
Regional spreads at age20 versus30: brown .279/.442; copper .274/.389; amber
.287/.519; golden .334/.431; pale/straw .381/.463. Full offering spreads differ
because scoped tare curves also contribute; do not call all 20-year prices equal.
Learned domestic component multipliers relative to the existing score calculation:
shade 1.043, vintage 1.078, tare .908. These are NOT percentage price changes.
The 30 prior scenarios have positive final margins in the weighted full-data fit,
but this is compliance with an imposed prior, not independent validation.

All 11 tests pass (six regional, five weighted): analytic gradients, template and
convergence mechanics, original-score recovery, foreign score preservation, exact
pure-tare equalities, full-offering weak monotonicity, symmetry, fold isolation,
metrics, and all historical hashes. No model promoted. Data/prices/old outcomes
remain unchanged. Soft hierarchy can encode the user's intent without yet improving
held-out agreement with historical answers. A future fresh test should distinguish
similar 20-year regional bundles, younger premium versus lighter older offerings,
and genuine exceptions; do not repeat prior scenarios as if independent validation.

## Round 24 — miss isolation and unresolved review COMPLETE; models unchanged

Record: round24-isolation.json. Fifteen pricing responses: 11 fresh component
pairs, one explicit original-pair correction, three previously unanswered pair
resolutions. A separate subjective-difficulty response is NOT a pricing sample.

Correction: round23-10 (central pale/straw/20-year 120 vs125 lb) changed from A
higher to exactly equal in round24-2. Preserve as explicit evidence_override for
future reconciliation; do not rewrite the original frozen Round23 score. Its
120-vs130 wider contrast is A very slightly. Other four original local tare ties
remain unchanged; tested 10 lb contrasts favor the lighter option very slightly.

All three unresolved pairs resolved directly after component isolation:
- round23-3: Western Europe amber30/125 vs northwest/120 = exact tie; two small
  isolated advantages offset by the user's direct answer.
- round23-9: southeast amber25/125 vs northeast/120 = B very slightly; provenance
  tied at equal tare, while lighter northeast carried the preference.
- round23-18: Western Europe golden25/120 vs northwest/125 = A very slightly;
  provenance tied at equal tare, while lighter Western Europe carried the preference.
Resolution IDs are stored in unresolved_queue; original source files stay intact.

The user explicitly explained the difficulty as a combination of separating
provenance and tare effects and distinguishing exact ties from very tiny premiums.
Use this to improve elicitation: compare components separately, then return to
the concrete original pair, with explicit same-price vs tiny premium vs unresolved
options. Do not infer equality from repeated strength adjectives or add a universal
threshold. This explains the user's hesitation here, not all historical model errors.

No pricing questions or difficulty clarification remain pending. Both models and
all source hashes remain unchanged; no refit, promotion, or evidence-v7 update.
Future authorized incorporation should apply the one correction in place, add the
11 fresh comparisons and three resolutions once, and preserve source provenance.
Round23 Q15's earlier in-round correction remains as recorded. A changed-label
retrospective rescore is not a new frozen-test accuracy result.

## Round 23 — provenance-scoped versus contextual v7 COMPLETE; no refit

17 answered; Q3/Q9/Q18 unresolved and excluded. Q15 was explicitly corrected
from A to exact tie before scoring; history retained and counted once. All models,
coefficients, local context lists, thresholds, order and predictions remain frozen.
Record: round23-fixed.json. No evidence-v7 update or candidate promotion.

Previous shared-scope contextual v7: 16/17 (94.1%). Provenance-scoped candidate:
12/17 (70.6%). Planned categories:
- Adjacent tare: shared 6/7, scoped 2/7.
- Wider tare: both 4/4.
- Other answered trade-offs: both 6/6 (three of this category unresolved).
Actual labels: 9 A, 8 ties, no B. Both got 8/9 strict preferences; neither reversed
a winner. Shared recognized all 8 exact ties; scoped recognized 4/8.

Both miss Q10: central pale/straw/20-year 120 versus125 lb, user A higher but
both predict tie. Scoped additionally misses four exact 5 lb ties, predicting A:
Q1 northeast copper/35-year 120/125; Q7 West Central Asia copper/35-year 120/125;
Q13 northwest golden/40-year 115/120; Q19 southeast brown/30-year 120/125.

This test supports broader transfer of plateaus in these cases and exposes a
cost of the current provenance-scoped fit. It does NOT undo the documented
southeast/Western Europe copper35 constraint conflict or justify forcing every
provenance to share hard equality. The scope correction remains necessary, but
its current transfer/pooling behavior is not a predictive upgrade here. Retain
both baselines; consider better calibrated partial sharing with scoped constraints
only in an explicitly authorized future experiment.

Small targeted sample, rich in adjacent-tare probes and no B preferences; not a
population accuracy estimate. No pooling of scores from different model versions.
Q3/Q9/Q18 remain on the unresolved list. This round is separate from training and
loses fresh-validation status if later used to tune or fit. All source/model hashes
and original historical test receipts verified unchanged.

## Latest architecture correction — provenance-scoped tare constraints

User explicitly requested fixing the shared-curve conflict identified in the
annotation. Implemented separately in provenance_tare_model.py; candidate and
validation receipts in provenance-tare-comparison.json; tests in
test_provenance_tare_model.py. Existing models and evidence-v7 remain unchanged.
No production promotion or evidence version change.

Exact tare constraints now bind a provenance/shade/vintage-local curve, never a
shared curve. Local curves are activated from TRAINING pure-tare comparison inputs
regardless of whether the answer is tie or strict, and partially pooled toward the
shared shade/vintage curve. Unobserved local contexts fall back to the learned
shared curve; this does not assert observed equality there. Full dataset: 27 local
contexts, 225 parameters versus the original 117. Nonnegative steps and full-grid
linear constraints preserve weak tare/age/shade monotonicity.

Specific annotated regression FIXED in the new fitted candidate:
- round21-12: Western Europe copper/35-year 120 lb = 125 lb, score gap exactly zero.
- round14-2: southeast copper/35-year 120 lb > 125 lb, classified as the confirmed
  strict preference. Its local step is not fixed by Western Europe's tie.
All 16 confirmed pure-tare equality cases have exact fitted score equality within
1e-7; no strict-preference feature difference is forced entirely to zero by the
direct step-fixing constraints. This does not claim every observed ranking fits.

Paired scope-ablation validation: same outer family folds/seeds and ORIGINAL
training-selected per-fold alpha/pooling/threshold from contextual v7. Local curve
activation and exact constraints use training rows only. Settings were held fixed
to isolate the scope change; no separate hyperparameter search for this candidate.
Results (shared-scope contextual v7 / provenance-scoped candidate):
- Overall accuracy: 75.7% / 75.9%.
- Balanced accuracy: 74.1% / 74.5%.
- All exact-tie recall: 75.1% / 70.7%.
- Strict pure-tare preference accuracy: 88.0% / 96.8%.
- Pure-tare tie recognition: 72.5% / 51.3%.
- Opposite-winner errors: 10.2 / 10.4 per 310.
This fixes constraint scope, not a demonstrated overall predictive upgrade.
Private scope reduces unjustified equality transfer but also loses some useful
transfer to withheld provenance contexts. More parameters need careful regularization.
The all-data candidate also regresses round21-3 from tie to B; round21-8 remains
predicted tie instead of A. Document these limits; do not imply all misses are fixed.

All-data fit: 280/310 classifications correct (training consistency only).
All six tests passed: scope of equality bounds, exact reported regression, shared
model reduction/penalty equivalence, training-only context selection and reuse of
training-selected settings, full-offering monotonicity/symmetry/metrics, and baseline
file hashes. Model source snapshots and historical scores are preserved. A fresh
frozen evaluation or training-only pooling calibration is needed before promotion.
The repeated exploratory validation is not an independent population accuracy claim.

## Current analytical evidence — version 7; contextual refit completed

Evidence-v7.json is current analytical input: 310 unique observations = 281 parent
v6 + all 20 Round21 answers + 9 fresh Round22 components. The Round21 Q11 review
and Round22 Q3 confirmation add no duplicate weight; one confirmation attaches to
round21-8. No label corrections. Counts: 138 A / 65 B / 107 ties. Prior evidence,
source files, baseline models, and frozen results remain hash-preserved.

Candidate/results: contextual-comparison-v7.json. Reproducer: refit_contextual_v7.py.
Tests: test_contextual_v7.py. Model remains the 117-parameter exact-tare contextual
structure: shade/vintage-specific steps shared across provenances, training-only
hard pure-tare equalities, pooled nonlinear curves, weak monotonicity and near-tie
classifier. Selected alpha 0.1, pooling 1.0, threshold 0.2. No architecture change,
price deployment, or baseline promotion.

Same outer 5-family folds x 5 seeds, inner 3-family folds; identical held-out rows
for a separately fold-trained contextual control restricted to v6 evidence versus
v7 candidate using the eligible new rows. Saved old coefficients are untouched.
Mean contextual control / v7 results:
- Accuracy: 75.2% / 75.7%.
- Balanced accuracy: 73.5% / 74.1%.
- All exact-tie recall: 70.1% / 75.1%.
- Opposite-winner errors: 10.4 / 10.2 per 310 predictions.
- Tare-only tie recognition (16 cases): 43.8% / 72.5%.
- Tare-only strict preference accuracy (25 cases): 97.6% / 88.0%.
Tie gains therefore come with a loss of genuine small premiums. This is a modest
trade-off, not an established broad improvement. Small targeted slices and reused
nonrandom evidence are not prospective population accuracy estimates.

All-data fit 269/310 classifications correct (training consistency only). All 16
pure-tare ties have exactly equal fitted scores within tolerance, enforced on
training evidence. The three latest tie targets round21-3/11/12 classify as ties;
only Q12 has exact underlying score equality, the other two use the decision band.
The confirmed central golden25 > pale30 preference (round21-8) still classifies tie.

EXPLICIT STRUCTURAL CONFLICT: round14-2 says southeast copper/35-year/120 lb is
strictly above 125 lb. Round21-12 says Western Europe at the same shade, age, and
tares ties. This model shares the step across provenances, so the hard Western
Europe equality forces southeast's step to zero. Its original strict answer is
retained and counted as a miss in forced_rank_conflicts; it was NOT erased or
changed to equality in the evidence. No amount of retuning the same fixed step
can satisfy both. Do not promote this candidate as honoring every confirmed rule.
Address provenance scope of the tare context before treating hard ties as universal.

All six verification tests passed: accounting/deduplication/no mutation, correction
guard, prior file hashes and original Round21 scores, training-only constraints and
nested split isolation, forced-conflict audit, exact pure-tare scores, full-offering
monotonicity, symmetry and metrics. Historical scores remain contextual16/20 versus
additive v6 11/20 for Round21. Round21/22 are now training data for the new candidate;
a future prospective test needs new frozen questions. No existing model was replaced.

## Round 22 — all four contextual-model misses isolated; no model changes

Completed in round22-isolation.json: 10 responses, 9 fresh component pairs,
1 explicit confirmation repeat; no corrections or unresolved answers.

- Round21 Q8: central golden/25-year/120 lb > pale/straw/30-year/120 lb very
  slightly, explicitly reconfirmed. Isolated pale-over-golden shade premium at
  30 years and golden 30-to-25 vintage premium were each very slight; direct
  comparison establishes the age premium is larger. The contextual-model
  opposite-winner regression is therefore still a confirmed miss.
- Round21 Q3: southeast125 = southwest125 and southwest120 = southwest125 at
  copper/30-year. Southwest120 > southwest130 very slightly. Component answers
  support the original exact tie.
- Round21 Q11: southwest125 = northeast125 and northeast120 = northeast125 at
  amber/30-year. Northeast120 > northeast130 very slightly. Component answers
  support the original exact tie, including the user-requested Round21 review.
- Round21 Q12: original Western Europe copper/35-year 120=125 lb remains unchanged;
  newly tested 120>130 lb very slightly. Larger tare difference matters here.

Scope caution for future fits: context_steps currently shares a shade/vintage
curve across all provenances. A prior southeast copper/35-year 125-vs-120 strict
preference (round14-2) and Western Europe's exact 120-vs-125 tie (round21-12)
are different judgments at the same shade/age/weight step. Do not impose one
shared hard plateau and silently erase that strict preference. These are modeling
constraints to reconcile, not authorization to change either original answer.

Both model snapshots/source hashes verified unchanged. Evidence-v6 and frozen
Round21 results (contextual16/20, v6 11/20) unchanged. No refit or promotion.
Future authorized incorporation should add Round21's 20 answers and these 9 fresh
component pairs once, attach the confirmation without extra weight, and preserve
the original evaluation receipts. Diagnosis is not fresh predictive validation.

## Round 21 — exact-tie contextual versus v6 frozen test COMPLETE

All 20 answered. User-requested Q11 review confirmed the original exact tie before
scoring; counted once, history retained. No unresolved exclusions. Every frozen
source/model/plan hash verified unchanged. Full record: round21-fixed.json.

Exact-tie contextual 16/20 (80%); additive v6 11/20 (55%). Planned categories:
- Adjacent-tare probes: contextual 6/7, v6 0/7. All seven user answers were exact
  ties. The six correct contextual ties also have zero score gaps within 1e-7,
  rather than relying only on the prediction band.
- Wider-tare probes: both 5/5; all user answers were A higher.
- Other trade-offs: contextual 5/8, v6 6/8.
Actual response mix: 12 ties and 8 A preferences, no B preferences. Overall exact
 ties recognized: contextual 9/12, v6 3/12. Strict preferences correct: contextual
7/8, v6 8/8. Opposite-winner errors: contextual one, v6 zero.

Contextual misses:
- Q3 southeast copper/30-year/125 lb vs southwest/120 lb: user tie, model B.
- Q8 central golden/25-year/120 lb vs pale/straw/30-year/120 lb: user A, model B.
  This is the one reversal introduced where v6 was correct; prioritize diagnosis.
- Q11 southwest amber/30-year/125 lb vs northeast/120 lb: user tie, model B.
- Q12 Western Europe copper/35-year/120 lb vs 125 lb: user tie, model A.

This is prospective support for transfer of known shade/vintage tare plateaus to
fresh provenance pairs, not an overall population-accuracy claim. The set was
purposefully heavy in adjacent-tare probes; all happened to be ties. It does not
yet establish preservation of tiny strict premiums across 5 lb in other contexts.
Do not hide the 5/8 versus 6/8 trade-off result or the new reversal behind 80%.
No model promotion, refit, or training evidence update was made. Preserve all
baselines and evidence-v6. Any future use in tuning removes this round's fresh
validation status. Score receipts remain immutable historical evidence.

## Latest experiment — context-specific nonlinear tare models tested

User authorized testing contextual nonlinear tare against v6 using confirmed
equalities and unchanged withheld-family validation. Existing models and evidence
remain unchanged. Files: compare_tare_models.py / tare-model-comparison.json;
exact-constraint ablation compare_exact_tare_ties.py / exact-tare-comparison.json.
Tests: test_tare_models.py and test_exact_tare_ties.py (five passed each).

Same evidence-v6 (281 pairs), five outer family folds x five seeds, three inner
family folds, and training-only selection of regularization/pooling/tie threshold.
Saved v6 outer predictions are reused exactly; no in-sample baseline comparison.
Candidates retain the same provenance, shade, vintage terms and ranking/tie loss:
- Global steps: 21 parameters, four nonnegative tare steps shared across contexts.
- Context steps: 117 parameters, four nonnegative steps for each shade/vintage
  combination (25 contexts), shrinking toward shared global step curves.
- Context exact-ties: same contextual structure; only confirmed PURE-TARE exact
  ties in the training fold force traversed steps to zero. Held-out labels never
  determine bounds. Other ties remain soft. Provenance-specific tare is NOT modeled.
Linear inequality constraints retain younger/lighter-shade weak monotonicity at
all tares; nonnegative steps retain weak lighter-tare monotonicity.

Mean held-out accuracy / all-tie recall / opposite-winner errors per 281:
- Linear v6: 74.6% / 60.7% / 8.6.
- Global steps: 75.0% / 62.6% / 8.4.
- Context soft ties: 74.0% / 63.3% / 12.0.
- Context exact training ties: 74.9% / 72.7% / 11.2.
These do not establish a general accuracy gain; ranges overlap and repeated
nonrandom data is not fresh prospective evidence. Do not claim the best headline
percentage is a deployment winner. The exact-context variant improves equality
recognition while losing some genuine preferences and making more reversals.

On the SEVEN confirmed tare-only tie cases, withheld recognition is 11.4% linear,
14.3% global steps, 42.9% soft context, 48.6% exact context. This very small slice
is descriptive; repeats are not independent new cases. Strict pure-tare preference
accuracy drops from 100% linear to 92.9% exact context across the 17 strict cases.
Provenance+tare accuracy is 65.1% linear versus 66.2% exact context.

Full-data exact-context fit: 250/281 classifications correct (in-sample only),
alpha 0.1, pooling 10, threshold 0.2. All seven observed pure-tare exact ties have
underlying score gaps zero within 1e-7, verified. The three latest cross-provenance
original misses round19-14/15/20 are all classified tie, but their score gaps are
~0.017, 0.042, 0.019: those are NOT exact fitted price equalities. Never conflate
a decision-band tie with equal scores or dollar amounts. Monotonicity and symmetry
are checked over all 1,250 offerings. Some untested contexts inherit shared effects;
this is extrapolation, not a claim that every provenance follows a known plateau.

The model can express the intended plateau behavior (synthetic test), and the
training constraint enforces known pure-tare equalities. Generalization to unseen
families remains limited. Recommended next step, if requested: freeze exact-context
candidate versus v6 on fresh comparisons covering both local ties and genuine
small preferences; keep overall and focused diagnostics separate. Do not replace
v6 or rewrite its historical scores. No model has been promoted.

## Latest diagnostic — audit the persistent v6 errors before another refit

User observed the repeated ~74% plateau and asked to focus on missed cases.
Audit implementation: audit_model_errors.py; output: error-audit-v6.json;
verification: test_error_audit.py. No model, coefficients, evidence, or historical
result changed. Each outer-fold prediction was reconstructed using its ORIGINAL
training rows and saved selected settings; all labels exactly matched saved v6
validation. This is an audit, not a newly tuned model.

281 distinct pairs evaluated over 5 reused splits, NOT 1,405 independent samples.
Mean 71.4 errors per 281 predictions:
- 35.8 missed exact ties (50.1% of errors).
- 27.0 real preferences called ties (37.8%).
- 8.6 opposite-winner errors (12.0%).
Thus 87.9% involve tie-versus-strict classification, but not necessarily tiny
score differences. Some exact ties receive large predicted margins.
43 pairs are wrong in all 5 repetitions, 20 in 4/5, and 9 in 3/5. This provides
a targeted diagnostic list; do not count repetitions as independent evidence.

84 pairs lie in identical-feature groups containing different observed labels.
Their mean error rate is 49.3%, versus 15.2% for the other 197 pairs. They account
for 41.4 of 71.4 mean errors (~58%). These are representation conflicts, NOT
proof of contradictory user answers. Example: a 5 lb lightness advantage has
identical additive features across contexts, yet northwest amber/40-year has a
strict preference (round14-5), while southwest brown/30-year has exact equality
(round18-5). Provenance-only comparisons also collapse across shade/age even when
rankings change. More examples with the same representation cannot fully resolve
those conflicting labels without changed features or an explicit response model.

Largest error volumes: provenance+tare 24.8 mean errors across 71 pairs (34.9%
error rate), provenance-only 24.0 across 93 (25.8%). Shade+vintage has 42.5% error
across 16 pairs and contains many outright reversals. Shade+tare has 60% error,
but only 8 pairs: treat its size cautiously. Vintage+tare is comparatively strong
at 91.5% correct across 40 pairs. Tiny slices are not robust population estimates.

Priorities for the next experiment:
1. Context-sensitive nonlinear tare effects/price plateaus, tested against the
   confirmed same-5-lb strict-versus-equal cases, rather than one global tare slope.
2. A small set of supported provenance/context effects, with pooling; broad
   interactions previously did not earn a clear generalization gain.
3. Targeted clarification of persistent shade/vintage reversals, especially the
   European versus West Central Asia trade-offs. Keep endpoint wording concrete.
Train/validate on the full evidence, not only failures; report targeted and overall
held-out results to catch new regressions. Do not manually patch all 43 cases or
add an interaction solely to memorize a comparison. New untouched prospective
validation is required after selecting a change from this audit.

A post-hoc threshold sweep over the reconstructed margins is saved as exploratory
only: best observed accuracy ~75.7%, and widening trades missed ties for lost real
preferences. It is NOT a valid new accuracy claim or authorization to change the
saved threshold. Models remain unchanged. All four audit tests passed.

## Current analytical evidence — version 6; additive refit completed

Evidence-v6.json is the current analytical input. Results/coefficients are in
additive-comparison-v6.json; reproducer refit_additive_v6.py, tests test_additive_v6.py.
281 unique observations = 252 parent v5 + 20 Round19 answers + 9 fresh Round20
component pairs. No new corrections, repeats, or inferred pairwise answers added.
Labels: 126 A / 64 B / 91 exact ties. All parent data and historical receipts remain
unchanged; versioned writes reject different content under an existing version.

Unchanged 18-parameter additive model with linear lightness, nonnegative shade/age
increments, provenance offsets, squared ranking hinge plus squared tie gaps, ridge,
and learned global tie band. Selected alpha 0.1, threshold 0.2. Preference-score
candidate only; not a price deployment or calibrated monetary margin.

Matched-family validation uses five outer folds x five seeds, inner three folds.
Compare a newly fold-trained control restricted to eligible v5 rows versus a
candidate using eligible v6 rows on identical outer held-out families. Existing
saved v5 model coefficients are untouched. Mean control / v6 results:
- Accuracy: 74.8% / 74.6%.
- Balanced accuracy: 73.1% / 73.1% (rounded; slight decline for v6).
- Opposite-winner errors: 9.8 / 8.6 per 281 predictions.
- Exact-tie class recall: 64.4% / 60.7%.
Performance is flat overall with fewer reversals but worse tie recall. Do not
claim v6 is an upgrade, or compare its score directly to older different-sized
validation sets. This is iterative use of nonrandom data, not fresh prospective
validation. Split ranges overlap and are not confidence intervals.

All-data fit: 227/281 correct (training consistency only). All three isolated
original ties remain missed: round19-14 predicts A, round19-15 predicts B,
round19-20 predicts B. Merely adding more examples to this fixed structure has
not solved its handling of exact local tare plateaus and attribute offsets.
The evidence remains distinct from the candidate's approximations. A tie-band
classification does not ensure equal fitted utility or exact dollar prices.

Five verification tests passed: source accounting/no duplicates or mutation;
unresolved/repeat guards; baseline/evidence hashes and original frozen scores;
matched nested family isolation and metric reconstruction; candidate symmetry and
weak monotonicity over the full offering. No model promoted or replaced. Historical
answer files, evidence v2-v5, all prior models, and Round19's 17/20 versus 11/20 score
remain unchanged. Round19/20 are now training inputs for v6; a new prospective test
must use new frozen comparisons. Future modeling should consider the repeated
structural tie limitation rather than assuming another unchanged refit will fix it.

## Round 20 — all three Round19 misses isolated; models unchanged

Completed in round20-isolation.json: 9 fresh component pairs, no corrections,
no unresolved answers, no direct original-pair repeats. All three original ties
are consistent with the separately answered equalities:

- Round19 Q14: southwest125 = southeast125, and southwest120 = southwest125,
  pale/straw/20-year. Southwest120 exceeds southwest130 very slightly.
- Round19 Q15: Western Europe120 = central120, and central115 = central120,
  golden/40-year. Central115 exceeds central125 very slightly.
- Round19 Q20: West Central Asia125 = South/Eastern Asia125, and South/Eastern
  Asia120 = South/Eastern Asia125, amber/20-year. South/Eastern Asia120 exceeds
  South/Eastern Asia130 very slightly.

These context-specific adjacent-tare equalities plus wider strict preferences
reinforce a limitation of exact pricing with a single strictly positive linear
tare term. Do not infer a universal cutoff or monetary premium from strength words.
Original ties were supported by component answers, not independently re-asked.

Both E and additive-v5 model/source hashes verified unchanged. Evidence-v5 and the
original frozen Round19 result (17/20 vs 11/20) remain unchanged. No refit or
promotion. If later authorized, a new evidence version can incorporate Round19's
20 answers and these 9 distinct component pairs once; none is yet in training.
This adaptive diagnosis is not new predictive-validation accuracy.

## Round 19 — frozen v5 additive versus E COMPLETE; no refit

All 20 answered; no unresolved exclusions. Q20 exactly equal. Evidence/scores:
round19-fixed.json. Source/model hashes, coefficients, threshold, order and
predictions verified unchanged throughout.

V5 additive matched 17/20 (85%); revision E matched 11/20 (55%). V5 got all
13 strict preferences correct and recognized 4/7 exact ties. E got 9/13 strict
preferences correct and recognized 2/7 ties. Opposite-winner errors: zero vs four.

V5 misses, all user exact ties:
- Q14 southwest pale/straw/20-year/120 lb vs southeast/125 lb: model A.
- Q15 Western Europe golden/40-year/120 lb vs central/115 lb: model B.
- Q20 West Central Asia amber/20-year/125 lb vs South/Eastern Asia/120 lb: model B.

Small purposeful varied test, not population accuracy. Similar scores in different
rounds are not controlled head-to-head comparisons of additive versions, and must
not be pooled as one frozen model. No evidence-v5 update, refit, or promotion.
Round19 remains outside training until explicitly incorporated; then it is no
longer fresh validation. Exact equality remains the miss category for v5 here.
All prior models, evidence snapshots and scoring receipts are unchanged.

## Current analytical evidence — version 5; additive refit completed

Current input: evidence-v5.json. Candidate/results: additive-comparison-v5.json.
Reproducer: refit_additive_v5.py. Verification: test_additive_v5.py.

252 unique observations = 224 parent v4 + all 20 answered Round17 pairs + 8 fresh
Round18 component pairs. The Round18 Q3 confirmation attaches to round17-3 and
adds no independent weight. No corrections in this update. Label counts: 112 A,
62 B, 78 exact ties. All earlier resolutions and corrections remain intact.
Historical source files, model snapshots, and frozen scores are hash-preserved.

Unchanged 18-parameter additive structure, squared ranking-hinge + squared tie-gap
objective, ridge, nonnegative increments and learned symmetric tie threshold.
Selected all-data settings: alpha 1.0, threshold 0.3. This is an experimental
preference classifier, not a change to production prices or exact-price semantics.

Matched validation: five outer grouped folds x five seeds; inner three grouped
folds select parameters using training data only. Compare a newly trained control
using only eligible v4 rows with a candidate using v5 rows, on IDENTICAL outer
held-out families. Saved v4 model coefficients are not modified.
Mean control / candidate results:
- Accuracy: 74.1% / 73.4%.
- Balanced accuracy: 72.6% / 72.0%.
- Opposite-winner errors: 11.8 / 9.2 per 252 predictions.
This is mixed, not an established improvement: fewer reversals but lower exact
classification accuracy. Split ranges overlap; iterative nonrandom evidence is not
fresh prospective validation. Do not compare 73.4% to earlier differently sized
experiments as though they shared the same test set.

All-data fit is 195/252 (training consistency only). Of the three latest targets:
round17-3 still predicts B instead of tie; round17-13 still predicts B instead of
tie; round17-15 now predicts tie correctly. The first two exact offset/equality
relationships remain unsatisfied. Structural restrictions persist; a universal
linear tare term does not express all contextual price plateaus. Verbal strengths
remain uncalibrated. No promotion or baseline replacement was made.

Five new tests pass: evidence accounting/no mutation/duplicates; confirmation
rather than double-counting; correction guards; preserved baseline and evidence
hashes plus original frozen scores; nested family isolation/metrics; candidate
symmetry and weak monotonicity over every supported offering. Versioned writes
reject different content under an existing version name. Future new experiments
should use v5 as evidence, while old loaders remain for historical reproducibility.
Round17 and its isolation findings are now training inputs, not fresh validation
for this candidate. A prospective test needs a new frozen unseen question set.

## Round 18 — three Round17 misses isolated; models unchanged

Completed in round18-isolation.json: 9 responses, 8 new component pairs and
1 explicit original-pair recheck. No corrections or unresolved answers.

- Round17 Q3: Western Europe amber/20-year/125 lb exactly equals Eastern Europe/
  115 lb, explicitly reconfirmed. Western Europe's premium over Eastern Europe
  at 125 lb offsets the Eastern Europe115 premium over Eastern Europe125.
- Round17 Q13: northeast125 = southwest125 and southwest120 = southwest125,
  brown/30-year. These support the original northeast125 = southwest120 tie.
  Southwest120 exceeds southwest130 very slightly.
- Round17 Q15: northwest125 = Western Europe125 and northwest120 = northwest125,
  golden/35-year. These support the original northwest120 = Western Europe125 tie.
  Northwest120 exceeds northwest130 very slightly.

The latter observations establish contextual exact-price equalities over the
specified 5 lb steps and strict preferences across 10 lb, not a universal tare
threshold. Similar verbal strengths are not numerical equality evidence; the
first target's equality was answered directly. No original labels were changed.

Both model snapshots/source hashes are verified unchanged. Evidence-v4 and the
original 17/20 versus 13/20 frozen Round17 result remain unchanged. No refit or
promotion. Future incorporation should add the 8 fresh component pairs once,
attach the confirmation to its source rather than duplicate it, and include the
Round17 answers only in a new evidence version if authorized. Diagnosis is not
fresh predictive validation and should not be reported as accuracy improvement.

## Round 17 — frozen v4 additive versus E COMPLETE; no refit

All 20 answered, no unresolved pairs. Q20=A. Full evidence, hashes and scoring:
round17-fixed.json. Models, coefficients, threshold, question order and predictions
verified unchanged throughout.

Additive v4 matched 17/20 (85%); revision E matched 13/20 (65%). V4 got all 14
strict preferences correct and recognized 3/6 exact ties. E got 13/14 strict
preferences correct and recognized 0/6 ties. Opposite-winner errors: zero versus one.

V4 misses, all exact ties:
- Q3 Western Europe amber/20-year/125 lb versus Eastern Europe/115 lb: model B.
- Q13 northeast brown/30-year/125 lb versus southwest/120 lb: model B.
- Q15 northwest golden/35-year/120 lb versus Western Europe/125 lb: model A.

Purposeful small varied sample, not population accuracy. Do not compare 85% and
the previous v3 round's 88.9% as a controlled head-to-head: different questions.
Do not pool results across changing additive versions as if one model was frozen.
Evidence-v4 and all model/source artifacts remain unchanged; no refit or promotion.
This round is still outside training and loses fresh validation status if reused
for fitting or tuning. Exact ties remain the principal miss category in this round.

## Current analytical evidence — version 4; additive refit completed

Current input: evidence-v4.json. Candidate/results: additive-comparison-v4.json.
Reproducer: refit_additive_v4.py. Verification: test_additive_v4.py.

224 unique comparisons = 183 v3 + 18 originally answered Round15 + 8 isolation
component pairs + 15 previously unresolved pairs resolved in Round16. Label counts:
95 A / 61 B / 68 exact ties. Each saved-pair resolution keeps its original source
ID and attaches round16 resolution provenance and prior unanswered state. Saved
source rows were not separately duplicated. The 15 resolutions include the two
Round15 unresolved pairs; the historical Round15 score still uses its original 18.
All prior v2/v3 corrections survive unchanged. No pending pair from the review
remains excluded from v4. Verbal strengths are retained without numeric targets.

The additive model structure is unchanged: 18 parameters, linear lightness,
nonnegative shade/age increments, provenance offsets, squared ranking hinge plus
squared tie gaps, ridge, and a learned symmetric tie band. Final settings alpha
0.1 and tie threshold 0.3. This is an experimental preference classifier, not a
production price change or a guarantee of exact fitted equalities.

Validation uses five outer grouped folds x five seeds, inner three grouped folds.
On identical test families, a newly trained control restricted to v3 training
rows is compared with a candidate using all eligible v4 training rows. Saved v3
coefficients are untouched. Mean results (v3-evidence control / v4 candidate):
- Accuracy: 72.4% / 73.1%.
- Balanced accuracy: 71.4% / 72.1%.
- Opposite-winner errors: 13.8 / 12.0 per 224 predictions.
- Exact-tie class recall: 63.8% / 63.2%.
This is a modest gain, not a clear tie-handling improvement. Repeated adaptive
data and overlapping split ranges do not establish fresh prospective performance.
Do not directly compare the older 183-row 73.4% to this 224-row 73.1% as regression;
the matched same-test-family control is the appropriate comparison.

All-data fit: 179/224 classifications correct (training consistency only).
Both focal exact ties remain missed: round15-4 predicts A, and round15-14 predicts
A. The two isolated adjacent-tare equalities also predict A. Wider tare preferences
are reproduced, but a single strictly positive linear tare effect cannot produce
exact adjacent equality and wider strict ordering as an exact utility rule. The
classifier's tie threshold also did not recover them at selected settings. Do not
claim merely including these observations has solved the structure limitation.
Hard ranking/equality feasibility remains false for this restricted model.

All five new tests passed: exact accounting and resolution provenance, duplicate
and override guards, old model/evidence/frozen-score hash preservation, matched
family splits and metric reconstruction, symmetry and full-offering weak monotonicity.
Original E, v3 candidate, earlier models, historical answer files and test receipts
are unchanged. No candidate was promoted. Future experiments should load v4;
legacy loaders intentionally reproduce historical inputs. Any new validation claim
requires a new frozen unseen set, since these resolutions/isolation answers are now
used in fitting. Versioned output files refuse silent replacement by different data.

## Round 16 — both misses isolated; all 15 unresolved pairs RESOLVED

Completed in round16-isolation.json: 23 answers = 8 fresh isolation pairs + 15
resolutions of previously unanswered pairs. Saved-pair outcomes: 9 exact ties,
5 B preferences, 1 A preference. All queue entries reference verified matching
resolution endpoints and answers. None remains unresolved in this review.

First miss (round15-4), southeast versus central brown/40-year:
- southeast120 = central120;
- southeast115 = southeast120;
- southeast115 > southeast125 very slightly;
- southeast115 > southeast130 slightly.
These are consistent with the original southeast115 = central120 answer.

Second miss (round15-14), southwest versus southeast pale/straw/30-year:
- southwest115 = southeast115;
- southwest110 = southwest115;
- southwest110 > southwest120 very slightly;
- southwest110 > southwest130 slightly.
These are consistent with the original southwest110 = southeast115 answer.

Do not recast the explicit adjacent-tare equalities as uncertainty. They and the
wider strict preferences cannot all be exact consequences of one strictly positive
linear tare term. Possible future structures include context-dependent nonlinear
tare effects or explicit price levels, but the limited findings do not identify a
universal threshold or justify extrapolation across all shades, ages, and zones.
No model changes were made.

The canonical resolution map is round16-isolation.json -> unresolved_queue;
historical files intentionally retain their old unresolved/deferred statuses and
frozen scores. In a future evidence version, integrate each resolved pair ONCE,
using its resolution provenance; do not discard it merely because it has revisits
or duplicate the unresolved source row. Also integrate the 8 new component pairs
and eligible Round15 answered pairs if authorized. Do not retroactively score these
15 resolutions as new successes in the historical frozen rounds.

Original Round15 score stays 16/18 v3 versus 13/18 E. All model/source hashes
were verified unchanged. Training evidence remains v3; none of this diagnostic
or unresolved-review evidence has been fitted or promoted. This was adaptive
elicitation, not an independent predictive evaluation.

## Round 15 — frozen v3 additive versus E COMPLETE; no refit

All 20 presented. Eighteen answered; Q3 and Q9 unresolved and excluded. Q20=B.
Source hashes, coefficient snapshot, question order and predictions verified
unchanged throughout. Evidence/scores: round15-fixed.json.

V3 additive: 16/18 (88.9%); revision E: 13/18 (72.2%). V3 got all 13 strict
preferences correct and recognized 3/5 exact ties. E got 12/13 strict preferences
correct and recognized 1/5 ties. Opposite-winner errors: v3 zero, E one.

V3's only misses (both also missed by E):
- Q4: southeast brown/40-year/115 lb versus central brown/40-year/120 lb;
  user exactly equal, model A.
- Q14: southwest pale-straw/30-year/110 lb versus southeast pale-straw/30-year/115 lb;
  user exactly equal, model A.

Do not generalize 88.9% to population accuracy: this was a small purposeful varied
sample with explicit price-order wording. Do not pool earlier scores across
model versions as though they tested one unchanged model. No refit, promotion,
or evidence-v3 modification made. Round 15 remains separate from training and
loses fresh-test status if later used to tune or fit. Preserve Q3/Q9 unresolved
exclusions when proposing future questions. The v3 model remains the leading
prediction candidate here; exact tie behavior still needs calibration and is
not solved by classification alone. Both historical models remain unchanged.

## Current analytical evidence — version 3; additive refit completed

Evidence: evidence-v3.json. Refit/validation: additive-comparison-v3.json.
Reproducer: refit_additive_v3.py. Verification: test_additive_v3.py.

183 distinct observations = 158 v2 + 19 answered Round 13 + 6 fresh Round 14
component pairs. Round 13 Q14 is unresolved and excluded. Round 14's original-pair
rechecks do not add samples: Q3 replaces round13-6 tie with B very very slightly;
Q6 and Q9 confirm round13-9 and round13-20. Label counts: 83 A / 50 B / 50 ties.
The v2 corrections remain intact. Historical sources and all model baselines were
hash-verified unchanged. Versioned outputs refuse replacement with different data.

The additive candidate retains 18 parameters, ranking squared-hinge + squared-tie
loss, ridge, weak monotonicity, and a learned symmetric tie band. Final settings:
alpha 0.1, threshold 0.4. Five outer grouped folds x five fixed seeds, inner three
folds. Compare two NEW fold-trained controls on identical outer test families:
one uses only the v2 subset of the training fold, the other all v3 training rows.
This does not alter any saved v2 model. No held-out family is used in training or
hyperparameter selection, for either control.

Matched-family mean results (v2-evidence control / v3 candidate):
- Accuracy: 72.5% / 73.4%.
- Balanced accuracy: 71.6% / 73.1%.
- Opposite-winner errors: 11.0 / 10.6 per 183 predictions.
The improvement is modest; split ranges overlap. Do not directly compare this
73.4% with the earlier 71.4% on a different 158-row test setup. Repeated adaptive
data and repeated splits do not constitute fresh prospective validation.

All-data fit: 148/183 classified correctly, which is NOT held-out accuracy.
Target results:
- Corrected round13-6: B, matched (also matched by the prior frozen prediction
  after correction; do not credit the refit for the label correction).
- Confirmed round13-9: exact tie, still predicted A.
- Confirmed round13-20: A, now matched instead of the previous tie.
At current coefficients, the absolute margin of Q9 (~0.486) exceeds Q20 (~0.478).
A single larger tie band would swallow the desired small Q20 preference before
fixing Q9. Thus do not globally widen the band to repair Q9 in isolation.

All three isolated findings are included, but not all are satisfied by the fitted
model. Hard ranking/equality feasibility remains false for the restricted additive
structure. Weak monotonicity can flatten steps; tie classifications do not ensure
exact equal utility or monetary prices. Qualitative strengths remain uncalibrated.

Five new tests passed: evidence accounting and correction provenance, no input
mutation or duplicates, override guards, preserved source hashes, matched grouped
splits and metrics, symmetry and full-offering weak monotonicity. No model was
promoted to production. Revision E, original additive snapshots, prior interaction
and objective results remain unchanged. New work should read evidence-v3.json;
legacy loaders intentionally retain historical evidence for baseline reproduction.
Round 13 has now been used in fitting and must not be called fresh validation of
this v3 candidate. A future prospective test needs newly frozen unseen comparisons.

## Round 14 — three misses isolated; models unchanged

Completed in round14-isolation.json: nine responses, six fresh component pairs,
three explicit original-pair rechecks. No unresolved answers and no refit.

- First target, round13-6: explicitly corrected from exact tie to **B higher,
  very very slightly** (southwest copper/35-year/120 lb over southeast/125 lb).
  Southeast120 = southwest120, and southeast120 narrowly exceeds southeast125.
  Preserve this as an evidence override; do not overwrite the original frozen
  score, baseline coefficients, or evidence-v2.json.
- Second target, round13-9: exact equality reaffirmed between northwest amber/
  40-year/120 lb and Western Europe/125 lb. The small Western Europe provenance
  premium and the small lightness premium offset in this specific pair.
- Third target, round13-20: **A higher very slightly** reaffirmed (southeast
  golden/30-year/120 lb over pale-straw/35-year/120 lb). The golden 35-to-30 age
  premium narrowly exceeds the pale-over-golden premium at 35 years. Both isolated
  components were very slight; the direct comparison establishes their ordering.

The historical frozen result remains 16/19 additive versus 11/19 E. With only
Q6's latest correction rescored, the same saved predictions would match 17/19
and 12/19 respectively, but that is retrospective clarified-label rescoring, NOT
an improved prospective test. No scoring receipt has been rewritten.

Next authorized modeling work should build a new evidence version from v2 plus
appropriate later observations, applying the round14-3 override in place and not
counting rechecks as new samples. Do not claim a global tie-band adjustment follows:
one genuine equality and one tiny strict preference remain. Local calibration
or context-specific effects may matter, but neither is uniquely identified here.
User requested models fixed for this diagnostic; do not refit or promote without
further authorization. All source/model hashes remain verified unchanged.

## Round 13 — frozen reconciled additive versus E COMPLETE; no refit

Question 20 answered A higher. Nineteen answered; Q14 unresolved and excluded.
Evidence: round13-fixed.json. Both model snapshots, source hashes, question order,
and all pre-answer predictions remained unchanged throughout.

Reconciled additive: **16/19 (84.2%)**, versus revision E **11/19 (57.9%)**.
Eight actual ties: additive recognized 6, E recognized 2. Additive had zero
opposite-winner errors and softened one real A preference to tie; E reversed two
strict preferences. These are prospective results on a preselected varied sample,
not a random population accuracy estimate or grounds for automatic deployment.

Additive misses:
- Q6: southeast copper/35-year/125 lb versus southwest copper/35-year/120 lb:
  user exactly equal; model B.
- Q9: northwest amber/40-year/120 lb versus Western Europe amber/40-year/125 lb:
  user exactly equal; model A.
- Q20: southeast golden/30-year/120 lb versus pale/straw/35-year/120 lb:
  user A higher; model tie.

No refit, promotion, or evidence-v2 modification made. Existing baseline models
and historical result files remain unchanged. Keep this round separate from the
158-row training evidence until a subsequent update explicitly incorporates it;
once used to fit or tune, it ceases to be fresh validation. Q14 belongs on the
unresolved exclusion list for future question selection. The additive candidate
is the leading predictor from this test, but its near-tie classifications do not
by themselves implement exact equal dollar prices in a production calculator.

## Current evidence and validation — reconciled version 2

Completed after Stefan approved applying the clarification corrections and rerunning
validation. `evidence-v2.json` is the current reconciled analytical input: 158 unique
comparisons, 73 A / 43 B / 42 exact ties. It replaces two labels in place and attaches
13 confirmations as provenance, without adding rows or increasing sample weights.
Stable original IDs/order preserve all family fold memberships. The two changes:
round7-9 A -> tie (round12-3), round11-17 B -> A (round12-4). Prior answers remain
attached in the versioned view; historical source ledgers are not overwritten.

`reconcile_and_compare.py` reproduces the snapshot and direct-ranking comparison.
`objective-comparison-v2.json` holds the new coefficients, settings, fold predictions,
feasibility checks, and hashes. Existing version paths reject different content;
future changes need a new version. `test_reconciliation.py` verifies exact changes,
no duplicated observations, reversed-option handling, override validation, snapshot
protection, historical hashes, identical folds, and metric reconstruction.

Same features, ranking/tie loss, nested groups, seeds, tuning grids, and selection
rule as the original objective experiment. On corrected labels, old OOF predictions
rescored / newly refitted OOF accuracy:
- Additive near-tie: 69.6% / 71.4%.
- Provenance-dependent shade: 69.4% / 69.0%.
- Provenance-dependent vintage: 69.1% / 71.0%.
New balanced accuracy: 70.4%, 68.7%, 70.6%, respectively. Comparing the earlier
68.4/68.1/67.8 scores directly to these mixes label rescoring with refitting; use
the same-label comparisons above. Split ranges are sensitivity, not confidence
intervals. This is repeated exploratory use of the same nonrandom sample, not a
new prospective validation or proof of a population accuracy rate.

The simpler additive candidate is a reasonable next frozen-test candidate because
complexity has not earned a clear gain. Existing E and all saved prior candidates
remain unchanged; no production replacement. The v2 candidates still predict tie
for the equal-tare West Central Asia ten-year trade-offs Q14/Q20, whose confirmed
answer is B. All predict the corrected Q17 answer A. Exact hard constraint feasibility
remains false for all three restricted families: the confirmed provenance/tare
interaction at 110 versus 120 lb remains unmodeled. Soft tie bands are not fitted
exact-price equality, and verbal magnitudes remain uncalibrated.

Important for future experiments: use evidence-v2.json, NOT the legacy loader's
unreconciled labels. Legacy scripts/results are intentionally preserved to reproduce
historical baselines. Confirmations/corrections from Round 12 are not a fresh holdout.
Freeze any newly chosen v2 candidate and a new diverse question set before claiming
prospective improvement. Five reconciliation tests passed. No Git repository exists
in this workspace; files are local and uncommitted.

## Latest clarification checkpoint — 15 answers; models unchanged

Round 12 is complete in round12-clarification.json: 13 direction confirmations,
2 corrections, and 5 explicit equal-price instructions. None selected uncertainty.
These are re-asked observations, not 15 new independent samples or validation data.

Apply the two explicit evidence_overrides before any new fit:
- round7-9 -> round12-3: southeast vs northeast, pale/straw/20-year/115 lb is now
  exactly equal, replacing A very slightly. At 110 lb southeast remains higher;
  at 120 lb exactly equal was reaffirmed. Tare dependence still has evidence,
  but the old boundary including 115 lb is stale.
- round11-17 -> round12-4: West Central Asia pale/straw/25-year/125 lb is now
  higher than brown/20-year/125 lb, replacing B from shared-reference wording.
  The prior West Central Asia/domestic reversal inferred from this answer is
  withdrawn as current evidence. Historical model comparisons remain reproducible
  snapshots of the old labels, not results on a reconciled current dataset.

West Central Asia's ten-year trade-off is reaffirmed: brown/25-year beats
pale/straw/35-year at equal 125 lb and in the original 125-versus-115 lb pair.
Other revisited directional comparisons and exact-price ties were confirmed.
Do not reduce the confirmed ties to mere uncertainty; the user selected exact
same price explicitly. Neither assume all errors are framing problems: most
revisited judgments stayed the same.

Next useful work is evidence reconciliation and a versioned rerun using corrected
labels, not more repetition or silent revision of saved baselines. Confirmations
replace/enrich source records without increasing their weight; corrections replace
old labels only in a new reconciled view. Keep all existing model/source files and
historical scoring receipts unchanged. No refit or reconciliation loader written
in this clarification checkpoint.

## Latest correction — Round 12 Q4

Direct endpoint instruction for West Central Asia pale/straw/25-year/125 lb versus
brown/20-year/125 lb is now A, strength unspecified. This explicitly supersedes
round11-17's B under the shared-reference framing; use round12's override before
future fitting. The previously claimed Q17/Q18/Q19 provenance reversal is NO LONGER
established by current answers. Its old model-structure inference is historical,
not a current justification for interactions. Other context dependence remains.
Q5 now awaits direct endpoints for round11-14: pale/straw/35-year versus brown/
25-year, both West Central Asia and 125 lb. Models and historical ledgers unchanged.

## Current clarification correction — Round 12 in progress

Q1: exactly equal at 120 lb, confirms round7-8. Q2: southeast higher very slightly
at 110 lb, confirms round6-2. Q3: exactly equal at 115 lb, explicitly REPLACES
round7-9's earlier A preference. Scope: southeast versus northeast, pale/straw,
20 years. The current confirmed distinction is at 110 lb; do not retain the old
115-lb preference in a future fit. The correction is stored as an evidence override
in round12-clarification.json; historical ledger and all baselines remain unchanged
for reproducibility. Apply overrides before any new fit; never double-count repeats.
Q4 has been answered (see latest correction): West Central Asia, 125 lb,
pale/straw 25-year versus brown 20-year. Do not show prior/model answers.

## Latest work — direct ranking/tie objective tested; clarification starting

New files: compare_objectives.py, objective-comparison.json, test_compare_objectives.py.
All old scripts, model coefficients/results, production pricing.py, and answer
ledgers were verified unchanged. No candidate was installed as the calculator.

The new convex objective uses squared hinge loss for strict rankings (penalize
wrong/insufficient direction, stop penalizing after an arbitrary unit margin),
squared score gaps for exact ties, and the existing ridge/partial-pooling penalties.
Unlike squared targets, large correctly directed gaps are not pulled back toward
+1/-1. The unit margin is a learning scale, NOT a monetary or verbal-strength value.

This is SOFT constraint fitting, not a guarantee of exact equality or every ranking.
Linear-program feasibility checks show all three restricted feature families cannot
satisfy all 158 hard ranking/equality constraints. Feature collisions explain part
of this: equal-tare southeast/northeast pale/20-year comparisons at 110/115 lb favor
southeast, but at 120/125/130 lb tie; these structures omit provenance-dependent tare
and represent those cases identically. This is a model restriction, not proof that
the user gave contradictory answers. Existing revision E has a narrow tare context
term and is NOT one of the models declared infeasible.

Same evidence, 5 repeated outer five-fold groups, inner three-fold groups, feature
families, alpha/pooling/threshold grids, and selection rule as the previous experiment.
Mean withheld-family accuracy (old squared-target -> direct-ranking objective):
- Additive near-tie: 63.3% -> 68.4%; balanced accuracy 62.3% -> 68.1%.
- Provenance-dependent shade: 60.6% -> 68.1%; balanced accuracy 59.4% -> 67.8%.
- Provenance-dependent vintage: 63.9% -> 67.8%; balanced accuracy 63.5% -> 68.1%.
Opposite-winner errors averaged 12.4, 12.6, 13.2 per 158, respectively. Additive and
shade improved all five paired splits; vintage improved four and tied one. These
are exploratory reuse of the same nonrandom data, not pristine held-out trials.
The three new candidates are too close to rank confidently by headline accuracy.

The all-data shade candidate has the correct underlying sign on the West Central
Asia Q17 reversal, but its learned band still predicts tie, not the user's B.
Vintage also predicts tie there, with the wrong underlying sign. Additive predicts
A. None fully resolves the diagnostic. All-data classifiers match 122/158, 126/158,
124/158 respectively. Predicted ties within a band are not exactly equal fitted
scores: the constraint audit records 41 nonzero fitted score gaps on 41 recorded
ties for each candidate. Do not claim hard equality constraints were satisfied.

All six new tests pass: analytical gradient, loss semantics, feasibility examples,
file preservation, swap symmetry/full-grid weak monotonicity, and same-family
splits/metric reconstruction. Reproduce with
`OPENBLAS_NUM_THREADS=1 python3 compare_objectives.py`.

Stefan requested clearer re-asking of prior uncertain/conflicting questions. Use
concrete final offerings and ask for a pricing instruction: A higher, B higher,
exactly the same price, or insufficient confidence. Keep uncertainty separate from
equal price; do not force a fabricated preference, invent dollar tolerances, or
silently overwrite old answers. Avoid strength labels on the first choice.
Follow up only where useful, using matched wider contrasts. Clarifications are
not independent fresh validation. New response record: round12-clarification.json.

## Latest work — provenance interaction models built and compared

`compare_interactions.py` builds separately saved candidates; `interaction-comparison.json`
contains validation predictions, chosen settings, coefficients, source hashes,
and training-only sensitivity results. `test_compare_interactions.py` verifies
splits, model structure, monotonicity, symmetry, metrics, and read-only baselines.

Evidence: 158 unique answered pairs (101 active + 18 Round 9 + 20 Round 10 +
19 unique Round 11). The Q13 confirmation repeat and all deferred/superseded
answers are excluded. Shared-reference questions compare their endpoint utility
differences; the common baseline cancels. Raw answers and qualitative strengths
are preserved and are not rewritten or assigned numerical strength targets.

Candidates: an 18-parameter additive near-tie CONTROL freshly fit for this
experiment; a 54-parameter model with provenance-specific shade increments; a
54-parameter model with provenance-specific vintage increments. All use learned
tie bands and nonnegative increments. Interaction coefficients shrink toward
shared means. These are preference classifiers, not price estimators. The existing
all-119 additive snapshots, revision E, and original comparison script/results
are unchanged; the new additive control does not replace a saved baseline.

Nested validation: five grouped outer folds, three inner folds, five fixed seeds.
All age/tare variants of an unordered provenance/shade family stay together.
Inner folds tune ridge strength, pooling strength, and tie threshold; outer answers
are excluded from fitting and tuning. Repeated splits reuse the same sample and
are not independent evidence. Dataset and model-family design are exploratory.

Mean held-out accuracy / balanced accuracy:
- Additive near-tie control: 63.3% / 62.3%.
- Provenance-dependent shade: 60.6% / 59.4%.
- Provenance-dependent vintage: 63.9% / 63.5%.

Accuracy excluding the 19 isolation probes: 60.6%, 57.8%, 61.2%, respectively.
Opposite-winner errors averaged 16.8, 15.4, 14.8 per 158. Vintage won three seed
splits, tied one, and lost one versus additive: its 0.6 percentage-point gain is
not convincing evidence of improvement. Split ranges overlap widely. The shade
candidate loses overall. Do not claim that better training fit proves generalization.

All-data selected candidates fit 118/158 additive and 124/158 each interaction.
Both selected interaction candidates still predict A for Round 11 Q17, which is
B (West Central Asia, 25-to-20 vintage premium exceeds brown-to-pale shade premium).
They also call ties on Q14/Q20, both B. Thus neither reproduces the central
structural discovery despite having the mathematical capacity to do so. A synthetic
unit test verifies that both interaction structures CAN express the provenance
reversal; failure is not a missing feature in the implementation.

With weaker pooling, shade can recover Q14/Q20 and reach 137/158 training matches
at one inspected setting, but Q17 remains tie or A. These are training-only
sensitivity checks with a fixed illustrative threshold, not selected validated
models. Do not promote the best in-sample setting or claim a solution to Q17.

Retrospective pre-Round-10 training on 119 answers: new additive control matched
16/20 Round 10 and 15/19 Round 11; shade 13/20 and 15/19; vintage 15/20 and 15/19.
The same rounds informed model design, so this is not pristine holdout validation.
The untouched baseline predictions remain: revision E 13/20 and 16/19; original
near-tie 16/20 and 15/19. No old coefficients or evidence files changed.

Recommendation: retain baselines. Before more elicitation or deployment, test a
training objective that better represents explicit ranking/tie constraints rather
than only squared error to +1/0/-1; keep the same disciplined held-out evaluation.
Any added interaction must improve generalization AND be checked against the
confirmed provenance reversal. Exact verbal margins remain uncalibrated, and
weak monotonicity permits flattened steps. No new candidate was installed as the
pricing calculator.

Reproduce: `OPENBLAS_NUM_THREADS=1 python3 compare_interactions.py`.
Verify: `python3 -m unittest -v test_compare_interactions.py`.

## Round 11 — isolation complete; both models unchanged

Evidence: round11-isolation.json. Twenty answers, 19 unique comparisons and one
explicit repeat (Q13 confirms Q2). Q20's “both add significant values” was clarified
as B, with no relative strength specified; it is not a tie. No refit was made.

At equal tare, West Central Asia brown/25-year beats pale-straw/35-year at both
125 lb (Q14) and 115 lb (Q20). The vintage premium already exceeds the shade
premium; the original younger brown option's lighter tare reinforces its advantage.

At West Central Asia/125 lb, the shade premium beats vintage 35-to-30 (Q15),
narrowly beats 30-to-25 (Q16), but loses to 25-to-20 (Q17). For the identical
25-to-20 versus shade comparison at 125 lb, domestic central (Q18) and southeast
(Q19, strongly) favor shade. Preserve the broader domestic qualification while
separating it from these two directly tested zones.

An independent provenance offset cancels from each within-provenance comparison.
Thus a global additive shade/vintage model cannot express the Q17/Q18/Q19 reversal;
a global tie band cannot repair opposite strict winners on identical feature
differences. Provenance-by-shade and/or provenance-by-vintage effects are needed,
but the data does not uniquely identify which component changes. Next experiment:
small regularized interaction candidates, without arbitrary per-pair patches.
Both existing models must remain fixed unless further changes are authorized.

Qualitative strengths are not measured additive numbers. The repeated ten-year
“overwhelmingly” answer alongside two five-year “slightly” answers is not alone an
ordinal contradiction. Do not infer a universal vintage cutoff or quantify the
shade/age/tare interactions from those words.

Diagnostic direction scores: E 16/19; near-tie 15/19. Both miss Q14/Q17/Q20;
near-tie additionally misses Q12. These adaptive, mostly single-factor probes are
not a fresh varied accuracy test and do not overturn the Round 10 comparison.
All 20 answers remain outside model fitting; source/model hashes still match.

## Round 10 — frozen two-model check COMPLETE; no refit

All 20 answered; no deferrals. Question 20: **A, strongly** (raw typo preserved).
Both models, source hashes, coefficient snapshot, question order, and predictions
verified unchanged against round10-fixed.json. Results remain separate from the
active fit; do not rerun compare_models.py as if Round 10 were training data without
explicitly identifying that change.

- Revision E: **13/20**; near-tie: **16/20**.
- Nine wide diagnostic pairs: both **8/9**.
- Eleven smaller-gap pairs: E **5/11**; near-tie **8/11**.
- Eight actual ties: E recognized 2; near-tie recognized 7. Near-tie also softened
  two actual very-slight preferences (Q2 and Q13) to ties. Both falsely picked A
  on actual tie Q5. Neither model's strength predictions were calibrated/scored.
- Both reversed Q10: West Central Asia, A pale/straw/35-year/125 lb versus B
  brown/25-year/115 lb; Stefan chose B very slightly. The combined shade-age-tare
  trade-off is not captured; this pair alone cannot isolate which effect is wrong.
- Matched wide contrasts: Q1/Q6 (Eastern Europe, 20 years/130 lb versus
  40 years/110 lb) both favored A moderately at pale/straw and brown. Q12/Q17
  (central, 20 years/125 lb versus 35 years/115 lb) favored A overwhelmingly at
  pale/straw and strongly at brown. Direction agrees across shades; the latter
  intensity difference is a tentative clue, not a measured interaction coefficient.

This prospective check supports the near-tie prediction layer, especially around
close choices. It does not establish 80% population accuracy: the 20 pairs were
purposefully selected, and nine widened pairs were easier for both models. Keep
wide and smaller-gap results separate. Preserve the all-119 near-tie candidate and
E unchanged; no production replacement or refit performed.

Recommended follow-up: isolate the Q10 trade-off by changing only age, shade, or
tare across matched wider pairs; separately inspect Q2/Q13 small-preference misses
before changing the tie band. Preserve Stefan's wider-difference diagnostic method
without allowing easy anchors to inflate claims about boundary accuracy.

## Latest work — model structure comparison complete; production E unchanged

Read README's experimental-model section and model-comparison.json. Reproducible
script: compare_models.py; tests: test_compare_models.py. No evidence answers or
production coefficients changed. Pricing.py's SHA-256 is preserved in the result.

Two 18-coefficient additive candidates: exact-tie sign classifier versus a learned
near-tie band; ridge fit with nonnegative shade/age/tare increments, free zone
offsets, no interactions. Both use identical features. The near-tie band predicts
user judgments; it must not silently redefine exact equality in the evidence or
be represented as calibrated uncertainty or a monetary tolerance.

101 old active + 18 Round 9 answered = 119 observations. Five repeats of nested
five-fold grouped validation (inner three folds), grouping provenance/shade pair
families across ages/tares, gave mean accuracy 52.9% exact / 62.7% near-tie and
balanced accuracy 48.7% / 63.1%. Near-tie improved all five repeats; split accuracy
range 56.3–70.6% is NOT a confidence interval. Opposite-winner errors averaged
23.0 / 10.2 per 119. Near-tie overcalls ties (46.4 predicted vs 33 observed).

Pre-Round-9-only training gave retrospective Round 9 scores 7/18 exact, 13/18
near-tie, 5/18 frozen E; always-tie baseline 8/18. Round 9 was already known during
experimental design, so do not promote 13/18 to fresh independent validation.
All-119 fitted candidates match 76/119 and 90/119 in-sample and flatten some
shade/vintage steps. They are experimental predictors, not replacement pricing.

Recommended next action: a new frozen comparison of E and the all-119 near-tie
candidate, with unseen, preselected varied pairs. Freeze both models and predictions
before elicitation. Exclude deferred pairs from BOTH comparisons.json and
round9-fixed.json. Do not replace E without considering the missing interactions,
collapsed steps, and tie overprediction. No fixed numerical mapping for verbal
strengths was introduced. No Git repository exists here; changes remain local.

## Round 9 — frozen prediction check COMPLETE; no refit

Question 19 was explicitly changed from tie to **save for later**; the prior tie
is superseded within round9-fixed.json, not usable as a fitting constraint.
Question 20 is **tie**. Questions 1 and 19 are deferred; 18 were answered.

Revision E matched **5/18 (27.8%)** exact A/B/tie outcomes: questions 9–13.
Of 13 mismatches, 5 reversed an A/B preference, 6 predicted a strict preference
where Stefan tied, and 2 predicted a tie where Stefan preferred B. Qualitative
strengths were not scored. The model hash matches its pre-round SHA-256; no
coefficients, question selection, or predictions changed during the round.

All round evidence, predictions, scoring, and question 19 correction history are
in `round9-fixed.json`, separate from the 101 previously fitted comparisons.
This is a preselected varied sample, not a random population accuracy estimate.
Seven prior-model deferrals plus subsequent rounds are already tracked separately;
the canonical fitted ledger has 10 deferred pairs, while Round 9 adds 2 held-out
deferrals (12 unique deferred pairs across both files). Do not re-ask either file's
saved pairs when proposing fresh questions.

**Next work:** assess model structure before another hand-tuned refit. Perfect
agreement on fitted pairs has not transferred to this frozen set. Compare simpler
regularized models and an explicit near-tie model without silently redefining
user ties; preserve user corrections and distinguish exploratory reuse of Round 9
from a future untouched evaluation. Revision E remains unchanged. Round 9 answers
have not yet been incorporated into pricing.py or the active fit ledger.

## Current state — revision E implemented, 2026-10-26

Round 8 completed with 17 answers and three deferrals. All **101 active rankings
and exact ties** pass; **10 saved pairs** and **2 superseded answers** are excluded.
No unanswered or pending-fit entries remain. Revision D matched **6/17** answers;
its predictions were recorded before each answer in comparisons.json. These were
adaptive gap probes, not a random evaluation or calibrated accuracy estimate.

### Latest fitted relationships

- Copper/30-year/120 lb: southeast = southwest = northeast > northwest = central.
- West Central Asia > South/Eastern Asia at copper and golden, but equal at brown,
  in the tested 30-year/120 lb pairs. Qualified tie/lean wording is retained.
- Eastern Europe versus West Central Asia at copper: a 5 lb disadvantage still
  wins at 20 and 30 years; a 10 lb disadvantage loses at 30 years. The 20-year
  10 lb pair remains saved. Chosen coefficients are provisional, not measurements.
- Both Asian provenances' tested copper 40-to-35 and 30-to-25 premiums beat 5 lb.
- Southwest = northeast at brown/30-year/120 lb. Southeast versus southwest at
  that offering was saved, so do not present any model ranking as a user answer.
- The copper coefficients were adjusted jointly, including Western Europe, to
  preserve all previous active preferences and monotone shade ordering. Numeric
  offsets and transfer to untested ages/tares remain provisional assumptions.

All 1,250 supported offerings pass bounds and adjacent monotonicity checks. Model
extrema remain unchanged from D. No dollar anchors were set. Qualitative intensity
is preserved in the data but not validated as a numerical scale. No Git repository
exists here, so the changes are local and uncommitted.

### Saved and superseded evidence

Saved: Round 5 Q1; revision Q12/Q15; Round 6 Q13; Round 7 Q2/Q17/Q18;
Round 8 Q9/Q14/Q16. Do not re-ask or probe around these unless Stefan wants to.
Superseded: Round 5 Q8 by revision Q13; Round 4 Q10 by Round 7 Q1.

### Next targets

Prefer a diverse frozen prediction check with a small preselected set spanning
unmeasured regions, before more adaptive fitting. Keep predictions hidden during
answers; report pre-fit results separately. Further fitted agreement should not
be described as predictive improvement. Numerical margin calibration, uncertain
or repeated judgments, and generalization deserve attention alongside new cells.

The revision D section below is historical; this section owns current counts.

## Historical state — revision D implemented, 2026-10-26

**Read this section before historical model descriptions below.** `pricing.py`
checks **84 active comparisons** in comparisons.json. README and spec.json describe
the current model. Round 7 is complete: 17 answers (including one explicit revisit)
and three saved. Revision C matched **5/17** before refitting; predictions are
retained on each answered Round 7 row. This is not a random held-out evaluation.

- Round 7 question 1 explicitly replaces the earlier central/brown/30-year B
  answer with **A, moderately**. The old exception is removed. Central beats
  West Asia / Middle East at all five tested vintages.
- Revision question 13 previously replaced Round 5 question 8 with **A slightly**.
  Both superseded answers remain in the history but are excluded from fitting.
- Seven saved pairs: Round 5 question 1; revision questions 12 and 15; Round 6
  question 13; Round 7 questions 2, 17, 18. Do not probe around saved pairs unless
  Stefan wants to revisit them. Deferred is not equal pricing.
- Pale/straw at 40 years, 120 lb: southeast = southwest = northeast > northwest
  = central. At 20 years, southeast beats northeast at 110/115 lb but ties at
  120/125/130 lb. The model has a narrow provenance/shade/age/tare interaction;
  it no longer assumes that provenance premiums are independent of tare.
- Golden at 20 years, 120 lb: southeast = southwest = northeast > northwest
  = central. Southeast > Western Europe; northwest versus Western Europe is
  saved. Do not present that saved relationship as elicited.
- Western Europe golden/20-year at 125 lb ties Eastern Europe at 120 lb. Joint
  European golden/20-year adjustments fit this relative premium while preserving
  earlier vintage rankings and monotonic ordering. Absolute offsets are provisional.
- Coefficients are one feasible calibration; numeric verbal margins are NOT
  measured. “Slightly” is retained qualitatively, not validated as a fixed scale.
- Every supported combination is checked for index bounds and adjacent lighter
  tare, younger age, and lighter shade ordering. These monotonic rules remain
  modeling assumptions rather than thousands of independently elicited answers.
- Model extrema are unchanged from C: floor = West Asia / Middle East and
  South/Eastern Asia at brown/40-year/130 lb; ceiling = southeast and southwest
  at pale-straw/20-year/110 lb. They are provisional global model consequences.
- No Git repository exists here; local changes have not been committed.

### Next revision targets

Prefer a diverse fresh prediction check before adding more coefficients. Sample
unmeasured shades, ages, and provenance pairings; report pre-fit matches separately
from fit consistency. The 20-year pale/straw tare boundary is measured only for
southeast versus northeast. Do not generalize it globally. Calibrate verbal price
margins and price anchors separately if Stefan wants actual price estimates.

Historical counts, equations, and “not fitted yet” notes below describe their
original rounds; this section supersedes them.

## How to run a round

1. Read this file and `pricing.py`. Run `python3 -c "from pricing import check_anchors; check_anchors()"`.
2. Ask for 5 or 10 new pairs. Do not repeat a pair already in the log below.
3. Label every option **A** and **B**. Put tare, provenance, shade, and vintage on both sides. Offer A, B, tie, or save for later. Save for later defers the pair; it is not a tie or a pricing constraint.
4. Do not reveal what the calculator picks. Do not argue the pair.
5. After the answers, score each one. A coin flip means a tie: record what Stefan says would break it.
6. Change `pricing.py`, the pricing section of `README.md`, and `spec.json` only for a rule he confirmed. Do not silently reverse an earlier explicit ranking.
7. Add the new pairs to the log in this file, rerun `check_anchors()`, and leave the next targets updated.

He writes "providence" for provenance. Use provenance in the files. He wants A/B, not a prose choice.

## Offering

Every stainless vessel carries every shade, every vintage, and every zone.

Shades, listed light to dark: pale/straw, golden, amber, copper, brown.

Vintages: 20, 25, 30, 35, 40 years.

Domestic zones: northwest, southwest, northeast, southeast, central.

Foreign zones: Western Europe, Eastern Europe, West Central Asia, South/Eastern Asia, West Asia / Middle East.

Tares: 110, 115, 120, 125, 130 lb. Lighter is more expensive.

## Calculator

`quote(provenance, shade, vintage_years, weight_lb)` in `pricing.py`.

One point is 5 lb of tare, one shade step, or 5 years. Lighter scores higher.

```
u = shade + vintage + origin(zone, shade) + lightness
t = (u - u_floor) / (u_ceiling - u_floor)
price = P_floor × (P_ceiling / P_floor)^t
```

Floor, t = 0: 130 lb, brown, 40 year, West Asia / Middle East.
Ceiling, t = 1: 110 lb, any domestic zone, pale/straw, 20 year.
Dollar amounts are not set. Pass `p_floor` and `p_ceiling` only as an illustration.

Origin, in points relative to Eastern Europe:

| Zone | Points | Status |
|---|---|---|
| Western Europe | 3 | Identified. 15 lb above Eastern Europe. |
| Eastern Europe | 0 | Reference. Ties central at amber. |
| West Central Asia | −1/6 | Just under Eastern Europe. He ranked EE above it. |
| South/Eastern Asia | −0.5 | Ties West Asia / Middle East. |
| West Asia / Middle East | −0.5 | Same. Shade breaks the tie. |
| Domestic, pale/straw | 4 | All five zones equal, one point above Western Europe. |
| Domestic, amber and darker | see below | Spread. Copper and brown reuse the amber gaps. |

Amber domestic points are one fit, not a unique measurement: southeast 2, southwest 1.25, northwest 1, northeast 0.5, central 0. Above amber, a zone rises linearly toward 4 at pale/straw.

`check_anchors()` encodes the 15 fitted comparisons plus this foreign order. It does not encode the open round.

## Open, do not treat as fitted

These answers are real. They are not in the calculator yet.

| Held fixed | Pair | He said | Calculator | What it would change |
|---|---|---|---|---|
| central, amber | A 110 lb, 40 year / B 130 lb, 20 year | B | tie | 20 years of youth beats 20 lb of tare. Vintage steps are larger than tare steps. |
| Eastern Europe, 120 lb | A golden, 30 year / B amber, 25 year | B | tie | One 5-year step beats one shade step from amber to golden. |
| 120 lb, pale/straw, 30 year | A southeast / B northwest | A | tie | Domestic zones do not meet at pale/straw. Southeast stays above northwest. |
| 130 lb, 30 year | A northwest, golden / B Western Europe, golden | A | B | Northwest is already above Western Europe at golden. The crossover is earlier than pale/straw. |
| 130 lb, 30 year | A northwest, copper / B Western Europe, copper | A | B | Northwest is also above Western Europe at copper. At amber, Western Europe is above northwest. The relationship is not a smooth rise with shade. |
| amber, 30 year | A 120 lb southeast / B 115 lb northwest | A | tie | The southeast–northwest gap is more than 5 lb. |
| 120 lb, brown, 30 year | A central / B West Asia / Middle East | B | A | At brown, West Asia / Middle East beats central. |

Question received as B, then corrected: 120 lb amber 30 year, South/Eastern Asia vs West Asia / Middle East, is a coin flip. Shade decides it. That tie is already in the calculator.

Do not smooth the copper/amber/golden northwest result into a straight line unless a later round supports it. Ask around that kink on purpose.

## Comparison log

Winner is what Stefan said. Model is what `pricing.py` says now.

### Round 1 — amber, 30 year

| # | A | B | Winner | Model |
|---|---|---|---|---|
| 1 | 115 lb northeast | 110 lb southwest | B | B |
| 2 | 120 lb southwest | 110 lb central | B | B |
| 3 | 120 lb northeast | 125 lb northwest | A | A |
| 4 | 110 lb northeast | 120 lb northeast | A | A |
| 5 | 115 lb Eastern Europe | 115 lb central | tie | tie |

### Round 2 — amber, 30 year

| # | A | B | Winner | Model |
|---|---|---|---|---|
| 1 | 120 lb Western Europe | 120 lb West Asia / Middle East | A | A |
| 2 | 130 lb northwest | 130 lb Western Europe | B | B |
| 3 | 110 lb West Asia / Middle East | 130 lb Western Europe | A | A |
| 4 | 110 lb Eastern Europe | 125 lb Western Europe | tie | tie |
| 5 | 115 lb southeast | 115 lb northwest | A | A |

### Round 3 — vintage 30 year, shade moves

| # | A | B | Winner | Model |
|---|---|---|---|---|
| 1 | 120 lb northwest pale/straw | 120 lb northwest brown | A | A |
| 2 | 130 lb northwest pale/straw | 130 lb Western Europe pale/straw | A | A |
| 3 | 110 lb West Asia / Middle East brown | 130 lb Western Europe pale/straw | B | B |
| 4 | 120 lb West Asia / Middle East pale/straw | 120 lb Western Europe brown | A | A |
| 5 | 115 lb southeast brown | 115 lb northwest pale/straw | B | B |

### Round 4 — vintage and middle shades

| # | A | B | Winner | Model |
|---|---|---|---|---|
| 1 | 120 lb central amber 20 year | 120 lb central amber 40 year | A | A |
| 2 | 110 lb central amber 40 year | 130 lb central amber 20 year | B | tie |
| 3 | 120 lb Eastern Europe golden 30 year | 120 lb Eastern Europe amber 25 year | B | tie |
| 4 | 120 lb Eastern Europe amber 30 year | 120 lb West Central Asia amber 30 year | A | A |
| 5 | 120 lb South/Eastern Asia amber 30 year | 120 lb West Asia / Middle East amber 30 year | coin flip, shade decides | tie |
| 6 | 120 lb southeast pale/straw 30 year | 120 lb northwest pale/straw 30 year | A | tie |
| 7 | 130 lb northwest golden 30 year | 130 lb Western Europe golden 30 year | A | B |
| 8 | 130 lb northwest copper 30 year | 130 lb Western Europe copper 30 year | A | B |
| 9 | 120 lb southeast amber 30 year | 115 lb northwest amber 30 year | A | tie |
| 10 | 120 lb central brown 30 year | 120 lb West Asia / Middle East brown 30 year | B | A |

### Round 5 — interactive refinement (2026-10-26, complete)

Response options: **A, B, tie, or save for later**. Deferred pairs remain unanswered and must not be fitted.

| # | A | B | Winner | Status |
|---|---|---|---|---|
| 1 | 115 lb domestic central amber 30 year | 125 lb domestic central amber 25 year | — | Save for later |
| 2 | 120 lb domestic central copper 30 year | 120 lb West Asia / Middle East copper 30 year | A | Recorded; evaluate with completed round |
| 3 | 120 lb domestic southeast brown 30 year | 120 lb domestic northwest brown 30 year | tie | Recorded; evaluate with completed round; no tie-breaker specified |
| 4 | 120 lb West Central Asia amber 30 year | 120 lb South/Eastern Asia amber 30 year | tie, leaning B | Soft preference only; not a firm B ranking; evaluate with completed round |
| 5 | 130 lb domestic northwest amber 25 year | 130 lb Western Europe amber 25 year | A | Recorded; evaluate with completed round; preserve earlier 30-year B ranking |
| 6 | 130 lb domestic northwest amber 35 year | 130 lb Western Europe amber 35 year | tie, leaning B | Soft preference only; not a firm B ranking; evaluate with completed round |
| 7 | 120 lb Eastern Europe copper 30 year | 120 lb Eastern Europe brown 25 year | A | Recorded; evaluate with completed round |
| 8 | 120 lb Eastern Europe pale/straw 30 year | 120 lb Eastern Europe golden 25 year | tie, leaning heavily B | Strong soft preference; not a firm B ranking; evaluate with completed round |
| 9 | 120 lb domestic southeast pale/straw 30 year | 115 lb domestic northwest pale/straw 30 year | tie, leaning B | Soft preference only; not a firm B ranking; evaluate with completed round |
| 10 | 120 lb domestic central golden 30 year | 120 lb West Asia / Middle East golden 30 year | A | Recorded; agrees with existing model |

## Round 5 assessment — not fitted yet

Current calculator outcomes for questions 1–10: A, A, A, A, B, B, tie, tie, B, A.
Question 1 is deferred and unscored. Of five firm answers (2, 3, 5, 7, 10),
two agree with the model (2, 10); three disagree (3, 5, 7).
Questions 4, 6, 8, 9 are qualified ties: preserve the lean and its strength,
not a hard equality or strict ranking. No numerical near-tie tolerance has been elicited.

Confirmed constraints for the next fit:
- At 120 lb, brown, 30 years, southeast and northwest tie. Their amber gap cannot simply carry into brown.
- At 130 lb, amber, 25 years, northwest beats Western Europe. Preserve the earlier opposite ranking at 30 years; origin must interact with vintage if both judgments stand.
- At 120 lb Eastern Europe, copper 30-year beats brown 25-year. Preserve the earlier amber 25-year over golden 30-year: a uniform shade-step value is insufficient with the current additive vintage model.
- Central beats West Asia / Middle East at copper and golden, 120 lb, 30 years. Preserve its earlier loss at brown.

No calculator coefficients changed in this elicitation round. Existing anchor checks pass,
but they do not validate the open Round 4 or Round 5 constraints. A future fit must
explicitly replace obsolete structural assumptions (domestic pale equality, fixed foreign
order across contexts, and shade-independent vintage effects) without silently reversing
observed firm pair rankings. Avoid inventing precise coefficients from ordinal answers.

## Next targets

- Revisit deferred Round 5 question 1 only when Stefan wants saved questions.
- Bound the northwest/Western Europe amber vintage crossover between 25 and 30 years using allowed offerings; the 35-year answer is a tie leaning B, not a strict B.
- Bound the copper–brown shade premium against a larger vintage difference.
- Determine whether the southeast/northwest brown tie persists at other vintages.
- Clarify how qualified ties should affect fitting: near-equality plus a directional preference; preserve “heavily” as distinct from an ordinary lean.
- Probe central against West Asia / Middle East at other brown vintages to locate the reversal.
- Do not repeat answered pairs or treat saved pairs as ties.

## Revision interview — 2026-10-26 (in progress)

These clarifications supersede Round 5's provisional treatment of leaning answers.

1. Asked how to interpret “tie, leaning B”: Stefan chose **B**, meaning B should
   cost slightly more; “leaning heavily B” means a larger premium. An unqualified
   tie remains equal pricing. Apply this to recorded leaning answers. Exact premium
   sizes remain unmeasured; these are directional price constraints, not hard ties.
2. Gap calibration: compared the price gap between 115 lb and 120 lb domestic
   southeast, both pale/straw, 30 years, against the prior gap favoring 115 lb
   northwest over 120 lb southeast at the same shade/vintage. Stefan chose **A:
   about the same**. This is a comparison of gap sizes, NOT selection of vessel A
   (120 lb) as more expensive. Treat approximately, not as an exact equality:
   exact equality would imply southeast and northwest tie at 115 lb, conflicting
   with the earlier explicit southeast preference at equal tare (120 lb).

Calculator remains unchanged pending reconciliation and fit.

3. Amber, 30 years: A = 125 lb domestic southeast; B = 115 lb domestic
   northwest. Stefan chose **B, slightly to moderately**. Together with Round 4
   question 9 (120 lb southeast beats 115 lb northwest), this brackets the
   southeast premium between 5 and 10 lb under additive, monotone tare pricing.
   Preserve the qualitative strength; no exact numerical margin supplied.

4. Eastern Europe, 120 lb: A = copper, 35 years; B = brown, 25 years.
   Stefan chose **A, slightly more**. Copper's advantage outweighs this 10-year
   youth difference; exact margin remains unmeasured. Preserve Round 5 question
   7 (copper 30-year beats brown 25-year) as well.

5. Eastern Europe, 120 lb: A = copper, 40 years; B = brown, 25 years.
   Stefan chose **B, very slightly**. Together with revision question 4,
   the copper–brown crossover lies between the tested 10- and 15-year
   differences for this context. Do not assume uniform vintage steps or
   extrapolate this bracket to other provenances without evidence.

6. Eastern Europe, amber: A = 115 lb, 30 years; B = 120 lb, 25 years.
   Stefan chose **B, very slightly**. In this context the five-year youth
   advantage narrowly outweighs a 5 lb lightness advantage. Exact margin
   remains unmeasured; do not impose the same vintage increment everywhere.

7. Eastern Europe, amber: A = 115 lb, 40 years; B = 120 lb, 35 years.
   Stefan chose **tie** (equal price per the clarified response semantics).
   Here the 35-versus-40-year youth premium offsets 5 lb of lightness;
   the 25-versus-30-year premium in revision question 6 was slightly larger.

8. Eastern Europe, amber: A = 115 lb, 35 years; B = 120 lb, 30 years.
   Stefan chose **tie** (equal price). Together with revision question 7,
   both older five-year steps offset 5 lb of lightness in the tested pairs.
   Revision question 6 places the 25-versus-30-year premium slightly above that.

9. Eastern Europe, amber: A = 115 lb, 25 years; B = 120 lb, 20 years.
   Stefan chose **B, very slightly**. The 20-versus-25-year premium narrowly
   outweighs 5 lb of lightness, as does the tested 25-versus-30-year premium.
   These qualitative margins do not establish identical numerical increments.

10. Eastern Europe, 30 years: A = 120 lb golden; B = 115 lb amber.
    Stefan chose **B, very slightly**. The golden-over-amber premium is
    narrowly below the tested 5 lb lightness advantage. This supports the
    earlier amber 25-year over golden 30-year ranking without assuming
    equal shade steps.

11. Eastern Europe, 30 years: A = 120 lb pale/straw; B = 115 lb golden.
    Stefan chose **A, slightly**. Pale/straw's premium over golden exceeds
    the tested 5 lb lightness advantage. Preserve Round 5 question 8:
    golden 25-year beats pale/straw 30-year (leaning heavily B, clarified
    as a larger price premium). These directional constraints can coexist,
    but their qualitative margin strengths may require clarification before
    fitting common numeric meanings to “very slightly,” “slightly,” and “heavily.”

12. Eastern Europe, 30 years: A = 120 lb amber; B = 115 lb copper.
    Stefan said “that's a tough one,” then explicitly chose **save for later**.
    Deferred and unscored; not a tie or a directional pricing constraint.

13. Explicit revisit of Round 5 question 8: Eastern Europe, 120 lb:
    A = pale/straw, 30 years; B = golden, 25 years. Stefan chose
    **A, slightly**. This explicitly SUPERSEDES the earlier “tie, leaning
    heavily B” answer for that exact pair. Keep the old entry as history,
    exclude it from active fit constraints. The intermediate abstract
    model-choice question was not answered; do not infer a model preference.
14. Eastern Europe, 30 years: A = 125 lb pale/straw; B = 115 lb golden.
    Stefan chose **tie** (equal prices). This identifies the pale/straw-over-
    golden premium with the tested 10 lb tare difference. Under linear tare
    points it equals 2 points; linearity remains a modeling assumption.

15. Eastern Europe, 30 years: A = 125 lb amber; B = 115 lb copper.
    Stefan chose **save for later**. Deferred and unscored, alongside revision
    question 12. Neither supplies a tie or a directional price constraint.

16. Amber, 25 years: A = 125 lb domestic northwest; B = 120 lb Western
    Europe. Stefan chose **B, very slightly**. Together with Round 5 question
    5 (northwest wins at equal 130 lb), this brackets northwest's provenance
    premium above zero and below 5 lb under a tare-independent provenance
    model; the tested 5 lb difference narrowly outweighs it.

17. Amber, 20 years, 120 lb: A = domestic northwest; B = Western Europe.
    Stefan chose **tie** (equal prices). Preserve the distinct 25-year
    northwest preference and 30-year Western Europe preference. Do not
    impose a monotone provenance premium across vintages.

18. Amber, 40 years, 120 lb: A = domestic northwest; B = Western Europe.
    Stefan chose **B, very slightly**. The observed equal-tare amber pattern
    is now: 20 years tie; 25 years northwest wins; 30 years Western Europe
    wins; 35 years Western Europe slightly higher (clarified leaning answer);
    40 years Western Europe very slightly higher. Tares vary across these
    observations; transferring the pattern across tares is an assumption.

19. Domestic northwest, amber, 120 lb: A = 20 years; B = 25 years.
    Stefan chose **A, slightly**. Preserve this within-provenance age ranking
    when fitting the nonmonotone northwest-versus-Western-Europe premium;
    a changing relative provenance premium does not itself imply that
    northwest 25-year costs more than northwest 20-year.

20. Amber, 30 years: A = 115 lb West Central Asia; B = 120 lb South/Eastern
    Asia. Stefan chose **A, very slightly**. Together with Round 5 question 4,
    this places South/Eastern Asia's premium over West Central Asia below
    5 lb under linear tare pricing. Revision B uses a provisional 0.9-point
    premium, so A wins this test by 0.1 point. This is a chosen feasible
    magnitude, not a directly measured decimal value.

## Round 6 — 20 fresh comparisons (complete; revision C fitted)

All 19 answered pairs below are now active in comparisons.json; question 13 is
deferred. Their pre-fit revision B predictions are retained on the evidence rows.

| # | A | B | Answer |
|---|---|---|---|
| 1 | 110 lb domestic southeast pale/straw 20 year | 110 lb domestic southwest pale/straw 20 year | tie |
| 2 | 110 lb domestic southeast pale/straw 20 year | 110 lb domestic northeast pale/straw 20 year | A, very slightly |
| 3 | 110 lb domestic northeast pale/straw 20 year | 110 lb domestic central pale/straw 20 year | A, slightly |
| 4 | 110 lb domestic northwest pale/straw 20 year | 110 lb domestic northeast pale/straw 20 year | B, very slightly |
| 5 | 110 lb domestic northwest pale/straw 20 year | 110 lb domestic central pale/straw 20 year | tie |
| 6 | 130 lb domestic central brown 40 year | 130 lb West Asia / Middle East brown 40 year | A, very slightly |
| 7 | 120 lb domestic central brown 40 year | 120 lb West Asia / Middle East brown 40 year | A, slightly |
| 8 | 120 lb domestic central brown 35 year | 120 lb West Asia / Middle East brown 35 year | A, moderately |
| 9 | 120 lb domestic central brown 25 year | 120 lb West Asia / Middle East brown 25 year | A, moderately |
| 10 | 120 lb domestic central brown 20 year | 120 lb West Asia / Middle East brown 20 year | A, moderately |
| 11 | 125 lb domestic central brown 25 year | 120 lb West Asia / Middle East brown 25 year | A, very slightly |
| 12 | 130 lb domestic central brown 25 year | 120 lb West Asia / Middle East brown 25 year | A, very slightly |
| 13 | 130 lb domestic central brown 25 year | 115 lb West Asia / Middle East brown 25 year | save for later |
| 14 | 115 lb Western Europe golden 30 year | 120 lb Western Europe golden 25 year | B, very slightly |
| 15 | 115 lb Western Europe brown 30 year | 120 lb Western Europe brown 25 year | B, very slightly |
| 16 | 115 lb domestic southeast pale/straw 30 year | 120 lb domestic southeast pale/straw 25 year | B, very slightly |
| 17 | 115 lb domestic southeast pale/straw 40 year | 120 lb domestic southeast pale/straw 35 year | B, very slightly |
| 18 | 115 lb domestic southeast brown 40 year | 120 lb domestic southeast brown 35 year | B, very slightly |
| 19 | 115 lb domestic southeast amber 40 year | 120 lb domestic southeast amber 35 year | B, very slightly |
| 20 | 115 lb domestic southwest amber 40 year | 120 lb domestic southwest amber 35 year | B, very slightly |

### Round 6 fit receipt

Revision C passes 68 active comparisons across the full history. Four deferred
pairs and one superseded answer remain excluded. Only directions and exact ties
are hard checks; qualitative strengths are not numerically validated. All supported
combinations retain younger, lighter-shade, and lighter-tare ordering, with index
bounds and illustrative price endpoints checked. No actual price anchors were set.

## Round 7 — 20 refinement/clarification comparisons (complete; revision D fitted)

| # | A | B | Answer | Status |
|---|---|---|---|---|
| 1 | 120 lb domestic central brown 30 year | 120 lb West Asia / Middle East brown 30 year | A, moderately | Explicit correction; fitted D |
| 2 | 120 lb domestic central brown 30 year | 120 lb Eastern Europe brown 30 year | save for later | Deferred; excluded from fit |
| 3 | 120 lb domestic southeast pale/straw 40 year | 120 lb domestic southwest pale/straw 40 year | tie | Fitted D |
| 4 | 120 lb domestic southeast pale/straw 40 year | 120 lb domestic northeast pale/straw 40 year | tie | Fitted D |
| 5 | 120 lb domestic southeast pale/straw 40 year | 120 lb domestic northwest pale/straw 40 year | A, very slightly | Fitted D |
| 6 | 120 lb domestic northwest pale/straw 40 year | 120 lb domestic central pale/straw 40 year | tie | Fitted D |
| 7 | 130 lb domestic southeast pale/straw 20 year | 130 lb domestic northeast pale/straw 20 year | tie | Fitted D |
| 8 | 120 lb domestic southeast pale/straw 20 year | 120 lb domestic northeast pale/straw 20 year | tie | Fitted D |
| 9 | 115 lb domestic southeast pale/straw 20 year | 115 lb domestic northeast pale/straw 20 year | A, very slightly | Fitted D |
| 10 | 125 lb domestic southeast pale/straw 20 year | 125 lb domestic northeast pale/straw 20 year | tie | Fitted D |
| 11 | 130 lb domestic northeast pale/straw 20 year | 130 lb domestic northwest pale/straw 20 year | A, very slightly | Fitted D |
| 12 | 120 lb domestic southeast golden 20 year | 120 lb domestic southwest golden 20 year | tie | Fitted D |
| 13 | 120 lb domestic southeast golden 20 year | 120 lb domestic northeast golden 20 year | tie | Fitted D |
| 14 | 120 lb domestic northeast golden 20 year | 120 lb domestic northwest golden 20 year | A, very slightly | Fitted D |
| 15 | 120 lb domestic northwest golden 20 year | 120 lb domestic central golden 20 year | tie | Fitted D |
| 16 | 120 lb domestic southeast golden 20 year | 120 lb Western Europe golden 20 year | A, very slightly | Fitted D |
| 17 | 120 lb domestic northwest golden 20 year | 120 lb Western Europe golden 20 year | save for later | Deferred; excluded from fit |
| 18 | 120 lb South/Eastern Asia pale/straw 20 year | 120 lb West Asia / Middle East pale/straw 20 year | save for later | Deferred; excluded from fit |
| 19 | 120 lb Western Europe golden 20 year | 120 lb Eastern Europe golden 20 year | A, slightly | Fitted D |
| 20 | 125 lb Western Europe golden 20 year | 120 lb Eastern Europe golden 20 year | tie | Fitted D |

### Round 7 fit receipt

All 84 active rankings/ties pass; seven deferred pairs and two superseded answers
are excluded. All 1,250 supported combinations pass bounds and adjacent monotonic
ordering at every tare, including the new tare interaction. Exact tie prices and
illustrative endpoints are checked; no actual dollar endpoints were set. Numerical
intensity labels remain uncalibrated. Revision C matched 5/17 answers before fitting.

## Round 8 — gap and transfer checks (complete; revision E fitted)

Ask one question at a time, adaptively. No fixed count requested. Record model
predictions before answers and do not disclose them during elicitation. Mix
underrepresented provenance/shade combinations with transfer tests; avoid saved
pairs. All 17 answered comparisons are now active; three deferred pairs remain excluded.

| # | A | B | Answer | Status |
|---|---|---|---|---|
| 1 | 120 lb West Central Asia copper 30 year | 120 lb South/Eastern Asia copper 30 year | Tie to very slightly A | Fitted E; slight A preference under established lean semantics |
| 2 | 120 lb West Central Asia golden 30 year | 120 lb South/Eastern Asia golden 30 year | A, very slightly | Fitted E |
| 3 | 120 lb West Central Asia brown 30 year | 120 lb South/Eastern Asia brown 30 year | tie | Fitted E |
| 4 | 120 lb Eastern Europe copper 30 year | 120 lb West Central Asia copper 30 year | A, moderately | Fitted E |
| 5 | 125 lb Eastern Europe copper 30 year | 120 lb West Central Asia copper 30 year | A, very slightly | Fitted E |
| 6 | 130 lb Eastern Europe copper 30 year | 120 lb West Central Asia copper 30 year | B, very slightly | Fitted E |
| 7 | 120 lb Eastern Europe copper 20 year | 120 lb West Central Asia copper 20 year | A, slightly | Fitted E |
| 8 | 125 lb Eastern Europe copper 20 year | 120 lb West Central Asia copper 20 year | A, very slightly | Fitted E |
| 9 | 130 lb Eastern Europe copper 20 year | 120 lb West Central Asia copper 20 year | save for later | Deferred; excluded from fit |
| 10 | 120 lb domestic southwest copper 30 year | 120 lb domestic northeast copper 30 year | tie | Fitted E |
| 11 | 120 lb domestic southeast copper 30 year | 120 lb domestic southwest copper 30 year | tie | Fitted E |
| 12 | 120 lb domestic northeast copper 30 year | 120 lb domestic northwest copper 30 year | A, slightly | Fitted E |
| 13 | 120 lb domestic northwest copper 30 year | 120 lb domestic central copper 30 year | tie | Fitted E |
| 14 | 125 lb domestic northeast copper 30 year | 120 lb domestic northwest copper 30 year | save for later | Deferred; excluded from fit |
| 15 | 120 lb domestic southwest brown 30 year | 120 lb domestic northeast brown 30 year | tie | Fitted E |
| 16 | 120 lb domestic southeast brown 30 year | 120 lb domestic southwest brown 30 year | save for later | Deferred; excluded from fit |
| 17 | 115 lb West Central Asia copper 30 year | 120 lb West Central Asia copper 25 year | B, very slightly | Fitted E |
| 18 | 115 lb West Central Asia copper 40 year | 120 lb West Central Asia copper 35 year | B, very slightly | Fitted E |
| 19 | 115 lb South/Eastern Asia copper 40 year | 120 lb South/Eastern Asia copper 35 year | B, very slightly | Fitted E |
| 20 | 115 lb South/Eastern Asia copper 30 year | 120 lb South/Eastern Asia copper 25 year | B, very slightly | Fitted E |

### Round 8 validation receipt

101 active rankings/ties; 10 deferred and 2 superseded excluded. Revision D
predictions matched 6/17 answers before refit. All 1,250 offering combinations
pass bounds and monotonicity; exact tie prices and illustrative endpoint prices
verified. Strength labels remain qualitative. No pending answers remain.

Round 11 Q13 confirmed Q2: A overwhelmingly. Do not count the repeated answer
as independent evidence or map the qualitative labels to additive numbers.
Q14 now asks which of two single-factor changes adds more from the SAME baseline
(West Central Asia brown/35-year/125 lb): A shade to pale/straw, B age to 25 years.
The resulting endpoint comparison is stored with shared_reference and question_type;
models remain fixed. This identifies relative premiums without inferring magnitude
from the word overwhelmingly.

Round 11 Q14 answered B, “35 to 25 would add much more.” From the shared
brown/35-year/125 lb baseline, the ten-year vintage premium exceeds the full
brown-to-pale shade premium. This is an ordinal comparison of premiums; preserve
the verbatim strength rather than mapping it to a number. Q15 awaits an answer:
same shade change versus the smaller 35-to-30-year change, same baseline. Models
remain frozen; no refit or price update.

Round 11 Q15 answered A: “From 35 to 30 no. Brown to pale is much more valuable
if the vintage difference is over 30 and within 5 years.” Exact tested comparison
favors shade strongly in the user's wording; preserve broader statement without
assuming untested boundaries or global transfer. Q16 awaits: from brown/30-year/
125 lb, compare shade to pale versus vintage to 25 years. Both models fixed.

Round 11 Q16 answered A very slightly: from brown/30-year/125 lb, the shade
premium to pale narrowly exceeds the vintage premium to 25 years. Q17 awaits:
from brown/25-year/125 lb, compare shade to pale versus vintage to 20 years.
Both models remain frozen; no numerical intensity assumptions introduced.

Round 11 Q17 answered B for West Central Asia, strength unspecified: “For west
central Asia, the vintage is more valuable; however, domestically, this would
not be true.” Preserve the domestic qualification; do not assume it means strict
A rather than a tie for every zone. Q18 awaits the identical shared-reference
comparison for domestic central at 125 lb (brown/25 baseline; shade to pale vs
vintage to 20). Both models remain frozen.

Round 11 Q18 answered A, strength unspecified, for domestic central: shade to
pale adds more than vintage 25-to-20 at 125 lb. Q19 awaits the identical
comparison for domestic southeast. No automatic generalization to every zone;
both models remain frozen.

Round 11 Q19 answered A strongly for domestic southeast: shade premium exceeds
25-to-20-year vintage premium at 125 lb. Q20 awaits: return to West Central Asia,
compare full shade change versus 35-to-25 vintage change at 115 lb. This matches
Q14 at a different tare and connects to the original target. Models fixed.

Round 12 clarification Q1 explicitly confirms equal prices for southeast versus
northeast, pale/straw/20-year/120 lb (original round7-8). This is not uncertainty
and not an independent new training sample. Q2 awaits the same pair at 110 lb
(revisits round6-2), using the same four explicit price-order/uncertainty options.
All existing models and original evidence files remain unchanged.

Round 12 Q2 explicitly confirms A higher very slightly at 110 lb (southeast
versus northeast, pale/straw/20-year; original round6-2). Together with Q1's
exact equality at 120 lb, this confirms tare dependence rather than mere wording
ambiguity in those two judgments. Q3 awaits 115 lb, revisiting round7-9.
Both confirmations remain separate from training to avoid double-counting.

Round 12 Q5 confirms B higher for West Central Asia pale/straw/35-year/125 lb
versus brown/25-year/125 lb (round11-14 direction). No new strength supplied and
no independent training sample added. Q6 awaits the original target with B at
115 lb (round10-10), using concrete price instructions. All models unchanged.

Round 12 Q6 explicitly confirms B for original round10-10. The copied option
phrase “even if only a little” is not a separate numerical strength judgment.
Q7 awaits round9-6: domestic northwest golden/40-year/115 lb versus pale-straw/
40-year/125 lb, direct price instructions. Preserve all baseline hashes and
apply recorded overrides before any future fit; repeated confirmations are not
independent samples.

Round 12 Q7 confirms A very slightly for round9-6. Q8 awaits round9-7: domestic
central brown/35-year/125 lb versus West Asia / Middle East brown/35-year/120 lb.
All existing models remain unchanged; retain the two recorded overrides for
future reconciled fitting and avoid double-counting confirmations.

Round 12 Q8 confirms A very slightly for round9-7. Q9 awaits round9-4: Western
Europe brown/25-year/130 lb versus Eastern Europe brown/25-year/115 lb.
All existing models remain unchanged; confirmations are not new independent
training observations.

Round 12 Q9 confirms B slightly for round9-4. Q10 awaits round9-8: domestic
southeast amber/20-year/125 lb versus southwest amber/20-year/115 lb.
Baseline models remain unchanged; repeated answers are not independent samples.

Round 12 Q10 confirms B moderately for round9-8. Q11 awaits round9-14: West
Asia / Middle East copper/25-year/120 lb versus Eastern Europe copper/25-year/
125 lb. Baseline models remain unchanged; repeated answers are not new samples.

Round 12 Q11 confirms B very slightly for round9-14. Q12 awaits round9-17:
domestic central golden/25-year/125 lb versus copper/20-year/115 lb. All baseline
model hashes remain unchanged; repeated confirmations are not new samples.

Round 12 Q12 confirms B moderately for round9-17. Q13 awaits round9-18:
domestic southeast pale/straw/25-year/130 lb versus golden/25-year/120 lb, using
explicit price instructions to distinguish equal pricing from uncertainty.
All baseline models remain unchanged.

Round 12 Q13 explicitly confirms equal prices for round9-18 (southeast pale/
25-year/130 lb versus golden/25-year/120 lb). Q14 awaits round9-5: West Central
Asia versus South/Eastern Asia, both copper/35-year/120 lb. Baseline models and
historical evidence remain unchanged; repeats do not add independent samples.

Round 12 Q14 explicitly confirms equal prices for round9-5 (West Central Asia
versus South/Eastern Asia, copper/35-year/120 lb). Q15 awaits round9-16: same
provenance pair, brown/35-year/120 lb. Models unchanged; confirmations are not
independent training samples.

Round 14 Q2: B higher “very very slightly” for southeast copper/35-year 125 lb
versus 120 lb. Q1 established southeast120 = southwest120. This conflicts with
the original exact tie in round13-6 under a single transitive price ordering.
Do not silently change any answer. Q3 explicitly rechecks round13-6 using the
price-order options. Both models remain frozen; repeat is not fresh validation.

Round 14 Q3 explicitly corrects round13-6 from tie to B “very, very slightly.”
Store as override for future reconciliation; do not rewrite the frozen score or
fit it yet. First miss isolated as tiny tare effect with equal provenances at
120 lb in this context. Q4 starts second miss (round13-9): northwest versus
Western Europe, both amber/40-year/125 lb, isolating provenance. Models fixed.

Round 14 Q4: Western Europe higher very slightly than northwest, both amber/
40-year/125 lb. Q5 awaits northwest120 versus northwest125, amber/40-year,
isolating tare for the second target. Both models remain frozen.

Round 14 Q5: northwest120 higher very slightly than northwest125 at amber/40
years. Q6 explicitly rechecks original round13-9 (northwest120 vs Western
Europe125). Q4 and Q5 both had very slight advantages; identical wording does
not prove equal magnitudes. Ask directly; do not infer or change original tie.
Models remain unchanged.

Round 14 Q6 explicitly confirms original round13-9 exact tie. The component
provenance and lightness advantages offset at amber/40-year in this pair; this
is a calibrated equality, not merely two similar adjectives. Q7 begins third
target round13-20: southeast golden versus pale/straw, both 35 years and 120 lb.
This isolates shade before varying vintage. Both models remain frozen.

Round 14 Q7: B higher very slightly (pale/straw over golden), southeast/35-year/
120 lb. Q8 awaits golden30 versus golden35, southeast/120 lb, isolating vintage
for the third target. All model hashes remain unchanged.

Round 14 Q8: A higher very slightly for southeast golden30 versus golden35 at
120 lb. Q9 explicitly rechecks original round13-20 (golden30 versus pale35 at
120 lb). Both individual premiums were very slight; do not infer their ordering
from adjectives. Await direct original-pair answer. Models remain frozen.

Round 16 Q2: exact equality for southeast115 versus southeast120, brown/40-year.
Together with Q1's southeast120=central120 this is consistent with original
round15-4's tie. Do not convert explicit equality to uncertainty or infer all
tares tie. Q3 widens to southeast115 versus southeast130, same shade/age.
Models remain frozen; finish this diagnosis then second miss then 15 queued
unresolved pairs.

Round 16 Q3: southeast115 higher slightly than southeast130 at brown/40-year.
Q4 awaits southeast115 versus southeast125, same shade/age, to locate the tare
premium between the confirmed 5 lb tie and 15 lb preference. Models unchanged.

Round 16 Q4: southeast115 higher very slightly than southeast125 at brown/
40-year. First target's tie is consistent with local 115=120 equality and
southeast120=central120; 125 and 130 are lower than 115. Do not generalize this
plateau across contexts. Q5 begins second target round15-14: southwest versus
southeast, both pale/straw/30-year/115 lb. Then proceed to all queued unresolved
pairs after the second target is isolated. Both models remain unchanged.

Round 16 Q5: southwest115 exactly equals southeast115, pale/straw/30-year.
Q6 awaits southwest110 versus southwest115 at the same shade/age, isolating
tare for second target round15-14. Models remain fixed.

Round 16 Q6: southwest110 exactly equals southwest115, pale/straw/30-year.
Together with Q5 this supports original round15-14's exact tie. Q7 widens to
southwest110 versus southwest130, same shade/age; do not infer a global flat
tare effect. Models remain fixed; unresolved queue follows this target.

Round 16 Q7: southwest110 higher slightly than southwest130, pale/straw/30-year.
Q8 awaits southwest110 versus southwest120, same shade/age, checking the
intermediate 10 lb difference before unresolved review. Models remain fixed.

Round 16 Q8: southwest110 higher very slightly than southwest120, pale/straw/
30-year. Both original misses are now consistent with context-specific equalities
for the tested 5 lb differences, plus strict preferences at wider differences.
No universal tare threshold inferred; no model updates. Phase moves to unresolved
review: 15 pairs queued. Q9 revisits r5-1 (central amber30/115 lb versus amber25/
125 lb), originally saved. Record resolution separately; no silent training update.

Round 16 Q9 resolves r5-1 as B very slightly (central amber25/125 lb over
amber30/115 lb). Resolution is in this round's queue; historical saved entry and
training snapshots remain unchanged. Q10 revisits revision-12, the saved Eastern
Europe amber120 versus copper115, both 30 years. Unresolved review: 1/15 resolved.
Both models remain fixed.

Round 16 Q10 resolves revision-12 as exactly equal: Eastern Europe amber120
versus copper115, both 30 years. Q11 revisits revision-15: amber125 versus
copper115, same provenance/age. Unresolved review: 2/15 resolved. Source
ledgers, evidence snapshots, and model hashes remain unchanged.

Round 16 Q11 resolves revision-15 as B very slightly: Eastern Europe copper115
over amber125 at 30 years. Q12 revisits round13-14, next saved pair.
Unresolved review: 3/15 resolved. Both models and source ledgers remain unchanged.

Round 16 Q12 resolves round13-14 as A very slightly: Western Europe golden
20-year/130 lb over 30-year/115 lb. Q13 revisits round15-3.
Unresolved review: 4/15 resolved. Models, frozen scores, and source ledgers unchanged.

Round 16 Q13 resolves round15-3 as exactly equal: Eastern Europe amber25/120 lb
versus Western Europe amber25/130 lb. Q14 revisits round15-9.
Unresolved review: 5/15 resolved. All baseline model hashes remain unchanged.

Round 16 Q14 resolves round15-9 as B very slightly: southwest amber35/120 lb
over southeast amber35/130 lb. Q15 revisits round6-13. Unresolved
review: 6/15 resolved. Models and historical scoring receipts remain unchanged.

Round 16 Q15 resolves round6-13 as B very slightly: West Asia / Middle East
brown25/115 lb over central brown25/130 lb. Q16 revisits round7-17.
Unresolved review: 7/15 resolved. Both models and original evidence unchanged.

Round 16 Q16 resolves round7-17 as exactly equal: northwest versus Western
Europe, golden/20-year/120 lb. Q17 revisits round7-18. Unresolved
review: 8/15 resolved. Models and historical scoring receipts remain unchanged.

Round 16 Q17 resolves round7-18 as exactly equal: South/Eastern Asia versus
West Asia / Middle East, pale/straw/20-year/120 lb. Q18 revisits round7-2.
Unresolved review: 9/15 resolved. Both models and original evidence remain unchanged.

Round 16 Q18 resolves round7-2 as exactly equal: domestic central versus Eastern
Europe, brown/30-year/120 lb. Q19 revisits round8-14. Unresolved
review: 10/15 resolved. Models and historical scoring receipts remain unchanged.

Round 16 Q19 resolves round8-14 as exactly equal: northeast copper30/125 lb
versus northwest copper30/120 lb. Q20 revisits round8-16. Unresolved
review: 11/15 resolved. Models and original source ledgers remain unchanged.

Round 16 Q20 resolves round8-16 as exactly equal: southeast versus southwest,
brown/30-year/120 lb. Q21 revisits round8-9. Unresolved review:
12/15 resolved. Both models and historical source evidence remain unchanged.

Round 16 Q21 resolves round8-9 as B very slightly: West Central Asia copper20/
120 lb over Eastern Europe copper20/130 lb. Q22 revisits round9-1.
Unresolved review: 13/15 resolved. Models and historical scoring receipts unchanged.

Round 16 Q22 resolves round9-1 as exactly equal: southwest amber25/120 lb versus
central amber25/115 lb. Q23 revisits final queued pair round9-19.
Unresolved review: 14/15 resolved. Models and original source ledgers unchanged.

Round 18 Q1: Western Europe higher very slightly than Eastern Europe, both
amber/20-year/125 lb. Q2 awaits Eastern Europe115 versus Eastern Europe125,
same shade/age, isolating the first target's tare difference. Models fixed.

Round 18 Q2: Eastern Europe115 higher very slightly than Eastern Europe125 at
amber/20-year. Q3 explicitly rechecks original round17-3: Western Europe125
versus Eastern Europe115. Do not infer equal magnitudes from similar strength
words; await direct pricing instruction. Both models remain frozen.

Round 18 Q3 confirms original round17-3 exact equality; first miss resolved as
a matched provenance/tare trade-off, no correction. Q4 begins round17-13:
northeast versus southwest, both brown/30-year/125 lb, isolating provenance.
All baseline models and original frozen-test scores remain unchanged.

Round 18 Q4: northeast125 exactly equals southwest125, brown/30-year.
Q5 awaits southwest120 versus southwest125, same shade/age, isolating tare
for second target round17-13. Both models remain fixed.

Round 18 Q5: southwest120 exactly equals southwest125 at brown/30-year.
Together with Q4, this is consistent with the original round17-13 tie.
Q6 widens to southwest120 versus southwest130, same shade/age; no global
tare threshold inferred. Models remain fixed.

Round 18 Q6: southwest120 higher very slightly than southwest130 at brown/
30-year. Combined with Q4/Q5, original round17-13 tie is consistent with the
isolated component answers. Q7 begins third target: northwest versus Western
Europe, both golden/35-year/125 lb. Both models remain fixed.

Round 18 Q7: northwest125 exactly equals Western Europe125, golden/35-year.
Q8 awaits northwest120 versus northwest125, same shade/age, isolating tare for
third target round17-15. Both models and frozen scores remain unchanged.

Round 18 Q8: northwest120 exactly equals northwest125 at golden/35-year.
Together with Q7, this supports original round17-15's exact tie. Q9 widens
to northwest120 versus northwest130, same shade/age. Models remain fixed.

Round 20 Q1: southwest125 exactly equals southeast125, pale/straw/20-year.
Q2 awaits southwest120 versus southwest125, same shade/age, isolating tare
for first target round19-14. Both model hashes remain unchanged.

Round 20 Q2: southwest120 exactly equals southwest125, pale/straw/20-year.
Together with Q1 this supports original round19-14's exact tie. Q3 widens
to southwest120 versus southwest130, same shade/age. Models remain fixed.

Round 20 Q3: southwest120 higher very slightly than southwest130, pale/straw/
20-year. Q1/Q2 support the first original tie; no correction or global threshold
inferred. Q4 begins second target: Western Europe versus central, both golden/
40-year/120 lb, isolating provenance. Models remain fixed.

Round 20 Q4: Western Europe120 exactly equals central120 at golden/40-year.
Q5 awaits central115 versus central120, same shade/age, isolating tare for
second target round19-15. All baseline model hashes remain unchanged.

Round 20 Q5: central115 exactly equals central120, golden/40-year. Together
with Q4, this supports original round19-15's tie. Q6 widens to central115
versus central125, same shade/age. Models remain fixed.

Round 20 Q6: central115 higher very slightly than central125, golden/40-year.
Q4/Q5 support the second original tie; no correction. Q7 begins third target:
West Central Asia versus South/Eastern Asia, both amber/20-year/125 lb.
Models remain frozen; no universal tare threshold inferred.

Round 20 Q7: West Central Asia125 exactly equals South/Eastern Asia125 at
amber/20-year. Q8 awaits South/Eastern Asia120 versus South/Eastern Asia125,
same shade/age, isolating tare for final target round19-20. Models remain fixed.

Round 20 Q8: South/Eastern Asia120 exactly equals South/Eastern Asia125, amber/
20-year. Together with Q7, this supports original round19-20's exact tie.
Q9 widens to South/Eastern Asia120 versus130, same shade/age. Models remain fixed.

Round 22 Q1: pale/straw higher very slightly than golden, central/30-year/120 lb.
Q2 awaits central golden25 versus golden30, both 120 lb, isolating vintage for
target round21-8. Both models remain frozen.

Round 22 Q2: central golden25 higher very slightly than golden30 at 120 lb.
Q3 explicitly rechecks original round21-8: golden25 versus pale/straw30, same
provenance/tare. Both components were very slight; await direct ordering rather
than infer equal magnitudes. Both models remain frozen.

Round 22 Q3 confirms original round21-8 A very slightly. First target retains
the contextual-model reversal; no answer correction. Q4 begins round21-3:
southeast versus southwest, both copper/30-year/125 lb. Both models remain fixed.

Round 22 Q4: southeast125 exactly equals southwest125, copper/30-year.
Q5 awaits southwest120 versus southwest125, same shade/age, isolating tare
for second target round21-3. Both models remain fixed.

Round 22 Q5: southwest120 exactly equals southwest125 at copper/30-year.
Together with Q4, this supports original round21-3's exact tie. Q6 widens
to southwest120 versus southwest130, same shade/age. Models remain fixed.

Round 22 Q6: southwest120 higher very slightly than southwest130, copper/30-year.
Q4/Q5 support second target's original tie. Q7 begins round21-11: southwest
versus northeast, both amber/30-year/125 lb. Both models remain frozen.

Round 22 Q7: southwest125 exactly equals northeast125, amber/30-year.
Q8 awaits northeast120 versus northeast125, same shade/age, isolating tare
for third target round21-11. Both model hashes remain unchanged.

Round 22 Q8: northeast120 exactly equals northeast125 at amber/30-year.
Together with Q7, this supports original round21-11's exact tie. Q9 widens
to northeast120 versus northeast130, same shade/age. Models remain fixed.

Round 22 Q9: northeast120 higher very slightly than northeast130 at amber/
30-year. Q7/Q8 support third original tie. Q10 starts final target round21-12:
Western Europe copper/35-year, 120 versus130 lb, widening the original
120-versus125 exact-tie pair. Both models remain frozen.

Round24 Q1: central pale/straw/20-year 120 lb higher very slightly than 130 lb.
Q2 explicitly rechecks original round23-10 (120 versus125 lb) to distinguish
tiny strict premium from exact equality. Models fixed; unresolved review follows
the five miss isolations.

Round24 Q2 explicitly corrects round23-10 from A to exactly equal: central pale/
20-year 120 versus125 lb. Override saved for future reconciliation; do not rewrite
the original frozen score. Q3 begins second target round23-1, northeast copper/
35-year 120 versus130 lb, widening tare. Models fixed.

Round24 Q3: northeast copper35 120 lb higher very slightly than130 lb. Original
round23-1 120=125 equality remains unchanged. Q4 begins third target round23-7:
West Central Asia copper35, 120 versus130 lb, widening the original tare contrast.
Both models fixed; unresolved Q3/Q9/Q18 review remains after miss isolation.

Round24 Q4: West Central Asia copper35 120 lb higher very slightly than130 lb.
Original round23-7 120=125 tie remains unchanged. Q5 begins fourth target
round23-13: northwest golden40, 115 versus125 lb. Both models remain frozen.

Round24 Q5: northwest golden40 115 lb higher very slightly than125 lb.
Original round23-13 115=120 tie remains unchanged. Q6 begins fifth target
round23-19: southeast brown30, 120 versus130 lb. Then review unresolved Q3/Q9/Q18.
Both models remain unchanged.

Round24 Q6: southeast brown30 120 lb higher very slightly than130 lb. Five miss
checks complete; first original answer corrected to tie, four others unchanged.
Phase now unresolved diagnosis. Q7 isolates provenance for round23-3: Western
Europe versus northwest, amber/30-year/125 lb. Queue status diagnosing, NOT resolved.
Separate component answers from original trade-off; ask why if difficulty persists.
Both models remain fixed.

Round24 Q7: Western Europe higher very slightly than northwest, amber30/125 lb.
Q8 isolates tare: northwest120 versus northwest125, same shade/age. Original
round23-3 remains unresolved while diagnosing; no cause inferred yet. Models fixed.

Round24 Q8: northwest120 higher very slightly than northwest125, amber/30-year.
Q9 returns to original unresolved round23-3 (Western Europe125 versus northwest120).
Both components are small; do not infer equal prices or the reason for difficulty
from identical adjectives. Await direct answer; models remain frozen.

Round24 Q9 resolves round23-3 as exactly equal. Component answers show offsetting
small provenance/tare advantages; do not claim subjective cause was confirmed.
Q10 begins round23-9 diagnosis: southeast versus northeast, amber25/125 lb.
Unresolved review 1/3 resolved; models unchanged.

Round24 Q10: southeast125 exactly equals northeast125, amber/25-year.
Q11 isolates tare: northeast120 versus northeast125, same shade/age.
Original round23-9 remains unresolved while diagnosing. Models remain fixed.

Round24 Q11: northeast120 higher than northeast125, amber/25-year; strength
unspecified. Q12 returns to original unresolved round23-9 (southeast125 versus
northeast120). Await direct answer rather than automatically resolve by inference.
Both models remain fixed.

Round24 Q12 resolves round23-9 as B very slightly after isolated provenance tie
and tare preference. Q13 begins final unresolved target round23-18: Western
Europe versus northwest, both golden/25-year/125 lb. Two of three resolved;
do not infer the user's subjective reason for previous difficulty. Models fixed.

Round24 Q13: Western Europe125 exactly equals northwest125, golden/25-year.
Q14 isolates tare: Western Europe120 versus125, same shade/age. Original
round23-18 remains unresolved pending direct revisit. Both models remain fixed.

Round24 Q14: Western Europe120 higher very slightly than125, golden/25-year.
Q15 returns to original unresolved round23-18 (Western Europe120 versus
northwest125). Await direct answer rather than resolve by inference. Models fixed.

Round24 Q15 resolves round23-18 as A very slightly. All five miss checks and
all three unresolved price pairs are complete: one explicit correction
(round23-10 A -> tie); unresolved Q3 tie, Q9 B very slightly, Q18 A very slightly.
A separate difficulty_review now asks why the original comparisons felt hard.
Do not infer the user's subjective explanation from the component pattern.
No more price questions pending, no refit, both model hashes unchanged.

Round26 Q1: NE over central very slightly at amber25/120 lb; user explicitly
states otherwise identical vintage >=30 would tie. Raw guidance saved without
global expansion. Q2 checks amber30/120 lb NE versus central directly. Models fixed.

Round26 Q2: NE equals central at amber30/120, with explanation that provenance
no longer creates a premium here. Original NE/SE25 tie unchanged. Q3 moves to
second target round25-13: northwest copper40, 120 versus130 lb, widening original
5 lb contrast. Both models fixed; no universal age/tare cutoff inferred.

Round26 Q3: northwest copper40 120 lb >130 very slightly; user says tare decides
with other attributes equal. Original120=125 tie unchanged. Q4 begins third
target round25-18 at older age: central versus southwest brown30/120 lb, compared
with original brown20 pair. No predicted direction disclosed; models fixed.

Round26 Q4: central equals southwest at brown30/120 lb; provenance no longer
creates premium here, per user. Q5 tests intermediate brown25/120 lb for the
same zone pair, between original20 premium and30 equality. Models fixed.
