from collections import Counter
from copy import deepcopy
import hashlib,json,unittest
from itertools import product
import numpy as np
import compare_models as base
import compare_tare_models as tare
import compare_objectives as old_objective
import provenance_tare_model as offering
import weighted_domestic_model as weighted
import domestic_hierarchy_model as prior
import refit_weighted_v10 as old_protocol
import semantic_weighted_model as semantic
import refit_weighted_v11 as r

class WeightedV11Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parent=json.loads((r.ROOT/'evidence-v10.json').read_text());cls.round=json.loads((r.ROOT/'round33-reconciliation.json').read_text())
        cls.evidence=json.loads((r.ROOT/'evidence-v11.json').read_text());cls.rows=cls.evidence['rows']
        cls.result=json.loads((r.ROOT/'weighted-hierarchy-comparison-v11.json').read_text());cls.cfg=cls.result['candidate_fit_all_401']
        off=cls.cfg['offering_snapshot'];cls.design=offering.Design(off['local_contexts']);cls.beta=np.array(off['coefficients']);cls.layer=weighted.Layer(cls.design,cls.beta);cls.params=np.array(cls.cfg['parameters'])

    def test_scoped_reconciliation_and_preservation(self):
        before=deepcopy((self.parent,self.round));rows,audit,unresolved=r.build_evidence(self.parent,self.round)
        self.assertEqual((self.parent,self.round),before);self.assertEqual(rows,self.rows)
        self.assertEqual(Counter(x['winner'] for x in rows),{'A':177,'B':83,'tie':137,'practical_similarity':4})
        updated={a['id'] for a in audit};self.assertEqual(updated,{'round7-13','round7-14','round7-16','round7-17','round31-2'})
        for old,new in zip(self.parent['rows'],rows):
            self.assertEqual(old['id'],new['id'])
            if old['id'] not in updated:
                stripped={k:v for k,v in new.items() if k not in ('judgment_type','direction')};self.assertEqual(stripped,old)
            if new['winner']=='practical_similarity':
                self.assertIsNone(new['direction']);self.assertEqual(new['judgment_type'],'practical_similarity')
                self.assertIn('prior_row',new['semantic_reconciliation'])
        self.assertEqual({x['id'] for x in unresolved},{'round27-7','round27-11'})
        self.assertTrue(all(x['judgment_type']=='unresolved' and x['winner'] is None for x in unresolved))
        self.assertFalse({x['id'] for x in unresolved}&{x['id'] for x in rows})
        self.assertEqual(len({frozenset((tuple(x['a']),tuple(x['b']))) for x in rows}),401)
        bad=deepcopy(self.round);bad['semantic_clarification']['selected_meaning']='exact equality'
        with self.assertRaises(ValueError):r.build_evidence(self.parent,bad)

    def test_historical_hashes(self):
        for f,h in self.result['method']['historical_file_hashes'].items():self.assertEqual(hashlib.sha256((r.ROOT/f).read_bytes()).hexdigest(),h,f)
        self.assertEqual(hashlib.sha256((r.ROOT/'evidence-v11.json').read_bytes()).hexdigest(),self.result['method']['evidence_sha256'])

    def test_distinct_similarity_loss_and_hard_constraints(self):
        x=np.eye(2);beta=np.array([.1,-.1]);gram=np.zeros((2,2));sim=np.array([2,2]);exact=np.array([0,0])
        value,grad=semantic.offering_objective(beta,x,sim,gram,0,.2)
        self.assertAlmostEqual(value,0);np.testing.assert_allclose(grad,0,atol=1e-12)
        exact_value,_=semantic.offering_objective(beta,x,exact,gram,0,.2);self.assertGreater(exact_value,0)
        value,_=semantic.offering_objective(np.array([.3,-.3]),x,sim,gram,0,.2);self.assertAlmostEqual(value,.02)
        example=deepcopy(next(q for q in self.rows if q['winner']=='tie' and q['a'][:3]==q['b'][:3] and q['a'][3]!=q['b'][3]))
        design=offering.Design.from_training([example]);self.assertTrue(np.any(design.fixed_steps([example])))
        example['winner']='practical_similarity';self.assertFalse(np.any(design.fixed_steps([example])))

    def test_semantic_metrics_do_not_merge_labels(self):
        y=np.array([1,0,2,2]);m=np.array([.1,.1,.1,0.])
        scores=semantic.assess(y,m,.2)
        self.assertEqual(scores['matched'],3)
        self.assertEqual(scores['recall'],{'strict_direction':1.,'exact_equality':0.,'practical_similarity':1.})
        self.assertEqual(semantic.operational_metrics(y,m,.2)['n'],2)
        with self.assertRaises(KeyError):semantic.arrays([{'winner':None}])

    def test_objective_gradients_and_legacy_equivalence(self):
        y,_=semantic.arrays(self.rows);x=self.design.array(self.rows);pen=self.design.penalty(1.);gram=pen.T@pen
        rng=np.random.default_rng(47);beta=self.beta+rng.normal(0,.01,len(self.beta))
        fn=lambda p:semantic.offering_objective(p,x,y,gram,.1,.2)
        _,grad=fn(beta)
        for i in [0,8,9,16,17,len(beta)-1]:
            delta=np.zeros(len(beta));delta[i]=1e-6;numeric=(fn(beta+delta)[0]-fn(beta-delta)[0])/2e-6
            self.assertAlmostEqual(numeric,grad[i],delta=2e-5)
        x,offset=self.layer.array(self.rows);params=self.params+rng.normal(0,.01,33)
        fn=lambda p:semantic.layer_objective(p,x,offset,y,self.layer,1.,.2)
        _,grad=fn(params)
        for i in range(33):
            delta=np.zeros(33);delta[i]=1e-6;numeric=(fn(params+delta)[0]-fn(params-delta)[0])/2e-6
            self.assertAlmostEqual(numeric,grad[i],delta=2e-5)
        mask=y!=2;a=semantic.layer_objective(params,x[mask],offset[mask],y[mask],self.layer,1.,.2);b=weighted.objective(params,x[mask],offset[mask],y[mask],self.layer,1.)
        self.assertEqual(a[0],b[0]);np.testing.assert_array_equal(a[1],b[1])

    def test_graph_semantics(self):
        self.assertEqual(set(r.consistency_audit(self.parent['rows'])['strict_edges_in_equality_or_preference_cycles']),{'round7-14','round7-16'})
        self.assertEqual(r.consistency_audit(self.rows)['strict_edges_in_equality_or_preference_cycles'],[])

    def test_folds_baseline_reproduction_and_training_scope(self):
        y,g=semantic.arrays(self.rows);old=json.loads((r.ROOT/'weighted-hierarchy-comparison-v10.json').read_text())
        for seed in prior.SEEDS:
            for fold,(tr,te) in enumerate(old_protocol.extended_folds(g[:366],g,seed)):
                self.assertFalse(set(g[tr])&set(g[te]))
                audit=next(a for a in self.result['nested_cv']['fold_audits'] if a['seed']==seed and a['fold']==fold)
                training=[self.rows[i] for i in tr]
                self.assertEqual(dict(Counter(q['winner'] for q in training)),audit['train_label_counts'])
                expected={tuple(q['a'][:3]) for q in training if q['a'][:3]==q['b'][:3] and q['a'][3]!=q['b'][3]}
                self.assertEqual({tuple(c) for c in audit['local_contexts']},expected)
                self.assertTrue(all(next(q for q in training if q['id']==ident)['winner']=='tie' for ident in audit['hard_tare_tie_ids']))
                for it,iv in base.folds(g[tr],3,seed+fold+7000):self.assertFalse(set(g[tr][it])&set(g[tr][iv]))
            control=next(v for v in self.result['nested_cv']['runs']['v10_evidence_control'] if v['seed']==seed);m=np.array(control['margins']);radius=np.array(control['similarity_radii'])
            pred=np.where(m>radius+1e-8,1,np.where(m<-radius-1e-8,-1,0))
            oldrun=next(v for v in old['nested_cv']['runs']['v10_evidence_candidate'] if v['seed']==seed)
            np.testing.assert_array_equal(pred,oldrun['predictions'])

    def test_full_grid_constraints_and_tare_equalities(self):
        for z,s,a,w in product(base.ZONES,base.SHADES,base.AGES,tare.WEIGHTS):
            value=self.layer.score([z,s,a,w],self.params)
            if a>20:self.assertGreaterEqual(self.layer.score([z,s,a-5,w],self.params)+2e-6,value)
            if s!='pale/straw':self.assertGreaterEqual(self.layer.score([z,base.SHADES[base.SHADES.index(s)+1],a,w],self.params)+2e-6,value)
            if w>110:self.assertGreaterEqual(self.layer.score([z,s,a,w-5],self.params)+2e-6,value)
        m=semantic.margins(self.rows,self.layer,self.params);mask=np.array([q['winner']=='tie' and q['a'][:3]==q['b'][:3] and q['a'][3]!=q['b'][3] for q in self.rows])
        self.assertEqual(int(sum(mask)),27);np.testing.assert_allclose(m[mask],0,atol=1e-7)

    def test_reported_metrics(self):
        y,_=semantic.arrays(self.rows)
        for runs in self.result['nested_cv']['runs'].values():
            for run in runs:
                m=np.array(run['margins']);radius=np.array(run['similarity_radii'])
                self.assertEqual(semantic.assess(y,m,radius),run['semantic_metrics'])
                self.assertEqual(semantic.operational_metrics(y,m,radius),run['legacy_band_diagnostic'])
        m=semantic.margins(self.rows,self.layer,self.params)
        self.assertEqual(semantic.assess(y,m,self.cfg['similarity_radius']),self.cfg['semantic_training_metrics'])

if __name__=='__main__':unittest.main()
