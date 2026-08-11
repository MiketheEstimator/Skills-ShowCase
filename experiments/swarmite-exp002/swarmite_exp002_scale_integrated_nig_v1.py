import json,sys,math,numpy as np
import swarmite_benchmark_v2 as b
TAU2=4.0; A0=3.0; B0=2.0

def build_models_nig(data,targets):
    fs=np.full((b.N,1<<b.N),-1e100); models={}
    for v in range(b.N):
        keep=np.array([t!=v for t in targets],dtype=bool); y=data[keep,v]; n=len(y)
        for pm in range(1<<b.N):
            if pm>>v&1: continue
            cols=[u for u in range(b.N) if pm>>u&1]; X=data[keep][:,cols] if cols else np.empty((n,0)); Xd=np.column_stack([np.ones(n),X]); d=Xd.shape[1]
            P0=np.eye(d)/TAU2; A=P0+Xd.T@Xd; Ainv=np.linalg.inv(A); rhs=Xd.T@y; mn=Ainv@rhs
            an=A0+n/2.0; bn=B0+0.5*float(y@y-rhs@mn)
            if not bn>0: raise FloatingPointError('nonpositive bn')
            _,ldA=np.linalg.slogdet(A); ldP0=d*math.log(1.0/TAU2)
            fs[v,pm]=(-0.5*n*math.log(2*math.pi)+0.5*(ldP0-float(ldA))+A0*math.log(B0)-an*math.log(bn)+math.lgamma(an)-math.lgamma(A0))
            models[(v,pm)]=(cols,mn,Ainv,an,bn)
    return fs,models

def pred_t(models,v,pm,row):
    cols,mn,Ainv,an,bn=models[(v,pm)]; x=np.array([1.0]+[row[u] for u in cols]); mean=float(x@mn); df=2.0*an; scale2=float((bn/an)*(1.0+x@Ainv@x)); return mean,df,max(scale2,1e-12)
def t_logpdf(y,mean,df,scale2):
    z=y-mean
    return math.lgamma((df+1)/2)-math.lgamma(df/2)-0.5*(math.log(df*math.pi)+math.log(scale2))-0.5*(df+1)*math.log1p((z*z)/(df*scale2))
def sim_row_t(p,models,target,setpoint,r):
    gi=int(r.choice(len(b.dags),p=p)); mask=int(b.dags[gi]); order=b.topo_from_mask(mask); row=np.zeros(b.N)
    for v in order:
        if v==target: row[v]=setpoint
        else:
            pm=int(b.parents[gi,v]); mean,df,scale2=pred_t(models,v,pm,row); row[v]=mean+math.sqrt(scale2)*r.standard_t(df)
    return row
def update_p_t(p,models,row,target):
    incfs=np.zeros((b.N,1<<b.N))
    for v in range(b.N):
        if v==target: continue
        for pm in range(1<<b.N):
            if pm>>v&1: continue
            mean,df,scale2=pred_t(models,v,pm,row); incfs[v,pm]=t_logpdf(row[v],mean,df,scale2)
    inc=np.zeros(len(b.dags))
    for v in range(b.N):
        if v!=target: inc+=incfs[v,b.parents[:,v]]
    lw=np.log(p+1e-300)+inc; lw-=lw.max(); q=np.exp(lw); q/=q.sum(); return q
def eig_t(p,models,a,seed,step,cid):
    _,t,s=a; h0=b.entropy(p); r=b.rng_for('r26-nig-planner',seed,step,cid); hs=[]
    for _ in range(b.EIG_SIMS): hs.append(b.entropy(update_p_t(p,models,sim_row_t(p,models,t,s,r),t)))
    return (h0-float(np.mean(hs)))/b.COSTS[t]
def run_treat(w,seed,trace_flag=False):
    data=b.env_sample(w,b.rng_for('v2','obs',seed),b.OBS_N); targets=[None]*b.OBS_N; fs,models=build_models_nig(data,targets); p=b.posterior_from_fs(fs); spend=0; sims=0; trace=[]
    while True:
        step=len(trace); aff=[a for a in b.proposals(p,seed,step,0) if b.COSTS[a[1]]<=b.BUDGET-spend]
        if not aff: break
        scores=[eig_t(p,models,a,seed,step,cid) for cid,a in enumerate(aff)]; sims+=b.EIG_SIMS*len(aff); _,t,s=aff[int(np.argmax(scores))]
        row=b.env_sample(w,b.rng_for('v2','env',seed,step,t,s),1,t,s)[0]; data=np.vstack([data,row]); targets.append(t); spend+=int(b.COSTS[t]); fs,models=build_models_nig(data,targets); p=b.posterior_from_fs(fs); trace.append((int(t),float(s),int(spend)))
        if min(b.COSTS)>b.BUDGET-spend: break
    m=b.posterior_metrics(p,w.dag_mask); em=b.edge_marginals(p); m.update({'spend':spend,'planner_sims':sims,'posterior_sum':float(p.sum()),'expected_edges':float(em.sum()),'trace':trace if trace_flag else None}); return m

def mechanics(seed):
    w=b.gen_world(seed); a=run_treat(w,seed,True); z=run_treat(w,seed,True); return {'seed':seed,'dag_support':29281,'finite':all(np.isfinite([a['edge_error'],a['brier'],a['posterior_sum'],a['expected_edges']])), 'posterior_sum':a['posterior_sum'],'spend':a['spend'],'deterministic_replay':a['trace']==z['trace'] and abs(a['edge_error']-z['edge_error'])<1e-12}
def run_world(seed):
    w=b.gen_world(seed); c=b.run_arm(w,seed,1,'portfolio'); t=run_treat(w,seed); true_edges=int(w.dag_mask).bit_count(); return {'seed':seed,'edge_delta':t['edge_error']-c['edge_error'],'brier_delta':t['brier']-c['brier'],'map_delta':t['map']-c['map'],'true_mass_delta':t['true_mass']-c['true_mass'],'treat_expected_edges':t['expected_edges'],'true_edges':true_edges,'treat_spend':t['spend']}
if __name__=='__main__':
    mode=sys.argv[1]; seeds=list(map(int,sys.argv[2:]))
    if mode=='mechanics':
        rows=[mechanics(s) for s in seeds]; print(json.dumps({'rows':rows,'passes':all(r['finite'] and r['dag_support']==29281 and abs(r['posterior_sum']-1)<1e-10 and r['spend']<=15 and r['deterministic_replay'] for r in rows)},separators=(',',':')))
    else:
        rows=[run_world(s) for s in seeds]; ds=np.array([r['edge_delta'] for r in rows]); bs=np.array([r['brier_delta'] for r in rows]); s={'n':len(rows),'mean_edge_delta':float(ds.mean()),'mean_brier_delta':float(bs.mean()),'wins':int((ds<0).sum()),'losses':int((ds>0).sum()),'harm_gt_0_50':int((ds>0.5).sum()),'net_map_delta':int(sum(r['map_delta'] for r in rows))}; s['passes_screen']=bool(s['mean_edge_delta']<=-0.10 and s['mean_brier_delta']<=0.005 and s['harm_gt_0_50']<=2); print(json.dumps({'rows':rows,'summary':s},separators=(',',':')))
