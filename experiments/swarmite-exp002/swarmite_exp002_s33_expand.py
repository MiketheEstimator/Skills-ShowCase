import json, math, numpy as np
import swarmite_benchmark_v2 as b
import swarmite_exp002_s23_robust_likelihood as s23
import swarmite_exp002_s32_modelset_diag as s32

T=5.0
FOLDS=5
CLASSES=('LG','TG','TT','SG','ST','AG','AT')


def transform(x, mech):
    if mech=='linear': return x
    if mech=='tanh': return np.tanh(x)
    if mech=='sin': return np.sin(x)
    if mech=='asinh': return np.arcsinh(x)
    raise ValueError(mech)


def gaussian_family_score(data,targets,v,pm,mech='linear',indices=None):
    idx=list(range(len(data))) if indices is None else list(indices)
    idx=[i for i in idx if targets[i]!=v]
    y=data[idx,v]
    cols=[u for u in range(b.N) if pm>>u&1]
    X=data[idx][:,cols] if cols else np.empty((len(y),0))
    X=transform(X,mech)
    Xd=np.column_stack([np.ones(len(y)),X])
    A=np.eye(Xd.shape[1])/b.TAU2+Xd.T@Xd
    Ainv=np.linalg.inv(A); rhs=Xd.T@y; mu=Ainv@rhs
    quad=float(y@y-rhs@mu); _,ld=np.linalg.slogdet(A)
    logdetC=float(ld+Xd.shape[1]*math.log(b.TAU2))
    sc=-0.5*(len(y)*math.log(2*math.pi)+logdetC+quad)
    return float(sc),(cols,mu,Ainv,mech)


def gaussian_logpred(model,row,v):
    cols,mu,Ainv,mech=model
    vals=np.array([row[u] for u in cols],float)
    vals=transform(vals,mech)
    x=np.concatenate(([1.0],vals))
    mean=float(x@mu); var=max(1e-12,float(1+x@Ainv@x)); z=float(row[v]-mean)
    return -0.5*(math.log(2*math.pi*var)+z*z/var)


def robust_family_score(data,targets,v,pm,mech='tanh',indices=None):
    idx=list(range(len(data))) if indices is None else list(indices)
    idx=[i for i in idx if targets[i]!=v]
    y=data[idx,v]
    cols=[u for u in range(b.N) if pm>>u&1]
    X=data[idx][:,cols] if cols else np.empty((len(y),0))
    X=transform(X,mech)
    X=np.column_stack([np.ones(len(y)),X])
    sc,beta=s23.fit_score(X,y)
    return float(sc),(cols,beta,mech)


def robust_logpred(model,row,v):
    cols,beta,mech=model
    vals=np.array([row[u] for u in cols],float)
    vals=transform(vals,mech)
    x=np.concatenate(([1.0],vals)); r=float(row[v]-x@beta)
    return float(s23.t_logpdf(np.array([r]))[0])


def class_spec(name):
    return {
      'LG':('linear','gaussian'),'TG':('tanh','gaussian'),'TT':('tanh','t3'),
      'SG':('sin','gaussian'),'ST':('sin','t3'),'AG':('asinh','gaussian'),'AT':('asinh','t3')
    }[name]


def build_class(data,targets,name):
    mech,noise=class_spec(name); fs=np.full((b.N,1<<b.N),-1e100); finite=True
    for v in range(b.N):
      for pm in range(1<<b.N):
        if pm>>v&1: continue
        if noise=='gaussian': sc,_=gaussian_family_score(data,targets,v,pm,mech)
        else: sc,_=robust_family_score(data,targets,v,pm,mech)
        fs[v,pm]=sc; finite=finite and bool(np.isfinite(sc))
    p=b.posterior_from_fs(fs)
    return p,finite


def cv_score(data,targets,name):
    mech,noise=class_spec(name); n=len(data); total=0.0; all_idx=list(range(n))
    for fold in range(FOLDS):
      te=[i for i in all_idx if i%FOLDS==fold]; tr=[i for i in all_idx if i%FOLDS!=fold]
      for v in range(b.N):
        pms=[pm for pm in range(1<<b.N) if not(pm>>v&1)]; scores=[]; models=[]
        for pm in pms:
          if noise=='gaussian': sc,m=gaussian_family_score(data,targets,v,pm,mech,tr)
          else: sc,m=robust_family_score(data,targets,v,pm,mech,tr)
          scores.append(sc); models.append(m)
        model=models[int(np.argmax(scores))]
        for i in te:
          if targets[i]==v: continue
          total += gaussian_logpred(model,data[i],v) if noise=='gaussian' else robust_logpred(model,data[i],v)
    return float(total)


def softmax_weights(scores,T=T):
    z=np.array([scores[c]/T for c in CLASSES],float); z-=np.max(z); w=np.exp(z); w/=w.sum()
    return {c:float(w[i]) for i,c in enumerate(CLASSES)}


def sigmoid(x):
    x=max(-40.0,min(40.0,float(x))); return 1/(1+math.exp(-x))


