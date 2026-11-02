"""Freeze fresh v21/v20 questions; retain correction outside frozen evidence."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
from pricing_v21 import Model as V21
from pricing_v20 import Model as V20
from freeze_round40 import collect,key
R=Path(__file__).resolve().parent
DESIGN=[
('zero_shade',['Eastern Europe','golden',30,130],['Eastern Europe','pale/straw',30,130]),
('mixed_tare',['Western Europe','pale/straw',30,120],['Western Europe','golden',25,125]),
('young_vintage',['West Central Asia','golden',20,115],['West Central Asia','pale/straw',25,115]),
('zero_shade',['Western Europe','pale/straw',20,130],['Western Europe','golden',20,130]),
('middle_tare',['Eastern Europe','golden',30,120],['Eastern Europe','pale/straw',35,120]),
('mixed_tare',['West Central Asia','pale/straw',25,125],['West Central Asia','golden',20,130]),
('light_tare',['Eastern Europe','pale/straw',35,115],['Eastern Europe','golden',30,115]),
('zero_shade',['West Central Asia','golden',40,130],['West Central Asia','pale/straw',40,130]),
('reinforcing',['Western Europe','golden',35,125],['Western Europe','pale/straw',30,125]),
('pure_five_lb',['Eastern Europe','pale/straw',20,120],['Eastern Europe','pale/straw',20,125]),
('domestic_control',['northeast','golden',25,125],['northeast','pale/straw',30,125]),
('young_vintage',['Eastern Europe','golden',20,110],['Eastern Europe','pale/straw',25,110]),
]
def main():
 out=R/'round41-fixed.json'
 if out.exists():raise FileExistsError(out)
 prior=json.loads((R/'evidence-v21.json').read_text());row=next(q for q in prior['rows'] if q['id']=='revision-13')
 correction={'source_id':'revision-13','source_evidence':'evidence-v21.json','a':row['a'],'b':row['b'],'previous_record':row,'corrected_direction':'B','corrected_meaningfulness':None,'raw_clarification':'To be sure, eastern europe at 120 lb, pale, versus golden 25 year ... the 25 year vintage must win unless I mistyped or was confused.','interpretation':'User corrects earlier direction: golden25 wins over pale30 at matched Eastern Europe120lb. Strength/meaningfulness not supplied; do not carry forward old slightly qualifier.','status':'pending_next_evidence_version','models_refit':False,'recorded_at':datetime.now(timezone.utc).isoformat()}
 cp=R/'revision-13-correction.json'
 if cp.exists():raise FileExistsError(cp)
 cp.write_text(json.dumps(correction,indent=2)+'\n')
 histories=sorted(set(R.glob('round*-fixed.json'))|set(R.glob('evidence*.json'))|{R/'comparisons.json'});seen=set()
 for p in histories:collect(json.loads(p.read_text()),seen)
 qs=[]
 for i,(category,aa,bb) in enumerate(DESIGN,1):
  for shift in (0,5,-5,10,-10,15,-15,20,-20):
   a=aa.copy();b=bb.copy();a[2]+=shift;b[2]+=shift
   if category=='young_vintage' and min(a[2],b[2])!=20:continue
   if a[2] in (20,25,30,35,40) and b[2] in (20,25,30,35,40) and key(a,b) not in seen:break
  else:raise ValueError(('No fresh design',i))
  seen.add(key(a,b));qs.append({'id':f'round41-{i}','number':i,'category':category,'a':a,'b':b,'status':'pending','direction':None,'meaningfulness':None,'raw_answer':None,'exact_price_instruction':False})
 models={'v21':V21(),'v20':V20()}
 for q in qs:q['predictions']={n:m.compare(q['a'],q['b']) for n,m in models.items()}
 sources=['shade-vintage-shared-delivery-v21.json','contextual-shade-delivery-v20.json','evidence-v21.json','benchmark-targets-v21.json','revision-13-correction.json','pricing_v21.py','pricing_v20.py','shade_vintage_shared_v21.py','contextual_shade_v20.py','contextual_fixes_v19.py','contextual_meaningfulness.py','domestic_shade_model.py','compare_models.py','freeze_round41.py','freeze_round40.py'];fields=['id','number','category','a','b','predictions']
 data={'round':41,'created_at':datetime.now(timezone.utc).isoformat(),'status':'in_progress','protocol':'12 fresh unordered pairs including reversed duplicates excluded. Attribute-selected zero-shade,mid/light-tare,young-vintage,mixed-tare and controls; design before model calls. Familiar families, not random population accuracy. Both models/predictions frozen. No feedback/scoring/refit before completion. Direction and meaningfulness separate, unresolved allowed. Explicit zero-shade/tie statements get separate checks; do not hide under practical classification.','pending_corrections':['revision-13-correction.json'],'models':{'v21':json.loads((R/'shade-vintage-shared-delivery-v21.json').read_text()),'v20':json.loads((R/'contextual-shade-delivery-v20.json').read_text())},'file_sha256':{f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in sources},'freshness_history_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in histories},'freeze_fields':fields,'questions_and_predictions_sha256':hashlib.sha256(json.dumps([{k:q[k] for k in fields} for q in qs],sort_keys=True).encode()).hexdigest(),'questions':qs,'rule_statements':[],'scores':None}
 out.write_text(json.dumps(data,indent=2)+'\n');saved=json.loads(out.read_text());assert hashlib.sha256(json.dumps([{k:q[k] for k in fields} for q in saved['questions']],sort_keys=True).encode()).hexdigest()==data['questions_and_predictions_sha256']
 for q in saved['questions']:
  for n,m in models.items():assert m.compare(q['a'],q['b'])==q['predictions'][n]
 for f,h in data['file_sha256'].items():assert hashlib.sha256((R/f).read_bytes()).hexdigest()==h
 p=R/'pricing-reset-progress.json';d=json.loads(p.read_text());d.update(status='Round41 frozen v21/v20; awaiting question1',active_round=out.name,next_question=1,answered_questions=0,pending_corrections=['revision-13-correction.json'],note='User corrected revision-13 to younger golden25 directionB; size unspecified. Correction separately saved for next evidence version. All12 fresh pairs and predictions frozen before answers.');p.write_text(json.dumps(d,indent=2)+'\n')
 block='## Active Round41 — frozen v21 versus v20\n\n12 fresh unordered pairs and predictions frozen in round41-fixed.json before answers.\nShow one at a time, hide predictions/interim scores, separate direction/meaningfulness,\nunresolved allowed. Explicit zero-shade claims checked separately. Q1 awaiting answer.\nUser correction saved in revision-13-correction.json: EE120 golden25 beats pale30;\nmeaningfulness unspecified. Earlier disagreement is superseded by clarification,\nbut frozen evidence/model artifacts remain intact until next evidence incorporation.\nNo refits during this round.\n\n'
 for name in ('README.md','HANDOFF.md'):
  p=R/name;first,rest=p.read_text().split('\n',1);p.write_text(first+'\n\n'+block+rest.lstrip('\n'))
 print(json.dumps({'frozen':12,'prediction_rechecks':24,'history_files':len(histories),'first':{k:qs[0][k] for k in ('a','b')}}))
if __name__=='__main__':main()
