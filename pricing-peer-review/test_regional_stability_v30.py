import unittest,json,hashlib
from pathlib import Path
from itertools import product
import numpy as np
import joint_objective_v22 as joint
import intrinsic_regional_v30 as oldmodel
import regional_mature_shade_v30 as newmodel
R=Path(__file__).resolve().parent
class Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.rows=json.loads((R/'benchmark-targets-v30.json').read_text())['rows'];cls.by={q['id']:q for q in cls.rows};cls.long=json.loads((R/'regional-solver-audit-v30.json').read_text());cls.norm=json.loads((R/'regional-minnorm-validation-v30.json').read_text());cls.new=json.loads((R/'regional-mature-shade-validation-v30.json').read_text())
 def test_solver_and_integrity(self):
  self.assertEqual(len(self.long['reruns']),5);self.assertEqual(len(self.long['fold_audits']),25)
  for f in self.long['fold_audits']:self.assertLessEqual(f['fit']['mip_gap'],.001)
  for r in (self.long,self.new):
   for f,h in r['source_hashes'].items():self.assertEqual(hashlib.sha256((R/f).read_bytes()).hexdigest(),h)
 def test_minimum_norm_preserves_training_judgments(self):
  for r,model,kind in ((self.norm,oldmodel,'regional_vintage'),(self.new,newmodel,'regional_mature_shade')):
   for f in r['fold_audits']:
    train=[self.by[id] for id in f['training_ids']];x=model.design(train,kind);a,s,*_=joint.evaluations(train,x@f['fit']['coefficients'],1.);b,*_=joint.evaluations(train,x@f['polished_fit']['coefficients'],1.);self.assertTrue(np.all(b[0,a[0]&s]));self.assertLessEqual(np.linalg.norm(f['polished_fit']['coefficients']),np.linalg.norm(f['fit']['coefficients'])+1e-5);self.assertTrue(set(f['polished_fit']['preserved_training_ids'])<=set(f['training_ids']))
 def test_no_family_leakage(self):
  import tare_compensation_v27 as bm
  gs=bm.parent.parent.additive.features.arrays(self.rows)[3];lookup={q['id']:gs[i] for i,q in enumerate(self.rows)}
  for f in self.new['fold_audits']:
   self.assertFalse({lookup[id] for id in f['training_ids']}&{lookup[id] for id in f['validation_ids']});self.assertTrue(set(f['fit']['protected_training_ids'])<=set(f['training_ids']))
 def test_required_controls_and_intrinsic_values(self):
  d=newmodel.DOMAIN;grid=list(product(d['provenances'],d['shades'],d['vintage_years'],d['tare_lb']));rng=np.random.default_rng(30)
  for c in (self.new['full_model'],self.new['polished_full_model']):
   st,lo,hi=newmodel.structural('regional_mature_shade');g=st@c['coefficients'];self.assertTrue(np.all(g>=lo-1e-6));self.assertTrue(np.all(g<=hi+1e-6))
   for id in (*newmodel.ANCHORS,*newmodel.NEW_ANCHORS):
    q=self.by[id];p=newmodel.predict(q['a'],q['b'],c);self.assertEqual(p['predicted_direction'],'A' if q['known_direction']==1 else 'B');self.assertEqual(p['predicted_meaningfulness'],'no_meaningful_difference' if q['materiality_target']==0 else 'meaningful_difference')
   for i,j,k in rng.integers(len(grid),size=(100,3)):self.assertAlmostEqual(newmodel.predict(grid[i],grid[j],c)['margin']+newmodel.predict(grid[j],grid[k],c)['margin'],newmodel.predict(grid[i],grid[k],c)['margin'])
  for z,a in product(d['provenances'],d['vintage_years']):np.testing.assert_array_equal(newmodel.features([z,'golden',a,130],'regional_mature_shade'),newmodel.features([z,'pale/straw',a,130],'regional_mature_shade'))
  for z,s,a,w in grid:
   if w<130:self.assertEqual(newmodel.features([z,s,a,w],'regional_mature_shade')[-1],newmodel.features([z,s,a,w+5],'regional_mature_shade')[-1])
if __name__=='__main__':unittest.main()
