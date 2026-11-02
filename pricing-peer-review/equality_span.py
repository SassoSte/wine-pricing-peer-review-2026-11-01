"""Intrinsic linear-model equality certificate; not a V28 pair-score classifier."""
import numpy as np
class LinearEqualityCertificate:
 def __init__(self,identity_vectors,weights,tolerance=1e-7):
  self.weights=np.asarray(weights,float);self.identities=np.asarray(identity_vectors,float).reshape((-1,len(self.weights)));self.tolerance=tolerance
  if not np.isfinite(self.weights).all() or not np.isfinite(self.identities).all():raise ValueError('Nonfinite values')
  if len(self.identities) and max(abs(self.identities@self.weights))>tolerance:raise ValueError('Reference model does not satisfy identities')
  _,s,v=np.linalg.svd(self.identities,full_matrices=False);self.basis=v[s>1e-10];self.rank=len(self.basis)
 def check(self,difference):
  d=np.asarray(difference,float)
  if d.shape!=self.weights.shape or not np.isfinite(d).all():raise ValueError('Invalid feature difference')
  residual=d-(d@self.basis.T)@self.basis;gap=float(d@self.weights);supported=bool(np.linalg.norm(residual)<=self.tolerance and abs(gap)<=self.tolerance)
  return {'supported':supported,'span_residual':float(np.linalg.norm(residual)),'reference_gap':gap,'basis':'confirmed identities in the specified intrinsic linear feature space','scope':'model-relative implication, not independently observed equality'}
