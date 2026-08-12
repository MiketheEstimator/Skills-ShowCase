import json,sys,math,numpy as np
import swarmite_benchmark_v2 as b
TAU2_T=0.5

def build_models(data,targets,tau2):
    fs=np.full((b.N,1<<b.N),-1e100); models={}
    for v in range(b.N):
        keep=np.array([t!=v for t in targets],dtype=bool); y=data[keep,v]
        for pm in range(1<<b.N):
            if pm>>v&1: continue
            cols=[u for u in range(b.N) if pm>>u&1]; X=data[keep][:,cols] if cols else np.empty((len(y),0)); Xd=np.column_stack([np.ones(len(y)),X]); A=np.eye(Xd.shape[1])/tau2+Xd.T@Xd; Ainv=np.linalg.inv(A); rhs=Xd.T@y; mu=Ainv@rhs; quad=float(y@y-rhs@mu); _,ld=np.linalg.slogdet(A); logdetC=float(ld+Xd.shape[1]*math.log(tau2)); fs[v,pm]=-0.5*(len(y)*math.log(2*math.pi)+logdetC+quad); models[(v,pm)]=(cols,mu,Ainv)
    return fs,models

def run_treat(w,seed):
    data=b.env_sample(w,b.rng_for('v2','obs',seed),b.OBS_N); targets=[None]*b.OBS_N; fs,models=build_models(data,targets,TAU2_T); p=b.posterior_from_fs(fs); spend=0; sims=0
    while True:
        step=len(targets)-b.OBS_N; aff=[a for a in b.proposals(p,seed,step,0) if b.COSTS[a[1]]<=b.BUDGET-spend]
        if not aff: break
        scores=[b.eig_score(p,models,a,seed,step,cid) for cid,a in enumerate(aff)]; sims+=b.EIG_SIMS*len(aff); _,t,s=aff[int(np.argmax(scores))]; row=b.env_sample(w,b.rng_for('v2','env',seed,step,t,s),1,t,s)[0]; data=np.vstack([data,row]); targets.append(t); spend+=int(b.COSTS[t]); fs,models=build_models(data,targets,TAU2_T); p=b.posterior_from_fs(fs)
        if min(b.COSTS)>b.BUDGET-spend: break
    m=b.posterior_metrics(p,w.dag_mask); m.update({'spend':spend,'planner_sims':sims}); return m

def run_world(seed):
    w=b.gen_world(seed); c=b.run_arm(w,seed,1,'portfolio'); t=run_treat(w,seed); return {'seed':seed,'edge_delta':t['edge_error']-c['edge_error'],'brier_delta':t['brier']-c['brier'],'map_delta':t['map']-c['map'],'true_mass_delta':t['true_mass']-c['true_mass']}

if __name__=='__main__':
 rows=[run_world(int(x)) for x in sys.argv[1:]]; ds=np.array([r['edge_delta'] for r in rows]); bs=np.array([r['brier_delta'] for r in rows]); s={'n':len(rows),'mean_edge_delta':float(ds.mean()),'mean_brier_delta':float(bs.mean()),'wins':int((ds<0).sum()),'losses':int((ds>0).sum()),'harm_gt_0_50':int((ds>0.5).sum()),'net_map_delta':int(sum(r['map_delta'] for r in rows))}; s['passes_screen']=bool(s['mean_edge_delta']<=-0.10 and s['mean_brier_delta']<=0.005 and s['harm_gt_0_50']<=2); print(json.dumps({'rows':rows,'summary':s},separators=(',',':')))
