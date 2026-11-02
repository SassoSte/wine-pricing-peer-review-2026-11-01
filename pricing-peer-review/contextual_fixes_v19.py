"""Two bounded residual parameters over immutable v18 utility and boundary."""
import numpy as np
import domestic_shade_model as utility
import contextual_meaningfulness as boundary
import refit_simple_benchmark_v16 as metrics

def heavy_pale(o):
 utility.features(o)
 return float(o[0] not in utility.DOMESTIC and o[1]=='pale/straw')*min(1.,max(0.,(o[3]-115)/10))

def components(rows,beta,radius,kind,eta):
 x=np.array([utility.features(q['a'])-utility.features(q['b']) for q in rows]);g=x@np.asarray(beta)
 # Fraction of existing foreign pale increment removed at higher shared tare.
 h=np.array([heavy_pale(q['b'])-heavy_pale(q['a']) for q in rows])*max(0.,beta[12])
 f=np.array([boundary.context_feature(q['a'],q['b'],beta,radius,kind) for q in rows])
 return g,h,radius*(1+eta*f),radius*f

def fit(rows,evidence,beta,radius,kind,eta,arm):
 g,h,r,f=components(rows,beta,radius,kind,eta);direct=metrics.verified_materiality(evidence)
 grid=np.linspace(0,1,21);best=None;choice=None
 for shade in grid if arm in ('shade','combined') else [0.]:
  for widen in grid if arm in ('boundary','combined') else [0.]:
   score=metrics.score(rows,g+shade*h,r+widen*f,direct)
   objective=(score['direction']['accuracy']+score['materiality']['balanced_accuracy'])/2
   key=(round(objective,12),round(score['directly_supported_materiality']['accuracy'],12),-score['materiality']['false_meaningful'],-(shade+widen),-shade)
   if best is None or key>best:best=key;choice={'shade_fraction':float(shade),'boundary_increment':float(widen),'training_objective':objective}
 return choice

def predict(a,b,cfg):
 g,h,r,f=components([{'a':a,'b':b}],cfg['underlying_coefficients'],cfg['base_radius'],cfg['context_kind'],cfg['context_coefficient']);gap=float((g+cfg['shade_fraction']*h)[0]);cut=float((r+cfg['boundary_increment']*f)[0])
 return {'predicted_direction':'A' if gap>1e-7 else 'B' if gap<-1e-7 else None,'predicted_meaningfulness':'meaningful_difference' if abs(gap)>cut else 'no_meaningful_difference','margin':gap,'decision_radius':cut,'exact_price_equality':None,'prediction_source':'model_only','units':'model score, not money'}