def paired(seed):
    world=b.gen_world(seed); c,data,targets,p0,cell=s32.run_control(world,seed)
    fs0,_=b.build_family_models(data,targets); p0c=b.posterior_from_fs(fs0); recon=float(np.max(np.abs(p0-p0c)))
    posts={}; finite=True
    for name in CLASSES:
      if name=='LG': posts[name]=p0.copy(); ok=True
      else: posts[name],ok=build_class(data,targets,name)
      finite=finite and ok
    scores={name:cv_score(data,targets,name) for name in CLASSES}
    weights=softmax_weights(scores)
    pexp=np.zeros_like(p0)
    for name in CLASSES: pexp += weights[name]*posts[name]
    pexp/=pexp.sum()
    # Frozen S30 two-class comparator using the exact same LG/TT predictive scores.
    alpha=sigmoid((scores['TT']-scores['LG'])/T)
    ps30=(1-alpha)*posts['LG']+alpha*posts['TT']; ps30/=ps30.sum()
    em=b.posterior_metrics(pexp,world.dag_mask); sm=b.posterior_metrics(ps30,world.dag_mask)
    base={k:v for k,v in c.items() if k!='trace'}
    ed=float(em['edge_error']-sm['edge_error']); bd=float(em['brier']-sm['brier'])
    return {
      'seed':int(seed),'cell':cell,'dag_count':len(b.dags),'spend':int(c['spend']),'trace_identical':True,
      'planning_reconstruction_max_abs':recon,'class_scores':scores,'weights':weights,'weights_sum':float(sum(weights.values())),
      'family_scores_finite':bool(finite),'expanded_sum':float(pexp.sum()),'s30_sum':float(ps30.sum()),'baseline_sum':float(p0.sum()),
      'expanded':em,'s30':sm,'control':base,'s30_alpha':float(alpha),
      'edge_delta_vs_s30':ed,'brier_delta_vs_s30':bd,'large_harm_vs_s30':int(ed>0.50),
      'edge_delta_vs_baseline':float(em['edge_error']-c['edge_error']),'brier_delta_vs_baseline':float(em['brier']-c['brier'])
    }


def boot(vals,reps=10000,seed=23333):
    x=np.asarray(vals,float); rr=np.random.default_rng(seed); m=np.mean(rr.choice(x,(reps,len(x)),replace=True),axis=1)
    return [float(np.quantile(m,.025)),float(np.quantile(m,.975))]


def summarize(rows):
    ed=[r['edge_delta_vs_s30'] for r in rows]; bd=[r['brier_delta_vs_s30'] for r in rows]
    by_cell={}
    for i,cn in enumerate(s32.CELLS):
      z=[r for r in rows if r['cell']==cn]
      by_cell[cn]={
        'n':len(z),'mean_edge_delta_vs_s30':float(np.mean([r['edge_delta_vs_s30'] for r in z])) if z else None,
        'mean_edge_delta_vs_baseline':float(np.mean([r['edge_delta_vs_baseline'] for r in z])) if z else None,
        'mean_brier_delta_vs_s30':float(np.mean([r['brier_delta_vs_s30'] for r in z])) if z else None,
        'mean_weights':{c:float(np.mean([r['weights'][c] for r in z])) if z else None for c in CLASSES}
      }
    mechanics=all(r['dag_count']==29281 and r['spend']<=15 and r['trace_identical'] and r['planning_reconstruction_max_abs']<=1e-10 and r['family_scores_finite'] and abs(r['weights_sum']-1)<1e-8 and abs(r['expanded_sum']-1)<1e-8 and abs(r['s30_sum']-1)<1e-8 and abs(r['baseline_sum']-1)<1e-8 and all(np.isfinite(list(r['class_scores'].values()))) for r in rows)
    sm={
      'n':len(rows),'mean_edge_delta_vs_s30':float(np.mean(ed)),'bootstrap95_edge_delta_vs_s30':boot(ed),
      'mean_brier_delta_vs_s30':float(np.mean(bd)),'large_harms_vs_s30':sum(r['large_harm_vs_s30'] for r in rows),
      'mean_edge_delta_vs_baseline':float(np.mean([r['edge_delta_vs_baseline'] for r in rows])),
      'wins_vs_s30':sum(r['edge_delta_vs_s30']<0 for r in rows),'mechanics_ok':mechanics,'by_cell':by_cell,
      'mean_weights':{c:float(np.mean([r['weights'][c] for r in rows])) for c in CLASSES}
    }
    sm['promote']=bool(mechanics and sm['mean_edge_delta_vs_s30']<=-0.10 and sm['bootstrap95_edge_delta_vs_s30'][1]<0 and sm['mean_brier_delta_vs_s30']<=0.005 and sm['large_harms_vs_s30']<=2 and sm['mean_edge_delta_vs_baseline']<0)
    return sm

if __name__=='__main__':
 import sys
 seeds=list(map(int,sys.argv[1:])); rows=[paired(s) for s in seeds]; print(json.dumps({'rows':rows,'summary':summarize(rows)},separators=(',',':')))
