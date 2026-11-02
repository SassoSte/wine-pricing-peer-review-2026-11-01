"""Incorporate direct materiality answers after preserving the frozen test receipt."""
from pathlib import Path
from copy import deepcopy
from collections import Counter
import hashlib,json
import numpy as np
import build_meaningful_benchmark as benchmark
from reconcile_and_compare import write_versioned

ROOT=Path(__file__).resolve().parent


def main():
    names=['evidence-v13.json','benchmark-targets-v13.json','meaningful-benchmark-v13.json','round35-fixed.json','build_meaningful_benchmark.py','compare_models.py','refit_meaningful_benchmark_v14.py']
    hashes={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in names}
    parent=json.loads((ROOT/'evidence-v13.json').read_text());test=json.loads((ROOT/'round35-fixed.json').read_text())
    assert len(test['questions'])==12 and all(q['status']=='answered' for q in test['questions'])
    assert hashlib.sha256(json.dumps([{k:q[k] for k in test['freeze_fields']} for q in test['questions']],sort_keys=True).encode()).hexdigest()==test['questions_and_predictions_sha256']
    rows=deepcopy(parent['rows']);seen={frozenset((tuple(q['a']),tuple(q['b']))) for q in rows}
    for q in test['questions']:
        pair=frozenset((tuple(q['a']),tuple(q['b'])));assert pair not in seen;seen.add(pair)
        label={'meaningful_A':'A','meaningful_B':'B','no_meaningful_difference':'practical_similarity'}[q['materiality']]
        rows.append({'id':q['id'],'a':q['a'],'b':q['b'],'winner':label,'judgment_type':'strict_preference' if label in ('A','B') else 'practical_similarity','direction':q['direction'],'strength':None,'status':'answered','raw_answer':q['raw_answer'],'explicit_materiality':q['materiality'],'exact_price_instruction':q['exact_price_instruction'],'answer_interpretation':q.get('interpretation'),'evidence_source':'round35-fixed.json'})
    assert len(rows)==413 and rows[:401]==parent['rows']
    ev={'version':14,'parent':'evidence-v13.json','parent_sha256':hashes['evidence-v13.json'],'row_count':413,'label_counts':dict(Counter(q['winner'] for q in rows)),'source_hashes':hashes,'unresolved_pairs':deepcopy(parent['unresolved_pairs']),'prospective_receipt':{'file':'round35-fixed.json','sha256':hashes['round35-fixed.json'],'matched':test['scores']['matched'],'n':test['scores']['n'],'scope':'Frozen v13 benchmark only. New v14 fit sees these answers, so its consistency on them is training performance.'},'protocol':'401 parent pairs unchanged plus12 fresh answered pairs, including11 direct meaningful directions and1 direct practical similarity. No reinterpretation of older ambiguous exact equalities. Original Q7/Q11 remain unresolved.','rows':rows}
    write_versioned(ROOT/'evidence-v14.json',ev)
    targets=benchmark.target_view(rows)
    for row,target in zip(rows,targets):
        if 'explicit_materiality' in row:
            target['materiality_target']={'meaningful_A':1,'meaningful_B':-1,'no_meaningful_difference':0}[row['explicit_materiality']]
            target['basis']='direct meaningfulness response in frozen Round35; not an adjective-derived proxy'
    view={'evidence':'evidence-v14.json','evidence_sha256':hashlib.sha256((ROOT/'evidence-v14.json').read_bytes()).hexdigest(),'source_hashes':hashes,'protocol':'Same partial target construction as v13, with explicit materiality taking precedence for12 new answers. Strong older qualifiers remain flagged proxies;229 direction-only cases remain unspecified.','materiality_counts':dict(Counter('unspecified' if r['materiality_target'] is None else 'no_meaningful_difference' if r['materiality_target']==0 else 'meaningful_direct_or_proxy' for r in targets)),'rows':targets}
    write_versioned(ROOT/'benchmark-targets-v14.json',view)
    x,m,d,g=benchmark.arrays(targets);scores={};choice=None;best=None
    for alpha in benchmark.ALPHAS:
        margins=np.zeros(len(rows))
        for tr,va in benchmark.base.folds(g,3,1301):margins[va]=x[va]@benchmark.fit([targets[i] for i in tr],alpha)
        for radius in benchmark.RADII:
            metrics=benchmark.materiality_metrics(m,benchmark.predict(margins,radius));metrics['meaningful_direct_or_proxy_n']=metrics.pop('meaningful_proxy_n');key=(round(metrics['balanced_accuracy'],12),round(metrics['accuracy'],12),alpha,radius);scores[f'{alpha}/{radius}']=metrics
            if best is None or key>best:best=key;choice=(alpha,radius)
    alpha,radius=choice;beta=benchmark.fit(targets,alpha);prediction=benchmark.predict(x@beta,radius)
    updated={'status':'same18-coefficient benchmark refit after frozen test; not independently validated','evidence':'evidence-v14.json','target_view':'benchmark-targets-v14.json','source_hashes':hashes,'alpha':alpha,'decision_radius':radius,'coefficients':beta.tolist(),'feature_names':benchmark.base.FEATURES,'architecture':'Unchanged18-coefficient monotone additive benchmark; same loss and calibration grid as v13.','inner_calibration_scores':scores,'frozen_v13_test_receipt':ev['prospective_receipt'],'new_rows_training_consistency':{'n':12,'matched':int(sum(prediction[401:]==m[401:])),'note':'Training consistency only; does not replace frozen8/12 result.'},'next':'Obtain price/reference-value anchors to define economically meaningful differences; no new architecture sweep.'}
    write_versioned(ROOT/'meaningful-benchmark-v14.json',updated)
    for f,h in hashes.items():assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h,f
    print(json.dumps({'rows':len(rows),'labels':ev['label_counts'],'materiality':view['materiality_counts'],'historical_frozen_score':test['scores']['matched'],'same_model_training_consistency':updated['new_rows_training_consistency'],'radius':radius}))

if __name__=='__main__':main()
