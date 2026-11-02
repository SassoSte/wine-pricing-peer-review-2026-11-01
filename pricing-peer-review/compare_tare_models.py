"""Nonlinear tare experiments; prior models/results and evidence are read-only."""
from __future__ import annotations
import hashlib
import json
from itertools import product
from pathlib import Path
import time
import numpy as np
from scipy.optimize import minimize, LinearConstraint
import compare_models as base
import compare_interactions as models
import compare_objectives as objectives
from reconcile_and_compare import write_versioned

ROOT=Path(__file__).resolve().parent
WEIGHTS=(130,125,120,115,110)
CONTEXTS=tuple(product(base.SHADES,base.AGES))
FAMILIES=('global_steps','context_steps')


def features(option,family):
    old=base.features(option)
    if family=='linear':return old
    if family not in FAMILIES:raise ValueError(family)
    z,s,age,w=option
    steps=np.array([float(w<=v) for v in WEIGHTS[1:]])
    if family=='global_steps':return np.r_[old[:17],steps]
    return np.r_[old[:17],np.concatenate([steps if ctx==(s,age) else np.zeros(4) for ctx in CONTEXTS])]


def names(family):
    if family=='linear':return base.FEATURES
    if family=='global_steps':return base.FEATURES[:17]+[f'tare step to {w} lb' for w in WEIGHTS[1:]]
    return base.FEATURES[:17]+[f'tare step to {w} lb at {s}/{age} years' for s,age in CONTEXTS for w in WEIGHTS[1:]]


def penalty(family,rho):
    n=len(names(family));count=1 if family=='global_steps' else len(CONTEXTS)
    rows=[]
    for j in range(17):
        r=np.zeros(n);r[j]=1;rows.append(r)
    means=[]
    for step in range(4):
        r=np.zeros(n);r[17+step::4]=1/count;means.append(r)
    overall=sum(means)/4
    rows.append(overall)
    # Nonlinear global shape, in addition to the shared mean slope.
    rows.extend(mean-overall for mean in means)
    if count>1:
        for ctx in range(count):
            for step in range(4):
                r=-means[step].copy();r[17+4*ctx+step]+=1
                rows.append(np.sqrt(rho)*r)
    return np.array(rows)


def monotonic_constraints(family):
    if family!='context_steps':return np.zeros((0,len(names(family))))
    rows=[]
    for s,age,w in product(base.SHADES,base.AGES,WEIGHTS):
        before=features(['Eastern Europe',s,age,w],family)
        if age>20:rows.append(features(['Eastern Europe',s,age-5,w],family)-before)
        i=base.SHADES.index(s)
        if i<4:rows.append(features(['Eastern Europe',base.SHADES[i+1],age,w],family)-before)
    return np.unique(np.array(rows),axis=0)


CONSTRAINTS={f:monotonic_constraints(f) for f in FAMILIES}


def fit(x,y,family,alpha,rho):
    r=penalty(family,rho);gram=r.T@r;n=x.shape[1]
    bounds=[(None,None)]*9+[(0.,None)]*(n-9)
    if family=='global_steps':
        result=minimize(objectives.objective,np.zeros(n),args=(x,y,gram,alpha),jac=True,
                        method='L-BFGS-B',bounds=bounds,
                        options={'ftol':1e-12,'gtol':1e-7,'maxiter':4000,'maxls':40})
    else:
        # Start at the feasible zero score; linear inequalities preserve
        # shade/age monotonicity despite context-dependent weight curves.
        result=minimize(objectives.objective,np.zeros(n),args=(x,y,gram,alpha),jac=True,
                        method='SLSQP',bounds=bounds,
                        constraints=[LinearConstraint(CONSTRAINTS[family],0,np.inf)],
                        options={'ftol':1e-9,'maxiter':1000})
    if not result.success:raise RuntimeError(f'{family}: {result.message}')
    if len(CONSTRAINTS[family]) and np.min(CONSTRAINTS[family]@result.x)<-1e-6:
        raise RuntimeError('Monotonicity constraint failure')
    return result.x


def arrays(rows,family):
    _,y,g=models.get_arrays(rows,'additive')
    return np.array([features(r['a'],family)-features(r['b'],family) for r in rows]),y,g


def select(x,y,g,family,seed):
    best=None;chosen=None
    for alpha in models.ALPHAS:
        for rho in ((1.,) if family=='global_steps' else models.POOLING):
            margins=np.zeros(len(y))
            for tr,va in base.folds(g,3,seed):margins[va]=x[va]@fit(x[tr],y[tr],family,alpha,rho)
            for threshold in base.THRESHOLDS:
                metric=base.metrics(y,base.classify(margins,threshold))
                key=(round(metric['balanced_accuracy'],12),round(metric['accuracy'],12),alpha,rho,-threshold)
                if best is None or key>best:
                    best=key;chosen={'alpha':alpha,'pooling':rho,'threshold':threshold,
                                    'inner_balanced_accuracy':metric['balanced_accuracy']}
    return chosen


def masks(rows):
    pure=np.array([r['a'][:3]==r['b'][:3] and r['a'][3]!=r['b'][3] for r in rows])
    tied=np.array([r['winner']=='tie' for r in rows])
    return {'all':np.ones(len(rows),dtype=bool),'pure_tare':pure,
            'confirmed_pure_tare_ties':pure&tied,'pure_tare_preferences':pure&~tied,
            'provenance_plus_tare':np.array([r['a'][0]!=r['b'][0] and r['a'][1:3]==r['b'][1:3] and r['a'][3]!=r['b'][3] for r in rows])}


