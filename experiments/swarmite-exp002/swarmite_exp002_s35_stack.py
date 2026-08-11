import json, numpy as np
import swarmite_benchmark_v2 as b
import swarmite_exp002_s33_expand as s33
import swarmite_exp002_s32_modelset_diag as s32

CLASSES=s33.CLASSES
T=s33.T

def components(seed):
    w=b.gen_world(seed); c,data,targets,p0,cell=s32.run_control(w,seed)
    posts={}; finite=True
    for name in CLASSES:
        if name=='LG': posts[name]=p0.copy(); ok=True
        else: posts[name],ok=s33.build_class(data,targets,name)
        finite=finite and ok
    lg=s33.cv_score(data,targets,'LG'); tt=s33.cv_score(data,targets,'TT'); alpha=s33.sigmoid((tt-lg)/T)
    ps30=(1-alpha)*posts['LG']+alpha*posts['TT']; ps30/=ps30.sum()
    cls_metrics={n:b.posterior_metrics(posts[n],w.dag_mask) for n in CLASSES}; s30m=b.posterior_metrics(ps30,w.dag_mask); base=b.posterior_metrics(p0,w.dag_mask)
    return {'seed':int(seed),'cell':cell,'world':w,'posts':posts,'class_metrics':cls_metrics,'s30':s30m,'base':base,'alpha':float(alpha),'finite':finite,'spend':int(c['spend']),'trace_identical':True}

def train_weights(rows):
    rng=np.random.default_rng(35235)
    cand=[np.eye(len(CLASSES))[i] for i in range(len(CLASSES))]+[np.ones(len(CLASSES))/len(CLASSES)]
    cand.extend(rng.dirichlet(np.ones(len(CLASSES)),size=20000))
    cells=s32.CELLS
    best=None; bestkey=None
    for w in cand:
        deltas=[]; cellmeans=[]
        for r in rows:
            mix=sum(w[i]*r['class_metrics'][n]['edge_error'] for i,n in enumerate(CLASSES)); d=mix-r['s30']['edge_error']; deltas.append(d)
        for c in cells:
            z=[d for d,r in zip(deltas,rows) if r['cell']==c]; cellmeans.append(float(np.mean(z)))
        key=(max(cellmeans),float(np.mean(deltas)),float(np.sum(np.square(w))))
        if bestkey is None or key<bestkey: bestkey=key; best=w.copy()
    return {n:float(best[i]) for i,n in enumerate(CLASSES)}, {'worst_cell_delta':float(bestkey[0]),'mean_delta':float(bestkey[1]),'l2':float(bestkey[2])}

def evaluate(seed,weights):
    r=components(seed); p=np.zeros_like(next(iter(r['posts'].values())))
    for n in CLASSES: p += weights[n]*r['posts'][n]
    p/=p.sum(); m=b.posterior_metrics(p,r['world'].dag_mask); ed=float(m['edge_error']-r['s30']['edge_error']); bd=float(m['brier']-r['s30']['brier'])
    return {'seed':r['seed'],'cell':r['cell'],'weights':weights,'edge_delta_vs_s30':ed,'brier_delta_vs_s30':bd,'edge_delta_vs_baseline':float(m['edge_error']-r['base']['edge_error']),'large_harm_vs_s30':int(ed>0.5),'spend':r['spend'],'trace_identical':True,'finite':r['finite'],'posterior_sum':float(p.sum())}

def boot(x,reps=10000,seed=23535):
    x=np.asarray(x,float); rr=np.random.default_rng(seed); m=np.mean(rr.choice(x,(reps,len(x)),replace=True),axis=1); return [float(np.quantile(m,.025)),float(np.quantile(m,.975))]

def summarize(rows):
    ed=[r['edge_delta_vs_s30'] for r in rows]; by={}
    for c in s32.CELLS:
        z=[r for r in rows if r['cell']==c]; by[c]=float(np.mean([r['edge_delta_vs_s30'] for r in z]))
    sm={'n':len(rows),'mean_edge_delta_vs_s30':float(np.mean(ed)),'bootstrap95_edge_delta_vs_s30':boot(ed),'mean_brier_delta_vs_s30':float(np.mean([r['brier_delta_vs_s30'] for r in rows])),'large_harms_vs_s30':sum(r['large_harm_vs_s30'] for r in rows),'mean_edge_delta_vs_baseline':float(np.mean([r['edge_delta_vs_baseline'] for r in rows])),'by_cell_mean_edge_delta_vs_s30':by,'mechanics_ok':all(r['spend']<=15 and r['trace_identical'] and r['finite'] and abs(r['posterior_sum']-1)<1e-8 for r in rows)}
    return sm
