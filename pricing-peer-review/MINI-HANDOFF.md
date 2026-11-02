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

## Latest completed focused test — keep existing, stop opposition penalties

Read premium-opposition-decision-v35.json and premium-opposition-validation-v35.json. Absolute/relative oppositiondiscounts both selectedzero inall25folds andfullfit.655pairs,413size labels,245direct. No gain overlarge-tare candidate. Forcedpenalty0.75fixesQ4/Q6butlosesQ9andotherpremiums:fullsize391→366,falsepremiums10→6,missedmeaningful12→41. Q9hasmoreoppositionthanQ4/Q6:genericcompetitiondiscount notsupported. Keepv28default+large-tareexperimental candidate;stopgenericpenalties/caseexceptions. Q4/Q6remainknownsize misses. Baselinehashverified,noquestionsorjobs pending.

## Latest completed experiment — v35 premium-size correction

Pilot12 incorporated once into evidence-v35.json:655unique pairs. Read premium-selection-v35.json. Rankingheldfixedv28. Onecoefficient0.7 boostsmeaningfulness only opposing5year vintage withtaregap>10lb whenv28winnerowns lightertare. Conditional family-heldout calibration: size388/413→390.2/413mean; direct226/245→228.2; both208/232→210.2. Falsepremiumsunchanged10all/6direct. Fullfit fixes3knowncases includingpilotQ9, changes3unknownsizecases. Q4,Q6stilloverstated. Broad5lb suppression rejected; rankidentity655rows, swapchecks,1000pure5lbcontrols pass; alltopoutputspreserved, notclaimednewlycorrect. Runnable predictor_premium_v35.py andpremium-config-v35.json; defaultv28retained. Baselineshashverified. Important: baselinepretrainedhistorical; evaluationisheldoutcorrectionconditionalonfrozenmodel, notfreshwholemodelvalidation. No questionspending orjobsrunning.

## Frozen combined pilot completed — 12 answers

combined-pilot-v34-fixed.json complete; combined-pilot-v34-results.json scored frozenforecasts, allhashesverified. Combined:direction10/12,size9/12,both7/12. v28:direction11/12,size9/12,both8/12. Retainv28default; candidate notpromoted. Q3both reverseBslight; Q4,Q6both overstatepremium; Q9both understateAmeaningful; Q10combinedreversesBslight whilev28correct. Clear-extreme/topprofile Q1,5,7,11 allcorrectboth. Voicefrontend repeatedly inventednextquestiondescriptions; user answeredverifiedtables aftercorrection. Q5initialBmeaningfulimmediatelycorrectedAmeaningful, historyretained. Q8voice-tail answerAbarelyrecorded; allanswerscomplete. No refit or evidence incorporation yet; no pendingquestion/backgroundjob. Userprefers tablesonlyduringelicitation.

## Active frozen pilot — combined predictor

combined-pilot-v34-fixed.json contains12 fresh attribute-stratified unordered comparisons and frozen combined/v28 forecasts. User authorized fresh test, one at a time. Question1 presented, awaiting answer. Do not expose forecasts/refit until all12answered. Combined runtime predictor_combined_v34.py/config combines frozen global-positive-v33 intrinsicrank with v28premium assessor, no mathchanges; diagnostic headconflict explicit.643row outputparity/swapchecks passed,0historical meaningfulheadconflicts. Verificationreceipt combined-verification-v34.json. Allhistorical roundJSON+latest evidence/comparisons scannedforunorderedduplicates. No runningjob. Preserve direction,meaningfulness,exactequality,practicalnondirection,unresolved separately.

## Latest completed audit — local balance, no new model adopted

Read local-balance-audit-v34.json, reproduced by audit_local_balance_v34.py. OldWE brown35/115 vsamber40/120 equality is representable alongside equal-tare Bslight andallthree nearbyrankingjudgments in fullfit. With entirefamilyheldout, model-implied crossing from diagnostic linearinterpolation lies114.529–118.116lb. Off-gridinterpolation notvalidated. Perturbing adjacenttare steps±1e-5 preservestrainingexactties,positiveguards,attribute ranges andtrainingdirectioncounts inall5folds,whilemovingoldergap. Thus evidence doesnotpin exact115balance outoffamily; not a new regional/shade exception or unresolved mathematicalcontradiction. Keep hardtrainingequalities, preservepositivepreferences, donotpretend memorizedcalibrationisgeneralization. No newcoefficient/config adopted. No runningjobs.

