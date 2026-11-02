"""Refit all19 weights with convex joint hinge loss; frozen v21 context rules."""
import numpy as np
from scipy import sparse
import osqp
import domestic_shade_model as utility
import shade_vintage_shared_v21 as context
import joint_objective_v22 as joint

PRIMARY_ALPHA=.001
SENSITIVITY_ALPHA=.01

def design(rows,reference):
 x=utility.arrays(rows)[0] if rows and 'materiality_target' in rows[0] else np.array([utility.features(q['a'])-utility.features(q['b']) for q in rows])
 # Pair-context transformation remains fixed; all underlying19 weights are free to refit.
 p=reference['shade_parameters']
 for i,q in enumerate(rows):
  a,b=q['a'],q['b']
  if {a[1],b[1]}!={'golden','pale/straw'}:continue
  pale=a if a[1]=='pale/straw' else b;dom=pale[0] in utility.DOMESTIC;tare=min(a[3],b[3]);young=min(a[2],b[2])==20
  shrink=p[1] if tare>=125 else p[0] if tare>=120 else 0.
  shrink=shrink+(1-shrink)*p[2]*young
  if dom:shrink=0.
  if tare>=130:shrink=1.
  delta=(1 if b[1]=='pale/straw' else -1)*shrink;x[i,12]+=delta
  if dom:x[i,18]+=delta
 # Boundary/proximity map frozen to the baseline reference, not refitted coefficients.
 r=context.components(rows,reference)[1]
 return x,r

def problem(rows,reference,alpha):
 x,r=design(rows,reference);scale=reference['base_radius'];xn=x*scale/r[:,None];m,d,groups=joint.masks(rows);parts=[];targets=[];weights=[];ng=sum(v.any() for v in groups.values())
 for name,mask in groups.items():
  indices=np.flatnonzero(mask)
  if not len(indices):continue
  weight=1/(ng*len(indices))
  for i in indices:
   if name in ('meaningful','practical_direction','direction_only'):
    parts.append(d[i]*xn[i]);targets.append(1.05 if name=='meaningful' else .01);weights.append(weight)
   if name in ('practical_direction','practical_only'):
    parts.extend([xn[i],-xn[i]]);targets.extend([-1.,-1.]);weights.extend([weight,weight])
 a=np.array(parts);b=np.array(targets);w=np.array(weights);k=len(w)
 # Monotone original attribute increments; pure5lb and domestic adjacent shade <=base radius.
 c=utility.C;rules=np.zeros((2,19));rules[0,17]=1;rules[1,12]=rules[1,18]=1
 structural=np.vstack([c,rules]);lo=np.zeros(len(structural));hi=np.r_[np.full(len(c),np.inf),np.ones(2)]
 A=sparse.vstack([sparse.hstack([sparse.csc_matrix(structural),sparse.csc_matrix((len(structural),k))]),sparse.hstack([sparse.csc_matrix(a),sparse.eye(k)]),sparse.hstack([sparse.csc_matrix((k,19)),sparse.eye(k)])],format='csc')
 lower=np.r_[lo,b,np.zeros(k)];upper=np.r_[hi,np.full(2*k,np.inf)]
 P=sparse.diags(np.r_[np.full(19,2*alpha),2*w],format='csc')
 return P,A,lower,upper,scale

def fit(rows,reference,alpha=PRIMARY_ALPHA):
 P,A,lo,hi,scale=problem(rows,reference,alpha);solver=osqp.OSQP();solver.setup(P=P,q=np.zeros(P.shape[0]),A=A,l=lo,u=hi,eps_abs=1e-9,eps_rel=1e-9,max_iter=200000,polishing=True,verbose=False);result=solver.solve(raise_error=False)
 if result.info.status!='solved':raise RuntimeError(result.info.status)
 if np.min(A@result.x-lo)<-2e-7 or np.min(hi-A@result.x)<-2e-7:raise RuntimeError('constraint violation')
 return {'coefficients':(result.x[:19]*scale).tolist(),'alpha':alpha,'solver_objective':float(result.info.obj_val),'solver_status':result.info.status}

def predict(a,b,cfg):
 x,r=design([{'a':a,'b':b}],cfg['reference_context']);g=float((x@cfg['coefficients'])[0]);cut=float(r[0])
 return {'predicted_direction':'A' if g>1e-7 else 'B' if g<-1e-7 else None,'predicted_meaningfulness':'meaningful_difference' if abs(g)>cut+1e-8 else 'no_meaningful_difference','margin':g,'decision_radius':cut,'exact_price_equality':None,'prediction_source':'model_only','units':'pair-comparison score, not a standalone price'}
