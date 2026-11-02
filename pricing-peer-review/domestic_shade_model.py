"""19-coefficient shade correction with training-only high-confidence constraints."""
from itertools import product
import numpy as np
from scipy import sparse
import osqp
from scipy.optimize import minimize,LinearConstraint,linprog
import compare_models as base
import build_meaningful_benchmark as simple
import refit_simple_benchmark_v16 as validation

DOMESTIC={'central','northwest','northeast','southwest','southeast'}
FEATURE='domestic x pale/straw'
STRICT_EPS=1e-4


def features(option):return np.r_[base.features(option),float(option[0] in DOMESTIC and option[1]=='pale/straw')]


def arrays(targets):
    _,m,d,g=simple.arrays(targets);x=np.array([features(r['a'])-features(r['b']) for r in targets]);return x,m,d,g


def structural_constraints():
    rows=[]
    for z,s,a,w in product(base.ZONES,base.SHADES,base.AGES,(110,115,120,125,130)):
        f=features([z,s,a,w]);i=base.SHADES.index(s)
        if a>20:rows.append(features([z,s,a-5,w])-f)
        if i<4:rows.append(features([z,base.SHADES[i+1],a,w])-f)
        if w>110:rows.append(features([z,s,a,w-5])-f)
    return np.unique(rows,axis=0)

C=structural_constraints()


def constraints(targets,evidence,radius,protect=True):
    matrices=[C];lower=[np.zeros(len(C))];upper=[np.full(len(C),np.inf)];ids=[]
    # Existing user rules:5lb alone and domestic golden/pale alone are negligible.
    rule=np.zeros((2,19));rule[0,17]=1;rule[1,12]=1;rule[1,18]=1
    matrices.append(rule);lower.append(np.zeros(2));upper.append(np.full(2,radius))
    if protect:
        x,m,d,_=arrays(targets);direct=validation.verified_materiality(evidence)
        for i,(t,is_direct) in enumerate(zip(targets,direct)):
            if not is_direct or not np.isfinite(m[i]):continue
            ids.append(t['id'])
            if m[i]==0:
                matrices.append(x[i:i+1]);lower.append(np.array([-radius]));upper.append(np.array([radius]))
                if d[i]!=0:matrices.append(d[i]*x[i:i+1]);lower.append(np.array([STRICT_EPS]));upper.append(np.array([np.inf]))
            else:matrices.append(d[i]*x[i:i+1]);lower.append(np.array([radius+STRICT_EPS]));upper.append(np.array([np.inf]))
    return np.vstack(matrices),np.concatenate(lower),np.concatenate(upper),ids


def fit_reference(targets,evidence,alpha,radius,protect=True):
    x,m,d,_=arrays(targets);c,lo,hi,ids=constraints(targets,evidence,radius,protect)
    result=minimize(simple.objective,np.zeros(19),args=(x,m,d,alpha),jac=True,method='SLSQP',bounds=[(None,None)]*9+[(0,None)]*9+[(None,None)],constraints=[LinearConstraint(c,lo,hi)],options={'ftol':1e-10,'maxiter':2000})
    if not result.success:raise RuntimeError(result.message)
    if np.min(c@result.x-lo)<-1e-7 or np.min(hi-c@result.x)<-1e-7:raise RuntimeError('Constraint violation')
    return result.x


def fit(targets,evidence,alpha,radius,protect=True):
    x,m,d,_=arrays(targets);meaningful=np.isfinite(m)&(m!=0);similar=m==0;directional=(d!=0)&~meaningful
    nm=int(sum(meaningful));ns=int(sum(similar));nd=int(sum(directional));n=19;hm=n;hs=hm+nm;hd=hs+ns;total=hd+nd
    P=sparse.diags(np.r_[np.full(n,2*alpha),np.full(nm+ns+nd,2.)],format='csc');q=np.zeros(total)
    def block(matrix,start=None,count=0):
        right=sparse.csc_matrix((len(matrix),total-n))
        if start is not None:right=sparse.hstack([sparse.csc_matrix((count,start-n)),sparse.eye(count),sparse.csc_matrix((count,total-start-count))],format='csc')
        return sparse.hstack([sparse.csc_matrix(matrix),right],format='csc')
    c,lo,hi,_=constraints(targets,evidence,radius,protect)
    A=sparse.vstack([block(c),block(m[meaningful,None]*x[meaningful],hm,nm),block(-x[similar],hs,ns),block(x[similar],hs,ns),block(d[directional,None]*x[directional],hd,nd),sparse.eye(total)],format='csc')
    lower=np.r_[lo,np.ones(nm),np.full(2*ns,-.25),np.full(nd,.05),np.full(9,-np.inf),np.zeros(9),-np.inf,np.zeros(total-n)]
    upper=np.r_[hi,np.full(len(lower)-len(hi),np.inf)]
    solver=osqp.OSQP();solver.setup(P=P,q=q,A=A,l=lower,u=upper,eps_abs=1e-9,eps_rel=1e-9,max_iter=200000,polishing=True,verbose=False)
    result=solver.solve(raise_error=False)
    if result.info.status!='solved':raise RuntimeError('Domestic-shade QP: '+result.info.status)
    if np.min(A@result.x-lower)<-2e-7 or np.min(upper-A@result.x)<-2e-7:raise RuntimeError('QP constraint violation')
    return result.x[:n]
