"""Frozen foundation values with one guarded shared-context premium feature."""
from pathlib import Path
import json,argparse
import numpy as np
from predictor_foundation_amplifiers_v30 import Model as ValueEngine,PARTS
DEFAULT_CONFIG=Path(__file__).with_name('premium-shared-context-config-v30.json')
class Model(ValueEngine):
 def __init__(self,path=DEFAULT_CONFIG):
  self.config=json.loads(Path(path).read_text());self.domain=self.config['domain'];self.weights=np.asarray(self.config['value_model']['coefficients'],float);self.head=self.config['premium_model'];self.hweights=np.asarray(self.head['coefficients'],float)
  if self.weights.shape!=(23,) or self.hweights.shape!=(14,) or not np.isfinite(self.weights).all() or not np.isfinite(self.hweights).all():raise ValueError('Invalid model dimensions/coefficients')
  if np.any(np.asarray(self.head['scale'])<=0):raise ValueError('Invalid standardization')
 def feature_active(self,a,b,g):
  s=self.config['premium_context'];y,o=(a,b) if a[2]<b[2] else (b,a)
  if s['exclude_younger35_with_heavier_tare'] and y[2]==35 and y[3]>o[3]:return False
  return a[0]==b[0] and abs(a[2]-b[2])==s['vintage_gap_years'] and abs(a[3]-b[3])<=s['maximum_tare_gap_lb'] and a[1] in s['shades'] and b[1] in s['shades'] and g*(1 if a[2]<b[2] else -1)>1e-7
 def compare(self,a,b):
  a,b=list(a),list(b);ca=self.components(a);cb=self.components(b);delta=ca-cb;g=float(delta.sum());sg=1 if g>1e-7 else -1 if g<-1e-7 else 0;va,ta=self._quality(a);vb,tb=self._quality(b);cd=abs(self._completion(a)-self._completion(b));pure5=a[:3]==b[:3] and abs(a[3]-b[3])==5 and cd==0;opposition=max(0.,(abs(delta).sum()-abs(g))/2);isolated=self.feature_active(a,b,g)
  h=np.array([1.,abs(g),*(sg*delta[:5]).tolist(),opposition,cd,(va+vb)/2,(ta+tb)/2,float(pure5),abs(self.domain['shades'].index(a[1])-self.domain['shades'].index(b[1]))/4,float(isolated)]);z=float(((h-np.asarray(self.head['mean']))/np.asarray(self.head['scale']))@self.hweights);score=float(1/(1+np.exp(-z))) if z>=0 else float(np.exp(z)/(1+np.exp(z)));large=score>self.head['cutoff'] and sg!=0
  return {'model':self.config['model_id'],'value_a':float(ca.sum()),'value_b':float(cb.sum()),'margin':g,'predicted_direction':'A' if sg>0 else 'B' if sg<0 else None,'predicted_meaningfulness':'meaningful_difference' if large else 'no_meaningful_difference','premium_justified':bool(large),'premium_justification_score':score,'shared_context_feature_active':bool(isolated),'components_a':dict(zip(PARTS,ca.tolist())),'components_b':dict(zip(PARTS,cb.tolist())),'prediction_source':'model_only','exact_price_equality':None,'value_units':self.config['value_units'],'premium_score_units':self.config['premium_score_units']}
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--a',required=True);p.add_argument('--b',required=True);p.add_argument('--config',default=str(DEFAULT_CONFIG));args=p.parse_args();print(json.dumps(Model(args.config).compare(json.loads(args.a),json.loads(args.b)),indent=2))
