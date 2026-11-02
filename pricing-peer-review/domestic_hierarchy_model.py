"""Soft domestic hierarchy overlay; all saved models and evidence read-only.
Regional layer is fitted inside training folds, preserving the existing offering
calculation and its provenance-scoped tare equalities.
"""
from __future__ import annotations
import hashlib
import json
from itertools import product
from pathlib import Path
import numpy as np
from scipy.optimize import minimize, LinearConstraint
import compare_models as base
import compare_tare_models as tare
import provenance_tare_model as offering
import refit_provenance_v8 as prior_protocol
from reconcile_and_compare import write_versioned

ROOT=Path(__file__).resolve().parent
DOMESTIC=('northeast','southwest','southeast','central','northwest')
# Ordinal prior template, centered: these are not prices or measured gap sizes.
TEMPLATE=np.array([2.,1.,1.,0.,0.]);TEMPLATE-=TEMPLATE.mean()
CONTEXTS=tuple(product(base.SHADES,base.AGES))
STRENGTHS=(.1,1.,10.)
SEEDS=(11,29,47,71,103)


def regional_features(option):
    base.features(option) # validate the supported offering
    z,s,age,_=option;features=np.zeros(30)
    if z in DOMESTIC:
        i=DOMESTIC.index(z);features[i]=1
        features[5+CONTEXTS.index((s,age))]=TEMPLATE[i]
    return features


class RegionalLayer:
    def __init__(self,design,beta):
        self.design=design;self.beta=np.asarray(beta)
        self.initial=np.zeros(30)
        for i,z in enumerate(DOMESTIC):self.initial[i]=self.beta[base.ZONES.index(z)-1]
        self.reference_mean=float(self.initial[:5].mean())
        cons=[];offsets=[]
        for z,s,age,w in product(DOMESTIC,base.SHADES,base.AGES,tare.WEIGHTS):
            a=[z,s,age,w]
            if age>20:
                b=[z,s,age-5,w];cons.append(regional_features(b)-regional_features(a));offsets.append(self.offset(b)-self.offset(a))
            k=base.SHADES.index(s)
            if k<4:
                b=[z,base.SHADES[k+1],age,w];cons.append(regional_features(b)-regional_features(a));offsets.append(self.offset(b)-self.offset(a))
        allrows=np.unique(np.c_[np.array(cons),np.array(offsets)],axis=0)
        self.c=allrows[:,:30];self.lower=-allrows[:,30]-1e-7
        # Weak guidance, not labeled observations: premium domestic 20-year vs
        # lower-tier 30-year at same shade, with maximum tare disadvantage.
        self.prior_pairs=[([z,s,20,130],[other,s,30,110])
                          for z in DOMESTIC[:3] for other in DOMESTIC[3:] for s in base.SHADES]
        self.p=np.array([regional_features(a)-regional_features(b) for a,b in self.prior_pairs])
        self.po=np.array([self.offset(a)-self.offset(b) for a,b in self.prior_pairs])

    def offset(self,option):
        score=float(self.design.features(option)@self.beta)
        if option[0] in DOMESTIC:score-=self.beta[base.ZONES.index(option[0])-1]
        return score

    def array(self,rows):
        return (np.array([regional_features(r['a'])-regional_features(r['b']) for r in rows]),
                np.array([self.offset(r['a'])-self.offset(r['b']) for r in rows]))

    def score(self,option,params):return self.offset(option)+regional_features(option)@params


def objective(params,x,offset,y,layer,strength):
    gap=offset+x@params;strict=y!=0
    slack=np.maximum(0.,1-y[strict]*gap[strict]);residual=np.zeros(len(y))
    residual[strict]=-y[strict]*slack;residual[~strict]=gap[~strict]
    value=float(slack@slack+gap[~strict]@gap[~strict]);grad=2*x.T@residual
    # Small domestic residual differences keep the ordinal template informative.
    theta=params[:5];gates=params[5:];td=theta-theta.mean();gd=gates-gates.mean()
    regular=4*float(td@td)+float(gd@gd)+(gates.mean()-.1)**2+.1*(theta.mean()-layer.reference_mean)**2
    rg=np.zeros(30);rg[:5]=8*td+.2*(theta.mean()-layer.reference_mean)/5
    rg[5:]=2*gd+2*(gates.mean()-.1)/25
    # Soft shrinkage only; no claim that every 20-year offering is equal.
    young=np.array([age==20 for _,age in CONTEXTS])
    regular+=2*float(gates[young]@gates[young]);rg[5:][young]+=4*gates[young]
    # Soft exceptions permitted. Unit margin 0.05 is a modeling convention,
    # not an elicited price or conversion of 'almost always' into a probability.
    prior_gap=layer.po+layer.p@params;short=np.maximum(0.,.05-prior_gap)
    regular+=.25*float(np.mean(short**2));rg+=-.5*layer.p.T@short/len(short)
    value+=strength*regular+1e-5*float(params@params)
    grad+=strength*rg+2e-5*params
    return value,grad


