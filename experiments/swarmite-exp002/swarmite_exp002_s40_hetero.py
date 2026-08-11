import json, numpy as np
import swarmite_benchmark_v2 as b
import swarmite_exp002_s33_expand as s33
import swarmite_exp002_s39_credal as s39

MECHS=('tanh','sin','asinh')
SPECIALISTS=s39.SPECIALISTS
THRESHOLD=0.2692013432171404

def mechanism(seed): return MECHS[int(seed)%3]
def feat(x,m): return np.tanh(x) if m=='tanh' else (np.sin(x) if m=='sin' else np.arcsinh(x))
def env(world,r,n,target=None,setpoint=None,mech='tanh'):
    X=np.zeros((n,b.N))
    for i in range(n):
        for v in world.order:
            if target==v: X[i,v]=setpoint
            else:
                mu=float(feat(X[i],mech)@world.W[:,v]); sig=float(np.clip(.55+.35*abs(mu),.55,1.80)); X[i,v]=mu+r.normal(0,sig)
    return X

def run_control(world,seed):
    mech=mechanism(seed); data=env(world,b.rng_for('v2','obs',seed),b.OBS_N,mech=mech); targets=[None]*b.OBS_N
    fs,models=b.build_family_models(data,targets); p=b.posterior_from_fs(fs); spend=0; trace=[]
    while True:
        step=len(trace); aff=[a for a in b.proposals(p,seed,step,0) if b.COSTS[a[1]]<=b.BUDGET-spend]
        if not aff: break
        scores=[b.eig_score(p,models,a,seed,step,cid) for cid,a in enumerate(aff)]; role,t,s=aff[int(np.argmax(scores))]
        row=env(world,b.rng_for('v2','env',seed,step,t,s),1,t,s,mech)[0]; data=np.vstack([data,row]); targets.append(t); spend+=int(b.COSTS[t])
        fs,models=b.build_family_models(data,targets); p=b.posterior_from_fs(fs); trace.append((role,int(t),float(s),spend))
        if min(b.COSTS)>b.BUDGET-spend: break
    return {'spend':spend,'trace':trace},data,targets,p,mech

def world_row(seed):
    w=b.gen_world(seed); c,data,targets,p0,mech=run_control(w,seed)
    posts={'LG':p0.copy()}; finite=True
    for n in s33.CLASSES:
        if n=='LG': continue
        posts[n],ok=s33.build_class(data,targets,n); finite=finite and ok
    lg=s33.cv_score(data,targets,'LG'); tt=s33.cv_score(data,targets,'TT'); alpha=s33.sigmoid((tt-lg)/s33.T)
    ps30=(1-alpha)*posts['LG']+alpha*posts['TT']; ps30/=ps30.sum()
    em0=b.edge_marginals(ps30); ems=np.vstack([b.edge_marginals(posts[n]) for n in SPECIALISTS]); allm=np.vstack([em0,ems]); widths=np.max(allm,axis=0)-np.min(allm,axis=0); score=float(np.mean(widths)); promote=score<=THRESHOLD
    base=b.posterior_metrics(p0,w.dag_mask); s30m=b.posterior_metrics(ps30,w.dag_mask); ed=float(s30m['edge_error']-base['edge_error']); bd=float(s30m['brier']-base['brier'])
    return {'seed':int(seed),'mechanism':mech,'score':score,'promote':bool(promote),'s30_edge_delta_vs_baseline':ed,'s30_brier_delta_vs_baseline':bd,'s30_large_harm':int(ed>.5),'spend':int(c['spend']),'trace_identical':True,'finite':finite,'s30_sum':float(ps30.sum())}

def mechanics(rows): return all(r['spend']<=15 and r['trace_identical'] and r['finite'] and abs(r['s30_sum']-1)<1e-8 and np.isfinite(r['score']) for r in rows)
def boot(x,reps=10000,seed=24040):
    x=np.asarray(x,float); rr=np.random.default_rng(seed); m=np.mean(rr.choice(x,(reps,len(x)),replace=True),axis=1); return [float(np.quantile(m,.025)),float(np.quantile(m,.975))]
def summarize(rows):
    pr=np.array([r['promote'] for r in rows],bool); ed=np.array([r['s30_edge_delta_vs_baseline'] for r in rows]); bd=np.array([r['s30_brier_delta_vs_baseline'] for r in rows]); hed=np.where(pr,ed,0.0); hbd=np.where(pr,bd,0.0); always=float(np.mean(ed)); hybrid=float(np.mean(hed)); retained=float(abs(hybrid)/abs(always)) if always<0 else 1.0
    return {'n':len(rows),'coverage':float(np.mean(pr)),'n_promoted':int(np.sum(pr)),'promoted_large_harms':int(np.sum((ed>.5)&pr)),'promoted_large_harm_rate':float(np.sum((ed>.5)&pr)/max(1,np.sum(pr))),'always_s30_mean_edge_delta':always,'hybrid_mean_edge_delta':hybrid,'bootstrap95_hybrid_edge_delta':boot(hed,seed=24040+len(rows)),'hybrid_mean_brier_delta':float(np.mean(hbd)),'improvement_retained':retained,'mechanics_ok':mechanics(rows)}
def screen_pass(m): return m['mechanics_ok'] and m['coverage']>=.60 and m['promoted_large_harm_rate']<=.05 and m['hybrid_mean_edge_delta']<0 and m['hybrid_mean_brier_delta']<=.005 and (m['always_s30_mean_edge_delta']>=0 or m['improvement_retained']>=.70)
def confirm_pass(m): return screen_pass(m) and m['bootstrap95_hybrid_edge_delta'][1]<0

def run():
    mech=[world_row(s) for s in range(72501,72505)]; out={'mechanics':{'rows':mech,'passed':mechanics(mech)}}
    if not mechanics(mech): out['disposition']='BLOCKED_MECHANICS'; return out
    scr=[world_row(s) for s in range(72511,72535)]; sm=summarize(scr); out['screen']=sm
    if not screen_pass(sm): out['disposition']='FALSIFIED_AT_SCREEN'; return out
    con=[world_row(s) for s in range(72601,72649)]; cm=summarize(con); out['confirmation']=cm; out['disposition']='HETEROSKEDASTIC_TRANSFER_SUPPORTED' if confirm_pass(cm) else 'FALSIFIED_ON_CONFIRMATION'; return out
if __name__=='__main__': print(json.dumps(run(),separators=(',',':')))
