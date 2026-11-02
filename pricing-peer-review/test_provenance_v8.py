from collections import Counter
from copy import deepcopy
import hashlib
import json
from itertools import product
import unittest
import numpy as np
import compare_models as base
import compare_interactions as common
import compare_tare_models as shared
import provenance_tare_model as scoped
import refit_provenance_v8 as r


class ProvenanceV8Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parent=json.loads((r.ROOT/'evidence-v7.json').read_text())
        cls.r23=json.loads((r.ROOT/'round23-fixed.json').read_text())
        cls.r24=json.loads((r.ROOT/'round24-isolation.json').read_text())
        cls.evidence=json.loads((r.ROOT/'evidence-v8.json').read_text())
        cls.result=json.loads((r.ROOT/'provenance-comparison-v8.json').read_text())
        cls.rows=cls.evidence['rows']
        cls.cfg=cls.result['candidate_fit_all_341']
        cls.design=scoped.Design(cls.cfg['local_contexts']);cls.beta=np.array(cls.cfg['coefficients'])

    def test_reconciliation_accounting_and_history(self):
        original=deepcopy((self.parent,self.r23,self.r24))
        rows,audit=r.build_evidence(self.parent,self.r23,self.r24)
        self.assertEqual((self.parent,self.r23,self.r24),original)
        self.assertEqual(rows,self.rows);self.assertEqual(rows[:310],self.parent['rows'])
        self.assertEqual(len(rows),341)
        self.assertEqual(Counter(q['winner'] for q in rows),{'A':156,'B':66,'tie':119})
        self.assertEqual(Counter(q['action'] for q in audit),{'new comparison':17,'new component comparison':11,'resolved previously unanswered':3,'correction':1})
        self.assertEqual(len({q['id'] for q in rows}),341)
        self.assertEqual(len({frozenset((tuple(q['a']),tuple(q['b']))) for q in rows}),341)
        by_id={q['id']:q for q in rows}
        self.assertEqual(by_id['round23-10']['winner'],'tie')
        self.assertEqual(by_id['round23-10']['prior_answer']['winner'],'A')
        self.assertEqual(by_id['round23-15']['winner'],'tie')
        for item in self.r24['unresolved_queue']:
            self.assertEqual(by_id[item['source_id']]['winner'],item['winner'])
            self.assertEqual(by_id[item['source_id']]['current_answer_source'],item['resolution_id'])
            self.assertNotIn(item['resolution_id'],by_id)
        self.assertEqual(self.evidence['workflow_feedback'],self.r24['difficulty_review'])

    def test_invalid_resolution_rejected(self):
        bad=deepcopy(self.r24);bad['unresolved_queue'][0]['winner']='B'
        with self.assertRaises(ValueError):r.build_evidence(self.parent,self.r23,bad)
        bad=deepcopy(self.r24);bad['evidence_overrides'][0]['winner']='A'
        with self.assertRaises(ValueError):r.build_evidence(self.parent,self.r23,bad)

    def test_preserved_baselines_and_evidence(self):
        for f,h in self.result['method']['historical_file_hashes'].items():
            self.assertEqual(hashlib.sha256((r.ROOT/f).read_bytes()).hexdigest(),h,f)
        self.assertEqual(hashlib.sha256((r.ROOT/'evidence-v8.json').read_bytes()).hexdigest(),self.result['method']['evidence_sha256'])

    def test_extended_folds_context_selection_and_old_predictions(self):
        _,_,g=common.get_arrays(self.rows,'additive');oldg=g[:310]
        old=json.loads((r.ROOT/'provenance-tare-comparison.json').read_text())
        audits={(a['seed'],a['fold'],a['model']):a for a in self.result['nested_cv']['fold_audits']}
        for seed in common.SEEDS:
            original=list(base.folds(oldg,5,seed));coverage=np.zeros(len(self.rows))
            for fold,(train,test) in enumerate(r.extended_folds(oldg,g,seed)):
                coverage[test]+=1
                np.testing.assert_array_equal(test[test<310],original[fold][1])
                np.testing.assert_array_equal(train[train<310],original[fold][0])
                for name,tr in [('v7_evidence_control',train[train<310]),('v8_evidence_candidate',train)]:
                    self.assertFalse(set(g[tr])&set(g[test]))
                    expected={tuple(self.rows[i]['a'][:3]) for i in tr if self.rows[i]['a'][:3]==self.rows[i]['b'][:3] and self.rows[i]['a'][3]!=self.rows[i]['b'][3]}
                    self.assertEqual(set(tuple(v) for v in audits[(seed,fold,name)]['local_contexts']),expected)
            np.testing.assert_array_equal(coverage,np.ones(len(self.rows)))
            control=next(q for q in self.result['nested_cv']['runs']['v7_evidence_control'] if q['seed']==seed)
            prior=next(q for q in old['nested_cv']['runs'] if q['seed']==seed)
            self.assertEqual(control['predictions'][:310],prior['predictions'])

    def test_exact_ties_remain_local_and_known_regression(self):
        x=self.design.array(self.rows);y=np.array([base.LABEL[q['winner']] for q in self.rows])
        mask=shared.masks(self.rows)['confirmed_pure_tare_ties']
        np.testing.assert_allclose((x@self.beta)[mask],0,atol=1e-7)
        fixed=self.design.fixed_steps(self.rows)
        self.assertFalse(np.any(fixed[:117]))
        self.assertTrue(fixed[self.design.local_index[('Western Europe','copper',35)]+1])
        self.assertFalse(fixed[self.design.local_index[('southeast','copper',35)]+1])
        by_id={q['id']:i for i,q in enumerate(self.rows)}
        self.assertLess(float(x[by_id['round14-2']]@self.beta),-self.cfg['threshold'])
        self.assertAlmostEqual(float(x[by_id['round21-12']]@self.beta),0,places=7)
        self.assertAlmostEqual(float(x[by_id['round23-10']]@self.beta),0,places=7)

    def test_monotonicity_symmetry_metrics(self):
        for z,s,age,w in product(base.ZONES,base.SHADES,base.AGES,shared.WEIGHTS):
            value=self.design.features([z,s,age,w])@self.beta
            if w>110:self.assertGreaterEqual(self.design.features([z,s,age,w-5])@self.beta+1e-6,value)
            if age>20:self.assertGreaterEqual(self.design.features([z,s,age-5,w])@self.beta+1e-6,value)
            if s!='pale/straw':self.assertGreaterEqual(self.design.features([z,base.SHADES[base.SHADES.index(s)+1],age,w])@self.beta+1e-6,value)
        x=self.design.array(self.rows);y=np.array([base.LABEL[q['winner']] for q in self.rows])
        np.testing.assert_array_equal(base.classify(-x@self.beta,self.cfg['threshold']),-base.classify(x@self.beta,self.cfg['threshold']))
        self.assertEqual(base.metrics(y,base.classify(x@self.beta,self.cfg['threshold']))['matched'],self.cfg['in_sample']['matched'])
        for runs in self.result['nested_cv']['runs'].values():
            for run in runs:self.assertEqual(base.metrics(y,np.array(run['predictions']))['matched'],run['metrics']['all']['matched'])


if __name__=='__main__':unittest.main()
