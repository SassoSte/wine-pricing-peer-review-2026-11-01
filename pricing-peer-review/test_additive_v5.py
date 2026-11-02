from collections import Counter
from copy import deepcopy
import hashlib
import json
from itertools import product
import unittest
import numpy as np
import compare_models as base
import compare_interactions as models
import refit_additive_v5 as r


class EvidenceV5Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.v4=json.loads((r.ROOT/'evidence-v4.json').read_text())
        cls.r17=json.loads((r.ROOT/'round17-fixed.json').read_text())
        cls.r18=json.loads((r.ROOT/'round18-isolation.json').read_text())
        cls.evidence=json.loads((r.ROOT/'evidence-v5.json').read_text())
        cls.results=json.loads((r.ROOT/'additive-comparison-v5.json').read_text())

    def test_accounting_and_confirmation(self):
        original=deepcopy((self.v4,self.r17,self.r18))
        rows,audit=r.build_evidence(self.v4,self.r17,self.r18)
        self.assertEqual((self.v4,self.r17,self.r18),original)
        self.assertEqual(rows,self.evidence['rows'])
        self.assertEqual(rows[:224],self.v4['rows'])
        self.assertEqual(len(rows),252)
        self.assertEqual(Counter(a['action'] for a in audit),{'new comparison':20,'new component comparison':8,'confirmation':1})
        self.assertEqual(Counter(x['winner'] for x in rows),{'A':112,'B':62,'tie':78})
        self.assertEqual(len({r['id'] for r in rows}),252)
        self.assertEqual(len({frozenset((tuple(x['a']),tuple(x['b']))) for x in rows}),252)
        self.assertNotIn('round18-3',[r['id'] for r in rows])
        target=next(r for r in rows if r['id']=='round17-3')
        self.assertEqual(target['winner'],'tie')
        self.assertEqual(target['clarification_history'][-1]['clarification_id'],'round18-3')

    def test_unexpected_correction_rejected(self):
        bad=deepcopy(self.r18)
        next(q for q in bad['questions'] if q['id']=='round18-3')['winner']='A'
        with self.assertRaises(ValueError):r.build_evidence(self.v4,self.r17,bad)

    def test_immutable_history_and_frozen_scores(self):
        for f,h in self.results['method']['historical_file_hashes'].items():
            self.assertEqual(hashlib.sha256((r.ROOT/f).read_bytes()).hexdigest(),h,f)
        self.assertEqual(hashlib.sha256((r.ROOT/'evidence-v5.json').read_bytes()).hexdigest(),self.results['method']['evidence_sha256'])
        rescored=self.results['unchanged_baseline_rescoring']
        self.assertEqual(rescored['revision_e']['round17_original_answers']['matched'],self.r17['scores']['revision_e']['matched'])
        self.assertEqual(rescored['frozen_v4_additive']['round17_original_answers']['matched'],self.r17['scores']['additive_v4']['matched'])

    def test_family_split_isolation_and_metrics(self):
        rows=self.evidence['rows'];_,y,g=models.get_arrays(rows,'additive');old=np.arange(len(rows))<224
        for seed in models.SEEDS:
            count=np.zeros(len(rows))
            for train,test in base.folds(g,5,seed):
                count[test]+=1
                for tr in (train,train[old[train]]):
                    self.assertFalse(set(g[tr])&set(g[test]))
                    for it,iv in base.folds(g[tr],3,seed):self.assertFalse(set(g[tr][it])&set(g[tr][iv]))
            np.testing.assert_array_equal(count,np.ones(len(rows)))
        for runs in self.results['nested_cv']['runs'].values():
            for run in runs:
                metric=base.metrics(y,np.array(run['predictions']))
                self.assertEqual(metric['matched'],run['metrics']['all']['matched'])
                self.assertAlmostEqual(metric['balanced_accuracy'],run['metrics']['all']['balanced_accuracy'])

    def test_candidate_fit_symmetry_and_weak_monotonicity(self):
        cfg=self.results['candidate_fit_all_252'];beta=np.array(cfg['coefficients'])
        x,y,_=models.get_arrays(self.evidence['rows'],'additive')
        self.assertEqual(base.metrics(y,base.classify(x@beta,cfg['threshold']))['matched'],cfg['in_sample']['matched'])
        np.testing.assert_array_equal(base.classify(-x@beta,cfg['threshold']),-base.classify(x@beta,cfg['threshold']))
        for z,s,age,w in product(base.ZONES,base.SHADES,base.AGES,(110,115,120,125,130)):
            value=base.features([z,s,age,w])@beta
            if w>110:self.assertGreaterEqual(base.features([z,s,age,w-5])@beta+1e-8,value)
            if age>20:self.assertGreaterEqual(base.features([z,s,age-5,w])@beta+1e-8,value)
            if s!='pale/straw':self.assertGreaterEqual(base.features([z,base.SHADES[base.SHADES.index(s)+1],age,w])@beta+1e-8,value)


if __name__=='__main__':unittest.main()
