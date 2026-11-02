"""Same19-coefficient v17 model, stronger soft penalty for legacy no-difference rows."""
import numpy as np
from scipy import sparse
from scipy.optimize import minimize,LinearConstraint
import osqp
import domestic_shade_model as original
import refit_simple_benchmark_v16 as validation

features=original.features
arrays=original.arrays
constraints=original.constraints


def legacy_negative_weights(targets,evidence,multiplier):
    _,m,_,_=arrays(targets);verified=np.array(validation.verified_materiality(evidence));return np.where((m==0)&~verified,multiplier,1.)


def objective(beta,x,m,d,alpha,weights):
    value,gradient=original.simple.objective(beta,x,m,d,alpha);negative=m==0;gap=x@beta;excess=np.maximum(0.,abs(gap[negative])-.25);extra=weights[negative]-1.
    return value+float((extra*excess)@excess),gradient+2*x[negative].T@(extra*np.sign(gap[negative])*excess)


def fit_reference(targets,evidence,alpha,radius,multiplier):
    x,m,d,_=arrays(targets);c,lo,hi,_=constraints(targets,evidence,radius,True);weights=legacy_negative_weights(targets,evidence,multiplier)
    result=minimize(objective,np.zeros(19),args=(x,m,d,alpha,weights),jac=True,method='SLSQP',bounds=[(None,None)]*9+[(0,None)]*9+[(None,None)],constraints=[LinearConstraint(c,lo,hi)],options={'ftol':1e-10,'maxiter':2000})
    if not result.success:raise RuntimeError(result.message)
    return result.x


def fit(targets,evidence,alpha,radius,multiplier):
    x,m,d,_=arrays(targets);meaningful=np.isfinite(m)&(m!=0);similar=m==0;directional=(d!=0)&~meaningful;weights=legacy_negative_weights(targets,evidence,multiplier)
    nm=int(sum(meaningful));ns=int(sum(similar));nd=int(sum(directional));n=19;hm=n;hs=hm+nm;hd=hs+ns;total=hd+nd
    P=sparse.diags(np.r_[np.full(n,2*alpha),np.full(nm,2.),2*weights[similar],np.full(nd,2.)],format='csc');q=np.zeros(total)
    def block(matrix,start=None,count=0):
        right=sparse.csc_matrix((len(matrix),total-n))
        if start is not None:right=sparse.hstack([sparse.csc_matrix((count,start-n)),sparse.eye(count),sparse.csc_matrix((count,total-start-count))],format='csc')
        return sparse.hstack([sparse.csc_matrix(matrix),right],format='csc')
    c,lo,hi,_=constraints(targets,evidence,radius,True)
    A=sparse.vstack([block(c),block(m[meaningful,None]*x[meaningful],hm,nm),block(-x[similar],hs,ns),block(x[similar],hs,ns),block(d[directional,None]*x[directional],hd,nd),sparse.eye(total)],format='csc')
    lower=np.r_[lo,np.ones(nm),np.full(2*ns,-.25),np.full(nd,.05),np.full(9,-np.inf),np.zeros(9),-np.inf,np.zeros(total-n)];upper=np.r_[hi,np.full(len(lower)-len(hi),np.inf)]
    solver=osqp.OSQP();solver.setup(P=P,q=q,A=A,l=lower,u=upper,eps_abs=1e-9,eps_rel=1e-9,max_iter=200000,polishing=True,verbose=False);result=solver.solve(raise_error=False)
    if result.info.status!='solved':raise RuntimeError(result.info.status)
    if np.min(A@result.x-lower)<-2e-7 or np.min(upper-A@result.x)<-2e-7:raise RuntimeError('Constraint violation')
    return result.x[:n]
