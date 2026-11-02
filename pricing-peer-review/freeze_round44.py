"""Freeze fresh targeted all-weight joint refit versus v24 comparisons."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
from pricing_joint_weights_v22 import Model as Refit
from pricing_v24 import Model as V24
from freeze_round40 import collect,key
R=Path(__file__).resolve().parent
DESIGN=[
('five_year',['Western Europe','golden',25,110],['Western Europe','pale/straw',30,110]),
('five_year',['Eastern Europe','pale/straw',35,110],['Eastern Europe','golden',30,110]),
('pure_five_lb',['central','amber',30,115],['central','amber',30,120]),
('five_year',['West Central Asia','golden',25,115],['West Central Asia','pale/straw',30,115]),
('zero_shade',['southeast','pale/straw',30,130],['southeast','golden',30,130]),
('five_year',['northwest','pale/straw',25,120],['northwest','golden',20,120]),
('same_age_shade',['Eastern Europe','golden',30,125],['Eastern Europe','pale/straw',30,125]),
('five_year',['Western Europe','golden',30,125],['Western Europe','pale/straw',35,120]),
('other_shade',['West Central Asia','amber',25,120],['West Central Asia','copper',30,115]),
('five_year',['Eastern Europe','pale/straw',30,120],['Eastern Europe','golden',25,125]),
('zero_shade',['northwest','golden',25,130],['northwest','pale/straw',25,130]),
('pure_five_lb',['Western Europe','copper',35,125],['Western Europe','copper',35,120]),
]

def main():
 out=R/'round44-fixed.json'
 if out.exists():raise FileExistsError(out)
 histories=sorted(set(R.glob('round*-fixed.json'))|set(R.glob('evidence*.json'))|{R/'comparisons.json'});seen=set()
 for p in histories:collect(json.loads(p.read_text()),seen)
 qs=[]
 for i,(category,aa,bb) in enumerate(DESIGN,1):
  for shift in (0,5,-5,10,-10,15,-15,20,-20):
   a=aa.copy();b=bb.copy();a[2]+=shift;b[2]+=shift
   if category in ('young_mixed_tare','domestic_vintage') and min(a[2],b[2])!=20:continue
   if a[2] in (20,25,30,35,40) and b[2] in (20,25,30,35,40) and key(a,b) not in seen:break
  else:raise ValueError(('No fresh pair',i))
  seen.add(key(a,b));qs.append({'id':f'round44-{i}','number':i,'category':category,'a':a,'b':b,'status':'pending','direction':None,'meaningfulness':None,'raw_answer':None,'exact_price_instruction':False})
 models={'joint_weight_refit':Refit(),'v24':V24()}
 for q in qs:q['predictions']={n:m.compare(q['a'],q['b']) for n,m in models.items()}
 sources=['direct-joint-weights-delivery-v22.json','five-year-premium-delivery-v24.json','evidence-v24.json','benchmark-targets-v24.json','pricing_joint_weights_v22.py','pricing_v24.py','five_year_premium_v23.py','joint_weight_refit_v22.py','joint_objective_v22.py','residual_fixes_v22.py','shade_vintage_shared_v21.py','contextual_shade_v20.py','contextual_fixes_v19.py','contextual_meaningfulness.py','domestic_shade_model.py','compare_models.py','freeze_round44.py','freeze_round40.py'];fields=['id','number','category','a','b','predictions']
 d={'round':44,'created_at':datetime.now(timezone.utc).isoformat(),'status':'in_progress','protocol':'12 fresh unordered pairs; reversed duplicates excluded against saved rounds/evidence. Six five-year golden/pale targets across foreign/domestic and mixed tare, plus same-age-shade/other-shade,2 zero-shade and2 pure5lb controls. All design/freshness choices precede model calls; no selection by prediction output. Familiar families,not random population sample. Freeze models/questions/predictions before answers; hide predictions/interim scoring; no refits. Direction and meaningfulness separate with unresolved option. Explicit ties/zero-premium claims scored separately from tiny preferences.','models':{'joint_weight_refit':json.loads((R/'direct-joint-weights-delivery-v22.json').read_text()),'v24':json.loads((R/'five-year-premium-delivery-v24.json').read_text())},'file_sha256':{f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in sources},'freshness_history_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in histories},'freeze_fields':fields,'questions_and_predictions_sha256':hashlib.sha256(json.dumps([{k:q[k] for k in fields} for q in qs],sort_keys=True).encode()).hexdigest(),'questions':qs,'rule_statements':[],'scores':None}
 out.write_text(json.dumps(d,indent=2)+'\n');saved=json.loads(out.read_text());assert hashlib.sha256(json.dumps([{k:q[k] for k in fields} for q in saved['questions']],sort_keys=True).encode()).hexdigest()==d['questions_and_predictions_sha256']
 for q in saved['questions']:
  for n,m in models.items():assert m.compare(q['a'],q['b'])==q['predictions'][n]
 for f,h in d['file_sha256'].items():assert hashlib.sha256((R/f).read_bytes()).hexdigest()==h
 p=R/'pricing-reset-progress.json';s=json.loads(p.read_text());s.update(status='Round44 frozen joint-weight refit versus v24; awaiting question1',active_round=out.name,next_question=1,answered_questions=0,note='12 fresh exact pairs and24 predictions frozen before answers. Separate direction/meaningfulness; unresolved allowed. No evidence/model changes.');p.write_text(json.dumps(s,indent=2)+'\n')
 block='## Active Round44 — joint weight refit versus v24\n\n12 fresh unordered comparisons checked against all saved rounds/evidence, including\nreversed orientation. Five-year golden/pale,domestic,mixed-tare and other-shade\nchallenges plus zero-shade/pure5lb controls. Selection precedes prediction calls.\nAll questions and24 predictions frozen in round44-fixed.json. Present one at a time;\nhide predictions/interim scores; direction/meaningfulness separate; unresolved\navailable. Explicit tie/zero-premium checks separate. Q1 awaiting answer. No refits.\n\n'
 for name in ('README.md','HANDOFF.md'):
  p=R/name;first,rest=p.read_text().split('\n',1);p.write_text(first+'\n\n'+block+rest.lstrip('\n'))
 print(json.dumps({'frozen_pairs':12,'prediction_rechecks':24,'history_files':len(histories),'first':{k:qs[0][k] for k in ('a','b')}}))
if __name__=='__main__':main()
