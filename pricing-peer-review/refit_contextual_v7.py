"""Evidence v7 and an exact-tare contextual refit; historical baselines read-only."""
from collections import Counter
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import numpy as np
import compare_models as base
import compare_interactions as common
import compare_tare_models as soft
import compare_exact_tare_ties as hard
from reconcile_and_compare import align_answer,write_versioned

ROOT=Path(__file__).resolve().parent
SOURCES=('pricing.py','compare_models.py','compare_interactions.py','compare_objectives.py',
         'compare_tare_models.py','compare_exact_tare_ties.py','tare-model-comparison.json',
         'exact-tare-comparison.json','evidence-v6.json','additive-comparison-v6.json',
         'round21-fixed.json','round22-isolation.json')


def build_evidence(v6,round21,round22):
    rows=deepcopy(v6['rows']);audit=[]
    for q in round21['questions']:
        if q['status']!='answered' or q.get('winner') not in ('A','B','tie'):raise ValueError('Round21 incomplete')
        rows.append(deepcopy(q));audit.append({'id':q['id'],'action':'new comparison'})
    for q in round22['questions']:
        if q['status']=='answered' and not q.get('revisits'):
            rows.append(deepcopy(q));audit.append({'id':q['id'],'action':'new component comparison'})
    by_id={r['id']:r for r in rows}
    for q in round22['questions']:
        if q['status']!='answered':raise ValueError('Isolation incomplete')
        if not q.get('revisits'):continue
        source=by_id[q['revisits']];winner=align_answer(source,q)
        if winner!=source['winner']:raise ValueError('Unexpected correction needs explicit handling')
        source.setdefault('clarification_history',[]).append({'clarification_id':q['id'],
             'winner_in_source_order':winner,'strength':q.get('strength'),'raw_answer':q.get('raw_answer'),'effect':'confirmation'})
        audit.append({'id':source['id'],'action':'confirmation','clarification_id':q['id']})
    assert len(v6['rows'])==281 and len(rows)==310
    assert rows[:281]==v6['rows']
    assert len(by_id)==len(rows)
    if len({frozenset((tuple(r['a']),tuple(r['b']))) for r in rows})!=len(rows):raise ValueError('Duplicate pair')
    assert Counter(a['action'] for a in audit)=={'new comparison':20,'new component comparison':9,'confirmation':1}
    return rows,audit


def forced_rank_conflicts(rows,x,y):
    fixed=hard.fixed_steps(x,y);out=[]
    for i,r in enumerate(rows):
        if y[i]==0:continue
        support=abs(x[i])>1e-10
        if np.any(support) and np.all(fixed[support]):
            out.append({'id':r['id'],'a':r['a'],'b':r['b'],'answer':r['winner'],
                        'effect':'Hard equality constraints from shared shade/vintage tare steps force this strict-preference score gap to zero. Evidence is retained and counted as a miss.'})
    return out


def evaluate(rows):
    x,y,g=soft.arrays(rows,'context_steps');old=np.arange(len(rows))<281
    masks=soft.masks(rows);masks.update({'prior_v6':old,'round21':(np.arange(len(rows))>=281)&(np.arange(len(rows))<301),'new_isolation':np.arange(len(rows))>=301})
    runs={'v6_evidence_control':[],'v7_evidence_candidate':[]};selections=[]
    for seed in common.SEEDS:
        pred={name:np.zeros(len(y),dtype=int) for name in runs}
        for fold,(train,test) in enumerate(base.folds(g,5,seed)):
            for name in runs:
                tr=train[old[train]] if name=='v6_evidence_control' else train
                assert not set(g[tr])&set(g[test])
                cfg=hard.select(x[tr],y[tr],g[tr],seed+fold+1000)
                beta=hard.fit(x[tr],y[tr],cfg['alpha'],cfg['pooling'])
                pred[name][test]=base.classify(x[test]@beta,cfg['threshold'])
                selections.append({'seed':seed,'fold':fold,'model':name,'train_n':len(tr),
                                   'fixed_step_count':int(sum(hard.fixed_steps(x[tr],y[tr]))),**cfg})
            print(f'Completed v7 matched-family seed {seed}, fold {fold+1}/5',flush=True)
        for name,pp in pred.items():runs[name].append({'seed':seed,'predictions':pp.tolist(),'metrics':{k:base.metrics(y[v],pp[v]) for k,v in masks.items()}})
    return {'row_ids':[r['id'] for r in rows],'groups':len(set(g)),'summary':{n:soft.summarize(v) for n,v in runs.items()},'runs':runs,'selections':selections}


