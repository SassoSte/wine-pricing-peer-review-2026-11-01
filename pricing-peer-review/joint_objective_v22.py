"""Joint decision objective with partial-label support; same two residuals/grid."""
from itertools import product
import numpy as np
import residual_fixes_v22 as residual
import refit_simple_benchmark_v16 as separate

def masks(rows):
 _,m,d,_=residual.previous.utility.arrays(rows);known=np.isfinite(m);pos=known&(m!=0);neg=m==0;kd=d!=0
 return m,d,{'meaningful':pos,'practical_direction':neg&kd,'practical_only':neg&~kd,'direction_only':~known&kd}

def evaluations(rows,margins,radii):
 g=np.atleast_2d(margins);r=np.broadcast_to(radii,g.shape);m,d,groups=masks(rows);sign=np.where(g>1e-7,1,np.where(g<-1e-7,-1,0));large=abs(g)>r;correct=np.ones(g.shape,dtype=bool)
 for name,mask in groups.items():
  if name=='meaningful':correct[:,mask]=large[:,mask]&(sign[:,mask]==d[mask])
  elif name=='practical_direction':correct[:,mask]=~large[:,mask]&(sign[:,mask]==d[mask])
  elif name=='practical_only':correct[:,mask]=~large[:,mask]
  else:correct[:,mask]=sign[:,mask]==d[mask]
 supported=np.logical_or.reduce(list(groups.values()));both=np.isfinite(m)&(d!=0)
 normalized=g/np.maximum(r,1e-6);loss=np.zeros(g.shape)
 for name,mask in groups.items():
  signed=normalized[:,mask]*d[mask]
  if name=='meaningful':loss[:,mask]=np.maximum(0,1.05-signed)**2
  elif name=='practical_direction':loss[:,mask]=np.maximum(0,.01-signed)**2+np.maximum(0,abs(normalized[:,mask])-1)**2
  elif name=='practical_only':loss[:,mask]=np.maximum(0,abs(normalized[:,mask])-1)**2
  else:loss[:,mask]=np.maximum(0,.01-signed)**2
 macro=np.mean([correct[:,mask].mean(axis=1) for mask in groups.values() if mask.any()],axis=0)
 jointloss=np.mean([loss[:,mask].mean(axis=1) for mask in groups.values() if mask.any()],axis=0)
 return correct,supported,both,groups,macro,jointloss

def score(rows,g,r):
 c,s,b,groups,macro,loss=evaluations(rows,g,r)
 return {'supported_n':int(s.sum()),'correct':int(c[0,s].sum()),'accuracy':float(c[0,s].mean()),'balanced_accuracy':float(macro[0]),'both_axes_n':int(b.sum()),'both_axes_correct':int(c[0,b].sum()),'both_axes_accuracy':float(c[0,b].mean()),'signed_joint_loss':float(loss[0]),'by_group':{k:{'n':int(v.sum()),'correct':int(c[0,v].sum()),'accuracy':float(c[0,v].mean()) if v.any() else None} for k,v in groups.items()}}

def fit(rows,evidence,cfg,objective):
 params=np.array(list(product(np.linspace(0,1,21),repeat=2)));g,r,h=residual.components(rows,cfg);gg=g[None,:]+params@h.T;c,s,b,groups,macro,loss=evaluations(rows,gg,r);direct=np.array(separate.verified_materiality(evidence));valid=direct&np.isfinite(masks(rows)[0]);directjoint=c[:,valid].mean(axis=1)
 if objective=='joint_accuracy':key=lambda i:(round(macro[i],12),round(directjoint[i],12),-round(loss[i],12),-float(params[i].sum()))
 elif objective=='joint_loss':key=lambda i:(-round(loss[i],12),round(macro[i],12),-float(params[i].sum()))
 else:raise ValueError(objective)
 i=max(range(len(params)),key=key)
 return {'residual_parameters':params[i].tolist(),'training_joint_accuracy':float(macro[i]),'training_joint_loss':float(loss[i]),'objective':objective}
