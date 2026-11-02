"""Build immutable evidence v5 and validate an additive direct-ranking candidate.
Historical source evidence and all prior model artifacts are read-only.
Run OPENBLAS_NUM_THREADS=1 python3 refit_additive_v5.py
"""
from __future__ import annotations
from collections import Counter
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import numpy as np
import compare_models as base
import compare_interactions as models
import compare_objectives as objectives
from reconcile_and_compare import align_answer, write_versioned
import pricing as production

ROOT=Path(__file__).resolve().parent
SOURCES=('pricing.py','compare_models.py','compare_interactions.py','compare_objectives.py',
         'reconcile_and_compare.py','model-comparison.json','interaction-comparison.json',
         'objective-comparison.json','objective-comparison-v2.json','evidence-v2.json',
         'comparisons.json','round9-fixed.json','round10-fixed.json','round11-isolation.json',
         'round12-clarification.json','round13-fixed.json','round14-isolation.json',
         'refit_additive_v3.py','additive-comparison-v3.json','evidence-v3.json',
         'round15-fixed.json','round16-isolation.json',
         'refit_additive_v4.py','additive-comparison-v4.json','evidence-v4.json',
         'round17-fixed.json','round18-isolation.json')


def build_evidence(v4, round17, round18):
    rows=deepcopy(v4['rows']);audit=[]
    for q in round17['questions']:
        if q['status']=='answered':
            rows.append(deepcopy(q));audit.append({'id':q['id'],'action':'new comparison','source':'round17-fixed.json'})
    for q in round18['questions']:
        if q['status']=='answered' and not q.get('revisits'):
            rows.append(deepcopy(q));audit.append({'id':q['id'],'action':'new component comparison','source':'round18-isolation.json'})
    by_id={r['id']:r for r in rows}
    for q in round18['questions']:
        if q['status']!='answered' or not q.get('revisits'):continue
        row=by_id[q['revisits']];winner=align_answer(row,q)
        if winner!=row['winner']:raise ValueError('Unexpected changed answer; explicit correction handling required')
        row.setdefault('clarification_history',[]).append({'clarification_id':q['id'],
            'winner_in_source_order':winner,'strength':q.get('strength'),'raw_answer':q.get('raw_answer'),'effect':'confirmation'})
        audit.append({'id':row['id'],'action':'confirmation','clarification_id':q['id']})
    seen=set();ids=set()
    for row in rows:
        key=frozenset((tuple(row['a']),tuple(row['b'])))
        if key in seen or row['id'] in ids:raise ValueError('Duplicate comparison or ID')
        seen.add(key);ids.add(row['id'])
    assert len(v4['rows'])==224 and len(rows)==252
    assert Counter(x['action'] for x in audit)=={'new comparison':20,'new component comparison':8,'confirmation':1}
    assert rows[:224]==v4['rows']
    return rows,audit


def evaluate(rows):
    x,y,g=models.get_arrays(rows,'additive')
    old_mask=np.arange(len(rows))<224
    subsets={'all':np.ones(len(rows),dtype=bool),'prior_v4':old_mask,
             'round17_original_answers':(np.arange(len(rows))>=224)&(np.arange(len(rows))<244),
             'isolation_components':np.arange(len(rows))>=244}
    runs={'v4_evidence_control':[],'v5_evidence_candidate':[]};selections=[]
    # Both trained anew within each outer fold; saved baseline models are NOT refit.
    for seed in models.SEEDS:
        predictions={name:np.zeros(len(y),dtype=int) for name in runs}
        for fold,(train,test) in enumerate(base.folds(g,5,seed)):
            for name in runs:
                tr=train[old_mask[train]] if name=='v4_evidence_control' else train
                assert not set(g[tr])&set(g[test])
                cfg=objectives.select(x[tr],y[tr],g[tr],'additive',seed+fold+1000)
                beta=objectives.fit(x[tr],y[tr],'additive',cfg['alpha'],cfg['pooling'])
                predictions[name][test]=base.classify(x[test]@beta,cfg['threshold'])
                selections.append({'seed':seed,'fold':fold,'model':name,'train_n':len(tr),'test_n':len(test),**cfg})
        for name,pred in predictions.items():
            runs[name].append({'seed':seed,'metrics':{key:base.metrics(y[mask],pred[mask]) for key,mask in subsets.items()},'predictions':pred.tolist()})
        print(f'Completed matched-family validation seed {seed}',flush=True)
    summary={}
    for name,items in runs.items():
        summary[name]={}
        for subset in subsets:
            mm=[r['metrics'][subset] for r in items]
            summary[name][subset]={k:float(np.mean([m[k] for m in mm])) for k in ('accuracy','balanced_accuracy','opposite_winner_errors','predicted_ties')}
            summary[name][subset]['n']=mm[0]['n']
            summary[name][subset]['accuracy_range']=[min(m['accuracy'] for m in mm),max(m['accuracy'] for m in mm)]
            summary[name][subset]['mean_recall']={k:float(np.mean([m['recall'][k] for m in mm if k in m['recall']])) for k in base.LABEL if any(k in m['recall'] for m in mm)}
    return {'row_ids':[r['id'] for r in rows],'groups':len(set(g)),'runs':runs,'summary':summary,'selections':selections}


