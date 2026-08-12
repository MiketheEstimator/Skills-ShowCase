import math,itertools,numpy as np
import swarmite_benchmark_v2 as b
CENTERS=np.array([-0.85,-0.65,-0.45,0.45,0.65,0.85]); SIG2=0.08**2

def lse(a):
 m=float(np.max(a)); return m+math.log(float(np.exp(a-m).sum()))
def build(data,targets):
 fs=np.full((b.N,1<<b.N),-1e100)
 for v in range(b.N):
  keep=np.array([t!=v for t in targets],bool); y=data[keep,v]; yy=float(y@y)
  for pm in range(1<<b.N):
   if pm>>v&1: continue
   cols=[u for u in range(b.N) if pm>>u&1]; k=len(cols); X=data[keep][:,cols] if cols else np.empty((len(y),0)); X=np.column_stack([np.ones(len(y)),X]); var=np.array([b.TAU2]+[SIG2]*k); pinv=1.0/var; A=np.diag(pinv)+X.T@X; C=np.linalg.inv(A); xty=X.T@y; const=-0.5*(len(y)*math.log(2*math.pi)+np.linalg.slogdet(A)[1]+float(np.log(var).sum()))
   if k==0:
    rhs=xty; fs[v,pm]=const-0.5*(yy-float(rhs@C@rhs))
   else:
    combos=np.array(list(itertools.product(CENTERS,repeat=k)),dtype=float); M=np.column_stack([np.zeros(len(combos)),combos]); R=M*pinv+xty; vals=const-0.5*(yy+(M*M*pinv).sum(axis=1)-np.einsum('ij,jk,ik->i',R,C,R)); fs[v,pm]=lse(vals)-k*math.log(6.0)
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