"""Freeze fresh targeted all-weight joint refit versus v24 comparisons."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
from pricing_v25 import Model as Refit
from pricing_v24 import Model as V24
from freeze_round40 import collect,key
R=Path(__file__).resolve().parent
DESIGN=[
('older_vintage',['West Central Asia','golden',35,110],['West Central Asia','pale/straw',40,110]),
('microshade',['southeast','amber',25,115],['southeast','copper',25,115]),
('brown_tradeoff',['Western Europe','brown',30,115],['northwest','amber',35,125]),
('older_vintage',['Eastern Europe','pale/straw',40,120],['Eastern Europe','golden',35,120]),
('large_tare',['South/Eastern Asia','amber',30,125],['South/Eastern Asia','amber',30,110]),
('regional_tradeoff',['central','golden',30,120],['northeast','golden',35,115]),
('microshade',['Western Europe','copper',20,125],['Western Europe','amber',20,125]),
('zero_shade',['southwest','golden',25,130],['southwest','pale/straw',25,130]),
('five_year_tradeoff',['West Central Asia','golden',30,120],['West Central Asia','pale/straw',25,125]),
('pure_five_lb',['Eastern Europe','brown',35,120],['Eastern Europe','brown',35,125]),
('foreign_tradeoff',['South/Eastern Asia','amber',20,125],['West Asia / Middle East','amber',30,115]),
('ten_year',['northwest','golden',40,125],['northwest','golden',30,125]),
]

def main():
 out=R/'round46-fixed.json'
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
  seen.add(key(a,b));qs.append({'id':f'round46-{i}','number':i,'category':category,'a':a,'b':b,'status':'pending','direction':None,'meaningfulness':None,'raw_answer':None,'exact_price_instruction':False})
 models={'v25':Refit(),'v24':V24()}
 for q in qs:q['predictions']={n:m.compare(q['a'],q['b']) for n,m in models.items()}
 sources=['older-dark-scoped-delivery-v25.json','five-year-premium-delivery-v24.json','evidence-v25.json','benchmark-targets-v25.json','pricing_v25.py','older_dark_scoped_v25.py','pricing_v24.py','five_year_premium_v23.py','joint_weight_refit_v22.py','joint_objective_v22.py','residual_fixes_v22.py','shade_vintage_shared_v21.py','contextual_shade_v20.py','contextual_fixes_v19.py','contextual_meaningfulness.py','domestic_shade_model.py','compare_models.py','freeze_round46.py','freeze_round40.py'];fields=['id','number','category','a','b','predictions']
 d={'round':46,'created_at':datetime.now(timezone.utc).isoformat(),'status':'in_progress','protocol':'12 fresh unordered pairs; reversed duplicates excluded against saved rounds/evidence. Varied attribute-selected older-vintage,microshade,brown and regional tradeoffs,small/large tare,zero-shade and five/ten-year age comparisons. All design/freshness choices precede model calls; no selection by prediction output. Familiar families,not random population sample. Freeze models/questions/predictions before answers; hide predictions/interim scoring; no refits. Direction and meaningfulness separate with unresolved option. Explicit ties/zero-premium claims scored separately from tiny preferences.','models':{'v25':json.loads((R/'older-dark-scoped-delivery-v25.json').read_text()),'v24':json.loads((R/'five-year-premium-delivery-v24.json').read_text())},'file_sha256':{f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in sources},'freshness_history_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in histories},'freeze_fields':fields,'questions_and_predictions_sha256':hashlib.sha256(json.dumps([{k:q[k] for k in fields} for q in qs],sort_keys=True).encode()).hexdigest(),'questions':qs,'rule_statements':[],'scores':None}
 out.write_text(json.dumps(d,indent=2)+'\n');saved=json.loads(out.read_text());assert hashlib.sha256(json.dumps([{k:q[k] for k in fields} for q in saved['questions']],sort_keys=True).encode()).hexdigest()==d['questions_and_predictions_sha256']
 for q in saved['questions']:
  for n,m in models.items():assert m.compare(q['a'],q['b'])==q['predictions'][n]
 for f,h in d['file_sha256'].items():assert hashlib.sha256((R/f).read_bytes()).hexdigest()==h
 p=R/'pricing-reset-progress.json';s=json.loads(p.read_text());s.update(status='Round46 frozen v25 versus v24; awaiting question1',active_round=out.name,next_question=1,answered_questions=0,note='12 fresh exact pairs and24 predictions frozen before answers. Separate direction/meaningfulness; unresolved allowed. No evidence/model changes.');p.write_text(json.dumps(s,indent=2)+'\n')
 block='## Active Round46 — v25 versus v24\n\n12 fresh unordered comparisons checked against all saved rounds/evidence, including\nreversed orientation. Older-vintage,microshade,brown,regional and mixed-attribute\nchallenges plus zero-shade/pure5lb controls. Selection precedes prediction calls.\nAll questions and24 predictions frozen in round46-fixed.json. Present one at a time;\nhide predictions/interim scores; direction/meaningfulness separate; unresolved\navailable. Explicit tie/zero-premium checks separate. Q1 awaiting answer. No refits.\n\n'
 for name in ('README.md','HANDOFF.md'):
  p=R/name;first,rest=p.read_text().split('\n',1);p.write_text(first+'\n\n'+block+rest.lstrip('\n'))
 print(json.dumps({'frozen_pairs':12,'prediction_rechecks':24,'history_files':len(histories),'first':{k:qs[0][k] for k in ('a','b')}}))
if __name__=='__main__':main()
