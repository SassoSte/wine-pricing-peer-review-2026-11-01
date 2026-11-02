"""Weighted hierarchy with distinct strict, exact and practical-similarity evidence.
Architecture/priors unchanged; new loss permits nonzero gaps inside a declared band.
"""
import numpy as np
from scipy.optimize import minimize,LinearConstraint
import compare_models as base
import compare_objectives as objective
import provenance_tare_model as offering
import weighted_domestic_model as weighted
import domestic_hierarchy_model as prior

LABEL={'A':1,'B':-1,'tie':0,'practical_similarity':2}
EXACT_TOL=1e-7


def arrays(rows):
    y=np.array([LABEL[r['winner']] for r in rows])
    groups=np.array([repr((tuple(sorted((r['a'][0],r['b'][0]))),tuple(sorted((r['a'][1],r['b'][1]))))) for r in rows])
    return y,groups


def adjustment(margins,y,radius):
    """Replace squared-zero targets on similar rows with epsilon-insensitive loss.
    Radius is a model-scale convention inherited from training-selected settings,
    never a user-supplied monetary amount. Similar rows generate no hard equality.
    """
    if radius<=0:raise ValueError('Practical similarity needs a positive declared band')
    similar=y==2;delta=np.zeros(len(y));m=margins[similar]
    excess=np.maximum(0.,abs(m)-radius)
    delta[similar]=2*(np.sign(m)*excess-m)
    return float(excess@excess-m@m),delta


def offering_objective(beta,x,y,gram,alpha,radius):
    proxy=np.where(y==2,0,y)
    value,gradient=objective.objective(beta,x,proxy,gram,alpha)
    delta,dgradient=adjustment(x@beta,y,radius)
    return value+delta,gradient+x.T@dgradient


def fit_offering(rows,cfg):
    design=offering.Design.from_training(rows);x=design.array(rows);y,_=arrays(rows)
    r=design.penalty(cfg['pooling']);gram=r.T@r;fixed=design.fixed_steps(rows)
    bounds=[(None,None)]*9+[(0.,0.) if fixed[j] else (0.,None) for j in range(9,design.n)]
    result=minimize(offering_objective,np.zeros(design.n),args=(x,y,gram,cfg['alpha'],cfg['threshold']),jac=True,method='SLSQP',bounds=bounds,constraints=[LinearConstraint(design.constraints,0,np.inf)],options={'ftol':1e-9,'maxiter':1200})
    if not result.success:raise RuntimeError(result.message)
    if np.min(design.constraints@result.x)<-1e-6:raise RuntimeError('Monotonicity failed')
    assert np.all(abs(result.x[fixed])<1e-8)
    return design,result.x


def layer_objective(params,x,offset,y,layer,strength,radius):
    proxy=np.where(y==2,0,y)
    value,gradient=weighted.objective(params,x,offset,proxy,layer,strength)
    delta,dgradient=adjustment(offset+x@params,y,radius)
    return value+delta,gradient+x.T@dgradient


def fit_layer(rows,layer,strength,radius):
    x,offset=layer.array(rows);y,_=arrays(rows)
    result=minimize(layer_objective,layer.initial.copy(),args=(x,offset,y,layer,strength,radius),jac=True,method='SLSQP',bounds=[(None,None)]*5+[(0,None)]*25+[(.05,None)]*3,constraints=[LinearConstraint(layer.c,layer.lower,np.inf)],options={'ftol':1e-9,'maxiter':1000})
    if not result.success:raise RuntimeError(result.message)
    if np.min(layer.c@result.x-layer.lower)<-2e-6:raise RuntimeError('Layer monotonicity failed')
    return result.x


def margins(rows,layer,params):
    x,offset=layer.array(rows);return offset+x@params


def assess(y,m,radius):
    """Two axes: direction and closeness. Similar may include zero; not unresolved.
    Strict correctness is sign-based even inside similarity band. Exact equality
    requires zero within numerical tolerance. A similarity claim permits either
    sign inside the declared band. Denominators and all three recalls are exposed.
    """
    y=np.asarray(y);m=np.asarray(m);radius=np.broadcast_to(radius,m.shape)
    direction=np.where(m>EXACT_TOL,1,np.where(m<-EXACT_TOL,-1,0))
    strict=abs(y)==1;exact=y==0;similar=y==2
    equal=abs(m)<=EXACT_TOL;near=abs(m)<=radius+1e-8
    correct=(strict&(direction==y))|(exact&equal)|(similar&near)
    recalls={};counts={}
    for name,mask in [('strict_direction',strict),('exact_equality',exact),('practical_similarity',similar)]:
        counts[name]=int(sum(mask))
        if np.any(mask):recalls[name]=float(np.mean(correct[mask]))
    return {'n':len(y),'matched':int(sum(correct)),'semantic_compatibility':float(np.mean(correct)) if len(y) else None,
            'balanced_semantic_compatibility':float(np.mean(list(recalls.values()))) if recalls else None,
            'counts':counts,'recall':recalls,'opposite_winner_errors':int(sum(strict&(direction==-y))),
            'predicted_exact_score_equalities':int(sum(equal)),'predicted_within_similarity_band':int(sum(near)),
            'exact_equality_precision_on_determinate_labels':float(np.mean(exact[equal&~similar])) if np.any(equal&~similar) else None,
            'note':'Set-valued semantic compatibility, not four-class accuracy. Practical similarity can contain either tiny direction or zero; unresolved excluded.'}


def operational_metrics(y,m,radius):
    """Legacy three-way diagnostic on determinate labels only; band is NOT proof
    of exact price equality. No similar row is converted to an exact tie here.
    """
    mask=y!=2;radius=np.broadcast_to(radius,np.shape(m))
    pred=np.where(m>radius+1e-8,1,np.where(m<-radius-1e-8,-1,0))
    return base.metrics(y[mask],pred[mask])


def choose(rows,cfg,seed):
    y,g=arrays(rows);pred={s:np.zeros(len(rows)) for s in prior.STRENGTHS}
    for tr,va in base.folds(g,3,seed):
        training=[rows[i] for i in tr];valid=[rows[i] for i in va]
        design,beta=fit_offering(training,cfg);layer=weighted.Layer(design,beta)
        for strength in prior.STRENGTHS:pred[strength][va]=margins(valid,layer,fit_layer(training,layer,strength,cfg['threshold']))
    scores={s:assess(y,m,cfg['threshold']) for s,m in pred.items()}
    best=max(prior.STRENGTHS,key=lambda s:(round(scores[s]['balanced_semantic_compatibility'],12),round(scores[s]['semantic_compatibility'],12),-scores[s]['opposite_winner_errors'],s))
    return best,scores[best]
