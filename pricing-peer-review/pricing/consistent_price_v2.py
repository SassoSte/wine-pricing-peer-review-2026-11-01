"""Versioned low-end pricing refinement; shared canonical engine and V28 unchanged."""
from pathlib import Path
import argparse,json
from consistent_price_layer import Model as Engine
DEFAULT=Path(__file__).with_name('consistent-price-config-v2.json')
class Model(Engine):
 def __init__(self,path=DEFAULT):super().__init__(path)
 def price(self,offering):
  result=super().price(offering);result['model_id']=self.config['model_id'];result['regional_low_end_transfer_assumed']=offering[0]!='northeast' and result['attribute_loss']>self.config['prior_supported_loss']+1e-9
  match=next((x for x in self.config['low_end_constraints'] if x['offering']==list(offering)),None)
  if match:
   result['calibration_status']='expert_center_target' if match['type']=='approximate_center' else 'expert_upper_bound_target'
   result['expert_constraint']=match
  result['market_validation']='not_established'
  return result
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--offering',required=True,help='JSON [region,shade,years,tare]');a=p.parse_args();print(json.dumps(Model().price(json.loads(a.offering)),indent=2))
