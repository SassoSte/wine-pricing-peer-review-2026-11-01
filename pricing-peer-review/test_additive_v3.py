from collections import Counter
from copy import deepcopy
import hashlib
import json
from itertools import product
import unittest
import numpy as np
import compare_models as base
import compare_interactions as models
import refit_additive_v3 as r


class EvidenceV3Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.v2=json.loads((r.ROOT/'evidence-v2.json').read_text())
        cls.r13=json.loads((r.ROOT/'round13-fixed.json').read_text())
        cls.r14=json.loads((r.ROOT/'round14-isolation.json').read_text())
        cls.evidence=json.loads((r.ROOT/'evidence-v3.json').read_text())
        cls.results=json.loads((r.ROOT/'additive-comparison-v3.json').read_text())

    def test_counts_corrections_and_no_duplicates(self):
        originals=deepcopy((self.v2,self.r13,self.r14))
        rows,audit=r.build_evidence(self.v2,self.r13,self.r14)
        self.assertEqual((self.v2,self.r13,self.r14),originals)
        self.assertEqual(rows,self.evidence['rows'])
        self.assertEqual(len(rows),183)
        self.assertEqual(Counter(a['action'] for a in audit),{'new comparison':19,'new component comparison':6,'correction':1,'confirmation':2})
        self.assertEqual(rows[:158],self.v2['rows'])
        by_id={x['id']:x for x in rows}
        self.assertEqual(by_id['round13-6']['winner'],'B')
        self.assertEqual(by_id['round13-6']['current_answer_source'],'round14-3')
        self.assertNotIn('round13-14',by_id)
        for q in ('round14-3','round14-6','round14-9'):self.assertNotIn(q,by_id)
        self.assertEqual(Counter(x['winner'] for x in rows),{'A':83,'B':50,'tie':50})
        self.assertEqual(len({frozenset((tuple(x['a']),tuple(x['b']))) for x in rows}),183)

    def test_reject_unapproved_correction(self):
        bad=deepcopy(self.r14);bad['evidence_overrides']=[]
        with self.assertRaises(ValueError):r.build_evidence(self.v2,self.r13,bad)

    def test_saved_baselines_and_evidence_unchanged(self):
        for f,h in self.results['method']['historical_file_hashes'].items():
            self.assertEqual(hashlib.sha256((r.ROOT/f).read_bytes()).hexdigest(),h,f)
        self.assertEqual(hashlib.sha256((r.ROOT/'evidence-v3.json').read_bytes()).hexdigest(),self.results['method']['evidence_sha256'])

    def test_matched_family_evaluation_and_metrics(self):
        rows=self.evidence['rows'];_,y,g=models.get_arrays(rows,'additive')
        old_mask=np.arange(len(rows))<158
        for seed in models.SEEDS:
            coverage=np.zeros(len(y))
            for train,test in base.folds(g,5,seed):
                coverage[test]+=1
                for tr in (train,train[old_mask[train]]):
                    self.assertFalse(set(g[tr])&set(g[test]))
                    for it,iv in base.folds(g[tr],3,seed):self.assertFalse(set(g[tr][it])&set(g[tr][iv]))
            np.testing.assert_array_equal(coverage,np.ones(len(y)))
        for runs in self.results['nested_cv']['runs'].values():
            for run in runs:
                actual=base.metrics(y,np.array(run['predictions']))
                self.assertEqual(actual['matched'],run['metrics']['all']['matched'])
                self.assertAlmostEqual(actual['balanced_accuracy'],run['metrics']['all']['balanced_accuracy'])

    def test_candidate_symmetry_monotonicity_and_fit(self):
        cfg=self.results['candidate_fit_all_183'];beta=np.array(cfg['coefficients'])
        x,y,_=models.get_arrays(self.evidence['rows'],'additive')
        self.assertEqual(base.metrics(y,base.classify(x@beta,cfg['threshold']))['matched'],cfg['in_sample']['matched'])
        np.testing.assert_array_equal(base.classify(-x@beta,cfg['threshold']),-base.classify(x@beta,cfg['threshold']))
        for z,s,age,w in product(base.ZONES,base.SHADES,base.AGES,(110,115,120,125,130)):
            value=base.features([z,s,age,w])@beta
            if w>110:self.assertGreaterEqual(base.features([z,s,age,w-5])@beta+1e-8,value)
            if age>20:self.assertGreaterEqual(base.features([z,s,age-5,w])@beta+1e-8,value)
            if s!='pale/straw':self.assertGreaterEqual(base.features([z,base.SHADES[base.SHADES.index(s)+1],age,w])@beta+1e-8,value)


if __name__=='__main__':unittest.main()
