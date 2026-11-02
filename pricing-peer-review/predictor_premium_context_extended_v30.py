"""Experimental wider shared-context premium feature; intrinsic values unchanged."""
from pathlib import Path
import json,argparse
from predictor_premium_context_v30 import Model as Parent
DEFAULT_CONFIG=Path(__file__).with_name('premium-context-extended-config-v30.json')
class Model(Parent):
 def __init__(self,path=DEFAULT_CONFIG):super().__init__(path)
 def feature_active(self,a,b,g):
  s=self.config['premium_context'];y,o=(a,b) if a[2]<b[2] else (b,a);light=a[1] in s['shades'] and b[1] in s['shades']
  shade_ok=light or (s['allow_adjacent_nonlight_shades'] and abs(self.domain['shades'].index(a[1])-self.domain['shades'].index(b[1]))<=s['maximum_shade_steps'])
  if s['exclude_younger35_with_heavier_tare'] and y[2]==35 and y[3]>o[3]:return False
  if not light:
   if y[2]>s['nonlight_maximum_younger_age']:return False
   guard=s['nonlight_same_shade_low_tare_guard']
   if y[2]==guard['younger_age'] and o[3]<=guard['maximum_older_tare'] and y[3]>o[3] and a[1]==b[1]:return False
  return shade_ok and a[0]==b[0] and abs(a[2]-b[2])==s['vintage_gap_years'] and abs(a[3]-b[3])<=s['maximum_tare_gap_lb'] and g*(1 if a[2]<b[2] else -1)>1e-7
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--a',required=True);p.add_argument('--b',required=True);p.add_argument('--config',default=str(DEFAULT_CONFIG));args=p.parse_args();print(json.dumps(Model(args.config).compare(json.loads(args.a),json.loads(args.b)),indent=2))
