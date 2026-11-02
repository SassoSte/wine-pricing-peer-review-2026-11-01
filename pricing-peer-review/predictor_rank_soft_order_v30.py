"""Updated intrinsic rankings with a separately frozen premium assessor."""
from pathlib import Path
from copy import deepcopy
import argparse,json
import numpy as np
from predictor_premium_context_extended_v30 import Model as Engine
from predictor_foundation_amplifiers_v30 import PARTS
DEFAULT_CONFIG=Path(__file__).with_name('rank-soft-order-frozen-premium-config-v30.json')
class ConfiguredEngine(Engine):
 def __init__(self,cfg):
  self.config=deepcopy(cfg);self.domain=cfg['domain'];self.weights=np.asarray(cfg['value_model']['coefficients'],float);self.head=cfg['premium_model'];self.hweights=np.asarray(self.head['coefficients'],float)
  if self.weights.shape!=(23,) or self.hweights.shape!=(14,) or not np.isfinite(self.weights).all() or not np.isfinite(self.hweights).all():raise ValueError('Invalid configuration')
class Model:
 def __init__(self,path=DEFAULT_CONFIG):
  self.config=json.loads(Path(path).read_text());self.premium_reference=ConfiguredEngine(self.config['premium_reference_model']);rank=deepcopy(self.config['premium_reference_model']);rank['value_model']=self.config['ranking_value_model'];self.ranking=ConfiguredEngine(rank);self.domain=self.ranking.domain
 def value(self,o):return self.ranking.value(o)
 def components(self,o):return self.ranking.components(o)
 def compare(self,a,b):
  p=self.premium_reference.compare(a,b);reference_direction=p['predicted_direction'];ca=self.ranking.components(a);cb=self.ranking.components(b);g=float((ca-cb).sum());direction='A' if g>1e-7 else 'B' if g<-1e-7 else None
  p.update(model=self.config['model_id'],value_a=float(ca.sum()),value_b=float(cb.sum()),margin=g,predicted_direction=direction,components_a=dict(zip(PARTS,ca.tolist())),components_b=dict(zip(PARTS,cb.tolist())),premium_reference_direction=reference_direction,ranking_reference_agreement=direction==reference_direction,premium_assessment_definition='Frozen unordered-pair meaningfulness assessor; score isnot calibrated winner-confidence. Ranking uses theupdated intrinsic value model.')
  return p
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--a',required=True);p.add_argument('--b',required=True);p.add_argument('--config',default=str(DEFAULT_CONFIG));args=p.parse_args();print(json.dumps(Model(args.config).compare(json.loads(args.a),json.loads(args.b)),indent=2))
