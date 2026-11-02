"""Evidence v9 and a weighted domestic hierarchy refit; all baselines read-only."""
from collections import Counter
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import numpy as np
import compare_models as base
import compare_tare_models as tare
import provenance_tare_model as offering
import domestic_hierarchy_model as prior
import weighted_domestic_model as weighted
import refit_provenance_v8 as protocol
from reconcile_and_compare import write_versioned

ROOT=Path(__file__).resolve().parent
SOURCES=('pricing.py','compare_models.py','compare_tare_models.py','provenance_tare_model.py',
         'domestic_hierarchy_model.py','weighted_domestic_model.py','refit_provenance_v8.py',
         'weighted-domestic-comparison.json','domestic-hierarchy-comparison.json',
         'provenance-comparison-v8.json','evidence-v8.json','round25-fixed.json','round26-isolation.json')


def build_evidence(parent,round25,round26):
    rows=deepcopy(parent['rows']);audit=[];guidance=[]
    for document,n,source,action in [(round25,20,'round25-fixed.json','new comparison'),
                                     (round26,5,'round26-isolation.json','new component comparison')]:
        if len(document['questions'])!=n:raise ValueError('Unexpected question count')
        for q in document['questions']:
            if q['status']!='answered' or q.get('winner') not in ('A','B','tie'):raise ValueError('Incomplete source')
            if q.get('revisits'):raise ValueError('Unexpected repeat requires reconciliation')
            rows.append(deepcopy(q));audit.append({'id':q['id'],'action':action,'source':source})
        for statement in document.get('rule_statements',[]):
            guidance.append({'source_file':source,**deepcopy(statement)})
    assert len(parent['rows'])==341 and len(rows)==366
    assert rows[:341]==parent['rows']
    if len({r['id'] for r in rows})!=366:raise ValueError('Duplicate IDs')
    if len({frozenset((tuple(r['a']),tuple(r['b']))) for r in rows})!=366:raise ValueError('Duplicate pair')
    assert Counter(a['action'] for a in audit)=={'new comparison':20,'new component comparison':5}
    return rows,audit,guidance


def extended_folds(parent_groups,groups,seed):
    assignments={}
    for fold,(_,te) in enumerate(protocol.extended_folds(parent_groups[:310],parent_groups,seed)):
        for g in set(parent_groups[te]):assignments[g]=fold
    sizes=np.array([sum(assignments.get(g)==i for g in groups) for i in range(5)])
    extra=sorted(set(groups)-set(assignments));np.random.default_rng(seed).shuffle(extra)
    extra.sort(key=lambda g:-sum(groups==g))
    for g in extra:
        fold=int(np.argmin(sizes));assignments[g]=fold;sizes[fold]+=sum(groups==g)
    which=np.array([assignments[g] for g in groups])
    for fold in range(5):yield np.flatnonzero(which!=fold),np.flatnonzero(which==fold)


def evaluate(rows,previous):
    _,y,g=protocol.common.get_arrays(rows,'additive')
    masks=tare.masks(rows);masks.update({'prior_v8':np.arange(len(rows))<341,
       'round25':(np.arange(len(rows))>=341)&(np.arange(len(rows))<361),
       'new_isolation':np.arange(len(rows))>=361,
       'domestic_provenance':np.array([r['a'][0] in prior.DOMESTIC and r['b'][0] in prior.DOMESTIC and r['a'][0]!=r['b'][0] for r in rows])})
    configs={(a['seed'],a['fold']):a for a in previous['nested_cv']['fold_audits']}
    runs={'v8_evidence_control':[],'v9_evidence_candidate':[]};audits=[]
    for seed in prior.SEEDS:
        predictions={n:np.zeros(len(y),dtype=int) for n in runs}
        for fold,(train,test) in enumerate(extended_folds(g[:341],g,seed)):
            cfg=configs[(seed,fold)];test_rows=[rows[i] for i in test]
            for name in runs:
                tr=train[train<341] if name=='v8_evidence_control' else train
                assert not set(g[tr])&set(g[test])
                training=[rows[i] for i in tr]
                if name=='v8_evidence_control':strength=cfg['prior_strength'];inner=None
                else:strength,inner=weighted.choose(training,cfg,seed+fold+7000)
                design,beta=offering.fit(training,cfg);layer=weighted.Layer(design,beta)
                params=weighted.fit(training,layer,strength)
                predictions[name][test]=weighted.predict(test_rows,layer,params,cfg['threshold'])
                audits.append({'seed':seed,'fold':fold,'model':name,'train_n':len(tr),
                    'alpha':cfg['alpha'],'pooling':cfg['pooling'],'threshold':cfg['threshold'],
                    'prior_strength':strength,'inner_balanced_accuracy':None if inner is None else inner['balanced_accuracy'],
                    'local_contexts':list(design.local_contexts)})
            print(f'Completed weighted v9 validation seed {seed}, fold {fold+1}/5',flush=True)
        old=next(r for r in previous['nested_cv']['runs'] if r['seed']==seed)
        np.testing.assert_array_equal(predictions['v8_evidence_control'][:341],np.array(old['predictions']))
        for name,pred in predictions.items():runs[name].append({'seed':seed,'predictions':pred.tolist(),'metrics':{k:base.metrics(y[v],pred[v]) for k,v in masks.items()}})
    return {'row_ids':[r['id'] for r in rows],'groups':len(set(g)),
            'summary':{n:tare.summarize(v) for n,v in runs.items()},'runs':runs,'fold_audits':audits}


