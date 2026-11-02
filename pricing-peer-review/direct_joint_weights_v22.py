"""Deterministic constrained coordinate search on actual joint correctness."""
import numpy as np
import joint_weight_refit_v22 as qp
import joint_objective_v22 as joint

def fit(rows,reference,starts):
 x,r=qp.design(rows,reference);scale=reference['base_radius'];xn=x*scale/r[:,None];xn[:,12]-=xn[:,18]
 m,d,groups=joint.masks(rows);pos=np.isfinite(m)&(m!=0);neg=m==0;kd=d!=0;both=np.isfinite(m)&kd;active=[v for v in groups.values() if v.any()]
 def evaluate(ps):
  gg=ps@xn.T;sign=np.where(gg>1e-7/scale,1,np.where(gg<-1e-7/scale,-1,0));large=abs(gg)>1.;correct=np.ones(gg.shape,dtype=bool);loss=np.zeros(gg.shape)
  for name,mask in groups.items():
   signed=gg[:,mask]*d[mask]
   if name=='meaningful':correct[:,mask]=large[:,mask]&(sign[:,mask]==d[mask]);loss[:,mask]=np.maximum(0,1.05-signed)**2
   elif name=='practical_direction':correct[:,mask]=~large[:,mask]&(sign[:,mask]==d[mask]);loss[:,mask]=np.maximum(0,.01-signed)**2+np.maximum(0,abs(gg[:,mask])-1)**2
   elif name=='practical_only':correct[:,mask]=~large[:,mask];loss[:,mask]=np.maximum(0,abs(gg[:,mask])-1)**2
   else:correct[:,mask]=sign[:,mask]==d[mask];loss[:,mask]=np.maximum(0,.01-signed)**2
  macro=np.mean([correct[:,v].mean(axis=1) for v in active],axis=0);ls=np.mean([loss[:,v].mean(axis=1) for v in active],axis=0)
  return [(round(macro[i],12),round(correct[i,both].mean(),12),-round(ls[i],12),-float(p@p)) for i,p in enumerate(ps)]
 winners=[]
 for initial in starts:
  p=np.array(initial)/scale;p[18]+=p[12];p[9:]=np.maximum(p[9:],0);p[17:]=np.minimum(p[17:],1-1e-7)
  for step in (.5,.2,.1,.05,.02,.005):
   for sweep in range(2):
    for col in range(19):
     ps=np.tile(p,(5,1));ps[:,col]+=np.array([-2,-1,0,1,2])*step
     if col>=9:ps[:,col]=np.maximum(ps[:,col],0)
     if col in (17,18):ps[:,col]=np.minimum(ps[:,col],1-1e-7)
     keys=evaluate(ps);best=max(range(5),key=lambda i:keys[i]);p=ps[best]
  winners.append((evaluate(p[None,:])[0],p))
 key,p=max(winners,key=lambda q:q[0]);beta=p.copy();beta[18]-=beta[12];beta*=scale
 return {'coefficients':beta.tolist(),'training_joint_balanced_accuracy':key[0],'training_both_axes_accuracy':key[1],'training_signed_joint_loss':-key[2],'optimizer':'two-start constrained coordinate search; no global optimality claim'}
