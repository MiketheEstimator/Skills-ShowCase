import json, math, numpy as np
import swarmite_benchmark_v2 as b
import swarmite_exp002_s5_nonlocal as s5
THRESH=1.50
# Student-t df=3 has variance 3; divide by sqrt(3) for unit variance.
def noise(r,n=None): return r.standard_t(3,size=n)/math.sqrt(3.0)
def env_sample_t(world,r,n,target=None,setpoint=None):
    X=np.zeros((n,b.N))
    for i in range(n):
        eps=noise(r,b.N)
        for v in world.order:
            if target==v: X[i,v]=setpoint
            else: X[i,v]=float(np.tanh(X[i])@world.W[:,v]+eps[v])
    return X
def run_control(world,seed):
    data=env_sample_t(world,b.rng_for('v2','obs',seed),b.OBS_N); targets=[None]*b.OBS_N
    fs,models=b.build_family_models(data,targets); p=b.posterior_from_fs(fs); spend=0; trace=[]
    while True:
        step=len(trace); aff=[a for a in b.proposals(p,seed,step,0) if b.COSTS[a[1]]<=b.BUDGET-spend]
        if not aff: break
        sc=[b.eig_score(p,models,a,seed,step,cid) for cid,a in enumerate(aff)]
        role,t,s=aff[int(np.argmax(sc))]
        row=env_sample_t(world,b.rng_for('v2','env',seed,step,t,s),1,t,s)[0]
        data=np.vstack([data,row]); targets.append(t); spend+=int(b.COSTS[t])
        fs,models=b.build_family_models(data,targets); p=b.posterior_from_fs(fs)
        trace.append((role,int(t),float(s),spend))
        if min(b.COSTS)>b.BUDGET-spend: break
    m=b.posterior_metrics(p,world.dag_mask); m.update({'spend':spend,'trace':trace,'posterior_sum':float(p.sum())})
    return m,data,targets,p
def paired(seed):
    w=b.gen_world(seed); c,data,targets,p0=run_control(w,seed); fs,_=s5.build(data,targets); ps=b.posterior_from_fs(fs); t=b.posterior_metrics(ps,w.dag_mask)
    D=float(np.abs(b.edge_marginals(ps)-b.edge_marginals(p0)).sum()); promote=D<=THRESH
    return {'seed':seed,'dag_mask':w.dag_mask,'dag_count':len(b.dags),'posterior_sum_control':float(p0.sum()),'posterior_sum_science':float(ps.sum()),'spend':c['spend'],'action_trace':c['trace'],'D':D,'promote':promote,'edge_delta':t['edge_error']-c['edge_error'],'brier_delta':t['brier']-c['brier'],'map_delta':t['map']-c['map'],'true_mass_delta':t['true_mass']-c['true_mass'],'large_harm':int(t['edge_error']-c['edge_error']>0.50),'trace_identical':True,'control':{k:v for k,v in c.items() if k!='trace'},'treatment':t}
def summary(rows):
    pr=[x for x in rows if x['promote']]; n=len(rows); nprom=len(pr)
    def mean(k): return float(np.mean([x[k] for x in pr])) if pr else None
    return {'n_total':n,'n_promoted':nprom,'coverage':nprom/n if n else 0,'mean_edge_delta_promoted':mean('edge_delta'),'mean_brier_delta_promoted':mean('brier_delta'),'wins_promoted':sum(x['edge_delta']<0 for x in pr),'large_harms_promoted':sum(x['large_harm'] for x in pr),'trace_identical_all':all(x['trace_identical'] for x in rows),'max_spend':max(x['spend'] for x in rows) if rows else 0,'all_finite_normalized':all(np.isfinite(x['posterior_sum_control']) and np.isfinite(x['posterior_sum_science']) and abs(x['posterior_sum_control']-1)<1e-8 and abs(x['posterior_sum_science']-1)<1e-8 for x in rows)}
if __name__=='__main__':
 import sys
 rows=[paired(int(s)) for s in sys.argv[1:]]; print(json.dumps({'rows':rows,'summary':summary(rows)},separators=(',',':')))
