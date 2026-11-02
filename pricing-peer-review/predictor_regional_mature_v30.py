"""Experimental intrinsic utility with regional and mature light-shade vintage terms."""
from pathlib import Path
import json,argparse
import numpy as np
DEFAULT_CONFIG=Path(__file__).with_name('regional-mature-selected-config-v30.json')
class Model:
 def __init__(self,path=DEFAULT_CONFIG):
  self.config=json.loads(Path(path).read_text());self.domain=self.config['domain'];self.weights=np.asarray(self.config['coefficients'],float)
  if self.weights.shape!=(25,) or not np.isfinite(self.weights).all():raise ValueError('Invalid25-coefficient utility configuration')
 def features(self,o):
  if len(o)!=4:raise ValueError('Expected provenance,shade,vintage,tare')
  z,s,a,w=o;d=self.domain
  if z not in d['provenances'] or s not in d['shades'] or a not in d['vintage_years'] or w not in d['tare_lb']:raise ValueError(o)
  f=[float(z==v) for v in d['provenances'][1:]]+[float(d['shades'].index(s)>=i) for i in range(1,5)]+[float(d['vintage_years'].index(a)>=i) for i in range(1,5)]+[(130-w)/5]
  if s=='pale/straw' and w==130:f[12]=0.
  return np.r_[f,float(z in d['domestic'] and a==20),float(z not in d['domestic'] and s=='pale/straw' and a<=25 and w<130),max(0,(120-w)/5),float(a<=30)*(130-w)/5,float(z in ('Western Europe','northeast') and s=='pale/straw' and a==20 and w==110),float(z=='South/Eastern Asia' and a==20),float(s in ('golden','pale/straw') and a<=35)]
 def value(self,o):return float(self.features(o)@self.weights)
 def compare(self,a,b):
  va=self.value(a);vb=self.value(b);g=va-vb;r=1.
  return {'value_a':va,'value_b':vb,'margin':g,'decision_radius':r,'predicted_direction':'A' if g>1e-7 else 'B' if g<-1e-7 else None,'predicted_meaningfulness':'meaningful_difference' if abs(g)>r+1e-8 else 'no_meaningful_difference','exact_price_equality':None,'prediction_source':'model_only','units':'intrinsic utility; not calibrated money','model':self.config['model_id']}
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--a',required=True);p.add_argument('--b',required=True);p.add_argument('--config',default=str(DEFAULT_CONFIG));args=p.parse_args();print(json.dumps(Model(args.config).compare(json.loads(args.a),json.loads(args.b)),indent=2))
