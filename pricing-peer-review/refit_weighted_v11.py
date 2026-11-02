"""Version semantic clarification without overwriting prior evidence or models."""
from copy import deepcopy
from collections import Counter
from pathlib import Path
import hashlib,json
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components
import compare_models as base
import compare_tare_models as tare
import provenance_tare_model as offering
import weighted_domestic_model as weighted
import domestic_hierarchy_model as prior
import refit_weighted_v10 as protocol
import semantic_weighted_model as semantic
from reconcile_and_compare import align_answer,write_versioned

ROOT=Path(__file__).resolve().parent
SOURCES=tuple(dict.fromkeys((*protocol.SOURCES,'refit_weighted_v10.py','evidence-v10.json','weighted-hierarchy-comparison-v10.json','regional-convergence-comparison-v10.json','selective-convergence-comparison-v10.json','round33-reconciliation.json','semantic_weighted_model.py','refit_weighted_v11.py')))


def build_evidence(parent,round33):
    if round33['semantic_clarification']['selected_meaning']!='practical similarity':raise ValueError('Missing explicit semantic clarification')
    rows=deepcopy(parent['rows']);index={r['id']:r for r in rows};audit=[]
    for row in rows:
        row['judgment_type']='exact_equality' if row['winner']=='tie' else 'strict_preference'
        row['direction']=row['winner'] if row['winner'] in ('A','B') else None
    similar=set(round33['semantic_clarification']['practical_similarity_option3_ids'])
    assert len(similar)==4 and len(round33['questions'])==5
    for q in round33['questions']:
        if q['status']!='answered':raise ValueError('Incomplete reconciliation')
        row=index[q['revisits']];aligned=align_answer(row,q)
        previous=deepcopy(row)
        if q['id'] in similar:
            if q['winner']!='tie':raise ValueError('Similarity clarification must refer to option3 response')
            row.update(winner='practical_similarity',judgment_type='practical_similarity',direction=None,strength=None)
        else:
            if aligned not in ('A','B'):raise ValueError('Preserve explicit directional answer')
            row.update(winner=aligned,judgment_type='strict_preference',direction=aligned,strength=q.get('strength'))
        row['current_raw_answer']=q['raw_answer'];row['current_answer_source']=q['id']
        row['semantic_reconciliation']={'source_file':'round33-reconciliation.json','question_id':q['id'],'raw_response':q['raw_answer'],'clarification':round33['semantic_clarification']['raw_answer'],'prior_version':'evidence-v10.json','prior_row':previous,'scope':'This specific revisited golden20/120 pair; no blanket reinterpretation of historical ties.','note':'Known strict direction retained for round33-1; practical qualification is metadata without an additional numerical bound. Four option3 responses now indicate practical similarity with unknown direction.'}
        audit.append({'id':row['id'],'source_question':q['id'],'old_winner':previous['winner'],'new_winner':row['winner'],'action':'semantic reclassification' if q['id'] in similar else 'direction confirmed; wording and strength updated'})
    unresolved=deepcopy(parent['unresolved_pairs'])
    for r in unresolved:r.update(judgment_type='unresolved',direction=None)
    assert len(rows)==401 and Counter(r['winner'] for r in rows)=={'A':177,'B':83,'tie':137,'practical_similarity':4}
    assert {r['id'] for r in unresolved}=={'round27-7','round27-11'}
    assert len({frozenset((tuple(r['a']),tuple(r['b']))) for r in rows})==401
    return rows,audit,unresolved


def consistency_audit(rows):
    nodes=sorted({tuple(r[k]) for r in rows for k in ('a','b')});ix={n:i for i,n in enumerate(nodes)};edges=[]
    for r in rows:
        if r['winner']=='practical_similarity':continue
        a,b=ix[tuple(r['a'])],ix[tuple(r['b'])]
        if r['winner']=='B':a,b=b,a
        edges.append((a,b,r['id'],r['winner']!='tie'))
        if r['winner']=='tie':edges.append((b,a,r['id'],False))
    graph=csr_matrix((np.ones(len(edges)),([e[0] for e in edges],[e[1] for e in edges])),shape=(len(nodes),len(nodes)))
    _,components=connected_components(graph,directed=True,connection='strong')
    return {'offering_nodes':len(nodes),'strict_edges_in_equality_or_preference_cycles':[e[2] for e in edges if e[3] and components[e[0]]==components[e[1]]],'scope':'Observed strict/equality graph only; practical similarity generates no equality edges. Does not establish identifiability or guarantee a restricted model can fit.'}


