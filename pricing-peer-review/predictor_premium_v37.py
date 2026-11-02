"""Experimental premium-only context correction; all ranking weights remain frozen."""
from pathlib import Path
import json,numpy as np
from predictor_premium_v35 import Model as LargeTare
DEFAULT_CONFIG=Path(__file__).with_name('premium-config-v37.json')
class Model(LargeTare):
 def __init__(self,path=DEFAULT_CONFIG):
  self.context_package=json.loads(Path(path).read_text());self.package=self.context_package['large_tare'];self.config=self.package['baseline'];self.domain=self.config['domain'];self.weights=np.asarray(self.config['coefficients'],float);self.beta=float(self.package['premium_correction']['coefficient']);self.gamma=float(self.context_package['context_correction']['coefficient'])
  if self.weights.shape!=(20,) or not np.isfinite(self.weights).all() or not 0<=self.gamma<=1:raise ValueError('Invalid configuration')
  self.weights.setflags(write=False)
 def compare(self,a,b):
  result=super().compare(a,b);g=result['margin'];winner,loser=(a,b) if g>0 else (b,a);feature=0.
  if abs(g)>1e-7 and loser[1]=='brown' and winner[1] in ('copper','amber'):
   c=self._pair(a,b)*self.weights;sg=1 if g>0 else -1;secondary=max(0.,sg*sum(c[:9]))+max(0.,sg*sum(c[9:13]));feature=max(0.,(winner[3]-120)/10)*secondary
  score=result['premium_decision_score']-self.gamma*feature
  result.update(model=self.context_package['model_id'],premium_context_deduction=self.gamma*feature,premium_decision_score=score,predicted_meaningfulness='meaningful_difference' if score>self.config['classification']['meaningfulness_epsilon'] else 'no_meaningful_difference')
  return result
