import json, math, numpy as np
import swarmite_benchmark_v2 as b
import swarmite_exp002_s23_robust_likelihood as s23
import swarmite_exp002_s29_adequacy as s29

REGIMES=('linear_gaussian_anchor','sin_gaussian','asinh_t7','leakyrelu_contaminated')
T=5.0

def regime(seed): return REGIMES[int(seed)%4]
def leaky(x): return np.where(x>=0,x,0.2*x)

def env(world,r,n,target=None,setpoint=None,reg='linear_gaussian_anchor'):
    if reg=='linear_gaussian_anchor': return b.env_sample(world,r,n,target,setpoint)
    X=np.zeros((n,b.N))
    for i in range(n):
      if reg=='sin_gaussian': eps=r.normal(size=b.N)
      elif reg=='asinh_t7': eps=r.standard_t(7,size=b.N)*math.sqrt(5/7)
      else:
        mix=r.random(b.N)<0.10; eps=np.where(mix,r.normal(0,3,size=b.N),r.normal(size=b.N))/math.sqrt(1.8)
      for v in world.order:
        if target==v: X[i,v]=setpoint
        else:
          z=X[i]
          feat=np.sin(z) if reg=='sin_gaussian' else (np.arcsinh(z) if reg=='asinh_t7' else leaky(z))
          X[i,v]=float(feat@world.W[:,v]+eps[v])
    return X

def run_control(world,seed):
    reg=regime(seed); data=env(world,b.rng_for('v2','obs',seed),b.OBS_N,reg=reg); targets=[None]*b.OBS_N; fs,models=b.build_family_models(data,targets); p=b.posterior_from_fs(fs); spend=0; trace=[]
    while True:
      step=len(trace); aff=[a for a in b.proposals(p,seed,step,0) if b.COSTS[a[1]]<=b.BUDGET-spend]
      if not aff: break
      scores=[b.eig_score(p,models,a,seed,step,cid) for cid,a in enumerate(aff)]; role,t,s=aff[int(np.argmax(scores))]
      row=env(world,b.rng_for('v2','env',seed,step,t,s),1,t,s,reg)[0]; data=np.vstack([data,row]); targets.append(t); spend+=int(b.COSTS[t]); fs,models=b.build_family_models(data,targets); p=b.posterior_from_fs(fs); trace.append((role,int(t),float(s),spend))
      if min(b.COSTS)>b.BUDGET-spend: break
    m=b.posterior_metrics(p,world.dag_mask); m.update({'spend':spend,'trace':trace,'posterior_sum':float(p.sum())}); return m,data,targets,p,reg

def adequacy(data,targets):
    n=len(data); base=0.0; robust=0.0; idx=list(range(n))
    for fold in range(5):
      te=[i for i in idx if i%5==fold]; tr=[i for i in idx if i%5!=fold]
      for v in range(b.N):
        pms=[pm for pm in range(1<<b.N) if not(pm>>v&1)]; bs=[]; bm=[]; rs=[]; rm=[]
        for pm in pms:
          sc,m=s29.baseline_fit_score(data,targets,v,pm,tr); bs.append(sc); bm.append(m)
          sc2,m2=s29.robust_fit_score(data,targets,v,pm,tr); rs.append(sc2); rm.append(m2)
        mb=bm[int(np.argmax(bs))]; mr=rm[int(np.argmax(rs))]
        for i in te:
          if targets[i]==v: continue
          base+=s29.baseline_logpred(mb,data[i],v); robust+=s29.robust_logpred(mr,data[i],v)
    return float(robust-base)

def sigmoid(x):
    x=max(-40.0,min(40.0,float(x))); return 1/(1+math.exp(-x))

