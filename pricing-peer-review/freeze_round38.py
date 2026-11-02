"""Freeze a twelve-pair prospective v18/v17 comparison before elicitation."""
from pathlib import Path
import json, hashlib
from datetime import datetime, timezone
from pricing_v18 import Model as V18
from pricing_v17_precision import Model as V17
ROOT=Path(__file__).resolve().parent

def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def pair(a,b): return frozenset((tuple(a),tuple(b)))
def collect(obj,seen):
    if isinstance(obj,dict):
        if isinstance(obj.get('a'),list) and isinstance(obj.get('b'),list) and len(obj['a'])==len(obj['b'])==4 and all(isinstance(v,(str,int,float)) for v in obj['a']+obj['b']):seen.add(pair(obj['a'],obj['b']))
        for v in obj.values():collect(v,seen)
    elif isinstance(obj,list):
        for v in obj:collect(v,seen)

# Attribute design fixed without querying either model: six mature regional cases,
# two younger regional controls, two shade/vintage trades and two mixed contrasts.
DESIGN=[
('mature_regional',['northwest','amber',35,120],['Western Europe','amber',35,125]),
('shade_vintage',['southeast','golden',25,120],['southeast','pale/straw',30,120]),
('mature_regional',['central','brown',35,120],['Eastern Europe','brown',35,120]),
('young_regional',['Western Europe','copper',25,115],['central','copper',25,120]),
('mature_regional',['southwest','golden',40,115],['northwest','golden',40,120]),
('mixed',['Eastern Europe','amber',25,115],['northeast','amber',35,125]),
('mature_regional',['West Central Asia','pale/straw',35,125],['Western Europe','pale/straw',35,120]),
('shade_vintage',['Western Europe','golden',25,125],['Western Europe','pale/straw',30,125]),
('mature_regional',['southeast','brown',30,125],['central','brown',30,120]),
('young_regional',['northeast','amber',20,125],['southwest','amber',20,125]),
('mixed',['West Central Asia','copper',25,130],['South/Eastern Asia','golden',30,110]),
('mature_regional',['Eastern Europe','golden',40,125],['central','golden',40,130]),
]

def main():
    out=ROOT/'round38-fixed.json'
    if out.exists():raise FileExistsError(out)
    histories=sorted(set(ROOT.glob('round*-fixed.json'))|set(ROOT.glob('evidence*.json'))|{ROOT/'comparisons.json'})
    seen=set()
    for p in histories:collect(json.loads(p.read_text()),seen)
    questions=[]
    for i,(category,aa,bb) in enumerate(DESIGN,1):
        # If an exact historical pair exists, shift both tares by the same amount;
        # never select or reject a pair using model output.
        for shift in (0,5,-5,10,-10,15,-15,20,-20):
            a=aa[:3]+[aa[3]+shift];b=bb[:3]+[bb[3]+shift]
            if a[3] in (110,115,120,125,130) and b[3] in (110,115,120,125,130) and pair(a,b) not in seen:break
        else:raise ValueError(('No fresh design variant',i))
        seen.add(pair(a,b));questions.append(dict(id=f'round38-{i}',number=i,category=category,a=a,b=b,status='pending',direction=None,meaningfulness=None,raw_answer=None,exact_price_instruction=False))
    # Only now instantiate models and compute all predictions.
    models={'v18':V18(),'improved_v17':V17()}
    for q in questions:q['predictions']={name:m.compare(q['a'],q['b']) for name,m in models.items()}
    files=['contextual-boundary-fit-delivery-v18.json','precision-shade-candidate-v17.json','pricing_v18.py','pricing_v17_precision.py','pricing_v17.py','contextual_meaningfulness.py','domestic_shade_model.py','compare_models.py','evidence-v18.json','benchmark-targets-v18.json','freeze_round38.py']
    fields=['id','number','category','a','b','predictions']
    frozen=[{k:q[k] for k in fields} for q in questions]
    data=dict(round=38,created_at=datetime.now(timezone.utc).isoformat(),status='in_progress',protocol='12 previously unseen unordered pairs; attribute-stratified design chosen before model calls. Nearby families may recur: fresh pairs, not entirely unseen attribute families or a random population sample. No refitting, prediction changes, feedback or adaptive question selection until all12 answered. Direction and meaningfulness scored separately; missing axes excluded, never inferred. Unresolved/save for later permitted. No clear direction is not exact equality.',models={name:json.loads((ROOT/file).read_text()) for name,file in [('v18','contextual-boundary-fit-delivery-v18.json'),('improved_v17','precision-shade-candidate-v17.json')]},file_sha256={f:digest(ROOT/f) for f in files},freshness_history_sha256={p.name:digest(p) for p in histories},freeze_fields=fields,questions_and_predictions_sha256=hashlib.sha256(json.dumps(frozen,sort_keys=True).encode()).hexdigest(),questions=questions,rule_statements=[],answer_options=dict(direction=['A','B','no_clear_direction','unresolved'],meaningfulness=['meaningful_difference','no_meaningful_difference','unresolved']),scores=None)
    out.write_text(json.dumps(data,indent=2)+'\n')
    # Verify serialized freeze and recompute predictions without exposing them.
    saved=json.loads(out.read_text())
    assert hashlib.sha256(json.dumps([{k:q[k] for k in fields} for q in saved['questions']],sort_keys=True).encode()).hexdigest()==data['questions_and_predictions_sha256']
    for q in saved['questions']:
        for name,m in models.items():assert m.compare(q['a'],q['b'])==q['predictions'][name]
    for f,h in data['file_sha256'].items():assert digest(ROOT/f)==h
    progress=ROOT/'pricing-reset-progress.json';p=json.loads(progress.read_text());p.update(status='Round38 frozen; awaiting question1',active_round=out.name,next_question=1,answered_questions=0,note='All12 pairs and both model predictions frozen. Record direction and meaningfulness separately; unresolved allowed. No refit until complete.');progress.write_text(json.dumps(p,indent=2)+'\n')
    block='## Active frozen comparison — Round38\n\n12 fresh unordered pairs compare v18 against improved precision v17. All pairs and\npredictions frozen in round38-fixed.json before answers. Attribute design preceded\nmodel calls; historical pairs including reversed pairs excluded. Some families recur.\nPresent one at a time; hide predictions and interim results. Record direction and\nmeaningfulness separately, allow unresolved/save for later, infer neither missing\naxis nor exact equality. Models/evidence stay fixed throughout. Q1 awaiting answer.\n\n'
    for name in ('README.md','HANDOFF.md'):
        path=ROOT/name;first,rest=path.read_text().split('\n',1);path.write_text(first+'\n\n'+block+rest.lstrip('\n'))
    print(json.dumps({'frozen':12,'freshness_checked_history_files':len(histories),'prediction_rechecks':24,'question1':{k:questions[0][k] for k in ('id','a','b')}}))
if __name__=='__main__':main()
