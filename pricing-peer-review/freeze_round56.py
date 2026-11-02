"""Freeze12 targeted WCA threshold/v28 pairs before elicitation."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
from predictor_intrinsic_threshold_v29 import Model as Candidate
from predictor_v28 import Model as Baseline
from freeze_round40 import collect,key
R=Path(__file__).resolve().parent
W='West Central Asia'
DESIGN=[
 ('wide_tare_ten_year_offset',[W,'amber',35,115],[W,'amber',25,130]),
 ('wide_tare_shade_vintage_offset',[W,'golden',30,110],[W,'pale/straw',25,125]),
 ('wide_tare_matched_control',[W,'copper',30,130],[W,'copper',30,115]),
 ('twenty_lb_ten_year_offset',[W,'pale/straw',20,130],[W,'golden',30,110]),
 ('wide_tare_shade_vintage_offset',[W,'golden',35,115],[W,'pale/straw',30,130]),
 ('wide_tare_opposed_shade_vintage',[W,'copper',30,125],[W,'amber',35,110]),
 ('twenty_lb_ten_year_offset',[W,'pale/straw',35,110],[W,'pale/straw',25,130]),
 ('twenty_lb_dark_shade_offset',[W,'amber',30,130],[W,'brown',35,110]),
 ('below_threshold_ten_lb_control',[W,'golden',25,115],[W,'pale/straw',20,125]),
 ('below_threshold_shade_control',[W,'copper',40,120],[W,'amber',40,130]),
 ('other_provenance_control',['Western Europe','amber',35,115],['Western Europe','amber',25,130]),
 ('other_provenance_control',['Eastern Europe','golden',30,110],['Eastern Europe','pale/straw',25,125]),
]
def main():
 out=R/'round56-fixed.json'
 if out.exists():raise FileExistsError(out)
 histories=sorted(set(R.glob('round*.json'))|set(R.glob('evidence*.json'))|{R/'comparisons.json',R/'benchmark-targets-v29.json'});seen=set()
 for p in histories:collect(json.loads(p.read_text()),seen)
 historical_seen=set(seen);qs=[]
 for i,(category,aa,bb) in enumerate(DESIGN,1):
  for shift in (0,5,-5,10,-10,15,-15,20,-20):
   a=aa.copy();b=bb.copy();a[2]+=shift;b[2]+=shift
   if a[2] in (20,25,30,35,40) and b[2] in (20,25,30,35,40) and key(a,b) not in seen:break
  else:raise ValueError(('No fresh pair',i))
  seen.add(key(a,b));qs.append({'id':f'round56-{i}','number':i,'category':category,'a':a,'b':b,'freshness_age_shift':shift,'status':'pending','direction':None,'meaningfulness':None,'raw_answer':None,'exact_price_instruction':False})
 models={'wca_threshold':Candidate(),'v28':Baseline()}
 for q in qs:q['predictions']={n:m.compare(q['a'],q['b']) for n,m in models.items()}
 sources=['intrinsic-threshold-config-v29.json','predictor_intrinsic_threshold_v29.py','model-config-v28.json','predictor_v28.py','predictor_v27.py','evidence-v29.json','benchmark-targets-v29.json','freeze_round56.py','freeze_round40.py'];fields=['id','number','category','a','b','freshness_age_shift','predictions']
 d={'round':56,'created_at':datetime.now(timezone.utc).isoformat(),'status':'in_progress','protocol':'12 fresh unordered pairs, reverse duplicates excluded from all saved round/evidence records and benchmark. Attribute design completed before predictions. Eight same-WCA15/20lb gap cases, including matched positive control and offsets from vintage/shade that may yield practical similarity or unresolved judgments; two WCA10lb boundary controls; two other-provenance controls. No desired answers assumed. One at a time; no interim predictions/scores disclosed. Direction,meaningfulness,exact equality and unresolved kept distinct. Fixed configurations/all24predictions before first answer. Targeted challenge set,not population accuracy; no refit until completed.','models':{'wca_threshold':json.loads((R/'intrinsic-threshold-config-v29.json').read_text()),'v28':json.loads((R/'model-config-v28.json').read_text())},'file_sha256':{f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in sources},'freshness_history_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in histories},'freeze_fields':fields,'questions_and_predictions_sha256':hashlib.sha256(json.dumps([{k:q[k] for k in fields} for q in qs],sort_keys=True).encode()).hexdigest(),'questions':qs,'rule_statements':[],'scores':None}
 out.write_text(json.dumps(d,indent=2)+'\n');saved=json.loads(out.read_text());assert hashlib.sha256(json.dumps([{k:q[k] for k in fields} for q in saved['questions']],sort_keys=True).encode()).hexdigest()==d['questions_and_predictions_sha256']
 assert len({key(q['a'],q['b']) for q in qs})==12
 for q in saved['questions']:
  assert key(q['a'],q['b']) not in historical_seen
  for n,m in models.items():assert m.compare(q['a'],q['b'])==q['predictions'][n]
 for f,h in d['file_sha256'].items():assert hashlib.sha256((R/f).read_bytes()).hexdigest()==h
 p=R/'pricing-reset-progress.json';s=json.loads(p.read_text());s.update(status='Round56 frozen WCA threshold/v28; awaiting question1',active_round=out.name,next_question=1,answered_questions=0,batch_size=1,current_batch=[1],note='12 fresh pairs and24predictions frozen. One at a time, separate direction/meaningfulness, exact equality and unresolved available. Predictions hidden; no model updates during round.');p.write_text(json.dumps(s,indent=2)+'\n')
 block='## Active Round56 — WCA threshold versusv28\n\n12 fresh targeted comparisons; one at a time. All24 predictions, configurations and\nsource hashes frozen in round56-fixed.json before first answer. Eight wide-WCA\ntare cases, twoWCA10lb boundary controls, twoother-provenance controls. Include\ncompeting attributes that may not warrant a premium; do not assume their answers.\nKeep direction/meaningfulness separate; practical similarity is not exact equality;\nunresolved available. Hide predictions/interim scores. Awaiting question1.\n\n'
 for name in ('README.md','HANDOFF.md'):
  p=R/name;first,rest=p.read_text().split('\n',1);p.write_text(first+'\n\n'+block+rest.lstrip())
 p=R/'SESSION-CHECKPOINT.md';p.write_text('# Current task — Round56 active\n\n'+block+'---\nHistorical checkpoint follows.\n\n'+p.read_text())
 print(json.dumps({'frozen_pairs':12,'prediction_rechecks':24,'history_files':len(histories),'first_question':{k:qs[0][k] for k in ('number','a','b')}}))
if __name__=='__main__':main()
