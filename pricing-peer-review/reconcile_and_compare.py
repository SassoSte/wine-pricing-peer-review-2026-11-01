"""Versioned clarification reconciliation and unchanged-protocol objective rerun.
Never modifies historical evidence, model scripts, or baseline result files.
Run OPENBLAS_NUM_THREADS=1 python3 reconcile_and_compare.py
"""
from __future__ import annotations
from copy import deepcopy
from collections import Counter
import hashlib
import json
from pathlib import Path
import numpy as np
import compare_models as base
import compare_interactions as models
import compare_objectives as objectives

ROOT=Path(__file__).resolve().parent
SOURCES=(*objectives.FROZEN,*objectives.EVIDENCE,'compare_objectives.py',
         'objective-comparison.json','round12-clarification.json')



def write_versioned(path, payload):
    """Allow identical reproduction, but never silently replace a version."""
    content=json.dumps(payload,indent=2)+'\n'
    if path.exists():
        if path.read_text()!=content:
            raise FileExistsError(f'{path.name} already exists with different content; create a new version')
        return
    path.write_text(content)


def align_answer(source, clarification):
    """Validate endpoints and align the clarified label to the original A/B order."""
    if source['a']==clarification['a'] and source['b']==clarification['b']:
        return clarification['winner']
    if source['a']==clarification['b'] and source['b']==clarification['a']:
        return {'A':'B','B':'A','tie':'tie'}[clarification['winner']]
    raise ValueError(f"Clarification endpoints do not match {source['id']}")


def reconcile(original, clarification):
    rows=deepcopy(original);by_id={r['id']:r for r in rows}
    answers={q['id']:q for q in clarification['questions'] if q['status']=='answered'}
    overrides={o['replacement_id']:o for o in clarification.get('evidence_overrides',[])}
    audit=[]
    for q in answers.values():
        source_id=q['revisits']
        if source_id not in by_id:raise ValueError(f'Unknown source: {source_id}')
        source=by_id[source_id];winner=align_answer(source,q)
        old=source['winner'];changed=winner!=old
        override=overrides.get(q['id'])
        if changed and override is None:raise ValueError('Changed answer missing explicit override')
        if override is not None:
            if override['source_id']!=source_id or override['winner']!=q['winner']:
                raise ValueError('Override and clarification disagree')
        confirmation={'clarification_id':q['id'],'raw_answer':q.get('raw_answer'),
                      'winner_in_source_order':winner,'strength':q.get('strength'),
                      'effect':'correction' if changed else 'confirmation'}
        source.setdefault('clarification_history',[]).append(confirmation)
        if changed:
            source['prior_answer']={k:deepcopy(source.get(k)) for k in ('winner','strength','raw_answer','status')}
            source['winner']=winner;source['strength']=q.get('strength')
            source['current_answer_source']=q['id']
            source['current_raw_answer']=q.get('raw_answer')
        audit.append({'source_id':source_id,'clarification_id':q['id'],
                      'old_winner':old,'current_winner':winner,'changed':changed})
    if set(overrides)-set(answers):raise ValueError('Unanswered override')
    assert len(rows)==len(original) and [r['id'] for r in rows]==[r['id'] for r in original]
    assert sum(r['changed'] for r in audit)==2
    return rows,audit


def old_predictions_rescored(rows, old_result):
    _,y,_=models.get_arrays(rows,'additive')
    diag=np.array([r['id'].startswith('round11-') for r in rows])
    result={}
    for family,runs in old_result['nested_cv']['runs'].items():
        scored=[]
        for run in runs:
            p=np.array(run['predictions'])
            scored.append({'seed':run['seed'],'all':base.metrics(y,p),
                           'pre_isolation':base.metrics(y[~diag],p[~diag]),
                           'isolation':base.metrics(y[diag],p[diag])})
        result[family]={'summary':models.summary(scored),'runs':scored}
    return result


