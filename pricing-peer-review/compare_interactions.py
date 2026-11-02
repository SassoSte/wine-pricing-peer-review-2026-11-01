"""Partially pooled provenance interactions; existing models/evidence are read-only.
Run OPENBLAS_NUM_THREADS=1 python3 compare_interactions.py (NumPy/SciPy required).
"""
from __future__ import annotations
import hashlib
import json
from collections import Counter
from pathlib import Path
import numpy as np
from scipy.optimize import lsq_linear
import compare_models as base
import pricing as production

ROOT=Path(__file__).resolve().parent
FAMILIES=('additive','shade','vintage')
ALPHAS=(.1,1.,10.)
POOLING=(1.,10.,100.)
SEEDS=(11,29,47,71,103)
FROZEN=('pricing.py','compare_models.py','model-comparison.json')


def load_rows():
    old,round9=base.load_rows()
    rows=old+round9
    for filename in ('round10-fixed.json','round11-isolation.json'):
        data=json.loads((ROOT/filename).read_text())
        rows += [r for r in data['questions'] if r['status']=='answered' and not r.get('revisits')]
    seen=set()
    for r in rows:
        k=frozenset((tuple(r['a']),tuple(r['b'])))
        if k in seen:raise ValueError(f'duplicate pair {r["id"]}')
        seen.add(k)
    assert len(rows)==158
    return rows


def names(family):
    if family=='additive':return base.FEATURES
    dim=base.SHADES[1:] if family=='shade' else base.AGES[1:]
    shared=[f'age increment:{y}' for y in base.AGES[1:]] if family=='shade' else [f'shade increment:{s}' for s in base.SHADES[1:]]
    return ([f'origin:{z} vs Eastern Europe' for z in base.ZONES[1:]]
            + [f'{family} increment:{v} in {z}' for z in base.ZONES for v in dim]
            + shared + ['lightness per 5 lb'])


def features(option,family):
    original=base.features(option)  # validates every input
    if family=='additive':return original
    if family not in ('shade','vintage'):raise ValueError(family)
    z=option[0];s=original[9:13];v=original[13:17]
    varying=s if family=='shade' else v
    shared=v if family=='shade' else s
    return np.r_[original[:9],np.concatenate([varying if zone==z else np.zeros(4) for zone in base.ZONES]),shared,original[-1]]


def penalty(family,rho):
    if family=='additive':return np.eye(18)
    # Penalize the global mean once, not once per zone, making shrinkage
    # comparable to the additive model. Separate penalty shrinks deviations.
    n=54;rows=[]
    for j in list(range(9))+list(range(49,54)):
        r=np.zeros(n);r[j]=1;rows.append(r)
    for step in range(4):
        mean=np.zeros(n);mean[9+step:49:4]=.1;rows.append(mean)
        for z in range(10):
            dev=-mean.copy();dev[9+4*z+step]+=1
            rows.append(np.sqrt(rho)*dev)
    return np.array(rows)


def fit(x,y,family,alpha,rho):
    n=x.shape[1];r=penalty(family,rho)
    xa=np.vstack((x,np.sqrt(alpha)*r));ya=np.r_[y,np.zeros(len(r))]
    lower=np.r_[np.full(9,-np.inf),np.zeros(n-9)]
    fitted=lsq_linear(xa,ya,bounds=(lower,np.inf),method='bvls',tol=1e-9)
    if not fitted.success:raise RuntimeError(fitted.message)
    return fitted.x


def select(x,y,g,family,seed):
    best=None;selected=None
    for alpha in ALPHAS:
        for rho in ((1.,) if family=='additive' else POOLING):
            margins=np.zeros(len(y))
            for tr,va in base.folds(g,3,seed):
                margins[va]=x[va]@fit(x[tr],y[tr],family,alpha,rho)
            for threshold in base.THRESHOLDS:
                m=base.metrics(y,base.classify(margins,threshold))
                key=(round(m['balanced_accuracy'],12),round(m['accuracy'],12),alpha,rho,-threshold)
                if best is None or key>best:
                    best=key;selected={'alpha':alpha,'pooling':rho,'threshold':threshold,
                                       'inner_balanced_accuracy':m['balanced_accuracy']}
    return selected


