"""Joint domestic hierarchy and offering-weight calibration; baselines read-only."""
import hashlib
import json
from itertools import product
import numpy as np
from scipy.optimize import minimize,LinearConstraint
import domestic_hierarchy_model as prior
import compare_models as base
import compare_tare_models as tare
import provenance_tare_model as offering
import refit_provenance_v8 as protocol
from reconcile_and_compare import write_versioned

ROOT=prior.ROOT


class Layer:
    def __init__(self,design,beta):
        self.design=design;self.beta=np.asarray(beta);self.initial=np.zeros(33)
        for i,z in enumerate(prior.DOMESTIC):self.initial[i]=self.beta[base.ZONES.index(z)-1]
        self.initial[30:]=1.;self.reference_mean=float(self.initial[:5].mean())
        constraints=[];offsets=[]
        for z,s,age,w in product(prior.DOMESTIC,base.SHADES,base.AGES,tare.WEIGHTS):
            a=[z,s,age,w]
            neighbors=[]
            if age>20:neighbors.append([z,s,age-5,w])
            k=base.SHADES.index(s)
            if k<4:neighbors.append([z,base.SHADES[k+1],age,w])
            for b in neighbors:constraints.append(self.features(b)-self.features(a));offsets.append(self.offset(b)-self.offset(a))
        unique=np.unique(np.c_[constraints,offsets],axis=0);self.c=unique[:,:33];self.lower=-unique[:,33]-1e-7
        self.prior_pairs=[([z,s,20,130],[other,s,30,110]) for z in prior.DOMESTIC[:3] for other in prior.DOMESTIC[3:] for s in base.SHADES]
        self.p=np.array([self.features(a)-self.features(b) for a,b in self.prior_pairs])
        self.po=np.array([self.offset(a)-self.offset(b) for a,b in self.prior_pairs])
        self.order=[]
        for hi,lo in [('northeast','southwest'),('northeast','southeast'),('southwest','central'),('southwest','northwest'),('southeast','central'),('southeast','northwest')]:
            v=np.zeros(33);h=prior.DOMESTIC.index(hi);l=prior.DOMESTIC.index(lo)
            v[h]=1;v[l]=-1;v[5:30]=(prior.TEMPLATE[h]-prior.TEMPLATE[l])/25;self.order.append(v)
        self.order=np.array(self.order)

    def features(self,option):
        regional=prior.regional_features(option)
        if option[0] not in prior.DOMESTIC:return np.r_[regional,np.zeros(3)]
        f=self.design.features(option)
        return np.r_[regional,f[9:13]@self.beta[9:13],f[13:17]@self.beta[13:17],f[17:]@self.beta[17:]]

    def offset(self,option):
        return 0. if option[0] in prior.DOMESTIC else float(self.design.features(option)@self.beta)

    def array(self,rows):return np.array([self.features(r['a'])-self.features(r['b']) for r in rows]),np.array([self.offset(r['a'])-self.offset(r['b']) for r in rows])
    def score(self,option,params):return self.offset(option)+self.features(option)@params


def objective(params,x,offset,y,layer,strength):
    margin=offset+x@params;strict=y!=0;slack=np.maximum(0.,1-y[strict]*margin[strict]);res=np.zeros(len(y));res[strict]=-y[strict]*slack;res[~strict]=margin[~strict]
    value=float(slack@slack+margin[~strict]@margin[~strict]);gradient=2*x.T@res
    theta=params[:5];gates=params[5:30];scales=params[30:];td=theta-theta.mean();gd=gates-gates.mean()
    reg=4*float(td@td)+float(gd@gd)+(gates.mean()-.1)**2+.1*(theta.mean()-layer.reference_mean)**2+float((scales-1)@(scales-1))
    grad=np.zeros(33);grad[:5]=8*td+.2*(theta.mean()-layer.reference_mean)/5;grad[5:30]=2*gd+2*(gates.mean()-.1)/25;grad[30:]=2*(scales-1)
    young=np.array([age==20 for _,age in prior.CONTEXTS]);reg+=2*float(gates[young]@gates[young]);grad[5:30][young]+=4*gates[young]
    # Explicit soft average domestic order; does not require each individual
    # context to obey the same rank. Margin 0.03 is a prior convention, not price.
    short=np.maximum(0.,.03-layer.order@params);reg+=10*float(short@short);grad+=-20*layer.order.T@short
    short=np.maximum(0.,.05-layer.po-layer.p@params);reg+=.25*float(np.mean(short**2));grad+=-.5*layer.p.T@short/len(short)
    return value+strength*reg+1e-5*float(params@params),gradient+strength*grad+2e-5*params


def fit(rows,layer,strength):
    x,offset=layer.array(rows);y=np.array([base.LABEL[r['winner']] for r in rows])
    result=minimize(objective,layer.initial.copy(),args=(x,offset,y,layer,strength),jac=True,method='SLSQP',
                    bounds=[(None,None)]*5+[(0,None)]*25+[(.05,None)]*3,
                    constraints=[LinearConstraint(layer.c,layer.lower,np.inf)],options={'ftol':1e-9,'maxiter':1000})
    if not result.success:raise RuntimeError(result.message)
    return result.x


def predict(rows,layer,params,threshold):
    x,offset=layer.array(rows);return base.classify(offset+x@params,threshold)


def choose(rows,cfg,seed):
    _,y,g=protocol.common.get_arrays(rows,'additive');pred={s:np.zeros(len(y),dtype=int) for s in prior.STRENGTHS}
    for tr,va in base.folds(g,3,seed):
        train=[rows[i] for i in tr];valid=[rows[i] for i in va]
        d,beta=offering.fit(train,cfg);layer=Layer(d,beta)
        for strength in prior.STRENGTHS:pred[strength][va]=predict(valid,layer,fit(train,layer,strength),cfg['threshold'])
    metrics={s:base.metrics(y,p) for s,p in pred.items()}
    best=max(prior.STRENGTHS,key=lambda s:(round(metrics[s]['balanced_accuracy'],12),round(metrics[s]['accuracy'],12),s))
    return best,metrics[best]


