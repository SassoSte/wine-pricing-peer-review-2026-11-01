"""Build immutable evidence v3 and validate an additive direct-ranking candidate.
Historical source evidence and all prior model artifacts are read-only.
Run OPENBLAS_NUM_THREADS=1 python3 refit_additive_v3.py
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
         'round12-clarification.json','round13-fixed.json','round14-isolation.json')


def build_evidence(v2, round13, round14):
    rows=deepcopy(v2['rows']);initial=len(rows)
    audit=[]
    for q in round13['questions']:
        if q['status']=='answered':
            rows.append(deepcopy(q));audit.append({'id':q['id'],'action':'new comparison','source':'round13-fixed.json'})
    for q in round14['questions']:
        if q['status']=='answered' and not q.get('revisits'):
            rows.append(deepcopy(q));audit.append({'id':q['id'],'action':'new component comparison','source':'round14-isolation.json'})
    by_id={r['id']:r for r in rows}
    overrides={o['replacement_id']:o for o in round14.get('evidence_overrides',[])}
    for q in round14['questions']:
        if q['status']!='answered' or not q.get('revisits'):continue
        row=by_id[q['revisits']];winner=align_answer(row,q);old=row['winner'];changed=old!=winner
        override=overrides.get(q['id'])
        if changed and not override:raise ValueError('Changed answer needs explicit override')
        if override and (override['source_id']!=row['id'] or override['winner']!=q['winner']):raise ValueError('Override mismatch')
        row.setdefault('clarification_history',[]).append({'clarification_id':q['id'],
            'winner_in_source_order':winner,'strength':q.get('strength'),'raw_answer':q.get('raw_answer'),
            'effect':'correction' if changed else 'confirmation'})
        if changed:
            row['prior_answer']={k:deepcopy(row.get(k)) for k in ('winner','strength','raw_answer','status')}
            row['winner']=winner;row['strength']=q.get('strength')
            row['current_answer_source']=q['id'];row['current_raw_answer']=q.get('raw_answer')
        audit.append({'id':row['id'],'clarification_id':q['id'],
                      'action':'correction' if changed else 'confirmation','old_winner':old,'current_winner':winner})
    seen=set()
    for r in rows:
        key=frozenset((tuple(r['a']),tuple(r['b'])))
        if key in seen:raise ValueError(f'Duplicate pair: {r["id"]}')
        seen.add(key)
    assert initial==158 and len(rows)==183
    assert len(by_id)==len(rows)
    return rows,audit


def evaluate(rows):
    x,y,g=models.get_arrays(rows,'additive')
    old_mask=np.arange(len(rows))<158
    subsets={'all':np.ones(len(rows),dtype=bool),'prior_v2':old_mask,
             'round13':np.array([r['id'].startswith('round13-') for r in rows]),
             'isolation_components':np.array([r['id'].startswith('round14-') for r in rows])}
    runs={'v2_evidence_control':[],'v3_evidence_candidate':[]};selections=[]
    # Both trained anew within each outer fold; saved baseline models are NOT refit.
    for seed in models.SEEDS:
        predictions={name:np.zeros(len(y),dtype=int) for name in runs}
        for fold,(train,test) in enumerate(base.folds(g,5,seed)):
            for name in runs:
                tr=train[old_mask[train]] if name=='v2_evidence_control' else train
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
    v2=json.loads((ROOT/'evidence-v2.json').read_text())
    r13=json.loads((ROOT/'round13-fixed.json').read_text());r14=json.loads((ROOT/'round14-isolation.json').read_text())
    rows,audit=build_evidence(v2,r13,r14)
    snapshot={'version':3,'parent':'evidence-v2.json','parent_sha256':hashes['evidence-v2.json'],
              'row_count':len(rows),'label_counts':dict(Counter(r['winner'] for r in rows)),
              'source_hashes':hashes,'reconciliation_audit':audit,
              'protocol':'158 parent observations + 19 answered Round13 + 6 fresh Round14 components; apply one correction in place; attach two confirmations, never duplicate rechecks. Q14 of Round13 excluded as unresolved. Qualitative strengths retained without numeric targets.',
              'rows':rows}
    evidence_file=ROOT/'evidence-v3.json';write_versioned(evidence_file,snapshot)
    cv=evaluate(rows);x,y,g=models.get_arrays(rows,'additive')
    cfg=objectives.select(x,y,g,'additive',401)
    beta=objectives.fit(x,y,'additive',cfg['alpha'],cfg['pooling']);margin=x@beta;pred=base.classify(margin,cfg['threshold'])
    highlights={'round13-6','round13-9','round13-20'}
    candidate={**cfg,'feature_names':base.FEATURES,'coefficients':beta.tolist(),
               'in_sample':base.metrics(y,pred),
               'constraint_audit':{'strict_rank_sign_violations':int(np.sum((y!=0)&(y*margin<=1e-8))),
                                   'ties_not_exactly_equal':int(np.sum((y==0)&(abs(margin)>1e-8)))},
               'target_predictions':[{'id':r['id'],'answer':r['winner'],'answer_source':r.get('current_answer_source',r['id']),
                    'prediction':{-1:'B',0:'tie',1:'A'}[int(pred[i])],'margin':float(margin[i])}
                    for i,r in enumerate(rows) if r['id'] in highlights]}
    old_cfg=json.loads((ROOT/'objective-comparison-v2.json').read_text())['candidates_fit_all_158']['additive']
    old_beta=np.array(old_cfg['coefficients']);old_pred=base.classify(x[158:]@old_beta,old_cfg['threshold'])
    e_pred=np.array([base.LABEL[production._winner(production.utility(*r['a']),production.utility(*r['b']))] for r in rows[158:]])
    saved_baselines={}
    for name,pp in [('frozen_v2_additive',old_pred),('revision_e',e_pred)]:
        saved_baselines[name]={'round13_corrected_labels':base.metrics(y[158:177],pp[:19]),
                               'six_isolation_components':base.metrics(y[177:],pp[19:]),
                               'scope':'Descriptive rescoring, not new prospective accuracy; original frozen Round13 score remains unchanged.'}
    result={'method':{'evidence_version':3,'evidence_file':evidence_file.name,
                       'evidence_sha256':hashlib.sha256(evidence_file.read_bytes()).hexdigest(),
                       'rows':len(rows),'features':'unchanged 18-parameter additive','objective':'unchanged squared ranking hinge + squared tie gaps + ridge',
                       'validation':'5 outer grouped folds x 5 seeds, inner 3 grouped folds; same selection grids and seeds. Compare newly trained v2-evidence control vs v3-evidence candidate on IDENTICAL outer test families. Saved model coefficients are never edited.',
                       'limits':'Repeated nonrandom evidence, no pristine holdout. Weak monotonicity; soft tie penalty does not ensure exact price equality. Rechecks never add independent weight.',
                       'historical_file_hashes':hashes},
            'nested_cv':cv,'candidate_fit_all_183':candidate,
            'hard_feasibility':objectives.hard_feasibility(x,y),
            'identical_feature_conflicts':objectives.feature_conflicts(rows,x,y),
            'unchanged_baseline_rescoring':saved_baselines}
    write_versioned(ROOT/'additive-comparison-v3.json',result)
    for f,h in hashes.items():assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h,f
    print(json.dumps({'labels':snapshot['label_counts'],'cv_all':{k:v['all'] for k,v in cv['summary'].items()},
                      'candidate_settings':cfg,'candidate_fit':candidate['in_sample']['matched'],
                      'targets':candidate['target_predictions'],'baselines_unchanged':True},indent=2))

if __name__=='__main__':main()
