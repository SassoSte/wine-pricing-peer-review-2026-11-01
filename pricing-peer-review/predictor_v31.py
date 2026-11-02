"""Experimental v31 intrinsic ranking with explicit equality and updated premium head."""
from pathlib import Path
import argparse,json
import numpy as np
from predictor_rank_soft_order_v30 import ConfiguredEngine
DEFAULT_CONFIG=Path(__file__).with_name('model-config-v31.json')
class Model:
 def __init__(self,path=DEFAULT_CONFIG):
  self.config=json.loads(Path(path).read_text());self.reference=ConfiguredEngine(self.config['premium_reference_model']);self.domain=self.config['domain'];self.weights=np.asarray(self.config['ranking_model']['coefficients'],float);self.eps=self.config['equality_tolerance']
  if self.weights.shape!=(32,) or not np.isfinite(self.weights).all():raise ValueError('Invalid32-coefficient ranking model')
 def features(self,o):
  f=self.reference._features(o);v,t=self.reference._quality(o);c=.5+.25*(v+t);j=3 if o[1]=='pale/straw' and o[3]==130 else self.domain['shades'].index(o[1]);weak=min((o[2]-20)/15,1.)*(4-j)/4
  return np.r_[f,[float(o[0]==z)*c*weak for z in self.domain['provenances'][1:]]]
 def components(self,o):
  f=self.features(o)*self.weights;return {'vintage':float(f[:4].sum()),'tare':float(f[4:8].sum()),'vintage_tare':float(f[8]),'provenance_base':float(f[9:18].sum()),'shade':float(f[18:22].sum()),'all_top':float(f[22]),'provenance_maturity_shade':float(f[23:].sum())}
 def value(self,o):return float(self.features(o)@self.weights)
 def compare(self,a,b):
  p=self.reference.compare(a,b);g=float((self.features(a)-self.features(b))@self.weights);equal=abs(g)<=self.eps;direction=None if equal else 'A' if g>0 else 'B';premium=bool(p['premium_justified'] and not equal)
  p.update(model=self.config['model_id'],value_a=self.value(a),value_b=self.value(b),margin=g,predicted_direction=direction,predicted_value_relation='equal' if equal else 'A_higher' if g>0 else 'B_higher',predicted_meaningfulness='meaningful_difference' if premium else 'no_meaningful_difference',premium_justified=premium,exact_price_equality=bool(equal),equality_tolerance=self.eps,equality_definition='Predicted equality of intrinsic pricingvalues within numericalsolver tolerance,not a broad near-tie band.',components_a=self.components(a),components_b=self.components(b))
  return p
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--a',required=True);p.add_argument('--b',required=True);p.add_argument('--config',default=str(DEFAULT_CONFIG));args=p.parse_args();print(json.dumps(Model(args.config).compare(json.loads(args.a),json.loads(args.b)),indent=2))
