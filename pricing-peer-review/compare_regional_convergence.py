"""Evidence-v10 structural comparison on unchanged withheld-family partitions."""
import hashlib,json
from pathlib import Path
import numpy as np
import compare_models as base
import compare_tare_models as tare
import provenance_tare_model as offering
import domestic_hierarchy_model as prior
import weighted_domestic_model as baseline
import regional_convergence_model as candidate
import refit_weighted_v10 as protocol
from reconcile_and_compare import write_versioned

ROOT=Path(__file__).resolve().parent
SOURCES=tuple(dict.fromkeys((*protocol.SOURCES,'refit_weighted_v10.py','evidence-v10.json','weighted-hierarchy-comparison-v10.json','regional_convergence_model.py','compare_regional_convergence.py','requirements-regional.txt')))


def masks(rows):
    out=tare.masks(rows)
    domestic=np.array([r['a'][0] in prior.DOMESTIC and r['b'][0] in prior.DOMESTIC and r['a'][0]!=r['b'][0] for r in rows])
    matched=np.array([r['a'][1:]==r['b'][1:] for r in rows]);equal=np.array([r['winner']=='tie' for r in rows]);older=np.array([r['a'][2]>=30 and r['b'][2]>=30 for r in rows])
    out.update(domestic_provenance=domestic,domestic_matched_regional_ties=domestic&matched&equal,domestic_older_regional_ties=domestic&matched&equal&older,domestic_young_regional_ties=domestic&matched&equal&~older,domestic_matched_regional_preferences=domestic&matched&~equal)
    return out


