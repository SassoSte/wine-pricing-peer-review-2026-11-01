"""Canonical pair predictor. Runtime dependencies: NumPy and one JSON configuration.

No training modules, historical model imports, evidence retrieval, or answer lookup.
Scores are comparative preferences, not monetary prices. Unresolved evidence is not
converted into a tie; confidence/abstention behaviour is deliberately unchanged.
"""
from pathlib import Path
import argparse
import json
import numpy as np

DEFAULT_CONFIG=Path(__file__).with_name('model-config.json')

class Model:
    def __init__(self,path=DEFAULT_CONFIG):
        self.config=json.loads(Path(path).read_text())
        c=self.config
        if c['schema_version']!=1:raise ValueError('Unsupported configuration schema')
        self.domain=c['domain'];self.domestic=set(self.domain['domestic'])
        self.weights=np.asarray(c['weights']['fitted'],dtype=float)
        self.reference=np.asarray(c['weights']['offset_reference'],dtype=float)
        self.provenance_reference=np.asarray(c['boundary']['provenance_reference_weights'],dtype=float)
        if self.weights.shape!=(19,) or self.reference.shape!=(19,) or self.provenance_reference.shape!=(9,):raise ValueError('Invalid weight dimensions')
        if not all(np.all(np.isfinite(v)) for v in (self.weights,self.reference,self.provenance_reference)):raise ValueError('Nonfinite weights')
        if c['boundary']['base_radius']<=0:raise ValueError('Invalid decision radius')
        for v in (self.weights,self.reference,self.provenance_reference):v.setflags(write=False)

    def _features(self,option):
        if len(option)!=4:raise ValueError('Expected provenance, shade, vintage years, tare lb')
        zone,shade,age,tare=option;d=self.domain
        if zone not in d['provenances'] or shade not in d['shades'] or age not in d['vintage_years'] or tare not in d['tare_lb']:raise ValueError(f'Unsupported option: {option}')
        return np.array([float(zone==z) for z in d['provenances'][1:]]+[float(d['shades'].index(shade)>=i) for i in range(1,5)]+[float(d['vintage_years'].index(age)>=i) for i in range(1,5)]+[(130-tare)/5,float(zone in self.domestic and shade=='pale/straw')])

    def _numeric(self,pairs):
        c=self.config;sc=c['shade_context'];fy=c['five_year'];off=c['offsets'];bound=c['boundary'];scale=bound['base_radius']
        if not pairs:return np.array([]),np.array([])
        raw=np.array([self._features(a)-self._features(b) for a,b in pairs]);shade=raw.copy();eligible=[];older=[];micro=[];context=[]
        for i,(a,b) in enumerate(pairs):
            contrast={a[1],b[1]}==set(sc['contrast'])
            if contrast:
                pale=a if a[1]=='pale/straw' else b;dom=pale[0] in self.domestic;tare=min(a[3],b[3]);young=min(a[2],b[2])==20
                shrink=sc['foreign_125_discount'] if tare>=125 else sc['foreign_120_discount'] if tare>=120 else 0.
                shrink=shrink+(1-shrink)*sc['youngest20_extra_discount']*young
                if dom:shrink=0.
                if tare>=sc['zero_premium_tare']:shrink=1.
                delta=(1 if b[1]=='pale/straw' else -1)*shrink;shade[i,12]+=delta
                if dom:shade[i,18]+=delta
            five=a[0]==b[0] and abs(a[2]-b[2])==fy['gap_years']
            if fy['scope']=='adjacent_shade':five=five and contrast
            eligible.append(five)
            older.append(a[0]==b[0] and {a[2],b[2]}==set(off['older_vintages']) and {a[1],b[1]}==set(off['older_shades']))
            micro.append(a[0]==b[0] and a[2:]==b[2:] and {a[1],b[1]}==set(off['micro_shades']))
            matched=a[0]!=b[0] and a[1]==b[1] and a[2]==b[2] and abs(a[3]-b[3])<=bound['matched_tare_limit']
            if not matched:context.append(0.);continue
            kind=bound['context_kind']
            if kind=='mature_shade':level=float(a[2]>=bound['old_vintage'] or (a[2]>=bound['brown_vintage'] and a[1]=='brown'))
            elif kind=='matched_control':level=1.
            elif kind=='shared_light_tare':level=(130-(a[3]+b[3])/2)/20
            else:raise ValueError('Unsupported boundary context')
            prov=abs(float(raw[i,:9]@self.provenance_reference));context.append(float(level*(1./(1.+prov/float(scale)))))
        eligible=np.array(eligible);adjusted=shade.copy();adjusted[:,13:17]+=fy['fraction']*raw[:,13:17]*eligible[:,None]
        # Preserve original operation order, including reference cancellation.
        age_delta=np.array([float(raw[i,13:17]@self.reference[13:17]) if yes else 0. for i,yes in enumerate(eligible)])
        legacy_gap=shade@self.reference+fy['fraction']*age_delta
        room=max(0.,scale*off['microshade_headroom_factor']-self.reference[10])
        offsets=np.column_stack([raw[:,13]*scale*np.array(older),raw[:,9]*scale,raw[:,10]*room*np.array(micro)])
        legacy_gap=legacy_gap+offsets@np.array([off['older_vintage_scale'],off['brown_step_scale'],off['microshade_scale']])
        correction=legacy_gap-adjusted@self.reference
        margins=adjusted@self.weights+correction
        context=np.array(context);radii=scale*(1+bound['context_scale']*context)+bound['additional_context_scale']*(scale*context)
        return margins,radii

    def compare_many(self,pairs):
        pairs=list(pairs);margins,radii=self._numeric(pairs);c=self.config['classification'];results=[]
        for gap,radius in zip(margins,radii):
            g=float(gap);r=float(radius)
            results.append({'predicted_direction':'A' if g>c['direction_epsilon'] else 'B' if g<-c['direction_epsilon'] else None,'predicted_meaningfulness':'meaningful_difference' if abs(g)>r+c['meaningfulness_epsilon'] else 'no_meaningful_difference','margin':g,'decision_radius':r,'exact_price_equality':c['exact_price_equality'],'prediction_source':'model_only','units':c['units'],'model':self.config['model_id']})
        return results

    def compare(self,a,b):
        return self.compare_many([(a,b)])[0]

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--a',required=True);p.add_argument('--b',required=True);p.add_argument('--config',default=str(DEFAULT_CONFIG));args=p.parse_args();print(json.dumps(Model(args.config).compare(json.loads(args.a),json.loads(args.b)),indent=2))
if __name__=='__main__':main()
