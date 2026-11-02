import hashlib
import json
import unittest
from itertools import product
import numpy as np
from scipy.optimize import check_grad
import compare_models as b
import compare_interactions as m
import compare_objectives as c


class ObjectiveTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result=json.loads((c.ROOT/'objective-comparison.json').read_text())
        cls.rows=m.load_rows()

    def test_gradient(self):
        rng=np.random.default_rng(42)
        x=rng.normal(size=(12,18));y=np.array([-1,0,1]*4);beta=rng.normal(size=18)*.1
        gram=np.eye(18)
        err=check_grad(lambda z:c.objective(z,x,y,gram,.3)[0],
                       lambda z:c.objective(z,x,y,gram,.3)[1],beta)
        self.assertLess(err,2e-5)

    def test_ranking_and_tie_semantics(self):
        x=np.ones((1,1));gram=np.zeros((1,1))
        for margin in (1.,2.,10.):
            loss,grad=c.objective(np.array([margin]),x,np.array([1]),gram,0)
            self.assertEqual(loss,0);self.assertEqual(grad[0],0)
        self.assertGreater(c.objective(np.array([-1.]),x,np.array([1]),gram,0)[0],0)
        self.assertEqual(c.objective(np.array([0.]),x,np.array([0]),gram,0)[0],0)
        self.assertGreater(c.objective(np.array([.1]),x,np.array([0]),gram,0)[0],0)

    def test_hard_feasibility_and_feature_collision(self):
        x=np.zeros((2,18));x[:,0]=1
        self.assertTrue(c.hard_feasibility(x,np.array([1,1]))['feasible'])
        self.assertFalse(c.hard_feasibility(x,np.array([1,0]))['feasible'])
        for f in m.FAMILIES:
            self.assertFalse(self.result['feasibility'][f]['hard_constraints']['feasible'])
            self.assertTrue(self.result['feasibility'][f]['identical_feature_conflicts'])

    def test_frozen_files(self):
        for f,digest in self.result['method']['preserved_file_hashes'].items():
            self.assertEqual(hashlib.sha256((c.ROOT/f).read_bytes()).hexdigest(),digest,f)

    def test_symmetry_and_full_grid(self):
        for family,cfg in self.result['candidates_fit_all_158'].items():
            beta=np.array(cfg['coefficients']);x,y,g=m.get_arrays(self.rows,family)
            np.testing.assert_array_equal(b.classify(-x@beta,cfg['threshold']),-b.classify(x@beta,cfg['threshold']))
            for z,s,age,w in product(b.ZONES,b.SHADES,b.AGES,(110,115,120,125,130)):
                val=m.features([z,s,age,w],family)@beta
                if w>110:self.assertGreaterEqual(m.features([z,s,age,w-5],family)@beta+1e-8,val)
                if age>20:self.assertGreaterEqual(m.features([z,s,age-5,w],family)@beta+1e-8,val)
                if s!='pale/straw':self.assertGreaterEqual(m.features([z,b.SHADES[b.SHADES.index(s)+1],age,w],family)@beta+1e-8,val)
        x,y,_=m.get_arrays(self.rows,'additive')
        np.testing.assert_allclose(c.fit(x,y,'additive',1,1),c.fit(-x,-y,'additive',1,1),atol=1e-7)

    def test_same_splits_and_metrics(self):
        old=json.loads((c.ROOT/'interaction-comparison.json').read_text())
        self.assertEqual(old['nested_cv']['row_ids'],self.result['nested_cv']['row_ids'])
        _,y,g=m.get_arrays(self.rows,'additive')
        for family,runs in self.result['nested_cv']['runs'].items():
            self.assertEqual([r['seed'] for r in runs],[r['seed'] for r in old['nested_cv']['runs'][family]])
            for run in runs:
                metrics=b.metrics(y,np.array(run['predictions']))
                self.assertEqual(metrics['matched'],run['all']['matched'])
                self.assertAlmostEqual(metrics['balanced_accuracy'],run['all']['balanced_accuracy'])
                for tr,te in b.folds(g,5,run['seed']):
                    self.assertFalse(set(g[tr])&set(g[te]))
                    for it,iv in b.folds(g[tr],3,run['seed']):self.assertFalse(set(g[tr][it])&set(g[tr][iv]))


if __name__=='__main__':unittest.main()