def main():
    files=('pricing.py','compare_models.py','compare_tare_models.py','provenance_tare_model.py',
           'refit_provenance_v8.py','evidence-v8.json','provenance-comparison-v8.json',
           'domestic_hierarchy_model.py','domestic-hierarchy-comparison.json')
    hashes={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in files}
    rows=json.loads((ROOT/'evidence-v8.json').read_text())['rows'];old=json.loads((ROOT/'provenance-comparison-v8.json').read_text());regional=json.loads((ROOT/'domestic-hierarchy-comparison.json').read_text())
    _,y,g=protocol.common.get_arrays(rows,'additive');configs={(a['seed'],a['fold']):a for a in old['nested_cv']['fold_audits'] if a['model']=='v8_evidence_candidate'}
    masks=tare.masks(rows);masks['domestic_provenance_comparisons']=np.array([r['a'][0] in prior.DOMESTIC and r['b'][0] in prior.DOMESTIC and r['a'][0]!=r['b'][0] for r in rows]);masks['domestic_20_same_other_attributes']=np.array([r['a'][0] in prior.DOMESTIC and r['b'][0] in prior.DOMESTIC and r['a'][0]!=r['b'][0] and r['a'][1:]==r['b'][1:] and r['a'][2]==20 for r in rows])
    runs=[];audits=[]
    for seed in prior.SEEDS:
        pred=np.zeros(len(y),dtype=int)
        for fold,(tr,te) in enumerate(protocol.extended_folds(g[:310],g,seed)):
            train=[rows[i] for i in tr];test=[rows[i] for i in te];cfg=configs[(seed,fold)]
            strength,inner=choose(train,cfg,seed+fold+7000)
            d,beta=offering.fit(train,cfg);layer=Layer(d,beta);params=fit(train,layer,strength)
            pred[te]=predict(test,layer,params,cfg['threshold'])
            audits.append({'seed':seed,'fold':fold,'prior_strength':strength,'inner_balanced_accuracy':inner['balanced_accuracy'],'alpha':cfg['alpha'],'pooling':cfg['pooling'],'threshold':cfg['threshold']})
            print(f'Completed weighted hierarchy seed {seed}, fold {fold+1}/5',flush=True)
        runs.append({'seed':seed,'predictions':pred.tolist(),'metrics':{k:base.metrics(y[v],pred[v]) for k,v in masks.items()}})
    cfg=old['candidate_fit_all_341'];design=offering.Design(cfg['local_contexts']);beta=np.array(cfg['coefficients']);layer=Layer(design,beta)
    strength,inner=choose(rows,cfg,801);params=fit(rows,layer,strength)
    diagnostics=[]
    for shade,age in prior.CONTEXTS:
        premiums={z:float(prior.regional_features([z,shade,age,120])@params[:30]) for z in prior.DOMESTIC}
        values={z:float(layer.score([z,shade,age,120],params)) for z in prior.DOMESTIC}
        diagnostics.append({'shade':shade,'vintage':age,'hierarchy_gain':float(params[5+prior.CONTEXTS.index((shade,age))]),'regional_premiums':premiums,'regional_spread':max(premiums.values())-min(premiums.values()),'full_scores_at_120_lb':values,'full_score_spread':max(values.values())-min(values.values())})
    result={'method':{'rows':len(rows),'change':'Learn domestic shade/vintage/tare scaling jointly with soft regional hierarchy and contextual convergence; foreign scores unchanged. Tare curves scaled by positive factor, preserving exact pure-tare ties and score direction; classifier margins can change.',
                     'prior':'Same centered [2,1,1,0,0] tier template, context gains, 20-year shrinkage and weak 20-vs30 premium-region dominance scenarios as regional-only model; add a soft average hierarchy-order penalty. Exact prior margin conventions are not elicited prices.',
                     'validation':'Same outer family partitions and base offering settings; inner grouped training refits both offering and weighted hierarchy to select prior strength. Expanded prior explored after regional-only result, so this is exploratory repeated validation, not a pristine new test.',
                     'historical_file_hashes':hashes},
            'nested_cv':{'summary':tare.summarize(runs),'runs':runs,'fold_audits':audits,'row_ids':[r['id'] for r in rows]},
            'comparison_summaries':regional['nested_cv']['summary'],
            'candidate_fit_all_341':{'prior_strength':strength,'threshold':cfg['threshold'],'offering_snapshot':cfg,'parameters':params.tolist(),
                'domestic_order':prior.DOMESTIC,'template':prior.TEMPLATE.tolist(),'contexts':prior.CONTEXTS,
                'domestic_component_scales':dict(zip(['shade','vintage','tare'],params[30:].tolist())),
                'in_sample':base.metrics(y,predict(rows,layer,params,cfg['threshold'])),'regional_diagnostics':diagnostics,
                'soft_dominance_prior_diagnostics':[{'a':a,'b':b,'margin':float(layer.score(a,params)-layer.score(b,params)),'note':'Prior scenario, not validation evidence'} for a,b in layer.prior_pairs]}}
    write_versioned(ROOT/'weighted-domestic-comparison.json',result)
    for f,h in hashes.items():assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h,f
    print(json.dumps({'validation':result['nested_cv']['summary']['all'],'scales':result['candidate_fit_all_341']['domestic_component_scales'],'prior_strength':strength,'baselines_unchanged':True},indent=2))

if __name__=='__main__':main()
