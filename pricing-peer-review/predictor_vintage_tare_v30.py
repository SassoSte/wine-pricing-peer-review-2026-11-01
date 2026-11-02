"""Experimental intrinsic values with a guarded vintage/tare meaningfulness boundary."""
from pathlib import Path
import argparse,json
from predictor_regional_mature_v30 import Model as IntrinsicModel
DEFAULT_CONFIG=Path(__file__).with_name('vintage-tare-guarded-config-v30.json')
class Model(IntrinsicModel):
 def __init__(self,path=DEFAULT_CONFIG):
  super().__init__(path)
  if not 0<self.config['vintage_tare_radius']<=1:raise ValueError('Invalid contextual radius')
 def compare(self,a,b):
  p=super().compare(a,b);s=self.config['threshold_scope'];y,o=(a,b) if a[2]<b[2] else (b,a)
  guarded=s['guard_same_shade_younger30_older_tare_at_most115'] and y[2]==30 and o[3]<=115 and a[1]==b[1]
  eligible=a[0]==b[0] and abs(a[2]-b[2])==s['age_gap'] and y[2]<=s['maximum_younger_age'] and y[3]-o[3]==s['younger_heavier_by_lb'] and abs(self.domain['shades'].index(a[1])-self.domain['shades'].index(b[1]))<=s['maximum_shade_steps'] and not guarded
  younger_sign=1 if a[2]<b[2] else -1
  if eligible and p['margin']*younger_sign>1e-7:
   p['decision_radius']=self.config['vintage_tare_radius'];p['predicted_meaningfulness']='meaningful_difference' if abs(p['margin'])>p['decision_radius']+1e-8 else 'no_meaningful_difference'
  return p
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--a',required=True);p.add_argument('--b',required=True);p.add_argument('--config',default=str(DEFAULT_CONFIG));args=p.parse_args();print(json.dumps(Model(args.config).compare(json.loads(args.a),json.loads(args.b)),indent=2))
