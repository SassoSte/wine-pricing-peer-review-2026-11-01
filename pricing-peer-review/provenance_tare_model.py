"""Provenance-scoped tare constraints with partially pooled local curves.
Historical evidence and all baseline models remain read-only.
"""
from __future__ import annotations
import hashlib
import json
from itertools import product
from pathlib import Path
import numpy as np
from scipy.optimize import minimize, LinearConstraint
import compare_models as base
import compare_interactions as common
import compare_tare_models as shared
import compare_objectives as objective
from reconcile_and_compare import write_versioned

ROOT=Path(__file__).resolve().parent


class Design:
    def __init__(self, local_contexts):
        self.local_contexts=tuple(sorted(tuple(c) for c in local_contexts))
        self.local_index={key:117+4*i for i,key in enumerate(self.local_contexts)}
        self.n=117+4*len(self.local_contexts)
        self.constraints=self._constraints()

    @classmethod
    def from_training(cls,rows):
        # Feature activation depends on comparison inputs, not the answer.
        # Any pure-tare comparison supports a local curve, whether strict or tied.
        return cls({tuple(r['a'][:3]) for r in rows if r['a'][:3]==r['b'][:3] and r['a'][3]!=r['b'][3]})

    def features(self,option):
        original=shared.features(option,'context_steps')
        result=np.r_[original,np.zeros(self.n-117)]
        key=tuple(option[:3])
        if key in self.local_index:
            result[17:117]=0
            start=self.local_index[key]
            result[start:start+4]=[float(option[3]<=w) for w in shared.WEIGHTS[1:]]
        return result

    def array(self,rows):
        return np.array([self.features(r['a'])-self.features(r['b']) for r in rows])

    def penalty(self,rho):
        prior=shared.penalty('context_steps',rho)
        rows=[np.r_[row,np.zeros(self.n-117)] for row in prior]
        for (zone,shade,age),local in self.local_index.items():
            shared_start=17+4*shared.CONTEXTS.index((shade,age))
            for step in range(4):
                row=np.zeros(self.n);row[local+step]=np.sqrt(rho);row[shared_start+step]=-np.sqrt(rho)
                rows.append(row)
        return np.array(rows)

    def fixed_steps(self,rows):
        fixed=np.zeros(self.n,dtype=bool)
        for row in rows:
            if row['winner']!='tie' or row['a'][:3]!=row['b'][:3] or row['a'][3]==row['b'][3]:continue
            key=tuple(row['a'][:3])
            if key not in self.local_index:raise ValueError('Missing local context for exact tare equality')
            support=abs(self.features(row['a'])-self.features(row['b']))>1e-10
            if np.any(support[:117]):raise ValueError('Exact equality escaped its provenance-local curve')
            fixed|=support
        return fixed

    def _constraints(self):
        rows=[]
        for zone,shade,age,w in product(base.ZONES,base.SHADES,base.AGES,shared.WEIGHTS):
            origin=self.features([zone,shade,age,w])
            if age>20:rows.append(self.features([zone,shade,age-5,w])-origin)
            idx=base.SHADES.index(shade)
            if idx<4:rows.append(self.features([zone,base.SHADES[idx+1],age,w])-origin)
        return np.unique(np.array(rows),axis=0)

    def names(self):
        return shared.names('context_steps')+[f'local tare step to {w} lb at {z}/{s}/{age}' for z,s,age in self.local_contexts for w in shared.WEIGHTS[1:]]


def fit(rows,cfg):
    design=Design.from_training(rows);x=design.array(rows)
    y=np.array([base.LABEL[r['winner']] for r in rows]);r=design.penalty(cfg['pooling']);gram=r.T@r
    fixed=design.fixed_steps(rows)
    bounds=[(None,None)]*9+[(0.,0.) if fixed[j] else (0.,None) for j in range(9,design.n)]
    result=minimize(objective.objective,np.zeros(design.n),args=(x,y,gram,cfg['alpha']),jac=True,
                    method='SLSQP',bounds=bounds,constraints=[LinearConstraint(design.constraints,0,np.inf)],
                    options={'ftol':1e-9,'maxiter':1200})
    if not result.success:raise RuntimeError(result.message)
    if np.min(design.constraints@result.x)<-1e-6:raise RuntimeError('Monotonicity failed')
    assert np.all(abs(result.x[fixed])<1e-8)
    return design,result.x


def score(rows,design,beta,threshold):
    return base.classify(design.array(rows)@beta,threshold)


