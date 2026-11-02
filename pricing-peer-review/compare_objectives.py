"""Ranking-margin versus squared-target objective, with unchanged feature families.
Run OPENBLAS_NUM_THREADS=1 python3 compare_objectives.py. Writes only new results.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import numpy as np
from scipy.optimize import minimize, linprog
import compare_models as base
import compare_interactions as models

ROOT=Path(__file__).resolve().parent
FROZEN=(*models.FROZEN,'compare_interactions.py','interaction-comparison.json')
EVIDENCE=('comparisons.json','round9-fixed.json','round10-fixed.json','round11-isolation.json')


def objective(beta,x,y,gram,alpha):
    """Strict rankings: squared hinge; exact ties: squared score difference.
    Margin 1 is an arbitrary learning scale, not a price or verbal-strength size.
    """
    margins=x@beta
    ranking=y!=0
    slack=np.maximum(0.,1-y[ranking]*margins[ranking])
    residual=np.zeros(len(y))
    residual[ranking]=-y[ranking]*slack
    residual[~ranking]=margins[~ranking]
    value=float(slack@slack + margins[~ranking]@margins[~ranking] + alpha*beta@gram@beta)
    gradient=2*x.T@residual+2*alpha*gram@beta
    return value,gradient


def fit(x,y,family,alpha,rho):
    r=models.penalty(family,rho);gram=r.T@r
    bounds=[(None,None)]*9+[(0.,None)]*(x.shape[1]-9)
    result=minimize(objective,np.zeros(x.shape[1]),args=(x,y,gram,alpha),
                    jac=True,method='L-BFGS-B',bounds=bounds,
                    options={'ftol':1e-12,'gtol':1e-7,'maxiter':4000,'maxls':40})
    if not result.success:raise RuntimeError(result.message)
    # Audit first-order optimality, allowing numerical tolerance at active bounds.
    _,grad=objective(result.x,x,y,gram,alpha)
    projected=grad.copy()
    active=(result.x[9:]<=1e-8)&(grad[9:]>0)
    projected[9:][active]=0
    if np.max(np.abs(projected))>2e-3:raise RuntimeError('Optimization did not converge adequately')
    return result.x


def select(x,y,g,family,seed):
    best=None;selected=None
    for alpha in models.ALPHAS:
        for rho in ((1.,) if family=='additive' else models.POOLING):
            margins=np.zeros(len(y))
            for tr,va in base.folds(g,3,seed):margins[va]=x[va]@fit(x[tr],y[tr],family,alpha,rho)
            for threshold in base.THRESHOLDS:
                m=base.metrics(y,base.classify(margins,threshold))
                key=(round(m['balanced_accuracy'],12),round(m['accuracy'],12),alpha,rho,-threshold)
                if best is None or key>best:
                    best=key;selected={'alpha':alpha,'pooling':rho,'threshold':threshold,
                                       'inner_balanced_accuracy':m['balanced_accuracy']}
    return selected


def hard_feasibility(x,y):
    rank=y!=0;tie=~rank
    result=linprog(np.zeros(x.shape[1]),A_ub=-y[rank,None]*x[rank],b_ub=-np.ones(int(sum(rank))),
                   A_eq=x[tie] if np.any(tie) else None,b_eq=np.zeros(int(sum(tie))) if np.any(tie) else None,
                   bounds=[(None,None)]*9+[(0,None)]*(x.shape[1]-9),method='highs')
    if result.status not in (0,2):raise RuntimeError(result.message)
    return {'feasible':result.success,'solver_status':int(result.status),'message':result.message,
            'constraint_scope':'All observed strict directions with margin >=1, exact equality for ties, nonnegative age/shade/tare increments. Homogeneous scaling makes margin 1 equivalent to existence of strict positive margins.'}


def feature_conflicts(rows,x,y):
    groups={}
    for i,vec in enumerate(x):
        nz=np.flatnonzero(abs(vec)>1e-10);sgn=1 if not len(nz) or vec[nz[0]]>0 else -1
        key=tuple(np.round(vec*sgn,10));groups.setdefault(key,[]).append((i,int(y[i]*sgn)))
    result=[]
    for values in groups.values():
        if len({v for _,v in values})>1:
            result.append([{'id':rows[i]['id'],'observed':rows[i]['winner'],'a':rows[i]['a'],'b':rows[i]['b'],'canonical_label':v} for i,v in values])
    return result


def run_cv(rows):
    arrays={f:models.get_arrays(rows,f) for f in models.FAMILIES};_,y,g=arrays['additive']
    diag=np.array([r['id'].startswith('round11-') for r in rows]);runs={f:[] for f in models.FAMILIES};selections=[]
    for seed in models.SEEDS:
        predictions={f:np.zeros(len(y),dtype=int) for f in models.FAMILIES}
        for fold,(tr,te) in enumerate(base.folds(g,5,seed)):
            for family,(x,_,_) in arrays.items():
                cfg=select(x[tr],y[tr],g[tr],family,seed+fold+1000)
                beta=fit(x[tr],y[tr],family,cfg['alpha'],cfg['pooling'])
                predictions[family][te]=base.classify(x[te]@beta,cfg['threshold'])
                selections.append({'seed':seed,'fold':fold,'family':family,**cfg})
        for f,pred in predictions.items():
            runs[f].append({'seed':seed,'all':base.metrics(y,pred),
                            'pre_isolation':base.metrics(y[~diag],pred[~diag]),
                            'isolation':base.metrics(y[diag],pred[diag]),'predictions':pred.tolist()})
        print(f'Completed direct-ranking validation seed {seed}',flush=True)
    return {'summary':{f:models.summary(v) for f,v in runs.items()},'runs':runs,
            'selections':selections,'row_ids':[r['id'] for r in rows],'groups':len(set(g))}


def main():
    hashes={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in FROZEN+EVIDENCE}
    rows=models.load_rows();old=json.loads((ROOT/'interaction-comparison.json').read_text())
    assert old['nested_cv']['row_ids']==[r['id'] for r in rows]
    feasibility={}
    for f in models.FAMILIES:
        x,y,_=models.get_arrays(rows,f)
        feasibility[f]={'hard_constraints':hard_feasibility(x,y),'identical_feature_conflicts':feature_conflicts(rows,x,y)}
    print('Hard-constraint feasibility:',{f:v['hard_constraints']['feasible'] for f,v in feasibility.items()},flush=True)
    cv=run_cv(rows);candidates={}
    ids={'round11-14','round11-15','round11-16','round11-17','round11-18','round11-19','round11-20'}
    for f in models.FAMILIES:
        x,y,g=models.get_arrays(rows,f);cfg=select(x,y,g,f,401);beta=fit(x,y,f,cfg['alpha'],cfg['pooling'])
        margin=x@beta;pred=base.classify(margin,cfg['threshold'])
        candidates[f]={**cfg,'feature_names':models.names(f),'coefficients':beta.tolist(),
                       'in_sample':base.metrics(y,pred),
                       'constraint_audit':{'strict_rank_sign_violations':int(np.sum((y!=0)&(y*margin<=1e-8))),
                                           'ties_not_exactly_equal':int(np.sum((y==0)&(abs(margin)>1e-8))),
                                           'note':'A near-tie classification is not an exact fitted equality.'},
                       'diagnostic_premiums':[{'id':r['id'],'actual':r['winner'],
                         'prediction':{-1:'B',0:'tie',1:'A'}[int(pred[i])],'margin':float(margin[i])}
                         for i,r in enumerate(rows) if r['id'] in ids]}
    result={'method':{'rows':len(rows),'objective':'sum(max(0,1-y*margin)^2) for strict rankings + sum(margin^2) for exact ties + existing ridge/partial-pooling penalty',
                      'contrast':'Unlike squared targets, correctly ranked examples incur no ranking penalty once the unit margin is reached; large correct gaps are not pulled back toward 1.',
                      'constraint_status':'Soft penalties, not guaranteed hard constraints. Hard feasibility checked separately; labels not rewritten.',
                      'evaluation':'Same 5 seeds, 5 outer/3 inner withheld-family folds, feature families, alpha/pooling/threshold grids, and balanced-accuracy selection as interaction-comparison.json',
                      'limitations':'Repeated adaptive dataset and iterative model selection; no pristine holdout, no statistical certainty from split ranges. Strength labels remain uncalibrated.',
                      'preserved_file_hashes':hashes},'feasibility':feasibility,'nested_cv':cv,
            'squared_target_baseline_summary':old['nested_cv']['summary'],'candidates_fit_all_158':candidates}
    (ROOT/'objective-comparison.json').write_text(json.dumps(result,indent=2)+'\n')
    for f,digest in hashes.items():assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==digest,f
    print(json.dumps({'new_cv':cv['summary'],'training_matches':{f:v['in_sample']['matched'] for f,v in candidates.items()},'all_baselines_unchanged':True},indent=2))

if __name__=='__main__':main()
