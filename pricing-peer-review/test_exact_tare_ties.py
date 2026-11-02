import hashlib
import json
from itertools import product
import unittest
import numpy as np
import compare_models as b
import compare_interactions as common
import compare_tare_models as soft
import compare_exact_tare_ties as hard


class ExactTareTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result=json.loads((hard.ROOT/'exact-tare-comparison.json').read_text())
        cls.rows=json.loads((hard.ROOT/'evidence-v6.json').read_text())['rows']
        cls.x,cls.y,cls.g=soft.arrays(cls.rows,'context_steps')

    def test_baselines_unchanged(self):
        for f,h in self.result['method']['preserved_file_hashes'].items():
            self.assertEqual(hashlib.sha256((hard.ROOT/f).read_bytes()).hexdigest(),h,f)

    def test_only_training_tare_ties_fix_steps(self):
        x=np.array([soft.features(['southwest','brown',40,120],'context_steps')-soft.features(['southwest','brown',40,125],'context_steps')])
        self.assertEqual(sum(hard.fixed_steps(x,np.array([0]))),1)
        self.assertEqual(sum(hard.fixed_steps(x,np.array([1]))),0)
        different=np.array([soft.features(['southwest','brown',40,120],'context_steps')-soft.features(['central','brown',40,125],'context_steps')])
        self.assertEqual(sum(hard.fixed_steps(different,np.array([0]))),0)
        configs={(c['seed'],c['fold']):c for c in self.result['nested_cv']['selections']}
        for seed in common.SEEDS:
            for fold,(tr,te) in enumerate(b.folds(self.g,5,seed)):
                self.assertFalse(set(self.g[tr])&set(self.g[te]))
                self.assertEqual(sum(hard.fixed_steps(self.x[tr],self.y[tr])),configs[(seed,fold)]['fixed_step_count'])

    def test_confirmed_tare_ties_have_exact_scores(self):
        cfg=self.result['candidate_fit_all_281'];beta=np.array(cfg['coefficients'])
        pure=soft.masks(self.rows)['confirmed_pure_tare_ties']
        self.assertEqual(sum(pure),7)
        np.testing.assert_allclose(self.x[pure]@beta,0,atol=1e-7)
        self.assertEqual(np.flatnonzero(hard.fixed_steps(self.x,self.y)).tolist(),cfg['fixed_step_indices'])
        self.assertEqual(b.metrics(self.y,b.classify(self.x@beta,cfg['threshold']))['matched'],cfg['in_sample']['matched'])

    def test_full_offering_monotonicity_and_symmetry(self):
        cfg=self.result['candidate_fit_all_281'];beta=np.array(cfg['coefficients'])
        for z,s,age,w in product(b.ZONES,b.SHADES,b.AGES,soft.WEIGHTS):
            score=soft.features([z,s,age,w],'context_steps')@beta
            if w>110:self.assertGreaterEqual(soft.features([z,s,age,w-5],'context_steps')@beta+1e-6,score)
            if age>20:self.assertGreaterEqual(soft.features([z,s,age-5,w],'context_steps')@beta+1e-6,score)
            if s!='pale/straw':self.assertGreaterEqual(soft.features([z,b.SHADES[b.SHADES.index(s)+1],age,w],'context_steps')@beta+1e-6,score)
        np.testing.assert_array_equal(b.classify(-self.x@beta,cfg['threshold']),-b.classify(self.x@beta,cfg['threshold']))

    def test_metrics(self):
        for run in self.result['nested_cv']['runs']:
            actual=b.metrics(self.y,np.array(run['predictions']))
            self.assertEqual(actual['matched'],run['metrics']['all']['matched'])
            self.assertAlmostEqual(actual['balanced_accuracy'],run['metrics']['all']['balanced_accuracy'])


if __name__=='__main__':unittest.main()
