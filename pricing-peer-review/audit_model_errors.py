"""Audit v6 out-of-fold errors without changing models or evidence."""
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import numpy as np
import compare_models as base
import compare_interactions as models
import compare_objectives as objective
from reconcile_and_compare import write_versioned

ROOT=Path(__file__).resolve().parent
ATTRS=('provenance','shade','vintage','tare')
LABEL={-1:'B',0:'tie',1:'A'}


def bucket(actual,pred):
    if actual==pred:return 'correct'
    if actual==0:return 'missed_exact_tie'
    if pred==0:return 'preference_called_tie'
    return 'opposite_winner'


def main():
    paths=('evidence-v6.json','additive-comparison-v6.json','pricing.py','compare_models.py','compare_interactions.py','compare_objectives.py')
    hashes={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in paths}
    evidence=json.loads((ROOT/'evidence-v6.json').read_text())
    result=json.loads((ROOT/'additive-comparison-v6.json').read_text())
    rows=evidence['rows'];x,y,g=models.get_arrays(rows,'additive')
    assert result['nested_cv']['row_ids']==[r['id'] for r in rows]
    selections={(s['seed'],s['fold']):s for s in result['nested_cv']['selections'] if s['model']=='v6_evidence_candidate'}
    events=[];per_row=defaultdict(list)
    for run in result['nested_cv']['runs']['v6_evidence_candidate']:
        seed=run['seed'];saved=np.array(run['predictions'])
        for fold,(train,test) in enumerate(base.folds(g,5,seed)):
            cfg=selections[(seed,fold)]
            beta=objective.fit(x[train],y[train],'additive',cfg['alpha'],cfg['pooling'])
            margins=x[test]@beta;pred=base.classify(margins,cfg['threshold'])
            np.testing.assert_array_equal(pred,saved[test])
            for i,margin,pp in zip(test,margins,pred):
                row=rows[i];kind='+'.join(ATTRS[j] for j in range(4) if row['a'][j]!=row['b'][j])
                event={'id':row['id'],'seed':seed,'fold':fold,'actual':row['winner'],
                       'prediction':LABEL[int(pp)],'error_type':bucket(int(y[i]),int(pp)),
                       'margin':float(margin),'threshold':cfg['threshold'],'contrast':kind,
                       'feature_group':g[i]}
                events.append(event);per_row[row['id']].append(event)
    repeats=len(result['nested_cv']['runs']['v6_evidence_candidate'])
    totals=Counter(e['error_type'] for e in events);errors=len(events)-totals['correct']
    def aggregate(field):
        groups=defaultdict(list)
        for event in events:groups[event[field]].append(event)
        output=[]
        for key,vals in groups.items():
            counts=Counter(e['error_type'] for e in vals)
            output.append({'category':key,'distinct_pairs':len({e['id'] for e in vals}),
                           'error_rate':1-counts['correct']/len(vals),
                           'mean_errors_per_repeat':(len(vals)-counts['correct'])/repeats,
                           'counts_over_all_repeats':dict(counts)})
        return sorted(output,key=lambda r:-r['mean_errors_per_repeat'])
    by_id={r['id']:r for r in rows};persistent=[]
    for id,vals in per_row.items():
        misses=sum(e['error_type']!='correct' for e in vals)
        if misses>=3:
            row=by_id[id]
            persistent.append({'id':id,'a':row['a'],'b':row['b'],'actual':row['winner'],
                               'misses':misses,'repeats':repeats,'contrast':vals[0]['contrast'],
                               'prediction_counts':dict(Counter(e['prediction'] for e in vals)),
                               'error_counts':dict(Counter(e['error_type'] for e in vals)),
                               'median_margin':float(np.median([e['margin'] for e in vals])),
                               'median_threshold':float(np.median([e['threshold'] for e in vals]))})
    persistent.sort(key=lambda q:(-q['misses'],q['id']))
    collisions=objective.feature_conflicts(rows,x,y)
    conflict_ids={q['id'] for group in collisions for q in group}
    conflict_stats={}
    for name,predicate in [('feature_collision',lambda e:e['id'] in conflict_ids),('no_feature_collision',lambda e:e['id'] not in conflict_ids)]:
        vals=[e for e in events if predicate(e)];nmiss=sum(e['error_type']!='correct' for e in vals)
        conflict_stats[name]={'pairs':len({e['id'] for e in vals}),'error_rate':nmiss/len(vals),'mean_errors_per_repeat':nmiss/repeats}
    # Post-hoc rule probes: descriptive only, not independently validated choices.
    threshold_probe=[]
    for threshold in (0.,.1,.2,.3,.4,.5,.65,.8):
        pred=base.classify(np.array([e['margin'] for e in events]),threshold)
        actual=np.array([base.LABEL[e['actual']] for e in events])
        threshold_probe.append({'threshold':threshold,**base.metrics(actual,pred)})
    out={'method':{'source_hashes':hashes,'rows':len(rows),'repeats':repeats,
                   'scope':'Reconstructed predictions on original outer withheld-family folds; all reconstructed labels exactly match saved v6 validation. Five repeats reuse 281 pairs, not 1405 independent observations.',
                   'limits':'Exploratory error audit; slices and threshold probes are post-hoc and not evidence of a new model improvement.'},
         'error_decomposition':{k:{'mean_per_repeat':v/repeats,'share_of_errors':v/errors if k!='correct' else None} for k,v in totals.items()},
         'persistent_miss_counts':dict(Counter(q['misses'] for q in persistent)),
         'by_contrast':aggregate('contrast'),'by_actual_label':aggregate('actual'),
         'by_family':aggregate('feature_group'),'feature_collision_stats':conflict_stats,
         'feature_collisions':collisions,'persistent_misses':persistent,
         'posthoc_threshold_probe':threshold_probe,'out_of_fold_events':events}
    write_versioned(ROOT/'error-audit-v6.json',out)
    for f,h in hashes.items():assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h,f
    print(json.dumps({k:out[k] for k in ['error_decomposition','persistent_miss_counts','by_contrast','feature_collision_stats']},indent=2))
    print('Persistent miss examples:',json.dumps(persistent[:12],indent=2))

if __name__=='__main__':main()
