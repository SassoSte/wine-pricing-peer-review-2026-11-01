"""One-parameter context-dependent boundary; underlying direction scores frozen."""
import numpy as np
import compare_models as base
import domestic_shade_model as score_model

KINDS=('matched_control','mature_shade','shared_light_tare')
ETAS=tuple(np.linspace(0.,1.,21).tolist())
TOL=1e-7


def context_feature(a,b,beta,base_radius,kind):
    if kind not in KINDS:raise ValueError(kind)
    matched=a[0]!=b[0] and a[1]==b[1] and a[2]==b[2] and abs(a[3]-b[3])<=5
    if not matched:return 0.
    if kind=='matched_control':context=1.
    elif kind=='mature_shade':context=float(a[2]>=35 or (a[2]>=30 and a[1]=='brown'))
    else:context=(130-(a[3]+b[3])/2)/20
    # Smooth proximity, not an invented geographic/tier adjacency table.
    # Very large modeled provenance gaps get less boundary expansion.
    prov=abs(float((base.features(a)[:9]-base.features(b)[:9])@np.asarray(beta)[:9]))
    proximity=1./(1.+prov/float(base_radius))
    return float(context*proximity)


def radius(a,b,beta,base_radius,kind,eta):
    if not 0<=eta<=1:raise ValueError('Bounded context coefficient required')
    return float(base_radius)*(1.+float(eta)*context_feature(a,b,beta,base_radius,kind))


def predict(a,b,beta,base_radius,kind,eta):
    beta=np.asarray(beta);gap=float((score_model.features(a)-score_model.features(b))@beta);r=radius(a,b,beta,base_radius,kind,eta);direction='A' if gap>1e-7 else 'B' if gap<-1e-7 else None
    return {'predicted_direction':direction,'predicted_meaningfulness':'meaningful_difference' if abs(gap)>r else 'no_meaningful_difference','margin':gap,'base_radius':float(base_radius),'decision_radius':r,'context_feature':context_feature(a,b,beta,base_radius,kind),'context_coefficient':eta,'exact_price_equality':None,'prediction_source':'model_only'}
