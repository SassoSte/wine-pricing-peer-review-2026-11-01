"""Bounded mixed-integer fit of actual joint correctness, no pair-specific rules."""
import warnings
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy import sparse
import joint_models_v27 as models
import joint_objective_v22 as joint

def fit(rows,time_limit=3.):
 x,offset,r,scale=models.design(rows,'additive',None);m,d,groups=joint.masks(rows);supported=np.logical_or.reduce(list(groups.values()));ids=np.flatnonzero(supported);index={i:j for j,i in enumerate(ids)};n=18;k=len(ids);nv=n+k+n;lower=np.r_[np.full(9,-8.),np.zeros(9),np.zeros(k+n)];upper=np.r_[np.full(17,8.),1-1e-7,np.ones(k),np.full(n,8.)];weights=np.zeros(k);A=[];b=[]
 for name,mask in groups.items():
  ii=np.flatnonzero(mask)
  if not len(ii):continue
  for i in ii:
   weights[index[i]]=1/(sum(v.any() for v in groups.values())*len(ii));constraints=[]
   if name in ('meaningful','practical_direction','direction_only'):constraints.append((d[i]*x[i],1.00001 if name=='meaningful' else .00001))
   if name in ('practical_direction','practical_only'):constraints.extend([(x[i],-.99999),(-x[i],-.99999)])
   for row,target in constraints:
    minimum=np.maximum(row,0)@lower[:n]+np.minimum(row,0)@upper[:n];big=max(0.,target-minimum);v=np.zeros(nv);v[:n]=row;v[n+index[i]]=big;A.append(v);b.append(target)
 # Every pure5lb change, including pale125->130, must remain nonmeaningful.
 row=np.zeros(nv);row[12]=row[17]=-1;A.append(row);b.append(-.99999)
 # L1 tiny tie-break; primary criterion remains four-group joint error.
 for j in range(n):
  for sign in (-1,1):
   row=np.zeros(nv);row[j]=sign;row[n+k+j]=1;A.append(row);b.append(0.)
 objective=np.r_[np.zeros(n),weights,np.full(n,1e-8)];integrality=np.r_[np.zeros(n),np.ones(k),np.zeros(n)]
 with warnings.catch_warnings():
  warnings.filterwarnings('ignore',message='Unrecognized options detected')
  result=milp(objective,integrality=integrality,bounds=Bounds(lower,upper),constraints=LinearConstraint(sparse.csc_matrix(np.array(A)),np.array(b),np.full(len(b),np.inf)),options={'time_limit':time_limit,'mip_rel_gap':.001,'threads':1})
 if result.x is None:raise RuntimeError('No feasible incumbent: '+str(result.message))
 if np.min(np.array(A)@result.x-np.array(b)) < -1e-6:raise RuntimeError('Constraint violation')
 return {'kind':'additive','coefficients':result.x[:n].tolist(),'reference_context':None,'decision_radius':1.,'optimizer':'MILP joint classification with single shared row-error binary for both axes','solver_status':int(result.status),'solver_message':result.message,'mip_gap':float(result.mip_gap),'objective':float(result.fun),'time_limit_seconds':time_limit,'global_optimum_proven':bool(result.status==0),'unlabelled_excluded':int(len(rows)-k)}
