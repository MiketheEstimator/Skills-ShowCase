import json,sys,numpy as np
import swarmite_benchmark_v2 as b

def scaled_props(p,seed,step):
    return [(role,t,float(s*2.0)) for role,t,s in b.proposals(p,seed,step,0)]

def run_treat(w,seed):
    data=b.env_sample(w,b.rng_for('v2','obs',seed),b.OBS_N); targets=[None]*b.OBS_N; fs,models=b.build_family_models(data,targets); p=b.posterior_from_fs(fs); spend=0; sims=0; trace=[]
    while True:
        step=len(trace); aff=[a for a in scaled_props(p,seed,step) if b.COSTS[a[1]]<=b.BUDGET-spend]
        if not aff: break
        scores=[b.eig_score(p,models,a,seed,step,cid) for cid,a in enumerate(aff)]; sims+=b.EIG_SIMS*len(aff); _,t,s=aff[int(np.argmax(scores))]
        row=b.env_sample(w,b.rng_for('v2','env',seed,step,t,s),1,t,s)[0]; data=np.vstack([data,row]); targets.append(t); spend+=int(b.COSTS[t]); fs,models=b.build_family_models(data,targets); p=b.posterior_from_fs(fs); trace.append((int(t),float(s),int(spend)))
        if min(b.COSTS)>b.BUDGET-spend: break
    m=b.posterior_metrics(p,w.dag_mask); m.update({'spend':spend,'planner_sims':sims,'trace':trace}); return m

def run_world(seed):
    w=b.gen_world(seed); c=b.run_arm(w,seed,1,'portfolio'); t=run_treat(w,seed); return {'seed':seed,'edge_delta':t['edge_error']-c['edge_error'],'brier_delta':t['brier']-c['brier'],'map_delta':t['map']-c['map'],'true_mass_delta':t['true_mass']-c['true_mass'],'compute_ratio':t['planner_sims']/c['planner_sims']}

if __name__=='__main__':
    rows=[run_world(int(x)) for x in sys.argv[1:]]; ds=np.array([r['edge_delta'] for r in rows]); bs=np.array([r['brier_delta'] for r in rows]); s={'n':len(rows),'mean_edge_delta':float(ds.mean()),'mean_brier_delta':float(bs.mean()),'wins':int((ds<0).sum()),'losses':int((ds>0).sum()),'harm_gt_0_50':int((ds>0.5).sum()),'net_map_delta':int(sum(r['map_delta'] for r in rows)),'mean_compute_ratio':float(np.mean([r['compute_ratio'] for r in rows]))}; s['passes_screen']=bool(s['mean_edge_delta']<=-0.10 and s['mean_brier_delta']<=0.005 and s['harm_gt_0_50']<=2); print(json.dumps({'rows':rows,'summary':s},separators=(',',':')))
