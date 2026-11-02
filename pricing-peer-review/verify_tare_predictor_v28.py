"""Full-domain parity with saved tare-compensation candidate; no fitting."""
from pathlib import Path
from itertools import product
import json,hashlib,time
import numpy as np
from predictor_v28 import Model
import tare_compensation_v27 as legacy
R=Path(__file__).resolve().parent

def main():
 started=time.monotonic();m=Model();cfg=json.loads((R/'tare-refit-candidate-v28.json').read_text())['model'];weights=np.array(cfg['coefficients']);hashes={f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in ('predictor_v28.py','predictor_v27.py','model-config-v28.json','tare-refit-candidate-v28.json','verify_tare_predictor_v28.py')};sources=m.config['source_hashes']
 for f,h in sources.items():assert hashlib.sha256((R/f).read_bytes()).hexdigest()==h,f
 seen=set()
 def collect(v):
  if isinstance(v,dict):
   a,b=v.get('a'),v.get('b')
   if isinstance(a,list) and isinstance(b,list) and len(a)==len(b)==4 and all(isinstance(x,(str,int,float)) for x in a+b):seen.add((tuple(a),tuple(b)))
   for x in v.values():collect(x)
  elif isinstance(v,list):
   for x in v:collect(x)
 for path in [*R.glob('round*-fixed.json'),R/'round50-isolation.json',R/'round52-clarifications.json',R/'round53-isolation.json',R/'round54-unresolved-isolation.json',R/'evidence-v28.json',R/'comparisons.json']:collect(json.loads(path.read_text()))
 for a,b in sorted(seen):
  p=m.compare(list(a),list(b));p.pop('model');assert p==legacy.predict(list(a),list(b),cfg)
 d=m.domain;options=[list(x) for x in product(d['provenances'],d['shades'],d['vintage_years'],d['tare_lb'])];total=0
 for i,a in enumerate(options):
  current=np.array([m._pair(a,b) for b in options]);old=legacy.design([{'a':a,'b':b} for b in options]);assert np.array_equal(current,old);assert np.array_equal(current@m.weights,old@weights);total+=len(options)
  if (i+1)%250==0:print(f'Verified {total:,} ordered pairs',flush=True)
 rng=np.random.default_rng(2701)
 for _ in range(2000):
  a=options[int(rng.integers(len(options)))];b=options[int(rng.integers(len(options)))];p=m.compare(a,b);p.pop('model');assert p==legacy.predict(a,b,cfg)
 for f,h in {**sources,**hashes}.items():assert hashlib.sha256((R/f).read_bytes()).hexdigest()==h,f
 receipt={'model':'v28_tare_compensation','historical_unique_pairs_exact_scalar':len(seen),'random_pairs_exact_scalar':2000,'supported_offerings':len(options),'ordered_pairs_checked':total,'feature_mismatches':0,'numeric_score_mismatches':0,'decision_rules_identical':True,'classification_mismatches':0,'source_hashes':sources,'runtime_hashes':hashes,'math_changed':False,'output_metadata_change':'New model identifier only; all prediction fields match.','elapsed_seconds':time.monotonic()-started}
 (R/'tare-predictor-equivalence-v28.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({k:v for k,v in receipt.items() if 'hash' not in k},indent=2))
if __name__=='__main__':main()