def get_arrays(rows,family):
    _,y,g=base.arrays(rows)
    x=np.array([features(r['a'],family)-features(r['b'],family) for r in rows])
    return x,y,g


def summary(runs):
    return {'mean_accuracy':float(np.mean([r['all']['accuracy'] for r in runs])),
            'mean_balanced_accuracy':float(np.mean([r['all']['balanced_accuracy'] for r in runs])),
            'accuracy_range':[min(r['all']['accuracy'] for r in runs),max(r['all']['accuracy'] for r in runs)],
            'mean_opposite_winner_errors':float(np.mean([r['all']['opposite_winner_errors'] for r in runs])),
            'mean_recall':{k:float(np.mean([r['all']['recall'][k] for r in runs])) for k in base.LABEL},
            'pre_isolation_accuracy':float(np.mean([r['pre_isolation']['accuracy'] for r in runs])),
            'isolation_accuracy':float(np.mean([r['isolation']['accuracy'] for r in runs]))}


def run_cv(rows):
    arrays={f:get_arrays(rows,f) for f in FAMILIES};_,y,g=arrays['additive']
    diag=np.array([r['id'].startswith('round11-') for r in rows])
    runs={f:[] for f in FAMILIES};selections=[]
    for seed in SEEDS:
        predictions={f:np.zeros(len(y),dtype=int) for f in FAMILIES}
        for fold,(tr,te) in enumerate(base.folds(g,5,seed)):
            for family,(x,_,_) in arrays.items():
                cfg=select(x[tr],y[tr],g[tr],family,seed+fold+1000)
                beta=fit(x[tr],y[tr],family,cfg['alpha'],cfg['pooling'])
                predictions[family][te]=base.classify(x[te]@beta,cfg['threshold'])
                selections.append({'seed':seed,'fold':fold,'family':family,**cfg})
        for family,pred in predictions.items():
            runs[family].append({'seed':seed,'all':base.metrics(y,pred),
                                'pre_isolation':base.metrics(y[~diag],pred[~diag]),
                                'isolation':base.metrics(y[diag],pred[diag]),
                                'predictions':pred.tolist()})
        print(f'Completed interaction validation seed {seed}',flush=True)
    return {'summary':{f:summary(v) for f,v in runs.items()},'runs':runs,'selections':selections,
            'row_ids':[r['id'] for r in rows],'groups':len(set(g))}


def frozen_predictions(rows):
    data=json.loads((ROOT/'model-comparison.json').read_text())
    out={}
    for name in ('additive_exact','additive_near_tie'):
        cfg=data['candidates_fit_all_119'][name]
        beta=np.array([cfg['coefficients'][k] for k in base.FEATURES])
        x,y,_=base.arrays(rows)
        out[name]=base.classify(x@beta,cfg['threshold'])
    out['revision_e']=np.array([base.LABEL[production._winner(production.utility(*r['a']),production.utility(*r['b']))] for r in rows])
    return out



def sensitivity(rows):
    """Training-only diagnostic; NOT model selection or independent validation."""
    ids={'round11-14','round11-17','round11-18','round11-19','round11-20'}
    indices=[i for i,r in enumerate(rows) if r['id'] in ids]
    results=[]
    for family in ('shade','vintage'):
        x,y,_=get_arrays(rows,family)
        for rho in POOLING:
            beta=fit(x,y,family,.1,rho);margin=x@beta;pred=base.classify(margin,.2)
            results.append({'family':family,'alpha':.1,'pooling':rho,'threshold':.2,
                            'scope':'training fit diagnostic only; fixed threshold, not validated selection',
                            'in_sample':base.metrics(y,pred),
                            'critical':[{'id':rows[i]['id'],'actual':rows[i]['winner'],
                                         'prediction':{-1:'B',0:'tie',1:'A'}[int(pred[i])],
                                         'margin':float(margin[i])} for i in indices]})
    return results


