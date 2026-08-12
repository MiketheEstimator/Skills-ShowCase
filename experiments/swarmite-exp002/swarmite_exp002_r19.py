import json,sys,math,numpy as np
import swarmite_benchmark_v2 as b
A=1.75; B=3.25
K=np.array([int(m).bit_count() for m in b.dags],dtype=float)
logh=np.array([math.lgamma(k+A)+math.lgamma(10-k+B)-math.lgamma(10+A+B) for k in K]); h=np.exp(logh-logh.max()); h/=h.sum(); u=np.full(len(b.dags),1.0/len(b.dags)); mix=0.5*u+0.5*h; LOG_MIX=np.log(mix)
def posterior(fs,mixed=False):
 ls=np.zeros(len(b.dags))
 for v in range(b.N): ls+=fs[v,b.parents[:,v]]
 if mixed: ls+=LOG_MIX
 ls-=ls.max(); p=np.exp(ls); p/=p.sum(); return p
def run_arm(w,seed,mixed=False):
 data=b.env_sample(w,b.rng_for('v2','obs',seed),b.OBS_N); targets=[None]*b.OBS_N; fs,models=b.build_family_models(data,targets); p=posterior(fs,mixed); spend=0; sims=0
 while True:
  step=len(targets)-b.OBS_N; aff=[a for a in b.proposals(p,seed,step,0) if b.COSTS[a[1]]<=b.BUDGET-spend]
  if not aff: break
  scores=[b.eig_score(p,models,a,seed,step,cid) for cid,a in enumerate(aff)]; sims+=b.EIG_SIMS*len(aff); _,t,s=aff[int(np.argmax(scores))]; row=b.env_sample(w,b.rng_for('v2','env',seed,step,t,s),1,t,s)[0]; data=np.vstack([data,row]); targets.append(t); spend+=int(b.COSTS[t]); fs,models=b.build_family_models(data,targets); p=posterior(fs,mixed)
  if min(b.COSTS)>b.BUDGET-spend: break
 m=b.posterior_metrics(p,w.dag_mask); m.update({'spend':spend,'planner_sims':sims}); return m
def run_world(seed):
 w=b.gen_world(seed); c=run_arm(w,seed,False); t=run_arm(w,seed,True); return {'seed':seed,'dag_mask':w.dag_mask,'control':c,'treatment':t,'edge_delta':t['edge_error']-c['edge_error'],'brier_delta':t['brier']-c['brier'],'map_delta':t['map']-c['map'],'true_mass_delta':t['true_mass']-c['true_mass']}
if __name__=='__main__':
 rows=[run_world(int(x)) for x in sys.argv[1:]]; ds=np.array([r['edge_delta'] for r in rows]); bs=np.array([r['brier_delta'] for r in rows]); s={'n':len(rows),'mean_edge_delta':float(ds.mean()),'mean_brier_delta':float(bs.mean()),'wins':int((ds<0).sum()),'losses':int((ds>0).sum()),'harm_gt_0_50':int((ds>0.5).sum()),'net_map_delta':int(sum(r['map_delta'] for r in rows))}; s['passes_screen']=bool(s['mean_edge_delta']<=-0.10 and s['mean_brier_delta']<=0.005 and s['harm_gt_0_50']<=2); print(json.dumps({'rows':rows,'summary':s},separators=(',',':')))
