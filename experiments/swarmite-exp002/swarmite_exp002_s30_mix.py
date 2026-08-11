import json, math, numpy as np
import swarmite_benchmark_v2 as b
import swarmite_exp002_s23_robust_likelihood as s23
import swarmite_exp002_s25_heterogeneous as s25
import swarmite_exp002_s29_adequacy as s29

TEMPS=(5.0,10.0,20.0,40.0); REGIMES=s25.REGIMES

def sigmoid(x):
    x=max(-40.0,min(40.0,float(x))); return 1.0/(1.0+math.exp(-x))

def world(seed):
    w=b.gen_world(seed); c,data,targets,p0,reg=s25.run_control(w,seed); fs,finite=s23.build(data,targets); pr=b.posterior_from_fs(fs); rm=b.posterior_metrics(pr,w.dag_mask); ad=s29.world_adequacy(seed); out={}
    for T in TEMPS:
        a=sigmoid(ad['ADEQ']/T); pm=(1-a)*p0+a*pr; pm=pm/pm.sum(); mm=b.posterior_metrics(pm,w.dag_mask); ed=float(mm['edge_error']-c['edge_error']); bd=float(mm['brier']-c['brier'])
        out[str(T)]={'alpha':float(a),'edge_delta':ed,'brier_delta':bd,'large_harm':int(ed>0.50),'posterior_sum':float(pm.sum())}
    return {'seed':int(seed),'regime':reg,'spend':int(c['spend']),'planning_posterior_sum':float(p0.sum()),'robust_posterior_sum':float(pr.sum()),'family_scores_finite':bool(finite),'ADEQ':float(ad['ADEQ']),'robust_edge_delta':float(rm['edge_error']-c['edge_error']),'robust_brier_delta':float(rm['brier']-c['brier']),'mix':out}

def boot(vals,reps=10000,seed=23030):
    x=np.asarray(vals,float); rr=np.random.default_rng(seed); m=np.mean(rr.choice(x,(reps,len(x)),replace=True),axis=1); return [float(np.quantile(m,.025)),float(np.quantile(m,.975))]

def summarize(rows,T,seed=23030):
    k=str(float(T)); ed=[r['mix'][k]['edge_delta'] for r in rows]; bd=[r['mix'][k]['brier_delta'] for r in rows]; by={}
    for i,reg in enumerate(REGIMES):
      z=[r for r in rows if r['regime']==reg]; e=[r['mix'][k]['edge_delta'] for r in z]; q=[r['mix'][k]['brier_delta'] for r in z]
      by[reg]={'n':len(z),'mean_edge_delta':float(np.mean(e)),'bootstrap95_edge_delta':boot(e,seed=seed+i+10),'mean_brier_delta':float(np.mean(q)),'large_harms':sum(r['mix'][k]['large_harm'] for r in z),'mean_alpha':float(np.mean([r['mix'][k]['alpha'] for r in z]))}
    return {'n':len(rows),'T':float(T),'mean_edge_delta':float(np.mean(ed)),'bootstrap95_edge_delta':boot(ed,seed=seed),'mean_brier_delta':float(np.mean(bd)),'large_harms':sum(r['mix'][k]['large_harm'] for r in rows),'wins':sum(x<0 for x in ed),'mean_alpha':float(np.mean([r['mix'][k]['alpha'] for r in rows])),'by_regime':by,'mechanics_ok':all(r['spend']<=15 and np.isfinite(r['ADEQ']) and abs(r['planning_posterior_sum']-1)<1e-8 and abs(r['robust_posterior_sum']-1)<1e-8 and r['family_scores_finite'] and abs(r['mix'][k]['posterior_sum']-1)<1e-8 for r in rows)}

def qualifies(sm):
    if not sm['mechanics_ok'] or sm['mean_edge_delta']>-0.10 or sm['mean_brier_delta']>0.005 or sm['large_harms']>5: return False
    lg=sm['by_regime']['linear_gaussian']
    if lg['mean_edge_delta']>0.10 or lg['mean_brier_delta']>0.010: return False
    for reg in REGIMES[1:]:
      v=sm['by_regime'][reg]
      if v['mean_edge_delta']>0 or v['mean_brier_delta']>0.005: return False
    return True

def qualifies_confirmation(sm):
    if not sm['mechanics_ok'] or sm['mean_edge_delta']>-0.10 or sm['bootstrap95_edge_delta'][1]>=0 or sm['mean_brier_delta']>0.005 or sm['large_harms']>8: return False
    lg=sm['by_regime']['linear_gaussian']
    if lg['mean_edge_delta']>0.05 or lg['mean_brier_delta']>0.005: return False
    for reg in REGIMES[1:]:
      v=sm['by_regime'][reg]
      if v['mean_edge_delta']>=0 or v['bootstrap95_edge_delta'][1]>=0 or v['mean_brier_delta']>0.005: return False
    return True

def training_grid(rows): return [{'T':T,'summary':summarize(rows,T,seed=23030+int(T)),'qualifies':qualifies(summarize(rows,T,seed=23030+int(T)))} for T in TEMPS]
def select_T(grid):
    q=[x for x in grid if x['qualifies']]
    if not q:return None
    best=min(x['summary']['mean_edge_delta'] for x in q); tied=[x for x in q if x['summary']['mean_edge_delta']<=best+0.01]; return float(max(x['T'] for x in tied))
def generate(lo,hi): return [world(s) for s in range(lo,hi+1)]
if __name__=='__main__':
 import sys
 mode=sys.argv[1]
 if mode=='train':
   rows=generate(71400,71447); grid=training_grid(rows); print(json.dumps({'rows':rows,'grid':grid,'selected_T':select_T(grid)},separators=(',',':')))
 elif mode in ('validation','confirmation'):
   T=float(sys.argv[2]); rows=generate(71500,71547) if mode=='validation' else generate(71600,71695); sm=summarize(rows,T,seed=23031 if mode=='validation' else 23032); print(json.dumps({'rows':rows,'summary':sm,'passes':qualifies(sm) if mode=='validation' else qualifies_confirmation(sm)},separators=(',',':')))
 else: raise SystemExit('mode')
