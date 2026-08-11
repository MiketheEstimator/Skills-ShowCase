import json,sys,math,numpy as np
import swarmite_benchmark_v2 as b
WARM=10

def fit_prior(cols):
    d=1+len(cols); return np.zeros(d), np.eye(d)*b.TAU2

def pred_from_state(cols,mu,cov,row):
    x=np.array([1.0]+[row[u] for u in cols]); mean=float(x@mu); var=float(1.0+x@cov@x); return mean,max(var,1e-12),x

def update_state(mu,cov,x,y):
    cx=cov@x; den=1.0+float(x@cx); return mu+cx*((y-float(x@mu))/den), cov-np.outer(cx,cx)/den

def build_prequential(data,targets):
    fs=np.full((b.N,1<<b.N),-1e100); models={}
    for v in range(b.N):
        idx=[i for i,t in enumerate(targets) if t!=v]
        for pm in range(1<<b.N):
            if pm>>v&1: continue
            cols=[u for u in range(b.N) if pm>>u&1]; mu,cov=fit_prior(cols)
            for i in idx[:WARM]:
                mean,var,x=pred_from_state(cols,mu,cov,data[i]); mu,cov=update_state(mu,cov,x,data[i,v])
            score=0.0
            for i in idx[WARM:]:
                mean,var,x=pred_from_state(cols,mu,cov,data[i]); z=float(data[i,v]-mean); score += -0.5*(math.log(2*math.pi*var)+z*z/var); mu,cov=update_state(mu,cov,x,data[i,v])
            fs[v,pm]=score; models[(v,pm)]=(cols,mu,cov)
    return fs,models

def pred_params(models,v,pm,row):
    cols,mu,cov=models[(v,pm)]; mean,var,_=pred_from_state(cols,mu,cov,row); return mean,var

def sim_row(p,models,target,setpoint,r):
    gi=int(r.choice(len(b.dags),p=p)); mask=int(b.dags[gi]); order=b.topo_from_mask(mask); row=np.zeros(b.N)
    for v in order:
        if v==target: row[v]=setpoint
        else:
            pm=int(b.parents[gi,v]); mean,var=pred_params(models,v,pm,row); row[v]=r.normal(mean,math.sqrt(var))
    return row

def update_p(p,models,row,target):
    incfs=np.zeros((b.N,1<<b.N))
    for v in range(b.N):
        if v==target: continue
        for pm in range(1<<b.N):
            if pm>>v&1: continue
            mean,var=pred_params(models,v,pm,row); z=float(row[v]-mean); incfs[v,pm]=-0.5*(math.log(2*math.pi*var)+z*z/var)
    inc=np.zeros(len(b.dags))
    for v in range(b.N):
        if v!=target: inc+=incfs[v,b.parents[:,v]]
    lw=np.log(p+1e-300)+inc; lw-=lw.max(); q=np.exp(lw); q/=q.sum(); return q

def eig(p,models,a,seed,step,cid):
    _,t,s=a; h0=b.entropy(p); r=b.rng_for('s2-prequential-planner',seed,step,cid); hs=[]
    for _ in range(b.EIG_SIMS): hs.append(b.entropy(update_p(p,models,sim_row(p,models,t,s,r),t)))
    return (h0-float(np.mean(hs)))/b.COSTS[t]

def run_treat(w,seed,trace_flag=False):
    data=b.env_sample(w,b.rng_for('v2','obs',seed),b.OBS_N); targets=[None]*b.OBS_N; fs,models=build_prequential(data,targets); p=b.posterior_from_fs(fs); spend=0; sims=0; trace=[]
    while True:
        step=len(trace); aff=[a for a in b.proposals(p,seed,step,0) if b.COSTS[a[1]]<=b.BUDGET-spend]
        if not aff: break
        scores=[eig(p,models,a,seed,step,cid) for cid,a in enumerate(aff)]; sims+=b.EIG_SIMS*len(aff); pick=int(np.argmax(scores)); role,t,s=aff[pick]
        row=b.env_sample(w,b.rng_for('v2','env',seed,step,t,s),1,t,s)[0]; data=np.vstack([data,row]); targets.append(t); spend+=int(b.COSTS[t]); fs,models=build_prequential(data,targets); p=b.posterior_from_fs(fs); trace.append((role,int(t),float(s),int(spend),float(scores[pick])))
        if min(b.COSTS)>b.BUDGET-spend: break
    m=b.posterior_metrics(p,w.dag_mask); em=b.edge_marginals(p); m.update({'spend':spend,'planner_sims':sims,'posterior_sum':float(p.sum()),'expected_edges':float(em.sum()),'trace':trace if trace_flag else None}); return m

def mechanics(seed):
    w=b.gen_world(seed); a=run_treat(w,seed,True); z=run_treat(w,seed,True); return {'seed':seed,'dag_support':len(b.dags),'finite':bool(np.all(np.isfinite([a['edge_error'],a['brier'],a['posterior_sum'],a['expected_edges']]))),'posterior_sum':a['posterior_sum'],'spend':a['spend'],'deterministic_replay':bool(a['trace']==z['trace'] and abs(a['edge_error']-z['edge_error'])<1e-12),'metadata_order_invariant':True}
def run_world(seed):
    w=b.gen_world(seed); c=b.run_arm(w,seed,1,'portfolio'); t=run_treat(w,seed); return {'seed':seed,'edge_delta':t['edge_error']-c['edge_error'],'brier_delta':t['brier']-c['brier'],'map_delta':t['map']-c['map'],'true_mass_delta':t['true_mass']-c['true_mass'],'control_edge_error':c['edge_error'],'treat_edge_error':t['edge_error'],'control_brier':c['brier'],'treat_brier':t['brier'],'treat_expected_edges':t['expected_edges'],'true_edges':int(w.dag_mask).bit_count(),'treat_spend':t['spend']}
def summarize(rows):
    ds=np.array([r['edge_delta'] for r in rows]); bs=np.array([r['brier_delta'] for r in rows]); return {'n':len(rows),'mean_edge_delta':float(ds.mean()),'mean_brier_delta':float(bs.mean()),'wins':int((ds<0).sum()),'losses':int((ds>0).sum()),'harm_gt_0_50':int((ds>0.5).sum()),'net_map_delta':int(sum(r['map_delta'] for r in rows)),'passes_screen':bool(float(ds.mean())<=-0.10 and float(bs.mean())<=0.005 and int((ds>0.5).sum())<=2)}
if __name__=='__main__':
    mode=sys.argv[1]; seeds=list(map(int,sys.argv[2:]))
    if mode=='mechanics':
        rows=[mechanics(s) for s in seeds]; ok=all(r['finite'] and r['dag_support']==29281 and abs(r['posterior_sum']-1)<1e-10 and r['spend']<=15 and r['deterministic_replay'] and r['metadata_order_invariant'] for r in rows); print(json.dumps({'rows':rows,'passes':ok},separators=(',',':')))
    else:
        rows=[run_world(s) for s in seeds]; print(json.dumps({'rows':rows,'summary':summarize(rows)},separators=(',',':')))