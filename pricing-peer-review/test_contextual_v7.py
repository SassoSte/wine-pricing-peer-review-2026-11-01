from collections import Counter
from copy import deepcopy
import hashlib
import json
from itertools import product
import unittest
import numpy as np
import compare_models as base
import compare_interactions as common
import compare_tare_models as soft
import compare_exact_tare_ties as hard
import refit_contextual_v7 as r


class ContextV7Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parent=json.loads((r.ROOT/'evidence-v6.json').read_text())
        cls.round21=json.loads((r.ROOT/'round21-fixed.json').read_text())
        cls.round22=json.loads((r.ROOT/'round22-isolation.json').read_text())
        cls.evidence=json.loads((r.ROOT/'evidence-v7.json').read_text())
        cls.result=json.loads((r.ROOT/'contextual-comparison-v7.json').read_text())
        cls.x,cls.y,cls.g=soft.arrays(cls.evidence['rows'],'context_steps')

    def test_accounting_confirmations_and_no_mutation(self):
        original=deepcopy((self.parent,self.round21,self.round22))
        rows,audit=r.build_evidence(self.parent,self.round21,self.round22)
        self.assertEqual((self.parent,self.round21,self.round22),original)
        self.assertEqual(rows,self.evidence['rows'])
        self.assertEqual(rows[:281],self.parent['rows'])
        self.assertEqual(len(rows),310)
        self.assertEqual(Counter(a['action'] for a in audit),{'new comparison':20,'new component comparison':9,'confirmation':1})
        self.assertEqual(Counter(a['winner'] for a in rows),{'A':138,'B':65,'tie':107})
        self.assertEqual(len({frozenset((tuple(q['a']),tuple(q['b']))) for q in rows}),310)
        ids=[q['id'] for q in rows];self.assertNotIn('round22-3',ids)
        self.assertEqual(ids.count('round21-11'),1)
        q=next(q for q in rows if q['id']=='round21-8')
        self.assertEqual(q['clarification_history'][-1]['clarification_id'],'round22-3')

    def test_bad_confirmation_rejected(self):
        bad=deepcopy(self.round22)
        next(q for q in bad['questions'] if q['id']=='round22-3')['winner']='B'
        with self.assertRaises(ValueError):r.build_evidence(self.parent,self.round21,bad)

    def test_baselines_and_scores_preserved(self):
        for f,h in self.result['method']['historical_file_hashes'].items():
            self.assertEqual(hashlib.sha256((r.ROOT/f).read_bytes()).hexdigest(),h,f)
        self.assertEqual(hashlib.sha256((r.ROOT/'evidence-v7.json').read_bytes()).hexdigest(),self.result['method']['evidence_sha256'])
        scores=self.result['unchanged_baseline_rescoring']
        self.assertEqual(scores['frozen_contextual']['round21']['matched'],16)
        self.assertEqual(scores['frozen_additive_v6']['round21']['matched'],11)

    def test_training_only_constraints_and_family_splits(self):
        old=np.arange(len(self.y))<281
        configs={(s['seed'],s['fold'],s['model']):s for s in self.result['nested_cv']['selections']}
        for seed in common.SEEDS:
            count=np.zeros(len(self.y))
            for fold,(train,test) in enumerate(base.folds(self.g,5,seed)):
                count[test]+=1
                for name,tr in [('v6_evidence_control',train[old[train]]),('v7_evidence_candidate',train)]:
                    self.assertFalse(set(self.g[tr])&set(self.g[test]))
                    self.assertEqual(sum(hard.fixed_steps(self.x[tr],self.y[tr])),configs[(seed,fold,name)]['fixed_step_count'])
                    for it,iv in base.folds(self.g[tr],3,seed):self.assertFalse(set(self.g[tr][it])&set(self.g[tr][iv]))
            np.testing.assert_array_equal(count,np.ones(len(self.y)))

    def test_conflicting_preference_preserved_and_audited(self):
        conflicts=self.result['forced_rank_conflicts']
        self.assertIn('round14-2',[q['id'] for q in conflicts])
        row=next(q for q in self.evidence['rows'] if q['id']=='round14-2')
        self.assertEqual(row['winner'],'B')
        cfg=self.result['candidate_fit_all_310'];beta=np.array(cfg['coefficients'])
        i=next(i for i,q in enumerate(self.evidence['rows']) if q['id']=='round14-2')
        self.assertAlmostEqual(float(self.x[i]@beta),0,places=7)

    def test_exact_ties_monotonicity_symmetry_and_metrics(self):
        cfg=self.result['candidate_fit_all_310'];beta=np.array(cfg['coefficients'])
        mask=soft.masks(self.evidence['rows'])['confirmed_pure_tare_ties']
        np.testing.assert_allclose(self.x[mask]@beta,0,atol=1e-7)
        np.testing.assert_array_equal(base.classify(-self.x@beta,cfg['threshold']),-base.classify(self.x@beta,cfg['threshold']))
        for z,s,age,w in product(base.ZONES,base.SHADES,base.AGES,soft.WEIGHTS):
            val=soft.features([z,s,age,w],'context_steps')@beta
            if w>110:self.assertGreaterEqual(soft.features([z,s,age,w-5],'context_steps')@beta+1e-6,val)
            if age>20:self.assertGreaterEqual(soft.features([z,s,age-5,w],'context_steps')@beta+1e-6,val)
            if s!='pale/straw':self.assertGreaterEqual(soft.features([z,base.SHADES[base.SHADES.index(s)+1],age,w],'context_steps')@beta+1e-6,val)
        for runs in self.result['nested_cv']['runs'].values():
            for run in runs:
                self.assertEqual(base.metrics(self.y,np.array(run['predictions']))['matched'],run['metrics']['all']['matched'])


if __name__=='__main__':unittest.main()
