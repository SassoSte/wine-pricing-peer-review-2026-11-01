"""Exploratory additive model comparison; never changes pricing.py or evidence.

Requires numpy/scipy. Run: python3 compare_models.py
Positive margin favors A. Scores are preference units, NOT dollars.
"""
from __future__ import annotations
import hashlib
import json
from collections import Counter
from pathlib import Path
import numpy as np
from scipy.optimize import lsq_linear

ROOT = Path(__file__).resolve().parent
ZONES = ('Eastern Europe', 'Western Europe', 'West Central Asia',
         'South/Eastern Asia', 'West Asia / Middle East', 'central',
         'northeast', 'northwest', 'southwest', 'southeast')
SHADES = ('brown', 'copper', 'amber', 'golden', 'pale/straw')
AGES = (40, 35, 30, 25, 20)
FEATURES = ([f'origin:{z} vs Eastern Europe' for z in ZONES[1:]]
            + [f'shade increment:{s}' for s in SHADES[1:]]
            + [f'age increment:{y}' for y in AGES[1:]] + ['lightness per 5 lb'])
LABEL = {'B': -1, 'tie': 0, 'A': 1}
LAMBDAS = (0.01, 0.1, 1.0, 10.0, 100.0)
THRESHOLDS = (0.0, .05, .1, .15, .2, .3, .4, .5, .65, .8, 1.01)
SEEDS = (11, 29, 47, 71, 103)


def features(option):
    zone, shade, age, weight = option
    if zone not in ZONES or shade not in SHADES or age not in AGES or weight not in (110,115,120,125,130):
        raise ValueError(f'Unsupported option: {option}')
    return np.array([float(zone == z) for z in ZONES[1:]]
                    + [float(SHADES.index(shade) >= i) for i in range(1,5)]
                    + [float(AGES.index(age) >= i) for i in range(1,5)]
                    + [(130-weight)/5], dtype=float)


def load_rows():
    previous = json.loads((ROOT/'comparisons.json').read_text())['comparisons']
    frozen = json.loads((ROOT/'round9-fixed.json').read_text())['questions']
    train = [r for r in previous if r['status'] == 'active']
    test = [r for r in frozen if r['status'] == 'answered']
    assert len(train) == 101 and len(test) == 18
    rows = train + test
    seen = set()
    for r in rows:
        key = frozenset((tuple(r['a']), tuple(r['b'])))
        if key in seen:
            raise ValueError(f'Duplicate pair: {r["id"]}')
        seen.add(key)
    return train, test


def arrays(rows):
    x = np.array([features(r['a'])-features(r['b']) for r in rows])
    y = np.array([LABEL[r['winner']] for r in rows])
    # Group age/tare variants of the same unordered provenance/shade pairing.
    groups = [repr((tuple(sorted((r['a'][0],r['b'][0]))),
                    tuple(sorted((r['a'][1],r['b'][1]))))) for r in rows]
    return x, y, np.array(groups)


def fit(x, y, alpha):
    # Symmetric score differences; no intercept. Ridge avoids unstable large
    # coefficients. Nonnegative increments retain weak monotonicity assumptions.
    xa = np.vstack((x, np.sqrt(alpha)*np.eye(len(FEATURES))))
    ya = np.r_[y, np.zeros(len(FEATURES))]
    lower = np.r_[np.full(9, -np.inf), np.zeros(9)]
    result = lsq_linear(xa, ya, bounds=(lower, np.inf), tol=1e-10)
    if not result.success:
        raise RuntimeError(result.message)
    return result.x


def classify(margins, threshold):
    return np.where(margins > threshold+1e-8, 1,
                    np.where(margins < -threshold-1e-8, -1, 0))


def metrics(y, pred):
    recalls = {name: float(np.mean(pred[y==val] == val))
               for name,val in LABEL.items() if np.any(y==val)}
    confusion = {actual: {predicted: int(np.sum((y==a)&(pred==b)))
                          for predicted,b in LABEL.items()}
                 for actual,a in LABEL.items()}
    return dict(n=len(y), matched=int(np.sum(y==pred)),
                accuracy=float(np.mean(y==pred)),
                balanced_accuracy=float(np.mean(list(recalls.values()))),
                recall=recalls, confusion_actual_to_predicted=confusion,
                opposite_winner_errors=int(np.sum(y*pred == -1)),
                predicted_ties=int(np.sum(pred==0)))


def folds(groups, k, seed):
    rng = np.random.default_rng(seed)
    unique = list(np.unique(groups)); rng.shuffle(unique)
    # Largest groups first, seeded tie order; balance rows without reading labels.
    unique.sort(key=lambda g: -np.sum(groups==g))
    bins=[[] for _ in range(k)]; sizes=np.zeros(k, dtype=int)
    for g in unique:
        target=int(np.argmin(sizes)); bins[target].append(g)
        sizes[target]+=int(np.sum(groups==g))
    for group_bin in bins:
        test=np.flatnonzero(np.isin(groups,group_bin))
        train=np.flatnonzero(~np.isin(groups,group_bin))
        assert not set(groups[test]) & set(groups[train])
        yield train,test