def main():
    hashes={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in SOURCES}
    v6=json.loads((ROOT/'evidence-v6.json').read_text());r21=json.loads((ROOT/'round21-fixed.json').read_text());r22=json.loads((ROOT/'round22-isolation.json').read_text())
    rows,audit=build_evidence(v6,r21,r22)
    snapshot={'version':7,'parent':'evidence-v6.json','parent_sha256':hashes['evidence-v6.json'],
              'row_count':len(rows),'label_counts':dict(Counter(r['winner'] for r in rows)),
              'source_hashes':hashes,'reconciliation_audit':audit,
              'protocol':'281 parent + 20 completed Round21 answers + 9 distinct Round22 component pairs. Q11 review and Q8 confirmation add no duplicate weight. No label changes; all history preserved.','rows':rows}
    path=ROOT/'evidence-v7.json';write_versioned(path,snapshot)
    x,y,g=soft.arrays(rows,'context_steps');conflicts=forced_rank_conflicts(rows,x,y)
    print('Strict preferences forced to tie by the shared-curve constraints:',[r['id'] for r in conflicts],flush=True)
    cv=evaluate(rows)
    cfg=hard.select(x,y,g,401);beta=hard.fit(x,y,cfg['alpha'],cfg['pooling']);margin=x@beta;pred=base.classify(margin,cfg['threshold'])
    masks=soft.masks(rows);focus={'round21-3','round21-8','round21-11','round21-12','round14-2'}
    candidate={**cfg,'feature_names':soft.names('context_steps'),'coefficients':beta.tolist(),
               'fixed_step_indices':np.flatnonzero(hard.fixed_steps(x,y)).tolist(),
               'in_sample':base.metrics(y,pred),
               'pure_tare_tie_audit':{'n':int(sum(masks['confirmed_pure_tare_ties'])),
                                      'exact_score_equalities':int(sum(abs(margin[masks['confirmed_pure_tare_ties']])<1e-7))},
               'target_predictions':[{'id':r['id'],'answer':r['winner'],
                    'prediction':{-1:'B',0:'tie',1:'A'}[int(pred[i])],'margin':float(margin[i]),'exact_score_equality':bool(abs(margin[i])<1e-7)} for i,r in enumerate(rows) if r['id'] in focus]}
    previous=json.loads((ROOT/'exact-tare-comparison.json').read_text())['candidate_fit_all_281']
    old_pred=base.classify(x[281:]@np.array(previous['coefficients']),previous['threshold'])
    linear=json.loads((ROOT/'additive-comparison-v6.json').read_text())['candidate_fit_all_281']
    linear_x=np.array([base.features(r['a'])-base.features(r['b']) for r in rows[281:]])
    linear_pred=base.classify(linear_x@np.array(linear['coefficients']),linear['threshold'])
    baselines={}
    for name,pp in [('frozen_contextual',old_pred),('frozen_additive_v6',linear_pred)]:
        baselines[name]={'round21':base.metrics(y[281:301],pp[:20]),'nine_components':base.metrics(y[301:],pp[20:]),'scope':'Original round21 score reproduced; isolation is adaptive, not fresh validation.'}
    result={'method':{'evidence_version':7,'evidence_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                      'structure':'Unchanged 117-parameter shade/vintage contextual tare curve shared across provenances; same hard training tare-tie constraints and weak monotonicity',
                      'validation':'Five repeated outer 5-family/inner 3-family folds. Identical outer test rows for new fold-trained v6-evidence control and v7-evidence candidate. Only training labels fix steps and select hyperparameters.',
                      'limits':'Exploratory adaptive evidence; no pristine holdout. Shared curves can force confirmed strict preferences to zero when another provenance ties; conflicts explicitly audited, not removed. No promotion.',
                      'historical_file_hashes':hashes},'nested_cv':cv,'candidate_fit_all_310':candidate,
            'forced_rank_conflicts':conflicts,'unchanged_baseline_rescoring':baselines}
    write_versioned(ROOT/'contextual-comparison-v7.json',result)
    for f,h in hashes.items():assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h,f
    print(json.dumps({'labels':snapshot['label_counts'],'cv_all':{k:v['all'] for k,v in cv['summary'].items()},'settings':cfg,'targets':candidate['target_predictions'],'baselines_unchanged':True},indent=2))

if __name__=='__main__':main()
