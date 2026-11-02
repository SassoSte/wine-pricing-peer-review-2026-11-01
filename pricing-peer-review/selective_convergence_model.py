"""Selective contextual regional equality refinement; baseline models read-only.
Regional score gaps at120 lb can fuse exactly. No pair lookup or global age cutoff.
"""
from itertools import product,combinations
import numpy as np
from scipy.optimize import minimize,LinearConstraint
from scipy import sparse
import osqp
import regional_convergence_model as original
import compare_models as base
import compare_tare_models as tare
import provenance_tare_model as offering
import domestic_hierarchy_model as prior
import weighted_domestic_model as baseline

CONTEXTS=prior.CONTEXTS
DOMESTIC=prior.DOMESTIC
PAIR_INDICES=tuple(combinations(range(5),2))
AGE_WEIGHTS={20:2.,25:1.,30:2.,35:3.,40:4.}
N=104

def regional_rows(rows):
    return [r for r in rows if r['a'][0] in DOMESTIC and r['b'][0] in DOMESTIC and r['a'][0]!=r['b'][0] and r['a'][1:]==r['b'][1:]]


def sample_weights(rows):
    regional=regional_rows(rows);ties=sum(r['winner']=='tie' for r in regional);strict=sum(r['winner']!='tie' for r in regional)
    premium_weight=max(1.,min(4.,ties/max(1,strict)))
    ids={r['id'] for r in regional if r['winner']!='tie'}
    return np.array([premium_weight if r['id'] in ids else 1. for r in rows])


class Layer(original.Layer):
    def __init__(self,design,beta,pilot_parameters,training_rows):
        super().__init__(design,beta)
        pilot=np.asarray(pilot_parameters);self.pilot_parameters=pilot.copy()
        self.reference_mean=float(pilot[:5].mean())
        self.initial=np.zeros(N);self.initial[0]=self.reference_mean
        for k,ctx in enumerate(CONTEXTS):
            regional=pilot[:5]+pilot[5+k]*prior.TEMPLATE
            self.initial[1+4*k:1+4*(k+1)]=(regional-self.reference_mean)[:4]
        self.initial[101:]=pilot[30:]
        self.anchor=self.initial.copy()
        self.reference_gap=self.d@self.anchor
        self.reference_smooth=self.smooth@self.anchor
        support=regional_rows(training_rows)
        self.support_ids=[r['id'] for r in support]
        self.support_details=[]
        for k,(shade,age) in enumerate(CONTEXTS):
            for j,(a,b) in enumerate(PAIR_INDICES):
                pair={DOMESTIC[a],DOMESTIC[b]};ties=0.;strict=0.
                for r in support:
                    if {r['a'][0],r['b'][0]}!=pair:continue
                    distance=abs(age-r['a'][2])/5+abs(base.SHADES.index(shade)-base.SHADES.index(r['a'][1]))
                    weight=1./(1.+distance)
                    if r['winner']=='tie':ties+=weight
                    else:strict+=weight
                # Smoothed support in the SAME provenance pair, declining with
                # shade/age distance. Strict premiums resist fusion fourfold.
                propensity=(1.+ties)/(2.+ties+4.*strict)
                self.fusion_weights[k*10+j]*=propensity
                self.support_details.append({'shade':shade,'vintage':age,'regions':[DOMESTIC[a],DOMESTIC[b]],'tie_support':ties,'premium_support':strict,'fusion_multiplier':propensity})
        self.loss_weights=sample_weights(training_rows)


def objective(v,x,offset,y,layer,strength):
    params=v[:N];u=v[N:];margin=offset+x@params;strict=y!=0
    slack=np.maximum(0.,1-y[strict]*margin[strict]);res=np.zeros(len(y));res[strict]=-y[strict]*slack;res[~strict]=margin[~strict]
    weights=layer.loss_weights
    value=float((weights[strict]*slack)@slack+(weights[~strict]*margin[~strict])@margin[~strict]);grad=2*x.T@(weights*res)
    gap=layer.d@params-layer.reference_gap;smooth=layer.smooth@params-layer.reference_smooth
    reg=.1*float(gap@gap)+.5*float(smooth@smooth)+float((params[101:]-layer.anchor[101:])@(params[101:]-layer.anchor[101:]))+.1*(params[0]-layer.reference_mean)**2
    rg=.2*layer.d.T@gap+layer.smooth.T@smooth;rg[101:]+=2*(params[101:]-layer.anchor[101:]);rg[0]+=.2*(params[0]-layer.reference_mean)
    # Zero-margin soft hierarchy permits equality; unlike the prior recipe,
    # no positive minimum regional premium is rewarded.
    short=np.maximum(0.,-layer.order@params);reg+=10*float(short@short);rg-=20*layer.order.T@short
    short=np.maximum(0.,.05-layer.p@params);reg+=.25*float(np.mean(short**2));rg-=.5*layer.p.T@short/len(short)
    fusion=.3*layer.fusion_weights
    return value+strength*(reg+fusion@u)+1e-5*float(params@params),np.r_[grad+strength*rg+2e-5*params,strength*fusion]


def fit_slsqp(rows,layer,strength):
    x,offset=layer.array(rows);y=np.array([base.LABEL[r['winner']] for r in rows])
    initial=np.r_[layer.initial,abs(layer.d@layer.initial)]
    result=minimize(objective,initial,args=(x,offset,y,layer,strength),jac=True,method='SLSQP',bounds=[(None,None)]*101+[(float(v),float(v)) for v in layer.anchor[101:]]+[(0,None)]*len(layer.d),constraints=[layer.constraints],options={'ftol':1e-8,'maxiter':1000})
    if not result.success:raise RuntimeError(result.message)
    params=result.x[:N]
    if np.min(layer.c@params)<-2e-6:raise RuntimeError('Monotonicity failed')
    return params