def summary(runs):
    first=runs[0]['semantic_metrics']
    return {'n':first['n'],'counts':first['counts'],
        **{k:float(np.mean([r['semantic_metrics'][k] for r in runs])) for k in ['semantic_compatibility','balanced_semantic_compatibility','opposite_winner_errors','predicted_exact_score_equalities','predicted_within_similarity_band']},
        'recall':{k:float(np.mean([r['semantic_metrics']['recall'][k] for r in runs])) for k in first['recall']},
        'legacy_band_diagnostic':tare.summarize([{'metrics':{'all':r['legacy_band_diagnostic']}} for r in runs])['all']}


def main():
    hashes={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in SOURCES}
    parent=json.loads((ROOT/'evidence-v10.json').read_text());round33=json.loads((ROOT/'round33-reconciliation.json').read_text())
    fields=round33['freeze_fields'];assert hashlib.sha256(json.dumps([{k:q[k] for k in fields} for q in round33['questions']],sort_keys=True).encode()).hexdigest()==round33['questions_sha256']
    for f,h in round33['file_sha256'].items():assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h,f
    rows,audit,unresolved=build_evidence(parent,round33)
    graph={'v10':consistency_audit(parent['rows']),'v11':consistency_audit(rows)}
    snapshot={'version':11,'parent':'evidence-v10.json','parent_sha256':hashes['evidence-v10.json'],'row_count':401,'label_counts':dict(Counter(r['winner'] for r in rows)),'source_hashes':hashes,'reconciliation_audit':audit,'semantic_clarification':round33['semantic_clarification'],'explanatory_guidance':deepcopy(parent['explanatory_guidance'])+[{'source_file':'round33-reconciliation.json',**deepcopy(s)} for s in round33['rule_statements']],'unresolved_pairs':unresolved,'consistency_audit':graph,'protocol':'Same401 unique pairs, no extra samples. Four specifically revisited rows become practical_similarity, no winner assigned. One strict direction retained. All other labels retained, not newly reverified. Practical similarity is neither exact equality nor unresolved; Q7/Q11 remain excluded. Raw prior records and clarification retained. No numerical user tolerance inferred.','rows':rows}
    write_versioned(ROOT/'evidence-v11.json',snapshot)
    previous=json.loads((ROOT/'weighted-hierarchy-comparison-v10.json').read_text());y,g=semantic.arrays(rows)
    configs={(a['seed'],a['fold']):a for a in previous['nested_cv']['fold_audits'] if a['model']=='v10_evidence_candidate'}
    runs={'v10_evidence_control':[],'v11_evidence_candidate':[]};audits=[]
    for seed in prior.SEEDS:
        ms={name:np.zeros(len(rows)) for name in runs};radii=np.zeros(len(rows))
        for fold,(tr,te) in enumerate(protocol.extended_folds(g[:366],g,seed)):
            assert not set(g[tr])&set(g[te]);cfg=configs[(seed,fold)];test=[rows[i] for i in te];radii[te]=cfg['threshold']
            oldtrain=[parent['rows'][i] for i in tr];d,beta=offering.fit(oldtrain,cfg);layer=weighted.Layer(d,beta);params=weighted.fit(oldtrain,layer,cfg['prior_strength']);ms['v10_evidence_control'][te]=semantic.margins(test,layer,params)
            training=[rows[i] for i in tr];strength,inner=semantic.choose(training,cfg,seed+fold+7000)
            d,beta=semantic.fit_offering(training,cfg);layer=weighted.Layer(d,beta);params=semantic.fit_layer(training,layer,strength,cfg['threshold']);ms['v11_evidence_candidate'][te]=semantic.margins(test,layer,params)
            audits.append({'seed':seed,'fold':fold,'train_n':len(tr),'test_n':len(te),'train_label_counts':dict(Counter(r['winner'] for r in training)),'alpha':cfg['alpha'],'pooling':cfg['pooling'],'threshold_and_similarity_radius':cfg['threshold'],'prior_strength':strength,'control_prior_strength':cfg['prior_strength'],'inner_semantic_metrics':inner,'local_contexts':list(d.local_contexts),'hard_tare_tie_ids':[r['id'] for r in training if r['winner']=='tie' and r['a'][:3]==r['b'][:3] and r['a'][3]!=r['b'][3]]})
            print(f'Completed semantic v11 seed {seed}, fold {fold+1}/5',flush=True)
        old=next(r for r in previous['nested_cv']['runs']['v10_evidence_candidate'] if r['seed']==seed)
        oldpred=np.where(ms['v10_evidence_control']>radii+1e-8,1,np.where(ms['v10_evidence_control']<-radii-1e-8,-1,0))
        np.testing.assert_array_equal(oldpred,old['predictions'])
        for name,m in ms.items():runs[name].append({'seed':seed,'margins':m.tolist(),'similarity_radii':radii.tolist(),'semantic_metrics':semantic.assess(y,m,radii),'legacy_band_diagnostic':semantic.operational_metrics(y,m,radii)})
    cfg=previous['candidate_fit_all_401']['offering_snapshot'];strength,inner=semantic.choose(rows,cfg,801)
    d,beta=semantic.fit_offering(rows,cfg);layer=weighted.Layer(d,beta);params=semantic.fit_layer(rows,layer,strength,cfg['threshold']);m=semantic.margins(rows,layer,params)
    pure=np.array([r['winner']=='tie' and r['a'][:3]==r['b'][:3] and r['a'][3]!=r['b'][3] for r in rows])
    def record(i,r):
        return {'id':r['id'],'judgment_type':r['judgment_type'],'recorded_direction':r['direction'],'margin':float(m[i]),'score_direction':'A' if m[i]>semantic.EXACT_TOL else 'B' if m[i]<-semantic.EXACT_TOL else 'equal','exact_score_equality':bool(abs(m[i])<=semantic.EXACT_TOL),'within_similarity_band':bool(abs(m[i])<=cfg['threshold']+1e-8)}
    candidate={'prior_strength':strength,'threshold':cfg['threshold'],'similarity_radius':cfg['threshold'],'exact_tolerance':semantic.EXACT_TOL,'offering_snapshot':{'alpha':cfg['alpha'],'pooling':cfg['pooling'],'threshold':cfg['threshold'],'local_contexts':list(d.local_contexts),'feature_names':d.names(),'coefficients':beta.tolist()},'parameters':params.tolist(),'domestic_order':prior.DOMESTIC,'template':prior.TEMPLATE.tolist(),'contexts':prior.CONTEXTS,'domestic_component_scales':dict(zip(['shade','vintage','tare'],params[30:].tolist())),'semantic_training_metrics':semantic.assess(y,m,cfg['threshold']),'legacy_training_band_diagnostic':semantic.operational_metrics(y,m,cfg['threshold']),'pure_tare_tie_audit':{'n':int(sum(pure)),'exact_score_equalities':int(sum(abs(m[pure])<=semantic.EXACT_TOL))},'reconciled_pair_predictions':[record(i,r) for i,r in enumerate(rows) if r['id'] in {a['id'] for a in audit}]}
    result={'method':{'evidence_version':11,'evidence_sha256':hashlib.sha256((ROOT/'evidence-v11.json').read_bytes()).hexdigest(),'historical_file_hashes':hashes,'architecture':'Unchanged provenance-scoped offering +33-parameter weighted domestic hierarchy; priors unchanged. Both stages use a new epsilon-insensitive practical-similarity loss.','semantics':'Strict squared hinge and retained exact-equality squared-zero loss unchanged. Similarity loss=max(0,abs(m)-radius)^2, permits either sign and nonzero gaps inside band. Similar rows never generate hard equality constraints. No unresolved targets fitted. Known slight direction remains strict; broad practical qualification metadata does not invent an extra numerical bound.','radius':'Inherited same per-fold threshold as model-scale similarity radius(0.15–0.5); full fit0.2. This is a declared modeling convention, not user-supplied monetary tolerance, and four similar pairs cannot establish a calibrated general tolerance.','prediction':'Separate score direction, numerical equality, and within-similarity-band flags. Direction and similarity may coexist. Unresolved is an evidence state, not an implemented abstention predictor.','validation':'Same401 rows/order/families as v10,5 outer folds x5 seeds. V10 control trained on old labels; v11 candidate on clarified labels. Base offering settings inherited; prior strength selected on grouped inner-training semantic compatibility, balancing strict-direction/exact-equality/practical-similarity recalls. Baseline original band predictions reproduced exactly. Four similarity rows are sparse and heavily influence a macro metric; report counts and per-type recalls.','reporting':'Semantic compatibility is set-valued, not four-class accuracy. Exact equality requires abs(m)<=1e-7; strict direction uses sign with same tolerance; similarity accepts either sign including zero within declared radius. Separately report legacy band diagnostic on397 determinate labels, where band ties are not proof of exact equality. Do not compare headline percentages directly with prior401-row three-class accuracy.','limits':'Repeated adaptive evidence, no fresh prospective validation. Only five revisited records updated; other equality labels not blanket reinterpreted. No peer-session interaction or baseline promotion.'},'nested_cv':{'row_ids':[r['id'] for r in rows],'runs':runs,'summary':{k:summary(v) for k,v in runs.items()},'fold_audits':audits},'candidate_fit_all_401':candidate}
    write_versioned(ROOT/'weighted-hierarchy-comparison-v11.json',result)
    for f,h in hashes.items():assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h,f
    print(json.dumps({'labels':snapshot['label_counts'],'graph_audit':graph,'validation':result['nested_cv']['summary'],'targets':candidate['reconciled_pair_predictions'],'baselines_unchanged':True},indent=2))

if __name__=='__main__':main()
