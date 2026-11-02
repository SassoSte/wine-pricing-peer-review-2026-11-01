import hashlib
import json
from itertools import product
import unittest
import numpy as np
import compare_models as b
import compare_interactions as old
import compare_tare_models as m


class TareModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result=json.loads((m.ROOT/'tare-model-comparison.json').read_text())
        cls.rows=json.loads((m.ROOT/'evidence-v6.json').read_text())['rows']

    def test_baselines_unchanged(self):
        for f,h in self.result['method']['preserved_file_hashes'].items():
            self.assertEqual(hashlib.sha256((m.ROOT/f).read_bytes()).hexdigest(),h,f)

    def test_linear_and_global_reduction(self):
        rng=np.random.default_rng(13);beta=rng.normal(size=18)
        global_beta=np.r_[beta[:17],np.repeat(beta[-1],4)]
        context_beta=np.r_[beta[:17],np.repeat(beta[-1],100)]
        self.assertAlmostEqual(np.linalg.norm(m.penalty('global_steps',1)@global_beta)**2,np.linalg.norm(beta)**2)
        self.assertAlmostEqual(np.linalg.norm(m.penalty('context_steps',100)@context_beta)**2,np.linalg.norm(beta)**2)
        for option in product(b.ZONES,b.SHADES,b.AGES,m.WEIGHTS):
            expected=b.features(option)@beta
            self.assertAlmostEqual(m.features(option,'global_steps')@global_beta,expected)
            self.assertAlmostEqual(m.features(option,'context_steps')@context_beta,expected)
        arbitrary=rng.normal(size=21)
        expanded=np.r_[arbitrary[:17],np.tile(arbitrary[17:],25)]
        self.assertAlmostEqual(np.linalg.norm(m.penalty('context_steps',100)@expanded)**2,np.linalg.norm(m.penalty('global_steps',1)@arbitrary)**2)

    def test_context_plateau_can_coexist_with_strict_same_weight_step(self):
        beta=np.r_[np.zeros(9),np.full(8,10.),np.ones(100)]
        ctx=m.CONTEXTS.index(('brown',40))
        beta[17+4*ctx+1]=0  # 125 -> 120 lb step only in this context
        def score(shade,age,w):return m.features(['southwest',shade,age,w],'context_steps')@beta
        self.assertAlmostEqual(score('brown',40,120),score('brown',40,125))
        self.assertGreater(score('brown',40,120),score('brown',40,130))
        self.assertGreater(score('copper',35,120),score('copper',35,125))
        self.assertGreaterEqual(np.min(m.CONSTRAINTS['context_steps']@beta),-1e-9)

    def test_saved_baseline_predictions_and_identical_groups(self):
        prior=json.loads((m.ROOT/'additive-comparison-v6.json').read_text())
        self.assertEqual(self.result['nested_cv']['row_ids'],prior['nested_cv']['row_ids'])
        runs=self.result['nested_cv']['runs']['linear_v6']
        for new,oldrun in zip(runs,prior['nested_cv']['runs']['v6_evidence_candidate']):
            self.assertEqual(new['seed'],oldrun['seed'])
            self.assertEqual(new['predictions'],oldrun['predictions'])
        _,y,g=m.arrays(self.rows,'global_steps')
        for seed in old.SEEDS:
            coverage=np.zeros(len(y))
            for tr,te in b.folds(g,5,seed):
                coverage[te]+=1;self.assertFalse(set(g[tr])&set(g[te]))
                for it,iv in b.folds(g[tr],3,seed):self.assertFalse(set(g[tr][it])&set(g[tr][iv]))
            np.testing.assert_array_equal(coverage,np.ones(len(y)))

    def test_full_grid_constraints_symmetry_and_metrics(self):
        _,y,_=m.arrays(self.rows,'global_steps')
        for family,cfg in self.result['candidates_fit_all_281'].items():
            beta=np.array(cfg['coefficients']);self.assertEqual(len(beta),len(m.names(family)))
            for z,s,age,w in product(b.ZONES,b.SHADES,b.AGES,m.WEIGHTS):
                score=m.features([z,s,age,w],family)@beta
                if w>110:self.assertGreaterEqual(m.features([z,s,age,w-5],family)@beta+1e-6,score)
                if age>20:self.assertGreaterEqual(m.features([z,s,age-5,w],family)@beta+1e-6,score)
                if s!='pale/straw':self.assertGreaterEqual(m.features([z,b.SHADES[b.SHADES.index(s)+1],age,w],family)@beta+1e-6,score)
            x,_,_=m.arrays(self.rows,family)
            np.testing.assert_array_equal(b.classify(-x@beta,cfg['threshold']),-b.classify(x@beta,cfg['threshold']))
            self.assertEqual(b.metrics(y,b.classify(x@beta,cfg['threshold']))['matched'],cfg['in_sample']['matched'])
        for runs in self.result['nested_cv']['runs'].values():
            for run in runs:
                self.assertEqual(b.metrics(y,np.array(run['predictions']))['matched'],run['metrics']['all']['matched'])


if __name__=='__main__':unittest.main()
