"""Bounded pair-context shade premium; same-shade tare comparisons unchanged."""
import numpy as np
import contextual_fixes_v19 as previous
import refit_simple_benchmark_v16 as metrics

def feature(a,b,beta):
 previous.utility.features(a);previous.utility.features(b)
 if a[0]!=b[0] or a[0] in previous.utility.DOMESTIC or a[3]!=b[3] or {a[1],b[1]}!={'golden','pale/straw'}:return np.zeros(2)
 sign=1 if b[1]=='pale/straw' else -1
 # Distinguish supported >=125 band from WE120; earlier EE120 direction retained.
 return sign*max(0.,beta[12])*np.array([float(a[3]>=125),float(a[3]==120 and a[0]=='Western Europe')])

def arrays(rows,cfg):
 g,_,r,f=previous.components(rows,cfg['underlying_coefficients'],cfg['base_radius'],cfg['context_kind'],cfg['context_coefficient']);assert cfg['shade_fraction']==0
 return g,r+cfg['boundary_increment']*f,np.array([feature(q['a'],q['b'],cfg['underlying_coefficients']) for q in rows])

def fit(rows,evidence,cfg,arm):
 g,r,h=arrays(rows,cfg);direct=metrics.verified_materiality(evidence);best=None;choice=None
 for high in np.linspace(0,1,21):
  for mid in np.linspace(0,1,21) if arm=='two_contexts' else [0.]:
   s=metrics.score(rows,g+h@np.array([high,mid]),r,direct);obj=(s['direction']['accuracy']+s['materiality']['balanced_accuracy'])/2
   key=(round(obj,12),round(s['directly_supported_materiality']['accuracy'],12),-s['materiality']['false_meaningful'],-(high+mid),-mid)
   if best is None or key>best:best=key;choice={'shade_coefficients':[float(high),float(mid)],'training_objective':obj}
 return choice

def predict(a,b,cfg):
 g,r,h=arrays([{'a':a,'b':b}],cfg);gap=float((g+h@np.array(cfg.get('shade_coefficients',[0.,0.])))[0]);cut=float(r[0])
 return {'predicted_direction':'A' if gap>1e-7 else 'B' if gap<-1e-7 else None,'predicted_meaningfulness':'meaningful_difference' if abs(gap)>cut else 'no_meaningful_difference','margin':gap,'decision_radius':cut,'exact_price_equality':None,'prediction_source':'model_only','units':'pair-comparison score, not a standalone price'}
