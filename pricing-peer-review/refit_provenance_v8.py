"""Immutable evidence v8 and provenance-scoped refit, preserving all baselines."""
from collections import Counter
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import numpy as np
import compare_models as base
import compare_interactions as common
import compare_tare_models as shared
import provenance_tare_model as scoped
from reconcile_and_compare import align_answer,write_versioned

ROOT=Path(__file__).resolve().parent
SOURCES=('pricing.py','compare_models.py','compare_interactions.py','compare_objectives.py',
         'compare_tare_models.py','compare_exact_tare_ties.py','provenance_tare_model.py',
         'provenance-tare-comparison.json','contextual-comparison-v7.json','evidence-v7.json',
         'round23-fixed.json','round24-isolation.json')


def build_evidence(v7,round23,round24):
    rows=deepcopy(v7['rows']);audit=[]
    sources={q['id']:q for q in round23['questions']}
    for q in round23['questions']:
        if q['status']=='answered':
            rows.append(deepcopy(q));audit.append({'id':q['id'],'action':'new comparison'})
    for q in round24['questions']:
        if q['status']=='answered' and not q.get('revisits'):
            rows.append(deepcopy(q));audit.append({'id':q['id'],'action':'new component comparison'})
    by_id={r['id']:r for r in rows};answers={q['id']:q for q in round24['questions']}
    for entry in round24['unresolved_queue']:
        if entry['status']!='resolved':raise ValueError('Resolution queue incomplete')
        original=sources[entry['source_id']];q=answers[entry['resolution_id']]
        if original['status']!='unresolved' or original.get('winner') is not None:raise ValueError('Source was already answered')
        if q['status']!='answered' or q['revisits']!=original['id']:raise ValueError('Wrong resolution')
        winner=align_answer(original,q)
        if winner!=entry['winner']:raise ValueError('Queue/answer mismatch')
        row=deepcopy(original);row['prior_answer']={k:deepcopy(row.get(k)) for k in ('status','winner','raw_answer','strength')}
        row.update(status='answered',winner=winner,strength=q.get('strength'),current_answer_source=q['id'],current_raw_answer=q.get('raw_answer'))
        row['resolution_provenance']={'source_file':'round23-fixed.json','resolution_file':'round24-isolation.json','resolution_id':q['id']}
        rows.append(row);by_id[row['id']]=row;audit.append({'id':row['id'],'action':'resolved previously unanswered','resolution_id':q['id']})
    for override in round24.get('evidence_overrides',[]):
        row=by_id[override['source_id']];q=answers[override['replacement_id']]
        if q['status']!='answered' or q['revisits']!=row['id']:raise ValueError('Wrong correction source')
        winner=align_answer(row,q)
        if winner!=override['winner'] or winner==row['winner']:raise ValueError('Invalid correction')
        prior={k:deepcopy(row.get(k)) for k in ('status','winner','raw_answer','strength')}
        row['prior_answer']=prior
        row.update(winner=winner,strength=q.get('strength'),current_answer_source=q['id'],current_raw_answer=q.get('raw_answer'))
        audit.append({'id':row['id'],'action':'correction','clarification_id':q['id'],'old_winner':prior['winner'],'current_winner':winner})
    assert rows[:310]==v7['rows']
    assert len(rows)==341 and len(by_id)==341
    if len({frozenset((tuple(r['a']),tuple(r['b']))) for r in rows})!=341:raise ValueError('Duplicate pair')
    assert Counter(a['action'] for a in audit)=={'new comparison':17,'new component comparison':11,'resolved previously unanswered':3,'correction':1}
    return rows,audit


def extended_folds(old_groups,groups,seed):
    """Keep every old family in its original test fold; allocate only NEW groups.
    This makes reuse of old training-selected settings leak-free for old families.
    New groups are assigned by size, without accessing labels.
    """
    assignment={}
    for fold,(_,test) in enumerate(base.folds(old_groups,5,seed)):
        for g in set(old_groups[test]):assignment[g]=fold
    sizes=np.array([sum(assignment.get(g)==i for g in groups) for i in range(5)])
    new=list(set(groups)-set(assignment));new.sort();np.random.default_rng(seed).shuffle(new)
    new.sort(key=lambda g:-sum(groups==g))
    for g in new:
        fold=int(np.argmin(sizes));assignment[g]=fold;sizes[fold]+=sum(groups==g)
    which=np.array([assignment[g] for g in groups])
    for fold in range(5):yield np.flatnonzero(which!=fold),np.flatnonzero(which==fold)


