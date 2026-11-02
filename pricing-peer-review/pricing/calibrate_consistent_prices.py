"""Calibrate a monotone price curve without changing V28."""
from pathlib import Path
import json,math,hashlib,itertools,sys
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent))
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from consistent_price_layer import attribute_loss,curve_value,Model
from predictor_v28 import Model as V28
ROOT=Path(__file__).resolve().parent.parent;P=ROOT/'pricing'
def fit_knots(observations):
 groups={}
 for o in observations:groups.setdefault(tuple(o['offering'][1:]),[]).append(o)
 values=sorted((v[0]['loss'],float(np.mean([math.log(o['anchor_price']/o['accepted_price']) for o in v]))) for v in groups.values())
 blocks=[]
 for x,y in values:
  blocks.append({'x':[x],'y':max(0.,y),'n':1})
  while len(blocks)>=2 and blocks[-2]['y']>blocks[-1]['y']:
   b=blocks.pop();a=blocks.pop();n=a['n']+b['n'];blocks.append({'x':a['x']+b['x'],'y':(a['y']*a['n']+b['y']*b['n'])/n,'n':n})
 knots=[[0.,0.]]
 for b in blocks:
  for x in b['x']:knots.append([x,b['y']])
 return knots

def main():
 base=json.loads((ROOT/'model-config-v28.json').read_text());domain=base['domain'];w=base['coefficients'];source=json.loads((P/'anchors-v1.json').read_text());known={q['provenance']:q for q in source['anchors'] if q.get('regional_seat_batch') is True};gridold=json.loads((P/'all-region-price-grid-v1.json').read_text());anchors={q['region']:{'price':q['reference_price_linear'],'status':q['anchor_status']} for q in gridold['regions']};obs=[]
 first=json.loads((P/'valuation-checks-v1.json').read_text())['checks'];second=json.loads((P/'independent-checks-v2.json').read_text())['checks']
 for q in first:obs.append({'id':q['id'],'offering':q['offering'],'accepted_price':q['proposed_price'],'source':'valuation-checks-v1.json','status':'post-disclosure expert plausibility'})
 for q in second:
  assert q.get('post_disclosure_feedback');obs.append({'id':q['id'],'offering':q['offering'],'accepted_price':round(q['frozen_estimate']),'source':'independent-checks-v2.json','status':'post-disclosure expert plausibility','initial_expert_estimate':q.get('expert_estimate'),'initial_expert_range':q.get('expert_range')})
 for o in obs:o['anchor_price']=known[o['offering'][0]]['price'];o['loss']=attribute_loss(o['offering'],domain,w)
 assert len(obs)==10 and len({tuple(o['offering'][1:]) for o in obs})==4
 knots=fit_knots(obs);groups={}
 for o in obs:groups.setdefault(tuple(o['offering'][1:]),[]).append(o)
 gx=np.array([v[0]['loss'] for v in groups.values()]);gy=np.array([np.mean([math.log(o['anchor_price']/o['accepted_price']) for o in v]) for v in groups.values()]);slope=float(gx@gy/(gx@gx))
 cfg={'model_id':'consistent-price-layer-v1','status':'experimental_calibrated_to_plausibility_not_market_data','domain':domain,'base_coefficients':w,'regional_anchors':anchors,'calibration_offerings':[o['offering'] for o in obs],'log_discount_knots':knots,'price_basis':'Wholefilledcask; seat/reference-status assumed comparable; samevolume,mint,initialrelease/distributorterms; fees/taxes/deliveryexcluded. Regularbatchdiscount notapplied.','source_hashes':{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in ['model-config-v28.json','pricing/all-region-price-grid-v1.json','pricing/anchors-v1.json','pricing/valuation-checks-v1.json','pricing/independent-checks-v2.json','pricing/consistent-price-protocol-v1.json','pricing/consistent_price_layer.py','pricing/calibrate_consistent_prices.py']}}
 (P/'consistent-price-config-v1.json').write_text(json.dumps(cfg,indent=2)+'\n');model=Model();fit=[]
 for o in obs:
  v=model.price(o['offering'])['price_usd'];fit.append({**o,'canonical_price':v,'residual':v-o['accepted_price'],'single_slope_price':o['anchor_price']*math.exp(-slope*o['loss'])})
 loo=[]
 for profile in groups:
  tr=[o for o in obs if tuple(o['offering'][1:])!=profile];test=groups[profile];kk=fit_knots(tr)
  for o in test:
   estimate=o['anchor_price']*math.exp(-curve_value(o['loss'],kk));loo.append({'id':o['id'],'heldout_profile':profile,'estimate':estimate,'accepted_price':o['accepted_price'],'error':estimate-o['accepted_price'],'extrapolation':o['loss']>kk[-1][0]})
 alloffers=[list(v) for v in itertools.product(domain['provenances'],domain['shades'],domain['vintage_years'],domain['tare_lb'])];prices={tuple(o):model.price(o) for o in alloffers};monotone=0;reference_checks=0;max_reference_diff=0.;anchors_checked=[]
 for z,q in known.items():
  v=model.price([z,'pale/straw',20,110])['price_usd'];assert abs(v-q['price'])<1e-8;anchors_checked.append(z)
 for o in alloffers:
  v=prices[tuple(o)]['price_usd'];assert math.isfinite(v) and v>0;z,s,a,t=o;neighbors=[]
  if a>20:neighbors.append([z,s,a-5,t])
  if t>110:neighbors.append([z,s,a,t-5])
  j=domain['shades'].index(s)
  if j<4:neighbors.append([z,domain['shades'][j+1],a,t])
  for n in neighbors:assert prices[tuple(n)]['price_usd']>=v-1e-8;monotone+=1
  for ref in [[z,'pale/straw',20,110],[z,'pale/straw',25,110],['northwest','golden',30,125]]:
   diff=abs(model.translate_from_reference(o,ref)-v);assert diff<1e-8;max_reference_diff=max(max_reference_diff,diff);reference_checks+=1
 grid=[{'offering':o,**prices[tuple(o)]} for o in alloffers]
 comparisons=[]
 for z in domain['provenances']:
  a=[z,'golden',25,115];b=[z,'pale/straw',25,110];c=[z,'pale/straw',20,110];assert abs(model.compare(a,b)['difference']+model.compare(b,c)['difference']-model.compare(a,c)['difference'])<1e-8
  comparisons.append({'region':z,'direct':model.price(a)['price_usd'],'via_intermediate':model.translate_from_reference(a,b)})
 region_summary=[{'region':z,'anchor_status':anchors[z]['status'],'minimum':min(v['price_usd'] for o,v in prices.items() if o[0]==z),'maximum':max(v['price_usd'] for o,v in prices.items() if o[0]==z)} for z in domain['provenances']]
 result={'scope':'Structuralconsistency fix andcalibration,not freshpricevalidation. Acceptedtargets arepost-disclosure hypotheticalvalues; fouruniqueprofiles.','fit_observations':fit,'fit_mae':float(np.mean([abs(x['residual']) for x in fit])),'fit_max_absolute_error':max(abs(x['residual']) for x in fit),'single_slope_fit_mae':float(np.mean([abs(x['single_slope_price']-x['accepted_price']) for x in fit])),'leave_profile_out':loo,'leave_profile_out_mae':float(np.mean([abs(x['error']) for x in loo])),'checks':{'anchors_exact':len(anchors_checked),'positive_prices':len(prices),'monotonic_adjacent_checks':monotone,'reference_independence_checks':reference_checks,'maximum_reference_discrepancy':max_reference_diff,'price_difference_telescoping_checks':len(comparisons),'global_pair_ordering':'Each comparison is canonicalprice difference; transitivity follows from scalarprice construction, not claimsaboutV28pair preferences.'},'comparison_examples':comparisons,'regions':region_summary,'extrapolated_profiles':sum(x['extrapolating_attribute_curve'] for x in prices.values()),'grid':grid,'limits':['Shared responsecurve isassumed acrossregions; regionalpriceanchors notall supplied.','Piecewise curve has4supported nonzero loss locations from4distinctprofilepatterns; no independent marketfit.','Beyondlargestloss, final log-slope extrapolation keepspositivity butdoesnot establish correctlow-endprices.','Canonicalprices can disagree withV28paircontext rankings; no claims topreserve everycomparison.','Newexternal priceanchor inconsistentwithconfig requiresa newcalibrationversion, notchangingreferenceon-the-fly.']}
 (P/'consistent-price-validation-v1.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['fit_mae','fit_max_absolute_error','single_slope_fit_mae','leave_profile_out_mae','checks','extrapolated_profiles','regions']},indent=2));print('FIT',[(x['id'],round(x['canonical_price'],2),x['accepted_price']) for x in fit])
if __name__=='__main__':main()
