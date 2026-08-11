import json, math, numpy as np
import swarmite_benchmark_v2 as b
import swarmite_exp002_s32_modelset_diag as s32
import swarmite_exp002_s33_expand as s33
import swarmite_exp002_s39_credal as s39
import swarmite_exp002_s41_density as s41
import swarmite_exp002_s42_worldclass as s42

SPECIALISTS=s39.SPECIALISTS
CREDAL_THRESHOLD=0.2692013432171404

def row(seed):
    w,den=s41.gen_world(seed); c,data,targets,p0,cell=s32.run_control(w,seed); fs,_=b.build_family_models(data,targets)
    es=s42.class_logevidence(fs,.15); ed=s42.class_logevidence(fs,.55); m=max(es,ed); qs=math.exp(es-m); qd=math.exp(ed-m); qdense=float(qd/(qs+qd))
    posts={'LG':p0.copy()}; finite=True
    for n in s33.CLASSES:
        if n=='LG': continue
        posts[n],ok=s33.build_class(data,targets,n); finite=finite and ok
    lg=s33.cv_score(data,targets,'LG'); tt=s33.cv_score(data,targets,'TT'); alpha=s33.sigmoid((tt-lg)/s33.T); ps30=(1-alpha)*posts['LG']+alpha*posts['TT']; ps30/=ps30.sum()
    em0=b.edge_marginals(ps30); ems=np.vstack([b.edge_marginals(posts[n]) for n in SPECIALISTS]); widths=np.max(np.vstack([em0,ems]),axis=0)-np.min(np.vstack([em0,ems]),axis=0); credal=float(np.mean(widths))
    base=b.posterior_metrics(p0,w.dag_mask); s30m=b.posterior_metrics(ps30,w.dag_mask); edge=float(s30m['edge_error']-base['edge_error']); br=float(s30m['brier']-base['brier'])
    return {'seed':int(seed),'density':den,'truth_dense':int(den=='dense'),'cell':cell,'p_dense':qdense,'credal_width':credal,'s30_edge_delta_vs_baseline':edge,'s30_brier_delta_vs_baseline':br,'s30_large_harm':int(edge>.50),'spend':int(c['spend']),'finite':bool(finite and np.isfinite(qdense)),'s30_sum':float(ps30.sum())}

def fit(rows):
    out={}
    for den in ('sparse','dense'):
        rr=[r for r in rows if r['density']==den]; out[den]={'mean_edge_delta':float(np.mean([r['s30_edge_delta_vs_baseline'] for r in rr])),'large_harm_rate':float(np.mean([r['s30_large_harm'] for r in rr])),'n':len(rr)}
    return out

def boot(x,reps=10000,seed=24343):
    x=np.asarray(x,float); rr=np.random.default_rng(seed); mm=np.mean(rr.choice(x,(reps,len(x)),replace=True),axis=1); return [float(np.quantile(mm,.025)),float(np.quantile(mm,.975))]
def mechanics(rows): return all(r['spend']<=15 and r['finite'] and abs(r['s30_sum']-1)<1e-8 and 0<=r['p_dense']<=1 for r in rows)
def summarize(rows,params):
    ed=np.array([r['s30_edge_delta_vs_baseline'] for r in rows]); bd=np.array([r['s30_brier_delta_vs_baseline'] for r in rows]); q=np.array([r['p_dense'] for r in rows]); cw=np.array([r['credal_width'] for r in rows]);
    mud=params['dense']['mean_edge_delta']*q+params['sparse']['mean_edge_delta']*(1-q); harm=params['dense']['large_harm_rate']*q+params['sparse']['large_harm_rate']*(1-q); ca=(mud<0)&(harm<=.05); ctrl=cw<=CREDAL_THRESHOLD
    def stats(mask):
        he=np.where(mask,ed,0.); hb=np.where(mask,bd,0.); always=float(np.mean(ed)); hy=float(np.mean(he)); ret=float(abs(hy)/abs(always)) if always<0 else 1.0
        return {'coverage':float(np.mean(mask)),'n_promoted':int(np.sum(mask)),'promoted_large_harms':int(np.sum((ed>.5)&mask)),'promoted_large_harm_rate':float(np.sum((ed>.5)&mask)/max(1,np.sum(mask))),'always_s30_mean_edge_delta':always,'hybrid_mean_edge_delta':hy,'bootstrap95_hybrid_edge_delta':boot(he,seed=24343+len(rows)+int(np.sum(mask))),'hybrid_mean_brier_delta':float(np.mean(hb)),'improvement_retained':ret}
    return {'n':len(rows),'class_aware':stats(ca),'s39_control':stats(ctrl),'mechanics_ok':mechanics(rows)}
def passed(s,confirm=False):
    m=s['class_aware']; c=s['s39_control']; ok=s['mechanics_ok'] and m['coverage']>=.60 and m['promoted_large_harm_rate']<=.05 and m['hybrid_mean_edge_delta']<0 and m['hybrid_mean_brier_delta']<=.005 and (m['always_s30_mean_edge_delta']>=0 or m['improvement_retained']>=.70) and m['hybrid_mean_edge_delta']<=c['hybrid_mean_edge_delta']+.02
    return ok and ((not confirm) or m['bootstrap95_hybrid_edge_delta'][1]<0)
def run():
    tr=[row(s) for s in range(73101,73149)]; params=fit(tr); out={'training':{'params':params,'summary':summarize(tr,params)}}
    if not mechanics(tr): out['disposition']='BLOCKED_MECHANICS'; return out
    va=[row(s) for s in range(73161,73197)]; vs=summarize(va,params); out['validation']=vs
    if not passed(vs): out['disposition']='FALSIFIED_ON_VALIDATION'; return out
    co=[row(s) for s in range(73201,73249)]; cs=summarize(co,params); out['confirmation']=cs; out['disposition']='CLASS_AWARE_DECISION_SUPPORTED' if passed(cs,True) else 'FALSIFIED_ON_CONFIRMATION'; return out
if __name__=='__main__': print(json.dumps(run(),separators=(',',':')))
