"""Controlled joint fits: simple additive utility versus existing v26 structure."""
import numpy as np
import domestic_shade_model as features
import joint_refit_v26 as contextual
import joint_objective_v22 as joint

def additive_features(option,domestic=False):
 f=features.features(option).copy();zone,shade,age,tare=option
 # One mandatory offering rule, not pair-specific weighting: pale=golden at130lb.
 if shade=='pale/straw' and tare==130:f[12]=0;f[18]=0
 if domestic:f[12]-=f[18];return f
 return f[:18]

def design(rows,kind,reference):
 if kind=='contextual':
  x,offset,r=contextual.design(rows,reference);scale=reference['base_model']['base_model']['reference_context']['base_radius'];xn=x.copy();xn[:,12]-=xn[:,18];return xn,offset,r,scale
 domestic=kind=='additive_domestic'
 x=np.array([additive_features(q['a'],domestic)-additive_features(q['b'],domestic) for q in rows]);return x,np.zeros(len(rows)),np.ones(len(rows)),1.

def fit(rows,kind,reference,start_coefficients):
 x,offset,r,scale=design(rows,kind,reference);xn=x*scale/r[:,None];on=offset/r;m,d,groups=joint.masks(rows);both=np.isfinite(m)&(d!=0);active=[v for v in groups.values() if v.any()];n=x.shape[1]
 if kind=='contextual':
  under=reference['base_model']['base_model'];room=max(0.,scale*(1-1e-7)-under['coefficients'][10]);amber_cap=max(0.,1-1e-7-reference['adjustments'][2]*room/scale)
 else:amber_cap=None
 def project(ps):
  ps[:,9:]=np.maximum(ps[:,9:],0)
  if kind=='contextual':ps[:,17:]=np.minimum(ps[:,17:],1-1e-7);ps[:,10]=np.minimum(ps[:,10],amber_cap)
  else:
   ps[:,17]=np.minimum(ps[:,17],1-1e-7)
   # Any5lb step, including pale125->130, stays inside the nonmeaningful band.
   ps[:,12]=np.minimum(ps[:,12],1-1e-7-ps[:,17])
   if n==19:ps[:,18]=np.minimum(ps[:,18],1-1e-7-ps[:,17])
  return ps
 def evaluate(ps):
  gg=ps@xn.T+on;sign=np.where(gg>1e-7/r,1,np.where(gg<-1e-7/r,-1,0));large=abs(gg)>1;correct=np.ones(gg.shape,bool);loss=np.zeros(gg.shape)
  for name,mask in groups.items():
   signed=gg[:,mask]*d[mask]
   if name=='meaningful':correct[:,mask]=large[:,mask]&(sign[:,mask]==d[mask]);loss[:,mask]=np.maximum(0,1.05-signed)**2
   elif name=='practical_direction':correct[:,mask]=~large[:,mask]&(sign[:,mask]==d[mask]);loss[:,mask]=np.maximum(0,.01-signed)**2+np.maximum(0,abs(gg[:,mask])-1)**2
   elif name=='practical_only':correct[:,mask]=~large[:,mask];loss[:,mask]=np.maximum(0,abs(gg[:,mask])-1)**2
   else:correct[:,mask]=sign[:,mask]==d[mask];loss[:,mask]=np.maximum(0,.01-signed)**2
  macro=np.mean([correct[:,v].mean(axis=1) for v in active],axis=0);ls=np.mean([loss[:,v].mean(axis=1) for v in active],axis=0)
  return [(round(macro[i],12),round(correct[i,both].mean(),12),-round(ls[i],12),-float(p@p)) for i,p in enumerate(ps)]
 oldscale=reference['base_model']['base_model']['reference_context']['base_radius'];start=np.array(start_coefficients)/oldscale
 if n==19:start[18]+=start[12]
 else:start=start[:18]
 winners=[]
 for mult in (1.,.8):
  p=project((start*mult)[None,:])[0]
  for step in (.5,.2,.1,.05,.02,.005):
   for sweep in range(2):
    for col in range(n):
     ps=np.tile(p,(5,1));ps[:,col]+=np.array([-2,-1,0,1,2])*step;ps=project(ps);keys=evaluate(ps);p=ps[max(range(5),key=lambda i:keys[i])]
  winners.append((evaluate(p[None,:])[0],p))
 key,p=max(winners,key=lambda q:q[0]);coeff=p*scale
 return {'kind':kind,'coefficients':coeff.tolist(),'reference_context':reference if kind=='contextual' else None,'decision_radius':1. if kind!='contextual' else None,'training_joint_balanced':key[0],'training_both_axes_accuracy':key[1],'training_joint_loss':-key[2]}

def margins(rows,cfg):
 x,offset,r,_=design(rows,cfg['kind'],cfg.get('reference_context'));return x@cfg['coefficients']+offset,r

def predict(a,b,cfg):
 g,r=margins([{'a':a,'b':b}],cfg);v=float(g[0]);cut=float(r[0]);return {'predicted_direction':'A' if v>1e-7 else 'B' if v<-1e-7 else None,'predicted_meaningfulness':'meaningful_difference' if abs(v)>cut+1e-8 else 'no_meaningful_difference','margin':v,'decision_radius':cut,'exact_price_equality':None,'prediction_source':'model_only','units':'preference score, not money'}