def paired(seed):
    w=b.gen_world(seed); c,data,targets,p0,reg=run_control(w,seed); fs0,_=b.build_family_models(data,targets); p0c=b.posterior_from_fs(fs0); recon=float(np.max(np.abs(p0-p0c))); fs,finite=s23.build(data,targets); pr=b.posterior_from_fs(fs); adeq=adequacy(data,targets); alpha=sigmoid(adeq/T); pm=(1-alpha)*p0+alpha*pr; pm/=pm.sum(); mm=b.posterior_metrics(pm,w.dag_mask); rm=b.posterior_metrics(pr,w.dag_mask)
    ed=float(mm['edge_error']-c['edge_error']); bd=float(mm['brier']-c['brier'])
    return {'seed':int(seed),'regime':reg,'dag_count':len(b.dags),'spend':int(c['spend']),'planning_reconstruction_max_abs':recon,'family_scores_finite':bool(finite),'p0_sum':float(p0.sum()),'pr_sum':float(pr.sum()),'pmix_sum':float(pm.sum()),'ADEQ':adeq,'alpha':float(alpha),'edge_delta':ed,'brier_delta':bd,'large_harm':int(ed>0.50),'robust_edge_delta':float(rm['edge_error']-c['edge_error']),'robust_brier_delta':float(rm['brier']-c['brier']),'trace_identical':True}

def boot(x,reps=10000,seed=23131):
    x=np.asarray(x,float); rr=np.random.default_rng(seed); m=np.mean(rr.choice(x,(reps,len(x)),replace=True),axis=1); return [float(np.quantile(m,.025)),float(np.quantile(m,.975))]
def summarize(rows):
    ed=[r['edge_delta'] for r in rows]; bd=[r['brier_delta'] for r in rows]; by={}
    for i,reg in enumerate(REGIMES):
      z=[r for r in rows if r['regime']==reg]; e=[r['edge_delta'] for r in z]
      by[reg]={'n':len(z),'mean_edge_delta':float(np.mean(e)),'bootstrap95_edge_delta':boot(e,seed=23131+i+10),'mean_brier_delta':float(np.mean([r['brier_delta'] for r in z])),'large_harms':sum(r['large_harm'] for r in z),'mean_alpha':float(np.mean([r['alpha'] for r in z])),'mean_ADEQ':float(np.mean([r['ADEQ'] for r in z]))}
    mech=all(r['dag_count']==29281 and r['spend']<=15 and r['planning_reconstruction_max_abs']<=1e-10 and r['family_scores_finite'] and all(abs(r[k]-1)<1e-8 for k in ('p0_sum','pr_sum','pmix_sum')) and np.isfinite(r['ADEQ']) for r in rows)
    return {'n':len(rows),'mean_edge_delta':float(np.mean(ed)),'bootstrap95_edge_delta':boot(ed),'mean_brier_delta':float(np.mean(bd)),'wins':sum(x<0 for x in ed),'large_harms':sum(r['large_harm'] for r in rows),'mean_alpha':float(np.mean([r['alpha'] for r in rows])),'by_regime':by,'mechanics_ok':mech}
def passes(sm):
    if not sm['mechanics_ok'] or sm['mean_edge_delta']>-0.10 or sm['bootstrap95_edge_delta'][1]>=0 or sm['mean_brier_delta']>0.005 or sm['large_harms']>8:return False
    lg=sm['by_regime']['linear_gaussian_anchor']
    if lg['mean_edge_delta']>0.05 or lg['mean_brier_delta']>0.005:return False
    sig=0
    for reg in REGIMES[1:]:
      v=sm['by_regime'][reg]
      if v['mean_edge_delta']>=0 or v['mean_brier_delta']>0.010:return False
      sig += int(v['bootstrap95_edge_delta'][1]<0)
    return sig>=2
if __name__=='__main__':
 import sys
 seeds=list(map(int,sys.argv[1:])); rows=[paired(s) for s in seeds]; sm=summarize(rows); print(json.dumps({'rows':rows,'summary':sm,'passes':passes(sm) if len(rows)>4 else None},separators=(',',':')))