## Latest completed test — evidence v34, brown attenuation rejected

Read brown-summary-v34.json and brown-validation-v34.json. Newequal-tare WE brown35/120 versusamber40/120 recorded Bslight,643unique pairs,462directions. Threepredeclaredarms: unchangedpositiveguarded architecture93.9827%rank,25%olderbrown vintage+tareattenuation93.2035%,50%90.6061%. Same25familyfolds; both olderWE comparisons heldouttogether. Equal-tare Bdirection alreadycorrect5/5 underunchangedstructure. Olderexacttie0/5 allarms; attenuation pushes it towardB, not equality. Fullfitsretain3/3exact trainingties; this isnotgeneralization.97500profilechecks pass. Rejectattenuation, retainprior improvedrankingcandidate andv28default. Testdoesnotdisproveallbrowncontext effects, just uniformolderbrown coreattenuation. No runningjobs orpendingquestion.

## Latest completed analysis — five small-preference collapses fixed

Read positive-summary-v33.json, positive-validation-v33.json. All five failures shared copper→amber coefficient zero in seed11fold2, despite three pure positive training examples. Added training-only positive sign floor1e-4 for directly observed single-feature strict differences; no new feature/region/lookup. Same25folds: rank93.8829→94.0998%; exactly five changed case-repeat outcomes, all improvements, no other directional changes. Allfive now5/5.1100training signchecks and32500profilechecks pass. Exactheldout unchanged0,0,0,2,0; fullfit3/3exact. global-positive-config-v33.json saved experimental ranking only. Defaultv28 unchanged. Older WE equality decomposed: vintage35→40 plus tare115→120 must exactly equal brown→amber; unique pattern absent when family withheld. Representable in fullfit, no transfer yet; do not hardcode heldout equality or widen tieband. Baselinehashesverified. No pending jobs.

## Latest completed experiment — evidence v33 and intrinsic exact equality

Two Central clarifications reconciled once into evidence-v33.json:642pairs,461strictdirections,3exactties,400size labels. Read exact-summary-v33.json and exact-validation-v33.json. Same21coefficient intrinsicglobalmodel with train-only hard equality constraints,25familyfolds. Hardrank93.8829%, softrefit93.7093%, frozenv32global93.6659% on same461directions. Exactheldout0,0,0,2,0 of3; both balancecases removedtogether in4/5splits. Dedicated leavefamilyout transfers WE↔Southeast exactly; older WE tie fails. Fullfit3/3exact,442/461strict forbothhardandsoft. Five smallpositives collapseinonefold inbotharms; regressioncheck IDs in summary.32500 monotoneprofile checks pass,130gold/pale rule retained. Baselinehashesverified. New global-exact-config-v33.json experimental, no premiumhead/defaultchange. No runningjobs. Next issue unseen older-vintage equality; do notcall trainingfit/generalization solved or startquestionnaire automatically.

## Latest equality investigation — completed

Read equality-decision-v32.json. Tested score-band and11feature symmetric context logistic equality detectors using same25familyfolds, training-only threshold selection protecting strict directions. Context recovers0/4ties all repeats; scoreband recovers2/4inone repeat only. Both erase some strict preferences; reject deployment. Verified a minimal mathematical contradiction by LP: round6-8 exact Central brown35/120 = MiddleEast brown35/120, but round9-7 Central brown35/125 > MiddleEast brown35/120, incompatible with lower-tare-never-worse. Each relation removal restores feasibility. Do not silently relabel. Next useful action resolve this single contradiction before hard-equality refit. Sparse exact labels and nontransitivity of pair closeness are separate limitations. No running jobs; existing models retained.

# Latest completed voice reconciliation — evidence v32

Read voice-summary-v32.json and voice-validation-v32.json. Six clarifications reconciled once:4superseded+2new=642pairs;460directions,399size labels,4exact ties. Raw clarifications/history retained. Global refit on same family partitions:428.8/458common strict directions versus frozen global429.6/458; do not promote. Frozen premium OOF rescoring: v28 366.6/397 versus experimental374.6/397. These size metrics separate from direction. All4exact ties missed in every heldout repeat. Full-config new-pair diagnostic: v28 correctly distinguishes copper slight from amber meaningful; experimental head calls both meaningful. This diagnostic is not blind validation. Baseline hashes verified; no active job. Default stays v28; next issue exact equality representation, not another shade bonus.