def select(x, y, groups, seed):
    # Tune on training-only grouped folds. Same fit family for both candidates;
    # only the second candidate may learn a nonzero decision band.
    results={'additive_exact':None,'additive_near_tie':None}
    best={name:None for name in results}
    for alpha in LAMBDAS:
        margins=np.zeros(len(y))
        for tr,va in folds(groups,3,seed):
            margins[va]=x[va] @ fit(x[tr],y[tr],alpha)
        for name in results:
            for threshold in ((0.0,) if name=='additive_exact' else THRESHOLDS):
                m=metrics(y,classify(margins,threshold))
                # Balanced accuracy is primary; then raw accuracy, stronger
                # regularization, and a smaller tie band for deterministic ties.
                key=(round(m['balanced_accuracy'],12),round(m['accuracy'],12),alpha,-threshold)
                if best[name] is None or key>best[name]:
                    best[name]=key
                    results[name]={'alpha':alpha,'threshold':threshold,
                                   'inner_balanced_accuracy':m['balanced_accuracy']}
    return results


def evaluate_nested(rows):
    x,y,g=arrays(rows)
    outputs={name:[] for name in ('additive_exact','additive_near_tie')}
    records=[]
    for seed in SEEDS:
        preds={name:np.zeros(len(y),dtype=int) for name in outputs}
        for fold,(tr,te) in enumerate(folds(g,5,seed)):
            chosen=select(x[tr],y[tr],g[tr],seed+fold+1000)
            for name,cfg in chosen.items():
                beta=fit(x[tr],y[tr],cfg['alpha'])
                preds[name][te]=classify(x[te]@beta,cfg['threshold'])
                records.append({'seed':seed,'fold':fold,'model':name,
                                'train_n':len(tr),'test_n':len(te),**cfg})
        for name,pred in preds.items():
            outputs[name].append({'seed':seed,**metrics(y,pred),
                                 'predictions':pred.tolist()})
        print(f'Completed grouped validation seed {seed}',flush=True)
    summary={}
    for name,runs in outputs.items():
        summary[name]={k:float(np.mean([r[k] for r in runs]))
                       for k in ('accuracy','balanced_accuracy','opposite_winner_errors','predicted_ties')}
        summary[name]['accuracy_range']=[min(r['accuracy'] for r in runs),max(r['accuracy'] for r in runs)]
        summary[name]['mean_recall']={label:float(np.mean([r['recall'][label] for r in runs])) for label in LABEL}
    return dict(summary=summary,runs=outputs,selections=records,
                row_ids=[r['id'] for r in rows],groups=len(set(g)))


def main():
    old,round9=load_rows();all_rows=old+round9
    model_hash=hashlib.sha256((ROOT/'pricing.py').read_bytes()).hexdigest()
    x,y,g=arrays(old);xt,yt,_=arrays(round9)
    historical={};chosen=select(x,y,g,307)
    for name,cfg in chosen.items():
        beta=fit(x,y,cfg['alpha']);pred=classify(xt@beta,cfg['threshold'])
        historical[name]={**cfg,**metrics(yt,pred),'predictions':pred.tolist()}
    historical['frozen_revision_e']=metrics(yt,np.array([LABEL[r['prediction_before_answer']] for r in round9]))
    # Fair class-frequency baselines; a constant predicts training majority.
    most_common=Counter(y.tolist()).most_common(1)[0][0]
    historical['training_majority']=metrics(yt,np.full(len(yt),most_common))
    historical['always_tie_diagnostic']=metrics(yt,np.zeros(len(yt),dtype=int))
    cv=evaluate_nested(all_rows)
    x,y,g=arrays(all_rows);selected=select(x,y,g,401)
    candidates={}
    for name,cfg in selected.items():
        beta=fit(x,y,cfg['alpha'])
        candidates[name]={**cfg,'coefficients':dict(zip(FEATURES,beta.tolist())),
                          'in_sample':metrics(y,classify(x@beta,cfg['threshold']))}
    result={'method':{'rows':len(all_rows),'label_counts':dict(Counter(r['winner'] for r in all_rows)),
                     'feature_count':len(FEATURES),'features':FEATURES,
                     'target':'A=+1, B=-1, tie=0; verbal strength ignored; score scale is not money',
                     'fit':'Ridge least squares; monotone nonnegative shade/age/tare increments; free provenance offsets; no interactions',
                     'models':'Identical feature family. Exact: zero tie band. Near-tie: symmetric band tuned on training-only folds.',
                     'cv':'5 outer grouped folds x 5 seeds; inner 3 grouped folds select ridge strength and decision band by balanced accuracy',
                     'group':'unordered provenance pair and unordered shade pair; all age/tare variants together',
                     'historical_caveat':'Round 9 was already inspected before this comparison was designed. Training excludes it, but results are retrospective, not a new pristine holdout.',
                     'cv_caveat':'Repeated splits reuse the same 119 answers; ranges are split sensitivity, not confidence intervals or independent new samples.',
                     'threshold_semantics':'Prediction of an elicited tie; does not rewrite exact-tie answers or assert equal dollar prices.',
                     'production_sha256':model_hash},
            'round9_diagnostic':historical,'round9_ids':[r['id'] for r in round9],
            'grouped_cv':cv,'candidates_fit_all_119':candidates}
    (ROOT/'model-comparison.json').write_text(json.dumps(result,indent=2)+'\n')
    assert hashlib.sha256((ROOT/'pricing.py').read_bytes()).hexdigest()==model_hash
    print(json.dumps({'round9':{k:{z:v[z] for z in ('matched','n','balanced_accuracy')} for k,v in historical.items()},'cv':cv['summary']},indent=2))

if __name__=='__main__':main()
