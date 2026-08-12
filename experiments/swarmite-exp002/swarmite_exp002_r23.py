import json,sys,math,numpy as np
import swarmite_benchmark_v2 as b
G=30.0; INTERCEPT_VAR=4.0; EPS=1e-6

def build_models_g(data,targets):
    fs=np.full((b.N,1<<b.N),-1e100); models={}
    for v in range(b.N):
        keep=np.array([t!=v for t in targets],dtype=bool); y=data[keep,v]
        for pm in range(1<<b.N):
            if pm>>v&1: continue
            cols=[u for u in range(b.N) if pm>>u&1]; Xp=data[keep][:,cols] if cols else np.empty((len(y),0)); Xd=np.column_stack([np.ones(len(y)),Xp]); d=1+len(cols); P=np.zeros((d,d)); P[0,0]=1.0/INTERCEPT_VAR; logdetSigma=math.log(INTERCEPT_VAR)
            if cols:
                gram=Xp.T@Xp+EPS*np.eye(len(cols)); P[1:,1:]=gram/G; _,ldg=np.linalg.slogdet(gram); logdetSigma+=len(cols)*math.log(G)-float(ldg)
            A=P+Xd.T@Xd; Ainv=np.linalg.inv(A); rhs=Xd.T@y; mu=Ainv@rhs; quad=float(y@y-rhs@mu); _,lda=np.linalg.slogdet(A); logdetC=float(lda+logdetSigma); fs[v,pm]=-0.5*(len(y)*math.log(2*math.pi)+logdetC+quad); models[(v,pm)]=(cols,mu,Ainv)
    return fs,models

def run_treat(w,seed,return_trace=False):
    data=b.env_sample(w,b.rng_for('v2','obs',seed),b.OBS_N); targets=[None]*b.OBS_N; fs,models=build_models_g(data,targets); p=b.posterior_from_fs(fs); spend=0; sims=0; trace=[]
    if not (np.isfinite(fs[fs>-1e90]).all() and np.isfinite(p).all() and abs(float(p.sum())-1)<1e-10): raise RuntimeError('nonfinite initial state')
    while True:
        step=len(trace); aff=[a for a in b.proposals(p,seed,step,0) if b.COSTS[a[1]]<=b.BUDGET-spend]
        if not aff: break
        scores=[b.eig_score(p,models,a,seed,step,cid) for cid,a in enumerate(aff)]; sims+=b.EIG_SIMS*len(aff)
        if not np.isfinite(scores).all(): raise RuntimeError('nonfinite EIG')
        _,t,s=aff[int(np.argmax(scores))]; row=b.env_sample(w,b.rng_for('v2','env',seed,step,t,s),1,t,s)[0]; data=np.vstack([data,row]); targets.append(t); spend+=int(b.COSTS[t]); fs,models=build_models_g(data,targets); p=b.posterior_from_fs(fs)
        if spend>b.BUDGET: raise RuntimeError('budget exceeded')
        trace.append((int(t),float(s),int(spend)))
        if min(b.COSTS)>b.BUDGET-spend: break
    m=b.posterior_metrics(p,w.dag_mask); m.update({'spend':spend,'planner_sims':sims,'trace':trace if return_trace else None,'posterior_sum':float(p.sum()),'dag_support':len(p)}); return m

def run_world(seed):
    w=b.gen_world(seed); c=b.run_arm(w,seed,1,'portfolio'); t=run_treat(w,seed); return {'seed':seed,'dag_mask':w.dag_mask,'control':{k:c[k] for k in c if k!='trace'},'treatment':t,'edge_delta':t['edge_error']-c['edge_error'],'brier_delta':t['brier']-c['brier'],'map_delta':t['map']-c['map'],'true_mass_delta':t['true_mass']-c['true_mass'],'compute_ratio':t['planner_sims']/c['planner_sims']}

if __name__=='__main__':
    mode=sys.argv[1]; seeds=[int(x) for x in sys.argv[2:]]
    if mode=='mechanics':
        out=[]
        for seed in seeds:
            w=b.gen_world(seed); a=run_treat(w,seed,True); z=run_treat(w,seed,True); out.append({'seed':seed,'finite':True,'dag_support':a['dag_support'],'posterior_sum':a['posterior_sum'],'spend':a['spend'],'deterministic_replay':a['trace']==z['trace'] and abs(a['edge_error']-z['edge_error'])<1e-12,'trace':a['trace']})
        print(json.dumps({'mechanics':out,'passes':all(x['finite'] and x['dag_support']==29281 and abs(x['posterior_sum']-1)<1e-10 and x['spend']<=15 and x['deterministic_replay'] for x in out)},separators=(',',':')))
    else:
        rows=[run_world(seed) for seed in seeds]; ds=np.array([r['edge_delta'] for r in rows]); bs=np.array([r['brier_delta'] for r in rows]); s={'n':len(rows),'mean_edge_delta':float(ds.mean()),'mean_brier_delta':float(bs.mean()),'wins':int((ds<0).sum()),'losses':int((ds>0).sum()),'harm_gt_0_50':int((ds>0.5).sum()),'net_map_delta':int(sum(r['map_delta'] for r in rows)),'mean_compute_ratio':float(np.mean([r['compute_ratio'] for r in rows]))}; s['passes_screen']=bool(s['mean_edge_delta']<=-0.10 and s['mean_brier_delta']<=0.005 and s['harm_gt_0_50']<=2); print(json.dumps({'rows':rows,'summary':s},separators=(',',':')))
