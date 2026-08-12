import json, math, numpy as np
from statistics import NormalDist
import swarmite_benchmark_v2 as b
import swarmite_exp002_s47_breadth as s47
import swarmite_exp002_s60_counterfactual_predictive_residual_state as s60
import swarmite_exp002_s69_predictive_calibration as s69
REGIMES=s69.REGIMES; DRAWS=s69.DRAWS; LAM=10.0
Z80=NormalDist().inv_cdf(.90); Z95=NormalDist().inv_cdf(.975)
def seeds(start,n):
 out=[]
 for rg in REGIMES: out += [x for x in s60.selected(start,n) if s47.regime(x)==rg][:n]
 return out
def cells(external_seed):
 reg,seed,w,c,data,targets,p0,meta=s47.state(external_seed); fs,models=b.build_family_models(data,targets); p=b.posterior_from_fs(fs); ent=float(-np.sum(p*np.log(np.maximum(p,1e-300)))); out=[]
 for target in range(b.N):
  for spi,sp in enumerate((-2.,2.)):
   rr=b.rng_for('s71','predictive',seed,target,spi); sims=np.asarray([b.sim_row_from_posterior(p,models,target,sp,rr) for _ in range(DRAWS)],float); obs=np.asarray(s69.actual(reg,w,seed,target,sp,meta),float)
   for j in range(b.N):
    if j==target: continue
    x=sims[:,j]; mu=float(np.mean(x)); sd=float(np.std(x,ddof=1))
    if not np.isfinite(sd) or sd<=1e-10:return None
    feat=[math.log(sd),abs(mu),sp,target/(b.N-1),j/(b.N-1),ent]
    out.append((reg,external_seed,feat,float(obs[j]-mu)/sd))
 return out
def design(rows,stats=None):
 X=np.asarray([r[2] for r in rows],float)
 if stats is None: stats=(X.mean(0),np.maximum(X.std(0),1e-6))
 m,s=stats; X=(X-m)/s; return np.c_[np.ones(len(X)),X],stats
def ridge(X,y):
 I=np.eye(X.shape[1]); I[0,0]=0; return np.linalg.solve(X.T@X+LAM*I,X.T@y)
def fit(rows):
 X,stats=design(rows); z=np.asarray([r[3] for r in rows]); wb=ridge(X,z); e=z-X@wb; ys=np.log(np.maximum(e*e,1e-4)); ws=ridge(X,ys); return stats,wb,ws
def transform(rows,cal):
 stats,wb,ws=cal; X,_=design(rows,stats); out=[]
 for r,bias,lv in zip(rows,X@wb,X@ws):
  scale=float(np.clip(np.exp(.5*lv),.5,2.)); out.append((r[0],r[1],r[3],(r[3]-bias)/scale))
 return out
def one(x):return {'mean':float(np.mean(x)),'rms':float(np.sqrt(np.mean(x*x))),'coverage80':float(np.mean(np.abs(x)<=Z80)),'coverage95':float(np.mean(np.abs(x)<=Z95))}
def metrics(rows):
 out={}
 for rg in REGIMES:
  a=np.asarray([[r[2],r[3]] for r in rows if r[0]==rg]); out[rg]={'raw':one(a[:,0]),'calibrated':one(a[:,1])}
 return out
def ce(v):return abs(v['coverage80']-.8)+abs(v['coverage95']-.95)
def disposition(m):
 raw=np.mean([ce(m[r]['raw']) for r in REGIMES]); cal=np.mean([ce(m[r]['calibrated']) for r in REGIMES]); imp=(raw-cal)/max(raw,1e-12); nb=all(ce(m[r]['calibrated'])<=ce(m[r]['raw'])+.02 for r in REGIMES); bounds=all(.74<=m[r]['calibrated']['coverage80']<=.86 and .91<=m[r]['calibrated']['coverage95']<=.98 and .85<=m[r]['calibrated']['rms']<=1.15 for r in REGIMES); return ('RESPONSE_STATE_CALIBRATION_SUPPORTED' if imp>=.2 and nb and bounds else 'RESPONSE_STATE_CALIBRATION_FALSIFIED'),raw,cal,imp
def gather(ss):
 out=[]
 for x in ss:
  q=cells(x)
  if q is None:return None
  out.extend(q)
 return out
def main():
 mech=gather(seeds(114001,2)); out={'mechanics':{'passed':bool(mech)}}
 if not mech:out['disposition']='BLOCKED_EXECUTION_MECHANICS';return out
 trseeds=seeds(114201,64); train=gather(trseeds)
 if train is None:out['disposition']='BLOCKED_EXECUTION_NONFINITE';return out
 oof=[]
 for fold in range(4):
  hold=set(trseeds[fold::4]); oof+=transform([r for r in train if r[1] in hold],fit([r for r in train if r[1] not in hold]))
 out['crossfit_training']=metrics(oof); test=gather(seeds(115201,64))
 if test is None:out['disposition']='BLOCKED_EXECUTION_NONFINITE';return out
 hm=metrics(transform(test,fit(train))); d,raw,cal,imp=disposition(hm); out['heldout']=hm; out['coverage_error']={'raw_mean':raw,'calibrated_mean':cal,'relative_improvement':imp}; out['disposition']=d; return out
if __name__=='__main__':print(json.dumps(main(),separators=(',',':')))
