from pathlib import Path
import json,hashlib
import numpy as np
import joint_models_v27 as model
import joint_objective_v22 as joint
import refit_simple_benchmark_v16 as metrics
from validate_contextual_meaningfulness_v18 import extend_folds
from reconcile_and_compare import write_versioned
R=Path(__file__).resolve().parent
ARMS=('v26','additive','additive_domestic','contextual')
SOURCES=['evidence-v26.json','evidence-v27.json','benchmark-targets-v27.json','joint-refit-validation-v26.json','joint-refit-candidate-v26.json','round49-fixed.json','round50-isolation.json','joint_models_v27.py','validate_joint_models_v27.py','joint_objective_v22.py','joint_refit_v26.py']
def main():
 hashes={f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in SOURCES};old=json.loads((R/'joint-refit-validation-v26.json').read_text());t=json.loads((R/'benchmark-targets-v27.json').read_text())['rows'];e=json.loads((R/'evidence-v27.json').read_text())['rows'];ix={q['id']:i for i,q in enumerate(t)};groups=model.features.arrays(t)[3];direct=metrics.verified_materiality(e);runs={a:[] for a in ARMS};audits=[]
 for seed in metrics.SEEDS:
  fs=sorted([q for q in old['nested_cv']['fold_audits'] if q['seed']==seed],key=lambda q:q['fold']);splits=[(np.array([ix[i] for i in f['training_ids']]),np.array([ix[i] for i in f['validation_ids']])) for f in fs];mm={a:np.zeros(len(t)) for a in ARMS};rr={a:np.zeros(len(t)) for a in ARMS}
  for fold,(tr,te) in enumerate(extend_folds(groups,groups[:556],splits,5,seed)):
   f=fs[fold];ref=f['fit']['reference_context'];start=f['fit']['coefficients'];assert [t[i]['id'] for i in tr if i<556]==f['training_ids'];assert not set(groups[tr])&set(groups[te]);train=[t[i] for i in tr];test=[t[i] for i in te];x,offset,r=model.contextual.design(test,ref);mm['v26'][te]=x@start+offset;rr['v26'][te]=r;fits={}
   for a in ARMS[1:]:
    fit=model.fit(train,a,ref,start);fits[a]=fit;g,r=model.margins(test,fit);mm[a][te]=g;rr[a][te]=r
   audits.append({'seed':seed,'fold':fold,'training_ids':[t[i]['id'] for i in tr],'validation_ids':[t[i]['id'] for i in te],'reference_context':ref,'start_coefficients':start,'fits':fits})
  prior=next(q for q in old['nested_cv']['runs']['joint_refit'] if q['seed']==seed);np.testing.assert_allclose(mm['v26'][:556],prior['margins'],atol=1e-12);np.testing.assert_allclose(rr['v26'][:556],prior['radii'],atol=1e-12)
  for a in ARMS:runs[a].append({'seed':seed,'margins':mm[a].tolist(),'radii':rr[a].tolist(),'score':metrics.score(t,mm[a],rr[a],direct),'joint_score':joint.score(t,mm[a],rr[a])})
  print('Completed seed',seed,flush=True)
 summary=metrics.summarize(runs);js={a:{k:(series[0]['joint_score'][k] if k.endswith('_n') else float(np.mean([q['joint_score'][k] for q in series]))) for k in ('supported_n','correct','accuracy','both_axes_n','both_axes_correct','both_axes_accuracy','balanced_accuracy','signed_joint_loss')} for a,series in runs.items()};base=summary['v26'];checks={}
 for a in ARMS[1:]:
  s=summary[a];checks[a]={'joint_improves':js[a]['balanced_accuracy']>js['v26']['balanced_accuracy']+1e-10,'both_axes_noninferior':js[a]['both_axes_accuracy']>=js['v26']['both_axes_accuracy']-1e-10,'direction_noninferior':s['direction']['accuracy']>=base['direction']['accuracy']-1e-10,'false_premiums_noninferior':s['materiality']['false_meaningful']<=base['materiality']['false_meaningful']+1e-10}
 eligible=[a for a in ARMS[1:] if all(checks[a].values())];winner=max(eligible,key=lambda a:(js[a]['balanced_accuracy'],-ARMS.index(a))) if eligible else 'v26'
 cfg=json.loads((R/'joint-refit-candidate-v26.json').read_text())['model'];full={a:model.fit(t,a,cfg['reference_context'],cfg['coefficients']) for a in ARMS[1:]}
 result={'source_hashes':hashes,'protocol':'Controlled joint fits on v27. 18-coefficient additive score with a fixed per-offering pale=golden130lb rule, no pair gates or offsets, constant normalized threshold1. Optional19th coefficient gives domestic pale its own increment. Hard cap tare+pale increment<=1 preserves every pure5lb step including125to130. Contextual control refits all19v26 weights with fixed existing context/offset/boundary. Same joint objective, starts and schedule. Original25 family splits extended label-free; all fitting train-only. Frozenv26 predictions unchanged. Select eligible joint winner; simpler wins exact tie. Unresolved not labels. Repeated/adaptive validation exploratory, not prospective.','row_ids':[q['id'] for q in t],'nested_cv':{'runs':runs,'summary':summary,'joint_summary':js,'fold_audits':audits},'full_models':full,'delivery':{'selected':winner,'checks':checks},'full_isolation_predictions':{a:{q['id']:model.predict(q['a'],q['b'],fit) for q in t if q['id'].startswith('round50-') or q['id'] in ('round49-2','round49-6','round49-16')} for a,fit in full.items()}}
 write_versioned(R/'joint-models-validation-v27.json',result);write_versioned(R/'joint-models-delivery-v27.json',{'selected_model':winner,'model':full.get(winner),'retained_source':'model-config.json' if winner=='v26' else None,'evidence':'evidence-v27.json','validation_file':'joint-models-validation-v27.json','validation':summary[winner],'joint_validation':js[winner]})
 for f,h in hashes.items():assert hashlib.sha256((R/f).read_bytes()).hexdigest()==h
 print(json.dumps({'summary':summary,'joint':js,'delivery':result['delivery']},indent=2))
if __name__=='__main__':main()