def summarize(runs):
    output={}
    for subset in runs[0]['metrics']:
        mm=[r['metrics'][subset] for r in runs]
        output[subset]={'n':mm[0]['n'],**{k:float(np.mean([m[k] for m in mm])) for k in ('accuracy','balanced_accuracy','opposite_winner_errors','predicted_ties')},
                       'accuracy_range':[min(m['accuracy'] for m in mm),max(m['accuracy'] for m in mm)],
                       'mean_recall':{k:float(np.mean([m['recall'][k] for m in mm if k in m['recall']])) for k in base.LABEL if any(k in m['recall'] for m in mm)}}
    return output


def evaluate(rows,previous):
    data={f:arrays(rows,f) for f in FAMILIES};_,y,g=data['global_steps'];subsets=masks(rows)
    assert previous['nested_cv']['row_ids']==[r['id'] for r in rows]
    # Exact saved outer predictions of the v6 model family; no in-sample scoring.
    runs={'linear_v6':[],'global_steps':[],'context_steps':[]};selections=[]
    for old in previous['nested_cv']['runs']['v6_evidence_candidate']:
        pred=np.array(old['predictions'])
        runs['linear_v6'].append({'seed':old['seed'],'metrics':{k:base.metrics(y[v],pred[v]) for k,v in subsets.items()},'predictions':pred.tolist()})
    for seed in models.SEEDS:
        pred={f:np.zeros(len(y),dtype=int) for f in FAMILIES}
        for fold,(tr,te) in enumerate(base.folds(g,5,seed)):
            for family,(x,_,_) in data.items():
                cfg=select(x[tr],y[tr],g[tr],family,seed+fold+1000)
                beta=fit(x[tr],y[tr],family,cfg['alpha'],cfg['pooling'])
                pred[family][te]=base.classify(x[te]@beta,cfg['threshold'])
                selections.append({'seed':seed,'fold':fold,'family':family,**cfg})
            print(f'Completed nonlinear tare seed {seed}, fold {fold+1}/5',flush=True)
        for family,pp in pred.items():runs[family].append({'seed':seed,'metrics':{k:base.metrics(y[v],pp[v]) for k,v in subsets.items()},'predictions':pp.tolist()})
    return {'row_ids':[r['id'] for r in rows],'groups':len(set(g)),'summary':{f:summarize(v) for f,v in runs.items()},'runs':runs,'selections':selections}


def main():
    paths=('pricing.py','compare_models.py','compare_interactions.py','compare_objectives.py',
           'refit_additive_v6.py','evidence-v6.json','additive-comparison-v6.json')
    hashes={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in paths}
    rows=json.loads((ROOT/'evidence-v6.json').read_text())['rows']
    previous=json.loads((ROOT/'additive-comparison-v6.json').read_text())
    cv=evaluate(rows,previous);candidates={};subset=masks(rows)
    focus={r['id'] for i,r in enumerate(rows) if subset['pure_tare'][i]}|{'round19-14','round19-15','round19-20'}
    for family in FAMILIES:
        x,y,g=arrays(rows,family);cfg=select(x,y,g,family,401)
        beta=fit(x,y,family,cfg['alpha'],cfg['pooling']);margin=x@beta;pred=base.classify(margin,cfg['threshold'])
        candidate={**cfg,'feature_names':names(family),'coefficients':beta.tolist(),'in_sample':base.metrics(y,pred),
                   'diagnostics':[{'id':r['id'],'a':r['a'],'b':r['b'],'answer':r['winner'],
                    'prediction':{-1:'B',0:'tie',1:'A'}[int(pred[i])],'margin':float(margin[i]),
                    'exact_score_equality':bool(abs(margin[i])<=1e-7)} for i,r in enumerate(rows) if r['id'] in focus]}
        if family=='context_steps':candidate['minimum_monotonic_constraint']=float(np.min(CONSTRAINTS[family]@beta))
        candidates[family]=candidate
    result={'method':{'rows':len(rows),'families':{'linear_v6':'18 parameters; saved v6 outer-fold predictions reused unchanged',
                       'global_steps':'21 parameters; four shared nonnegative tare increments',
                       'context_steps':'117 parameters; four nonnegative tare increments per shade/vintage context; partial pooling toward global step curve'},
                      'constraints':'Lighter tare cannot reduce score. Linear inequalities preserve younger/lighter-shade weak monotonicity at every supported tare. Provenance remains additive, so no provenance-specific tare curve is included.',
                      'objective':'Same direct-ranking squared hinge + squared exact-tie gap penalties, with comparable ridge on global mean and extra pooling on context deviations',
                      'selection':'Same five seeds and outer 5 / inner 3 family folds, alpha/pooling/threshold grids; tune on training only. Equal-price cases receive no extra weight.',
                      'limits':'Exploratory architecture selected after error audit; nonrandom adaptive evidence, no pristine holdout. 117 parameters require strong shrinkage. Classification tie is not necessarily exact score equality. Split ranges are not confidence intervals.',
                      'preserved_file_hashes':hashes},'nested_cv':cv,'candidates_fit_all_281':candidates}
    write_versioned(ROOT/'tare-model-comparison.json',result)
    for f,h in hashes.items():assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h,f
    print(json.dumps({'summary':{f:v['all'] for f,v in cv['summary'].items()},'baselines_unchanged':True},indent=2))

if __name__=='__main__':main()
