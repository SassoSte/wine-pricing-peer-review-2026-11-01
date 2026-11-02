"""Sparse contextual regional equality experiment; baseline models read-only.
Regional score gaps at120 lb can fuse exactly. No pair lookup or global age cutoff.
"""
from itertools import product,combinations
import numpy as np
from scipy.optimize import minimize,LinearConstraint
from scipy import sparse
import osqp
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

class Layer:
    def __init__(self,design,beta):
        self.design=design;self.beta=np.asarray(beta)
        offsets=np.array([self.beta[base.ZONES.index(z)-1] for z in DOMESTIC])
        self.reference_mean=float(offsets.mean());self.initial=np.zeros(N)
        self.initial[0]=self.reference_mean
        self.initial[1:101]=np.tile((offsets-offsets.mean())[:4],25)
        self.initial[101:]=1.
        cons=[];lower=[]
        for z,s,age,w in product(DOMESTIC,base.SHADES,base.AGES,tare.WEIGHTS):
            a=[z,s,age,w];neighbors=[]
            if age>20:neighbors.append([z,s,age-5,w])
            k=base.SHADES.index(s)
            if k<4:neighbors.append([z,base.SHADES[k+1],age,w])
            for b in neighbors:cons.append(self.features(b)-self.features(a));lower.append(-1e-7)
        self.c=np.unique(np.array(cons),axis=0)
        self.d=np.array([self.features([DOMESTIC[i],s,age,120])-self.features([DOMESTIC[j],s,age,120]) for s,age in CONTEXTS for i,j in PAIR_INDICES])
        self.fusion_weights=np.array([AGE_WEIGHTS[age] for s,age in CONTEXTS for _ in PAIR_INDICES])
        # Smooth adjacent shade/age regional score contrasts without forcing an
        # age cutoff, a direction, or equality outside the reference tare.
        smooth=[]
        for k,(s,age) in enumerate(CONTEXTS):
            neighbors=[]
            if age>20:neighbors.append((s,age-5))
            si=base.SHADES.index(s)
            if si<4:neighbors.append((base.SHADES[si+1],age))
            for ctx in neighbors:
                j=CONTEXTS.index(ctx)
                smooth.extend(self.d[k*10:(k+1)*10]-self.d[j*10:(j+1)*10])
        self.smooth=np.array(smooth)
        self.order=np.array([np.mean([self.features([hi,s,a,120])-self.features([lo,s,a,120]) for s,a in CONTEXTS],axis=0) for hi,lo in [('northeast','southwest'),('northeast','southeast'),('southwest','central'),('southwest','northwest'),('southeast','central'),('southeast','northwest')]])
        self.prior_pairs=[([z,s,20,130],[other,s,30,110]) for z in DOMESTIC[:3] for other in DOMESTIC[3:] for s in base.SHADES]
        self.p=np.array([self.features(a)-self.features(b) for a,b in self.prior_pairs])
        zeros=np.zeros((len(self.c),len(self.d)));eye=np.eye(len(self.d))
        self.constraints=LinearConstraint(np.vstack([np.c_[self.c,zeros],np.c_[-self.d,eye],np.c_[self.d,eye]]),np.r_[np.full(len(self.c),-1e-7),np.zeros(2*len(self.d))],np.inf)

    def features(self,option):
        f=self.design.features(option);out=np.zeros(N)
        if option[0] not in DOMESTIC:return out
        out[0]=1.;start=1+4*CONTEXTS.index((option[1],option[2]));z=DOMESTIC.index(option[0])
        if z<4:out[start+z]=1.
        else:out[start:start+4]=-1.
        out[101:]=[f[9:13]@self.beta[9:13],f[13:17]@self.beta[13:17],f[17:]@self.beta[17:]]
        return out

    def offset(self,option):return 0. if option[0] in DOMESTIC else float(self.design.features(option)@self.beta)
    def array(self,rows):return np.array([self.features(r['a'])-self.features(r['b']) for r in rows]),np.array([self.offset(r['a'])-self.offset(r['b']) for r in rows])
    def score(self,option,params):return self.offset(option)+self.features(option)@np.asarray(params)


