import json, math, numpy as np
import swarmite_benchmark_v2 as b
import swarmite_exp002_s5_nonlocal as s5
import swarmite_exp002_s17_compound as s17

NU=3.0; SCALE=1.0/math.sqrt(3.0); MAX_ITER=30; TOL=1e-8

def t_logpdf(r):
    z=r/SCALE
    c=math.lgamma((NU+1)/2)-math.lgamma(NU/2)-0.5*math.log(NU*math.pi)-math.log(SCALE)
    return c-0.5*(NU+1)*np.log1p((z*z)/NU)

def fit_score(X,y):
    d=X.shape[1]; prec=np.eye(d)/b.TAU2
    beta=np.linalg.solve(X.T@X+prec,X.T@y)
    for _ in range(MAX_ITER):
        res=y-X@beta; z=res/SCALE; wt=((NU+1)/(NU+z*z))/(SCALE*SCALE)
        A=X.T@(wt[:,None]*X)+prec; rhs=X.T@(wt*y); nb=np.linalg.solve(A,rhs)
        if float(np.max(np.abs(nb-beta)))<TOL: beta=nb; break
        beta=nb
    res=y-X@beta
    ll=float(np.sum(t_logpdf(res)))
    logprior=-0.5*float(beta@prec@beta)-0.5*d*math.log(2*math.pi*b.TAU2)
    penalty=0.5*d*math.log(len(y)+1.0)
    score=ll+logprior-penalty
    return float(score),beta

def build(data,targets):
    fs=np.full((b.N,1<<b.N),-1e100); finite=True
    for v in range(b.N):
        keep=np.array([t!=v for t in targets],dtype=bool); y=data[keep,v]
        for pm in range(1<<b.N):
            if pm>>v&1: continue
            cols=[u for u in range(b.N) if pm>>u&1]
            X=np.tanh(data[keep][:,cols]) if cols else np.empty((len(y),0)); X=np.column_stack([np.ones(len(y)),X])
            sc,_=fit_score(X,y); fs[v,pm]=sc; finite=finite and bool(np.isfinite(sc))
    return fs,finite

def paired(seed):
    w=b.gen_world(seed); c,data,targets,p0=s17.run_control(w,seed)
    fs0,_=b.build_family_models(data,targets); p0c=b.posterior_from_fs(fs0); recon=float(np.max(np.abs(p0-p0c)))
    fs,finite=build(data,targets); pt=b.posterior_from_fs(fs); tm=b.posterior_metrics(pt,w.dag_mask)
    fss,_=s5.build(data,targets); ps=b.posterior_from_fs(fss); sm=b.posterior_metrics(ps,w.dag_mask)
    return {'seed':int(seed),'dag_mask':int(w.dag_mask),'dag_count':len(b.dags),'spend':int(c['spend']),'action_trace':c['trace'],'trace_identical':True,
      'planning_reconstruction_max_abs':recon,'family_scores_finite':finite,'posterior_sum':float(pt.sum()),
      'treatment':tm,'fixed_s5':sm,'control':{k:v for k,v in c.items() if k!='trace'},
      'edge_delta':float(tm['edge_error']-c['edge_error']),'brier_delta':float(tm['brier']-c['brier']),
      'true_mass_delta':float(tm['true_mass']-c['true_mass']),'map_delta':int(tm['map']-c['map']),
      'edge_delta_vs_s5':float(tm['edge_error']-sm['edge_error']),'brier_delta_vs_s5':float(tm['brier']-sm['brier']),
      'large_harm':int(tm['edge_error']-c['edge_error']>0.50)}

def summarize(rows):
    return {'n':len(rows),'mean_edge_delta':float(np.mean([r['edge_delta'] for r in rows])),'mean_brier_delta':float(np.mean([r['brier_delta'] for r in rows])),
      'mean_edge_delta_vs_s5':float(np.mean([r['edge_delta_vs_s5'] for r in rows])),'mean_brier_delta_vs_s5':float(np.mean([r['brier_delta_vs_s5'] for r in rows])),
      'wins':sum(r['edge_delta']<0 for r in rows),'large_harms':sum(r['large_harm'] for r in rows),'trace_identical_all':all(r['trace_identical'] for r in rows),
      'dag_count_ok':all(r['dag_count']==29281 for r in rows),'spend_ok':all(r['spend']<=15 for r in rows),'planning_reconstruction_ok':all(r['planning_reconstruction_max_abs']<=1e-10 for r in rows),
      'scores_finite':all(r['family_scores_finite'] for r in rows),'posterior_normalized':all(np.isfinite(r['posterior_sum']) and abs(r['posterior_sum']-1)<1e-8 for r in rows)}
def bootstrap(rows,reps=10000,seed=22323):
    x=np.asarray([r['edge_delta'] for r in rows]); rr=np.random.default_rng(seed); m=np.mean(rr.choice(x,(reps,len(x)),replace=True),axis=1); return [float(np.quantile(m,.025)),float(np.quantile(m,.975))]
if __name__=='__main__':
 import sys
 rows=[paired(int(s)) for s in sys.argv[1:]]; print(json.dumps({'rows':rows,'summary':summarize(rows),'bootstrap95_edge_delta':bootstrap(rows) if rows else None},separators=(',',':')))