def main():
    hashes={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in FROZEN}
    source_files=('comparisons.json','round9-fixed.json','round10-fixed.json','round11-isolation.json')
    source_hashes={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in source_files}
    rows=load_rows();cv=run_cv(rows)
    candidates={};labels=np.array([base.LABEL[r['winner']] for r in rows])
    diagnostic_indices=[i for i,r in enumerate(rows) if r['id'] in ('round11-14','round11-15','round11-16','round11-17','round11-18','round11-19','round11-20')]
    for family in FAMILIES:
        x,y,g=get_arrays(rows,family);cfg=select(x,y,g,family,401)
        beta=fit(x,y,family,cfg['alpha'],cfg['pooling']);margin=x@beta;pred=base.classify(margin,cfg['threshold'])
        candidates[family]={**cfg,'feature_names':names(family),'coefficients':beta.tolist(),
                            'in_sample':base.metrics(y,pred),
                            'diagnostic_premiums':[{'id':rows[i]['id'],'actual':rows[i]['winner'],
                             'prediction':{-1:'B',0:'tie',1:'A'}[int(pred[i])], 'margin':float(margin[i])} for i in diagnostic_indices]}
    # Fairer updated-family comparison: withhold both recent rounds together.
    # Retrospective: the interaction hypotheses were designed after seeing them.
    historical={}
    for family in FAMILIES:
        x,y,g=get_arrays(rows,family);cfg=select(x[:119],y[:119],g[:119],family,307)
        beta=fit(x[:119],y[:119],family,cfg['alpha'],cfg['pooling'])
        pred=base.classify(x[119:]@beta,cfg['threshold'])
        historical[family]={**cfg,'round10':base.metrics(y[119:139],pred[:20]),
                            'round11':base.metrics(y[139:],pred[20:])}
    preserved={}
    for name,pred in frozen_predictions(rows[119:]).items():
        preserved[name]={'round10':base.metrics(labels[119:139],pred[:20]),
                         'round11':base.metrics(labels[139:],pred[20:])}
    result={'method':{'rows':len(rows),'counts':dict(Counter(r['winner'] for r in rows)),
                     'families':{'additive':'18 parameters; newly refitted control only, no saved baseline modified',
                                 'shade':'54 parameters; zone-specific nonnegative shade increments, common age/tare',
                                 'vintage':'54 parameters; zone-specific nonnegative age increments, common shade/tare'},
                     'regularization':'ridge on global mean and zone offsets; additional shrinkage of each zone-specific increment toward global mean',
                     'selection':'nested 5 outer / 3 inner group folds, 5 fixed seeds; inner balanced accuracy tunes alpha, pooling, tie band',
                     'groups':'unordered provenance pair and shade pair; age/tare variants remain together',
                     'strengths':'not fitted numerically; A/B/tie directions only',
                     'limitations':'adaptive nonrandom evidence; repeated splits are not new samples; no pristine holdout remains; comparison family designed after Round 11; 54 parameters vs 158 rows needs strong regularization',
                     'interpretation':'predictive preference scores, not dollar prices; tie band predicts elicited ties, does not change recorded equality semantics',
                     'baseline_hashes':hashes,'evidence_hashes':source_hashes},
            'nested_cv':cv,'candidates_fit_all_158':candidates,
            'training_only_pooling_sensitivity':sensitivity(rows),
            'retrospective_train119_test39':historical,'unchanged_baselines_test39':preserved}
    (ROOT/'interaction-comparison.json').write_text(json.dumps(result,indent=2)+'\n')
    for f,digest in {**hashes,**source_hashes}.items():
        assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==digest,f
    print(json.dumps({'cv':cv['summary'],'fit':{f:v['in_sample']['matched'] for f,v in candidates.items()},'baselines_preserved':True},indent=2))

if __name__=='__main__':main()
