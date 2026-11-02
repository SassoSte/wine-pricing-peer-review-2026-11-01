"""Freeze targeted v20/v19 comparisons before collecting any answers."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
from pricing_v20 import Model as V20
from pricing_v19 import Model as V19
R=Path(__file__).resolve().parent
DESIGN=[
 ('shade_only',['Eastern Europe','golden',25,130],['Eastern Europe','pale/straw',25,130]),
 ('shade_vintage',['West Central Asia','pale/straw',35,130],['West Central Asia','golden',30,130]),
 ('below_boundary',['Western Europe','golden',30,120],['Western Europe','pale/straw',35,120]),
 ('pure_five_lb',['Western Europe','pale/straw',25,130],['Western Europe','pale/straw',25,125]),
 ('shade_vintage',['Eastern Europe','golden',20,125],['Eastern Europe','pale/straw',25,125]),
 ('shade_only',['Western Europe','pale/straw',35,130],['Western Europe','golden',35,130]),
 ('unequal_tare',['West Central Asia','golden',25,120],['West Central Asia','pale/straw',30,125]),
 ('shade_only',['West Central Asia','golden',30,130],['West Central Asia','pale/straw',30,130]),
 ('below_boundary',['Eastern Europe','pale/straw',25,115],['Eastern Europe','golden',20,115]),
 ('shade_vintage',['Western Europe','pale/straw',40,125],['Western Europe','golden',35,125]),
 ('pure_five_lb',['Eastern Europe','golden',35,125],['Eastern Europe','golden',35,130]),
 ('unequal_tare',['Eastern Europe','pale/straw',30,125],['Eastern Europe','golden',25,130]),
]
def key(a,b):return frozenset((tuple(a),tuple(b)))
def collect(x,seen):
 if isinstance(x,dict):
  a,b=x.get('a'),x.get('b')
  if isinstance(a,list) and isinstance(b,list) and len(a)==len(b)==4 and all(isinstance(v,(str,int,float)) for v in a+b):seen.add(key(a,b))
  for v in x.values():collect(v,seen)
 elif isinstance(x,list):
  for v in x:collect(v,seen)
def main():
 p=R/'round40-fixed.json'
 if p.exists():raise FileExistsError(p)
 files=sorted(set(R.glob('round*-fixed.json'))|set(R.glob('evidence*.json'))|{R/'comparisons.json'});seen=set()
 for f in files:collect(json.loads(f.read_text()),seen)
 qs=[]
 # Freshness fallback changes both ages equally, retaining factor contrasts and tare strata.
 for i,(category,aa,bb) in enumerate(DESIGN,1):
  for age_shift in (0,5,-5,10,-10,15,-15,20,-20):
   a=aa.copy();b=bb.copy();a[2]+=age_shift;b[2]+=age_shift
   if a[2] in (20,25,30,35,40) and b[2] in (20,25,30,35,40) and key(a,b) not in seen:break
  else:raise ValueError(('No fresh pair for design slot',i))
  seen.add(key(a,b));qs.append({'id':f'round40-{i}','number':i,'category':category,'a':a,'b':b,'status':'pending','direction':None,'meaningfulness':None,'raw_answer':None,'exact_price_instruction':False})
 # All attribute selection complete before any prediction calls.
 models={'v20':V20(),'v19':V19()}
 for q in qs:q['predictions']={name:m.compare(q['a'],q['b']) for name,m in models.items()}
 sources=['contextual-shade-delivery-v20.json','contextual-fixes-delivery-v19.json','evidence-v20.json','benchmark-targets-v20.json','pricing_v20.py','pricing_v19.py','contextual_shade_v20.py','contextual_fixes_v19.py','contextual_meaningfulness.py','domestic_shade_model.py','compare_models.py','freeze_round40.py'];fields=['id','number','category','a','b','predictions']
 d={'round':40,'created_at':datetime.now(timezone.utc).isoformat(),'status':'in_progress','protocol':'12 fresh unordered pairs, checked including reversed orientation against saved rounds/evidence.6 targeted eligible shade-only/vintage contrasts;2 below-boundary,2 pure5lb,2 unequal-tare controls. Design and freshness substitutions precede prediction calls; no selection for agreement/disagreement. Familiar families: not independent random sample. All questions and predictions frozen before answers. No refit or interim scoring. Direction and meaningfulness separate; missing/unresolved axes excluded, practical similarity not exact equality.','models':{'v20':json.loads((R/'contextual-shade-delivery-v20.json').read_text()),'v19':json.loads((R/'contextual-fixes-delivery-v19.json').read_text())},'file_sha256':{f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in sources},'freshness_history_sha256':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'freeze_fields':fields,'questions_and_predictions_sha256':hashlib.sha256(json.dumps([{k:q[k] for k in fields} for q in qs],sort_keys=True).encode()).hexdigest(),'questions':qs,'rule_statements':[],'scores':None}
 p.write_text(json.dumps(d,indent=2)+'\n');saved=json.loads(p.read_text());assert hashlib.sha256(json.dumps([{k:q[k] for k in fields} for q in saved['questions']],sort_keys=True).encode()).hexdigest()==d['questions_and_predictions_sha256']
 for q in saved['questions']:
  for name,m in models.items():assert m.compare(q['a'],q['b'])==q['predictions'][name]
 for f,h in d['file_sha256'].items():assert hashlib.sha256((R/f).read_bytes()).hexdigest()==h
 p=R/'pricing-reset-progress.json';s=json.loads(p.read_text());s.update(status='Round40 frozen v20/v19 comparison; awaiting question1',active_round='round40-fixed.json',next_question=1,answered_questions=0,note='12 fresh exact pairs;6 shade targets+6 controls. All predictions frozen. Separate direction/meaningfulness, unresolved allowed. No model or evidence changes.');p.write_text(json.dumps(s,indent=2)+'\n')
 block='## Active Round40 — frozen v20 versus v19\n\n12 fresh unordered pairs verified against saved rounds/evidence, including reversed\norientation.6 eligible shade targets+6 below-boundary/tare controls. Attribute design\nprecedes model calls. All questions/predictions saved in round40-fixed.json, frozen\nbefore answers. Familiar families, not random population sample. Present one at a\ntime, hide predictions/interim scores, record direction and meaningfulness separately.\nUnresolved/save for later allowed on either axis. Q1 awaiting answer. No refits.\n\n'
 for name in ('README.md','HANDOFF.md'):
  p=R/name;first,rest=p.read_text().split('\n',1);p.write_text(first+'\n\n'+block+rest.lstrip('\n'))
 print(json.dumps({'frozen_pairs':12,'prediction_rechecks':24,'history_files':len(files),'first':{k:qs[0][k] for k in ('a','b')}}))
if __name__=='__main__':main()
