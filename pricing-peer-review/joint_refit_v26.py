"""Joint refit of19 weights with v25 context and comparison boundaries frozen."""
import numpy as np
import older_dark_scoped_v25 as baseline
import joint_weight_refit_v22 as linear
import joint_objective_v22 as joint

def design(rows,reference):
 five=reference['base_model'];underlying=five['base_model'];context=underlying['reference_context'];beta=np.array(underlying['coefficients']);x,r=linear.design(rows,context)
 for i,q in enumerate(rows):
  a,b=q['a'],q['b'];eligible=a[0]==b[0] and abs(a[2]-b[2])==5
  if five['scope']=='adjacent_shade':eligible=eligible and {a[1],b[1]}=={'golden','pale/straw'}
  if eligible:x[i,13:17]+=five['five_year_fraction']*(linear.utility.features(a)[13:17]-linear.utility.features(b)[13:17])
 g,cut,h=baseline.components(rows,five);old=g+h@reference['adjustments'];offset=old-x@beta
 return x,offset,r

def fit(rows,reference):
 x,offset,r=design(rows,reference);underlying=reference['base_model']['base_model'];scale=underlying['reference_context']['base_radius'];beta=np.array(underlying['coefficients']);xn=x*scale/r[:,None];xn[:,12]-=xn[:,18];on=offset/r
 micro=reference['adjustments'][2]*max(0.,scale*(1-1e-7)-beta[10]);amber_cap=max(0.,(scale*(1-1e-7)-micro)/scale)
 m,d,groups=joint.masks(rows);both=np.isfinite(m)&(d!=0);active=[v for v in groups.values() if v.any()]
 def evaluate(ps):
  gg=ps@xn.T+on;sign=np.where(gg>1e-7/r,1,np.where(gg<-1e-7/r,-1,0));large=abs(gg)>1.;correct=np.ones(gg.shape,dtype=bool);loss=np.zeros(gg.shape)
  for name,mask in groups.items():
   signed=gg[:,mask]*d[mask]
   if name=='meaningful':correct[:,mask]=large[:,mask]&(sign[:,mask]==d[mask]);loss[:,mask]=np.maximum(0,1.05-signed)**2
   elif name=='practical_direction':correct[:,mask]=~large[:,mask]&(sign[:,mask]==d[mask]);loss[:,mask]=np.maximum(0,.01-signed)**2+np.maximum(0,abs(gg[:,mask])-1)**2
   elif name=='practical_only':correct[:,mask]=~large[:,mask];loss[:,mask]=np.maximum(0,abs(gg[:,mask])-1)**2
   else:correct[:,mask]=sign[:,mask]==d[mask];loss[:,mask]=np.maximum(0,.01-signed)**2
  macro=np.mean([correct[:,v].mean(axis=1) for v in active],axis=0);ls=np.mean([loss[:,v].mean(axis=1) for v in active],axis=0)
  return [(round(macro[i],12),round(correct[i,both].mean(),12),-round(ls[i],12),-float(p@p)) for i,p in enumerate(ps)]
 def constrain(ps,col=None):
  ps[:,9:]=np.maximum(ps[:,9:],0);ps[:,17:]=np.minimum(ps[:,17:],1-1e-7);ps[:,10]=np.minimum(ps[:,10],amber_cap);return ps
 winners=[]
 for multiplier in (1.,.8):
  p=beta*multiplier/scale;p[18]+=p[12];p=constrain(p[None,:])[0]
  for step in (.5,.2,.1,.05,.02,.005):
   for sweep in range(2):
    for col in range(19):
     ps=np.tile(p,(5,1));ps[:,col]+=np.array([-2,-1,0,1,2])*step;ps=constrain(ps);keys=evaluate(ps);p=ps[max(range(5),key=lambda i:keys[i])]
  winners.append((evaluate(p[None,:])[0],p))
 key,p=max(winners,key=lambda v:v[0]);b=p.copy();b[18]-=b[12];b*=scale
 return {'coefficients':b.tolist(),'reference_context':reference,'training_joint_balanced':key[0],'training_both_axes_accuracy':key[1],'training_signed_joint_loss':-key[2],'optimizer':'two deterministic train-only starts; constrained19-weight coordinate search, no global optimality claim'}

def predict(a,b,cfg):
 x,offset,r=design([{'a':a,'b':b}],cfg['reference_context']);g=float((x@cfg['coefficients']+offset)[0]);cut=float(r[0])
 return {'predicted_direction':'A' if g>1e-7 else 'B' if g<-1e-7 else None,'predicted_meaningfulness':'meaningful_difference' if abs(g)>cut+1e-8 else 'no_meaningful_difference','margin':g,'decision_radius':cut,'exact_price_equality':None,'prediction_source':'model_only','units':'pair-comparison score, not a standalone price'}