def fit(rows,layer,strength):
    x,offset=layer.array(rows);y=np.array([base.LABEL[r['winner']] for r in rows])
    result=minimize(objective,layer.initial.copy(),args=(x,offset,y,layer,strength),jac=True,
                    method='SLSQP',bounds=[(None,None)]*5+[(0.,None)]*25,
                    constraints=[LinearConstraint(layer.c,layer.lower,np.inf)],
                    options={'ftol':1e-9,'maxiter':1000})
    if not result.success:raise RuntimeError(result.message)
    if np.min(layer.c@result.x-layer.lower)<-1e-6:raise RuntimeError('Monotonicity failed')
    return result.x


def predict(rows,layer,params,threshold):
    x,offset=layer.array(rows);return base.classify(offset+x@params,threshold)


def choose(training,cfg,seed):
    _,y,g=prior_protocol.common.get_arrays(training,'additive')
    predictions={s:np.zeros(len(y),dtype=int) for s in STRENGTHS}
    for tr,va in base.folds(g,3,seed):
        train=[training[i] for i in tr];valid=[training[i] for i in va]
        design,beta=offering.fit(train,cfg);layer=RegionalLayer(design,beta)
        for strength in STRENGTHS:
            params=fit(train,layer,strength);predictions[strength][va]=predict(valid,layer,params,cfg['threshold'])
    scored={s:base.metrics(y,p) for s,p in predictions.items()}
    strength=max(STRENGTHS,key=lambda s:(round(scored[s]['balanced_accuracy'],12),round(scored[s]['accuracy'],12),s))
    return strength,scored[strength]


def labels_scan(rows):
    relevant=[]
    for r in rows:
        for a,b,expected in [(r['a'],r['b'],'A'),(r['b'],r['a'],'B')]:
            if a[0] in DOMESTIC[:3] and b[0] in DOMESTIC and a[2]==20 and b[2]>20 and a[3]>b[3]:
                relevant.append({'id':r['id'],'newer':a,'older':b,'answer':r['winner'],'supports_young_premium':r['winner']==expected})
    return relevant


