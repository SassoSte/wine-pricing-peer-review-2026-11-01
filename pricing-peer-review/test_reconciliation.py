import hashlib
import json
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
import numpy as np
import compare_models as base
import compare_interactions as models
import reconcile_and_compare as rc


class ReconciliationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original=models.load_rows()
        cls.clarifications=json.loads((rc.ROOT/'round12-clarification.json').read_text())
        cls.evidence=json.loads((rc.ROOT/'evidence-v2.json').read_text())
        cls.results=json.loads((rc.ROOT/'objective-comparison-v2.json').read_text())

    def test_exactly_two_changes_no_duplicates_or_input_mutation(self):
        before=deepcopy(self.original)
        rows,audit=rc.reconcile(self.original,self.clarifications)
        self.assertEqual(self.original,before)
        self.assertEqual(len(rows),158)
        self.assertEqual([r['id'] for r in rows],[r['id'] for r in before])
        changed={r['id']:(old['winner'],r['winner']) for old,r in zip(before,rows) if old['winner']!=r['winner']}
        self.assertEqual(changed,{'round7-9':('A','tie'),'round11-17':('B','A')})
        self.assertEqual(sum(a['changed'] for a in audit),2)
        self.assertEqual(sum(not a['changed'] for a in audit),13)
        self.assertEqual(len({frozenset((tuple(r['a']),tuple(r['b']))) for r in rows}),158)
        self.assertEqual(rows,self.evidence['rows'])

    def test_alignment_and_unapproved_changes_fail(self):
        r=self.original[0];q={'a':r['b'],'b':r['a'],'winner':'A'}
        self.assertEqual(rc.align_answer(r,q),'B')
        q['a']=['invalid']
        with self.assertRaises(ValueError):rc.align_answer(r,q)
        bad=deepcopy(self.clarifications);bad['evidence_overrides']=[]
        with self.assertRaises(ValueError):rc.reconcile(self.original,bad)

    def test_version_cannot_be_overwritten(self):
        with TemporaryDirectory() as directory:
            p=Path(directory)/'test.json'
            rc.write_versioned(p,{'v':1});rc.write_versioned(p,{'v':1})
            with self.assertRaises(FileExistsError):rc.write_versioned(p,{'v':2})
            self.assertEqual(json.loads(p.read_text()),{'v':1})

    def test_historical_hashes_and_snapshot(self):
        for name,digest in self.results['method']['preserved_file_hashes'].items():
            self.assertEqual(hashlib.sha256((rc.ROOT/name).read_bytes()).hexdigest(),digest,name)
        self.assertEqual(hashlib.sha256((rc.ROOT/'evidence-v2.json').read_bytes()).hexdigest(),self.results['method']['evidence_sha256'])

    def test_same_split_membership_and_metrics(self):
        rows=self.evidence['rows'];_,y,g=models.get_arrays(rows,'additive')
        oldg=models.get_arrays(self.original,'additive')[2]
        np.testing.assert_array_equal(g,oldg)
        for seed in models.SEEDS:
            for (tr,te),(otr,ote) in zip(base.folds(g,5,seed),base.folds(oldg,5,seed)):
                np.testing.assert_array_equal(tr,otr);np.testing.assert_array_equal(te,ote)
                self.assertFalse(set(g[tr])&set(g[te]))
        for runs in self.results['nested_cv']['runs'].values():
            for run in runs:
                actual=base.metrics(y,np.array(run['predictions']))
                self.assertEqual(actual['matched'],run['all']['matched'])
                self.assertAlmostEqual(actual['balanced_accuracy'],run['all']['balanced_accuracy'])


if __name__=='__main__':unittest.main()
