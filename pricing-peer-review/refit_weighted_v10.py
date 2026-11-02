"""Evidence v10 and a weighted domestic hierarchy refit; all baselines read-only."""
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
import refit_weighted_v9 as previous_protocol
from reconcile_and_compare import align_answer
from reconcile_and_compare import write_versioned

ROOT=Path(__file__).resolve().parent
ROUND_FILES=('round27-fixed.json',)+tuple(f'round{n}-isolation.json' for n in range(28,33))
SOURCES=tuple(dict.fromkeys((*previous_protocol.SOURCES,'refit_weighted_v9.py',
    'evidence-v9.json','weighted-hierarchy-comparison-v9.json',*ROUND_FILES)))


def verify_freeze(document):
    fields=document['freeze_fields'];n=document.get('initial_frozen_question_count',len(document['questions']))
    payload=[{k:q[k] for k in fields} for q in document['questions'][:n]]
    assert hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest()==document['questions_and_predictions_sha256']
    for freeze in document.get('adaptive_question_freezes',[]):
        q=next(q for q in document['questions'] if q['id']==freeze['question_id'])
        payload={k:q[k] for k in freeze['freeze_fields']}
        assert hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest()==freeze['sha256']
    for filename,h in document['file_sha256'].items():
        assert hashlib.sha256((ROOT/filename).read_bytes()).hexdigest()==h,filename


def build_evidence(parent,documents):
    rows=deepcopy(parent['rows']);audit=[];guidance=[]
    key=lambda q:frozenset((tuple(q['a']),tuple(q['b'])))
    index={key(q):q for q in rows}
    originals={q['id']:q for q in documents[0]['questions']}
    resolutions={'round30-3':'round27-15','round31-3':'round27-20'}
    unresolved_keys={key(originals[i]) for i in ('round27-7','round27-11')}
    for source,document in zip(ROUND_FILES,documents):
        for q in document['questions']+document.get('supplemental_comparisons',[]):
            if q.get('winner') not in ('A','B','tie'):
                audit.append({'id':q['id'],'source':source,'action':'excluded unresolved'})
                continue
            if key(q) in unresolved_keys:raise ValueError('Original Q7/Q11 must remain unresolved')
            row=deepcopy(q)
            if q['id'] in resolutions:
                original=originals[resolutions[q['id']]]
                row=deepcopy(original);row.update(winner=align_answer(original,q),status='answered',strength=q.get('strength'),
                    raw_answer=q['raw_answer'],resolved_by=q['id'],resolution_source=source,
                    original_unresolved_answer=original.get('raw_answer'),label_basis=q.get('label_basis','Direct explicit pricing response'))
            if key(row) in index:
                old=index[key(row)];label=align_answer(old,row)
                if old['winner']!=label:raise ValueError(f"Conflicting repeat {q['id']} versus {old['id']}; explicit reconciliation needed")
                audit.append({'id':q['id'],'source':source,'action':'confirmation; no extra sample','existing_id':old['id'],
                    'raw_answer':q.get('raw_answer'),'strength':q.get('strength'),'winner_in_existing_order':label})
                continue
            row['evidence_source']=source
            rows.append(row);index[key(row)]=row
            audit.append({'id':row['id'],'answer_id':q['id'],'source':source,'action':'resolved original' if q['id'] in resolutions else 'new comparison'})
        for statement in document.get('rule_statements',[]):
            guidance.append({'source_file':source,**deepcopy(statement)})
        for feedback in document.get('workflow_feedback',[]):
            guidance.append({'source_file':source,'metadata_type':'workflow_feedback',**deepcopy(feedback)})
    unresolved=[deepcopy(originals[i]) for i in ('round27-7','round27-11')]
    assert len(parent['rows'])==366 and rows[:366]==parent['rows']
    assert len(rows)==401 and len({q['id'] for q in rows})==401 and len(index)==401
    assert all(key(q) not in unresolved_keys for q in rows)
    return rows,audit,guidance,unresolved


