import hashlib
import json
from itertools import product
import unittest
import numpy as np
from scipy.optimize import check_grad
import compare_models as b
import compare_tare_models as t
import provenance_tare_model as p
import refit_provenance_v8 as protocol
import domestic_hierarchy_model as h


class HierarchyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result=json.loads((h.ROOT/'domestic-hierarchy-comparison.json').read_text())
        cls.rows=json.loads((h.ROOT/'evidence-v8.json').read_text())['rows']
        cls.cfg=cls.result['candidate_fit_all_341'];off=cls.cfg['offering_snapshot']
        cls.design=p.Design(off['local_contexts']);cls.beta=np.array(off['coefficients'])
        cls.layer=h.RegionalLayer(cls.design,cls.beta);cls.params=np.array(cls.cfg['regional_parameters'])

    def test_baselines_and_data_unchanged(self):
        for f,digest in self.result['method']['historical_file_hashes'].items():
            self.assertEqual(hashlib.sha256((h.ROOT/f).read_bytes()).hexdigest(),digest,f)
        self.assertEqual(len(self.rows),341)
        self.assertEqual(len(self.layer.prior_pairs),30)

    def test_original_offering_recovered_and_foreign_unchanged(self):
        for option in product(b.ZONES,b.SHADES,b.AGES,t.WEIGHTS):
            original=self.design.features(option)@self.beta
            self.assertAlmostEqual(self.layer.score(option,self.layer.initial),original)
            if option[0] not in h.DOMESTIC:self.assertAlmostEqual(self.layer.score(option,self.params),original)

    def test_template_soft_residual_and_convergence(self):
        params=np.r_[np.zeros(5),np.full(25,.1)]
        values={z:h.regional_features([z,'amber',30,120])@params for z in h.DOMESTIC}
        self.assertGreater(values['northeast'],values['southwest'])
        self.assertEqual(values['southwest'],values['southeast'])
        self.assertGreater(values['southeast'],values['central'])
        self.assertEqual(values['central'],values['northwest'])
        # A zero gain can remove that hierarchy premium, without requiring it
        # at other contexts; residuals permit evidence-based exceptions.
        params[5+h.CONTEXTS.index(('amber',20))]=0
        self.assertEqual(len({h.regional_features([z,'amber',20,120])@params for z in h.DOMESTIC}),1)
        params[h.DOMESTIC.index('central')]=1
        self.assertGreater(h.regional_features(['central','amber',30,120])@params,values['northeast'])

    def test_gradient(self):
        rows=self.rows[:30];x,offset=self.layer.array(rows);y=np.array([b.LABEL[r['winner']] for r in rows])
        rng=np.random.default_rng(9);params=self.layer.initial+rng.uniform(.01,.05,size=30)
        error=check_grad(lambda q:h.objective(q,x,offset,y,self.layer,1.)[0],lambda q:h.objective(q,x,offset,y,self.layer,1.)[1],params)
        self.assertLess(error,1e-4)

    def test_tare_differences_symmetry_and_full_grid(self):
        for z,s,age in product(b.ZONES,b.SHADES,b.AGES):
            for wa,wb in zip(t.WEIGHTS,t.WEIGHTS[1:]):
                old=(self.design.features([z,s,age,wa])-self.design.features([z,s,age,wb]))@self.beta
                new=self.layer.score([z,s,age,wa],self.params)-self.layer.score([z,s,age,wb],self.params)
                self.assertAlmostEqual(old,new)
        for z,s,age,w in product(b.ZONES,b.SHADES,b.AGES,t.WEIGHTS):
            value=self.layer.score([z,s,age,w],self.params)
            if age>20:self.assertGreaterEqual(self.layer.score([z,s,age-5,w],self.params)+2e-6,value)
            if s!='pale/straw':self.assertGreaterEqual(self.layer.score([z,b.SHADES[b.SHADES.index(s)+1],age,w],self.params)+2e-6,value)
        x,o=self.layer.array(self.rows);margin=o+x@self.params
        np.testing.assert_array_equal(b.classify(-margin,self.cfg['threshold']),-b.classify(margin,self.cfg['threshold']))

    def test_fold_groups_baseline_reconstruction_and_metrics(self):
        old=json.loads((h.ROOT/'provenance-comparison-v8.json').read_text())
        _,y,g=protocol.common.get_arrays(self.rows,'additive')
        for run,prior in zip(self.result['nested_cv']['runs']['current_v8'],old['nested_cv']['runs']['v8_evidence_candidate']):
            self.assertEqual(run['seed'],prior['seed']);self.assertEqual(run['predictions'],prior['predictions'])
        for seed in h.SEEDS:
            for fold,(tr,te) in enumerate(protocol.extended_folds(g[:310],g,seed)):
                self.assertFalse(set(g[tr])&set(g[te]))
                for it,iv in b.folds(g[tr],3,seed+fold+7000):self.assertFalse(set(g[tr][it])&set(g[tr][iv]))
        for runs in self.result['nested_cv']['runs'].values():
            for run in runs:self.assertEqual(b.metrics(y,np.array(run['predictions']))['matched'],run['metrics']['all']['matched'])


if __name__=='__main__':unittest.main()
