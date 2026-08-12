import json, numpy as np
import swarmite_benchmark_v2 as b
import swarmite_exp002_s40_hetero as s40
import swarmite_exp002_s47_breadth as s47
import swarmite_exp002_s60_counterfactual_predictive_residual_state as s60
import swarmite_exp002_s64_constrained_local_posterior_projection as s64

REGIMES=('linear','heteroskedastic'); DRAWS=32

def seeds(start,n):
    out=[]
    for rg in REGIMES: out += [x for x in s60.selected(start,n) if s47.regime(x)==rg][:n]
    return out

def rows(start,n): return [s64.world_base(x) for x in seeds(start,n)]
def mechanics(a,n): return len(a)==2*n and all(sum(r['regime']==rg for r in a)==n for rg in REGIMES) and all(r['spend']<=15 and r['trace_identical'] and r['finite'] and r['mechanics_ok'] for r in a)

def actual(reg,w,seed,target,sp,meta):
    rr=b.rng_for('s69','actual',seed,target,sp)
    if reg=='heteroskedastic': return s40.env(w,rr,1,target,sp,meta['mechanism'])[0]
    return b.env_sample(w,rr,1,target,sp)[0]

def world_stats(external_seed):
    reg,seed,w,c,data,targets,p0,meta=s47.state(external_seed)
    fs,models=b.build_family_models(data,targets); p=b.posterior_from_fs(fs)
    z=[]; c80=[]; c95=[]
    for target in range(b.N):
        for spi,sp in enumerate((-2.0,2.0)):
            rr=b.rng_for('s69','predictive',seed,target,spi)
            sims=np.asarray([b.sim_row_from_posterior(p,models,target,sp,rr) for _ in range(DRAWS)],float)
            obs=np.asarray(actual(reg,w,seed,target,sp,meta),float)
            for j in range(b.N):
                if j==target: continue
                x=sims[:,j]; mu=float(np.mean(x)); sd=float(np.std(x,ddof=1))
                if not np.isfinite(sd) or sd<=1e-10: return None
                zz=(float(obs[j])-mu)/sd; z.append(zz)
                lo80,hi80=np.quantile(x,[.10,.90]); lo95,hi95=np.quantile(x,[.025,.975])
                c80.append(lo80<=obs[j]<=hi80); c95.append(lo95<=obs[j]<=hi95)
    return z,c80,c95

def summarize(z,c80,c95):
    z=np.asarray(z,float)
    return {'n_response_cells':int(len(z)),'mean_standardized_residual':float(np.mean(z)),'rms_standardized_residual':float(np.sqrt(np.mean(z*z))),'coverage80':float(np.mean(c80)),'coverage95':float(np.mean(c95))}

def evaluate(a):
    by={rg:[[],[],[]] for rg in REGIMES}; finite=True
    for r in a:
        q=world_stats(r['external_seed'])
        if q is None: finite=False; continue
        for k in range(3): by[r['regime']][k].extend(q[k])
    out={rg:summarize(*by[rg]) for rg in REGIMES}
    return {'n_worlds':len(a),'draws_per_target_setpoint':DRAWS,'finite':finite,'by_regime':out}

def disposition(e):
    if not e['finite']: return 'BLOCKED_EXECUTION_NONFINITE'
    def ok(v): return abs(v['mean_standardized_residual'])<=.25 and .75<=v['rms_standardized_residual']<=1.35 and .70<=v['coverage80']<=.90 and .88<=v['coverage95']<=.99
    return 'PREDICTIVE_CALIBRATION_SUPPORTED' if all(ok(v) for v in e['by_regime'].values()) else 'PREDICTIVE_MISCALIBRATION_SUPPORTED'

if __name__=='__main__':
    me=rows(111201,2); out={'mechanics':{'passed':mechanics(me,2)},'draws':DRAWS}
    if not out['mechanics']['passed']: out['disposition']='BLOCKED_EXECUTION_MECHANICS'
    else:
        ev=evaluate(rows(111401,64)); out['diagnostic']=ev; out['disposition']=disposition(ev)
    print(json.dumps(out,separators=(',',':')))
