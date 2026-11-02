"""Freeze20 fresh broader pairs for consolidatedv26 versusv25, five at a time."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
from predictor import Model as V26
from pricing_v25 import Model as V25
from freeze_round40 import collect,key
R=Path(__file__).resolve().parent
DESIGN=[
('domestic_tradeoff',['central','amber',25,120],['northeast','amber',30,115]),
('foreign_shade_tradeoff',['Western Europe','copper',25,120],['South/Eastern Asia','pale/straw',20,125]),
('older_vintage',['West Central Asia','golden',35,115],['West Central Asia','pale/straw',40,120]),
('microshade',['southwest','amber',20,125],['southwest','copper',20,125]),
('large_tare',['Eastern Europe','brown',30,110],['Eastern Europe','brown',30,130]),
('provenance_tare',['northwest','golden',25,115],['Western Europe','golden',25,120]),
('foreign_tradeoff',['West Asia / Middle East','amber',35,125],['South/Eastern Asia','amber',30,115]),
('zero_shade',['central','golden',35,130],['central','pale/straw',35,130]),
('brown_tradeoff',['northeast','brown',25,115],['southeast','amber',30,120]),
('five_year_ten_lb',['Eastern Europe','golden',25,125],['Eastern Europe','pale/straw',30,115]),
('pure_five_lb',['Western Europe','pale/straw',35,120],['Western Europe','pale/straw',35,125]),
('ten_year_fifteen_lb',['southwest','golden',20,130],['central','golden',30,115]),
('foreign_tradeoff',['West Central Asia','copper',30,120],['Eastern Europe','amber',25,125]),
('reinforcing',['northwest','golden',30,110],['northwest','golden',35,125]),
('microshade',['South/Eastern Asia','amber',25,120],['South/Eastern Asia','copper',25,120]),
('brown_cross_provenance',['Western Europe','brown',35,115],['northwest','amber',40,120]),
('domestic_vintage',['central','golden',20,125],['central','pale/straw',25,120]),
('provenance_only',['northeast','copper',35,120],['southwest','copper',35,120]),
('foreign_tradeoff',['West Asia / Middle East','pale/straw',30,125],['West Central Asia','golden',25,120]),
('vintage_only',['Eastern Europe','golden',40,125],['Eastern Europe','golden',30,125]),
]
def main():
 out=R/'round49-fixed.json'
 if out.exists():raise FileExistsError(out)
 histories=sorted(set(R.glob('round*-fixed.json'))|set(R.glob('evidence*.json'))|{R/'comparisons.json'});seen=set()
 for p in histories:collect(json.loads(p.read_text()),seen)
 qs=[]
 for i,(category,aa,bb) in enumerate(DESIGN,1):
  for shift in (0,5,-5,10,-10,15,-15,20,-20):
   a=aa.copy();b=bb.copy();a[2]+=shift;b[2]+=shift
   if category=='domestic_vintage' and min(a[2],b[2])!=20:continue
   if a[2] in (20,25,30,35,40) and b[2] in (20,25,30,35,40) and key(a,b) not in seen:break
  else:raise ValueError(('No fresh pair',i))
  seen.add(key(a,b));qs.append({'id':f'round49-{i}','number':i,'category':category,'a':a,'b':b,'status':'pending','direction':None,'meaningfulness':None,'raw_answer':None,'exact_price_instruction':False})
 models={'v26':V26(),'v25':V25()}
 for q in qs:q['predictions']={n:m.compare(q['a'],q['b']) for n,m in models.items()}
 sources=['model-config.json','predictor.py','older-dark-scoped-delivery-v25.json','evidence-v26.json','benchmark-targets-v26.json','pricing_v25.py','older_dark_scoped_v25.py','five_year_premium_v23.py','joint_weight_refit_v22.py','joint_objective_v22.py','residual_fixes_v22.py','shade_vintage_shared_v21.py','contextual_shade_v20.py','contextual_fixes_v19.py','contextual_meaningfulness.py','domestic_shade_model.py','compare_models.py','freeze_round49.py','freeze_round40.py'];fields=['id','number','category','a','b','predictions']
 d={'round':49,'created_at':datetime.now(timezone.utc).isoformat(),'status':'in_progress','protocol':'20 fresh unordered pairs, reversed duplicates excluded from all saved rounds/evidence. Broader attribute-stratified domestic/foreign/mixed-provenance,shade/vintage/tare and controls across all10 provenances. Design and freshness choices precede prediction calls; not selected by prediction agreement. Four batches of5, no adaptive substitutions. Frozen consolidatedv26 versusv25; hide predictions and interim scoring. Direction/meaningfulness separate, unresolved allowed. Tie/practical/unresolved not conflated; no inferred missing sizes. Small selected sample, not random population accuracy.','models':{'v26':json.loads((R/'model-config.json').read_text()),'v25':json.loads((R/'older-dark-scoped-delivery-v25.json').read_text())},'file_sha256':{f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in sources},'freshness_history_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in histories},'freeze_fields':fields,'questions_and_predictions_sha256':hashlib.sha256(json.dumps([{k:q[k] for k in fields} for q in qs],sort_keys=True).encode()).hexdigest(),'questions':qs,'rule_statements':[],'scores':None}
 out.write_text(json.dumps(d,indent=2)+'\n');saved=json.loads(out.read_text());assert hashlib.sha256(json.dumps([{k:q[k] for k in fields} for q in saved['questions']],sort_keys=True).encode()).hexdigest()==d['questions_and_predictions_sha256']
 for q in saved['questions']:
  for n,m in models.items():assert m.compare(q['a'],q['b'])==q['predictions'][n]
 for f,h in d['file_sha256'].items():assert hashlib.sha256((R/f).read_bytes()).hexdigest()==h
 p=R/'pricing-reset-progress.json';s=json.loads(p.read_text());s.update(status='Round49 frozen consolidatedv26/v25; awaiting answers1-5',active_round=out.name,next_question=1,answered_questions=0,batch_size=5,current_batch=[1,2,3,4,5],note='20 fresh broader pairs and40 predictions frozen before answers. Five at a time; separate direction/meaningfulness; unresolved available. No adaptive selection/refit.');p.write_text(json.dumps(s,indent=2)+'\n')
 block='## Active Round49 — consolidatedv26 versusv25\n\n20 fresh unordered comparisons, reverse duplicates checked against all saved rounds/\nevidence. Broader variety across all10 provenances,shade/vintage/tare and mixed\ntradeoffs/controls. Design precedes model calls. All40 predictions and source hashes\nfrozen in round49-fixed.json. Present5 at a time; hide predictions/interim scores,\nseparate direction/meaningfulness, unresolved allowed. Awaiting batch Q1-5.\n\n'
 for name in ('README.md','HANDOFF.md'):
  p=R/name;first,rest=p.read_text().split('\n',1);p.write_text(first+'\n\n'+block+rest.lstrip('\n'))
 print(json.dumps({'frozen':20,'prediction_rechecks':40,'history_files':len(histories)}))
 for q in qs[:5]:print(json.dumps({k:q[k] for k in ('number','a','b')}))
if __name__=='__main__':main()
