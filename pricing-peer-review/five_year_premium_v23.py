"""One fractional five-year premium over frozen joint weight refit."""
import numpy as np
import joint_weight_refit_v22 as base
import joint_objective_v22 as joint

def components(rows,cfg,scope):
 x,r=base.design(rows,cfg['reference_context']);beta=np.array(cfg['coefficients']);g=x@beta;h=[]
 for q in rows:
  a,b=q['a'],q['b'];eligible=a[0]==b[0] and abs(a[2]-b[2])==5
  if scope=='adjacent_shade':eligible=eligible and {a[1],b[1]}=={'golden','pale/straw'}
  elif scope!='same_provenance':raise ValueError(scope)
  age_delta=(base.utility.features(a)[13:17]-base.utility.features(b)[13:17])@beta[13:17]
  h.append(float(age_delta) if eligible else 0.)
 return g,r,np.array(h)

def fit(rows,cfg,scope):
 g,r,h=components(rows,cfg,scope);params=np.linspace(0,1,21);gg=g[None,:]+params[:,None]*h;correct,supported,both,groups,macro,loss=joint.evaluations(rows,gg,r)
 idx=max(range(len(params)),key=lambda i:(round(macro[i],12),round(correct[i,both].mean(),12),-round(loss[i],12),-params[i]))
 return {'five_year_fraction':float(params[idx]),'scope':scope,'training_joint_balanced':float(macro[idx]),'training_joint_loss':float(loss[idx])}

def predict(a,b,cfg):
 g,r,h=components([{'a':a,'b':b}],cfg['base_model'],cfg['scope']);gap=float((g+cfg['five_year_fraction']*h)[0]);cut=float(r[0])
 return {'predicted_direction':'A' if gap>1e-7 else 'B' if gap<-1e-7 else None,'predicted_meaningfulness':'meaningful_difference' if abs(gap)>cut+1e-8 else 'no_meaningful_difference','margin':gap,'decision_radius':cut,'exact_price_equality':None,'prediction_source':'model_only','units':'pair-comparison score, not a standalone price'}
