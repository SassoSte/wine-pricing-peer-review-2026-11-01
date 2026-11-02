"""One additional domestic20-year coefficient over simple additive utility."""
import warnings
import numpy as np
from scipy import sparse
from scipy.optimize import milp,Bounds,LinearConstraint,linprog
import joint_models_v27 as additive
import joint_objective_v22 as joint
ANCHORS=('round49-2','round50-4','round49-17')

def features(option):
 return np.r_[additive.additive_features(option),float(option[0] in additive.features.DOMESTIC and option[2]==20)]

def design(rows):return np.array([features(q['a'])-features(q['b']) for q in rows])

def classification_constraints(rows,x):
 m,d,groups=joint.masks(rows);supported=np.logical_or.reduce(list(groups.values()));ids=np.flatnonzero(supported);index={i:j for j,i in enumerate(ids)};constraints=[];weights=np.zeros(len(ids));ng=sum(v.any() for v in groups.values())
 for name,mask in groups.items():
  ii=np.flatnonzero(mask)
  if not len(ii):continue
  for i in ii:
   j=index[i];weights[j]=1/(ng*len(ii))
   if name in ('meaningful','practical_direction','direction_only'):constraints.append((j,d[i]*x[i],1.00001 if name=='meaningful' else .00001))
   if name in ('practical_direction','practical_only'):constraints.extend([(j,x[i],-.99999),(j,-x[i],-.99999)])
 return ids,weights,constraints

def fit(rows,protect_anchors=False,time_limit=3.):
 x=design(rows);ids,weights,cons=classification_constraints(rows,x);n=19;k=len(ids);nv=n+k+n;lo=np.r_[np.full(9,-8.),np.zeros(n-9),np.zeros(k+n)];hi=np.r_[np.full(n,8.),np.ones(k),np.full(n,8.)];hi[17]=.9999999;protected=[]
 if protect_anchors:
  for j,i in enumerate(ids):
   if rows[i]['id'] in ANCHORS:hi[n+j]=0;protected.append(rows[i]['id'])
 A=[];b=[]
 for j,row,target in cons:
  minimum=np.maximum(row,0)@lo[:n]+np.minimum(row,0)@hi[:n];v=np.zeros(nv);v[:n]=row;v[n+j]=max(0.,target-minimum);A.append(v);b.append(target)
 v=np.zeros(nv);v[12]=v[17]=-1;A.append(v);b.append(-.99999)
 for j in range(n):
  for sign in (-1,1):
   v=np.zeros(nv);v[j]=sign;v[n+k+j]=1;A.append(v);b.append(0.)
 objective=np.r_[np.zeros(n),weights,np.full(n,1e-8)];integrality=np.r_[np.zeros(n),np.ones(k),np.zeros(n)];matrix=sparse.csc_matrix(np.array(A))
 with warnings.catch_warnings():
  warnings.filterwarnings('ignore',message='Unrecognized options detected')
  result=milp(objective,integrality=integrality,bounds=Bounds(lo,hi),constraints=LinearConstraint(matrix,np.array(b),np.full(len(b),np.inf)),options={'time_limit':time_limit,'mip_rel_gap':.001,'threads':1})
 if result.x is None:raise RuntimeError('No feasible incumbent: '+str(result.message))
 if np.min(matrix@result.x-np.array(b)) < -1e-6:raise RuntimeError('Constraint violation')
 return {'kind':'additive_domestic20','coefficients':result.x[:n].tolist(),'decision_radius':1.,'protected_training_ids':protected,'solver_status':int(result.status),'solver_message':result.message,'mip_gap':float(result.mip_gap),'objective':float(result.fun),'time_limit_seconds':time_limit,'solver_tolerance_met':bool(result.status==0),'exact_optimum_proven':bool(result.status==0 and result.mip_gap<1e-12)}

def predict(a,b,cfg):
 g=float((features(a)-features(b))@cfg['coefficients']);r=cfg['decision_radius'];return {'predicted_direction':'A' if g>1e-7 else 'B' if g<-1e-7 else None,'predicted_meaningfulness':'meaningful_difference' if abs(g)>r+1e-8 else 'no_meaningful_difference','margin':g,'decision_radius':r,'exact_price_equality':None,'prediction_source':'model_only','units':'preference score, not money'}

def feasibility(rows,enabled):
 x=design(rows)
 if not enabled:x=x[:,:18]
 ids,_,cons=classification_constraints(rows,x);n=x.shape[1];A=[-row for _,row,_ in cons];b=[-target for _,_,target in cons];v=np.zeros(n);v[12]=v[17]=1;A.append(v);b.append(.99999)
 with warnings.catch_warnings():
  warnings.filterwarnings('ignore',message='Unrecognized options detected')
  result=linprog(np.zeros(n),A_ub=np.array(A),b_ub=np.array(b),bounds=[(None,None)]*9+[(0,None)]*(n-9),method='highs',options={'threads':1})
 return {'feasible':bool(result.success),'status':int(result.status),'message':result.message,'witness_coefficients':result.x.tolist() if result.success else None,'qualification':'Feasibility witness only, not fitted model or monetary estimates.'}
