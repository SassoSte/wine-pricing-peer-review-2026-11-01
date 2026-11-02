"""One bounded pair-context correction; only matched-provenance/tare tradeoffs."""
import numpy as np
import contextual_fixes_v19 as previous
import refit_simple_benchmark_v16 as metrics

def feature(a,b,beta):
 previous.utility.features(a);previous.utility.features(b)
 if a[0]!=b[0] or a[0] in previous.utility.DOMESTIC or a[3]!=b[3] or {a[1],b[1]}!={'golden','pale/straw'}:return 0.
 pale=a if a[1]=='pale/straw' else b;gold=b if a[1]=='pale/straw' else a
 if pale[2]<=gold[2]:return 0.
 heavy=min(1.,max(0.,(a[3]-115)/10))
 return (1 if b[1]=='pale/straw' else -1)*heavy*max(0.,beta[12])

def arrays(rows,cfg):
 g,h,r,f=previous.components(rows,cfg['underlying_coefficients'],cfg['base_radius'],cfg['context_kind'],cfg['context_coefficient'])
 assert cfg['shade_fraction']==0
 return g,r+cfg['boundary_increment']*f,np.array([feature(q['a'],q['b'],cfg['underlying_coefficients']) for q in rows])

def fit(rows,evidence,cfg):
 g,r,h=arrays(rows,cfg);direct=metrics.verified_materiality(evidence);records=[]
 for coefficient in np.linspace(0,1,21):
  score=metrics.score(rows,g+coefficient*h,r,direct);objective=(score['direction']['accuracy']+score['materiality']['balanced_accuracy'])/2
  records.append({'coefficient':float(coefficient),'objective':objective,'score':score})
 best=max(records,key=lambda q:(round(q['objective'],12),round(q['score']['directly_supported_materiality']['accuracy'],12),-q['score']['materiality']['false_meaningful'],-q['coefficient']))
 return best['coefficient'],records

def predict(a,b,cfg):
 g,r,h=arrays([{'a':a,'b':b}],cfg);gap=float(g[0]+cfg.get('narrow_shade_coefficient',0)*h[0]);cut=float(r[0])
 return {'predicted_direction':'A' if gap>1e-7 else 'B' if gap<-1e-7 else None,'predicted_meaningfulness':'meaningful_difference' if abs(gap)>cut else 'no_meaningful_difference','margin':gap,'decision_radius':cut,'exact_price_equality':None,'prediction_source':'model_only','units':'pair-comparison score, not a standalone price'}
