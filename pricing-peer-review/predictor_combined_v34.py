"""Frozen intrinsic ranking plus independently frozen premium assessment; no evidence lookup."""
from pathlib import Path
import json,numpy as np
from predictor_v27 import Model as PremiumEngine
DEFAULT_CONFIG=Path(__file__).with_name('combined-config-v34.json')
class Model:
 def __init__(self,path=DEFAULT_CONFIG):
  self.config=json.loads(Path(path).read_text());self.domain=self.config['domain'];self.weights=np.asarray(self.config['ranking']['value_model']['coefficients'],float)
  if self.weights.shape!=(21,) or not np.isfinite(self.weights).all():raise ValueError('Invalid ranking coefficients')
  self.premium=PremiumEngine.__new__(PremiumEngine);self.premium.config=self.config['premium'];self.premium.domain=self.premium.config['domain'];self.premium.weights=np.asarray(self.premium.config['coefficients'],float)
  if self.premium.weights.shape!=(20,) or not np.isfinite(self.premium.weights).all():raise ValueError('Invalid premium coefficients')
  self.weights.setflags(write=False);self.premium.weights.setflags(write=False)
 def features(self,o):
  self.premium._offering(o) # Domain validation.
  z,s,a,w=o;d=self.domain;f=np.array([float(z==p) for p in d['provenances'][1:]]+[float(d['shades'].index(s)>=i) for i in range(1,5)]+[float(a<=i) for i in (35,30,25,20)]+[float(w<=i) for i in (125,120,115,110)])
  if s=='pale/straw' and w==130:f[12]=0
  return f
 def value(self,o):return float(self.features(o)@self.weights)
 def compare(self,a,b):
  g=float((self.features(a)-self.features(b))@self.weights);direction='A' if g>1e-7 else 'B' if g<-1e-7 else None;p=self.premium.compare(a,b);meaningful=p['predicted_meaningfulness']=='meaningful_difference';conflict=meaningful and p['predicted_direction']!=direction
  return {'model':self.config['model_id'],'predicted_direction':direction,'exact_price_equality':abs(g)<=1e-7,'predicted_meaningfulness':p['predicted_meaningfulness'],'margin':g,'premium_reference_direction':p['predicted_direction'],'premium_reference_margin':p['margin'],'head_conflict':conflict,'prediction_source':'model_only','units':'preference scores, not money'}
