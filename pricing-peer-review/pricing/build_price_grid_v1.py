"""Exhaustive pricing stress grid around frozen V28; no model or anchor refit."""
from pathlib import Path
import json,math,itertools,hashlib,csv,sys
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from predictor_v28 import Model
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'pricing'
def main():
 m=Model();d=m.domain;anchors=json.loads((OUT/'anchors-v1.json').read_text());known={a['provenance']:a['price'] for a in anchors['anchors'] if a.get('regional_seat_batch') is True};ne=['northeast','pale/straw',20,110];nw=['northwest','pale/straw',20,110];gap=m.compare(ne,nw)['margin'];k=(known['northeast']-known['northwest'])/gap;kl=math.log(known['northeast']/known['northwest'])/gap
 regions=[];grid=[];rank_reversals=[];monotonicity=[];pathcases=[]
 for z in d['provenances']:
  ref=[z,'pale/straw',20,110];zscore=m.compare(ref,nw)['margin'];base=known.get(z,1000+k*zscore);logbase=known.get(z,1000*math.exp(kl*zscore));rr=[]
  intermediate=[z,'pale/straw',25,110];interprice=base+k*m.compare(intermediate,ref)['margin']
  for s,a,t in itertools.product(d['shades'],d['vintage_years'],d['tare_lb']):
   offering=[z,s,a,t];score=m.compare(offering,ref)['margin'];linear=base+k*score;log=logbase*math.exp(kl*score);via=interprice+k*m.compare(offering,intermediate)['margin'];path=via-linear
   flags=[]
   if linear<=0:flags.append('invalid_nonpositive_linear')
   divergence=abs(linear-log)/max(abs(linear),abs(log),1e-12)
   if divergence>.25:flags.append('mapping_divergence_over25pct')
   if z not in known:flags.append('unanchored_region')
   if abs(path)>1:flags.append('anchor_path_difference_over1usd')
   record={'region':z,'anchor_status':'user_established' if z in known else 'model_inferred','shade':s,'vintage_years':a,'tare_lb':t,'reference_linear':base,'reference_log':logbase,'delta_score':score,'linear_usd':linear,'log_usd':log,'scenario_low_usd':min(linear,log),'scenario_high_usd':max(linear,log),'relative_mapping_divergence':divergence,'via_25year_intermediate_usd':via,'path_difference_usd':path,'flags':flags};rr.append(record);grid.append(record)
   if abs(path)>1:pathcases.append({'offering':offering,'direct':linear,'via_intermediate':via,'difference':path})
  idx={(r['shade'],r['vintage_years'],r['tare_lb']):r for r in rr}
  for r in rr:
   neighbors=[]
   if r['vintage_years']>20:neighbors.append((r['shade'],r['vintage_years']-5,r['tare_lb']))
   if r['tare_lb']>110:neighbors.append((r['shade'],r['vintage_years'],r['tare_lb']-5))
   si=d['shades'].index(r['shade'])
   if si<4:neighbors.append((d['shades'][si+1],r['vintage_years'],r['tare_lb']))
   for n in neighbors:
    if idx[n]['linear_usd']<r['linear_usd']-1e-6:monotonicity.append({'worse':r,'better':idx[n]})
  for i,r in enumerate(rr):
   a=[z,r['shade'],r['vintage_years'],r['tare_lb']]
   for b_rec in rr[i+1:]:
    b=[z,b_rec['shade'],b_rec['vintage_years'],b_rec['tare_lb']];pred=m.compare(a,b)['margin'];pricegap=r['linear_usd']-b_rec['linear_usd']
    if abs(pred)>1e-7 and abs(pricegap)>1 and pred*pricegap<0:rank_reversals.append({'a':a,'b':b,'price_a':r['linear_usd'],'price_b':b_rec['linear_usd'],'pair_score':pred,'pair_implied_usd_gap':k*pred,'listed_usd_gap':pricegap})
  regions.append({'region':z,'anchor_status':'user_established' if z in known else 'model_inferred','reference_score_vs_nw':zscore,'reference_price_linear':base,'reference_price_log':logbase,'linear_min':min(r['linear_usd'] for r in rr),'linear_max':max(r['linear_usd'] for r in rr),'log_min':min(r['log_usd'] for r in rr),'log_max':max(r['log_usd'] for r in rr),'invalid_linear_count':sum(r['linear_usd']<=0 for r in rr),'mapping_divergence_count':sum(r['relative_mapping_divergence']>.25 for r in rr),'path_sensitive_count':sum(abs(r['path_difference_usd'])>1 for r in rr)})
 assert len(grid)==1250;assert all(abs(r['linear_usd']-r['log_usd'])<1e-8 for r in grid if r['anchor_status']=='user_established' and [r['shade'],r['vintage_years'],r['tare_lb']]==['pale/straw',20,110])
 result={'status':'stress_test_not_validated_price_list','formulas':{'linear':'P_r(x)=anchor_r+k*g(x,reference_r)','log':'P_r(x)=anchor_r*exp(k_log*g(x,reference_r))','unknown_region_anchor':'Infer reference price fromNorthwest topanchor using respective mapping; provisionalonly.'},'linear_scale':k,'log_scale':kl,'known_regions':list(known),'scenario_interpretation':'MIN/MAX of two assumed mappings only; not an uncertainty/confidence interval or floor/ceiling onmarketprices. Nonpositive linearvalues remain visible and invalid, not clipped.','scope':'Wholefilledcask base initial-release price, samevolume/mint/terms and comparable reference-status assumption; fees/taxes/deliveryexcluded. Only4actualtop-profileprices supplied; otherregions lackanchors. No broad regular-batch discount extrapolation.','regions':regions,'grid':grid,'diagnostics':{'invalid_linear_count':sum(r['linear_usd']<=0 for r in grid),'unanchored_region_offerings':sum(r['anchor_status']=='model_inferred' for r in grid),'mapping_divergence_over25pct':sum(r['relative_mapping_divergence']>.25 for r in grid),'path_sensitive_count':len(pathcases),'max_path_difference':max(abs(r['difference']) for r in pathcases),'within_region_rank_reversals_over1usd':len(rank_reversals),'single_attribute_monotonicity_violations':len(monotonicity)},'monotonicity_violations':monotonicity,'path_examples':pathcases[:12],'ranking_reversals':rank_reversals,'source_hashes':{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in ['model-config-v28.json','predictor_v27.py','pricing/anchors-v1.json','pricing/build_price_grid_v1.py']}}
 (OUT/'all-region-price-grid-v1.json').write_text(json.dumps(result,indent=2)+'\n')
 with (OUT/'all-region-price-grid-v1.csv').open('w',newline='') as f:
  writer=csv.DictWriter(f,fieldnames=list(grid[0]));writer.writeheader()
  for row in grid:writer.writerow({**row,'flags':' | '.join(row['flags'])})
 print(json.dumps({'diagnostics':result['diagnostics'],'regions':regions,'ranking_examples':rank_reversals[:3]},indent=2))
if __name__=='__main__':main()