def main():
    hashes={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in SOURCES}
    original=models.load_rows();clarification=json.loads((ROOT/'round12-clarification.json').read_text())
    rows,audit=reconcile(original,clarification)
    old=json.loads((ROOT/'objective-comparison.json').read_text())
    assert old['nested_cv']['row_ids']==[r['id'] for r in rows]
    original_groups=models.get_arrays(original,'additive')[2]
    current_groups=models.get_arrays(rows,'additive')[2]
    np.testing.assert_array_equal(original_groups,current_groups)
    for seed in models.SEEDS:
        for (ot,ov),(nt,nv) in zip(base.folds(original_groups,5,seed),base.folds(current_groups,5,seed)):
            np.testing.assert_array_equal(ot,nt);np.testing.assert_array_equal(ov,nv)
    snapshot={'version':2,'source_hashes':hashes,'row_count':len(rows),
              'label_counts':dict(Counter(r['winner'] for r in rows)),
              'protocol':'Apply explicit corrections in place by original source ID; enrich confirmations with provenance; no duplicate observations or extra weights. Historical files unchanged.',
              'reconciliation_audit':audit,'rows':rows}
    evidence_path=ROOT/'evidence-v2.json';write_versioned(evidence_path,snapshot)
    feasibility={}
    for f in models.FAMILIES:
        x,y,_=models.get_arrays(rows,f)
        feasibility[f]={'hard_constraints':objectives.hard_feasibility(x,y),
                        'identical_feature_conflicts':objectives.feature_conflicts(rows,x,y)}
    cv=objectives.run_cv(rows);candidates={}
    highlighted={'round7-9','round11-14','round11-17','round11-18','round11-19','round11-20'}
    for family in models.FAMILIES:
        x,y,g=models.get_arrays(rows,family);cfg=objectives.select(x,y,g,family,401)
        beta=objectives.fit(x,y,family,cfg['alpha'],cfg['pooling']);margin=x@beta;pred=base.classify(margin,cfg['threshold'])
        candidates[family]={**cfg,'feature_names':models.names(family),'coefficients':beta.tolist(),
                            'in_sample':base.metrics(y,pred),
                            'constraint_audit':{'strict_rank_sign_violations':int(np.sum((y!=0)&(y*margin<=1e-8))),
                                                'ties_not_exactly_equal':int(np.sum((y==0)&(abs(margin)>1e-8)))},
                            'highlighted_predictions':[{'id':r['id'],'answer':r['winner'],
                             'answer_source':r.get('current_answer_source',r['id']),
                             'prediction':{-1:'B',0:'tie',1:'A'}[int(pred[i])],'margin':float(margin[i])}
                             for i,r in enumerate(rows) if r['id'] in highlighted]}
    result={'method':{'evidence_version':2,'evidence_file':'evidence-v2.json',
                      'evidence_sha256':hashlib.sha256(evidence_path.read_bytes()).hexdigest(),
                      'rows':len(rows),'corrections':2,'confirmations':13,
                      'protocol':'Same direct-ranking objective, feature families, splits, seeds, hyperparameter grids, and training-only nested selection as objective-comparison.json',
                      'limits':'Exploratory reuse of existing answers and validation families; not a fresh independent test. Soft penalties do not guarantee exact ties. Clarifications are not new independent samples.',
                      'preserved_file_hashes':hashes},
            'feasibility':feasibility,'nested_cv':cv,
            'old_result_on_old_labels':old['nested_cv']['summary'],
            'old_predictions_rescored_on_v2':old_predictions_rescored(rows,old),
            'candidates_fit_all_158':candidates}
    write_versioned(ROOT/'objective-comparison-v2.json',result)
    for f,digest in hashes.items():assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==digest,f
    print(json.dumps({'labels':snapshot['label_counts'],'new_cv':cv['summary'],
                      'training_matches':{f:v['in_sample']['matched'] for f,v in candidates.items()},
                      'hard_feasible':{f:v['hard_constraints']['feasible'] for f,v in feasibility.items()},
                      'historical_files_unchanged':True},indent=2))

if __name__=='__main__':main()
