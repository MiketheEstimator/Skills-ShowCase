import math,itertools,numpy as np
import swarmite_benchmark_v2 as b
MU=0.65; SIG2=0.15**2

def lse(a):
 m=max(a); return m+math.log(sum(math.exp(x-m) for x in a))
def lev(X,y,m0,var):
 P=np.diag(1.0/var); A=P+X.T@X; C=np.linalg.inv(A); rhs=P@m0+X.T@y; mn=C@rhs; q=float(y@y+m0@P@m0-rhs@mn); return -0.5*(len(y)*math.log(2*math.pi)+np.linalg.slogdet(A)[1]+float(np.log(var).sum())+q)
def build(data,targets):
 fs=np.full((b.N,1<<b.N),-1e100)
 for v in range(b.N):
  keep=np.array([t!=v for t in targets],bool); y=data[keep,v]
  for pm in range(1<<b.N):
   if pm>>v&1: continue
   cols=[u for u in range(b.N) if pm>>u&1]; X=data[keep][:,cols] if cols else np.empty((len(y),0)); X=np.column_stack([np.ones(len(y)),X]); k=len(cols); vals=[]
   for sg in itertools.product((-1.,1.),repeat=k): vals.append(lev(X,y,np.array([0.]+[MU*s for s in sg]),np.array([b.TAU2]+[SIG2]*k)))
   fs[v,pm]=lse(vals)-k*math.log(2.)
 _,models=b.build_family_models(data,targets); return fs,models
def run(w,seed):
 data=b.env_sample(w,b.rng_for('v2','obs',seed),b.OBS_N); targets=[None]*b.OBS_N; fs,models=build(data,targets); p=b.posterior_from_fs(fs); spend=0; trace=[]
 while True:
  step=len(trace); aff=[a for a in b.proposals(p,seed,step,0) if b.COSTS[a[1]]<=b.BUDGET-spend]
  if not aff: break
  sc=[b.eig_score(p,models,a,seed,step,cid) for cid,a in enumerate(aff)]; role,t,s=aff[int(np.argmax(sc))]; row=b.env_sample(w,b.rng_for('v2','env',seed,step,t,s),1,t,s)[0]; data=np.vstack([data,row]); targets.append(t); spend+=int(b.COSTS[t]); fs,models=build(data,targets); p=b.posterior_from_fs(fs); trace.append((role,int(t),float(s),spend))
  if min(b.COSTS)>b.BUDGET-spend: break
 m=b.posterior_metrics(p,w.dag_mask); m['spend']=spend; m['expected_edges']=float(b.edge_marginals(p).sum()); m['trace']=trace; m['posterior_sum']=float(p.sum()); return m
def paired(seed):
 w=b.gen_world(seed); c=b.run_arm(w,seed,1,'portfolio'); t=run(w,seed); return {'seed':seed,'edge_delta':t['edge_error']-c['edge_error'],'brier_delta':t['brier']-c['brier'],'map_delta':t['map']-c['map'],'true_mass_delta':t['true_mass']-c['true_mass'],'treat_expected_edges':t['expected_edges'],'true_edges':int(w.dag_mask).bit_count(),'spend':t['spend']}