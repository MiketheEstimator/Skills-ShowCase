import math,itertools,numpy as np
import swarmite_benchmark_v2 as b
import swarmite_exp002_s5_nonlocal as s5

def env_sample_nonlinear(world,r,n,target=None,setpoint=None):
    X=np.zeros((n,b.N))
    for i in range(n):
        for v in world.order:
            if target==v: X[i,v]=setpoint
            else: X[i,v]=float(np.tanh(X[i])@world.W[:,v]+r.normal())
    return X

def run_control(world,seed):
    data=env_sample_nonlinear(world,b.rng_for('v2','obs',seed),b.OBS_N); targets=[None]*b.OBS_N
    fs,models=b.build_family_models(data,targets); p=b.posterior_from_fs(fs); spend=0; trace=[]
    while True:
        step=len(trace); aff=[a for a in b.proposals(p,seed,step,0) if b.COSTS[a[1]]<=b.BUDGET-spend]
        if not aff: break
        sc=[b.eig_score(p,models,a,seed,step,cid) for cid,a in enumerate(aff)]
        role,t,s=aff[int(np.argmax(sc))]
        row=env_sample_nonlinear(world,b.rng_for('v2','env',seed,step,t,s),1,t,s)[0]
        data=np.vstack([data,row]); targets.append(t); spend+=int(b.COSTS[t])
        fs,models=b.build_family_models(data,targets); p=b.posterior_from_fs(fs)
        trace.append({'step':step,'role':role,'target':int(t),'setpoint':float(s),'spend':spend})
        if min(b.COSTS)>b.BUDGET-spend: break
    m=b.posterior_metrics(p,world.dag_mask); m.update({'spend':spend,'trace':trace})
    return m,data,targets

def paired(seed):
    w=b.gen_world(seed); c,data,targets=run_control(w,seed)
    fs,_=s5.build(data,targets); p=b.posterior_from_fs(fs); t=b.posterior_metrics(p,w.dag_mask)
    trace=[(x['role'],x['target'],x['setpoint'],x['spend']) for x in c['trace']]
    return {'seed':seed,'dag_mask':w.dag_mask,'dag_count':len(b.dags),'posterior_sum':float(p.sum()),'spend':c['spend'],'action_trace':trace,'edge_delta':t['edge_error']-c['edge_error'],'brier_delta':t['brier']-c['brier'],'map_delta':t['map']-c['map'],'true_mass_delta':t['true_mass']-c['true_mass'],'trace_identical':True,'control':c,'treatment':t}

if __name__=='__main__':
    import sys,json
    print(json.dumps([paired(int(s)) for s in sys.argv[1:]],separators=(',',':')))
