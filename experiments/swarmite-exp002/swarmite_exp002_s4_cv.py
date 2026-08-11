import math, numpy as np
import swarmite_benchmark_v2 as b
K=5

def fit(data,idx,v,cols):
    X=data[idx][:,cols] if cols else np.empty((len(idx),0)); y=data[idx,v]; Xd=np.column_stack([np.ones(len(idx)),X]); A=np.eye(Xd.shape[1])/b.TAU2+Xd.T@Xd; C=np.linalg.inv(A); return C@(Xd.T@y),C

def build(data,targets):
    fs=np.full((b.N,1<<b.N),-1e100)
    for v in range(b.N):
        eligible=[i for i,t in enumerate(targets) if t!=v]; folds=[[i for j,i in enumerate(eligible) if j%K==f] for f in range(K)]
        for pm in range(1<<b.N):
            if pm>>v&1: continue
            cols=[u for u in range(b.N) if pm>>u&1]; score=0.0
            for f in range(K):
                hold=folds[f]; train=[i for ff in range(K) if ff!=f for i in folds[ff]]; mu,C=fit(data,train,v,cols)
                for i in hold:
                    x=np.array([1.0]+[data[i,u] for u in cols]); m=float(x@mu); var=max(1.0+float(x@C@x),1e-12); z=float(data[i,v]-m); score+=-0.5*(math.log(2*math.pi*var)+z*z/var)
            fs[v,pm]=score
    _,models=b.build_family_models(data,targets); return fs,models

def run(world,seed):
    data=b.env_sample(world,b.rng_for('v2','obs',seed),b.OBS_N); targets=[None]*b.OBS_N; fs,models=build(data,targets); p=b.posterior_from_fs(fs); spend=0; trace=[]
    while True:
        step=len(trace); aff=[a for a in b.proposals(p,seed,step,0) if b.COSTS[a[1]]<=b.BUDGET-spend]
        if not aff: break
        scores=[b.eig_score(p,models,a,seed,step,cid) for cid,a in enumerate(aff)]; role,t,s=aff[int(np.argmax(scores))]; row=b.env_sample(world,b.rng_for('v2','env',seed,step,t,s),1,t,s)[0]
        data=np.vstack([data,row]); targets.append(t); spend+=int(b.COSTS[t]); fs,models=build(data,targets); p=b.posterior_from_fs(fs); trace.append((role,int(t),float(s),spend))
        if min(b.COSTS)>b.BUDGET-spend: break
    m=b.posterior_metrics(p,world.dag_mask); m['spend']=spend; m['expected_edges']=float(b.edge_marginals(p).sum()); m['trace']=trace; return m

def paired(seed):
    w=b.gen_world(seed); c=b.run_arm(w,seed,1,'portfolio'); t=run(w,seed); return {'seed':seed,'edge_delta':t['edge_error']-c['edge_error'],'brier_delta':t['brier']-c['brier'],'map_delta':t['map']-c['map'],'true_mass_delta':t['true_mass']-c['true_mass'],'treat_expected_edges':t['expected_edges'],'true_edges':int(w.dag_mask).bit_count(),'spend':t['spend']}