## Latest voice clarification — two targets are equal price

Read shade-tare-tie-clarifications-v31.json before further fitting. User revised both round42-12 (Western Europe) and round54-11 (Southeast) to ties/equal price: copper25/125 versus amber30/115. Five years and10lb balance in this bracket; adjacent shade does not decide. Record once in next evidence version, retain history. Frozen v31/results remain historical. Do not continue forcing B or extrapolate universal exchange rates.

# Latest experiment — shared shade–tare interaction

Completed user-authorized test in shade_tare_global_v31.py; results in shade-tare-global-summary-v31.json and shade-tare-global-validation-v31.json. One nonnegative intrinsic amber-or-lighter x normalized lower-tare term;22 coefficients. Same25 family folds and train-only ridge selection. Global ranking93.3913%, candidate93.6087%; target WE and Southeast tradeoffs each correct only1/5 versus0/5. Six gained and one lost repeat-case outcomes; full-data interaction effectivelyzero. Reject promotion: no reliable transfer.13,000 monotonicity/zero-shade profile checks pass; baseline hashes verified. Premium head not fitted, so exceptional premium and small-premium size preservation not claimed. Default and global reference retained. No running job.

# Mini handoff — 2026-10-28

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

## Current state

- Workspace `/Users/stefansassoon/projects/wine`; no Git checkout at last check.
- Evidence **v31**:640unique pairs,460strict directions,396size labels,3explicit exactties.
- Round57's18reviews reconciled into existingpairs; no duplicate weighting.
- Active default remains `predictor_v28.py` / `model-config-v28.json`.
- New refit: `predictor_v31.py` / `model-config-v31.json`, experimental, not promoted.
- Read `model-selection-v31.json` first; task complete, no pendingquestion or backgroundfit.

## Critical semantic distinctions

Read `premium-semantics-clarification.json`. Vintage/tare foundation; provenance/shade
contextual modifiers. Value ranking, premium justification and buyer preference differ.
Exactprice equality is nowexplicit in reviewcases1/15/18 (canonicalround50-9/round6-8/round8-4).
Case11 is practicalsimilarity withoutcleardirection, notexactequality. Case7 has nominal
B/tiny pluspossible inventory-dependent tie. Keep rawexplanations and all histories.
Do not convert slightpreferences tozero, missingdirections to equality, or unresolved tosimilarity.

## Refitting and validation

Old23value basis could not express regional equality at35 plusstrictsmall regional
advantages at25/30. Refit adds9region-specific coefficients forone common maturity/darkness
interaction,32value terms total. Priceequalities enforced only in training. Gold/pale
remain identicalat130lb throughoutallfeatures. Latestreviewconstraints fit in full data.
Bestrefit anchorschanges towardmatchingv30trainingfits and refits premiumhead onv31,
retaining thelegacyreferenceencoder. No answerlookup in prediction.

| Model, scored on v31 | Value relation + size correct |
|---|---:|
| Frozen v28 | 85.11% |
| Frozen v30 soft-order/frozen-premium candidate | 87.95% |
| New anchored v31 refit | 85.30% |

219complete relation/size cases nowincludeexactties; older220-case percentages are not
directly comparable. All three models get0/3exactties when theirfamilies arewithheld.
The refit satisfiesall18reviewed judgments onprovidedaxes in fullfit, including3exactties;
this isnotgeneralization. Frozenmodel gains come fromclarifiedlabels,not improvedweights.
V28 remainsdefault, but it isnot thehighest scorer onthe revisedbenchmark.

Two older preferences conflict with latestexactties pluslower-tare monotonicity:
`round9-7` vs `round6-8`, and `round8-5` vs `round8-4`. Retained/flagged,not silentlyrelabelled.
See `v31-equality-conflicts.json`. No further questionnaire isauthorized.

59tests passed;1250offerings and1640runtimepair checks. Preservedallbaselines andv30.
SourceRound57file staysimmutable; its prereconciliation pendingflag ishistorical.
Currentcompletion receipt:`round57-reconciled-v31.json`.

Usefulfiles: `v31-refit-validation.json`, `v31-anchored-validation.json`,
`v31-representation-check.json`, `test_evidence_refit_v31.py`, `HANDOFF.md`.
Use `PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 .venv-regional/bin/python ...`.