def extended_folds(parent_groups,groups,seed):
    assignments={}
    for fold,(_,te) in enumerate(previous_protocol.extended_folds(parent_groups[:341],parent_groups,seed)):
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
    masks=tare.masks(rows);masks.update({'prior_v9':np.arange(len(rows))<366,
       'new_v10':np.arange(len(rows))>=366,
       'domestic_provenance':np.array([r['a'][0] in prior.DOMESTIC and r['b'][0] in prior.DOMESTIC and r['a'][0]!=r['b'][0] for r in rows])})
    configs={(a['seed'],a['fold']):a for a in previous['nested_cv']['fold_audits'] if a['model']=='v9_evidence_candidate'}
    runs={'v9_evidence_control':[],'v10_evidence_candidate':[]};audits=[]
    for seed in prior.SEEDS:
        predictions={n:np.zeros(len(y),dtype=int) for n in runs}
        for fold,(train,test) in enumerate(extended_folds(g[:366],g,seed)):
            cfg=configs[(seed,fold)];test_rows=[rows[i] for i in test]
            for name in runs:
                tr=train[train<366] if name=='v9_evidence_control' else train
                assert not set(g[tr])&set(g[test])
                training=[rows[i] for i in tr]
                if name=='v9_evidence_control':strength=cfg['prior_strength'];inner=None
                else:strength,inner=weighted.choose(training,cfg,seed+fold+7000)
                design,beta=offering.fit(training,cfg);layer=weighted.Layer(design,beta)
                params=weighted.fit(training,layer,strength)
                predictions[name][test]=weighted.predict(test_rows,layer,params,cfg['threshold'])
                audits.append({'seed':seed,'fold':fold,'model':name,'train_n':len(tr),
                    'alpha':cfg['alpha'],'pooling':cfg['pooling'],'threshold':cfg['threshold'],
                    'prior_strength':strength,'inner_balanced_accuracy':None if inner is None else inner['balanced_accuracy'],
                    'local_contexts':list(design.local_contexts)})
            print(f'Completed weighted v10 validation seed {seed}, fold {fold+1}/5',flush=True)
        old=next(r for r in previous['nested_cv']['runs']['v9_evidence_candidate'] if r['seed']==seed)
        np.testing.assert_array_equal(predictions['v9_evidence_control'][:366],np.array(old['predictions']))
        for name,pred in predictions.items():runs[name].append({'seed':seed,'predictions':pred.tolist(),'metrics':{k:base.metrics(y[v],pred[v]) for k,v in masks.items()}})
    return {'row_ids':[r['id'] for r in rows],'groups':len(set(g)),
            'summary':{n:tare.summarize(v) for n,v in runs.items()},'runs':runs,'fold_audits':audits}


def main():
    hashes={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in SOURCES}
    parent=json.loads((ROOT/'evidence-v9.json').read_text())
    documents=[json.loads((ROOT/f).read_text()) for f in ROUND_FILES]
    for document in documents:verify_freeze(document)
    previous=json.loads((ROOT/'weighted-hierarchy-comparison-v9.json').read_text())
    rows,audit,guidance,unresolved=build_evidence(parent,documents)
    snapshot={'version':10,'parent':'evidence-v9.json','parent_sha256':hashes['evidence-v9.json'],
       'row_count':len(rows),'label_counts':dict(Counter(r['winner'] for r in rows)),
       'source_hashes':hashes,'reconciliation_audit':audit,'explanatory_guidance':guidance,
       'unresolved_pairs':unresolved,
       'protocol':'366 parent plus35 unique answered pairs. Original Round27 Q7/Q11 excluded, retained unresolved; Q15/Q20 resolved under original IDs. Same-pair confirmations not extra samples. Supplemental provenance-swap answer included once. Explanations are metadata, not numeric margins or extra observations. Frozen historical scores unchanged.',
       'rows':rows}
    path=ROOT/'evidence-v10.json';write_versioned(path,snapshot)
    cv=evaluate(rows,previous)
    oldcfg=previous['candidate_fit_all_366']['offering_snapshot']
    strength,inner=weighted.choose(rows,oldcfg,801)
    design,beta=offering.fit(rows,oldcfg);layer=weighted.Layer(design,beta);params=weighted.fit(rows,layer,strength)
    _,y,_=protocol.common.get_arrays(rows,'additive');x,offset=layer.array(rows);margins=offset+x@params;pred=base.classify(margins,oldcfg['threshold'])
    offering_snapshot={'alpha':oldcfg['alpha'],'pooling':oldcfg['pooling'],'threshold':oldcfg['threshold'],
       'local_contexts':list(design.local_contexts),'feature_names':design.names(),'coefficients':beta.tolist()}
    targets={'round27-3','round27-4','round27-9','round27-13','round27-14','round27-18','round27-19','round27-15','round27-20','round14-2','round21-12'}
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
    result={'method':{'evidence_version':10,'evidence_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
       'structure':'Same weighted hierarchy + provenance-scoped offering pipeline. Base offering refit on training data; same base regularization and thresholds; prior strength selected within training-only inner family folds.',
       'validation':'Preserve original v9 family folds and base settings; new families assigned without labels. Matched v9-evidence control vs v10 candidate on identical test rows. Old control predictions reproduce original results on all original rows.',
       'explanations':'Stored as scoped metadata, not duplicated labels or arbitrary numeric strengths. Existing prior formulation unchanged to isolate evidence effects; no universal >=30 equality or >=10 dominance constraint added.',
       'limits':'Repeated adaptive nonrandom data; not fresh prospective validation. Equal-price classifier output need not imply exact fitted score equality except enforced pure-tare ties.',
       'historical_file_hashes':hashes},'nested_cv':cv,'candidate_fit_all_401':candidate}
    write_versioned(ROOT/'weighted-hierarchy-comparison-v10.json',result)
    for f,h in hashes.items():assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h,f
    print(json.dumps({'labels':snapshot['label_counts'],'cv_all':{k:v['all'] for k,v in cv['summary'].items()},
                     'settings':{'prior_strength':strength,'scales':candidate['domestic_component_scales']},
                     'targets':candidate['target_predictions'],'baselines_unchanged':True},indent=2))

if __name__=='__main__':main()
