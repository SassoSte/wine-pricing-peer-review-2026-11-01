"""Freeze20 fresh varied tare-compensation versus v26 comparisons in batches of5."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
from predictor_v27 import Model as Candidate
from predictor import Model as V26
from freeze_round40 import collect,key
R=Path(__file__).resolve().parent
DESIGN=[
('five_year_heavier',['Western Europe','golden',25,130],['Western Europe','pale/straw',30,125]),
('domestic_tradeoff',['northeast','amber',30,115],['southwest','amber',25,125]),
('five_year_heavier',['West Central Asia','amber',30,120],['West Central Asia','copper',35,115]),
('shade_only',['Eastern Europe','pale/straw',25,125],['Eastern Europe','golden',25,125]),
('provenance_tare',['South/Eastern Asia','amber',25,110],['West Central Asia','amber',25,120]),
('five_year_heavier',['central','golden',25,125],['central','pale/straw',30,120]),
('brown_tradeoff',['Western Europe','brown',40,115],['northwest','amber',35,120]),
('pure_five_lb',['southwest','copper',30,120],['southwest','copper',30,125]),
('zero_shade',['West Asia / Middle East','golden',30,130],['West Asia / Middle East','pale/straw',30,130]),
('five_year_heavier',['Eastern Europe','amber',25,125],['Eastern Europe','amber',30,120]),
('domestic_tradeoff',['northwest','golden',25,120],['central','golden',20,125]),
('foreign_tradeoff',['Western Europe','copper',35,125],['South/Eastern Asia','pale/straw',30,120]),
('fifteen_lb_tradeoff',['West Central Asia','pale/straw',30,115],['West Central Asia','golden',25,130]),
('microshade',['southeast','amber',35,120],['southeast','copper',35,120]),
('foreign_tradeoff',['Eastern Europe','golden',20,125],['Western Europe','golden',25,120]),
('pure_fifteen_lb',['central','brown',35,110],['central','brown',35,125]),
('older_excluded',['Western Europe','golden',40,125],['Western Europe','golden',35,130]),
('dark_foreign',['West Asia / Middle East','brown',30,120],['South/Eastern Asia','copper',35,115]),
('zero_shade',['northeast','golden',20,130],['northeast','pale/straw',20,130]),
('ten_year_tradeoff',['West Central Asia','golden',30,115],['West Central Asia','golden',20,125]),
]
def main():
 out=R/'round51-fixed.json'
 if out.exists():raise FileExistsError(out)
 histories=sorted(set(R.glob('round*-fixed.json'))|set(R.glob('evidence*.json'))|{R/'comparisons.json',R/'round50-isolation.json'});seen=set()
 for p in histories:collect(json.loads(p.read_text()),seen)
 qs=[]
 for i,(category,aa,bb) in enumerate(DESIGN,1):
  for shift in (0,5,-5,10,-10,15,-15,20,-20):
   a=aa.copy();b=bb.copy();a[2]+=shift;b[2]+=shift
   if category=='five_year_heavier' and min(a[2],b[2])>30:continue
   if category=='older_excluded' and {a[2],b[2]}!={35,40}:continue
   if a[2] in (20,25,30,35,40) and b[2] in (20,25,30,35,40) and key(a,b) not in seen:break
  else:raise ValueError(('No fresh pair',i))
  seen.add(key(a,b));qs.append({'id':f'round51-{i}','number':i,'category':category,'a':a,'b':b,'status':'pending','direction':None,'meaningfulness':None,'raw_answer':None,'exact_price_instruction':False})
 models={'tare_compensation':Candidate(),'v26':V26()}
 for q in qs:q['predictions']={n:m.compare(q['a'],q['b']) for n,m in models.items()}
 sources=['model-config-v27.json','predictor_v27.py','model-config.json','predictor.py','evidence-v27.json','benchmark-targets-v27.json','freeze_round51.py','freeze_round40.py'];fields=['id','number','category','a','b','predictions']
 d={'round':51,'created_at':datetime.now(timezone.utc).isoformat(),'status':'in_progress','protocol':'20 fresh unordered pairs, reverse duplicates excluded from saved rounds/evidence/isolation. Broad stratification across all10 provenances,shade/vintage/tare and mixed trades;4 eligible younger5lb-heavier cases plus out-of-scope controls. Attribute design and freshness substitutions before predictions; no selection by model agreement. Four batches of5; predictions fixed before answers. Direction/meaningfulness separate; unresolved available. No prior answers/interim scores exposed. Selected familiar families, not random population accuracy.','models':{'tare_compensation':json.loads((R/'model-config-v27.json').read_text()),'v26':json.loads((R/'model-config.json').read_text())},'file_sha256':{f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in sources},'freshness_history_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in histories},'freeze_fields':fields,'questions_and_predictions_sha256':hashlib.sha256(json.dumps([{k:q[k] for k in fields} for q in qs],sort_keys=True).encode()).hexdigest(),'questions':qs,'rule_statements':[],'scores':None}
 out.write_text(json.dumps(d,indent=2)+'\n');saved=json.loads(out.read_text());assert hashlib.sha256(json.dumps([{k:q[k] for k in fields} for q in saved['questions']],sort_keys=True).encode()).hexdigest()==d['questions_and_predictions_sha256']
 for q in saved['questions']:
  for n,m in models.items():assert m.compare(q['a'],q['b'])==q['predictions'][n]
 for f,h in d['file_sha256'].items():assert hashlib.sha256((R/f).read_bytes()).hexdigest()==h,f
 p=R/'pricing-reset-progress.json';s=json.loads(p.read_text());s.update(status='Round51 frozen tare-compensation/v26; awaiting answers1-5',active_round=out.name,next_question=1,answered_questions=0,batch_size=5,current_batch=[1,2,3,4,5],note='20 fresh varied pairs and40 predictions frozen before answers. Five at a time; separate direction/meaningfulness; unresolved allowed. No adaptive substitution or refit.');p.write_text(json.dumps(s,indent=2)+'\n')
 block='## Active Round51 — tare-compensation model versusv26\n\n20 fresh varied pairs across all10 provenances; includes4 active compensation-context\ncomparisons and older/zero-shade/pure-tare/out-of-scope controls. Reverse duplicates\nchecked against saved rounds/evidence/isolation. Attribute selection precedes predictions.\nAll40 predictions and model/config hashes frozen in round51-fixed.json. Present5 at\na time; hide predictions/interim scores; separate axes, unresolved available. Awaiting\nbatch Q1-5. No mathematical changes during this round.\n\n'
 for name in ('README.md','HANDOFF.md'):
  p=R/name;first,rest=p.read_text().split('\n',1);p.write_text(first+'\n\n'+block+rest.lstrip('\n'))
 print(json.dumps({'frozen_pairs':20,'prediction_rechecks':40,'history_files':len(histories)}))
 for q in qs[:5]:print(json.dumps({k:q[k] for k in ('number','a','b')}))
if __name__=='__main__':main()
