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

# Latest completed work — foundation/amplifier two-head architecture

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

---
Historical checkpoints follow.

# Latest completed work — vintage/tare threshold test

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

---
Historical checkpoints follow.

# Latest completed work — regional stability audit

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

---
Historical checkpoints follow.

# Latest completed work — evidencev30

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

---
Historical checkpoints follow.

# Current task — Round56 complete

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


---
Historical checkpoint follows.

# Latest completed work — intrinsic refinements

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

---
Prior checkpoint follows.

# Resumed and completed — v29 comparison

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


---
Historical pause checkpoint follows; current state is above.

# Wine model session checkpoint — 2026-10-27

User requested a pause and compaction preparation. Stop here; no active questionnaire or fit.
Read this checkpoint before the long historical README/HANDOFF. Live state is also in
pricing-reset-progress.json. Workspace: /Users/stefansassoon/projects/wine.

## Current delivery

- Evidence: evidence-v28.json and benchmark-targets-v28.json; 620 unique pairs.
- Working entry point: predictor_v28.py; config: model-config-v28.json.
- Shared inference engine: predictor_v27.py. NumPy + JSON, no answer lookup.
- Current architecture: 18 additive terms + matched-provenance five-year golden/pale
  comparison term + scoped five-pound tare compensation; 20 fitted coefficients.
- This is a PAIR comparator, not a single intrinsic monetary price function.
- tare-refit-validation-v28.json / model-selection-v28.json hold validation. v28 beat
  previous tare model on complete judgments 176.6/202 vs170.0, direction93.45% vs91.43%,
  false premiums13.0 vs19.6; missed meaningful13.6 vs11.8. Means over5 reused family
  repeats, not fresh independent accuracy. Runtime parity exhaustively verified.
- Frozen historical baselines, tests and raw answers must remain intact.

## What changed in the latest explanation — critical

Round55 is complete: round55-tare-context-isolation.json contains10 active judgments,
verbatim explanations and frozen prediction snapshots. round55-findings.json summarizes.
These judgments are NOT YET incorporated into v28 and no weights were changed afterward.

The user clarified that price belongs to EACH OFFERING intrinsically, based on attributes,
combinations, and position within inventory/home-geography brackets. A comparison reveals
the difference; it does not create a premium. Current pair-dependent bonuses do not guarantee
that property. Do not pretend they already implement an intrinsic valuation model.

Vintage generally carries greatest weight; vintage and tare are the two most important.
This is qualitative/contextual priority, not universal dominance or elicited percentages.
Provenance position is assessed within its home-geography ladder, and shade-distance matters.
Do not turn informal adjacency counts into invented numerical weights or market statistics.

### New exception to the old pure-five-pound constraint

The user explicitly assigns an exceptional meaningful premium when110lb completes an
all-top-tier offering. Positive cases, with both alternatives otherwise identical:

- Western Europe, pale/straw,20years:110lb >115lb meaningfully, described as a lot more.
- Domestic Northeast, pale/straw,20years:110lb >115lb meaningfully.

Small positive/practically similar controls, NOT ties:

- Western Europe,pale,20years:115lb >120lb slightly.
- Western Europe,pale,25years:110lb >115lb slightly.
- Western Europe,golden,20years:110lb >115lb slightly.
- Domestic Northwest,pale,20years:110lb >115lb slightly.

Thus the old blanket hard constraint “every pure5lb step must be nonmeaningful” is now
known to be wrong for these explicit contexts. Preserve ordinary controls, allow scoped
exceptions. Do not keep an invalid test merely because previous model versions passed it.
The collector/commemorative rarity language is the user's valuation rationale, not a
verified inventory frequency or a literal product category. Untested regions not inferred.

### Crossed-profile comparisons from the user's proposed method

- WE golden20/110 vs NW pale20/110: A slightly higher/practically similar/not tie.
  User says golden/pale is one shade step, much weaker contrast than pale vs copper/brown.
- Same profiles at115lb: no clear price-based direction, practically similar, approximately
  same pricing; taste determines choice. NOT exact mathematical equality. User describes
  WE as top in its home geography, NW several steps away within its domestic bracket;
  do not impose a precise ordinal map or a universal NW>=WE relation from that wording.

