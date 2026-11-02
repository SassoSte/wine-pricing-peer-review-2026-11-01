"""Predeclared no/25%/50% attenuation of vintage and tare contributions for brown aged35+ only."""
from pathlib import Path
import json,hashlib,itertools
import numpy as np
import global_positive_v33 as base
import brown_attenuation_v34 as brown
from evaluate_voice_v32 import metrics,family
R=Path(__file__).resolve().parent
ARMS={'unchanged_structure':0.,'brown25':.25,'brown50':.5}
def module(rho):
 brown.RHO=rho
 return brown if rho else base
def main():
 rows=json.loads((R/'benchmark-targets-v34.json').read_text())['rows'];by={q['id']:q for q in rows};ix={q['id']:i for i,q in enumerate(rows)};prior=json.loads((R/'positive-validation-v33.json').read_text());runs={name:[] for name in ARMS};audits=[]
 for seed in (11,29,47,71,103):
  gaps={name:np.zeros(len(rows)) for name in ARMS};seen=set()
  for f in [f for f in prior['fold_audits'] if f['seed']==seed]:
   families={family(by[id]) for id in f['validation_ids']};test=[q for q in rows if family(q) in families];train=[q for q in rows if family(q) not in families];assert not seen.intersection(q['id'] for q in test);seen.update(q['id'] for q in test);te=[ix[q['id']] for q in test]
   for name,rho in ARMS.items():
    m=module(rho);cfg=m.select(train,seed*100+f['fold'],True);gaps[name][te]=m.design(test)@cfg['coefficients'];audits.append({'arm':name,'seed':seed,'fold':f['fold'],'training_ids':[q['id'] for q in train],'validation_ids':[q['id'] for q in test],'fit':cfg})
  assert len(seen)==len(rows)
  for name,g in gaps.items():runs[name].append({'seed':seed,'margins':g.tolist(),'metrics':metrics(rows,g)})
  print(seed,{name:runs[name][-1]['metrics'] for name in ARMS},flush=True)
 full={};checks=0
 for name,rho in ARMS.items():
  m=module(rho);cfg=m.select(rows,34001,True);full[name]={'fit':cfg,'metrics':metrics(rows,m.design(rows)@cfg['coefficients'])}
  for fit in [cfg]+[f['fit'] for f in audits if f['arm']==name]:
   w=np.array(fit['coefficients'])
   for z,s,a,t in itertools.product(base.D['provenances'],base.D['shades'],base.D['vintage_years'],base.D['tare_lb']):
    val=m.features([z,s,a,t])@w
    if a>20:assert m.features([z,s,a-5,t])@w>=val-1e-6
    if t>110:assert m.features([z,s,a,t-5])@w>=val-1e-6
    j=base.D['shades'].index(s)
    if j<4:assert m.features([z,base.D['shades'][j+1],a,t])@w>=val-1e-6
    if s=='pale/straw' and t==130:assert abs(val-m.features([z,'golden',a,t])@w)<1e-7
    checks+=1
 out={'protocol':'v34 deduplicated voice judgment. Compare same positive-guarded hard-equality21coefficient architecture with no attenuation versus predeclared25% and50% vintage/tare contribution reduction for brown age35+. No region or pair lookup. Refitweights train-only with ridge chosen insideeach outerfold. Samefamily grouping retains older tie and newequal-tare clarification together whenheldout. Contextual maximumshade range remains belowprovenance. Threefixedarms exploratory, not nestedselection ofattenuation. Premiumhead not changed.','runs':runs,'fold_audits':audits,'full_models':full,'profile_checks':checks,'source_hashes':{f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in ['evidence-v34.json','benchmark-targets-v34.json','global_positive_v33.py','brown_attenuation_v34.py','evaluate_brown_v34.py']}}
 (R/'brown-validation-v34.json').write_text(json.dumps(out,indent=2)+'\n');print('FULL', {name:v['metrics'] for name,v in full.items()},flush=True)
if __name__=='__main__':main()
