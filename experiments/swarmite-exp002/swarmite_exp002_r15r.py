import json, time, numpy as np
import swarmite_benchmark_v2 as b

ACTIONS=[('FIXED',t,s) for t in range(b.N) for s in (-2.0,2.0)]

def score_eig(p,models,a,seed,step,cid,sims,ns):
    _,t,s=a; h0=b.entropy(p); hs=[]; r=b.rng_for(ns,seed,step,cid)
    for _ in range(sims):
        row=b.sim_row_from_posterior(p,models,t,s,r)
        q=b.update_p_with_row(p,models,row,t)
        hs.append(b.entropy(q))
    return (h0-float(np.mean(hs)))/b.COSTS[t]

def initial_state(world,seed):
    data=b.env_sample(world,b.rng_for('v2','obs',seed),b.OBS_N)
    targets=[None]*b.OBS_N
    fs,models=b.build_family_models(data,targets)
    return data,targets,b.posterior_from_fs(fs),models

def simulated_terminal(data0,targets0,p0,models0,seed,action_index,rollout_id):
    data=data0.copy(); targets=list(targets0); p=p0.copy(); models=models0
    _,t,s=ACTIONS[action_index]
    row=b.sim_row_from_posterior(p,models,t,s,b.rng_for('r15r-terminal-first',seed,action_index,rollout_id))
    data=np.vstack([data,row]); targets.append(t)
    fs,models=b.build_family_models(data,targets); p=b.posterior_from_fs(fs)
    spend=int(b.COSTS[t]); samples=1; step=1
    while min(b.COSTS)<=b.BUDGET-spend:
        affordable=[a for a in b.proposals(p,seed,step,0) if b.COSTS[a[1]]<=b.BUDGET-spend]
        if not affordable: break
        scores=[]
        for cid,a in enumerate(affordable):
            scores.append(score_eig(p,models,a,seed,step,cid,3,f'r15r-terminal-eig-{action_index}-{rollout_id}'))
            samples+=3
        a=affordable[int(np.argmax(scores))]; _,t,s=a
        row=b.sim_row_from_posterior(p,models,t,s,b.rng_for('r15r-terminal-env',seed,action_index,rollout_id,step,t,s)); samples+=1
        data=np.vstack([data,row]); targets.append(t); spend+=int(b.COSTS[t])
        fs,models=b.build_family_models(data,targets); p=b.posterior_from_fs(fs); step+=1
    em=b.edge_marginals(p)
    return -float(np.sum(4*em*(1-em))),samples

def real_arm(world,seed,first_action_index):
    data,targets,p,models=initial_state(world,seed)
    _,t,s=ACTIONS[first_action_index]
    row=b.env_sample(world,b.rng_for('r15r-real-env',seed,0,t,s),1,t,s)[0]
    data=np.vstack([data,row]); targets.append(t); spend=int(b.COSTS[t])
    fs,models=b.build_family_models(data,targets); p=b.posterior_from_fs(fs)
    step=1; planner_sims=0
    while min(b.COSTS)<=b.BUDGET-spend:
        affordable=[a for a in b.proposals(p,seed,step,0) if b.COSTS[a[1]]<=b.BUDGET-spend]
        if not affordable: break
        scores=[]
        for cid,a in enumerate(affordable):
            scores.append(score_eig(p,models,a,seed,step,cid,3,'r15r-real-eig')); planner_sims+=3
        a=affordable[int(np.argmax(scores))]; _,t,s=a
        row=b.env_sample(world,b.rng_for('r15r-real-env',seed,step,t,s),1,t,s)[0]
        data=np.vstack([data,row]); targets.append(t); spend+=int(b.COSTS[t])
        fs,models=b.build_family_models(data,targets); p=b.posterior_from_fs(fs); step+=1
    m=b.posterior_metrics(p,world.dag_mask); m['planner_sims']=planner_sims
    return m

def run_world(seed):
    started=time.time(); world=b.gen_world(seed); data,targets,p,models=initial_state(world,seed)
    audit=[score_eig(p,models,a,seed,0,i,30,'r15r-audit') for i,a in enumerate(ACTIONS)]
    shortlist=[int(x) for x in np.argsort(audit)[::-1][:3]]
    control=shortlist[0]; control_cost=int(b.COSTS[ACTIONS[control][1]])
    eligible=[i for i in shortlist if b.COSTS[ACTIONS[i][1]]<=control_cost]
    terminal={}; selection_samples=300
    for ai in eligible:
        vals=[]
        for rid in range(4):
            v,n=simulated_terminal(data,targets,p,models,seed,ai,rid); vals.append(v); selection_samples+=n
        terminal[ai]=float(np.mean(vals))
    treatment=max(eligible,key=lambda i:terminal[i])
    cm=real_arm(world,seed,control)
    tm=cm if treatment==control else real_arm(world,seed,treatment)
    delta=tm['edge_error']-cm['edge_error']
    return {'seed':seed,'dag_mask':world.dag_mask,'shortlist':shortlist,'eligible':eligible,'control_action':control,'treatment_action':treatment,'control_cost':control_cost,'treatment_cost':int(b.COSTS[ACTIONS[treatment][1]]),'paired_edge_delta_treatment_minus_control':delta,'paired_brier_delta':tm['brier']-cm['brier'],'paired_true_mass_delta':tm['true_mass']-cm['true_mass'],'paired_map_delta':tm['map']-cm['map'],'override':int(treatment!=control),'harmful_gt_0_10':int(delta>.10),'selection_planner_samples':selection_samples,'compute_ratio_vs_one_step_audit':selection_samples/300.0,'wall_seconds':time.time()-started}

if __name__=='__main__':
    import sys
    for seed in map(int,sys.argv[1:]): print(json.dumps(run_world(seed),separators=(',',':')))
