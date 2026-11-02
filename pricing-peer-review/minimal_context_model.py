"""Three context coefficients added to the unchanged18-feature simple benchmark."""
from itertools import product
import numpy as np
from scipy.optimize import minimize,LinearConstraint
import compare_models as base
import build_meaningful_benchmark as simple

DOMESTIC={'northeast','southwest','southeast','central','northwest'}
TERMS=('northwest x amber','domestic x (30-vintage)/10','West Central Asia x golden-or-pale')
N=21


def features(option,active=(0,1,2)):
    original=base.features(option);z,s,age,w=option
    context=np.array([float(z=='northwest' and s=='amber'),float(z in DOMESTIC)*(30-age)/10,float(z=='West Central Asia' and s in ('golden','pale/straw'))])
    return np.r_[original,context[list(active)]]


def constraints(active=(0,1,2)):
    rows=[]
    for z,s,age,w in product(base.ZONES,base.SHADES,base.AGES,(110,115,120,125,130)):
        before=features([z,s,age,w],active);i=base.SHADES.index(s)
        if age>20:rows.append(features([z,s,age-5,w],active)-before)
        if i<4:rows.append(features([z,base.SHADES[i+1],age,w],active)-before)
        if w>110:rows.append(features([z,s,age,w-5],active)-before)
    return np.unique(rows,axis=0)

C=constraints()


def arrays(targets):
    _,material,direction,g=simple.arrays(targets)
    x=np.array([features(r['a'])-features(r['b']) for r in targets])
    return x,material,direction,g


def fit(targets,alpha):
    x,m,d,_=arrays(targets)
    result=minimize(simple.objective,np.zeros(N),args=(x,m,d,alpha),jac=True,method='SLSQP',bounds=[(None,None)]*9+[(0,None)]*9+[(None,None)]*3,constraints=[LinearConstraint(C,0,np.inf)],options={'ftol':1e-11,'maxiter':3000})
    if not result.success:raise RuntimeError(result.message)
    if np.min(C@result.x)<-1e-7:raise RuntimeError('Monotonicity failed')
    return result.x
