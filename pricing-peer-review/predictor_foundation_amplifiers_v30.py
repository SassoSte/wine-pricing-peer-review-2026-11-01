"""Standalone NumPy+JSON experimental value and premium-justification predictor."""
from pathlib import Path
import argparse,json
import numpy as np
DEFAULT_CONFIG=Path(__file__).with_name('foundation-amplifiers-selected-config-v30.json')
PARTS=('vintage','tare','vintage_tare','provenance','shade','all_top')
class Model:
 def __init__(self,path=DEFAULT_CONFIG):
  self.config=json.loads(Path(path).read_text());self.domain=self.config['domain'];self.weights=np.asarray(self.config['value_model']['coefficients'],float);self.head=self.config['premium_model'];self.hweights=np.asarray(self.head['coefficients'],float)
  if self.weights.shape!=(23,) or self.hweights.shape!=(13,) or not np.isfinite(self.weights).all() or not np.isfinite(self.hweights).all():raise ValueError('Invalid model coefficients')
  if np.any(np.asarray(self.head['scale'])<=0):raise ValueError('Invalid standardization scale')
 def _quality(self,o):return (40-o[2])/20,(130-o[3])/20
 def _completion(self,o):
  c=self.config['all_top_profile'];return float(o[0] in c['provenances'] and o[1]==c['shade'] and o[2]==c['vintage'] and o[3]==c['tare'])
 def _features(self,o):
  if len(o)!=4:raise ValueError('Expected provenance,shade,vintage,tare')
  z,s,a,w=o;d=self.domain
  if z not in d['provenances'] or s not in d['shades'] or a not in d['vintage_years'] or w not in d['tare_lb']:raise ValueError(o)
  v,t=self._quality(o);c=self.config['context_multiplier'];context=c['intercept']+c['vintage_quality_weight']*v+c['tare_quality_weight']*t
  f=[float(a<=k) for k in (35,30,25,20)]+[float(w<=k) for k in (125,120,115,110)]+[v*t]+[float(z==k)*context for k in d['provenances'][1:]]+[float(d['shades'].index(s)>=i)*context for i in range(1,5)]
  if s=='pale/straw' and w==130:f[21]=0.
  return np.r_[f,self._completion(o)]
 def components(self,o):
  f=self._features(o)*self.weights;return np.array([f[:4].sum(),f[4:8].sum(),f[8],f[9:18].sum(),f[18:22].sum(),f[22]])
 def value(self,o):return float(self.components(o).sum())
 def compare(self,a,b):
  a,b=list(a),list(b);ca=self.components(a);cb=self.components(b);delta=ca-cb;g=float(delta.sum());sg=1 if g>1e-7 else -1 if g<-1e-7 else 0;va,ta=self._quality(a);vb,tb=self._quality(b);cd=abs(self._completion(a)-self._completion(b));pure5=a[:3]==b[:3] and abs(a[3]-b[3])==5 and cd==0;opposition=max(0.,(abs(delta).sum()-abs(g))/2)
  h=np.array([1.,abs(g),*(sg*delta[:5]).tolist(),opposition,cd,(va+vb)/2,(ta+tb)/2,float(pure5),abs(self.domain['shades'].index(a[1])-self.domain['shades'].index(b[1]))/4]);logit=float(((h-np.asarray(self.head['mean']))/np.asarray(self.head['scale']))@self.hweights);score=float(1/(1+np.exp(-logit))) if logit>=0 else float(np.exp(logit)/(1+np.exp(logit)));large=score>self.head['cutoff'] and sg!=0
  return {'model':self.config['model_id'],'value_a':float(ca.sum()),'value_b':float(cb.sum()),'margin':g,'predicted_direction':'A' if sg>0 else 'B' if sg<0 else None,'predicted_meaningfulness':'meaningful_difference' if large else 'no_meaningful_difference','premium_justification_score':score,'premium_justified':bool(large),'components_a':dict(zip(PARTS,ca.tolist())),'components_b':dict(zip(PARTS,cb.tolist())),'exact_price_equality':None,'prediction_source':'model_only','value_units':self.config['value_units'],'premium_score_units':self.config['premium_score_units']}
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--a',required=True);p.add_argument('--b',required=True);p.add_argument('--config',default=str(DEFAULT_CONFIG));args=p.parse_args();print(json.dumps(Model(args.config).compare(json.loads(args.a),json.loads(args.b)),indent=2))
