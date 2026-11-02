"""Training-only exact tare-equality constraint ablation; soft and old models untouched."""
import hashlib
import json
import numpy as np
from scipy.optimize import minimize, LinearConstraint
import compare_tare_models as soft
import compare_models as base
import compare_interactions as common
import compare_objectives as objective
from reconcile_and_compare import write_versioned

ROOT=soft.ROOT


def fixed_steps(x,y):
    pure=(y==0)&np.all(abs(x[:,:17])<=1e-10,axis=1)
    fixed=np.any(abs(x[pure])>1e-10,axis=0) if np.any(pure) else np.zeros(x.shape[1],dtype=bool)
    assert not np.any(fixed[:17])
    return fixed


def fit(x,y,alpha,rho):
    r=soft.penalty('context_steps',rho);gram=r.T@r;n=x.shape[1]
    fixed=fixed_steps(x,y)
    bounds=[(None,None)]*9+[(0.,0.) if fixed[j] else (0.,None) for j in range(9,n)]
    result=minimize(objective.objective,np.zeros(n),args=(x,y,gram,alpha),jac=True,
                    method='SLSQP',bounds=bounds,
                    constraints=[LinearConstraint(soft.CONSTRAINTS['context_steps'],0,np.inf)],
                    options={'ftol':1e-9,'maxiter':1000})
    if not result.success:raise RuntimeError(result.message)
    if np.min(soft.CONSTRAINTS['context_steps']@result.x)<-1e-6:raise RuntimeError('Monotonicity failed')
    assert np.all(abs(result.x[fixed])<1e-8)
    return result.x


def select(x,y,g,seed):
    best=None;chosen=None
    for alpha in common.ALPHAS:
        for rho in common.POOLING:
            margin=np.zeros(len(y))
            for tr,va in base.folds(g,3,seed):margin[va]=x[va]@fit(x[tr],y[tr],alpha,rho)
            for t in base.THRESHOLDS:
                metric=base.metrics(y,base.classify(margin,t))
                key=(round(metric['balanced_accuracy'],12),round(metric['accuracy'],12),alpha,rho,-t)
                if best is None or key>best:
                    best=key;chosen={'alpha':alpha,'pooling':rho,'threshold':t,'inner_balanced_accuracy':metric['balanced_accuracy']}
    return chosen


def main():
    paths=('pricing.py','compare_models.py','compare_interactions.py','compare_objectives.py',
           'compare_tare_models.py','tare-model-comparison.json','evidence-v6.json','additive-comparison-v6.json')
    hashes={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in paths}
    rows=json.loads((ROOT/'evidence-v6.json').read_text())['rows'];old=json.loads((ROOT/'tare-model-comparison.json').read_text())
    x,y,g=soft.arrays(rows,'context_steps');masks=soft.masks(rows);runs=[];selections=[]
    for seed in common.SEEDS:
        pred=np.zeros(len(y),dtype=int)
        for fold,(tr,te) in enumerate(base.folds(g,5,seed)):
            cfg=select(x[tr],y[tr],g[tr],seed+fold+1000)
            beta=fit(x[tr],y[tr],cfg['alpha'],cfg['pooling'])
            pred[te]=base.classify(x[te]@beta,cfg['threshold'])
            selections.append({'seed':seed,'fold':fold,**cfg,'fixed_step_count':int(sum(fixed_steps(x[tr],y[tr])))})
            print(f'Completed exact-tare training constraints seed {seed}, fold {fold+1}/5',flush=True)
        runs.append({'seed':seed,'predictions':pred.tolist(),'metrics':{k:base.metrics(y[v],pred[v]) for k,v in masks.items()}})
    cfg=select(x,y,g,401);beta=fit(x,y,cfg['alpha'],cfg['pooling']);margin=x@beta;pred=base.classify(margin,cfg['threshold'])
    focus={r['id'] for i,r in enumerate(rows) if masks['pure_tare'][i]}|{'round19-14','round19-15','round19-20'}
    result={'method':{'constraint':'Fix to zero only the context-specific tare increments traversed by exact tare-only ties present in each TRAINING fold. No held-out labels used. Same shade/age monotonicity, loss, grids, folds, and pooling as soft context candidate.',
                      'scope':'Only pure-tare equalities hard-enforced; provenance offset ties and other exact ties remain soft. Unseen contexts are not declared equal. Experimental ablation, not fresh prospective validation.',
                      'preserved_file_hashes':hashes},
            'nested_cv':{'summary':soft.summarize(runs),'runs':runs,'selections':selections,'row_ids':[r['id'] for r in rows]},
            'prior_candidate_summaries':old['nested_cv']['summary'],
            'candidate_fit_all_281':{**cfg,'feature_names':soft.names('context_steps'),'coefficients':beta.tolist(),
               'fixed_step_indices':np.flatnonzero(fixed_steps(x,y)).tolist(),'in_sample':base.metrics(y,pred),
               'diagnostics':[{'id':r['id'],'answer':r['winner'],'prediction':{-1:'B',0:'tie',1:'A'}[int(pred[i])],
                              'margin':float(margin[i]),'exact_score_equality':bool(abs(margin[i])<1e-7)} for i,r in enumerate(rows) if r['id'] in focus]}}
    write_versioned(ROOT/'exact-tare-comparison.json',result)
    for f,h in hashes.items():assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h,f
    print(json.dumps(result['nested_cv']['summary'],indent=2))

if __name__=='__main__':main()