def fit(rows,layer,strength):
    """Exact convex QP equivalent to objective(), with nonnegative hinge slacks."""
    x,offset=layer.array(rows);y=np.array([base.LABEL[r['winner']] for r in rows])
    tied=y==0;strict=~tied
    nu=len(layer.d);nh=int(sum(strict));no=len(layer.order);np_=len(layer.p)
    total=N+nu+nh+no+np_
    us=N;hs=us+nu;os=hs+nh;ps=os+no
    reg=.1*layer.d.T@layer.d+.5*layer.smooth.T@layer.smooth
    reg[0,0]+=.1
    reg[101:,101:]+=np.eye(3)
    weights=layer.loss_weights
    h=x[tied].T@(weights[tied,None]*x[tied])+strength*reg+1e-5*np.eye(N)
    quadratic=sparse.block_diag((2*h,sparse.csc_matrix((nu,nu)),2*sparse.diags(weights[strict]),20*strength*sparse.eye(no),(.5*strength/np_)*sparse.eye(np_)),format='csc')
    linear=np.zeros(total);linear[:N]=2*x[tied].T@(weights[tied]*offset[tied])
    linear[:N]-=strength*(.2*layer.d.T@layer.reference_gap+layer.smooth.T@layer.reference_smooth)
    linear[0]-=.2*strength*layer.reference_mean;linear[101:104]-=2*strength*layer.anchor[101:]
    linear[us:hs]=strength*.3*layer.fusion_weights
    def block(matrix,start=None,count=0):
        left=sparse.csc_matrix(matrix)
        right=sparse.csc_matrix((len(matrix),total-N))
        if start is not None:
            right=sparse.hstack([sparse.csc_matrix((count,start-N)),sparse.eye(count),sparse.csc_matrix((count,total-start-count))],format='csc')
        return sparse.hstack([left,right],format='csc')
    constraint=sparse.vstack([block(layer.c),block(-layer.d,us,nu),block(layer.d,us,nu),
        block(y[strict,None]*x[strict],hs,nh),block(layer.order,os,no),block(layer.p,ps,np_),sparse.eye(total)],format='csc')
    bounds=np.r_[np.full(101,-np.inf),layer.anchor[101:],np.zeros(total-N)]
    lower=np.r_[np.full(len(layer.c),-1e-7),np.zeros(2*nu),1-y[strict]*offset[strict],np.zeros(no),np.full(np_,.05),bounds]
    upper=np.full(len(lower),np.inf);upper[-total+101:-total+104]=layer.anchor[101:]
    solver=osqp.OSQP();solver.setup(P=sparse.triu(quadratic,format='csc'),q=linear,A=constraint,l=lower,u=upper,eps_abs=1e-8,eps_rel=1e-8,max_iter=200000,polishing=True,verbose=False)
    result=solver.solve(raise_error=False)
    if result.info.status!='solved':raise RuntimeError(f'QP failed: {result.info.status}')
    if np.min(constraint@result.x-lower)<-2e-6 or np.min(upper-constraint@result.x)<-2e-6:raise RuntimeError('QP feasibility failed')
    return result.x[:N]


def predict(rows,layer,params,threshold):
    x,offset=layer.array(rows);return base.classify(offset+x@params,threshold)


def selection_metrics(rows,y,pred):
    overall=base.metrics(y,pred)
    indices={r['id'] for r in regional_rows(rows)}
    regional=np.array([r['id'] in indices for r in rows]);ties=regional&(y==0);premiums=regional&(y!=0)
    recalls=[float(np.mean(pred[m]==y[m])) for m in (ties,premiums) if np.any(m)]
    regional_balanced=float(np.mean(recalls)) if recalls else overall['balanced_accuracy']
    return {**overall,'regional_equality_premium_balanced_accuracy':regional_balanced,
            'selection_score':.5*(overall['balanced_accuracy']+regional_balanced)}


def choose(rows,cfg,seed):
    _,y,g=baseline.protocol.common.get_arrays(rows,'additive');pred={s:np.zeros(len(y),dtype=int) for s in prior.STRENGTHS}
    pilot_audits=[]
    for inner_fold,(tr,va) in enumerate(base.folds(g,3,seed)):
        training=[rows[i] for i in tr];valid=[rows[i] for i in va]
        design,beta=offering.fit(training,cfg)
        # Pilot fitting and its prior selection are nested INSIDE inner training.
        pilot_strength,_=baseline.choose(training,cfg,seed+17)
        pilot_layer=baseline.Layer(design,beta);pilot=baseline.fit(training,pilot_layer,pilot_strength)
        layer=Layer(design,beta,pilot,training)
        pilot_audits.append({'inner_fold':inner_fold,'training_ids':[r['id'] for r in training],'support_ids':layer.support_ids,'pilot_prior_strength':pilot_strength,'pilot_selection_seed':seed+17})
        for strength in prior.STRENGTHS:pred[strength][va]=predict(valid,layer,fit(training,layer,strength),cfg['threshold'])
    metrics={s:selection_metrics(rows,y,p) for s,p in pred.items()}
    best=max(prior.STRENGTHS,key=lambda s:(round(metrics[s]['selection_score'],12),round(metrics[s]['balanced_accuracy'],12),round(metrics[s]['accuracy'],12),-s))
    return best,{**metrics[best],'pilot_audits':pilot_audits}