def objective(v,x,offset,y,layer,strength):
    params=v[:N];u=v[N:];margin=offset+x@params;strict=y!=0
    slack=np.maximum(0.,1-y[strict]*margin[strict]);res=np.zeros(len(y));res[strict]=-y[strict]*slack;res[~strict]=margin[~strict]
    value=float(slack@slack+margin[~strict]@margin[~strict]);grad=2*x.T@res
    gap=layer.d@params;smooth=layer.smooth@params
    reg=.1*float(gap@gap)+.5*float(smooth@smooth)+float((params[101:]-1)@(params[101:]-1))+.1*(params[0]-layer.reference_mean)**2
    rg=.2*layer.d.T@gap+layer.smooth.T@smooth;rg[101:]+=2*(params[101:]-1);rg[0]+=.2*(params[0]-layer.reference_mean)
    # Zero-margin soft hierarchy permits equality; unlike the prior recipe,
    # no positive minimum regional premium is rewarded.
    short=np.maximum(0.,-layer.order@params);reg+=10*float(short@short);rg-=20*layer.order.T@short
    short=np.maximum(0.,.05-layer.p@params);reg+=.25*float(np.mean(short**2));rg-=.5*layer.p.T@short/len(short)
    fusion=.3*layer.fusion_weights
    return value+strength*(reg+fusion@u)+1e-5*float(params@params),np.r_[grad+strength*rg+2e-5*params,strength*fusion]


def fit_slsqp(rows,layer,strength):
    x,offset=layer.array(rows);y=np.array([base.LABEL[r['winner']] for r in rows])
    initial=np.r_[layer.initial,abs(layer.d@layer.initial)]
    result=minimize(objective,initial,args=(x,offset,y,layer,strength),jac=True,method='SLSQP',bounds=[(None,None)]*101+[(.05,None)]*3+[(0,None)]*len(layer.d),constraints=[layer.constraints],options={'ftol':1e-8,'maxiter':1000})
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
    h=x[tied].T@x[tied]+strength*reg+1e-5*np.eye(N)
    quadratic=sparse.block_diag((2*h,sparse.csc_matrix((nu,nu)),2*sparse.eye(nh),20*strength*sparse.eye(no),(.5*strength/np_)*sparse.eye(np_)),format='csc')
    linear=np.zeros(total);linear[:N]=2*x[tied].T@offset[tied]
    linear[0]-=.2*strength*layer.reference_mean;linear[101:104]-=2*strength
    linear[us:hs]=strength*.3*layer.fusion_weights
    def block(matrix,start=None,count=0):
        left=sparse.csc_matrix(matrix)
        right=sparse.csc_matrix((len(matrix),total-N))
        if start is not None:
            right=sparse.hstack([sparse.csc_matrix((count,start-N)),sparse.eye(count),sparse.csc_matrix((count,total-start-count))],format='csc')
        return sparse.hstack([left,right],format='csc')
    constraint=sparse.vstack([block(layer.c),block(-layer.d,us,nu),block(layer.d,us,nu),
        block(y[strict,None]*x[strict],hs,nh),block(layer.order,os,no),block(layer.p,ps,np_),sparse.eye(total)],format='csc')
    bounds=np.r_[np.full(101,-np.inf),np.full(3,.05),np.zeros(total-N)]
    lower=np.r_[np.full(len(layer.c),-1e-7),np.zeros(2*nu),1-y[strict]*offset[strict],np.zeros(no),np.full(np_,.05),bounds]
    solver=osqp.OSQP();solver.setup(P=sparse.triu(quadratic,format='csc'),q=linear,A=constraint,l=lower,u=np.full(len(lower),np.inf),eps_abs=1e-8,eps_rel=1e-8,max_iter=200000,polishing=True,verbose=False)
    result=solver.solve(raise_error=False)
    if result.info.status!='solved':raise RuntimeError(f'QP failed: {result.info.status}')
    if np.min(constraint@result.x-lower)<-2e-6:raise RuntimeError('QP feasibility failed')
    return result.x[:N]


def predict(rows,layer,params,threshold):
    x,offset=layer.array(rows);return base.classify(offset+x@params,threshold)


def choose(rows,cfg,seed):
    _,y,g=baseline.protocol.common.get_arrays(rows,'additive');pred={s:np.zeros(len(y),dtype=int) for s in prior.STRENGTHS}
    for tr,va in base.folds(g,3,seed):
        training=[rows[i] for i in tr];valid=[rows[i] for i in va]
        design,beta=offering.fit(training,cfg);layer=Layer(design,beta)
        for strength in prior.STRENGTHS:pred[strength][va]=predict(valid,layer,fit(training,layer,strength),cfg['threshold'])
    metrics={s:base.metrics(y,p) for s,p in pred.items()}
    best=max(prior.STRENGTHS,key=lambda s:(round(metrics[s]['balanced_accuracy'],12),round(metrics[s]['accuracy'],12),s))
    return best,metrics[best]