def main():
    hashes={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in SOURCES}
    parent=json.loads((ROOT/'evidence-v8.json').read_text());r25=json.loads((ROOT/'round25-fixed.json').read_text());r26=json.loads((ROOT/'round26-isolation.json').read_text())
    previous=json.loads((ROOT/'weighted-domestic-comparison.json').read_text())
    rows,audit,guidance=build_evidence(parent,r25,r26)
    snapshot={'version':9,'parent':'evidence-v8.json','parent_sha256':hashes['evidence-v8.json'],
       'row_count':len(rows),'label_counts':dict(Counter(r['winner'] for r in rows)),
       'source_hashes':hashes,'reconciliation_audit':audit,'explanatory_guidance':guidance,
       'protocol':'341 parent + 20 Round25 answers + 5 fresh Round26 components. Explanations retained verbatim with scope; they are not extra observations or quantitative margin targets. No new synthetic labels or global hard cutoff.','rows':rows}
    path=ROOT/'evidence-v9.json';write_versioned(path,snapshot)
    cv=evaluate(rows,previous)
    oldcfg=previous['candidate_fit_all_341']['offering_snapshot']
    strength,inner=weighted.choose(rows,oldcfg,801)
    design,beta=offering.fit(rows,oldcfg);layer=weighted.Layer(design,beta);params=weighted.fit(rows,layer,strength)
    _,y,_=protocol.common.get_arrays(rows,'additive');x,offset=layer.array(rows);margins=offset+x@params;pred=base.classify(margins,oldcfg['threshold'])
    offering_snapshot={'alpha':oldcfg['alpha'],'pooling':oldcfg['pooling'],'threshold':oldcfg['threshold'],
       'local_contexts':list(design.local_contexts),'feature_names':design.names(),'coefficients':beta.tolist()}
    targets={'round25-11','round25-13','round25-18','round26-1','round26-2','round26-4','round26-5','round14-2','round21-12'}
    candidate={'prior_strength':strength,'threshold':oldcfg['threshold'],'offering_snapshot':offering_snapshot,
       'parameters':params.tolist(),'domestic_order':prior.DOMESTIC,'template':prior.TEMPLATE.tolist(),'contexts':prior.CONTEXTS,
       'domestic_component_scales':dict(zip(['shade','vintage','tare'],params[30:].tolist())),
       'in_sample':base.metrics(y,pred),
       'pure_tare_tie_audit':{'n':int(sum(tare.masks(rows)['confirmed_pure_tare_ties'])),
                             'exact_score_equalities':int(sum(abs(margins[tare.masks(rows)['confirmed_pure_tare_ties']])<1e-7))},
       'target_predictions':[{'id':r['id'],'answer':r['winner'],'prediction':{-1:'B',0:'tie',1:'A'}[int(pred[i])],
           'margin':float(margins[i]),'exact_score_equality':bool(abs(margins[i])<1e-7)} for i,r in enumerate(rows) if r['id'] in targets]}
    diagnostics=[]
    for shade,age in prior.CONTEXTS:
        premiums={z:float(prior.regional_features([z,shade,age,120])@params[:30]) for z in prior.DOMESTIC}
        diagnostics.append({'shade':shade,'vintage':age,'hierarchy_gain':float(params[5+prior.CONTEXTS.index((shade,age))]),'regional_premiums':premiums,'regional_spread':max(premiums.values())-min(premiums.values())})
    candidate['regional_diagnostics']=diagnostics
    result={'method':{'evidence_version':9,'evidence_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
       'structure':'Same weighted hierarchy + provenance-scoped offering pipeline. Base offering refit on training data; same base regularization and thresholds; prior strength selected within training-only inner family folds.',
       'validation':'Preserve original v8 family folds and base settings; new families assigned without labels. Matched v8-evidence control vs v9 candidate on identical test rows. Old control predictions reproduce original results on all original rows.',
       'explanations':'Stored as scoped metadata, not duplicated labels or arbitrary numeric strengths. Existing prior formulation unchanged to isolate evidence effects; no universal >=30 equality or >=10 dominance constraint added.',
       'limits':'Repeated adaptive nonrandom data; not fresh prospective validation. Equal-price classifier output need not imply exact fitted score equality except enforced pure-tare ties.',
       'historical_file_hashes':hashes},'nested_cv':cv,'candidate_fit_all_366':candidate}
    write_versioned(ROOT/'weighted-hierarchy-comparison-v9.json',result)
    for f,h in hashes.items():assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h,f
    print(json.dumps({'labels':snapshot['label_counts'],'cv_all':{k:v['all'] for k,v in cv['summary'].items()},
                     'settings':{'prior_strength':strength,'scales':candidate['domestic_component_scales']},
                     'targets':candidate['target_predictions'],'baselines_unchanged':True},indent=2))

if __name__=='__main__':main()
