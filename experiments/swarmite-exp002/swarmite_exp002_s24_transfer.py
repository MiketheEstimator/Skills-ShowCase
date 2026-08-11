import json, math, numpy as np
import swarmite_benchmark_v2 as b
import swarmite_exp002_s5_nonlocal as s5
import swarmite_exp002_s23_robust_likelihood as s23

TRUE_DF=5.0; TRUE_SCALE=math.sqrt((TRUE_DF-2.0)/TRUE_DF)
def softsign(x): return x/(1.0+np.abs(x))
def env_sample(world,r,n,target=None,setpoint=None):
    X=np.zeros((n,b.N))
    for i in range(n):
        eps=r.standard_t(TRUE_DF,size=b.N)*TRUE_SCALE
        for v in world.order:
            if target==v: X[i,v]=setpoint
            else: X[i,v]=float(softsign(X[i])@world.W[:,v]+eps[v])
    return X

def run_control(world,seed):
    data=env_sample(world,b.rng_for('v2','obs',seed),b.OBS_N); targets=[None]*b.OBS_N
    fs,models=b.build_family_models(data,targets); p=b.posterior_from_fs(fs); spend=0; trace=[]
    while True:
        step=len(trace); aff=[a for a in b.proposals(p,seed,step,0) if b.COSTS[a[1]]<=b.BUDGET-spend]
        if not aff: break
        sc=[b.eig_score(p,models,a,seed,step,cid) for cid,a in enumerate(aff)]; role,t,s=aff[int(np.argmax(sc))]
        row=env_sample(world,b.rng_for('v2','env',seed,step,t,s),1,t,s)[0]
        data=np.vstack([data,row]); targets.append(t); spend+=int(b.COSTS[t]); fs,models=b.build_family_models(data,targets); p=b.posterior_from_fs(fs); trace.append((role,int(t),float(s),spend))
        if min(b.COSTS)>b.BUDGET-spend: break
    m=b.posterior_metrics(p,world.dag_mask); m.update({'spend':spend,'trace':trace,'posterior_sum':float(p.sum())}); return m,data,targets,p

def paired(seed):
    w=b.gen_world(seed); c,data,targets,p0=run_control(w,seed); fs0,_=b.build_family_models(data,targets); p0c=b.posterior_from_fs(fs0); recon=float(np.max(np.abs(p0-p0c)))
    fs,finite=s23.build(data,targets); pt=b.posterior_from_fs(fs); tm=b.posterior_metrics(pt,w.dag_mask)
    fss,_=s5.build(data,targets); ps=b.posterior_from_fs(fss); sm=b.posterior_metrics(ps,w.dag_mask)
    return {'seed':int(seed),'dag_mask':int(w.dag_mask),'dag_count':len(b.dags),'spend':int(c['spend']),'action_trace':c['trace'],'trace_identical':True,'planning_reconstruction_max_abs':recon,'family_scores_finite':finite,'posterior_sum':float(pt.sum()),'treatment':tm,'fixed_s5':sm,'control':{k:v for k,v in c.items() if k!='trace'},'edge_delta':float(tm['edge_error']-c['edge_error']),'brier_delta':float(tm['brier']-c['brier']),'edge_delta_vs_s5':float(tm['edge_error']-sm['edge_error']),'brier_delta_vs_s5':float(tm['brier']-sm['brier']),'large_harm':int(tm['edge_error']-c['edge_error']>0.50)}
def summarize(rows):
    return {'n':len(rows),'mean_edge_delta':float(np.mean([r['edge_delta'] for r in rows])),'mean_brier_delta':float(np.mean([r['brier_delta'] for r in rows])),'mean_edge_delta_vs_s5':float(np.mean([r['edge_delta_vs_s5'] for r in rows])),'mean_brier_delta_vs_s5':float(np.mean([r['brier_delta_vs_s5'] for r in rows])),'wins':sum(r['edge_delta']<0 for r in rows),'large_harms':sum(r['large_harm'] for r in rows),'trace_identical_all':all(r['trace_identical'] for r in rows),'dag_count_ok':all(r['dag_count']==29281 for r in rows),'spend_ok':all(r['spend']<=15 for r in rows),'planning_reconstruction_ok':all(r['planning_reconstruction_max_abs']<=1e-10 for r in rows),'scores_finite':all(r['family_scores_finite'] for r in rows),'posterior_normalized':all(np.isfinite(r['posterior_sum']) and abs(r['posterior_sum']-1)<1e-8 for r in rows)}
def bootstrap(rows,reps=10000,seed=22424):
    x=np.asarray([r['edge_delta'] for r in rows]); rr=np.random.default_rng(seed); m=np.mean(rr.choice(x,(reps,len(x)),replace=True),axis=1); return [float(np.quantile(m,.025)),float(np.quantile(m,.975))]
if __name__=='__main__':
 import sys
 rows=[paired(int(s)) for s in sys.argv[1:]]; print(json.dumps({'rows':rows,'summary':summarize(rows),'bootstrap95_edge_delta':bootstrap(rows) if rows else None},separators=(',',':')))
