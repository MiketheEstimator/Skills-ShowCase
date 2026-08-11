import numpy as np
import swarmite_benchmark_v2 as b
import swarmite_exp002_s5_nonlocal as s5

def gen_shift(seed):
 r=b.rng_for('v2','world',seed); order=list(map(int,r.permutation(b.N))); W=np.zeros((b.N,b.N)); mask=0
 for a in range(b.N):
  for bb in range(a+1,b.N):
   u,v=order[a],order[bb]
   if r.random()<0.35:
    W[u,v]=r.choice([-1,1])*r.uniform(.15,.90); mask|=1<<b.EDGE_INDEX[(u,v)]
 if int(mask).bit_count()<2:
  for a,bb in [(0,1),(1,2)]:
   u,v=order[a],order[bb]
   if W[u,v]==0:
    W[u,v]=r.choice([-1,1])*r.uniform(.15,.90); mask|=1<<b.EDGE_INDEX[(u,v)]
 return b.World(mask,W,order,seed)
def dual(seed):
 w=gen_shift(seed); c=b.run_arm(w,seed,1,'portfolio'); data=b.env_sample(w,b.rng_for('v2','obs',seed),b.OBS_N); targets=[None]*b.OBS_N
 for tr in c['trace']:
  step=tr['step']; t=tr['target']; sp=tr['setpoint']; row=b.env_sample(w,b.rng_for('v2','env',seed,step,t,sp),1,t,sp)[0]; data=np.vstack([data,row]); targets.append(t)
 fs,_=s5.build(data,targets); p=b.posterior_from_fs(fs); m=b.posterior_metrics(p,w.dag_mask); return w,c,m,float(p.sum())
def paired(seed):
 w,c,t,ps=dual(seed); mags=np.abs(w.W[w.W!=0]); return {'seed':seed,'edge_delta':t['edge_error']-c['edge_error'],'brier_delta':t['brier']-c['brier'],'map_delta':t['map']-c['map'],'true_mass_delta':t['true_mass']-c['true_mass'],'trace_identical':True,'spend':c['spend'],'min_effect':float(mags.min()),'max_effect':float(mags.max())}