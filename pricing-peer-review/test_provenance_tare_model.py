import hashlib
import json
from itertools import product
import unittest
import numpy as np
import compare_models as base
import compare_interactions as common
import compare_tare_models as shared
import provenance_tare_model as model


class ProvenanceScopeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows=json.loads((model.ROOT/'evidence-v7.json').read_text())['rows']
        cls.result=json.loads((model.ROOT/'provenance-tare-comparison.json').read_text())
        cls.cfg=cls.result['candidate_fit_all_310']
        cls.design=model.Design(cls.cfg['local_contexts']);cls.beta=np.array(cls.cfg['coefficients'])

    def test_equality_bound_does_not_escape_provenance(self):
        fixed=self.design.fixed_steps(self.rows)
        we=self.design.local_index[('Western Europe','copper',35)]
        se=self.design.local_index[('southeast','copper',35)]
        step=1 # 125 -> 120
        self.assertTrue(fixed[we+step])
        self.assertFalse(fixed[se+step])
        self.assertFalse(np.any(fixed[:117]))
        self.assertEqual(self.cfg['forced_strict_preference_ids'],[])

    def test_exact_reported_regression(self):
        threshold=self.cfg['threshold']
        by_id={r['id']:r for r in self.rows}
        self.assertEqual(by_id['round14-2']['winner'],'B')
        self.assertEqual(by_id['round21-12']['winner'],'tie')
        se=self.design.array([by_id['round14-2']])@self.beta
        we=self.design.array([by_id['round21-12']])@self.beta
        self.assertLess(se[0],-threshold)
        self.assertAlmostEqual(we[0],0,places=7)
        pure=shared.masks(self.rows)['confirmed_pure_tare_ties']
        np.testing.assert_allclose((self.design.array(self.rows)@self.beta)[pure],0,atol=1e-7)

    def test_shared_curve_reduction(self):
        rng=np.random.default_rng(32);shared_beta=rng.normal(size=117)
        expanded=np.r_[shared_beta,np.zeros(self.design.n-117)]
        for (zone,shade,age),start in self.design.local_index.items():
            k=17+4*shared.CONTEXTS.index((shade,age));expanded[start:start+4]=shared_beta[k:k+4]
        self.assertAlmostEqual(np.linalg.norm(self.design.penalty(10)@expanded)**2,
                               np.linalg.norm(shared.penalty('context_steps',10)@shared_beta)**2)
        for option in product(base.ZONES,base.SHADES,base.AGES,shared.WEIGHTS):
            self.assertAlmostEqual(self.design.features(option)@expanded,shared.features(option,'context_steps')@shared_beta)

    def test_training_only_local_contexts_and_fixed_settings(self):
        _,_,groups=common.get_arrays(self.rows,'additive')
        audits={(a['seed'],a['fold']):a for a in self.result['nested_cv']['fold_audits']}
        old=json.loads((model.ROOT/'contextual-comparison-v7.json').read_text())
        settings={(s['seed'],s['fold']):s for s in old['nested_cv']['selections'] if s['model']=='v7_evidence_candidate'}
        for seed in common.SEEDS:
            coverage=np.zeros(len(self.rows))
            for fold,(tr,te) in enumerate(base.folds(groups,5,seed)):
                coverage[te]+=1;self.assertFalse(set(groups[tr])&set(groups[te]))
                train=[self.rows[i] for i in tr]
                expected={tuple(r['a'][:3]) for r in train if r['a'][:3]==r['b'][:3] and r['a'][3]!=r['b'][3]}
                audit=audits[(seed,fold)]
                self.assertEqual(set(tuple(x) for x in audit['local_contexts']),expected)
                for k in ('alpha','pooling','threshold'):self.assertEqual(audit[k],settings[(seed,fold)][k])
            np.testing.assert_array_equal(coverage,np.ones(len(self.rows)))

    def test_full_grid_monotonicity_symmetry_and_metrics(self):
        for z,s,age,w in product(base.ZONES,base.SHADES,base.AGES,shared.WEIGHTS):
            score=self.design.features([z,s,age,w])@self.beta
            if w>110:self.assertGreaterEqual(self.design.features([z,s,age,w-5])@self.beta+1e-6,score)
            if age>20:self.assertGreaterEqual(self.design.features([z,s,age-5,w])@self.beta+1e-6,score)
            if s!='pale/straw':self.assertGreaterEqual(self.design.features([z,base.SHADES[base.SHADES.index(s)+1],age,w])@self.beta+1e-6,score)
        x=self.design.array(self.rows);y=np.array([base.LABEL[r['winner']] for r in self.rows])
        np.testing.assert_array_equal(base.classify(-x@self.beta,self.cfg['threshold']),-base.classify(x@self.beta,self.cfg['threshold']))
        self.assertEqual(base.metrics(y,base.classify(x@self.beta,self.cfg['threshold']))['matched'],self.cfg['in_sample']['matched'])
        for run in self.result['nested_cv']['runs']:
            self.assertEqual(base.metrics(y,np.array(run['predictions']))['matched'],run['metrics']['all']['matched'])

    def test_historical_artifacts_unchanged(self):
        for f,h in self.result['method']['historical_file_hashes'].items():
            self.assertEqual(hashlib.sha256((model.ROOT/f).read_bytes()).hexdigest(),h,f)


if __name__=='__main__':unittest.main()