### Two original reported misses

1. Source round53-2: WCA golden30/115 vs golden25/130.
   User REAFFIRMED A moderately/meaningfully higher.15lb gap and its position on the tare
   spectrum are the main driver. Pale adds something in the original pale variant, but
   shade is not required for meaningful A premium. Current v28 gets A direction but
   understates size. The all-top completion mechanism is additional guidance; it does
   not alone explain this non-top-profile large-gap case.
2. Source round47-18: Southwest golden30/125 vs Northwest golden25/130.
   Latest answer (round55-10) is NO CLEAR PRICE-BASED DIRECTION, practically similar,
   NOT an exact tie. Both are middling profiles, nuances insufficient for premium.
   This supersedes the earlier strict A/slightly label when next evidence is reconciled.
   Do not continue calling predicted B a direction error against a target no longer given.
   Do not rewrite original frozen test receipts; retain correction history.

## Reconciliation and validation discipline

- Deduplicate by unordered exact offering pair; reverse A/B label when necessary while
  preserving presented orientation and raw answer. Supersede active original IDs in-place,
  with previous records retained; never duplicate-weight clarification/probe pairs.
- Keep direction separate from meaningfulness. A small positive premium is not zero.
- “Unresolved / too close to call, not a tie” is missing judgement, not practical similarity.
- No-clear-direction + practical similarity is a supplied size judgement without a sign,
  not an exact equality. Do not invent a winner.
- Historical “slightly” alone was retained as direction-only unless the answer/explicit
  question established the practical category. Attribute importance is not automatically
  overall premium magnitude.
- All original unresolved comparisons were explicitly resolved in Rounds52–54. Last
  probe round54-17 (NE brown25/115 vs amber30/120) is A/slightly, binary size unspecified.
  v28 has empty fully-unresolved registry, but244 size labels remain unspecified.
- Many old meaningful labels are strength-derived proxies; do not describe every label
  as an explicit two-axis judgement.
- Compare on identical current evidence and group families; no answer lookup as prediction.
  Keep related provenance/shade variants together in held-out folds. Train-only constraints.
- Prior global additive model failed a three-judgment feasibility check; that rules out
  shared additive weights + shared threshold, NOT all intrinsic utility functions.
  Offering-level interactions/nonlinear curves are distinct from comparison-created value.

## Likely next work, only after user resumes/authorizes

1. Reconcile Round55 into a new evidence version (likelyv29; check existing files first),
   preserving source round53-2 history and replacing round47-18 direction with missing.
2. Formulate a small intrinsic-offering-value candidate with bracket-dependent/nonlinear
   tare and a tested all-top completion interaction; do not simply strengthen tare globally
   or silently preserve pair bonuses inconsistent with the user's value interpretation.
3. Test against currentv28 using joint direction+meaningfulness objective, correct scoped
   five-pound controls, and preserved zero golden/pale premium at130lb. No numeric money
   anchors have been supplied. Do not claim calibrated dollar prices.
4. Inspect regressions/stability and deliver the better tested model; not every new model
   must replace its predecessor. Current request was a pause, NOT authorization to run this
   fit immediately or start more elicitation.

## Workflow / user preferences

- Minimal ceremony. Act on clear authorized work; don't repeatedly ask permission or repeat
  “baselines unchanged/no questionnaire started” in final answers as boilerplate.
- State actual outcomes, known limitations and meaningful tradeoffs, not inflated progress.
- One-at-a-time explanations have been useful. User's crossed-profile comparison idea is
  important: hold two attributes fixed, compare profiles, repeat at another shared level.
- Do not unnecessarily repeat questions already answered. Preserve full explanations.
- No subagents unless explicitly requested or a project instruction requires delegation.
- Python: PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 .venv-regional/bin/python ...
  Existing SciPy/NumPy/OSQP and HiGHS available. Use single-thread solver options; mixing
  HiGHS thread counts in one process can fail. MILP tolerance status is not exact optimality.
- This directory has not been a Git checkout; do not invent commits/deployments.
- No background job was left running at the checkpoint.
