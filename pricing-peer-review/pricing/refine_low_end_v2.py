"""Append two expert-constrained knots; preserve previous fitted range exactly."""
from pathlib import Path
import json,math,copy,itertools,hashlib
import numpy as np
from consistent_price_layer import Model as Previous,attribute_loss
from consistent_price_v2 import Model
P=Path(__file__).resolve().parent;ROOT=P.parent
def main():
 old=json.loads((P/'consistent-price-config-v1.json').read_text());judgments=json.loads((P/'low-end-checks-v1.json').read_text());by={q['id']:q for q in judgments['checks']};assert by['ne-amber-35-120']['expert_estimate']['amount']==450;assert by['ne-brown-40-130']['expert_price_constraint']['amount']==300;assert by['ne-brown-40-130']['expert_price_constraint']['type']=='upper_bound'
 cfg=copy.deepcopy(old);cfg['model_id']='consistent-price-layer-v2';cfg['parent_config']='consistent-price-config-v1.json';cfg['prior_supported_loss']=old['log_discount_knots'][-1][0];cfg['low_end_constraints']=[];anchor=cfg['regional_anchors']['northeast']['price']
 for id,price,kind in [('ne-amber-35-120',450.,'approximate_center'),('ne-brown-40-130',300.,'upper_bound')]:
  q=by[id];loss=attribute_loss(q['offering'],cfg['domain'],cfg['base_coefficients']);log_discount=math.log(anchor/price)
  if kind=='upper_bound':log_discount=float(np.nextafter(log_discount,np.inf))
  assert loss>cfg['log_discount_knots'][-1][0];assert log_discount>=cfg['log_discount_knots'][-1][1];cfg['log_discount_knots'].append([loss,log_discount]);cfg['low_end_constraints'].append({'id':id,'offering':q['offering'],'type':kind,'amount_usd':price,'treatment':'Fit to approximate450center' if kind=='approximate_center' else 'Use300as ceiling-active endpoint, consistentwithnear300guidance; not a claimedexacttransactionprice orverifiedcostfloor.'})
 cfg['qualification']='Provisionalmonetarylayer. Original5knots andregionalanchors unchanged;2Northeastexpertjudgments extend curve. Otherregions inheritsharedrelativecurve asanassumption. Full domain interpolation isnotindependentmarketvalidation. No regularbatchdiscount orfees added.'
 cfg['source_hashes']={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in [P/'consistent-price-config-v1.json',P/'consistent_price_layer.py',P/'consistent_price_v2.py',P/'low-end-checks-v1.json',P/'refine_low_end_v2.py',ROOT/'model-config-v28.json']}
 out=P/'consistent-price-config-v2.json';assert not out.exists(),'Preserve existing version';out.write_text(json.dumps(cfg,indent=2)+'\n');m=Model();prev=Previous();offers=[list(o) for o in itertools.product(m.domain['provenances'],m.domain['shades'],m.domain['vintage_years'],m.domain['tare_lb'])];grid=[];adj=refs=unchanged=0
 for o in offers:
  current=m.price(o);oldp=prev.price(o);v=current['price_usd'];assert math.isfinite(v) and v>0
  if current['attribute_loss']<=cfg['prior_supported_loss']+1e-9:assert abs(v-oldp['price_usd'])<1e-8;unchanged+=1
  z,s,a,t=o;neighbors=[]
  if a>20:neighbors.append([z,s,a-5,t])
  if t>110:neighbors.append([z,s,a,t-5])
  j=m.domain['shades'].index(s)
  if j<4:neighbors.append([z,m.domain['shades'][j+1],a,t])
  for n in neighbors:assert m.price(n)['price_usd']>=v-1e-8;adj+=1
  for ref in [[z,'pale/straw',20,110],[z,'amber',35,120],['northwest','brown',40,130]]:assert abs(m.translate_from_reference(o,ref)-v)<1e-8;refs+=1
  grid.append({'offering':o,'previous_price_usd':oldp['price_usd'],'price_usd':v,'change_usd':v-oldp['price_usd'],**{k:current[k] for k in ['attribute_loss','log_discount','anchor_price','anchor_status','extrapolating_attribute_curve','calibration_status','regional_low_end_transfer_assumed']}})
 constraints=[{'id':c['id'],'offering':c['offering'],'type':c['type'],'target':c['amount_usd'],'price_usd':m.price(c['offering'])['price_usd']} for c in cfg['low_end_constraints']];assert abs(constraints[0]['price_usd']-450)<1e-8;assert constraints[1]['price_usd']<=300
 anchors=[]
 for z,a in cfg['regional_anchors'].items():
  v=m.price([z,'pale/straw',20,110])['price_usd'];assert v==a['price'];anchors.append({'region':z,'price':v,'status':a['status']})
 checks=json.loads((P/'consistent-price-validation-v1.json').read_text())['fit_observations'];preserved=[]
 for q in checks:
  v=m.price(q['offering'])['price_usd'];assert abs(v-q['canonical_price'])<1e-8;preserved.append({'id':q['id'],'accepted_price':q['accepted_price'],'prior_model_price':q['canonical_price'],'new_model_price':v})
 result={'scope':'Calibration to two new expertjudgments, notfreshvalidation. Upperbound used asceiling-activeendpoint,notcostdata.','constraints':constraints,'prior_accepted_checks':preserved,'anchors':anchors,'checks':{'finite_positive_prices':len(grid),'adjacent_monotonic_checks':adj,'reference_independence_checks':refs,'prior_in_span_prices_unchanged':unchanged,'accepted_model_prices_preserved':len(preserved),'current_grid_extrapolations':sum(x['extrapolating_attribute_curve'] for x in grid),'non_NE_low_end_transfer_profiles':sum(x['regional_low_end_transfer_assumed'] for x in grid)},'grid':grid,'source_config_sha256':hashlib.sha256(out.read_bytes()).hexdigest()};(P/'consistent-price-validation-v2.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'constraints':constraints,'checks':result['checks']},indent=2))
if __name__=='__main__':main()
