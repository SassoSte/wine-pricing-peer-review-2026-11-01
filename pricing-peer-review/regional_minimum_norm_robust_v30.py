"""Real minimum-L2 tie-break preserving every correct primary-fit training judgment."""
from copy import deepcopy
import numpy as np
from scipy import sparse
import osqp
from scipy.optimize import minimize,LinearConstraint
from types import SimpleNamespace
import intrinsic_regional_v30 as base
import joint_objective_v22 as joint

def polish(rows,cfg,design=None,structural=None):
 design=design or (lambda rs:base.design(rs,'regional_vintage'));structural=structural or (lambda:base.structural('regional_vintage'))
 x=design(rows);old=np.array(cfg['coefficients']);n=len(old);correct,supported,*_=joint.evaluations(rows,x@old,1.);keep=correct[0]&supported
 ids,weights,cons=base.classification_constraints(rows,x);A=[];lo=[];hi=[]
 for j,row,target in cons:
  if keep[ids[j]]:A.append(row);lo.append(target);hi.append(np.inf)
 st,l,u=structural();A.extend(st);lo.extend(l);hi.extend(u)
 lower=np.r_[np.full(9,-8.),np.zeros(n-9)];lower[[19,21,23]]=-8
 A.extend(np.eye(n));lo.extend(lower);hi.extend(np.full(n,8.))
 mat=sparse.csc_matrix(np.array(A));lo=np.array(lo);hi=np.array(hi)
 solver=osqp.OSQP();solver.setup(P=sparse.csc_matrix(2*np.eye(n)),q=np.zeros(n),A=mat,l=lo,u=hi,verbose=False,eps_abs=1e-9,eps_rel=1e-9,max_iter=200000,polishing=True);solver.warm_start(x=old);r=solver.solve()
 if r.info.status_val not in (1,2):
  fallback=minimize(lambda v:float(v@v),old,jac=lambda v:2*v,method='SLSQP',constraints=[LinearConstraint(mat.toarray(),lo,hi)],options={'ftol':1e-12,'maxiter':3000})
  if not fallback.success:raise RuntimeError('QP fallback: '+fallback.message)
  r=SimpleNamespace(x=fallback.x,info=SimpleNamespace(status_val=1,status='SLSQP minimum-L2 fallback after OSQP iteration limit'))
 if np.min(mat@r.x-lo)<-1e-6 or np.min(hi-mat@r.x)<-1e-6:raise RuntimeError('QP constraint violation')
 after,_,*_=joint.evaluations(rows,x@r.x,1.);assert np.all(after[0,keep]);assert np.linalg.norm(r.x)<=np.linalg.norm(old)+1e-5
 out=deepcopy(cfg);out.update(coefficients=r.x.tolist(),primary_incumbent_objective=cfg['objective'],postfit='minimum_L2_preserve_correct_training_labels',postfit_status=r.info.status,coefficient_norm_before=float(np.linalg.norm(old)),coefficient_norm_after=float(np.linalg.norm(r.x)),preserved_training_ids=[q['id'] for q,k in zip(rows,keep) if k],training_joint_before=joint.score(rows,x@old,1.),training_joint_after=joint.score(rows,x@r.x,1.))
 return out