def main():
    files=('pricing.py','compare_models.py','compare_tare_models.py','provenance_tare_model.py',
           'refit_provenance_v8.py','evidence-v8.json','provenance-comparison-v8.json')
    hashes={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in files}
    rows=json.loads((ROOT/'evidence-v8.json').read_text())['rows'];previous=json.loads((ROOT/'provenance-comparison-v8.json').read_text())
    _,y,g=prior_protocol.common.get_arrays(rows,'additive')
    configs={(a['seed'],a['fold']):a for a in previous['nested_cv']['fold_audits'] if a['model']=='v8_evidence_candidate'}
    subsets=tare.masks(rows)
    subsets['domestic_provenance_comparisons']=np.array([r['a'][0] in DOMESTIC and r['b'][0] in DOMESTIC and r['a'][0]!=r['b'][0] for r in rows])
    subsets['domestic_20_same_other_attributes']=np.array([r['a'][0] in DOMESTIC and r['b'][0] in DOMESTIC and r['a'][0]!=r['b'][0] and r['a'][1:]==r['b'][1:] and r['a'][2]==20 for r in rows])
    runs={'current_v8':[],'domestic_hierarchy':[]};audits=[]
    for seed in SEEDS:
        pred={n:np.zeros(len(y),dtype=int) for n in runs}
        for fold,(tr,te) in enumerate(prior_protocol.extended_folds(g[:310],g,seed)):
            train=[rows[i] for i in tr];test=[rows[i] for i in te];cfg=configs[(seed,fold)]
            strength,inner=choose(train,cfg,seed+fold+7000)
            design,beta=offering.fit(train,cfg);layer=RegionalLayer(design,beta);params=fit(train,layer,strength)
            pred['current_v8'][te]=offering.score(test,design,beta,cfg['threshold'])
            pred['domestic_hierarchy'][te]=predict(test,layer,params,cfg['threshold'])
            audits.append({'seed':seed,'fold':fold,'prior_strength':strength,'inner_balanced_accuracy':inner['balanced_accuracy'],
                           'alpha':cfg['alpha'],'pooling':cfg['pooling'],'threshold':cfg['threshold']})
            print(f'Completed hierarchy validation seed {seed}, fold {fold+1}/5',flush=True)
        old=next(r for r in previous['nested_cv']['runs']['v8_evidence_candidate'] if r['seed']==seed)
        np.testing.assert_array_equal(pred['current_v8'],np.array(old['predictions']))
        for name,p in pred.items():runs[name].append({'seed':seed,'predictions':p.tolist(),'metrics':{k:base.metrics(y[v],p[v]) for k,v in subsets.items()}})
    cfg=previous['candidate_fit_all_341'];design=offering.Design(cfg['local_contexts']);beta=np.array(cfg['coefficients']);layer=RegionalLayer(design,beta)
    strength,inner=choose(rows,cfg,801);params=fit(rows,layer,strength)
    regional=[]
    for shade,age in CONTEXTS:
        premiums={z:float(regional_features([z,shade,age,120])@params) for z in DOMESTIC}
        values={z:float(layer.score([z,shade,age,120],params)) for z in DOMESTIC}
        regional.append({'shade':shade,'vintage':age,'hierarchy_gain':float(params[5+CONTEXTS.index((shade,age))]),
                         'regional_premiums':premiums,'regional_spread':max(premiums.values())-min(premiums.values()),
                         'full_scores_at_120_lb':values,'full_score_spread':max(values.values())-min(values.values())})
    result={'method':{'evidence':'evidence-v8.json','rows':len(rows),'prior':'Northeast > southwest/southeast > central/northwest as an ordinal template, with learned domestic residuals and nonnegative shade/vintage gates. Within-tier equality not forced.',
                     'prior_assumptions':'Centered template [2,1,1,0,0], weak mean-gate target 0.1 in preference units; 20-year gates softly shrink toward zero. Weak premium-region20 vs central/northwest30 prior at equal shade and 130-vs110 tare, not synthetic observations. No fixed 20-vs25 dominance assumption.',
                     'scope':'Regional overlay only; baseline offering and local tare curves held fixed within each training fold. Pure-tare differences exactly preserved. Foreign-only comparisons unchanged.',
                     'validation':'Same current-v8 outer family assignments and training-selected offering settings. Inner 3 family folds refit offering and regional layer on inner training only, selecting prior strength by balanced accuracy. No held-out outcomes used. Existing baseline predictions reproduced exactly.',
                     'limits':'Exploratory user-informed prior; sparse evidence for young premium-region dominance. No pristine holdout or calibrated dollar prices. Layer adds 30 parameters; constrained to preserve weak ordering.',
                     'historical_file_hashes':hashes},
            'guidance_evidence_scan':labels_scan(rows),
            'nested_cv':{'summary':{n:tare.summarize(v) for n,v in runs.items()},'runs':runs,'fold_audits':audits,'row_ids':[r['id'] for r in rows]},
            'candidate_fit_all_341':{'prior_strength':strength,'threshold':cfg['threshold'],'offering_snapshot':cfg,
              'domestic_order':DOMESTIC,'template':TEMPLATE.tolist(),'contexts':CONTEXTS,'regional_parameters':params.tolist(),
              'in_sample':base.metrics(y,predict(rows,layer,params,cfg['threshold'])),'regional_diagnostics':regional,
              'soft_dominance_prior_diagnostics':[{'a':a,'b':b,'margin':float(layer.score(a,params)-layer.score(b,params)),
                                                  'note':'Prior scenario, not validation evidence'} for a,b in layer.prior_pairs]}}
    write_versioned(ROOT/'domestic-hierarchy-comparison.json',result)
    for f,h in hashes.items():assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h,f
    print(json.dumps({'validation':{n:v['all'] for n,v in result['nested_cv']['summary'].items()},'strength':strength,'baselines_unchanged':True},indent=2))

if __name__=='__main__':main()
