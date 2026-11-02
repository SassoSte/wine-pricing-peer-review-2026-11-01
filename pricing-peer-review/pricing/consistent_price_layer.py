"""Canonical per-offering prices from monotone attribute loss and versioned anchors.
No pair-context adjustment enters the price. This is a provisional pricing layer,
not a change to V28 and not a calibrated market price/confidence estimator.
"""
from pathlib import Path
import json,math
import numpy as np
DEFAULT=Path(__file__).with_name('consistent-price-config-v1.json')
def attribute_loss(offering,domain,weights):
 z,s,age,tare=offering
 if z not in domain['provenances'] or s not in domain['shades'] or age not in domain['vintage_years'] or tare not in domain['tare_lb']:raise ValueError('Offering outside validated input domain')
 shade=[float(domain['shades'].index(s)>=i) for i in range(1,5)]
 if s=='pale/straw' and tare==130:shade[3]=0.
 quality=np.array(shade+[float(age<=i) for i in (35,30,25,20)]+[(130-tare)/5])
 top=np.r_[np.ones(8),4.]
 return float((top-quality)@np.asarray(weights)[9:18])
def curve_value(x,knots):
 if x<0 and x>-1e-10:x=0.
 if x<0:raise ValueError('Negative quality loss')
 for (x0,y0),(x1,y1) in zip(knots,knots[1:]):
  if x<=x1:return y0+(y1-y0)*(x-x0)/(x1-x0)
 (x0,y0),(x1,y1)=knots[-2:];return y1+(y1-y0)*(x-x1)/(x1-x0)
class Model:
 def __init__(self,path=DEFAULT):
  self.config=json.loads(Path(path).read_text());self.domain=self.config['domain'];self.weights=np.array(self.config['base_coefficients'],float);self.knots=self.config['log_discount_knots'];self.anchors=self.config['regional_anchors']
  if any(x[0]>=y[0] or x[1]>y[1] for x,y in zip(self.knots,self.knots[1:])):raise ValueError('Nonmonotone or duplicate knots')
 def price(self,offering):
  loss=attribute_loss(offering,self.domain,self.weights);discount=curve_value(loss,self.knots);anchor=self.anchors[offering[0]];price=anchor['price']*math.exp(-discount)
  return {'price_usd':price,'attribute_loss':loss,'log_discount':discount,'anchor_price':anchor['price'],'anchor_status':anchor['status'],'extrapolating_attribute_curve':loss>self.knots[-1][0]+1e-9,'price_basis':self.config['price_basis'],'calibration_status':'supplied_anchor' if offering[1:]==['pale/straw',20,110] and anchor['status']=='user_established' else 'accepted_estimate_used_for_fit' if list(offering) in self.config.get('calibration_offerings',[]) else 'unvalidated_offering','status':'provisional_model_price_not_market_validation'}
 def compare(self,a,b):
  pa=self.price(a)['price_usd'];pb=self.price(b)['price_usd'];return {'price_a':pa,'price_b':pb,'difference':pa-pb,'ratio':pa/pb}
 def translate_from_reference(self,offering,reference):
  # Uses this config's canonical reference price, never an arbitrary external price.
  px=self.price(offering);pr=self.price(reference)
  return pr['price_usd']*(px['anchor_price']/pr['anchor_price'])*math.exp(pr['log_discount']-px['log_discount'])
