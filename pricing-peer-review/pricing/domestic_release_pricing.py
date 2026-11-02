"""Locked provisional domestic release-price reference; no new pricing mathematics."""
from pathlib import Path
import argparse,hashlib,json
from consistent_price_v2 import Model as PricingEngine
ROOT=Path(__file__).resolve().parent.parent
DEFAULT=Path(__file__).with_name('domestic-release-policy-v2.json')
class Model:
 def __init__(self,path=DEFAULT):
  self.policy=json.loads(Path(path).read_text())
  for name,digest in self.policy['source_hashes'].items():
   if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=digest:raise ValueError('Locked pricing component changed: '+name)
  self.engine=PricingEngine(ROOT/self.policy['pricing_config'])
 def price(self,offering):
  if not offering or offering[0] not in self.policy['approved_regions']:raise ValueError('Region outside locked domestic pricing scope')
  result=self.engine.price(offering)
  return {**result,'reference_status':'locked_provisional_domestic_release_schedule','currency':'USD','batch_basis':'seat-origin/reference-status','excluded_costs':['fees','taxes','delivery'],'qualification':'Reference estimate under stated comparable terms; not a transaction price, delivered cost, or confidence guarantee.'}
 def compare(self,a,b):
  pa=self.price(a)['price_usd'];pb=self.price(b)['price_usd'];return {'price_a':pa,'price_b':pb,'difference':pa-pb,'ratio':pa/pb}
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--offering',required=True,help='JSON [region,shade,vintage_years,tare_lb]');a=p.parse_args();print(json.dumps(Model().price(json.loads(a.offering)),indent=2))