def main():
    hashes={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in SOURCES}
    v4=json.loads((ROOT/'evidence-v4.json').read_text())
    r17=json.loads((ROOT/'round17-fixed.json').read_text());r18=json.loads((ROOT/'round18-isolation.json').read_text())
    rows,audit=build_evidence(v4,r17,r18)
    snapshot={'version':5,'parent':'evidence-v4.json','parent_sha256':hashes['evidence-v4.json'],
              'row_count':len(rows),'label_counts':dict(Counter(r['winner'] for r in rows)),
              'source_hashes':hashes,'reconciliation_audit':audit,
              'protocol':'224 parent + 20 answered Round17 + 8 fresh Round18 components. One original-pair confirmation attaches to source without an additional observation or weight. No answer corrections; all prior versions and frozen scores preserved.',
              'rows':rows}
    evidence_file=ROOT/'evidence-v5.json';write_versioned(evidence_file,snapshot)
    cv=evaluate(rows);x,y,g=models.get_arrays(rows,'additive')
    cfg=objectives.select(x,y,g,'additive',401)
    beta=objectives.fit(x,y,'additive',cfg['alpha'],cfg['pooling']);margin=x@beta;pred=base.classify(margin,cfg['threshold'])
    highlights={'round17-3','round17-13','round17-15'}
    candidate={**cfg,'feature_names':base.FEATURES,'coefficients':beta.tolist(),
               'in_sample':base.metrics(y,pred),
               'constraint_audit':{'strict_rank_sign_violations':int(np.sum((y!=0)&(y*margin<=1e-8))),
                                   'ties_not_exactly_equal':int(np.sum((y==0)&(abs(margin)>1e-8)))},
               'target_predictions':[{'id':r['id'],'answer':r['winner'],'answer_source':r.get('current_answer_source',r['id']),
                    'prediction':{-1:'B',0:'tie',1:'A'}[int(pred[i])],'margin':float(margin[i])}
                    for i,r in enumerate(rows) if r['id'] in highlights]}
    old_cfg=json.loads((ROOT/'additive-comparison-v4.json').read_text())['candidate_fit_all_224']
    old_beta=np.array(old_cfg['coefficients']);old_pred=base.classify(x[224:]@old_beta,old_cfg['threshold'])
    e_pred=np.array([base.LABEL[production._winner(production.utility(*r['a']),production.utility(*r['b']))] for r in rows[224:]])
    saved_baselines={}
    for name,pp in [('frozen_v4_additive',old_pred),('revision_e',e_pred)]:
        saved_baselines[name]={'round17_original_answers':base.metrics(y[224:244],pp[:20]),
                               'eight_isolation_components':base.metrics(y[244:],pp[20:]),
                               'scope':'Round17 original frozen scores preserved. Isolation is adaptive diagnosis, not independent accuracy.'}
    result={'method':{'evidence_version':5,'evidence_file':evidence_file.name,
                       'evidence_sha256':hashlib.sha256(evidence_file.read_bytes()).hexdigest(),
                       'rows':len(rows),'features':'unchanged 18-parameter additive','objective':'unchanged squared ranking hinge + squared tie gaps + ridge',
                       'validation':'5 outer grouped folds x 5 seeds, inner 3 grouped folds; same selection grids and seeds. Compare newly trained v4-evidence control vs v5-evidence candidate on IDENTICAL outer test families. Saved model coefficients are never edited.',
                       'limits':'Repeated nonrandom evidence, no pristine holdout. Weak monotonicity; soft tie penalty does not ensure exact price equality. Rechecks never add independent weight.',
                       'historical_file_hashes':hashes},
            'nested_cv':cv,'candidate_fit_all_252':candidate,
            'hard_feasibility':objectives.hard_feasibility(x,y),
            'identical_feature_conflicts':objectives.feature_conflicts(rows,x,y),
            'unchanged_baseline_rescoring':saved_baselines}
    write_versioned(ROOT/'additive-comparison-v5.json',result)
    for f,h in hashes.items():assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h,f
    print(json.dumps({'labels':snapshot['label_counts'],'cv_all':{k:v['all'] for k,v in cv['summary'].items()},
                      'candidate_settings':cfg,'candidate_fit':candidate['in_sample']['matched'],
                      'targets':candidate['target_predictions'],'baselines_unchanged':True},indent=2))

if __name__=='__main__':main()
