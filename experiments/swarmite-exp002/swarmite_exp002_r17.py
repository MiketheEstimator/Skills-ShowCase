import json, sys, time, math
import numpy as np
import swarmite_benchmark_v2 as b

LAMBDAS=(0.0,0.25,0.5,0.75,1.0)
EDGE_COUNTS=np.array([int(m).bit_count() for m in b.dags],dtype=float)
LOG_PRIOR_BASE=EDGE_COUNTS*math.log(0.35)+(10.0-EDGE_COUNTS)*math.log(0.65)

def posterior_from_fs_lambda(fs,lam):
    ls=np.zeros(len(b.dags))
    for v in range(b.N): ls += fs[v,b.parents[:,v]]
    if lam: ls += float(lam)*LOG_PRIOR_BASE
    ls-=ls.max(); p=np.exp(ls); p/=p.sum(); return p

def run_arm_lambda(world,seed,lam):
    data=b.env_sample(world,b.rng_for('v2','obs',seed),b.OBS_N); targets=[None]*b.OBS_N
    fs,models=b.build_family_models(data,targets); p=posterior_from_fs_lambda(fs,lam)
    spend=0; trace=[]; planner_sims=0
    while True:
        step=len(trace); allc=b.proposals(p,seed,step,0)
        affordable=[a for a in allc if b.COSTS[a[1]]<=b.BUDGET-spend]
        if not affordable: break
        scores=[]
        for cid,a in enumerate(affordable):
            scores.append(b.eig_score(p,models,a,seed,step,cid)); planner_sims+=b.EIG_SIMS
        pick=int(np.argmax(scores)); role,target,setpoint=affordable[pick]
        row=b.env_sample(world,b.rng_for('v2','env',seed,step,target,setpoint),1,target,setpoint)[0]
        data=np.vstack([data,row]); targets.append(target); spend+=int(b.COSTS[target])
        fs,models=b.build_family_models(data,targets); p=posterior_from_fs_lambda(fs,lam)
        trace.append({'step':step,'role':role,'target':int(target),'setpoint':setpoint,'cost':int(b.COSTS[target]),'spend':spend})
        if min(b.COSTS)>b.BUDGET-spend: break
    m=b.posterior_metrics(p,world.dag_mask)
    m.update({'spend':spend,'interventions':len(trace),'planner_sims':planner_sims})
    return m

def run_world(seed):
    t=time.time(); w=b.gen_world(seed); arms={}
    for lam in LAMBDAS: arms[str(lam)]=run_arm_lambda(w,seed,lam)
    base=arms['0.0']
    deltas={k:{'edge_delta':v['edge_error']-base['edge_error'],'brier_delta':v['brier']-base['brier'],'map_delta':v['map']-base['map'],'true_mass_delta':v['true_mass']-base['true_mass']} for k,v in arms.items()}
    return {'seed':seed,'dag_mask':w.dag_mask,'arms':arms,'deltas_vs_lambda0':deltas,'wall_seconds':time.time()-t}

def summarize(rows):
    out={}
    for lam in LAMBDAS:
        k=str(lam); ds=np.array([r['deltas_vs_lambda0'][k]['edge_delta'] for r in rows]); bs=np.array([r['deltas_vs_lambda0'][k]['brier_delta'] for r in rows])
        out[k]={'mean_edge_delta':float(ds.mean()),'mean_brier_delta':float(bs.mean()),'wins':int((ds<0).sum()),'losses':int((ds>0).sum()),'harm_gt_0_50':int((ds>0.50).sum())}
    eligible=[lam for lam in LAMBDAS if out[str(lam)]['mean_brier_delta']<=0.005]
    best=min(eligible,key=lambda x:(out[str(x)]['mean_edge_delta'],x))
    best_err=out[str(best)]['mean_edge_delta']
    tied=[x for x in eligible if out[str(x)]['mean_edge_delta']<=best_err+0.01]
    selected=min(tied)
    return {'n':len(rows),'by_lambda':out,'selected_lambda':selected,'selection_rule':'minimum mean edge delta subject to mean Brier delta <= +0.005; within 0.01 choose smaller lambda'}

if __name__=='__main__':
    rows=[run_world(int(s)) for s in sys.argv[1:]]
    print(json.dumps({'rows':rows,'summary':summarize(rows)},separators=(',',':')))