def main():
    hashes={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in SOURCES}
    evidence=json.loads((ROOT/'evidence-v10.json').read_text());rows=evidence['rows']
    previous=json.loads((ROOT/'weighted-hierarchy-comparison-v10.json').read_text())
    assert len(rows)==401 and all(r['id'] not in ('round27-7','round27-11') for r in rows)
    _,y,g=baseline.protocol.common.get_arrays(rows,'additive');subsets=masks(rows)
    configs={(a['seed'],a['fold']):a for a in previous['nested_cv']['fold_audits'] if a['model']=='v10_evidence_candidate'}
    runs={'v10_baseline':[],'regional_convergence':[]};audits=[]
    for seed in prior.SEEDS:
        pred={name:np.zeros(len(y),dtype=int) for name in runs}
        for fold,(tr,te) in enumerate(protocol.extended_folds(g[:366],g,seed)):
            assert not set(g[tr])&set(g[te])
            train=[rows[i] for i in tr];test=[rows[i] for i in te];cfg=configs[(seed,fold)]
            strength,inner=candidate.choose(train,cfg,seed+fold+7000)
            design,beta=offering.fit(train,cfg)
            old_layer=baseline.Layer(design,beta);old_params=baseline.fit(train,old_layer,cfg['prior_strength'])
            pred['v10_baseline'][te]=baseline.predict(test,old_layer,old_params,cfg['threshold'])
            layer=candidate.Layer(design,beta);params=candidate.fit(train,layer,strength)
            pred['regional_convergence'][te]=candidate.predict(test,layer,params,cfg['threshold'])
            audits.append({'seed':seed,'fold':fold,'train_n':len(tr),'test_n':len(te),'alpha':cfg['alpha'],'pooling':cfg['pooling'],'threshold':cfg['threshold'],'prior_strength':strength,'inner_balanced_accuracy':inner['balanced_accuracy'],'baseline_prior_strength':cfg['prior_strength'],'local_contexts':list(design.local_contexts),'reference_fused_pair_contexts':int(sum(abs(layer.d@params)<1e-7))})
            print(f'Completed regional convergence seed {seed}, fold {fold+1}/5',flush=True)
        old=next(r for r in previous['nested_cv']['runs']['v10_evidence_candidate'] if r['seed']==seed)
        np.testing.assert_array_equal(pred['v10_baseline'],old['predictions'])
        for name,p in pred.items():runs[name].append({'seed':seed,'predictions':p.tolist(),'metrics':{k:base.metrics(y[m],p[m]) for k,m in subsets.items()}})
    cfg=previous['candidate_fit_all_401']['offering_snapshot']
    strength,inner=candidate.choose(rows,cfg,801)
    design=offering.Design(cfg['local_contexts']);layer=candidate.Layer(design,np.array(cfg['coefficients']));params=candidate.fit(rows,layer,strength)
    predictions=candidate.predict(rows,layer,params,cfg['threshold']);x,offset=layer.array(rows);margins=offset+x@params
    targets={'round27-3','round27-4','round27-9','round27-13','round27-14','round27-18','round27-19','round27-15','round27-20','round14-2','round21-12'}
    exact={k:{'n':int(sum(subsets[k])),'exact_score_equalities':int(sum(abs(margins[subsets[k]])<1e-7))} for k in ['confirmed_pure_tare_ties','domestic_matched_regional_ties','domestic_older_regional_ties']}
    diagnostics=[]
    for shade,age in prior.CONTEXTS:
        scores={z:float(layer.score([z,shade,age,120],params)) for z in prior.DOMESTIC}
        diagnostics.append({'shade':shade,'vintage':age,'full_scores_at_120_lb':scores,'spread':max(scores.values())-min(scores.values()),'equal_region_pairs':[[prior.DOMESTIC[i],prior.DOMESTIC[j]] for i,j in candidate.PAIR_INDICES if abs(scores[prior.DOMESTIC[i]]-scores[prior.DOMESTIC[j]])<1e-7]})
    result={'method':{'evidence':'evidence-v10.json','rows':401,'historical_file_hashes':hashes,
        'solver':'OSQP1.1.3 in isolated .venv-regional; same convex objective as SLSQP reference. Pre-run full-data solver parity checked at strengths0.1/1/10 without selecting model or changing priors.',
        'structure':'Replace persistent domestic region offsets and tier gates with centered shade/age-specific regional deviations plus a common domestic intercept; retain positive domestic shade/vintage/tare scaling of the same provenance-scoped offering fit. Foreign-only scores unchanged.',
        'equality':'L1 fusion penalty on pairwise domestic total score differences at reference tare120 lb can produce actual zero gaps. Reference equality is not guaranteed at other tare levels because local tare curves remain distinct. No regional equality labels are imposed as hard constraints.',
        'priors':{'age_fusion_weights':candidate.AGE_WEIGHTS,'fusion_coefficient':.3,'gap_ridge':.1,'adjacent_gap_smoothing':.5,'note':'Prespecified modeling conventions, not prices or claimed universal age laws. Age20 also shrunk for young convergence; older penalties grow after25. Soft average hierarchy has zero minimum margin, permitting equality; prior young premium-region dominance guidance retained.'},
        'validation':'Same v10 five outer family folds x five seeds. Same training-selected base offering settings and0.2 decision threshold. Inner3 family folds refit offering+candidate to select strength from0.1/1/10. Every v10 held-out baseline prediction reproduced exactly. No outer validation labels used for fitting or selection.',
        'limits':'Exploratory structural test on repeatedly used adaptive evidence, not an untouched prospective test.104 predictive parameters versus33 in v10 layer;250 auxiliary absolute-gap variables are optimization only. No abstention mechanism; original Q7/Q11 remain excluded.'},
        'nested_cv':{'row_ids':[r['id'] for r in rows],'runs':runs,'summary':{name:tare.summarize(v) for name,v in runs.items()},'fold_audits':audits},
        'candidate_fit_all_401':{'prior_strength':strength,'threshold':cfg['threshold'],'offering_snapshot':cfg,'parameters':params.tolist(),'domestic_order':prior.DOMESTIC,'contexts':prior.CONTEXTS,'reference_tare':120,'domestic_component_scales':dict(zip(['shade','vintage','tare'],params[101:].tolist())),'in_sample':base.metrics(y,predictions),'equality_audits':exact,'regional_diagnostics':diagnostics,'target_predictions':[{'id':r['id'],'answer':r['winner'],'prediction':{-1:'B',0:'tie',1:'A'}[int(predictions[i])],'margin':float(margins[i]),'exact_score_equality':bool(abs(margins[i])<1e-7)} for i,r in enumerate(rows) if r['id'] in targets]}}
    write_versioned(ROOT/'regional-convergence-comparison-v10.json',result)
    for f,h in hashes.items():assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h,f
    print(json.dumps({'all':{name:s['all'] for name,s in result['nested_cv']['summary'].items()},'strength':strength,'equalities':exact,'targets':result['candidate_fit_all_401']['target_predictions'],'baselines_unchanged':True},indent=2))

if __name__=='__main__':main()
