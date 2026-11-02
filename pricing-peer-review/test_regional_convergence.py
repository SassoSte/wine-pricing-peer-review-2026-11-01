import hashlib,json,unittest
from pathlib import Path
from itertools import product
import numpy as np
import compare_models as base
import compare_tare_models as tare
import provenance_tare_model as offering
import domestic_hierarchy_model as prior
import weighted_domestic_model as baseline
import regional_convergence_model as candidate
import compare_regional_convergence as run
import refit_weighted_v10 as protocol

class RegionalConvergenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.evidence=json.loads((run.ROOT/'evidence-v10.json').read_text());cls.rows=cls.evidence['rows']
        cls.result=json.loads((run.ROOT/'regional-convergence-comparison-v10.json').read_text());cls.cfg=cls.result['candidate_fit_all_401']
        off=cls.cfg['offering_snapshot'];cls.design=offering.Design(off['local_contexts']);cls.beta=np.array(off['coefficients']);cls.layer=candidate.Layer(cls.design,cls.beta);cls.params=np.array(cls.cfg['parameters'])

    def test_historical_hashes_and_unresolved_exclusion(self):
        for f,h in self.result['method']['historical_file_hashes'].items():self.assertEqual(hashlib.sha256((run.ROOT/f).read_bytes()).hexdigest(),h,f)
        self.assertEqual({r['id'] for r in self.evidence['unresolved_pairs']},{'round27-7','round27-11'})
        self.assertFalse({'round27-7','round27-11'}&{r['id'] for r in self.rows})
        self.assertEqual(len(self.rows),401)

    def test_family_isolation_and_baseline_reproduction(self):
        _,y,g=baseline.protocol.common.get_arrays(self.rows,'additive')
        old=json.loads((run.ROOT/'weighted-hierarchy-comparison-v10.json').read_text())
        self.assertEqual(self.result['nested_cv']['row_ids'],old['nested_cv']['row_ids'])
        for seed in prior.SEEDS:
            count=np.zeros(len(y))
            for fold,(tr,te) in enumerate(protocol.extended_folds(g[:366],g,seed)):
                count[te]+=1;self.assertFalse(set(g[tr])&set(g[te]))
                expected={tuple(self.rows[i]['a'][:3]) for i in tr if self.rows[i]['a'][:3]==self.rows[i]['b'][:3] and self.rows[i]['a'][3]!=self.rows[i]['b'][3]}
                audit=next(a for a in self.result['nested_cv']['fold_audits'] if a['seed']==seed and a['fold']==fold)
                self.assertEqual({tuple(c) for c in audit['local_contexts']},expected)
                for it,iv in base.folds(g[tr],3,seed+fold+7000):self.assertFalse(set(g[tr][it])&set(g[tr][iv]))
            np.testing.assert_array_equal(count,np.ones(len(y)))
            actual=next(r for r in self.result['nested_cv']['runs']['v10_baseline'] if r['seed']==seed)
            original=next(r for r in old['nested_cv']['runs']['v10_evidence_candidate'] if r['seed']==seed)
            self.assertEqual(actual['predictions'],original['predictions'])

    def test_objective_gradient(self):
        rng=np.random.default_rng(52);v=np.r_[self.layer.initial,abs(self.layer.d@self.layer.initial)]+rng.normal(0,.02,candidate.N+len(self.layer.d))
        rows=self.rows[:35];x,offset=self.layer.array(rows);y=np.array([base.LABEL[r['winner']] for r in rows]);value,gradient=candidate.objective(v,x,offset,y,self.layer,1.)
        self.assertTrue(np.isfinite(value))
        for index in [0,1,4,18,52,99,100,101,102,103,104,len(v)-1]:
            delta=np.zeros(len(v));delta[index]=1e-6
            numeric=(candidate.objective(v+delta,x,offset,y,self.layer,1.)[0]-candidate.objective(v-delta,x,offset,y,self.layer,1.)[0])/2e-6
            self.assertAlmostEqual(numeric,gradient[index],delta=2e-5)

    def test_qp_matches_reference_optimizer(self):
        qp=candidate.fit(self.rows,self.layer,1.)
        reference=candidate.fit_slsqp(self.rows,self.layer,1.)
        x,offset=self.layer.array(self.rows);y=np.array([base.LABEL[r['winner']] for r in self.rows])
        def value(p):return candidate.objective(np.r_[p,abs(self.layer.d@p)],x,offset,y,self.layer,1.)[0]
        self.assertAlmostEqual(value(qp),value(reference),delta=1e-4)
        np.testing.assert_array_equal(candidate.predict(self.rows,self.layer,qp,.2),candidate.predict(self.rows,self.layer,reference,.2))

    def test_full_grid_monotonicity_and_foreign_invariance(self):
        for z,s,age,w in product(base.ZONES,base.SHADES,base.AGES,tare.WEIGHTS):
            value=self.layer.score([z,s,age,w],self.params)
            if z not in prior.DOMESTIC:self.assertAlmostEqual(value,self.design.features([z,s,age,w])@self.beta)
            if age>20:self.assertGreaterEqual(self.layer.score([z,s,age-5,w],self.params)+2e-6,value)
            if s!='pale/straw':self.assertGreaterEqual(self.layer.score([z,base.SHADES[base.SHADES.index(s)+1],age,w],self.params)+2e-6,value)
            if w>110:self.assertGreaterEqual(self.layer.score([z,s,age,w-5],self.params)+2e-6,value)

    def test_tare_equalities_and_symmetry(self):
        x,offset=self.layer.array(self.rows);margin=offset+x@self.params;mask=tare.masks(self.rows)['confirmed_pure_tare_ties']
        np.testing.assert_allclose(margin[mask],0,atol=1e-7)
        np.testing.assert_array_equal(base.classify(-margin,self.cfg['threshold']),-base.classify(margin,self.cfg['threshold']))
        old=json.loads((run.ROOT/'weighted-hierarchy-comparison-v10.json').read_text())['candidate_fit_all_401']['offering_snapshot']
        self.assertEqual(old,self.cfg['offering_snapshot'])

    def test_regional_equality_diagnostics(self):
        # Exact fusion diagnostics must match actual complete scores, including tare.
        for d in self.cfg['regional_diagnostics']:
            scores={z:self.layer.score([z,d['shade'],d['vintage'],120],self.params) for z in prior.DOMESTIC}
            self.assertAlmostEqual(max(scores.values())-min(scores.values()),d['spread'])
            for a,b in d['equal_region_pairs']:self.assertLess(abs(scores[a]-scores[b]),1e-7)
        self.assertEqual(self.params.shape,(104,))
        self.assertTrue(np.any(abs(self.layer.d@self.params)<1e-7))

    def test_metrics_and_equality_counts(self):
        _,y,_=baseline.protocol.common.get_arrays(self.rows,'additive');subsets=run.masks(self.rows)
        for runs in self.result['nested_cv']['runs'].values():
            for r in runs:
                for key,mask in subsets.items():self.assertEqual(base.metrics(y[mask],np.array(r['predictions'])[mask]),r['metrics'][key])
        pred=candidate.predict(self.rows,self.layer,self.params,self.cfg['threshold']);self.assertEqual(base.metrics(y,pred),self.cfg['in_sample'])
        x,offset=self.layer.array(self.rows);m=offset+x@self.params
        for key,audit in self.cfg['equality_audits'].items():
            self.assertEqual(audit['n'],int(sum(subsets[key])))
            self.assertEqual(audit['exact_score_equalities'],int(sum(abs(m[subsets[key]])<1e-7)))

if __name__=='__main__':unittest.main()
