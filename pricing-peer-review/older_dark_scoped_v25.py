"""Targeted older-age and dark-shade residuals over frozen v24."""
from itertools import product
import numpy as np
import five_year_premium_v23 as baseline
import joint_objective_v22 as joint

def components(rows,cfg):
 g,r,h=baseline.components(rows,cfg['base_model'],cfg['scope']);g=g+cfg['five_year_fraction']*h
 beta=np.array(cfg['base_model']['coefficients']);scale=cfg['base_model']['reference_context']['base_radius'];x=np.array([baseline.base.utility.features(q['a'])-baseline.base.utility.features(q['b']) for q in rows])
 # Cumulative age35 step, brown->copper step, copper->amber step.
 # Cap added amber increment so originally negligible adjacent shade remains negligible.
 room=max(0.,scale*(1-1e-7)-beta[10]);older_gate=np.array([q['a'][0]==q['b'][0] and {q['a'][2],q['b'][2]}=={35,40} and {q['a'][1],q['b'][1]}=={'golden','pale/straw'} for q in rows])
 micro_gate=np.array([q['a'][0]==q['b'][0] and q['a'][2:]==q['b'][2:] and {q['a'][1],q['b'][1]}=={'amber','copper'} for q in rows])
 features=np.column_stack([x[:,13]*scale*older_gate,x[:,9]*scale,x[:,10]*room*micro_gate])
 return g,r,features

def fit(rows,cfg,arm):
 params=np.array(list(product(np.linspace(0,2,21) if arm in ('older','combined') else [0.],np.linspace(0,2,11) if arm in ('dark','combined') else [0.],np.linspace(0,1,11) if arm in ('dark','combined') else [0.])))
 g,r,h=components(rows,cfg);gg=g[None,:]+params@h.T;c,s,b,groups,macro,loss=joint.evaluations(rows,gg,r)
 i=max(range(len(params)),key=lambda i:(round(macro[i],12),round(c[i,b].mean(),12),-round(loss[i],12),-float(params[i].sum())))
 return {'adjustments':params[i].tolist(),'training_joint_balanced':float(macro[i]),'training_joint_loss':float(loss[i])}

def predict(a,b,cfg):
 g,r,h=components([{'a':a,'b':b}],cfg['base_model']);gap=float((g+h@cfg.get('adjustments',[0.,0.,0.]))[0]);cut=float(r[0])
 return {'predicted_direction':'A' if gap>1e-7 else 'B' if gap<-1e-7 else None,'predicted_meaningfulness':'meaningful_difference' if abs(gap)>cut+1e-8 else 'no_meaningful_difference','margin':gap,'decision_radius':cut,'exact_price_equality':None,'prediction_source':'model_only','units':'pair-comparison score, not a standalone price'}
