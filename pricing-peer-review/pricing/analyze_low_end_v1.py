"""Compare low-end extrapolation assumptions without changing calibrated pricing."""
from pathlib import Path
import json,math,itertools,hashlib
from consistent_price_layer import Model
P=Path(__file__).resolve().parent
ALPHAS={'current_exponential':0.,'slower_tail':1.,'slowest_tested_tail':2.}
def main():
 m=Model();cfg=m.config;knots=cfg['log_discount_knots'];(x0,y0),(cut,level)=knots[-2:];slope=(level-y0)/(cut-x0)
 def value(o,alpha):
  p=m.price(o);t=max(0.,p['attribute_loss']-cut)
  if t==0:return p['price_usd']
  factor=math.exp(-slope*t) if alpha==0 else (1+alpha*slope*t)**(-1/alpha)
  return p['anchor_price']*math.exp(-level)*factor
 offers=[list(x) for x in itertools.product(m.domain['provenances'],m.domain['shades'],m.domain['vintage_years'],m.domain['tare_lb'])];rows=[]
 for o in offers:
  prices={name:value(o,a) for name,a in ALPHAS.items()};loss=m.price(o)['attribute_loss'];rows.append({'offering':o,'loss':loss,'extrapolated':loss>cut+1e-9,'prices':prices,'scenario_spread_usd':max(prices.values())-min(prices.values()),'anchor_status':m.anchors[o[0]]['status']})
 by={tuple(x['offering']):x for x in rows};checks=0
 for o in offers:
  z,s,a,t=o;neighbors=[]
  if a>20:neighbors.append([z,s,a-5,t])
  if t>110:neighbors.append([z,s,a,t-5])
  j=m.domain['shades'].index(s)
  if j<4:neighbors.append([z,m.domain['shades'][j+1],a,t])
  for name,alpha in ALPHAS.items():
   v=by[tuple(o)]['prices'][name];assert math.isfinite(v) and v>0
   for n in neighbors:assert by[tuple(n)]['prices'][name]>=v-1e-8;checks+=1
   if by[tuple(o)]['loss']<=cut+1e-9:assert abs(v-m.price(o)['price_usd'])<1e-8
 samples=[]
 for profile in [('pale/straw',30,120),('copper',35,125),('brown',40,130)]:
  for z in ['northeast','northwest']:samples.append(by[(z,*profile)])
 region=[]
 for z in m.domain['provenances']:
  rr=[x for x in rows if x['offering'][0]==z];region.append({'region':z,'tail_count':sum(x['extrapolated'] for x in rr),'bounds':{name:{'min':min(x['prices'][name] for x in rr),'max':max(x['prices'][name] for x in rr)} for name in ALPHAS}})
 out={'scope':'Sensitivity analysis only; no tail chosen or pricingconfigchanged. All three match existingcalibration andboundarylog-slope, positiveandmonotone. Scenario spread isnotconfidence ormarketprice range.','boundary_loss':cut,'boundary_log_discount':level,'boundary_price_fraction':math.exp(-level),'boundary_log_slope':slope,'formula':'For t=max(0,loss-cut), P=P_boundary*exp(-s*t) whenalpha0; else P=P_boundary*(1+alpha*s*t)^(-1/alpha). Beforeboundary alluseunchangedcalibratedcurve.','scenario_alpha':ALPHAS,'reasoning':'These curves haveequalvalue andfirstderivative atboundary and preserveallanchors/acceptedfit, yetdiffer greatly awayfromsupport. Currentdata cannotidentify tailcurvature. No positiveeconomicfloor imposed; allapproachzero asymptotically.','checks':{'positive_prices_per_scenario':1250,'all_adjacent_monotonic_checks':checks,'in_span_prices_unchanged_per_scenario':sum(not x['extrapolated'] for x in rows),'out_of_span_profiles':sum(x['extrapolated'] for x in rows)},'representative_profiles':samples,'region_bounds':region,'grid':rows,'decision':'Consolidate canonicalpriceengine andevidence/provenance/status schema. Keep low-endtail explicitlyprovisional; do not selectoraverage tails withoutlow-endpriceevidence. A lower-bracket pricedoffering and ideallyone mid-bracket point are needed toseparate level,curvature andfloor assumptions.','source_hashes':{f:hashlib.sha256((P/f).read_bytes()).hexdigest() for f in ['consistent-price-config-v1.json','consistent_price_layer.py','analyze_low_end_v1.py']}}
 (P/'low-end-curve-analysis-v1.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'boundary':cut,'slope':slope,'checks':out['checks'],'samples':samples},indent=2))
if __name__=='__main__':main()
