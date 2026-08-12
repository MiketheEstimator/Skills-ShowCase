import json, math, numpy as np
from statistics import NormalDist
import swarmite_benchmark_v2 as b
import swarmite_exp002_s47_breadth as s47
import swarmite_exp002_s60_counterfactual_predictive_residual_state as s60
import swarmite_exp002_s69_predictive_calibration as s69

REGIMES=s69.REGIMES; DRAWS=s69.DRAWS; NBINS=5; SHRINK=100.0
Z80=NormalDist().inv_cdf(.90); Z95=NormalDist().inv_cdf(.975)

def seeds(start,n):
    out=[]
    for rg in REGIMES: out += [x for x in s60.selected(start,n) if s47.regime(x)==rg][:n]
    return out

def cells(external_seed):
    reg,seed,w,c,data,targets,p0,meta=s47.state(external_seed)
    fs,models=b.build_family_models(data,targets); p=b.posterior_from_fs(fs); out=[]
    for target in range(b.N):
        for spi,sp in enumerate((-2.0,2.0)):
            rr=b.rng_for('s70','predictive',seed,target,spi)
            sims=np.asarray([b.sim_row_from_posterior(p,models,target,sp,rr) for _ in range(DRAWS)],float)
            obs=np.asarray(s69.actual(reg,w,seed,target,sp,meta),float)
            for j in range(b.N):
                if j==target: continue
                x=sims[:,j]; mu=float(np.mean(x)); sd=float(np.std(x,ddof=1))
                if not np.isfinite(sd) or sd<=1e-10: return None
                out.append((reg,external_seed,math.log(sd),float(obs[j]-mu)/sd))
    return out

def fit(rows):
    ls=np.asarray([r[2] for r in rows]); z=np.asarray([r[3] for r in rows]); cuts=np.quantile(ls,np.linspace(0,1,NBINS+1)[1:-1])
    gb=float(np.mean(z)); gs=max(float(np.std(z-gb,ddof=1)),.2); pars=[]
    for k in range(NBINS):
        idx=np.digitize(ls,cuts)==k; zz=z[idx]; n=len(zz)
        if n<2: pars.append((gb,gs)); continue
        lb=float(np.mean(zz)); lscl=max(float(np.std(zz-lb,ddof=1)),.2); w=n/(n+SHRINK)
        pars.append((w*lb+(1-w)*gb,w*lscl+(1-w)*gs))
    return cuts,pars

def transform(rows,cal):
    cuts,pars=cal; out=[]
    for reg,seed,ls,z in rows:
        k=int(np.digitize([ls],cuts)[0]); bias,scale=pars[k]; out.append((reg,seed,z,(z-bias)/scale))
    return out

def metrics(rows):
    out={}
    for rg in REGIMES:
        a=np.asarray([[r[2],r[3]] for r in rows if r[0]==rg],float); raw=a[:,0]; cal=a[:,1]
        def one(x): return {'mean':float(np.mean(x)),'rms':float(np.sqrt(np.mean(x*x))),'coverage80':float(np.mean(np.abs(x)<=Z80)),'coverage95':float(np.mean(np.abs(x)<=Z95))}
        out[rg]={'raw':one(raw),'calibrated':one(cal)}
    return out

def coverage_error(v): return abs(v['coverage80']-.8)+abs(v['coverage95']-.95)

def disposition(m):
    raw=np.mean([coverage_error(m[r]['raw']) for r in REGIMES]); cal=np.mean([coverage_error(m[r]['calibrated']) for r in REGIMES])
    improve=(raw-cal)/max(raw,1e-12)
    no_bad=all(coverage_error(m[r]['calibrated'])<=coverage_error(m[r]['raw'])+.02 for r in REGIMES)
    bounds=all(.74<=m[r]['calibrated']['coverage80']<=.86 and .91<=m[r]['calibrated']['coverage95']<=.98 and .85<=m[r]['calibrated']['rms']<=1.15 for r in REGIMES)
    return ('RESPONSE_CALIBRATION_SUPPORTED' if improve>=.20 and no_bad and bounds else 'RESPONSE_CALIBRATION_FALSIFIED'),raw,cal,improve

def gather(ss):
    out=[]
    for x in ss:
        q=cells(x)
        if q is None: return None
        out.extend(q)
    return out

def main():
    mech=gather(seeds(112001,2)); out={'mechanics':{'passed':mech is not None and len(mech)>0}}
    if not out['mechanics']['passed']: out['disposition']='BLOCKED_EXECUTION_MECHANICS'; return out
    trseeds=seeds(112201,64); train=gather(trseeds)
    if train is None: out['disposition']='BLOCKED_EXECUTION_NONFINITE'; return out
    # four-fold world-level cross-fit
    oof=[]
    for fold in range(4):
        hold=set(trseeds[fold::4]); fitrows=[r for r in train if r[1] not in hold]; testrows=[r for r in train if r[1] in hold]
        oof.extend(transform(testrows,fit(fitrows)))
    out['crossfit_training']=metrics(oof)
    cal=fit(train); test=gather(seeds(113201,64))
    if test is None: out['disposition']='BLOCKED_EXECUTION_NONFINITE'; return out
    hm=metrics(transform(test,cal)); d,raw,ce,imp=disposition(hm)
    out['heldout']=hm; out['coverage_error']={'raw_mean':raw,'calibrated_mean':ce,'relative_improvement':imp}; out['disposition']=d; return out

if __name__=='__main__': print(json.dumps(main(),separators=(',',':')))
