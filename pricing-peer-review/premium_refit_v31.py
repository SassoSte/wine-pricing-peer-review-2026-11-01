import numpy as np
from scipy.optimize import minimize,Bounds,LinearConstraint
from scipy.special import expit
import joint_objective_v22 as joint
from premium_context_adjacent_shade_v30 import HEAD_RIDGE,HEAD_NAMES,PROTECTED

def fit_head(rows,oof_h,full_h,weighting="joint_groups"):
 m,d,_=joint.masks(rows);known=np.isfinite(m);y=(m[known]!=0).astype(float);h=oof_h[known];mean=h.mean(axis=0);std=h.std(axis=0);mean[0]=0.;std[0]=1.;std[std<1e-6]=1.;x=(h-mean)/std
 n=len(y);pos=max(1,sum(y));neg=max(1,n-sum(y));weights=np.where(y==1,.5/pos,.5/neg)
 if weighting=='joint_groups':
  groups=[y==1,(y==0)&(d[known]!=0),(y==0)&(d[known]==0)];active=sum(v.any() for v in groups);weights=np.zeros(n)
  for mask in groups:
   if mask.any():weights[mask]=1/(active*mask.sum())
 def objective(b):
  z=x@b;pen=b.copy();pen[0]=0
  return float(np.sum(weights*(np.logaddexp(0,z)-y*z))+.5*HEAD_RIDGE*(pen@pen)),x.T@(weights*(expit(z)-y))+HEAD_RIDGE*pen
 # Meaningfulness protection uses only known training rows under the fitted training utility.
 C=[];ids=[]
 for i,q in enumerate(rows):
  if (q['id'] in PROTECTED or q.get('latest_source_id','').startswith('round57-')) and np.isfinite(m[i]):
   C.append((1 if m[i]!=0 else -1)*(full_h[i]-mean)/std);ids.append(q['id'])
 constraints=[]
 if C:constraints=[LinearConstraint(np.array(C),np.full(len(C),.02),np.full(len(C),np.inf))]
 lo=np.full(x.shape[1],-np.inf);hi=np.full(x.shape[1],np.inf);lo[1]=0.;lo[8]=0.;lo[13]=0.;hi[11]=0.
 r=minimize(objective,np.zeros(x.shape[1]),jac=True,method='SLSQP',bounds=Bounds(lo,hi),constraints=constraints,options={'ftol':1e-10,'maxiter':1500})
 if not r.success:raise RuntimeError('Premium head: '+r.message)
 if C and np.min(np.array(C)@r.x)<.02-1e-6:raise RuntimeError('Premium head control violation')
 return {'coefficients':r.x.tolist(),'mean':mean.tolist(),'scale':std.tolist(),'feature_names':HEAD_NAMES,'ridge':HEAD_RIDGE,'weighting':weighting,'protected_training_ids':ids,'solver_message':r.message,'cutoff':.5}