def main():
    files=('pricing.py','compare_models.py','compare_interactions.py','compare_objectives.py',
           'compare_tare_models.py','compare_exact_tare_ties.py','evidence-v7.json',
           'contextual-comparison-v7.json','exact-tare-comparison.json','additive-comparison-v6.json')
    hashes={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in files}
    rows=json.loads((ROOT/'evidence-v7.json').read_text())['rows']
    baseline=json.loads((ROOT/'contextual-comparison-v7.json').read_text())
    configs={(s['seed'],s['fold']):s for s in baseline['nested_cv']['selections'] if s['model']=='v7_evidence_candidate'}
    _,y,g=common.get_arrays(rows,'additive');masks=shared.masks(rows)
    assert baseline['nested_cv']['row_ids']==[r['id'] for r in rows]
    runs=[];audits=[]
    for seed in common.SEEDS:
        pred=np.zeros(len(rows),dtype=int)
        for fold,(tr,te) in enumerate(base.folds(g,5,seed)):
            train=[rows[i] for i in tr];test=[rows[i] for i in te];cfg=configs[(seed,fold)]
            assert not set(g[tr])&set(g[te])
            design,beta=fit(train,cfg);pred[te]=score(test,design,beta,cfg['threshold'])
            audits.append({'seed':seed,'fold':fold,'local_contexts':list(design.local_contexts),
                           'parameters':design.n,'fixed_step_count':int(sum(design.fixed_steps(train))),
                           'alpha':cfg['alpha'],'pooling':cfg['pooling'],'threshold':cfg['threshold']})
            print(f'Completed provenance-scope validation seed {seed}, fold {fold+1}/5',flush=True)
        runs.append({'seed':seed,'predictions':pred.tolist(),'metrics':{k:base.metrics(y[v],pred[v]) for k,v in masks.items()}})
    # Hold original settings fixed to isolate the scope correction, including
    # full-data candidate settings. No tuning on outer held-out answers.
    cfg=baseline['candidate_fit_all_310'];design,beta=fit(rows,cfg)
    margins=design.array(rows)@beta;pred=base.classify(margins,cfg['threshold']);fixed=design.fixed_steps(rows)
    forced=[]
    for i,row in enumerate(rows):
        support=abs(design.features(row['a'])-design.features(row['b']))>1e-10
        if y[i]!=0 and np.any(support) and np.all(fixed[support]):forced.append(row['id'])
    highlights={'round14-2','round21-12','round21-3','round21-8','round21-11'}
    # Preserve an auditable original baseline summary on the same masks.
    oldruns=[]
    for run in baseline['nested_cv']['runs']['v7_evidence_candidate']:
        pp=np.array(run['predictions']);oldruns.append({'seed':run['seed'],'metrics':{k:base.metrics(y[v],pp[v]) for k,v in masks.items()}})
    result={'method':{'change':'Exact tare constraints scoped to provenance+shade+vintage, never the shared curve. Local curves activated only from training pure-tare comparison inputs; shrink to shared context curve. Unobserved local contexts use shared curve.',
                       'validation':'Same five seeds/outer withheld families and ORIGINAL TRAINING-SELECTED per-fold hyperparameters as contextual v7. Fixed-settings scope ablation, not a separately hyperparameter-tuned contender. Local contexts/constraints discovered inside training fold only.',
                       'constraints':'Nonnegative tare steps and full-grid weak shade/age monotonicity. Only exact pure-tare ties are hard constraints; ranking loss remains soft.',
                       'limits':'More parameters; exploratory use of known evidence. New prospective validation needed before promotion. Context transfer is soft, not proof every unobserved provenance shares a plateau.',
                       'historical_file_hashes':hashes},
            'nested_cv':{'summary':shared.summarize(runs),'runs':runs,'fold_audits':audits,'row_ids':[r['id'] for r in rows]},
            'shared_scope_baseline_summary':shared.summarize(oldruns),
            'candidate_fit_all_310':{'alpha':cfg['alpha'],'pooling':cfg['pooling'],'threshold':cfg['threshold'],
               'local_contexts':list(design.local_contexts),'feature_names':design.names(),'coefficients':beta.tolist(),
               'in_sample':base.metrics(y,pred),'forced_strict_preference_ids':forced,
               'pure_tare_tie_audit':{'n':int(sum(masks['confirmed_pure_tare_ties'])),
                 'exact_score_equalities':int(sum(abs(margins[masks['confirmed_pure_tare_ties']])<1e-7))},
               'target_predictions':[{'id':row['id'],'answer':row['winner'],'prediction':{-1:'B',0:'tie',1:'A'}[int(pred[i])],
                    'margin':float(margins[i]),'exact_score_equality':bool(abs(margins[i])<1e-7)} for i,row in enumerate(rows) if row['id'] in highlights]}}
    write_versioned(ROOT/'provenance-tare-comparison.json',result)
    for f,h in hashes.items():assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h,f
    print(json.dumps({'new_validation':result['nested_cv']['summary']['all'],
                     'baseline_validation':result['shared_scope_baseline_summary']['all'],
                     'targets':result['candidate_fit_all_310']['target_predictions'],
                     'forced_rank_conflicts':forced},indent=2))

if __name__=='__main__':main()
