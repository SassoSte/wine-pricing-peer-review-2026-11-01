"""Experimental v28 ranking with one calibrated winning-tare premium correction."""
from pathlib import Path
import json,numpy as np
from predictor_v27 import Model as Engine
DEFAULT_CONFIG=Path(__file__).with_name('premium-config-v35.json')
class Model(Engine):
 def __init__(self,path=DEFAULT_CONFIG):
  self.package=json.loads(Path(path).read_text());self.config=self.package['baseline'];self.domain=self.config['domain'];self.weights=np.asarray(self.config['coefficients'],float);self.beta=float(self.package['premium_correction']['coefficient'])
  if self.weights.shape!=(20,) or not np.isfinite(self.weights).all() or not np.isfinite(self.beta) or self.beta<0:raise ValueError('Invalid config')
  self.weights.setflags(write=False)
 def compare(self,a,b):
  result=super().compare(a,b);g=result['margin'];opposed=(a[2]-b[2])*(a[3]-b[3])<0;lighter_wins=g*(b[3]-a[3])>1e-7
  strength=max(0.,(abs(a[3]-b[3])-10)/5) if abs(a[2]-b[2])==5 and opposed and lighter_wins else 0.
  score=abs(g)-result['decision_radius']+self.beta*strength
  result.update(model=self.package['model_id'],predicted_meaningfulness='meaningful_difference' if score>self.config['classification']['meaningfulness_epsilon'] else 'no_meaningful_difference',premium_correction=self.beta*strength,premium_decision_score=score)
  return result
