"""Replace domestic20 offering bonus with one matched-provenance5-year feature."""
import warnings
import numpy as np
from scipy import sparse
from scipy.optimize import milp,Bounds,LinearConstraint,linprog
import domestic_vintage_context_v27 as parent
ANCHORS=parent.ANCHORS

def pair_features(a,b):
 raw=parent.additive.additive_features(a)-parent.additive.additive_features(b)
 eligible=a[0]==b[0] and abs(a[2]-b[2])==5 and {a[1],b[1]}=={'golden','pale/straw'}
 return np.r_[raw,float(np.sign(b[2]-a[2])) if eligible else 0.]

def design(rows):return np.array([pair_features(q['a'],q['b']) for q in rows])

def fit(rows,time_limit=3.):
 x=design(rows);ids,weights,cons=parent.classification_constraints(rows,x);n=19;k=len(ids);nv=n+k+n;lo=np.r_[np.full(9,-8.),np.zeros(n-9),np.zeros(k+n)];hi=np.r_[np.full(n,8.),np.ones(k),np.full(n,8.)];hi[17]=.9999999;protected=[]
 for j,i in enumerate(ids):
  if rows[i]['id'] in ANCHORS:hi[n+j]=0;protected.append(rows[i]['id'])
 A=[];b=[]
 for j,row,target in cons:
  minimum=np.maximum(row,0)@lo[:n]+np.minimum(row,0)@hi[:n];v=np.zeros(nv);v[:n]=row;v[n+j]=max(0.,target-minimum);A.append(v);b.append(target)
 v=np.zeros(nv);v[12]=v[17]=-1;A.append(v);b.append(-.99999)
 for j in range(n):
  for sign in (-1,1):
   v=np.zeros(nv);v[j]=sign;v[n+k+j]=1;A.append(v);b.append(0.)
 obj=np.r_[np.zeros(n),weights,np.full(n,1e-8)];integ=np.r_[np.zeros(n),np.ones(k),np.zeros(n)];matrix=sparse.csc_matrix(np.array(A))
 with warnings.catch_warnings():
  warnings.filterwarnings('ignore',message='Unrecognized options detected')
  result=milp(obj,integrality=integ,bounds=Bounds(lo,hi),constraints=LinearConstraint(matrix,np.array(b),np.full(len(b),np.inf)),options={'time_limit':time_limit,'mip_rel_gap':.001,'threads':1})
 if result.x is None:raise RuntimeError('No feasible incumbent: '+str(result.message))
 if np.min(matrix@result.x-np.array(b)) < -1e-6:raise RuntimeError('Constraint violation')
 return {'kind':'additive_matched_vintage_pair','coefficients':result.x[:n].tolist(),'decision_radius':1.,'protected_training_ids':protected,'solver_status':int(result.status),'solver_message':result.message,'mip_gap':float(result.mip_gap),'objective':float(result.fun),'time_limit_seconds':time_limit,'solver_tolerance_met':bool(result.status==0),'exact_optimum_proven':bool(result.status==0 and result.mip_gap<1e-12)}

def predict(a,b,cfg):
 g=float(pair_features(a,b)@cfg['coefficients']);r=cfg['decision_radius'];return {'predicted_direction':'A' if g>1e-7 else 'B' if g<-1e-7 else None,'predicted_meaningfulness':'meaningful_difference' if abs(g)>r+1e-8 else 'no_meaningful_difference','margin':g,'decision_radius':r,'exact_price_equality':None,'prediction_source':'model_only','units':'pair-comparison score, not a standalone price'}

def feasibility(rows,kind):
 x=parent.design(rows) if kind=='domestic20' else design(rows);ids,_,cons=parent.classification_constraints(rows,x);A=[-row for _,row,_ in cons];b=[-v for _,_,v in cons];v=np.zeros(19);v[12]=v[17]=1;A.append(v);b.append(.99999)
 with warnings.catch_warnings():
  warnings.filterwarnings('ignore',message='Unrecognized options detected')
  result=linprog(np.zeros(19),A_ub=np.array(A),b_ub=np.array(b),bounds=[(None,None)]*9+[(0,None)]*10,method='highs',options={'threads':1})
 return {'feasible':bool(result.success),'status':int(result.status),'qualification':'Feasibility only, not prediction validation or numeric premium estimates.'}
