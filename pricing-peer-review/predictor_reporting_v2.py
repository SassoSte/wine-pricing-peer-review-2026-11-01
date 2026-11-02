"""Consolidated reporting over frozen predictors. No fitting or evidence lookup."""
from pathlib import Path
import argparse,hashlib,json
from predictor_v28 import Model as V28
from predictor_premium_v37 import Model as Contextual
ROOT=Path(__file__).resolve().parent
DEFAULT_CONFIG=ROOT/'reporting-config-v2.json'
class Model:
 def __init__(self,config=DEFAULT_CONFIG,backend=None):
  self.config=json.loads(Path(config).read_text());self.backend=backend or self.config['default_backend']
  if self.backend not in self.config['backends']:raise ValueError('Unknown backend')
  self.spec=self.config['backends'][self.backend]
  for path,digest in self.spec['source_hashes'].items():
   if hashlib.sha256((ROOT/path).read_bytes()).hexdigest()!=digest:raise ValueError('Frozen source changed: '+path)
  self.engine=(V28 if self.backend=='v28' else Contextual)(ROOT/self.spec['config'])
 def compare(self,a,b):
  raw=self.engine.compare(a,b);band=self.spec.get('band');direction=raw['predicted_direction'];score=abs(raw['margin']) if self.backend=='v28' else raw['premium_decision_score']+1
  if band is None:
   zone='not_calibrated';meaningful=None;boundary=None
  elif score<band['lower']:
   zone='small_directional_advantage' if direction else 'no_meaningful_premium';meaningful=False;boundary=False
  elif score<band['upper']:
   zone='borderline_premium';meaningful=None;boundary=True
  else:zone='meaningful_premium';meaningful=True;boundary=False
  return {'backend':self.backend,'premium_reporting_score':score,'direction':direction,'premium_zone':zone,'meaningful_premium':meaningful,'exact_price_equality':None,'uncertainty':{'premium_boundary':boundary,'premium_assessment_withheld':meaningful is None,'calibrated_probability':None,'direction_confidence':'not_calibrated','band_status':self.spec['band_status']},'equality_status':'not_established_by_pair_comparator','legacy_prediction':raw,'units':'preference score, not money'}
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--a',required=True);p.add_argument('--b',required=True);p.add_argument('--backend',default=None);args=p.parse_args();print(json.dumps(Model(backend=args.backend).compare(json.loads(args.a),json.loads(args.b)),indent=2))