def evaluate(rows,previous):
    _,y,g=common.get_arrays(rows,'additive');old_groups=g[:310]
    configs={(a['seed'],a['fold']):a for a in previous['nested_cv']['fold_audits']}
    masks=shared.masks(rows);masks.update({'prior_v7':np.arange(len(rows))<310,
       'round23_corrected_answers':(np.arange(len(rows))>=310)&(np.arange(len(rows))<327),
       'new_components':(np.arange(len(rows))>=327)&(np.arange(len(rows))<338),
       'resolutions':np.arange(len(rows))>=338})
    runs={'v7_evidence_control':[],'v8_evidence_candidate':[]};audits=[]
    for seed in common.SEEDS:
        pred={name:np.zeros(len(rows),dtype=int) for name in runs}
        for fold,(train,test) in enumerate(extended_folds(old_groups,g,seed)):
            cfg=configs[(seed,fold)]
            for name in runs:
                tr=train[train<310] if name=='v7_evidence_control' else train
                assert not set(g[tr])&set(g[test])
                train_rows=[rows[i] for i in tr];test_rows=[rows[i] for i in test]
                design,beta=scoped.fit(train_rows,cfg)
                pred[name][test]=scoped.score(test_rows,design,beta,cfg['threshold'])
                audits.append({'seed':seed,'fold':fold,'model':name,'train_n':len(tr),
                  'alpha':cfg['alpha'],'pooling':cfg['pooling'],'threshold':cfg['threshold'],
                  'local_contexts':list(design.local_contexts),'parameters':design.n,
                  'fixed_step_count':int(sum(design.fixed_steps(train_rows)))})
            print(f'Completed v8 provenance-scope seed {seed}, fold {fold+1}/5',flush=True)
        oldrun=next(r for r in previous['nested_cv']['runs'] if r['seed']==seed)
        np.testing.assert_array_equal(pred['v7_evidence_control'][:310],np.array(oldrun['predictions']))
        for name,pp in pred.items():runs[name].append({'seed':seed,'predictions':pp.tolist(),'metrics':{k:base.metrics(y[v],pp[v]) for k,v in masks.items()}})
    return {'row_ids':[r['id'] for r in rows],'groups':len(set(g)),'summary':{n:shared.summarize(v) for n,v in runs.items()},'runs':runs,'fold_audits':audits}


def main():
    hashes={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in SOURCES}
    v7=json.loads((ROOT/'evidence-v7.json').read_text());r23=json.loads((ROOT/'round23-fixed.json').read_text());r24=json.loads((ROOT/'round24-isolation.json').read_text())
    previous=json.loads((ROOT/'provenance-tare-comparison.json').read_text())
    rows,audit=build_evidence(v7,r23,r24)
    snapshot={'version':8,'parent':'evidence-v7.json','parent_sha256':hashes['evidence-v7.json'],
       'row_count':len(rows),'label_counts':dict(Counter(r['winner'] for r in rows)),
       'source_hashes':hashes,'reconciliation_audit':audit,
       'protocol':'310 parent + 17 answered Round23 + 11 fresh components + 3 formerly unresolved pairs. Apply round24-2 correction to round23-10 in place. No duplicate repeats; subjective difficulty response is workflow feedback, not a price observation.',
       'workflow_feedback':r24.get('difficulty_review'),'rows':rows}
    evidence=ROOT/'evidence-v8.json';write_versioned(evidence,snapshot)
    cv=evaluate(rows,previous)
    cfg=previous['candidate_fit_all_310'];design,beta=scoped.fit(rows,cfg)
    x=design.array(rows);y=np.array([base.LABEL[r['winner']] for r in rows]);margin=x@beta;pred=base.classify(margin,cfg['threshold']);fixed=design.fixed_steps(rows)
    forced=[]
    for i,row in enumerate(rows):
        support=abs(x[i])>1e-10
        if y[i]!=0 and np.any(support) and np.all(fixed[support]):forced.append(row['id'])
    mask=shared.masks(rows)['confirmed_pure_tare_ties']
    focus={'round14-2','round21-12','round23-1','round23-7','round23-10','round23-13','round23-19'}
    candidate={'alpha':cfg['alpha'],'pooling':cfg['pooling'],'threshold':cfg['threshold'],
       'local_contexts':list(design.local_contexts),'feature_names':design.names(),'coefficients':beta.tolist(),
       'in_sample':base.metrics(y,pred),'forced_strict_preference_ids':forced,
       'pure_tare_tie_audit':{'n':int(sum(mask)),'exact_score_equalities':int(sum(abs(margin[mask])<1e-7))},
       'target_predictions':[{'id':r['id'],'answer':r['winner'],'answer_source':r.get('current_answer_source',r['id']),
          'prediction':{-1:'B',0:'tie',1:'A'}[int(pred[i])],'margin':float(margin[i]),'exact_score_equality':bool(abs(margin[i])<1e-7)} for i,r in enumerate(rows) if r['id'] in focus]}
    result={'method':{'evidence_version':8,'evidence_sha256':hashlib.sha256(evidence.read_bytes()).hexdigest(),
       'structure':'Unchanged provenance-scoped local curves with partial pooling and training-only pure-tare exact constraints',
       'validation':'Preserve original v7 outer family assignments and training-selected per-fold settings. Add only new groups to folds deterministically without labels. Compare original-evidence fold control with augmented-evidence candidate on identical test rows; local contexts and constraints built within training only. No hyperparameter retuning.',
       'limits':'Fixed-settings data-update experiment on adaptive nonrandom evidence; no new independent prospective validation. Tie classification may not imply exact score equality.',
       'historical_file_hashes':hashes},'nested_cv':cv,'candidate_fit_all_341':candidate}
    write_versioned(ROOT/'provenance-comparison-v8.json',result)
    for f,h in hashes.items():assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h,f
    print(json.dumps({'labels':snapshot['label_counts'],'cv_all':{k:v['all'] for k,v in cv['summary'].items()},
                     'candidate_parameters':design.n,'targets':candidate['target_predictions'],'scope_conflicts':forced,'baselines_unchanged':True},indent=2))

if __name__=='__main__':main()
